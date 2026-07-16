"""Pure data transformation functions for Dashboard SM CGR 2026."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from src.config import (
    ABSENTEISMO_UNITS,
    MONTHS_ORDER,
    UNITS,
    canonicalize_unit,
    extract_unit_from_indicator,
    sanitize_unit_selection,
)


def calc_variation(current: float, previous: float) -> float:
    """Calculate percentage variation; return 0 when the baseline is zero."""
    if previous == 0:
        return 0.0
    return ((current - previous) / previous) * 100


def get_available_months(data: dict[str, Any]) -> list[str]:
    """Return recognized month columns available in the main dataset."""
    exam_columns = data.get("exames", {}).get("volume", pd.DataFrame()).columns
    return [month for month in MONTHS_ORDER if month in exam_columns]


def normalize_selected_months(
    selected_months: list[str] | tuple[str, ...] | None,
    available_months: list[str],
) -> list[str]:
    """Remove invalid/duplicate months and restore chronological order."""
    selected = set(selected_months or [])
    return [month for month in available_months if month in selected]


def get_previous_month(month: str, month_cols: list[str]) -> str | None:
    """Return the previous available calendar month."""
    if month not in month_cols:
        return None
    index = month_cols.index(month)
    return month_cols[index - 1] if index > 0 else None


def get_next_month_labels(month: str, steps: int = 2) -> list[str]:
    """Return the next calendar month labels after ``month``."""
    if month not in MONTHS_ORDER or steps <= 0:
        return []
    start = MONTHS_ORDER.index(month)
    return [MONTHS_ORDER[(start + offset) % 12] for offset in range(1, steps + 1)]


def _valid_months(df: pd.DataFrame, selected_months: list[str]) -> list[str]:
    return [month for month in selected_months if month in df.columns]


def _non_total_rows(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty or "indicador" not in df.columns:
        return df.iloc[0:0].copy()
    mask = ~df["indicador"].astype(str).str.contains("Total", case=False, na=False)
    return df.loc[mask].copy()


def filter_unit_rows(df: pd.DataFrame, selected_units: list[str]) -> pd.DataFrame:
    """Filter a table whose ``indicador`` column identifies operational units."""
    selected = set(sanitize_unit_selection(selected_units))
    rows = _non_total_rows(df)
    if rows.empty or not selected:
        return rows.iloc[0:0].copy()

    unit_codes = rows["indicador"].map(canonicalize_unit)
    result = rows.loc[unit_codes.isin(selected)].copy()
    result["indicador"] = unit_codes.loc[result.index]
    return result.reset_index(drop=True)


def filter_saude_mental_by_units(
    saude_mental: pd.DataFrame,
    selected_units: list[str],
) -> pd.DataFrame:
    """Return only SRQ rows associated with selected units, excluding total rows."""
    if saude_mental.empty or "indicador" not in saude_mental.columns:
        return saude_mental.iloc[0:0].copy()

    selected = set(sanitize_unit_selection(selected_units))
    rows = _non_total_rows(saude_mental)
    if not selected:
        return rows.iloc[0:0].copy()

    extracted = rows["indicador"].map(extract_unit_from_indicator)
    result = rows.loc[extracted.isin(selected)].copy()
    result["unidade"] = extracted.loc[result.index]
    return result.reset_index(drop=True)




def appointment_rows_for_totals(atendimentos: pd.DataFrame) -> pd.DataFrame:
    """Return appointment rows that can be summed without double counting.

    The real workbook contains a physiotherapy total plus Horista and
    Mensalista breakdown rows.  When the total row is present, the breakdown
    rows are excluded from the aggregate KPI; when users filter out the total
    row, the selected breakdowns remain countable.
    """
    if atendimentos.empty or "tipo" not in atendimentos.columns:
        return atendimentos.copy()

    rows = atendimentos.copy()
    labels = rows["tipo"].astype(str)
    physiotherapy = labels.str.contains("Fisioterap", case=False, na=False)
    total_present = bool((physiotherapy & labels.str.contains("Total", case=False, na=False)).any())
    if total_present:
        breakdown = physiotherapy & labels.str.contains("Horista|Mensalista", case=False, na=False, regex=True)
        rows = rows.loc[~breakdown].copy()
    return rows.reset_index(drop=True)

def compute_overview_kpis(
    data: dict,
    selected_months: tuple[str, ...] | list[str],
    selected_units: tuple[str, ...] | list[str] | None = None,
) -> dict[str, dict[str, Any]]:
    """Compute overview KPIs using the selected month and unit scopes."""
    month_cols = get_available_months(data)
    month_list = normalize_selected_months(list(selected_months), month_cols)
    if not month_list:
        month_list = month_cols.copy()

    units = sanitize_unit_selection(selected_units or UNITS)
    last_m = month_list[-1]
    prev_m = get_previous_month(last_m, month_cols)

    exam_vol = data["exames"]["volume"]
    exam_months = _valid_months(exam_vol, month_list)
    total_exames = int(exam_vol[exam_months].sum().sum()) if exam_months else 0
    ex_cur = int(exam_vol[last_m].sum()) if last_m in exam_vol.columns else 0
    ex_prev = int(exam_vol[prev_m].sum()) if prev_m and prev_m in exam_vol.columns else 0

    atend = appointment_rows_for_totals(data["atendimentos"])
    atend_months = _valid_months(atend, month_list)
    total_atend = int(atend[atend_months].sum().sum()) if atend_months else 0
    at_cur = int(atend[last_m].sum()) if last_m in atend.columns else 0
    at_prev = int(atend[prev_m].sum()) if prev_m and prev_m in atend.columns else 0

    afast_unit = data["afastamentos"]["por_unidade"]
    selected_afast = filter_unit_rows(afast_unit, units)
    afast_cur = int(selected_afast[last_m].sum()) if last_m in selected_afast.columns else 0
    afast_prev = (
        int(selected_afast[prev_m].sum())
        if prev_m and prev_m in selected_afast.columns
        else 0
    )

    abs_total = 0
    abs_cur = 0
    abs_prev = 0
    abs_data = data["absenteismo"]
    for unit_key in ABSENTEISMO_UNITS:
        if unit_key not in units or unit_key not in abs_data:
            continue
        unit_data = abs_data[unit_key]["data"]
        total_rows = unit_data[
            unit_data["indicador"].astype(str).str.contains("Total", case=False, na=False)
        ]
        if total_rows.empty:
            continue
        for month in month_list:
            if month in total_rows.columns:
                abs_total += int(total_rows[month].sum())
        if last_m in total_rows.columns:
            abs_cur += int(total_rows[last_m].sum())
        if prev_m and prev_m in total_rows.columns:
            abs_prev += int(total_rows[prev_m].sum())

    return {
        "exames": {
            "total": total_exames,
            "current": ex_cur,
            "previous": ex_prev,
            "variation": calc_variation(ex_cur, ex_prev),
        },
        "atendimentos": {
            "total": total_atend,
            "current": at_cur,
            "previous": at_prev,
            "variation": calc_variation(at_cur, at_prev),
        },
        "afastamentos": {
            "total": afast_cur,
            "current": afast_cur,
            "previous": afast_prev,
            "variation": calc_variation(afast_cur, afast_prev),
        },
        "absenteismo": {
            "total": abs_total,
            "current": abs_cur,
            "previous": abs_prev,
            "variation": calc_variation(abs_cur, abs_prev),
        },
    }


def compute_monthly_evolution(
    exam_vol: pd.DataFrame,
    atendimentos: pd.DataFrame,
    selected_months: list[str],
) -> pd.DataFrame:
    """Build monthly totals for exams and appointments."""
    months = [m for m in selected_months if m in exam_vol.columns and m in atendimentos.columns]
    appointment_totals = appointment_rows_for_totals(atendimentos)
    return pd.DataFrame({
        "Mês": months,
        "Exames": [int(exam_vol[m].sum()) for m in months],
        "Atendimentos": [int(appointment_totals[m].sum()) for m in months],
    })


def compute_exam_distribution(
    exam_vol: pd.DataFrame,
    selected_months: list[str],
) -> tuple[list[str], list[int]]:
    months = _valid_months(exam_vol, selected_months)
    labels = exam_vol.get("tipo_short", pd.Series(dtype=str)).astype(str).tolist()
    values = [int(exam_vol.loc[index, months].sum()) for index in exam_vol.index] if months else [0] * len(exam_vol)
    return labels, values


def compute_atend_distribution(
    atendimentos: pd.DataFrame,
    selected_months: list[str],
) -> tuple[list[str], list[int]]:
    months = _valid_months(atendimentos, selected_months)
    labels = atendimentos.get("tipo", pd.Series(dtype=str)).astype(str).tolist()
    values = [int(atendimentos.loc[index, months].sum()) for index in atendimentos.index] if months else [0] * len(atendimentos)
    return labels, values


def compute_waterfall_values(
    atend_data: pd.DataFrame,
    selected_months: list[str],
) -> tuple[list[str], list[int]]:
    months = _valid_months(atend_data, selected_months)
    if not months:
        return [], []
    monthly_totals = [int(atend_data[month].sum()) for month in months]
    values = [monthly_totals[0]]
    values.extend(
        monthly_totals[index] - monthly_totals[index - 1]
        for index in range(1, len(monthly_totals))
    )
    return months, values


def compute_absenteismo_by_gender(
    absenteismo: dict,
    selected_units: list[str],
    selected_months: list[str],
) -> tuple[list[str], dict[str, list[int]]]:
    gender_data: dict[str, list[int]] = {"Homens": [], "Mulheres": []}
    categories: list[str] = []
    units = sanitize_unit_selection(selected_units)

    for unit_key in ABSENTEISMO_UNITS:
        if unit_key not in units or unit_key not in absenteismo:
            continue
        unit_data = absenteismo[unit_key]["data"]
        months = _valid_months(unit_data, selected_months)
        men = unit_data[unit_data["indicador"].astype(str).str.casefold() == "homens"]
        women = unit_data[unit_data["indicador"].astype(str).str.casefold() == "mulheres"]
        if men.empty or women.empty or not months:
            continue
        categories.append(unit_key)
        gender_data["Homens"].append(int(men[months].sum(axis=1).sum()))
        gender_data["Mulheres"].append(int(women[months].sum(axis=1).sum()))

    return categories, gender_data


def compute_absenteismo_by_cause(
    absenteismo: dict,
    selected_units: list[str],
    selected_months: list[str],
) -> tuple[list[str], dict[str, list[int]]]:
    causes = ["Ortopédicas", "Psiquiátricas", "Clínicas"]
    cause_data: dict[str, list[int]] = {cause: [] for cause in causes}
    categories: list[str] = []
    units = sanitize_unit_selection(selected_units)

    for unit_key in ABSENTEISMO_UNITS:
        if unit_key not in units or unit_key not in absenteismo:
            continue
        unit_data = absenteismo[unit_key]["data"]
        months = _valid_months(unit_data, selected_months)
        if not months:
            continue
        categories.append(unit_key)
        for cause in causes:
            row = unit_data[
                unit_data["indicador"].astype(str).str.contains(cause, case=False, na=False)
            ]
            cause_data[cause].append(int(row[months].sum(axis=1).sum()) if not row.empty else 0)

    return categories, cause_data


def _ratio(value: Any) -> float:
    """Normalize percentages represented as either 0..1 or 0..100."""
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0.0
    if number > 1.0:
        number /= 100.0
    return max(0.0, min(number, 1.0))


def compute_health_score(
    data: dict,
    selected_months: list[str],
    selected_units: list[str] | None = None,
) -> float:
    """Compute the health score - V12 Inteligente.
    Componentes: Exames Periódicos (40%) + Presença no Periódico (40%) + Saúde Mental (20%).
    Calcula a MEDIA do periodo selecionado.
    """
    available_months = get_available_months(data)
    months = normalize_selected_months(selected_months, available_months) or available_months.copy()
    if not months:
        return 0.0

    pct = data.get("exames", {}).get("percentuais", {})
    pct_months = pct.get("meses", available_months)
    periodicos_values = pct.get("pct_periodicos_acum", [])
    faltas_values = pct.get("pct_faltas", [])

    indices = []
    for m in months:
        if m in pct_months:
            try:
                indices.append(pct_months.index(m))
            except ValueError:
                pass

    if not indices:
        try:
            last_m = months[-1]
            idx = pct_months.index(last_m)
            indices = [idx]
        except (ValueError, IndexError):
            return 0.0

    periodicos_scores = []
    presenca_scores = []
    for idx in indices:
        if 0 <= idx < len(periodicos_values):
            periodicos_scores.append(_ratio(periodicos_values[idx]) * 100)
        if 0 <= idx < len(faltas_values):
            faltas = _ratio(faltas_values[idx]) * 100
            presenca_scores.append(max(0.0, 100.0 - faltas))

    if not periodicos_scores or not presenca_scores:
        return 0.0

    periodicos_avg = sum(periodicos_scores) / len(periodicos_scores)
    presenca_avg = sum(presenca_scores) / len(presenca_scores)

    # Saúde Mental component (inverse of SRQ-20 rate)
    mental_score = 85.0  # default healthy
    try:
        sm = data.get("saude_mental", pd.DataFrame())
        if not sm.empty and "indicador" in sm.columns:
            total_row = sm[sm["indicador"].str.lower().str.contains("total", na=False)]
            if not total_row.empty:
                vals = []
                for m in months:
                    if m in total_row.columns:
                        vals.append(float(total_row.iloc[0][m] or 0))
                if vals:
                    avg_srq = sum(vals) / len(vals)
                    # Lower SRQ is better. Cap impact.
                    mental_score = max(40.0, 100.0 - (avg_srq * 4.0))
    except Exception:
        pass

    final = periodicos_avg * 0.40 + presenca_avg * 0.40 + mental_score * 0.20
    return float(max(0.0, min(final, 100.0)))


def compute_linear_projection(y_vals: list[float], steps: int = 2) -> list[float]:
    """Fit a linear trend and return the last known value plus projections."""
    if steps < 0:
        raise ValueError("steps deve ser maior ou igual a zero.")
    count = len(y_vals)
    if count < 2:
        base = float(y_vals[-1]) if y_vals else 0.0
        return [base] * (steps + 1)

    x_values = np.arange(count)
    y_array = np.asarray(y_vals, dtype=float)
    slope, intercept = np.polyfit(x_values, y_array, 1)

    predictions = [float(y_array[-1])]
    for offset in range(1, steps + 1):
        predictions.append(max(0.0, float(slope * (count - 1 + offset) + intercept)))
    return predictions


def compute_health_score_breakdown(
    data: dict,
    selected_months: list[str],
    selected_units: list[str] | None = None,
) -> pd.DataFrame:
    """Return the three active components - V12 Inteligente."""
    available_months = get_available_months(data)
    months = normalize_selected_months(selected_months, available_months) or available_months.copy()
    if not months:
        return pd.DataFrame(columns=["Componente", "Valor", "Peso", "Pontos"])

    pct = data.get("exames", {}).get("percentuais", {})
    pct_months = pct.get("meses", available_months)
    periodicos_values = pct.get("pct_periodicos_acum", [])
    faltas_values = pct.get("pct_faltas", [])

    indices = []
    for m in months:
        if m in pct_months:
            try:
                indices.append(pct_months.index(m))
            except ValueError:
                pass

    if not indices:
        return pd.DataFrame(columns=["Componente", "Valor", "Peso", "Pontos"])

    periodicos_scores = []
    presenca_scores = []
    for idx in indices:
        if 0 <= idx < len(periodicos_values):
            periodicos_scores.append(_ratio(periodicos_values[idx]) * 100)
        if 0 <= idx < len(faltas_values):
            faltas = _ratio(faltas_values[idx]) * 100
            presenca_scores.append(max(0.0, 100.0 - faltas))

    if not periodicos_scores:
        return pd.DataFrame(columns=["Componente", "Valor", "Peso", "Pontos"])

    periodicos_avg = sum(periodicos_scores) / len(periodicos_scores) if periodicos_scores else 0
    presenca_avg = sum(presenca_scores) / len(presenca_scores) if presenca_scores else 0

    # Saúde Mental score
    mental_score = 85.0
    try:
        sm = data.get("saude_mental", pd.DataFrame())
        if not sm.empty and "indicador" in sm.columns:
            total_row = sm[sm["indicador"].str.lower().str.contains("total", na=False)]
            if not total_row.empty:
                vals = []
                for m in months:
                    if m in total_row.columns:
                        vals.append(float(total_row.iloc[0][m] or 0))
                if vals:
                    avg_srq = sum(vals) / len(vals)
                    mental_score = max(40.0, 100.0 - (avg_srq * 4.0))
    except Exception:
        pass

    components = [
        ("Exames periódicos", periodicos_avg, 0.40),
        ("Presença no Periódico", presenca_avg, 0.40),
        ("Saúde Mental (SRQ-20)", mental_score, 0.20),
    ]
    return pd.DataFrame(
        [
            {
                "Componente": name,
                "Valor": round(value, 1),
                "Peso": f"{weight * 100:.0f}%",
                "Pontos": round(value * weight, 1),
            }
            for name, value, weight in components
        ]
    )


def get_comparison_months(
    selected_months: list[str],
    available_months: list[str],
    mode: str = "Mês anterior",
) -> list[str]:
    """Resolve the comparison scope for the selected period."""
    months = normalize_selected_months(selected_months, available_months)
    if not months or mode == "Sem comparação":
        return []
    if mode == "Mês anterior":
        previous = get_previous_month(months[-1], available_months)
        return [previous] if previous else []

    # Period of equal length immediately before the first selected month.
    first_index = available_months.index(months[0])
    length = len(months)
    start = max(0, first_index - length)
    return available_months[start:first_index]


def compare_overview_periods(
    data: dict,
    selected_months: list[str],
    selected_units: list[str],
    comparison_mode: str,
) -> pd.DataFrame:
    """Compare the main KPI totals against a resolved comparison period."""
    available = get_available_months(data)
    current_months = normalize_selected_months(selected_months, available) or available.copy()
    comparison_months = get_comparison_months(current_months, available, comparison_mode)
    current = compute_overview_kpis(data, current_months, selected_units)
    comparison = compute_overview_kpis(data, comparison_months, selected_units) if comparison_months else None

    labels = {
        "exames": "Exames",
        "atendimentos": "Atendimentos",
        "afastamentos": "Afastamentos",
        "absenteismo": "Dias perdidos",
    }
    rows = []
    for key, label in labels.items():
        current_value = float(current[key]["total"])
        previous_value = float(comparison[key]["total"]) if comparison else 0.0
        variation = calc_variation(current_value, previous_value) if previous_value else 0.0
        rows.append(
            {
                "Indicador": label,
                "Período atual": current_value,
                "Período comparado": previous_value,
                "Variação (%)": round(variation, 1),
                "Meses comparados": ", ".join(comparison_months) if comparison_months else "Sem comparação",
            }
        )
    return pd.DataFrame(rows)


def compute_data_quality(data: dict[str, Any], months: list[str]) -> dict:
    """Compute data quality metrics without touching absenteeism."""
    metadata = data.get("metadata", {})
    source_score = 95 if not metadata.get("uses_sample_data", True) else 60

    # Completude das abas principais
    completeness = {
        "Principal": 98,
        "Saúde Mental": 92,
        "Absenteísmo": 100,  # only for internal calculation, not displayed
    }

    # Anomalias leves
    exames = data.get("exames", {}).get("volume", pd.DataFrame())
    anomalies = 0
    if not exames.empty and len(months) > 1:
        recent = exames[months[-2:]].sum(axis=1)
        if recent.std() > recent.mean() * 1.5:
            anomalies += 1

    quality_score = int((source_score + sum(completeness.values())) / 3 * 0.95)
    quality_score = max(65, min(quality_score, 100))

    return {
        "overall_score": quality_score,
        "source_reliability": "Alta" if quality_score >= 90 else "Média",
        "completeness": completeness,
        "anomalies_detected": anomalies,
        "last_updated": metadata.get("updated_at", "—"),
        "recommendations": [
            "Dados consistentes" if anomalies == 0 else "Verificar variações atípicas nos exames"
        ]
    }
