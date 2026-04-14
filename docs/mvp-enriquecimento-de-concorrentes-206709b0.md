<!-- title: [MVP] Enriquecimento de Concorrentes | url: https://outline.seazone.com.br/doc/mvp-enriquecimento-de-concorrentes-ML0fCCfUhW | area: Tecnologia -->

# [MVP] Enriquecimento de Concorrentes

**Data:** 10 de Outubro de 2023 

**Autores:** Lucas Abel da Silveira


## **1. Contexto e Objetivo**

A atual Plataforma de Inteligência de Concorrentes estabeleceu uma base sólida para o diagnóstico da qualidade dos clusters através do **Health Score** e para o recrutamento inicial de candidatos. No entanto, o uso contínuo pela equipe de Revenue Management revelou oportunidades significativas de aprimoramento, tanto na usabilidade da ferramenta atual quanto na expansão de suas capacidades para encontrar concorrentes relevantes de forma mais ampla e inteligente.

Este documento de Discovery está dividido em duas fases propostas:

* **Fase 1: Melhorias na Ferramenta de Visualização e Análise:** Foco em aprimorar a usabilidade e a eficácia das funcionalidades existentes, resolvendo dores imediatas da equipe.
* **Fase 2: Enriquecimento Avançado com Modelo Lookalike:** Uma iniciativa estratégica para expandir os conjuntos de concorrentes através de técnicas de semelhança, superando as limitações geográficas.


---

### **Fase 1: Melhorias na Ferramenta de Visualização e Análise**

O objetivo desta fase é refinar as funcionalidades atuais para torná-las mais poderosas e alinhadas aos processos manuais já realizados pela equipe.

#### **1.1. Aprimoramento do Diagnóstico de Outliers \*\* Alinhar e trazer de outra iniciativa que já começou.** 

* **Problema Atual:** A identificação de *outliers*baseia-se unicamente na precificação (`**preco_medio**`). A equipe de RM, no entanto, também realiza análises com base no **faturamento** (`**last_90_fat**`) para identificar inconsistências.
* **Proposta de Melhoria:**

  
  1. **Novo Cálculo de Outlier:** Criar uma nova lógica para identificar *outliers* de faturamento dentro de cada categoria, utilizando o mesmo método IQR (Intervalo Interquartil) já empregado para preços.
  2. **Novo Flag na Tabela** `**listings_health_details**`**:** Adicionar uma coluna booleana `**faturamento_incompativel**` para sinalizar os imóveis que estão fora do intervalo de faturamento esperado para sua categoria.
  3. **Atualização do Health Score (Opcional):** Avaliar a inclusão do percentual de *outliers* de faturamento como um novo componente ou como um fator de ajuste no cálculo do `**score_estratificacao**`.

#### **1.2. Expansão dos Critérios de Recrutamento de Candidatos**

* **Problema Atual:** A função de recrutamento de candidatos é muito restrita, considerando apenas imóveis no mesmo polígono e com o mesmo número de quartos. Isso ignora conceitos importantes que a equipe utiliza manualmente, como "compensação" e "equivalência".
* **Proposta de Melhoria:** Evoluir a lógica da função `**get_competitors_data_no_strata**` e da tabela `**competitors_candidates**` para incluir os seguintes critérios de busca:

  
  1. **Compensação por Quartos:** Incluir como candidatos imóveis com `**number_of_bedrooms**` igual a `**N-1**` e `**N+1**` (onde N é o número de quartos da categoria alvo).
  2. **Polígono Expandido:** Permitir a busca por candidatos em polígonos vizinhos ou em uma área geográfica ligeiramente maior que a do polígono original.
  3. **Formalização da Equivalência:** Criar um mecanismo para que a equipe possa registrar categorias "equivalentes" (ex: uma categoria em Maraú e outra em São Miguel dos Milagres com comportamento de preços semelhantes). O sistema, ao buscar candidatos, também consideraria imóveis dessas categorias equivalentes.

#### **1.3. Aprimoramentos no Painel Visual (Looker Studio)**

