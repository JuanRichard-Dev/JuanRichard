"""
Charts Module — Dashboard SM CGR 2026
=======================================
Plotly chart factory functions with premium dark theme styling.
Each function returns a configured ``go.Figure`` ready for ``st.plotly_chart``.
"""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go

from src.config import COLORS, PALETTE, UNIT_COLORS, UI_COLORS
from src.responsive import (
    calculate_chart_height,
    calculate_plot_margins,
    compact_month_labels,
    estimate_legend_rows,
    get_legend_config,
    infer_category_count,
)

# ---------------------------------------------------------------------------
# Shared Layout Defaults
# ---------------------------------------------------------------------------

LAYOUT_DEFAULTS: dict = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(
        family='Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
        color=UI_COLORS["text_secondary"],
        size=13,
    ),
    margin=dict(l=55, r=34, t=66, b=62),
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        borderwidth=0,
        font=dict(size=12, color=UI_COLORS["text_secondary"]),
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="left",
        x=0.0,
        tracegroupgap=8,
    ),
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        tickfont=dict(size=12, color=UI_COLORS["text_muted"]),
        linecolor="rgba(148,163,184,0.15)",
        tickcolor="rgba(148,163,184,0.18)",
        automargin=True,
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor=UI_COLORS["grid"],
        gridwidth=1,
        zeroline=False,
        nticks=5,
        tickfont=dict(size=12, color=UI_COLORS["text_muted"]),
        linecolor="rgba(148,163,184,0.08)",
        tickcolor="rgba(148,163,184,0.18)",
        automargin=True,
    ),
    separators=",.",
    hoverlabel=dict(
        bgcolor=UI_COLORS["card_hover"],
        font_size=13,
        font_family='Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif',
        font_color=UI_COLORS["text"],
        bordercolor=UI_COLORS["border"],
        align="left",
        namelength=-1,
    ),
    height=400,
    colorway=PALETTE,
)



def _format_percent_pt(value: object, *, signed: bool = True) -> str:
    """Format a percentage for UI/hover with one decimal and pt-BR decimal comma."""
    try:
        number = float(value)
    except (TypeError, ValueError):
        return "—"
    if pd.isna(number):
        return "—"
    prefix = "+" if signed and number > 0 else ""
    return f"{prefix}{number:.1f}%".replace(".", ",")


def _format_number_pt(value: object, *, decimals: int = 0, suffix: str = "") -> str:
    """Format numeric hover text without leaking floating-point precision."""
    try:
        number = float(value)
    except (TypeError, ValueError):
        return "—"
    if pd.isna(number):
        return "—"
    rendered = f"{number:,.{max(0, decimals)}f}"
    rendered = rendered.replace(",", "__THOUSAND__").replace(".", ",").replace("__THOUSAND__", ".")
    return f"{rendered}{suffix}"


def _contrast_text_color(hex_color: str) -> str:
    """Choose light/dark in-bar text from the actual bar color luminance."""
    value = str(hex_color or "").strip().lstrip("#")
    if len(value) != 6:
        return UI_COLORS["text"]
    try:
        r, g, b = (int(value[i:i+2], 16) / 255.0 for i in (0, 2, 4))
    except ValueError:
        return UI_COLORS["text"]
    def linear(channel: float) -> float:
        return channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4
    luminance = 0.2126 * linear(r) + 0.7152 * linear(g) + 0.0722 * linear(b)
    return "#09111F" if luminance >= 0.52 else "#F8FAFC"


# Marker shapes cycled across multi-series line charts so each series is
# distinguishable by outline, not only by color — helps colorblind readers
# and printed/grayscale views where two nearby hues (e.g. two blues) read
# as identical.
_MARKER_SYMBOLS = ["circle", "diamond", "square", "triangle-up", "star"]


