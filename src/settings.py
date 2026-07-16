"""External dashboard settings with safe defaults.

Business targets and presentation parameters can be changed in
``dashboard_settings.json`` without editing Python source files. Missing or
invalid values fall back to validated defaults.
"""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SETTINGS_PATH = PROJECT_ROOT / "dashboard_settings.json"

DEFAULT_SETTINGS: dict[str, Any] = {
    "targets": {
        "health_score": 80.0,
        "periodicos_pct": 95.0,
        "faltas_pct_max": 5.0,
        "absenteismo_monthly_max": 500.0,
        "mental_cases_max": 10.0,
        "variation_warning_pct": 15.0,
    },
    "analytics": {
        "moving_average_window": 3,
        "forecast_months": 2,
        "forecast_min_points": 3,
        "default_daily_absence_cost": 350.0,
    },
    "data": {"stale_after_days": 35},
    "ui": {"max_alerts": 4, "table_height": 420},
}


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def _coerce_number(value: Any, default: float, *, minimum: float | None = None) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return float(default)
    if minimum is not None and number < minimum:
        return float(default)
    return number


def load_dashboard_settings(path: Path | None = None) -> dict[str, Any]:
    """Load and validate the optional JSON settings file."""
    settings_path = path or SETTINGS_PATH
    loaded: dict[str, Any] = {}
    if settings_path.exists():
        try:
            parsed = json.loads(settings_path.read_text(encoding="utf-8"))
            if isinstance(parsed, dict):
                loaded = parsed
        except (OSError, json.JSONDecodeError):
            loaded = {}

    settings = _deep_merge(DEFAULT_SETTINGS, loaded)

    targets = settings["targets"]
    for key, default in DEFAULT_SETTINGS["targets"].items():
        targets[key] = _coerce_number(targets.get(key), default, minimum=0.0)

    analytics = settings["analytics"]
    analytics["moving_average_window"] = int(
        _coerce_number(
            analytics.get("moving_average_window"),
            DEFAULT_SETTINGS["analytics"]["moving_average_window"],
            minimum=1.0,
        )
    )
    analytics["forecast_months"] = int(
        _coerce_number(
            analytics.get("forecast_months"),
            DEFAULT_SETTINGS["analytics"]["forecast_months"],
            minimum=0.0,
        )
    )
    analytics["forecast_min_points"] = int(
        _coerce_number(
            analytics.get("forecast_min_points"),
            DEFAULT_SETTINGS["analytics"]["forecast_min_points"],
            minimum=2.0,
        )
    )
    analytics["default_daily_absence_cost"] = _coerce_number(
        analytics.get("default_daily_absence_cost"),
        DEFAULT_SETTINGS["analytics"]["default_daily_absence_cost"],
        minimum=0.0,
    )

    settings["data"]["stale_after_days"] = int(
        _coerce_number(
            settings["data"].get("stale_after_days"),
            DEFAULT_SETTINGS["data"]["stale_after_days"],
            minimum=1.0,
        )
    )
    settings["ui"]["max_alerts"] = int(
        _coerce_number(
            settings["ui"].get("max_alerts"),
            DEFAULT_SETTINGS["ui"]["max_alerts"],
            minimum=1.0,
        )
    )
    settings["ui"]["table_height"] = int(
        _coerce_number(
            settings["ui"].get("table_height"),
            DEFAULT_SETTINGS["ui"]["table_height"],
            minimum=200.0,
        )
    )
    return settings
