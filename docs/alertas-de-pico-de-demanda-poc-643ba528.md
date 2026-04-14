<!-- title: Alertas de Pico de Demanda (POC) | url: https://outline.seazone.com.br/doc/alertas-de-pico-de-demanda-poc-Hq0utdw7Uv | area: Tecnologia -->

# Alertas de Pico de Demanda (POC)

**Data:** 09-06-2025\n**Versão:** 1.0\n**Responsável:** Lucas Abel da Silveira



1. **Introdução e Objetivo do Módulo 1** 

   Este documento detalha o desenvolvimento, os testes e os resultados da **Prova de Conceito (POC)** do produto **"Alerta de Pico de Demanda"**. O objetivo principal desta fase inicial é validar a viabilidade técnica de um sistema de alerta que identifica picos de demanda anormal nos imóveis Seazone com antecedência. A detecção desses sinais visa permitir que o time de Revenue Management (RM) realize ajustes proativos na estratégia de precificação, otimizando a receita.

   Esta POC foca em uma solução simples e funcional, projetada para rápida implementação e validação colaborativa com o time de RM.

   \
2. **Plano de Ação Executado** 

O desenvolvimento seguiu um plano de ação estruturado em três fases:

* **Fase 1: Preparação e Análise Exploratória (EDA):** Coleta e consolidação de dados de reservas do último ano (até Mai/2025). Análise da distribuição de capacidade, do lead time (antecedência) das reservas e da velocidade histórica de criação de reservas para definir os parâmetros e a lógica dos alertas.
* **Fase 2: Implementação e Teste Retrospectivo (Backtesting):** Desenvolvimento de scripts Python para aplicar as lógicas de alerta aos dados históricos. Foram realizadas múltiplas iterações para refinar os limiares, agrupar alertas relacionados e remover redundâncias, com o objetivo de tornar a saída mais acionável.
* **Fase 3 (Próximos Passos): Validação e Produção da POC:** Apresentação dos resultados do backtest ao time de RM para validação qualitativa, coleta de feedback e implementação do pipeline para geração de alertas diários.

  \

3\. Definições Estratégicas e Lógica dos Alertas

As seguintes premissas e estratégias foram definidas com base na EDA e em alinhamento com os objetivos da POC:

**3.1. Escopo e Parâmetros Globais**

* **Fonte de Dados:** Análise focada exclusivamente em reservas de imóveis Seazone.
* **Granularidade:** Alertas gerados no nível de **polígono**, para capturar eventos locais (nível bairro).
* **Exclusão de Polígonos:** Polígonos com **2 ou menos unidades** foram desconsiderados nesta fase para simplificar a lógica e focar em áreas onde a métrica de "velocidade de reserva" é mais significativa.
* **Antecedência Mínima (min_lead_time_days):** A análise se concentra apenas em reservas feitas com **pelo menos 23 dias de antecedência** (correspondente ao P75 do histórico), a fim de filtrar o comportamento de última hora.
* **Faixas de Capacidade:** Para aplicar limiares mais precisos, os polígonos considerados (>2 unidades) foram segmentados em: "3-10 unidades", "11-30 unidades" e ">30 unidades".

#### **3.2. Estratégias de Alerta Implementadas**

**Alerta Tipo 1: Pico de Demanda para Período Alvo**

* **Objetivo:** Detectar demanda concentrada para datas ou eventos específicos.
* **Lógica:** Alerta quando múltiplas reservas recentes (criadas nos últimos 3 dias) se sobrepõem em um mesmo dia futuro (ou período consecutivo).

**Alerta Tipo 2: Volume Alto de Novas Reservas**

* **Objetivo:** Identificar um interesse súbito e generalizado por um polígono.
* **Lógica:** Alerta quando um volume anormal de novas reservas com alta antecedência é criado para o mesmo polígono no último dia, independentemente das datas de check-in.\n\n

### 4. Backtest: Desafios, Iterações e Limiares Finais

O processo de backtesting foi iterativo para refinar a qualidade dos alertas.

* **Desafios Iniciais:** As primeiras versões geraram um volume excessivo de alertas (>80/dia) devido à repetição e limiares muito sensíveis.
* **Soluções Implementadas:**

  
  1. **Agrupamento:** Alertas do Tipo 1 para datas consecutivas foram agrupados em um único alerta de "período alvo".
  2. **Desduplicação:** Implementada lógica para mostrar apenas a primeira ocorrência de um alerta do Tipo 1 para o mesmo (polígono, período alvo), eliminando repetições em dias subsequentes.
  3. **Limiares Adaptativos:** Para a faixa ">30 unidades", foram introduzidos limiares percentuais que se ajustam dinamicamente à capacidade do polígono, resolvendo a questão da grande variação de tamanho dentro desta faixa.

#### **4.1. Limiares Finais Definidos para a POC**

* **Alerta Tipo 1 (Pico de Demanda por Período Alvo):**
  * **3-10 unidades:** **2** reservas sobrepostas
  * **11-30 unidades:** **3** reservas sobrepostas
  * **>30 unidades:** **10%** da capacidade do polígono
* **Alerta Tipo 2 (Volume Alto de Novas Reservas):**
  * **3-10 unidades:** **2** novas reservas/dia
  * **11-30 unidades:** **4** novas reservas/dia
  * **>30 unidades:** **15%** da capacidade do polígono

#### **4.2. Resultados Finais do Backtest**

* **Total de Alertas (Desduplicados):** **1.924** (em 654 dias de simulação).
* **Média de Alertas por Dia:** **\~4.4 alertas/dia**, com uma mediana de 3 e picos de \~12 (P95).
* **Conclusão do Backtest:** O volume final de alertas é considerado gerenciável e significativo para a validação com o time de RM. Os limiares ajustados e a lógica de agrupamento/desduplicação foram eficazes em focar em sinais mais fortes e reduzir o ruído.

### 5. Próximos Passos


1. **Validação da POC com o Time de RM:** Apresentar os resultados do backtest para análise qualitativa, coletando feedback sobre a relevância e acionabilidade dos alertas.
2. **Implementação em Produção:** Iniciar a geração diária de alertas para monitoramento "ao vivo" via Slack.
3. **Ajuste Iterativo:** Com base no feedback contínuo, refinar os parâmetros e a lógica do sistema.
4. **Evolução Futura (Pós-POC):** Se a POC for bem-sucedida, considerar a expansão para incluir:
   * Análise de sazonalidade.
   * Regras específicas para polígonos de baixa capacidade.
   * Análise de dados de concorrentes e fontes externas para uma detecção de eventos mais preditiva.