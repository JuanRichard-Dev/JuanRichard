# V10.2.1 — Correção de dependências no Streamlit Cloud

## Causa do erro

O erro `ModuleNotFoundError` em `import plotly.graph_objects as go` ocorre quando o
Streamlit Cloud não instala o pacote Plotly. O arquivo `requirements.txt` precisa
estar exatamente na raiz do repositório, no mesmo nível de `app.py`.

## Estrutura correta no GitHub

```text
vtt/
├── app.py
├── requirements.txt
├── runtime.txt
├── .python-version
├── Dashboard SM CGR 2026.xlsx
└── src/
    ├── charts.py
    └── ...
```

Não deixe esses arquivos dentro de outra pasta como
`Dashboard-main-V10.2.1-Dependency-Hotfix/` dentro do repositório.

## Atualização

1. Apague ou substitua o conteúdo atual do repositório.
2. Extraia o ZIP Root Ready.
3. Envie **todos os arquivos extraídos diretamente para a raiz** do repositório.
4. Confirme no GitHub que `app.py` e `requirements.txt` aparecem lado a lado.
5. Faça commit e push.
6. No Streamlit Cloud, use **Manage app → Reboot app**.
7. Se o log não mostrar a instalação do Plotly, exclua somente o app publicado e
   faça o deploy novamente com Python 3.12.

## Linha esperada no log

```text
+ plotly==6.5.2
```

## Dependências principais

```text
plotly==6.5.2
streamlit==1.58.0
pandas==2.3.3
numpy==2.3.5
pyarrow==20.0.0
openpyxl==3.1.5
reportlab==4.4.10
requests==2.32.5
```
