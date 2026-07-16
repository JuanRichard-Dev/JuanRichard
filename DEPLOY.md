# Guia de deploy


## Obrigatório para este hotfix: recriar o app com Python 3.12

O log que motivou a V10.1.2 mostrou que o app existente estava sendo executado com **Python 3.14.6**, embora o repositório declarasse Python 3.12. No Community Cloud, a versão do interpretador é escolhida quando o app é criado e não muda apenas com commit ou reboot.

1. Salve o subdomínio atual, os secrets e as coordenadas do GitHub.
2. Em **Manage app**, abra o menu `...` e escolha **Delete app**.
3. Crie o app novamente com o mesmo repositório, branch e `app.py`.
4. Abra **Advanced settings**.
5. Selecione **Python 3.12**.
6. Reinsira os secrets.
7. Use o mesmo subdomínio e conclua o deploy.
8. No novo log, confirme a linha `runtime_environment` com `"python": "3.12..."`.

Arquivos `.python-version` e `runtime.txt` também foram incluídos para hosts que os respeitam, mas a seleção em **Advanced settings** é a etapa decisiva no Streamlit Community Cloud.

## Recomendação principal: Streamlit Community Cloud

É o caminho mais simples para gerar um link e compartilhar o dashboard.

1. Crie um repositório **privado** no GitHub.
2. Envie todos os arquivos deste projeto.
3. Acesse `https://share.streamlit.io`.
4. Clique em **Create app**.
5. Escolha o repositório, a branch e `app.py`.
6. Defina um subdomínio.
7. Em **Advanced settings / Secrets**, copie as configurações necessárias a partir de `.streamlit/secrets.toml.example`.
8. Mantenha o app privado e convide seu chefe pelo e-mail corporativo, ou configure Microsoft Entra ID.

Documentação oficial:
- https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app
- https://docs.streamlit.io/deploy/streamlit-community-cloud/share-your-app

### Configuração mínima

Nenhum secret é necessário quando o Excel está versionado no repositório e o app
fica privado no Streamlit Community Cloud:

```toml
DATA_SOURCE = "local"
AUTH_MODE = "off"
```

Para adicionar uma segunda barreira de proteção:

```toml
DATA_SOURCE = "local"
AUTH_MODE = "password"
APP_PASSWORD = "uma-senha-forte"
```

## Microsoft Entra ID

No Azure/Entra, registre um aplicativo Web e use como redirect URI:

```text
https://SEU-APP.streamlit.app/oauth2callback
```

Nos secrets:

```toml
AUTH_MODE = "oidc"
ALLOWED_EMAILS = "chefe@empresa.com,voce@empresa.com"

[auth]
redirect_uri = "https://SEU-APP.streamlit.app/oauth2callback"
cookie_secret = "CHAVE_LONGA_ALEATORIA"

[auth.microsoft]
client_id = "CLIENT_ID"
client_secret = "CLIENT_SECRET"
server_metadata_url = "https://login.microsoftonline.com/TENANT_ID/v2.0/.well-known/openid-configuration"
```

Documentação oficial:
- https://docs.streamlit.io/develop/tutorials/authentication/microsoft

## Render

Este projeto inclui `render.yaml`.

1. Envie o projeto para o GitHub.
2. No Render, clique em **New > Blueprint**.
3. Selecione o repositório.
4. Adicione os secrets no painel de Environment.
5. Faça o deploy.

O comando de inicialização já está configurado:

```bash
streamlit run app.py --server.address 0.0.0.0 --server.port $PORT
```

A verificação de saúde usa:

```text
/_stcore/health
```

## Docker

```bash
docker build -t dashboard-sm-cgr .
docker run --rm -p 8501:8501 \
  -e DATA_SOURCE=local \
  -e AUTH_MODE=password \
  -e APP_PASSWORD='senha-forte' \
  dashboard-sm-cgr
```

Abra `http://localhost:8501`.

## SharePoint

Configure uma aplicação no Microsoft Entra com acesso ao Microsoft Graph e
forneça:

```toml
DATA_SOURCE = "sharepoint"
MS_TENANT_ID = "..."
MS_CLIENT_ID = "..."
MS_CLIENT_SECRET = "..."
MS_DRIVE_ID = "..."
MS_ITEM_ID = "..."
```

A aplicação baixa o arquivo pelo Graph e mantém cache por cinco minutos.

## Fonte por URL

```toml
DATA_SOURCE = "url"
DATA_URL = "https://servidor/arquivo.xlsx"
# DATA_BEARER_TOKEN = "token-opcional"
```

## Banco de dados opcional

Antes do deploy com warehouse, instale `requirements-warehouse.txt` em vez do arquivo principal isolado. No Community Cloud, mescle essas duas dependências no `requirements.txt` ou substitua o conteúdo conforme a necessidade.

A V8 pode espelhar as tabelas normalizadas em um banco SQL:

```toml
WAREHOUSE_ENABLED = true
DATABASE_URL = "postgresql+psycopg://usuario:senha@host:5432/banco"
```

Para SQLite:

```toml
WAREHOUSE_ENABLED = true
DATABASE_URL = "sqlite:///dashboard.db"
```

## Por que não Vercel

Vercel é excelente para aplicações serverless/ASGI/WSGI, mas Streamlit utiliza
uma sessão Python persistente e comunicação por WebSocket. Para este projeto,
Streamlit Community Cloud, Render ou Docker são opções mais previsíveis. Uma
migração real para Vercel exigiria reescrever a interface em Next.js/React e
transformar o Python em uma API separada.

## População e metas por unidade

Os arquivos `population_by_unit.csv` e `unit_targets.csv` são enviados vazios de
valores para evitar dados fictícios. Preencha somente com valores corporativos
reais. As análises normalizadas e as tabelas de cumprimento de metas aparecem
automaticamente quando os arquivos possuem números válidos.
