<!-- title: Validação de Qualidade de Concorrentes | url: https://outline.seazone.com.br/doc/validacao-de-qualidade-de-concorrentes-hBnbdzRGOG | area: Tecnologia -->

# Validação de Qualidade de Concorrentes

### **Product Discovery: Validação de Qualidade de Concorrentes**

* **Iniciativa:** Validação de Qualidade de Concorrentes
* **Objetivo de Negócio Associado:** Aumentar a Densidade e Qualidade dos Dados de Concorrentes
* **Status:** Em Discovery
* **Versão:** 1.0

### 1. Resumo Executivo 

Nossa capacidade de precificar imóveis de forma eficaz e automática depende diretamente da qualidade dos dados de nossos concorrentes. Atualmente, operamos com uma visibilidade limitada sobre essa qualidade, especialmente em clusters de precificação com poucos concorrentes ou com dados ruidosos. Este projeto propõe a criação de um **"Painel de Saúde dos Clusters"**, uma ferramenta de diagnóstico que mede, de forma contínua, a qualidade de nossos dados de concorrentes e uma **"Ferramenta de Recrutamento"** que permite ao time de RM melhorar ativamente a base de concorrentes. O objetivo é transformar a confiança cega em confiança informada, capacitando o time de RM a tomar decisões melhores e pavimentando o caminho para a automação da precificação.

### 2. Contexto Geral (Onde Estamos Hoje)

A Seazone utiliza um sistema de precificação que se baseia fortemente na análise de mercado, especificamente nos dados de nossos concorrentes diretos. Para tornar essa análise relevante, agrupamos os concorrentes em "clusters" ou categorias extremamente granulares, definidas por Cidade-Polígono-Strata-Nº_Quartos. A performance (preço, ocupação) dos membros de um cluster é o principal insumo para nossas estratégias de preço.

Para um imóvel ser considerado um "concorrente" oficial, ele precisa ser "estratificado" (classificado em uma categoria de qualidade como SIM, JR, SUP, TOP, MASTER), seja por um analista humano ou pelo nosso modelo de IA. A precisão dessa estratificação e a robustez dos dados de cada concorrente são, portanto, a fundação de toda a nossa inteligência de precificação.

### 3. O Problema Central (As Dores que Enfrentamos)

Apesar da sofisticação do nosso sistema de clusters, enfrentamos dores críticas que limitam sua eficácia e escalabilidade:


1. **Decisões no Escuro (A Dor da Incerteza):** O time de RM não possui um mecanismo para avaliar a "saúde" de um cluster antes de usá-lo para precificar. Eles não sabem se um cluster com 10 concorrentes é composto por 10 imóveis sólidos ou por 4 sólidos e 6 com dados problemáticos (strata errada, preços anômalos, etc.). Isso gera desconfiança e leva a ajustes manuais excessivos.
2. **Qualidade Inconsistente (A Dor dos "Clusters Magros"):** Muitos clusters possuem um número baixo de concorrentes (>7 é o mínimo desejável). Nestes casos, a presença de apenas alguns concorrentes com strata incorreta ou dados de baixa robustez distorce drasticamente as métricas de percentil, levando a sugestões de preço enviesadas e pouco confiáveis.
3. **Gargalo de Ação (A Dor da Ineficiência):** Mesmo quando um analista de RM suspeita que um cluster está fraco, não existe um processo ou ferramenta para "melhorá-lo" de forma eficiente. O trabalho de encontrar novos concorrentes qualificados dentro de um polígono é um processo de "caça" manual, lento e pouco escalável.


### 4. Solução Proposta: Ferramentas de Diagnóstico e Ação

\nPara resolver estas dores, propomos a construção de um produto composto por duas ferramentas integradas:

#### **Ferramenta 1: O Painel de Diagnóstico de Saúde dos Clusters**

Uma interface central que permite ao time de RM avaliar a qualidade de todos os clusters de forma rápida e visual.

* **Visão Macro (Health Score):** Uma tabela onde cada linha é um cluster, com colunas que medem os pilares da qualidade:
  * Health Score Geral: Uma nota consolidada (0-100) para priorização rápida.
  * **Concorrentes:** Quantidade de imóveis no cluster.
  * **Qualidade da Stratificação (%):** % de concorrentes cuja strata é considerada confiável (sem divergências ou performance incompatível).
  * **Robustez do Cluster (%):** % de concorrentes com dados sólidos (sem anomalias de preço, ocupação, histórico, etc.).
* **Visão Detalhada (Drill-Down):** Ao clicar em um cluster, o usuário acessa uma lista de todos os seus concorrentes, com flags que expõem os problemas individuais:
  * Divergência de Strata? (Ex: Humano: SUP vs. IA: MASTER).
  * Performance Incompatível? (Ex: Preço de TOP, mas faturamento de JR).
  * Baixa Robustez? (com detalhes sobre o motivo).
  * **Ação:** Exportar listas filtradas (ex: "Concorrentes com Strata Suspeita") para análise externa.
* **Ferramenta 2: A Ferramenta de Recrutamento de Concorrentes**

  Uma ferramenta acionável que permite ao RM ativamente melhorar a densidade e qualidade dos clusters.
  * **Fluxo de Trabalho:**

    
    1. O RM seleciona um cluster que precisa de mais concorrentes.
    2. O sistema busca em nosso banco de dados de listings brutos por "candidatos" que correspondam aos critérios do cluster (polígono, nº de quartos) mas que ainda não são concorrentes oficiais.
    3. A ferramenta exibe uma lista de candidatos com informações chave para qualificação:
       * Link do anúncio.
       * Status da Strata: (Ex: "Não Stratificado" ou "Strata Automática - Não Validada").
       * Potencial de Qualidade: (Ex: "Imóvel com +20 fotos, +10 reviews").
       * Strata Sugerida pela IA: (Se disponível).

**Ação do RM:** O RM pode, a partir desta lista, validar a strata sugerida pela IA ou realizar uma estratificação manual, "promovendo" o candidato a concorrente oficial e fortalecendo o cluster.


### 5. Definição de Pronto (DoD) 

Esta iniciativa será considerada "pronta" do ponto de vista de produto quando:

* **Funcionalidade Entregue:** Os componentes do MVP (Painel de Diagnóstico com os principais KPIs e a primeira versão da Ferramenta de Recrutamento) estão em produção e funcionais.
* **Documentação e Treinamento:** A equipe foi treinada sobre como usar as ferramentas e existe uma documentação clara sobre como interpretar as métricas de saúde.

  \n