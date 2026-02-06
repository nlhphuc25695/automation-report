from __future__ import annotations

from typing import List

from googleapiclient.discovery import build

from report_automation.templates import ObjectiveTemplate


def create_sheet_from_objective(title: str, template: ObjectiveTemplate) -> str:
    sheets = build("sheets", "v4")
    spreadsheet = {
        "properties": {"title": title},
        "sheets": [{"properties": {"title": tab}} for tab in template.sheet_tabs],
    }
    created = sheets.spreadsheets().create(body=spreadsheet).execute()
    return created["spreadsheetId"]


def seed_kpi_sections(spreadsheet_id: str, template: ObjectiveTemplate) -> None:
    sheets = build("sheets", "v4")
    summary_rows: List[List[object]] = [
        ["KPI", "Value"],
    ]
    for kpi in template.kpis:
        summary_rows.append([kpi, ""])

    highlights_rows: List[List[object]] = [["Highlights"], *[[item] for item in template.highlights]]

    requests = [
        {
            "range": "Summary!A1",
            "values": summary_rows,
        },
        {
            "range": "Summary!D1",
            "values": highlights_rows,
        },
    ]

    body = {"valueInputOption": "RAW", "data": requests}
    sheets.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()
