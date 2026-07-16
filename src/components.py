"""
Components Module — Dashboard SM CGR 2026
=========================================
Reusable UI components for the executive dark-mode dashboard:
header, KPI cards, section titles, insights, rankings, and filter badges.
"""

from __future__ import annotations

import html
from datetime import datetime
from functools import lru_cache

import streamlit as st

from src.config import COLORS
from src.i18n import normalize_language, tr
from src.transforms import calc_variation

# ---------------------------------------------------------------------------
# Executive Header
# ---------------------------------------------------------------------------

def render_header(
    selected_months: list[str] | None = None,
    updated_at: object | None = None,
    *,
    language: str = "pt",
) -> None:
    """Render a clean, multilingual executive header."""
    language = normalize_language(language)
    months = selected_months or []
    if not months:
        period_text = "—"
    elif len(months) == 1:
        period_text = months[0]
    else:
        period_text = f"{months[0]} – {months[-1]}"

    if hasattr(updated_at, "strftime"):
        update_text = updated_at.strftime("%d/%m/%Y %H:%M")
    else:
        update_text = "—"

    st.markdown(f"""
    <div class="dashboard-header clean-header">
        <div class="header-main">
            <div class="header-title">🏥 {html.escape(tr('dashboard_title', language))}</div>
            <div class="header-subtitle">{html.escape(tr('dashboard_subtitle', language))}</div>
            <div class="header-meta clean-meta">
                <div class="header-meta-item">📅 <span>{html.escape(tr('period', language))}: <b>{html.escape(period_text)}</b></span></div>
                <div class="header-meta-item">🔄 <span>{html.escape(tr('updated_at', language))}: <b>{html.escape(update_text)}</b></span></div>
            </div>
        </div>
        <div class="header-badge">{html.escape(tr('executive_panel', language))}</div>
    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Executive Filter Badges Container
# ---------------------------------------------------------------------------

def render_filter_badge(label: str, value: str, active: bool = False) -> None:
    """Render a visual filter badge for active selections."""
    active_class = "active" if active else ""
    st.markdown(f"""
    <span class="filter-badge {active_class}">
        <b>{label}:</b> {value}
    </span>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# KPI Card (renders a single card with full HTML)
# ---------------------------------------------------------------------------

@lru_cache(maxsize=128)
def _render_sparkline_svg(values: tuple[float, ...], color: str) -> str:
    """Cached SVG sparkline renderer (performance optimized)."""
    if len(values) < 2:
        return ""

    width, height = 92, 26
    min_v = min(values)
    max_v = max(values)
    span = max_v - min_v or 1.0
    n = len(values)

    # Build points
    points = []
    for i in range(n):
        x = (i / (n - 1)) * (width - 6) + 3
        y = height - 4 - ((values[i] - min_v) / span) * (height - 8)
        points.append(f"{x:.1f},{y:.1f}")

    polyline = " ".join(points)
    last_x, last_y = points[-1].split(",")

    return (
        '<div class="kpi-sparkline" aria-hidden="true" style="margin: 4px 0 2px;">'
        f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" '
        'style="display:block; shape-rendering: geometricPrecision;">'
        f'<polyline points="{polyline}" fill="none" stroke="{color}" '
        'stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round"/>'
        f'<circle cx="{last_x}" cy="{last_y}" r="2.3" fill="{color}" opacity="0.9"/>'
        '</svg></div>'
    )


def _sparkline_svg(series: list[float] | tuple[float, ...] | None, color: str) -> str:
    """Optimized compact SVG sparkline for KPI cards.

    - Uses lru_cache for repeated identical calls
    - No gradient/defs (lighter parsing)
    - Only polyline + last point highlight (best signal-to-noise)
    """
    values = tuple(float(v) for v in (series or []) if isinstance(v, (int, float)))
    if len(values) < 2:
        return ""
    return _render_sparkline_svg(values, color)


def _target_status(value: float, target: float | None, target_direction: str) -> tuple[str, str, str]:
    # REMOVIDO: badge CRITICO / Meta solicitado pelo usuario
    return "", "", ""


def _build_kpi_html(
    icon: str,
    label: str,
    value: str,
    current: float = 0.0,
    previous: float = 0.0,
    color: str = "blue",
    delay: int = 1,
    suffix: str = "",
    show_trend: bool = True,
    context: str = "",
    trend_label: str = "",
    series: list[float] | tuple[float, ...] | None = None,
    target: float | None = None,
    target_direction: str = "higher",
    tooltip: str = "",
) -> str:
    """Build a KPI card with trend, target status and a compact sparkline."""
    variation = calc_variation(current, previous)
    label = html.escape(str(label))
    value = html.escape(str(value))
    context = html.escape(str(context))
    trend_label = html.escape(str(trend_label))
    tooltip = html.escape(str(tooltip), quote=True)
    help_html = '<span class="kpi-help">ⓘ</span>' if tooltip else ''

    trend_html = ""
    if show_trend and previous != 0:
        actual_direction = "up" if variation > 0 else "down" if variation < 0 else "neutral"
        favourable = (
            variation >= 0 if target_direction == "higher"
            else variation <= 0 if target_direction == "lower"
            else None
        )
        semantic_class = "neutral" if favourable is None or variation == 0 else "good" if favourable else "bad"
        arrow = "▲" if actual_direction == "up" else "▼" if actual_direction == "down" else "●"
        trend_text = f"{variation:+.1f}%" if variation else "0.0%"
        lbl = trend_label or "em relação ao mês anterior"
        trend_html = f'<div class="kpi-trend {semantic_class}">{arrow} {trend_text} {lbl}</div>'

    # Badge CRITICO/Meta desabilitado conforme solicitado
    status, status_class, target_text = ("", "", "")
    status_html = ""

    context_html = f'<div class="kpi-context">{context}</div>' if context else ""
    sparkline = _sparkline_svg(series, COLORS.get(color, COLORS["blue"]))

    parts = [
        f'<div class="kpi-card {color} delay-{delay}">',
        '<div class="kpi-topline">',
        f'<div class="kpi-icon">{icon}</div>',
        status_html,
        '</div>',
        f'<div class="kpi-label" title="{tooltip}">{label} {help_html}</div>',
        f'<div class="kpi-value">{value}{suffix}</div>',
        context_html,
        sparkline,
        trend_html,
        '</div>',
    ]
    return ''.join(part for part in parts if part)


def render_kpi_card(
    icon: str,
    label: str,
    value: str,
    current: float = 0.0,
    previous: float = 0.0,
    color: str = "blue",
    delay: int = 1,
    suffix: str = "",
    show_trend: bool = True,
    context: str = "",
    trend_label: str = "",
    series: list[float] | tuple[float, ...] | None = None,
    target: float | None = None,
    target_direction: str = "higher",
    tooltip: str = "",
) -> None:
    html_block = _build_kpi_html(
        icon=icon, label=label, value=value, current=current, previous=previous,
        color=color, delay=delay, suffix=suffix, show_trend=show_trend,
        context=context, trend_label=trend_label, series=series,
        target=target, target_direction=target_direction, tooltip=tooltip,
    )
    st.markdown(html_block.strip(), unsafe_allow_html=True)


def render_kpi_row(kpis: list[dict], cols_count: int = 4) -> None:
    """Render responsive KPI rows, including optional targets and sparklines."""
    if not kpis:
        return
    safe_count = max(1, int(cols_count))
    for row_start in range(0, len(kpis), safe_count):
        row_items = kpis[row_start:row_start + safe_count]
        columns = st.columns(len(row_items))
        for local_index, (column, kpi) in enumerate(zip(columns, row_items)):
            with column:
                render_kpi_card(
                    icon=kpi.get("icon", "📊"),
                    label=kpi.get("label", ""),
                    value=kpi.get("value", "0"),
                    current=float(kpi.get("current", 0.0)),
                    previous=float(kpi.get("previous", 0.0)),
                    color=kpi.get("color", "blue"),
                    delay=row_start + local_index + 1,
                    suffix=kpi.get("suffix", ""),
                    show_trend=kpi.get("show_trend", True),
                    context=kpi.get("context", ""),
                    trend_label=kpi.get("trend_label", ""),
                    series=kpi.get("series"),
                    target=kpi.get("target"),
                    target_direction=kpi.get("target_direction", "higher"),
                    tooltip=kpi.get("tooltip", ""),
                )



def render_health_score_radial(score: float) -> None:
    """Render a reliable, responsive radial index using semantic HTML/CSS.

    The visual intentionally avoids Plotly for this compact overview element so
    it cannot disappear because of SVG/container sizing conflicts.
    """
    numeric_score = max(0.0, min(float(score or 0.0), 100.0))
    angle = numeric_score * 3.6
    accessible = f"Índice de Saúde Ocupacional: {numeric_score:.1f}%"
    markup = (
        '<div class="health-score-visual-card" role="img" '
        f'aria-label="{html.escape(accessible)}">'
        '<div class="health-score-visual-glow" aria-hidden="true"></div>'
        f'<div class="health-score-visual-ring" style="--score-angle:{angle:.2f}deg">'
        '<div class="health-score-visual-core">'
        f'<strong>{numeric_score:.1f}%</strong>'
        '<span>ÍNDICE GERAL</span>'
        '</div>'
        '</div>'
        '<div class="health-score-visual-caption">'
        '<strong>Saúde ocupacional</strong>'
        '<span>Composição inteligente: Exames + Presença + Saúde Mental (V12).</span>'
        '</div>'
        '</div>'
    )
    st.markdown(markup, unsafe_allow_html=True)


def render_health_score_breakdown_cards(frame) -> None:
    """Render the active score components without targets or status badges."""
    if frame is None or getattr(frame, "empty", True):
        st.info("Não há composição do índice para o período selecionado.")
        return

    icons = {
        "Exames periódicos": "🧪",
        "Presença no Periódico": "✅",
        "Saúde Mental (SRQ-20)": "🧠",
    }

    cards: list[str] = []
    for _, row in frame.iterrows():
        component = str(row.get("Componente", "Indicador"))
        value = max(0.0, min(float(row.get("Valor", 0.0) or 0.0), 100.0))
        points = float(row.get("Pontos", 0.0) or 0.0)
        weight = str(row.get("Peso", "—"))
        icon = icons.get(component, "📊")
        cards.extend(
            [
                '<article class="health-breakdown-card health-clean-card">',
                '<div class="health-breakdown-head">',
                f'<span class="health-breakdown-icon">{icon}</span>',
                '<div class="health-breakdown-heading">',
                f'<strong>{html.escape(component)}</strong>',
                f'<span>Participação no índice: {html.escape(weight)}</span>',
                '</div>',
                '</div>',
                '<div class="health-clean-value-row">',
                f'<strong>{value:.1f}%</strong>',
                f'<span>{points:.1f} pontos no índice</span>',
                '</div>',
                '<div class="health-breakdown-progress health-clean-progress" aria-hidden="true">',
                f'<span style="width:{value:.1f}%"></span>',
                '</div>',
                '</article>',
            ]
        )

    wrapper = (
        '<div class="health-breakdown-intro health-clean-intro">'
        '<div><span class="health-breakdown-eyebrow">COMPOSIÇÃO ATUAL</span>'
        '<h3>Componentes do índice</h3></div>'
        '<p>Leitura objetiva dos dois indicadores ativos no período selecionado.</p>'
        '</div>'
        '<div class="health-breakdown-grid health-clean-grid">'
        + "".join(cards)
        + '</div>'
    )
    st.markdown(wrapper, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Section Header
# ---------------------------------------------------------------------------

def render_section_header(icon: str, title: str) -> None:
    """Render a styled section header with icon."""
    st.markdown(f"""
    <div class="section-header">
        <span class="section-icon">{icon}</span>
        <h2>{title}</h2>
    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Chart Container
# ---------------------------------------------------------------------------

def render_chart_container(title: str, dot_color: str = "blue") -> str:
    """Return HTML for chart container opening. Use with st.markdown."""
    return f"""
    <div class="chart-container">
        <div class="chart-title">
            <span class="dot dot-{dot_color}"></span>
            {title}
        </div>
    </div>
    """


def chart_title_html(title: str, dot_color: str = "blue") -> str:
    """Return just the title HTML to place above a Plotly chart."""
    return f"""
    <div class="chart-title" style="margin-bottom: 0.5rem;">
        <span class="dot dot-{dot_color}"></span>
        {title}
    </div>
    """


# ---------------------------------------------------------------------------
# Insight Cards
# ---------------------------------------------------------------------------

def render_insight(icon: str, title: str, text: str, card_type: str = "") -> None:
    """Render insight using modern Shadcn-style alert."""
    variant_map = {
        "success": "success",
        "warning": "warning",
        "danger": "destructive",
        "": "default"
    }
    variant = variant_map.get(card_type, "default")
    shad_alert(title=f"{icon} {title}", message=text, variant=variant)


# ---------------------------------------------------------------------------
# Ranking Rows
# ---------------------------------------------------------------------------

def render_ranking(position: int, text: str, value: str = "") -> None:
    """Render a single ranking row with medals for top 3 positions."""
    if position == 1:
        pos_class = "gold"
        medal = "🥇"
    elif position == 2:
        pos_class = "silver"
        medal = "🥈"
    elif position == 3:
        pos_class = "bronze"
        medal = "🥉"
    else:
        pos_class = "default"
        medal = f"{position}º"

    value_html = f'<div class="ranking-value">{value}</div>' if value else ""

    st.markdown(f"""
    <div class="ranking-row">
        <div class="ranking-position {pos_class}">{medal}</div>
        <div class="ranking-text">{text}</div>
        {value_html}
    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Sidebar Section
# ---------------------------------------------------------------------------

def sidebar_section(title: str) -> None:
    """Render a sidebar section header."""
    st.sidebar.markdown(f'<div class="sidebar-section">{title}</div>', unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Metric Summary
# ---------------------------------------------------------------------------

def render_metric_summary(
    title: str,
    value: str,
    context: str = "",
    border_color: str = "blue"
) -> None:
    """Render a compact metric summary component with custom color border."""
    st.markdown(f"""
    <div style="border-left: 3px solid var(--{border_color}, #3B82F6); padding-left: 0.75rem; margin-bottom: 0.75rem;">
        <div style="font-size: 0.7rem; text-transform: uppercase; color: var(--text-secondary); font-weight: 600; letter-spacing: 0.05em;">{title}</div>
        <div style="font-size: 1.15rem; font-weight: 700; color: var(--text-primary); margin-top: 0.1rem;">{value}</div>
        {f'<div style="font-size: 0.7rem; color: var(--text-muted); margin-top: 0.05rem;">{context}</div>' if context else ''}
    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Spacer
# ---------------------------------------------------------------------------

def spacer(height: str = "1rem") -> None:
    """Add vertical spacing."""
    st.markdown(f'<div style="height: {height};"></div>', unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Responsive Layout Helpers
# ---------------------------------------------------------------------------

def get_responsive_columns(desktop_ratio: list[float] | float, tablet_ratio: list[float] | float | None = None, mobile_stacked: bool = True) -> tuple:
    """
    Create responsive columns that adapt to screen size.
    
    On desktop: uses desktop_ratio
    On tablet (768-1024px): uses tablet_ratio if provided, else desktop_ratio
    On mobile (< 768px): stacks vertically if mobile_stacked=True
    
    Args:
        desktop_ratio: Column ratio for desktop (e.g., [3, 2] or [2, 1, 1])
        tablet_ratio: Column ratio for tablet (optional)
        mobile_stacked: If True, stack columns on mobile (returns single column)
    
    Returns:
        tuple of Streamlit columns
    """
    # Use query params to detect if we're on mobile (Streamlit doesn't have native screen size detection)
    # For now, use desktop ratio as default - CSS media queries handle actual responsiveness
    ratio = desktop_ratio if isinstance(desktop_ratio, list) else [desktop_ratio]
    return st.columns(ratio)


def responsive_columns_equal(n: int) -> tuple:
    """Create n equally-sized responsive columns."""
    return st.columns(n)


def create_two_column_layout(left_ratio: float = 3, right_ratio: float = 2) -> tuple:
    """Create a responsive two-column layout (common pattern)."""
    return st.columns([left_ratio, right_ratio])


def create_sidebar_layout() -> None:
    """Inject CSS for responsive sidebar handling on mobile."""
    st.markdown("""
    <style>
    @media (max-width: 768px) {
        section[data-testid="stSidebar"] {
            position: relative;
            width: 100% !important;
            min-width: auto !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Filter context, quality and alert components
# ---------------------------------------------------------------------------

def render_filter_context(
    *,
    months: list[str] | tuple[str, ...],
    units: list[str] | tuple[str, ...],
    page: str,
    source_updated_at: object | None = None,
    applied_at: object | None = None,
    language: str = "pt",
) -> None:
    """Show the current scope in a compact multilingual card."""
    language = normalize_language(language)
    if page in {"Exames", "Atendimentos"}:
        unit_text = tr("consolidated_source", language)
    else:
        unit_text = ", ".join(units) if units else "—"
    month_text = ", ".join(months) if months else "—"
    from src.i18n import page_label
    st.markdown(
        f"""
        <div class="filter-context-card compact-filter-context">
            <span><b>{html.escape(tr('page', language))}:</b> {html.escape(page_label(page, language))}</span>
            <span><b>{html.escape(tr('months', language))}:</b> {html.escape(month_text)}</span>
            <span><b>{html.escape(tr('units', language))}:</b> {html.escape(unit_text)}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_executive_narrative(text: str | list | None, *, title: str = "Leitura executiva do período", collapsible: bool = True) -> None:
    """Render executive narrative with optional collapsible behavior."""
    
    def _render_content():
        # Handle different text types safely
        if isinstance(text, list):
            safe_text = "<br>".join(str(item) for item in text)
        elif text is None:
            safe_text = "Nenhum resumo disponível."
        else:
            safe_text = str(text)
        
        st.markdown(
            f"""
            <div class="executive-narrative">
                <div class="executive-narrative-text">{html.escape(safe_text)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    if collapsible:
        shad_collapsible(
            title=f"🧭 {title}",
            content_func=_render_content,
            default_open=True,
            key="collapsible_executive_narrative"
        )
    else:
        _render_content()


def render_alerts(alerts: list[object], max_items: int = 4) -> None:
    """Render alert dataclasses without coupling the component to the module."""
    for alert in alerts[:max_items]:
        severity = getattr(alert, "severity", "warning")
        icon = {"danger": "🚨", "warning": "⚠️", "success": "✅", "info": "ℹ️"}.get(severity, "⚠️")
        render_insight(
            icon,
            str(getattr(alert, "title", "Alerta")),
            str(getattr(alert, "message", "")),
            severity if severity in {"danger", "warning", "success"} else "",
        )

# ---------------------------------------------------------------------------
# Empty states and source status
# ---------------------------------------------------------------------------

def render_empty_state(
    title: str,
    message: str,
    *,
    icon: str = "🔎",
    hint: str = "Use os filtros laterais para alterar o escopo.",
) -> None:
    """Modern empty state using Shadcn-style alert."""
    shad_alert(
        title=title,
        message=f"{message} {hint}",
        variant="default"
    )


def render_data_quality_section(summary: dict, *, title: str = "Qualidade dos Dados", collapsible: bool = True) -> None:
    """Modern Data Quality section using Shadcn-style + collapsible behavior."""
    
    def _render_content():
        if not summary or not summary.get("has_data"):
            shad_alert(
                "Dados insuficientes",
                "Não foi possível avaliar a completude dos dados no período selecionado. Verifique o arquivo e os filtros.",
                variant="warning"
            )
            return

        completeness = summary.get("completeness_pct", 0)
        last_month = summary.get("last_month_with_data", "—")
        missing = summary.get("missing_months", [])
        notes = summary.get("notes", [])

        record_counts = summary.get("record_counts", {})
        source_filename = summary.get("source_filename", "—")
        updated_at = summary.get("updated_at")

        content_parts = [
            f"<div><strong>Último mês com dados:</strong> {html.escape(str(last_month))}</div>",
        ]

        if missing:
            content_parts.append(f"<div><strong>Meses sem dados:</strong> <span style='color:#f59e0b'>{', '.join(missing)}</span></div>")

        if record_counts:
            rec_text = []
            if record_counts.get("exam_types"):
                rec_text.append(f"Exames: {record_counts['exam_types']}")
            if record_counts.get("mental_rows"):
                rec_text.append(f"Saúde Mental: {record_counts['mental_rows']}")
            if rec_text:
                content_parts.append(f"<div><strong>Registros:</strong> {' • '.join(rec_text)}</div>")

        if updated_at and hasattr(updated_at, "strftime"):
            content_parts.append(f"<div><strong>Atualizado em:</strong> {updated_at.strftime('%d/%m/%Y %H:%M')}</div>")

        if source_filename != "—":
            content_parts.append(f"<div><strong>Arquivo:</strong> {html.escape(source_filename)}</div>")

        if notes:
            content_parts.append(f"<div style='margin-top:0.5rem; font-size:0.85rem; color:#94a3b8'>{ ' • '.join(notes) }</div>")

        content = "".join(content_parts)

        shad_card(
            title=title,
            content=content,
            icon="📊",
            class_name="border border-white/10"
        )

    if collapsible:
        shad_collapsible(
            title=title,
            content_func=_render_content,
            default_open=True,
            key=f"collapsible_{title.replace(' ', '_').lower()}"
        )
    else:
        _render_content()


def render_source_status(
    *,
    filename: str,
    updated_at: object | None,
    load_seconds: float | None,
    quality_score: float | None,
    stale: bool = False,
    source_type: str = "local",
    fallback_used: bool = False,
    size_bytes: int | None = None,
    checksum: str = "",
    checked_at: object | None = None,
    changed_at: object | None = None,
    next_check_at: object | None = None,
    language: str = "pt",
) -> None:
    """Show a simplified multilingual operational status."""
    language = normalize_language(language)

    def format_datetime(value: object | None) -> str:
        if hasattr(value, "strftime"):
            return value.strftime("%d/%m/%Y %H:%M")
        if isinstance(value, str) and value:
            try:
                return datetime.fromisoformat(value).strftime("%d/%m/%Y %H:%M")
            except ValueError:
                return value
        return "—"

    changed_text = format_datetime(changed_at or updated_at)
    checked_text = format_datetime(checked_at)

    source_labels = {
        "google_sheets": "Google Sheets",
        "url": "URL remota",
        "local": "Local / OneDrive",
        "sharepoint": "SharePoint",
    }
    source_text = source_labels.get(source_type, source_type)

    if fallback_used:
        status_class = "stale"
        state_text = "🟠 " + tr("contingency_active", language)
    elif stale:
        status_class = "stale"
        state_text = "🟡 " + tr("data_attention", language)
    else:
        status_class = "healthy"
        state_text = "🟢 " + tr("source_synced", language)

    st.markdown(
        f"""
        <div class="source-status-card compact-source-status {status_class}">
            <div class="source-status-main">
                <span><b>{html.escape(tr('source', language))}:</b> {html.escape(source_text)}</span>
                <span><b>{html.escape(tr('last_update', language))}:</b> {html.escape(changed_text)}</span>
                <span><b>{html.escape(tr('last_check', language))}:</b> {html.escape(checked_text)}</span>
            </div>
            <div class="source-status-state">{html.escape(state_text)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================================
# SHADCN-STYLE COMPONENTS (Modern, clean, Tailwind-based)
# ============================================================================

def shad_card(title: str, content: str, *, icon: str = "", class_name: str = "") -> None:
    """Modern Shadcn-style card with advanced Tailwind entrance animation."""
    html_content = f"""
    <div class="bg-[#111827] border border-white/10 rounded-2xl p-6 shadow-soft hover:border-[#2563EB]/40 transition-all duration-200 animate-fade-in-up {class_name}">
        <div class="flex items-center gap-3 mb-4">
            {f'<div class="text-2xl">{icon}</div>' if icon else ''}
            <div class="text-lg font-semibold text-[#F1F5F9] tracking-tight">{html.escape(title)}</div>
        </div>
        <div class="text-[#CBD5E1] text-[15px] leading-relaxed">
            {content}
        </div>
    </div>
    """
    st.markdown(html_content, unsafe_allow_html=True)


def shad_badge(text: str, variant: str = "default") -> str:
    """Shadcn-style badge."""
    variants = {
        "default": "bg-white/10 text-white border-white/20",
        "success": "bg-emerald-500/15 text-emerald-400 border-emerald-500/30",
        "warning": "bg-amber-500/15 text-amber-400 border-amber-500/30",
        "destructive": "bg-red-500/15 text-red-400 border-red-500/30",
        "outline": "bg-transparent border-white/30 text-white/80"
    }
    classes = variants.get(variant, variants["default"])
    return f'<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border {classes}">{html.escape(text)}</span>'


def shad_alert(title: str, message: str, variant: str = "default") -> None:
    """Shadcn-style alert component."""
    variants = {
        "default": "border-white/20 bg-white/5",
        "success": "border-emerald-500/40 bg-emerald-950/30",
        "warning": "border-amber-500/40 bg-amber-950/30",
        "destructive": "border-red-500/40 bg-red-950/30",
    }
    classes = variants.get(variant, variants["default"])
    
    icon_map = {"default": "ℹ️", "success": "✅", "warning": "⚠️", "destructive": "🚨"}
    icon = icon_map.get(variant, "ℹ️")

    st.markdown(f"""
    <div class="shad-alert {classes}">
        <div class="flex gap-3">
            <div class="text-lg mt-0.5">{icon}</div>
            <div>
                <div class="font-semibold text-white mb-1">{html.escape(title)}</div>
                <div class="text-sm text-white/70">{html.escape(message)}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def shad_metric(label: str, value: str, change: str = "", trend: str = "neutral") -> None:
    """Clean metric card in Shadcn style."""
    trend_color = {"up": "text-emerald-400", "down": "text-red-400", "neutral": "text-white/60"}.get(trend, "text-white/60")

    st.markdown(f"""
    <div class="shad-metric">
        <div class="text-xs text-white/60 tracking-wider uppercase mb-1">{html.escape(label)}</div>
        <div class="text-3xl font-semibold text-white tracking-tighter">{html.escape(value)}</div>
        {f'<div class="text-sm mt-1 {trend_color}">{html.escape(change)}</div>' if change else ''}
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# CROSS-FILTERING SYSTEM (Interactive filtering between charts)
# Suporte completo a múltiplos filtros simultâneos
# ============================================================================

def init_cross_filter_state():
    """Initialize session state for multiple cross-filters."""
    if "cross_filters" not in st.session_state:
        st.session_state.cross_filters = {}  # {filter_type: filter_value}


def get_cross_filters():
    """Return all active cross-filters as a dictionary."""
    init_cross_filter_state()
    return st.session_state.cross_filters


def set_cross_filter(filter_type: str, filter_value: any):
    """Add or update a cross-filter (supports multiple filters)."""
    init_cross_filter_state()
    st.session_state.cross_filters[filter_type] = filter_value


def remove_cross_filter(filter_type: str):
    """Remove a specific cross-filter."""
    init_cross_filter_state()
    if filter_type in st.session_state.cross_filters:
        del st.session_state.cross_filters[filter_type]


def clear_all_cross_filters():
    """Remove all active cross-filters."""
    st.session_state.cross_filters = {}


def apply_cross_filters(df: pd.DataFrame) -> pd.DataFrame:
    """Apply all active cross-filters to a DataFrame.
    
    The DataFrame columns must match the filter_type keys.
    """
    init_cross_filter_state()
    filters = st.session_state.cross_filters
    
    if not filters:
        return df
    
    filtered_df = df.copy()
    
    for filter_type, filter_value in filters.items():
        if filter_type in filtered_df.columns:
            filtered_df = filtered_df[
                filtered_df[filter_type].astype(str) == str(filter_value)
            ]
    
    return filtered_df


def render_cross_filters_status():
    """Display all active filters with individual remove buttons."""
    init_cross_filter_state()
    filters = st.session_state.cross_filters
    
    if not filters:
        return
    
    st.caption("**Filtros ativos entre gráficos:**")
    
    # Create columns for each filter + clear all button
    num_filters = len(filters)
    cols = st.columns(num_filters + 1)
    
    for idx, (filter_type, filter_value) in enumerate(filters.items()):
        with cols[idx]:
            if st.button(
                f"✕ {filter_type}: {filter_value}", 
                key=f"remove_{filter_type}",
                help=f"Remover filtro de {filter_type}"
            ):
                remove_cross_filter(filter_type)
                st.rerun()
    
    # Clear all button
    with cols[-1]:
        if st.button("Limpar todos", key="clear_all_cross_filters"):
            clear_all_cross_filters()
            st.rerun()


# ============================================================================
# DYNAMIC FILTERS (Filtros dinâmicos baseados nos dados)
# ============================================================================

def render_dynamic_filter(
    df: pd.DataFrame,
    column: str,
    label: str = None,
    multiselect: bool = True,
    key: str = None
) -> list:
    """Render a dynamic filter (selectbox or multiselect) based on DataFrame column.
    
    Returns the selected values.
    """
    if column not in df.columns:
        return []
    
    unique_values = sorted(df[column].dropna().astype(str).unique().tolist())
    
    if not unique_values:
        return []
    
    label = label or column.replace("_", " ").title()
    key = key or f"dynamic_filter_{column}"
    
    if multiselect:
        selected = st.multiselect(
            label,
            options=unique_values,
            default=unique_values,  # All selected by default
            key=key
        )
    else:
        selected = st.selectbox(
            label,
            options=["Todos"] + unique_values,
            key=key
        )
        if selected == "Todos":
            selected = unique_values
        else:
            selected = [selected]
    
    return selected


def apply_dynamic_filters(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    """Apply multiple dynamic filters to a DataFrame.
    
    filters = {
        "unidade": ["B2BN", "B2BF"],
        "tipo_exame": ["Admissional"]
    }
    """
    filtered_df = df.copy()
    
    for column, selected_values in filters.items():
        if column in filtered_df.columns and selected_values:
            filtered_df = filtered_df[
                filtered_df[column].astype(str).isin([str(v) for v in selected_values])
            ]
    
    return filtered_df


def render_dynamic_filters_panel(
    df: pd.DataFrame,
    columns: list[str],
    title: str = "Filtros Dinâmicos"
) -> dict:
    """Render a complete panel of dynamic filters.
    
    Returns a dictionary with selected values for each column.
    """
    st.subheader(title)
    
    selected_filters = {}
    
    for col in columns:
        if col in df.columns:
            selected = render_dynamic_filter(
                df=df,
                column=col,
                multiselect=True,
                key=f"panel_{col}"
            )
            if selected:
                selected_filters[col] = selected
    
    return selected_filters


# ============================================================================
# ADDITIONAL SHADCN COMPONENTS
# ============================================================================

def shad_tabs(tabs: list[str], key: str = "shad_tabs") -> int:
    """Shadcn-style tabs using Streamlit tabs."""
    return st.tabs(tabs)


def shad_progress(value: float, label: str = "", max_value: float = 100.0) -> None:
    """Shadcn-style progress bar."""
    percentage = min(max(value / max_value, 0), 1)
    
    st.markdown(f"""
    <div class="shad-progress-container">
        {f'<div class="shad-progress-label">{html.escape(label)}</div>' if label else ''}
        <div class="shad-progress-bar">
            <div class="shad-progress-fill" style="width: {percentage * 100}%;"></div>
        </div>
        <div class="shad-progress-value">{value:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)


def shad_skeleton(lines: int = 3, width: str = "100%") -> None:
    """Shadcn-style loading skeleton."""
    skeleton_html = ""
    for i in range(lines):
        w = "60%" if i == lines - 1 else width
        skeleton_html += f'<div class="shad-skeleton" style="width: {w};"></div>'
    
    st.markdown(f"""
    <div class="shad-skeleton-container">
        {skeleton_html}
    </div>
    """, unsafe_allow_html=True)


def shad_button(label: str, variant: str = "default", key: str = None) -> bool:
    """Shadcn-style button."""
    return st.button(label, key=key)


def shad_collapsible(title: str, content_func, *, 
                     default_open: bool = True,
                     key: str = None,
                     icon_closed: str = "▶",
                     icon_open: str = "▼") -> None:
    """
    Componente colapsável moderno estilo Shadcn (versão mais robusta).
    """
    if key is None:
        key = f"collapsible_{title.lower().replace(' ', '_').replace('🧭', '').strip()}"

    if key not in st.session_state:
        st.session_state[key] = default_open

    is_open = st.session_state[key]
    button_label = f"{icon_open if is_open else icon_closed}  {title}"

    with st.container():
        if st.button(button_label, key=f"{key}_toggle", use_container_width=True):
            st.session_state[key] = not is_open
            st.rerun()

        if is_open:
            st.markdown('<div class="animate-expand open">', unsafe_allow_html=True)
            content_func()
            st.markdown('</div>', unsafe_allow_html=True)


def render_premium_progress_bar(
    label: str,
    value: float,
    max_value: float = 100.0,
    color: str = "#EC4899",
    show_delta: float | None = None,
    height: int = 28,
) -> None:
    """Render a modern premium progress bar (V12)."""
    pct = max(0.0, min(float(value) / max(max_value, 1e-6) * 100.0, 100.0))
    delta_html = ""
    if show_delta is not None:
        delta_val = float(show_delta)
        if delta_val > 0.05:
            delta_label = f"subiu {abs(delta_val):.1f} pontos".replace(".", ",")
            delta_color = "#34D399"
        elif delta_val < -0.05:
            delta_label = f"caiu {abs(delta_val):.1f} pontos".replace(".", ",")
            delta_color = "#F87171"
        else:
            delta_label = "estável"
            delta_color = "#94A3B8"
        delta_html = f'<span style="color:{delta_color};font-weight:600;margin-left:10px;font-size:0.9rem">{delta_label}</span>'

    markup = f'''
    <div class="premium-progress-card" style="
        background: linear-gradient(135deg, rgba(26,20,51,0.95), rgba(30,18,64,0.9));
        border: 1px solid rgba(124,58,237,0.25);
        border-radius: 16px;
        padding: 16px 20px;
        margin-bottom: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.25);
    ">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
            <span style="color:#E2E8F0;font-weight:600;font-size:0.95rem;">{html.escape(label)}</span>
            <div style="display:flex;align-items:center;">
                <span style="color:#F8FAFC;font-weight:700;font-size:1.15rem;">{pct:.1f}%</span>
                {delta_html}
            </div>
        </div>
        <div style="
            width:100%;
            height:{height}px;
            background: rgba(15,10,31,0.8);
            border-radius: 999px;
            overflow: hidden;
            position: relative;
            box-shadow: inset 0 2px 6px rgba(0,0,0,0.4);
        ">
            <div style="
                width: {pct:.2f}%;
                height: 100%;
                background: linear-gradient(90deg, {color}cc, {color});
                border-radius: 999px;
                transition: width 0.8s cubic-bezier(0.4,0,0.2,1);
                box-shadow: 0 0 12px {color}66;
                position: relative;
            ">
                <div style="
                    position: absolute;
                    top: 0; left: 0; right: 0; bottom: 0;
                    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent);
                    animation: shimmer 2.2s infinite;
                "></div>
            </div>
        </div>
    </div>
    '''
    st.markdown(markup, unsafe_allow_html=True)
