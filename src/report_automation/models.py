from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class AdsDailyRow:
    date: date
    platform: str
    account_id: str
    campaign_id: str
    adset_id: Optional[str]
    ad_id: Optional[str]
    spend: float
    impressions: int
    clicks: int
    conversions: float
    revenue: float
    client_id: str
    currency: str


@dataclass
class MonthlySummaryRow:
    month: date
    platform: str
    client_id: str
    spend: float
    impressions: int
    clicks: int
    ctr: float
    cpc: float
    conversions: float
    cpa: float
    roas: float
