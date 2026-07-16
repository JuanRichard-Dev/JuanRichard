# Arquitetura V8

```text
Fonte Excel
  ├─ arquivo local
  ├─ URL autenticada
  └─ SharePoint / Microsoft Graph
          ↓
src/data_sources.py
          ↓
src/data_loader.py
          ↓
Validação + camada semântica
          ↓
KPIs / filtros / gráficos / PDF
          ↓
Streamlit
          ├─ Community Cloud
          ├─ Render
          └─ Docker
```

## Camadas

- `src/data_sources.py`: resolve e baixa a fonte.
- `src/data_loader.py`: interpreta as três abas reais.
- `src/semantic.py`: padroniza as estruturas analíticas.
- `src/transforms.py`: cálculos de negócio.
- `src/analytics.py`: rankings, narrativas, comparações e projeções.
- `src/charts.py`: figuras Plotly.
- `src/components.py`: componentes visuais.
- `src/auth.py`: autenticação e autorização.
- `src/population.py`: indicadores normalizados por população.
- `src/unit_targets.py`: metas opcionais específicas por unidade.
- `src/reporting.py`: relatório executivo em PDF.
- `src/warehouse.py`: espelhamento opcional em banco SQL.
- `src/audit.py`: eventos estruturados.

## Limitações da fonte atual

Exames e atendimentos não possuem abertura por unidade na planilha. O dashboard
não inventa esse cruzamento. Taxas por população só aparecem quando
`population_by_unit.csv` contém valores reais positivos.
