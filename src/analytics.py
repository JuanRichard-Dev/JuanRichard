"""Higher-level analytical calculations for the Power BI style dashboard."""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Any

import numpy as np
import pandas as pd

from src.config import ABSENTEISMO_UNITS, TARGETS, UNITS
from src.semantic import build_semantic_model, semantic_monthly_totals
from src.transforms import (
    calc_variation,
    filter_saude_mental_by_units,
    filter_unit_rows,
    get_available_months,
    get_previous_month,
    normalize_selected_months,
)


@dataclass(frozen=True)
class ForecastResult:
    labels: list[str]
    forecast: list[float]
    lower: list[float]
    upper: list[float]
    confidence: str


def rolling_average(values: list[float], window: int = 3) -> list[float | None]:
    """Return a simple moving average aligned with the original series."""
    if window <= 1:
        return [float(value) for value in values]
    series = pd.Series(values, dtype=float)
    return [None if pd.isna(value) else float(value) for value in series.rolling(window).mean()]


def linear_forecast_with_interval(
    values: list[float],
    labels: list[str],
    future_labels: list[str],
) -> ForecastResult | None:
    """Transparent linear projection with an approximate 95% interval.

    At least three observations are required.  Forecasts and confidence bounds
    are clipped at zero because all dashboard metrics are non-negative counts.
    """
    if len(values) < 3 or len(values) != len(labels) or not future_labels:
        return None

    y = np.asarray(values, dtype=float)
    x = np.arange(len(y), dtype=float)
    slope, intercept = np.polyfit(x, y, 1)
    fitted = slope * x + intercept
    residuals = y - fitted

    degrees = max(len(y) - 2, 1)
    residual_std = float(sqrt(float(np.square(residuals).sum()) / degrees))
    x_mean = float(x.mean())
    sxx = float(np.square(x - x_mean).sum()) or 1.0

    forecast: list[float] = []
    lower: list[float] = []
    upper: list[float] = []
    for offset in range(1, len(future_labels) + 1):
        x_new = float(len(y) - 1 + offset)
        estimate = float(slope * x_new + intercept)
        standard_error = residual_std * sqrt(1.0 + (1.0 / len(y)) + ((x_new - x_mean) ** 2 / sxx))
        margin = 1.96 * standard_error
        forecast.append(max(0.0, estimate))
        lower.append(max(0.0, estimate - margin))
        upper.append(max(0.0, estimate + margin))

    # A short series cannot support strong forecasting claims.
    confidence = "moderada" if len(values) >= 5 and residual_std <= max(float(y.mean()) * 0.25, 1.0) else "baixa"
    return ForecastResult(future_labels, forecast, lower, upper, confidence)


def period_label(months: list[str] | tuple[str, ...]) -> str:
    months = list(months)
    if not months:
        return "sem período"
    if len(months) == 1:
        return months[0]
    return f"{months[0]} a {months[-1]}"


def scope_label(units: list[str] | tuple[str, ...], all_units: list[str] | tuple[str, ...] = UNITS) -> str:
    units = list(units)
    if not units or set(units) == set(all_units):
        return "todas as unidades"
    return ", ".join(units)


def dynamic_title(
    title: str,
    *,
    months: list[str] | tuple[str, ...],
    units: list[str] | tuple[str, ...] | None = None,
    include_units: bool = True,
) -> str:
    """Create a two-line chart title with the active analytical scope."""
    subtitle = f"Período: {period_label(months)}"
    if include_units and units is not None:
        subtitle += f" | Unidades: {scope_label(units)}"
    return f"{title}<br><sup>{subtitle}</sup>"


def executive_metric_series(
    data: dict[str, Any],
    selected_months: list[str],
    selected_units: list[str],
) -> pd.DataFrame:
    return semantic_monthly_totals(data, selected_months, selected_units)


