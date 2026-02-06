from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Dict, List

import yaml


def _prompt(label: str, default: str | None = None) -> str:
    suffix = f" [{default}]" if default else ""
    value = input(f"{label}{suffix}: ").strip()
    return value or (default or "")


def _prompt_list(label: str) -> List[str]:
    raw = input(f"{label} (comma separated): ").strip()
    if not raw:
        return []
    return [item.strip() for item in raw.split(",") if item.strip()]


def build_config_interactive() -> Dict:
    print("=== Report Automation Config Form ===")
    settings = {
        "currency": _prompt("Currency", "VND"),
        "locale": _prompt("Locale", "vi-VN"),
        "timezone": _prompt("Timezone", "Asia/Ho_Chi_Minh"),
        "bigquery": {
            "project_id": _prompt("GCP Project ID"),
            "dataset": _prompt("BigQuery Dataset", "ads_reporting"),
        },
    }

    clients: List[Dict] = []
    more = "y"
    while more.lower() == "y":
        client = {
            "client_id": _prompt("Client ID"),
            "name": _prompt("Client Name"),
            "objective": _prompt("Objective (ecom|lead|branding|social)", "ecom"),
            "drive_folder_id": _prompt("Drive Folder ID"),
            "sheet_template_id": _prompt("Sheet Template ID (optional)", ""),
            "slides_template_id": _prompt("Slides Template ID (optional)", ""),
            "ad_accounts": {
                "meta": _prompt_list("Meta Account IDs"),
                "google": _prompt_list("Google Ads Customer IDs"),
                "tiktok": _prompt_list("TikTok Account IDs"),
            },
        }
        clients.append(client)
        more = _prompt("Add another client? (y/n)", "n")

    return {"settings": settings, "clients": clients}


def write_config(config: Dict, output_path: str | Path) -> None:
    output_path = Path(output_path)
    with output_path.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(config, handle, sort_keys=False, allow_unicode=True)
