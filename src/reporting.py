"""Generate a compact multilingual executive PDF from the active dashboard scope."""

from __future__ import annotations

from datetime import datetime
from io import BytesIO
from typing import Any

from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.shapes import Drawing
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from src.analytics import executive_metric_series, unit_period_ranking
from src.executive_intelligence import (
    executive_narrative_i18n,
    executive_recommendations,
    mental_latest,
    periodic_coverage,
    severity_proxy,
)
from src.i18n import normalize_language, tr
from src.transforms import compute_overview_kpis


def _safe_text(text, fallback="—"):
    if text is None:
        return fallback
    try:
        s = str(text).strip()
        if not s:
            return fallback
        s = s.replace("\xa0", " ").replace("\x00", "")
        return s
    except Exception:
        return fallback


def _safe_para(text, style, fallback="—"):
    return Paragraph(_safe_text(text, fallback), style)


def _safe_number(value, fallback="0"):
    try:
        if value is None:
            return fallback
        return f"{float(value):,.0f}".replace(",", ".")
    except Exception:
        return fallback


def _number(value: float) -> str:
    return _safe_number(value)


def _line_chart(months: list[str], values: list[float]) -> Drawing:
    drawing = Drawing(720, 230)
    chart = HorizontalLineChart()
    chart.x = 55
    chart.y = 45
    chart.height = 135
    chart.width = 620
    chart.data = [values]
    chart.categoryAxis.categoryNames = months
    chart.categoryAxis.labels.angle = 25
    chart.categoryAxis.labels.fontSize = 8
    chart.valueAxis.labels.fontSize = 8
    chart.lines[0].strokeColor = colors.HexColor("#2563EB")
    chart.lines[0].strokeWidth = 2
    drawing.add(chart)
    return drawing


def _bar_chart(labels: list[str], values: list[float]) -> Drawing:
    drawing = Drawing(720, 240)
    chart = VerticalBarChart()
    chart.x = 55
    chart.y = 45
    chart.height = 140
    chart.width = 620
    chart.data = [values]
    chart.categoryAxis.categoryNames = labels
    chart.categoryAxis.labels.fontSize = 8
    chart.valueAxis.labels.fontSize = 8
    chart.bars[0].fillColor = colors.HexColor("#10B981")
    drawing.add(chart)
    return drawing


def _copy(language: str) -> dict[str, str]:
    if language == "en":
        return {
            "title": "Executive Report — Medical Service CGR 2026",
            "generated": "Generated",
            "user": "User",
            "quality": "Data quality",
            "source": "Source status",
            "indicator": "Metric",
            "current": "Current / period",
            "previous": "Previous",
            "alerts": "Management priorities",
            "trend": "Lost-day trend",
            "ranking": "Lost days by unit",
            "unit": "Unit",
            "share": "Share",
            "disclaimer": "Management report generated from aggregated dashboard data. It does not replace clinical, occupational or regulatory assessment.",
        }
    if language == "fr":
        return {
            "title": "Rapport Executif — Service Medical CGR 2026",
            "generated": "Genere",
            "user": "Utilisateur",
            "quality": "Qualite des donnees",
            "source": "Etat de la source",
            "indicator": "Indicateur",
            "current": "Actuel / periode",
            "previous": "Precedent",
            "alerts": "Priorites de gestion",
            "trend": "Evolution des jours perdus",
            "ranking": "Jours perdus par unite",
            "unit": "Unite",
            "share": "Part",
            "disclaimer": "Rapport de gestion produit a partir de donnees agregees.",
        }
    return {
        "title": "Relatorio Executivo — Servico Medico CGR 2026",
        "generated": "Gerado em",
        "user": "Usuario",
        "quality": "Qualidade dos dados",
        "source": "Status da fonte",
        "indicator": "Indicador",
        "current": "Atual / periodo",
        "previous": "Anterior",
        "alerts": "Prioridades gerenciais",
        "trend": "Tendencia de dias perdidos",
        "ranking": "Dias perdidos por unidade",
        "unit": "Unidade",
        "share": "Participacao",
        "disclaimer": "Relatorio gerencial gerado a partir de dados agregados do dashboard. Nao substitui avaliacao clinica, ocupacional ou normativa.",
    }


