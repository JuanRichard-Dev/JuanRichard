"""
Charts Module — Dashboard SM CGR 2026
=======================================
Plotly chart factory functions with premium dark theme styling.
Each function returns a configured ``go.Figure`` ready for ``st.plotly_chart``.
"""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go

from src.config import COLORS, PALETTE, UNIT_COLORS
from src.responsive import (
    calculate_chart_height,
    calculate_plot_margins,
    compact_month_labels,
    estimate_legend_rows,
    get_legend_config,
    infer_category_count,
)

# ---------------------------------------------------------------------------
# Altair exploration (optional modern declarative alternative/complement)
# Altair + Vega-Lite offers excellent defaults, built-in interactivity (brush,
# zoom, tooltips, selections), and beautiful statistical visualizations.
# Use st.altair_chart() in the app. Dark theme applied manually.
# ---------------------------------------------------------------------------
try:
    import altair as alt
    ALTAIR_AVAILABLE = True
except ImportError:
    ALTAIR_AVAILABLE = False
    alt = None  # type: ignore

# ---------------------------------------------------------------------------
# Shared Layout Defaults
# ---------------------------------------------------------------------------

LAYOUT_DEFAULTS: dict = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(15, 10, 31, 0.48)",
    font=dict(family="Inter, sans-serif", color="#E9D5FF", size=12),
    margin=dict(l=55, r=30, t=80, b=90),
    legend=dict(
        bgcolor="rgba(30, 11, 58, 0.70)",
        bordercolor="rgba(124, 58, 237, 0.32)",
        borderwidth=1,
        font=dict(size=11, color="#E9D5FF"),
        orientation="h",
        yanchor="bottom",
        y=-0.35,
        xanchor="center",
        x=0.5,
    ),
    xaxis=dict(
        gridcolor="rgba(124, 58, 237, 0.14)",
        zerolinecolor="rgba(124, 58, 237, 0.28)",
        tickfont=dict(size=11, color="#C4B5FD"),
        linecolor="rgba(124, 58, 237, 0.25)",
        automargin=True,
    ),
    yaxis=dict(
        gridcolor="rgba(124, 58, 237, 0.14)",
        zerolinecolor="rgba(124, 58, 237, 0.28)",
        tickfont=dict(size=11, color="#C4B5FD"),
        linecolor="rgba(124, 58, 237, 0.25)",
        automargin=True,
    ),
    separators=",.",
    hoverlabel=dict(
        bgcolor="#1E0B3A",
        font_size=12,
        font_family="Inter, sans-serif",
        font_color="#FFFFFF",
        bordercolor="#7C3AED",
        align="left",
        namelength=-1,
    ),
    height=400,
    colorway=["#7C3AED", "#EC4899", "#D946EF", "#A78BFA", "#F472B6", "#8B5CF6", "#C084FC", "#FFFFFF"],
)


def _smart_wrap_title(text: str, max_chars: int = 65) -> str:
    """Advanced title wrapping optimized for both Streamlit and notebook rendering.
    More aggressive wrapping to prevent cutoff in narrow containers.
    """
    if not text or len(text) <= max_chars:
        return text
    if "<br>" in text or "<BR>" in text:
        return text
    words = text.split()
    lines: list[str] = []
    current_line = ""
    for word in words:
        test_line = current_line + (" " if current_line else "") + word
        if len(test_line) <= max_chars:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return "<br>".join(lines)


def wrap_long_yaxis_labels(labels: list[str], max_chars: int = 28) -> list[str]:
    """Wrap long category labels for horizontal bar charts.
    Prevents text overflow and improves readability in notebooks and narrow views.
    """
    wrapped = []
    for label in labels:
        if len(label) > max_chars:
            # Simple word-based wrapping
            words = label.split()
            lines = []
            current = ""
            for word in words:
                if len(current) + len(word) + 1 <= max_chars:
                    current = (current + " " + word).strip()
                else:
                    if current:
                        lines.append(current)
                    current = word
            if current:
                lines.append(current)
            wrapped.append("<br>".join(lines))
        else:
            wrapped.append(label)
    return wrapped


def _apply_layout(
    fig: go.Figure, title: str = "", height: int = 380, *, subtitle: str = ""
) -> go.Figure:
    """Apply content-aware layout defaults without fixed figure widths.

    - Smart wrapping for long titles to eliminate cutoffs
    - Optional elegant subtitle rendered below title via annotation
    - Increased breathing room and premium typography
    """
    category_count = infer_category_count(fig)
    series_names = [
        str(getattr(trace, "name", "") or "")
        for trace in fig.data
        if getattr(trace, "showlegend", True) is not False
    ]
    legend_rows = estimate_legend_rows(series_names) if len(series_names) > 1 else 0

    wrapped_title = _smart_wrap_title(title) if title else ""
    title_lines = max(1, wrapped_title.lower().count("<br") + 1) if wrapped_title else 0

    # Detect horizontal bar charts for special label handling
    is_horizontal_bar = False
    for trace in fig.data:
        if getattr(trace, "type", None) == "bar" and getattr(trace, "orientation", None) == "h":
            is_horizontal_bar = True
            break

    x_values: list[object] = []
    for trace in fig.data:
        trace_x = getattr(trace, "x", None)
        if trace_x is None:
            continue
        try:
            x_values.extend(list(trace_x)[:12])
        except TypeError:
            continue

    margins = calculate_plot_margins(
        title_lines=title_lines,
        legend_rows=legend_rows,
        x_label_length=max((len(str(v)) for v in x_values), default=0),
        outside_labels=any(
            getattr(trace, "textposition", None) == "outside" for trace in fig.data
        ),
    )

    # Give a little extra top margin when subtitle or multi-line title is present
    if subtitle:
        margins["t"] = max(margins.get("t", 60), 82 + title_lines * 18)
    elif title_lines > 1:
        margins["t"] = max(margins.get("t", 60), 70 + title_lines * 16)

    safe_height = calculate_chart_height(
        "generic",
        category_count=category_count,
        series_count=max(1, len(series_names)),
        legend_rows=legend_rows,
        requested=height,
    )

    # Define valores padrão para dragmode e fixedrange
    if 'interactive' not in locals():
        interactive = False

    dragmode = "zoom" if interactive else False
    fixedrange = not interactive

    layout_kwargs = {
        **LAYOUT_DEFAULTS,
        "height": safe_height,
        "autosize": True,
        "dragmode": dragmode,
        "uirevision": "dashboard-stable",
        "margin": margins,
        "transition": {"duration": 450, "easing": "cubic-in-out"},
        "xaxis": {
            **LAYOUT_DEFAULTS["xaxis"],
            "automargin": True,
            "fixedrange": fixedrange,
            "tickangle": -45 if locals().get('is_heatmap', False) or "mes" in str(title).lower() else 0,
        },
        "yaxis": {
            **LAYOUT_DEFAULTS["yaxis"],
            "automargin": True,
            "fixedrange": fixedrange,
        },
    }

    if len(series_names) > 1:
        layout_kwargs["legend"] = get_legend_config(
            item_count=len(series_names),
            max_label_length=max(map(len, series_names), default=0),
            legend_rows=legend_rows,
        )

    if title:
        layout_kwargs["title"] = dict(
            text=wrapped_title,
            font=dict(
                size=14.5 if title_lines > 1 else 15.5,
                color="#F8FBFF",
                family="Inter, sans-serif",
            ),
            x=0.015,
            xanchor="left",
            y=0.955,
            yanchor="top",
            pad=dict(t=4, b=6, l=4, r=4),
        )

    # Advanced handling for horizontal bar charts (long labels)
    if is_horizontal_bar:
        for trace in fig.data:
            if getattr(trace, "type", None) == "bar" and getattr(trace, "orientation", None) == "h":
                if hasattr(trace, "y") and trace.y is not None:
                    try:
                        wrapped_y = wrap_long_yaxis_labels(list(trace.y))
                        trace.y = wrapped_y
                    except Exception:
                        pass

        # Increase left margin for wrapped labels
        if "margin" in layout_kwargs:
            layout_kwargs["margin"]["l"] = max(layout_kwargs["margin"].get("l", 60), 95)
        else:
            layout_kwargs["margin"] = {"l": 95, "r": 30, "t": 70, "b": 50}

    fig.update_layout(**layout_kwargs)

    # Elegant subtitle as separate annotation (never cuts off, modern separation)
    if subtitle:
        sub_wrapped = _smart_wrap_title(subtitle, max_chars=90)
        sub_y = 0.905 - (title_lines - 1) * 0.028
        fig.add_annotation(
            text=sub_wrapped,
            x=0.015,
            y=sub_y,
            xref="paper",
            yref="paper",
            showarrow=False,
            font=dict(size=11.2, color="#94A3B8", family="Inter, sans-serif"),
            align="left",
            yanchor="top",
        )

    return fig


