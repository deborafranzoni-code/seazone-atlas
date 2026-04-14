<!-- title: Panorama de Aluguel por Temporada - Geração dos Dados[ Pipeline Automático] | url: https://outline.seazone.com.br/doc/panorama-de-aluguel-por-temporada-geracao-dos-dados-pipeline-automatico-oJC2kr9Hty | area: Tecnologia -->

# Panorama de Aluguel por Temporada - Geração dos Dados[ Pipeline Automático]

**Data:** 27/10/2025\n**Autor:** Lucas Abel da Silveira (PM de Dados)

**Stakeholders:** Leandro Shimanuki (Diretor de Marketing)

### **1. Visão do Projeto** 

Tornar a Seazone a principal referência em dados e inteligência de mercado para o aluguel por temporada no Brasil. Criaremos um ativo de marketing recorrente e de alto impacto, que fortalece nossa marca como autoridade, gera mídia espontânea e fornece insights valiosos para o mercado, investidores e nossos próprios clientes.

### **2. Problema** 

O Panorama anterior (2023) foi um sucesso, mas sua criação foi manual, pontual e baseada em uma metodologia de coleta de dados que não é mais escalável. A dependência de processos manuais impede a recorrência e a agilidade para gerar insights. Precisamos evoluir de um relatório estático para uma plataforma de dados dinâmica, que dê autonomia ao time de Marketing e garanta a sustentabilidade do projeto a longo prazo.

### **3. Objetivos** 

* **Objetivo de Negócio:** Solidificar o posicionamento da Seazone como líder de mercado, gerando pelo menos 3 menções na grande mídia com o lançamento do relatório.
* **Objetivo de Produto:** Criar uma fonte única e confiável de verdade sobre o desempenho do mercado de aluguel por temporada no Brasil.
* **Objetivo do Usuário (Marketing):** Proporcionar autonomia total para a equipe de Marketing explorar os dados, criar rankings, gráficos e insights de forma independente, sem a necessidade de intervenção técnica da equipe de Dados/Engenharia para cada nova análise.

### **4. O Que Estamos Construindo**

Uma plataforma de dados auto-suficiente, modelada em nossa infraestrutura padrão (GCP), cuja interface final será um conjunto de dashboards interativos no Looker. Esta plataforma permitirá ao Marketing gerar o relatório "Panorama do Aluguel por Temporada" de forma anual, além de explorar quatro estudos inéditos que trarão insights exclusivos ao mercado.

A solução será composta por três grandes módulos de visualização:


1. **Panorama Geral:** Uma visão macro do Brasil, com rankings e comparações entre estados e cidades.
2. **Análise Detalhada por Estado:** Uma visão aprofundada que permite filtrar e analisar as métricas de desempenho de cada unidade da federação.
3. **Estudos Inéditos:** Quatro análises exclusivas que gerarão conteúdo único e de alto valor para a Seazone.

### **5. Requisitos Funcionais**

**5.1. Módulo: Panorama Geral**

* **Dados:** O sistema deve permitir a visualização das seguintes métricas em nível nacional, por região e por estado:
  * Faturamento total.
  * Quantidade de imóveis (listings).
  * Diária média.
  * Taxa de ocupação média.
* **Visualizações:** O usuário deve conseguir gerar:
  * Rankings dos "Top 20" estados e cidades para cada métrica principal.
  * Gráficos de Barras mostrando a participação percentual das regiões do Brasil no faturamento total.
  * Séries históricas (2017+) mostrando a evolução do mercado nacional.

**5.2. Módulo: Análise Detalhada por Estado**

* **Dados:** Ao selecionar um estado, o sistema deve exibir:
  * As mesmas métricas do panorama geral, mas detalhadas para o estado e suas cidades.
  * Dados segmentados por tipo de imóvel (1 quarto, 2 quartos, 3+ quartos).
  * Dados segmentados por tipo de gestão (Profissional vs. Individual).
* **Visualizações:** O usuário deve conseguir gerar:
  * Ranking das "Top 20" cidades daquele estado.
  * Gráficos de barras verticais mostrando a evolução anual (2017+) do faturamento, número de imóveis, diária média e taxa de ocupação do estado.
  * Um infográfico de resumo com os principais KPIs do estado (crescimento YoY, diária média, etc.).

**5.3. Módulo: Estudos Inéditos (Fase 2 - Viabilidade a Ser Confirmada)**

*Este módulo contém análises de maior complexidade. A entrega dependerá de uma análise de viabilidade de esforço vs. impacto. Os estudos propostos como possibilidades são:*

* **Estudo 1 - Score de Infraestrutura:** Uma visualização que permita comparar o faturamento médio de imóveis com e sem determinadas amenities (ex: ar-condicionado, piscina, Wi-Fi/ com ou sem garagem ) por estado ou cidade.
* **Estudo 2 - Otimização de Capacidade:** Um gráfico que mostre a relação entre o número de quartos de um imóvel e seu faturamento médio anual, ajudando a identificar o "tamanho ideal" por região.
* **Estudo 3 - Sazonalidade da Demanda:** Um gráfico de linhas que mostre a taxa de ocupação média mês a mês para o Brasil e para os principais estados, destacando os picos de alta e baixa temporada.
* **Estudo 4 - Segmentação por Perfil:** Uma análise que agrupe imóveis por perfis temáticos (ex: "Família", "Home Office") e compare o desempenho de faturamento e ocupação entre eles.

**5.4. Funcionalidades Gerais**

* **Filtros:** Todos os dashboards devem permitir filtragem por:
  * Ano (2024, 2023, 2022, etc.).
  * Região, Estado, Cidade.
  * Tipo de imóvel e tipo de gestão.
* **Exportação:** O usuário deve conseguir exportar qualquer gráfico ou tabela para formatos de imagem (PNG) e de dados (CSV).

  \

### **6. Requisitos Não-Funcionais**

* **Performance:** Os dashboards devem carregar de firna rápida( segundos não minutos) .
* **Confiabilidade:** Os dados devem ser atualizados de forma automatizada e recorrente, com uma frequência a ser definida (ex: Mensal/ talvez trimestral a ser alinhado).
* **Usabilidade:** A interface no Looker deve ser intuitiva, permitindo que um usuário não-técnico do time de Marketing consiga explorar os dados e criar visualizações com autonomia.

### **7. Critérios de Sucesso**

* O time de Marketing consegue gerar 100% do relatório final do Panorama 2024 utilizando apenas os dashboards do Looker, sem necessidade de extrações de dados manuais.
* O relatório é publicado até o final de Janeiro de 2025.
* A geração de insights para os "Estudos Inéditos" leva menos de 2 horas de trabalho do analista de marketing.

### **8. Escopo**

* * **Fase 1 ( Entrega Inicial):**
    * **Dentro do Escopo:** Criação dos dashboards para o **Panorama Geral** e **Análise Detalhada por Estado**, com todas as funcionalidades e atualização mensal.
    * **Fora do Escopo:** Os "Estudos Inéditos" não serão desenvolvidos nesta fase.
  * **Fase 2 ( Pós Validação dos daos Fase 1):**
    * **Dentro do Escopo:** Análise de viabilidade (esforço vs. impacto) para cada um dos **Estudos Inéditos**. Desenvolvimento daqueles que forem priorizados.
    * **Fora do Escopo:** Qualquer nova funcionalidade não listada ou que surja durante o desenvolvimento da Fase 1.