"""Data-quality validation and reconciliation rules.

Validation is intentionally separated from the loader.  The loader guarantees
that the application can work with the workbook; this module explains the
quality of what was loaded and surfaces warnings instead of silently hiding
inconsistencies.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any

import pandas as pd

from src.config import ABSENTEISMO_UNITS, DATA_STALE_AFTER_DAYS, MONTHS_ORDER, UNITS
from src.transforms import filter_unit_rows, get_available_months


@dataclass(frozen=True)
class ValidationIssue:
    severity: str  # error, warning, info
    area: str
    check: str
    message: str
    affected: int = 0


@dataclass(frozen=True)
class ValidationReport:
    score: float
    issues: tuple[ValidationIssue, ...]
    checks_total: int
    checks_passed: int
    generated_at: datetime

    @property
    def errors(self) -> int:
        return sum(issue.severity == "error" for issue in self.issues)

    @property
    def warnings(self) -> int:
        return sum(issue.severity == "warning" for issue in self.issues)

    def issues_dataframe(self) -> pd.DataFrame:
        if not self.issues:
            return pd.DataFrame(
                [{"Severidade": "OK", "Área": "Geral", "Verificação": "Todas", "Mensagem": "Nenhum problema encontrado", "Afetados": 0}]
            )
        return pd.DataFrame(
            [
                {
                    "Severidade": issue.severity.upper(),
                    "Área": issue.area,
                    "Verificação": issue.check,
                    "Mensagem": issue.message,
                    "Afetados": issue.affected,
                }
                for issue in self.issues
            ]
        )

    def as_dict(self) -> dict[str, Any]:
        return {
            "score": self.score,
            "checks_total": self.checks_total,
            "checks_passed": self.checks_passed,
            "generated_at": self.generated_at.isoformat(),
            "issues": [asdict(issue) for issue in self.issues],
        }


def _month_numeric_issues(df: pd.DataFrame, area: str, months: list[str]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for month in [m for m in months if m in df.columns]:
        numeric = pd.to_numeric(df[month], errors="coerce")
        invalid = int(numeric.isna().sum() - df[month].isna().sum())
        if invalid > 0:
            issues.append(
                ValidationIssue("error", area, "Valores numéricos", f"{invalid} valor(es) não numérico(s) em {month}.", invalid)
            )
        negative = int((numeric.fillna(0) < 0).sum())
        if negative > 0:
            issues.append(
                ValidationIssue("warning", area, "Valores negativos", f"{negative} valor(es) negativo(s) em {month}.", negative)
            )
    return issues


def _duplicate_label_issues(df: pd.DataFrame, label: str, area: str) -> list[ValidationIssue]:
    if label not in df.columns:
        return [ValidationIssue("error", area, "Coluna de identificação", f"Coluna obrigatória '{label}' não encontrada.")]
    duplicated = int(df[label].astype(str).str.strip().duplicated(keep=False).sum())
    if duplicated:
        return [ValidationIssue("warning", area, "Duplicidades", f"{duplicated} linha(s) possuem rótulos duplicados.", duplicated)]
    return []


def validate_loaded_data(data: dict[str, Any]) -> ValidationReport:
    """Run structural, content and reconciliation checks on loaded data."""
    issues: list[ValidationIssue] = []
    checks_total = 0
    checks_passed = 0

    def check(condition: bool, issue: ValidationIssue) -> None:
        nonlocal checks_total, checks_passed
        checks_total += 1
        if condition:
            checks_passed += 1
        else:
            issues.append(issue)

    required_keys = {"exames", "afastamentos", "atendimentos", "absenteismo", "saude_mental", "top_postos"}
    missing = required_keys.difference(data)
    check(not missing, ValidationIssue("error", "Estrutura", "Conjuntos obrigatórios", "Conjuntos ausentes: " + ", ".join(sorted(missing))))

    months = get_available_months(data) if not missing else []
    check(bool(months), ValidationIssue("error", "Estrutura", "Meses", "Nenhum mês reconhecido na base."))
    check(months == sorted(months, key=MONTHS_ORDER.index), ValidationIssue("warning", "Estrutura", "Ordem dos meses", "Os meses não estão em ordem cronológica."))

    if "exames" in data:
        volume = data["exames"].get("volume", pd.DataFrame())
        issues.extend(_month_numeric_issues(volume, "Exames", months))
        issues.extend(_duplicate_label_issues(volume, "tipo_short", "Exames"))
        pct = data["exames"].get("percentuais", {})
        ratios = list(pct.get("pct_periodicos_acum", [])) + list(pct.get("pct_faltas", []))
        check(all(0 <= float(value) <= 1 for value in ratios), ValidationIssue("error", "Exames", "Percentuais", "Há percentuais fora da faixa de 0 a 100%."))

    if "atendimentos" in data:
        issues.extend(_month_numeric_issues(data["atendimentos"], "Atendimentos", months))
        issues.extend(_duplicate_label_issues(data["atendimentos"], "tipo", "Atendimentos"))

    if "afastamentos" in data:
        by_unit = data["afastamentos"].get("por_unidade", pd.DataFrame())
        issues.extend(_month_numeric_issues(by_unit, "Afastamentos por unidade", months))
        unit_rows = filter_unit_rows(by_unit, UNITS)
        total_rows = by_unit[by_unit.get("indicador", pd.Series(dtype=str)).astype(str).str.contains("Total", case=False, na=False)]
        for month in [m for m in months if m in by_unit.columns]:
            if not total_rows.empty:
                informed = int(pd.to_numeric(total_rows[month], errors="coerce").fillna(0).sum())
                calculated = int(pd.to_numeric(unit_rows[month], errors="coerce").fillna(0).sum())
                check(
                    informed == calculated,
                    ValidationIssue(
                        "warning",
                        "Afastamentos",
                        f"Reconciliação {month}",
                        f"Total informado ({informed}) difere da soma das unidades ({calculated}).",
                        abs(informed - calculated),
                    ),
                )

    if "absenteismo" in data:
        available_abs_units = [unit for unit in ABSENTEISMO_UNITS if unit in data["absenteismo"]]
        check(
            set(available_abs_units) == set(ABSENTEISMO_UNITS),
            ValidationIssue("warning", "Absenteísmo", "Cobertura de unidades", "Nem todas as unidades esperadas possuem bloco de absenteísmo."),
        )
        for unit in available_abs_units:
            unit_df = data["absenteismo"][unit].get("data", pd.DataFrame())
            issues.extend(_month_numeric_issues(unit_df, f"Absenteísmo {unit}", months))
            issues.extend(_duplicate_label_issues(unit_df, "indicador", f"Absenteísmo {unit}"))

    if "saude_mental" in data:
        mental = data["saude_mental"]
        issues.extend(_month_numeric_issues(mental, "Saúde Mental", months))
        issues.extend(_duplicate_label_issues(mental, "indicador", "Saúde Mental"))

    metadata = data.get("metadata", {})
    updated_at = metadata.get("updated_at")
    if isinstance(updated_at, datetime):
        now = datetime.now(updated_at.tzinfo or timezone.utc)
        age_days = (now - updated_at.replace(tzinfo=updated_at.tzinfo or timezone.utc)).days
        check(age_days <= DATA_STALE_AFTER_DAYS, ValidationIssue("warning", "Arquivo", "Atualização", f"A planilha foi atualizada há {age_days} dias.", age_days))

    # Each issue generated by helper functions represents a failed check.
    helper_failures = len(issues) - (checks_total - checks_passed)
    checks_total += max(helper_failures, 0)

    # Weighted penalty avoids a single informational warning destroying the score.
    penalty = sum(
        {"error": 12.0, "warning": 4.0, "info": 1.0}.get(issue.severity, 2.0)
        for issue in issues
    )
    score = max(0.0, 100.0 - penalty)
    final_passed = max(0, checks_total - len(issues))
    return ValidationReport(
        score=score,
        issues=tuple(issues),
        checks_total=checks_total,
        checks_passed=final_passed,
        generated_at=datetime.now(),
    )


def dimension_coverage_table() -> pd.DataFrame:
    """Document which source tables can respond to each filter dimension."""
    return pd.DataFrame(
        [
            ["Exames", "Sim", "Não", "Sim", "Não", "Não"],
            ["Atendimentos", "Sim", "Não", "Não", "Sim", "Não"],
            ["Afastamentos por unidade", "Sim", "Sim", "Não", "Não", "Não"],
            ["Motivos de afastamento", "Sim", "Não", "Não", "Não", "Sim"],
            ["Absenteísmo", "Sim", "B2BN/B2BF/SF", "Não", "Não", "Motivos agregados"],
            ["Saúde Mental", "Sim", "Sim", "Não", "Não", "Não"],
            ["Previdenciário / CAT", "Sim", "Não", "Não", "Não", "Não"],
            ["Top Postos", "Sim", "Não", "Não", "Não", "Não"],
        ],
        columns=["Conjunto", "Mês", "Unidade", "Tipo de exame", "Tipo de atendimento", "Motivo"],
    )