def _empty_figure(title: str, height: int, message: str = "Sem dados no escopo selecionado") -> go.Figure:
    """Return a consistent empty chart instead of a blank Plotly canvas."""
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        x=0.5,
        y=0.5,
        xref="paper",
        yref="paper",
        showarrow=False,
        font=dict(size=13, color="#64748B"),
    )
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    return _apply_layout(fig, title, height)


def _hex_to_rgb(hex_color: str) -> str:
    """Convert hex color to 'r, g, b' string for rgba() usage."""
    h = hex_color.lstrip("#")
    return f"{int(h[0:2], 16)}, {int(h[2:4], 16)}, {int(h[4:6], 16)}"


def _wrap_axis_label(label: str, max_len: int = 20) -> str:
    """Wrap long axis labels to avoid overlap in executive charts."""
    clean = str(label).strip()
    if len(clean) <= max_len:
        return clean
    words = clean.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if len(candidate) <= max_len:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return "<br>".join(lines[:3])


# ---------------------------------------------------------------------------
# Line Chart
# ---------------------------------------------------------------------------

def line_chart(
    df: pd.DataFrame,
    x: str,
    y_cols: list[str],
    names: list[str] | None = None,
    title: str = "",
    colors: list[str] | None = None,
    height: int = 380,
    fill: bool = False,
    forecasts: dict[str, list[float]] | None = None,
    forecast_x: list[str] | None = None,
) -> go.Figure:
    """Multi-series line chart with spline interpolation and optional forecast support."""
    fig = go.Figure()
    colors = colors or PALETTE
    names = names or y_cols

    for idx, col in enumerate(y_cols):
        c = colors[idx % len(colors)]
        
        # Historical Trace
        fig.add_trace(go.Scatter(
            x=df[x],
            y=df[col],
            name=names[idx],
            mode="lines+markers",
            line=dict(color=c, width=2.5, shape="spline"),
            marker=dict(
                size=7, color=c,
                line=dict(width=1.5, color="#0B0F19"),
            ),
            fill="tozeroy" if fill else None,
            fillcolor=f"rgba({_hex_to_rgb(c)}, 0.08)" if fill else None,
            hovertemplate=(
                f"<b>{names[idx]} (Histórico)</b><br>"
                "%{x}: %{y:,.0f}<extra></extra>"
            ),
        ))
        
        # Forecast Overlay Trace (Dashed)
        if forecasts and col in forecasts and forecast_x:
            f_vals = forecasts[col]
            fig.add_trace(go.Scatter(
                x=forecast_x,
                y=f_vals,
                name=f"{names[idx]} (Projeção)",
                mode="lines+markers",
                line=dict(color=c, width=2.0, shape="spline", dash="dash"),
                marker=dict(
                    size=6, color=c, symbol="circle-open",
                    line=dict(width=1.5, color=c),
                ),
                hovertemplate=(
                    f"<b>{names[idx]} (Projeção)</b><br>"
                    "%{x}: %{y:,.0f}<extra></extra>"
                ),
            ))

    return _apply_layout(fig, title, height)



# ---------------------------------------------------------------------------
# Area Chart (Stacked)
# ---------------------------------------------------------------------------

def area_chart(
    df: pd.DataFrame,
    x: str,
    y_cols: list[str],
    names: list[str] | None = None,
    title: str = "",
    colors: list[str] | None = None,
    height: int = 380,
) -> go.Figure:
    """Stacked area chart."""
    fig = go.Figure()
    colors = colors or PALETTE
    names = names or y_cols

    for idx, col in enumerate(y_cols):
        c = colors[idx % len(colors)]
        fig.add_trace(go.Scatter(
            x=df[x],
            y=df[col],
            name=names[idx],
            mode="lines",
            line=dict(width=0.5, color=c),
            stackgroup="one",
            fillcolor=f"rgba({_hex_to_rgb(c)}, 0.25)",
            hovertemplate=(
                f"<b>{names[idx]}</b><br>"
                "%{x}: %{y:,.0f}<extra></extra>"
            ),
        ))

    return _apply_layout(fig, title, height)


# ---------------------------------------------------------------------------
# Bar Chart (Single Series)
# ---------------------------------------------------------------------------

