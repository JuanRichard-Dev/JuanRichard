# Automação local: Excel → Google Drive

Este processo roda **no computador que possui o Excel local**, verifica a planilha a cada 10 minutos e atualiza um único arquivo no Google Drive somente quando o conteúdo mudou. A leitura é protegida contra arquivos parcialmente salvos: tamanho, data de modificação e estrutura ZIP/XLSX precisam estar estáveis antes do envio.

## 1. Preparar o Google Drive

1. Crie um projeto no Google Cloud e ative a **Google Drive API**.
2. Crie uma conta de serviço e baixe o JSON de credenciais.
3. Crie ou escolha uma pasta no Google Drive.
4. Compartilhe essa pasta com o e-mail da conta de serviço com permissão **Editor**. Não publique o arquivo e não coloque o JSON no GitHub.
5. Copie o ID da pasta a partir da URL do Drive. O ID do arquivo é opcional: se não for informado, o script procura pelo nome e cria o arquivo na primeira execução.

## 2. Instalar no Windows

No PowerShell, dentro desta pasta:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Edite `.env` com o caminho absoluto da planilha e o caminho absoluto do JSON da conta de serviço. O script não carrega `.env` automaticamente de propósito; no PowerShell, carregue as variáveis antes de executar ou defina-as no Agendador de Tarefas. Uma forma simples para teste é:

```powershell
$env:LOCAL_XLSX_PATH = 'C:\Dados\Dashboard SM CGR 2026.xlsx'
$env:GOOGLE_SERVICE_ACCOUNT_FILE = 'C:\Dados\google-service-account.json'
$env:GOOGLE_DRIVE_FOLDER_ID = 'ID_DA_PASTA'
$env:SYNC_INTERVAL_SECONDS = '600'
py .\sync_excel_to_drive.py
```

Para testar uma única vez:

```powershell
py .\sync_excel_to_drive.py --once
```

O loop contínuo deve ser executado com uma conta de usuário que permaneça ativa. Para iniciar com o Windows, use o **Agendador de Tarefas** configurado para executar `python.exe` no ambiente virtual e iniciar em `google_drive_sync`; ou mantenha o processo contínuo como uma tarefa de inicialização. Não configure simultaneamente loop contínuo e uma tarefa a cada 10 minutos, pois isso gera concorrência desnecessária.

## 3. Configurar o dashboard Streamlit

A versão atual do dashboard foi ajustada para aceitar uma fonte privada do Google Drive, sem SharePoint:

```toml
DATA_SOURCE = "google_drive"
DATA_GOOGLE_DRIVE_FILE_ID = "ID_DO_ARQUIVO"
GOOGLE_SERVICE_ACCOUNT_JSON = "{ ... JSON da conta de serviço ... }"
AUTO_REFRESH_SECONDS = 600
```

No Render, coloque os valores em **Environment Variables/Secrets**, nunca no repositório. A conta de serviço usada pelo dashboard também precisa ter acesso de leitura ao arquivo. O dashboard gera um token temporário para cada leitura; nenhuma chave privada é enviada ao navegador.

O `AUTO_REFRESH_SECONDS` controla a frequência de consulta do arquivo remoto. O Streamlit também passa a executar um rerun automático no mesmo intervalo, portanto o painel reflete o novo arquivo sem depender de o usuário clicar em “Sincronizar”. O botão manual continua disponível.

## Segurança e operação

Adicione ao `.gitignore` local: `.env`, `*.json`, `.google_drive_sync.sha256` e qualquer log com credenciais. Se a planilha contém dados pessoais ou de saúde, mantenha o arquivo privado no Drive e use uma conta de serviço com acesso somente à pasta necessária. O script nunca substitui o arquivo se a validação do XLSX falhar e tenta novamente no ciclo seguinte.