def _direct_end_labels_safe(df: pd.DataFrame, y_cols: list[str]) -> bool:
    """Avoid end-label collisions when last values are visually too close."""
    valid = [col for col in y_cols if col in df.columns]
    if len(valid) <= 1 or df.empty:
        return True
    numeric = df[valid].apply(pd.to_numeric, errors="coerce")
    values = numeric.to_numpy(dtype=float)
    finite = values[pd.notna(values)]
    if finite.size == 0:
        return True
    data_min = float(finite.min())
    data_max = float(finite.max())
    span = max(abs(data_max - data_min), abs(data_max) * 0.10, 1.0)
    last = [float(numeric[col].fillna(0.0).iloc[-1]) for col in valid]
    threshold = span * 0.075
    return all(abs(a - b) >= threshold for i, a in enumerate(last) for b in last[i + 1:])

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
    legend_rows = estimate_legend_rows(series_names, available_chars=48) if len(series_names) > 1 else 0

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
        "transition": {"duration": 260, "easing": "cubic-in-out"},
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
        font=dict(size=13, color=UI_COLORS["text_muted"]),
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
    value_suffix: str = "",
    direct_labels: bool = True,
) -> go.Figure:
    """Executive multi-series trend chart with unified hover and end labels."""
    if df.empty or not y_cols:
        return _empty_figure(title, height)

    fig = go.Figure()
    colors = colors or PALETTE
    names = names or y_cols
    use_direct_labels = bool(direct_labels and len(y_cols) <= 3 and _direct_end_labels_safe(df, y_cols))

    for idx, col in enumerate(y_cols):
        if col not in df.columns:
            continue
        c = colors[idx % len(colors)]
        values = pd.to_numeric(df[col], errors="coerce").fillna(0.0)
        marker_sizes = [6.0] * max(0, len(values) - 1) + ([9.0] if len(values) else [])
        # Marker shape is a second, color-independent cue distinguishing each
        # series — series 2+ get a distinct symbol (color alone isn't
        # reliable for colorblind readers, and several dashboard palettes
        # cluster in the same hue family). Single-series charts keep the
        # plain circle since there's nothing to disambiguate.
        marker_symbol = _MARKER_SYMBOLS[idx % len(_MARKER_SYMBOLS)] if len(y_cols) > 1 else "circle"
        fig.add_trace(go.Scatter(
            x=df[x],
            y=values,
            name=names[idx],
            showlegend=not use_direct_labels,
            mode="lines+markers",
            line=dict(color=c, width=2.8, shape="linear"),
            marker=dict(
                size=marker_sizes, color=c, symbol=marker_symbol,
                line=dict(width=1.0, color=UI_COLORS["background"]),
            ),
            fill="tozeroy" if fill and len(y_cols) == 1 else None,
            fillcolor=f"rgba({_hex_to_rgb(c)}, 0.14)" if fill and len(y_cols) == 1 else None,
            hovertemplate=(
                f"<b>{names[idx]}</b>: %{{y:,.1f}}{value_suffix}<extra></extra>"
            ),
        ))

        if forecasts and col in forecasts and forecast_x:
            f_vals = forecasts[col]
            fig.add_trace(go.Scatter(
                x=forecast_x,
                y=f_vals,
                name=f"{names[idx]} (Projeção)",
                mode="lines+markers",
                line=dict(color=c, width=2.0, shape="linear", dash="dash"),
                marker=dict(size=6, color=c, symbol="circle-open", line=dict(width=1.5, color=c)),
                hovertemplate=(
                    f"<b>{names[idx]} (Projeção)</b>: %{{y:,.1f}}{value_suffix}<extra></extra>"
                ),
            ))

    _apply_layout(fig, title, height)
    fig.update_layout(hovermode="x unified", hoverdistance=30, showlegend=not use_direct_labels and len(fig.data) > 1)
    fig.update_xaxes(
        showspikes=True,
        spikecolor="rgba(148,163,184,0.24)",
        spikethickness=1,
        spikedash="dot",
        spikemode="across",
        spikesnap="cursor",
    )

    # Direct end labels remove the need to constantly map line colors to legends.
    if use_direct_labels and not df.empty:
        last_x = df[x].iloc[-1]

        # Position labels by actual value proximity instead of a fixed
        # per-series offset. The previous approach (offsets = [-12, 10, 28]
        # keyed only by trace index) could push a lower-value series' label
        # *upward*, straight into the label above it, whenever two series
        # ended close together — exactly what happened with two series
        # ending 28 units apart on a shared axis dominated by a third,
        # much larger series. This estimates each label's pixel position
        # from its real value, then enforces a minimum vertical gap
        # top-to-bottom so labels only ever get pushed apart, never into
        # each other.
        plot_h = float(fig.layout.height or height)
        margin = fig.layout.margin
        top_m = float(margin.t or 60)
        bottom_m = float(margin.b or 50)
        plot_area_h = max(80.0, plot_h - top_m - bottom_m)

        all_vals: list[float] = []
        for col in y_cols:
            if col in df.columns:
                all_vals.extend(pd.to_numeric(df[col], errors="coerce").dropna().tolist())
        axis_min = min(all_vals + [0.0]) if all_vals else 0.0
        axis_max = max(all_vals) if all_vals else 1.0
        pad = max((axis_max - axis_min) * 0.08, 1.0)
        axis_min -= pad
        axis_max += pad
        axis_span = max(axis_max - axis_min, 1e-6)

        def _value_to_px(v: float) -> float:
            # Pixel distance from the top of the plotting area (0 = top).
            return plot_area_h * (1.0 - (v - axis_min) / axis_span)

        label_gap_px = 24.0  # approx. rendered pill height, incl. padding
        entries = []
        for idx, col in enumerate(y_cols):
            if col not in df.columns:
                continue
            value = float(pd.to_numeric(df[col], errors="coerce").fillna(0.0).iloc[-1])
            entries.append({
                "idx": idx, "col": col, "value": value,
                "px": _value_to_px(value), "original_px": _value_to_px(value),
            })

        entries.sort(key=lambda e: e["px"])
        for i in range(1, len(entries)):
            min_px = entries[i - 1]["px"] + label_gap_px
            if entries[i]["px"] < min_px:
                entries[i]["px"] = min_px

        for e in entries:
            idx, col, value = e["idx"], e["col"], e["value"]
            c = colors[idx % len(colors)]
            formatted = f"{value:,.1f}{value_suffix}" if value_suffix else f"{value:,.0f}"
            # yshift is positive-up in Plotly; our px axis increases downward,
            # so a larger adjusted px (pushed down) needs a negative yshift.
            yshift = e["original_px"] - e["px"]
            fig.add_annotation(
                x=last_x, y=value,
                text=f"<b>{names[idx]}</b> · {formatted}",
                showarrow=False,
                xshift=12,
                yshift=yshift,
                xanchor="left",
                bgcolor="rgba(12,22,39,0.86)",
                bordercolor=f"rgba({_hex_to_rgb(c)}, 0.18)",
                borderwidth=1,
                borderpad=4,
                font=dict(size=11.6, color=UI_COLORS["text"]),
            )
        fig.layout.margin.r = max(int(fig.layout.margin.r or 0), 130)
    return fig

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
                f"<b>{names[idx]}</b>: %{{y:,.0f}}<extra></extra>"
            ),
        ))

    _apply_layout(fig, title, height)
    fig.update_layout(hovermode="x unified", hoverdistance=24)
    fig.update_xaxes(unifiedhovertitle=dict(text="<b>%{x}</b>"))
    return fig


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
            textposition="outside",
            cliponaxis=False,
            textfont=dict(color=UI_COLORS["text_secondary"], size=12),
            hovertemplate="<b>%{y}</b><br>Valor: %{x:,.0f}<extra></extra>",
        ))
    else:
        fig = go.Figure(go.Bar(
            x=df[x], y=df[y], orientation="v",
            marker=dict(color=c, line=dict(width=0), cornerradius=6),
            text=df[y].apply(lambda v: f"{v:,.0f}"),
            textposition="outside",
            cliponaxis=False,
            textfont=dict(color=UI_COLORS["text_secondary"], size=12),
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
            hovertemplate=f"<b>{name}</b>: %{{y:,.0f}}<extra></extra>",
        ))

    fig.update_layout(barmode="stack", hovermode="x unified", hoverdistance=24)
    fig.update_xaxes(unifiedhovertitle=dict(text="<b>%{x}</b>"))
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
    """Grouped comparison chart with restrained spacing and direct values."""
    if not data_dict or not categories:
        return _empty_figure(title, height)
    fig = go.Figure()
    colors = colors or PALETTE

    for idx, (name, values) in enumerate(data_dict.items()):
        c = colors[idx % len(colors)]
        fig.add_trace(go.Bar(
            x=compact_month_labels(categories),
            y=values,
            name=name,
            marker=dict(color=c, cornerradius=5),
            text=[f"{v:,.0f}" if float(v) != 0 else "" for v in values],
            textposition="outside",
            cliponaxis=False,
            textfont=dict(size=11.5, color=UI_COLORS["text_secondary"]),
            hovertemplate=(f"<b>{name}</b>: %{{y:,.0f}}<extra></extra>"),
        ))

    max_value = max((float(v) for values in data_dict.values() for v in values), default=0.0)
    legend_rows = estimate_legend_rows(data_dict.keys(), available_chars=44)
    safe_height = calculate_chart_height(
        "grouped_bar", category_count=len(categories), series_count=len(data_dict),
        legend_rows=legend_rows, requested=max(height, 390),
    )
    _apply_layout(fig, title, safe_height)
    fig.update_layout(
        barmode="group", bargap=.28, bargroupgap=.10, hovermode="x unified", hoverdistance=24,
        legend=get_legend_config(
            item_count=len(data_dict), max_label_length=max(map(len, data_dict.keys()), default=0),
            legend_rows=legend_rows, chart_type="grouped_bar",
        ),
    )
    if max_value > 0:
        fig.update_yaxes(range=[0, max_value * 1.18], fixedrange=True)
    fig.update_xaxes(tickangle=0, fixedrange=True, unifiedhovertitle=dict(text="<b>%{x}</b>"))
    return fig

