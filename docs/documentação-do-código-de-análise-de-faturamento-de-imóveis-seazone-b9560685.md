<!-- title: Documentação do Código de Análise de Faturamento de Imóveis Seazone | url: https://outline.seazone.com.br/doc/documentacao-do-codigo-de-analise-de-faturamento-de-imoveis-seazone-BhmW4WQNmY | area: Tecnologia -->

# Documentação do Código de Análise de Faturamento de Imóveis Seazone

## Objetivo

O código tem como objetivo principal identificar imóveis Seazone com faturamento anômalo em relação aos seus concorrentes, considerando um período de 6 meses. A análise é baseada na comparação do faturamento de cada imóvel Seazone com uma banda de valores calculada a partir do faturamento de seus concorrentes de mesma categoria.

## Fontes de Dados

O código utiliza três arquivos CSV como entrada:

**[rm_concorrentes - Concorrentes com strata.csv](https://drive.google.com/file/d/1RUjvcibWo8Ax_tmYfJRDeNfObHFZ3O7v/view?usp=drive_link)**: Contém informações sobre os imóveis concorrentes, incluindo ID do Airbnb, categoria e strata. Essa informação foi extraída de uma [tabela fornecida pelo time de RM.](https://docs.google.com/spreadsheets/d/1LG4hvCMQZOwKbHXkuzL091Cs4LYu7_qHOC8ZDE0CZvY/edit?gid=452789173#gid=452789173)

**[concorrentes_faturamento](https://drive.google.com/file/d/1Zabgm01yhJBBtLXRgP4MuMkdow-iAyVF/view?usp=drive_link)**: Contém o faturamento mensal dos imóveis concorrentes. Esses dados foram extraídos do sirius através da query:

```sql
select *
from "revenuedata-ljkritvzunqm".daily_revenue_sapron drs
join  "inputdata-kdatqapgmwx1".setup_groups sg on sg.id_seazone = drs.listing
join "saprondata-9dkamzx2grjg".listing_status ls on drs.listing = ls.code
where sg.state='current' and sg.group_type = 'Categoria' 
and ls.status = 'Active'
and ls.churn  = false and cast(drs."date" as date)
BETWEEN date_add('month', -6, current_date) AND current_date;
```

**[faturamento_sz_alive_6m](https://drive.google.com/file/d/1W8XEI6wLruuz0lKWOKegJGrIcxDimzSH/view?usp=drive_link)**: Contém o faturamento mensal dos imóveis Seazone.  Esses dados foram extraídos da consulta na camada enriched através da query:

```sql
SELECT *
FROM analise_faturamento
WHERE state IS NOT NULL
  AND strata IS NOT NULL
  AND city IS NOT NULL
  AND listing_type IS NOT NULL
  AND (
    (ano = YEAR(CURRENT_DATE - INTERVAL 6 MONTH) AND mes >= MONTH(CURRENT_DATE - INTERVAL 6 MONTH))
    OR
    (ano = YEAR(CURRENT_DATE) AND mes <= MONTH(CURRENT_DATE))
  )
ORDER BY ano, mes;
```

## Etapas da Análise

O código realiza as seguintes etapas para identificar as anomalias:

### Preparação dos Dados:

* Leitura dos arquivos CSV e criação dos DataFrames `filtered_rm_concorrentes`, `listing_df` e `listing_sz_df`. 
* Mescla dos DataFrames para combinar informações de faturamento e categoria dos imóveis Seazone e concorrentes. 
* Filtragem dos dados para considerar apenas os últimos 6 meses. Formatação da categoria dos imóveis para facilitar a comparação. 

### Classificação dos Imóveis:

* Identificação das categorias presentes nos DataFrames de imóveis Seazone e concorrentes. Filtragem dos DataFrames para incluir apenas imóveis com categorias presentes em ambos os conjuntos de dados. Pois os imoveis seazone precisam ter concorrentes, ou seja, as mesma categorias presentes na base de dados de imoveis seazone, devem aparecer na base de dados dos imoveis concorrentes.
* Criação de um identificador único para cada categoria, mês e ano, chamado de "cluster". (os clusters são gerados a partir da junção de `categoria_mes_ano`)

  ### Cálculo da Banda de Faturamento:


* Cálculo dos percentis 10 (banda inferior) e 90 (banda superior), mediana e número de concorrentes para cada cluster. (Essa etapa pode ser alterada conforme a necessidade do problema. Esses valores foram decididos a partir da execução do algoritmos com diferentes valores, onde os valores atuais geraram menos falsos positivos).

### Identificação de Anomalias:

* Gearção dos DataFrrames `seazone_banda` e `banda` :
  * `banda`: define o que é considerado um faturamento "normal" para cada grupo de imóveis (cluster), com base no faturamento dos concorrentes.


  * `seazone_banda`: junta as informações do faturamento dos imóveis Seazone com essa banda, permitindo identificar os imóveis com faturamento anômalo.
* Mescla do DataFrame `seazone_banda` com o DataFrame `banda` para comparar o faturamento dos imóveis Seazone com a banda de valores. Cálculo da porcentagem de desvio do faturamento em relação à banda. 
* Identificação dos imóveis com faturamento fora da banda por 3 meses consecutivos e com desvio superior a 15%. 

### Análise Estatística das Anomalias:

* Extração da strata da categoria dos imóveis. Geração de gráficos para visualizar a distribuição das anomalias por categoria e strata. 

### Geração de Relatório:

Criação de um resumo com informações sobre os imóveis com anomalias, incluindo a categoria final (acima ou abaixo da banda), quantidade de meses fora da banda, período de meses consecutivos fora da banda, categoria, strata e valores da banda. Geração de um relatório com estatísticas gerais sobre as anomalias, como a porcentagem de imóveis com anomalias, número de imóveis com faturamento acima e abaixo da banda, e categorias mais frequentes entre os imóveis anômalos.

## Resultados

O código gera um arquivo CSV chamado "resumo_analise_categorica_10_90.csv" contendo o resumo das anomalias identificadas. Além disso, são gerados gráficos para visualização da distribuição das anomalias por categoria e strata.

## Conclusões

O código fornece uma análise detalhada do faturamento dos imóveis Seazone em comparação com seus concorrentes, permitindo a identificação de anomalias que podem indicar problemas de precificação ou outros fatores que afetam o desempenho dos imóveis. As informações geradas pelo código podem ser utilizadas para tomada de decisões estratégicas, como ajustes de preços, campanhas de marketing ou melhorias nos imóveis.

Espero que esta documentação seja útil para entender o funcionamento e os resultados do código. Em caso de dúvidas, fico à disposição para esclarecer.