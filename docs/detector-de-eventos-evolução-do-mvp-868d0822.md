<!-- title: Detector de Eventos - Evolução do MVP | url: https://outline.seazone.com.br/doc/detector-de-eventos-evolucao-do-mvp-ukdsBZJ9Sp | area: Tecnologia -->

# Detector de Eventos - Evolução do MVP

[Registro call de Disvovery](https://outline.seazone.com.br/doc/registro-call-de-disvovery-qum0YFGpsP)

[Proposta reumida(One Page/ One Hour Pledge)](/doc/proposta-reumidaone-page-one-hour-pledge-EOetFTPOGp)

## **Documento de Discovery**

### **1. Visão Geral do Projeto**

#### **1.1. Contexto Atual**

O sistema atual consiste em dois alertas independentes que detectam picos de demanda:

* **Alertas Internos:** Monitoram padrões de reservas Seazone com antecedência
* **Alertas de Concorrentes:** Identificam picos de ocupação em concorrentes

Ambos os sistemas geram valor para o time de RM, mas sofrem com:

* Excesso de ruído e falsos positivos
* Processo manual pesado (\~1 hora/dia)
* Falta de integração entre os sistemas
* Formato inadequado de entrega (CSVs fragmentados)

#### **1.2. Objetivo da Evolução**

Evoluir os sistemas para reduzir ruído, automatizar processos e criar uma "conversa" entre os alertas através de integração seletiva de dados, mantendo a separação lógica das duas fontes.

### **2. Requisitos Funcionais**

#### **2.1. Arquitetura Geral**

**Componentes do Sistema:**

```markup
Cloud Functions (GCP)
    ↓
BigQuery (Armazenamento)
    ↓
Google Sheets (Interface do Usuário)
    ↓
Slack (Notificações)
```


**Fluxo de Dados:**


1. Cloud Functions executam diariamente 
2. Processam dados de reservas Seazone e concorrentes
3. Aplicam filtros e lógicas de detecção
4. Armazenam resultados no BigQuery
5. Atualizam Google Sheets com alertas do dia
6. Envia notificações resumidas para o Slack

#### **2.2. Estrutura do Google Sheets**

**Abas:**

* **Alertas_Internos_Ativos**: Alertas de pico de demanda interna não verificados
* **Alertas_Internos_Arquivado**: Histórico de alertas internos verificados
* **Alertas_Concorrentes_Ativos**: Alertas de concorrentes não verificados
* **Alertas_Concorrentes_Arquivado**: Histórico de alertas de concorrentes verificados
* **Dashboard**: Resumo de métricas e estatísticas


**Colunas - Alertas Internos:**

| **Coluna** | **Tipo** | **Descrição** | **Obrigatório** |
|----|----|----|----|
| ID | STRING | Hash MD5 (Polígono + Período + Tipo) | Sim |
| Data_Alerta | DATE | Data de geração do alerta | Sim |
| Tipo_Alerta | STRING | "Pico de Demanda Interna" | Sim |
| Poligono | STRING | Nome do polígono | Sim |
| Faixa_Capacidade | STRING | "3-10", "11-30" ou ">30" | Sim |
| Data_Alvo_Inicio | DATE | Início do período de alta demanda | Sim |
| Data_Alvo_Fim | DATE | Fim do período de alta demanda | Sim |
| Metrica_Valor | FLOAT | Valor que acionou o alerta | Sim |
| Threshold_Usado | STRING | Limiar utilizado (ex: "3", "15%") | Sim |
| Ocupacao_Concorrentes | FLOAT | Ocupação dos concorrentes no período | Não |
| Evento_Mapeado | STRING | Evento conhecido (se aplicável) | Não |
| Alerta_Externo | BOOLEAN | Se sistema externo alertou para mesma data | Não |
| Status | LISTA | "Ajustar Preço", "Monitorar", "Ignorar", "Falso Positivo" | Sim |
| Check | BOOLEANO | Marcação de verificação | Sim |
| Data_Status | DATE | Data da última atualização do status | Não |

**Colunas - Alertas de Concorrentes:**

| **Coluna** | **Tipo** | **Descrição** | **Obrigatório** |
|----|----|----|----|
| ID | STRING | Hash MD5 (Região + Polígono + Período) | Sim |
| Data_Alerta | DATE | Data de geração do alerta | Sim |
| Tipo_Alerta | STRING | "Pico de Demanda Concorrentes" | Sim |
| Regiao | STRING | Nome da região | Sim |
| Poligono | STRING | Nome do polígono | Sim |
| Periodo | STRING | Período do pico de demanda | Sim |
| Taxa_Ocupacao | FLOAT | Taxa de ocupação dos concorrentes | Sim |
| Total_Imoveis_Ativos | INTEGER | Número de imóveis ativos | Sim |
| Ocupacao_Interna | FLOAT | Ocupação Seazone no período | Não |
| Alerta_Interno | BOOLEAN | Se sistema interno alertou para mesma data | Não |
| Status | LISTA | "Ajustar Preço", "Monitorar", "Ignorar", "Falso Positivo" | Sim |
| Check | BOOLEANO | Marcação de verificação | Sim |
| Data_Status | DATE | Data da última atualização do status | Não |

#### **2.3. Lógica de Detecção - Alertas Internos**

**Fonte de Dados:** Reservas Seazone dos últimos 365 dias

**Pré-filtros:**

* Apenas polígonos com 3 ou mais unidades Seazone
* Apenas reservas com pelo menos ==35 dias== de antecedência
* Excluir períodos já mapeados como eventos conhecidos

**Lógica de Detecção por Faixa de Capacidade:**

**Faixa 3-10 unidades:**

* Alertar se ≥ 3 reservas se sobrepõem no período
* Período de sobreposição: 3 dias consecutivos

**Faixa 11-30 unidades:**

* Alertar se ≥ 4 reservas se sobrepõem no período
* Período de sobreposição: 3 dias consecutivos

**Faixa >30 unidades:**

* Alertar se ≥ 20% da capacidade do polígono se sobrepõem no período
* Período de sobreposição: 3 dias consecutivos

**Lógica de Agrupamento:**

* Alertas para datas adjacentes (±3 dias) devem ser agrupados em único período
* Exemplo: alertas para 20/11, 21/11 e 22/11 → período "20/11 a 22/11"

#### **2.4. Lógica de Detecção - Alertas de Concorrentes**

**Fonte de Dados:** Dados de ocupação de concorrentes

**Pré-filtros:**


* Apenas regiões pré-definidas (13 regiões principais)
* Apenas polígonos com 20 ou mais imóveis
* Excluir polígonos expandidos
* Antecedência: até 180 dias

**Lógica de Detecção:**

* **Pico Moderado:** Ocupação > média + 1.15 \* desvio padrão E ≥ 10%
* **Pico Forte:** Ocupação > média + 1.5 \* desvio padrão E ≥ 15%
* Apenas picos fortes serão notificados (pico moderado apenas para histórico)

**Cálculo de Média e Desvio Padrão:**

* Base: Histórico de ocupação dos últimos 365 dias
* Por polígono
* Considerar sazonalidade (mês do ano)

#### **2.5. Integração Seletiva** 

**Para Alertas Externos → Internos:**

* Consultar ocupação Seazone para o mesmo período
* Verificar se existe alerta interno ativo para a data
* Incluir informações nas colunas:
  * **Ocupacao_Interna**: Taxa de ocupação Seazone
  * **Alerta_Interno**: Boolean indicando se há alerta interno

**Para Alertas Internos → Externos:**

* Consultar ocupação de concorrentes para o mesmo período
* Verificar se há evento mapeado pelo RM
* Verificar se sistema externo alertou para a data
* Incluir informações nas colunas:
  * **Ocupacao_Concorrentes**: Taxa de ocupação concorrentes
  * **Evento_Mapeado**: Nome do evento (se aplicável)
  * **Alerta_Externo**: Boolean indicando alerta externo

#### **2.6. Filtros Inteligentes**

**Filtro de Eventos Mapeados:**

* Manter tabela de eventos conhecidos (Natal, Reveillon, CCXP, Oktoberfest, etc.)
* Não gerar alerta externo para datas com eventos já mapeados
* Para alertas internas, incluir informação do evento no campo `Evento_Mapeado`

**Filtro de Relevância:**

* Não gerar alerta para regiões sem imóveis Seazone ativos
* Não gerar alerta se ocupação Seazone = 0% E ocupação concorrentes < 20%
* Para alertas internos, não gerar se o polígono tem > 100 unidades e reservas < 5% da capacidade

**Filtro de Deduplicação:**

* Usar hash único baseado em (Polígono + Período + Tipo)
* Não gerar alerta duplicado no mesmo dia
* Agrupar alertas de datas adjacentes automaticamente

### **3. Requisitos Não Funcionais**

#### **3.1. Performance**

* Tempo de execução diário: < 10 minutos
* Google Sheets deve suportar até 10.000 linhas por aba sem perda de performance
* Atualização diária pela manhã

#### **3.2. Disponibilidade**

* Sistema deve executar diariamente
* Google Sheets disponível 24/7 para acesso do usuário
* BigQuery com retenção de dados de 365 dias

#### **3.3. Usabilidade**

* Interface do Google Sheets deve ser intuitiva com colunas congeladas
* Validação: Check só pode ser marcado após Status ser definido
* Menu com opções de limpeza e ajuda
* Cores/formato para fácil identificação de alertas críticos

#### **3.4. Segurança**

* Acesso editável ao Google Sheets restrito ao time de RM
* Logs de execução por 30 dias para auditoria

### **4. Estrutura de Entregáveis**

#### **Fase 1: Qualidade dos Alertas** 

**Entregáveis:**


1. Especificação detalhada dos filtros e lógicas de detecção
2. Esquema das tabelas no BigQuery
3. Documentação dos parâmetros e limiares

#### **Fase 2: Estrutura do Google Sheets** 

**Entregáveis:**


1. Modelo do Google Sheets com colunas definidas
2. Script de append e deduplicação
3. Validação de Check condicional
4. Menu de funções (limpeza, ajuda)

**Aprovação:** Product Manager 

#### **Fase 3: Integração Seletiva** 

**Entregáveis:**


1. Lógica de cruzamento de dados entre sistemas
2. Implementação dos campos de integração
3. Testes de integração com dados históricos

**Aprovação:** Product Manager

#### **Fase 4: Filtros Inteligentes (3 dias)**

**Entregáveis:**


1. Implementação do filtro de eventos mapeados
2. Implementação do filtro de relevância
3. Testes de redução de ruído

**Aprovação:** Product Manager

#### **Fase 5: Validação e Deploy (3 dias)**

**Entregáveis:**


1. Script de deploy automatizado
2. Documentação de operação
3. Treinamento do time de RM

**Aprovação:** Product Manager e Gerente de RM

### **5. Parâmetros e Configurações**

#### **5.1. Parâmetros de Alertas Internos**

| **Parâmetro** | **Valor** | **Descrição** |
|----|----|----|
| MIN_LEAD_TIME_DAYS | 23 | Antecedência mínima para considerar |
| MIN_UNITS_PER_POLYGON | 3 | Mínimo de unidades por polígono |
| OVERLAP_DAYS | 3 | Dias de sobreposição para considerar pico |
| THRESHOLD_3_10 | 3 | Limiar para faixa 3-10 unidades |
| THRESHOLD_11_30 | 4 | Limiar para faixa 11-30 unidades |
| THRESHOLD_GT_30 | 0.20 | Porcentagem para faixa >30 unidades |
| ADJACENT_DAYS_RANGE | 3 | Dias adjacentes para agrupamento |

#### **5.2. Parâmetros de Alertas de Concorrentes**

| **Parâmetro** | **Valor** | **Descrição** |
|----|----|----|
| MAX_LEAD_TIME_DAYS | 180 | Antecedência máxima para considerar |
| MIN_UNITS_PER_POLYGON | 20 | Mínimo de unidades por polígono |
| MODERATE_THRESHOLD_LOW | 1.15 | Multiplicador para pico moderado |
| MODERATE_THRESHOLD_HIGH | 1.5 | Multiplicador para pico forte |
| MODERATE_MIN_OCCUPANCY | 0.10 | Ocupação mínima para pico moderado |
| STRONG_MIN_OCCUPANCY | 0.15 | Ocupação mínima para pico forte |
| REGIONS | \["Brasília", "Canela", "Curitiba", ...\] | Lista de regiões monitoradas |

#### **5.3. Parâmetros de Integração**

| **Parâmetro** | **Valor** | **Descrição** |
|----|----|----|
| EVENTS_TABLE | eventos_mapeados | Tabela com eventos conhecidos |
| RELEVANCE_THRESHOLD | 0.20 | Ocupação mínima concorrentes para considerar |
| LARGE_POLYGON_UNITS | 100 | Unidades para considerar "grande" polígono |
| LARGE_POLYGON_MIN_RESERVES | 0.05 | Porcentagem mínima para alertar em grandes polígonos |

### **6. Ferramentas e Tecnologias**

#### **6.1. Ferramentas Definidas**

* **Cloud Functions (GCP):** Para execução do pipeline diário
* **BigQuery:** Para armazenamento de dados históricos
* **Google Sheets:** Para interface do usuário e gestão de alertas
* **Slack API:** Para notificações
* **Apps Script:** Para automação do Google Sheets


### **7. Critérios Esperados**

| **Critério** | **Descrição** | **Métrica** |
|----|----|----|
| Redução de Ruído | Diminuição no volume total de alertas | ≥ 60% |
| Eficiência | Redução no tempo manual gasto com alertas | ≥ 60% |
| Qualidade | Alertas com integração seletiva | 100% |
| Performance | Tempo de execução diário | < 10 minutos |
| Usabilidade | Taxa de adoção do fluxo correto | ≥ 90% |
| Integração | Cruzamento de dados entre sistemas | 100% |


### **8. Riscos e Mitigações**

| **Risco** | **Probabilidade** | **Impacto** | **Mitigação** |
|----|----|----|----|
| Dados de ocupação indisponíveis | Média | Alto | Ter fallback (não aplicar filtro se dados não disponíveis) |
| Performance do Sheets | Baixa | Médio | Limpeza automática após 30 dias |
| Limiares muito restritivos | Média | Alto | Acompanhamento semanal + ajustes conforme feedback |
| Resistência à mudança | Baixa | Médio | Treinamento + acompanhamento próximo nas primeiras semanas |