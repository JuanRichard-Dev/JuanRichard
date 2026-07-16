from pathlib import Path

from src.charts import bar_chart, health_score_radial_chart, percent_stacked_bar_chart
from src.data_loader import get_data_file_signature, load_all_data
from src.responsive import apply_figure_safety
from src.transforms import compute_health_score_breakdown, get_available_months

ROOT = Path(__file__).resolve().parents[1]


def test_global_title_safety_moves_title_away_from_svg_edge():
    fig = bar_chart(
        __import__("pandas").DataFrame({"Mês": ["Janeiro", "Fevereiro"], "Valor": [10, 20]}),
        "Mês", "Valor", "Motivos no período<br><sup>Período: Janeiro a Junho</sup>", "#4A8DFF"
    )
    apply_figure_safety(fig)
    assert float(fig.layout.title.y) <= 0.94
    assert int(fig.layout.margin.t) >= 84
    assert int(fig.layout.title.pad.t) >= 8


def test_multiline_chart_title_keeps_reserved_space():
    fig = percent_stacked_bar_chart(
        {"Periódicos": [10, 20], "Demissionais": [5, 8]},
        ["Janeiro", "Fevereiro"],
        "Participação dos tipos de exame<br><sup>Período: Janeiro a Junho</sup>",
    )
    apply_figure_safety(fig)
    assert int(fig.layout.margin.t) >= 84


def test_health_breakdown_contains_only_active_components():
    workbook = ROOT / "Dashboard SM CGR 2026.xlsx"
    data = load_all_data(get_data_file_signature(workbook), "v10.5.4", str(workbook))
    months = get_available_months(data)
    frame = compute_health_score_breakdown(data, months, ["B2BN"])
    assert frame["Componente"].tolist() == ["Exames periódicos", "Presença no Periódico"]
    assert frame["Peso"].tolist() == ["50%", "50%"]
    assert "Meta" not in frame.columns


def test_radial_health_chart_has_no_status_or_target_copy():
    fig = health_score_radial_chart(48.2, target=80.0)
    annotations = " ".join(str(item.text) for item in fig.layout.annotations)
    assert "CRÍTICO" not in annotations
    assert "Referência" not in annotations
    assert "80%" not in annotations
