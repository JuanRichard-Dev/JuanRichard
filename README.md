# V10.5 Executive Intelligence

A versão V10.5 acrescenta uma visão de diretoria, comparação com metas, recomendações gerenciais, taxas normalizadas, PDF multilíngue e marcos operacionais, mantendo a interface clean e sem inventar métricas não suportadas pela planilha.

Consulte `V10_5_EXECUTIVE_INTELLIGENCE.md` para configuração e limitações.



## V10.4 Premium Board Edition
- Refinamento visual executivo com foco em apresentação institucional.
- Melhor alinhamento, espaçamento e hierarquia visual.
- Cards, tabelas, botões e abas com acabamento premium e leitura mais limpa.
# Dashboard SM CGR 2026 — V10.1.2 Premium AutoSync Stability Hotfix

Dashboard executivo em Streamlit, construído sobre a planilha real do Serviço Médico e preparado para funcionar com experiência visual semelhante a um relatório Power BI.


## Correção V10.1.2 — estabilidade do runtime

Esta revisão trata a queda nativa `Segmentation fault` observada no Streamlit Community Cloud após mudanças de filtro. Como esse tipo de falha encerra o processo fora do tratamento normal de exceções do Python, o pacote foi endurecido em várias camadas:

- runtime direcionado para **Python 3.12.11**;
- dependências principais fixadas em versões exatas e reproduzíveis;
- `pyarrow` fixado e retirado do caminho crítico das tabelas estilizadas;
- tabelas executivas renderizadas como HTML determinístico, preservando o visual;
- pools nativos de NumPy/OpenBLAS/Arrow limitados a uma thread;
- `faulthandler` ativado para registrar stacks de baixo nível caso outra falha nativa ocorra;
- ReportLab carregado somente quando o usuário solicita o PDF;
- autenticação OIDC e warehouse SQL removidos das dependências principais e separados em arquivos opcionais;
- promoção de `last_valid.xlsx` executada apenas uma vez por checksum em cada sessão;
- log estruturado `runtime_environment` com versões efetivamente utilizadas no host;
- teste de estresse com 24 mudanças consecutivas de período.

> Importante: no Streamlit Community Cloud, alterar `.python-version` não muda o Python de um app que já foi criado. Para sair do Python 3.14, exclua e publique novamente o app escolhendo **Python 3.12** em **Advanced settings**.

## Correção V10.1.1

Esta revisão elimina uma condição de corrida na gravação dos snapshots no Streamlit Cloud. Cada execução agora utiliza um arquivo temporário exclusivo antes da promoção atômica, impedindo o `FileNotFoundError` em `os.replace` quando duas sessões ou reruns sincronizam ao mesmo tempo. A mesma proteção foi aplicada a `last_valid.xlsx`, `last_valid.json` e `source_state.json`.

## Principais recursos

- **Google Sheets como fonte padrão**, usando exportação direta em XLSX;
- **AutoSync a cada 120 segundos** enquanto o painel estiver aberto;
- validação contra arquivo vazio, ZIP inválido e páginas HTML de erro/login;
- snapshots imutáveis em `.runtime/snapshots/`, mantendo as 6 versões mais recentes;
- contingência automática por `.runtime/last_valid.xlsx` quando a origem falhar;
- indicação visual `🟠 Contingência ativa`, com horário da última alteração válida;
- painel operacional com fonte, arquivo, verificação, alteração, tamanho, checksum e próxima verificação;
- botão **Sincronizar agora**, que limpa o cache, baixa novamente, valida e recarrega o dashboard;
- tema executivo azul-marinho, cards consistentes, alto contraste e layout responsivo;
- modo apresentação otimizado para reuniões e monitores Full HD/ultrawide;
- suporte alternativo a arquivo local/OneDrive e SharePoint via Microsoft Graph;
- nenhum dado fictício.

## Fonte padrão

```text
https://docs.google.com/spreadsheets/d/1uvtKSQ4PmUcahUhvHEwrqfyeudb1zNto/export?format=xlsx
```

A planilha precisa estar acessível para download. Caso o Google retorne uma página de login ou erro em HTML, o arquivo é rejeitado e a última versão validada permanece ativa.

## Início rápido

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Dependências opcionais:

```powershell
# Microsoft/OIDC
pip install -r requirements-auth.txt

# Warehouse SQL/PostgreSQL
pip install -r requirements-warehouse.txt
```

Acesse `http://127.0.0.1:8501`.

## Configuração

Copie `.streamlit/secrets.toml.example` para `.streamlit/secrets.toml` ou use variáveis de ambiente.

```toml
DATA_SOURCE = "google_sheets"
DATA_URL = "https://docs.google.com/spreadsheets/d/1uvtKSQ4PmUcahUhvHEwrqfyeudb1zNto/export?format=xlsx"
AUTO_REFRESH_ENABLED = true
AUTO_REFRESH_SECONDS = 120
KEEP_SOURCE_SNAPSHOTS = 6
```

Para usar arquivo local/OneDrive:

```toml
DATA_SOURCE = "local"
DATA_LOCAL_PATH = "C:/caminho/Dashboard SM CGR 2026.xlsx"
```

## Contingência

1. A origem é baixada e validada como XLSX.
2. O parser completo do dashboard valida estrutura, abas e dados.
3. Somente depois o arquivo é promovido para `.runtime/last_valid.xlsx`.
4. Se uma atualização falhar, o dashboard usa a última versão válida e mantém o AutoSync tentando recuperar a origem.

## Segurança

- o dashboard não escreve na planilha de origem;
- `.streamlit/secrets.toml` e `.runtime/` são ignorados pelo Git;
- os arquivos de saúde devem permanecer na infraestrutura aprovada;
- a porta 8501 não deve ser exposta diretamente à internet sem autenticação e proxy seguro.

## Testes

```powershell
python -m pytest -q
```
