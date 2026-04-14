<!-- title: Definições de Regras de Negócio | url: https://outline.seazone.com.br/doc/definicoes-de-regras-de-negocio-TCXcoRfThx | area: Tecnologia -->

# Definições de Regras de Negócio

## **1. Introdução**

Este documento detalha as regras de negócio para o cálculo da Meta 2.0, definindo como o faturamento e as metas serão calculados para imóveis Seazone e concorrentes, bem como os critérios para considerar ou desconsiderar listings no processo de avaliação de metas.


## **2. Métodos de Cálculo de Faturamento**

**2.1. Imóveis Seazone:**

* **Meta Mensal:**
  * Cálculo: Faturamento real do imóvel acumulado no mês até a data de execução do cálculo.
  * Considerações:
    * Taxa de Limpeza: Não considerada no cálculo.
    * Taxa de OTA: Já pegamos o valor sem taxa de OTA(considerando a taxa da OTA do Airbnb).
    * Fonte de Dados: Dados provenientes do sistema Sapron.
* **Meta Trimestral:**
  * Cálculo: Faturamento real do imóvel acumulado no trimestre até a data de execução do cálculo.
  * Considerações:
    * Taxa de Limpeza: Não considerada no cálculo.
    * Taxa de OTA: Já pegamos o valor sem taxa de OTA(considerando a taxa da OTA do Airbnb).
    * Fonte de Dados: Dados provenientes do sistema Sapron.
* **Meta Trimestral Confirmada:**
  * Cálculo: Faturamento real do imóvel acumulado no trimestre, considerando apenas os dias **do início do trimestre até o dia anterior à data de execução do cálculo (d-1).**
  * Considerações:
    * Taxa de Limpeza: Não considerada no cálculo.
    * Taxa de OTA: Já pegamos o valor sem taxa de OTA (considerando a taxa da OTA do Airbnb).
    * Fonte de Dados: Dados provenientes do sistema Sapron.

      \

  2\.2 **Imóveis Concorrentes:**
* **Meta Mensal:**
  * Cálculo: Faturamento estimado com base no percentil definido para a categoria de imóveis.
  * Considerações:
    * Percentil: Percentil 50 (Mediana) como padrão inicial, com possibilidade de ajuste por categoria/imóvel pelo time RM.
    * Taxa de Limpeza: Não considerada no cálculo.
    * Taxa de OTA: Excluída do cálculo, multiplicando o valor vindo do Data Lake por 0,85 (extimando a taxa da OTA do Airbnb).
    * Fonte de Dados: Dados provenientes do Data Lake.
* **Meta Trimestral:**
  * Cálculo: Faturamento estimado com base no percentil definido para a categoria de imóveis, acumulado no trimestre até a data de execução do cálculo.
  * Considerações:
    * Percentil: Percentil 50 (Mediana) como padrão inicial, com possibilidade de ajuste por categoria/imóvel pelo time RM.
    * Taxa de Limpeza: Não considerada no cálculo.
    * Taxa de OTA: IExcluída do cálculo, multiplicando o valor vindo do Data Lake por 0,85 (considerando a taxa da OTA do Airbnb).
    * Fonte de Dados: Dados provenientes do Data Lake.
* **Meta Trimestral Confirmada:**
  * Cálculo: Faturamento estimado com base no percentil definido para a categoria de imóveis, considerando apenas os dias **do início do trimestre até o dia anterior à data de execução do cálculo (d-1).**
  * Considerações:
    * Percentil: Percentil 50 (Mediana) como padrão inicial, com possibilidade de ajuste por categoria/imóvel pelo time RM.
    * Taxa de Limpeza: Não considerada no cálculo.
    * Taxa de OTA: Excluída do cálculo, multiplicando o valor vindo do Data Lake por 0,85 (considerando a taxa da OTA do Airbnb).
    * Fonte de Dados: Dados provenientes do Data Lake.

## **3. Regras para Listings Seazone:**


* **Bloqueios Last Minute:** Bloqueios de reservas de última hora **não são considerados** no cálculo do número de bloqueios para fins de desconsiderar a meta.
* **Status de Atividade (n_days_status):** Imóveis devem ter n_days_status > 0, indicando que devem estar ativos desde o último dia do mês anterior para serem considerados no cálculo da meta.
* **Remoção de Regras Específicas para Bloqueios:** As regras específicas de desconsideração de meta baseadas no número de bloqueios (como a regra antiga de >= 8 bloqueios) **foram removidas**.
* **Percentil Próprio como Meta (Opcional):** Possibilidade de definir um percentil de meta específico para cada id_seazone dentro da mesma categoria, parametrizável pelo time RM.

  \

## **4. Regras para Concorrentes:**


* **Percentil Padrão:** Percentil 50 (Mediana) será utilizado como padrão para o cálculo da meta dos concorrentes, com a possibilidade de ajuste para cada id_seazone dentro da mesma categoria.
* **Faturamento Mensal Mínimo:** Apenas concorrentes com faturamento mensal **maior que 0** serão considerados na análise.
* **Preços Incorretos:** Concorrentes com preços identificados como "incorretos" **serão desconsiderados** no cálculo.
* **Número Mínimo de Concorrentes por Categoria:** Categorias com **menos de 10 concorrentes com faturamento positivo no mês** não terão a meta calculada.

## **5. Regras Gerais (Aplicáveis a Imóveis Seazone e Concorrentes):**


* **Fechamento Mensal:** Para o cálculo da meta mensal, considera-se o período do **início ao fim do mês em questão.** Os dados utilizados para este cálculo serão "congelados" (armazenados) no dia seguinte ao fechamento do mês (Fechamento do mês + 1 dia).
* **Fechamento Trimestral:** Para o cálculo da meta trimestral, considera-se o período do **início ao fim do trimestre em questão.** Os dados utilizados para este cálculo serão "congelados" (armazenados) no dia seguinte ao fechamento do trimestre (Fechamento do Trimestre + 1 dia).