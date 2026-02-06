from __future__ import annotations

import os
from datetime import date
from typing import Iterable, List, Optional

from report_automation.connectors.adapter import (
    AdapterContext,
    AdapterNotConfiguredError,
    demo_rows,
    require_value,
)
from report_automation.connectors.base import AdsConnector
from report_automation.credentials import GoogleAdsCredentials
from report_automation.models import AdsDailyRow


class GoogleAdsConnector(AdsConnector):
    platform = "google"

    def __init__(self, credentials: Optional[GoogleAdsCredentials]) -> None:
        self.credentials = credentials

    def fetch_daily_rows(
        self,
        client_id: str,
        account_ids: List[str],
        start_date: date,
        end_date: date,
        currency: str,
    ) -> Iterable[AdsDailyRow]:
        context = AdapterContext(
            client_id=client_id,
            account_ids=account_ids,
            start_date=start_date,
            end_date=end_date,
            currency=currency,
        )
        if os.getenv("DRY_RUN") == "1":
            return []
        if os.getenv("DEMO_DATA") == "1":
            demo: List[AdsDailyRow] = []
            for account_id in account_ids:
                demo.extend(demo_rows(context, self.platform, account_id))
            return demo
        if not self.credentials:
            raise AdapterNotConfiguredError("Missing Google Ads credentials.")
        require_value(self.credentials.developer_token, "Google Ads developer_token")
        require_value(self.credentials.client_id, "Google Ads client_id")
        require_value(self.credentials.client_secret, "Google Ads client_secret")
        require_value(self.credentials.refresh_token, "Google Ads refresh_token")

        # TODO: Replace this skeleton with real Google Ads API calls.
        # Suggested: Google Ads Query Language (GAQL) for campaign stats.
        query = self._build_gaql_query(context)
        raise NotImplementedError(
            f"Google Ads adapter skeleton ready. GAQL example: {query}"
        )

    def _build_gaql_query(self, context: AdapterContext) -> str:
        start = context.start_date.isoformat()
        end = context.end_date.isoformat()
        return (
            "SELECT "
            "segments.date, "
            "customer.id, "
            "campaign.id, "
            "metrics.cost_micros, "
            "metrics.impressions, "
            "metrics.clicks, "
            "metrics.conversions, "
            "metrics.conversions_value "
            "FROM campaign "
            f"WHERE segments.date >= '{start}' AND segments.date < '{end}'"
        )
