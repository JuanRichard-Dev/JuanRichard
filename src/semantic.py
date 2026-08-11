"""Semantic layer built exclusively from the delivered real workbook.

The workbook is stored in a presentation-oriented layout.  This module turns
its normalized wide tables into consistent long-form analytical datasets so
all pages use the same dimensions and aggregation rules.
"""

from __future__ import annotations

from typing import Any

import pandas as pd

from src.config import ABSENTEISMO_UNITS, MONTHS_ORDER, UNITS
from src.transforms import (
    appointment_rows_for_totals,
    filter_saude_mental_by_units,
    filter_unit_rows,
    get_available_months,
    normalize_selected_months,
)


def _wide_to_long(
    frame: pd.DataFrame,
    *,
    label_column: str,
    label_name: str,
    months: list[str],
    category: str,
    unit: str | None = None,
) -> pd.DataFrame:
    """Convert a normalized wide source table into the semantic long format."""
    valid_months = [month for month in months if month in frame.columns]
    if frame.empty or label_column not in frame.columns or not valid_months:
        return pd.DataFrame(
            columns=["Categoria", label_name, "Unidade", "Mês", "Ordem Mês", "Valor"]
        )

    long = frame[[label_column] + valid_months].melt(
        id_vars=[label_column],
        value_vars=valid_months,
        var_name="Mês",
        value_name="Valor",
    )
    long = long.rename(columns={label_column: label_name})
    long.insert(0, "Categoria", category)
    long["Unidade"] = unit
    long["Ordem Mês"] = long["Mês"].map({month: index for index, month in enumerate(MONTHS_ORDER)})
    long["Valor"] = pd.to_numeric(long["Valor"], errors="coerce").fillna(0)
    return long[["Categoria", label_name, "Unidade", "Mês", "Ordem Mês", "Valor"]]


def build_semantic_model(data: dict[str, Any]) -> dict[str, pd.DataFrame]:
    """Build reusable analytical tables from the user's real workbook.

    No record is invented.  Every output value is derived from one of the
    normalized source tables produced by :mod:`src.data_loader`.
    """
    months = get_available_months(data)

    exams = _wide_to_long(
        data["exames"]["volume"],
        label_column="tipo_short",
        label_name="Indicador",
        months=months,
        category="Exames",
    )

    appointments_source = appointment_rows_for_totals(data["atendimentos"])
    appointments = _wide_to_long(
        appointments_source,
        label_column="tipo",
        label_name="Indicador",
        months=months,
        category="Atendimentos",
    )

    afast_units_source = filter_unit_rows(data["afastamentos"]["por_unidade"], UNITS)
    afast_units = _wide_to_long(
        afast_units_source,
        label_column="indicador",
        label_name="Indicador",
        months=months,
        category="Afastamentos",
    )
    if not afast_units.empty:
        afast_units["Unidade"] = afast_units["Indicador"]

    reasons = _wide_to_long(
        data["afastamentos"]["por_motivo"],
        label_column="indicador",
        label_name="Indicador",
        months=months,
        category="Motivos de afastamento",
    )

    absenteeism_frames: list[pd.DataFrame] = []
    for unit in ABSENTEISMO_UNITS:
        unit_payload = data["absenteismo"].get(unit)
        if not unit_payload:
            continue
        unit_data = unit_payload["data"]
        long = _wide_to_long(
            unit_data,
            label_column="indicador",
            label_name="Indicador",
            months=months,
            category="Absenteísmo",
            unit=unit,
        )
        absenteeism_frames.append(long)
    absenteeism = (
        pd.concat(absenteeism_frames, ignore_index=True)
        if absenteeism_frames
        else pd.DataFrame(columns=["Categoria", "Indicador", "Unidade", "Mês", "Ordem Mês", "Valor"])
    )

    mental_source = filter_saude_mental_by_units(data["saude_mental"], UNITS)
    mental = _wide_to_long(
        mental_source,
        label_column="unidade",
        label_name="Indicador",
        months=months,
        category="Saúde Mental",
    )
    if not mental.empty:
        mental["Unidade"] = mental["Indicador"]

    return {
        "exames": exams,
        "atendimentos": appointments,
        "afastamentos_unidade": afast_units,
        "afastamentos_motivo": reasons,
        "absenteismo": absenteeism,
        "saude_mental": mental,
    }


def filter_semantic(
    frame: pd.DataFrame,
    *,
    months: list[str] | tuple[str, ...] | None = None,
    units: list[str] | tuple[str, ...] | None = None,
    indicators: list[str] | tuple[str, ...] | None = None,
) -> pd.DataFrame:
    """Apply common semantic dimensions consistently."""
    result = frame.copy()
    if months is not None and "Mês" in result.columns:
        result = result[result["Mês"].isin(list(months))]
    if units is not None and "Unidade" in result.columns:
        requested = set(units)
        result = result[result["Unidade"].isna() | result["Unidade"].isin(requested)]
    if indicators is not None and "Indicador" in result.columns:
        result = result[result["Indicador"].isin(list(indicators))]
    return result.reset_index(drop=True)


def semantic_monthly_totals(
    data: dict[str, Any],
    selected_months: list[str],
    selected_units: list[str],
) -> pd.DataFrame:
    """Return the five executive metrics on one consistent monthly table."""
    months = normalize_selected_months(selected_months, get_available_months(data))
    model = data.get("semantic") or build_semantic_model(data)

    rows: list[dict[str, object]] = []
    for month in months:
        exams = model["exames"].query("Mês == @month")["Valor"].sum()
        appointments = model["atendimentos"].query("Mês == @month")["Valor"].sum()
        afast = model["afastamentos_unidade"]
        afast = afast[(afast["Mês"] == month) & afast["Unidade"].isin(selected_units)]["Valor"].sum()

        abs_frame = model["absenteismo"]
        abs_total = abs_frame[
            (abs_frame["Mês"] == month)
            & abs_frame["Unidade"].isin(selected_units)
            & abs_frame["Indicador"].astype(str).str.casefold().eq("total")
        ]["Valor"].sum()

        mental = model["saude_mental"]
        mental_total = mental[
            (mental["Mês"] == month) & mental["Unidade"].isin(selected_units)
        ]["Valor"].sum()

        rows.append(
            {
                "Mês": month,
                "Exames": float(exams),
                "Atendimentos": float(appointments),
                "Afastamentos": float(afast),
                "Dias Perdidos": float(abs_total),
                "SRQ-20": float(mental_total),
            }
        )
    return pd.DataFrame(rows)


def source_coverage_notes(data: dict[str, Any]) -> dict[str, str]:
    """Describe the real dimensional coverage without implying unavailable joins."""
    _ = data
    return {
        "Exames": "A fonte apresenta tipo de exame por mês, sem abertura por unidade.",
        "Atendimentos": "A fonte apresenta tipo de atendimento por mês, sem abertura por unidade.",
        "Afastamentos": "A fonte contém unidade e motivo em blocos separados; motivo não cruza unidade.",
        "Absenteísmo": "A fonte detalha B2BN, B2BF e SF por mês, causa e gênero.",
        "Saúde Mental": "A fonte detalha os casos SRQ-20 por unidade e mês.",
    }
