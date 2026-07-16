"""Tests for the internal OneDrive/SharePoint hosting runtime."""

from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.config import DATA_SCHEMA_VERSION
from src.data_loader import get_data_file_signature, load_all_data
from src.data_sources import (
    mark_source_valid,
    prepare_data_source,
    prepare_last_valid_source,
    quick_file_signature,
)

ROOT = Path(__file__).resolve().parents[1]
WORKBOOK = ROOT / "Dashboard SM CGR 2026.xlsx"


class InternalHostingTests(unittest.TestCase):
    def test_local_source_uses_immutable_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "source.xlsx"
            source.write_bytes(WORKBOOK.read_bytes())
            runtime = Path(temp_dir) / "runtime"

            with patch.dict(
                os.environ,
                {
                    "DATA_SOURCE": "local",
                    "DATA_LOCAL_PATH": str(source),
                    "LOCAL_RUNTIME_DIR": str(runtime),
                },
                clear=False,
            ):
                prepared = prepare_data_source()
                self.assertTrue(prepared.path.exists())
                self.assertNotEqual(prepared.path, source)
                self.assertEqual(Path(prepared.original_path), source.resolve())
                self.assertEqual(prepared.source_signature, quick_file_signature(source))

                data = load_all_data(
                    get_data_file_signature(prepared.path),
                    DATA_SCHEMA_VERSION,
                    str(prepared.path),
                )
                self.assertFalse(data["metadata"]["uses_sample_data"])

    def test_last_valid_recovery_copy_roundtrip(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "source.xlsx"
            source.write_bytes(WORKBOOK.read_bytes())
            runtime = Path(temp_dir) / "runtime"

            with patch.dict(
                os.environ,
                {
                    "DATA_SOURCE": "local",
                    "DATA_LOCAL_PATH": str(source),
                    "LOCAL_RUNTIME_DIR": str(runtime),
                },
                clear=False,
            ):
                prepared = prepare_data_source()
                mark_source_valid(prepared)
                fallback = prepare_last_valid_source()

            self.assertIsNotNone(fallback)
            assert fallback is not None
            self.assertTrue(fallback.fallback_used)
            self.assertTrue(fallback.path.exists())
            self.assertEqual(fallback.checksum, prepared.checksum)
            self.assertEqual(fallback.original_path, str(source.resolve()))

    def test_internal_operation_files_exist(self) -> None:
        expected = [
            "CONFIGURAR_HOST_INTERNO.ps1",
            "INICIAR_LOCAL.bat",
            "INICIAR_REDE_INTERNA.bat",
            "INSTALAR_INICIALIZACAO_AUTOMATICA.ps1",
            "REMOVER_INICIALIZACAO_AUTOMATICA.ps1",
            "DIAGNOSTICAR_HOST_INTERNO.ps1",
            "HOSPEDAGEM_INTERNA.md",
            "OPERACAO_E_RECUPERACAO.md",
        ]
        for relative in expected:
            with self.subTest(relative=relative):
                self.assertTrue((ROOT / relative).exists())

    def test_runtime_and_real_secrets_are_ignored(self) -> None:
        gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
        self.assertIn(".runtime/", gitignore)
        self.assertIn(".streamlit/secrets.toml", gitignore)
        self.assertFalse((ROOT / ".streamlit/secrets.toml").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
