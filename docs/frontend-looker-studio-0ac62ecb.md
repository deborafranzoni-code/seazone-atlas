<!-- title: Frontend (Looker Studio) | url: https://outline.seazone.com.br/doc/frontend-looker-studio-VzETeGXTuw | area: Tecnologia -->

# Frontend (Looker Studio)

**Projeto:** Dashboard de Observabilidade (Lake) 

**Fonte de Dados:** Google BigQuery (`lake_observability`) 

**Status do Backend:** ✅ Concluído (Tabelas populadas) 

**Foco:** Construção de Interface e UX


---

## 1. Objetivo da Visualização

Transformar as tabelas técnicas migradas da AWS para o BigQuery em um painel gerencial e operacional. O painel deve substituir integralmente o Power BI atual, eliminando a necessidade de consulta aos logs brutos para verificações de rotina.

**Diferencial:** O painel deve refletir a nova arquitetura orientada a dados, onde `scrapers_health` e métricas de MAPE são as fontes da verdade.


---

## 2. Mapeamento de Fontes de Dados (Backend $\to$ Frontend)

Para o desenvolvedor do Looker Studio, estas são as conexões exatas que devem ser feitas.

| Requisito do Discovery (RF) | Tabela Entregue (BigQuery) | Observação para o Frontend |
|:---|:---|:---|
| **RF01 - Saúde dos Scrapers** | `lake_observability.scrapers_health` | Filtrar onde `status = 'sucesso'` vs `falha`. |
| **RF02 - Volume de Dados** | `lake_observability.scrapers_health` | Usar campos `rows_inserted` e comparar com D-1. |
| **RF03 - MAPE (Receita)** | lake_observability.revenue_mape_report_last_days<br>lake_observability.revenue_mape_report_last_years | Criar gráficos de linha temporal. |
| **RF03 - MAPE (Preço Médio)** | `lake_observability.priceav_mape_report` | Monitorar desvios na coluna `average_price`. |
| **RF04 - Anomalias** | lake_observability.anomaly_mape_report<br>lake_observability.anomaly_price_antecedence | Cards de contagem de alertas. |
| **RF05 - OLX/Vivareal** | `lake_observability.scrapers_health` (Validar) | **Atenção:** Filtrar `source IN ('olx', 'vivareal')` e aplicar regra de data mensal. |


---

## 3. Estrutura do Dashboard (Sitemap)

O painel será composto por **3 Páginas Principais**, organizadas por nível de detalhe.

### 🏠 Página 1: Visão Geral (Overview & Health)

*Publico-alvo: Liderança e DataOps (Check rápido matinal)*

**1. Cabeçalho:**

* Data da última atualização (Max Timestamp das tabelas).
* **KPI Principal:** % de Saúde Global dos Scrapers (Hoje).

**2. Seção: Ingestão de Dados (RF01 e RF02)**

* **Gráfico de Barras:** Status dos Scrapers por Container (Sucesso vs Falha).
  * *Regra de Visualização:* Agrupar "Internals" como um único container se necessário.
* **Tabela de Volumetria Crítica:** Listar tabelas onde `rows_inserted` caiu > 20% em relação a ontem (D-1).
  * *Formatação Condicional:* Vermelho se Variação < -20%.

**3. Seção: Qualidade de Negócio (RF03)**

* **Scorecards:** MAPE Médio de Faturamento (Últimos 15 dias) e MAPE Médio de Preço.
* **Alerta de Anomalias:** Cartão grande exibindo número de anomalias detectadas hoje (RF04).


---

### 📉 Página 2: Métricas de Qualidade (MAPE & Revenue)

*Publico-alvo: Analistas de Pricing/Revenue*

**1. Análise de Faturamento (Revenue MAPE)**

* **Filtros de Página:** Período (7, 15, 30, 60 dias).
* **Gráfico de Tendência:** Linha do tempo do MAPE nos últimos 30 dias.
  * *Objetivo:* Identificar se o modelo está degradando.
* **Top Ofensores:** Tabela `revenue_mape_report_big_errors` listando os IDs (listings) com maior erro absoluto.

**2. Análise de Preço (Price AV)**

* **Gráfico:** Variação do Preço Médio Diário.
* **Detecção:** Plotar linha de preço vs linha de tendência esperada.


---

### 🔍 Página 3: Diagnóstico Detalhado & Críticos

*Publico-alvo: Engenharia (Investigação de falhas)*

**1. Detalhe dos Scrapers (Log View)**

* Tabela completa conectada a `scrapers_health`.
* Colunas: `Source`, `Container`, `Start Time`, `End Time`, `Rows Inserted`, `Status`.
* **Filtro:** Botão para exibir apenas "Falhas".

**2. Validadores Mensais (RF05 - OLX/Vivareal)**

