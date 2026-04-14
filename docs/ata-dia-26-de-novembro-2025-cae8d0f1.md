<!-- title: Ata dia 26 de Novembro 2025 | url: https://outline.seazone.com.br/doc/ata-dia-26-de-novembro-2025-M8SpNm18Wq | area: Tecnologia -->

# Ata dia 26 de Novembro 2025

# Ata de Reunião: Quinzenal BU - Dados Imóveis

**Data:** 26 de Novembro\n**Participantes:** Lucas Abel , Fábio Garcia, Arilo Claudio, Lucas Machado Azevedo.\n**Gravação:** **[Link da Gravação](https://drive.google.com/file/d/1iQ_PkBPDvU8NUq2BIzX5Sezs0pQL4iGU/view)**


---

## 1. Revisão de KPIs e Dados

**Status dos KPIs:**

* **Preenchimento:** Fábio confirmou que ele (ou o Victor) ficará responsável pelo preenchimento dos KPIs de identificação. Alguns dados históricos ("acima da meta") precisarão ser puxados retroativamente.
* **Concorrentes:**
  * Lucas Abel apresentou dados sobre o crescimento de concorrentes categorizados (dobrou em 15 dias).
  * **Discussão sobre "Concorrentes Úteis":** Arilo e Fábio levantaram a necessidade de saber qual percentual desses concorrentes é realmente aproveitável (estão dentro dos polígonos de atuação da RM e passam nos filtros de qualidade).
  * **Definição:** Foi acordado criar ou desmembrar um KPI para "Concorrentes Categorizados Úteis": listings que estão no polígono, passam nas regras de filtragem, mas ainda não foram categorizados (nem pela automação, nem manualmente). O objetivo é que esse número tenda a zero.
* **Qualidade das Categorias:** Atualmente, 85% das categorias têm qualidade alta. O objetivo é reduzir a porcentagem de categorias de baixa qualidade a cada reunião.

**System Price (SP):**

* **Adoção em Não-Sazonais:** Está em 55%. A meta para este mês é 60%, e Lucas Abel acredita que será batida com as inclusões recentes feitas pelo Victor. Meta final de 100% até o fim do ano.
* **Desempenho por Categoria:** Houve uma queda nos indicadores (crítico, berlinda, etc.). Lucas explicou que isso se deve à entrada de novas praças (São Paulo, Brasil) que ainda oscilam, diluindo o bom desempenho consolidado de Goiânia.
* **Regionalização:** Fábio solicitou e Lucas confirmou que o Dashboard (ainda não em produção oficial) já permite filtrar o desempenho do System Price por região (ex: SP SP Goiânia, SP Brasília), para evitar análises misturadas ("salada de dados").

## 2. Suporte e Iniciativas em Andamento

**Suporte:**

* **Imóveis em Quarentena:** Único ticket aberto. Regra de negócio corrigida e enviada para validação do time de operações (Victor).

**Entregas (Delivery):**

* **Quarentena de Baixa Qualidade (Concorrentes):** Houve um pequeno atraso na planilha automatizada, mas a limpeza da base será feita manualmente ainda esta semana, cruzando dados da lista da Vivi.
* **Enriquecimento de Concorrentes (Lookalike):** Em desenvolvimento, previsão de entrega para validação em 1-2 semanas.
* **System Price (Evolução Não-Sazonais):** Em andamento contínuo.

**Backlog Imediato:**

* Expansão da categorização automática.
* Colocar o Dashboard de Meta Performance em produção.
* System Price para Sazonais (previsto para próximos trimestres).

## 3. Discussão: Limpeza de Base e Quarentena

**Preocupação Operacional:**

* Fábio expressou receio sobre limpar concorrentes "outliers" (que faturam muito acima da média) no final do mês, pois isso pode facilitar artificialmente o batimento da meta.
* **Consenso:** Concordaram que a limpeza é necessária filosoficamente (dados corretos), mas o discurso deve ser alinhado para explicar eventuais mudanças bruscas nos resultados.

**Processo de Quarentena (Definição Técnica):**

* Lucas Abel esclareceu que o processo não depende mais apenas da lista manual da Vivi. Existem lógicas implementadas:

  
  1. Bloqueio de "Bruxos" (preços/faturamentos irreais).
  2. Remoção de imóveis antigos sem reviews recentes.
  3. Nova lógica (em validação): Identificar imóveis ocupando muito acima da categoria com preços discrepantes.
* **Futuro:** O objetivo é que esses concorrentes identificados como ruins vão para "Inativos" no sistema, saindo da base de cálculo.

## 4. Alinhamento Estratégico e Dores do Time (Feedback do Arilo)

**Mudança de Foco:**

* Arilo sugeriu que as próximas reuniões foquem menos em KPIs de resultado e mais em **problemas e dores reais** do time de precificação, independente da solução tecnológica.

**Dores Levantadas (Fábio):**

* **Recorrência de Criticidade:** Hoje analisa-se o imóvel "crítico" ou "berlinda" apenas no mês vigente. A dor é não conseguir identificar facilmente o imóvel que é **recorrentemente crítico** (histórico de má performance), o que é um forte indício de Churn.
* **Validação de Hipóteses de Mercado (Antecedência):** A Seazone vende muito "em cima da hora". A dúvida é: isso é uma característica da região ou é porque a Seazone só consegue precificar para vender em cima da hora? Falta dados comparativos para saber se o concorrente está vendendo com mais antecedência.

## 5. Roadmap e Pilares de Produto

Lucas Abel apresentou um mapeamento dividido em 4 pilares para organizar o backlog:


1. **Plataforma de Precificação (Sirius):**
   * Considerado consolidado (Core Engine, Setup, AGC).
2. **Inteligência de Mercado (Concorrentes/PIC):**
   * Em construção: Quarentena e Enriquecimento.
   * Fábio comentou que o foco atual no System Price já serve como uma excelente "lupa" para validar a qualidade dos concorrentes.
3. **Otimização e Automação:**
   * Consolidado: Escadinha e Gaper.
   * **Em desenvolvimento:** System Price (evolução dos não-sazonais).
   * **Novidade:** Discutiu-se o "Motor de precificação reativo à ocupação" (aumentar preço automaticamente se bater meta muito cedo). Lucas confirmou que isso está no escopo do app em desenvolvimento.
   * **Planejamento Sazonais:** A ideia é começar o System Price Sazonal por **Florianópolis** como laboratório, por ter mais dados, antes de expandir para o Nordeste.
4. **Análise de Desempenho:**
   * Meta 2.0: Discussão pendente sobre revisão da lógica de metas (Bill levantou a possibilidade).
   * Alertas: Ideia de criar alertas para "Recorrência de status Crítico" (sugestão baseada na dor levantada pelo Fábio).

## 6. Próximos Passos (Action Items)

* **Lucas Abel:**
  * Organizar a planilha de backlog com base nas discussões (trazer estruturada na próxima call).
  * Incluir Victor e Vivi nos convites das próximas reuniões para trazerem a visão operacional do dia a dia.
* **Fábio/Time:**
  * Preencher os KPIs históricos faltantes.
  * Refletir e trazer novas "dores" e problemas operacionais nos próximos 15 dias.
* **Geral:**
  * Próxima reunião focará em enriquecer o backlog com base nos problemas reais trazidos pelos analistas (Victor/Vivi).