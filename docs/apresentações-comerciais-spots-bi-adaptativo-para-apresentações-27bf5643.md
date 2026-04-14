<!-- title: Apresentações Comerciais( Spots ) - BI Adaptativo para Apresentações | url: https://outline.seazone.com.br/doc/apresentacoes-comerciais-spots-bi-adaptativo-para-apresentacoes-eoppqCnJLF | area: Tecnologia -->

# Apresentações Comerciais( Spots ) - BI Adaptativo para Apresentações

**Versão:** 1.0 

**Data:** 24 de Outubro de 2023 

**Autor:** Lucas Abel da SIlveira/ PM de Dados\n**Status:** Em Validação


## **1. Introdução & Contexto Estratégico**

Esta iniciativa visa resolver uma dor crítica e recorrente do time Comercial da Seazone: a falta de acesso rápido e confiável a dados de mercado para embazar suas apresentações e argumentos de venda. Atualmente, a equipe depende de análises manuais, planilhas descentralizadas e, muitas vezes, da intuição para responder a objeções de clientes e validar o potencial de investimento dos empreendimentos (Spots).

A capacidade de apresentar dados concretos sobre a valorização de uma região, o desempenho de imóveis similares e a quebra de objeções com números é um diferencial competitivo fundamental. Este projeto tem como objetivo construir uma base de dados e uma ferramenta de análise que capacitem o time Comercial a fechar vendas mais rápido, com maior confiança e eficiência.

## **2. Problema**

