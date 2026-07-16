from pathlib import Path

from src.charts import grouped_bar_chart, percent_stacked_bar_chart
from src.responsive import calculate_chart_height, compact_month_labels
from src.styles import get_css

ROOT = Path(__file__).resolve().parents[1]


def test_removed_sidebar_actions_are_not_rendered():
    app = (ROOT / "app.py").read_text(encoding="utf-8")
    assert "Conferir impacto dos filtros" not in app
    assert "Fonte e cobertura" not in app
    assert "Dicionário de métricas" not in app
    assert "prepare_pdf_v8" in app
    assert "download_pdf_v8" in app


def test_notebook_grid_and_sidebar_restore_are_present():
    css = get_css()
    assert "@media (max-width: 1439px)" in css
    assert ':has(div[data-testid="stPlotlyChart"])' in css
    assert 'button[data-testid="stSidebarCollapseButton"]' in css
    assert "visibility: visible" in css


def test_dropdown_popover_keeps_native_geometry():
    css = get_css()
    final_section = css[css.rfind("V10.5.3 — NOTEBOOK-FIRST RESPONSIVE RETROFIT"):]
    assert 'body [data-baseweb="popover"]' in final_section
    assert "width: max-content" not in final_section
    assert "background: #0D2239" in final_section


def test_composition_chart_reserves_legend_space():
    months = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho"]
    data = {
        "Atendimento Médico": [238, 368, 493, 456, 490, 512],
        "Atendimento de Enfermagem": [104, 63, 83, 120, 79, 123],
        "Atendimento Fisioterapêutico Total": [222, 208, 284, 318, 319, 260],
        "Atendimento Fisioterapêutico Horista": [128, 138, 177, 217, 211, 206],
        "Atendimento Fisioterapêutico Mensalista": [94, 70, 107, 98, 108, 54],
        "CAT (Comunicado de Acidente de Trabalho)": [3, 3, 2, 3, 1, 3],
    }
    fig = percent_stacked_bar_chart(data, months, "Composição Mensal")
    assert fig.layout.height >= 450
    assert fig.layout.margin.t >= 100
    assert fig.layout.legend.orientation == "h"
    assert all("customdata[2]" in trace.hovertemplate for trace in fig.data)


def test_hourly_monthly_chart_keeps_labels_visible():
    months = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho"]
    fig = grouped_bar_chart(
        {"Horista": [128, 138, 177, 217, 211, 206], "Mensalista": [94, 70, 107, 98, 108, 54]},
        months,
        "Horistas versus Mensalistas",
    )
    assert fig.layout.height >= 430
    assert fig.layout.margin.r >= 60
    assert all(trace.cliponaxis is False for trace in fig.data)


def test_height_and_month_helpers():
    assert calculate_chart_height("composition", category_count=6, series_count=7, legend_rows=3) >= 450
    months = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto"]
    assert compact_month_labels(months) == ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago"]
