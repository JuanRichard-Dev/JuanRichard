# Segurança e privacidade

## Regras obrigatórias

- Não coloque senhas, client secrets ou tokens no GitHub.
- Não envie `.streamlit/secrets.toml` para o repositório.
- Use repositório privado para dados corporativos.
- Prefira Microsoft Entra ID/OIDC para uso corporativo.
- Restrinja usuários com `ALLOWED_EMAILS`.
- Configure unidades por e-mail quando um gestor não puder visualizar todas.
- Não torne o app público enquanto o Excel real estiver incluído no repositório.

## Modos de autenticação

### `AUTH_MODE=off`

Use somente quando o próprio provedor já protege o acesso, por exemplo um app
privado do Streamlit Community Cloud ou uma rede corporativa.

### `AUTH_MODE=password`

Barreira simples para demonstração. Armazene `APP_PASSWORD` em secrets.

### `AUTH_MODE=oidc`

Recomendado. O login é realizado pelo Microsoft Entra ID usando os comandos
nativos `st.login`, `st.user` e `st.logout`.

## Autorização por unidade

No bloco `[authorization]`, associe e-mails às unidades. Contas administrativas
podem acessar tudo; gestores podem ser limitados a B2BN, B2BF, SF, SITE ou OUTROS.

## Logs

O dashboard envia eventos estruturados ao stdout. Em Render/Docker, esses logs
podem ser coletados pelo provedor. Para gravar JSONL localmente:

```toml
AUDIT_FILE_ENABLED = true
AUDIT_FILE_PATH = "logs/audit.jsonl"
```

O sistema não registra conteúdo clínico individual porque a planilha atual é
consolidada.
