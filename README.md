# Dashboard SM CGR 2026 — V22

Dashboard executivo em Streamlit para acompanhamento de Exames, Atendimentos, Afastamentos, Dias Perdidos e Saúde Mental (SRQ-20).

## Estrutura essencial

- `app.py` — aplicação Streamlit.
- `src/` — carregamento, transformação, componentes, gráficos, estilos, filtros e integrações.
- `.streamlit/config.toml` — tema/configuração do Streamlit.
- `requirements.txt` — dependências de produção.
- `Dashboard SM CGR 2026.xlsx` — fonte local atualmente usada pelo dashboard.
- `population_by_unit.csv` — denominadores por unidade para indicadores normalizados.
- `render.yaml` — deploy no Render.
- `tests/` + `.github/workflows/ci.yml` — smoke/regressão mínima no GitHub.

## Executar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Desenvolvimento/testes

```bash
pip install -r requirements-dev.txt
pytest -q
```

## Segurança

Nunca envie `.streamlit/secrets.toml` ao GitHub. Use `.streamlit/secrets.toml.example` apenas como referência e configure segredos no ambiente de hospedagem.

> Se este repositório for público, revise a planilha `Dashboard SM CGR 2026.xlsx` antes do upload para garantir que nenhum dado interno/confidencial seja publicado.


## Interface atual

A V22 padroniza selectbox, multiselect e menus suspensos em navy/slate com acento azul funcional, removendo estilos roxos legados e artefatos de foco dos controles nativos.
