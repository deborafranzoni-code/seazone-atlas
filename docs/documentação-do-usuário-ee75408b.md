<!-- title: Documentação do Usuário | url: https://outline.seazone.com.br/doc/documentacao-do-usuario-MqOsumkfep | area: Tecnologia -->

# Documentação do Usuário

# **1. Objetivo do Dashboard**

Bem-vindo ao Dashboard de Desempenho do **System Price**. Esta ferramenta foi criada para permitir uma análise granular e detalhada da performance do nosso motor de sugestão automática de preços.

O objetivo é fornecer insights claros sobre a acurácia das sugestões de preço, identificar desvios (vieses), entender onde ocorrem intervenções manuais (overrides) e, por fim, encontrar oportunidades para otimizar a nossa estratégia de precificação.

A data de atualização dos dados é exibida no canto superior direito do painel.

# **2. Componentes Principais do Dashboard**

O dashboard é dividido em quatro seções principais:


1. **Filtros de Análise:** Permite segmentar os dados para focar em cenários específicos.
2. **Indicadores de Performance (KPIs):** Exibe os principais resultados de performance do período filtrado.
3. **Análise de Desempenho:** Gráficos que mostram a evolução da performance ao longo do tempo e detalhamentos por cidade.
4. **Análise Cruzada (Deep Dive):** Uma matriz de calor para investigações profundas, cruzando diferentes dimensões.


-----

# **3. Como Utilizar o Dashboard**

## **3.1. Filtros de Análise**

Use esta seção para refinar sua análise. Qualquer filtro aplicado aqui afetará todos os gráficos e KPIs do dashboard.

* **Selecionar período:** Defina o intervalo de datas que você deseja analisar.
* **Cidade:** Filtre por uma ou mais cidades específicas.
* **Região:** Selecione as regiões do país (ex: Sudeste, Nordeste).
* **Feriado/Evento:** Analise o desempenho em dias normais, feriados ou eventos especiais.
* **Faixa de Antecedência:** Avalie a performance para reservas feitas com diferentes antecedências (ex: 0-15 dias, 61+ dias).
* **Categoria:** Filtre por tipo de imóvel (ex: apartamento, casa).
* **Tipo de Ocorrência:** Separe a análise entre "Dia de Semana" e "Final de Semana".
* **Strata:** Filtre por um segmento ou classificação específica do imóvel (JR, MASTER, SIM).
* **Tipo de Sazonalidade:** Analise por característica de sazonalidade do mercado (Região fria, Região quente).
* **Limpar Filtros:** Clique neste botão a qualquer momento para remover todas as seleções e retornar à visualização padrão.

## **3.2. Indicadores de Performance (KPIs) e Gráfico de Tendência**

Esta seção apresenta uma visão geral da performance e sua evolução no tempo.

**Principais Indicadores (KPIs):**

* **MAPE (vs. RM) - *Erro Percentual Absoluto Médio***: Indica o tamanho médio do erro das sugestões de preço, em percentual. **Quanto menor, melhor a performance.**
* **Viés da Sugestão (MPE) - *Erro Percentual Médio***: Mostra a direção do erro.
  * **Valor Negativo (-4,73% no exemplo):** O sistema tende a sugerir preços **abaixo** do praticado (subprecificação).
  * **Valor Positivo:** O sistema tende a sugerir preços **acima** do praticado (sobreprecificação).
  * O ideal é um valor próximo de zero.
* **Taxa de Override (>10%):** Percentual de vezes que um usuário alterou a sugestão do sistema em mais de 10%. Uma taxa alta pode indicar baixa confiança no modelo ou necessidade de ajustes.
* **Nº de Precificações:** O volume total de sugestões de preço geradas no período. Serve para dar contexto estatístico à análise.

**Gráfico de Evolução do Desempenho:**

Este gráfico mostra a tendência da métrica selecionada ao longo do tempo.

* **Como interagir:** Você pode alterar a métrica exibida no gráfico (MAPE, Taxa Override, MPE ou Contagem) clicando no ícone de gráfico e selecionando a opção desejada.
* **Como interpretar a tendência:**
  * **Tendência Ascendente:** Indica uma piora na performance (exceto para a Contagem).
  * **Tendência Descendente:** Indica uma melhora na performance (exceto para a Contagem).
  * **Volatilidade Alta:** Pode indicar inconsistência no modelo ou fortes mudanças sazonais.

## **3.3. Gráfico de Cidades**

Esta visualização detalha a performance por cidade, permitindo comparar e identificar as de melhor e pior desempenho.

* **Dica de Uso:** Por padrão, o gráfico exibe o MAPE. Para alterar a métrica (ex: visualizar o MPE por cidade), clique no ícone de opções do gráfico no canto superior direito.

## **3.4. Análise Cruzada - Deep Dive**

Use esta matriz de calor para fazer uma investigação detalhada e encontrar a causa raiz dos problemas ou sucessos.

* **Como usar:**

  
  1. Selecione as duas dimensões que deseja cruzar nos menus "Dimensão das Linhas" e "Dimensão das Colunas" (ex: Antecedência vs. Sazonalidade).
  2. Analise o mapa de calor para identificar "hotspots" (células com cores intensas).
* **Como interpretar o mapa de calor:**
  * **Para MAPE e Taxa de Override:** Cores mais intensas (vermelho) indicam **pior performance**.
  * **Para MPE (Viés):**
    * **Azul:** O System Price está muito **barato** (subprecificação).
    * **Laranja:** O System Price está muito **caro** (sobreprecificação).
  * **Para Contagem:** Cores mais intensas indicam **maior volume de dados**, o que traz maior confiabilidade estatística para aquele segmento.

> **Dica Estratégica:** Para gerar o máximo impacto, **foque sua atenção nos segmentos com alta contagem (cor intensa) e performance ruim (vermelho/laranja/azul intenso).** São nesses pontos que as melhorias trarão os maiores resultados.