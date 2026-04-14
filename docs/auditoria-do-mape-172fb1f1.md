<!-- title: Auditoria do MAPE | url: https://outline.seazone.com.br/doc/auditoria-do-mape-BCWAPnPPrl | area: Tecnologia -->

# Auditoria do MAPE

### **Auditoria do MAPE**

**Versão:** 1.0\n**Data:** 26/10/2024\n**Autor: Lucas Abel da Silveira** PM (Product Manager)\n**Time Responsável:** DataOps

**Público-Alvo:** Coordenador, Gerente, PM

### **1. Problema**

**Investigação Lenta e Centralizada no Time Técnico**

* **Contexto:**
  * Quando o MAPE dos últimos 15 dias varia bruscamente (ex: 25% → 35%), **gestores  precisam solicitar análises ao time de DataOps**.
  * O processo atual:
    * Requisição manual ao DataOps.
    * Análise complexa no Athena/S3 (horas ou dias).
    * Dificuldade em distinguir causas:
      * Erros de dados (scraping, bloqueios incorretos).
      * Outliers naturais (MAPE > 1000%).
      * Problemas estruturais (ex: mudanças em OTAs).
* **Impacto:**
  * **Atraso em ações corretivas** (ex: correção de bloqueios).
  * **Sobrecarga do time de DataOps** com demandas reativas.
  * **Decisões sem agilidade** pela diretoria.


### **2. Solução Proposta**

**Ferramenta Self-Service de Auditoria (GCP: BigQuery + Looker Studio)**

* **Objetivo:**
  * Permitir que **gestores e PM investiguem variações do MAPE em minutos**, sem dependência do DataOps.
  * Gerar **acionáveis claros** para o time técnico (ex: "Corrigir bloqueios no imóvel X").
* **Princípios:**
  * **Autonomia para não-técnicos:** Interface intuitiva com filtros e visualizações pré-definidas.
  * **Classificação automática de causas:** Sistema que categoriza problemas sem necessidade de queries manuais.
  * **Foco em ação:** Relatórios com recomendações diretas para o DataOps.

### **3. Plano de Implementação (Etapas)**

#### **Fase 1: Infraestrutura**

| **Tarefa** | **Responsável** | **Entregável** |
|----|----|----|
| 1.1. Migrar dados do S3/Athena para BQ | DataOps | Tabelas particionadas por data no BQ |
| 1.2. Criar views de auditoria | DataOps | Views: `v_mape_comparison`, `v_root_cause` (com lógica de classificação de erros) |
| 1.3. Otimizar performance | DataOps | Clustering/indexação para consultas < 10s |


#### **Fase 2: Dashboard Self-Service**

| **Tarefa** | **Responsável** | **Entregável** |
|----|----|----|
| 2.1. Criar protótipo no Looker Studio | DataOps/Solutions | Layout com: |
|    |    | - Filtros amigáveis (períodos, tipo de erro) |
|    |    | - Gráfico de variação do MAPE (linha do tempo) |
|    |    | - Tabela "Top 10 Imóveis Impactados" |
| 2.2. Implementar drill-down por ID | DataOps/Solutions | Página detalhada: |
|    |    | - Gráfico real vs. previsto |
|    |    | - Flags visuais: `n_infs`, bloqueios, outliers |