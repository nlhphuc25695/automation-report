from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from typing import Dict, List

from report_automation.models import AdsDailyRow


@dataclass
class AdapterContext:
    client_id: str
    account_ids: List[str]
    start_date: date
    end_date: date
    currency: str


class AdapterNotConfiguredError(RuntimeError):
    pass


def require_value(value: str, label: str) -> None:
    if not value:
        raise AdapterNotConfiguredError(f"Missing {label}. Fill config/ads_credentials.yaml.")


def date_range_payload(start_date: date, end_date: date) -> Dict[str, str]:
    return {
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
    }


def standard_metrics() -> List[str]:
    return [
        "spend",
        "impressions",
        "clicks",
        "conversions",
        "revenue",
    ]


def demo_rows(context: AdapterContext, platform: str, account_id: str) -> List[AdsDailyRow]:
    rows: List[AdsDailyRow] = []
    current = context.start_date
    while current < context.end_date:
        base = (current.day % 7) + 1
        spend = float(100 * base)
        impressions = 1000 * base
        clicks = 50 * base
        conversions = float(5 * base)
        revenue = float(300 * base)
        rows.append(
            AdsDailyRow(
                date=current,
                platform=platform,
                account_id=account_id,
                campaign_id=f"camp_{platform}_{base}",
                adset_id=f"adset_{platform}_{base}",
                ad_id=f"ad_{platform}_{base}",
                spend=spend,
                impressions=impressions,
                clicks=clicks,
                conversions=conversions,
                revenue=revenue,
                client_id=context.client_id,
                currency=context.currency,
            )
        )
        current += timedelta(days=1)
    return rows