* **Dificuldade em Destravar Vendas:** Vendedores enfrentam objeções frequentes (ex: "Vale a pena pagar mais por um imóvel com garagem?") sem ter dados rápidos para respondê-las.
* **Processo Manual e Ineficiente:** A geração de apresentações é um processo manual, demorado e que consome tempo que poderia ser usado em atividades de venda.
* **Falta de Validação de Mercado:** É difícil provar de forma objetiva que um bairro ou uma cidade é um excelente investimento, ou que o modelo "Spot" da Seazone supera imóveis tradicionais.
* **Dados Descentralizados e de Baixa Qualidade:** As informações existentes estão espalhadas em diferentes fontes (planilhas, BI's, APIs externas) e muitas vezes não são confiáveis ou estão prontas para uso.
* **Oportunidade Perdida:** A ausência de um material rico em dados impacta negativamente a percepção de valor do cliente e a taxa de conversão das vendas.

## **3. Objetivos**

**Objetivo Principal:** Empoderar o time Comercial com dados estratégicos para aumentar a taxa de conversão de vendas e reduzir o ciclo de negociação.

**Objetivos Específicos:**

* Reduzir o tempo gasto para preparar uma apresentação comercial para um novo lançamento.
* Fornecer uma resposta baseada em dados para as 3 principais objeções de clientes (garagem, tamanho, piscina).
* Criar um ranking de valorização padronizado para todos os lançamentos ativos e futuros.
* Gerar pelo menos 3 insights de "marketing" (clickbait) por trimestre para o time de Marketing, baseados nos dados coletados.

## **4. Escopo Detalhado**

O projeto será dividido em 4 pilares de análise, entregues de forma incremental. O foco principal será em **imóveis Studios (0 ou 1 quarto)**.


**Pilar 1: Rankings de Mercado (Nacional e por Cidade)**

| **Funcionalidade/Métrica** | **Descrição Detalhada** | **Regra de Negócio / Critérios** | **Fonte de Dados** |
|----|----|----|----|
| **Top Faturamento de Studios** | Faturamento médio dos studios de melhor performance (percentil 90) de cada cidade. | Não é a média geral. Considerar apenas imóveis de 0 ou 1 quarto. | Tabelas **PRD-Lake** |
| **Aumento de Listings** | Variação percentual no número total de imóveis ativos na cidade. | Comparar período atual vs. período anterior (ex: último trimestre). | Tabelas **PRD-Lake** |
| **Aumento de Diária Média** | Variação percentual no preço médio da diária praticada na cidade. | Comparar período atual vs. período anterior. | Tabelas **PRD-Lake** |
| **Taxa de Ocupação** | Índice médio de ocupação dos imóveis na cidade. | Média de ocupação de todos os listings qualificados. | Tabelas **PRD-Lake** |
| **Composição por Tipologia** | Percentual de studios em relação ao total de imóveis da cidade. | (% Studios / Total Listings) \* 100. | Tabelas **PRD-Lake** |
| **% de "Pro Hosts"** | Percentual de anfitriões profissionais (10+ listings) na cidade. | Contar hosts com 10+ listings e dividir pelo total de hosts. | Tabelas **PRD-Lake** |
| **Ranking do Bairro** | Aplicar as métricas acima (faturamento, ocupação, etc.) para comparar bairros dentro de uma mesma cidade. | O bairro do Spot deve ser comparado contra os principais concorrentes. | Tabelas **PRD-Lake** |
| **\* Número de Eventos Locais** | Contagem de dias com picos de ocupação (>80%) no bairro. | Contar dias no ano em que a ocupação média do bairro superou 80%. | Tabelas **PRD-Lake** |


**Pilar 2: Quebras de Objeção (Análise de Spot)**

| **Funcionalidade/Métrica** | **Descrição Detalhada** | **Regra de Negócio / Critérios** | **Fonte de Dados** |
|----|----|----|----|
| **Garagem vs. Sem Garagem** | Comparação de faturamento médio, diária e ocupação. | Filtrar listings no mesmo bairro e comparar os grupos. | Tabelas **PRD-Lake** |
| **\*Planta Pequena vs. Grande** | Comparação de performance de imóveis de 1 quarto de diferentes tamanhos. | **Solução Proposta:** Gerar lista de links/faturamento para classificação manual pelo Comercial. | Tabelas **PRD-Lake** |
| **Piscina vs. Sem Piscina** | Comparação de performance de imóveis com e sem piscina. | Filtrar listings no mesmo bairro e comparar os grupos. | Tabelas **PRD-Lake** |


**Pilar 3: Análise de Valorização e ROI**

| **Funcionalidade/Métrica** | **Descrição Detalhada** | **Regra de Negócio / Critérios** | **Fonte de Dados** |
|----|----|----|----|
| **ROI (Spot vs. Apartamento Padrão)** | Cálculo do Retorno sobre o Investimento. | (Faturamento Anual / Valor do Imóvel) \* 100. | **Dependência:** Dados de valorização imobiliária. |
| **Mapa de Preços (Usados)** | Tabela com valores de imóveis usados na região. | Média de preço por m² ou por tipologia. | Dados externos (Viva Real, OLX) + **Time de Investimentos** |
| **Mapa de Preços (Lançamentos)** | Tabela com valores de imóveis novos na região. | Média de preço por m² ou por tipologia. | Dados externos (Incorporadoras) + **Time de Investimentos** |


---

**Pilar 4: Rankings Seazone (Dados Próprios)**

| **Funcionalidade/Métrica** | **Descrição Detalhada** | **Regra de Negócio / Critérios** | **Fonte de Dados** |
|----|----|----|----|
| **Cidades Mais Buscadas** | Ranking das cidades onde nossos imóveis recebem mais visualizações. | Contar visualizações de página dos listings da Seazone por cidade. | Tabelas **PRD-Lake** |


## **5. Locais Prioritários**


1. Caraguatuba-SP (Caraguá Spot)
2. Demais spot lançamentos com prioridade para fora de Florianópolis: <https://lancamentos.seazone.com.br/>

Florianópolis-SC (Campeche, Ponta das Canas, Jurerê), Foz do Iguaçu/PR, Barra Grande/BA, Itacaré/BA, Bonito/MS, , Goiânia-GO, Anitápolis-SC.

## **6.** Links auxiliares:


1. Apresentações Realizadas: 

   
   1. [Marista Spot](https://docs.google.com/presentation/d/1nQghHESUW-hJJ5eGd8Crw_bG-5dmQMDYgaezE-bXKrA/edit?disco=AAABr89hm9Q&slide=id.g3808f504e8b_1_501#slide=id.g3808f504e8b_1_501)
   2. [Jurere Spot II](https://docs.google.com/presentation/d/1_mfMm2bLxbw1drCh4f7CJY-STjF24RH-Mwn1EhMPA0I/edit?slide=id.g380b84b17b7_5_5#slide=id.g380b84b17b7_5_5)
2. Planilhas com Dados usados: 

   
   1. [Dados jurere](https://docs.google.com/spreadsheets/d/1pa4Hw-70L9r7Rcx0ODRIgsTtK46iDdIExM4MuU6LtXc/edit?hl=pt-br&pli=1&gid=1759559448#gid=1759559448)
   2. [Dados Marista](https://docs.google.com/spreadsheets/d/1ZHi7Jvx4l114_p_IpqARH31Ym7p4t8_zBt_EXWfhIvo/edit?gid=761896373#gid=761896373)
3. [Pagina de lançamento Spots](https://lancamentos.seazone.com.br/)