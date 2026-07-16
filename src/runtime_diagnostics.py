"""Low-overhead runtime metadata for cloud crash diagnostics."""

from __future__ import annotations

import platform
import sys
from importlib.metadata import PackageNotFoundError, version
from typing import Any

_PACKAGES = (
    "streamlit",
    "pandas",
    "numpy",
    "pyarrow",
    "plotly",
    "openpyxl",
    "reportlab",
)


def _package_version(name: str) -> str:
    try:
        return version(name)
    except PackageNotFoundError:
        return "not-installed"


def runtime_payload() -> dict[str, Any]:
    """Return versions without importing native packages again."""
    return {
        "python": platform.python_version(),
        "implementation": platform.python_implementation(),
        "platform": sys.platform,
        "machine": platform.machine(),
        "packages": {name: _package_version(name) for name in _PACKAGES},
    }
