"""Config Module — Dashboard SM CGR 2026 — V19.1 Executive Polish Visual System."""

from __future__ import annotations

MONTHS_ORDER = [
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
]

# Unidades CORRETAS conforme Excel + usuário: B2BN, B2BF, SF, SITE, OUTROS
UNITS = ['B2BN', 'B2BF', 'SF', 'SITE', 'OUTROS']
ABSENTEISMO_UNITS = ['B2BN', 'B2BF', 'SF']

def canonicalize_unit(unit: str) -> str:
    if not unit:
        return ""
    u = str(unit).strip()
    upper = u.upper()
    # Normaliza variações
    if "B2BN" in upper or "B2B N" in upper:
        return "B2BN"
    if "B2BF" in upper or "B2B F" in upper:
        return "B2BF"
    if upper == "SF" or " SF" in f" {upper} " or upper.startswith("SF ") or upper.endswith(" SF") or "SÃO FRANCISCO" in upper or "SAO FRANCISCO" in upper:
        return "SF"
    if "SITE" in upper:
        return "SITE"
    if "OUTRO" in upper:
        return "OUTROS"
    # Mantém compatibilidade com nomes antigos se aparecerem
    if "B2BS" in upper:
        return "SITE"  # mapeia B2BS antigo para SITE se necessário
    if "B2BG" in upper:
        return "SF"
    if "MATRIZ" in upper:
        return "OUTROS"
    # Retorna como está se já for válido
    for orig in UNITS:
        if orig.upper() == upper:
            return orig
    return u

def extract_unit_from_indicator(indicator: str) -> str:
    if not indicator:
        return ""
    text = str(indicator)
    upper = text.upper()
    # Verifica cada unidade na string
    for unit in UNITS:
        if unit.lower() in text.lower():
            return unit
        if unit.upper() in upper:
            return unit
    # Tenta extrair após último -
    if "-" in text:
        last = text.split("-")[-1].strip()
        cu = canonicalize_unit(last)
        if cu in UNITS:
            return cu
    return canonicalize_unit(text)

def sanitize_unit_selection(selected) -> list[str]:
    """Normalize unit selections without silently changing an explicit empty choice.

    ``None`` means no selection was supplied (use the dashboard default). An
    explicit empty iterable means the user cleared the slicer and must remain
    empty so the UI can show an honest empty state.
    """
    if selected is None:
        return UNITS.copy()
    selected_values = list(selected)
    if not selected_values:
        return []
    result = []
    for u in selected_values:
        cu = canonicalize_unit(u)
        if cu in UNITS:
            result.append(cu)
    # Remove duplicatas mantendo ordem.
    seen = []
    for r in result:
        if r not in seen:
            seen.append(r)
    return seen

# V19 — sistema visual executivo consolidado e refinado. A cor identifica o assunto, não julga o resultado.
# O fundo permanece neutro/navy; violeta é reservado à marca e Saúde Mental.
UI_COLORS = {
    "background": "#09111F",
    "background_secondary": "#0D1728",
    "card": "#111C2E",
    "card_hover": "#16243A",
    "border": "#263852",
    "grid": "rgba(151, 166, 186, 0.09)",
    "text": "#F8FAFC",
    "text_secondary": "#D7E0EC",
    "text_muted": "#97A6BA",
    "brand": "#9B8AFB",
}

COLORS = {
    "blue": "#4C8DFF",
    "light_blue": "#76A9FF",
    "dark_blue": "#2F6FE4",
    "navy": "#0D1728",
    "cyan": "#56C8F5",
    "light_cyan": "#8AD9F7",
    "purple": "#B49AF7",
    "light_purple": "#CFC0FB",
    "dark_purple": "#9277F3",
    "magenta": "#C7A5FA",
    "fuchsia": "#C7A5FA",
    "lavender": "#CFC0FB",
    "white": "#F8FAFC",
    # Compatibility keys are metric identities, never good/bad semantics.
    "green": "#26C6B5",
    "light_green": "#63D9CD",
    "orange": "#F5B84B",
    "red": "#FF8A5B",
    "pink": "#F19AC2",
    "yellow": "#F8C95F",
    "gray": "#97A6BA",
    "primary": "#9B8AFB",
    "secondary": "#4C8DFF",
    "accent": "#26C6B5",
}

