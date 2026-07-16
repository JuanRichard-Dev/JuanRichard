"""Automatic source monitoring for local, Google Sheets and SharePoint data."""

from __future__ import annotations

import html
from datetime import datetime, timedelta

import streamlit as st

from src.data_sources import DataSourceError, PreparedDataSource, probe_data_source, quick_file_signature
from src.runtime_config import get_bool, get_int

_INTERVAL_SECONDS = get_int("AUTO_REFRESH_SECONDS", 120, minimum=15)
_RUN_EVERY = f"{_INTERVAL_SECONDS}s" if get_bool("AUTO_REFRESH_ENABLED", True) else None


def auto_sync_interval_seconds() -> int:
    return _INTERVAL_SECONDS


def _format_datetime(value: datetime | None) -> str:
    return value.strftime("%d/%m/%Y %H:%M:%S") if isinstance(value, datetime) else "—"


def _format_size(size_bytes: int) -> str:
    if size_bytes >= 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.2f} MB"
    return f"{size_bytes / 1024:.1f} KB"


def _source_label(source_type: str) -> str:
    labels = {
        "google_sheets": "Google Sheets",
        "url": "URL remota",
        "local": "Arquivo local / OneDrive",
        "sharepoint": "SharePoint",
    }
    return labels.get(source_type, source_type.replace("_", " ").title())


def _render_sync_card(
    source: PreparedDataSource,
    *,
    last_check: datetime,
    next_check: datetime,
    status: str,
    error: str = "",
) -> None:
    contingency = source.fallback_used or status == "contingency"
    status_class = "contingency" if contingency else ("warning" if status == "warning" else "online")
    status_text = (
        "🟠 Contingência ativa"
        if contingency
        else ("🟡 Verificação com alerta" if status == "warning" else "🟢 AutoSync ativo")
    )
    change_time = source.changed_at or source.modified_at
    error_html = (
        f'<div class="autosync-error" title="{html.escape(error)}">{html.escape(error[:150])}</div>'
        if error else ""
    )
    st.markdown(
        f"""
        <div class="autosync-card {status_class}">
            <div class="autosync-card-head">
                <span class="autosync-title">{status_text}</span>
                <span class="autosync-interval">{_INTERVAL_SECONDS}s</span>
            </div>
            <div class="autosync-grid">
                <div><span>Fonte</span><strong>{html.escape(_source_label(source.source_type))}</strong></div>
                <div><span>Arquivo</span><strong title="{html.escape(source.display_name)}">{html.escape(source.display_name)}</strong></div>
                <div><span>Última verificação</span><strong>{_format_datetime(last_check)}</strong></div>
                <div><span>Última alteração</span><strong>{_format_datetime(change_time)}</strong></div>
                <div><span>Tamanho</span><strong>{_format_size(source.size_bytes)}</strong></div>
                <div><span>Versão</span><strong>{html.escape(source.checksum[:12])}</strong></div>
                <div class="autosync-next"><span>Próxima verificação</span><strong>{_format_datetime(next_check)}</strong></div>
            </div>
            {error_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


@st.fragment(run_every=_RUN_EVERY)
def render_source_monitor(source: PreparedDataSource) -> None:
    """Check the source every configured interval and rerun when it changes."""
    now = datetime.now()
    last_check = source.checked_at or now
    next_check = now + timedelta(seconds=_INTERVAL_SECONDS)
    status = "contingency" if source.fallback_used else "online"
    error = ""

    if get_bool("AUTO_REFRESH_ENABLED", True):
        try:
            if source.source_type == "local" and source.original_path and not source.fallback_used:
                current_signature = quick_file_signature(source.original_path)
                if current_signature == (0, 0):
                    raise DataSourceError("O arquivo local está temporariamente indisponível.")
                changed = current_signature != source.source_signature
                latest = None
            else:
                latest = probe_data_source(source)
                last_check = latest.checked_at or now
                changed = latest.checksum != source.checksum

            st.session_state["_autosync_last_check"] = last_check.isoformat()
            st.session_state["_autosync_next_check"] = next_check.isoformat()
            st.session_state["_autosync_status"] = "online"
            st.session_state.pop("_autosync_error", None)

            if changed or source.fallback_used:
                st.session_state["_source_change_detected_at"] = now.isoformat()
                st.cache_data.clear()
                st.rerun()
        except DataSourceError as exc:
            status = "contingency" if source.fallback_used else "warning"
            error = str(exc)
            last_check = now
            st.session_state["_autosync_last_check"] = now.isoformat()
            st.session_state["_autosync_next_check"] = next_check.isoformat()
            st.session_state["_autosync_status"] = status
            st.session_state["_autosync_error"] = error
    else:
        status = "warning"
        error = "AutoSync desativado na configuração."

    _render_sync_card(
        source,
        last_check=last_check,
        next_check=next_check,
        status=status,
        error=error,
    )


# Backward-compatible name used by V10 app/tests.
def render_local_source_monitor(source: PreparedDataSource) -> None:
    render_source_monitor(source)
