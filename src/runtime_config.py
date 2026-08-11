"""Runtime configuration helpers for local and cloud deployments.

Values may come from environment variables or Streamlit secrets. Secrets take
precedence when both sources define the same key. No credential is committed to
the repository.
"""

from __future__ import annotations

import os
from typing import Any

try:
    import streamlit as st
except ModuleNotFoundError:  # pragma: no cover - diagnostics without Streamlit
    st = None  # type: ignore[assignment]


def _secret_value(key: str) -> Any:
    if st is None:
        return None
    try:
        if key in st.secrets:
            return st.secrets[key]
    except Exception:
        return None
    return None


def get_setting(key: str, default: Any = None) -> Any:
    """Read a scalar setting from Streamlit secrets or the environment."""
    secret = _secret_value(key)
    if secret not in (None, ""):
        return secret
    return os.getenv(key, default)


def get_bool(key: str, default: bool = False) -> bool:
    value = get_setting(key, default)
    if isinstance(value, bool):
        return value
    return str(value).strip().casefold() in {"1", "true", "yes", "sim", "on"}


def get_csv(key: str, default: list[str] | None = None) -> list[str]:
    value = get_setting(key, None)
    if value is None:
        return list(default or [])
    if isinstance(value, (list, tuple, set)):
        return [str(item).strip() for item in value if str(item).strip()]
    return [item.strip() for item in str(value).split(",") if item.strip()]


def get_section(name: str) -> dict[str, Any]:
    """Return a Streamlit secrets section when it exists."""
    if st is None:
        return {}
    try:
        section = st.secrets.get(name, {})
        return dict(section) if section else {}
    except Exception:
        return {}


def get_int(key: str, default: int = 0, *, minimum: int | None = None) -> int:
    """Read an integer setting with safe fallback and optional minimum."""
    value = get_setting(key, default)
    try:
        result = int(value)
    except (TypeError, ValueError):
        result = int(default)
    if minimum is not None:
        result = max(minimum, result)
    return result


def get_float(
    key: str,
    default: float = 0.0,
    *,
    minimum: float | None = None,
) -> float:
    """Read a floating-point setting with safe fallback."""
    value = get_setting(key, default)
    try:
        result = float(value)
    except (TypeError, ValueError):
        result = float(default)
    if minimum is not None:
        result = max(minimum, result)
    return result
