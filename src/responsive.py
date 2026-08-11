"""Responsive visual helpers for Streamlit + Plotly.

The dashboard uses a browser-native adaptive profile. CSS media/container
queries react to the real viewport width (notebook, Full HD, QHD and 4K), while
these helpers calculate chart density, heights, margins, legends, hover behavior
and tick labels from the actual figure content. This keeps the Python layer
stable without adding a fragile JavaScript viewport dependency.
"""
from __future__ import annotations

from math import ceil
import html
import re
from typing import Any, Iterable

import plotly.graph_objects as go

MONTH_SHORT = {
    "Janeiro": "Jan", "Fevereiro": "Fev", "Março": "Mar", "Abril": "Abr",
    "Maio": "Mai", "Junho": "Jun", "Julho": "Jul", "Agosto": "Ago",
    "Setembro": "Set", "Outubro": "Out", "Novembro": "Nov", "Dezembro": "Dez",
}


def compact_month_labels(values: Iterable[Any], *, threshold: int = 8) -> list[str]:
    labels = [str(value) for value in values]
    if len(labels) < threshold:
        return labels
    return [MONTH_SHORT.get(label, label[:3]) for label in labels]


def infer_category_count(fig: go.Figure) -> int:
    counts: list[int] = []
    for trace in fig.data:
        for axis in (getattr(trace, "x", None), getattr(trace, "y", None)):
            try:
                counts.append(len(axis))
            except TypeError:
                pass
    return max(counts, default=0)


def calculate_chart_height(
    chart_type: str,
    *,
    category_count: int = 0,
    series_count: int = 1,
    legend_rows: int = 1,
    requested: int | None = None,
) -> int:
    """Return a content-aware height using 1366x768 as the safe baseline."""
    chart_type = chart_type.casefold()
    base = {
        "gauge": 270,
        "time": 410,
        "line": 400,
        "bar": 390,
        "grouped_bar": 430,
        "stacked": 430,
        "composition": 450,
        "pareto": 455,
        "ranking": 350,
        "heatmap": 350,
        "donut": 390,
        "waterfall": 400,
    }.get(chart_type, 390)

    if chart_type in {"ranking", "horizontal_bar"}:
        base = max(base, 150 + category_count * 38)
    elif chart_type in {"pareto", "bar", "grouped_bar", "stacked", "composition"}:
        base += max(0, category_count - 6) * 14
    if chart_type in {"composition", "stacked"}:
        base += max(0, series_count - 4) * 16
    base += max(0, legend_rows - 1) * 24
    if requested is not None:
        base = max(base, requested)
    return int(min(620, max(260, base)))


def estimate_legend_rows(series_names: Iterable[str], *, available_chars: int = 58) -> int:
    names = [str(name) for name in series_names]
    if not names:
        return 0
    total = sum(max(8, len(name) + 4) for name in names)
    return max(1, ceil(total / max(available_chars, 1)))


def get_legend_config(
    *,
    item_count: int,
    max_label_length: int,
    legend_rows: int = 1,
    chart_type: str = "generic",
) -> dict[str, Any]:
    """Notebook-safe horizontal legend positioned above the plotting area."""
    font_size = 12 if item_count <= 5 and max_label_length <= 24 else 11
    y = 1.04 + max(0, legend_rows - 1) * 0.055
    config: dict[str, Any] = {
        "orientation": "h",
        "x": 0,
        "xanchor": "left",
        "y": y,
        "yanchor": "bottom",
        "font": {"size": font_size, "color": "#CBD5E1"},
        "bgcolor": "rgba(0,0,0,0)",
        "borderwidth": 0,
        "traceorder": "normal",
    }
    # Let Plotly wrap legend items using the actual available width. Fixed
    # pixel entry widths look tidy on one monitor but become fragile on
    # notebooks and unnecessarily sparse on QHD/4K displays.
    return config


