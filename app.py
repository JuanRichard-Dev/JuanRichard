"""Dashboard Serviço Médico CGR 2026 — V10 Responsive Health.

Power BI-style analytical experience built exclusively from the user's real
``Dashboard SM CGR 2026.xlsx`` workbook.
"""

from __future__ import annotations

# Native-runtime hardening must execute before importing NumPy, pandas,
# PyArrow or Streamlit. Community Cloud can run several sessions and fragment
# reruns in the same process; keeping native worker pools small reduces memory
# pressure and removes unnecessary cross-library thread contention.
import faulthandler
import os
import sys
from datetime import datetime
from hashlib import sha1
from typing import Any, Iterable

for _name in (
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "NUMEXPR_NUM_THREADS",
    "ARROW_NUM_THREADS",
):
    os.environ.setdefault(_name, "1")
os.environ.setdefault("PYTHONFAULTHANDLER", "1")
try:
    faulthandler.enable(file=sys.stderr, all_threads=True)
except (RuntimeError, OSError):
    # Some managed hosts do not expose a writable/fileno-compatible stderr.
    pass

import pandas as pd
import streamlit as st

# ---------------------------------------------------------------------------
# Page configuration — must be the first Streamlit command
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Dashboard SM CGR 2026",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.set_option("client.showSidebarNavigation", False)

