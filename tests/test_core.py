"""Small regression suite for the current repository structure."""
from __future__ import annotations

import py_compile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_required_runtime_files_exist() -> None:
    required = [
        "app.py",
        "requirements.txt",
        ".streamlit/config.toml",
        "Dashboard SM CGR 2026.xlsx",
        "population_by_unit.csv",
    ]
    for relative in required:
        assert (ROOT / relative).exists(), relative


def test_app_compiles() -> None:
    py_compile.compile(str(ROOT / "app.py"), doraise=True)


def test_v22_controls_use_neutral_blue_palette() -> None:
    styles = (ROOT / "src" / "styles.py").read_text(encoding="utf-8")
    config = (ROOT / ".streamlit" / "config.toml").read_text(encoding="utf-8")
    app = (ROOT / "app.py").read_text(encoding="utf-8")
    assert "_v1060_dropdown_roxo" not in styles
    assert "--control-accent:#4C8DFF" in styles
    assert "--control-bg-selected:#1D3150" in styles
    assert 'primaryColor = "#4C8DFF"' in config
    assert 'sort_options = ["Padrão"]' in app
    assert 'sort_by != "Padrão"' in app
    assert "caret-color:transparent" in styles
