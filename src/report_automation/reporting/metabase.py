from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


def notify_metabase_refresh(client_id: str, month_label: str) -> None:
    """
    Metabase typically refreshes on query. This hook can be used to send
    notifications or trigger external automation if needed.
    """
    logger.info("Metabase refresh requested for %s (%s)", client_id, month_label)
