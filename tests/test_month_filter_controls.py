"""Regression tests for month and slicer selection controls."""

from __future__ import annotations

import unittest
from pathlib import Path

from src.filters import build_filter_state


class MonthFilterControlTests(unittest.TestCase):
    def setUp(self) -> None:
        self.available = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio"]

    def test_empty_selection_remains_empty(self) -> None:
        state = build_filter_state(
            months=[],
            available_months=self.available,
            units=[],
            exams=[],
            appointments=[],
            reasons=[],
            available_exams=["Periódicos"],
            available_appointments=["Atendimento Médico"],
            available_reasons=["Clínicos"],
        )
        self.assertEqual(state.months, ())
        self.assertEqual(state.units, ())
        self.assertEqual(state.exams, ())
        self.assertEqual(state.appointments, ())
        self.assertEqual(state.reasons, ())

    def test_single_month_is_supported(self) -> None:
        state = build_filter_state(
            months=["Março"],
            available_months=self.available,
            units=["B2BN"],
        )
        self.assertEqual(state.months, ("Março",))

    def test_all_months_are_supported(self) -> None:
        state = build_filter_state(
            months=self.available,
            available_months=self.available,
            units=["B2BN"],
        )
        self.assertEqual(state.months, tuple(self.available))

    def test_months_are_returned_in_calendar_order(self) -> None:
        state = build_filter_state(
            months=["Maio", "Janeiro", "Março"],
            available_months=self.available,
            units=["B2BN"],
        )
        self.assertEqual(state.months, ("Janeiro", "Março", "Maio"))

    def test_app_contains_quick_period_and_all_clear_controls(self) -> None:
        app_text = (
            Path(__file__).resolve().parents[1] / "app.py"
        ).read_text(encoding="utf-8")

        for label in [
            "Último mês",
            "Últimos 3",
            "Todos os meses",
            "Limpar meses",
            "_render_all_clear_buttons",
        ]:
            self.assertIn(label, app_text)
        self.assertIn("if not selected_months:", app_text)
        self.assertNotIn(") or month_cols.copy()", app_text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
