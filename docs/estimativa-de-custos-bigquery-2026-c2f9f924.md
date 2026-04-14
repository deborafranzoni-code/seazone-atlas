<!-- title: Estimativa de custos BigQuery (2026) | url: https://outline.seazone.com.br/doc/estimativa-de-custos-bigquery-2026-woN4B8g6XX | area: Tecnologia -->

# Estimativa de custos BigQuery (2026)

# 


---

\* *Informações sobre custos obtidas no site oficial da google cloud platform em 29/01/2026*

## 1. Detalhamento de Custos BigQuery (Modelo On-Demand)

### A. Armazenamento (Active Storage)

O armazenamento refere-se ao espaço ocupado pelos dados no dataset events.

* **Volume Projetado:** 1,65 milhão de eventos ocupam entre **5 GB e 7 GB**.
* **Limite Gratuito:** Os primeiros **10 GB** por mês são isentos de cobrança.
* **Custo Estimado:** **US$ 0,00**.

### B. Processamento de Consultas (Queries)

Refere-se à leitura de dados realizada pelo GrowthBook para gerar estatísticas.

* **Processamento Projetado:** Estimado em menos de **200 GB** por mês para este volume de eventos.
* **Limite Gratuito:** O primeiro **1 TB (1.000 GB)** processado por mês é gratuito.
* **Custo Estimado:** **US$ 0,00**.

### C. Ingestão de Dados (Batch Export)

* **Regra:** O carregamento de dados via jobs (método de exportação horária do PostHog) não possui custo de processamento no BigQuery.
* **Custo:** **US$ 0,00**.


---

## 2. Comparativo de Custos Mensais (Projeção 1.65M)

| Plataforma | Volume de Eventos | Custo Estimado | Observação |
|----|----|----|----|
| **PostHog**  | 1,65 Milhão  | **US$ 32,73**  | Inclui 1M gratuito + excedente.  |
| **BigQuery**  | 1,65 Milhão  | **US$ 0,00**  | Totalmente coberto pelo *Free Tier*.  |


---

## 3. Evidência Técnica ([Calculadora GCP](https://cloud.google.com/products/calculator?dl=CjhDaVJoWWpoa1lXWTVOUzB6T0RGbExUUXdPVFF0T0dReU15MHhOR0l4WXpkaU56SmlOelFRQVE9PRALGiQyMUYxMUFGNC0xMTBDLTQyNEYtOUUyQS0zQ0I1OTZEQzNCRjE)) 

Abaixo, a simulação configurada para o modelo **On-Demand** na região us-central1, comprovando a viabilidade financeira do projeto:

##  ![](/api/attachments.redirect?id=a094d495-f767-4e31-ac07-69c747527110 " =911x768")\n4. Conclusão

A análise do faturamento atual do PostHog indica que o site já processou **1,35 milhão de eventos**. Com base na taxa de uso atual, a projeção final para o ciclo mensal é de **1,65 milhão de eventos**. Mesmo com este volume, a infraestrutura no **Google Cloud (BigQuery)** permaneceria operando com **custo zero** devido aos limites do nível gratuito (*Always Free*).


---

## 5. Referências Oficiais de Precificação (GCP 2026)

Para auditoria e validação técnica dos custos apresentados, consulte a documentação oficial do Google Cloud:

### A. Armazenamento (Storage)

* **Link:** [cloud.google.com/bigquery/pricing#storage](https://cloud.google.com/bigquery/pricing#storage)
* **Regra Free Tier:** Os primeiros **10 GB** de armazenamento lógico por mês são gratuitos (*Always Free*).
* **Aplicação:** Com uma projeção de \~7 GB para 1.65M de eventos, o custo permanece **US$ 0,00**.

### B. Consultas e Análises (Queries)

* **Link:** [cloud.google.com/bigquery/pricing#queries](https://cloud.google.com/bigquery/pricing#queries)
* **Regra Free Tier:** O primeiro **1 TB (1.000 GB)** de processamento de consultas por mês é gratuito no modelo On-Demand.
* **Aplicação:** As consultas do GrowthBook processarão um volume significativamente menor que o limite de 1.000 GB, mantendo o custo em **US$ 0,00**.

### C. Ingestão de Dados (Batch Load)

* **Link:** [cloud.google.com/bigquery/docs/loading-data](https://cloud.google.com/bigquery/docs/loading-data)
* **Regra:** O carregamento de dados via jobs de carga (Batch) é **isento de custos de ingestão** no BigQuery.
* **Aplicação:** A exportação horária realizada pelo PostHog utiliza este método, garantindo que não haja cobrança para "entrar" com os dados no Google Cloud.



---

\n*Relatório gerado em 29 de Janeiro de 2026.*


\