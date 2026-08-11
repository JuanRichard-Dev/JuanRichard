"""Optional population denominators for normalized occupational-health rates."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.config import UNITS, canonicalize_unit

PROJECT_ROOT = Path(__file__).resolve().parent.parent
POPULATION_PATH = PROJECT_ROOT / "population_by_unit.csv"


def load_population(path: Path | None = None) -> pd.DataFrame:
    path = path or POPULATION_PATH
    if not path.exists():
        return pd.DataFrame(columns=["Unidade", "Populacao"])
    frame = pd.read_csv(path)
    if frame.empty or not {"Unidade", "Populacao"}.issubset(frame.columns):
        return pd.DataFrame(columns=["Unidade", "Populacao"])
    result = frame[["Unidade", "Populacao"]].copy()
    result["Unidade"] = result["Unidade"].map(canonicalize_unit)
    result["Populacao"] = pd.to_numeric(result["Populacao"], errors="coerce")
    result = result[
        result["Unidade"].isin(UNITS) & result["Populacao"].gt(0)
    ].drop_duplicates("Unidade", keep="last")
    return result.reset_index(drop=True)


def add_rate_per_100(
    frame: pd.DataFrame,
    *,
    value_column: str = "Valor",
    unit_column: str = "Unidade",
    population: pd.DataFrame | None = None,
    rate_column: str = "Taxa por 100 colaboradores",
) -> pd.DataFrame:
    population = load_population() if population is None else population.copy()
    if frame.empty or population.empty:
        return pd.DataFrame()
    result = frame.copy()
    result = result.merge(population, left_on=unit_column, right_on="Unidade", how="inner")
    if result.empty:
        return result
    result[rate_column] = (
        pd.to_numeric(result[value_column], errors="coerce").fillna(0)
        / result["Populacao"]
        * 100
    )
    return result