def horizontal_bar_chart(
    labels: list[str],
    values: list[int],
    title: str = "",
    colors: list[str] | None = None,
    height: int = 350,
) -> go.Figure:
    """Horizontal bar chart — ideal for comparing named categories."""
    explicit_colors = colors

    # Sort ascending for horizontal bar readability
    sorted_pairs = sorted(zip(values, labels))
    sorted_values = [p[0] for p in sorted_pairs]
    sorted_labels = [p[1] for p in sorted_pairs]
    bar_colors = ([explicit_colors[i % len(explicit_colors)] for i in range(len(sorted_labels))]
                  if explicit_colors else [COLORS["blue"]] * len(sorted_labels))

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
        textposition="outside",
        cliponaxis=False,
        textfont=dict(color=UI_COLORS["text_secondary"], size=12),
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
            line=dict(color=UI_COLORS["background"], width=2),
        ),
        textfont=dict(size=12, color=UI_COLORS["text_secondary"]),
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
            "<span style='font-size:11px;color:#94A3B8'>Total</span>"
        ),
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=19, color=UI_COLORS["text"]),
    )

    legend_rows = estimate_legend_rows(labels, available_chars=42) if len(labels) > 1 else 0
    safe_height = calculate_chart_height(
        "donut", category_count=len(labels), legend_rows=legend_rows, requested=height
    )
    _apply_layout(fig, title, safe_height)
    fig.update_layout(
        showlegend=True,
        margin=dict(l=20, r=20, t=44, b=max(28, 18 + legend_rows * 22)),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.05,
            xanchor="center",
            x=0.5,
            font=dict(size=11.5 if len(labels) > 4 else 12, color=UI_COLORS["text_secondary"]),
        ),
        hovermode="closest",
    )
    return fig


