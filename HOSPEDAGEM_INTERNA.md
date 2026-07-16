# Hospedagem interna — OneDrive, SharePoint e Streamlit

## Arquitetura

SharePoint → OneDrive sincronizado → snapshot local seguro → Streamlit interno.

A aplicação nunca modifica a planilha original. Ela cria uma cópia imutável em
`.runtime/snapshots` e usa essa cópia durante cada carga.

## Instalação inicial

Abra o PowerShell na pasta do projeto:

```powershell
powershell -ExecutionPolicy Bypass -File .\CONFIGURAR_HOST_INTERNO.ps1
```

O script usa como padrão:

```text
C:\Users\SEU_USUARIO\OneDrive - MFP Michelin\Dashboard SM CGR 2026.xlsx
```

Também é possível informar outro caminho:

```powershell
powershell -ExecutionPolicy Bypass -File .\CONFIGURAR_HOST_INTERNO.ps1 `
  -WorkbookPath "C:\caminho\Dashboard SM CGR 2026.xlsx"
```

## Teste local

Execute:

```text
INICIAR_LOCAL.bat
```

Abra `http://127.0.0.1:8501`.

## Acesso pela rede

Somente após autorização do TI, execute:

```text
INICIAR_REDE_INTERNA.bat
```

O TI deve liberar TCP 8501 apenas na rede corporativa. O endereço será:

```text
http://NOME-DO-COMPUTADOR:8501
```

Não publique a porta 8501 na internet.

## Inicialização automática

Para iniciar após o logon da conta hospedeira:

```powershell
powershell -ExecutionPolicy Bypass -File .\INSTALAR_INICIALIZACAO_AUTOMATICA.ps1
```

Essa tarefa depende de a conta estar conectada. Para execução permanente sem
logon, solicite ao TI uma VM/servidor e uma conta de serviço.

## Atualização automática

A cada 120 segundos, uma função isolada verifica a data e o tamanho do arquivo
original. Quando detecta alteração:

1. limpa os caches;
2. executa novamente o aplicativo;
3. aguarda o arquivo ficar estável;
4. cria um snapshot;
5. valida e recalcula todo o dashboard.

O intervalo pode ser alterado em `.streamlit/secrets.toml`:

```toml
AUTO_REFRESH_SECONDS = 120
```

## Diagnóstico

```powershell
powershell -ExecutionPolicy Bypass -File .\DIAGNOSTICAR_HOST_INTERNO.ps1
```

O diagnóstico verifica caminho, OneDrive, Python, porta, health check e IPs.
