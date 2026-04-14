<!-- title: Fundamentos do MAPE | url: https://outline.seazone.com.br/doc/fundamentos-do-mape-ct1dlXBlFU | area: Tecnologia -->

# Fundamentos do MAPE

## O que é MAPE (Mean Absolute Percentage Error)

### 1. Definição do MAPE

**MAPE** (Mean Absolute Percentage Error) é uma métrica estatística utilizada para medir a precisão de previsões ou modelos de previsão. Ele calcula a média dos erros absolutos entre os valores reais e os valores previstos, expressos em termos percentuais.

**Importância do MAPE:**

* **Avaliação da Precisão:** Permite avaliar quão precisas são as previsões em relação aos valores reais.
* **Comparabilidade:** Facilita a comparação da precisão entre diferentes modelos ou entre diferentes conjuntos de dados.
* **Interpretação Intuitiva:** Por ser expressa em porcentagem, é de fácil compreensão para stakeholders não técnicos.

### 2. Fórmula Matemática do MAPE

A fórmula do MAPE é definida da seguinte maneira:

 ![](/api/attachments.redirect?id=4c9d6639-1bf2-45ff-aa9e-52f96924bee9 " =370x106")

**Componentes da Fórmula:**

* n: Número total de observações.
* Ai: Valor real da observação i.
* Fi​: Valor previsto para a observação i.

**Explicação:**


1. **Erro Absoluto Percentual:** Para cada observação i, calcula-se o erro absoluto entre o valor real e o valor previsto, dividido pelo valor real, multiplicado por 100 para obter a porcentagem.
2. **Média dos Erros:** Soma-se todos os erros absolutos percentuais e divide-se pelo número total de observações n, resultando na média dos erros.

Exemplo Prático: 

| listing | airbnb_listing_id | sum_actual_revenue | sum_estimated_revenue | \|error\| |
|----|----|----|----|----|
| JDE792 | 1186899132083029911 | 5038.59 | 9586 | 90.00% |
| CCM004 | 614654082546391518 | 6448.6 | 10868 | 69.00% |
| EPC204 | 554303241478819544 | 5746.92 | 7460 | 30.00% |
| MHF0607 | 1187061700423806804 | 5241.87 | 4159 | 21.00% |

* Na planilha acima temos exemplos reais de faturamento de nossos listings em uma janela de 15 dias(12-12-24 até 26-12-24). Usamos a granularidade de previsão neste caso de 15 dias, assim temos a soma do faturamento real de cada imóvel nestes 15 dias(sum_actual_revenue) e a soma do valor estimado no nosso modelo de predição(sum_estimated_revenue). 
* Na coluna |error| temos o valor do erro Absoluto de cada predição. 
* Neste caso nosso MAPE será a media destes erros absolutos, portanto (90+69+30+21)/4= 52,5%

  \
  ### 
* \

### 3.Pontos Fortes do MAPE

* **Facilidade de Interpretação:**
  * Por ser expresso em porcentagem, o MAPE é intuitivo e facilmente compreensível para diversos públicos, incluindo aqueles sem formação técnica.
* **Comparabilidade:**
  * Permite a comparação direta da precisão entre diferentes modelos de previsão ou entre diferentes conjuntos de dados, independentemente das unidades de medida.
* **Simplicidade:**
  * A fórmula do MAPE é simples e fácil de implementar, tornando-o uma métrica acessível para muitas aplicações.

### 4.Limitações e Desvantagens do MAPE

* **Sensibilidade a Valores Próximos de Zero:**
  * Quando os valores reais são próximos de zero, o denominador na fórmula do MAPE pode tornar a *métrica extremamente volátil ou indefinida, resultando em erros muito altos ou impossíveis de calcular*.
* **Impacto de Outliers:**
  * Valores extremos nos erros absolutos percentuais podem distorcer o MAPE, especialmente em conjuntos de dados com outliers significativos.
* **Assimetria na Interpretação:**
  * O MAPE penaliza erros de previsão de forma assimétrica, o que pode não refletir adequadamente a severidade dos erros em diferentes contextos.
* **Não Diferencia Entre Subestimações e Superestimações:**
  * O MAPE considera apenas o erro absoluto, não distinguindo entre previsões que subestimam ou superestimam os valores reais.