# ---------------------------------------------------------------------------
# Share Bar
# ---------------------------------------------------------------------------

def share_bar_chart(
    values: dict[str, float],
    title: str = "",
    *,
    colors: list[str] | None = None,
    height: int = 250,
    value_suffix: str = "",
) -> go.Figure:
    """Single 100% horizontal composition bar for an immediate part-to-whole read."""
    clean = {str(k): max(0.0, float(v)) for k, v in values.items() if float(v) >= 0}
    total = sum(clean.values())
    if not clean or total <= 0:
        return _empty_figure(title, height)
    colors = colors or PALETTE
    fig = go.Figure()
    for idx, (name, value) in enumerate(clean.items()):
        share = value / total * 100.0
        label = f"{name} · {share:.0f}%" if share >= 16 else (f"{share:.0f}%" if share >= 8 else "")
        fig.add_trace(go.Bar(
            y=["Composição"],
            x=[share],
            orientation="h",
            name=name,
            marker=dict(color=colors[idx % len(colors)], cornerradius=5),
            text=[label],
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(size=12, color=_contrast_text_color(colors[idx % len(colors)])),
            customdata=[[value, share]],
            hovertemplate=(
                f"<b>{name}</b>: %{{customdata[0]:,.0f}}{value_suffix} · %{{customdata[1]:.1f}}%<extra></extra>"
            ),
        ))
    legend_rows = estimate_legend_rows(clean.keys(), available_chars=42) if len(clean) > 1 else 0
    safe_height = max(height, 220 + max(0, legend_rows - 1) * 22)
    _apply_layout(fig, title, safe_height)
    fig.update_layout(
        barmode="stack",
        bargap=.48,
        hovermode="y unified",
        hoverdistance=24,
        showlegend=True,
        margin=dict(l=18, r=18, t=44, b=max(52, 34 + legend_rows * 20)),
        legend=dict(
            orientation="h", yanchor="top", y=-0.12, xanchor="left", x=0,
            font=dict(size=11.2, color=UI_COLORS["text_secondary"]),
        ),
        uniformtext_minsize=10,
        uniformtext_mode="hide",
    )
    fig.update_xaxes(range=[0, 100], showgrid=False, showticklabels=False, zeroline=False, fixedrange=True)
    fig.update_yaxes(showgrid=False, showticklabels=False, fixedrange=True, unifiedhovertitle=dict(text="<b>Composição</b>"))
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
    """Compact annotated heatmap: numbers remain primary, color is secondary."""
    if not z or not x or not y:
        return _empty_figure(title, height)
    fig = go.Figure(go.Heatmap(
        z=z,
        x=compact_month_labels(x),
        y=y,
        colorscale=[
            [0.00, "#111C2E"],
            [0.22, "#17325B"],
            [0.48, "#2F6FE4"],
            [0.72, "#7C8CF8"],
            [1.00, "#B49AF7"],
        ],
        text=[[f"{v:,.0f}" for v in row] for row in z],
        texttemplate="<b>%{text}</b>",
        textfont=dict(size=12.5, color="#F8FAFC"),
        hovertemplate="<b>%{y}</b><br>Período: %{x}<br>Valor: %{z:,.0f}<extra></extra>",
        showscale=False,
        xgap=3,
        ygap=3,
    ))
    _apply_layout(fig, title, height)
    fig.update_xaxes(showgrid=False, tickangle=0)
    fig.update_yaxes(showgrid=False)
    return fig

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
        increasing=dict(marker=dict(color=COLORS["orange"], line=dict(width=0))),
        decreasing=dict(marker=dict(color=COLORS["gray"], line=dict(width=0))),
        totals=dict(marker=dict(color=COLORS["blue"], line=dict(width=0))),
        connector=dict(line=dict(color="rgba(148,163,184,0.28)", width=1)),
        textposition="outside",
        cliponaxis=False,
        textfont=dict(size=12, color=UI_COLORS["text"]),
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
                tickfont=dict(color=UI_COLORS["text_muted"], size=11),
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
                dict(range=[0, percentage_max], color="rgba(148, 163, 184, 0.08)"),
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
    if len(sorted_pairs) > 6:
        top_pairs = sorted_pairs[:5]
        remaining_total = sum(value for value, _ in sorted_pairs[5:])
        sorted_pairs = top_pairs + [(remaining_total, "Outros")]
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
        textfont=dict(color=UI_COLORS["text"], size=12),
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

    _apply_layout(fig, title, height)
    fig.update_layout(
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(size=12, color=UI_COLORS["text_secondary"]),
            orientation="h",
            yanchor="bottom",
            y=1.08,
            xanchor="left",
            x=0,
        ),
        margin=calculate_plot_margins(
            title_lines=max(1, len(title)//58 + 1),
            legend_rows=estimate_legend_rows(["Valor", "% acumulado"], available_chars=46),
            x_label_length=max(map(len, original_labels), default=0),
            outside_labels=True,
        ),
        xaxis={
            **LAYOUT_DEFAULTS["xaxis"],
            "automargin": True,
            "fixedrange": True,
            "tickfont": {"size": 12, "color": UI_COLORS["text_muted"]},
            "tickangle": -24,
        },
        yaxis={
            **LAYOUT_DEFAULTS["yaxis"],
            "automargin": True,
            "fixedrange": True,
            "tickfont": {"size": 12, "color": UI_COLORS["text_muted"]},
        },
        yaxis2=dict(
            overlaying="y",
            side="right",
            range=[0, 105],
            gridcolor="rgba(0,0,0,0)",
            tickfont=dict(color=COLORS["orange"], size=12),
            ticksuffix="%",
            fixedrange=True,
        ),
        showlegend=True,
    )
    return fig


