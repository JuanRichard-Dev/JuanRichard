"""Responsive visual helpers for Streamlit + Plotly.

The dashboard uses a safe notebook-first profile because Streamlit does not
expose the browser width to Python without an extra frontend component. CSS
media queries handle grid reflow while these helpers calculate chart density,
heights, margins, legends and tick labels from the actual figure content.
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
    font_size = 11 if item_count <= 5 and max_label_length <= 24 else 10
    y = 1.04 + max(0, legend_rows - 1) * 0.055
    config: dict[str, Any] = {
        "orientation": "h",
        "x": 0,
        "xanchor": "left",
        "y": y,
        "yanchor": "bottom",
        "font": {"size": font_size, "color": "#D9E6F2"},
        "bgcolor": "rgba(0,0,0,0)",
        "borderwidth": 0,
        "traceorder": "normal",
    }
    # Supported by Plotly 6.5.2; helps wrap long legends consistently.
    if chart_type in {"composition", "stacked", "pareto"}:
        config.update(entrywidth=132, entrywidthmode="pixels")
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


def apply_figure_safety(fig: go.Figure) -> go.Figure:
    """Apply responsive, accessible and title-safe safeguards at render time."""
    title_text = getattr(fig.layout.title, "text", None)
    title_lines = _title_line_count(title_text)
    legend_rows = _visible_legend_rows(fig)

    margin = fig.layout.margin
    existing_l = int(getattr(margin, "l", None) or 0)
    existing_r = int(getattr(margin, "r", None) or 0)
    existing_t = int(getattr(margin, "t", None) or 0)
    existing_b = int(getattr(margin, "b", None) or 0)

    safe_margin = calculate_plot_margins(
        title_lines=title_lines,
        legend_rows=legend_rows,
        x_label_length=0,
        y_label_length=0,
        outside_labels=False,
    )
    final_margin = {
        "l": max(existing_l, safe_margin["l"]),
        "r": max(existing_r, safe_margin["r"]),
        "t": max(existing_t, safe_margin["t"]),
        "b": max(existing_b, safe_margin["b"]),
        "pad": max(int(getattr(margin, "pad", None) or 0), 6),
    }

    layout_updates: dict[str, Any] = {
        "autosize": True,
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "dragmode": False,
        "margin": final_margin,
        "hoverlabel": {
            "bgcolor": "#0F2138",
            "bordercolor": "rgba(96,165,250,.42)",
            "font": {"color": "#F8FBFF", "size": 12},
            "align": "left",
            "namelength": -1,
        },
    }

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

    fig.update_layout(**layout_updates)
    fig.update_xaxes(automargin=True, fixedrange=True)
    fig.update_yaxes(automargin=True, fixedrange=True)
    return fig

