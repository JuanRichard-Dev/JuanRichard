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
    available_exams: Iterable[str] | None = None,
    available_appointments: Iterable[str] | None = None,
    available_reasons: Iterable[str] | None = None,
) -> dict[str, list[str]]:
    """Read a validated shareable analytical scope from query parameters."""
    months_available = list(available_months)
    units_available = list(available_units)
    result = {
        "months": [item for item in _split(query.get("meses")) if item in months_available],
        "units": [item for item in _split(query.get("unidades")) if item in units_available],
    }
    optional = (
        ("exams", "exames", available_exams),
        ("appointments", "atendimentos", available_appointments),
        ("reasons", "motivos", available_reasons),
    )
    for result_key, query_key, available in optional:
        if available is not None:
            allowed = list(available)
            result[result_key] = [item for item in _split(query.get(query_key)) if item in allowed]
    return result


def filter_query_values(
    months: Iterable[str],
    units: Iterable[str],
    *,
    page: str | None = None,
    exams: Iterable[str] | None = None,
    appointments: Iterable[str] | None = None,
    reasons: Iterable[str] | None = None,
) -> dict[str, str]:
    """Encode the shareable analytical scope.

    Extra page-specific filters are optional, preserving compatibility with
    older callers that only share period and units.
    """
    values = {
        "meses": ",".join(months),
        "unidades": ",".join(units),
    }
    if page:
        values["page"] = str(page)
    if exams is not None:
        values["exames"] = ",".join(exams)
    if appointments is not None:
        values["atendimentos"] = ",".join(appointments)
    if reasons is not None:
        values["motivos"] = ",".join(reasons)
    return values

