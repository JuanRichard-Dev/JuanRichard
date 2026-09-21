"""Dashboard Serviço Médico CGR 2026 — V22 Controls Polish.

Power BI-style analytical experience built exclusively from the user's real
``Dashboard SM CGR 2026.xlsx`` workbook.
"""

from __future__ import annotations

# Native-runtime hardening must execute before importing NumPy, pandas,
# PyArrow or Streamlit. Community Cloud can run several sessions and fragment
# reruns in the same process; keeping native worker pools small reduces memory
# pressure and removes unnecessary cross-library thread contention.
import faulthandler
import html
import io
import os
import re
import sys
from datetime import datetime
from hashlib import sha1
from typing import Any, Callable, Iterable

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
try:
    from streamlit_autorefresh import st_autorefresh
except ModuleNotFoundError:  # Keeps lightweight CI smoke tests dependency-free.
    def st_autorefresh(*_args: Any, **_kwargs: Any) -> int:
        return 0

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

# Reconsulta a fonte remota sem exigir interação do usuário. O intervalo é
# configurável no ambiente; 600 segundos corresponde aos 10 minutos pedidos.
if os.getenv("AUTO_REFRESH_ENABLED", "true").strip().casefold() not in {"0", "false", "no", "não"}:
    try:
        _auto_refresh_seconds = max(30, int(os.getenv("AUTO_REFRESH_SECONDS", "600")))
    except ValueError:
        _auto_refresh_seconds = 600
    st_autorefresh(interval=_auto_refresh_seconds * 1000, key="dashboard_auto_refresh")


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
        "pyarrow==20.0.0\nopenpyxl==3.1.5\nrequests==2.32.5",
        language="text",
    )
    st.stop()


# ---------------------------------------------------------------------------
# Local imports
# ---------------------------------------------------------------------------
from src.analytics import (  # noqa: E402
    dynamic_title,
    executive_metric_series,
    reason_pareto_table,
    unit_change_contribution,
    unit_latest_ranking,
    unit_period_ranking,
)
from src.audit import log_event  # noqa: E402
from src.auth import enforce_authentication, render_user_sidebar  # noqa: E402
from src.charts import (  # noqa: E402
    diverging_bar_chart,
    enhanced_time_series_chart,
    grouped_bar_chart,
    line_chart,
    matrix_heatmap,
    percent_stacked_bar_chart,
    ranking_bar_chart,
    share_bar_chart,
)
from src.components import (  # noqa: E402
    render_empty_state,
    render_header,
    render_insight,
    render_kpi_row,
    render_section_header,
    sidebar_section,
)
from src.icons import icon as icon_svg  # noqa: E402
from src.config import (  # noqa: E402
    ABSENTEISMO_UNITS,
    COLORS,
    COMPARISON_MODES,
    DATA_SCHEMA_VERSION,
    DATA_STALE_AFTER_DAYS,
    METRIC_COLORS,
    METRIC_PALETTES,
    PAGE_ICONS,
    PAGE_NAMES,
    PALETTE,
    TABLE_HEIGHT,
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
    executive_comparison_table,
    mental_latest,
    periodic_coverage,
)
from src.i18n import page_label, tr  # noqa: E402
from src.population import add_rate_per_100, load_population  # noqa: E402
from src.responsive import apply_figure_safety  # noqa: E402
from src.runtime_diagnostics import runtime_payload  # noqa: E402
from src.semantic import source_coverage_notes  # noqa: E402
import streamlit.components.v1 as components  # noqa: E402
from src.styles import get_css, get_dropdown_js_fix, get_ux_effects_js  # noqa: E402


@st.cache_data(show_spinner=False)
def _cached_dashboard_css() -> str:
    """Cache the ~127KB CSS payload so it's built once per process instead of
    on every Streamlit rerun (every filter change, every button click).
    get_css() takes no arguments and is deterministic, so this only ever
    recomputes after a real app restart/redeploy — never mid-session."""
    return get_css()
from src.transforms import (  # noqa: E402
    appointment_rows_for_totals,
    calc_variation,
    compute_absenteismo_by_cause,
    compute_absenteismo_by_gender,
    compute_overview_kpis,
    filter_saude_mental_by_units,
    filter_unit_rows,
    get_available_months,
    get_previous_month,
    normalize_selected_months,
)
from src.url_state import filter_query_values, read_filter_query  # noqa: E402
from src.validators import validate_loaded_data  # noqa: E402
from src.warehouse import WarehouseError, sync_to_warehouse  # noqa: E402

# ---------------------------------------------------------------------------
# Global presentation helpers
# ---------------------------------------------------------------------------
st.markdown(_cached_dashboard_css(), unsafe_allow_html=True)

# Belt-and-suspenders enforcement for the select/multiselect dropdown palette.
# The CSS layer above (V23 in styles.py) already targets this, but BaseWeb
# can mount its own <style> for the popover *after* ours (only when the
# dropdown is first opened), so a plain CSS !important can lose an
# insertion-order tie. This repaints the same colors as inline styles —
# which always outrank any stylesheet rule — every time the dropdown DOM
# changes. height=0 keeps it invisible; it only ever touches the parent
# document via window.parent, never renders its own visible content.
components.html(get_dropdown_js_fix(), height=0)

# Small UX delighter: floating back-to-top button once the page scrolls a
# bit. Same window.parent mechanism as the fix above, fully independent —
# safe to remove on its own without touching the dropdown fix.
components.html(get_ux_effects_js(), height=0)


user_context = enforce_authentication()

if not st.session_state.get("_runtime_environment_logged", False):
    log_event("runtime_environment", runtime_payload())
    st.session_state["_runtime_environment_logged"] = True

_CHART_CFG = {
    # V21: keep chart chrome quiet; export guidance is not exposed in the sidebar.
    "displayModeBar": "hover",
    "modeBarButtonsToRemove": [
        "zoom2d", "pan2d", "select2d", "lasso2d",
        "zoomIn2d", "zoomOut2d", "autoScale2d", "resetScale2d",
    ],
    "responsive": True,
    "scrollZoom": False,
    "displaylogo": False,
    "editable": False,
    "staticPlot": False,
    "doubleClick": False,
    "showTips": False,
    "toImageButtonOptions": {
        "format": "png",
        "filename": "dashboard_cgr_2026",
        "scale": 2,
    },
}


def show_chart(fig, **kwargs: Any) -> None:
    """Render Plotly figures with a single adaptive visual gateway.

    Titles are rendered by Streamlit instead of inside Plotly. This gives every
    chart the same typography, reduces SVG padding and keeps the plotting area
    visually aligned with cards and section headers.
    """
    if fig is None:
        return

    raw_title = str(getattr(fig.layout.title, "text", "") or "").strip()
    if raw_title:
        normalized = re.sub(r"<br\s*/?>", "\n", raw_title, flags=re.IGNORECASE)
        normalized = re.sub(r"</?sup>", "", normalized, flags=re.IGNORECASE)
        normalized = html.unescape(re.sub(r"<[^>]+>", "", normalized)).strip()
        title_lines = [line.strip() for line in normalized.splitlines() if line.strip()]
        main_title = title_lines[0] if title_lines else normalized
        subtitle = " · ".join(title_lines[1:])
        subtitle_html = (
            f'<div class="v16-chart-subtitle">{html.escape(subtitle)}</div>'
            if subtitle else ""
        )
        st.markdown(
            '<div class="v16-chart-heading">'
            f'<div class="v16-chart-title">{html.escape(main_title)}</div>'
            f'{subtitle_html}</div>',
            unsafe_allow_html=True,
        )
        fig.update_layout(title=None, margin=dict(t=24))

    apply_figure_safety(fig)
    kwargs.setdefault("width", "stretch")
    kwargs.setdefault("theme", None)
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


def compact_ranking_frame(
    frame: pd.DataFrame,
    *,
    label_col: str,
    value_col: str,
    max_items: int = 6,
    other_label: str = "Outros",
    min_other_share: float = 3.0,
) -> pd.DataFrame:
    """Keep rankings compact without inventing a visually meaningless 'Outros'.

    The share denominator always remains the complete source total. A tail is
    aggregated only when it is large enough to matter visually; otherwise the
    top real categories are shown and the tiny remainder stays in the detail table.
    """
    if frame.empty:
        return frame.copy()
    work = frame[[label_col, value_col]].copy()
    work[value_col] = pd.to_numeric(work[value_col], errors="coerce").fillna(0.0)
    work = work.sort_values(value_col, ascending=False).reset_index(drop=True)
    full_total = float(work[value_col].sum())
    if len(work) > max_items:
        keep_count = max(1, max_items - 1)
        tail_total = float(work.iloc[keep_count:][value_col].sum())
        tail_share = (tail_total / full_total * 100.0) if full_total else 0.0
        if tail_share >= min_other_share:
            kept = work.iloc[:keep_count].copy()
            aggregate_label = (
                "Demais"
                if kept[label_col].astype(str).str.casefold().eq(other_label.casefold()).any()
                else other_label
            )
            work = pd.concat([
                kept,
                pd.DataFrame([{label_col: aggregate_label, value_col: tail_total}]),
            ], ignore_index=True)
        else:
            work = work.iloc[:max_items].copy()
    work["Participação (%)"] = work[value_col] / full_total * 100 if full_total else 0.0
    return work




def _variation_style(value: object, semantics: str = "neutral") -> str:
    """Keep table variations descriptive; direction is carried by the sign."""
    try:
        float(value)
    except (TypeError, ValueError):
        return ""
    return "color: #CBD5E1; font-weight: 650"

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



@st.cache_data(show_spinner=False, max_entries=64)
def _cached_table_exports(csv_text: str) -> tuple[bytes, bytes]:
    """Build CSV/Excel payloads once per distinct table state."""
    csv_bytes = csv_text.encode("utf-8-sig")
    export_frame = pd.read_csv(io.StringIO(csv_text))
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
        export_frame.to_excel(writer, index=False, sheet_name="Dados")
    return csv_bytes, excel_buffer.getvalue()


