from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import date, datetime
from typing import List, Optional
from zoneinfo import ZoneInfo

from report_automation.config import AppConfig
from report_automation.connectors.google_ads import GoogleAdsConnector
from report_automation.connectors.meta import MetaAdsConnector
from report_automation.connectors.tiktok import TikTokAdsConnector
from report_automation.credentials import AdsCredentials, load_credentials
from report_automation.models import AdsDailyRow, MonthlySummaryRow
from report_automation.reporting.metabase import notify_metabase_refresh
from report_automation.reporting.sheets import create_monthly_sheet, update_sheet_data
from report_automation.reporting.slides import build_slide_replacements, create_monthly_slides
from report_automation.storage.bigquery import BigQueryConfig, BigQueryStore
from report_automation.summary import summarize_month
from report_automation.time_windows import month_window, previous_month_window

logger = logging.getLogger(__name__)


@dataclass
class JobResult:
    client_id: str
    status: str
    daily_rows: int
    summary_rows: int
    sheet_url: str
    slides_url: str
    errors: List[str]


def _current_date_in_tz(timezone: str) -> date:
    now = datetime.now(ZoneInfo(timezone))
    return now.date()


def parse_target_month(value: Optional[str]) -> Optional[date]:
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m").date().replace(day=1)
    except ValueError as exc:
        raise ValueError("target month must be in YYYY-MM format") from exc


def run_monthly_job(
    config: AppConfig,
    target_month: Optional[str],
    credentials_path: Optional[str] = None,
) -> List[JobResult]:
    timezone = config.settings.timezone
    target_date = parse_target_month(target_month)
    if target_date is None:
        window = previous_month_window(_current_date_in_tz(timezone))
    else:
        window = month_window(target_date)

    logger.info("Running job for month %s (%s -> %s)", window.month_label, window.start, window.end)

    store = BigQueryStore(
        BigQueryConfig(
            project_id=config.settings.bigquery.project_id,
            dataset=config.settings.bigquery.dataset,
        )
    )
    store.ensure_dataset_and_tables()

    results: List[JobResult] = []

    credentials: Optional[AdsCredentials] = None
    if credentials_path:
        credentials = load_credentials(credentials_path)

    connectors = [
        MetaAdsConnector(credentials.meta if credentials else None),
        GoogleAdsConnector(credentials.google_ads if credentials else None),
        TikTokAdsConnector(credentials.tiktok if credentials else None),
    ]

    for client in config.clients:
        daily_rows: List[AdsDailyRow] = []
        errors: List[str] = []

        for connector in connectors:
            account_ids = getattr(client.ad_accounts, connector.platform, [])
            if not account_ids:
                continue
            try:
                rows = connector.fetch_daily_rows(
                    client_id=client.client_id,
                    account_ids=account_ids,
                    start_date=window.start,
                    end_date=window.end,
                    currency=config.settings.currency,
                )
                daily_rows.extend(list(rows))
            except Exception as exc:
                errors.append(f"{connector.platform}: {exc}")
                logger.exception(
                    "Connector %s failed for client %s: %s",
                    connector.platform,
                    client.client_id,
                    exc,
                )
                continue

        summaries: List[MonthlySummaryRow] = summarize_month(
            rows=daily_rows,
            month_start=window.start,
            client_id=client.client_id,
        )

        try:
            store.reset_client_month(client.client_id, window.start, window.end)
            store.load_daily_rows(daily_rows)
            store.load_monthly_summary(summaries)
        except Exception as exc:
            errors.append(f"bigquery: {exc}")
            logger.exception("BigQuery load failed for client %s: %s", client.client_id, exc)

        sheet_url = ""
        sheet_title = f"{client.name} Report {window.month_label}"
        try:
            sheet = create_monthly_sheet(
                drive_folder_id=client.drive_folder_id,
                template_id=client.sheet_template_id,
                title=sheet_title,
                objective=client.objective,
            )
            update_sheet_data(sheet.spreadsheet_id, summaries, daily_rows)
            sheet_url = sheet.spreadsheet_url
        except Exception as exc:
            errors.append(f"sheets: {exc}")
            logger.exception("Sheets update failed for client %s: %s", client.client_id, exc)

        slides_url = ""
        slide_title = f"{client.name} Slides {window.month_label}"
        replacements = build_slide_replacements(window.month_label, summaries)
        try:
            slides = create_monthly_slides(
                drive_folder_id=client.drive_folder_id,
                template_id=client.slides_template_id,
                title=slide_title,
                replacements=replacements,
                objective=client.objective,
            )
            slides_url = slides.presentation_url
        except Exception as exc:
            errors.append(f"slides: {exc}")
            logger.exception("Slides update failed for client %s: %s", client.client_id, exc)

        notify_metabase_refresh(client.client_id, window.month_label)

        status = "success"
        if errors and daily_rows:
            status = "partial"
        elif errors and not daily_rows:
            status = "failed"

        results.append(
            JobResult(
                client_id=client.client_id,
                status=status,
                daily_rows=len(daily_rows),
                summary_rows=len(summaries),
                sheet_url=sheet_url,
                slides_url=slides_url,
                errors=errors,
            )
        )

    return results
