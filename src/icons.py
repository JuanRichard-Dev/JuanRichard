"""Small inline-SVG icon set, added in V13.1 to replace emoji at the most
visible spots (section headers, hero KPI, status dots).

Deliberately NOT using an icon font/CDN (e.g. Tabler, Font Awesome): this
project already avoids external runtime dependencies wherever possible
and can be deployed on an internal/
restricted network (see HOSPEDAGEM_INTERNA.md), where a blocked CDN would
silently break every icon. Every icon here is a static string, no network
call, no JavaScript.

Each icon is a 24x24 outline glyph sized with width/height="1em" so it
scales with the surrounding font-size exactly like the emoji character it
replaces, and colored with stroke="currentColor" so it inherits whatever
text color is already active (KPI accent color, status color, etc.)
instead of carrying its own fixed color the way emoji do.

This module has no imports beyond the standard library and no Streamlit/
Plotly dependency, so it can be exercised standalone (see
tests/test_icons_render.py-style checks run during development).
"""

_STROKE = 'fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"'
_WRAP_OPEN = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="1em" height="1em" style="vertical-align:-0.125em" aria-hidden="true" {stroke}>'


def _svg(inner: str, stroke: bool = True) -> str:
    open_tag = _WRAP_OPEN.format(stroke=_STROKE if stroke else 'fill="currentColor" stroke="none"')
    return f"{open_tag}{inner}</svg>"