def _render_table_toolbar(
    frame: pd.DataFrame,
    *,
    table_id: str,
    enable_export: bool,
    enable_search: bool,
    enable_sort: bool,
    search_columns: list[str] | None,
) -> pd.DataFrame:
    """Render an optional search box, sort control, and CSV/Excel export
    buttons above a table, returning the (possibly filtered/sorted) copy.

    Every widget key is namespaced with table_id, so callers must keep it
    unique per table rendered on the same page run.
    """
    result = frame

    if enable_search or enable_sort:
        search_col, sort_col, dir_col = st.columns([3, 2, 2])

        if enable_search:
            with search_col:
                query = st.text_input(
                    "Buscar na tabela",
                    key=f"tbl_search_{table_id}",
                    placeholder="🔍 Buscar…",
                    label_visibility="collapsed",
                )
            if query.strip():
                candidate_columns = [c for c in (search_columns or list(result.columns)) if c in result.columns]
                if not candidate_columns:
                    candidate_columns = list(result.columns)
                needle = query.strip().lower()
                mask = pd.Series(False, index=result.index)
                for column in candidate_columns:
                    mask = mask | result[column].astype(str).str.lower().str.contains(needle, na=False, regex=False)
                result = result[mask]

        if enable_sort and not result.empty:
            sort_options = ["Padrão"] + list(result.columns)
            with sort_col:
                sort_by = st.selectbox(
                    "Ordenar por",
                    options=sort_options,
                    key=f"tbl_sort_{table_id}",
                    label_visibility="collapsed",
                    help="Escolha a coluna usada para ordenar a tabela.",
                )
            if sort_by != "Padrão":
                with dir_col:
                    if pd.api.types.is_numeric_dtype(result[sort_by]) or pd.api.types.is_datetime64_any_dtype(result[sort_by]):
                        direction_options = ["↓ Maior primeiro", "↑ Menor primeiro"]
                        ascending_labels = {"↑ Menor primeiro"}
                    else:
                        direction_options = ["A → Z", "Z → A"]
                        ascending_labels = {"A → Z"}
                    direction_label = st.selectbox(
                        "Direção",
                        options=direction_options,
                        key=f"tbl_sort_dir_{table_id}",
                        label_visibility="collapsed",
                        help="Defina a direção da ordenação.",
                    )
                result = result.sort_values(
                    by=sort_by,
                    ascending=direction_label in ascending_labels,
                    kind="stable",
                )

    if enable_export and not result.empty:
        csv_payload, xlsx_payload = _cached_table_exports(result.to_csv(index=False))
        csv_col, xlsx_col, _spacer = st.columns([1, 1, 6])
        with csv_col:
            st.download_button(
                "⬇ CSV",
                data=csv_payload,
                file_name=f"{table_id}.csv",
                mime="text/csv",
                key=f"tbl_csv_{table_id}",
            )
        with xlsx_col:
            st.download_button(
                "⬇ Excel",
                data=xlsx_payload,
                file_name=f"{table_id}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key=f"tbl_xlsx_{table_id}",
            )

    return result


