"""Executive intelligence helpers built only from supported aggregate data."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd

from src.alerts import generate_alerts
from src.analytics import reason_pareto_table, unit_period_ranking
from src.config import TARGETS, UNITS
from src.i18n import normalize_language, tr
from src.population import add_rate_per_100, load_population
from src.transforms import calc_variation, compute_overview_kpis
from src.unit_targets import load_unit_targets

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MILESTONES_PATH = PROJECT_ROOT / "dashboard_milestones.csv"


@dataclass(frozen=True)
class Milestone:
    month: str
    title: str
    description: str


def _ratio_to_percent(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0.0
    return number * 100.0 if 0 <= number <= 1 else number


def periodic_coverage(data: dict[str, Any], selected_months: list[str]) -> tuple[float, float]:
    """Return current and previous periodic coverage percentages."""
    percentuais = data.get("exames", {}).get("percentuais", {})
    months = list(percentuais.get("meses", []))
    values = list(percentuais.get("pct_periodicos_acum", []))
    scoped = [month for month in selected_months if month in months]
    if not scoped:
        return 0.0, 0.0
    current_index = months.index(scoped[-1])
    previous_index = current_index - 1
    current = _ratio_to_percent(values[current_index]) if current_index < len(values) else 0.0
    previous = _ratio_to_percent(values[previous_index]) if 0 <= previous_index < len(values) else 0.0
    return current, previous


def mental_latest(monthly_metrics: pd.DataFrame) -> tuple[float, float]:
    if monthly_metrics.empty or "SRQ-20" not in monthly_metrics.columns:
        return 0.0, 0.0
    series = pd.to_numeric(monthly_metrics["SRQ-20"], errors="coerce").fillna(0.0)
    current = float(series.iloc[-1])
    previous = float(series.iloc[-2]) if len(series) > 1 else 0.0
    return current, previous


def severity_proxy(kpis: dict[str, dict[str, Any]]) -> tuple[float, float]:
    """Lost days divided by active leaves; this is a management proxy, not duration."""
    current_leaves = float(kpis["afastamentos"]["current"] or 0)
    previous_leaves = float(kpis["afastamentos"]["previous"] or 0)
    current_days = float(kpis["absenteismo"]["current"] or 0)
    previous_days = float(kpis["absenteismo"]["previous"] or 0)
    current = current_days / current_leaves if current_leaves else 0.0
    previous = previous_days / previous_leaves if previous_leaves else 0.0
    return current, previous


def executive_comparison_table(
    data: dict[str, Any],
    selected_months: list[str],
    selected_units: list[str],
    monthly_metrics: pd.DataFrame,
    *,
    language: str = "pt",
) -> pd.DataFrame:
    """Comparison table without Meta/Status columns."""
    language = normalize_language(language)
    kpis = compute_overview_kpis(data, selected_months, selected_units)
    mental_current, mental_previous = mental_latest(monthly_metrics)
    periodic_current, periodic_previous = periodic_coverage(data, selected_months)
    rows = [
        (tr("exams", language), kpis["exames"]["current"], kpis["exames"]["previous"]),
        (tr("appointments", language), kpis["atendimentos"]["current"], kpis["atendimentos"]["previous"]),
        (tr("active_leaves", language), kpis["afastamentos"]["current"], kpis["afastamentos"]["previous"]),
        (tr("lost_days", language), kpis["absenteismo"]["current"], kpis["absenteismo"]["previous"]),
        (tr("srq_cases", language), mental_current, mental_previous),
        (tr("periodic_coverage", language), periodic_current, periodic_previous),
    ]
    records: list[dict[str, Any]] = []
    for label, current, previous in rows:
        records.append(
            {
                tr("metric", language): label,
                tr("current", language): float(current),
                tr("previous", language): float(previous),
                tr("variation", language): calc_variation(float(current), float(previous)),
            }
        )
    return pd.DataFrame(records)


def load_milestones(path: Path | None = None, selected_months: list[str] | None = None) -> list[Milestone]:
    path = path or MILESTONES_PATH
    if not path.exists():
        return []
    try:
        frame = pd.read_csv(path, comment="#")  # skip commented instruction lines
    except (OSError, pd.errors.ParserError, UnicodeDecodeError):
        return []
    required = {"Mes", "Titulo", "Descricao", "Ativo"}
    if frame.empty or not required.issubset(frame.columns):
        return []
    # Filter only truly active rows with non-empty title/description
    active = frame[
        frame["Ativo"].astype(str).str.strip().str.casefold().isin({"1", "true", "sim", "yes", "oui"})
        & frame["Titulo"].astype(str).str.strip().ne("")
        & frame["Descricao"].astype(str).str.strip().ne("")
    ].copy()
    if selected_months:
        active = active[active["Mes"].astype(str).isin(selected_months)]
    if active.empty:
        return []
    return [
        Milestone(str(row["Mes"]), str(row["Titulo"]), str(row["Descricao"]))
        for _, row in active.iterrows()
    ]


def normalized_rate_table(
    data: dict[str, Any],
    selected_months: list[str],
    selected_units: list[str],
) -> pd.DataFrame:
    population = load_population()
    if population.empty:
        return pd.DataFrame()
    absences = unit_period_ranking(data, selected_months, selected_units, "Afastamentos")
    lost_days = unit_period_ranking(data, selected_months, selected_units, "Dias Perdidos")
    absence_rate = add_rate_per_100(absences, population=population, rate_column="Afastamentos por 100")
    lost_rate = add_rate_per_100(lost_days, population=population, rate_column="Dias perdidos por 100")
    if absence_rate.empty and lost_rate.empty:
        return pd.DataFrame()
    left = absence_rate[["Unidade", "Populacao", "Afastamentos por 100"]] if not absence_rate.empty else pd.DataFrame(columns=["Unidade", "Populacao", "Afastamentos por 100"])
    right = lost_rate[["Unidade", "Dias perdidos por 100"]] if not lost_rate.empty else pd.DataFrame(columns=["Unidade", "Dias perdidos por 100"])
    return left.merge(right, on="Unidade", how="outer").sort_values("Dias perdidos por 100", ascending=False, na_position="last")


def data_readiness_table(
    *,
    validation_score: float,
    fallback_used: bool,
    source_stale: bool,
    language: str = "pt",
) -> pd.DataFrame:
    language = normalize_language(language)
    population = load_population()
    targets = load_unit_targets()
    milestones = load_milestones()
    if language == "en":
        labels = ["Validated data quality", "Remote source", "Population denominators", "Unit targets", "Operational milestones"]
        ready = "Ready"
        pending = "Pending configuration"
        contingency = "Fallback active"
        attention = "Review freshness"
    elif language == "fr":
        labels = ["Qualité validée", "Source distante", "Effectifs par unité", "Objectifs par unité", "Jalons opérationnels"]
        ready = "Prêt"
        pending = "Configuration requise"
        contingency = "Mode secours actif"
        attention = "Vérifier la fraîcheur"
    else:
        labels = ["Qualidade validada", "Fonte remota", "População por unidade", "Metas por unidade", "Marcos operacionais"]
        ready = "Pronto"
        pending = "Configuração pendente"
        contingency = "Contingência ativa"
        attention = "Revisar atualização"
    source_status = contingency if fallback_used else attention if source_stale else ready
    values = [
        f"{validation_score:.0f}%",
        source_status,
        f"{len(population)}/{len(UNITS)}" if not population.empty else pending,
        str(len(targets)) if not targets.empty else pending,
        str(len(milestones)) if milestones else pending,
    ]
    return pd.DataFrame({tr("metric", language): labels, tr("status", language): values})


def executive_recommendations(
    data: dict[str, Any],
    selected_months: list[str],
    selected_units: list[str],
    monthly_metrics: pd.DataFrame,
    *,
    language: str = "pt",
) -> list[tuple[str, str, str]]:
    """Return at most four grounded management priorities."""
    language = normalize_language(language)
    kpis = compute_overview_kpis(data, selected_months, selected_units)
    ranking = unit_period_ranking(data, selected_months, selected_units, "Dias Perdidos")
    reasons = reason_pareto_table(data, selected_months)
    mental_current, mental_previous = mental_latest(monthly_metrics)
    periodic_current, _ = periodic_coverage(data, selected_months)
    recommendations: list[tuple[str, str, str]] = []

    def text(pt: str, en: str, fr: str) -> str:
        return {"pt": pt, "en": en, "fr": fr}[language]

    current_days = float(kpis["absenteismo"]["current"])
    target_days = float(TARGETS["absenteismo_monthly_max"])
    if current_days > 0:  # mostra sempre que houver dias, sem checar meta
        recommendations.append((
            "🚨",
            text("Absenteísmo", "Absenteeism", "Absentéisme"),
            text(
                f"Foram registrados {current_days:,.0f} dias perdidos no mês de referência.",
                f"{current_days:,.0f} lost days were recorded in the reference month.",
                f"{current_days:,.0f} jours perdus ont été enregistrés au cours du mois de référence.",
            ),
        ))
    if not ranking.empty:
        top = ranking.iloc[0]
        recommendations.append((
            "🏭",
            text(f"Concentrar ação na unidade {top['Unidade']}", f"Focus action on {top['Unidade']}", f"Concentrer l’action sur {top['Unidade']}"),
            text(
                f"A unidade representa {float(top['Participação (%)']):.1f}% dos dias perdidos do período.",
                f"The unit represents {float(top['Participação (%)']):.1f}% of lost days in the period.",
                f"L’unité représente {float(top['Participação (%)']):.1f}% des jours perdus de la période.",
            ),
        ))
    if not reasons.empty:
        reason = reasons.iloc[0]
        recommendations.append((
            "🎯",
            text(f"Atuar sobre {str(reason['Motivo']).lower()}", f"Act on {str(reason['Motivo']).lower()}", f"Agir sur {str(reason['Motivo']).lower()}"),
            text(
                f"Esse motivo concentra {float(reason['Participação (%)']):.1f}% dos afastamentos classificados.",
                f"This reason accounts for {float(reason['Participação (%)']):.1f}% of classified leaves.",
                f"Ce motif représente {float(reason['Participação (%)']):.1f}% des arrêts classés.",
            ),
        ))
    if periodic_current >= 0:  # mostra sempre, sem checar meta
        recommendations.append((
            "🧪",
            text("Exames periódicos", "Periodic exams", "Examens périodiques"),
            text(
                f"A cobertura está em {periodic_current:.1f}%.",
                f"Coverage is {periodic_current:.1f}%.",
                f"La couverture est de {periodic_current:.1f}%.",
            ),
        ))
    if mental_current > TARGETS["mental_cases_max"] or mental_current > mental_previous:
        recommendations.append((
            "🧠",
            text("Acompanhar a evolução do SRQ-20", "Monitor SRQ-20 progression", "Suivre l’évolution du SRQ-20"),
            text(
                f"O último mês registrou {mental_current:,.0f} casos alterados; acompanhe a tendência por unidade preservando a confidencialidade.",
                f"The latest month recorded {mental_current:,.0f} positive cases; monitor the unit trend while preserving confidentiality.",
                f"Le dernier mois compte {mental_current:,.0f} cas positifs ; suivre la tendance par unité en préservant la confidentialité.",
            ),
        ))

    if not recommendations:
        recommendations.append((
            "✅",
            text("Manter o acompanhamento preventivo", "Maintain preventive monitoring", "Maintenir le suivi préventif"),
            text("Nenhum limite crítico foi ultrapassado no escopo atual.", "No critical threshold was exceeded in the current scope.", "Aucun seuil critique n’a été dépassé dans le périmètre actuel."),
        ))
    return recommendations[:4]


def executive_narrative_i18n(
    data: dict[str, Any],
    selected_months: list[str],
    selected_units: list[str],
    monthly_metrics: pd.DataFrame,
    *,
    language: str = "pt",
) -> str:
    language = normalize_language(language)
    kpis = compute_overview_kpis(data, selected_months, selected_units)
    ranking = unit_period_ranking(data, selected_months, selected_units, "Dias Perdidos")
    reasons = reason_pareto_table(data, selected_months)
    mental_current, _ = mental_latest(monthly_metrics)
    top_unit = str(ranking.iloc[0]["Unidade"]) if not ranking.empty else "—"
    top_share = float(ranking.iloc[0]["Participação (%)"]) if not ranking.empty else 0.0
    top_reason = str(reasons.iloc[0]["Motivo"]) if not reasons.empty else "—"
    reason_share = float(reasons.iloc[0]["Participação (%)"]) if not reasons.empty else 0.0
    exams_total = float(kpis["exames"]["total"])
    appointments_total = float(kpis["atendimentos"]["total"])
    days_total = float(kpis["absenteismo"]["total"])
    active_current = float(kpis["afastamentos"]["current"])


# ---------------------------------------------------------------------------
# DATA QUALITY & COMPLETENESS (New improvement - fully data-driven)
# ---------------------------------------------------------------------------

def data_quality_summary(
    data: dict[str, Any],
    selected_months: list[str],
) -> dict[str, Any]:
    """Return a structured summary of data completeness based only on real loaded data."""
    summary: dict[str, Any] = {
        "has_data": False,
        "recognized_months": [],
        "last_month_with_data": None,
        "completeness_pct": 0.0,
        "missing_months": [],
        "notes": [],
    }

    if not data or not selected_months:
        summary["notes"].append("Nenhum dado carregado ou período selecionado.")
        return summary

    # Try to extract month columns from different possible structures
    month_cols: list[str] = []
    for key in ["exames", "afastamentos", "saude_mental"]:
        section = data.get(key, {})
        if isinstance(section, dict):
            if "month_cols" in section:
                month_cols = section["month_cols"]
                break
            # Fallback: look for common month keys inside dataframes
            for df_key in ["volume", "por_motivo", "mensal"]:
                df = section.get(df_key)
                if isinstance(df, pd.DataFrame) and not df.empty:
                    possible_months = [c for c in df.columns if str(c).upper() in 
                                       ["JANEIRO","FEVEREIRO","MARÇO","ABRIL","MAIO","JUNHO",
                                        "JULHO","AGOSTO","SETEMBRO","OUTUBRO","NOVEMBRO","DEZEMBRO",
                                        "JAN","FEV","MAR","ABR","MAI","JUN","JUL","AGO","SET","OUT","NOV","DEZ"]]
                    if possible_months:
                        month_cols = possible_months
                        break

    if not month_cols:
        # Fallback to selected_months
        month_cols = selected_months

    summary["recognized_months"] = month_cols
    summary["has_data"] = True

    # Determine last month with actual data (non-null in key metrics)
    last_with_data = None
    for m in reversed(month_cols):
        has_value = False
        for section_name in ["exames", "saude_mental"]:  # safe sections only
            section = data.get(section_name, {})
            if isinstance(section, dict):
                for df in section.values():
                    if isinstance(df, pd.DataFrame) and m in df.columns:
                        if df[m].notna().any():
                            has_value = True
                            break
        if has_value:
            last_with_data = m
            break

    summary["last_month_with_data"] = last_with_data or (month_cols[-1] if month_cols else None)

    # Completeness calculation
    months_with_data = sum(1 for m in selected_months if m in month_cols)
    if selected_months:
        summary["completeness_pct"] = round((months_with_data / len(selected_months)) * 100, 1)

    summary["missing_months"] = [m for m in selected_months if m not in month_cols]

    # Enriching: add record counts and freshness (from metadata if available)
    metadata = data.get("metadata", {})
    summary["record_counts"] = metadata.get("record_counts", {})
    summary["source_filename"] = metadata.get("source_filename", "—")
    summary["updated_at"] = metadata.get("updated_at")

    if summary["last_month_with_data"]:
        summary["notes"].append(f"Dados disponíveis até {summary['last_month_with_data']}.")

    if summary["missing_months"]:
        summary["notes"].append(f"Meses sem dados no período: {', '.join(summary['missing_months'])}.")

    return summary

    if language == "en":
        return (
            f"From {selected_months[0]} to {selected_months[-1]}, {exams_total:,.0f} exams and {appointments_total:,.0f} appointments were recorded. "
            f"The period accumulated {days_total:,.0f} lost days; the latest month closed with {active_current:,.0f} active leaves and {mental_current:,.0f} positive SRQ-20 cases. "
            f"{top_unit} concentrated {top_share:.1f}% of lost days, while {top_reason.lower()} was the leading classified reason ({reason_share:.1f}%)."
        )
    if language == "fr":
        return (
            f"De {selected_months[0]} à {selected_months[-1]}, {exams_total:,.0f} examens et {appointments_total:,.0f} consultations ont été enregistrés. "
            f"La période totalise {days_total:,.0f} jours perdus ; le dernier mois compte {active_current:,.0f} arrêts actifs et {mental_current:,.0f} cas SRQ-20 positifs. "
            f"{top_unit} concentre {top_share:.1f}% des jours perdus, tandis que {top_reason.lower()} est le principal motif classé ({reason_share:.1f}%)."
        )
    return (
        f"Entre {selected_months[0]} e {selected_months[-1]}, foram registrados {exams_total:,.0f} exames e {appointments_total:,.0f} atendimentos. "
        f"O período acumulou {days_total:,.0f} dias perdidos; o último mês encerrou com {active_current:,.0f} afastamentos ativos e {mental_current:,.0f} casos SRQ-20 alterados. "
        f"A unidade {top_unit} concentrou {top_share:.1f}% dos dias perdidos, enquanto {top_reason.lower()} foi o principal motivo classificado ({reason_share:.1f}%)."
    ).replace(",", ".")
