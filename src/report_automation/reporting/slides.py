from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Dict, List

from googleapiclient.discovery import build

from report_automation.models import MonthlySummaryRow
from report_automation.reporting.slides_templates import create_slides_from_objective
from report_automation.templates import get_template


@dataclass
class SlidesResult:
    presentation_id: str
    presentation_url: str


def create_monthly_slides(
    drive_folder_id: str,
    template_id: str,
    title: str,
    replacements: Dict[str, str],
    objective: str,
) -> SlidesResult:
    if os.getenv("DRY_RUN") == "1":
        return SlidesResult(presentation_id="DRY_RUN", presentation_url="")

    if not template_id:
        template = get_template(objective)
        presentation_id = create_slides_from_objective(title, template)
        if drive_folder_id:
            drive = build("drive", "v3")
            drive.files().update(
                fileId=presentation_id,
                addParents=drive_folder_id,
                fields="id, webViewLink",
            ).execute()
        slides = build("slides", "v1")
        presentation = slides.presentations().get(presentationId=presentation_id).execute()
        drive = build("drive", "v3")
        drive_meta = drive.files().get(fileId=presentation_id, fields="webViewLink").execute()
        return SlidesResult(
            presentation_id=presentation_id,
            presentation_url=drive_meta.get("webViewLink", ""),
        )

    drive = build("drive", "v3")
    body = {
        "name": title,
        "parents": [drive_folder_id] if drive_folder_id else [],
    }
    copied = drive.files().copy(fileId=template_id, body=body).execute()

    slides = build("slides", "v1")
    requests = []
    for key, value in replacements.items():
        requests.append(
            {
                "replaceAllText": {
                    "containsText": {"text": key, "matchCase": True},
                    "replaceText": value,
                }
            }
        )
    if requests:
        slides.presentations().batchUpdate(
            presentationId=copied["id"], body={"requests": requests}
        ).execute()

    return SlidesResult(
        presentation_id=copied["id"],
        presentation_url=copied.get("webViewLink", ""),
    )


def build_slide_replacements(
    month_label: str,
    summary_rows: List[MonthlySummaryRow],
) -> Dict[str, str]:
    total_spend = sum(row.spend for row in summary_rows)
    total_impressions = sum(row.impressions for row in summary_rows)
    total_clicks = sum(row.clicks for row in summary_rows)
    total_conversions = sum(row.conversions for row in summary_rows)

    return {
        "{{month}}": month_label,
        "{{total_spend}}": f"{total_spend:,.0f}",
        "{{total_impressions}}": f"{total_impressions:,}",
        "{{total_clicks}}": f"{total_clicks:,}",
        "{{total_conversions}}": f"{total_conversions:,.0f}",
    }
