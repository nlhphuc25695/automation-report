from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date
from typing import Iterable, List

from report_automation.models import AdsDailyRow


class AdsConnector(ABC):
    platform: str

    @abstractmethod
    def fetch_daily_rows(
        self,
        client_id: str,
        account_ids: List[str],
        start_date: date,
        end_date: date,
        currency: str,
    ) -> Iterable[AdsDailyRow]:
        raise NotImplementedError
