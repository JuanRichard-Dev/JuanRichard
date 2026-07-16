"""Optional authentication and unit-level authorization.

Supported modes:
- ``off``: no login, intended only for local/private networks.
- ``password``: one shared password stored in secrets or an environment variable.
- ``oidc``: native Streamlit OIDC login, suitable for Microsoft Entra ID.
"""

from __future__ import annotations

import hashlib
import hmac
from dataclasses import dataclass
from typing import Any

import streamlit as st

from src.config import UNITS
from src.runtime_config import get_csv, get_section, get_setting


@dataclass(frozen=True)
class UserContext:
    authenticated: bool
    name: str
    email: str
    role: str
    allowed_units: tuple[str, ...]
    auth_mode: str


def _normalize_email(value: Any) -> str:
    return str(value or "").strip().casefold()


def _password_digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _allowed_units_for_email(email: str) -> tuple[str, ...]:
    """Resolve optional role/unit mappings from secrets.

    Example:
    [authorization]
    admin_emails = ["director@company.com"]
    b2bn_emails = ["manager@company.com"]
    """
    authorization = get_section("authorization")
    admin_emails = {
        _normalize_email(item)
        for item in authorization.get("admin_emails", get_csv("ADMIN_EMAILS"))
    }
    if email and email in admin_emails:
        return tuple(UNITS)

    allowed: list[str] = []
    for unit in UNITS:
        key = f"{unit.lower()}_emails"
        configured = authorization.get(key, get_csv(key.upper()))
        normalized = {_normalize_email(item) for item in configured}
        if email and email in normalized:
            allowed.append(unit)

    # No explicit mapping means the authenticated user can see the complete
    # dashboard. Restriction is only applied when an allow-list is configured.
    has_any_mapping = bool(admin_emails) or any(
        authorization.get(f"{unit.lower()}_emails") for unit in UNITS
    )
    if has_any_mapping:
        return tuple(allowed)
    return tuple(UNITS)


def _oidc_user_fields() -> tuple[str, str]:
    user = st.user
    name = str(getattr(user, "name", "") or "Usuário")
    email = _normalize_email(
        getattr(user, "email", "")
        or getattr(user, "preferred_username", "")
        or getattr(user, "upn", "")
    )
    return name, email


def enforce_authentication() -> UserContext:
    """Render login UI when required and return the active user context."""
    mode = str(get_setting("AUTH_MODE", "off")).strip().casefold()
    if mode not in {"off", "password", "oidc"}:
        mode = "off"

    if mode == "off":
        return UserContext(True, "Visitante", "", "viewer", tuple(UNITS), mode)

    if mode == "password":
        expected = str(get_setting("APP_PASSWORD", ""))
        if not expected:
            st.error("AUTH_MODE=password está ativo, mas APP_PASSWORD não foi configurada.")
            st.stop()

        if not st.session_state.get("_password_authenticated", False):
            st.title("🔐 Dashboard privado")
            st.caption("Informe a senha definida pelo administrador para acessar o painel.")
            password = st.text_input("Senha", type="password", key="shared_password_input")
            if st.button("Entrar", type="primary", use_container_width=True):
                valid = hmac.compare_digest(_password_digest(password), _password_digest(expected))
                if valid:
                    st.session_state["_password_authenticated"] = True
                    st.rerun()
                st.error("Senha inválida.")
            st.stop()

        return UserContext(True, "Usuário autorizado", "", "viewer", tuple(UNITS), mode)

    # OIDC mode
    try:
        logged_in = bool(st.user.is_logged_in)
    except Exception:
        st.error(
            "A autenticação OIDC não foi inicializada. Configure a seção [auth] "
            "nos secrets e instale Authlib."
        )
        st.stop()

    if not logged_in:
        st.title("🔐 Dashboard corporativo")
        st.caption("Entre com sua conta Microsoft autorizada.")
        if st.button("Entrar com Microsoft", type="primary", use_container_width=True):
            st.login("microsoft")
        st.stop()

    name, email = _oidc_user_fields()
    allowed_emails = {_normalize_email(value) for value in get_csv("ALLOWED_EMAILS")}
    authorization = get_section("authorization")
    allowed_emails.update(
        _normalize_email(value) for value in authorization.get("allowed_emails", [])
    )
    if allowed_emails and email not in allowed_emails:
        st.error("Sua conta foi autenticada, mas não possui autorização para este dashboard.")
        st.button("Sair", on_click=st.logout)
        st.stop()

    units = _allowed_units_for_email(email)
    if not units:
        st.error("Sua conta não possui unidades liberadas.")
        st.button("Sair", on_click=st.logout)
        st.stop()

    role = "admin" if set(units) == set(UNITS) else "unit_manager"
    return UserContext(True, name, email, role, units, mode)


def render_user_sidebar(user: UserContext) -> None:
    """Show a compact user identity block in the sidebar."""
    if user.auth_mode == "off":
        return
    st.sidebar.markdown("---")
    st.sidebar.caption(f"Conectado como **{user.name}**")
    if user.email:
        st.sidebar.caption(user.email)
    if user.auth_mode == "oidc":
        st.sidebar.button("Sair", on_click=st.logout, use_container_width=True)
    elif user.auth_mode == "password":
        if st.sidebar.button("Sair", use_container_width=True):
            st.session_state.pop("_password_authenticated", None)
            st.rerun()