* Tabela específica filtrada para fontes mensais.
* **Regra de Cor (Calculated Field):**
  * Se `data_atual` > `ultimo_dia_mes` + 2 dias E `rows_inserted` = 0 $\rightarrow$ **VERMELHO (CRÍTICO)**.
  * Caso contrário $\rightarrow$ **VERDE**.


---

## 4. Regras de Negócio para o Frontend (Looker Studio)

Como o Backend entrega os dados "quase prontos", o Frontend precisa aplicar as regras de apresentação definidas no Discovery inicial:


1. **Regra de "Saúde" (Calculated Field):**
   * No Looker, criar um campo `is_healthy`.
   * Logica: `CASE WHEN status = 'Success' THEN 1 ELSE 0 END`.
   * A tolerância de 48h para scrapers mensais deve ser tratada preferencialmente no SQL da View, mas se for no Looker, usar comparação de datas: `DATE_DIFF(current_date, last_run_date) > 32`.
2. **Filtros de Exclusão:**
   * Aplicar filtro global para remover fontes marcadas como "Legado" ou "Ranking" que não devem impactar a nota de saúde (conforme RF01).
3. **Comparação D-0 vs D-1:**
   * Utilizar a funcionalidade de "Date Range Comparison" do Looker Studio nas tabelas de volumetria para exibir a setinha de queda/aumento percentual automaticamente.


---

## 5. Pontos de Atenção & Validação

Antes de entregar o dashboard, o desenvolvedor do Looker deve validar estes pontos com o time de DataOps (que construiu as tabelas):


1. **Conexão OLX/Vivareal:** Confirmar se os dados dessas fontes estão caindo na tabela `scrapers_health` com o nome `source` correto. Se não estiverem, o RF05 não poderá ser cumprido nesta tela.
2. **Latência:** O Looker Studio por padrão faz cache de 12 horas no BigQuery.
   * *Ação:* Alterar a configuração do report para "Data Freshness: 1 hour" ou usar o botão de "Refresh Data" manual, dado que o requisito é atualização até as 8h BRT.
3. **Desligamento S3:** O documento técnico menciona que o `insert_report` ainda alimenta o S3. O Dashboard do Looker **NÃO** deve conectar no S3. Deve conectar **apenas** no BigQuery para garantir que, quando a chave do S3 for desligada, o painel continue funcionando.


---

\nLinks Importantes: 

Documentação Técnica: @[BI de Observabilidade](mention://1d79a1e8-07ea-44cc-a5c4-310fb8b2e172/document/b7d3cc99-1004-4b51-9f96-bd1838ee7437)

BigQuery:

* [anomaly_mape_report](https://console.cloud.google.com/bigquery?inv=1&invt=Ab214g&project=data-resources-448418&ws=!1m10!1m4!4m3!1sdata-resources-448418!2slake_observability!3sscrapers_health!1m4!4m3!1sdata-resources-448418!2slake_observability!3sanomaly_mape_report)
* [anomaly_price_antecedence](https://console.cloud.google.com/bigquery?inv=1&invt=Ab214g&project=data-resources-448418&ws=!1m10!1m4!4m3!1sdata-resources-448418!2slake_observability!3sscrapers_health!1m4!4m3!1sdata-resources-448418!2slake_observability!3sanomaly_mape_report)
* [priceav_mape_report](https://console.cloud.google.com/bigquery?inv=1&invt=Ab214g&project=data-resources-448418&ws=!1m10!1m4!4m3!1sdata-resources-448418!2slake_observability!3sscrapers_health!1m4!4m3!1sdata-resources-448418!2slake_observability!3spriceav_mape_report)
* [revenue_mape_report_last_years](https://console.cloud.google.com/bigquery?inv=1&invt=Ab214g&project=data-resources-448418&ws=!1m10!1m4!4m3!1sdata-resources-448418!2slake_observability!3sscrapers_health!1m4!4m3!1sdata-resources-448418!2slake_observability!3srevenue_mape_monthly_last_years)
* [revenue_mape_report_last_days](https://console.cloud.google.com/bigquery?inv=1&invt=Ab214g&project=data-resources-448418&ws=!1m10!1m4!4m3!1sdata-resources-448418!2slake_observability!3sscrapers_health!1m4!4m3!1sdata-resources-448418!2slake_observability!3srevenue_mape_report_last_days)
* [revenue_mape_report_big_errors](https://console.cloud.google.com/bigquery?inv=1&invt=Ab214g&project=data-resources-448418&ws=!1m10!1m4!4m3!1sdata-resources-448418!2slake_observability!3sscrapers_health!1m4!4m3!1sdata-resources-448418!2slake_observability!3srevenue_mape_monthly_big_errors)
* [scrapers_health](https://console.cloud.google.com/bigquery?inv=1&invt=Ab214g&project=data-resources-448418&ws=!1m10!1m4!4m3!1sdata-resources-448418!2slake_observability!3sscrapers_health!1m4!4m3!1sdata-resources-448418!2slake_observability!3srevenue_mape_report_last_days)