def bar_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str = "",
    color: str | None = None,
    height: int = 380,
    orientation: str = "v",
) -> go.Figure:
    """Single-series bar chart (vertical or horizontal)."""
    c = color or COLORS["blue"]

    if orientation == "h":
        fig = go.Figure(go.Bar(
            y=df[x], x=df[y], orientation="h",
            marker=dict(color=c, line=dict(width=0), cornerradius=6),
            text=df[y].apply(lambda v: f"{v:,.0f}"),
            textposition="auto",
            textfont=dict(color="#E2E8F0", size=11),
            hovertemplate="<b>%{y}</b><br>Valor: %{x:,.0f}<extra></extra>",
        ))
    else:
        fig = go.Figure(go.Bar(
            x=df[x], y=df[y], orientation="v",
            marker=dict(color=c, line=dict(width=0), cornerradius=6),
            text=df[y].apply(lambda v: f"{v:,.0f}"),
            textposition="outside",
            textfont=dict(color="#CBD5E1", size=11),
            hovertemplate="<b>%{x}</b><br>Valor: %{y:,.0f}<extra></extra>",
        ))

    return _apply_layout(fig, title, height)


# ---------------------------------------------------------------------------
# Stacked Bar Chart
# ---------------------------------------------------------------------------

def stacked_bar_chart(
    data_dict: dict[str, list],
    categories: list[str],
    title: str = "",
    colors: list[str] | None = None,
    height: int = 380,
) -> go.Figure:
    """Stacked bar chart from a dict ``{series_name: [values]}``."""
    fig = go.Figure()
    colors = colors or PALETTE

    for idx, (name, values) in enumerate(data_dict.items()):
        c = colors[idx % len(colors)]
        fig.add_trace(go.Bar(
            x=categories,
            y=values,
            name=name,
            marker=dict(color=c, cornerradius=4),
            hovertemplate=(
                f"<b>{name}</b><br>"
                "%{x}: %{y:,.0f}<extra></extra>"
            ),
        ))

    fig.update_layout(barmode="stack")
    return _apply_layout(fig, title, height)


# ---------------------------------------------------------------------------
# Grouped Bar Chart
# ---------------------------------------------------------------------------

def grouped_bar_chart(
    data_dict: dict[str, list],
    categories: list[str],
    title: str = "",
    colors: list[str] | None = None,
    height: int = 380,
) -> go.Figure:
    """Grouped bar chart for side-by-side comparisons."""
    fig = go.Figure()
    colors = colors or PALETTE

    for idx, (name, values) in enumerate(data_dict.items()):
        c = colors[idx % len(colors)]
        fig.add_trace(go.Bar(
            x=categories,
            y=values,
            name=name,
            marker=dict(color=c, cornerradius=6),
            text=[f"{v:,.0f}" for v in values],
            textposition="outside",
            cliponaxis=False,
            textfont=dict(size=11, color="#EAF2FC"),
            hovertemplate=(
                f"<b>{name}</b><br>"
                "%{x}: %{y:,.0f}<extra></extra>"
            ),
        ))

    max_value = max((float(v) for values in data_dict.values() for v in values), default=0.0)
    legend_rows = estimate_legend_rows(data_dict.keys(), available_chars=48)
    safe_height = calculate_chart_height(
        "grouped_bar", category_count=len(categories), series_count=len(data_dict),
        legend_rows=legend_rows, requested=max(height, 430),
    )
    _apply_layout(fig, title, safe_height)
    fig.update_layout(
        barmode="group",
        bargap=.24,
        bargroupgap=.08,
        legend=get_legend_config(
            item_count=len(data_dict), max_label_length=max(map(len, data_dict.keys()), default=0),
            legend_rows=legend_rows, chart_type="grouped_bar",
        ),
        margin=calculate_plot_margins(
            title_lines=max(1, len(title)//58 + 1), legend_rows=legend_rows,
            x_label_length=max(map(len, map(str, categories)), default=0), outside_labels=True,
        ),
    )
    if max_value > 0:
        fig.update_yaxes(range=[0, max_value * 1.20], automargin=True, fixedrange=True)
    fig.update_xaxes(tickfont=dict(size=11), automargin=True, fixedrange=True)
    return fig


# ---------------------------------------------------------------------------
# Horizontal Bar Chart (for rankings/comparisons)
# ---------------------------------------------------------------------------

def horizontal_bar_chart(
    labels: list[str],
    values: list[int],
    title: str = "",
    colors: list[str] | None = None,
    height: int = 350,
) -> go.Figure:
    """Horizontal bar chart — ideal for comparing named categories."""
    colors = colors or PALETTE

    # Sort ascending for horizontal bar readability
    sorted_pairs = sorted(zip(values, labels))
    sorted_values = [p[0] for p in sorted_pairs]
    sorted_labels = [p[1] for p in sorted_pairs]
    bar_colors = [colors[i % len(colors)] for i in range(len(sorted_labels))]

    fig = go.Figure(go.Bar(
        y=sorted_labels,
        x=sorted_values,
        orientation="h",
        marker=dict(
            color=bar_colors,
            line=dict(width=0),
            cornerradius=6,
        ),
        text=[f"{v:,.0f}" for v in sorted_values],
        textposition="auto",
        textfont=dict(color="#E2E8F0", size=11),
        hovertemplate="<b>%{y}</b><br>Valor: %{x:,.0f}<extra></extra>",
    ))

    return _apply_layout(fig, title, height)


# ---------------------------------------------------------------------------
# Donut Chart
# ---------------------------------------------------------------------------

def donut_chart(
    labels: list[str],
    values: list[int],
    title: str = "",
    colors: list[str] | None = None,
    height: int = 380,
) -> go.Figure:
    """Donut chart with central total annotation."""
    colors = colors or PALETTE

    fig = go.Figure(go.Pie(
        labels=labels,
        values=values,
        hole=0.6,
        marker=dict(
            colors=colors[: len(labels)],
            line=dict(color="#0B0F19", width=2),
        ),
        textfont=dict(size=11, color="#E2E8F0"),
        textinfo="percent",
        textposition="inside",
        insidetextorientation="horizontal",
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Valor: %{value:,.0f}<br>"
            "%{percent}<extra></extra>"
        ),
    ))

    total = sum(values)
    fig.add_annotation(
        text=(
            f"<b>{total:,.0f}</b><br>"
            "<span style='font-size:10px;color:#64748B'>Total</span>"
        ),
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=18, color="#F1F5F9"),
    )

    _apply_layout(fig, title, height)
    fig.update_layout(
        showlegend=True,
        margin=dict(l=20, r=20, t=44, b=20),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.05,
            xanchor="center",
            x=0.5,
            font=dict(size=11, color="#D9E6F2"),
        ),
    )
    return fig


# ---------------------------------------------------------------------------
# Heatmap
# ---------------------------------------------------------------------------

