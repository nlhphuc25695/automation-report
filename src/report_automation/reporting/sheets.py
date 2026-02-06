from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Dict, Iterable, List

from googleapiclient.discovery import build

from report_automation.models import AdsDailyRow, MonthlySummaryRow
from report_automation.reporting.sheets_templates import create_sheet_from_objective, seed_kpi_sections
from report_automation.templates import get_template


@dataclass
class SheetResult:
    spreadsheet_id: str
    spreadsheet_url: str


def create_monthly_sheet(
    drive_folder_id: str,
    template_id: str,
    title: str,
    objective: str,
) -> SheetResult:
    if os.getenv("DRY_RUN") == "1":
        return SheetResult(spreadsheet_id="DRY_RUN", spreadsheet_url="")

    if not template_id:
        template = get_template(objective)
        spreadsheet_id = create_sheet_from_objective(title, template)
        seed_kpi_sections(spreadsheet_id, template)
        if drive_folder_id:
            drive = build("drive", "v3")
            drive.files().update(
                fileId=spreadsheet_id,
                addParents=drive_folder_id,
                fields="id, webViewLink",
            ).execute()
        sheets = build("sheets", "v4")
        spreadsheet = sheets.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
        return SheetResult(
            spreadsheet_id=spreadsheet_id,
            spreadsheet_url=spreadsheet.get("spreadsheetUrl", ""),
        )

    drive = build("drive", "v3")
    body = {
        "name": title,
        "parents": [drive_folder_id] if drive_folder_id else [],
    }
    copied = drive.files().copy(fileId=template_id, body=body).execute()
    return SheetResult(
        spreadsheet_id=copied["id"],
        spreadsheet_url=copied.get("webViewLink", ""),
    )


def update_sheet_data(
    spreadsheet_id: str,
    summary_rows: List[MonthlySummaryRow],
    daily_rows: List[AdsDailyRow],
) -> None:
    if os.getenv("DRY_RUN") == "1":
        return

    sheets = build("sheets", "v4")
    values: List[Dict[str, object]] = []

    values.append(
        {
            "range": "Summary!A1",
            "values": _summary_table(summary_rows),
        }
    )

    platform_tables = _platform_tables(summary_rows)
    values.extend(platform_tables)

    values.append(
        {
            "range": "Raw!A1",
            "values": _raw_table(daily_rows),
        }
    )

    body = {"valueInputOption": "RAW", "data": values}
    sheets.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheet_id, body=body
    ).execute()


def _summary_table(rows: List[MonthlySummaryRow]) -> List[List[object]]:
    header = [
        "Platform",
        "Spend",
        "Impressions",
        "Clicks",
        "CTR",
        "CPC",
        "Conversions",
        "CPA",
        "ROAS",
    ]
    data = [header]
    for row in rows:
        data.append(
            [
                row.platform,
                row.spend,
                row.impressions,
                row.clicks,
                row.ctr,
                row.cpc,
                row.conversions,
                row.cpa,
                row.roas,
            ]
        )
    return data


def _platform_tables(rows: List[MonthlySummaryRow]) -> List[Dict[str, object]]:
    tables: List[Dict[str, object]] = []
    for platform in ["meta", "google", "tiktok"]:
        platform_rows = [row for row in rows if row.platform == platform]
        if not platform_rows:
            continue
        sheet_name = f"Platform {platform.capitalize()}"
        tables.append({"range": f"{sheet_name}!A1", "values": _summary_table(platform_rows)})
    return tables


def _raw_table(rows: List[AdsDailyRow]) -> List[List[object]]:
    header = [
        "Date",
        "Platform",
        "Account ID",
        "Campaign ID",
        "Adset ID",
        "Ad ID",
        "Spend",
        "Impressions",
        "Clicks",
        "Conversions",
        "Revenue",
        "Client ID",
        "Currency",
    ]
    data = [header]
    for row in rows:
        data.append(
            [
                row.date.isoformat(),
                row.platform,
                row.account_id,
                row.campaign_id,
                row.adset_id or "",
                row.ad_id or "",
                row.spend,
                row.impressions,
                row.clicks,
                row.conversions,
                row.revenue,
                row.client_id,
                row.currency,
            ]
        )
    return data
