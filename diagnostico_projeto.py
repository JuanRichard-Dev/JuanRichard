"""Command-line diagnostic for the V7 dashboard using the real workbook."""

from __future__ import annotations

import sys

from src.alerts import generate_alerts
from src.analytics import (
    build_executive_narrative,
    reason_pareto_table,
    unit_latest_ranking,
    unit_period_ranking,
)
from src.config import ABSENTEISMO_UNITS, DATA_SCHEMA_VERSION, UNITS
from src.data_loader import DataLoadError, get_data_file_signature, load_all_data
from src.semantic import build_semantic_model, semantic_monthly_totals
from src.transforms import (
    appointment_rows_for_totals,
    compute_overview_kpis,
    filter_unit_rows,
    get_available_months,
)
from src.validators import validate_loaded_data


def _direct_absence_days(data: dict, months: list[str]) -> int:
    total = 0
    for unit in ABSENTEISMO_UNITS:
        unit_data = data["absenteismo"][unit]["data"]
        row = unit_data[unit_data["indicador"].astype(str).str.casefold().eq("total")]
        total += int(row[months].sum(axis=1).sum()) if not row.empty else 0
    return total


def main() -> int:
    signature = get_data_file_signature()
    try:
        data = load_all_data(signature, DATA_SCHEMA_VERSION)
    except DataLoadError as exc:
        print(f"ERRO: {exc}")
        return 2

    months = get_available_months(data)
    report = validate_loaded_data(data)
    metadata = data.get("metadata", {})

    print("=" * 84)
    print("DIAGNÓSTICO DO DASHBOARD — V7 PROFESSIONAL / PLANILHA REAL")
    print("=" * 84)
    print("Arquivo:", metadata.get("source_path"))
    print("Atualizado em:", metadata.get("updated_at"))
    print("Tempo de carga:", metadata.get("load_seconds"), "s")
    print("Assinatura:", signature)
    print("Meses reconhecidos:", months)
    print(f"Qualidade: {report.score:.0f}% | erros: {report.errors} | avisos: {report.warnings}")

    if not months:
        print("ERRO: nenhum mês reconhecido.")
        return 2

    model = build_semantic_model(data)
    monthly = semantic_monthly_totals(data, months, UNITS)
    print("\nCamada semântica:")
    for name, frame in model.items():
        print(f"  {name:24s} | linhas: {len(frame):4d}")

    print("\nMétricas mensais reconciliadas:")
    print(monthly.to_string(index=False))

    print("\nTeste do filtro de unidade:")
    results = {}
    for unit in UNITS:
        metrics = compute_overview_kpis(data, months, [unit])
        results[unit] = (
            metrics["afastamentos"]["current"],
            metrics["absenteismo"]["total"],
        )
        print(
            f"  {unit:7s} | afastamentos atuais: {results[unit][0]:5d} "
            f"| dias perdidos no período: {results[unit][1]:5d}"
        )
    print("OK: filtros distintos." if len(set(results.values())) > 1 else "AVISO: valores idênticos.")

    print("\nRankings:")
    print("Afastamentos — último mês")
    print(unit_latest_ranking(data, months, UNITS, "Afastamentos").to_string(index=False))
    print("\nDias perdidos — período")
    print(unit_period_ranking(data, months, UNITS, "Dias Perdidos").to_string(index=False))
    print("\nPareto de motivos")
    print(reason_pareto_table(data, months).to_string(index=False))

    print("\nNarrativa executiva:")
    print(build_executive_narrative(data, months, UNITS))

    print("\nAlertas:")
    alerts = generate_alerts(data, months, UNITS)
    if not alerts:
        print("  Nenhum alerta gerado.")
    for alert in alerts:
        print(f"  [{alert.severity.upper()}] {alert.title}: {alert.message}")

    if report.issues:
        print("\nProblemas de qualidade:")
        print(report.issues_dataframe().to_string(index=False))

    # Reconciliation is derived from the current workbook, not hard-coded totals.
    direct_exams = int(data["exames"]["volume"][months].sum().sum())
    direct_appointments = int(
        appointment_rows_for_totals(data["atendimentos"])[months].sum().sum()
    )
    direct_days = _direct_absence_days(data, months)
    last_month = months[-1]
    direct_active = int(
        filter_unit_rows(data["afastamentos"]["por_unidade"], UNITS)[last_month].sum()
    )

    semantic_values = {
        "Exames": int(monthly["Exames"].sum()),
        "Atendimentos": int(monthly["Atendimentos"].sum()),
        "Dias perdidos": int(monthly["Dias Perdidos"].sum()),
        "Afastamentos atuais": int(monthly.iloc[-1]["Afastamentos"]),
    }
    direct_values = {
        "Exames": direct_exams,
        "Atendimentos": direct_appointments,
        "Dias perdidos": direct_days,
        "Afastamentos atuais": direct_active,
    }

    print("\nReconciliação dinâmica:")
    mismatches = []
    for name, direct_value in direct_values.items():
        semantic_value = semantic_values[name]
        status = "OK" if semantic_value == direct_value else "DIVERGENTE"
        print(
            f"  {name:24s}: semântico {semantic_value:6d} | "
            f"fonte {direct_value:6d} | {status}"
        )
        if status != "OK":
            mismatches.append(name)

    print("\nDiagnóstico concluído.")
    return 1 if report.errors or mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