def heatmap(
    z: list[list],
    x: list[str],
    y: list[str],
    title: str = "",
    height: int = 380,
) -> go.Figure:
    """Heatmap with text annotations."""
    fig = go.Figure(go.Heatmap(
        z=z,
        x=x,
        y=y,
        colorscale=[
            [0, "#1E0B3A"],
            [0.2, "#4C1D95"],
            [0.4, "#6D28D9"],
            [0.6, "#7C3AED"],
            [0.8, "#A78BFA"],
            [1, "#EC4899"],
        ],
        text=[[f"{v:,.0f}" for v in row] for row in z],
        texttemplate="%{text}",
        textfont=dict(size=12, color="#E2E8F0"),
        hovertemplate=(
            "<b>%{y}</b> — %{x}<br>"
            "Valor: %{z:,.0f}<extra></extra>"
        ),
        colorbar=dict(
            tickfont=dict(color="#64748B"),
            borderwidth=0,
        ),
    ))

    return _apply_layout(fig, title, height)


# ---------------------------------------------------------------------------
# Treemap
# ---------------------------------------------------------------------------

def treemap(
    labels: list[str],
    parents: list[str],
    values: list[int],
    title: str = "",
    colors: list[str] | None = None,
    height: int = 420,
) -> go.Figure:
    """Treemap chart for hierarchical proportions."""
    colors = colors or PALETTE

    fig = go.Figure(go.Treemap(
        labels=labels,
        parents=parents,
        values=values,
        marker=dict(
            colors=colors[: len(labels)],
            line=dict(width=2, color="#0B0F19"),
            cornerradius=8,
        ),
        textfont=dict(size=13, color="#F1F5F9"),
        textinfo="label+value+percent parent",
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Valor: %{value:,.0f}<br>"
            "%{percentParent:.1%} do total<extra></extra>"
        ),
    ))

    return _apply_layout(fig, title, height)


# ---------------------------------------------------------------------------
# Waterfall Chart
# ---------------------------------------------------------------------------

def waterfall_chart(
    categories: list[str],
    values: list[int],
    title: str = "",
    height: int = 400,
) -> go.Figure:
    """Waterfall chart showing cumulative month-over-month changes."""
    measures = ["absolute"] + ["relative"] * (len(values) - 1)

    fig = go.Figure(go.Waterfall(
        x=categories,
        y=values,
        measure=measures,
        increasing=dict(marker=dict(color=COLORS["green"], line=dict(width=0))),
        decreasing=dict(marker=dict(color=COLORS["red"], line=dict(width=0))),
        totals=dict(marker=dict(color=COLORS["blue"], line=dict(width=0))),
        connector=dict(line=dict(color="rgba(124, 58, 237, 0.35)", width=1)),
        textposition="outside",
        cliponaxis=False,
        textfont=dict(size=11, color="#EAF2FC"),
        text=[
            f"{v:+,.0f}" if i > 0 else f"{v:,.0f}"
            for i, v in enumerate(values)
        ],
        hovertemplate="<b>%{x}</b><br>Valor: %{y:,.0f}<extra></extra>",
    ))

    return _apply_layout(fig, title, height)


# ---------------------------------------------------------------------------
# Funnel Chart
# ---------------------------------------------------------------------------

def funnel_chart(
    labels: list[str],
    values: list[int],
    title: str = "",
    colors: list[str] | None = None,
    height: int = 380,
) -> go.Figure:
    """Funnel chart for ranked distributions."""
    colors = colors or PALETTE

    fig = go.Figure(go.Funnel(
        y=labels,
        x=values,
        marker=dict(
            color=colors[: len(labels)],
            line=dict(width=1, color="#0B0F19"),
        ),
        textfont=dict(color="#E2E8F0", size=12),
        textinfo="value+percent initial",
        hovertemplate="<b>%{y}</b><br>Valor: %{x:,.0f}<extra></extra>",
        connector=dict(line=dict(color="rgba(59,130,246,0.15)", width=1)),
    ))

    return _apply_layout(fig, title, height)



def health_score_radial_chart(
    score: float,
    *,
    target: float | None = None,
    height: int = 300,
) -> go.Figure:
    """Render a clean health index without targets, zones or status labels."""
    numeric_score = max(0.0, min(float(score), 100.0))
    remaining = max(0.0, 100.0 - numeric_score)

    fig = go.Figure()
    fig.add_trace(
        go.Pie(
            values=[100],
            labels=["Escala do índice"],
            hole=0.88,
            domain={"x": [0.0, 1.0], "y": [0.0, 1.0]},
            marker={
                "colors": ["rgba(74,141,255,0.16)"],
                "line": {"color": "rgba(130,165,205,0.12)", "width": 2},
            },
            textinfo="none",
            hoverinfo="skip",
            showlegend=False,
        )
    )
    fig.add_trace(
        go.Pie(
            values=[numeric_score, remaining],
            labels=["Índice atual", "Restante da escala"],
            hole=0.70,
            domain={"x": [0.075, 0.925], "y": [0.075, 0.925]},
            marker={
                "colors": [COLORS["blue"], "rgba(30,41,59,0.56)"],
                "line": {"color": "rgba(15,23,42,0.88)", "width": 2},
            },
            sort=False,
            direction="clockwise",
            rotation=90,
            textinfo="none",
            hovertemplate="<b>%{label}</b><br>%{value:.1f}%<extra></extra>",
            showlegend=False,
        )
    )
    fig.add_annotation(
        x=0.5, y=0.56, text=f"<b>{numeric_score:.1f}%</b>", showarrow=False,
        font={"family": "Inter, sans-serif", "size": 40, "color": "#F8FAFC"},
    )
    fig.add_annotation(
        x=0.5, y=0.40, text="ÍNDICE GERAL", showarrow=False,
        font={"family": "Inter, sans-serif", "size": 11, "color": "#94A3B8"},
    )
    fig.update_layout(
        autosize=True,
        height=height,
        margin={"l": 8, "r": 8, "t": 12, "b": 12},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Inter, sans-serif", "color": "#F1F5F9"},
        showlegend=False,
        separators=",.",
        hoverlabel={
            "bgcolor": "#1E0B3A",
            "bordercolor": "rgba(96,165,250,0.35)",
            "font": {"family": "Inter, sans-serif", "size": 12, "color": "#F8FAFC"},
        },
        uirevision="health-score-radial-v1054",
    )
    return fig


# ---------------------------------------------------------------------------
# Gauge Chart
# ---------------------------------------------------------------------------

