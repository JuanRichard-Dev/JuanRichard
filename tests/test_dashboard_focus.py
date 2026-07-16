"""Tests for the analytics-only Power BI style navigation."""

from __future__ import annotations

import unittest

from src.config import PAGE_ICONS, PAGE_NAMES


class DashboardFocusTests(unittest.TestCase):
    def test_only_analytical_pages_are_exposed(self) -> None:
        self.assertEqual(
            PAGE_NAMES,
            [
                "Resumo Executivo",
                "Visão Geral",
                "Exames",
                "Atendimentos",
                "Afastamentos",
                "Saúde Mental",
            ],
        )
        self.assertEqual(len(PAGE_NAMES), len(PAGE_ICONS))

    def test_administrative_pages_are_not_exposed(self) -> None:
        forbidden = {
            "Qualidade dos Dados",
            "Exportações",
            "Planos de Ação",
        }
        self.assertTrue(forbidden.isdisjoint(PAGE_NAMES))


if __name__ == "__main__":
    unittest.main(verbosity=2)