# Tailwind CSS via CDN + Enhanced Configuration
st.markdown("""
<script src="https://cdn.tailwindcss.com"></script>
<script>
tailwind.config = {
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        'dark-bg': '#130A2B',
        'dark-card': '#1E1240',
        'dark-border': 'rgba(255,255,255,0.08)',
        'accent-blue': '#8B5CF6',
        'accent-green': '#EC4899',
        'accent-orange': '#D946EF',
        'accent-red': '#EF4444',
        'text-primary': '#F1F5F9',
        'text-secondary': '#94A3B8',
      },
      borderRadius: {
        'xl': '16px',
        '2xl': '20px',
      },
      boxShadow: {
        'soft': '0 4px 24px rgba(0, 0, 0, 0.25)',
        'glow': '0 0 20px rgba(37, 99, 235, 0.15)',
      },
      animation: {
        'fade-in-up': 'fadeInUp 0.5s ease-out forwards',
        'fade-in-down': 'fadeInDown 0.5s ease-out forwards',
        'fade-in': 'fadeIn 0.4s ease-out forwards',
        'scale-in': 'scaleIn 0.3s ease-out forwards',
        'zoom-in': 'zoomIn 0.4s ease-out forwards',
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'glow-pulse': 'glowPulse 2s ease-in-out infinite alternate',
        'slide-in-right': 'slideInRight 0.4s ease-out forwards',
        'slide-in-left': 'slideInLeft 0.4s ease-out forwards',
        'shimmer': 'shimmer 2s linear infinite',
        'float': 'float 3s ease-in-out infinite',
        'bounce-soft': 'bounceSoft 1s ease-in-out infinite',
        'progress': 'progress 1.5s ease-out forwards',
        'wiggle': 'wiggle 1s ease-in-out infinite',
        'heartbeat': 'heartbeat 1.5s ease-in-out infinite',
      },
      keyframes: {
        fadeInUp: {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        fadeInDown: {
          '0%': { opacity: '0', transform: 'translateY(-20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        scaleIn: {
          '0%': { opacity: '0', transform: 'scale(0.95)' },
          '100%': { opacity: '1', transform: 'scale(1)' },
        },
        zoomIn: {
          '0%': { opacity: '0', transform: 'scale(0.8)' },
          '100%': { opacity: '1', transform: 'scale(1)' },
        },
        glowPulse: {
          '0%': { boxShadow: '0 0 15px rgba(37, 99, 235, 0.2)' },
          '100%': { boxShadow: '0 0 30px rgba(37, 99, 235, 0.5)' },
        },
        slideInRight: {
          '0%': { opacity: '0', transform: 'translateX(30px)' },
          '100%': { opacity: '1', transform: 'translateX(0)' },
        },
        slideInLeft: {
          '0%': { opacity: '0', transform: 'translateX(-30px)' },
          '100%': { opacity: '1', transform: 'translateX(0)' },
        },
        shimmer: {
          '0%': { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-6px)' },
        },
        bounceSoft: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-4px)' },
        },
        progress: {
          '0%': { width: '0%' },
          '100%': { width: '100%' },
        },
        wiggle: {
          '0%, 100%': { transform: 'rotate(-3deg)' },
          '50%': { transform: 'rotate(3deg)' },
        },
        heartbeat: {
          '0%, 100%': { transform: 'scale(1)' },
          '14%': { transform: 'scale(1.1)' },
          '28%': { transform: 'scale(1)' },
          '42%': { transform: 'scale(1.1)' },
          '70%': { transform: 'scale(1)' },
        }
      }
    }
  }
}
</script>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Deployment dependency preflight
# ---------------------------------------------------------------------------
try:
    import plotly  # noqa: F401
except ModuleNotFoundError:
    st.error("A dependência Plotly não foi instalada no ambiente do Streamlit Cloud.")
    st.markdown(
        "O arquivo `requirements.txt` precisa estar na **raiz do repositório**, "
        "no mesmo nível de `app.py`. Depois do commit, reinicie ou recrie o app."
    )
    st.code(
        "plotly==6.5.2\nstreamlit==1.58.0\npandas==2.3.3\nnumpy==2.3.5\n"
        "pyarrow==20.0.0\nopenpyxl==3.1.5\nreportlab==4.4.10\nrequests==2.32.5",
        language="text",
    )
    st.stop()


# ---------------------------------------------------------------------------
# Local imports
# ---------------------------------------------------------------------------
from src.alerts import detect_anomalies, generate_alerts  # noqa: E402
from src.analytics import (  # noqa: E402
    build_executive_narrative,
    dynamic_title,
    executive_metric_series,
    linear_forecast_with_interval,
    metric_summary_matrix,
    period_label,
    reason_pareto_table,
    unit_change_contribution,
    unit_latest_ranking,
    unit_period_ranking,
)
from src.audit import log_event  # noqa: E402
from src.auth import enforce_authentication, render_user_sidebar  # noqa: E402
from src.auto_refresh import render_local_source_monitor  # noqa: E402
from src.charts import (  # noqa: E402
    bar_chart,
    bridge_waterfall_chart,
    bullet_chart,
    enhanced_time_series_chart,
    grouped_bar_chart,
    matrix_heatmap,
    pareto_chart,
    percent_stacked_bar_chart,
    ranking_bar_chart,
)
from src.components import (  # noqa: E402
    render_alerts,
    render_empty_state,
    render_executive_narrative,
    render_filter_badge,
    render_filter_context,
    render_header,
    render_health_score_breakdown_cards,
    render_insight,
    render_kpi_row,
    render_ranking,
    render_section_header,
    render_source_status,
    sidebar_section,
)
from src.config import (  # noqa: E402
    ABSENTEISMO_UNITS,
    COLORS,
    COMPARISON_MODES,
    DATA_SCHEMA_VERSION,
    DATA_STALE_AFTER_DAYS,
    DEFAULT_DAILY_ABSENCE_COST,
    FORECAST_MIN_POINTS,
    FORECAST_MONTHS,
    MAX_ALERTS,
    METRIC_COLORS,
    MOVING_AVERAGE_WINDOW,
    PAGE_NAMES,
    PALETTE,
    TABLE_HEIGHT,
    TARGETS,
    UNIT_COLORS,
    UNITS,
)
from src.data_loader import DataLoadError, get_data_file_signature, load_all_data  # noqa: E402
from src.data_sources import (  # noqa: E402
    DataSourceError,
    discard_unvalidated_snapshot,
    mark_source_valid,
    prepare_data_source,
    prepare_last_valid_source,
)
from src.filters import (  # noqa: E402
    build_filter_state,
    filter_appointments,
    filter_exam_volume,
    filter_reasons,
)
from src.executive_intelligence import (  # noqa: E402
    data_readiness_table,
    executive_comparison_table,
    executive_narrative_i18n,
    executive_recommendations,
    load_milestones,
    mental_latest,
    normalized_rate_table,
    periodic_coverage,
    severity_proxy,
)
from src.i18n import LANGUAGE_OPTIONS, page_label, tr  # noqa: E402
from src.population import add_rate_per_100, load_population  # noqa: E402
from src.responsive import apply_figure_safety  # noqa: E402
from src.runtime_diagnostics import runtime_payload  # noqa: E402
from src.semantic import source_coverage_notes  # noqa: E402
from src.styles import get_css  # noqa: E402
from src.transforms import (  # noqa: E402
    appointment_rows_for_totals,
    calc_variation,
    compare_overview_periods,
    compute_absenteismo_by_cause,
    compute_absenteismo_by_gender,
    compute_health_score_breakdown,
    compute_overview_kpis,
    filter_saude_mental_by_units,
    filter_unit_rows,
    get_available_months,
    get_next_month_labels,
    get_previous_month,
    normalize_selected_months,
)
from src.unit_targets import apply_unit_targets  # noqa: E402
from src.url_state import filter_query_values, read_filter_query  # noqa: E402
from src.validators import validate_loaded_data  # noqa: E402
from src.warehouse import WarehouseError, sync_to_warehouse  # noqa: E402

# ---------------------------------------------------------------------------
# Global presentation helpers
# ---------------------------------------------------------------------------
st.markdown(get_css(), unsafe_allow_html=True)

# TEMA GLOBAL + UX RESPONSIVA DO PAINEL LATERAL
# Mantém o conteúdo fluido, ocupa toda a largura disponível e preserva o
# controle nativo do Streamlit para recolher/reabrir a sidebar.
st.markdown("""
<style>
    :root {
        --sidebar-control-size: 42px;
        --sidebar-control-offset: 12px;
    }

    html,
    body,
    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"] {
        width: 100% !important;
        max-width: 100% !important;
        overflow-x: hidden !important;
        box-sizing: border-box !important;
    }

    .stApp {
        background: #130A2B !important;
    }

    /* A área principal sempre ocupa 100% da largura que estiver disponível.
       Quando a sidebar é recolhida, o próprio layout flex do Streamlit entrega
       toda a viewport ao conteúdo, sem manter largura máxima artificial. */
    [data-testid="stMain"] {
        flex: 1 1 auto !important;
        min-width: 0 !important;
        margin-left: 0 !important;
        transition: width 180ms ease, margin 180ms ease !important;
    }

    [data-testid="stMainBlockContainer"],
    .stMainBlockContainer,
    section.main > div.block-container {
        width: 100% !important;
        max-width: none !important;
        min-width: 0 !important;
        padding-left: clamp(0.75rem, 1.5vw, 1.5rem) !important;
        padding-right: clamp(0.75rem, 1.5vw, 1.5rem) !important;
        box-sizing: border-box !important;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #170E33 0%, #130A2B 100%) !important;
        border-right: 1px solid rgba(139,92,246,0.18) !important;
        transition: transform 180ms ease, width 180ms ease !important;
    }

    /* Mantém visíveis os controles nativos de fechar e reabrir a sidebar.
       Os seletores cobrem as estruturas usadas nas versões atuais do Streamlit
       e oferecem fallback para variações do DOM. */
    [data-testid="stSidebarCollapseButton"],
    [data-testid="collapsedControl"],
    button[data-testid="stSidebarCollapseButton"] {
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
        pointer-events: auto !important;
        z-index: 1000002 !important;
    }

    [data-testid="collapsedControl"] {
        position: fixed !important;
        top: var(--sidebar-control-offset) !important;
        left: var(--sidebar-control-offset) !important;
        width: var(--sidebar-control-size) !important;
        height: var(--sidebar-control-size) !important;
    }

    [data-testid="collapsedControl"] button,
    [data-testid="stSidebarCollapseButton"] button,
    button[data-testid="stSidebarCollapseButton"] {
        width: var(--sidebar-control-size) !important;
        min-width: var(--sidebar-control-size) !important;
        height: var(--sidebar-control-size) !important;
        min-height: var(--sidebar-control-size) !important;
        padding: 0 !important;
        border-radius: 12px !important;
        border: 1px solid rgba(139, 92, 246, 0.42) !important;
        background: rgba(20, 12, 45, 0.96) !important;
        color: #F8FAFC !important;
        box-shadow: 0 10px 28px rgba(0, 0, 0, 0.30) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        transition: transform 160ms ease, border-color 160ms ease,
                    background 160ms ease, box-shadow 160ms ease !important;
    }

    [data-testid="collapsedControl"] button:hover,
    [data-testid="stSidebarCollapseButton"] button:hover,
    button[data-testid="stSidebarCollapseButton"]:hover {
        transform: translateY(-1px) !important;
        border-color: rgba(196, 181, 253, 0.75) !important;
        background: rgba(39, 24, 78, 0.98) !important;
        box-shadow: 0 12px 32px rgba(76, 29, 149, 0.34) !important;
    }

    [data-testid="collapsedControl"] button:focus-visible,
    [data-testid="stSidebarCollapseButton"] button:focus-visible,
    button[data-testid="stSidebarCollapseButton"]:focus-visible {
        outline: 3px solid rgba(167, 139, 250, 0.42) !important;
        outline-offset: 2px !important;
    }

    /* Caso o tema global oculte o cabeçalho padrão, mantém somente o controle
       necessário à reabertura da sidebar e evita reexibir a barra de ferramentas. */
    header[data-testid="stHeader"] {
        display: block !important;
        visibility: visible !important;
        height: 0 !important;
        min-height: 0 !important;
        background: transparent !important;
        pointer-events: none !important;
        z-index: 1000001 !important;
    }

    header[data-testid="stHeader"] [data-testid="collapsedControl"] {
        pointer-events: auto !important;
    }

    header[data-testid="stHeader"] [data-testid="stToolbar"],
    header[data-testid="stHeader"] [data-testid="stDecoration"] {
        display: none !important;
    }

    /* Garante expansão total mesmo nas variações de estado/atributo do DOM. */
    section[data-testid="stSidebar"][aria-expanded="false"] ~ [data-testid="stMain"],
    section[data-testid="stSidebar"][data-state="collapsed"] ~ [data-testid="stMain"],
    section[data-testid="stSidebar"][data-collapsed="true"] ~ [data-testid="stMain"] {
        width: 100vw !important;
        max-width: 100vw !important;
        margin-left: 0 !important;
    }

    /* Dashboard headers e cards */
    div[data-testid="stVerticalBlock"] > div { }

    @media (max-width: 768px) {
        :root {
            --sidebar-control-size: 40px;
            --sidebar-control-offset: 8px;
        }

        [data-testid="stMainBlockContainer"],
        .stMainBlockContainer,
        section.main > div.block-container {
            padding-left: 0.65rem !important;
            padding-right: 0.65rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

user_context = enforce_authentication()

if not st.session_state.get("_runtime_environment_logged", False):
    log_event("runtime_environment", runtime_payload())
    st.session_state["_runtime_environment_logged"] = True

_CHART_CFG = {
    "displayModeBar": False,
    "responsive": True,
    "scrollZoom": False,
    "displaylogo": False,
    "editable": False,
    "staticPlot": False,
    "doubleClick": False,
    "showTips": False,
}


def show_chart(fig, **kwargs: Any) -> None:
    """Render every Plotly figure through one responsive, hover-safe gateway."""
    if fig is None:
        return
    apply_figure_safety(fig)
    kwargs.setdefault("width", "stretch")
    st.plotly_chart(fig, config=_CHART_CFG, **kwargs)


def format_operational_unit(unit: object) -> str:
    """Keep the internal value ``SF`` while blocking browser expansion."""
    value = str(unit).strip()
    return "S\u200bF" if value.upper() == "SF" else value


def normalized_percent(value: object) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0.0
    return number * 100 if 0 <= number <= 1 else number


def _variation_style(value: object, semantics: str = "neutral") -> str:
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return ""
    if numeric == 0 or semantics == "neutral":
        return "color: #94A3B8"
    favourable = numeric > 0 if semantics == "higher" else numeric < 0
    return (
        "color: #34D399; font-weight: 700"
        if favourable
        else "color: #FCA5A5; font-weight: 700"
    )


def _variation_series(current: pd.Series, previous: pd.Series | None) -> pd.Series:
    """Vectorized percentage variation with safe zero handling."""
    current_values = pd.to_numeric(current, errors="coerce").fillna(0.0).astype(float)
    if previous is None:
        return pd.Series(0.0, index=current_values.index)
    previous_values = pd.to_numeric(previous, errors="coerce").fillna(0.0).astype(float)
    result = pd.Series(0.0, index=current_values.index, dtype=float)
    valid = previous_values.ne(0.0)
    result.loc[valid] = (
        (current_values.loc[valid] - previous_values.loc[valid])
        / previous_values.loc[valid].abs()
        * 100.0
    )
    return result.round(1)

def _month_series(frame: pd.DataFrame, month_name: str | None) -> pd.Series:
    """Return a numeric month series or a zero-filled fallback when the column is absent."""
    if not month_name or month_name not in frame.columns:
        return pd.Series(0.0, index=frame.index, dtype=float)
    return pd.to_numeric(frame[month_name], errors="coerce").fillna(0.0).astype(float)



def display_matrix(
    frame: pd.DataFrame,
    *,
    percent_columns: list[str] | None = None,
    integer_columns: list[str] | None = None,
    decimal_columns: list[str] | None = None,
    variation_columns: list[str] | None = None,
    bar_columns: list[str] | None = None,
    variation_semantics: str = "neutral",
) -> None:
    """Display a compact analytical matrix with explicit formatting."""
    if frame.empty:
        st.info("Não há dados no escopo selecionado.")
        return
    percent_columns = [column for column in (percent_columns or []) if column in frame.columns]
    integer_columns = [column for column in (integer_columns or []) if column in frame.columns]
    decimal_columns = [column for column in (decimal_columns or []) if column in frame.columns]
    variation_columns = [column for column in (variation_columns or []) if column in frame.columns]
    bar_columns = [column for column in (bar_columns or []) if column in frame.columns]

    formats: dict[str, str] = {column: "{:.1f}%" for column in percent_columns}
    formats.update({column: "{:,.0f}" for column in integer_columns})
    formats.update({column: "{:,.1f}" for column in decimal_columns})
    safe_frame = frame.copy()
    styler = safe_frame.style.format(formats, na_rep="—")
    for column in variation_columns:
        styler = styler.map(lambda value: _variation_style(value, variation_semantics), subset=[column])
    for column in bar_columns:
        styler = styler.bar(subset=[column], color="rgba(139, 92, 246, 0.35)")

    # Render as deterministic HTML instead of sending a pandas Styler through
    # PyArrow on every filter rerun. This preserves the Power BI-like styling
    # while removing a native serialization path from the hottest UI flow.
    fingerprint_source = safe_frame.to_csv(index=False, na_rep="—")
    styler = styler.set_uuid(sha1(fingerprint_source.encode("utf-8")).hexdigest()[:12])
    styler = styler.set_table_styles(
        [
            {"selector": "table", "props": [("width", "100%"), ("border-collapse", "separate"), ("border-spacing", "0")]},
            {"selector": "thead th", "props": [("background", "#1E1240"), ("color", "#C4B5FD"), ("font-weight", "700"), ("padding", "10px 12px"), ("border-bottom", "1px solid rgba(139,92,246,.20)")]},
            {"selector": "tbody td", "props": [("padding", "9px 12px"), ("color", "#E9D5FF"), ("border-bottom", "1px solid rgba(139,92,246,.10)")]},
            {"selector": "tbody tr:nth-child(even)", "props": [("background", "rgba(30,18,64,.42)")]},
            {"selector": "tbody tr:hover", "props": [("background", "rgba(139,92,246,.10)")]},
        ],
        overwrite=False,
    )
    estimated_height = 64 + 44 * (len(safe_frame) + 1)
    table_height = estimated_height if len(safe_frame) <= 10 else min(TABLE_HEIGHT, estimated_height)
    st.markdown(
        f'<div class="safe-html-table" style="max-height:{table_height}px">{styler.to_html()}</div>',
        unsafe_allow_html=True,
    )


def metric_series(frame: pd.DataFrame, metric: str, max_points: int = 8) -> list[float]:
    """Return the last N historical values for a metric to be used in sparklines.

    Tries flexible column name matching (case-insensitive, partial match).
    Always returns clean float list, limited to max_points for compact sparklines.
    """
    if frame is None or frame.empty:
        return []

    # Flexible column matching
    cols_lower = {str(c).lower(): c for c in frame.columns}
    metric_lower = metric.lower()

    col = None
    if metric in frame.columns:
        col = metric
    elif metric_lower in cols_lower:
        col = cols_lower[metric_lower]
    else:
        # Partial match
        for lower_name, original in cols_lower.items():
            if metric_lower in lower_name or lower_name in metric_lower:
                col = original
                break

    if col is None:
        return []

    try:
        series = frame[col].astype(float).dropna().tolist()
        if len(series) > max_points:
            series = series[-max_points:]  # last N points for compact sparkline
        return [round(v, 2) if isinstance(v, float) else float(v) for v in series]
    except Exception:
        return []


def time_series_figure(
    frame: pd.DataFrame,
    metric: str,
    title: str,
    *,
    target: float | None = None,
    target_label: str = "Limite configurado",
    projections: bool = True,
    suffix: str = "",
) -> None:
    values = metric_series(frame, metric)
    future_labels = (
        get_next_month_labels(str(frame["Mês"].iloc[-1]), FORECAST_MONTHS)
        if not frame.empty and FORECAST_MONTHS > 0
        else []
    )
    forecast = (
        linear_forecast_with_interval(values, frame["Mês"].astype(str).tolist(), future_labels)
        if projections and len(values) >= FORECAST_MIN_POINTS
        else None
    )
    connected_labels = ([str(frame["Mês"].iloc[-1])] + forecast.labels) if forecast else None
    connected_values = ([values[-1]] + forecast.forecast) if forecast else None
    connected_lower = ([values[-1]] + forecast.lower) if forecast else None
    connected_upper = ([values[-1]] + forecast.upper) if forecast else None
    fig = enhanced_time_series_chart(
        frame,
        x="Mês",
        y=metric,
        title=title,
        color=METRIC_COLORS.get(metric, COLORS["blue"]),
        moving_average=MOVING_AVERAGE_WINDOW,
        target=target,
        target_label=target_label,
        forecast_labels=connected_labels,
        forecast_values=connected_values,
        forecast_lower=connected_lower,
        forecast_upper=connected_upper,
        milestones=load_milestones(selected_months=frame["Mês"].astype(str).tolist()),
        value_suffix=suffix,
    )
    show_chart(fig)
    if forecast:
        st.caption(
            f"Projeção linear indicativa para os próximos {len(forecast.labels)} meses; confiabilidade {forecast.confidence}. "
            "A faixa sombreada representa um intervalo aproximado de 95%."
        )


# ---------------------------------------------------------------------------
# Load and validate the real workbook
# ---------------------------------------------------------------------------
source_warning = ""
primary_source_error = ""

try:
    prepared_source = prepare_data_source()
    file_signature = get_data_file_signature(prepared_source.path)
    data = load_all_data(
        file_signature,
        DATA_SCHEMA_VERSION,
        str(prepared_source.path),
    )
    promotion_key = f"_source_promoted_{prepared_source.checksum[:20]}"
    if st.session_state.get(promotion_key, False):
        contingency_saved = True
    else:
        contingency_saved = mark_source_valid(prepared_source)
        if contingency_saved:
            st.session_state[promotion_key] = True
    if not contingency_saved:
        source_warning = (
            "A fonte atual foi carregada normalmente, mas não foi possível atualizar "
            "a cópia local de contingência nesta execução."
        )
except (DataSourceError, DataLoadError) as exc:
    if isinstance(exc, DataLoadError) and "prepared_source" in locals():
        discard_unvalidated_snapshot(prepared_source)
    primary_source_error = str(exc)
    fallback_source = prepare_last_valid_source()
    if fallback_source is None:
        st.error("Não foi possível carregar a fonte de dados do dashboard.")
        st.code(primary_source_error, language=None)
        st.caption(
            "Confira a sincronização do OneDrive, o caminho DATA_LOCAL_PATH e "
            "a opção 'Sempre manter neste dispositivo'."
        )
        st.stop()

    try:
        prepared_source = fallback_source
        file_signature = get_data_file_signature(prepared_source.path)
        data = load_all_data(
            file_signature,
            DATA_SCHEMA_VERSION,
            str(prepared_source.path),
        )
        source_warning = (
            "A planilha sincronizada não pôde ser utilizada agora. "
            "O painel está exibindo a última versão que foi carregada e "
            "validada com sucesso. Detalhe técnico: "
            + primary_source_error
        )
    except DataLoadError as fallback_error:
        st.error("A fonte atual e a cópia de contingência não puderam ser carregadas.")
        st.code(
            f"Fonte atual: {primary_source_error}\n"
            f"Contingência: {fallback_error}",
            language=None,
        )
        st.stop()

metadata = data.setdefault("metadata", {})
metadata.update(
    {
        "source_type": prepared_source.source_type,
        "source_checksum": prepared_source.checksum,
        "source_detail": prepared_source.detail,
        "source_display_name": prepared_source.display_name,
        "source_original_path": prepared_source.original_path,
        "source_size_bytes": prepared_source.size_bytes,
        "source_signature_original": prepared_source.source_signature,
        "source_checked_at": prepared_source.checked_at,
        "source_changed_at": prepared_source.changed_at or prepared_source.modified_at,
        "source_etag": prepared_source.etag,
        "fallback_used": prepared_source.fallback_used,
    }
)
if prepared_source.modified_at is not None:
    metadata["updated_at"] = prepared_source.modified_at

if st.session_state.pop("_source_change_detected_at", None):
    st.toast("Nova versão da planilha detectada, validada e carregada.", icon="🔄")

manual_sync_requested = st.session_state.pop("_manual_sync_requested_at", None)
if manual_sync_requested:
    if prepared_source.fallback_used:
        st.toast("A sincronização falhou; a contingência permaneceu ativa.", icon="🟠")
    else:
        st.toast("Sincronização manual concluída e planilha validada.", icon="✅")

# Optional SQL warehouse synchronization. It runs only once per source checksum
# in each Streamlit session.
warehouse_key = f"_warehouse_synced_{prepared_source.checksum[:16]}"
if not st.session_state.get(warehouse_key, False):
    try:
        written_tables = sync_to_warehouse(data)
        st.session_state[warehouse_key] = True
        if written_tables:
            log_event("warehouse_synced", {"tables": written_tables})
    except WarehouseError as exc:
        st.warning(f"Warehouse não sincronizado: {exc}")

validation_report = validate_loaded_data(data)
coverage_notes = source_coverage_notes(data)

exames = data["exames"]
afastamentos = data["afastamentos"]
atendimentos = data["atendimentos"]
absenteismo = data["absenteismo"]
saude_mental = data["saude_mental"]
top_postos = data["top_postos"]
source_updated_at = data.get("metadata", {}).get("updated_at")
audit_session_key = f"_audit_loaded_{prepared_source.checksum[:16]}_{user_context.email or user_context.name}"
if not st.session_state.get(audit_session_key, False):
    log_event(
        "dashboard_loaded",
        {
            "source_type": prepared_source.source_type,
            "source_checksum": prepared_source.checksum[:16],
            "user": user_context.email or user_context.name,
        },
    )
    st.session_state[audit_session_key] = True

month_cols = get_available_months(data)
all_units = [unit for unit in UNITS if unit in user_context.allowed_units]
available_exams_all = exames["volume"]["tipo_short"].astype(str).tolist()
available_atends_all = atendimentos["tipo"].astype(str).tolist()
available_reasons_all = afastamentos["por_motivo"]["indicador"].astype(str).tolist()

# ---------------------------------------------------------------------------
# Immediate Power BI-style filter state
# ---------------------------------------------------------------------------
FILTER_VERSION = "powerbi-v10-responsive-health"
FILTER_KEYS = {
    "months": "v8_months",
    "units": "v8_units",
    "exams": "v8_exams",
    "appointments": "v8_appointments",
    "reasons": "v8_reasons",
    "comparison": "v8_comparison",
}

if st.session_state.get("_v8_filter_version") != FILTER_VERSION:
    for key in list(st.session_state):
        if key.startswith(("v5_", "v6_", "v8_", "draft_", "selected_", "applied_filters", "operational_units_filter")):
            st.session_state.pop(key, None)
    query_defaults = read_filter_query(
        st.query_params,
        available_months=month_cols,
        available_units=all_units,
    )
    st.session_state[FILTER_KEYS["months"]] = query_defaults["months"] or month_cols.copy()
    st.session_state[FILTER_KEYS["units"]] = query_defaults["units"] or all_units.copy()
    st.session_state[FILTER_KEYS["exams"]] = available_exams_all.copy()
    st.session_state[FILTER_KEYS["appointments"]] = available_atends_all.copy()
    st.session_state[FILTER_KEYS["reasons"]] = available_reasons_all.copy()
    st.session_state[FILTER_KEYS["comparison"]] = COMPARISON_MODES[0]
    st.session_state["_v8_filter_version"] = FILTER_VERSION

# Remove stale choices when the workbook changes.
# Preserve an intentionally empty month selection. Previously, the ``or``
# fallback restored every month immediately after the user removed the last
# chip, which made the X button appear not to work.
st.session_state[FILTER_KEYS["months"]] = normalize_selected_months(
    st.session_state.get(FILTER_KEYS["months"], month_cols.copy()),
    month_cols,
)
st.session_state[FILTER_KEYS["units"]] = [
    unit for unit in st.session_state.get(FILTER_KEYS["units"], all_units.copy()) if unit in all_units
]
st.session_state[FILTER_KEYS["exams"]] = [
    value for value in st.session_state.get(FILTER_KEYS["exams"], available_exams_all.copy()) if value in available_exams_all
]
st.session_state[FILTER_KEYS["appointments"]] = [
    value for value in st.session_state.get(FILTER_KEYS["appointments"], available_atends_all.copy()) if value in available_atends_all
]
st.session_state[FILTER_KEYS["reasons"]] = [
    value for value in st.session_state.get(FILTER_KEYS["reasons"], available_reasons_all.copy()) if value in available_reasons_all
]
if st.session_state.get(FILTER_KEYS["comparison"]) not in COMPARISON_MODES:
    st.session_state[FILTER_KEYS["comparison"]] = COMPARISON_MODES[0]


def _set_filter_values(state_key: str, values: Iterable[str]) -> None:
    """Set a slicer value through a stable Streamlit callback."""
    st.session_state[state_key] = list(values)


def _restore_all_filters() -> None:
    st.session_state[FILTER_KEYS["months"]] = month_cols.copy()
    st.session_state[FILTER_KEYS["units"]] = all_units.copy()
    st.session_state[FILTER_KEYS["exams"]] = available_exams_all.copy()
    st.session_state[FILTER_KEYS["appointments"]] = available_atends_all.copy()
    st.session_state[FILTER_KEYS["reasons"]] = available_reasons_all.copy()
    st.session_state[FILTER_KEYS["comparison"]] = COMPARISON_MODES[0]


def _clear_data_cache() -> None:
    """Force a fresh download, full validation and dashboard rerun."""
    st.session_state["_manual_sync_requested_at"] = datetime.now().isoformat()
    st.cache_data.clear()


def _render_all_clear_buttons(
    *,
    prefix: str,
    state_key: str,
    all_values: list[str],
    all_label: str = "Todos",
    clear_label: str = "Limpar",
) -> None:
    left, right = st.columns(2)
    with left:
        st.button(
            f"✓ {all_label}",
            key=f"{prefix}_all_v8",
            width="stretch",
            on_click=_set_filter_values,
            args=(state_key, all_values),
        )
    with right:
        st.button(
            f"✕ {clear_label}",
            key=f"{prefix}_clear_v8",
            width="stretch",
            on_click=_set_filter_values,
            args=(state_key, []),
        )


# ---------------------------------------------------------------------------
# Sidebar — os filtros são aplicados automaticamente, sem botão Aplicar.
# Controles rápidos preservados: Último mês, Últimos 3, Todos os meses e Limpar meses.
# Ação manual preservada: Sincronizar agora.
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <style>
        section[data-testid="stSidebar"] { 
            background: #0F172A !important; 
            border-right: 1px solid rgba(255,255,255,0.07); 
        }
        section[data-testid="stSidebar"] .block-container {
            padding-top: 1.2rem !important;
            padding-bottom: 1.5rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        section[data-testid="stSidebar"] div[role="radiogroup"] label {
            border-radius: 12px !important; 
            padding: 10px 14px !important; 
            margin-bottom: 6px !important;
            border: 1px solid transparent !important; 
            transition: all 0.2s ease !important; 
            font-size: 0.87rem !important;
            line-height: 1.4 !important;
        }
        section[data-testid="stSidebar"] div[role="radiogroup"] label:hover { 
            background: rgba(255,255,255,0.05) !important; 
            border-color: rgba(255,255,255,0.08) !important;
        }
        section[data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"] {
            background: rgba(37,99,235,0.18) !important; 
            border-color: rgba(37,99,235,0.3) !important; 
            font-weight: 600 !important;
            box-shadow: 0 2px 8px rgba(37,99,235,0.15) !important;
        }
        /* Botões com respiro */
        section[data-testid="stSidebar"] button { 
            border-radius: 10px !important; 
            font-size: 0.78rem !important; 
            height: 38px !important;
            font-weight: 500 !important;
            letter-spacing: 0.2px !important;
        }
        /* Expanders com espaçamento confortável */
        section[data-testid="stSidebar"] details {
            background: rgba(255,255,255,0.035) !important; 
            border: 1px solid rgba(255,255,255,0.07) !important;
            border-radius: 12px !important; 
            margin-bottom: 12px !important; 
            padding: 0 !important;
        }
        section[data-testid="stSidebar"] details summary {
            font-size: 0.82rem !important; 
            font-weight: 600 !important; 
            color: #CBD5E1 !important;
            padding: 12px 14px !important; 
            min-height: 44px !important;
            letter-spacing: 0.3px !important;
        }
        section[data-testid="stSidebar"] details div[data-testid="stExpanderDetails"] { 
            padding: 12px 14px 16px 14px !important; 
        }
        /* Selectbox idioma com respiro */
        section[data-testid="stSidebar"] div[data-testid="stSelectbox"] {
            margin-bottom: 4px !important;
        }
        .sidebar-logo { 
            text-align:center; 
            padding: 0.8rem 0 1.2rem 0 !important; 
            border-bottom: 1px solid rgba(255,255,255,0.07); 
            margin-bottom: 1.2rem !important; 
        }
        /* Filtros header spacing */
        .filter-header-spacer { height: 8px; }
    </style>
    <div class="sidebar-logo">
        <div style="font-size:1.8rem">🏥</div>
        <div style="font-size:0.85rem;font-weight:700;color:#F1F5F9;letter-spacing:0.5px;margin-top:4px">SM CGR 2026</div>
        <div style="font-size:0.65rem;color:#64748B;margin-top:2px;text-transform:uppercase;letter-spacing:1px">Serviço Médico</div>
    </div>
    """, unsafe_allow_html=True)

    _, col_lang, _ = st.columns([0.15, 0.7, 0.15])
    with col_lang:
        language_label = st.selectbox("Idioma / Language", options=list(LANGUAGE_OPTIONS.keys()), key="dashboard_language_v105", index=0, label_visibility="collapsed")
    language_code = LANGUAGE_OPTIONS[language_label]

    navigation_icons = {
        "Resumo Executivo": "◆",
        "Visão Geral": "▦",
        "Exames": "◉",
        "Atendimentos": "✚",
        "Afastamentos": "▤",
        "Saúde Mental": "◈",
    }

    page = st.radio(
        "Navegação principal",
        options=PAGE_NAMES,
        key="main_navigation_native_v8",
        format_func=lambda page_name: (
            f"{navigation_icons.get(page_name, '•')}  {page_label(page_name, language_code)}"
        ),
        label_visibility="collapsed",
    )

    st.markdown('<div style="height:16px"></div>', unsafe_allow_html=True)
    sidebar_section(f"🎛️ {tr('filters', language_code)}")
    st.caption(tr("filters_caption", language_code))
    st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)

    action_left, action_right = st.columns(2)
    with action_left:
        st.button(
            f"↺ {tr('restore_filters', language_code)}",
            key="restore_all_filters_v8",
            width="stretch",
            on_click=_restore_all_filters,
        )
    with action_right:
        st.button(
            f"⟳ {tr('sync_now', language_code)}",
            key="reload_data_v8",
            width="stretch",
            on_click=_clear_data_cache,
            help="Limpa o cache remoto, baixa novamente, valida o XLSX e atualiza o painel.",
        )

    with st.expander(f"📅 {tr('analysis_period', language_code)}", expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            st.button(tr("latest_month", language_code), key="months_latest_v8", width="stretch", on_click=_set_filter_values, args=(FILTER_KEYS["months"], month_cols[-1:] if month_cols else []))
            st.button(tr("last_6", language_code), key="months_last6_v8", width="stretch", on_click=_set_filter_values, args=(FILTER_KEYS["months"], month_cols[-6:]))
        with c2:
            st.button(tr("last_3", language_code), key="months_last3_v8", width="stretch", on_click=_set_filter_values, args=(FILTER_KEYS["months"], month_cols[-3:]))
            st.button(tr("year_to_date", language_code), key="months_ytd_v8", width="stretch", on_click=_set_filter_values, args=(FILTER_KEYS["months"], month_cols))
        _render_all_clear_buttons(prefix="months", state_key=FILTER_KEYS["months"], all_values=month_cols, all_label=tr("all_months", language_code), clear_label=tr("clear_months", language_code))

    with st.expander(f"🗓️ {tr('months_analysis', language_code)} • {len(st.session_state.get(FILTER_KEYS['months'], []))}", expanded=False):
        st.multiselect(tr("months_analysis", language_code), options=month_cols, key=FILTER_KEYS["months"], placeholder="Selecione", label_visibility="collapsed")

    unit_filter_pages = {"Resumo Executivo", "Visão Geral", "Afastamentos", "Saúde Mental"}
    if page in unit_filter_pages:
        with st.expander(f"🏢 {tr('operational_units', language_code)} • {len(st.session_state.get(FILTER_KEYS['units'], []))}", expanded=False):
            _render_all_clear_buttons(prefix="units", state_key=FILTER_KEYS["units"], all_values=all_units)
            st.multiselect(tr("operational_units", language_code), all_units, key=FILTER_KEYS["units"], format_func=format_operational_unit, label_visibility="collapsed", placeholder="Selecione")

    if page == "Exames":
        st.markdown("**Tipos de exame**")
        _render_all_clear_buttons(
            prefix="exams",
            state_key=FILTER_KEYS["exams"],
            all_values=available_exams_all,
        )
        st.multiselect(
            "Tipos de exame",
            available_exams_all,
            key=FILTER_KEYS["exams"],
            label_visibility="collapsed",
            placeholder="Selecione os tipos de exame",
        )
    elif page == "Atendimentos":
        st.markdown("**Tipos de atendimento**")
        _render_all_clear_buttons(
            prefix="appointments",
            state_key=FILTER_KEYS["appointments"],
            all_values=available_atends_all,
        )
        st.multiselect(
            "Tipos de atendimento",
            available_atends_all,
            key=FILTER_KEYS["appointments"],
            label_visibility="collapsed",
            placeholder="Selecione os tipos de atendimento",
        )
    elif page == "Afastamentos":
        st.markdown("**Motivos de afastamento**")
        _render_all_clear_buttons(
            prefix="reasons",
            state_key=FILTER_KEYS["reasons"],
            all_values=available_reasons_all,
        )
        st.multiselect(
            "Motivos de afastamento",
            available_reasons_all,
            key=FILTER_KEYS["reasons"],
            label_visibility="collapsed",
            placeholder="Selecione os motivos",
        )

    # REMOVIDO: Comparação e Modo apresentação (clean)
    if FILTER_KEYS["comparison"] not in st.session_state:
        st.session_state[FILTER_KEYS["comparison"]] = COMPARISON_MODES[0] if COMPARISON_MODES else "Mês anterior"
    presentation_mode = False

    filters = build_filter_state(
        months=st.session_state[FILTER_KEYS["months"]],
        available_months=month_cols,
        units=st.session_state[FILTER_KEYS["units"]],
        exams=st.session_state[FILTER_KEYS["exams"]],
        appointments=st.session_state[FILTER_KEYS["appointments"]],
        reasons=st.session_state[FILTER_KEYS["reasons"]],
        available_exams=available_exams_all,
        available_appointments=available_atends_all,
        available_reasons=available_reasons_all,
        comparison_mode=st.session_state[FILTER_KEYS["comparison"]],
    )

    selected_months = list(filters.months)
    selected_units = list(filters.units)
    selected_exams = list(filters.exams)
    selected_atends = list(filters.appointments)
    selected_reasons = list(filters.reasons)

    # Keep a shareable link with the current period and units.
    query_values = filter_query_values(selected_months, selected_units)
    for query_key, query_value in query_values.items():
        if query_value:
            st.query_params[query_key] = query_value
        elif query_key in st.query_params:
            del st.query_params[query_key]

    filter_fingerprint = (
        page,
        tuple(selected_months),
        tuple(selected_units),
        tuple(selected_exams),
        tuple(selected_atends),
        tuple(selected_reasons),
        filters.comparison_mode,
    )
    if st.session_state.get("_last_filter_fingerprint_v8") != filter_fingerprint:
        log_event(
            "filters_changed",
            {
                "page": page,
                "months": selected_months,
                "units": selected_units,
                "comparison": filters.comparison_mode,
                "user": user_context.email or user_context.name,
            },
        )
        st.session_state["_last_filter_fingerprint_v8"] = filter_fingerprint

    # REMOVIDO: ESCOPO ATUAL (Meses: 6/6 e Unidades: 5/5) - poluindo

    # The sidebar action area intentionally remains compact. Diagnostic, source
    # coverage and metric-dictionary expanders were removed from rendering;
    # source integrity continues to be available in the AutoSync status card.

    if selected_months and selected_units:
        if st.button(f"📄 {tr('prepare_report', language_code)}", key="prepare_pdf_v8", width="stretch"):
            with st.spinner("Gerando PDF executivo..."):
                # ReportLab is imported only when a report is requested. It is
                # not part of the normal filter/rerun path on Community Cloud.
                from src.reporting import build_executive_pdf

                st.session_state["_executive_pdf_v8"] = build_executive_pdf(
                    data,
                    selected_months,
                    selected_units,
                    generated_by=user_context.email or user_context.name,
                    language=language_code,
                    source_status=tr("contingency_active", language_code) if data.get("metadata", {}).get("fallback_used") else tr("source_synced", language_code),
                    quality_score=validation_report.score,
                )
                log_event(
                    "executive_pdf_generated",
                    {"months": selected_months, "units": selected_units, "user": user_context.email},
                )
        if st.session_state.get("_executive_pdf_v8"):
            st.download_button(
                f"⬇ {tr('download_report', language_code)}",
                data=st.session_state["_executive_pdf_v8"],
                file_name=f"executive_report_sm_cgr_2026_{language_code}.pdf",
                mime="application/pdf",
                key="download_pdf_v8",
                width="stretch",
            )

    # REMOVIDO: AutoSync ativo card - poluindo
    # render_local_source_monitor(prepared_source)
    render_user_sidebar(user_context)

# Empty slicers are valid states. Keep the sidebar available and avoid
# calculations that require at least one item in the active scope.
if not selected_months:
    render_header([], source_updated_at, language=language_code)
    render_empty_state(
        "Nenhum mês selecionado",
        "Selecione um ou mais meses para carregar os KPIs, gráficos e tabelas.",
        icon="📅",
        hint="Use Último mês, Últimos 3 ou Todos os meses no painel lateral.",
    )
    st.stop()

if page in unit_filter_pages and not selected_units:
    render_header(selected_months, source_updated_at, language=language_code)
    render_empty_state(
        "Nenhuma unidade selecionada",
        "O escopo atual não contém unidades operacionais.",
        icon="🏭",
        hint="Selecione uma unidade ou use Todos no filtro lateral.",
    )
    st.stop()

if page == "Exames" and not selected_exams:
    render_header(selected_months, source_updated_at, language=language_code)
    render_empty_state(
        "Nenhum tipo de exame selecionado",
        "Selecione ao menos um tipo de exame para montar a análise.",
        icon="🔬",
    )
    st.stop()

if page == "Atendimentos" and not selected_atends:
    render_header(selected_months, source_updated_at, language=language_code)
    render_empty_state(
        "Nenhum tipo de atendimento selecionado",
        "Selecione ao menos um tipo de atendimento para montar a análise.",
        icon="🩺",
    )
    st.stop()

last_m = selected_months[-1]
prev_m = get_previous_month(last_m, month_cols)
trend_lbl = f"vs. {prev_m}" if prev_m else ""
monthly_metrics = executive_metric_series(data, selected_months, selected_units)


def common_page_header() -> None:
    render_header(selected_months, source_updated_at, language=language_code)
    if isinstance(source_updated_at, datetime):
        now = datetime.now(source_updated_at.tzinfo) if source_updated_at.tzinfo else datetime.now()
        updated_age_days = max(0, (now - source_updated_at).days)
    else:
        updated_age_days = 0
    metadata = data.get("metadata", {})
    # REMOVIDO - Fonte sincronizada bar
    # render_source_status(...)
    if source_warning:
        st.warning(source_warning)
    # REMOVIDO - Página/Meses/Unidades bar
    # render_filter_context(...)


# ---------------------------------------------------------------------------
# RESUMO EXECUTIVO / BOARD SUMMARY
# ---------------------------------------------------------------------------
if page == "Resumo Executivo":
    common_page_header()
    # REMOVIDO - Leitura executiva do período bar
    # render_executive_narrative(...)

    board_kpis = compute_overview_kpis(data, selected_months, selected_units)
    mental_current, mental_previous = mental_latest(monthly_metrics)
    periodic_current, periodic_previous = periodic_coverage(data, selected_months)
    severity_current, severity_previous = severity_proxy(board_kpis)

    tooltip_text = {
        "pt": {
            "exams": "Total de exames realizados no mês mais recente do escopo.",
            "appointments": "Total de atendimentos contabilizados no mês mais recente.",
            "leaves": "Quantidade de afastamentos ativos registrada no mês mais recente.",
            "days": "Soma dos dias perdidos no mês mais recente. Quanto menor, melhor.",
            "mental": "Quantidade agregada de triagens SRQ-20 alteradas no mês mais recente.",
            "coverage": "Percentual acumulado de cobertura dos exames periódicos.",
            "severity": "Indicador gerencial: dias perdidos divididos pelos afastamentos ativos. Não representa duração clínica individual.",
        },
        "en": {
            "exams": "Exams performed in the latest month of the selected scope.",
            "appointments": "Appointments recorded in the latest month.",
            "leaves": "Active leaves recorded in the latest month.",
            "days": "Lost days recorded in the latest month. Lower is better.",
            "mental": "Aggregated positive SRQ-20 screenings in the latest month.",
            "coverage": "Cumulative periodic-exam coverage percentage.",
            "severity": "Management proxy: lost days divided by active leaves. It is not an individual clinical duration measure.",
        },
        "fr": {
            "exams": "Examens réalisés au cours du dernier mois du périmètre.",
            "appointments": "Consultations enregistrées au cours du dernier mois.",
            "leaves": "Arrêts actifs enregistrés au cours du dernier mois.",
            "days": "Jours perdus au cours du dernier mois. Plus bas est préférable.",
            "mental": "Dépistages SRQ-20 positifs agrégés au cours du dernier mois.",
            "coverage": "Pourcentage cumulé de couverture des examens périodiques.",
            "severity": "Indicateur de gestion : jours perdus divisés par arrêts actifs. Il ne s’agit pas d’une durée clinique individuelle.",
        },
    }[language_code]

    render_section_header("◆", tr("executive_snapshot", language_code))
    render_kpi_row([
        {
            "icon": "🧪", "label": tr("exams", language_code),
            "value": f"{board_kpis['exames']['current']:,.0f}",
            "current": board_kpis["exames"]["current"], "previous": board_kpis["exames"]["previous"],
            "series": metric_series(monthly_metrics, "Exames"), "color": "blue",
            "context": selected_months[-1], "trend_label": f"vs. {prev_m}" if prev_m else "",
            "target_direction": "neutral", "tooltip": tooltip_text["exams"],
        },
        {
            "icon": "🩺", "label": tr("appointments", language_code),
            "value": f"{board_kpis['atendimentos']['current']:,.0f}",
            "current": board_kpis["atendimentos"]["current"], "previous": board_kpis["atendimentos"]["previous"],
            "series": metric_series(monthly_metrics, "Atendimentos"), "color": "green",
            "context": selected_months[-1], "trend_label": f"vs. {prev_m}" if prev_m else "",
            "target_direction": "neutral", "tooltip": tooltip_text["appointments"],
        },
        {
            "icon": "📋", "label": tr("active_leaves", language_code),
            "value": f"{board_kpis['afastamentos']['current']:,.0f}",
            "current": board_kpis["afastamentos"]["current"], "previous": board_kpis["afastamentos"]["previous"],
            "series": metric_series(monthly_metrics, "Afastamentos"), "color": "orange",
            "context": selected_months[-1], "trend_label": f"vs. {prev_m}" if prev_m else "",
            "target_direction": "lower", "tooltip": tooltip_text["leaves"],
        },
        {
            "icon": "📉", "label": tr("lost_days", language_code),
            "value": f"{board_kpis['absenteismo']['current']:,.0f}",
            "current": board_kpis["absenteismo"]["current"], "previous": board_kpis["absenteismo"]["previous"],
            "series": metric_series(monthly_metrics, "Dias Perdidos"), "color": "red",
            "context": selected_months[-1], "trend_label": f"vs. {prev_m}" if prev_m else "",
            "target": TARGETS["absenteismo_monthly_max"], "target_direction": "lower",
            "tooltip": tooltip_text["days"],
        },
    ], cols_count=4)

    render_kpi_row([
        {
            "icon": "🧠", "label": tr("srq_cases", language_code), "value": f"{mental_current:,.0f}",
            "current": mental_current, "previous": mental_previous, "series": metric_series(monthly_metrics, "SRQ-20"),
            "color": "purple", "target": TARGETS["mental_cases_max"], "target_direction": "lower",
            "trend_label": f"vs. {prev_m}" if prev_m else "", "tooltip": tooltip_text["mental"],
        },
        {
            "icon": "✅", "label": tr("periodic_coverage", language_code), "value": f"{periodic_current:.1f}%",
            "current": periodic_current, "previous": periodic_previous, "color": "cyan",
            "target": TARGETS["periodicos_pct"], "target_direction": "higher",
            "trend_label": f"vs. {prev_m}" if prev_m else "", "tooltip": tooltip_text["coverage"],
        },
        {
            "icon": "⚖️", "label": tr("absence_severity_proxy", language_code), "value": f"{severity_current:.1f}",
            "current": severity_current, "previous": severity_previous, "color": "orange",
            "target_direction": "lower", "trend_label": f"vs. {prev_m}" if prev_m else "",
            "context": tr("informational", language_code), "tooltip": tooltip_text["severity"],
        },
    ], cols_count=3)

    col_trend, col_impact = st.columns([3, 2], gap="large")
    with col_trend:
        render_section_header("📈", tr("main_trend", language_code))
        trend_title = {
            "pt": "Dias perdidos — evolução mensal",
            "en": "Lost days — monthly trend",
            "fr": "Jours perdus — évolution mensuelle",
        }[language_code]
        time_series_figure(
            monthly_metrics, "Dias Perdidos", trend_title,
            target=TARGETS["absenteismo_monthly_max"], target_label=tr("target", language_code), projections=True,
        )
    with col_impact:
        render_section_header("🏭", tr("largest_impact", language_code))
        board_ranking = unit_period_ranking(data, selected_months, selected_units, "Dias Perdidos")
        ranking_title = {
            "pt": "Dias perdidos por unidade",
            "en": "Lost days by unit",
            "fr": "Jours perdus par unité",
        }[language_code]
        show_chart(ranking_bar_chart(
            board_ranking, label_col="Unidade", value_col="Valor", share_col="Participação (%)",
            title=ranking_title, colors_by_label=UNIT_COLORS, height=390,
        ))

    render_section_header("📊", tr("management_comparison", language_code))
    comparison_table = executive_comparison_table(
        data, selected_months, selected_units, monthly_metrics, language=language_code
    )
    current_col = tr("current", language_code)
    previous_col = tr("previous", language_code)
    variation_col = tr("variation", language_code)
    display_matrix(
        comparison_table,
        decimal_columns=[current_col, previous_col],
        percent_columns=[variation_col],
        variation_columns=[variation_col],
        variation_semantics="neutral",
        bar_columns=[current_col],
    )

    render_section_header("🧭", tr("recommended_actions", language_code))
    for rec_icon, rec_title, rec_message in executive_recommendations(
        data, selected_months, selected_units, monthly_metrics, language=language_code
    ):
        render_insight(rec_icon, rec_title, rec_message, "warning" if rec_icon in {"🚨", "🧪", "🧠"} else "")

    rate_table = normalized_rate_table(data, selected_months, selected_units)
    if not rate_table.empty:
        render_section_header("👥", tr("normalized_rates", language_code))
        display_matrix(
            rate_table,
            integer_columns=["Populacao"],
            decimal_columns=["Afastamentos por 100", "Dias perdidos por 100"],
            bar_columns=["Dias perdidos por 100"],
        )

# ---------------------------------------------------------------------------
# VISÃO GERAL
# ---------------------------------------------------------------------------
elif page == "Visão Geral":
    common_page_header()
    render_executive_narrative(build_executive_narrative(data, selected_months, selected_units))

    if validation_report.score < 80 or validation_report.errors:
        st.warning(
            f"A base possui qualidade estimada em {validation_report.score:.0f}% e requer atenção. "
            "Os gráficos abaixo utilizam somente os valores reconhecidos e validados."
        )

    # Exibe somente os componentes individuais do índice.
    # O indicador geral em formato radial foi removido para evitar uma leitura
    # ambígua como se representasse a porcentagem de empregados saudáveis.
    breakdown = compute_health_score_breakdown(data, selected_months, selected_units)
    with st.container(key="health_score_components_section"):
        render_health_score_breakdown_cards(breakdown)

    kpis = compute_overview_kpis(data, selected_months, selected_units)
    latest_mental = metric_series(monthly_metrics, "SRQ-20")
    render_kpi_row(
        [
            {
                "icon": "🔬", "label": "Exames", "value": f"{kpis['exames']['total']:,.0f}",
                "current": kpis["exames"]["current"], "previous": kpis["exames"]["previous"],
                "color": "blue", "series": metric_series(monthly_metrics, "Exames"),
                "context": f"Média de {kpis['exames']['total']/max(len(selected_months),1):,.0f} por mês", "trend_label": trend_lbl,
                "target_direction": "neutral",
            },
            {
                "icon": "🩺", "label": "Atendimentos", "value": f"{kpis['atendimentos']['total']:,.0f}",
                "current": kpis["atendimentos"]["current"], "previous": kpis["atendimentos"]["previous"],
                "color": "green", "series": metric_series(monthly_metrics, "Atendimentos"),
                "context": f"Média de {kpis['atendimentos']['total']/max(len(selected_months),1):,.0f} por mês", "trend_label": trend_lbl,
                "target_direction": "neutral",
            },
            {
                "icon": "🚑", "label": "Afastamentos ativos", "value": f"{kpis['afastamentos']['current']:,.0f}",
                "current": kpis["afastamentos"]["current"], "previous": kpis["afastamentos"]["previous"],
                "color": "orange", "series": metric_series(monthly_metrics, "Afastamentos"),
                "context": f"Casos em {last_m}", "trend_label": trend_lbl, "target_direction": "lower",
            },
            {
                "icon": "📋", "label": "Dias perdidos", "value": f"{kpis['absenteismo']['total']:,.0f}",
                "current": kpis["absenteismo"]["current"], "previous": kpis["absenteismo"]["previous"],
                "color": "red", "series": metric_series(monthly_metrics, "Dias Perdidos"),
                "context": f"{kpis['absenteismo']['current']:,.0f} no último mês", "trend_label": trend_lbl,
                "target": TARGETS["absenteismo_monthly_max"], "target_direction": "lower",
            },
            {
                "icon": "🧠", "label": "SRQ-20 alterados", "value": f"{latest_mental[-1] if latest_mental else 0:,.0f}",
                "current": latest_mental[-1] if latest_mental else 0, "previous": latest_mental[-2] if len(latest_mental)>1 else 0,
                "color": "purple", "series": latest_mental, "context": f"Casos em {last_m}", "trend_label": trend_lbl,
                "target": TARGETS["mental_cases_max"], "target_direction": "lower",
            },
        ],
        cols_count=5,
    )

    if filters.comparison_mode != "Sem comparação":
        render_section_header("📊", f"Comparação — {filters.comparison_mode}")
        comparison = compare_overview_periods(data, selected_months, selected_units, filters.comparison_mode)
        if comparison["Meses comparados"].eq("Sem comparação").all():
            st.info(
                "Não há histórico anterior suficiente para o modo de comparação selecionado. "
                "Escolha outro período ou use Sem comparação."
            )
        else:
            display_matrix(
                comparison,
                integer_columns=["Período atual", "Período comparado"],
                percent_columns=["Variação (%)"],
                variation_columns=["Variação (%)"],
                bar_columns=["Período atual"],
                variation_semantics="neutral",
            )

    active_alerts = generate_alerts(data, selected_months, selected_units)
    render_section_header("🚨", "Alertas automáticos e limites de gestão")
    if active_alerts:
        render_alerts(active_alerts, max_items=MAX_ALERTS)
    else:
        render_insight(
            "✅",
            "Nenhum alerta crítico no escopo",
            "Os indicadores selecionados não ultrapassaram os limites configurados.",
            "success",
        )

    col_trend, col_rank = st.columns([3, 2])
    with col_trend:
        render_section_header("📈", "Tendência principal")
        overview_metric = st.radio(
            "Indicador da tendência",
            ["Exames", "Atendimentos", "Afastamentos", "Dias Perdidos", "SRQ-20"],
            horizontal=True,
            key="v8_overview_metric",
        )
        target = TARGETS["absenteismo_monthly_max"] if overview_metric == "Dias Perdidos" else TARGETS["mental_cases_max"] if overview_metric == "SRQ-20" else None
        time_series_figure(
            monthly_metrics,
            overview_metric,
            dynamic_title(overview_metric, months=selected_months, units=selected_units),
            target=target,
            projections=True,
        )
        anomalies = detect_anomalies(
            metric_series(monthly_metrics, overview_metric),
            monthly_metrics["Mês"].astype(str).tolist(),
            z_threshold=2.0,
        )
        if (not st.session_state.get("presentation_mode_v8", False) and not anomalies.empty
                and anomalies.get("Z-score", pd.Series(dtype=float)).abs().ge(2.0).any()):
            with st.expander("⚠️ Variação atípica detectada"):
                display_matrix(anomalies, integer_columns=["Valor"], variation_columns=[])
    with col_rank:
        render_section_header("🏭", "Onde está o maior impacto")
        rank_metric = st.radio("Ranking por", ["Afastamentos", "Dias Perdidos", "SRQ-20"], horizontal=True, key="v8_rank_metric")
        ranking = unit_latest_ranking(data, selected_months, selected_units, rank_metric)
        show_chart(ranking_bar_chart(
            ranking,
            label_col="Unidade", value_col="Valor", previous_col="Anterior", share_col="Participação (%)",
            title=dynamic_title(f"{rank_metric} por unidade — {last_m}", months=[last_m], units=selected_units),
            colors_by_label=UNIT_COLORS,
        ))

    col_bridge, col_pareto = st.columns(2)
    with col_bridge:
        render_section_header("🧩", "Contribuição para a variação")
        bridge_metric = st.radio("Explicar mudança de", ["Afastamentos", "Dias Perdidos", "SRQ-20"], horizontal=True, key="v8_bridge_metric")
        previous_total, contributions, current_total = unit_change_contribution(data, selected_months, selected_units, bridge_metric)
        show_chart(bridge_waterfall_chart(
            previous_total,
            contributions,
            current_total,
            title=dynamic_title(f"Quem fez {bridge_metric.lower()} mudar", months=[last_m], units=selected_units),
        ))
    with col_pareto:
        render_section_header("🎯", "Pareto dos motivos")
        reason_table = reason_pareto_table(data, selected_months)
        show_chart(pareto_chart(
            reason_table["Motivo"].tolist(),
            reason_table["Valor"].astype(int).tolist(),
            title=dynamic_title("Motivos de afastamento", months=selected_months, units=selected_units, include_units=False),
            height=370,
        ))
        st.caption(coverage_notes["Afastamentos"])

    render_section_header("🌡️", "Mapa de intensidade — dias perdidos")
    abs_matrix_rows = []
    for unit in ABSENTEISMO_UNITS:
        if unit not in selected_units:
            continue
        unit_data = absenteismo[unit]["data"]
        total = unit_data[unit_data["indicador"].astype(str).str.casefold().eq("total")]
        if not total.empty:
            abs_matrix_rows.append({"Unidade": unit, **{month: int(total[month].sum()) for month in selected_months}})
    abs_matrix = pd.DataFrame(abs_matrix_rows)
    show_chart(matrix_heatmap(
        abs_matrix,
        row_col="Unidade",
        month_cols=selected_months,
        title=dynamic_title("Dias perdidos por unidade e mês", months=selected_months, units=selected_units),
        height=310,
    ))

    render_section_header("📋", "Matriz executiva")
    summary = metric_summary_matrix(data, selected_months, selected_units)
    display_matrix(
        summary,
        integer_columns=["Total do período", "Último mês", "Mês anterior", "Média mensal", "Pico"],
        percent_columns=["Variação (%)"],
        variation_columns=["Variação (%)"],
        variation_semantics="neutral",
    )

# ---------------------------------------------------------------------------
# EXAMES
# ---------------------------------------------------------------------------
elif page == "Exames":
    common_page_header()
    render_section_header("🔬", "Gestão de exames ocupacionais")
    st.caption(coverage_notes.get("Exames", "Visão consolidada dos exames ocupacionais."))

    exam_vol = filter_exam_volume(exames["volume"], filters)
    months = selected_months
    total_by_month = [float(exam_vol[month].sum()) for month in months] if not exam_vol.empty else [0.0] * len(months)
    total_period = sum(total_by_month)
    current = total_by_month[-1] if total_by_month else 0.0
    previous = total_by_month[-2] if len(total_by_month) > 1 else 0.0

    periodic = exam_vol[exam_vol["tipo_short"] == "Periódicos"] if not exam_vol.empty else pd.DataFrame()
    periodic_series = [float(periodic[month].sum()) for month in months] if not periodic.empty else [0.0] * len(months)
    periodic_total = sum(periodic_series)

    pct = exames.get("percentuais", {})
    pct_months = pct.get("meses", months)
    pct_index = pct_months.index(last_m) if last_m in pct_months else max(0, len(pct_months) - 1)
    periodicos_acum_list = pct.get("pct_periodicos_acum", [])
    faltas_list = pct.get("pct_faltas", [])

    periodic_pct = normalized_percent(periodicos_acum_list[pct_index]) if pct_index < len(periodicos_acum_list) else 0.0
    absence_pct = normalized_percent(faltas_list[pct_index]) if pct_index < len(faltas_list) else 0.0
    presence_pct = max(0.0, 100.0 - absence_pct)

    periodic_pct_series = [normalized_percent(v) for v in periodicos_acum_list[: len(pct_months)]]
    absence_pct_series = [normalized_percent(v) for v in faltas_list[: len(pct_months)]]
    presence_series = [max(0.0, 100.0 - v) for v in absence_pct_series]

    # Simple linear projection of coverage (no targets)
    proj_values = []
    if len(periodic_pct_series) >= 2:
        try:
            from src.transforms import compute_linear_projection
            proj_values = compute_linear_projection(periodic_pct_series, steps=3)
        except Exception:
            proj_values = []

    # --- KPI Row (no targets) ---
    render_kpi_row([
        {
            "icon": "🔬",
            "label": "Exames no período",
            "value": f"{total_period:,.0f}".replace(",", "."),
            "current": current,
            "previous": previous,
            "series": total_by_month,
            "color": "blue",
            "context": f"{len(exam_vol)} tipo(s) selecionado(s)",
            "trend_label": trend_lbl,
            "target_direction": "neutral",
        },
        {
            "icon": "🔄",
            "label": "Exames periódicos",
            "value": f"{periodic_total:,.0f}".replace(",", "."),
            "current": periodic_series[-1] if periodic_series else 0,
            "previous": periodic_series[-2] if len(periodic_series) > 1 else 0,
            "series": periodic_series,
            "color": "green",
            "context": f"{(periodic_total / total_period * 100) if total_period else 0:.1f}% do volume",
            "trend_label": trend_lbl,
            "target_direction": "higher",
        },
        {
            "icon": "📈",
            "label": "Cobertura acumulada",
            "value": f"{periodic_pct:.1f}%",
            "current": periodic_pct,
            "previous": periodic_pct_series[-2] if len(periodic_pct_series) > 1 else 0,
            "series": periodic_pct_series,
            "color": "purple",
            "context": f"Indicador em {last_m}",
            "trend_label": trend_lbl,
            "target_direction": "higher",
        },
        {
            "icon": "✅",
            "label": "Presença no Periódico",
            "value": f"{presence_pct:.1f}%",
            "current": presence_pct,
            "previous": presence_series[-2] if len(presence_series) > 1 else 0,
            "series": presence_series,
            "color": "green" if presence_pct >= 70 else "orange",
            "context": f"Inverso das faltas ({absence_pct:.1f}%)",
            "trend_label": trend_lbl,
            "target_direction": "higher",
        },
    ], cols_count=4)

    # --- Premium progress bar for coverage (no target/meta) ---
    try:
        from src.components import render_premium_progress_bar
        delta_cov = periodic_pct - (periodic_pct_series[-2] if len(periodic_pct_series) > 1 else periodic_pct)
        render_premium_progress_bar(
            label=f"Cobertura de Exames Periódicos — {last_m}",
            value=periodic_pct,
            max_value=100.0,
            color="#A78BFA",
            show_delta=delta_cov,
            height=26,
        )
    except Exception:
        pass

    # --- Narrative (no "crítico" / no "meta") ---
    # Diferença absoluta em pontos (ex: 16,6% → 40,9% = subiu 24,3 pontos)
    prev_cov = periodic_pct_series[-2] if len(periodic_pct_series) > 1 else periodic_pct
    cov_points = periodic_pct - prev_cov
    if cov_points > 0.05:
        cov_txt = f"subiu {cov_points:.1f} pontos".replace(".", ",")
    elif cov_points < -0.05:
        cov_txt = f"caiu {abs(cov_points):.1f} pontos".replace(".", ",")
    else:
        cov_txt = "ficou estável"

    if len(proj_values) >= 2:
        proj_text = f" No ritmo atual, a cobertura projetada em 3 meses fica em torno de {proj_values[-1]:.0f}%."
    else:
        proj_text = ""

    if absence_pct >= 30:
        narrative = (
            f"Cobertura acumulada em {str(round(periodic_pct,1)).replace('.',',')}% ({cov_txt}). "
            f"Faltas/não agendamento em {str(round(absence_pct,1)).replace('.',',')}% — principal ponto de atenção no momento."
            f"{proj_text}"
        )
        n_icon, n_title, n_type = "⚠️", "Ponto de atenção: faltas elevadas", "warning"
    elif cov_points > 0.05:
        narrative = (
            f"Cobertura acumulada em {str(round(periodic_pct,1)).replace('.',',')}% ({cov_txt} no último mês). "
            f"Presença no periódico em {str(round(presence_pct,1)).replace('.',',')}%."
            f"{proj_text}"
        )
        n_icon, n_title, n_type = "📈", "Cobertura em evolução", "success"
    else:
        narrative = (
            f"Cobertura acumulada em {str(round(periodic_pct,1)).replace('.',',')}% ({cov_txt}). "
            f"Presença no periódico em {str(round(presence_pct,1)).replace('.',',')}%."
            f"{proj_text}"
        )
        n_icon, n_title, n_type = "➡️", "Situação atual", ""

    render_insight(n_icon, n_title, narrative, n_type)

    # --- Bullet charts without targets emphasis ---
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        show_chart(bullet_chart(
            periodic_pct, periodic_pct,
            f"Periódicos — {last_m}",
            max_value=100,
            height=190,
        ))
    with col_b2:
        show_chart(bullet_chart(
            absence_pct, absence_pct,
            f"Faltas — {last_m}",
            max_value=max(40, absence_pct * 1.3),
            lower_is_better=True,
            height=190,
        ))

    # --- Composition + Trend ---
    col_comp, col_trend = st.columns([3, 2])
    with col_comp:
        render_section_header("🧱", "Composição mensal por tipo")
        if not exam_vol.empty:
            composition = (
                exam_vol.set_index("tipo_short")[months]
                .astype(float)
                .T
                .to_dict("list")
            )
            show_chart(percent_stacked_bar_chart(
                composition,
                months,
                dynamic_title("Participação dos tipos de exame", months=months, units=selected_units, include_units=False),
                colors=PALETTE,
            ))
        else:
            st.info("Sem dados de exames para o filtro atual.")

    with col_trend:
        render_section_header("📈", "Tendência de cobertura")
        if periodic_pct_series:
            trend_df = pd.DataFrame({
                "Mês": pct_months[:len(periodic_pct_series)],
                "Cobertura %": periodic_pct_series,
            })
            mask = trend_df["Mês"].isin(months)
            if mask.any():
                trend_df = trend_df[mask]
            frame_cov = pd.DataFrame({"Mês": trend_df["Mês"], "Cobertura": trend_df["Cobertura %"]})
            time_series_figure(
                frame_cov,
                "Cobertura",
                dynamic_title("Cobertura acumulada de periódicos", months=months, include_units=False),
                projections=True,
            )

    # --- Volume by type ---
    render_section_header("📊", "Volume por tipo de exame")
    if not exam_vol.empty:
        type_totals = (
            exam_vol.assign(Total=exam_vol[months].sum(axis=1))
            [["tipo_short", "Total"]]
            .rename(columns={"tipo_short": "Tipo", "Total": "Valor"})
            .sort_values("Valor", ascending=False)
        )
        type_totals["Participação (%)"] = (type_totals["Valor"] / type_totals["Valor"].sum() * 100).round(1)
        type_totals["Anterior"] = 0
        show_chart(ranking_bar_chart(
            type_totals,
            label_col="Tipo",
            value_col="Valor",
            previous_col="Anterior",
            share_col="Participação (%)",
            title=dynamic_title("Volume acumulado por tipo", months=months, include_units=False),
        ))

    # --- Monthly detail table ---
    render_section_header("📋", "Detalhamento mensal")
    if not exam_vol.empty:
        detail = exam_vol[["tipo_short"] + months].copy()
        detail = detail.rename(columns={"tipo_short": "Tipo"})
        detail["Total"] = detail[months].sum(axis=1)
        display_matrix(
            detail,
            integer_columns=months + ["Total"],
            bar_columns=["Total"],
        )


# ---------------------------------------------------------------------------
# ATENDIMENTOS
# ---------------------------------------------------------------------------
elif page == "Atendimentos":
    common_page_header()
    render_section_header("🏥", "Atendimentos ambulatoriais")
    st.caption(coverage_notes["Atendimentos"])

    atend_data = filter_appointments(atendimentos, filters)
    total_rows = appointment_rows_for_totals(atend_data)
    months = selected_months
    total_series = [float(total_rows[month].sum()) for month in months]
    total_period = sum(total_series)

    medical = atend_data[atend_data["tipo"] == "Atendimento Médico"]
    medical_series = [float(medical[month].sum()) for month in months]
    physio_total = atend_data[atend_data["tipo"] == "Atendimento Fisioterapêutico Total"]
    if physio_total.empty:
        physio_total = atend_data[atend_data["tipo"].str.contains("Fisioterap", case=False, na=False)]
    physio_series = [float(physio_total[month].sum()) for month in months]
    peak_index = total_series.index(max(total_series)) if total_series else 0

    render_kpi_row([
        {
            "icon": "🩺", "label": "Total de atendimentos", "value": f"{total_period:,.0f}",
            "current": total_series[-1] if total_series else 0, "previous": total_series[-2] if len(total_series)>1 else 0,
            "series": total_series, "color": "blue", "context": "Sem dupla contagem da fisioterapia", "trend_label": trend_lbl,
            "target_direction": "neutral",
        },
        {
            "icon": "👨‍⚕️", "label": "Atendimento médico", "value": f"{sum(medical_series):,.0f}",
            "current": medical_series[-1] if medical_series else 0, "previous": medical_series[-2] if len(medical_series)>1 else 0,
            "series": medical_series, "color": "green", "context": f"{sum(medical_series)/total_period*100 if total_period else 0:.1f}% do total", "trend_label": trend_lbl,
            "target_direction": "neutral",
        },
        {
            "icon": "🦴", "label": "Fisioterapia", "value": f"{sum(physio_series):,.0f}",
            "current": physio_series[-1] if physio_series else 0, "previous": physio_series[-2] if len(physio_series)>1 else 0,
            "series": physio_series, "color": "cyan", "context": f"{sum(physio_series)/total_period*100 if total_period else 0:.1f}% do total", "trend_label": trend_lbl,
            "target_direction": "neutral",
        },
        {
            "icon": "📅", "label": "Pico mensal", "value": f"{max(total_series) if total_series else 0:,.0f}",
            "current": max(total_series) if total_series else 0, "previous": 0, "series": total_series,
            "color": "purple", "context": months[peak_index] if months else "—", "show_trend": False,
            "target_direction": "neutral",
        },
    ], cols_count=4)

    col_comp, col_trend = st.columns([3, 2])
    with col_comp:
        render_section_header("🧱", "Mudança da composição")
        composition_source = appointment_rows_for_totals(atend_data)
        composition = (
            composition_source.set_index("tipo")[months]
            .astype(float)
            .T
            .to_dict("list")
        )
        show_chart(percent_stacked_bar_chart(
            composition,
            months,
            dynamic_title("Participação por tipo de atendimento", months=months, units=selected_units, include_units=False),
            colors=PALETTE,
        ))
    with col_trend:
        render_section_header("📈", "Tendência selecionável")
        choices = ["Total"] + atend_data["tipo"].astype(str).tolist()
        selected_attendance = st.selectbox("Série analisada", choices, key="v8_attendance_trend")
        if selected_attendance == "Total":
            trend_values = total_series
        else:
            row = atend_data[atend_data["tipo"] == selected_attendance].iloc[0]
            trend_values = [float(row[month]) for month in months]
        trend_frame = pd.DataFrame({"Mês": months, selected_attendance: trend_values})
        time_series_figure(
            trend_frame,
            selected_attendance,
            dynamic_title(selected_attendance, months=months, units=selected_units, include_units=False),
            projections=True,
        )

    col_pareto, col_waterfall = st.columns(2)
    with col_pareto:
        render_section_header("🎯", "Pareto dos atendimentos")
        totals = appointment_rows_for_totals(atend_data).copy()
        totals["Valor"] = totals[months].sum(axis=1)
        show_chart(pareto_chart(
            totals["tipo"].tolist(), totals["Valor"].astype(int).tolist(),
            title=dynamic_title("Tipos de atendimento", months=months, units=selected_units, include_units=False),
        ))
    with col_waterfall:
        render_section_header("🌊", "Variação mensal")
        deltas = [total_series[0]] + [total_series[index] - total_series[index-1] for index in range(1, len(total_series))]
        from src.charts import waterfall_chart
        show_chart(waterfall_chart(months, [int(value) for value in deltas], dynamic_title("Fluxo do volume mensal", months=months, units=selected_units, include_units=False)))

    fisio_h = atend_data[atend_data["tipo"].str.contains("Horista", na=False)]
    fisio_m = atend_data[atend_data["tipo"].str.contains("Mensalista", na=False)]
    if not fisio_h.empty and not fisio_m.empty:
        render_section_header("🦴", "Fisioterapia — vínculo de trabalho")
        show_chart(grouped_bar_chart(
            {
                "Horista": [int(fisio_h[month].sum()) for month in months],
                "Mensalista": [int(fisio_m[month].sum()) for month in months],
            },
            months,
            dynamic_title("Horista versus mensalista", months=months, units=selected_units, include_units=False),
            colors=[COLORS["cyan"], COLORS["purple"]],
        ))

    render_section_header("📋", "Matriz de atendimentos")
    matrix = atend_data[["tipo"] + months].copy()
    matrix["Total"] = matrix[months].sum(axis=1)
    matrix["Participação (%)"] = matrix["Total"] / matrix["Total"].sum() * 100 if matrix["Total"].sum() else 0
    matrix["Variação (%)"] = _variation_series(
        matrix[last_m], matrix[prev_m] if prev_m and prev_m in matrix.columns else None
    )
    matrix = matrix.rename(columns={"tipo": "Tipo de atendimento"})
    display_matrix(matrix, integer_columns=months+["Total"], percent_columns=["Participação (%)", "Variação (%)"], variation_columns=["Variação (%)"], bar_columns=["Total"], variation_semantics="neutral")

# ---------------------------------------------------------------------------
# AFASTAMENTOS
# ---------------------------------------------------------------------------
elif page == "Afastamentos":
    common_page_header()
    render_section_header("📋", "Afastamentos e absenteísmo")
    tab_active, tab_abs, tab_prev = st.tabs(["📊 Afastamentos ativos", "📋 Dias perdidos", "⚖️ Previdenciário"])

    with tab_active:
        unit_rows = filter_unit_rows(afastamentos["por_unidade"], selected_units)
        reason_rows = filter_reasons(afastamentos["por_motivo"], filters)
        ranking = unit_latest_ranking(data, selected_months, selected_units, "Afastamentos")
        current_total = float(ranking["Valor"].sum()) if not ranking.empty else 0
        previous_total = float(ranking["Anterior"].sum()) if not ranking.empty else 0
        leader = ranking.iloc[0] if not ranking.empty else None
        monthly_active = [float(unit_rows[month].sum()) for month in selected_months]

        render_kpi_row([
            {
                "icon": "🚑", "label": "Afastamentos ativos", "value": f"{current_total:,.0f}",
                "current": current_total, "previous": previous_total, "series": monthly_active,
                "color": "orange", "context": f"Total em {last_m}", "trend_label": trend_lbl, "target_direction": "lower",
            },
            {
                "icon": "🏭", "label": "Unidade líder", "value": str(leader["Unidade"]) if leader is not None else "—",
                "current": float(leader["Valor"]) if leader is not None else 0, "previous": float(leader["Anterior"]) if leader is not None else 0,
                "series": [], "color": "blue", "context": f"{leader['Valor']:,.0f} casos | {leader['Participação (%)']:.1f}%" if leader is not None else "Sem dados",
                "show_trend": False, "target_direction": "neutral",
            },
            {
                "icon": "📈", "label": "Variação mensal", "value": f"{calc_variation(current_total, previous_total):+.1f}%",
                "current": current_total, "previous": previous_total, "series": monthly_active,
                "color": "red" if current_total > previous_total else "green", "context": f"{previous_total:,.0f} → {current_total:,.0f}",
                "show_trend": False, "target_direction": "lower",
            },
            {
                "icon": "📊", "label": "Média por unidade", "value": f"{current_total/max(len(ranking),1):,.1f}",
                "current": current_total/max(len(ranking),1), "previous": previous_total/max(len(ranking),1) if len(ranking) else 0,
                "series": [], "color": "purple", "context": f"{len(ranking)} unidade(s) no escopo", "trend_label": trend_lbl, "target_direction": "lower",
            },
        ], cols_count=4)

        col_evol, col_rank = st.columns([3, 2])
        with col_evol:
            render_section_header("📈", "Evolução por unidade")
            selected_unit_series = st.selectbox("Unidade analisada", ["Total"] + unit_rows["indicador"].astype(str).tolist(), key="v8_afast_unit")
            if selected_unit_series == "Total":
                values = monthly_active
            else:
                row = unit_rows[unit_rows["indicador"] == selected_unit_series].iloc[0]
                values = [float(row[month]) for month in selected_months]
            frame = pd.DataFrame({"Mês": selected_months, selected_unit_series: values})
            time_series_figure(
                frame,
                selected_unit_series,
                dynamic_title("Afastamentos ativos", months=selected_months, units=selected_units),
                projections=True,
            )
        with col_rank:
            render_section_header("🏆", "Ranking do último mês")
            show_chart(ranking_bar_chart(
                ranking,
                label_col="Unidade", value_col="Valor", previous_col="Anterior", share_col="Participação (%)",
                title=dynamic_title(f"Afastamentos — {last_m}", months=[last_m], units=selected_units),
                colors_by_label=UNIT_COLORS,
            ))

        col_bridge, col_pareto = st.columns(2)
        with col_bridge:
            render_section_header("🧩", "Contribuição por unidade")
            prev_total, contributions, cur_total = unit_change_contribution(data, selected_months, selected_units, "Afastamentos")
            show_chart(bridge_waterfall_chart(
                prev_total, contributions, cur_total,
                title=dynamic_title("Mudança dos afastamentos", months=[last_m], units=selected_units),
            ))
        with col_pareto:
            render_section_header("🎯", "Pareto de motivos")
            reason_table = reason_pareto_table(data, selected_months, selected_reasons)
            if reason_table.empty:
                render_empty_state(
                    "Nenhum motivo selecionado",
                    "O ranking de motivos está vazio, mas as demais análises de afastamentos continuam disponíveis.",
                    icon="🎯",
                    hint="Selecione motivos no filtro lateral ou use Todos.",
                )
            else:
                show_chart(pareto_chart(
                    reason_table["Motivo"].tolist(), reason_table["Valor"].astype(int).tolist(),
                    title=dynamic_title("Motivos no período", months=selected_months, units=selected_units, include_units=False),
                ))
            st.caption(coverage_notes["Afastamentos"])

        render_section_header("📋", "Matriz por unidade")
        latest_series = _month_series(unit_rows, last_m)
        previous_series = _month_series(unit_rows, prev_m)
        matrix = pd.DataFrame({
            "Unidade": unit_rows["indicador"].astype(str),
            "Último mês": latest_series,
            "Mês anterior": previous_series,
        })
        matrix["Variação (%)"] = _variation_series(
            matrix["Último mês"], matrix["Mês anterior"]
        )
        matrix["Participação (%)"] = matrix["Último mês"] / matrix["Último mês"].sum() * 100 if matrix["Último mês"].sum() else 0
        display_matrix(matrix, integer_columns=["Último mês", "Mês anterior"], percent_columns=["Variação (%)", "Participação (%)"], variation_columns=["Variação (%)"], bar_columns=["Último mês"], variation_semantics="lower")

        population = load_population()
        rate_table = add_rate_per_100(ranking, population=population)
        if not rate_table.empty:
            render_section_header("👥", "Afastamentos por 100 colaboradores")
            display_matrix(
                rate_table[["Unidade", "Valor", "Populacao", "Taxa por 100 colaboradores"]],
                integer_columns=["Valor", "Populacao"],
                percent_columns=["Taxa por 100 colaboradores"],
                bar_columns=["Taxa por 100 colaboradores"],
            )
        else:
            st.caption(
                "Para comparar taxas entre unidades, preencha population_by_unit.csv com a população real."
            )

        target_table = apply_unit_targets(
            ranking,
            indicator="Afastamentos ativos",
            value_column="Valor",
        )
        if not target_table.empty:
            render_section_header("🎯", "Cumprimento de metas por unidade")
            display_matrix(
                target_table[["Unidade", "Valor", "Meta", "Status"]],
                integer_columns=["Valor", "Meta"],
                bar_columns=["Valor"],
            )

    with tab_abs:
        abs_months = [month for month in selected_months if month in absenteismo.get("month_cols", [])]
        period_rank = unit_period_ranking(data, selected_months, selected_units, "Dias Perdidos")
        latest_rank = unit_latest_ranking(data, selected_months, selected_units, "Dias Perdidos")
        total_period_days = float(period_rank["Valor"].sum()) if not period_rank.empty else 0
        latest_days = float(latest_rank["Valor"].sum()) if not latest_rank.empty else 0
        previous_days = float(latest_rank["Anterior"].sum()) if not latest_rank.empty else 0
        leader = period_rank.iloc[0] if not period_rank.empty else None

        render_kpi_row([
            {
                "icon": "📋", "label": "Dias perdidos no período", "value": f"{total_period_days:,.0f}",
                "current": latest_days, "previous": previous_days, "series": metric_series(monthly_metrics, "Dias Perdidos"),
                "color": "red", "context": f"Média de {total_period_days/max(len(abs_months),1):,.0f}/mês", "trend_label": trend_lbl,
                "target": TARGETS["absenteismo_monthly_max"], "target_direction": "lower",
            },
            {
                "icon": "📅", "label": "Último mês", "value": f"{latest_days:,.0f}",
                "current": latest_days, "previous": previous_days, "series": metric_series(monthly_metrics, "Dias Perdidos"),
                "color": "orange", "context": last_m, "trend_label": trend_lbl,
                "target": TARGETS["absenteismo_monthly_max"], "target_direction": "lower",
            },
            {
                "icon": "🏭", "label": "Maior impacto", "value": str(leader["Unidade"]) if leader is not None else "—",
                "current": float(leader["Valor"]) if leader is not None else 0, "previous": 0, "series": [],
                "color": "purple", "context": f"{leader['Valor']:,.0f} dias | {leader['Participação (%)']:.1f}%" if leader is not None else "Sem dados",
                "show_trend": False, "target_direction": "neutral",
            },
            {
                "icon": "⚖️", "label": "Variação do mês", "value": f"{calc_variation(latest_days, previous_days):+.1f}%",
                "current": latest_days, "previous": previous_days, "series": metric_series(monthly_metrics, "Dias Perdidos"),
                "color": "red" if latest_days > previous_days else "green", "context": f"{previous_days:,.0f} → {latest_days:,.0f}",
                "show_trend": False, "target_direction": "lower",
            },
        ], cols_count=4)

        render_section_header("🌡️", "Mapa de calor por unidade e mês")
        heat_rows = []
        for unit in ABSENTEISMO_UNITS:
            if unit not in selected_units:
                continue
            unit_data = absenteismo[unit]["data"]
            total = unit_data[unit_data["indicador"].astype(str).str.casefold().eq("total")]
            heat_rows.append({"Unidade": unit, **{month: int(total[month].sum()) for month in abs_months}})
        heat_frame = pd.DataFrame(heat_rows)
        show_chart(matrix_heatmap(
            heat_frame,
            row_col="Unidade", month_cols=abs_months,
            title=dynamic_title("Intensidade de dias perdidos", months=abs_months, units=selected_units),
        ))

        col_trend, col_rank = st.columns([3, 2])
        with col_trend:
            render_section_header("📈", "Tendência de dias perdidos")
            unit_options = [unit for unit in ABSENTEISMO_UNITS if unit in selected_units]
            selected_abs_unit = st.selectbox("Unidade analisada", ["Total"] + unit_options, key="v8_abs_unit")
            if selected_abs_unit == "Total":
                values = metric_series(monthly_metrics, "Dias Perdidos")
            else:
                unit_data = absenteismo[selected_abs_unit]["data"]
                total = unit_data[unit_data["indicador"].astype(str).str.casefold().eq("total")]
                values = [float(total[month].sum()) for month in abs_months]
            frame = pd.DataFrame({"Mês": abs_months, "Dias Perdidos": values})
            time_series_figure(
                frame,
                "Dias Perdidos",
                dynamic_title("Dias perdidos", months=abs_months, units=[selected_abs_unit] if selected_abs_unit != "Total" else selected_units),
                target=TARGETS["absenteismo_monthly_max"],
                projections=True,
            )
        with col_rank:
            render_section_header("🏆", "Participação no período")
            period_rank_display = period_rank.copy()
            period_rank_display["Anterior"] = 0
            show_chart(ranking_bar_chart(
                period_rank_display,
                label_col="Unidade", value_col="Valor", previous_col="Anterior", share_col="Participação (%)",
                title=dynamic_title("Dias perdidos acumulados", months=abs_months, units=selected_units),
                colors_by_label=UNIT_COLORS,
            ))

        population = load_population()
        days_rate = add_rate_per_100(
            period_rank,
            population=population,
            rate_column="Dias perdidos por 100 colaboradores",
        )
        if not days_rate.empty:
            render_section_header("📐", "Indicador normalizado por população")
            display_matrix(
                days_rate[["Unidade", "Valor", "Populacao", "Dias perdidos por 100 colaboradores"]],
                integer_columns=["Valor", "Populacao"],
                percent_columns=["Dias perdidos por 100 colaboradores"],
                bar_columns=["Dias perdidos por 100 colaboradores"],
            )

        days_targets = apply_unit_targets(
            latest_rank,
            indicator="Dias Perdidos",
            value_column="Valor",
        )
        if not days_targets.empty:
            render_section_header("🎯", "Metas mensais de dias perdidos")
            display_matrix(
                days_targets[["Unidade", "Valor", "Meta", "Status"]],
                integer_columns=["Valor", "Meta"],
                bar_columns=["Valor"],
            )

        col_cause, col_gender = st.columns(2)
        with col_cause:
            render_section_header("🩻", "Composição por causa")
            categories, cause_data = compute_absenteismo_by_cause(absenteismo, selected_units, abs_months)
            show_chart(percent_stacked_bar_chart(
                cause_data,
                categories,
                dynamic_title("Causas por unidade", months=abs_months, units=selected_units),
                colors=[COLORS["blue"], COLORS["purple"], COLORS["green"]],
            ))
        with col_gender:
            render_section_header("👥", "Composição por gênero")
            categories, gender_data = compute_absenteismo_by_gender(absenteismo, selected_units, abs_months)
            show_chart(percent_stacked_bar_chart(
                gender_data,
                categories,
                dynamic_title("Gênero por unidade", months=abs_months, units=selected_units),
                colors=[COLORS["blue"], COLORS["pink"]],
            ))

        render_section_header("💸", "Simulação de impacto financeiro")
        col_input, col_cost = st.columns([1, 2])
        with col_input:
            daily_cost = st.number_input(
                "Custo estimado por dia perdido (R$)", min_value=0.0, value=DEFAULT_DAILY_ABSENCE_COST, step=50.0,
                help="Parâmetro de simulação; não é lido da planilha.",
            )
            st.metric("Custo estimado", f"R$ {total_period_days*daily_cost:,.2f}")
            st.caption("Estimativa gerencial baseada exclusivamente nos dias perdidos do filtro atual.")
        with col_cost:
            cost_frame = period_rank.copy()
            if not cost_frame.empty:
                cost_frame["Custo"] = cost_frame["Valor"] * daily_cost
                show_chart(ranking_bar_chart(
                    cost_frame.rename(columns={"Custo": "Valor Custo"}),
                    label_col="Unidade", value_col="Valor Custo", share_col="Participação (%)",
                    title=dynamic_title("Impacto financeiro estimado", months=abs_months, units=selected_units),
                    colors_by_label=UNIT_COLORS, value_suffix="",
                ))

    with tab_prev:
        st.caption("Os indicadores previdenciários são consolidados na planilha e não possuem abertura por unidade.")
        prev_data = afastamentos["previdenciaria"].copy()
        prev_kpis = []
        for index, row in prev_data.iterrows():
            values = [float(row[month]) for month in selected_months]
            prev_kpis.append({
                "icon": ["👴", "⚖️", "🔄", "🏥"][index % 4],
                "label": str(row["indicador"]), "value": f"{values[-1]:,.0f}",
                "current": values[-1], "previous": values[-2] if len(values)>1 else 0,
                "series": values, "color": ["blue", "orange", "cyan", "red"][index % 4],
                "context": f"Casos em {last_m}", "trend_label": trend_lbl, "target_direction": "lower",
            })
        render_kpi_row(prev_kpis, cols_count=4)

        selected_prev_metric = st.selectbox("Indicador previdenciário", prev_data["indicador"].astype(str).tolist(), key="v8_prev_metric")
        row = prev_data[prev_data["indicador"] == selected_prev_metric].iloc[0]
        frame = pd.DataFrame({"Mês": selected_months, selected_prev_metric: [float(row[month]) for month in selected_months]})
        time_series_figure(
            frame,
            selected_prev_metric,
            dynamic_title(selected_prev_metric, months=selected_months, units=selected_units, include_units=False),
            projections=True,
        )

        cat = afastamentos["cat_b91"]
        if not cat.empty:
            cat_values = [int(cat[month].sum()) for month in selected_months]
            cat_frame = pd.DataFrame({"Mês": selected_months, "CAT B-91": cat_values})
            show_chart(bar_chart(cat_frame, "Mês", "CAT B-91", dynamic_title("Emissões CAT B-91", months=selected_months, units=selected_units, include_units=False), COLORS["cyan"]))

# ---------------------------------------------------------------------------
# SAÚDE MENTAL
# ---------------------------------------------------------------------------
elif page == "Saúde Mental":
    common_page_header()
    render_section_header("🧠", "Saúde Mental — Rastreamento SRQ-20")
    st.caption("Rastreamento de saúde mental dos colaboradores via questionário SRQ-20 no exame periódico.")

    mental_rows = filter_saude_mental_by_units(saude_mental, selected_units)
    mental_monthly = [float(mental_rows[month].sum()) for month in selected_months] if not mental_rows.empty else [0.0] * len(selected_months)
    latest_ranking = unit_latest_ranking(data, selected_months, selected_units, "SRQ-20")
    period_ranking = unit_period_ranking(data, selected_months, selected_units, "SRQ-20")
    leader = latest_ranking.iloc[0] if not latest_ranking.empty else None

    # --- Derived metrics ---
    current_cases = mental_monthly[-1] if mental_monthly else 0.0
    previous_cases = mental_monthly[-2] if len(mental_monthly) > 1 else 0.0
    var_pct = calc_variation(current_cases, previous_cases)

    # Taxa de incidência = SRQ-20 / Exames periódicos do mês
    exam_volume = data.get("exames", {}).get("volume", pd.DataFrame())
    periodicos_row = exam_volume[exam_volume.get("tipo_short", pd.Series(dtype=str)) == "Periódicos"] if not exam_volume.empty else pd.DataFrame()
    exams_last = 0.0
    if not periodicos_row.empty and last_m in periodicos_row.columns:
        exams_last = float(periodicos_row.iloc[0][last_m] or 0)
    incidence_rate = (current_cases / exams_last * 100.0) if exams_last > 0 else 0.0

    # Trend status
    if len(mental_monthly) >= 3:
        recent_trend = mental_monthly[-1] - mental_monthly[-3]
        trend_status = "Piora" if recent_trend > 0 else ("Melhora" if recent_trend < 0 else "Estável")
    else:
        trend_status = "Piora" if var_pct > 5 else ("Melhora" if var_pct < -5 else "Estável")
    trend_color = "red" if trend_status == "Piora" else ("green" if trend_status == "Melhora" else "blue")

    # --- KPI Row (premium) ---
    render_kpi_row([
        {
            "icon": "🧠",
            "label": "SRQ-20 alterados",
            "value": f"{current_cases:,.0f}",
            "current": current_cases,
            "previous": previous_cases,
            "series": mental_monthly,
            "color": "purple",
            "context": f"Total em {last_m}",
            "trend_label": trend_lbl,
            "target": TARGETS.get("mental_cases_max"),
            "target_direction": "lower",
        },
        {
            "icon": "📉",
            "label": "Taxa de Incidência",
            "value": f"{incidence_rate:.1f}%",
            "current": incidence_rate,
            "previous": 0,
            "series": [],
            "color": "pink",
            "context": "casos / exames periódicos",
            "show_trend": False,
            "target_direction": "lower",
        },
        {
            "icon": "🏭",
            "label": "Unidade crítica",
            "value": str(leader["Unidade"]) if leader is not None else "—",
            "current": float(leader["Valor"]) if leader is not None else 0,
            "previous": float(leader["Anterior"]) if leader is not None else 0,
            "series": [],
            "color": "orange",
            "context": f"{leader['Valor']:,.0f} caso(s) | {leader['Participação (%)']:.1f}%" if leader is not None else "Sem dados",
            "show_trend": False,
            "target_direction": "lower",
        },
        {
            "icon": "📡",
            "label": "Tendência",
            "value": trend_status,
            "current": current_cases,
            "previous": previous_cases,
            "series": mental_monthly,
            "color": trend_color,
            "context": f"Variação: {var_pct:+.1f}% vs mês anterior",
            "show_trend": False,
            "target_direction": "lower",
        },
    ], cols_count=4)

    # --- Narrative insight card ---
    top_units = []
    if not period_ranking.empty:
        top_units = period_ranking.head(2)["Unidade"].tolist()
    top_units_str = " e ".join(top_units) if top_units else "—"

    if var_pct > 10:
        narrative = f"SRQ-20 aumentou {var_pct:.0f}% no último mês. Maior concentração em {top_units_str}. Recomenda-se atenção prioritária."
        insight_type = "warning"
        insight_icon = "⚠️"
        insight_title = "Atenção: piora detectada"
    elif var_pct < -10:
        narrative = f"SRQ-20 reduziu {abs(var_pct):.0f}% no último mês. Concentração principal em {top_units_str}."
        insight_type = "success"
        insight_icon = "✅"
        insight_title = "Melhora no período"
    else:
        narrative = f"Volume estável ({var_pct:+.1f}%). Maior concentração em {top_units_str}."
        insight_type = ""
        insight_icon = "➡️"
        insight_title = "Situação estável"

    render_insight(insight_icon, insight_title, narrative, insight_type)

    # --- Main charts ---
    col_trend, col_rank = st.columns([3, 2])
    with col_trend:
        render_section_header("📈", "Evolução SRQ-20 + Média Móvel")
        options = ["Total"] + mental_rows["unidade"].astype(str).tolist() if not mental_rows.empty else ["Total"]
        mental_metric = st.selectbox("Unidade analisada", options, key="v12_mental_unit")
        if mental_metric == "Total" or mental_rows.empty:
            values = mental_monthly
        else:
            row = mental_rows[mental_rows["unidade"] == mental_metric]
            values = [float(row.iloc[0][month]) for month in selected_months] if not row.empty else [0.0] * len(selected_months)
        frame = pd.DataFrame({"Mês": selected_months, "SRQ-20": values})
        time_series_figure(
            frame,
            "SRQ-20",
            dynamic_title("Triagens SRQ-20 alteradas", months=selected_months, units=selected_units),
            target=TARGETS.get("mental_cases_max") if mental_metric == "Total" else None,
            projections=True,
        )

    with col_rank:
        render_section_header("🏆", "Unidades com maior incidência")
        show_chart(ranking_bar_chart(
            latest_ranking,
            label_col="Unidade", value_col="Valor", previous_col="Anterior", share_col="Participação (%)",
            title=dynamic_title(f"SRQ-20 — {last_m}", months=[last_m], units=selected_units),
            colors_by_label=UNIT_COLORS,
        ))

    # --- Heatmap ---
    render_section_header("🌡️", "Mapa de intensidade por unidade e mês")
    if not mental_rows.empty:
        heat_frame = mental_rows[["unidade"] + selected_months].copy().rename(columns={"unidade": "Unidade"})
        show_chart(matrix_heatmap(
            heat_frame,
            row_col="Unidade", month_cols=selected_months,
            title=dynamic_title("SRQ-20 por unidade e mês", months=selected_months, units=selected_units),
        ))
    else:
        st.info("Sem dados de SRQ-20 para o filtro atual.")

    # --- Composition ---
    render_section_header("📊", "Composição acumulada por unidade")
    period_display = period_ranking.copy()
    if not period_display.empty:
        period_display["Anterior"] = 0
        show_chart(ranking_bar_chart(
            period_display,
            label_col="Unidade", value_col="Valor", previous_col="Anterior", share_col="Participação (%)",
            title=dynamic_title("Casos acumulados no período", months=selected_months, units=selected_units),
            colors_by_label=UNIT_COLORS,
        ))

    # --- Population rate (if available) ---
    population = load_population()
    mental_rate = add_rate_per_100(
        period_ranking,
        population=population,
        rate_column="SRQ-20 por 100 colaboradores",
    )
    if not mental_rate.empty:
        render_section_header("👥", "SRQ-20 normalizado por população")
        display_matrix(
            mental_rate[["Unidade", "Valor", "Populacao", "SRQ-20 por 100 colaboradores"]],
            integer_columns=["Valor", "Populacao"],
            percent_columns=["SRQ-20 por 100 colaboradores"],
            bar_columns=["SRQ-20 por 100 colaboradores"],
        )

    # --- Targets ---
    mental_targets = apply_unit_targets(
        latest_ranking,
        indicator="SRQ-20",
        value_column="Valor",
    )
    if not mental_targets.empty:
        render_section_header("🎯", "Metas de saúde mental por unidade")
        display_matrix(
            mental_targets[["Unidade", "Valor", "Meta", "Status"]],
            integer_columns=["Valor", "Meta"],
            bar_columns=["Valor"],
        )

    # --- Risk reading ---
    render_section_header("💡", "Leitura de risco e recomendações")
    col_i1, col_i2 = st.columns(2)
    with col_i1:
        if var_pct > 0:
            render_insight("⚠️", "Crescimento no último mês", f"Os casos aumentaram {var_pct:.1f}% em relação a {prev_m}.", "warning")
        elif var_pct < 0:
            render_insight("✅", "Redução no último mês", f"Os casos recuaram {abs(var_pct):.1f}% em relação a {prev_m}.", "success")
        else:
            render_insight("➡️", "Estabilidade", "O volume permaneceu estável no último mês.", "")
    with col_i2:
        if leader is not None:
            render_insight(
                "🏭", "Concentração operacional",
                f"{leader['Unidade']} responde por {leader['Participação (%)']:.1f}% dos casos em {last_m}. "
                "A análise deve ser complementada por contexto clínico e populacional.",
                "warning" if leader["Participação (%)"] >= 40 else "",
            )

