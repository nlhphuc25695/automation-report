from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class ObjectiveTemplate:
    objective: str
    sheet_tabs: List[str]
    slide_titles: List[str]
    kpis: List[str]
    highlights: List[str]


TEMPLATES: Dict[str, ObjectiveTemplate] = {
    "ecom": ObjectiveTemplate(
        objective="ecom",
        sheet_tabs=["Summary", "Platform Meta", "Platform Google", "Platform TikTok", "Top Products", "Raw"],
        slide_titles=[
            "Monthly Performance Overview",
            "Revenue & ROAS",
            "Top Campaigns",
            "Top Products",
            "Next Month Focus",
        ],
        kpis=["Spend", "Revenue", "ROAS", "Orders", "AOV", "CPA"],
        highlights=["Best ROAS campaign", "Top product by revenue", "Highest AOV segment"],
    ),
    "lead": ObjectiveTemplate(
        objective="lead",
        sheet_tabs=["Summary", "Platform Meta", "Platform Google", "Platform TikTok", "Lead Quality", "Raw"],
        slide_titles=[
            "Monthly Lead Overview",
            "Cost per Lead",
            "Lead Quality",
            "Top Campaigns",
            "Next Month Focus",
        ],
        kpis=["Spend", "Leads", "CPL", "Qualified Leads", "Conversion Rate"],
        highlights=["Lowest CPL campaign", "Highest quality source", "Lead drop-offs"],
    ),
    "branding": ObjectiveTemplate(
        objective="branding",
        sheet_tabs=["Summary", "Platform Meta", "Platform Google", "Platform TikTok", "Reach & Frequency", "Raw"],
        slide_titles=[
            "Monthly Awareness Overview",
            "Reach & Frequency",
            "Video Performance",
            "Top Creative",
            "Next Month Focus",
        ],
        kpis=["Spend", "Reach", "Impressions", "Frequency", "Video Views", "CPM"],
        highlights=["Best performing creative", "Reach efficiency", "View rate"],
    ),
    "social": ObjectiveTemplate(
        objective="social",
        sheet_tabs=["Summary", "Platform Meta", "Platform Google", "Platform TikTok", "Engagement", "Raw"],
        slide_titles=[
            "Monthly Social Overview",
            "Engagement Metrics",
            "Top Content",
            "Community Growth",
            "Next Month Focus",
        ],
        kpis=["Spend", "Engagements", "ER", "Clicks", "Video Views", "CPC"],
        highlights=["Top engagement post", "Best CTR campaign", "Follower growth"],
    ),
}


def get_template(objective: str) -> ObjectiveTemplate:
    key = (objective or "ecom").strip().lower()
    if key not in TEMPLATES:
        key = "ecom"
    return TEMPLATES[key]
