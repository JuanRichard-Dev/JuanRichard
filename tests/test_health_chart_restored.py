from pathlib import Path

from src.transforms import compute_health_score_breakdown, get_available_months
from src.data_loader import load_all_data, get_data_file_signature

ROOT = Path(__file__).resolve().parents[1]


def test_health_visual_renderer_and_side_cards_are_present():
    app = (ROOT / "app.py").read_text(encoding="utf-8")
    components = (ROOT / "src" / "components.py").read_text(encoding="utf-8")
    styles = (ROOT / "src" / "styles.py").read_text(encoding="utf-8")
    assert "render_health_score_radial(health_score)" in app
    assert "health-score-visual-ring" in components
    assert "conic-gradient" in styles
    assert "max-width: 920px" in styles


def test_presence_component_uses_requested_name():
    path = ROOT / "Dashboard SM CGR 2026.xlsx"
    signature = get_data_file_signature(path)
    data = load_all_data(signature, "v10.5.5-test", str(path))
    months = get_available_months(data)
    frame = compute_health_score_breakdown(data, months, ["B2BN"])
    assert frame["Componente"].tolist() == ["Exames periódicos", "Presença no Periódico"]