def gauge_chart(
    value: float,
    title: str = "",
    max_val: float = 1.0,
    color: str | None = None,
    height: int = 230,
) -> go.Figure:
    """Gauge/indicator chart for normalized percentage KPIs (0.0 to ``max_val``)."""
    c = color or COLORS["blue"]

    # The dashboard passes normalized values (for example, 0.85 = 85%).
    # Keep the same public API while validating values before building the chart.
    numeric_value = float(value)
    numeric_max = float(max_val)

    if numeric_max <= 0:
        raise ValueError("max_val deve ser maior que zero.")

    numeric_value = max(0.0, min(numeric_value, numeric_max))
    percentage_value = numeric_value * 100
    percentage_max = numeric_max * 100

    indicator_config: dict = dict(
        mode="gauge+number",
        value=percentage_value,

        # ``domain`` belongs to go.Indicator, not to its ``gauge`` object.
        domain=dict(x=[0, 1], y=[0, 1]),

        number=dict(
            suffix="%",
            font=dict(size=34, color="#F1F5F9", family="Inter, sans-serif"),
            valueformat=".1f",
        ),
        gauge=dict(
            axis=dict(
                range=[0, percentage_max],
                tickfont=dict(color="#64748B", size=10),
                ticklen=4,
                tickwidth=1,
                showticklabels=True,
            ),
            bar=dict(
                color=c,
                thickness=0.7,
                line=dict(color="rgba(59, 130, 246, 0.25)", width=1),
            ),
            bgcolor="rgba(17, 24, 39, 0.45)",
            borderwidth=1,
            bordercolor="rgba(59, 130, 246, 0.18)",
            steps=[
                dict(range=[0, percentage_max * 0.33], color="rgba(239, 68, 68, 0.08)"),
                dict(
                    range=[percentage_max * 0.33, percentage_max * 0.66],
                    color="rgba(245, 158, 11, 0.08)",
                ),
                dict(
                    range=[percentage_max * 0.66, percentage_max],
                    color="rgba(16, 185, 129, 0.1)",
                ),
            ],
            threshold=dict(
                line=dict(color="rgba(255,255,255,0.2)", width=0),
                thickness=0.75,
                value=percentage_value,
            ),
        ),
    )

    # Preserve the optional title parameter without forcing an empty title area.
    if title:
        indicator_config["title"] = dict(
            text=title,
            font=dict(size=14, color="#CBD5E1", family="Inter, sans-serif"),
        )

    fig = go.Figure(go.Indicator(**indicator_config))

    fig.update_layout(
        autosize=True,
        height=height,
        margin=dict(l=10, r=10, t=38, b=8),
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color="#F1F5F9"),
    )
    return fig


# ---------------------------------------------------------------------------
# Pareto Chart
# ---------------------------------------------------------------------------

def pareto_chart(
    labels: list[str],
    values: list[int],
    title: str = "",
    height: int = 420,
) -> go.Figure:
    """Pareto chart with cleaner spacing, wrapped labels and fixed presentation layout."""
    if not labels or not values:
        return _empty_figure(title, height)

    sorted_pairs = sorted(zip(values, labels), reverse=True)
    sorted_values = [p[0] for p in sorted_pairs]
    original_labels = [str(p[1]) for p in sorted_pairs]
    wrapped_labels = [_wrap_axis_label(label, 18) for label in original_labels]

    total = sum(sorted_values)
    cumulative: list[float] = []
    running = 0
    for value in sorted_values:
        running += value
        cumulative.append((running / total) * 100 if total > 0 else 0)

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=wrapped_labels,
        y=sorted_values,
        customdata=original_labels,
        marker=dict(color=COLORS["blue"], cornerradius=6),
        name="Valor",
        text=[f"{value:,.0f}" for value in sorted_values],
        textposition="outside",
        textfont=dict(color="#F8FBFF", size=11),
        cliponaxis=False,
        hovertemplate="<b>%{customdata}</b><br>Valor: %{y:,.0f}<extra></extra>",
    ))

    fig.add_trace(go.Scatter(
        x=wrapped_labels,
        y=cumulative,
        customdata=original_labels,
        mode="lines+markers",
        name="% acumulado",
        yaxis="y2",
        line=dict(color=COLORS["orange"], width=2.5),
        marker=dict(size=7, color=COLORS["orange"]),
        hovertemplate="<b>%{customdata}</b><br>Acumulado: %{y:.1f}%<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=wrapped_labels,
        y=[80.0] * len(wrapped_labels),
        mode="lines",
        name="Referência 80%",
        yaxis="y2",
        line=dict(color="#A8BCD1", width=1.5, dash="dot"),
        hoverinfo="skip",
    ))

    _apply_layout(fig, title, height)
    fig.update_layout(
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(size=11, color="#D9E6F2"),
            orientation="h",
            yanchor="bottom",
            y=1.08,
            xanchor="left",
            x=0,
        ),
        margin=calculate_plot_margins(
            title_lines=max(1, len(title)//58 + 1),
            legend_rows=estimate_legend_rows(["Valor", "% acumulado", "Referência 80%"], available_chars=46),
            x_label_length=max(map(len, original_labels), default=0),
            outside_labels=True,
        ),
        xaxis={
            **LAYOUT_DEFAULTS["xaxis"],
            "automargin": True,
            "fixedrange": True,
            "tickfont": {"size": 10, "color": "#D9E6F2"},
            "tickangle": -24,
        },
        yaxis={
            **LAYOUT_DEFAULTS["yaxis"],
            "automargin": True,
            "fixedrange": True,
            "tickfont": {"size": 11, "color": "#D9E6F2"},
        },
        yaxis2=dict(
            overlaying="y",
            side="right",
            range=[0, 105],
            gridcolor="rgba(0,0,0,0)",
            tickfont=dict(color=COLORS["orange"], size=11),
            ticksuffix="%",
            fixedrange=True,
        ),
        showlegend=True,
    )
    return fig


# ---------------------------------------------------------------------------
# Power BI-style analytical charts
# ---------------------------------------------------------------------------

