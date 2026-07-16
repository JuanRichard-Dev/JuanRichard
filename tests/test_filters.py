"""Regression tests executed exclusively against the delivered real workbook."""

from __future__ import annotations

import unittest

from src.config import DATA_SCHEMA_VERSION, UNITS, canonicalize_unit
from src.data_loader import get_data_file_signature, load_all_data
from src.transforms import (
    compute_absenteismo_by_cause,
    compute_absenteismo_by_gender,
    compute_health_score,
    compute_overview_kpis,
    filter_saude_mental_by_units,
    get_available_months,
    normalize_selected_months,
)


class RealWorkbookFilterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = load_all_data(get_data_file_signature(), DATA_SCHEMA_VERSION)
        cls.months = get_available_months(cls.data)

    def test_source_is_real_workbook(self) -> None:
        metadata = self.data["metadata"]
        self.assertEqual(metadata["source_filename"], "Dashboard SM CGR 2026.xlsx")
        self.assertFalse(metadata["uses_sample_data"])
        self.assertEqual(metadata["source_sheets"], ["Principal", "Absenteísmo", "Saúde Mental"])

    def test_recognized_months_match_filled_principal_period(self) -> None:
        metadata_months = self.data["metadata"]["recognized_months"]
        self.assertEqual(self.months, metadata_months)
        self.assertGreaterEqual(len(self.months), 1)
        selected = [self.months[-1], self.months[0]]
        self.assertEqual(normalize_selected_months(selected, self.months), [self.months[0], self.months[-1]])

    def test_sao_francisco_alias_remains_sf(self) -> None:
        self.assertEqual(canonicalize_unit("São Francisco"), "SF")
        self.assertIn("SF", UNITS)
        self.assertNotIn("São Francisco", UNITS)

    def test_unit_filter_changes_real_kpis(self) -> None:
        b2bn = compute_overview_kpis(self.data, tuple(self.months), ("B2BN",))
        sf = compute_overview_kpis(self.data, tuple(self.months), ("SF",))

        self.assertGreaterEqual(b2bn["afastamentos"]["current"], 0)
        self.assertGreaterEqual(sf["afastamentos"]["current"], 0)
        self.assertGreater(b2bn["absenteismo"]["total"], 0)
        self.assertGreater(sf["absenteismo"]["total"], 0)
        self.assertNotEqual(b2bn["absenteismo"]["total"], sf["absenteismo"]["total"])

    def test_health_score_uses_only_active_components(self) -> None:
        b2bn = compute_health_score(self.data, self.months, ["B2BN"])
        all_units = compute_health_score(self.data, self.months, UNITS)
        self.assertAlmostEqual(b2bn, all_units)
        self.assertGreaterEqual(b2bn, 0)
        self.assertLessEqual(b2bn, 100)

    def test_mental_health_filter_uses_real_rows(self) -> None:
        filtered = filter_saude_mental_by_units(self.data["saude_mental"], ["SF"])
        self.assertEqual(filtered["unidade"].tolist(), ["SF"])
        self.assertEqual(int(filtered["Maio"].sum()), 0)

    def test_absenteeism_breakdowns_match_real_workbook(self) -> None:
        categories, gender = compute_absenteismo_by_gender(
            self.data["absenteismo"], ["B2BN"], ["Maio"]
        )
        self.assertEqual(categories, ["B2BN"])
        self.assertEqual(gender["Homens"], [367])
        self.assertEqual(gender["Mulheres"], [100])

        categories, causes = compute_absenteismo_by_cause(
            self.data["absenteismo"], ["SF"], ["Maio"]
        )
        self.assertEqual(categories, ["SF"])
        self.assertEqual(causes["Clínicas"], [231])
        self.assertEqual(causes["Psiquiátricas"], [16])


if __name__ == "__main__":
    unittest.main(verbosity=2)
