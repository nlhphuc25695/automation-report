from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional

import yaml


@dataclass
class MetaCredentials:
    app_id: str
    app_secret: str
    access_token: str


@dataclass
class GoogleAdsCredentials:
    developer_token: str
    client_id: str
    client_secret: str
    refresh_token: str
    login_customer_id: str


@dataclass
class TikTokCredentials:
    access_token: str
    advertiser_id: str


@dataclass
class AdsCredentials:
    meta: MetaCredentials
    google_ads: GoogleAdsCredentials
    tiktok: TikTokCredentials


def load_credentials(path: str | Path) -> AdsCredentials:
    path = Path(path)
    with path.open("r", encoding="utf-8") as handle:
        raw = yaml.safe_load(handle) or {}

    meta_raw = raw.get("meta") or {}
    google_raw = raw.get("google_ads") or {}
    tiktok_raw = raw.get("tiktok") or {}

    return AdsCredentials(
        meta=MetaCredentials(
            app_id=meta_raw.get("app_id", ""),
            app_secret=meta_raw.get("app_secret", ""),
            access_token=meta_raw.get("access_token", ""),
        ),
        google_ads=GoogleAdsCredentials(
            developer_token=google_raw.get("developer_token", ""),
            client_id=google_raw.get("client_id", ""),
            client_secret=google_raw.get("client_secret", ""),
            refresh_token=google_raw.get("refresh_token", ""),
            login_customer_id=google_raw.get("login_customer_id", ""),
        ),
        tiktok=TikTokCredentials(
            access_token=tiktok_raw.get("access_token", ""),
            advertiser_id=tiktok_raw.get("advertiser_id", ""),
        ),
    )