def display_matrix(
    frame: pd.DataFrame,
    *,
    percent_columns: list[str] | None = None,
    integer_columns: list[str] | None = None,
    decimal_columns: list[str] | None = None,
    variation_columns: list[str] | None = None,
    bar_columns: list[str] | None = None,
    variation_semantics: str = "neutral",
    table_id: str | None = None,
    enable_export: bool = False,
    enable_search: bool = False,
    enable_sort: bool = False,
    search_columns: list[str] | None = None,
) -> None:
    """Display a compact analytical matrix with explicit formatting.

    table_id, enable_export, enable_search, and enable_sort are opt-in and
    default to off, so every existing call site renders exactly as before.
    Pass a table_id unique to this call site to turn on export (CSV/Excel)
    and, optionally, search/sort. Without a table_id the flags are ignored
    rather than raising, since a missing key would otherwise crash the page.
    """
    if frame.empty:
        render_empty_state(
            "Sem dados para exibir",
            "Não há dados no escopo selecionado.",
            icon="🔎",
        )
        return

    if table_id and (enable_export or enable_search or enable_sort):
        frame = _render_table_toolbar(
            frame,
            table_id=table_id,
            enable_export=enable_export,
            enable_search=enable_search,
            enable_sort=enable_sort,
            search_columns=search_columns,
        )
        if frame.empty:
            st.caption("🔍 Nenhum resultado para a busca. Ajuste o termo pesquisado.")
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
        styler = styler.bar(subset=[column], color="rgba(76, 141, 255, 0.20)")

    # Drop pandas' raw positional index (0, 1, 2…) from the rendered table —
    # it carries no meaning for the viewer and previously showed up as an
    # unlabeled leading numeric column.
    styler = styler.hide(axis="index")

    # Render as deterministic HTML instead of sending a pandas Styler through
    # PyArrow on every filter rerun. This preserves the Power BI-like styling
    # while removing a native serialization path from the hottest UI flow.
    fingerprint_source = safe_frame.to_csv(index=False, na_rep="—")
    styler = styler.set_uuid(sha1(fingerprint_source.encode("utf-8")).hexdigest()[:12])

    # Right-align every numeric column (and its header) so figures line up
    # on their ones place and scan the way a financial/analytical table
    # should — left alignment on numbers is the single biggest readability
    # gap in the previous table output. Columns are targeted by position via
    # the "colN" class pandas already emits per cell, so this needs no HTML
    # restructuring.
    numeric_columns = [
        column for column in safe_frame.columns
        if column in percent_columns or column in integer_columns
        or column in decimal_columns or column in variation_columns
    ]
    numeric_table_styles = [
        {
            "selector": f"th.col{safe_frame.columns.get_loc(column)}, td.col{safe_frame.columns.get_loc(column)}",
            "props": [("text-align", "right"), ("font-variant-numeric", "tabular-nums")],
        }
        for column in numeric_columns
    ]

    styler = styler.set_table_styles(
        [
            {"selector": "table", "props": [("width", "100%"), ("border-collapse", "separate"), ("border-spacing", "0")]},
            {"selector": "thead th", "props": [("background", "#16243A"), ("color", "#D7E0EC"), ("font-weight", "700"), ("padding", "10px 12px"), ("border-bottom", "1px solid rgba(151,166,186,.15)"), ("position", "sticky"), ("top", "0"), ("z-index", "1")]},
            {"selector": "tbody td", "props": [("padding", "9px 12px"), ("color", "#E2E8F0"), ("border-bottom", "1px solid rgba(151,166,186,.09)"), ("transition", "background-color .15s ease")]},
            {"selector": "tbody tr:nth-child(even)", "props": [("background", "rgba(148,163,184,.025)")]},
            {"selector": "tbody tr:hover", "props": [("background", "rgba(76,141,255,.07)")]},
            *numeric_table_styles,
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
    projections: bool = False,
    suffix: str = "",
) -> None:
    """Render observed historical values only.

    V15 intentionally removes automatic projections from the presentation
    surface so every visible value is directly traceable to the workbook.
    The ``projections`` argument is kept for call-site compatibility and is
    ignored.
    """
    metric_key = str(metric).casefold()
    if metric in METRIC_COLORS:
        chart_color = METRIC_COLORS[metric]
    elif "dias perdidos" in metric_key:
        chart_color = METRIC_COLORS["Dias Perdidos"]
    elif "afast" in metric_key:
        chart_color = METRIC_COLORS["Afastamentos"]
    elif "srq" in metric_key or "mental" in metric_key:
        chart_color = METRIC_COLORS["SRQ-20"]
    elif "atend" in metric_key or "fisioter" in metric_key or "consulta" in metric_key:
        chart_color = METRIC_COLORS["Atendimentos"]
    elif "cobertura" in metric_key:
        chart_color = METRIC_COLORS["Cobertura"]
    elif "exame" in metric_key or "periód" in metric_key or "periodic" in metric_key:
        chart_color = METRIC_COLORS["Exames"]
    else:
        chart_color = COLORS["blue"]

    fig = enhanced_time_series_chart(
        frame,
        x="Mês",
        y=metric,
        title=title,
        color=chart_color,
        moving_average=0,
        milestones=None,
        value_suffix=suffix,
    )
    show_chart(fig)


# ---------------------------------------------------------------------------
# Load and validate the real workbook
# ---------------------------------------------------------------------------
# Branded loading state. Every st.cache_data() call below already sets
# show_spinner=False (Streamlit's default spinner doesn't match the dark
# purple theme), which means a cold cache — the very first run in a new
# session, or right after a redeploy — previously rendered a blank page for
# however long the workbook took to read and validate. st.empty() reserves
# a slot we can fill immediately and clear the instant real data is ready;
# on a warm cache (every rerun after the first) this resolves in the same
# frame, so it never flashes for returning interactions.
_loading_slot = st.empty()
_loading_slot.markdown(
    """
    <div class="v27-load-screen">
        <div class="v27-load-mark">🏥</div>
        <div class="v27-load-title">Carregando o painel</div>
        <div class="v27-load-sub">Lendo e validando a planilha de origem…</div>
        <div class="v27-load-bars">
            <div class="shad-skeleton" style="width: 100%;"></div>
            <div class="shad-skeleton" style="width: 88%;"></div>
            <div class="shad-skeleton" style="width: 64%;"></div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

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
        _loading_slot.empty()
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
        _loading_slot.empty()
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

_loading_slot.empty()

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
FILTER_VERSION = "v18-executive-finish"
DEFAULT_MONTHS = month_cols[-6:] if len(month_cols) > 6 else month_cols.copy()
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
        available_exams=available_exams_all,
        available_appointments=available_atends_all,
        available_reasons=available_reasons_all,
    )
    st.session_state[FILTER_KEYS["months"]] = query_defaults["months"] or DEFAULT_MONTHS.copy()
    st.session_state[FILTER_KEYS["units"]] = query_defaults["units"] or all_units.copy()
    st.session_state[FILTER_KEYS["exams"]] = query_defaults.get("exams") or available_exams_all.copy()
    st.session_state[FILTER_KEYS["appointments"]] = query_defaults.get("appointments") or available_atends_all.copy()
    st.session_state[FILTER_KEYS["reasons"]] = query_defaults.get("reasons") or available_reasons_all.copy()
    st.session_state[FILTER_KEYS["comparison"]] = COMPARISON_MODES[0]
    st.session_state["_v8_filter_version"] = FILTER_VERSION

# Remove stale choices when the workbook changes.
# Preserve an intentionally empty month selection. Previously, the ``or``
# fallback restored every month immediately after the user removed the last
# chip, which made the X button appear not to work.
st.session_state[FILTER_KEYS["months"]] = normalize_selected_months(
    st.session_state.get(FILTER_KEYS["months"], DEFAULT_MONTHS.copy()),
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

# V14: page is part of the shareable analytical context.
_nav_key = "main_navigation_native_v8"
_query_page = str(st.query_params.get("page", "")).strip()
if _query_page in PAGE_NAMES and st.session_state.get("_page_query_applied_v14") != _query_page:
    st.session_state[_nav_key] = _query_page
    st.session_state["_page_query_applied_v14"] = _query_page


def _sync_navigation_query() -> None:
    current_page = st.session_state.get(_nav_key)
    if current_page in PAGE_NAMES:
        st.query_params["page"] = current_page
        st.session_state["_page_query_applied_v14"] = current_page


def _set_filter_values(state_key: str, values: Iterable[str]) -> None:
    """Set a slicer value through a stable Streamlit callback."""
    st.session_state[state_key] = list(values)


PERIOD_PRESETS = {
    "Último mês": month_cols[-1:] if month_cols else [],
    "Últimos 3 meses": month_cols[-3:],
    "Últimos 6 meses": DEFAULT_MONTHS.copy(),
    "Ano até agora": month_cols.copy(),
}


def _infer_period_preset() -> str:
    current = list(st.session_state.get(FILTER_KEYS["months"], []))
    for label, values in PERIOD_PRESETS.items():
        if current == list(values):
            return label
    return "Personalizado"


if "_period_preset_v18" not in st.session_state:
    st.session_state["_period_preset_v18"] = _infer_period_preset()


def _apply_period_preset() -> None:
    label = st.session_state.get("_period_preset_v18", "Últimos 6 meses")
    if label in PERIOD_PRESETS:
        st.session_state[FILTER_KEYS["months"]] = list(PERIOD_PRESETS[label])


def _restore_all_filters() -> None:
    st.session_state[FILTER_KEYS["months"]] = DEFAULT_MONTHS.copy()
    st.session_state[FILTER_KEYS["units"]] = all_units.copy()
    st.session_state[FILTER_KEYS["exams"]] = available_exams_all.copy()
    st.session_state[FILTER_KEYS["appointments"]] = available_atends_all.copy()
    st.session_state[FILTER_KEYS["reasons"]] = available_reasons_all.copy()
    st.session_state[FILTER_KEYS["comparison"]] = COMPARISON_MODES[0]
    st.session_state["_period_preset_v18"] = _infer_period_preset()


def _disable_presentation_mode() -> None:
    st.session_state["_presentation_mode_v18"] = False


def _selection_summary(values: list[str], all_values: list[str], *, all_label: str = "Todos") -> str:
    if not values:
        return "Nenhum"
    if len(values) == len(all_values):
        return all_label
    return f"{len(values)}/{len(all_values)}"


def _filters_changed_from_default(current_page: str) -> bool:
    if list(st.session_state.get(FILTER_KEYS["months"], [])) != DEFAULT_MONTHS:
        return True
    if current_page in {"Resumo Executivo", "Afastamentos", "Saúde Mental"} and list(st.session_state.get(FILTER_KEYS["units"], [])) != all_units:
        return True
    if current_page == "Exames" and list(st.session_state.get(FILTER_KEYS["exams"], [])) != available_exams_all:
        return True
    if current_page == "Atendimentos" and list(st.session_state.get(FILTER_KEYS["appointments"], [])) != available_atends_all:
        return True
    if current_page == "Afastamentos" and list(st.session_state.get(FILTER_KEYS["reasons"], [])) != available_reasons_all:
        return True
    return False


def _clear_data_cache() -> None:
    """Force a fresh download, full validation and dashboard rerun."""
    st.session_state["_manual_sync_requested_at"] = datetime.now().isoformat()
    st.cache_data.clear()




# ---------------------------------------------------------------------------
# Sidebar — os filtros são aplicados automaticamente, sem botão Aplicar.
# V14: período unificado, navegação enxuta e sincronização separada dos filtros.
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="sidebar-logo-mark" aria-hidden="true">SM</div>
        <div class="sidebar-logo-copy">
            <div class="sidebar-logo-title">CGR 2026</div>
            <div class="sidebar-logo-subtitle">Serviço Médico</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    language_code = "pt"

    sidebar_section("NAVEGAÇÃO")
    page = st.radio(
        "Navegação principal",
        options=PAGE_NAMES,
        key="main_navigation_native_v8",
        format_func=lambda page_name: (
            f"{PAGE_ICONS.get(page_name, '•')}  {page_label(page_name, language_code)}"
        ),
        label_visibility="collapsed",
        on_change=_sync_navigation_query,
    )

    presentation_mode = st.toggle(
        "Modo apresentação",
        key="_presentation_mode_v18",
        help="Oculta a navegação e amplia a área útil para TV, projetor ou compartilhamento de tela.",
    )

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    sidebar_section("FILTROS")
    st.caption("Aplicação automática · padrão: últimos 6 meses")

    st.selectbox(
        "Período",
        options=[*PERIOD_PRESETS.keys(), "Personalizado"],
        key="_period_preset_v18",
        on_change=_apply_period_preset,
        help="Use Personalizado somente quando precisar escolher meses específicos.",
    )
    if st.session_state.get("_period_preset_v18") == "Personalizado":
        st.multiselect(
            "Meses",
            options=month_cols,
            key=FILTER_KEYS["months"],
            placeholder="Selecione os meses",
        )

    unit_filter_pages = {"Resumo Executivo", "Afastamentos", "Saúde Mental"}
    if page in unit_filter_pages:
        unit_summary = _selection_summary(
            list(st.session_state.get(FILTER_KEYS["units"], [])), all_units, all_label="Todas"
        )
        with st.expander(f"Unidades · {unit_summary}", expanded=False):
            st.multiselect(
                "Unidades operacionais",
                all_units,
                key=FILTER_KEYS["units"],
                format_func=format_operational_unit,
                label_visibility="collapsed",
                placeholder="Selecione as unidades",
            )

    if page == "Exames":
        exam_summary = _selection_summary(
            list(st.session_state.get(FILTER_KEYS["exams"], [])), available_exams_all, all_label="Todos"
        )
        with st.expander(f"Tipos de exame · {exam_summary}", expanded=False):
            st.multiselect(
                "Tipos de exame",
                available_exams_all,
                key=FILTER_KEYS["exams"],
                label_visibility="collapsed",
                placeholder="Selecione os tipos de exame",
            )
    elif page == "Atendimentos":
        att_summary = _selection_summary(
            list(st.session_state.get(FILTER_KEYS["appointments"], [])), available_atends_all, all_label="Todos"
        )
        with st.expander(f"Tipos de atendimento · {att_summary}", expanded=False):
            st.multiselect(
                "Tipos de atendimento",
                available_atends_all,
                key=FILTER_KEYS["appointments"],
                label_visibility="collapsed",
                placeholder="Selecione os tipos de atendimento",
            )
    elif page == "Afastamentos":
        reason_summary = _selection_summary(
            list(st.session_state.get(FILTER_KEYS["reasons"], [])), available_reasons_all, all_label="Todos"
        )
        with st.expander(f"Motivos · {reason_summary}", expanded=False):
            st.multiselect(
                "Motivos de afastamento",
                available_reasons_all,
                key=FILTER_KEYS["reasons"],
                label_visibility="collapsed",
                placeholder="Selecione os motivos",
            )

    if _filters_changed_from_default(page):
        st.markdown(
            '<div class="v19-filter-status"><span aria-hidden="true"></span>Escopo personalizado</div>',
            unsafe_allow_html=True,
        )

        # Per-category removable chips: each active (non-default) filter on
        # this page gets its own small "reset just this one" button, so the
        # person doesn't have to open every expander to see — or clear —
        # what's currently narrowing the view. The single "Limpar filtros"
        # button below still resets everything at once.
        active_filter_chips: list[tuple[str, Callable[[], None]]] = []
        if list(st.session_state.get(FILTER_KEYS["months"], [])) != DEFAULT_MONTHS:
            def _clear_months_filter() -> None:
                st.session_state[FILTER_KEYS["months"]] = DEFAULT_MONTHS.copy()
                st.session_state["_period_preset_v18"] = _infer_period_preset()
            active_filter_chips.append(("✕ Período", _clear_months_filter))
        if page in unit_filter_pages and list(st.session_state.get(FILTER_KEYS["units"], [])) != all_units:
            def _clear_units_filter() -> None:
                st.session_state[FILTER_KEYS["units"]] = all_units.copy()
            active_filter_chips.append(("✕ Unidades", _clear_units_filter))
        if page == "Exames" and list(st.session_state.get(FILTER_KEYS["exams"], [])) != available_exams_all:
            def _clear_exams_filter() -> None:
                st.session_state[FILTER_KEYS["exams"]] = available_exams_all.copy()
            active_filter_chips.append(("✕ Tipos de exame", _clear_exams_filter))
        if page == "Atendimentos" and list(st.session_state.get(FILTER_KEYS["appointments"], [])) != available_atends_all:
            def _clear_appointments_filter() -> None:
                st.session_state[FILTER_KEYS["appointments"]] = available_atends_all.copy()
            active_filter_chips.append(("✕ Tipos de atendimento", _clear_appointments_filter))
        if page == "Afastamentos" and list(st.session_state.get(FILTER_KEYS["reasons"], [])) != available_reasons_all:
            def _clear_reasons_filter() -> None:
                st.session_state[FILTER_KEYS["reasons"]] = available_reasons_all.copy()
            active_filter_chips.append(("✕ Motivos", _clear_reasons_filter))

        if active_filter_chips:
            with st.container(key="v27_filter_chip_row"):
                chip_cols = st.columns(len(active_filter_chips))
                for chip_col, (chip_label, chip_callback) in zip(chip_cols, active_filter_chips):
                    with chip_col:
                        st.button(
                            chip_label,
                            key=f"v27_chip_{chip_label}",
                            on_click=chip_callback,
                            help=f"Remover apenas o filtro: {chip_label[2:]}",
                            width="stretch",
                        )

        st.button(
            "↺ Limpar filtros",
            key="restore_all_filters_v18",
            width="stretch",
            on_click=_restore_all_filters,
            help="Retorna ao período padrão e restaura todas as categorias da página.",
        )

    if FILTER_KEYS["comparison"] not in st.session_state:
        st.session_state[FILTER_KEYS["comparison"]] = COMPARISON_MODES[0] if COMPARISON_MODES else "Mês anterior"

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

    query_values = filter_query_values(
        selected_months, selected_units, page=page,
        exams=selected_exams if page == "Exames" else None,
        appointments=selected_atends if page == "Atendimentos" else None,
        reasons=selected_reasons if page == "Afastamentos" else None,
    )
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
    if st.session_state.get("_last_filter_fingerprint_v18") != filter_fingerprint:
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
        st.session_state["_last_filter_fingerprint_v18"] = filter_fingerprint

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    sidebar_section("DADOS")
    if isinstance(source_updated_at, datetime):
        st.caption(f"Atualizado {source_updated_at.strftime('%d/%m/%Y %H:%M')}")
    st.button(
        "⟳ Sincronizar",
        key="reload_data_v18",
        width="stretch",
        on_click=_clear_data_cache,
        help="Limpa o cache, baixa novamente, valida o XLSX e atualiza o painel.",
    )


    render_user_sidebar(user_context)

if presentation_mode:
    st.markdown('<div class="presentation-mode-marker" aria-hidden="true"></div>', unsafe_allow_html=True)
    _pres_left, _pres_right = st.columns([8, 2])
    with _pres_right:
        st.button(
            "Sair da apresentação",
            key="exit_presentation_v18",
            width="stretch",
            on_click=_disable_presentation_mode,
        )

# Empty slicers are valid states. Keep the sidebar available and avoid
# calculations that require at least one item in the active scope.
if not selected_months:
    render_header([], source_updated_at, page=page, selected_units=selected_units, language=language_code)
    render_empty_state(
        "Nenhum mês selecionado",
        "Selecione um ou mais meses para carregar os KPIs, gráficos e tabelas.",
        icon="📅",
        hint="Escolha um período no painel lateral.",
    )
    st.stop()

if page in unit_filter_pages and not selected_units:
    render_header(selected_months, source_updated_at, page=page, selected_units=selected_units, language=language_code)
    render_empty_state(
        "Nenhuma unidade selecionada",
        "O escopo atual não contém unidades operacionais.",
        icon="🏭",
        hint="Selecione uma ou mais unidades no filtro lateral ou limpe os filtros para restaurar o padrão.",
    )
    st.stop()

if page == "Exames" and not selected_exams:
    render_header(selected_months, source_updated_at, page=page, selected_units=selected_units, language=language_code)
    render_empty_state(
        "Nenhum tipo de exame selecionado",
        "Selecione ao menos um tipo de exame para montar a análise.",
        icon="🔬",
    )
    st.stop()

if page == "Atendimentos" and not selected_atends:
    render_header(selected_months, source_updated_at, page=page, selected_units=selected_units, language=language_code)
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
    render_header(selected_months, source_updated_at, page=page, selected_units=selected_units, language=language_code)
    if isinstance(source_updated_at, datetime):
        now = datetime.now(source_updated_at.tzinfo) if source_updated_at.tzinfo else datetime.now()
        updated_age_days = max(0, (now - source_updated_at).days)
    else:
        updated_age_days = 0
    metadata = data.get("metadata", {})
    if source_warning:
        st.warning(source_warning)
    specific_scope = ""
    if page == "Exames" and len(selected_exams) != len(available_exams_all):
        specific_scope = selected_exams[0] if len(selected_exams) == 1 else f"{len(selected_exams)} tipos de exame selecionados"
    elif page == "Atendimentos" and len(selected_atends) != len(available_atends_all):
        specific_scope = selected_atends[0] if len(selected_atends) == 1 else f"{len(selected_atends)} tipos de atendimento selecionados"
    elif page == "Afastamentos" and len(selected_reasons) != len(available_reasons_all):
        specific_scope = selected_reasons[0] if len(selected_reasons) == 1 else f"{len(selected_reasons)} motivos selecionados"
    if specific_scope:
        st.markdown(f'<div class="specific-filter-note">Filtro específico: {html.escape(specific_scope)}</div>', unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# RESUMO EXECUTIVO / BOARD SUMMARY
# ---------------------------------------------------------------------------
if page == "Resumo Executivo":
    common_page_header()

    board_kpis = compute_overview_kpis(data, selected_months, selected_units)
    mental_current, mental_previous = mental_latest(monthly_metrics)
    periodic_current, periodic_previous = periodic_coverage(data, selected_months)

    tooltip_text = {
        "pt": {
            "exams": "Total de exames realizados no mês mais recente do escopo.",
            "appointments": "Total de atendimentos contabilizados no mês mais recente.",
            "leaves": "Quantidade de afastamentos ativos registrada no mês mais recente.",
            "days": "Soma dos dias perdidos registrada no mês mais recente.",
            "mental": "Quantidade agregada de triagens SRQ-20 alteradas no mês mais recente.",
            "coverage": "Percentual acumulado de cobertura dos exames periódicos.",
        },
        "en": {
            "exams": "Exams performed in the latest month of the selected scope.",
            "appointments": "Appointments recorded in the latest month.",
            "leaves": "Active leaves recorded in the latest month.",
            "days": "Lost days recorded in the latest month.",
            "mental": "Aggregated positive SRQ-20 screenings in the latest month.",
            "coverage": "Cumulative periodic-exam coverage percentage.",
        },
        "fr": {
            "exams": "Examens réalisés au cours du dernier mois du périmètre.",
            "appointments": "Consultations enregistrées au cours du dernier mois.",
            "leaves": "Arrêts actifs enregistrés au cours du dernier mois.",
            "days": "Jours perdus au cours du dernier mois.",
            "mental": "Dépistages SRQ-20 positifs agrégés au cours du dernier mois.",
            "coverage": "Pourcentage cumulé de couverture des examens périodiques.",
        },
    }[language_code]

    render_section_header("◆", "Indicadores do mês")

    # V14: avoid duplicating one KPI in a large hero and again in the grid.
    # Priority is communicated by status, trend and the executive narrative below.

    render_kpi_row([
        {
            "icon": icon_svg("clipboard-check"), "label": tr("exams", language_code),
            "value": f"{board_kpis['exames']['current']:,.0f}",
            "current": board_kpis["exames"]["current"], "previous": board_kpis["exames"]["previous"],
            "series": metric_series(monthly_metrics, "Exames"), "color": "blue",
            "context": selected_months[-1], "trend_label": f"vs. {prev_m}" if prev_m else "", "tooltip": tooltip_text["exams"],
        },
        {
            "icon": icon_svg("medical-cross"), "label": tr("appointments", language_code),
            "value": f"{board_kpis['atendimentos']['current']:,.0f}",
            "current": board_kpis["atendimentos"]["current"], "previous": board_kpis["atendimentos"]["previous"],
            "series": metric_series(monthly_metrics, "Atendimentos"), "color": "green",
            "context": selected_months[-1], "trend_label": f"vs. {prev_m}" if prev_m else "", "tooltip": tooltip_text["appointments"],
        },
        {
            "icon": icon_svg("clipboard"), "label": tr("active_leaves", language_code),
            "value": f"{board_kpis['afastamentos']['current']:,.0f}",
            "current": board_kpis["afastamentos"]["current"], "previous": board_kpis["afastamentos"]["previous"],
            "series": metric_series(monthly_metrics, "Afastamentos"), "color": "orange",
            "context": selected_months[-1], "trend_label": f"vs. {prev_m}" if prev_m else "", "tooltip": tooltip_text["leaves"],
        },
        {
            "icon": icon_svg("bars"), "label": tr("lost_days", language_code),
            "value": f"{board_kpis['absenteismo']['current']:,.0f}",
            "current": board_kpis["absenteismo"]["current"], "previous": board_kpis["absenteismo"]["previous"],
            "series": metric_series(monthly_metrics, "Dias Perdidos"), "color": "red",
            "context": selected_months[-1], "trend_label": f"vs. {prev_m}" if prev_m else "",
            "tooltip": tooltip_text["days"],
        },
    ], cols_count=4)

    render_kpi_row([
        {
            "icon": icon_svg("brain-pulse"), "label": tr("srq_cases", language_code), "value": f"{mental_current:,.0f}",
            "current": mental_current, "previous": mental_previous, "series": metric_series(monthly_metrics, "SRQ-20"),
            "color": "purple", "context": selected_months[-1],
            "trend_label": f"vs. {prev_m}" if prev_m else "", "tooltip": tooltip_text["mental"],
        },
        {
            "icon": icon_svg("shield-check"), "label": tr("periodic_coverage", language_code), "value": f"{periodic_current:.1f}%",
            "current": periodic_current, "previous": periodic_previous, "color": "cyan", "context": "Acumulado no ano",
            "trend_label": f"vs. {prev_m}" if prev_m else "", "tooltip": tooltip_text["coverage"],
        },
    ], cols_count=2)

    col_trend, col_impact = st.columns([3, 2], gap="large")
    with col_trend:
        render_section_header("📈", "Evolução mensal")
        days_period_total = float(pd.to_numeric(monthly_metrics.get("Dias Perdidos", pd.Series(dtype=float)), errors="coerce").fillna(0).sum())
        trend_title = f"Dias perdidos por mês<br>{selected_months[0]} – {selected_months[-1]} · {days_period_total:,.0f} dias no período"
        time_series_figure(
            monthly_metrics, "Dias Perdidos", trend_title,
            projections=False,
        )
    with col_impact:
        render_section_header("🏭", "Distribuição por unidade")
        board_ranking = unit_period_ranking(data, selected_months, selected_units, "Dias Perdidos")
        ranking_title = f"Dias perdidos por unidade<br>{selected_months[0]} – {selected_months[-1]} · participação no período"
        show_chart(ranking_bar_chart(
            board_ranking, label_col="Unidade", value_col="Valor", share_col="Participação (%)",
            title=ranking_title, colors_by_label=UNIT_COLORS, height=390,
        ))

    if not presentation_mode:
        with st.expander("Ver comparação detalhada", expanded=False):
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
                table_id="resumo_comparativo_gestao",
                enable_sort=True,
                enable_export=True,
            )

    render_section_header("◆", "Destaques do período")
    _days_ranking = unit_period_ranking(data, selected_months, selected_units, "Dias Perdidos")
    _reason_table = reason_pareto_table(data, selected_months)
    _highlight_cols = st.columns(2)
    with _highlight_cols[0]:
        if not _days_ranking.empty:
            _top = _days_ranking.iloc[0]
            render_insight(
                "🏭",
                "Maior volume de dias perdidos",
                f"{_top['Unidade']} concentrou {_top['Participação (%)']:.1f}% dos dias perdidos no período selecionado.",
                "",
            )
        else:
            render_insight("🏭", "Distribuição por unidade", "Sem dados disponíveis no escopo atual.", "")
    with _highlight_cols[1]:
        if not _reason_table.empty:
            _reason = _reason_table.iloc[0]
            render_insight(
                "📋",
                "Motivo com maior volume",
                f"{_reason['Motivo']} representou {_reason['Participação (%)']:.1f}% dos registros classificados no período.",
                "",
            )
        else:
            render_insight("📋", "Motivos de afastamento", "Sem dados classificados no escopo atual.", "")

# ---------------------------------------------------------------------------
# EXAMES
# ---------------------------------------------------------------------------
elif page == "Exames":
    common_page_header()
    if not presentation_mode and coverage_notes.get("Exames"):
        with st.expander("Sobre os dados", expanded=False):
            st.caption(coverage_notes.get("Exames", "Visão consolidada dos exames ocupacionais."))

    exam_vol = filter_exam_volume(exames["volume"], filters)
    if exam_vol.empty:
        render_empty_state(
            "Sem registros para os filtros selecionados",
            "Não há tipos de exame disponíveis no escopo atual.",
            icon="🔬",
            hint="Ajuste os tipos de exame ou limpe os filtros.",
        )
        st.stop()
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

    # --- KPI Row com tooltips contextuais ---
    render_kpi_row([
        {
            "icon": "🔬",
            "label": "Exames realizados",
            "value": f"{current:,.0f}".replace(",", "."),
            "current": current,
            "previous": previous,
            "series": total_by_month,
            "color": "blue",
            "context": f"{total_period:,.0f} no período · {len(exam_vol)} tipo(s)".replace(",", "."),
            "trend_label": trend_lbl,
            "tooltip": "Total de exames ocupacionais realizados no período selecionado, somando todos os tipos de exame filtrados.",
        },
        {
            "icon": "🔄",
            "label": "Exames periódicos",
            "value": f"{periodic_series[-1] if periodic_series else 0:,.0f}".replace(",", "."),
            "current": periodic_series[-1] if periodic_series else 0,
            "previous": periodic_series[-2] if len(periodic_series) > 1 else 0,
            "series": periodic_series,
            "color": "blue",
            "context": f"{periodic_total:,.0f} no período · {(periodic_total / total_period * 100) if total_period else 0:.1f}% do volume".replace(",", "."),
            "trend_label": trend_lbl,
            "tooltip": "Quantidade de exames periódicos realizados. Exames periódicos são obrigatórios pela NR-7 e garantem o acompanhamento contínuo da saúde dos colaboradores.",
        },
        {
            "icon": "📈",
            "label": "Cobertura acumulada",
            "value": f"{periodic_pct:.1f}%",
            "current": periodic_pct,
            "previous": periodic_pct_series[-2] if len(periodic_pct_series) > 1 else 0,
            "series": periodic_pct_series,
            "color": "cyan",
            "context": f"Indicador em {last_m}",
            "trend_label": trend_lbl,
            "tooltip": "Percentual acumulado de colaboradores que realizaram o exame periódico no ano, conforme os dados da planilha.",
        },
        {
            "icon": "✅",
            "label": "Presença no Periódico",
            "value": f"{presence_pct:.1f}%",
            "current": presence_pct,
            "previous": presence_series[-2] if len(presence_series) > 1 else 0,
            "series": presence_series,
            "color": "cyan",
            "context": f"Inverso das faltas ({absence_pct:.1f}%)",
            "trend_label": trend_lbl,
            "tooltip": f"Taxa de presença nos exames periódicos, calculada como 100% menos a taxa de faltas/não agendamento ({absence_pct:.1f}%).",
        },
    ], cols_count=4)
    # --- Leitura descritiva baseada somente nos dados observados ---
    prev_cov = periodic_pct_series[-2] if len(periodic_pct_series) > 1 else periodic_pct
    cov_points = periodic_pct - prev_cov
    if cov_points > 0:
        cov_txt = f"aumentou {cov_points:.1f} pontos".replace(".", ",")
        n_icon, n_title = "↗", "Variação da cobertura"
    elif cov_points < 0:
        cov_txt = f"reduziu {abs(cov_points):.1f} pontos".replace(".", ",")
        n_icon, n_title = "↘", "Variação da cobertura"
    else:
        cov_txt = "permaneceu no mesmo nível"
        n_icon, n_title = "→", "Cobertura no período"
    narrative = (
        f"Cobertura acumulada em {str(round(periodic_pct,1)).replace('.',',')}%; "
        f"{cov_txt} em relação ao mês anterior. "
        f"Presença no periódico: {str(round(presence_pct,1)).replace('.',',')}%; "
        f"faltas/não agendamento: {str(round(absence_pct,1)).replace('.',',')}%."
    )
    render_insight(n_icon, n_title, narrative, "")

    tab_exam_overview, tab_exam_types, tab_exam_detail = st.tabs([
        "Visão geral", "Tipos de exame", "Detalhamento"
    ])

    with tab_exam_overview:
        col_volume, col_coverage = st.columns(2, gap="large")
        with col_volume:
            render_section_header("📈", "Volume mensal")
            volume_df = pd.DataFrame({"Mês": months, "Exames": total_by_month})
            time_series_figure(
                volume_df,
                "Exames",
                f"Exames realizados por mês<br>{months[0]} – {months[-1]} · {total_period:,.0f} no período",
            )
        with col_coverage:
            render_section_header("◉", "Cobertura acumulada")
            if periodic_pct_series:
                trend_df = pd.DataFrame({
                    "Mês": pct_months[:len(periodic_pct_series)],
                    "Cobertura": periodic_pct_series,
                })
                trend_df = trend_df[trend_df["Mês"].isin(months)]
                if not trend_df.empty:
                    time_series_figure(
                        trend_df,
                        "Cobertura",
                        f"Cobertura acumulada de periódicos<br>{last_m} · {periodic_pct:.1f}%",
                        suffix="%",
                    )
                else:
                    render_empty_state(
                        "Sem histórico de cobertura",
                        "Não há histórico de cobertura para o período selecionado.",
                        icon="📅",
                    )

    with tab_exam_types:
        col_comp, col_rank = st.columns(2)
        with col_comp:
            render_section_header("🧱", "Composição mensal")
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
                    colors=METRIC_PALETTES["Exames"],
                    top_n=4,
                ))
        with col_rank:
            render_section_header("📊", "Volume por tipo")
            if not exam_vol.empty:
                type_totals = (
                    exam_vol.assign(Total=exam_vol[months].sum(axis=1))
                    [["tipo_short", "Total"]]
                    .rename(columns={"tipo_short": "Tipo", "Total": "Valor"})
                    .sort_values("Valor", ascending=False)
                )
                type_totals = compact_ranking_frame(
                    type_totals, label_col="Tipo", value_col="Valor", max_items=6
                )
                show_chart(ranking_bar_chart(
                    type_totals,
                    label_col="Tipo",
                    value_col="Valor",
                    share_col="Participação (%)",
                    title=dynamic_title("Volume acumulado por tipo", months=months, include_units=False),
                    default_color=METRIC_COLORS["Exames"],
                ))

        if not exam_vol.empty and len(months) > 1:
            trend_totals = (
                exam_vol.assign(Total=exam_vol[months].sum(axis=1))
                .sort_values("Total", ascending=False)
                .head(3)
            )
            top_exam_types = trend_totals["tipo_short"].astype(str).tolist()
            if top_exam_types:
                render_section_header("↗", "Evolução dos tipos mais realizados")
                type_trend = {"Mês": months}
                for exam_type in top_exam_types:
                    row = exam_vol[exam_vol["tipo_short"].astype(str) == exam_type]
                    type_trend[exam_type] = [float(row[month].sum()) for month in months]
                show_chart(line_chart(
                    pd.DataFrame(type_trend),
                    "Mês",
                    top_exam_types,
                    names=top_exam_types,
                    colors=PALETTE[:len(top_exam_types)],
                    title=f"Principais tipos ao longo do período<br>{months[0]} – {months[-1]}",
                    height=390,
                ))

    with tab_exam_detail:
        if not exam_vol.empty:
            detail = exam_vol[["tipo_short"] + months].copy()
            detail = detail.rename(columns={"tipo_short": "Tipo"})
            detail["Total"] = detail[months].sum(axis=1)
            display_matrix(
                detail,
                integer_columns=months + ["Total"],
                bar_columns=["Total"],
                table_id="exames_detalhamento_mensal",
                enable_search=True,
                enable_sort=True,
                enable_export=True,
                search_columns=["Tipo"],
            )


# ---------------------------------------------------------------------------
# ATENDIMENTOS
# ---------------------------------------------------------------------------
elif page == "Atendimentos":
    common_page_header()
    if not presentation_mode and coverage_notes.get("Atendimentos"):
        with st.expander("Sobre os dados", expanded=False):
            st.caption(coverage_notes["Atendimentos"])

    atend_data = filter_appointments(atendimentos, filters)
    if atend_data.empty:
        render_empty_state(
            "Sem registros para os filtros selecionados",
            "Não há atendimentos disponíveis no escopo atual.",
            icon="🩺",
            hint="Ajuste os tipos de atendimento ou limpe os filtros.",
        )
        st.stop()
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
            "icon": "🩺", "label": "Atendimentos no mês", "value": f"{total_series[-1] if total_series else 0:,.0f}",
            "current": total_series[-1] if total_series else 0, "previous": total_series[-2] if len(total_series)>1 else 0,
            "series": total_series, "color": "green", "context": f"{total_period:,.0f} no período · sem dupla contagem", "trend_label": trend_lbl,
            "tooltip": "Total de atendimentos no período selecionado, sem dupla contagem de sessões de fisioterapia.",
        },
        {
            "icon": "👨‍⚕️", "label": "Atendimento médico", "value": f"{medical_series[-1] if medical_series else 0:,.0f}",
            "current": medical_series[-1] if medical_series else 0, "previous": medical_series[-2] if len(medical_series)>1 else 0,
            "series": medical_series, "color": "green", "context": f"{sum(medical_series):,.0f} no período · {sum(medical_series)/total_period*100 if total_period else 0:.1f}%", "trend_label": trend_lbl,
            "tooltip": "Atendimentos realizados por profissionais médicos no período selecionado.",
        },
        {
            "icon": "🦴", "label": "Fisioterapia", "value": f"{physio_series[-1] if physio_series else 0:,.0f}",
            "current": physio_series[-1] if physio_series else 0, "previous": physio_series[-2] if len(physio_series)>1 else 0,
            "series": physio_series, "color": "cyan", "context": f"{sum(physio_series):,.0f} no período · {sum(physio_series)/total_period*100 if total_period else 0:.1f}%", "trend_label": trend_lbl,
            "tooltip": "Sessões de fisioterapia no período selecionado, contabilizadas separadamente do atendimento médico.",
        },
        {
            "icon": "📅", "label": "Pico mensal", "value": f"{max(total_series) if total_series else 0:,.0f}",
            "current": max(total_series) if total_series else 0, "previous": 0, "series": total_series,
            "color": "green", "context": months[peak_index] if months else "—", "show_trend": False,
            "tooltip": "Maior volume mensal de atendimentos registrado no período selecionado.",
        },
    ], cols_count=4)

    tab_att_overview, tab_att_profile, tab_att_detail = st.tabs([
        "Visão geral", "Perfil", "Detalhamento"
    ])

    with tab_att_overview:
        col_trend, col_mix = st.columns([3, 1.35], gap="large")
        with col_trend:
            render_section_header("📈", "Evolução mensal")
            trend_frame = pd.DataFrame({
                "Mês": months,
                "Total": total_series,
                "Médico": medical_series,
                "Fisioterapia": physio_series,
            })
            show_chart(line_chart(
                trend_frame,
                "Mês",
                ["Total", "Médico", "Fisioterapia"],
                names=["Total", "Médico", "Fisioterapia"],
                title=f"Atendimentos por grupo<br>{months[0]} – {months[-1]} · {total_period:,.0f} atendimentos no período",
                colors=PALETTE[:3],
                height=410,
            ))
        with col_mix:
            render_section_header("◫", "Composição do período")
            medical_period = float(sum(medical_series))
            physio_period = float(sum(physio_series))
            other_period = max(0.0, float(total_period) - medical_period - physio_period)
            share_values = {"Médico": medical_period, "Fisioterapia": physio_period}
            if other_period > 0:
                share_values["Outros"] = other_period
            show_chart(share_bar_chart(
                share_values,
                title=f"Distribuição dos atendimentos<br>{months[0]} – {months[-1]}",
                colors=METRIC_PALETTES["Atendimentos"][:len(share_values)],
                height=275,
            ))

    with tab_att_profile:
        col_comp, col_pareto = st.columns(2)
        with col_comp:
            render_section_header("🧱", "Composição mensal")
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
                colors=METRIC_PALETTES["Atendimentos"],
                top_n=4,
            ))
        with col_pareto:
            render_section_header("📊", "Volume por tipo")
            totals = appointment_rows_for_totals(atend_data).copy()
            totals["Valor"] = totals[months].sum(axis=1)
            totals = totals.rename(columns={"tipo": "Tipo"})
            totals = compact_ranking_frame(
                totals, label_col="Tipo", value_col="Valor", max_items=6
            )
            show_chart(ranking_bar_chart(
                totals,
                label_col="Tipo",
                value_col="Valor",
                share_col="Participação (%)",
                title=dynamic_title("Volume por tipo de atendimento", months=months, units=selected_units, include_units=False),
                default_color=METRIC_COLORS["Atendimentos"],
            ))

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
                colors=METRIC_PALETTES["Atendimentos"][1:3],
            ))

    with tab_att_detail:
        matrix = atend_data[["tipo"] + months].copy()
        matrix["Total"] = matrix[months].sum(axis=1)
        matrix["Participação (%)"] = matrix["Total"] / matrix["Total"].sum() * 100 if matrix["Total"].sum() else 0
        matrix["Variação (%)"] = _variation_series(
            matrix[last_m], matrix[prev_m] if prev_m and prev_m in matrix.columns else None
        )
        matrix = matrix.rename(columns={"tipo": "Tipo de atendimento"})
        display_matrix(
            matrix,
            integer_columns=months + ["Total"],
            percent_columns=["Participação (%)", "Variação (%)"],
            variation_columns=["Variação (%)"],
            bar_columns=["Total"],
            variation_semantics="neutral",
            table_id="atendimentos_matriz_tipo",
            enable_search=True,
            enable_sort=True,
            enable_export=True,
            search_columns=["Tipo de atendimento"],
        )


# ---------------------------------------------------------------------------
# AFASTAMENTOS
# ---------------------------------------------------------------------------
elif page == "Afastamentos":
    common_page_header()

    absence_metric = st.radio(
        "Métrica analisada",
        ["Afastamentos ativos", "Dias perdidos"],
        horizontal=True,
        key="v13_absence_metric",
        help="Alterne a métrica principal sem perder os filtros de período e unidade.",
    )
    is_lost_days = absence_metric == "Dias perdidos"
    metric_key = "Dias Perdidos" if is_lost_days else "Afastamentos"
    metric_title = "Dias perdidos" if is_lost_days else "Afastamentos ativos"
    metric_icon = "📋" if is_lost_days else "🚑"
    metric_color = "red" if is_lost_days else "orange"
    metric_tooltip = (
        "Soma de dias perdidos por afastamento no mês mais recente do período selecionado."
        if is_lost_days else
        "Número total de afastamentos médicos ativos no mês mais recente do período."
    )

    if is_lost_days:
        metric_months = [month for month in selected_months if month in absenteismo.get("month_cols", [])]
        unit_rows = []
        for unit in ABSENTEISMO_UNITS:
            if unit not in selected_units or unit not in absenteismo:
                continue
            unit_data = absenteismo[unit]["data"]
            total = unit_data[unit_data["indicador"].astype(str).str.casefold().eq("total")]
            unit_rows.append({"indicador": unit, **{month: float(total[month].sum()) for month in metric_months}})
        unit_rows = pd.DataFrame(unit_rows)
        ranking = unit_latest_ranking(data, selected_months, selected_units, metric_key)
        period_rank = unit_period_ranking(data, selected_months, selected_units, metric_key)
    else:
        metric_months = selected_months
        unit_rows = filter_unit_rows(afastamentos["por_unidade"], selected_units)
        ranking = unit_latest_ranking(data, selected_months, selected_units, metric_key)
        period_rank = unit_period_ranking(data, selected_months, selected_units, metric_key)

    if unit_rows.empty or not metric_months:
        render_empty_state(
            "Sem registros para os filtros selecionados",
            f"Não há dados de {metric_title.lower()} no escopo atual.",
            icon=metric_icon,
            hint="Ajuste o período, as unidades ou limpe os filtros.",
        )
        st.stop()

    metric_last_m = metric_months[-1] if metric_months else last_m
    metric_prev_m = metric_months[-2] if len(metric_months) > 1 else None
    current_total = float(ranking["Valor"].sum()) if not ranking.empty else 0.0
    previous_total = float(ranking["Anterior"].sum()) if not ranking.empty else 0.0
    monthly_change = calc_variation(current_total, previous_total)
    leader = ranking.iloc[0] if not ranking.empty else None
    monthly_values = (
        [float(unit_rows[month].sum()) for month in metric_months]
        if not unit_rows.empty and metric_months else [0.0] * len(metric_months)
    )

    render_kpi_row([
        {
            "icon": metric_icon, "label": metric_title, "value": f"{current_total:,.0f}",
            "current": current_total, "previous": previous_total, "series": monthly_values,
            "color": metric_color, "context": f"Total em {metric_last_m}", "trend_label": f"vs. {metric_prev_m}" if metric_prev_m else "", "tooltip": metric_tooltip,
        },
        {
            "icon": "🏭", "label": "Maior volume no mês", "value": str(leader["Unidade"]) if leader is not None else "—",
            "current": float(leader["Valor"]) if leader is not None else 0,
            "previous": float(leader["Anterior"]) if leader is not None else 0,
            "series": [], "color": metric_color,
            "context": f"{leader['Valor']:,.0f} · {leader['Participação (%)']:.1f}% do total" if leader is not None else "Sem dados",
            "show_trend": False,
            "tooltip": "Unidade com maior valor da métrica no mês mais recente do período selecionado.",
        },
        {
            "icon": "📈", "label": "Mudança no mês", "value": f"{current_total - previous_total:+,.0f}",
            "current": current_total, "previous": previous_total, "series": monthly_values,
            "color": metric_color,
            "context": f"{monthly_change:+.1f}% · {previous_total:,.0f} → {current_total:,.0f}", "show_trend": False, "tooltip": "Diferença absoluta e percentual da métrica em relação ao mês anterior.",
        },
    ], cols_count=3)

    leader_context = (
        f" {leader['Unidade']} concentra {leader['Participação (%)']:.1f}% do resultado mais recente."
        if leader is not None else ""
    )
    if monthly_change > 0:
        render_insight(
            "↗", "Aumento no último mês",
            f"{metric_title} aumentou {monthly_change:.1f}% em relação ao mês anterior.{leader_context}",
            "",
        )
    elif monthly_change < 0:
        render_insight(
            "↘", "Redução no último mês",
            f"{metric_title} reduziu {abs(monthly_change):.1f}% em relação ao mês anterior.{leader_context}",
            "",
        )
    else:
        render_insight(
            "→", "Sem variação no último mês",
            f"{metric_title} permaneceu no mesmo nível do mês anterior.{leader_context}",
            "",
        )

    tab_overview, tab_causes, tab_units, tab_social = st.tabs([
        "Visão geral", "Causas & perfil", "Unidades", "Previdenciário"
    ])

    with tab_overview:
        col_evol, col_rank = st.columns([3, 2])
        with col_evol:
            render_section_header("📈", "Evolução mensal")
            trend_data: dict[str, list[float] | list[str]] = {
                "Mês": metric_months,
                "Total": monthly_values,
            }
            trend_colors = [METRIC_COLORS[metric_key]]
            trend_names = ["Total"]
            trend_source = period_rank if is_lost_days else ranking
            top_units_for_trend = trend_source.head(2)["Unidade"].astype(str).tolist() if not trend_source.empty else []
            for unit in top_units_for_trend:
                selected_row = unit_rows[unit_rows["indicador"].astype(str) == unit]
                if selected_row.empty:
                    continue
                trend_data[unit] = [float(selected_row.iloc[0][month]) for month in metric_months]
                trend_names.append(unit)
                trend_colors.append(UNIT_COLORS.get(unit, METRIC_COLORS[metric_key]))
            frame = pd.DataFrame(trend_data)
            if not frame.empty and metric_months:
                show_chart(line_chart(
                    frame,
                    "Mês",
                    trend_names,
                    names=trend_names,
                    title=f"{metric_title} — total e principais unidades<br>{metric_months[0]} – {metric_months[-1]} · {sum(monthly_values):,.0f} no período",
                    colors=trend_colors,
                    height=420,
                ))
            else:
                render_empty_state("Sem histórico disponível", "Não há meses compatíveis com a métrica no filtro atual.")

        with col_rank:
            render_section_header("🏆", "Ranking por unidade")
            rank_display = period_rank.copy() if is_lost_days else ranking.copy()
            show_chart(ranking_bar_chart(
                rank_display, label_col="Unidade", value_col="Valor",
                previous_col=None if is_lost_days else "Anterior",
                share_col="Participação (%)",
                title=f"{metric_title} por unidade<br>{metric_last_m} · participação no mês",
                colors_by_label=UNIT_COLORS,
                default_color=METRIC_COLORS[metric_key],
            ))

    with tab_causes:
        if is_lost_days:
            render_section_header("▦", "Distribuição por unidade e mês")
            if not unit_rows.empty and metric_months:
                heat_frame = unit_rows.rename(columns={"indicador": "Unidade"})
                show_chart(matrix_heatmap(
                    heat_frame,
                    row_col="Unidade",
                    month_cols=metric_months,
                    title=dynamic_title("Dias perdidos por unidade e mês", months=metric_months, units=selected_units),
                ))
            else:
                render_empty_state(
                    "Sem dados de dias perdidos",
                    "Não há registros de dias perdidos para o filtro atual.",
                    icon="🏭",
                )

            col_cause, col_gender = st.columns(2)
            with col_cause:
                render_section_header("🩻", "Composição por causa")
                categories, cause_data = compute_absenteismo_by_cause(absenteismo, selected_units, metric_months)
                show_chart(percent_stacked_bar_chart(
                    cause_data, categories,
                    dynamic_title("Causas por unidade", months=metric_months, units=selected_units),
                    colors=METRIC_PALETTES["Dias Perdidos"][:3],
                ))
            with col_gender:
                render_section_header("👥", "Composição por gênero")
                categories, gender_data = compute_absenteismo_by_gender(absenteismo, selected_units, metric_months)
                show_chart(percent_stacked_bar_chart(
                    gender_data, categories,
                    dynamic_title("Gênero por unidade", months=metric_months, units=selected_units),
                    colors=[METRIC_PALETTES["Dias Perdidos"][1], "#94A3B8"],
                ))
        else:
            col_bridge, col_pareto = st.columns(2)
            with col_bridge:
                render_section_header("🧩", "Contribuição para a variação")
                _prev_total_bridge, contributions, _cur_total_bridge = unit_change_contribution(
                    data, selected_months, selected_units, metric_key
                )
                show_chart(diverging_bar_chart(
                    contributions,
                    label_col="Unidade",
                    value_col="Contribuição",
                    title=f"Contribuição por unidade<br>{metric_prev_m or 'Período anterior'} → {metric_last_m}",
                    colors_by_label=UNIT_COLORS,
                    default_color=METRIC_COLORS["Afastamentos"],
                ))
            with col_pareto:
                render_section_header("▤", "Principais motivos")
                reason_table = reason_pareto_table(data, selected_months, selected_reasons)
                if reason_table.empty:
                    render_empty_state(
                        "Nenhum motivo selecionado",
                        "O ranking de motivos está vazio, mas as demais análises continuam disponíveis.",
                        icon="🎯",
                        hint="Selecione motivos no filtro lateral ou use Todos.",
                    )
                else:
                    reason_display = compact_ranking_frame(
                        reason_table, label_col="Motivo", value_col="Valor", max_items=6
                    )
                    show_chart(ranking_bar_chart(
                        reason_display,
                        label_col="Motivo",
                        value_col="Valor",
                        share_col="Participação (%)",
                        title=dynamic_title(
                            "Principais motivos no período", months=selected_months,
                            units=selected_units, include_units=False,
                        ),
                        default_color=METRIC_COLORS["Afastamentos"],
                    ))
            if not presentation_mode:
                st.caption(coverage_notes["Afastamentos"])

    with tab_units:
        render_section_header("📋", "Comparativo por unidade")
        latest_series = _month_series(unit_rows, metric_last_m)
        previous_series = _month_series(unit_rows, metric_prev_m)
        matrix = pd.DataFrame({
            "Unidade": unit_rows["indicador"].astype(str) if not unit_rows.empty else pd.Series(dtype=str),
            "Último mês": latest_series,
            "Mês anterior": previous_series,
        })
        matrix["Variação (%)"] = _variation_series(matrix["Último mês"], matrix["Mês anterior"])
        matrix["Participação (%)"] = (
            matrix["Último mês"] / matrix["Último mês"].sum() * 100 if matrix["Último mês"].sum() else 0
        )
        if not presentation_mode:
            with st.expander("Ver comparativo detalhado", expanded=False):
                display_matrix(
                    matrix,
                    integer_columns=["Último mês", "Mês anterior"],
                    percent_columns=["Variação (%)", "Participação (%)"],
                    variation_columns=["Variação (%)"],
                    bar_columns=["Último mês"],
                    variation_semantics="neutral",
                    table_id="afastamentos_matriz_unidade_unificada",
                    enable_export=True,
                    enable_sort=True,
                )

        population = load_population()
        rate_column = "Dias perdidos por 100 colaboradores" if is_lost_days else "Afastamentos por 100 colaboradores"
        rate_source = period_rank if is_lost_days else ranking
        rate_table = add_rate_per_100(rate_source, population=population, rate_column=rate_column)
        if not rate_table.empty:
            render_section_header("👥", "Comparação por população")
            show_chart(ranking_bar_chart(
                rate_table,
                label_col="Unidade",
                value_col=rate_column,
                title=dynamic_title(rate_column, months=metric_months, units=selected_units),
                colors_by_label=UNIT_COLORS,
                default_color=METRIC_COLORS[metric_key],
                decimals=1,
            ))
            with st.expander("Ver dados normalizados", expanded=False):
                display_matrix(
                    rate_table[["Unidade", "Valor", "Populacao", rate_column]],
                    integer_columns=["Valor", "Populacao"],
                    decimal_columns=[rate_column],
                    bar_columns=[rate_column],
                    table_id="afastamentos_taxa_populacao_unificada",
                    enable_export=True,
                    enable_sort=True,
                )
        else:
            st.caption("Para comparar taxas entre unidades, preencha population_by_unit.csv com a população real.")

    with tab_social:
        render_section_header("🏥", "Indicadores previdenciários")
        prev_data = afastamentos["previdenciaria"].copy()
        prev_kpis = []
        for index, row in prev_data.iterrows():
            values = [float(row[month]) for month in selected_months]
            prev_kpis.append({
                "icon": ["👴", "⚖️", "🔄", "🏥"][index % 4],
                "label": str(row["indicador"]),
                "value": f"{values[-1]:,.0f}",
                "current": values[-1],
                "previous": values[-2] if len(values) > 1 else 0,
                "series": values,
                "color": ["blue", "orange", "cyan", "red"][index % 4],
                "context": f"Casos em {last_m}",
                "trend_label": trend_lbl,
            })
        render_kpi_row(prev_kpis, cols_count=4)

        if not prev_data.empty:
            selected_prev_metric = st.selectbox(
                "Indicador previdenciário",
                prev_data["indicador"].astype(str).tolist(),
                key="v8_prev_metric",
            )
            selected_prev_row = prev_data[prev_data["indicador"] == selected_prev_metric].iloc[0]
            frame = pd.DataFrame({
                "Mês": selected_months,
                selected_prev_metric: [float(selected_prev_row[month]) for month in selected_months],
            })
            time_series_figure(
                frame,
                selected_prev_metric,
                dynamic_title(
                    selected_prev_metric, months=selected_months,
                    units=selected_units, include_units=False,
                ),
                projections=False,
            )

        cat = afastamentos["cat_b91"]
        if not cat.empty:
            render_section_header("📊", "Emissões CAT B-91")
            cat_values = [int(cat[month].sum()) for month in selected_months]
            time_series_figure(
                pd.DataFrame({"Mês": selected_months, "CAT B-91": cat_values}),
                "CAT B-91",
                dynamic_title(
                    "Emissões CAT B-91", months=selected_months,
                    units=selected_units, include_units=False,
                ),
            )

# ---------------------------------------------------------------------------
# SAÚDE MENTAL
# ---------------------------------------------------------------------------
elif page == "Saúde Mental":
    common_page_header()
    st.caption("SRQ-20 agregado no exame periódico · resultado alterado indica rastreamento, não diagnóstico clínico.")

    mental_rows = filter_saude_mental_by_units(saude_mental, selected_units)
    if mental_rows.empty:
        render_empty_state(
            "Sem registros para os filtros selecionados",
            "Não há dados agregados de SRQ-20 para as unidades selecionadas.",
            icon="🧠",
            hint="Ajuste as unidades ou limpe os filtros.",
        )
        st.stop()
    mental_monthly = (
        [float(mental_rows[month].sum()) for month in selected_months]
        if not mental_rows.empty else [0.0] * len(selected_months)
    )
    latest_ranking = unit_latest_ranking(data, selected_months, selected_units, "SRQ-20")
    period_ranking = unit_period_ranking(data, selected_months, selected_units, "SRQ-20")
    leader = latest_ranking.iloc[0] if not latest_ranking.empty else None

    current_cases = mental_monthly[-1] if mental_monthly else 0.0
    previous_cases = mental_monthly[-2] if len(mental_monthly) > 1 else 0.0
    var_pct = calc_variation(current_cases, previous_cases)

    exam_volume = data.get("exames", {}).get("volume", pd.DataFrame())
    periodicos_row = (
        exam_volume[exam_volume.get("tipo_short", pd.Series(dtype=str)) == "Periódicos"]
        if not exam_volume.empty else pd.DataFrame()
    )
    exams_last = 0.0
    exams_previous = 0.0
    if not periodicos_row.empty and last_m in periodicos_row.columns:
        exams_last = float(periodicos_row.iloc[0][last_m] or 0)
    if not periodicos_row.empty and prev_m and prev_m in periodicos_row.columns:
        exams_previous = float(periodicos_row.iloc[0][prev_m] or 0)
    periodic_exam_series = (
        [float(periodicos_row.iloc[0][month] or 0) for month in selected_months if month in periodicos_row.columns]
        if not periodicos_row.empty else []
    )
    screening_rate = (current_cases / exams_last * 100.0) if exams_last > 0 else 0.0
    previous_screening_rate = (previous_cases / exams_previous * 100.0) if exams_previous > 0 else 0.0


    render_kpi_row([
        {
            "icon": "🧠",
            "label": "SRQ-20 alterados",
            "value": f"{current_cases:,.0f}",
            "current": current_cases,
            "previous": previous_cases,
            "series": mental_monthly,
            "color": "purple",
            "context": f"Registros em {last_m}",
            "trend_label": trend_lbl,
            "tooltip": "Quantidade agregada de triagens SRQ-20 com resultado alterado no último mês do período selecionado.",
        },
        {
            "icon": "🔄",
            "label": "Exames periódicos",
            "value": f"{exams_last:,.0f}",
            "current": exams_last,
            "previous": exams_previous,
            "series": periodic_exam_series,
            "color": "cyan",
            "context": f"Realizados em {last_m}",
            "trend_label": trend_lbl,
            "tooltip": "Quantidade de exames periódicos registrada no mesmo mês usado na leitura agregada do SRQ-20.",
        },
        {
            "icon": "📉",
            "label": "SRQ-20 / periódicos",
            "value": f"{screening_rate:.1f}%",
            "current": screening_rate,
            "previous": previous_screening_rate,
            "series": [],
            "color": "purple",
            "context": f"{current_cases:,.0f} alterados / {exams_last:,.0f} periódicos" if exams_last else "Sem denominador no mês",
            "show_trend": exams_previous > 0,
            "trend_label": trend_lbl,
            "tooltip": "Proporção observada de SRQ-20 alterados em relação aos exames periódicos do mesmo mês. Não representa diagnóstico nem incidência epidemiológica.",
        },
        {
            "icon": "🏭",
            "label": "Maior volume no mês",
            "value": str(leader["Unidade"]) if leader is not None else "—",
            "current": float(leader["Valor"]) if leader is not None else 0,
            "previous": float(leader["Anterior"]) if leader is not None else 0,
            "series": [],
            "color": "purple",
            "context": f"{leader['Valor']:,.0f} registros · {leader['Participação (%)']:.1f}% do total" if leader is not None else "Sem dados",
            "show_trend": False,
            "tooltip": "Unidade com maior número absoluto de SRQ-20 alterados no mês mais recente. Deve ser interpretada junto da população e do volume de exames.",
        },
    ], cols_count=4)

    top_units = period_ranking.head(2)["Unidade"].tolist() if not period_ranking.empty else []
    top_units_str = " e ".join(top_units) if top_units else "—"
    leader_share = float(leader["Participação (%)"]) if leader is not None else 0.0

    if var_pct > 0:
        narrative = (
            f"As triagens alteradas aumentaram {var_pct:.1f}% no último mês. "
            f"Os maiores volumes no período estão em {top_units_str}; compare também o volume de periódicos e a população de cada unidade."
        )
        insight_type, insight_icon, insight_title = "", "↗", "Aumento no último mês"
    elif var_pct < 0:
        narrative = (
            f"As triagens alteradas reduziram {abs(var_pct):.1f}% no último mês. "
            f"Os maiores volumes no período estão em {top_units_str}."
        )
        insight_type, insight_icon, insight_title = "", "↘", "Redução no último mês"
    else:
        narrative = (
            f"O volume permaneceu no mesmo nível do mês anterior. "
            f"Os maiores volumes no período estão em {top_units_str}."
        )
        insight_type, insight_icon, insight_title = "", "→", "Sem variação no último mês"
    render_insight(insight_icon, insight_title, narrative, insight_type)

    tab_overview, tab_units, tab_actions = st.tabs([
        "Visão geral", "Unidades", "Observações"
    ])

    with tab_overview:
        col_trend, col_rank = st.columns([3, 2])
        with col_trend:
            render_section_header("📈", "Evolução mensal")
            trend_data: dict[str, list[float] | list[str]] = {
                "Mês": selected_months,
                "Total": mental_monthly,
            }
            trend_names = ["Total"]
            trend_colors = [METRIC_COLORS["SRQ-20"]]
            top_mental_units = period_ranking.head(2)["Unidade"].astype(str).tolist() if not period_ranking.empty else []
            for unit in top_mental_units:
                selected_row = mental_rows[mental_rows["unidade"].astype(str) == unit]
                if selected_row.empty:
                    continue
                trend_data[unit] = [float(selected_row.iloc[0][month]) for month in selected_months]
                trend_names.append(unit)
                trend_colors.append(UNIT_COLORS.get(unit, METRIC_COLORS["SRQ-20"]))
            frame = pd.DataFrame(trend_data)
            show_chart(line_chart(
                frame,
                "Mês",
                trend_names,
                names=trend_names,
                title=f"SRQ-20 alterados — total e principais unidades<br>{selected_months[0]} – {selected_months[-1]} · {sum(mental_monthly):,.0f} registros no período",
                colors=trend_colors,
                height=420,
            ))

        with col_rank:
            render_section_header("🏆", "Maior volume no mês")
            show_chart(ranking_bar_chart(
                latest_ranking,
                label_col="Unidade", value_col="Valor", previous_col="Anterior", share_col="Participação (%)",
                title=f"SRQ-20 por unidade<br>{last_m} · participação no mês",
                colors_by_label=UNIT_COLORS,
            ))

    with tab_units:
        render_section_header("▦", "Distribuição por unidade e mês")
        if not mental_rows.empty:
            heat_frame = mental_rows[["unidade"] + selected_months].copy().rename(columns={"unidade": "Unidade"})
            show_chart(matrix_heatmap(
                heat_frame,
                row_col="Unidade", month_cols=selected_months,
                title=dynamic_title("SRQ-20 por unidade e mês", months=selected_months, units=selected_units),
            ))
        else:
            render_empty_state(
                "Sem dados de SRQ-20",
                "Não há registros de SRQ-20 para o filtro atual.",
                icon="🩺",
            )

        population = load_population()
        mental_rate = add_rate_per_100(
            period_ranking,
            population=population,
            rate_column="SRQ-20 por 100 colaboradores",
        )

        col_accum, col_rate = st.columns(2, gap="large")
        with col_accum:
            render_section_header("📊", "Acumulado no período")
            period_display = period_ranking.copy()
            if not period_display.empty:
                show_chart(ranking_bar_chart(
                    period_display,
                    label_col="Unidade", value_col="Valor", share_col="Participação (%)",
                    title=dynamic_title("SRQ-20 acumulado", months=selected_months, units=selected_units),
                    colors_by_label=UNIT_COLORS,
                    default_color=METRIC_COLORS["SRQ-20"],
                ))

        with col_rate:
            render_section_header("👥", "Por 100 colaboradores")
            if not mental_rate.empty:
                show_chart(ranking_bar_chart(
                    mental_rate,
                    label_col="Unidade",
                    value_col="SRQ-20 por 100 colaboradores",
                    title=dynamic_title("SRQ-20 por 100 colaboradores", months=selected_months, units=selected_units),
                    colors_by_label=UNIT_COLORS,
                    default_color=METRIC_COLORS["SRQ-20"],
                    decimals=1,
                ))
            else:
                st.caption("Preencha population_by_unit.csv para comparar unidades por 100 colaboradores.")

        if not mental_rate.empty:
            with st.expander("Ver dados normalizados", expanded=False):
                display_matrix(
                    mental_rate[["Unidade", "Valor", "Populacao", "SRQ-20 por 100 colaboradores"]],
                    integer_columns=["Valor", "Populacao"],
                    decimal_columns=["SRQ-20 por 100 colaboradores"],
                    bar_columns=["SRQ-20 por 100 colaboradores"],
                    table_id="saude_mental_taxa_populacao",
                    enable_export=True,
                    enable_sort=True,
                )

    with tab_actions:
        render_section_header("💡", "Observações do período")
        col_i1, col_i2 = st.columns(2)
        with col_i1:
            if var_pct > 0:
                render_insight(
                    "↗", "Aumento observado",
                    f"O volume aumentou {var_pct:.1f}% em relação a {prev_m}. Compare a mudança com o volume de exames periódicos e a população por unidade.",
                    "",
                )
            elif var_pct < 0:
                render_insight(
                    "↘", "Redução observada",
                    f"O volume recuou {abs(var_pct):.1f}% em relação a {prev_m}. A variação é apresentada diretamente a partir dos registros do período.",
                    "",
                )
            else:
                render_insight(
                    "→", "Sem variação mensal",
                    "O volume permaneceu no mesmo nível do mês anterior. A distribuição pode ser consultada por unidade e população.",
                    "",
                )

        with col_i2:
            if leader is not None:
                render_insight(
                    "🏭", "Distribuição por unidade",
                    f"{leader['Unidade']} responde por {leader_share:.1f}% dos casos em {last_m}. O quadro de Unidades permite comparar esse volume com população, periódicos e histórico.",
                    "",
                )
            else:
                render_insight("🏭", "Sem distribuição disponível", "Não há ranking disponível no escopo atual.", "")

        render_insight(
            "🧠", "Uso responsável do SRQ-20",
            "O SRQ-20 é apresentado de forma agregada como dado de rastreamento. O resultado alterado não representa diagnóstico clínico individual nem estabelece causa ocupacional.",
            "",
        )
