<!-- title: Documentação do Usuário | url: https://outline.seazone.com.br/doc/documentacao-do-usuario-s1yIgUV4Eb | area: Tecnologia -->

# 📄 Documentação do Usuário

# 1. Introdução

Este documento tem como objetivo orientar o uso do **BI para Apresentações Comerciais**, desenvolvida para apoiar o time Comercial na análise de dados de mercado e na construção de apresentações mais embasadas e eficientes. O principal objetivo é ajudar o time Comercial com dados estratégicos para aumentar a taxa de conversão de vendas e reduzir o ciclo de negociação.

**Link do Looker:** <https://lookerstudio.google.com/reporting/e7a3dc08-adb9-420b-9eca-d94ab89870cd/page/p_6u189watxd>

# 2. Visão Geral do Dashboard

O dashboard é dividido em **três abas principais**, cada uma voltada a um tipo específico de análise:

* **Dossiê do SPOT:** apresenta métricas consolidadas das regiões, como faturamento médio mensal, faturamento anual bruto e líquido, taxa de ocupação, entre outros indicadores relevantes para avaliação de desempenho e potencial de investimento.
* **Rankings de Mercado:** exibe rankings por cidade e bairro para diferentes métricas de mercado, permitindo identificar regiões com maior ou menor potencial.
* **Evolução Temporal:** apresenta a evolução das principais métricas ao longo do tempo, com visualizações mensais ou anuais, possibilitando a análise de tendências e sazonalidades.


# 3. Utilização do Dashborad

## 3.1. Filtro de Dados Gerais

O dashboard permite segmentar os dados por meio de filtros, possibilitando análises mais precisas e alinhadas ao contexto de cada apresentação comercial. Os principais filtros disponíveis são:

* `**Estado**`**,** `**Cidade**` **e** `**Bairro**`**:** utilizados para selecionar a localização desejada e restringir a análise a uma região específica. Recomenda-se sempre validar se o **nível de detalhe (cidade ou bairro) está adequado ao tipo de comparação que se deseja realizar.**
* `**Tipo de Imóvel**`**:** permite selecionar o tipo de imóvel a ser analisado, como apartamento, casa, hotel e outros. 
* `**Número de Quartos**`**:** possibilita segmentar os dados de acordo com a quantidade de quartos do imóvel, facilitando comparações mais consistentes entre unidades com perfis equivalentes.

 ![](/api/attachments.redirect?id=e511e459-b099-44ee-80ce-5b8dc52bdcf0 " =1177x176")


## 3.2. Página do Dossiê do SPOT

A aba **Dossiê do SPOT** concentra as principais métricas de desempenho e possui uma funcionalidade específica relacionada ao uso de **percentis**, localizada na área de **KPIs Principais**. As métricas dessa seção podem ser visualizadas de acordo com três opções de percentil:

* **Sem percentil:** apresenta a média geral dos imóveis considerados na análise.
* **Percentil 75:** apresenta a média dos 25% melhores imóveis (top 25%) dentro do grupo selecionado.
* **Percentil 90:** apresenta a média dos 10% melhores imóveis (top 10%) dentro do grupo selecionado.

Essas opções permitem analisar diferentes cenários de performance, desde uma visão mais conservadora até uma visão mais otimista, sendo especialmente úteis para embasar argumentos comerciais conforme o perfil do cliente.

 ![](/api/attachments.redirect?id=e91c5c9c-82f1-479b-81c5-efc9b4cd9c8d " =1117x547")


Os faturamentos anuais são dados por:

* Faturamento médio anual bruto: É 12x o faturamento médio mensal.
* Faturamento médio anual líquido (OTA): faturamento médio anual bruto - (faturamento médio anual bruto \* 0.15)
* Faturamento médio anual líquido (OTA + Taxas): faturamento médio anual bruto - taxas. As taxas são apresentadas na tabela a seguir:

| **TAXA** | **VALOR MENSAL (PARA ANUAL: MULTIPLICAR POR 12)** |
|----|----|
| Taxa OTA | 15,0% |
| Taxa SZN | 20,0% |
| Condominio | R$ 250 |
| IPTU | R$ 50  |
| Energia | R$ 100  |
| Internet | R$ 99 |
| Agua | R$ 70 |
| Jardineiro | R$ 0  |
| Piscineiro | R$ 0 |
| Manutencao | R$ 50 |


