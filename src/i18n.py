"""Small, dependency-free translation layer for executive presentation surfaces."""

from __future__ import annotations

from typing import Any

LANGUAGE_OPTIONS: dict[str, str] = {
    "Português": "pt",
    "English": "en",
    "Français": "fr",
}

PAGE_LABELS: dict[str, dict[str, str]] = {
    "Resumo Executivo": {"pt": "Resumo Executivo", "en": "Executive Summary", "fr": "Synthèse Exécutive"},
    "Visão Geral": {"pt": "Visão Geral", "en": "Overview", "fr": "Vue d’ensemble"},
    "Exames": {"pt": "Exames", "en": "Exams", "fr": "Examens"},
    "Atendimentos": {"pt": "Atendimentos", "en": "Appointments", "fr": "Consultations"},
    "Afastamentos": {"pt": "Afastamentos", "en": "Leaves", "fr": "Arrêts"},
    "Saúde Mental": {"pt": "Saúde Mental", "en": "Mental Health", "fr": "Santé mentale"},
}

_TRANSLATIONS: dict[str, dict[str, str]] = {
    "dashboard_title": {"pt": "Dashboard Serviço Médico", "en": "Medical Service Dashboard", "fr": "Tableau de bord du Service Médical"},
    "dashboard_subtitle": {"pt": "CGR 2026 — Painel Executivo", "en": "CGR 2026 — Executive Dashboard", "fr": "CGR 2026 — Tableau de bord exécutif"},
    "period": {"pt": "Período", "en": "Period", "fr": "Période"},
    "updated_at": {"pt": "Atualizado em", "en": "Updated", "fr": "Mis à jour"},
    "executive_panel": {"pt": "Painel executivo", "en": "Executive view", "fr": "Vue exécutive"},
    "filters": {"pt": "Filtros", "en": "Filters", "fr": "Filtres"},
    "filters_caption": {"pt": "Os filtros são aplicados automaticamente.", "en": "Filters are applied automatically.", "fr": "Les filtres sont appliqués automatiquement."},
    "restore_filters": {"pt": "Restaurar filtros", "en": "Reset filters", "fr": "Réinitialiser"},
    "sync_now": {"pt": "Sincronizar agora", "en": "Sync now", "fr": "Synchroniser"},
    "analysis_period": {"pt": "Período", "en": "Period", "fr": "Période"},
    "latest_month": {"pt": "Último mês", "en": "Latest month", "fr": "Dernier mois"},
    "last_3": {"pt": "Últimos 3", "en": "Last 3", "fr": "3 derniers"},
    "last_6": {"pt": "Últimos 6", "en": "Last 6", "fr": "6 derniers"},
    "year_to_date": {"pt": "Ano até agora", "en": "Year to date", "fr": "Depuis janvier"},
    "all_months": {"pt": "Todos os meses", "en": "All months", "fr": "Tous les mois"},
    "clear_months": {"pt": "Limpar meses", "en": "Clear months", "fr": "Effacer les mois"},
    "months_analysis": {"pt": "Meses de análise", "en": "Analysis months", "fr": "Mois analysés"},
    "operational_units": {"pt": "Unidades operacionais", "en": "Operational units", "fr": "Unités opérationnelles"},
    "comparison": {"pt": "Comparação", "en": "Comparison", "fr": "Comparaison"},
    "presentation_mode": {"pt": "Modo apresentação", "en": "Presentation mode", "fr": "Mode présentation"},
    "current_scope": {"pt": "Escopo atual", "en": "Current scope", "fr": "Périmètre actuel"},
    "executive_reading": {"pt": "Leitura executiva do período", "en": "Executive period review", "fr": "Lecture exécutive de la période"},
    "executive_snapshot": {"pt": "Resumo para diretoria", "en": "Board summary", "fr": "Synthèse pour la direction"},
    "management_comparison": {"pt": "Comparação gerencial", "en": "Management comparison", "fr": "Comparaison de gestion"},
    "main_trend": {"pt": "Tendência principal", "en": "Main trend", "fr": "Tendance principale"},
    "largest_impact": {"pt": "Onde está o maior impacto", "en": "Largest impact", "fr": "Impact principal"},
    "recommended_actions": {"pt": "Prioridades recomendadas", "en": "Recommended priorities", "fr": "Priorités recommandées"},
    "normalized_rates": {"pt": "Indicadores por 100 colaboradores", "en": "Indicators per 100 employees", "fr": "Indicateurs pour 100 salariés"},
    "data_readiness": {"pt": "Confiabilidade e preparação dos dados", "en": "Data confidence and readiness", "fr": "Fiabilité et préparation des données"},
    "metric": {"pt": "Indicador", "en": "Metric", "fr": "Indicateur"},
    "current": {"pt": "Atual", "en": "Current", "fr": "Actuel"},
    "previous": {"pt": "Anterior", "en": "Previous", "fr": "Précédent"},
    "variation": {"pt": "Variação (%)", "en": "Change (%)", "fr": "Variation (%)"},
    "target": {"pt": "Meta", "en": "Target", "fr": "Objectif"},
    "status": {"pt": "Status", "en": "Status", "fr": "Statut"},
    "within_target": {"pt": "Dentro da meta", "en": "On target", "fr": "Objectif atteint"},
    "attention": {"pt": "Atenção", "en": "Attention", "fr": "Attention"},
    "critical": {"pt": "Crítico", "en": "Critical", "fr": "Critique"},
    "informational": {"pt": "Informativo", "en": "Informational", "fr": "Informatif"},
    "not_configured": {"pt": "Não configurada", "en": "Not configured", "fr": "Non configuré"},
    "exams": {"pt": "Exames", "en": "Exams", "fr": "Examens"},
    "appointments": {"pt": "Atendimentos", "en": "Appointments", "fr": "Consultations"},
    "active_leaves": {"pt": "Afastamentos ativos", "en": "Active leaves", "fr": "Arrêts actifs"},
    "lost_days": {"pt": "Dias perdidos", "en": "Lost days", "fr": "Jours perdus"},
    "srq_cases": {"pt": "SRQ-20 alterados", "en": "Positive SRQ-20", "fr": "SRQ-20 positifs"},
    "periodic_coverage": {"pt": "Cobertura de periódicos", "en": "Periodic exam coverage", "fr": "Couverture des examens périodiques"},
    "absence_severity_proxy": {"pt": "Dias perdidos por afastamento ativo", "en": "Lost days per active leave", "fr": "Jours perdus par arrêt actif"},
    "source": {"pt": "Fonte", "en": "Source", "fr": "Source"},
    "last_update": {"pt": "Última atualização", "en": "Last update", "fr": "Dernière mise à jour"},
    "last_check": {"pt": "Última verificação", "en": "Last check", "fr": "Dernière vérification"},
    "source_synced": {"pt": "Fonte sincronizada", "en": "Source synced", "fr": "Source synchronisée"},
    "contingency_active": {"pt": "Contingência ativa", "en": "Fallback active", "fr": "Mode secours actif"},
    "data_attention": {"pt": "Atenção à atualização", "en": "Update attention", "fr": "Attention à la mise à jour"},
    "page": {"pt": "Página", "en": "Page", "fr": "Page"},
    "months": {"pt": "Meses", "en": "Months", "fr": "Mois"},
    "units": {"pt": "Unidades", "en": "Units", "fr": "Unités"},
    "consolidated_source": {"pt": "Fonte consolidada", "en": "Consolidated source", "fr": "Source consolidée"},
    "prepare_report": {"pt": "Preparar relatório executivo", "en": "Prepare executive report", "fr": "Préparer le rapport exécutif"},
    "download_report": {"pt": "Baixar relatório PDF", "en": "Download PDF report", "fr": "Télécharger le rapport PDF"},
    "confidentiality": {"pt": "Uso gerencial interno — dados agregados e confidenciais.", "en": "Internal management use — aggregated and confidential data.", "fr": "Usage interne de gestion — données agrégées et confidentielles."},
}


def normalize_language(language: str | None) -> str:
    value = str(language or "pt").strip().lower()
    return value if value in {"pt", "en", "fr"} else "pt"


def tr(key: str, language: str = "pt", **kwargs: Any) -> str:
    language = normalize_language(language)
    values = _TRANSLATIONS.get(key, {})
    text = values.get(language) or values.get("pt") or key
    try:
        return text.format(**kwargs)
    except (KeyError, ValueError):
        return text


def page_label(page: str, language: str = "pt") -> str:
    language = normalize_language(language)
    values = PAGE_LABELS.get(page, {})
    return values.get(language) or values.get("pt") or page
