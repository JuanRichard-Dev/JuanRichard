"""Smoke tests for the five current dashboard pages."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

PAGES = ["Resumo Executivo", "Exames", "Atendimentos", "Afastamentos", "Saúde Mental"]


def test_all_current_pages_execute() -> None:
    runner = Path(__file__).with_name("smoke_runner.py")
    for page in PAGES:
        result = subprocess.run(
            [sys.executable, str(runner), page],
            capture_output=True,
            text=True,
            timeout=60,
        )
        assert result.returncode == 0, result.stdout + "\n" + result.stderr
