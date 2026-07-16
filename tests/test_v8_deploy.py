"""V8 deployment, reporting, source and normalization tests."""

from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import pandas as pd

from src.config import DATA_SCHEMA_VERSION, UNITS
from src.data_loader import get_data_file_signature, load_all_data
from src.data_sources import DataSourceError, prepare_data_source
from src.population import add_rate_per_100, load_population
from src.reporting import build_executive_pdf
from src.transforms import get_available_months
from src.unit_targets import apply_unit_targets, load_unit_targets
from src.url_state import filter_query_values, read_filter_query

ROOT = Path(__file__).resolve().parents[1]
WORKBOOK = ROOT / "Dashboard SM CGR 2026.xlsx"


class DeployReadyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = load_all_data(
            get_data_file_signature(WORKBOOK),
            DATA_SCHEMA_VERSION,
            str(WORKBOOK),
        )
        cls.months = get_available_months(cls.data)

    def test_dynamic_workbook_path_uses_real_data(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            copied = Path(temp_dir) / "copy.xlsx"
            copied.write_bytes(WORKBOOK.read_bytes())
            data = load_all_data(
                get_data_file_signature(copied),
                DATA_SCHEMA_VERSION,
                str(copied),
            )
            self.assertEqual(data["metadata"]["source_filename"], "copy.xlsx")
            self.assertEqual(data["metadata"]["recognized_months"], self.months)
            self.assertFalse(data["metadata"]["uses_sample_data"])

    def test_local_source_is_resolved(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch.dict(
                os.environ,
                {
                    "DATA_SOURCE": "local",
                    "DATA_LOCAL_PATH": str(WORKBOOK),
                    "LOCAL_RUNTIME_DIR": temp_dir,
                },
                clear=False,
            ):
                prepared = prepare_data_source()
        self.assertEqual(prepared.source_type, "local")
        self.assertEqual(Path(prepared.original_path), WORKBOOK.resolve())
        self.assertTrue(prepared.snapshot)
        self.assertNotEqual(prepared.path, WORKBOOK.resolve())
        self.assertEqual(len(prepared.checksum), 64)

    def test_invalid_source_is_rejected(self) -> None:
        with patch.dict(os.environ, {"DATA_SOURCE": "invalid"}, clear=False):
            with self.assertRaises(DataSourceError):
                prepare_data_source()

    def test_shareable_filter_query(self) -> None:
        values = filter_query_values(["Janeiro", "Março"], ["B2BN", "SF"])
        parsed = read_filter_query(
            values,
            available_months=self.months,
            available_units=UNITS,
        )
        self.assertEqual(parsed["months"], ["Janeiro", "Março"])
        self.assertEqual(parsed["units"], ["B2BN", "SF"])

    def test_population_rates_require_real_denominator(self) -> None:
        frame = pd.DataFrame({"Unidade": ["B2BN", "SF"], "Valor": [50, 20]})
        population = pd.DataFrame({"Unidade": ["B2BN", "SF"], "Populacao": [1000, 200]})
        result = add_rate_per_100(frame, population=population)
        self.assertEqual(result["Taxa por 100 colaboradores"].round(1).tolist(), [5.0, 10.0])
        self.assertTrue(load_population(ROOT / "population_by_unit.csv").empty)

    def test_unit_targets_are_optional_and_data_driven(self) -> None:
        self.assertTrue(load_unit_targets(ROOT / "unit_targets.csv").empty)
        frame = pd.DataFrame({"Unidade": ["B2BN"], "Valor": [80]})
        targets = pd.DataFrame(
            {"Indicador": ["Dias Perdidos"], "Unidade": ["B2BN"], "Meta": [100], "Direcao": ["lower"]}
        )
        result = apply_unit_targets(
            frame,
            indicator="Dias Perdidos",
            value_column="Valor",
            targets=targets,
        )
        self.assertEqual(result.iloc[0]["Status"], "Dentro da meta")

    def test_executive_pdf_is_valid(self) -> None:
        pdf = build_executive_pdf(self.data, self.months, UNITS, generated_by="teste")
        self.assertTrue(pdf.startswith(b"%PDF"))
        self.assertGreater(len(pdf), 5000)

    def test_deployment_files_exist(self) -> None:
        expected = [
            "Dockerfile",
            "render.yaml",
            "Procfile",
            ".python-version",
            "DEPLOY.md",
            "SECURITY.md",
            "ARCHITECTURE.md",
            ".streamlit/secrets.toml.example",
            ".github/workflows/ci.yml",
        ]
        for relative in expected:
            with self.subTest(relative=relative):
                self.assertTrue((ROOT / relative).exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
