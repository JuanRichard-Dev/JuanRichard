# Melhorias implementadas — V9 Internal AutoSync

## Fonte e sincronização

- Leitura direta da planilha sincronizada pelo OneDrive.
- O arquivo original é somente leitura para o dashboard.
- Verificação automática da origem a cada dois minutos.
- Botão **Verificar agora** para atualização imediata.
- Detecção por data de modificação e tamanho do arquivo.
- Metadados de origem, checksum, tamanho e horário exibidos no painel.

## Segurança da leitura

- Espera até que a planilha pare de mudar durante a sincronização.
- Repetição automática quando o OneDrive ainda está substituindo o arquivo.
- Validação de que o conteúdo recebido é realmente um XLSX.
- Criação de snapshot imutável antes de processar os dados.
- O dashboard nunca calcula diretamente sobre um arquivo em gravação.

## Contingência

- Armazena automaticamente a última versão validada.
- Se a fonte ficar indisponível ou inválida, mantém o painel operacional.
- Exibe aviso claro quando está usando a cópia de contingência.
- Mantém quantidade limitada de snapshots para não ocupar espaço sem controle.

## Hospedagem interna

- Script de configuração automática do computador hospedeiro.
- Inicialização somente local em `127.0.0.1`.
- Inicialização na rede interna em `0.0.0.0`.
- Script para instalar inicialização automática após o logon.
- Script para remover a tarefa agendada.
- Diagnóstico de planilha, OneDrive, Python, porta, health check e IP.
- Documentação específica para firewall, TI e operação interna.

## Segurança operacional

- Proteção XSRF e CORS explicitamente habilitadas.
- `.runtime` e `secrets.toml` excluídos do Git.
- Logs estruturados opcionais sem conteúdo clínico da planilha.
- Nenhuma senha ou credencial real incluída no projeto.
- A porta 8501 não deve ser publicada na internet.

## Interface e experiência

- Status da atualização automática na barra lateral.
- Estado de contingência visível.
- Origem monitorada disponível em **Fonte e cobertura**.
- Notificação quando uma nova versão é detectada.
- Filtros e página atual são preservados após atualização automática.

## Validação

- Planilha real utilizada.
- Nenhum dado fictício incluído.
- Testes de snapshots e recuperação adicionados.
- Testes de filtros, cálculos, páginas e relatórios mantidos.
