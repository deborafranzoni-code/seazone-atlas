<!-- title: WorkFlow Real Data | url: https://outline.seazone.com.br/doc/workflow-real-data-Iib7ltn9rl | area: Tecnologia -->

# WorkFlow Real Data

## **1. Contexto do Projeto**

A **Real Reservation** ("Real Data Reservation") é um componente crítico da arquitetura de dados da Seazone, responsável por:

* Processar e enriquecer dados brutos de reservas obtidos via API do **Stays**.
* Alimentar sistemas estratégicos como **Sirius** (análise de performance), **Meta** (otimização de campanhas) e **MAPE** (validação de modelos preditivos).

**Problema Central:**\nO sistema atual sofre com **falhas recorrentes de timeout**, **limitações de escalabilidade** e **redundância operacional**, comprometendo a confiabilidade dos dados e a eficiência do ecossistema.


## **2. Problema de Negócio**

### **Sintomas Observados:**

* **Timeouts crônicos:** O sistema excede o tempo limite de execução, resultando em dados desatualizados.
* **Incapacidade de escalar:** A arquitetura não suporta o crescimento orgânico da operação (ex.: aumento no volume de reservas).
* **Redundância de esforços:** O Sirius realiza processamento semelhante ao da Real Reservation, gerando custos desnecessários.
* **Risco operacional:** Dados imprecisos afetam decisões de precificação, alocação de recursos e acurácia de modelos.


## **3. Objetivos da Iniciativa**

### **Objetivo Principal:**

**Reestruturar a Real Reservation para garantir escalabilidade, confiabilidade e eficiência no processamento de dados de reservas.**

## **4. Escopo do Projeto**

### **Incluso::**

* **Revisão arquitetural** da Real Reservation (foco em redução de requisições ao Stays).
* **Integração com o Sirius:** Utilizar dados processados pelo Sirius como fonte primária quando aplicável.
* **Otimização de código:** Revisão de eficiência, legibilidade e escalabilidade.
* **Implementação de escalabilidade horizontal:** Ajuste de threads, paralelização e uso de recursos (ex.: AWS Lambda).
* **Monitoramento:** Implementação de alertas para falhas e degradação de performance. - Caso aplicável.

### **Não Incluso::**

* Desenvolvimento de novas funcionalidades para o Sirius ou Meta.
* Mudanças na API do Stays (fora do controle da Seazone).
* Reestruturação total do ecossistema de dados (foco exclusivo na Real Reservation).

## **4. Plano de Implementação**

### **Fase 1: Diagnóstico e Planejamento**

* **Atividades:**
  * Mapear fluxo atual da Real Reservation (requisições, dependências, gargalos).
  * Auditar integração com o Sirius (o que pode ser reaproveitado?).
* **Entregável:** Documento de arquitetura atual e plano de ação.

### **Fase 2: Implementação do Band-Aid**

* **Atividades:**
  * Replicar aumento de threads para todas as etapas da Real Reservation.
  * Testar desempenho com volume dobrado de reservas.
* **Entregável:** Relatório de teste com métricas de estabilidade.

### **Fase 3: Reestruturação Estrutural** 

* **Atividades:**
  * Redesenhar arquitetura (integração Sirius, redução de requisições ao Stays).
  * Otimizar código (eficiência, paralelização).
  * Implementar monitoramento e alertas.
* **Entregável:** Nova versão da Real Reservation

### **Fase 4: Validação e Deploy** 

* **Atividades:**
  * Testes de carga, integração e aceitação com times de dados (DataSoutions\[Sirius\]/DataOps).
  * Deploy em produção.
* **Entregável:** Sistema em produção.