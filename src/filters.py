"""Central filter model and diagnostics for the dashboard.

Widgets are applied immediately on each Streamlit rerun.  Their values are
normalized into an immutable :class:`FilterState`, ensuring every KPI, chart
and matrix consumes the same canonical scope.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

import pandas as pd

from src.config import COMPARISON_MODES, sanitize_unit_selection
from src.transforms import normalize_selected_months


@dataclass(frozen=True)
class FilterState:
    """Canonical set of filters used by every page and calculation."""

    months: tuple[str, ...]
    units: tuple[str, ...]
    exams: tuple[str, ...] = ()
    appointments: tuple[str, ...] = ()
    reasons: tuple[str, ...] = ()
    comparison_mode: str = "Mês anterior"

    @property
    def signature(self) -> tuple[Any, ...]:
        """Stable hashable representation used by caches and audit logging."""
        return (
            self.months,
            self.units,
            self.exams,
            self.appointments,
            self.reasons,
            self.comparison_mode,
        )

    def as_dict(self) -> dict[str, Any]:
        return {
            "months": list(self.months),
            "units": list(self.units),
            "exams": list(self.exams),
            "appointments": list(self.appointments),
            "reasons": list(self.reasons),
            "comparison_mode": self.comparison_mode,
        }


def build_filter_state(
    *,
    months: Iterable[str] | None,
    available_months: list[str],
    units: Iterable[object] | None,
    exams: Iterable[str] | None = None,
    appointments: Iterable[str] | None = None,
    reasons: Iterable[str] | None = None,
    available_exams: list[str] | None = None,
    available_appointments: list[str] | None = None,
    available_reasons: list[str] | None = None,
    comparison_mode: str = "Mês anterior",
) -> FilterState:
    """Validate widget values and return a canonical immutable filter state."""
    # Empty month selection is intentional and must remain empty.
    # The application handles this state with a friendly empty-state message,
    # instead of silently restoring every month.
    normalized_months = normalize_selected_months(list(months or []), available_months)

    # Empty selections are intentional for every slicer. The UI presents a
    # clear empty state instead of silently converting an empty slicer to all.
    normalized_units = sanitize_unit_selection(units)

    def valid(values: Iterable[str] | None, available: list[str] | None) -> tuple[str, ...]:
        available = available or []
        selected = [value for value in (values or []) if value in available]
        return tuple(selected)

    normalized_comparison = (
        comparison_mode if comparison_mode in COMPARISON_MODES else COMPARISON_MODES[0]
    )
    return FilterState(
        months=tuple(normalized_months),
        units=tuple(normalized_units),
        exams=valid(exams, available_exams),
        appointments=valid(appointments, available_appointments),
        reasons=valid(reasons, available_reasons),
        comparison_mode=normalized_comparison,
    )


def filter_exam_volume(df: pd.DataFrame, filters: FilterState) -> pd.DataFrame:
    if "tipo_short" not in df.columns:
        return df.copy()
    return df[df["tipo_short"].isin(filters.exams)].copy()


def filter_appointments(df: pd.DataFrame, filters: FilterState) -> pd.DataFrame:
    if "tipo" not in df.columns:
        return df.copy()
    return df[df["tipo"].isin(filters.appointments)].copy()


def filter_reasons(df: pd.DataFrame, filters: FilterState) -> pd.DataFrame:
    if "indicador" not in df.columns:
        return df.copy()
    return df[df["indicador"].isin(filters.reasons)].copy()


def filter_scope_table(
    filters: FilterState,
    *,
    page: str,
    available_months: list[str],
    available_units: list[str],
    available_exams: list[str],
    available_appointments: list[str],
    available_reasons: list[str],
) -> pd.DataFrame:
    """Create a human-readable diagnostic table for the active filter scope."""
    unit_pages = {"Visão Geral", "Afastamentos", "Saúde Mental"}
    rows = [
        {
            "Filtro": "Meses",
            "Aplicado": ", ".join(filters.months) or "Nenhum mês selecionado",
            "Selecionados": len(filters.months),
            "Disponíveis": len(available_months),
            "Afeta esta página": "Sim",
        },
        {
            "Filtro": "Unidades",
            "Aplicado": ", ".join(filters.units) or "Nenhuma unidade selecionada",
            "Selecionados": len(filters.units),
            "Disponíveis": len(available_units),
            "Afeta esta página": "Sim" if page in unit_pages else "Não — fonte consolidada",
        },
    ]

    page_specific = {
        "Exames": ("Tipos de exame", filters.exams, available_exams),
        "Atendimentos": ("Tipos de atendimento", filters.appointments, available_appointments),
        "Afastamentos": ("Motivos", filters.reasons, available_reasons),
    }
    if page in page_specific:
        label, values, available = page_specific[page]
        rows.append(
            {
                "Filtro": label,
                "Aplicado": ", ".join(values) or "Nenhum item selecionado",
                "Selecionados": len(values),
                "Disponíveis": len(available),
                "Afeta esta página": "Sim",
            }
        )

    rows.append(
        {
            "Filtro": "Comparação",
            "Aplicado": filters.comparison_mode,
            "Selecionados": 1,
            "Disponíveis": 3,
            "Afeta esta página": "Indicadores com histórico",
        }
    )
    return pd.DataFrame(rows)


def filter_reduction_summary(
    before: int,
    after: int,
) -> dict[str, float | int]:
    """Return consistent before/after diagnostics for tables."""
    reduction = 0.0 if before <= 0 else max(0.0, (1 - after / before) * 100)
    return {"before": before, "after": after, "reduction_pct": reduction}
