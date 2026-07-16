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
from collections.abc import Mapping

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

# FORÇA TEMA ROXO DIRETO NO APP (garantia extra além do styles.py)
st.markdown("""
<style>
    .stApp { background: #130A2B !important; }
    section[data-testid="stSidebar"] { 
        background: linear-gradient(180deg, #170E33 0%, #130A2B 100%) !important; 
        border-right: 1px solid rgba(139,92,246,0.18) !important;
    }
    /* Dashboard headers e cards */
    div[data-testid="stVerticalBlock"] > div { }
    /* Remove setinha << que estava duplicada */
    #collapseSidebarBtn, #expandSidebarBtn { display: none !important; }
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
    return "S​F" if value.upper() == "SF" else value


def normalized_percent(value: object) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0.0
    return number * 100 if 0 <= number <= 1 else number




def _coerce_float(value: object, default: float = 0.0) -> float:
    """Best-effort float conversion for numeric or formatted percentage values."""
    if value is None:
        return default
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip()
    if not text:
        return default
    text = text.replace('%', '').replace('pontos', '').replace('no índice', '')
    text = text.replace('no indice', '').replace('ponto', '').strip()
    if ',' in text and '.' in text:
        text = text.replace('.', '').replace(',', '.')
    else:
        text = text.replace(',', '.')
    try:
        return float(text)
    except ValueError:
        return default


def _first_present(mapping: Mapping[str, object], *keys: str, default: object = None) -> object:
    for key in keys:
        if key in mapping and mapping[key] not in (None, ''):
            return mapping[key]
    return default


def _pick_component_icon(label: str, item: Mapping[str, object]) -> str:
    explicit_icon = _first_present(item, 'icon', 'emoji', 'symbol', default='')
    if explicit_icon:
        return str(explicit_icon)
    label_lower = label.lower()
    if 'presen' in label_lower:
        return '✅'
    if 'saúde' in label_lower or 'saude' in label_lower or 'srq' in label_lower or 'mental' in label_lower:
        return '🧠'
    if 'exame' in label_lower or 'periód' in label_lower or 'period' in label_lower:
        return '🧪'
    return '📊'


def _normalize_health_breakdown_items(breakdown: object) -> list[dict[str, object]]:
    items_source: list[object] = []
    if isinstance(breakdown, Mapping):
        components = breakdown.get('components')
        if isinstance(components, (list, tuple)):
            items_source = list(components)
        else:
            items_source = [value for value in breakdown.values() if isinstance(value, Mapping)]
    elif isinstance(breakdown, (list, tuple)):
        items_source = list(breakdown)

    normalized_items: list[dict[str, object]] = []
    for index, item in enumerate(items_source):
        if not isinstance(item, Mapping):
            continue

        label = str(
            _first_present(
                item,
                'label', 'title', 'name', 'component', 'metric', 'indicator',
                default=f'Componente {index + 1}',
            )
        )

        raw_value = _first_present(
            item,
            'value', 'percentage', 'percent', 'pct', 'score', 'current',
            'result', 'value_pct', 'display_value', 'progress',
            default=0.0,
        )
        percent_value = normalized_percent(_coerce_float(raw_value, 0.0))
        percent_value = max(0.0, min(percent_value, 100.0))

        normalized_items.append({
            'label': label,
            'icon': _pick_component_icon(label, item),
            'percent': percent_value,
        })

    return normalized_items


def render_health_score_breakdown_cards(breakdown: object) -> None:
    """Render simplified health score cards with only title, main percentage and progress bar."""
    items = _normalize_health_breakdown_items(breakdown)
    if not items:
        st.info('Não há componentes do índice disponíveis para o filtro atual.')
        return

    st.markdown(
        """
        <style>
        .health-components-wrapper { margin: 0.35rem 0 1rem 0; }
        .health-components-title {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin: 0 0 0.85rem 0;
            color: #F8FAFC;
            font-size: 1.05rem;
            font-weight: 800;
            line-height: 1.2;
        }
        .health-breakdown-card {
            background: linear-gradient(180deg, rgba(13, 37, 67, 0.96) 0%, rgba(11, 31, 57, 0.98) 100%);
            border: 1px solid rgba(76, 153, 255, 0.22);
            border-radius: 18px;
            padding: 1rem 1rem 0.95rem 1rem;
            min-height: 162px;
            box-shadow: 0 12px 28px rgba(3, 12, 24, 0.22);
        }
        .health-breakdown-card-top {
            display: flex;
            align-items: center;
            gap: 0.6rem;
            margin-bottom: 1.2rem;
        }
        .health-breakdown-icon {
            width: 30px;
            height: 30px;
            border-radius: 10px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background: rgba(59, 130, 246, 0.16);
            border: 1px solid rgba(96, 165, 250, 0.25);
            font-size: 0.95rem;
            flex: 0 0 30px;
        }
        .health-breakdown-label {
            color: #F8FAFC;
            font-size: 0.88rem;
            font-weight: 700;
            line-height: 1.25;
        }
        .health-breakdown-value {
            color: #F8FAFC;
            font-size: 2.05rem;
            font-weight: 800;
            line-height: 1;
            margin: 0 0 1.45rem 0;
            letter-spacing: -0.02em;
        }
        .health-breakdown-progress {
            width: 100%;
            height: 6px;
            border-radius: 999px;
            background: rgba(148, 163, 184, 0.20);
            overflow: hidden;
        }
        .health-breakdown-progress-fill {
            height: 100%;
            border-radius: 999px;
            background: linear-gradient(90deg, #4F95FF 0%, #31C2EB 100%);
        }
        @media (max-width: 768px) {
            .health-breakdown-card { min-height: auto; }
            .health-breakdown-value { font-size: 1.8rem; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="health-components-wrapper"><div class="health-components-title">Componentes do índice</div></div>', unsafe_allow_html=True)
    columns = st.columns(2)
    for index, item in enumerate(items):
        column = columns[index % 2]
        with column:
            st.markdown(
                f"""
                <div class="health-breakdown-card">
                    <div class="health-breakdown-card-top">
                        <div class="health-breakdown-icon">{item['icon']}</div>
                        <div class="health-breakdown-label">{item['label']}</div>
                    </div>
                    <div class="health-breakdown-value">{item['percent']:.1f}%</div>
                    <div class="health-breakdown-progress">
                        <div class="health-breakdown-progress-fill" style="width: {item['percent']:.1f}%"></div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

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
        (current_values.loc[valid] - previous_values.loc[valid]) / previous_values.loc[valid].abs() * 100.0
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

    fingerprint_source = safe_frame.to_csv(index=False, na_rep="—")
    styler = styler.set_uuid(sha1(fingerprint_source.encode("utf-8")).hexdigest()[:12])
    styler = styler.set_table_styles(
        [
            {"selector": "table", "props": [("width", "100%"), ("border-collapse", "separate"), ("border-spacing", "0")]},
            {"selector": "thead th", "props": [("background", "#1E1240"), ("color", "#C4B5FD"), ("font-weight", "700"), ("padding", "10px 12px"), ("border-bottom", "1px solid rgba(139,92,246,.20)")]},
            {"selector": "tbody td", "props": [("padding", "9px 12px"), ("color", "#E9D5FF"), ("border-bottom", "1px solid rgba(139,92,246,.10)")]},
            {"selector": "tbody tr:nth-child(even)", "props": [("background", "rgba(30,18,64,0.4)")]},
        ]
    )

    st.markdown(
        f'<div style="overflow-x:auto; background:#1E1240; border-radius:12px; border:1px solid rgba(139,92,246,.15); padding:4px;">{styler.to_html(index=False, escape=False)}</div>',
        unsafe_allow_html=True,
    )
