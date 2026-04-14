<!-- title: Auditoria do MAPE - Arquitetura de Dados | url: https://outline.seazone.com.br/doc/auditoria-do-mape-arquitetura-de-dados-Uw7zQxENd0 | area: Tecnologia -->

# Auditoria do MAPE - Arquitetura de Dados

**Versão:** 1.0\n**Data:** 02/10/2025\n**Autor:** PM (Product Manager)\n**Time Responsável:** DataOps\n**Stakeholders:** Diretoria, DataSolutions, Negócios

### **1. Contexto**

#### **1.1. Problema de Negócio**

Atualmente, quando o KPI do MAPE dos últimos 15 dias sofre alterações bruscas (ex: de 25% para 35%), não temos uma forma ágil de identificar a causa raiz. O processo atual envolve:

* Solicitações manuais ao time de DataOps
* Análises complexas e demoradas no Athena/S3
* Dificuldade em distinguir entre diferentes tipos de erros
* Falta de visibilidade sobre o impacto de granularidades

Isso resulta em:

* Atraso em ações corretivas
* Sobrecarga do time técnico com demandas reativas
* Decisões estratégicas baseadas em dados não validados

#### **1.2. Solução Proposta**

Desenvolver uma infraestrutura de dados que permita:

* Comparação entre dois períodos para identificar variações
* Decomposição do erro em fatores acionáveis (bloqueios, ocupação, preço)
* Análise das fontes de detecção de bloqueios (heurístico, ML3, NN)
* Identificação de granularidades críticas de forma controlada

#### **1.3. Público-Alvo**

* **Primário**: Time de DataOps (construção e manutenção)
* **Secundário**: Time de DataSolutions (consumo dos dados)

### **2. Requisitos Levantados**

#### **2.1. Requisitos Funcionais**

| **ID** | **Requisito** | **Descrição** | **Prioridade** |
|----|----|----|----|
| RF-01 | Comparação de Períodos | Permitir selecionar dois períodos (A e B) para análise comparativa | Alta |
| RF-02 | Decomposição do Erro | Mostrar a contribuição percentual de cada fator para o erro total (bloqueios, ocupação, preço) | Alta |
| RF-03 | Análise de Fontes de Bloqueio | Identificar concordância entre as três fontes (heurístico, ML3, NN) | Alta |
| RF-04 | Alertas de Granularidade | Exibir granularidades críticas apenas quando necessário (estados, stratas, etc.) | Média |
| RF-05 | Drill-down por Imóvel | Permitir análise detalhada dos imóveis com maior impacto no MAPE | Alta |
| RF-06 | Geração de Acionáveis | Fornecer recomendações específicas para cada tipo de problema identificado | Alta |

### **3. Detalhamento de Dados**

#### **3.1. Fontes de Dados Existentes**

| **Fonte** | **Descrição** | **Utilidade** |
|----|----|----|
| ```javascript
seazone_real_data
``` | Dados reais de reservas e faturamento | Base para cálculo do MAPE real |
| ```javascript
brlink_seazone_enriched_data
``` | Dados previstos pelo modelo | Base para cálculo do MAPE previsto |
| ```javascript
staging_reservations_blockdetected_ml3
``` | Predições de bloqueio do modelo ML3 | Análise de fontes de bloqueio |
| ```javascript
staging_reservations_blockdetected_nn
``` | Predições de bloqueio do modelo NN | Análise de fontes de bloqueio |

#### **3.2. Tabelas a Serem Criadas no BigQuery**

**Tabela 1:**

```javascript
mape_history
```

**Descrição**: Histórico de MAPE e métricas relacionadas por dia e imóvel