def _title_line_count(title_text: object, *, wrap_at: int = 52) -> int:
    """Estimate visible Plotly title lines, including HTML line breaks."""
    raw = str(title_text or "").strip()
    if not raw:
        return 0
    normalized = re.sub(r"<br\s*/?>", "\n", raw, flags=re.IGNORECASE)
    normalized = html.unescape(re.sub(r"<[^>]+>", "", normalized))
    visible_lines = [line.strip() for line in normalized.splitlines() if line.strip()] or [normalized]
    return sum(max(1, ceil(len(line) / max(wrap_at, 1))) for line in visible_lines)


def _visible_legend_rows(fig: go.Figure) -> int:
    names = [
        str(getattr(trace, "name", "") or "")
        for trace in fig.data
        if getattr(trace, "showlegend", True) is not False and str(getattr(trace, "name", "") or "").strip()
    ]
    if len(names) <= 1:
        return 0
    legend = fig.layout.legend
    if getattr(legend, "orientation", None) != "h":
        return 0
    return estimate_legend_rows(names)


def calculate_plot_margins(
    *,
    title_lines: int = 1,
    legend_rows: int = 0,
    x_label_length: int = 0,
    y_label_length: int = 0,
    outside_labels: bool = False,
) -> dict[str, int]:
    """Calculate balanced margins without placing titles against the SVG edge."""
    title_space = 0 if title_lines <= 0 else 44 + title_lines * 20
    legend_space = max(0, legend_rows) * 23
    top = max(44, title_space + legend_space)
    bottom = 48 + (22 if x_label_length > 14 else 0)
    left = 44 + min(48, max(0, y_label_length - 7) * 3)
    right = 28 + (42 if outside_labels else 0)
    return {"l": left, "r": right, "t": top, "b": bottom, "pad": 6}


def _choose_hover_mode(fig: go.Figure) -> str:
    """Choose a hover policy that complements labels instead of covering them."""
    traces = list(fig.data)
    if not traces:
        return "closest"
    trace_types = {str(getattr(trace, "type", "") or "") for trace in traces}
    if trace_types & {"heatmap", "pie", "treemap", "funnel", "indicator", "waterfall"}:
        return "closest"

    # Stacked/grouped categorical bars are much easier to inspect with one
    # compact tooltip per category. Horizontal share bars use the y axis.
    if trace_types <= {"bar"} and len(traces) > 1:
        orientations = {str(getattr(trace, "orientation", "v") or "v") for trace in traces}
        return "y unified" if orientations == {"h"} else "x unified"

    # Time-series charts should never spawn multiple overlapping hover boxes.
    if "scatter" in trace_types:
        return "x unified"
    return "closest"


def _protect_trace_labels(fig: go.Figure) -> None:
    """Prevent direct labels from being clipped by the Plotly plotting domain."""
    for trace in fig.data:
        if getattr(trace, "type", None) != "bar":
            continue
        text_position = str(getattr(trace, "textposition", "") or "")
        if text_position in {"outside", "auto"}:
            try:
                trace.cliponaxis = False
            except Exception:
                pass