Por padrão, as métricas exibidas nessa aba são calculadas com base no nível de **cidade**. Caso seja necessário visualizar os dados no nível de **bairro**, o usuário deve ativar essa opção em **Métricas Opcionais**, conforme ilustrado nas imagens abaixo.

 ![Aparece ao passar o mouse por cima do valor da métrica](/api/attachments.redirect?id=199a5f53-75cd-48f9-bdbc-8e854c988b35 "left-50 =300x172")  ![](/api/attachments.redirect?id=c1fc1451-266a-4165-b099-90c70851ccc1 "left-50 =288x175")


\

\

\
Além dos KPIs, a aba apresenta uma tabela de **faturamento por listing**, que lista os imóveis utilizados para compor as análises de quebra de objeção, como `**Garagem vs. Sem Garagem**` e `**Piscina vs. Sem Piscina**`**.**

 ![](/api/attachments.redirect?id=de830302-073b-4d1a-8c22-ba706f3617b9 " =1047x852")


Ao selecionar um ou mais imóveis nessa tabela, os gráficos de quebra de objeção são automaticamente filtrados, passando a exibir apenas os dados referentes aos listings selecionados. No exemplo apresentado, o gráfico mostra a média dos cinco primeiros imóveis selecionados, todos com piscina, permitindo uma comparação direta e visual entre os grupos analisados.

 ![](/api/attachments.redirect?id=7d5b72c4-0a05-4468-b2fa-1adffc9820d1 " =1015x795")


## 3.3. Página dos Rankings de Mercado

A página **Rankings de Mercado** apresenta uma visão comparativa do desempenho de cidades e bairros a partir de cinco métricas principais, todas calculadas com base nos últimos 12 meses:

* **Faturamento Médio dos Top 10% de Studios (R$):** representa o faturamento médio dos studios com melhor desempenho (percentil 90) em cada região analisada.
* **Taxa de Ocupação (%):** indica o nível médio de ocupação dos imóveis na localidade durante o período considerado.
* **Aumento de Listings (%):** mostra a variação percentual no número de imóveis anunciados, sinalizando expansão ou retração da oferta na região.
* **Aumento da Diária Média (%):** reflete a variação percentual da diária média dos imóveis ao longo do período analisado.
* **% de Pro Hosts (%):** indica a proporção de hosts profissionais (aqueles com mais de 10 listings) em relação ao total de hosts da região.

Ao selecionar qualquer uma dessas métricas, a tabela de ranking é automaticamente atualizada, permitindo analisar e comparar cidades ou bairros sob diferentes perspectivas de mercado. Além disso, a página conta com um **filtro por quantidade de listings**, que pode ser utilizado para excluir regiões com poucos imóveis anunciados. Esse filtro é especialmente útil para evitar distorções causadas por **outliers**, ou seja, localidades com uma base muito pequena de listings que podem inflar artificialmente as médias. Para utilizá-lo, basta definir um valor mínimo (controle à esquerda) e um valor máximo (controle à direita).

 ![](/api/attachments.redirect?id=c9b33b19-67f3-40b7-a26a-77715078493e " =1080x840")

Por fim, para auxiliar na interpretação dos dados, foi disponibilizado o botão **"Descrição das Métricas"**. Ao selecioná-lo, o usuário é direcionado para uma aba específica que detalha como cada métrica é calculada.


## 3.4. Página da Evolução Temporal

A página **Evolução Temporal** permite analisar o comportamento das principais métricas ao longo do tempo, possibilitando a identificação de tendências, variações sazonais e mudanças estruturais de mercado. Além dos filtros gerais do dashboard, esta página conta com filtros adicionais específicos:

* **Métricas:** permite selecionar qual indicador será analisado no gráfico.
* **Granularidade:** define o nível de análise entre **cidade** ou **bairro**.
* **Dimensão Temporal:** possibilita alternar entre visualizações por **mês** ou **ano**.
* **Período:** permite escolher o intervalo de análise, incluindo últimos 3, 6 ou 12 meses, além de períodos mais longos como últimos 2, 3 ou 5 anos.

Esses filtros possibilitam adaptar a análise conforme o objetivo da apresentação, seja para avaliar tendências recentes ou analisar o comportamento histórico do mercado.

 ![](/api/attachments.redirect?id=4ad0618d-996e-44b1-86e0-28185653c75c " =902x876")


Ao final da página, é exibida a **Soma do Faturamento Médio dos Top 10% de Studios**, calculada de acordo com a localidade selecionada (cidade ou bairro) e o período definido. 

 ![](/api/attachments.redirect?id=9f948e2b-8ab3-4094-a46d-783461cc7a8e " =624x234")