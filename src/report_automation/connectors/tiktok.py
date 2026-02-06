from __future__ import annotations

import os
from datetime import date
from typing import Iterable, List, Optional

from report_automation.connectors.adapter import (
    AdapterContext,
    AdapterNotConfiguredError,
    date_range_payload,
    demo_rows,
    require_value,
)
from report_automation.connectors.base import AdsConnector
from report_automation.credentials import TikTokCredentials
from report_automation.models import AdsDailyRow


class TikTokAdsConnector(AdsConnector):
    platform = "tiktok"

    def __init__(self, credentials: Optional[TikTokCredentials]) -> None:
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
            raise AdapterNotConfiguredError("Missing TikTok Ads credentials.")
        require_value(self.credentials.access_token, "TikTok access_token")

        # TODO: Replace this skeleton with real TikTok Ads API calls.
        request_payload = self._build_request_payload(context)
        raise NotImplementedError(
            f"TikTok Ads adapter skeleton ready. Build request like: {request_payload}"
        )

    def _build_request_payload(self, context: AdapterContext) -> dict:
        return {
            "advertiser_ids": context.account_ids,
            "report_type": "BASIC",
            "data_level": "AUCTION_CAMPAIGN",
            "dimensions": ["campaign_id", "stat_time_day"],
            "metrics": ["spend", "impressions", "clicks", "conversions", "total_complete_payment_rate"],
            "filtering": {"time_range": date_range_payload(context.start_date, context.end_date)},
        }
