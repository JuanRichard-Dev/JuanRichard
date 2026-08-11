"""Minimal structured audit logging for production deployments."""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.runtime_config import get_bool, get_setting

LOGGER = logging.getLogger("dashboard_sm_cgr")
if not LOGGER.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(message)s"))
    LOGGER.addHandler(handler)
LOGGER.setLevel(logging.INFO)


def log_event(event: str, payload: dict[str, Any] | None = None) -> None:
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": event,
        **(payload or {}),
    }
    line = json.dumps(record, ensure_ascii=False, default=str)
    LOGGER.info(line)

    if not get_bool("AUDIT_FILE_ENABLED", False):
        return
    path = Path(str(get_setting("AUDIT_FILE_PATH", "logs/audit.jsonl")))
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")
    except OSError:
        LOGGER.exception("Não foi possível gravar o audit log em arquivo.")
