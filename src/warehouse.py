"""Optional persistence of normalized dashboard tables to SQL databases."""

from __future__ import annotations

from typing import Any

import pandas as pd

from src.runtime_config import get_bool, get_setting


class WarehouseError(RuntimeError):
    pass


def _tables_from_data(data: dict[str, Any]) -> dict[str, pd.DataFrame]:
    tables: dict[str, pd.DataFrame] = {
        "exames_volume": data["exames"]["volume"],
        "atendimentos": data["atendimentos"],
        "afastamentos_unidade": data["afastamentos"]["por_unidade"],
        "afastamentos_motivo": data["afastamentos"]["por_motivo"],
        "afastamentos_previdenciario": data["afastamentos"]["previdenciaria"],
        "cat_b91": data["afastamentos"]["cat_b91"],
        "saude_mental": data["saude_mental"],
        "top_postos": data["top_postos"],
    }
    absenteismo = data.get("absenteismo", {})
    for unit in ("B2BN", "B2BF", "SF"):
        if unit in absenteismo:
            tables[f"absenteismo_{unit.lower()}"] = absenteismo[unit]["data"]
    return tables


def sync_to_warehouse(data: dict[str, Any]) -> list[str]:
    """Write normalized tables when WAREHOUSE_ENABLED=true.

    ``DATABASE_URL`` may point to SQLite, PostgreSQL or another SQLAlchemy
    compatible database. Existing tables are replaced per workbook version.
    """
    if not get_bool("WAREHOUSE_ENABLED", False):
        return []
    database_url = str(get_setting("DATABASE_URL", "")).strip()
    if not database_url:
        raise WarehouseError("WAREHOUSE_ENABLED está ativo, mas DATABASE_URL não foi configurada.")
    try:
        from sqlalchemy import create_engine
    except ModuleNotFoundError as exc:  # pragma: no cover
        raise WarehouseError("Instale SQLAlchemy para usar o warehouse.") from exc

    engine = create_engine(database_url, pool_pre_ping=True)
    written: list[str] = []
    with engine.begin() as connection:
        for table_name, frame in _tables_from_data(data).items():
            frame.copy().to_sql(table_name, connection, if_exists="replace", index=False)
            written.append(table_name)
    return written