def unit_latest_ranking(
    data: dict[str, Any],
    selected_months: list[str],
    selected_units: list[str],
    metric: str = "Afastamentos",
) -> pd.DataFrame:
    """Rank units and calculate share and month-over-month variation."""
    months = normalize_selected_months(selected_months, get_available_months(data))
    if not months:
        return pd.DataFrame(columns=["Unidade", "Valor", "Anterior", "Variação (%)", "Participação (%)"])
    last = months[-1]
    previous = get_previous_month(last, get_available_months(data))
    rows: list[dict[str, float | str]] = []

    if metric == "Afastamentos":
        frame = filter_unit_rows(data["afastamentos"]["por_unidade"], selected_units)
        for _, row in frame.iterrows():
            current = float(row.get(last, 0))
            prior = float(row.get(previous, 0)) if previous else 0.0
            rows.append({"Unidade": str(row["indicador"]), "Valor": current, "Anterior": prior})
    elif metric == "Dias Perdidos":
        for unit in ABSENTEISMO_UNITS:
            if unit not in selected_units or unit not in data["absenteismo"]:
                continue
            unit_data = data["absenteismo"][unit]["data"]
            total = unit_data[unit_data["indicador"].astype(str).str.casefold().eq("total")]
            current = float(total[last].sum()) if last in total.columns else 0.0
            prior = float(total[previous].sum()) if previous and previous in total.columns else 0.0
            rows.append({"Unidade": unit, "Valor": current, "Anterior": prior})
    elif metric == "SRQ-20":
        mental = filter_saude_mental_by_units(data["saude_mental"], selected_units)
        for _, row in mental.iterrows():
            current = float(row.get(last, 0))
            prior = float(row.get(previous, 0)) if previous else 0.0
            rows.append({"Unidade": str(row["unidade"]), "Valor": current, "Anterior": prior})
    else:
        raise ValueError(f"Métrica de ranking não suportada: {metric}")

    result = pd.DataFrame(rows)
    if result.empty:
        return pd.DataFrame(columns=["Unidade", "Valor", "Anterior", "Variação (%)", "Participação (%)"])
    total_value = float(result["Valor"].sum())
    result["Variação (%)"] = [calc_variation(current, prior) for current, prior in zip(result["Valor"], result["Anterior"])]
    result["Participação (%)"] = (result["Valor"] / total_value * 100) if total_value else 0.0
    return result.sort_values("Valor", ascending=False).reset_index(drop=True)


def unit_period_ranking(
    data: dict[str, Any],
    selected_months: list[str],
    selected_units: list[str],
    metric: str = "Dias Perdidos",
) -> pd.DataFrame:
    """Rank units by accumulated value in the selected period."""
    months = normalize_selected_months(selected_months, get_available_months(data))
    model = data.get("semantic") or build_semantic_model(data)
    if metric == "Dias Perdidos":
        frame = model["absenteismo"]
        frame = frame[
            frame["Unidade"].isin(selected_units)
            & frame["Mês"].isin(months)
            & frame["Indicador"].astype(str).str.casefold().eq("total")
        ]
    elif metric == "Afastamentos":
        frame = model["afastamentos_unidade"]
        frame = frame[frame["Unidade"].isin(selected_units) & frame["Mês"].isin(months)]
    elif metric == "SRQ-20":
        frame = model["saude_mental"]
        frame = frame[frame["Unidade"].isin(selected_units) & frame["Mês"].isin(months)]
    else:
        raise ValueError(f"Métrica de período não suportada: {metric}")

    if frame.empty:
        return pd.DataFrame(columns=["Unidade", "Valor", "Participação (%)"])
    result = frame.groupby("Unidade", as_index=False)["Valor"].sum()
    total = float(result["Valor"].sum())
    result["Participação (%)"] = (result["Valor"] / total * 100) if total else 0.0
    return result.sort_values("Valor", ascending=False).reset_index(drop=True)


def unit_change_contribution(
    data: dict[str, Any],
    selected_months: list[str],
    selected_units: list[str],
    metric: str = "Afastamentos",
) -> tuple[float, pd.DataFrame, float]:
    """Return previous total, unit deltas and current total for a bridge chart."""
    ranking = unit_latest_ranking(data, selected_months, selected_units, metric)
    if ranking.empty:
        return 0.0, pd.DataFrame(columns=["Unidade", "Contribuição"]), 0.0
    previous_total = float(ranking["Anterior"].sum())
    current_total = float(ranking["Valor"].sum())
    contributions = ranking[["Unidade"]].copy()
    contributions["Contribuição"] = ranking["Valor"] - ranking["Anterior"]
    contributions = contributions.sort_values("Contribuição", ascending=False).reset_index(drop=True)
    return previous_total, contributions, current_total


def reason_pareto_table(
    data: dict[str, Any],
    selected_months: list[str],
    selected_reasons: list[str] | None = None,
) -> pd.DataFrame:
    frame = data["afastamentos"]["por_motivo"].copy()
    if selected_reasons is not None:
        frame = frame[frame["indicador"].isin(selected_reasons)]
    months = [month for month in selected_months if month in frame.columns]
    result = pd.DataFrame({
        "Motivo": frame["indicador"].astype(str),
        "Valor": frame[months].sum(axis=1) if months else 0,
    }).sort_values("Valor", ascending=False)
    total = float(result["Valor"].sum())
    result["Participação (%)"] = (result["Valor"] / total * 100) if total else 0.0
    result["Acumulado (%)"] = result["Participação (%)"].cumsum()
    return result.reset_index(drop=True)




