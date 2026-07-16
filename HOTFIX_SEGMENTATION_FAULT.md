# Hotfix V10.1.2 — Segmentation fault no Streamlit Cloud

## Evidência do log

O processo iniciou corretamente, carregou a fonte Google Sheets e respondeu a diversas interações. Aproximadamente 21 minutos depois, uma mudança no filtro de meses foi registrada e o processo foi encerrado pelo sistema operacional com:

```text
Segmentation fault
```

Não houve traceback Python. Portanto, a falha ocorreu em código nativo, no interpretador ou em uma extensão compilada, e não em uma exceção comum tratável com `try/except`.

O mesmo log mostrou:

```text
Python 3.14.6
Streamlit 1.59.1
NumPy 2.5.1
PyArrow 25.0.0
```

O repositório anterior declarava Python 3.12, mas o app já existente no Community Cloud continuava preso ao Python selecionado no momento da criação.

## Limite da conclusão

Sem core dump ou stack nativa não é possível afirmar qual biblioteca provocou o SIGSEGV. A correção reduz simultaneamente os caminhos de maior risco e torna uma eventual reincidência diagnosticável.

## Mudanças aplicadas

1. Python alvo fixado em 3.12.11.
2. Dependências principais com versões exatas.
3. Streamlit 1.58.0 e PyArrow 20.0.0.
4. Tabelas estilizadas renderizadas como HTML, sem `st.dataframe` no fluxo principal.
5. Pools nativos de NumPy/OpenBLAS/MKL/NumExpr/Arrow limitados a uma thread.
6. `faulthandler` habilitado antes de pandas, NumPy, PyArrow e Streamlit.
7. ReportLab importado apenas quando o PDF é solicitado.
8. OIDC, SQLAlchemy, psycopg e greenlet removidos do runtime principal.
9. Promoção da contingência limitada a uma vez por checksum por sessão.
10. Evento `runtime_environment` adicionado aos logs.
11. Teste de estresse com 24 mudanças consecutivas no filtro de meses.

## Procedimento obrigatório no Streamlit Community Cloud

A versão do Python de um app já publicado não é alterada por commit, `.python-version` ou reboot.

1. Anote subdomínio, secrets, repositório, branch e arquivo principal.
2. Exclua o app atual.
3. Publique novamente.
4. Em **Advanced settings**, selecione **Python 3.12**.
5. Restaure os secrets e o subdomínio.
6. Confirme no log:

```json
{"event":"runtime_environment","python":"3.12.x"}
```

Se o log ainda mostrar Python 3.14, o app não foi recriado com o runtime correto.

## Dependências opcionais

O runtime principal foi reduzido para evitar módulos nativos sem uso.

- Microsoft/OIDC: `requirements-auth.txt`
- Warehouse SQL/PostgreSQL: `requirements-warehouse.txt`

Use esses arquivos somente quando os recursos correspondentes estiverem realmente ativados.
