"""Static tests for the responsive health score layout."""

from __future__ import annotations

import unittest
from pathlib import Path


class ResponsiveHealthLayoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).resolve().parents[1]
        cls.app = (cls.root / "app.py").read_text(encoding="utf-8")
        cls.styles = (cls.root / "src/styles.py").read_text(encoding="utf-8")
        cls.components = (cls.root / "src/components.py").read_text(encoding="utf-8")

    def test_overview_uses_new_responsive_section(self) -> None:
        self.assertIn('key="health_score_section"', self.app)
        self.assertIn("render_health_score_radial(health_score)", self.app)
        self.assertIn("render_health_score_breakdown_cards(", self.app)
        self.assertNotIn("health-score-gauge", self.app)

    def test_responsive_breakpoints_exist(self) -> None:
        self.assertIn("@media (max-width: 1180px)", self.styles)
        self.assertIn("@media (max-width: 760px)", self.styles)
        self.assertIn("@media (max-width: 430px)", self.styles)
        self.assertIn("flex-wrap: wrap !important", self.styles)
        self.assertIn("grid-template-columns: 1fr", self.styles)

    def test_breakdown_cards_are_built_without_multiline_html(self) -> None:
        self.assertIn('st.markdown(wrapper, unsafe_allow_html=True)', self.components)
        self.assertIn("health-breakdown-grid", self.components)
        self.assertIn("health-clean-card", self.components)
        self.assertNotIn("Meta {target", self.components)


if __name__ == "__main__":
    unittest.main(verbosity=2)