* **Dependência da Escala dos Dados:**
  * Embora o MAPE seja expresso em porcentagem, ele ainda pode ser influenciado pela escala dos dados, especialmente em séries temporais com tendências ou sazonalidades fortes.

## Cálculo Detalhado do nosso MAPE

Este tópico detalhará como a equipe calcula cada MAPE apresentado nos relatórios e no BI de observabilidade, explicando a metodologia específica e as razões para usar cada métrica.

### Visão Geral do Cálculo do MAPE

* **Descrição Geral:** Para medir o MAPE , utilizamos dados provenientes de fontes confiáveis, especificamente os anúncios da Seazone, já que são os únicos que dispomos com informações reais de ocupação, bloqueios, preço e faturamento. Para isso, realizamos a extração (scraping) dos nossos anúncios diretamente do site do Airbnb e aplicamos o mesmo processo utilizado para os nossos concorrentes, incluindo armazenamento, limpeza, enriquecimento e implementação de lógicas e modelos de detecção de bloqueios. Em seguida, comparamos os resultados previstos com os dados reais presentes em nossos bancos de dados. 
* **Objetivos Específicos:** Com o cálculo do MAPE aplicado a esses dados, conseguimos, a partir de uma amostra de aproximadamente 1.600 imóveis de diversas regiões do Brasil, controlar e estimar a margem de erro em nossas predições em relação aos concorrentes. Atualmente, trabalhamos com uma base de cerca de 200 mil imóveis extraídos de várias regiões do Brasil, para os quais coletamos informações de preço e disponibilidade.


