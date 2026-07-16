# Operação, contingência e recuperação

## Cópia de contingência

Após cada carregamento válido, o sistema mantém:

```text
.runtime/last_valid.xlsx
.runtime/last_valid.json
```

Se o OneDrive estiver sincronizando, o arquivo desaparecer temporariamente ou
uma nova versão estiver inválida, o dashboard continua exibindo a última versão
validada e mostra um aviso explícito.

## Snapshots

Os snapshots imutáveis ficam em:

```text
.runtime/snapshots/
```

Por padrão são mantidos os seis mais recentes. Eles não são enviados ao GitHub.

## Recuperar a fonte principal

1. confirme que o OneDrive está aberto;
2. confirme que o arquivo possui ícone verde;
3. feche o Excel se houver conflito de gravação;
4. clique em **Verificar agora** no dashboard;
5. confira o painel **Fonte e cobertura**.

## Logs

Quando habilitado, o log estruturado fica em:

```text
.runtime/logs/audit.jsonl
```

O log não grava o conteúdo da planilha.

## Atualização do projeto

Antes de substituir uma versão:

1. encerre o Streamlit;
2. preserve `.streamlit/secrets.toml`;
3. extraia a nova versão em outra pasta;
4. copie apenas o `secrets.toml`;
5. execute os testes;
6. inicie localmente;
7. somente então substitua o host oficial.
