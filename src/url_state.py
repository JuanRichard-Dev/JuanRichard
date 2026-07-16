"""Shareable filter state encoded in Streamlit query parameters."""

from __future__ import annotations

from collections.abc import Iterable, Mapping


def _split(value: object) -> list[str]:
    if value is None:
        return []
    if isinstance(value, (list, tuple)):
        items: list[str] = []
        for item in value:
            items.extend(str(item).split(","))
        return [item.strip() for item in items if item.strip()]
    return [item.strip() for item in str(value).split(",") if item.strip()]


def read_filter_query(
    query: Mapping[str, object],
    *,
    available_months: Iterable[str],
    available_units: Iterable[str],
) -> dict[str, list[str]]:
    months_available = list(available_months)
    units_available = list(available_units)
    months = [item for item in _split(query.get("meses")) if item in months_available]
    units = [item for item in _split(query.get("unidades")) if item in units_available]
    return {"months": months, "units": units}


def filter_query_values(months: Iterable[str], units: Iterable[str]) -> dict[str, str]:
    return {
        "meses": ",".join(months),
        "unidades": ",".join(units),
    }
