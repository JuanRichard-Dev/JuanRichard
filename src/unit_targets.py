"""Optional targets per metric and operational unit."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.config import UNITS, canonicalize_unit

PROJECT_ROOT = Path(__file__).resolve().parent.parent
UNIT_TARGETS_PATH = PROJECT_ROOT / "unit_targets.csv"


def load_unit_targets(path: Path | None = None) -> pd.DataFrame:
    path = path or UNIT_TARGETS_PATH
    columns = ["Indicador", "Unidade", "Meta", "Direcao"]
    if not path.exists():
        return pd.DataFrame(columns=columns)
    frame = pd.read_csv(path)
    if frame.empty or not set(columns).issubset(frame.columns):
        return pd.DataFrame(columns=columns)
    result = frame[columns].copy()
    result["Unidade"] = result["Unidade"].map(canonicalize_unit)
    result["Meta"] = pd.to_numeric(result["Meta"], errors="coerce")
    result["Direcao"] = result["Direcao"].astype(str).str.strip().str.casefold()
    result = result[
        result["Unidade"].isin(UNITS)
        & result["Meta"].notna()
        & result["Direcao"].isin({"higher", "lower"})
    ]
    return result.drop_duplicates(["Indicador", "Unidade"], keep="last").reset_index(drop=True)


def apply_unit_targets(
    frame: pd.DataFrame,
    *,
    indicator: str,
    value_column: str,
    unit_column: str = "Unidade",
    targets: pd.DataFrame | None = None,
) -> pd.DataFrame:
    targets = load_unit_targets() if targets is None else targets.copy()
    if frame.empty or targets.empty:
        return pd.DataFrame()
    selected = targets[targets["Indicador"].astype(str).eq(indicator)].copy()
    if selected.empty:
        return pd.DataFrame()
    result = frame.copy().merge(selected, left_on=unit_column, right_on="Unidade", how="inner")
    if result.empty:
        return result
    values = pd.to_numeric(result[value_column], errors="coerce")
    result["Atingiu meta"] = [
        value >= target if direction == "higher" else value <= target
        for value, target, direction in zip(values, result["Meta"], result["Direcao"])
    ]
    result["Status"] = result["Atingiu meta"].map({True: "Dentro da meta", False: "Fora da meta"})
    return result
