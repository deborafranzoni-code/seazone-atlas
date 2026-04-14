<!-- title: Migração do BI de Observabilidade para Looker Studio (GCP) | url: https://outline.seazone.com.br/doc/migracao-do-bi-de-observabilidade-para-looker-studio-gcp-RdffESNbrr | area: Tecnologia -->

# Migração do BI de Observabilidade para Looker Studio (GCP)

## **1. Contexto do Projeto**

* **Sistema Atual:** Dashboard de Observabilidade do Lake hospedado no [Microsoft Power BI](https://app.powerbi.com/reportEmbed?reportId=671ff174-3b7a-4508-b56d-b2d4c23808f7&autoAuth=true&ctid=1bc6b8f1-1aa6-4836-90ac-40f3fc44fd46)
* **Motivação da Migração:**
  * Modernização da infraestrutura de BI
  * Melhor integração com ecossistema GCP
  * Redução de custos operacionais
  * Necessidade de correções e melhorias nas métricas atuais
* **Escopo Restrito:** Apenas métricas de observabilidade serão migradas para GCP. Dados brutos e scrapers permanecem na AWS.


## **2. Objetivos do Projeto**


1. Migrar o dashboard de observabilidade do Power BI para Looker Studio (GCP)
2. Garantir atualização dos dados até às 8h BRT
3. Corrigir inconsistências identificadas no BI atual:
   * Lógica de contagem de scrapers saudáveis
   * Remoção de métricas irrelevantes (Guest Favorite)
   * Validação de dados críticos (OLX, Vivareal)
4. Integrar novas métricas do canal `**#data-alerts-anomalias-lake**`


## **3. Escopo do Projeto**

### **Incluso:**

* Migração das seguintes métricas para GCP:
  * Saúde dos Scrapers (agregada por container)
  * Volume de dados inseridos no Lake (por tabela)
  * MAPE de Faturamento, Preço e Disponibilidade
  * Anomalias do Lake (MAPE Mudança de Preço PriceAV e Anomalias nas Aquisições de Preço)
  * Validação de dados críticos (OLX, Vivareal)
* Implementação de pipeline de extração de dados da AWS para GCP
* Configuração de agendamento e monitoramento

### **Não Incluso:**

* Desenvolvimento de novas métricas (exceto as já solicitadas)
* Alteração na lógica de cálculo das métricas na AWS (apenas correções de bugs)
* Migração de dados brutos ou scrapers para GCP
* Desenvolvimento do frontend no Looker Studio (responsabilidade do time de Solutions)

## **4. Requisitos Funcionais**

### **RF01 - Saúde dos Scrapers**

* **Descrição:** Exibir percentual de scrapers saudáveis, agrupados por container( INTERNALS DEVEM CONTAR COMO UM SCRAPER)
* **Regras de Negócio:**
  * Scrapers diários: Considerar saudável se executou nas últimas 24h
  * Scrapers semanais: Considerar saudável se executou nos últimos 7 dias + 48h de tolerância
  * Scrapers mensais: Considerar saudável se executou no último mês + 48h de tolerância
  * Excluir scrapers inativos (ex: Ranking)
  * Contar falhas por container (não por scraper individual)
* **Fonte de Dados:** Tabela na AWS
* **Visualização Esperada:** Card principal com percentual de saúde + detalhamento por container

### **RF02 - Volume de Dados Inseridos**

* **Descrição:** Exibir volume de linhas inseridas no Lake por tabela, com variação em relação ao último report
* **Regras de Negócio:**
  * Excluir tabelas não utilizadas (ex: relacionadas a Ranking)
  * Manter apenas tabelas principais (ex: `**airbnb_price**`, `**reservations**`, etc.)
* **Fonte de Dados:** Tabela na AWS
* **Visualização Esperada:** Tabela com volume e variação percentual

### **RF03 - MAPE de Faturamento, Preço e Disponibilidade**

* **Descrição:** Exibir MAPE (Erro Percentual Absoluto Médio) para:
  * Faturamento (por período: 7, 15, 30, 60 dias)
  * Preço e Disponibilidade (geral)
* **Regras de Negócio:**
  * Corrigir dados desatualizados (última atualização: 29/10/2024)
  * Garantir atualização diária
* **Fonte de Dados:** Tabela na AWS
* **Visualização Esperada:** Gráfico de linha + tabela de detalhamento


### **RF04 - Anomalias do Lake**

* **Descrição:** Exibir métricas do canal `**#data-alerts-anomalias-lake**`:
  * MAPE Mudança de Preço PriceAV
  * Anomalias nas Aquisições de Preço
* **Regras de Negócio:**
  * Atualização em tempo real (ou quase real)
* **Fonte de Dados:** Tabela na AWS
* **Visualização Esperada:** Cards de contagem + lista detalhada

### **Revisão do RF05 - Validação de Dados Críticos (OLX e Vivareal)**

#### **Descrição:**

Validar integridade de dados de OLX e Vivareal, considerando sua natureza **mensal** e validando a integridade end-to-end (RAW → CLEAN).

#### **Regras de Negócio (Ajustadas):**


1. **Periodicidade:**
   * OLX e Vivareal são scrapers **mensais** (executam 1x/mês).
   * Janela de validação: **último mês + 48h de tolerância** (ex: para setembro/2025, dados devem existir entre 01/09 e 02/10).
2. **Critérios de Status:**

| **Camada** | **Status "OK" (Verde)** | **Status "FALHA" (Vermelho)** |
|----|----|----|
| **RAW** | Dados brutos existem no mês anterior | Sem dados brutos do mês anterior |
| **CLEAN** | Dados limpos existem no mês anterior | Dados brutos existem, mas não foram processados para CLEAN |

## **5. Arquitetura Proposta**

### **6.2. Componentes Técnicos**

| **Componente** | **Serviço GCP** | **Descrição** |
|----|----|----|
| **Extração** | Cloud Function | Função serverless (Python) para extrair dados da AWS |
| **Armazenamento** | BigQuery | Armazena tabelas de observabilidade |
| **Agendamento** | Cloud Scheduler | Dispara extração diária às 5h BRT |
| **Monitoramento** | Cloud Monitoring | Monitora saúde do pipeline |
| **Visualização** | Looker Studio | Dashboard de BI |

### **6.3. Estrutura de Tabelas no BigQuery**

| **Tabela** | **Descrição** | **Frequência** |
|----|----|----|
| `**scraper_health_daily**` | Saúde dos scrapers por container | Diária |
| `**insert_report_daily**` | Volume de dados inseridos por tabela | Diária |
| `**mape_metrics_daily**` | MAPE de faturamento, preço e disponibilidade | Diária |
| `**anomalias_lake_daily**` | Anomalias do Lake | Diaria |
| `**data_quality_checks**` | Validação de OLX e Vivareal | Mensal |


## **7. Plano de Implementação**

### **Fase 1: Preparação** 

| **Atividade** | **Responsável** | **Entregável** |
|----|----|----|
| Corrigir lógica de scrapers na AWS | DataOps | Tabela `**scraper_health**` atualizada |
| Remover métricas irrelevantes (Guest Favorite) | DataOps | Queries ajustadas |
| Validar dados de MAPE, OLX e Vivareal | DataOps | Relatório de validação |
| Criar tabela de anomalias (se não existir) | DataOps | Tabela `**anomalias_lake**` |

### **Fase 2: Desenvolvimento** 

| **Atividade** | **Responsável** | **Entregável** |
|----|----|----|
| Configurar ambiente GCP (BigQuery, IAM) | DataOps | Projeto GCP pronto |
| Desenvolver Cloud Function de extração | DataOps | Código da função |
| Testar extração com dados históricos | DataOps | Logs de execução |
| Configurar agendamento (Cloud Scheduler) | DataOps | Job agendado |

#### **Fase 3: Validação (Infraestrutura e Dados)**

| **Atividade** | **Responsável** | **Entregável** |
|----|----|----|
| Executar extração paralela com Power BI | DataOps | Relatório de comparação de dados (BigQuery vs Power BI) |
| Validar estrutura de dados no BigQuery | DataOps | Certificado de qualidade dos dados |
| Disponibilizar documentação técnica das tabelas | DataOps | Dicionário de dados para o Solutions |


\n