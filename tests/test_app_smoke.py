"""Smoke test every analytical page without requiring a browser."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


class AppPageSmokeTests(unittest.TestCase):
    def test_all_pages_execute_with_real_workbook(self) -> None:
        runner = Path(__file__).with_name("smoke_runner.py")
        pages = ["Resumo Executivo", "Visão Geral", "Exames", "Atendimentos", "Afastamentos", "Saúde Mental"]
        for page in pages:
            with self.subTest(page=page):
                result = subprocess.run(
                    [sys.executable, str(runner), page],
                    capture_output=True,
                    text=True,
                    timeout=60,
                )
                self.assertEqual(result.returncode, 0, msg=result.stdout + "\n" + result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
