"""Regression tests for V10.1 Premium AutoSync and executive theme."""

from __future__ import annotations

import os
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest.mock import patch

from src.data_sources import (
    DEFAULT_GOOGLE_SHEETS_URL,
    DataSourceError,
    _save_snapshot,
    cleanup_snapshot_cache,
    mark_source_valid,
    validate_xlsx_payload,
)
from src.styles import get_css

ROOT = Path(__file__).resolve().parents[1]
WORKBOOK = ROOT / "Dashboard SM CGR 2026.xlsx"


class PremiumAutoSyncTests(unittest.TestCase):
    def test_default_google_sheets_url_is_configured(self) -> None:
        self.assertEqual(
            DEFAULT_GOOGLE_SHEETS_URL,
            "https://docs.google.com/spreadsheets/d/1uvtKSQ4PmUcahUhvHEwrqfyeudb1zNto/export?format=xlsx",
        )

    def test_real_workbook_passes_binary_validation(self) -> None:
        validate_xlsx_payload(WORKBOOK.read_bytes())

    def test_html_login_response_is_rejected(self) -> None:
        with self.assertRaises(DataSourceError):
            validate_xlsx_payload(
                b"<!doctype html><html><body>Login</body></html>",
                content_type="text/html; charset=utf-8",
            )

    def test_non_xlsx_zip_is_rejected(self) -> None:
        with self.assertRaises(DataSourceError):
            validate_xlsx_payload(b"PK-not-a-real-workbook")

    def test_snapshot_retention_keeps_six_latest(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            runtime = Path(temp_dir)
            snapshots = runtime / "snapshots"
            snapshots.mkdir(parents=True)
            for index in range(8):
                path = snapshots / f"dashboard-{index:02d}.xlsx"
                path.write_bytes(b"test")
                os.utime(path, (index + 1, index + 1))

            with patch.dict(
                os.environ,
                {
                    "LOCAL_RUNTIME_DIR": str(runtime),
                    "KEEP_SOURCE_SNAPSHOTS": "6",
                },
                clear=False,
            ):
                cleanup_snapshot_cache()

            remaining = sorted(item.name for item in snapshots.glob("dashboard-*.xlsx"))
            self.assertEqual(len(remaining), 6)
            self.assertNotIn("dashboard-00.xlsx", remaining)
            self.assertNotIn("dashboard-01.xlsx", remaining)

    def test_concurrent_snapshot_writes_do_not_share_temp_file(self) -> None:
        content = WORKBOOK.read_bytes()
        with tempfile.TemporaryDirectory() as temp_dir:
            runtime = Path(temp_dir) / "runtime"
            with patch.dict(
                os.environ,
                {"LOCAL_RUNTIME_DIR": str(runtime)},
                clear=False,
            ):
                def save_once(_index: int):
                    return _save_snapshot(
                        content,
                        WORKBOOK.name,
                        source_type="google_sheets",
                        display_name=WORKBOOK.name,
                        detail="concurrency regression",
                    )

                with ThreadPoolExecutor(max_workers=12) as executor:
                    prepared_sources = list(executor.map(save_once, range(48)))

                paths = {source.path for source in prepared_sources}
                self.assertEqual(len(paths), 1)
                snapshot = next(iter(paths))
                self.assertTrue(snapshot.exists())
                validate_xlsx_payload(snapshot.read_bytes())
                self.assertFalse(list(snapshot.parent.glob("*.tmp")))

                with ThreadPoolExecutor(max_workers=12) as executor:
                    results = list(executor.map(mark_source_valid, prepared_sources))
                self.assertTrue(all(results))
                self.assertTrue((runtime / "last_valid.xlsx").exists())
                self.assertTrue((runtime / "last_valid.json").exists())
                self.assertFalse(list(runtime.rglob("*.tmp")))

    def test_snapshot_persistence_error_becomes_contingency_error(self) -> None:
        content = WORKBOOK.read_bytes()
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch.dict(
                os.environ,
                {"LOCAL_RUNTIME_DIR": str(Path(temp_dir) / "runtime")},
                clear=False,
            ), patch(
                "src.data_sources._atomic_write_bytes",
                side_effect=PermissionError("read-only runtime"),
            ):
                with self.assertRaisesRegex(DataSourceError, "cópia de contingência"):
                    _save_snapshot(
                        content,
                        WORKBOOK.name,
                        source_type="google_sheets",
                        display_name=WORKBOOK.name,
                        detail="persistence failure regression",
                    )

    def test_power_bi_theme_and_autosync_card_are_present(self) -> None:
        css = get_css()
        self.assertIn("--bg-primary: #081321", css)
        self.assertIn("--bg-card: #10243B", css)
        self.assertIn(".autosync-card", css)
        self.assertIn(".presentation-mode-marker", (ROOT / "app.py").read_text(encoding="utf-8"))
        self.assertIn("Sincronizar agora", (ROOT / "app.py").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
