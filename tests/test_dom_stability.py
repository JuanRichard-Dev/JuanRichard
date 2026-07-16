"""Regression tests for a native, mutation-free Streamlit frontend."""

from __future__ import annotations

import unittest
from pathlib import Path


class DomStabilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).resolve().parents[1]
        cls.app_text = (cls.root / "app.py").read_text(encoding="utf-8")
        cls.requirements = (cls.root / "requirements.txt").read_text(encoding="utf-8").lower()

    def test_third_party_navigation_is_removed(self) -> None:
        self.assertNotIn("streamlit_option_menu", self.app_text)
        self.assertNotIn("option_menu(", self.app_text)
        self.assertNotIn("streamlit-option-menu", self.requirements)

    def test_native_radio_navigation_is_used(self) -> None:
        self.assertIn("main_navigation_native_v8", self.app_text)
        self.assertIn("page = st.radio(", self.app_text)

    def test_no_custom_dom_script_is_used(self) -> None:
        forbidden = [
            "streamlit.components",
            "MutationObserver",
            "insertBefore",
            "removeChild",
            "window.parent.document",
            "<script>",
        ]
        for token in forbidden:
            with self.subTest(token=token):
                self.assertNotIn(token, self.app_text)

    def test_plotly_scroll_zoom_is_disabled(self) -> None:
        self.assertIn('"scrollZoom": False', self.app_text)
        self.assertIn('"responsive": True', self.app_text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