def apply_figure_safety(fig: go.Figure) -> go.Figure:
    """Apply responsive, accessible and hover-safe safeguards at render time.

    V20 treats the chart as an adaptive component: margins protect direct labels,
    unified hover is used for temporal/stacked comparisons, legends can wrap to
    the actual width, and categorical labels are allowed to trigger automargins.
    """
    title_text = getattr(fig.layout.title, "text", None)
    title_lines = _title_line_count(title_text)
    legend_rows = _visible_legend_rows(fig)

    margin = fig.layout.margin
    existing_l = int(getattr(margin, "l", None) or 0)
    existing_r = int(getattr(margin, "r", None) or 0)
    existing_t = int(getattr(margin, "t", None) or 0)
    existing_b = int(getattr(margin, "b", None) or 0)

    outside_labels = any(
        str(getattr(trace, "textposition", "") or "") in {"outside", "auto"}
        for trace in fig.data
        if getattr(trace, "type", None) == "bar"
    )
    safe_margin = calculate_plot_margins(
        title_lines=title_lines,
        legend_rows=legend_rows,
        x_label_length=0,
        y_label_length=0,
        outside_labels=outside_labels,
    )
    final_margin = {
        "l": max(existing_l, safe_margin["l"]),
        "r": max(existing_r, safe_margin["r"]),
        "t": max(existing_t, safe_margin["t"]),
        "b": max(existing_b, safe_margin["b"]),
        "pad": max(int(getattr(margin, "pad", None) or 0), 6),
    }

    current_hover = str(getattr(fig.layout, "hovermode", "") or "")
    hovermode = current_hover if current_hover and current_hover != "None" else _choose_hover_mode(fig)

    layout_updates: dict[str, Any] = {
        "autosize": True,
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "dragmode": False,
        "margin": final_margin,
        "hovermode": hovermode,
        "hoverdistance": 24,
        "hoverlabel": {
            "bgcolor": "#0D182A",
            "bordercolor": "#33445E",
            "font": {"color": "#F8FAFC", "size": 12},
            "align": "left",
            "namelength": -1,
        },
    }
    # spikedistance is useful for x-unified temporal inspection but can make
    # closest-hover categorical charts feel sticky.
    if hovermode == "x unified":
        layout_updates["spikedistance"] = -1

    if title_lines:
        current_title = fig.layout.title.to_plotly_json()
        current_font = dict(current_title.get("font", {}) or {})
        current_font.setdefault("family", "Inter, sans-serif")
        current_font.setdefault("color", "#F8FBFF")
        current_font["size"] = min(16, max(14, int(current_font.get("size", 15) or 15)))
        current_title.update(
            x=0.015,
            xanchor="left",
            y=0.94,
            yanchor="top",
            font=current_font,
            pad={"t": 8, "b": 14, "l": 2, "r": 2},
        )
        layout_updates["title"] = current_title

    _protect_trace_labels(fig)
    fig.update_layout(**layout_updates)
    fig.update_xaxes(
        automargin=True,
        fixedrange=True,
        ticklabeloverflow="allow",
    )
    fig.update_yaxes(
        automargin=True,
        fixedrange=True,
        ticklabeloverflow="allow",
    )

    # V27 — replace Plotly's raw, unstyled default spike line with one
    # consistent, elegant treatment across the whole dashboard. Unified
    # hover modes ("x unified" / "y unified") force a spike line on by
    # default even when no chart-building function ever configured one —
    # that forced default renders as a stark, undashed white line, which
    # is exactly what showed up on charts (bars, composition, share bars…)
    # that only ever intended to use the unified hover *label*, not a
    # crosshair. A chart-type function may still request its own spike
    # styling explicitly (e.g. line charts already do); since this runs
    # last, it becomes the single source of truth so every chart matches,
    # and "closest"/other hover modes get spikes turned off outright since
    # nothing here ever asked for one.
    unified_spike_style = dict(
        showspikes=True,
        spikemode="across",
        spikesnap="cursor",
        spikethickness=1,
        spikedash="solid",
        spikecolor="rgba(167, 139, 250, 0.38)",
    )
    if hovermode == "x unified":
        fig.update_xaxes(**unified_spike_style)
        fig.update_yaxes(showspikes=False)
    elif hovermode == "y unified":
        fig.update_yaxes(**unified_spike_style)
        fig.update_xaxes(showspikes=False)
    else:
        fig.update_xaxes(showspikes=False)
        fig.update_yaxes(showspikes=False)

    if hovermode == "x unified":
        fig.update_xaxes(unifiedhovertitle={"text": "<b>%{x}</b>"})
    elif hovermode == "y unified":
        fig.update_yaxes(unifiedhovertitle={"text": "<b>%{y}</b>"})
    return fig