* **MAPE Últimos 12 meses**
  * **MAPE Faturamento**
    * **Definição:** O MAPE (Mean Absolute Percentage Error) de Faturamento mede a porcentagem média de erro absoluto entre o faturamento previsto (calculado pelo pipeline, month_fat_pipe_after_discount) e o faturamento real (sum_reservation_daily_price).
    * Fórmula: 
      * `MAPE = |(Faturamento Real - Faturamento Previsto)| / Faturamento Real`  
    * **Código:**

      ```python
      monthly_fat_df['mape'] = abs(
          (monthly_fat_df['sum_reservation_daily_price'] - monthly_fat_df['month_fat_pipe_after_discount'])
          /monthly_fat_df['sum_reservation_daily_price'])
      ```
    * **Exceções e Filtros:**
      * **Tratamento de Divisão por Zero:** Para evitar erros de divisão por zero, quando o faturamento real é igual a 0 e o faturamento previsto também é 0, o MAPE é definido como 0:
        *   `monthly_fat_df.loc[(monthly_fat_df['sum_reservation_daily_price'] == 0) &`

          `                   (monthly_fat_df['month_fat_pipe_after_discount'] == 0),`

          `                    'mape'] = 0`
      * **Remoção de Dados Inconsistentes:** São removidos os registros onde o faturamento real é zero, mas o faturamento previsto é diferente de zero, pois indicam um problema nos dados:
        * código:
          *  `monthly_fat_df = monthly_fat_df[~((monthly_fat_df['sum_reservation_daily_price'] == 0) & (monthly_fat_df['month_fat_pipe_after_discount'] != 0))]`
        * **Agregação Mensal:** O MAPE é calculado para cada registro (imóvel/mês) e, em seguida, é feita uma média para obter o MAPE mensal:
          *  `monthly_fat_df = monthly_fat_df.groupby(['ano_mes'], as_index=False).agg(`

            `    mape=('mape', 'mean')`

            `)`
  * **MAPE Faturamento (quando acertamos todos os bloqueios)**
    * **Definição:** Este MAPE de Faturamento é calculado de forma semelhante ao anterior, mas considera apenas os casos em que os bloqueios foram corretamente previstos pelo pipeline. Ou seja, blocked_dates_pipe é igual a blocked_dates.
    * **Código:**

      ```python
      mape_blocked = monthly_fat_df.loc[monthly_fat_df['diff_blocked'] == 0]
       mape_blocked = mape_blocked.groupby(['ano_mes'], as_index=False).agg(mape_blocked=('mape', 'mean'))
      ```
      * diff_blocked = blocked_dates_pipe - blocked_dates
    * **Filtros:**
      * Filtra os registros onde a diferença entre os dias bloqueados previstos e os dias bloqueados reais é zero (ou seja, a previsão de bloqueios foi perfeita):

        ```python
        monthly_fat_df.loc[monthly_fat_df['diff_blocked'] == 0]
        ```

        \
    * **Objetivo:** Este cálculo isola o impacto dos erros de previsão de faturamento que não são causados por erros de previsão de bloqueios, permitindo avaliar a qualidade do modelo de previsão em si quando os bloqueios são conhecidos.

      \
  * **MAPE Taxa de Ocupação**
    * **Definição:** O MAPE da Taxa de Ocupação mede a porcentagem média de erro absoluto entre a taxa de ocupação prevista (occ_rate_staging) e a taxa de ocupação real (occ_rate_real).
    * **Fórmula:**

      ```javascript
      MAPE_Taxa_Ocupação = |(Taxa de Ocupação Real - Taxa de Ocupação Prevista)| / Taxa de Ocupação Real
      ```

      **content_copydownload**

      Use code **[with caution](https://support.google.com/legal/answer/13505487)**.
    * **Cálculo da Taxa de Ocupação:**
      * **Taxa de Ocupação Prevista (occ_rate_staging):**

        ```javascript
        monthly_fat_df['occ_rate_staging'] = monthly_fat_df['occupied_dates_pipe']\
            /(monthly_fat_df['days_in_month'] - monthly_fat_df['blocked_dates'])
        ```

        **content_copydownload**

        Use code **[with caution](https://support.google.com/legal/answer/13505487)**.Python
      * **Taxa de Ocupação Real (occ_rate_real):**

        ```javascript
        monthly_fat_df['occ_rate_real'] = monthly_fat_df['occupied_dates']\
            /(monthly_fat_df['days_in_month'] - monthly_fat_df['blocked_dates'])
        ```

        **content_copydownload**

        Use code **[with caution](https://support.google.com/legal/answer/13505487)**.Python
    * **Código:**

      ```javascript
      monthly_fat_df['mape_occ'] = abs(
          (monthly_fat_df['occ_rate_real'] - monthly_fat_df['occ_rate_staging'])
          /monthly_fat_df['occ_rate_real'])
      ```

      **content_copydownload**

      Use code **[with caution](https://support.google.com/legal/answer/13505487)**.Python
    * **Exceções e Filtros:**
      * **Tratamento de Divisão por Zero:** Quando a taxa de ocupação real e prevista são ambas 0, o MAPE é definido como 0:

        ```javascript
        monthly_fat_df.loc[(monthly_fat_df['occ_rate_real'] == 0) & (monthly_fat_df['occ_rate_staging'] == 0), 'mape_occ'] = 0
        ```

        **content_copydownload**

        Use code **[with caution](https://support.google.com/legal/answer/13505487)**.Python
      * **Remoção de Dados Inconsistentes:** São removidos os registros onde a taxa de ocupação real é 0, mas a taxa de ocupação prevista é diferente de zero:

        ```javascript
        monthly_fat_df.loc[~((monthly_fat_df['occ_rate_real'] == 0) & (monthly_fat_df['occ_rate_staging'] != 0))].groupby(
        ['ano_mes'], as_index=False).agg(mape_occ=('mape_occ', 'mean'))
        ```

        **content_copydownload**

        Use code **[with caution](https://support.google.com/legal/answer/13505487)**.Python
    * **Agregação Mensal:** O MAPE é calculado para cada registro (imóvel/mês) e, em seguida, é feita uma média para obter o MAPE mensal
  * Exemplo do report: 
    * É reportado no canal #lake-mape-report, diáriamente o cálculo dos ultimos 12 meses, no padrão a seguir.\n![](/api/attachments.redirect?id=bae44880-1a30-43bf-8a33-3d31c9368da1 " =472x313")
* **Análise de Maiores Erros por Imóvel:** 

  A análise de maiores erros por imóvel visa identificar de forma clara e objetiva, quais imóveis estão com erros de previsão significativos no mês atual, e qual o impacto deles no erro geral. Ao focar nos imóveis com maiores erros e maior `MAPE_impacto`, é possível otimizar o modelo de previsão para as propriedades mais problemáticas e melhorar o desempenho geral das previsões.

       **1. Critérios de Identificação**
  * **Foco no Mês Atual:** A análise de maiores erros por imóvel é realizada especificamente para o mês atual.
  * **Seleção de Imóveis com Maiores MAPEs:** Imóveis são identificados como tendo "maiores erros" com base no valor do MAPE de faturamento para aquele mês.
  * **Ranking:** Os imóveis são ordenados em ordem decrescente de MAPE, do maior erro para o menor.
  * **Top N:** O relatório exibe os N imóveis com os maiores erros, onde N é definido como 5 no código atual (`biggest_mapes.head(5)`), mas pode ser ajustado.

    **2. Cálculo do MAPE**
    * **Base de Cálculo:** O MAPE utilizado para identificar os maiores erros é o mesmo MAPE de faturamento que foi calculado anteriormente:

      ```python
      monthly_fat_df['mape'] = abs(
          (monthly_fat_df['sum_reservation_daily_price'] - monthly_fat_df['month_fat_pipe_after_discount'])
          /monthly_fat_df['sum_reservation_daily_price'])
      ```
    * **Detalhes:**
      * É a média percentual absoluta da diferença entre o faturamento real e o faturamento previsto.
      * Já inclui tratamento para evitar divisão por zero e remover dados inconsistentes conforme descrito na documentação anterior.
    * **Finalidade:** O MAPE nesse contexto serve como um indicador do quão distante a previsão de faturamento para um determinado imóvel está do faturamento real, no mês atual.

      **3. Cálculo do** `MAPE_impacto` (`mape_reduction`)
      * **Definição:** `MAPE_impacto` (nomeado `mape_reduction` no código) mede a redução no MAPE médio geral do mês se o imóvel específico fosse removido do cálculo.
      * **Código:**

        ```python
         biggest_mapes['mape_reduction'] = biggest_mapes.apply(lambda x: (this_month_monthly_fat['mape'].mean() -
                                                                         this_month_monthly_fat.drop(x.name)['mape'].mean()), axis=1)
        ```
      * **Passo a Passo:**

        
        1. `this_month_monthly_fat['mape'].mean()`: Calcula o MAPE médio de todos os imóveis no mês atual.
        2. `this_month_monthly_fat.drop(x.name)['mape'].mean()`: Para cada imóvel (linha `x` do DataFrame `biggest_mapes`), remove aquele imóvel do DataFrame `this_month_monthly_fat` e calcula o novo MAPE médio com os imóveis restantes.
        3. **Subtração:** A diferença entre o MAPE médio original (1) e o MAPE médio sem o imóvel (2) resulta em `mape_reduction`.

    \
    * **Objetivo:** O `MAPE_impacto` ajuda a identificar quais imóveis estão mais "fora da curva" em termos de erro de previsão, e que, portanto, merecem uma análise mais aprofundada.

    **4. Exibição no Relatório**
    * **Formato:** A saída do relatório é formatada para apresentar os imóveis com maiores erros em uma lista ordenada.
    * **Conteúdo:** Para cada um dos N imóveis (5 por padrão), o relatório exibe:
      * **Índice:** A posição do imóvel no ranking (1º, 2º, 3º, etc.)
      * `listing`: O identificador do imóvel.
      * `MAPE`: O valor do MAPE de faturamento do imóvel no mês atual, expresso em porcentagem.
      * `MAPE_impacto` (mape_reduction): A redução no MAPE médio geral do mês que seria alcançada se o imóvel fosse removido da análise, também expressa em porcentagem.

    **Exemplo de Saída**
  * ![](/api/attachments.redirect?id=b46a9462-5182-4538-a926-0198b88a88ad " =391x136")

    **Observações:**
    * Os valores de MAPE e MAPE_impacto são exibidos com duas casas decimais.
    * Os 5 maiores erros são selecionados utilizando `.head(5)` sobre a coluna `mape` que foi previamente ordenada por ordem decrescente.

    \
    \
* **Cálculo de MAPE para Scrapers de Preço e Disponibilidade**
  * Metodologia específica.
  * Componentes do cálculo.
* **Cálculo de MAPE para Períodos Recorrentes**
  * Últimos 12 Meses.
  * Últimos 6 Meses.
  * Últimos Dias (7, 15, 30, 60 dias).
* **Justificativa para a Escolha das Métricas**
  * Razões para utilizar diferentes tipos de MAPE.
  * Benefícios no monitoramento.
* **Ferramentas e Scripts Utilizados no Cálculo**
  * Softwares e bibliotecas empregadas.
  * Exemplos de scripts ou templates.
* **Exemplos de Cálculo Detalhado**
  * Exemplos reais ou fictícios.
  * Interpretação dos resultados.