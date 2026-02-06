from __future__ import annotations

import os
from datetime import date
from typing import Iterable, List, Optional

from report_automation.connectors.adapter import (
    AdapterContext,
    AdapterNotConfiguredError,
    demo_rows,
    date_range_payload,
    require_value,
)
from report_automation.connectors.base import AdsConnector
from report_automation.credentials import MetaCredentials
from report_automation.models import AdsDailyRow


class MetaAdsConnector(AdsConnector):
    platform = "meta"

    def __init__(self, credentials: Optional[MetaCredentials]) -> None:
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
            raise AdapterNotConfiguredError("Missing Meta Ads credentials.")
        require_value(self.credentials.app_id, "Meta app_id")
        require_value(self.credentials.app_secret, "Meta app_secret")
        require_value(self.credentials.access_token, "Meta access_token")

        # TODO: Replace this skeleton with real Meta Marketing API calls.
        # Suggested endpoint: /act_{ad_account_id}/insights with fields + time_range
        request_payload = self._build_request_payload(context)
        raise NotImplementedError(
            f"Meta Ads adapter skeleton ready. Build request like: {request_payload}"
        )

    def _build_request_payload(self, context: AdapterContext) -> dict:
        return {
            "level": "campaign",
            "fields": [
                "date_start",
                "date_stop",
                "account_id",
                "campaign_id",
                "spend",
                "impressions",
                "clicks",
                "actions",
                "action_values",
            ],
            "time_range": date_range_payload(context.start_date, context.end_date),
            "time_increment": 1,
        }
