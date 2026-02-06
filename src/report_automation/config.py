from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

import yaml


@dataclass
class BigQueryConfig:
    project_id: str
    dataset: str


@dataclass
class Settings:
    currency: str
    locale: str
    timezone: str
    bigquery: BigQueryConfig


@dataclass
class AdsAccounts:
    meta: List[str]
    google: List[str]
    tiktok: List[str]


@dataclass
class ClientConfig:
    client_id: str
    name: str
    drive_folder_id: str
    sheet_template_id: str
    slides_template_id: str
    objective: str
    ad_accounts: AdsAccounts


@dataclass
class AppConfig:
    settings: Settings
    clients: List[ClientConfig]


def _load_ads_accounts(payload: Dict) -> AdsAccounts:
    return AdsAccounts(
        meta=list(payload.get("meta", []) or []),
        google=list(payload.get("google", []) or []),
        tiktok=list(payload.get("tiktok", []) or []),
    )


def load_config(path: str | Path) -> AppConfig:
    path = Path(path)
    with path.open("r", encoding="utf-8") as handle:
        raw = yaml.safe_load(handle)

    if not raw:
        raise ValueError("Config file is empty")

    settings_raw = raw.get("settings") or {}
    bq_raw = settings_raw.get("bigquery") or {}
    settings = Settings(
        currency=settings_raw.get("currency", "VND"),
        locale=settings_raw.get("locale", "vi-VN"),
        timezone=settings_raw.get("timezone", "Asia/Ho_Chi_Minh"),
        bigquery=BigQueryConfig(
            project_id=bq_raw.get("project_id", ""),
            dataset=bq_raw.get("dataset", "ads_reporting"),
        ),
    )

    clients = []
    for client in raw.get("clients", []) or []:
        clients.append(
            ClientConfig(
                client_id=client["client_id"],
                name=client.get("name", client["client_id"]),
                drive_folder_id=client.get("drive_folder_id", ""),
                sheet_template_id=client.get("sheet_template_id", ""),
                slides_template_id=client.get("slides_template_id", ""),
                objective=client.get("objective", "ecom"),
                ad_accounts=_load_ads_accounts(client.get("ad_accounts") or {}),
            )
        )

    if not clients:
        raise ValueError("Config must contain at least one client")

    return AppConfig(settings=settings, clients=clients)
