"""Regression coverage for the V10.1.2 native-runtime stability hotfix."""

from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

try:
    from streamlit.testing.v1 import AppTest
except ModuleNotFoundError:
    AppTest = None


ROOT = Path(__file__).resolve().parents[1]


class StabilityConfigurationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.app_text = (ROOT / "app.py").read_text(encoding="utf-8")
        cls.requirements = (ROOT / "requirements.txt").read_text(encoding="utf-8")

    def test_cloud_runtime_is_pinned_to_python_312(self) -> None:
        self.assertEqual((ROOT / ".python-version").read_text().strip(), "3.12.11")
        self.assertEqual((ROOT / "runtime.txt").read_text().strip(), "python-3.12.11")

    def test_core_dependencies_are_reproducibly_pinned(self) -> None:
        required_exact = (
            "streamlit==1.58.0",
            "pandas==2.3.3",
            "numpy==2.3.5",
            "pyarrow==20.0.0",
            "plotly==6.5.2",
        )
        for pin in required_exact:
            with self.subTest(pin=pin):
                self.assertIn(pin, self.requirements)
        self.assertNotIn("psycopg", self.requirements.casefold())
        self.assertNotIn("sqlalchemy", self.requirements.casefold())
        self.assertNotIn("streamlit[auth]", self.requirements.casefold())

    def test_native_worker_pools_and_faulthandler_are_enabled_before_pandas(self) -> None:
        pandas_position = self.app_text.index("import pandas as pd")
        self.assertLess(self.app_text.index('"OPENBLAS_NUM_THREADS"'), pandas_position)
        self.assertLess(self.app_text.index("faulthandler.enable"), pandas_position)

    def test_hot_path_avoids_arrow_styler_serialization(self) -> None:
        self.assertNotIn("st.dataframe(", self.app_text)
        self.assertIn("styler.to_html()", self.app_text)

    def test_reportlab_is_lazy_loaded(self) -> None:
        self.assertNotIn("from src.reporting import build_executive_pdf  # noqa", self.app_text)
        self.assertIn("from src.reporting import build_executive_pdf", self.app_text)


@unittest.skipIf(AppTest is None, "Streamlit testing runtime is not installed")
class StabilityRerunStressTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.runtime = tempfile.TemporaryDirectory()
        cls.previous = {
            key: os.environ.get(key)
            for key in ("DATA_SOURCE", "DATA_LOCAL_PATH", "AUTO_REFRESH_ENABLED", "LOCAL_RUNTIME_DIR")
        }
        os.environ.update(
            {
                "DATA_SOURCE": "local",
                "DATA_LOCAL_PATH": str(ROOT / "Dashboard SM CGR 2026.xlsx"),
                "AUTO_REFRESH_ENABLED": "false",
                "LOCAL_RUNTIME_DIR": cls.runtime.name,
            }
        )

    @classmethod
    def tearDownClass(cls) -> None:
        for key, value in cls.previous.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
        cls.runtime.cleanup()

    def test_repeated_month_filter_reruns_remain_clean(self) -> None:
        app = AppTest.from_file(str(ROOT / "app.py"), default_timeout=40).run()
        self.assertEqual(list(app.exception), [])
        sequences = [
            ["Fevereiro", "Março", "Abril", "Maio", "Junho"],
            ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho"],
            ["Abril", "Maio", "Junho"],
            ["Junho"],
        ]
        for index in range(24):
            month_filter = next(widget for widget in app.multiselect if widget.label == "Meses de análise")
            month_filter.set_value(sequences[index % len(sequences)]).run(timeout=40)
            self.assertEqual(list(app.exception), [], f"rerun {index + 1} failed")


if __name__ == "__main__":
    unittest.main(verbosity=2)
