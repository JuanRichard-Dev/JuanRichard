"""Config Module — Dashboard SM CGR 2026 - TEMA ROXO FORTE - UNIDADES CORRETAS"""

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
    if not selected:
        return UNITS.copy()
    result = []
    for u in selected:
        cu = canonicalize_unit(u)
        if cu in UNITS:
            result.append(cu)
    # Remove duplicatas mantendo ordem
    seen = []
    for r in result:
        if r not in seen:
            seen.append(r)
    return seen or UNITS.copy()

# CORES - ROXO FORTE + MAGENTA NEON + BRANCO FORTE
COLORS = {
    "blue": "#7C3AED",
    "light_blue": "#A78BFA",
    "dark_blue": "#5B21B6",
    "navy": "#1E0B3A",
    "cyan": "#A78BFA",
    "light_cyan": "#C4B5FD",
    "purple": "#7C3AED",
    "light_purple": "#A78BFA",
    "dark_purple": "#4C1D95",
    "magenta": "#EC4899",
    "fuchsia": "#D946EF",
    "lavender": "#C4B5FD",
    "white": "#FFFFFF",
    "green": "#EC4899",
    "light_green": "#F0ABFC",
    "orange": "#D946EF",
    "red": "#F43F5E",
    "pink": "#F472B6",
    "yellow": "#E9D5FF",
    "gray": "#A78BFA",
    "primary": "#7C3AED",
    "secondary": "#EC4899",
    "accent": "#D946EF",
}

PALETTE = [
    "#7C3AED", "#EC4899", "#D946EF", "#A78BFA",
    "#F472B6", "#8B5CF6", "#C084FC", "#FFFFFF",
    "#4C1D95", "#BE185D",
]

UNIT_COLORS = {
    "B2BN": "#7C3AED",
    "B2BF": "#EC4899",
    "SF": "#D946EF",
    "SITE": "#A78BFA",
    "OUTROS": "#F472B6",
    "Default": "#7C3AED",
}

METRIC_COLORS = {
    "exames": "#7C3AED",
    "atendimentos": "#EC4899",
    "afastamentos": "#D946EF",
    "absenteismo": "#F43F5E",
    "saude_mental": "#8B5CF6",
    "periodic_coverage": "#7C3AED",
    "periodic_absences": "#EC4899",
    "total": "#7C3AED",
    "blue": "#7C3AED",
    "green": "#EC4899",
    "orange": "#D946EF",
    "red": "#F43F5E",
    "purple": "#7C3AED",
    "cyan": "#A78BFA",
}

CHART_GRADIENTS = {
    "purple_to_magenta": ["#7C3AED", "#EC4899"],
    "purple_to_fuchsia": ["#7C3AED", "#D946EF"],
}

COMPARISON_MODES = ["Mês anterior", "Mês homólogo", "Acumulado anual", "Sem comparação"]
PAGE_NAMES = ["Resumo Executivo", "Visão Geral", "Exames", "Atendimentos", "Afastamentos", "Saúde Mental"]
DATA_SCHEMA_VERSION = "v10"
DATA_STALE_AFTER_DAYS = 7
DEFAULT_DAILY_ABSENCE_COST = 150.0
FORECAST_MIN_POINTS = 3
FORECAST_MONTHS = 2
MAX_ALERTS = 10
MOVING_AVERAGE_WINDOW = 3
TABLE_HEIGHT = 400

class _Targets(dict):
    def __missing__(self, key):
        if "max" in key:
            return 1000
        if "coverage" in key or "pct" in key or "min" in key:
            return 95
        return 0
    def __getitem__(self, key):
        return super().get(key, self.__missing__(key))

TARGETS = _Targets({
    "periodic_coverage": 95,
    "periodic_absences": 5,
    "periodicos_pct": 95,
    "periodicos_coverage": 95,
    "faltas_pct_max": 10,
    "mental_cases_max": 10,
    "exam_coverage": 95,
    "exames_coverage": 95,
    "absenteismo_monthly_max": 50,
    "afastamentos_monthly_max": 30,
    "atendimentos_monthly_min": 0,
    "exames_monthly_min": 0,
})

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
