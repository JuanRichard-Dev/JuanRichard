"""Tests for external, validated dashboard settings."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from src.settings import DEFAULT_SETTINGS, load_dashboard_settings


class SettingsTests(unittest.TestCase):
    def test_missing_file_uses_defaults(self) -> None:
        missing = Path(tempfile.gettempdir()) / "missing-dashboard-settings.json"
        settings = load_dashboard_settings(missing)
        self.assertEqual(settings["targets"]["health_score"], DEFAULT_SETTINGS["targets"]["health_score"])

    def test_partial_file_is_merged_and_validated(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "settings.json"
            path.write_text(
                json.dumps({
                    "targets": {"health_score": 85},
                    "analytics": {"forecast_months": -10},
                }),
                encoding="utf-8",
            )
            settings = load_dashboard_settings(path)
            self.assertEqual(settings["targets"]["health_score"], 85.0)
            self.assertEqual(
                settings["analytics"]["forecast_months"],
                DEFAULT_SETTINGS["analytics"]["forecast_months"],
            )
            self.assertIn("periodicos_pct", settings["targets"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