def bullet_chart(
    value: float,
    target: float,
    title: str,
    *,
    max_value: float = 100.0,
    lower_is_better: bool = False,
    height: int = 190,
    value_suffix: str = "%",
) -> go.Figure:
    """Bullet chart roxo — título completo, sem corte de texto (fix Periódicos)."""
    value = float(value)
    target = float(target)
    max_value = max(float(max_value), value, target, 1.0)

    if lower_is_better:
        steps = [
            dict(range=[0, target], color="rgba(124, 58, 237, 0.20)"),
            dict(range=[target, min(max_value, target * 1.35)], color="rgba(217, 70, 239, 0.18)"),
            dict(range=[min(max_value, target * 1.35), max_value], color="rgba(244, 63, 94, 0.15)"),
        ]
        bar_color = "#7C3AED" if value <= target else "#D946EF" if value <= target * 1.35 else "#F43F5E"
    else:
        warning_start = max(0.0, target * 0.75)
        steps = [
            dict(range=[0, warning_start], color="rgba(244, 63, 94, 0.15)"),
            dict(range=[warning_start, target], color="rgba(217, 70, 239, 0.18)"),
            dict(range=[target, max_value], color="rgba(124, 58, 237, 0.20)"),
        ]
        bar_color = "#7C3AED" if value >= target else "#D946EF" if value >= warning_start else "#F43F5E"

    display_title = str(title or "").strip()
    # Never hard-clip short operational labels like "Periódicos — Junho"
    if len(display_title) > 52:
        display_title = display_title[:30] + "…" + display_title[-18:]

    title_len = max(len(display_title), 14)
    left_margin = min(240, max(120, int(title_len * 7.5)))

    fig = go.Figure(go.Indicator(
        mode="number+gauge",
        value=value,
        number={
            "suffix": value_suffix,
            "valueformat": ".1f",
            "font": {"size": 18, "color": "#FFFFFF", "family": "Inter, sans-serif"},
        },
        title={"text": ""},  # annotation below avoids left clipping
        gauge={
            "shape": "bullet",
            "axis": {
                "range": [0, max_value],
                "tickfont": {"size": 10, "color": "#A78BFA"},
                "tickwidth": 1,
                "dtick": 20 if max_value <= 100 else None,
            },
            "bar": {"color": bar_color, "thickness": 0.55},
            "steps": steps,
            "threshold": {
                "line": {"color": "#FFFFFF", "width": 2.0},
                "thickness": 0.80,
                "value": target,
            },
            "bgcolor": "rgba(15, 10, 31, 0.55)",
            "borderwidth": 0,
        },
        domain={"x": [0.02, 0.98], "y": [0.28, 0.78]},
    ))
    fig.update_layout(
        height=height,
        margin=dict(l=left_margin, r=70, t=28, b=28),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color="#E9D5FF"),
        autosize=True,
        annotations=[
            dict(
                text=display_title,
                x=0.0,
                y=0.52,
                xref="paper",
                yref="paper",
                xanchor="right",
                yanchor="middle",
                xshift=-12,
                showarrow=False,
                align="right",
                font=dict(size=12, color="#E2E8F0", family="Inter, sans-serif"),
            )
        ],
    )
    return fig


