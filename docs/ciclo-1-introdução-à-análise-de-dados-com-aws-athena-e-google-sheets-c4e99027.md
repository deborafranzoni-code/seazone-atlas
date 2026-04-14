<!-- title: Ciclo 1: Introdução à Análise de Dados com AWS Athena e Google Sheets | url: https://outline.seazone.com.br/doc/ciclo-1-introducao-a-analise-de-dados-com-aws-athena-e-google-sheets-ORKcnoxez0 | area: Tecnologia -->

# Ciclo 1: Introdução à Análise de Dados com AWS Athena e Google Sheets

# **Aula Introdutória (1 hora):**

* **Conectando-se à AWS:**
  * Acessando a console da AWS.
  * Visão geral dos serviços AWS relevantes.
* **Introdução ao AWS Athena:**
  * Conceitos básicos do Athena.
  * Navegação pela interface do Athena.
* **Conhecendo a Camada Enriched:**
  * Visão geral das tabelas `Monthly_fat_locations` e `details`.
  * Estrutura e tipos de dados das tabelas.
* **Praticando SQL no Athena:**
  * Escrita de consultas simples.
  * Uso de cláusulas SELECT, WHERE, GROUP BY, ORDER BY.
* **Exportando Resultados:**
  * Como baixar resultados de consultas em formato CSV.
* **Análise de Dados no Google Sheets:**
  * Importação de arquivos CSV.
  * Uso de fórmulas e funções básicas.
  * Criação de gráficos.

**Ferramentas:**

* AWS Athena
* Google Sheets
* ChatGPT

**Objetivos de Aprendizado:**

* Conectar-se à AWS.
* Conhecer e manipular as tabelas da Camada Enriched.
* Praticar SQL usando o Athena.
* Baixar resultados em formato CSV.
* Analisar dados usando o Google Sheets.

# Desafio

**Contexto:**

A empresa está planejando expandir suas operações e precisa identificar as melhores cidades para investir com base nos dados do Airbnb. Sua tarefa é fornecer insights que ajudarão na tomada de decisão.

**Tarefa:**


1. **Identificar as Top 5 Cidades por Faturamento Médio:**
   * Utilize o AWS Athena para consultar a tabela `Monthly_fat_locations`.
   * Escreva uma consulta SQL que retorne as 5 cidades com o maior `average_revenue`.
   * Certifique-se de filtrar os dados para o mês e ano mais recentes disponíveis (`month_year`).
2. **Analisar Listings Qualificados:**
   * Para cada uma das 5 cidades identificadas, calcule o percentual de listings qualificados (`count_qualified_listings`).
   * Um listing qualificado é definido como aquele com mais de 10 reviews, instant book ativado e faturamento nos últimos 6 meses maior que zero.
   * Calcule: `(count_qualified_listings / count_listings) * 100` para obter o percentual.
3. **Apresentar os Resultados:**
   * Baixe o resultado da consulta em formato CSV.
   * Importe o CSV para o Google Sheets.
   * Crie um relatório que inclua:
     * Uma tabela resumindo os dados coletados.
     * Gráficos que representem visualmente o faturamento médio e o percentual de listings qualificados por cidade.
     * Uma breve análise escrita interpretando os resultados e recomendando as cidades mais promissoras para investimento.
4. **Entrega:**
   * Compartilhe o documento do Google Sheets com seu supervisor.
   * Esteja preparada para apresentar seus achados em uma reunião breve.

**Entrega Esperada:**

* Consultas SQL utilizadas.
* Documento do Google Sheets com análise, gráficos e insights.
* Apresentação clara e profissional dos resultados.