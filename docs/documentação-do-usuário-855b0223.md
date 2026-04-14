<!-- title: Documentação do Usuário | url: https://outline.seazone.com.br/doc/documentacao-do-usuario-M2BerXw8gS | area: Tecnologia -->

# Documentação do Usuário

**O que é o Dashboard de Saúde e Qualidade de Categorias:** O Dashboard de Saúde e Qualidade de Categorias é uma ferramenta desenvolvida para apoiar o time de Revenue Management (RM) no monitoramento contínuo da qualidade das categorias de concorrência. Seu principal objetivo é identificar se uma categoria possui uma base de concorrentes saudável, consistente e confiável para apoiar decisões de precificação e estratégia. A partir dessa análise, o dashboard sinaliza categorias que estão em boas condições e aquelas que necessitam de ajustes ou reforços.

#### Visão Geral do Dashboard: 

Para cada categoria, são exibidas métricas que explicam o motivo do status atribuído, permitindo ao usuário compreender rapidamente **quais fatores impactam negativamente ou positivamente** a qualidade da categoria. Além da análise agregada, o painel permite: Explorar os **imóveis individuais** que compõem uma categoria; Analisar a **frequência de incompatibilidade de preço**; Identificar oportunidades de melhoria para categorias críticas; Visualizar **sugestões de novos concorrentes** para fortalecer categorias com baixa qualidade.


1. Aba de Painel de Saúde

   
   1. **Filtros Gerais:**

      Há cinco filtros no topo do dashboard, que permitem segmentar e refinar a análise, os quais são:
      * Categoria
      * Status (se a categoria está com a saúde verde, amarela ou vermelha)
      * Polígono (região que a categoria está associada)
      * Strata (SIM, JR, SUP, TOP, MASTER)
      * Quartos (número de quartos que uma categoria possui)

      ![](/api/attachments.redirect?id=32c694c9-6a49-4387-a014-e071270bb4ca " =557.5x51.5")

      Os filtros afetam todas as visualizações de forma integrada, permitindo análises rápidas e direcionadas.

      \
   2. **Tabela de Diagnóstico de Saúde e Qualidade dos Clusters (Categorias):**

      ![](/api/attachments.redirect?id=35111c31-c2dd-402a-873f-4cea196f19ce " =641x133")

      *Indicadores de Saúde da Categoria:*
      * **Score de Quantidade**: avalia se a categoria possui um número adequado de concorrentes.
      * **Score de Frequência**: analisa a recorrência de incompatibilidades de preço ao longo do tempo.
      * **Score de Estratificação**: mede a consistência dos preços dentro da categoria.

        \
        Esses indicadores permitem identificar **qual aspecto da categoria está comprometido**, direcionando ações mais assertivas.

        \

      *Status das categorias:*
      * **Verde**: categoria saudável, com base de concorrentes adequada e indicadores estáveis.
      * **Amarelo**: categoria em atenção, apresentando algum nível de inconsistência ou fragilidade.
      * **Vermelho**: categoria crítica, com necessidade clara de ajustes ou reforço da base competitiva.

        O status é calculado a partir de um conjunto de indicadores, apresentados no próprio dashboard para facilitar a interpretação.

        \

      *Métricas de Distorção da Meta:*
      * % Compensação: Percentual de listing por compensação.
      * Gap Mediana: Porcentagem de diferença entre a Meta e a Mediana do faturamento do cluster.
      * Z-Score: Mede quantos desvios padrão o preço atual está distante da média da categoria.
      * Gap Média: Diferença percentual entre a Meta e a Média do cluster.

      \
   3. **Tabela de Detalhamento dos Imóvel numa Categoria Selecionada:**

      Para uma análise mais granular, o dashboard permite visualizar os imóveis que compõem uma categoria específica. Nessa visão, é possível analisar informações individuais, como: Frequência de incompatibilidade de preço; Modo de categorização; categoria do imóvel; comportamento histórico de preço do imóvel; Faturamento do Imóvel; Meta do Cluster do Imóvel; % de Distância do Faturamento da Meta; Taxa de Ocupação; Diária Média do Imóvel e do Cluster; e Status na Quarentena.

      Essa análise auxilia na identificação de imóveis que impactam negativamente a saúde da categoria.

      ![](/api/attachments.redirect?id=61904dc7-4486-4374-82af-9b7b6e2eec68 " =513x109")

      Filtros:

      ![](/api/attachments.redirect?id=b28f4924-4610-47ef-ab3d-38338ec443de " =143.5x54")

      ![](/api/attachments.redirect?id=a837e000-a144-47ff-8a2b-c5af2e6a724d " =143.5x183")
   4. **Tabela de Candidatos a Concorrentes:**

      Para categorias classificadas como **amarelas ou vermelhas**, o dashboard disponibiliza uma tabela de **candidatos a concorrentes**. Essa tabela apresenta imóveis que podem ser considerados para fortalecer a categoria, utilizando diferentes estratégias de sugestão, como: Regras baseadas em similaridade estrutural; Expansão controlada de clusters (quartos adjacentes e/ou polígonos vizinhos); Similaridade entre imóveis baseada em características e comportamento. Cada candidato possui uma **origem** associada (por exemplo, similaridade ou machine learning), facilitando o entendimento de como aquela sugestão foi gerada. 

      ![](/api/attachments.redirect?id=9dde1a5a-d40f-4b29-bbc6-016cc5fb4047 " =552.5x129")

   Cada candidato apresenta uma coluna chamada **Origem**, que indica como aquela sugestão foi gerada. As possíveis origens são:
   * **machine_learning**: candidatos sugeridos a partir de clusters gerados por modelo.
   * **expandido_quartos**: inclusão de imóveis com número de quartos adjacentes.
   * **expandido_polígono**: inclusão de imóveis de regiões geográficas semelhantes.
   * **similaridade**: imóveis selecionados com base em similaridade de características e comportamento.

   Essa distinção permite avaliar o **nível de proximidade e o grau de expansão** utilizado em cada sugestão.

   ![](/api/attachments.redirect?id=44b007bf-d2cf-4446-8cad-37d91b3b5e8e " =213.5x165.5")

   e. Gráfico de distribuição dos status: O gráfico **Distribuição dos Status** apresenta uma visão consolidada da quantidade de categorias em cada estado de saúde: **verde, amarelo e vermelho**. Ele responde rapidamente à pergunta: "Como está, de forma geral, a saúde das categorias hoje?".

   ![](/api/attachments.redirect?id=78837a4b-5709-4a06-b8f3-eed1b7ac0eff " =214x185")



