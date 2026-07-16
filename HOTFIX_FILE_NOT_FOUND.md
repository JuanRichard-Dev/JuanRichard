# Hotfix V10.1.1 — FileNotFoundError no AutoSync

## Sintoma

O Streamlit Cloud encerrava a execução em `os.replace(temporary, target)` dentro de `src/data_sources.py`.

## Causa

Sessões e reruns simultâneos utilizavam o mesmo caminho temporário, por exemplo:

```text
dashboard-<checksum>.xlsx.tmp
```

Quando uma execução movia esse arquivo primeiro, a segunda já não o encontrava.

## Correção

- temporários exclusivos com `tempfile.mkstemp`;
- temporário criado no mesmo diretório do arquivo final;
- promoção atômica com `os.replace`;
- proteção aplicada a snapshots, `last_valid.xlsx`, `last_valid.json` e `source_state.json`;
- falha de persistência passa a ativar contingência, sem derrubar o dashboard.

## Deploy

Substitua os arquivos do repositório pelo conteúdo deste pacote, faça commit/push e reinicie o aplicativo no Streamlit Cloud. As configurações e secrets existentes podem ser mantidos.