def enhanced_time_series_chart(
    df: pd.DataFrame,
    *,
    x: str,
    y: str,
    title: str,
    color: str | None = None,
    moving_average: int = 3,
    target: float | None = None,
    target_label: str = "Meta",
    forecast_labels: list[str] | None = None,
    forecast_values: list[float] | None = None,
    forecast_lower: list[float] | None = None,
    forecast_upper: list[float] | None = None,
    milestones: list[object] | None = None,
    height: int = 410,
    value_suffix: str = "",
) -> go.Figure:
    """Time series with previous-period tooltips, moving average and forecast band."""
    c = color or COLORS["blue"]
    working = df[[x, y]].copy()
    working[y] = pd.to_numeric(working[y], errors="coerce").fillna(0.0)
    working["Anterior"] = working[y].shift(1)
    working["Variação"] = ((working[y] - working["Anterior"]) / working["Anterior"] * 100).replace([float("inf"), -float("inf")], 0).fillna(0)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=working[x],
        y=working[y],
        mode="lines+markers",
        name=y,
        line=dict(color=c, width=3, shape="spline"),
        marker=dict(size=8, color=c, line=dict(width=1.5, color="#0B0F19")),
        customdata=working[["Anterior", "Variação"]],
        hovertemplate=(
            f"<b>{y}</b><br>Período: %{{x}}<br>Valor observado: %{{y:,.1f}}{value_suffix}"
            f"<br>Mês anterior: %{{customdata[0]:,.1f}}{value_suffix}"
            "<br>Variação mensal: %{customdata[1]:+.1f}%<extra></extra>"
        ),
    ))

    if moving_average > 1 and len(working) >= moving_average:
        ma = working[y].rolling(moving_average).mean()
        fig.add_trace(go.Scatter(
            x=working[x], y=ma,
            mode="lines", name=f"Média móvel ({moving_average})",
            line=dict(color="#94A3B8", width=2, dash="dot", shape="spline"),
            hovertemplate=f"<b>Média móvel</b><br>%{{x}}: %{{y:,.1f}}{value_suffix}<extra></extra>",
        ))

    if target is not None:
        fig.add_hline(
            y=float(target), line_dash="dash", line_width=2, line_color=COLORS["orange"],
            annotation_text=f"{target_label}: {target:,.1f}{value_suffix}",
            annotation_position="top left",
            annotation_font_color=COLORS["orange"],
        )

    if milestones:
        milestone_x: list[str] = []
        milestone_y: list[float] = []
        milestone_custom: list[tuple[str, str]] = []
        values_by_period = {str(period): float(value) for period, value in zip(working[x], working[y])}
        for milestone in milestones:
            month = str(getattr(milestone, "month", ""))
            if month not in values_by_period:
                continue
            milestone_x.append(month)
            milestone_y.append(values_by_period[month])
            milestone_custom.append((str(getattr(milestone, "title", "Marco")), (" ".join(str(getattr(milestone, "description", "")).split())[:82] + ("…" if len(" ".join(str(getattr(milestone, "description", "")).split())) > 82 else ""))))
        if milestone_x:
            fig.add_trace(go.Scatter(
                x=milestone_x,
                y=milestone_y,
                mode="markers",
                name="Marcos",
                marker=dict(symbol="diamond", size=11, color=COLORS["orange"], line=dict(width=1, color="#F8FBFF")),
                customdata=milestone_custom,
                hovertemplate=(
                    "<b>%{customdata[0]}</b><br>Período: %{x}<br>%{customdata[1]}"
                    "<extra></extra>"
                ),
            ))

    if forecast_labels and forecast_values:
        has_interval = (
            forecast_lower
            and forecast_upper
            and len(forecast_lower) == len(forecast_labels) == len(forecast_upper)
        )
        if has_interval:
            band_x = list(forecast_labels) + list(reversed(forecast_labels))
            band_y = list(forecast_upper) + list(reversed(forecast_lower))
            fig.add_trace(go.Scatter(
                x=band_x, y=band_y, fill="toself",
                fillcolor=f"rgba({_hex_to_rgb(c)}, 0.12)",
                line=dict(color="rgba(0,0,0,0)"),
                hoverinfo="skip", showlegend=True, name="Intervalo estimado",
            ))

        projection_customdata = None
        projection_hover = f"<b>Projeção</b><br>Período: %{{x}}<br>Estimativa: %{{y:,.1f}}{value_suffix}"
        if has_interval:
            projection_customdata = list(zip(forecast_lower, forecast_upper))
            projection_hover += (
                f"<br>Faixa inferior: %{{customdata[0]:,.1f}}{value_suffix}"
                f"<br>Faixa superior: %{{customdata[1]:,.1f}}{value_suffix}"
            )
        projection_hover += "<extra></extra>"

        fig.add_trace(go.Scatter(
            x=forecast_labels, y=forecast_values,
            mode="lines+markers", name="Projeção",
            line=dict(color=c, width=2.5, dash="dash"),
            marker=dict(size=8, symbol="circle-open", color=c, line=dict(width=1.6, color=c)),
            customdata=projection_customdata,
            hovertemplate=projection_hover,
        ))

    _apply_layout(fig, title, height)
    fig.update_layout(
        hovermode="closest",
        hoverdistance=30,
        spikedistance=30,
        legend=get_legend_config(
            item_count=len([trace for trace in fig.data if trace.showlegend is not False]),
            max_label_length=max((len(str(trace.name or "")) for trace in fig.data), default=0),
            legend_rows=estimate_legend_rows([str(trace.name or "") for trace in fig.data]),
            chart_type="time",
        ),
        margin=calculate_plot_margins(
            title_lines=max(1, len(title)//58 + 1),
            legend_rows=estimate_legend_rows([str(trace.name or "") for trace in fig.data]),
            x_label_length=max((len(str(value)) for value in working[x]), default=0),
        ),
    )
    fig.update_xaxes(
        showspikes=True,
        spikecolor="rgba(168, 188, 209, 0.42)",
        spikethickness=1,
        spikedash="dot",
        spikemode="across",
        spikesnap="cursor",
    )
    return fig


def percent_stacked_bar_chart(
    data_dict: dict[str, list[float]],
    categories: list[str],
    title: str,
    *,
    colors: list[str] | None = None,
    height: int = 390,
) -> go.Figure:
    """Responsive 100% stacked composition chart with a notebook-safe legend."""
    colors = colors or PALETTE
    full_names = list(data_dict.keys())
    if not full_names or not categories:
        return _empty_figure(title, height)

    matrix = pd.DataFrame(data_dict, index=categories).fillna(0.0)
    totals = matrix.sum(axis=1).replace(0, 1)
    percentages = matrix.div(totals, axis=0) * 100

    compact_names = {
        "Atendimento Fisioterapêutico Total": "Fisioterapia total",
        "Atendimento Fisioterapêutico Horista": "Fisio. horista",
        "Atendimento Fisioterapêutico Mensalista": "Fisio. mensalista",
        "CAT (Comunicado de Acidente de Trabalho)": "CAT",
        "Saídas de Ambulância (Urgência/Emergência)": "Saídas ambulância",
        "Retorno ao Trabalho": "Retorno",
        "Exames Complementares": "Complementares",
    }
    visual_names = [compact_names.get(name, name) for name in full_names]
    legend_rows = estimate_legend_rows(visual_names, available_chars=52)
    safe_height = calculate_chart_height(
        "composition", category_count=len(categories), series_count=len(full_names),
        legend_rows=legend_rows, requested=max(height, 450),
    )

    fig = go.Figure()
    for index, (full_name, visual_name) in enumerate(zip(full_names, visual_names)):
        values = matrix[full_name].tolist()
        pct = percentages[full_name].tolist()
        fig.add_trace(go.Bar(
            x=compact_month_labels(categories),
            y=pct,
            name=visual_name,
            legendgroup=full_name,
            marker=dict(color=colors[index % len(colors)], cornerradius=3),
            customdata=list(zip(values, pct, [full_name] * len(values))),
            hovertemplate=(
                "<b>%{customdata[2]}</b><br>Período: %{x}<br>Valor: %{customdata[0]:,.0f}"
                "<br>Participação: %{customdata[1]:.1f}%<extra></extra>"
            ),
        ))

    _apply_layout(fig, title, safe_height)
    fig.update_layout(
        barmode="stack",
        barnorm=None,
        bargap=.22,
        legend=get_legend_config(
            item_count=len(full_names),
            max_label_length=max(map(len, visual_names), default=0),
            legend_rows=legend_rows,
            chart_type="composition",
        ),
        margin=calculate_plot_margins(
            title_lines=max(1, len(title)//58 + 1),
            legend_rows=legend_rows,
            x_label_length=max(map(len, map(str, categories)), default=0),
        ),
    )
    fig.update_xaxes(
        tickmode="array", tickvals=compact_month_labels(categories),
        ticktext=compact_month_labels(categories), tickangle=0, automargin=True, fixedrange=True,
    )
    fig.update_yaxes(range=[0, 100], ticksuffix="%", automargin=True, fixedrange=True)
    return fig


def ranking_bar_chart(
    frame: pd.DataFrame,
    *,
    label_col: str,
    value_col: str,
    title: str,
    previous_col: str | None = None,
    share_col: str | None = None,
    colors_by_label: dict[str, str] | None = None,
    height: int = 350,
    value_suffix: str = "",
) -> go.Figure:
    """Horizontal ranking with share and variation in the tooltip."""
    if frame.empty:
        return _empty_figure(title, height)
    height = min(540, max(height, 180 + len(frame) * 38))
    work = frame.sort_values(value_col, ascending=True).copy()
    labels = work[label_col].astype(str).tolist()
    values = work[value_col].astype(float).tolist()
    previous = work[previous_col].astype(float).tolist() if previous_col and previous_col in work else [0.0] * len(work)
    shares = work[share_col].astype(float).tolist() if share_col and share_col in work else [0.0] * len(work)
    variations = [((value - prev) / prev * 100) if prev else 0.0 for value, prev in zip(values, previous)]
    bar_colors = [
        (colors_by_label or UNIT_COLORS).get(label, COLORS["blue"])
        for label in labels
    ]

    fig = go.Figure(go.Bar(
        y=labels, x=values, orientation="h",
        marker=dict(color=bar_colors, cornerradius=6),
        text=[f"{value:,.0f}{value_suffix}" for value in values],
        textposition="outside",
        customdata=list(zip(previous, variations, shares)),
        hovertemplate=(
            "<b>%{y}</b><br>Valor: %{x:,.1f}" + value_suffix +
            "<br>Anterior: %{customdata[0]:,.1f}"
            "<br>Variação: %{customdata[1]:+.1f}%"
            "<br>Participação: %{customdata[2]:.1f}%<extra></extra>"
        ),
    ))
    _apply_layout(fig, title, height)
    fig.update_layout(margin=dict(l=70, r=70, t=65, b=40), showlegend=False)
    return fig


def bridge_waterfall_chart(
    previous_total: float,
    contributions: pd.DataFrame,
    current_total: float,
    *,
    title: str,
    label_col: str = "Unidade",
    contribution_col: str = "Contribuição",
    height: int = 370,
) -> go.Figure:
    """Waterfall explaining which units drove the month-over-month change."""
    labels = ["Mês anterior"] + contributions[label_col].astype(str).tolist() + ["Mês atual"]
    values = [float(previous_total)] + contributions[contribution_col].astype(float).tolist() + [float(current_total)]
    measures = ["absolute"] + ["relative"] * len(contributions) + ["total"]
    text = [f"{previous_total:,.0f}"] + [f"{value:+,.0f}" for value in contributions[contribution_col]] + [f"{current_total:,.0f}"]

    fig = go.Figure(go.Waterfall(
        x=labels, y=values, measure=measures,
        text=text, textposition="outside",
        increasing=dict(marker=dict(color=COLORS["red"])),
        decreasing=dict(marker=dict(color=COLORS["green"])),
        totals=dict(marker=dict(color=COLORS["blue"])),
        connector=dict(line=dict(color="rgba(148,163,184,0.35)")),
        hovertemplate="<b>%{x}</b><br>Impacto: %{y:+,.0f}<extra></extra>",
    ))
    return _apply_layout(fig, title, height)


def matrix_heatmap(
    frame: pd.DataFrame,
    *,
    row_col: str,
    month_cols: list[str],
    title: str,
    height: int = 340,
) -> go.Figure:
    """Power BI-like matrix heatmap from a row label and month columns."""
    if frame.empty or not month_cols:
        return _empty_figure(title, height)
    height = min(520, max(height, 170 + len(frame) * 42))
    z = frame[month_cols].astype(float).values.tolist()
    y = frame[row_col].astype(str).tolist()
    return heatmap(z=z, x=month_cols, y=y, title=title, height=height)


# ============================================================================
# ALTAIR CHART HELPERS (Exploration of modern declarative viz)
# ============================================================================

def _altair_dark_theme() -> dict:
    """Return a dark executive theme config for Altair charts."""
    return {
        "background": "#111827",
        "title": {"fontSize": 15, "fontWeight": 600, "color": "#F8FBFF", "anchor": "start"},
        "axis": {
            "labelColor": "#94A3B8",
            "titleColor": "#CBD5E1",
            "gridColor": "rgba(124, 58, 237, 0.16)",
            "domainColor": "rgba(124, 58, 237, 0.35)",
            "tickColor": "rgba(124, 58, 237, 0.30)",
        },
        "legend": {
            "labelColor": "#CBD5E1",
            "titleColor": "#F1F5F9",
            "symbolType": "circle",
        },
        "view": {"stroke": "transparent"},
        "range": {
            "category": ["#7C3AED", "#10B981", "#0EA5E9", "#F97316", "#A855F7", "#EC4899"],
            "ordinal": ["#7C3AED", "#10B981", "#0EA5E9", "#F97316", "#A855F7"],
        },
    }


def altair_interactive_grouped_bar(
    df: pd.DataFrame,
    *,
    x_col: str,
    y_col: str,
    color_col: str | None = None,
    title: str = "",
    subtitle: str = "",
    height: int = 380,
    interactive: bool = True,
) -> "alt.Chart | None":
    """Modern interactive grouped/stacked bar chart with Altair.

    Excellent for category comparisons with built-in tooltips, legend selection,
    and smooth interactions. Complements the Plotly versions.
    """
    if not ALTAIR_AVAILABLE or df.empty:
        return None

    chart = (
        alt.Chart(df)
        .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4, opacity=0.92)
        .encode(
            x=alt.X(f"{x_col}:N", title=x_col.replace("_", " ").title(), sort="-y"),
            y=alt.Y(f"{y_col}:Q", title=y_col.replace("_", " ").title()),
            color=alt.Color(f"{color_col}:N", title=color_col.replace("_", " ").title()) if color_col else alt.value("#7C3AED"),
            tooltip=[
                alt.Tooltip(f"{x_col}:N", title=x_col),
                alt.Tooltip(f"{y_col}:Q", title=y_col, format=",.1f"),
                alt.Tooltip(f"{color_col}:N", title=color_col) if color_col else alt.Tooltip(),
            ],
        )
        .properties(
            title=title,
            height=height,
            width="container",
        )
        .configure(**_altair_dark_theme())
    )

    if interactive:
        chart = chart.interactive()  # zoom/pan + tooltips

    if subtitle:
        # Altair title can be rich text, but we keep simple; subtitle can be added in app layer
        pass

    return chart


def altair_correlation_heatmap(
    df: pd.DataFrame,
    *,
    numeric_cols: list[str] | None = None,
    title: str = "Correlação entre Métricas",
    height: int = 420,
) -> "alt.Chart | None":
    """Beautiful interactive correlation heatmap with Altair.

    Great for executive overview of relationships between KPIs.
    Uses Pearson correlation and nice diverging palette.
    """
    if not ALTAIR_AVAILABLE or df.empty:
        return None

    if numeric_cols is None:
        numeric_cols = df.select_dtypes(include="number").columns.tolist()[:12]

    if len(numeric_cols) < 2:
        return None

    corr_df = df[numeric_cols].corr().reset_index().melt("index")
    corr_df.columns = ["var1", "var2", "correlation"]

    chart = (
        alt.Chart(corr_df)
        .mark_rect(cornerRadius=3)
        .encode(
            x=alt.X("var1:N", title="Variável", sort=numeric_cols),
            y=alt.Y("var2:N", title="Variável", sort=numeric_cols),
            color=alt.Color(
                "correlation:Q",
                scale=alt.Scale(scheme="blueorange", domain=[-1, 1]),
                title="Correlação (Pearson)",
            ),
            tooltip=[
                alt.Tooltip("var1:N", title="Variável 1"),
                alt.Tooltip("var2:N", title="Variável 2"),
                alt.Tooltip("correlation:Q", title="Correlação", format=".2f"),
            ],
        )
        .properties(title=title, height=height, width="container")
        .configure(**_altair_dark_theme())
        .interactive()
    )
    return chart


def altair_interactive_line(
    df: pd.DataFrame,
    *,
    x_col: str,
    y_col: str,
    color_col: str | None = None,
    title: str = "",
    height: int = 380,
) -> "alt.Chart | None":
    """Interactive line chart with Altair (great for time series trends)."""
    if not ALTAIR_AVAILABLE or df.empty:
        return None

    base = alt.Chart(df).mark_line(point=True, strokeWidth=2.5)

    encoding = {
        "x": alt.X(f"{x_col}:N", title=x_col),
        "y": alt.Y(f"{y_col}:Q", title=y_col),
        "tooltip": [x_col, y_col]
    }

    if color_col and color_col in df.columns:
        encoding["color"] = alt.Color(f"{color_col}:N")

    chart = (
        base.encode(**encoding)
        .properties(title=title or f"{y_col} por {x_col}", height=height)
        .interactive()
    )

    return chart