# ---------------------------------------------------------------------------
# Power BI-style analytical charts
# ---------------------------------------------------------------------------

def enhanced_time_series_chart(
    df: pd.DataFrame,
    *,
    x: str,
    y: str,
    title: str,
    color: str | None = None,
    moving_average: int = 3,
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
    value_format = ",.1f" if value_suffix else ",.0f"
    working = df[[x, y]].copy()
    working[y] = pd.to_numeric(working[y], errors="coerce").fillna(0.0)
    working["Anterior"] = working[y].shift(1)
    working["Variação"] = ((working[y] - working["Anterior"]) / working["Anterior"] * 100).replace([float("inf"), -float("inf")], 0)
    working["Anterior texto"] = [
        _format_number_pt(value, decimals=1 if value_suffix else 0, suffix=value_suffix) if pd.notna(value) else "—"
        for value in working["Anterior"]
    ]
    working["Variação texto"] = [
        _format_percent_pt(value) if pd.notna(previous) else "—"
        for value, previous in zip(working["Variação"], working["Anterior"])
    ]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=working[x],
        y=working[y],
        mode="lines+markers",
        name=y,
        showlegend=False,
        line=dict(color=c, width=2.8, shape="linear"),
        marker=dict(
            size=[6.5] * max(0, len(working) - 1) + ([9] if len(working) else []),
            color=c,
            line=dict(width=1.2, color=UI_COLORS["background"]),
        ),
        customdata=working[["Anterior texto", "Variação texto"]],
        fill="tozeroy",
        fillcolor=f"rgba({_hex_to_rgb(c)}, 0.16)",
        hovertemplate=(
            f"<b>{y}</b><br>Período: %{{x}}<br>Valor observado: %{{y:{value_format}}}{value_suffix}"
            "<br>Mês anterior: %{customdata[0]}"
            "<br>Variação mensal: %{customdata[1]}<extra></extra>"
        ),
    ))

    if moving_average > 1 and len(working) >= moving_average:
        ma = working[y].rolling(moving_average).mean()
        fig.add_trace(go.Scatter(
            x=working[x], y=ma,
            mode="lines", name=f"Média móvel ({moving_average})",
            line=dict(color=UI_COLORS["text_muted"], width=1.8, dash="dot", shape="linear"),
            hovertemplate=f"<b>Média móvel</b><br>%{{x}}: %{{y:,.1f}}{value_suffix}<extra></extra>",
        ))

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
        hovermode="x unified",
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
        spikecolor="rgba(148, 163, 184, 0.28)",
        spikethickness=1,
        spikedash="dot",
        spikemode="across",
        spikesnap="cursor",
    )
    if not working.empty:
        last_x = working[x].iloc[-1]
        last_y = float(working[y].iloc[-1])
        last_label = f"{last_y:,.1f}{value_suffix}" if value_suffix else f"{last_y:,.0f}"
        fig.add_annotation(
            x=last_x,
            y=last_y,
            text=f"<b>{last_label}</b>",
            showarrow=False,
            xshift=12,
            yshift=12,
            xanchor="left",
            bgcolor=UI_COLORS["card_hover"],
            bordercolor="rgba(148,163,184,0.18)",
            borderwidth=1,
            borderpad=4,
            font=dict(size=12, color=UI_COLORS["text"]),
        )
        fig.layout.margin.r = max(int(fig.layout.margin.r or 0), 78)
    fig.update_yaxes(rangemode="tozero", ticksuffix=value_suffix)
    return fig