| **Coluna** | **Tipo** | **Descrição** | **Obrigatório** |
|----|----|----|----|
| ```javascript
date
``` | DATE | Data da métrica | Sim |
| ```javascript
listing_id
``` | STRING | ID do imóvel | Sim |
| ```javascript
mape_value
``` | FLOAT | Valor do MAPE do imóvel no dia | Sim |
| ```javascript
actual_revenue
``` | FLOAT | Faturamento real do dia | Sim |
| ```javascript
predicted_revenue
``` | FLOAT | Faturamento previsto pelo modelo | Sim |
| ```javascript
occupancy_rate
``` | FLOAT | Taxa de ocupação real | Sim |
| ```javascript
predicted_occupancy
``` | FLOAT | Taxa de ocupação prevista | Sim |
| ```javascript
blocked_days
``` | INTEGER | Dias bloqueados (regra final) | Sim |
| ```javascript
heuristic_blocked
``` | BOOLEAN | Bloqueio por regra heurística | Sim |
| ```javascript
ml3_blocked
``` | INTEGER | Bloqueio previsto pelo modelo ML3 | Sim |
| ```javascript
nn_blocked
``` | INTEGER | Bloqueio previsto pelo modelo NN | Sim |
| ```javascript
avg_price
``` | FLOAT | Preço médio real | Sim |
| ```javascript
predicted_avg_price
``` | FLOAT | Preço médio previsto | Sim |
| ```javascript
state
``` | STRING | Estado do imóvel | Sim |
| ```javascript
city
``` | STRING | Cidade do imóvel | Sim |
| ```javascript
strata
``` | STRING | Strata de qualidade (TOP, MASTER, etc.) | Sim |
| ```javascript
property_type
``` | STRING | Tipo do imóvel (apartamento, casa, etc.) | Sim |
| ```javascript
bedrooms
``` | INTEGER | Número de quartos | Sim |
| ```javascript
created_at
``` | TIMESTAMP | Data de criação do registro | Sim |
| ```javascript
updated_at
``` | TIMESTAMP | Data de atualização do registro | Sim |

**Particionamento**: Por **date** (ano, mês, dia) **Clusterização**: Por **state**, **strata**

**Tabela 2:**

```javascript
mape_comparison
```

**Descrição**: Resultados pré-calculados de comparação entre períodos

| **Coluna** | **Tipo** | **Descrição** | **Obrigatório** |
|----|----|----|----|
| ```javascript
comparison_id
``` | STRING | ID único da comparação | Sim |
| ```javascript
period_a_start
``` | DATE | Data inicial do período A | Sim |
| ```javascript
period_a_end
``` | DATE | Data final do período A | Sim |
| ```javascript
period_b_start
``` | DATE | Data inicial do período B | Sim |
| ```javascript
period_b_end
``` | DATE | Data final do período B | Sim |
| ```javascript
global_mape_a
``` | FLOAT | MAPE global no período A | Sim |
| ```javascript
global_mape_b
``` | FLOAT | MAPE global no período B | Sim |
| ```javascript
mape_variation
``` | FLOAT | Variação percentual do MAPE | Sim |
| ```javascript
error_decomposition_blocked
``` | FLOAT | % do erro atribuído a bloqueios | Sim |
| ```javascript
error_decomposition_occupancy
``` | FLOAT | % do erro atribuído a ocupação | Sim |
| ```javascript
error_decomposition_price
``` | FLOAT | % do erro atribuído a preço | Sim |
| ```javascript
source_concordance_heuristic_ml
``` | FLOAT | % concordância heurístico × ML | Sim |
| ```javascript
source_concordance_ml_nn
``` | FLOAT | % concordância ML × NN | Sim |
| ```javascript
conflict_days
``` | INTEGER | Dias com conflito entre fontes | Sim |
| ```javascript
created_at
``` | TIMESTAMP | Data de criação da comparação | Sim |
| ```javascript
updated_at
``` | TIMESTAMP | Data de atualização da comparação | Sim |

**Particionamento**: Por **period_b_start** (ano, mês) **Atualização**: Diária ou sob demanda

**Tabela 3:**

```javascript
mape_granularity_analysis
```

**Descrição**: Análise de granularidades críticas

| **Coluna** | **Tipo** | **Descrição** | **Obrigatório** |
|----|----|----|----|
| ```javascript
analysis_id
``` | STRING | ID único da análise | Sim |
| ```javascript
period_start
``` | DATE | Data inicial do período analisado | Sim |
| ```javascript
period_end
``` | DATE | Data final do período analisado | Sim |
| ```javascript
granularity_type
``` | STRING | Tipo de granularidade (state, strata, etc.) | Sim |
| ```javascript
granularity_value
``` | STRING | Valor da granularidade (SP, TOP, etc.) | Sim |
| ```javascript
mape_value
``` | FLOAT | MAPE para esta granularidade | Sim |
| ```javascript
comparison_to_avg
``` | FLOAT | Comparação com a média global | Sim |
| ```javascript
is_critical
``` | BOOLEAN | Indica se é uma granularidade crítica | Sim |
| ```javascript
created_at
``` | TIMESTAMP | Data de criação da análise | Sim |

