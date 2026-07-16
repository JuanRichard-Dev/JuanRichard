## V10.5.5 — Health Chart Restored
- Restaurado o anel visual do Índice de Saúde Ocupacional.
- Componentes mantidos ao lado em notebook/desktop.
- Renomeado Presença no Trabalho para Presença no Periódico.

## V10.5.4 — Chart Titles & Clean Health
- Corrigido corte vertical dos títulos em todos os gráficos.
- Simplificado o Índice de Saúde Ocupacional para dois componentes ativos.
- Removidas metas, badges de status e classificação Crítico na seção.
- Renomeado Ausência de Faltas para Presença no Trabalho.

## V10.5.3 Responsive Prompt Upgrade
- Responsividade notebook-first com reflow de gráficos e KPIs.
- Alturas, margens e legendas Plotly calculadas pelo conteúdo.
- Correção profunda de Composição Mensal e Horistas versus Mensalistas.
- Remoção de Conferir impacto dos filtros, Fonte e cobertura e Dicionário de métricas.
- Estados escuros consistentes em filtros e preservação do controle nativo da sidebar.

## V10.5.2 Fine Visual Polish
- Polimento visual fino com foco em hierarquia, espaçamento e consistência.
- Ajuste de alturas dos cards e respiro adicional entre blocos.
- Refino dos containers de gráficos, tabs e tabela.

## V10.5.1 Layout Polish
- Ajustes visuais e de espaçamento em tabelas e gráficos.
- Correção do corte da última linha na matriz de atendimentos.
- Refino de layout no Pareto, composição e fluxo mensal.

## V10.5 Executive Intelligence

- Nova página Resumo Executivo para diretoria.
- Comparação atual, anterior, meta e status.
- Prioridades gerenciais e indicador de severidade agregado.
- Taxas por 100 colaboradores condicionadas à população configurada.
- Português, Inglês e Francês na visão executiva e no PDF.
- Marcos operacionais opcionais com hover nos gráficos.
- Tooltips de definição nos KPIs e painel de confiabilidade dos dados.

## V10.4.1 Interactive Hover
- Hover de inspeção reativado sem liberar zoom ou arraste.
- Tooltips aprimorados para histórico, média móvel e projeções.
- Faixa estimada disponível no tooltip da projeção.
- Linha-guia discreta para leitura precisa do mês.

## V10.2.1 Dependency Hotfix
- `requirements.txt` reorganizado e mantido na raiz.
- Plotly declarado explicitamente como dependência principal.
- Verificação amigável de dependências antes dos imports locais.
- Pacote Root Ready sem pasta intermediária.

## V10.2 Executive Clean Fix
- Simplificação visual executiva e foco no essencial.
- Correção do KeyError em Afastamentos / Dias perdidos.
- Gráficos bloqueados para apresentação (sem zoom/arraste).
- Pareto reorganizado para evitar sobreposição de rótulos.

# Changelog

## V10.1.2 Premium AutoSync Stability Hotfix

- Runtime de produção direcionado para Python 3.12.11.
- Dependências principais fixadas em versões exatas para builds reproduzíveis.
- Streamlit fixado em 1.58.0 e PyArrow em 20.0.0.
- Tabelas pandas estilizadas passaram a ser renderizadas como HTML determinístico, retirando serialização Arrow do fluxo mais frequente de filtros.
- NumPy/OpenBLAS/MKL/NumExpr/Arrow limitados a uma thread por processo.
- `faulthandler` habilitado antes de importar bibliotecas nativas.
- Log `runtime_environment` adicionado com Python, arquitetura e versões instaladas.
- ReportLab passou a ser importado somente ao gerar o relatório PDF.
- OIDC e warehouse SQL foram separados em `requirements-auth.txt` e `requirements-warehouse.txt`.
- A cópia `last_valid` não é regravada em toda interação quando o checksum já foi promovido na sessão.
- Adicionado teste de estresse com 24 mudanças consecutivas de filtros.
- Suíte final: 59 testes aprovados e health check HTTP confirmado.

## V10.1.1 Premium AutoSync Hotfix

- Corrigida condição de corrida entre sessões/reruns simultâneos do Streamlit Cloud.
- Arquivos temporários agora recebem nomes exclusivos no mesmo filesystem do destino.
- Gravações de snapshot, `last_valid.xlsx`, metadados e estado remoto são atômicas.
- Falhas de persistência do snapshot são convertidas em contingência controlada.
- Falha ao atualizar a cópia de contingência não derruba dados já carregados.
- Limpeza dos snapshots foi protegida contra exclusões concorrentes.
- Testes de concorrência adicionados com 48 gravações simultâneas.
- Testes de interface passaram a usar fonte local isolada para execução determinística.

## V10.1 Premium AutoSync

- Google Sheets definido como fonte remota padrão.
- AutoSync remoto e local configurado para 120 segundos.
- Rejeição explícita de HTML de login/erro e de XLSX estruturalmente inválido.
- Retenção de 6 snapshots em `.runtime/snapshots/`.
- Promoção segura para `.runtime/last_valid.xlsx` somente após o parser completo.
- Recuperação automática da origem mesmo quando o painel está em contingência.
- Painel de status com fonte, arquivo, verificação, alteração, tamanho, checksum e próxima execução.
- Botão Sincronizar agora com limpeza de cache, download, validação e feedback.
- Nova paleta executiva azul-marinho e componentes visuais inspirados no Power BI.
- Modo apresentação revisado para Full HD e ultrawide.
- Testes de regressão para validação de payload, retenção e identidade visual.

## V10 Responsive Health

- Gauge semicircular substituído por um indicador radial completo.
- Zonas de desempenho e status incorporados ao gráfico.
- Composição do índice convertida em cartões analíticos responsivos.
- Resultado, meta, peso, pontos e distância passam a ser vistos sem tabela horizontal.
- Seção do índice passa a empilhar automaticamente em notebooks e tablets.
- Cards de composição passam para uma coluna em telas estreitas.
- Canvas principal ampliado para aproveitar melhor monitores Full HD e ultrawide.
- Altura do gráfico adaptada para desktop, tablet e celular.
- Testes de regressão adicionados para gráfico e breakpoints.

# Changelog

## V9 Internal AutoSync

- Fonte local/OneDrive lida por snapshot imutável.
- Leitura com repetição e verificação de estabilidade.
- Atualização automática configurável.
- Cópia de contingência da última versão válida.
- Metadados adicionais de origem e sincronização.
- Botão Verificar agora limpa todos os caches.
- Scripts Windows para configuração, execução, diagnóstico e tarefa agendada.
- Configuração explícita de XSRF e CORS.
- Novos testes de hospedagem interna.
- Arquivos temporários e snapshots ignorados pelo Git.

# Changelog

## 8.0.0 — Deploy Ready

- Deploy para Streamlit Community Cloud, Render e Docker.
- Autenticação opcional por senha ou Microsoft Entra ID/OIDC.
- Autorização por unidade e allow-list de e-mails.
- Fontes local, URL e SharePoint via Microsoft Graph.
- PDF executivo com KPIs, alertas, tendência e ranking.
- Filtros persistidos em URL compartilhável.
- Modo apresentação.
- Últimos 6 meses e ano até agora.
- População por unidade e taxas normalizadas opcionais.
- Warehouse SQL opcional.
- Logs estruturados.
- CI com GitHub Actions e Ruff.
- Dockerfile, Render Blueprint, Procfile e health check.
- Dicionário de métricas dentro da aplicação.
- Arquivos de arquitetura, segurança e deploy.

## 7.0.0

- Melhorias de estabilidade, filtros, gráficos, cache e qualidade da fonte.
