# Implementação — V10.1 Premium AutoSync

## Fluxo de sincronização

`src/data_sources.py` resolve a fonte configurada, baixa ou lê o XLSX, rejeita HTML e arquivos inválidos, calcula SHA-256 e cria um snapshot imutável. `src/auto_refresh.py` executa a verificação periódica e solicita um rerun quando detecta nova versão.

## Estados operacionais

- `🟢 AutoSync ativo`: origem acessível e versão atual carregada.
- `🟡 Verificação com alerta`: falha transitória, mantendo a versão atualmente carregada.
- `🟠 Contingência ativa`: origem atual não pôde ser validada e o painel está usando `.runtime/last_valid.xlsx`.

## Retenção

A variável `KEEP_SOURCE_SNAPSHOTS` mantém no mínimo 5 snapshots; o valor recomendado e configurado é 6.

## Validação

A validação técnica exige:

- assinatura ZIP `PK`;
- arquivo ZIP íntegro;
- presença de `[Content_Types].xml`;
- presença da estrutura `xl/`;
- ausência de resposta HTML.

Depois, `load_all_data()` executa a validação semântica do workbook antes da promoção para a contingência.

## Identidade visual

- fundo principal `#081321`;
- fundo secundário `#0D1D31`;
- cards `#10243B`;
- cards em destaque `#142A45`;
- texto principal `#F4F8FC`;
- texto secundário `#B8C7D9`;
- azul principal `#4A8DFF`.
