"""Regression tests for the analytical layer using the real workbook."""

from __future__ import annotations

import unittest
from pathlib import Path

import pandas as pd

from src.analytics import (
    build_executive_narrative,
    linear_forecast_with_interval,
    metric_summary_matrix,
    reason_pareto_table,
    unit_change_contribution,
    unit_latest_ranking,
    unit_period_ranking,
)
from src.charts import (
    bridge_waterfall_chart,
    bullet_chart,
    enhanced_time_series_chart,
    health_score_radial_chart,
    matrix_heatmap,
    percent_stacked_bar_chart,
    ranking_bar_chart,
)
from src.config import DATA_SCHEMA_VERSION, UNITS
from src.data_loader import get_data_file_signature, load_all_data
from src.semantic import build_semantic_model, semantic_monthly_totals
from src.transforms import get_available_months


class AnalyticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = load_all_data(get_data_file_signature(), DATA_SCHEMA_VERSION)
        cls.months = get_available_months(cls.data)

    def test_semantic_model_uses_real_totals(self) -> None:
        model = build_semantic_model(self.data)
        monthly = semantic_monthly_totals(self.data, self.months, UNITS)
        self.assertEqual(int(model["exames"]["Valor"].sum()), int(monthly["Exames"].sum()))
        self.assertEqual(int(model["atendimentos"]["Valor"].sum()), int(monthly["Atendimentos"].sum()))
        self.assertGreater(int(monthly["Dias Perdidos"].sum()), 0)
        latest = unit_latest_ranking(self.data, self.months, UNITS, "Afastamentos")
        self.assertEqual(int(monthly.iloc[-1]["Afastamentos"]), int(latest["Valor"].sum()))

    def test_rankings_and_contributions_use_real_units(self) -> None:
        latest = unit_latest_ranking(self.data, self.months, UNITS, "Afastamentos")
        self.assertTrue(set(latest["Unidade"]).issubset(set(UNITS)))
        self.assertTrue(latest["Valor"].is_monotonic_decreasing)
        period = unit_period_ranking(self.data, self.months, UNITS, "Dias Perdidos")
        monthly = semantic_monthly_totals(self.data, self.months, UNITS)
        self.assertEqual(int(period["Valor"].sum()), int(monthly["Dias Perdidos"].sum()))
        previous, contributions, current = unit_change_contribution(
            self.data, self.months, UNITS, "Afastamentos"
        )
        self.assertEqual(int(contributions["Contribuição"].sum()), int(current - previous))

    def test_narrative_and_matrix_are_data_driven(self) -> None:
        narrative = build_executive_narrative(self.data, self.months, UNITS)
        monthly = semantic_monthly_totals(self.data, self.months, UNITS)
        exams_text = f"{int(monthly['Exames'].sum()):,}".replace(",", ".")
        lost_days_text = f"{int(monthly['Dias Perdidos'].sum()):,}".replace(",", ".")
        self.assertIn(f"{exams_text} exames", narrative)
        self.assertIn(f"{lost_days_text} dias perdidos", narrative)
        matrix = metric_summary_matrix(self.data, self.months, UNITS)
        self.assertEqual(matrix["Indicador"].tolist(), [
            "Exames", "Atendimentos", "Afastamentos", "Dias Perdidos", "SRQ-20"
        ])

    def test_pareto_and_forecast_are_explainable(self) -> None:
        pareto = reason_pareto_table(self.data, self.months)
        self.assertEqual(pareto.iloc[0]["Motivo"], "Ortopédicos")
        self.assertAlmostEqual(float(pareto.iloc[-1]["Acumulado (%)"]), 100.0, places=6)
        real_exam_series = semantic_monthly_totals(self.data, self.months, UNITS)["Exames"].tolist()
        forecast = linear_forecast_with_interval(
            real_exam_series, self.months, ["Junho", "Julho"]
        )
        self.assertIsNotNone(forecast)
        assert forecast is not None
        self.assertEqual(len(forecast.forecast), 2)
        self.assertTrue(all(value >= 0 for value in forecast.lower))
        self.assertTrue(all(lo <= mid <= hi for lo, mid, hi in zip(forecast.lower, forecast.forecast, forecast.upper)))

    def test_new_chart_factories_build_figures(self) -> None:
        pct = self.data["exames"]["percentuais"]
        periodic_pct = float(pct["pct_periodicos_acum"][-1]) * 100
        bullet = bullet_chart(periodic_pct, 95, "Cobertura")
        self.assertEqual(len(bullet.data), 1)

        monthly = semantic_monthly_totals(self.data, self.months, UNITS)
        trend = enhanced_time_series_chart(
            monthly, x="Mês", y="Exames", title="Exames",
            forecast_labels=["Maio", "Junho", "Julho"],
            forecast_values=[float(monthly.iloc[-1]["Exames"]), 330, 340],
            forecast_lower=[float(monthly.iloc[-1]["Exames"]), 300, 305],
            forecast_upper=[float(monthly.iloc[-1]["Exames"]), 360, 375],
        )
        self.assertGreaterEqual(len(trend.data), 4)

        exam_volume = self.data["exames"]["volume"]
        composition = {
            str(row["tipo_short"]): [float(row[month]) for month in self.months]
            for _, row in exam_volume.iterrows()
        }
        stacked = percent_stacked_bar_chart(composition, self.months, "Composição")
        self.assertEqual(len(stacked.data), len(exam_volume))

        ranking_df = unit_latest_ranking(self.data, self.months, UNITS, "Afastamentos")
        ranking = ranking_bar_chart(
            ranking_df, label_col="Unidade", value_col="Valor",
            previous_col="Anterior", share_col="Participação (%)", title="Ranking",
        )
        self.assertEqual(len(ranking.data), 1)

        previous, contributions, current = unit_change_contribution(
            self.data, self.months, UNITS, "Afastamentos"
        )
        bridge = bridge_waterfall_chart(previous, contributions, current, title="Ponte")
        self.assertEqual(len(bridge.data), 1)

        heat_rows = []
        for unit in ["B2BN", "B2BF", "SF"]:
            unit_data = self.data["absenteismo"][unit]["data"]
            total = unit_data[unit_data["indicador"] == "Total"]
            heat_rows.append({"Unidade": unit, **{month: int(total[month].sum()) for month in self.months}})
        heat = matrix_heatmap(
            pd.DataFrame(heat_rows), row_col="Unidade", month_cols=self.months, title="Heatmap"
        )
        self.assertEqual(len(heat.data), 1)

    def test_health_score_radial_chart_is_responsive_and_complete(self) -> None:
        figure = health_score_radial_chart(42.8, target=80.0, height=320)
        self.assertEqual(len(figure.data), 2)
        self.assertEqual(int(figure.layout.height), 320)
        annotations = [str(item.text) for item in figure.layout.annotations]
        self.assertTrue(any("42.8%" in text for text in annotations))
        self.assertTrue(any("ÍNDICE GERAL" in text for text in annotations))
        self.assertFalse(any("CRÍTICO" in text for text in annotations))
        self.assertFalse(any("80%" in text for text in annotations))

    def test_filters_are_immediate_without_apply_button(self) -> None:
        app_text = (Path(__file__).resolve().parents[1] / "app.py").read_text(encoding="utf-8")
        self.assertNotIn("Aplicar filtros", app_text)
        self.assertNotIn("dashboard_filter_form", app_text)
        self.assertIn("aplicados automaticamente", app_text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
