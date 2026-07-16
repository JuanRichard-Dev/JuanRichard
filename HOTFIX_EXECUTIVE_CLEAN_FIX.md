# V10.2 Executive Clean Fix

## Principais melhorias
- Correção do erro `KeyError: Mês anterior` na página de Afastamentos.
- Cabeçalho executivo simplificado, com foco em período, atualização e status da fonte.
- Barra de status da fonte reduzida ao essencial, com detalhes técnicos mantidos na lateral.
- Cartão de escopo aplicado simplificado.
- Texto e tipografia com contraste mais alto para melhor leitura em apresentações.
- Gráficos Plotly em modo estático: sem zoom, sem arrastar, sem alteração pelo mouse.
- Pareto de atendimentos e motivos reorganizado: mais espaço, rótulos quebrados e legenda reposicionada.
- Matriz por unidade simplificada para leitura mais objetiva.
- Exibição de anomalias históricas apenas em situações realmente relevantes fora do modo apresentação.

## Validação
- `python -m py_compile app.py src/*.py`
- `pytest -q tests/test_app_integration.py tests/test_app_smoke.py tests/test_month_filter_controls.py tests/test_dashboard_focus.py`
- Resultado: **10 testes aprovados**