**Particionamento**: Por **period_start** (ano, mês) e **granularity_type** **Atualização**: Diária

**Tabela 4:**

```javascript
mape_top_properties
```

**Descrição**: Imóveis com maior impacto no MAPE

| **Coluna** | **Tipo** | **Descrição** | **Obrigatório** |
|----|----|----|----|
| ```javascript
analysis_date
``` | DATE | Data da análise | Sim |
| ```javascript
listing_id
``` | STRING | ID do imóvel | Sim |
| ```javascript
mape_value
``` | FLOAT | MAPE do imóvel | Sim |
| ```javascript
mape_variation
``` | FLOAT | Variação do MAPE em relação ao período anterior | Sim |
| ```javascript
main_factor
``` | STRING | Fator principal do erro (blocked, occupancy, price) | Sim |
| ```javascript
source_problem
``` | STRING | Fonte do problema (heuristic, ml3, nn, conflict) | Sim |
| ```javascript
impact_score
``` | FLOAT | Score de impacto no MAPE global | Sim |
| ```javascript
created_at
``` | TIMESTAMP | Data de criação do registro | Sim |

**Particionamento**: Por **analysis_date** (ano, mês, dia) **Atualização**: Diária


### **4. Etapas de Implementação**

#### **Fase 1: Preparação do Ambiente** 

| **Etapa** | **Descrição** | **Responsável** | **Entregável** | **Dependências** |
|----|----|----|----|----|
| 1.1 | Provisionar ambiente GCP | DataOps | Projeto GCP com permissões |    |
| 1.2 | Configurar BigQuery | DataOps | Dataset e tabelas base | 1.1 |
| 1.3 | Configurar IAM | DataOps | Service accounts e permissões | 1.1 |
| 1.4 | Estabelecer pipeline de dados | DataOps | Arquitetura de ingestão | 1.2 |

#### **Fase 2: Desenvolvimento das Tabelas**

| **Etapa** | **Descrição** | **Responsável** | **Entregável** | **Dependências** |
|----|----|----|----|----|
| 2.1 | Criar tabela mape_history | DataOps | Tabela particionada e clusterizada | 1.2 |
| 2.2 | Criar tabela mape_comparison | DataOps | Tabela com lógica de comparação | 2.1 |
| 2.3 | Criar tabela mape_granularity_analysis | DataOps | Tabela de análise de granularidades | 2.1 |
| 2.4 | Criar tabela mape_top_properties | DataOps | Tabela de top impactadores | 2.1 |
| 2.5 | Criar views de análise | DataOps | Views otimizadas para dashboard | 2.2-2.4 |

#### **Fase 3: Pipeline de Dados** 

| **Etapa** | **Descrição** | **Responsável** | **Entregável** | **Dependências** |
|----|----|----|----|----|
| 3.1 | Desenvolver ETL de extração | DataOps | Scripts de extração das fontes | 2.1-2.4 |
| 3.2 | Implementar lógica de transformação | DataOps | Scripts de transformação e enriquecimento | 3.1 |
| 3.3 | Configurar agendamento | DataOps | Pipeline automatizado diário | 3.2 |
| 3.4 | Implementar qualidade de dados | DataOps | Testes e validações | 3.3 |

#### **Fase 4: Testes e Validação (Semana 4)**

| **Etapa** | **Descrição** | **Responsável** | **Entregável** | **Dependências** |
|----|----|----|----|----|
| 4.1 | Testar com dados históricos | DataOps | Relatório de validação | 3.4 |
| 4.2 | Validar performance | DataOps | Métricas de performance | 4.1 |
| 4.3 | Documentar APIs | DataOps | Documentação para DataSolutions | 4.2 |
| 4.4 | Handoff para DataSolutions | DataOps | Ambiente pronto para consumo | 4.3 |