ICONS: dict[str, str] = {
    "trend": _svg('<polyline points="3,17 9,11 13,15 21,5"/><polyline points="14,5 21,5 21,12"/>'),
    "building": _svg('<path d="M4 21V10L12 4l8 6v11"/><line x1="9" y1="21" x2="9" y2="14"/><line x1="15" y1="21" x2="15" y2="14"/>'),
    "bars": _svg('<rect x="4" y="12" width="4" height="9" rx="0.5"/><rect x="10" y="6" width="4" height="15" rx="0.5"/><rect x="16" y="9" width="4" height="12" rx="0.5"/>'),
    "compass": _svg('<circle cx="12" cy="12" r="9"/><polyline points="9,15 15,9"/><polyline points="10,9 15,9 15,14"/>'),
    "people": _svg('<circle cx="8" cy="8" r="3.2"/><path d="M2.5 20a5.5 5.5 0 0 1 11 0"/><circle cx="17" cy="9" r="2.6"/><path d="M13.5 20a4.2 4.2 0 0 1 8 -1.3"/>'),
    "alert-triangle": _svg('<path d="M12 4 L21 20 L3 20 Z"/><line x1="12" y1="10" x2="12" y2="14.5"/><circle cx="12" cy="17" r="0.6" fill="currentColor" stroke="none"/>'),
    "medical-cross": _svg('<circle cx="12" cy="12" r="9"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/>'),
    "clipboard-check": _svg('<rect x="5" y="4" width="14" height="17" rx="2"/><path d="M9 4V2.5a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1V4"/><polyline points="8.5,13 11,15.5 16,10"/>'),
    "clipboard": _svg('<rect x="5" y="4" width="14" height="17" rx="2"/><rect x="9" y="2.5" width="6" height="3" rx="1"/><line x1="8" y1="11" x2="16" y2="11"/><line x1="8" y1="15" x2="16" y2="15"/>'),
    "target": _svg('<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="4.5"/><circle cx="12" cy="12" r="1" fill="currentColor" stroke="none"/>'),
    "podium": _svg('<rect x="3" y="13" width="5" height="8" rx="1"/><rect x="9.5" y="7" width="5" height="14" rx="1"/><rect x="16" y="10" width="5" height="11" rx="1"/>'),
    "wave": _svg('<path d="M2 14 Q6 8 10 14 T18 14"/>'),
    "layers": _svg('<path d="M12 3 3 8 12 13 21 8Z"/><path d="M3 13l9 5 9-5"/>'),
    "thermometer": _svg('<rect x="10" y="3" width="4" height="12" rx="2"/><circle cx="12" cy="18" r="3"/>'),
    "ruler": _svg('<line x1="3" y1="12" x2="21" y2="12"/><line x1="6" y1="9" x2="6" y2="15"/><line x1="11" y1="9" x2="11" y2="15"/><line x1="16" y1="9" x2="16" y2="15"/>'),
    "coins": _svg('<circle cx="8" cy="16" r="5"/><circle cx="16" cy="8" r="5"/>'),
    "brain-pulse": _svg('<circle cx="12" cy="12" r="9"/><path d="M6 12h3l1.5-3 3 6 1.5-3h3"/>'),
    "lightbulb": _svg('<path d="M9 18h6"/><path d="M10 21h4"/><path d="M12 3a6 6 0 0 0-4 10.5c.6.6 1 1.5 1 2.5h6c0-1 .4-1.9 1-2.5A6 6 0 0 0 12 3Z"/>'),
    "activity": _svg('<polyline points="2,12 7,12 9,6 13,18 16,12 22,12"/>'),
    "search": _svg('<circle cx="10.5" cy="10.5" r="6.5"/><line x1="15.5" y1="15.5" x2="21" y2="21"/>'),
    "download": _svg('<path d="M12 3v12"/><polyline points="7,10 12,15 17,10"/><line x1="4" y1="20" x2="20" y2="20"/>'),
    "shield-check": _svg('<path d="M12 3l7 3v6c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6Z"/><polyline points="9,12 11,14 15,9.5"/>'),
    "sync": _svg('<path d="M4 12a8 8 0 0 1 14-5.3L21 9"/><path d="M21 4v5h-5"/><path d="M20 12a8 8 0 0 1-14 5.3L3 15"/><path d="M3 20v-5h5"/>'),
    "calendar": _svg('<rect x="3" y="5" width="18" height="16" rx="2"/><line x1="7" y1="3" x2="7" y2="7"/><line x1="17" y1="3" x2="17" y2="7"/><line x1="3" y1="10" x2="21" y2="10"/><circle cx="8" cy="14.5" r=".8" fill="currentColor" stroke="none"/><circle cx="12" cy="14.5" r=".8" fill="currentColor" stroke="none"/><circle cx="16" cy="14.5" r=".8" fill="currentColor" stroke="none"/>'),
    "stethoscope": _svg('<path d="M6 3v5a4 4 0 0 0 8 0V3"/><path d="M10 12v2a5 5 0 0 0 10 0v-1"/><circle cx="20" cy="10.5" r="2"/>'),
    "ambulance": _svg('<path d="M3 7h11v11H3z"/><path d="M14 11h4l3 3v4h-7z"/><circle cx="7" cy="19" r="2"/><circle cx="17" cy="19" r="2"/><line x1="6" y1="11" x2="11" y2="11"/><line x1="8.5" y1="8.5" x2="8.5" y2="13.5"/>'),
    "scales": _svg('<line x1="12" y1="3" x2="12" y2="20"/><line x1="6" y1="6" x2="18" y2="6"/><path d="M6 6 3 12h6L6 6Z"/><path d="M18 6 15 12h6L18 6Z"/><line x1="8" y1="20" x2="16" y2="20"/>'),
}


def icon(name: str, *, fallback: str = "") -> str:
    """Return the inline-SVG markup for an icon name. Falls back to the
    given text/emoji (or an empty string) if the name isn't in the set,
    so a typo degrades gracefully instead of raising."""
    return ICONS.get(name, fallback)


_STATUS_COLOR = {
    "green": "#10B981",
    "yellow": "#FBBF24",
    "orange": "#F97316",
    "red": "#DC2626",
}


def status_dot(status: str, *, label: str = "") -> str:
    """Return a small filled status dot (replacement for 🟢🟡🟠🔴), with an
    accessible label instead of relying on color alone (WCAG 1.4.1)."""
    color = _STATUS_COLOR.get(status, _STATUS_COLOR["green"])
    aria = f' role="img" aria-label="{label}"' if label else ' aria-hidden="true"'
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 12 12" width="0.7em" height="0.7em" '
        f'style="vertical-align:0.05em"{aria}><circle cx="6" cy="6" r="5" fill="{color}"/></svg>'
    )