2. **Aba de Auditoria do Cluster**

   A aba de Auditoria do Cluster permite analisar detalhadamente o comportamento de faturamento dos concorrentes dentro de uma ou mais categorias. 

   \
   
   1. **Filtro Geral:** 

      Nessa aba, é usado como filtro a Categoria, em que pode selecionar uma ou mais categorias para possíveis comparações no Boxplot.![](/api/attachments.redirect?id=a154ad6a-ba72-4266-a62c-f0cd8063d18a " =641x55")
   2. **Boxplot Comparativo:** 

      O Boxplot Comparativo apresenta a **distribuição do faturamento dos concorrentes** dentro do cluster selecionado. Ele permite analisar a distribuição geral do faturamento do cluster e comparar múltiplas categorias simultaneamente.

      ![](/api/attachments.redirect?id=4b154741-986b-45d0-9569-cc4291eaf925 " =513x319")

      *Diferenciação visual dos concorrentes:*
      * Concorrentes Nativos: Representam os concorrentes originalmente pertencentes à categoria. São exibidos com bolinhas verdes vazadas.
      * Concorrentes Compensados: Concorrentes adicionados por mecanismos de compensação. São exibidos com bolinhas vermelhas preenchidas.

        \
   3. Calendário de Concorrentes do Mês Atual:

      O Calendário Forense apresenta uma visão detalhada do comportamento diário dos concorrentes no mês atual, permitindo uma análise granular da disponibilidade e do faturamento.

      ![](/api/attachments.redirect?id=b0fa4f12-67a0-49f6-8eef-94509fd9e9ad " =641x317")

   A visualização é apresentada em formato de tabela matricial:
   * **Linhas:** representam os concorrentes do cluster
   * **Colunas:** representam os dias do mês
   * **Células:** representam o valor da diária de cada concorrente em cada dia

   \
   *Status:* Indica a situação do concorrente naquele dia:
   * Available (Livre): disponível para reserva
   * Occupied (Ocupado): reservado
   * Blocked (Bloqueado): indisponível para reserva