def _format_number_pt(value: float) -> str:
    return f"{float(value):,.0f}".replace(",", ".")


def _format_decimal_pt(value: float, digits: int = 1) -> str:
    return f"{float(value):.{digits}f}".replace(".", ",")

def build_executive_narrative(
    data: dict[str, Any],
    selected_months: list[str],
    selected_units: list[str],
) -> str:
    """Generate a concise, fully data-driven executive narrative."""
    monthly = semantic_monthly_totals(data, selected_months, selected_units)
    if monthly.empty:
        return "Não há dados no escopo selecionado."

    totals = monthly[["Exames", "Atendimentos", "Dias Perdidos"]].sum()
    last = monthly.iloc[-1]
    previous = monthly.iloc[-2] if len(monthly) > 1 else None

    ranking = unit_period_ranking(data, selected_months, selected_units, "Dias Perdidos")
    top_unit_text = ""
    if not ranking.empty:
        top = ranking.iloc[0]
        top_unit_text = (
            f" A unidade {top['Unidade']} concentrou "
            f"{_format_decimal_pt(top['Participação (%)'])}% dos dias perdidos do período."
        )

    reason_table = reason_pareto_table(data, selected_months)
    reason_text = ""
    if not reason_table.empty:
        reason = reason_table.iloc[0]
        reason_text = (
            f" O principal motivo de afastamento foi {reason['Motivo'].lower()}, com "
            f"{_format_decimal_pt(reason['Participação (%)'])}% do total por motivo."
        )

    trend_text = ""
    if previous is not None:
        abs_var = calc_variation(float(last["Dias Perdidos"]), float(previous["Dias Perdidos"]))
        direction = "aumentaram" if abs_var > 0 else "recuaram" if abs_var < 0 else "ficaram estáveis"
        trend_text = (
            f" No último mês, os dias perdidos {direction} "
            f"{_format_decimal_pt(abs(abs_var))}% frente ao mês anterior."
        )

    return (
        f"Entre {selected_months[0]} e {selected_months[-1]}, foram realizados {_format_number_pt(totals['Exames'])} exames "
        f"e {_format_number_pt(totals['Atendimentos'])} atendimentos. O período acumulou {_format_number_pt(totals['Dias Perdidos'])} dias perdidos, "
        f"enquanto o mês mais recente encerrou com {_format_number_pt(last['Afastamentos'])} afastamentos ativos e "
        f"{_format_number_pt(last['SRQ-20'])} triagens SRQ-20 alteradas."
        f"{trend_text}{top_unit_text}{reason_text}"
    )


def metric_summary_matrix(
    data: dict[str, Any],
    selected_months: list[str],
    selected_units: list[str],
) -> pd.DataFrame:
    """Create a Power BI-like matrix with totals, last values and variations."""
    monthly = semantic_monthly_totals(data, selected_months, selected_units)
    if monthly.empty:
        return pd.DataFrame()
    metric_columns = [column for column in monthly.columns if column != "Mês"]
    rows: list[dict[str, float | str]] = []
    for metric in metric_columns:
        series = monthly[metric].astype(float)
        current = float(series.iloc[-1])
        previous = float(series.iloc[-2]) if len(series) > 1 else 0.0
        rows.append({
            "Indicador": metric,
            "Total do período": float(series.sum()) if metric not in {"Afastamentos", "SRQ-20"} else current,
            "Último mês": current,
            "Mês anterior": previous,
            "Variação (%)": calc_variation(current, previous),
            "Média mensal": float(series.mean()),
            "Pico": float(series.max()),
        })
    return pd.DataFrame(rows)


def target_status(value: float, target: float | None, direction: str = "higher") -> tuple[str, str]:
    """Return status label and semantic color name for target comparison."""
    if target is None:
        return "Sem meta", "blue"
    achieved = value >= target if direction == "higher" else value <= target
    if achieved:
        return "Dentro da meta", "green"
    gap_ratio = abs(value - target) / max(abs(target), 1.0)
    return ("Atenção", "orange") if gap_ratio <= 0.15 else ("Crítico", "red")


def configured_target(metric: str) -> tuple[float | None, str]:
    mapping = {
        "Health Score": (TARGETS["health_score"], "higher"),
        "% Periódicos": (TARGETS["periodicos_pct"], "higher"),
        "% Faltas": (TARGETS["faltas_pct_max"], "lower"),
        "Dias Perdidos": (TARGETS["absenteismo_monthly_max"], "lower"),
        "SRQ-20": (TARGETS["mental_cases_max"], "lower"),
    }
    return mapping.get(metric, (None, "higher"))
