from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class MonthWindow:
    start: date
    end: date
    month_label: str


def month_window(target_date: date) -> MonthWindow:
    start = target_date.replace(day=1)
    if start.month == 12:
        end = date(start.year + 1, 1, 1)
    else:
        end = date(start.year, start.month + 1, 1)
    return MonthWindow(start=start, end=end, month_label=start.strftime("%Y-%m"))


def previous_month_window(reference_date: date) -> MonthWindow:
    if reference_date.month == 1:
        prev_month = date(reference_date.year - 1, 12, 1)
    else:
        prev_month = date(reference_date.year, reference_date.month - 1, 1)
    return month_window(prev_month)