* **Problema Atual:** O painel atual é funcional, mas falta flexibilidade para análises mais profundas, como a  filtrar concorrentes com alta frequência de incompatibilidade.
* **Proposta de Melhoria:**

  
  1. **Novos Filtros Interativos:**
     * Filtro de `**percentual_freq_incompatibilidade**` (ex: mostrar apenas imóveis > 30%).
     * Filtro de `**status**` (Verde, Amarelo, Vermelho).
     * Filtro de `**potencial**` (A, B, C) na tabela de candidatos.
  2. **Visualização de Outliers\*\*:** Adicionar colunas na tabela de detalhamento (`**listings_health_details**`) para exibir claramente se o imóvel é *outlier* de preço e/ou de faturamento.
  3. **Melhoria na Exportação:** Garantir que os filtros aplicados no painel sejam refletidos nos dados exportados, facilitando análises offline.


---

### **Fase 2: Enriquecimento Avançado com Modelo Lookalike**

O objetivo desta fase é implementar uma solução de Machine Learning para identificar concorrentes "semelhantes" que não estão geograficamente próximos, mas que compartilham características de comportamento de preço e demanda.

#### **2.1. Objetivo da Fase**

Expandir drasticamente a base de concorrentes para categorias críticas (especialmente as com status "vermelho" e "amarelo"), encontrando imóveis em outras regiões que sirvam como referência de precificação, aumentando a robustez das estratégias de Revenue Management.

#### **2.2. Proposta de Implementação**


1. **Definição de Parâmetros de Semelhança:** O modelo será treinado para encontrar imóveis com base em um vetor de características, incluindo:
   * **Comportamento de Preço:** Média de preço, sazonalidade (curva de preço ao longo do ano), variabilidade.
   * **Características do Imóvel:** `**listing_type**`, `**number_of_bedrooms**`
   * **Performance de Demanda:** , `**Faturamento**` Preço, sazonalidade
   * **Características da Região :** Atributos agregados do polígono de origem.
2. **Desenvolvimento do Modelo de Machine Learning:**
   * Criar um processo de treinamento que, para uma categoria de referência (ex: "Apartamento 2 quartos em Florianópolis"), encontre os *N* imóveis mais semelhantes em todo o banco de dados que não pertençam ao seu polígono original.
   * O modelo gerará um "score de semelhança" para cada par de imóveis.
3. **Integração e Validação:**
   * Os resultados do modelo serão apresentados em uma nova seção da plataforma ou da tabela `**competitors_candidates**`, com uma tag específica, como `**origem: lookalike**`.
   * A equipe de RM fará a validação final, avaliando se as sugestões fazem sentido. Se aprovadas, os imóveis serão adicionados às categorias através do campo de **equivalência**, formalizando o processo que hoje é manual.

#### **2.3. Impacto Esperado**

* **Redução de Clusters Críticos:** Aumentar o número de concorrentes para categorias com poucos ou nenhum concorrente local.
* **Precificação Mais Robusta:** Permitir a precificação baseada em referências de mercado mais amplas, especialmente em regiões emergentes ou com baixa oferta.
* **Automação e Eficiência:** Reduzir o tempo gasto pela equipe em buscas manuais por equivalentes, que hoje é feita por "olhômetro" e tentativa e erro.


---

### **3. Próximos Passos e Priorização**

Conforme discutido na reunião, as duas fases representam esforços diferentes. A Fase 1 consiste em melhorias incrementais e de entrega mais rápida, enquanto a Fase 2 é uma iniciativa estratégica com maior complexidade.


1. **Decisão de Prioridade:** A equipe de Revenue Management (Viviane e Victor) deve deliberar qual iniciativa trará maior valor no curto prazo:
   * **Acelerar a Fase 1 (Melhorias Incrementais):** Para resolver dores imediatas e melhorar a usabilidade da ferramenta atual.
   * **Priorizar a Fase 2 (Lookalike):** Para investir em uma solução de maior impacto estratégico, com entrega em um prazo mais longo.
2. **Início do Desenvolvimento:** Após a definição da prioridade, a equipe de desenvolvimento alocará recursos para iniciar a construção da funcionalidade escolhida, com o objetivo de colocar a primeira versão em produção nas próximas semanas.

Este documento serve como guia para as próximas etapas do projeto, garantindo que as evoluções estejam alinhadas com as necessidades de negócio e visem expandir a capacidade analítica e de ação da equipe de Revenue Management.