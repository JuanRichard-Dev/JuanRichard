"""Integration tests executed by Streamlit's official AppTest runner."""

from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

try:
    from streamlit.testing.v1 import AppTest
except ModuleNotFoundError:  # Streamlit is installed by requirements.txt on the host.
    AppTest = None


@unittest.skipIf(AppTest is None, "Streamlit testing runtime is not installed")
class DashboardAppIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.project_root = Path(__file__).resolve().parents[1]
        cls.app_path = cls.project_root / "app.py"
        cls.runtime = tempfile.TemporaryDirectory()
        cls.previous_environment = {
            key: os.environ.get(key)
            for key in (
                "DATA_SOURCE",
                "DATA_LOCAL_PATH",
                "AUTO_REFRESH_ENABLED",
                "LOCAL_RUNTIME_DIR",
            )
        }
        os.environ.update(
            {
                "DATA_SOURCE": "local",
                "DATA_LOCAL_PATH": str(cls.project_root / "Dashboard SM CGR 2026.xlsx"),
                "AUTO_REFRESH_ENABLED": "false",
                "LOCAL_RUNTIME_DIR": cls.runtime.name,
            }
        )

    @classmethod
    def tearDownClass(cls) -> None:
        for key, value in cls.previous_environment.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
        cls.runtime.cleanup()

    def test_all_analytical_pages_render_without_exceptions(self) -> None:
        app = AppTest.from_file(str(self.app_path), default_timeout=40).run()
        self.assertEqual(list(app.exception), [])

        pages = ["Resumo Executivo", "Visão Geral", "Exames", "Atendimentos", "Afastamentos", "Saúde Mental"]
        for page in pages:
            with self.subTest(page=page):
                navigation = next(
                    radio for radio in app.radio
                    if radio.label == "Navegação principal"
                )
                navigation.set_value(page).run(timeout=40)
                self.assertEqual(list(app.exception), [])

    def test_empty_month_selection_shows_safe_empty_state(self) -> None:
        app = AppTest.from_file(str(self.app_path), default_timeout=40).run()
        month_filter = next(
            widget for widget in app.multiselect
            if widget.label == "Meses de análise"
        )
        month_filter.set_value([]).run(timeout=40)
        self.assertEqual(list(app.exception), [])
        rendered_text = " ".join(item.value for item in app.markdown)
        self.assertIn("Nenhum mês selecionado", rendered_text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