def percent_stacked_bar_chart(
    data_dict: dict[str, list[float]],
    categories: list[str],
    title: str,
    *,
    colors: list[str] | None = None,
    height: int = 390,
    top_n: int | None = None,
    other_label: str = "Outros",
) -> go.Figure:
    """100% composition chart with optional Top-N aggregation for simpler reading."""
    colors = colors or PALETTE
    full_names = list(data_dict.keys())
    if not full_names or not categories:
        return _empty_figure(title, height)

    matrix = pd.DataFrame(data_dict, index=categories).fillna(0.0)
    if top_n and len(matrix.columns) > top_n:
        totals_by_series = matrix.sum(axis=0).sort_values(ascending=False)
        keep = totals_by_series.head(top_n).index.tolist()
        drop = [col for col in matrix.columns if col not in keep]
        compact = matrix[keep].copy()
        aggregate_label = other_label if other_label not in keep else "Demais"
        compact[aggregate_label] = matrix[drop].sum(axis=1)
        matrix = compact

    full_names = list(matrix.columns)
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
    legend_rows = estimate_legend_rows(visual_names, available_chars=44)
    safe_height = calculate_chart_height(
        "composition", category_count=len(categories), series_count=len(full_names),
        legend_rows=legend_rows, requested=max(height, 410),
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
            marker=dict(
                color=colors[index % len(colors)],
                line=dict(color="rgba(9,17,31,0.34)", width=0.7),
                cornerradius=2,
            ),
            text=[f"{share:.0f}%" if share >= 13 else "" for share in pct],
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(size=11.5, color=_contrast_text_color(colors[index % len(colors)])),
            customdata=list(zip(values, pct, [visual_name] * len(values))),
            hovertemplate=(
                "<b>%{customdata[2]}</b>: %{customdata[0]:,.0f} · %{customdata[1]:.1f}%<extra></extra>"
            ),
        ))

    _apply_layout(fig, title, safe_height)
    fig.update_layout(
        barmode="stack", bargap=.30,
        hovermode="x unified", hoverdistance=24,
        uniformtext_minsize=10, uniformtext_mode="hide",
        legend=get_legend_config(
            item_count=len(full_names), max_label_length=max(map(len, visual_names), default=0),
            legend_rows=legend_rows, chart_type="composition",
        ),
    )
    fig.update_xaxes(tickangle=0, fixedrange=True, unifiedhovertitle=dict(text="<b>%{x}</b>"))
    fig.update_yaxes(range=[0, 100], ticksuffix="%", dtick=25, fixedrange=True)
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
    default_color: str | None = None,
    height: int = 350,
    value_suffix: str = "",
    decimals: int = 0,
) -> go.Figure:
    """Horizontal ranking optimized for fast comparison and honest tooltips."""
    if frame.empty:
        return _empty_figure(title, height)
    height = min(540, max(height, 175 + len(frame) * 37))
    work = frame.sort_values(value_col, ascending=True).copy()
    labels = work[label_col].astype(str).tolist()
    values = pd.to_numeric(work[value_col], errors="coerce").fillna(0.0).tolist()
    has_previous = bool(previous_col and previous_col in work.columns)
    has_share = bool(share_col and share_col in work.columns)
    previous = pd.to_numeric(work[previous_col], errors="coerce").fillna(0.0).tolist() if has_previous else [0.0] * len(work)
    shares = pd.to_numeric(work[share_col], errors="coerce").fillna(0.0).tolist() if has_share else [0.0] * len(work)
    variations = [((value - prev) / prev * 100) if prev else 0.0 for value, prev in zip(values, previous)]
    variation_text = [_format_percent_pt(value) for value in variations]
    fallback = default_color or COLORS["blue"]
    bar_colors = [(colors_by_label or {}).get(label, fallback) for label in labels]

    value_fmt = f",.{max(0, int(decimals))}f"
    text = []
    for value, share in zip(values, shares):
        base = _format_number_pt(value, decimals=max(0, int(decimals)), suffix=value_suffix)
        share_text = _format_percent_pt(share, signed=False)
        text.append(f"{base} · {share_text}" if has_share else base)

    if has_previous and has_share:
        customdata = list(zip(previous, variation_text, shares))
        hover = (
            f"<b>%{{y}}</b><br>Valor: %{{x:{value_fmt}}}" + value_suffix +
            f"<br>Anterior: %{{customdata[0]:{value_fmt}}}" + value_suffix +
            "<br>Variação: %{customdata[1]}"
            "<br>Participação: %{customdata[2]:.1f}%<extra></extra>"
        )
    elif has_previous:
        customdata = list(zip(previous, variation_text))
        hover = (
            f"<b>%{{y}}</b><br>Valor: %{{x:{value_fmt}}}" + value_suffix +
            f"<br>Anterior: %{{customdata[0]:{value_fmt}}}" + value_suffix +
            "<br>Variação: %{customdata[1]}<extra></extra>"
        )
    elif has_share:
        customdata = list(zip(shares))
        hover = (
            f"<b>%{{y}}</b><br>Valor: %{{x:{value_fmt}}}" + value_suffix +
            "<br>Participação: %{customdata[0]:.1f}%<extra></extra>"
        )
    else:
        customdata = None
        hover = f"<b>%{{y}}</b><br>Valor: %{{x:{value_fmt}}}" + value_suffix + "<extra></extra>"

    fig = go.Figure(go.Bar(
        y=labels, x=values, orientation="h",
        marker=dict(color=bar_colors, cornerradius=6, opacity=.94),
        text=text, textposition="outside",
        textfont=dict(size=12, color=UI_COLORS["text_secondary"]),
        cliponaxis=False,
        customdata=customdata,
        hovertemplate=hover,
    ))
    _apply_layout(fig, title, height)
    fig.update_layout(margin=dict(l=88, r=105, t=52, b=36), showlegend=False, bargap=.28)
    fig.update_xaxes(showgrid=False, showticklabels=False, rangemode="tozero", zeroline=False)
    fig.update_yaxes(showgrid=False)
    return fig

