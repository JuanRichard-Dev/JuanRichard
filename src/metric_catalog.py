"""Metric definitions shown inside the dashboard."""

from __future__ import annotations

METRIC_CATALOG: dict[str, dict[str, str]] = {
    "Exames": {
        "definicao": "Quantidade de exames ocupacionais registrados no período.",
        "formula": "Soma dos tipos de exame selecionados.",
        "direcao": "Contextual; deve ser interpretado com o plano ocupacional.",
        "fonte": "Aba Principal.",
    },
    "Atendimentos": {
        "definicao": "Quantidade de atendimentos assistenciais registrados.",
        "formula": "Soma dos atendimentos, sem duplicar os subtotais horista e mensalista da fisioterapia.",
        "direcao": "Contextual; volume maior não é necessariamente pior.",
        "fonte": "Aba Principal.",
    },
    "Afastamentos ativos": {
        "definicao": "Quantidade de pessoas com afastamento ativo no mês.",
        "formula": "Soma das unidades selecionadas no último mês do filtro.",
        "direcao": "Menor é melhor.",
        "fonte": "Aba Principal.",
    },
    "Dias perdidos": {
        "definicao": "Quantidade de dias de trabalho perdidos por afastamentos.",
        "formula": "Soma dos blocos de absenteísmo das unidades selecionadas.",
        "direcao": "Menor é melhor.",
        "fonte": "Aba Absenteísmo.",
    },
    "SRQ-20": {
        "definicao": "Quantidade de triagens SRQ-20 classificadas como alteradas.",
        "formula": "Soma das unidades selecionadas no período.",
        "direcao": "Menor é melhor; não representa diagnóstico clínico.",
        "fonte": "Aba Saúde Mental.",
    },
}
