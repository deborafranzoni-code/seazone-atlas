<!-- title: Documentação do Usuário | url: https://outline.seazone.com.br/doc/documentacao-do-usuario-oo7BIB3exN | area: Tecnologia -->

# Documentação do Usuário

**O que é o Dashboard de Auditoria de Variação de Concorrentes:**\nÉ uma ferramenta que compara dados de concorrentes entre duas datas e identifica de modo automatizado as causas das variações no período escolhido, proporcionando ao time de Revenue Management clareza e agilidade no diagnóstico.

### **Visão Geral do Dashboard:**


1. **KPIs agregados**: Essa parte do dashboard possibilita visualizar o número de concorrentes na data inicial e na data final, o número de concorrentes ganhos no período, o número de concorrentes perdidos no período e a variação líquida (diferença entre o número de concorrentes na data inicial e na data final). 

   ![KPIs agregados](/api/attachments.redirect?id=f8e526ed-e07c-41ca-aa82-d9cf1c0adb13 " =553.5x115.5")

   \
2. **Tabela detalhada**: É composta pelo ID do concorrente, categoria, status inicial (se o imóvel estava ativo/inativo/null na data inicial), status final(se o imóvel estava ativo/inativo/null na data final), tipo de mudança (perda ou ganho) e motivo da mudança. Os motivos de mudança podem ser:
   * **Passou nos filtros (reviews/fat)**: imóvel começou a cumprir os critérios mínimos de reviews/faturamento. ('passed_the_filters' virou true.)
   * **Mudou de categoria**: mesmo airbnb_listing_id trocou de 'category'.
   * **Falhou nos filtros (reviews/fat)**: imóvel deixou de cumprir os critérios mínimos de reviews/faturamento. (passed_the_filters virou false.)
   * **Ganhou categoria válida:** is_competitor virou true.
   * **Sem categoria válida**: is_competitor virou false.
   * **Morto**: is_dead virou true.
   * **Ativado por regra is_active**: mudança em is_active (quando passa a ser considerado ativo porque estava abaixo do limite de 15 manuais).
   * **Desativado** **por regra is_active**: quando excede o limite (>15) de manuais e é forçado para inativo.
   * **Voltou a ficar vivo**: is_dead virou false.

  OBS: Quando o caractere "-" aparece na tabela, significa que o imóvel **não estava na categoria na data em questão** (ex.: ainda não existia, ou já tinha mudado de categoria). 

 ![Tabela de Detalhamento da Variação](/api/attachments.redirect?id=9c47e681-1e30-41b9-a016-fe6d5f03d11b " =551x229")


3. **Gráfico de distribuição de motivos de mudança**: Aponta quantos imóveis mudaram por cada motivo durante o período escolhido para observação. Esse gráfico pode ajudar a identificar rapidamente qual foi o motivo predominante de mudança no período, por exemplo, se a maioria foi por mudança de categoria ou por falha nos filtros.

   ![Gráfico de distribuição de motivos de mudança](/api/attachments.redirect?id=466cc0da-1869-4a04-88e6-49dec49039a7 " =548.5x216.5")

### **Filtros de análise:**


1. É possível filtrar os dados por data, escolhendo uma data inicial e uma data final para observar os dados.
2. É possível filtrar a tabela detalhada pelo tipo da mudança (perda/ganho).
3. É possível filtrar a tabela detalhada pelo motivo da mudança.\n