# Restrained qualitative palette. Single-metric charts use METRIC_COLORS.
PALETTE = [
    "#4C8DFF",  # blue
    "#26C6B5",  # teal
    "#B49AF7",  # violet
    "#F5B84B",  # amber
    "#56C8F5",  # sky
    "#FF8A5B",  # coral
    "#97A6BA",  # slate
    "#7C8CF8",  # indigo
    "#63D9CD",  # light teal
    "#CFC0FB",  # lavender
]

# Unidade = identidade fixa em todas as páginas.
UNIT_COLORS = {
    "B2BN": "#B49AF7",
    "B2BF": "#4C8DFF",
    "SF": "#F5B84B",
    "SITE": "#26C6B5",
    "OUTROS": "#97A6BA",
    "Default": "#97A6BA",
}

# Métrica = identidade fixa. Direção é comunicada por seta/texto, nunca pela cor.
METRIC_PALETTES = {
    "Exames": ["#2F6FE4", "#4C8DFF", "#56C8F5", "#8FB7FF", "#97A6BA"],
    "Atendimentos": ["#168F84", "#26C6B5", "#56C8F5", "#7C8CF8", "#97A6BA"],
    "Afastamentos": ["#C98A1D", "#F5B84B", "#F8C95F", "#F9D98B", "#97A6BA"],
    "Dias Perdidos": ["#D96035", "#FF8A5B", "#FFA27F", "#FFC0A8", "#97A6BA"],
    "SRQ-20": ["#7E63DA", "#9B8AFB", "#B49AF7", "#CFC0FB", "#97A6BA"],
    "Previdenciario": ["#2A85B8", "#3BA7D8", "#56C8F5", "#8AD9F7", "#97A6BA"],
}

METRIC_COLORS = {
    "exames": "#4C8DFF",
    "Exames": "#4C8DFF",
    "atendimentos": "#26C6B5",
    "Atendimentos": "#26C6B5",
    "afastamentos": "#F5B84B",
    "Afastamentos": "#F5B84B",
    "absenteismo": "#FF8A5B",
    "Dias Perdidos": "#FF8A5B",
    "saude_mental": "#B49AF7",
    "SRQ-20": "#B49AF7",
    "periodic_coverage": "#56C8F5",
    "Cobertura": "#56C8F5",
    "periodic_absences": "#97A6BA",
    "total": "#9B8AFB",
    "blue": "#4C8DFF",
    "green": "#26C6B5",
    "orange": "#F5B84B",
    "red": "#FF8A5B",
    "purple": "#B49AF7",
    "cyan": "#56C8F5",
}

# Decorative brand gradient; never performance encoding.
CHART_GRADIENTS = {
    "brand": ["#9B8AFB", "#7C8CF8"],
}

COMPARISON_MODES = ["Mês anterior", "Mês homólogo", "Acumulado anual", "Sem comparação"]
PAGE_NAMES = ["Resumo Executivo", "Exames", "Atendimentos", "Afastamentos", "Saúde Mental"]
PAGE_ICONS = {
    "Resumo Executivo": "◆",
    "Exames": "◉",
    "Atendimentos": "✚",
    "Afastamentos": "▤",
    "Saúde Mental": "◈",
}
DATA_SCHEMA_VERSION = "v10"
DATA_STALE_AFTER_DAYS = 7
MOVING_AVERAGE_WINDOW = 3
TABLE_HEIGHT = 400


ENCODING_FIXES = {
    "Ã§": "ç", "Ã£": "ã", "Ã¡": "á", "Ã©": "é",
    "Ã­": "í", "Ã³": "ó", "Ãº": "ú", "Â": "",
}

def __getattr__(name: str):
    if name.endswith("_FIXES") or name.endswith("_MAP") or name.endswith("_MAPPING") or name.endswith("_ALIAS"):
        return {}
    if name.endswith("_ORDER") or name.endswith("_UNITS") or name.endswith("_MODES") or name.endswith("_NAMES") or name.endswith("_COLUMNS"):
        return []
    if name.startswith("DEFAULT_") or name.endswith("_VERSION") or name.endswith("_DAYS") or name.endswith("_COST") or name.endswith("_POINTS") or name.endswith("_MONTHS") or name.endswith("_ALERTS") or name.endswith("_WINDOW") or name.endswith("_HEIGHT"):
        return 0
    return None
