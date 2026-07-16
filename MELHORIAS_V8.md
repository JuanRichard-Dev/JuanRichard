# Melhorias implementadas — V8 Deploy Ready

## Deploy

- Streamlit Community Cloud.
- Render por `render.yaml`.
- Docker.
- `Procfile`, `start.sh` e GitHub Actions.
- Configuração de produção e health check.

## Fontes de dados

- planilha local;
- arquivo por URL HTTPS;
- SharePoint via Microsoft Graph;
- checksum e metadados da fonte;
- invalidação de cache quando a origem muda.

## Segurança

- acesso livre, senha ou Microsoft Entra ID;
- lista opcional de e-mails permitidos;
- permissão opcional por unidade;
- credenciais somente por secrets ou variáveis de ambiente;
- nenhum segredo real incluído.

## Relatório executivo

- PDF com período, unidades, usuário, narrativa, KPIs, alertas,
  tendência e ranking.

## Filtros

- seleção individual;
- todos e limpar;
- últimos três meses;
- últimos seis meses;
- ano até agora;
- seleção vazia segura;
- filtros compartilháveis pela URL;
- modo apresentação.

## Indicadores adicionais

- população por unidade;
- taxas por 100 colaboradores;
- metas por unidade;
- cumprimento de meta;
- sem estimativas ou valores fictícios.

## Dados e operação

- warehouse opcional via SQLAlchemy;
- SQLite e PostgreSQL;
- logs estruturados em JSON;
- catálogo de métricas;
- módulos separados por responsabilidade;
- documentação de arquitetura, segurança e implantação.

## Qualidade

- 37 testes automatizados;
- cinco páginas testadas;
- Ruff aprovado;
- compilação aprovada;
- servidor Streamlit validado.

## Limitação preservada

O dashboard não inventa cruzamentos ausentes na planilha. Exames e
atendimentos continuam consolidados quando a fonte não informa a unidade.
