from __future__ import annotations

from collections import defaultdict
from datetime import date
from typing import Iterable, List

from report_automation.models import AdsDailyRow, MonthlySummaryRow


def summarize_month(
    rows: Iterable[AdsDailyRow],
    month_start: date,
    client_id: str,
) -> List[MonthlySummaryRow]:
    grouped = defaultdict(lambda: {
        "spend": 0.0,
        "impressions": 0,
        "clicks": 0,
        "conversions": 0.0,
        "revenue": 0.0,
    })

    for row in rows:
        bucket = grouped[row.platform]
        bucket["spend"] += row.spend
        bucket["impressions"] += row.impressions
        bucket["clicks"] += row.clicks
        bucket["conversions"] += row.conversions
        bucket["revenue"] += row.revenue

    summaries: List[MonthlySummaryRow] = []
    for platform, agg in grouped.items():
        impressions = agg["impressions"]
        clicks = agg["clicks"]
        spend = agg["spend"]
        conversions = agg["conversions"]
        revenue = agg["revenue"]

        ctr = (clicks / impressions) if impressions else 0.0
        cpc = (spend / clicks) if clicks else 0.0
        cpa = (spend / conversions) if conversions else 0.0
        roas = (revenue / spend) if spend else 0.0

        summaries.append(
            MonthlySummaryRow(
                month=month_start,
                platform=platform,
                client_id=client_id,
                spend=spend,
                impressions=impressions,
                clicks=clicks,
                ctr=ctr,
                cpc=cpc,
                conversions=conversions,
                cpa=cpa,
                roas=roas,
            )
        )

    return summaries
