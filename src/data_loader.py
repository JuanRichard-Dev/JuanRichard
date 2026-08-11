"""Excel loading and normalization for the real Dashboard SM CGR 2026 workbook.

The source workbook delivered with the project contains three sheets:
``Principal``, ``Absenteísmo`` and ``Saúde Mental``.  This loader derives the
logical datasets used by the application directly from those sheets; it does
not generate or inject demonstration records.
"""

from __future__ import annotations

import re
import unicodedata
from datetime import datetime
from pathlib import Path
from time import perf_counter
from typing import Any, Callable

import pandas as pd

try:
    import streamlit as st
except ModuleNotFoundError:  # Allows non-UI diagnostics before dependencies are installed.
    class _CacheDataFallback:
        def __call__(self, func=None, **_kwargs):
            if func is not None:
                return func
            return lambda wrapped: wrapped

        @staticmethod
        def clear() -> None:
            return None

    class _StreamlitFallback:
        cache_data = _CacheDataFallback()

    st = _StreamlitFallback()

from src.config import (
    DATA_SCHEMA_VERSION,
    ENCODING_FIXES,
    MONTHS_ORDER,
    canonicalize_unit,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FILENAME = "Dashboard SM CGR 2026.xlsx"
DATA_PATH: Path = PROJECT_ROOT / DATA_FILENAME
REQUIRED_SHEETS = {"Principal", "Absenteísmo", "Saúde Mental"}


class DataLoadError(RuntimeError):
    """Raised when the real workbook cannot be loaded or validated."""


def get_data_file_signature(path: Path | str | None = None) -> tuple[int, int]:
    """Return a cache key that changes whenever the real workbook changes."""
    if path is None:
        path = DATA_PATH
    elif isinstance(path, str):
        path = Path(path)
    if not path.exists():
        return (0, 0)
    stat = path.stat()
    return (stat.st_mtime_ns, stat.st_size)


def _plain_text(value: object) -> str:
    text = "" if value is None else str(value).strip()
    normalized = unicodedata.normalize("NFKD", text)
    normalized = "".join(char for char in normalized if not unicodedata.combining(char))
    normalized = re.sub(r"\s+", " ", normalized)
    return normalized.casefold()


def _fix_encoding(text: object) -> object:
    if not isinstance(text, str):
        return text
    result = text
    for bad, good in ENCODING_FIXES.items():
        result = result.replace(bad, good)
    return result.strip()


def _fix_df_encoding(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    for column in result.columns:
        if result[column].dtype == object:
            result[column] = result[column].apply(
                lambda value: _fix_encoding(value) if pd.notna(value) else value
            )
    result.columns = [_fix_encoding(str(column)) for column in result.columns]
    return result


def _fix_month_cols(df: pd.DataFrame) -> pd.DataFrame:
    rename_map: dict[object, str] = {}
    prefixes = {
        "jan": "Janeiro",
        "fev": "Fevereiro",
        "mar": "Março",
        "abr": "Abril",
        "mai": "Maio",
        "jun": "Junho",
        "jul": "Julho",
        "ago": "Agosto",
        "set": "Setembro",
        "out": "Outubro",
        "nov": "Novembro",
        "dez": "Dezembro",
    }
    for column in df.columns:
        lowered = _plain_text(column)
        for prefix, full_name in prefixes.items():
            if lowered.startswith(prefix):
                rename_map[column] = full_name
                break
    return df.rename(columns=rename_map)


def _active_months(df: pd.DataFrame) -> list[str]:
    """Return months that contain at least one source value in the sheet."""
    months: list[str] = []
    for month in MONTHS_ORDER:
        if month in df.columns and df[month].notna().any():
            months.append(month)
    return months


def _to_numeric_months(df: pd.DataFrame, month_cols: list[str]) -> pd.DataFrame:
    result = df.copy()
    for month in month_cols:
        if month in result.columns:
            result[month] = pd.to_numeric(result[month], errors="coerce").fillna(0).astype(int)
    return result


def _normalize_ratio(value: object) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0.0
    if number > 1.0:
        number /= 100.0
    return max(0.0, min(number, 1.0))


def _clean_source(df: pd.DataFrame, sheet_name: str) -> tuple[pd.DataFrame, str]:
    if df.empty:
        raise ValueError(f"A aba '{sheet_name}' está vazia.")
    cleaned = _fix_df_encoding(_fix_month_cols(df))
    first_col = cleaned.columns[0]
    cleaned[first_col] = cleaned[first_col].astype("string").str.strip()
    return cleaned, first_col


def _select_rows(
    df: pd.DataFrame,
    label_col: str,
    predicate: Callable[[str], bool],
) -> pd.DataFrame:
    mask = df[label_col].fillna("").map(lambda value: predicate(_plain_text(value)))
    return df.loc[mask].copy()


def _prepare_numeric_table(
    rows: pd.DataFrame,
    source_label: str,
    target_label: str,
    month_cols: list[str],
) -> pd.DataFrame:
    result = rows[[source_label] + month_cols].copy()
    result.columns = [target_label] + month_cols
    result[target_label] = result[target_label].astype("string").str.strip()
    result = result[result[target_label].notna() & result[target_label].ne("")].reset_index(drop=True)
    return _to_numeric_months(result, month_cols)


def _exam_short_name(value: object) -> str:
    key = _plain_text(value)
    if "periodic" in key:
        return "Periódicos"
    if "admission" in key:
        return "Admissionais"
    if "demission" in key:
        return "Demissionais"
    if "mudanca de funcao" in key:
        return "Mudança de Função"
    if "retorno ao trabalho" in key:
        return "Retorno ao Trabalho"
    return str(value).strip()


def _appointment_name(value: object) -> str:
    key = _plain_text(value)
    if key.startswith("atendimento medico"):
        return "Atendimento Médico"
    if key.startswith("atendimento de enfermagem"):
        return "Atendimento de Enfermagem"
    if "fisioterap" in key and "horista" in key:
        return "Atendimento Fisioterapêutico Horista"
    if "fisioterap" in key and "mensalista" in key:
        return "Atendimento Fisioterapêutico Mensalista"
    if "fisioterap" in key and "total" in key:
        return "Atendimento Fisioterapêutico Total"
    if key.startswith("cat ("):
        return "CAT (Comunicado de Acidente de Trabalho)"
    if "saidas de ambulancia" in key:
        return "Saídas de Ambulância (Urgência/Emergência)"
    return str(value).strip()


def _reason_name(value: object) -> str:
    key = _plain_text(value)
    if "ortoped" in key:
        return "Ortopédicos"
    if "psiquiatr" in key:
        return "Psiquiátricos"
    if "clinic" in key:
        return "Clínicos"
    if "outros" in key:
        return "Outros motivos"
    return str(value).strip()


def _abs_indicator_name(value: object, *, total_row: bool = False) -> str:
    if total_row:
        return "Total"
    key = _plain_text(value)
    if "ortoped" in key:
        return "Causas Ortopédicas"
    if "psiquiatr" in key:
        return "Causas Psiquiátricas"
    if "clinic" in key:
        return "Causas Clínicas"
    if key.startswith("homens"):
        return "Homens"
    if key.startswith("mulheres"):
        return "Mulheres"
    return str(value).strip()


@st.cache_data(show_spinner=False)
def load_all_data(
    file_signature: tuple[int, int] | None = None,
    schema_version: str = DATA_SCHEMA_VERSION,
    data_path: str | Path | None = None,
) -> dict[str, Any]:
    """Load and normalize the user's real workbook without sample records.

    ``data_path`` keeps local development backward compatible while allowing
    cloud deployments to provide a downloaded SharePoint or URL file.
    """
    resolved_path = Path(data_path).expanduser().resolve() if data_path else DATA_PATH
    _ = file_signature or get_data_file_signature(resolved_path)
    _ = schema_version
    started_at = perf_counter()

    if not resolved_path.exists():
        raise DataLoadError(f"Arquivo de dados não encontrado: {resolved_path}")

    try:
        with pd.ExcelFile(resolved_path) as xls:
            sheet_names = list(xls.sheet_names)
            missing = REQUIRED_SHEETS.difference(sheet_names)
            if missing:
                raise ValueError("Abas obrigatórias ausentes: " + ", ".join(sorted(missing)))

            principal = _load_principal(xls)
            global_months = principal.pop("month_cols")
            result = {
                "exames": principal["exames"],
                "afastamentos": principal["afastamentos"],
                "atendimentos": principal["atendimentos"],
                "top_postos": principal["top_postos"],
                "absenteismo": _load_absenteismo(xls, global_months),
                "saude_mental": _load_saude_mental(xls, global_months),
            }

        # Build the shared semantic layer once per workbook cache entry.
        from src.semantic import build_semantic_model
        result["semantic"] = build_semantic_model(result)

        result["metadata"] = {
            "source_path": str(resolved_path),
            "source_filename": resolved_path.name,
            "source_sheets": sheet_names,
            "updated_at": datetime.fromtimestamp(resolved_path.stat().st_mtime),
            "file_signature": get_data_file_signature(resolved_path),
            "recognized_months": global_months,
            "source_layout": "Principal + Absenteísmo + Saúde Mental",
            "uses_sample_data": False,
            "load_seconds": round(perf_counter() - started_at, 4),
            "record_counts": {
                "exam_types": int(len(result["exames"]["volume"])),
                "appointment_types": int(len(result["atendimentos"])),
                "absence_reasons": int(len(result["afastamentos"]["por_motivo"])),
                "mental_rows": int(len(result["saude_mental"])),
            },
        }
        return result
    except DataLoadError:
        raise
    except Exception as exc:
        raise DataLoadError(f"Erro ao carregar ou validar a planilha real: {exc}") from exc


def _load_principal(xls: pd.ExcelFile) -> dict[str, Any]:
    df, label_col = _clean_source(pd.read_excel(xls, "Principal"), "Principal")
    month_cols = _active_months(df)
    if not month_cols:
        raise ValueError("Nenhum mês preenchido foi reconhecido na aba 'Principal'.")

    # Exames: five monthly volume rows plus two percentage indicators.
    exam_rows = _select_rows(
        df,
        label_col,
        lambda key: key.startswith("exames ")
        and "mensal" in key
        and "faltas" not in key
        and "acumulado" not in key,
    )
    volume = _prepare_numeric_table(exam_rows, label_col, "tipo", month_cols)
    volume["tipo_short"] = volume["tipo"].map(_exam_short_name)
    volume["TOTAL"] = volume[month_cols].sum(axis=1)

    labels_normalized = df[label_col].fillna("").map(_plain_text)
    periodic_candidates = df.loc[
        labels_normalized.str.contains("exames periodicos", regex=False)
        & labels_normalized.str.contains("acumulado", regex=False)
    ]
    absence_candidates = df.loc[
        labels_normalized.str.contains("exames periodicos", regex=False)
        & labels_normalized.str.contains("faltas", regex=False)
    ]
    if periodic_candidates.empty or absence_candidates.empty:
        raise ValueError("Indicadores percentuais de exames periódicos não foram encontrados na aba Principal.")
    periodic_row = periodic_candidates.iloc[0]
    absence_row = absence_candidates.iloc[0]
    percentages = {
        "meses": month_cols,
        "pct_periodicos_acum": [_normalize_ratio(periodic_row[month]) for month in month_cols],
        "pct_faltas": [_normalize_ratio(absence_row[month]) for month in month_cols],
    }

    # Afastamentos by operational unit.
    unit_source = _select_rows(
        df,
        label_col,
        lambda key: key.startswith("afastamentos ativos -"),
    )
    by_unit = _prepare_numeric_table(unit_source, label_col, "indicador", month_cols)

    def unit_from_label(value: object) -> str:
        key = _plain_text(value)
        if key.endswith("- total"):
            return "Total"
        suffix = str(value).split("-", 1)[-1].strip()
        return canonicalize_unit(suffix)

    by_unit["indicador"] = by_unit["indicador"].map(unit_from_label)

    reason_source = _select_rows(
        df,
        label_col,
        lambda key: key.startswith("afastamentos ativos por"),
    )
    by_reason = _prepare_numeric_table(reason_source, label_col, "indicador", month_cols)
    by_reason["indicador"] = by_reason["indicador"].map(_reason_name)

    previdenciary_keys = {
        "aposentados afastados",
        "limbo previdenciario total",
        "em reabilitacao pelo inss",
        "aposentados por invalidez",
    }
    previd_source = _select_rows(df, label_col, lambda key: key in previdenciary_keys)
    previdenciary = _prepare_numeric_table(previd_source, label_col, "indicador", month_cols)

    cat_source = _select_rows(
        df,
        label_col,
        lambda key: "b-91" in key or "nexo ocupacional" in key,
    )
    cat_b91 = _prepare_numeric_table(cat_source, label_col, "indicador", month_cols)

    appointment_source = _select_rows(
        df,
        label_col,
        lambda key: key.startswith("atendimento ")
        or key.startswith("cat (")
        or "saidas de ambulancia" in key,
    )
    appointments = _prepare_numeric_table(appointment_source, label_col, "tipo", month_cols)
    appointments["tipo"] = appointments["tipo"].map(_appointment_name)
    appointments["TOTAL"] = appointments[month_cols].sum(axis=1)
    appointments["contabilizar_total"] = ~appointments["tipo"].str.contains(
        "Horista|Mensalista", case=False, na=False, regex=True
    )

    top_source = _select_rows(
        df,
        label_col,
        lambda key: key.startswith("posto com mais afastamentos"),
    )
    top_posts = top_source[[label_col] + month_cols].copy()
    top_posts.columns = ["posicao"] + month_cols

    def position(value: object) -> str:
        match = re.search(r"-\s*(\d+)\s+lugar", _plain_text(value))
        return f"{match.group(1)}º" if match else str(value).strip()

    top_posts["posicao"] = top_posts["posicao"].map(position)
    top_posts = top_posts.reset_index(drop=True)

    expected_exam_types = {"Periódicos", "Admissionais", "Demissionais", "Mudança de Função", "Retorno ao Trabalho"}
    missing_exam_types = expected_exam_types.difference(set(volume["tipo_short"]))
    if missing_exam_types:
        raise ValueError("Tipos de exame não reconhecidos na aba Principal: " + ", ".join(sorted(missing_exam_types)))

    return {
        "month_cols": month_cols,
        "exames": {"volume": volume, "percentuais": percentages},
        "afastamentos": {
            "por_unidade": by_unit,
            "por_motivo": by_reason,
            "previdenciaria": previdenciary,
            "cat_b91": cat_b91,
        },
        "atendimentos": appointments,
        "top_postos": top_posts,
    }


def _load_absenteismo(xls: pd.ExcelFile, global_months: list[str]) -> dict[str, Any]:
    df, label_col = _clean_source(pd.read_excel(xls, "Absenteísmo"), "Absenteísmo")
    month_cols = [month for month in global_months if month in df.columns]
    if not month_cols:
        raise ValueError("Nenhum mês da aba Principal foi encontrado na aba 'Absenteísmo'.")

    labels = df[label_col].fillna("").map(_plain_text)
    block_starts = [index for index, key in labels.items() if key.startswith("atestados (dias perdidos)")]
    if not block_starts:
        raise ValueError("Blocos de unidades não foram encontrados na aba 'Absenteísmo'.")

    result: dict[str, Any] = {"month_cols": month_cols}
    for position_index, start_index in enumerate(block_starts):
        end_index = block_starts[position_index + 1] if position_index + 1 < len(block_starts) else len(df)
        source_label = str(df.loc[start_index, label_col])
        unit = next((candidate for candidate in ("B2BN", "B2BF", "SF") if candidate in source_label.upper()), None)
        if unit is None:
            continue

        block = df.loc[start_index:end_index - 1, [label_col] + month_cols].copy()
        block.columns = ["indicador"] + month_cols
        block = block[block["indicador"].notna()].reset_index(drop=True)
        block["indicador"] = [
            _abs_indicator_name(value, total_row=index == 0)
            for index, value in enumerate(block["indicador"])
        ]
        block = _to_numeric_months(block, month_cols)
        result[unit] = {"unidade": unit, "data": block}

    missing_units = {"B2BN", "B2BF", "SF"}.difference(result)
    if missing_units:
        raise ValueError("Unidades ausentes na aba Absenteísmo: " + ", ".join(sorted(missing_units)))
    return result


def _load_saude_mental(xls: pd.ExcelFile, global_months: list[str]) -> pd.DataFrame:
    df, label_col = _clean_source(pd.read_excel(xls, "Saúde Mental"), "Saúde Mental")
    month_cols = [month for month in global_months if month in df.columns]
    if not month_cols:
        raise ValueError("Nenhum mês da aba Principal foi encontrado na aba 'Saúde Mental'.")

    result = df[[label_col] + month_cols].copy()
    result.columns = ["indicador"] + month_cols
    result = result[result["indicador"].notna()].reset_index(drop=True)

    normalized_indicators: list[str] = []
    for value in result["indicador"]:
        key = _plain_text(value)
        if "total" in key:
            normalized_indicators.append("Total")
        else:
            normalized_indicators.append(canonicalize_unit(value))
    result["indicador"] = normalized_indicators
    return _to_numeric_months(result, month_cols)