def diverging_bar_chart(
    frame: pd.DataFrame,
    *,
    label_col: str,
    value_col: str,
    title: str,
    colors_by_label: dict[str, str] | None = None,
    default_color: str | None = None,
    height: int = 340,
) -> go.Figure:
    """Signed horizontal bars around zero; ideal for contribution/change analysis."""
    if frame.empty:
        return _empty_figure(title, height)
    work = frame[[label_col, value_col]].copy()
    work[value_col] = pd.to_numeric(work[value_col], errors="coerce").fillna(0.0)
    work = work.sort_values(value_col, ascending=True)
    labels = work[label_col].astype(str).tolist()
    values = work[value_col].astype(float).tolist()
    fallback = default_color or COLORS["orange"]
    colors = [(colors_by_label or {}).get(label, fallback) for label in labels]
    fig = go.Figure(go.Bar(
        y=labels,
        x=values,
        orientation="h",
        marker=dict(color=colors, cornerradius=5),
        text=[f"{value:+,.0f}" for value in values],
        textposition="outside",
        textfont=dict(size=12, color=UI_COLORS["text_secondary"]),
        cliponaxis=False,
        hovertemplate="<b>%{y}</b><br>Contribuição: %{x:+,.0f}<extra></extra>",
    ))
    _apply_layout(fig, title, max(height, 180 + 38 * len(work)))
    fig.add_vline(x=0, line_width=1.2, line_color="rgba(151,166,186,0.34)")
    fig.update_layout(showlegend=False, bargap=.28, margin=dict(l=88, r=72, t=50, b=36))
    fig.update_xaxes(showgrid=True, gridcolor=UI_COLORS["grid"], zeroline=False)
    fig.update_yaxes(showgrid=False)
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
        increasing=dict(marker=dict(color=COLORS["orange"])),
        decreasing=dict(marker=dict(color=COLORS["gray"])),
        totals=dict(marker=dict(color=COLORS["orange"])) ,
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
