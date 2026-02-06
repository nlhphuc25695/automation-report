from __future__ import annotations

from typing import Dict, List

from googleapiclient.discovery import build

from report_automation.templates import ObjectiveTemplate


def create_slides_from_objective(title: str, template: ObjectiveTemplate) -> str:
    slides = build("slides", "v1")
    presentation = slides.presentations().create(body={"title": title}).execute()
    presentation_id = presentation["presentationId"]

    requests: List[Dict[str, object]] = []
    for idx, slide_title in enumerate(template.slide_titles, start=1):
        slide_id = f"slide_{idx}"
        title_id = f"title_{idx}"
        body_id = f"body_{idx}"
        requests.append(
            {
                "createSlide": {
                    "objectId": slide_id,
                    "slideLayoutReference": {"predefinedLayout": "TITLE_AND_BODY"},
                    "placeholderIdMappings": [
                        {"layoutPlaceholder": {"type": "TITLE", "index": 0}, "objectId": title_id},
                        {"layoutPlaceholder": {"type": "BODY", "index": 0}, "objectId": body_id},
                    ],
                }
            }
        )
        requests.append(
            {
                "insertText": {
                    "objectId": title_id,
                    "insertionIndex": 0,
                    "text": slide_title,
                }
            }
        )
        requests.append(
            {
                "insertText": {
                    "objectId": body_id,
                    "insertionIndex": 0,
                    "text": "Insights / Key points here",
                }
            }
        )

    if requests:
        slides.presentations().batchUpdate(
            presentationId=presentation_id,
            body={"requests": requests},
        ).execute()

    return presentation_id
