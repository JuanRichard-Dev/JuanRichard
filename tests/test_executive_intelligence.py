"""Tests for V10.5 executive intelligence features."""

from pathlib import Path

import pandas as pd

from src.config import DATA_SCHEMA_VERSION
from src.data_loader import get_data_file_signature, load_all_data
from src.executive_intelligence import (
    data_readiness_table,
    executive_comparison_table,
    executive_narrative_i18n,
    executive_recommendations,
    load_milestones,
    severity_proxy,
)
from src.analytics import executive_metric_series
from src.i18n import page_label, tr
from src.transforms import compute_overview_kpis

ROOT = Path(__file__).resolve().parents[1]

def _data():
    path = ROOT / "Dashboard SM CGR 2026.xlsx"
    return load_all_data(get_data_file_signature(path), DATA_SCHEMA_VERSION, str(path))

def test_languages_and_page_labels():
    assert page_label("Resumo Executivo", "en") == "Executive Summary"
    assert page_label("Resumo Executivo", "fr") == "Synthèse Exécutive"
    assert tr("lost_days", "pt") == "Dias perdidos"

def test_comparison_and_recommendations_are_grounded():
    data = _data()
    months = data["metadata"]["recognized_months"]
    units = ["B2BN", "B2BF", "SF", "SITE", "OUTROS"]
    monthly = executive_metric_series(data, months, units)
    table = executive_comparison_table(data, months, units, monthly, language="pt")
    assert not table.empty
    assert "Indicador" in table.columns
    assert "Status" in table.columns
    recommendations = executive_recommendations(data, months, units, monthly, language="pt")
    assert recommendations
    narrative = executive_narrative_i18n(data, months, units, monthly, language="fr")
    assert "jours perdus" in narrative.lower()

def test_severity_proxy_is_safe():
    data = _data()
    months = data["metadata"]["recognized_months"]
    kpis = compute_overview_kpis(data, months, ["B2BN", "B2BF", "SF", "SITE", "OUTROS"] )
    current, previous = severity_proxy(kpis)
    assert current >= 0
    assert previous >= 0

def test_milestone_template_and_readiness():
    milestones = load_milestones(ROOT / "dashboard_milestones.csv")
    assert milestones == []
    readiness = data_readiness_table(validation_score=92, fallback_used=False, source_stale=False)
    assert isinstance(readiness, pd.DataFrame)
    assert len(readiness) == 5
