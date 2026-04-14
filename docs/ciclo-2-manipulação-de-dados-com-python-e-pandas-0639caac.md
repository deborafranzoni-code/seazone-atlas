<!-- title: Ciclo 2: Manipulação de Dados com Python e Pandas | url: https://outline.seazone.com.br/doc/ciclo-2-manipulacao-de-dados-com-python-e-pandas-k5x7tM3Z20 | area: Tecnologia -->

# Ciclo 2: Manipulação de Dados com Python e Pandas

# **Aula Introdutória (1 hora):**

* **Conectando-se à AWS via VS Code:**
  * Configuração do ambiente de desenvolvimento.
  * Extensões necessárias para integração com AWS.
* **Introdução ao Python e Pandas:**
  * Conceitos básicos de Python.
  * Manipulação de dados com Pandas.
* **Uso do Jupyter Notebook:**
  * Configuração e execução de notebooks.
  * Estrutura de um notebook (células de código e markdown).
* **Consultas Avançadas no Athena:**
  * Uso de joins, subconsultas e funções agregadas.
* **Data Cleaning e Preparação de Dados:**
  * Identificação e tratamento de valores ausentes.
  * Conversão de tipos de dados.
  * Criação de novas colunas e features.
* **Utilizando o ChatGPT:**
  * Como obter assistência para código e resolução de problemas.

**Ferramentas:**

* AWS Athena
* ChatGPT
* VS Code
* Python
* Jupyter Notebook

**Objetivos de Aprendizado:**

* Conectar-se à AWS via VS Code.
* Aprofundar o conhecimento nas tabelas da Camada Enriched.
* Praticar SQL avançado no Athena.
* Manipular arquivos CSV usando Python e Pandas.
* Realizar análise exploratória de dados no Jupyter Notebook.

# Desafio

**Contexto:**

A empresa deseja entender quais fatores influenciam as avaliações (star ratings) dos listings no Airbnb e se um imóvel com maior star rating consegue faturar mais.

**Tarefa:**


1. **Extração de Dados:**
   * Utilize o Athena para consultar a tabela
   * Baixe o resultado em formato CSV.
2. **Limpeza e Preparação dos Dados:**
   * Importe o CSV para um Jupyter Notebook utilizando Pandas.
   * Realize o tratamento de dados:
     * Remova ou impute valores ausentes.
     * Converta colunas para os tipos de dados adequados.
     * Codifique variáveis categóricas (por exemplo, `is_superhost`, `can_instant_book`).
3. **Análise Exploratória de Dados (EDA):**
   * Utilize técnicas de EDA para identificar correlações entre o `star_rating` e outras variáveis.
   * Crie visualizações como gráficos de dispersão, histogramas e matrizes de correlação.
   * Analise quais fatores têm maior impacto nas avaliações dos hóspedes.
   * Seguimente os imóveis pelas principais características para conseguir avaliar o impacto do star rating no faturamento.
4. **Insights e Recomendações:**
   * Documente suas descobertas no Jupyter Notebook.
   * Forneça insights acionáveis que a empresa possa utilizar para melhorar os listings.
   * Sugira estratégias baseadas nos fatores identificados.
5. **Entrega:**
   * Envie o arquivo do Jupyter Notebook (.ipynb) com todo o código, análises e visualizações.
   * Certifique-se de que o notebook esteja bem organizado e comentado.

**Entrega Esperada:**

* Jupyter Notebook com o código Python e análises.
* Visualizações gráficas que suportem suas conclusões.
* Insights e recomendações bem fundamentados.