def build_executive_pdf(
    data: dict[str, Any],
    months: list[str],
    units: list[str],
    *,
    generated_by: str = "",
    language: str = "pt",
    source_status: str = "",
    quality_score: float | None = None,
) -> bytes:
    language = normalize_language(language)
    copy = _copy(language)
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        rightMargin=16 * mm,
        leftMargin=16 * mm,
        topMargin=14 * mm,
        bottomMargin=14 * mm,
        title=copy["title"],
    )
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="CenterTitle", parent=styles["Title"], alignment=TA_CENTER, textColor=colors.HexColor("#0F172A")))
    story: list[Any] = [_safe_para(copy["title"], styles["CenterTitle"]), Spacer(1, 5 * mm)]
    period_str = f"{months[0]} - {months[-1]}" if months and len(months) > 1 else (months[0] if months else "—")
    units_str = ", ".join([str(u) for u in units]) if units else "—"
    context = (
        f"{_safe_text(tr('period', language), 'Periodo')}: {_safe_text(period_str)} | "
        f"{_safe_text(tr('units', language), 'Unidades')}: {_safe_text(units_str)} | {_safe_text(copy['generated'])}: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    )
    if generated_by:
        context += f" | {copy['user']}: {_safe_text(generated_by)}"
    if source_status:
        context += f" | {copy['source']}: {_safe_text(source_status)}"
    if quality_score is not None:
        context += f" | {copy['quality']}: {quality_score:.0f}%"
    story.extend([_safe_para(context, styles["Normal"]), Spacer(1, 4 * mm)])

    metric_frame = executive_metric_series(data, months, units)
    narrative = executive_narrative_i18n(data, months, units, metric_frame, language=language)
    story.extend([
        _safe_para(narrative, styles["BodyText"], "Sem narrativa disponivel para o periodo selecionado."),
        Spacer(1, 5 * mm),
    ])

    kpis = compute_overview_kpis(data, months, units)
    mental_current, mental_previous = mental_latest(metric_frame)
    periodic_current, periodic_previous = periodic_coverage(data, months)
    severity_current, severity_previous = severity_proxy(kpis)
    rows = [
        [copy["indicator"], copy["current"], copy["previous"]],
        [tr("exams", language), _number(kpis["exames"]["current"]), _number(kpis["exames"]["previous"])],
        [tr("appointments", language), _number(kpis["atendimentos"]["current"]), _number(kpis["atendimentos"]["previous"])],
        [tr("active_leaves", language), _number(kpis["afastamentos"]["current"]), _number(kpis["afastamentos"]["previous"])],
        [tr("lost_days", language), _number(kpis["absenteismo"]["current"]), _number(kpis["absenteismo"]["previous"])],
        [tr("srq_cases", language), _number(mental_current), _number(mental_previous)],
        [tr("periodic_coverage", language), f"{periodic_current:.1f}%", f"{periodic_previous:.1f}%"],
        [tr("absence_severity_proxy", language), f"{severity_current:.1f}", f"{severity_previous:.1f}"],
    ]
    table = Table(rows, colWidths=[90 * mm, 65 * mm, 50 * mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F172A")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#CBD5E1")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))
    story.extend([table, Spacer(1, 6 * mm)])

    priorities = executive_recommendations(data, months, units, metric_frame, language=language)
    if priorities:
        story.append(_safe_para(copy["alerts"], styles["Heading2"]))
        for _icon, title, message in priorities:
            safe_title = _safe_text(title, "Sem titulo")
            safe_msg = _safe_text(message, "—")
            story.append(_safe_para(f"• <b>{safe_title}</b>: {safe_msg}", styles["BodyText"]))
        story.append(Spacer(1, 4 * mm))

    if not metric_frame.empty:
        story.append(_safe_para(copy["trend"], styles["Heading2"]))
        story.append(_line_chart(metric_frame["Mês"].astype(str).tolist(), metric_frame["Dias Perdidos"].astype(float).tolist()))

    ranking = unit_period_ranking(data, months, units, "Dias Perdidos")
    if not ranking.empty:
        story.extend([PageBreak(), _safe_para(copy["ranking"], styles["Heading2"]), _bar_chart(ranking["Unidade"].astype(str).tolist(), ranking["Valor"].astype(float).tolist())])
        ranking_rows = [[copy["unit"], tr("lost_days", language), copy["share"]]] + [
            [str(row["Unidade"]), _number(float(row["Valor"])), f"{float(row['Participação (%)']):.1f}%"]
            for _, row in ranking.iterrows()
        ]
        rt = Table(ranking_rows, colWidths=[70 * mm, 60 * mm, 50 * mm])
        rt.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F172A")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#CBD5E1")),
            ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
            ("PADDING", (0, 0), (-1, -1), 6),
        ]))
        story.append(rt)

    story.extend([Spacer(1, 6 * mm), _safe_para(f"{_safe_text(tr('confidentiality', language))} {_safe_text(copy['disclaimer'])}", styles["Italic"])])
    doc.build(story)
    return buffer.getvalue()
