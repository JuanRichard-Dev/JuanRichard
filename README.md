# Dashboard SM CGR 2026 — V22

Dashboard executivo em Streamlit para acompanhamento de Exames, Atendimentos, Afastamentos, Dias Perdidos e Saúde Mental (SRQ-20).

## Estrutura essencial

- `app.py` — aplicação Streamlit.
- `src/` — carregamento, transformação, componentes, gráficos, estilos, filtros e integrações.
- `.streamlit/config.toml` — tema/configuração do Streamlit.
- `requirements.txt` — dependências de produção.
- `Dashboard SM CGR 2026.xlsx` — fonte local atualmente usada pelo dashboard.
- `google_drive_sync/` — automação independente que envia o XLSX local ao Google Drive a cada 10 minutos.
- `population_by_unit.csv` — denominadores por unidade para indicadores normalizados.
- `render.yaml` — deploy no Render.
- `tests/` + `.github/workflows/ci.yml` — smoke/regressão mínima no GitHub.

## Executar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Arquitetura recomendada: Excel local → Google Drive → Streamlit

O dashboard suporta `DATA_SOURCE=google_drive` para ler um arquivo privado do Google Drive usando uma conta de serviço. Configure `DATA_GOOGLE_DRIVE_FILE_ID`, `GOOGLE_SERVICE_ACCOUNT_JSON` e `AUTO_REFRESH_SECONDS=600` nos secrets/variáveis do Render. O arquivo JSON da conta de serviço nunca deve ser commitado.

No computador que possui a planilha, siga o guia em [`google_drive_sync/README.md`](google_drive_sync/README.md). O script verifica o XLSX local, rejeita cópias incompletas ou corrompidas, atualiza o mesmo arquivo no Drive e não faz upload quando o hash não mudou. O Streamlit executa um rerun automático no mesmo intervalo e mantém o botão de sincronização manual.

## Desenvolvimento/testes

```bash
pip install -r requirements-dev.txt
pytest -q
```

## Segurança

Nunca envie `.streamlit/secrets.toml` ao GitHub. Use `.streamlit/secrets.toml.example` apenas como referência e configure segredos no ambiente de hospedagem.

Não publique a planilha nem a chave privada da conta de serviço. Compartilhe a pasta do Drive somente com a conta de serviço e conceda ao dashboard acesso de leitura; conceda edição apenas à automação local.

> Se este repositório for público, revise a planilha `Dashboard SM CGR 2026.xlsx` antes do upload para garantir que nenhum dado interno/confidencial seja publicado.


## Interface atual

A V22 padroniza selectbox, multiselect e menus suspensos em navy/slate com acento azul funcional, removendo estilos roxos legados e artefatos de foco dos controles nativos.
