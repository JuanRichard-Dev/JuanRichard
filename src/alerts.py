"""Rule-based alerts and lightweight anomaly detection."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd

from src.config import TARGETS
from src.transforms import (
    compute_health_score,
    compute_overview_kpis,
    filter_saude_mental_by_units,
    get_available_months,
    normalize_selected_months,
)


@dataclass(frozen=True)
class Alert:
    severity: str
    title: str
    message: str
    metric: str
    value: float
    threshold: float | None = None


def _variation_alert(metric: str, label: str, current: float, previous: float, threshold: float) -> Alert | None:
    if previous <= 0:
        return None
    variation = ((current - previous) / previous) * 100
    if variation >= threshold:
        return Alert(
            "warning",
            f"Alta relevante em {label}",
            f"{label} aumentou {variation:.1f}% em relação ao período anterior.",
            metric,
            variation,
            threshold,
        )
    return None


def generate_alerts(
    data: dict[str, Any],
    selected_months: list[str],
    selected_units: list[str],
) -> list[Alert]:
    """Generate explainable alerts using configured business thresholds."""
    alerts: list[Alert] = []
    kpis = compute_overview_kpis(data, selected_months, selected_units)
    score = compute_health_score(data, selected_months, selected_units)

    # Alerta de saude - agora sempre baseado no score dinamico
    if score < TARGETS["health_score"]:
        alerts.append(
            Alert(
                "danger",
                "Índice de saúde",
                f"O índice está em {score:.1f}%.",
                "health_score",
                score,
                TARGETS["health_score"],
            )
        )

    for metric, label in [("afastamentos", "afastamentos"), ("absenteismo", "dias perdidos")]:
        alert = _variation_alert(
            metric,
            label,
            kpis[metric]["current"],
            kpis[metric]["previous"],
            TARGETS["variation_warning_pct"],
        )
        if alert:
            alerts.append(alert)

    if kpis["absenteismo"]["current"] > 0:
        alerts.append(
            Alert(
                "danger",
                "Absenteísmo",
                f"Foram registrados {kpis['absenteismo']['current']:.0f} dias perdidos no mês de referência.",
                "absenteismo",
                float(kpis["absenteismo"]["current"]),
                TARGETS["absenteismo_monthly_max"],
            )
        )

    months = normalize_selected_months(selected_months, get_available_months(data))
    if months:
        last = months[-1]
        mental = filter_saude_mental_by_units(data["saude_mental"], selected_units)
        mental_cases = float(mental[last].sum()) if last in mental.columns else 0.0
        if mental_cases > TARGETS["mental_cases_max"]:
            alerts.append(
                Alert(
                    "warning",
                    "Atenção à saúde mental",
                    f"Há {mental_cases:.0f} triagens SRQ-20 alteradas nas unidades selecionadas.",
                    "saude_mental",
                    mental_cases,
                    TARGETS["mental_cases_max"],
                )
            )

    pct = data["exames"]["percentuais"]
    # CORRIGIDO: agora calcula media do periodo selecionado, nao so ultimo mes
    if months:
        indices = []
        for m in months:
            if m in pct.get("meses", []):
                try:
                    indices.append(pct["meses"].index(m))
                except ValueError:
                    pass
        if indices:
            periodic_vals = []
            for idx in indices:
                try:
                    val = pct.get("pct_periodicos_acum", [0])[idx]
                    periodic_vals.append(float(val) * 100 if float(val) <= 1 else float(val))
                except (IndexError, ValueError, TypeError):
                    pass
            if periodic_vals:
                periodic = sum(periodic_vals) / len(periodic_vals)
                # Mostra alerta independente de meta, mas mantem logica se quiser filtrar por meta baixa
                if periodic < TARGETS["periodicos_pct"] or True:  # sempre mostra se houver dado
                    alerts.append(
                        Alert(
                            "warning",
                            "Exames periódicos",
                            f"A cobertura está em {periodic:.1f}%.",
                            "periodicos",
                            periodic,
                            TARGETS["periodicos_pct"],
                        )
                    )

    if not alerts:
        alerts.append(
            Alert(
                "success",
                "Nenhum alerta crítico",
                "Os indicadores selecionados estão dentro dos limites configurados.",
                "geral",
                0.0,
                None,
            )
        )
    return alerts


def detect_anomalies(values: list[float], labels: list[str], z_threshold: float = 2.0) -> pd.DataFrame:
    """Return points with an absolute z-score above the threshold.

    This intentionally uses a transparent statistical rule instead of a black
    box model.  At least four observations are required.
    """
    if len(values) < 4 or len(values) != len(labels):
        return pd.DataFrame(columns=["Período", "Valor", "Z-score", "Classificação"])

    series = np.asarray(values, dtype=float)
    standard_deviation = float(series.std(ddof=0))
    if standard_deviation == 0:
        return pd.DataFrame(columns=["Período", "Valor", "Z-score", "Classificação"])

    z_scores = (series - series.mean()) / standard_deviation
    rows = []
    for label, value, z_score in zip(labels, series, z_scores):
        if abs(z_score) >= z_threshold:
            rows.append(
                {
                    "Período": label,
                    "Valor": float(value),
                    "Z-score": round(float(z_score), 2),
                    "Classificação": "Acima do esperado" if z_score > 0 else "Abaixo do esperado",
                }
            )
    return pd.DataFrame(rows)
