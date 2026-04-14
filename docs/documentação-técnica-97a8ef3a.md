<!-- title: Documentação Técnica | url: https://outline.seazone.com.br/doc/documentacao-tecnica-3bHkTPDqPc | area: Tecnologia -->

# Documentação Técnica

## **Bibliotecas Utilizadas**


Ambos os scripts, get_high_prices_anomaly e get_low_prices_anomaly, utilizam um conjunto comum de bibliotecas para realizar suas funções, desde a manipulação de dados até a comunicação com serviços externos e tratamento de erros.


### **Bibliotecas Principais**


* **pandas**: Essencial para a manipulação e análise de dados. É utilizada para criar e operar DataFrames, que são a estrutura central de dados em todo o processo.
* **awswrangler**: Facilita a interação com serviços da AWS, principalmente para a execução de consultas no Athena e leitura de dados do S3, integrando o poder do pandas com o ecossistema da AWS.
* **boto3**: O SDK da AWS para Python, utilizado para criar e gerenciar a sessão com a AWS, permitindo que a aplicação interaja de forma segura com os serviços da nuvem.
* **requests**: Utilizada para enviar notificações de erro para um webhook, garantindo que qualquer falha na execução seja comunicada.
* **slack_sdk**: Empregada para enviar alertas e os resultados da análise (em formato CSV) para um canal específico no Slack, facilitando a comunicação e a ação da equipe.


### **Módulos e Funções Específicas**


* **os**: Utilizada para acessar variáveis de ambiente, como credenciais da AWS e tokens de serviços, de forma segura.
* **traceback**: Empregada para capturar e formatar as informações de exceções, permitindo um logging de erro detalhado.
* **functions_framework**: Framework do Google Cloud Functions que permite que as funções Python sejam acionadas por eventos HTTP.
* **datetime**: Especificamente timedelta e datetime, são utilizadas para manipulações de data e hora, cruciais para filtrar os períodos de análise de preços.
* **slack_sdk.errors.SlackApiError**: Usada para tratar erros específicos que podem ocorrer durante a comunicação com a API do Slack.


\
### **Conceito Geral e Ambiente de Execução**


Os scripts get_high_prices_anomaly e get_low_prices_anomaly são duas automações de monitoramento de preços projetadas para identificar e alertar sobre potenciais desalinhamentos na estratégia de precificação dos imóveis da Seazone em relação ao mercado. Cada script foca em um tipo específico de anomalia, baseado na antecedência da data.

Ambas as automações são implementadas como Cloud Functions no ambiente da **Google Cloud Platform (GCP)**, operando como recursos de dados que são acionados para processar informações e entregar insights. Elas se conectam a bancos de dados hospedados na AWS para coletar os dados necessários e, ao final, enviam os resultados para a equipe através do Slack.


1. **high_prices_earlier (get_high_prices_anomaly):**
   * **Objetivo:** Detectar imóveis da Seazone que estão com preços **muito altos** para **datas próximas** (nos próximos 14 dias).
   * **Justificativa:** Preços elevados em cima da hora, quando a ocupação do imóvel ainda está baixa, podem afastar potenciais clientes de última hora, resultando em diárias não vendidas. A função busca corrigir esses desvios para maximizar a ocupação de curto prazo.
2. **low_price_late (get_low_prices_anomaly):**
   * **Objetivo:** Detectar imóveis que estão com preços **muito baixos** para **datas distantes** (de 1 a 6 meses no futuro).
   * **Justificativa:** Preços baixos com muita antecedência, especialmente em períodos de alta temporada, representam uma perda de receita potencial. A função identifica essas oportunidades para ajustar os preços para cima, garantindo uma precificação mais estratégica e lucrativa a longo prazo.


---


### **Análise de Preços Altos em Datas Próximas (get_high_prices_anomaly)**


Esta função é responsável por identificar imóveis da Seazone cujos preços para os próximos 14 dias estão acima do praticado por concorrentes diretos, sinalizando um risco de perda de reservas de última hora.


#### **Lógica de Funcionamento Detalhada**


O processo é executado em etapas bem definidas, desde a coleta de dados até o envio do alerta.


1. **Conexão e Extração de Dados:**
   * A função inicia estabelecendo uma sessão com a AWS usando boto3.
   * Quatro consultas paralelas são executadas no Athena com awswrangler para buscar:

     
     1. O mapeamento entre os imóveis da Seazone e seus concorrentes diretos (competitors_plus).
     2. Os preços diários dos concorrentes para os próximos 14 dias que não estão bloqueados ou ocupados.
     3. Os preços diários, categoria, estrato e preço mínimo dos imóveis da Seazone para o mesmo período.
     4. A taxa de ocupação mensal histórica dos imóveis da Seazone.
2. **Pré-processamento e Enriquecimento:**
   * Os dados de preços da Seazone e dos concorrentes são limpos, com os tipos de dados ajustados para numérico e data.
   * A taxa de ocupação é vinculada aos dados diários da Seazone. É aplicado um filtro crucial: a análise prossegue apenas para imóveis cuja **ocupação no mês é inferior a 60%**. Isso foca a análise em imóveis que realmente precisam de atenção para garantir reservas.
3. **Análise de Sazonalidade:**
   * A função seasonality é chamada para classificar cada data do período de análise. Ela lê arquivos Parquet do S3 que contêm as regras de clima e temporada por localidade e atribui a cada dia um dos seguintes rótulos: Alta temporada, Média temporada ou Baixa temporada.
4. **Cálculo de Preços de Referência dos Concorrentes:**
   * A função repart_by_season calcula o preço de referência dos concorrentes de forma dinâmica, de acordo com a sazonalidade:
     * **Alta temporada:** O preço de referência é o **percentil 75 (P75)** dos concorrentes. Espera-se que a Seazone esteja entre os mais caros, mas não acima de todos.
     * **Média temporada:** O preço de referência é o **percentil 60 (P60)**.
     * **Baixa temporada:** O preço de referência é o **percentil 50 (P50)**, ou seja, a mediana dos preços dos concorrentes.
5. **Identificação das Anomalias:**
   * Com os dados enriquecidos, a função aplica um conjunto de filtros para encontrar as anomalias. Um preço é considerado uma anomalia se todas as seguintes condições forem verdadeiras:
     * O preço da Seazone é **maior** que o preço de referência do concorrente (calculado no passo anterior).
     * A data analisada **não está ocupada**.
     * O imóvel possui **5 ou mais concorrentes** mapeados para garantir uma comparação robusta.
     * O preço atual da Seazone **não é o preço mínimo** configurado, indicando que há margem para redução.
6. **Agrupamento e Formatação Final:**
   * As datas individuais com anomalias são agrupadas em períodos contínuos pela função agrupar_datas_continuas. Isso transforma uma sequência de alertas diários (ex: 10/07, 11/07, 12/07) em um único alerta de período (10/07/2025 - 12/07/2025), tornando a visualização mais limpa.
7. **Notificação via Slack:**
   * A função _send_slack_alert é acionada. Ela formata o DataFrame final, renomeando as colunas para maior clareza, gera um arquivo CSV e o envia para o canal #pricing-anomalies no Slack, junto com uma mensagem de alerta.


#### **Funções Auxiliares Principais**


* seasonality(df, listings, today): Enriquece os dados da Seazone com a classificação de temporada (Alta, Média, Baixa) para cada dia.
* repart_by_season(df_seazone, df_competitor): Separa os dados por temporada e calcula os preços de referência dos concorrentes usando diferentes percentis.
* agrupar_datas_continuas(df): Agrupa dias anômalos consecutivos em um único período para facilitar a leitura do relatório.
* _send_slack_alert(anomalies_df): Formata e envia o relatório final em formato CSV para o Slack.


#### **Saída**


O resultado final é uma mensagem no Slack com um arquivo **high_price_earlier.csv** anexado. O arquivo lista os imóveis, os períodos de datas anômalas, o preço da Seazone, a média do preço dos concorrentes e o motivo da anomalia (baseado na temporada).Conceito Geral e Ambiente de Execução Os scripts get_high_prices_anomaly e get_low_prices_anomaly são duas automações de monitoramento de preços projetadas para identificar e alertar sobre potenciais desalinhamentos na estratégia de precificação dos imóveis da Seazone em relação ao mercado. Cada script foca em um tipo específico de anomalia, baseado na antecedência da data. Ambas as automações são implementadas como Cloud Functions no ambiente da Google Cloud Platform (GCP), operando como recursos de dados que são acionados para processar informações e entregar insights. Elas se conectam a bancos de dados hospedados na AWS para coletar os dados necessários e, ao final, enviam os resultados para a equipe através do Slack. high_prices_earlier (get_high_prices_anomaly): Objetivo: Detectar imóveis da Seazone que estão com preços muito altos para datas próximas (nos próximos 14 dias). Justificativa: Preços elevados em cima da hora, quando a ocupação do imóvel ainda está baixa, podem afastar potenciais clientes de última hora, resultando em diárias não vendidas. A função busca corrigir esses desvios para maximizar a ocupação de curto prazo. low_price_late (get_low_prices_anomaly): Objetivo: Detectar imóveis que estão com preços muito baixos para datas distantes (de 1 a 6 meses no futuro). Justificativa: Preços baixos com muita antecedência, especialmente em períodos de alta temporada, representam uma perda de receita potencial. A função identifica essas oportunidades para ajustar os preços para cima, garantindo uma precificação mais estratégica e lucrativa a longo prazo. Análise de Preços Altos em Datas Próximas (get_high_prices_anomaly) Esta função é responsável por identificar imóveis da Seazone cujos preços para os próximos 14 dias estão acima do praticado por concorrentes diretos, sinalizando um risco de perda de reservas de última hora. Lógica de Funcionamento Detalhada O processo é executado em etapas bem definidas, desde a coleta de dados até o envio do alerta. Conexão e Extração de Dados: A função inicia estabelecendo uma sessão com a AWS usando boto3. Quatro consultas paralelas são executadas no Athena com awswrangler para buscar: O mapeamento entre os imóveis da Seazone e seus concorrentes diretos (competitors_plus). Os preços diários dos concorrentes para os próximos 14 dias que não estão bloqueados ou ocupados. Os preços diários, categoria, estrato e preço mínimo dos imóveis da Seazone para o mesmo período. A taxa de ocupação mensal histórica dos imóveis da Seazone. Pré-processamento e Enriquecimento: Os dados de preços da Seazone e dos concorrentes são limpos, com os tipos de dados ajustados para numérico e data. A taxa de ocupação é vinculada aos dados diários da Seazone. É aplicado um filtro crucial: a análise prossegue apenas para imóveis cuja ocupação no mês é inferior a 60%. Isso foca a análise em imóveis que realmente precisam de atenção para garantir reservas. Análise de Sazonalidade: A função seasonality é chamada para classificar cada data do período de análise. Ela lê arquivos Parquet do S3 que contêm as regras de clima e temporada por localidade e atribui a cada dia um dos seguintes rótulos: Alta temporada, Média temporada ou Baixa temporada. Cálculo de Preços de Referência dos Concorrentes: A função repart_by_season calcula o preço de referência dos concorrentes de forma dinâmica, de acordo com a sazonalidade: Alta temporada: O preço de referência é o percentil 75 (P75) dos concorrentes. Espera-se que a Seazone esteja entre os mais caros, mas não acima de todos. Média temporada: O preço de referência é o percentil 60 (P60). Baixa temporada: O preço de referência é o percentil 50 (P50), ou seja, a mediana dos preços dos concorrentes. Identificação das Anomalias: Com os dados enriquecidos, a função aplica um conjunto de filtros para encontrar as anomalias. Um preço é considerado uma anomalia se todas as seguintes condições forem verdadeiras: O preço da Seazone é maior que o preço de referência do concorrente (calculado no passo anterior). A data analisada não está ocupada. O imóvel possui 5 ou mais concorrentes mapeados para garantir uma comparação robusta. O preço atual da Seazone não é o preço mínimo configurado, indicando que há margem para redução. Agrupamento e Formatação Final: As datas individuais com anomalias são agrupadas em períodos contínuos pela função agrupar_datas_continuas. Isso transforma uma sequência de alertas diários (ex: 10/07, 11/07, 12/07) em um único alerta de período (10/07/2025 - 12/07/2025), tornando a visualização mais limpa. Notificação via Slack: A função _send_slack_alert é acionada. Ela formata o DataFrame final, renomeando as colunas para maior clareza, gera um arquivo CSV e o envia para o canal #pricing-anomalies no Slack, junto com uma mensagem de alerta. Funções Auxiliares Principais seasonality(df, listings, today): Enriquece os dados da Seazone com a classificação de temporada (Alta, Média, Baixa) para cada dia. repart_by_season(df_seazone, df_competitor): Separa os dados por temporada e calcula os preços de referência dos concorrentes usando diferentes percentis. agrupar_datas_continuas(df): Agrupa dias anômalos consecutivos em um único período para facilitar a leitura do relatório. _send_slack_alert(anomalies_df): Formata e envia o relatório final em formato CSV para o Slack. Saída O resultado final é uma mensagem no Slack com um arquivo high_price_earlier.csv anexado. O arquivo lista os imóveis, os períodos de datas anômalas, o preço da Seazone, a média do preço dos concorrentes e o motivo da anomalia (baseado na temporada).Conceito Geral e Ambiente de Execução Os scripts get_high_prices_anomaly e get_low_prices_anomaly são duas automações de monitoramento de preços projetadas para identificar e alertar sobre potenciais desalinhamentos na estratégia de precificação dos imóveis da Seazone em relação ao mercado. Cada script foca em um tipo específico de anomalia, baseado na antecedência da data. Ambas as automações são implementadas como Cloud Functions no ambiente da Google Cloud Platform (GCP), operando como recursos de dados que são acionados para processar informações e entregar insights. Elas se conectam a bancos de dados hospedados na AWS para coletar os dados necessários e, ao final, enviam os resultados para a equipe através do Slack. high_prices_earlier (get_high_prices_anomaly): Objetivo: Detectar imóveis da Seazone que estão com preços muito altos para datas próximas (nos próximos 14 dias). Justificativa: Preços elevados em cima da hora, quando a ocupação do imóvel ainda está baixa, podem afastar potenciais clientes de última hora, resultando em diárias não vendidas. A função busca corrigir esses desvios para maximizar a ocupação de curto prazo. low_price_late (get_low_prices_anomaly): Objetivo: Detectar imóveis que estão com preços muito baixos para datas distantes (de 1 a 6 meses no futuro). Justificativa: Preços baixos com muita antecedência, especialmente em períodos de alta temporada, representam uma perda de receita potencial. A função identifica essas oportunidades para ajustar os preços para cima, garantindo uma precificação mais estratégica e lucrativa a longo prazo. Análise de Preços Altos em Datas Próximas (get_high_prices_anomaly) Esta função é responsável por identificar imóveis da Seazone cujos preços para os próximos 14 dias estão acima do praticado por concorrentes diretos, sinalizando um risco de perda de reservas de última hora. Lógica de Funcionamento Detalhada O processo é executado em etapas bem definidas, desde a coleta de dados até o envio do alerta. Conexão e Extração de Dados: A função inicia estabelecendo uma sessão com a AWS usando boto3. Quatro consultas paralelas são executadas no Athena com awswrangler para buscar: O mapeamento entre os imóveis da Seazone e seus concorrentes diretos (competitors_plus). Os preços diários dos concorrentes para os próximos 14 dias que não estão bloqueados ou ocupados. Os preços diários, categoria, estrato e preço mínimo dos imóveis da Seazone para o mesmo período. A taxa de ocupação mensal histórica dos imóveis da Seazone. Pré-processamento e Enriquecimento: Os dados de preços da Seazone e dos concorrentes são limpos, com os tipos de dados ajustados para numérico e data. A taxa de ocupação é vinculada aos dados diários da Seazone. É aplicado um filtro crucial: a análise prossegue apenas para imóveis cuja ocupação no mês é inferior a 60%. Isso foca a análise em imóveis que realmente precisam de atenção para garantir reservas. Análise de Sazonalidade: A função seasonality é chamada para classificar cada data do período de análise. Ela lê arquivos Parquet do S3 que contêm as regras de clima e temporada por localidade e atribui a cada dia um dos seguintes rótulos: Alta temporada, Média temporada ou Baixa temporada. Cálculo de Preços de Referência dos Concorrentes: A função repart_by_season calcula o preço de referência dos concorrentes de forma dinâmica, de acordo com a sazonalidade: Alta temporada: O preço de referência é o percentil 75 (P75) dos concorrentes. Espera-se que a Seazone esteja entre os mais caros, mas não acima de todos. Média temporada: O preço de referência é o percentil 60 (P60). Baixa temporada: O preço de referência é o percentil 50 (P50), ou seja, a mediana dos preços dos concorrentes. Identificação das Anomalias: Com os dados enriquecidos, a função aplica um conjunto de filtros para encontrar as anomalias. Um preço é considerado uma anomalia se todas as seguintes condições forem verdadeiras: O preço da Seazone é maior que o preço de referência do concorrente (calculado no passo anterior). A data analisada não está ocupada. O imóvel possui 5 ou mais concorrentes mapeados para garantir uma comparação robusta. O preço atual da Seazone não é o preço mínimo configurado, indicando que há margem para redução. Agrupamento e Formatação Final: As datas individuais com anomalias são agrupadas em períodos contínuos pela função agrupar_datas_continuas. Isso transforma uma sequência de alertas diários (ex: 10/07, 11/07, 12/07) em um único alerta de período (10/07/2025 - 12/07/2025), tornando a visualização mais limpa. Notificação via Slack: A função _send_slack_alert é acionada. Ela formata o DataFrame final, renomeando as colunas para maior clareza, gera um arquivo CSV e o envia para o canal #pricing-anomalies no Slack, junto com uma mensagem de alerta. Funções Auxiliares Principais seasonality(df, listings, today): Enriquece os dados da Seazone com a classificação de temporada (Alta, Média, Baixa) para cada dia. repart_by_season(df_seazone, df_competitor): Separa os dados por temporada e calcula os preços de referência dos concorrentes usando diferentes percentis. agrupar_datas_continuas(df): Agrupa dias anômalos consecutivos em um único período para facilitar a leitura do relatório. _send_slack_alert(anomalies_df): Formata e envia o relatório final em formato CSV para o Slack. Saída O resultado final é uma mensagem no Slack com um arquivo high_price_earlier.csv anexado. O arquivo lista os imóveis, os períodos de datas anômalas, o preço da Seazone, a média do preço dos concorrentes e o motivo da anomalia (baseado na temporada).Conceito Geral e Ambiente de Execução Os scripts get_high_prices_anomaly e get_low_prices_anomaly são duas automações de monitoramento de preços projetadas para identificar e alertar sobre potenciais desalinhamentos na estratégia de precificação dos imóveis da Seazone em relação ao mercado. Cada script foca em um tipo específico de anomalia, baseado na antecedência da data. Ambas as automações são implementadas como Cloud Functions no ambiente da Google Cloud Platform (GCP), operando como recursos de dados que são acionados para processar informações e entregar insights. Elas se conectam a bancos de dados hospedados na AWS para coletar os dados necessários e, ao final, enviam os resultados para a equipe através do Slack. high_prices_earlier (get_high_prices_anomaly): Objetivo: Detectar imóveis da Seazone que estão com preços muito altos para datas próximas (nos próximos 14 dias). Justificativa: Preços elevados em cima da hora, quando a ocupação do imóvel ainda está baixa, podem afastar potenciais clientes de última hora, resultando em diárias não vendidas. A função busca corrigir esses desvios para maximizar a ocupação de curto prazo. low_price_late (get_low_prices_anomaly): Objetivo: Detectar imóveis que estão com preços muito baixos para datas distantes (de 1 a 6 meses no futuro). Justificativa: Preços baixos com muita antecedência, especialmente em períodos de alta temporada, representam uma perda de receita potencial. A função identifica essas oportunidades para ajustar os preços para cima, garantindo uma precificação mais estratégica e lucrativa a longo prazo. Análise de Preços Altos em Datas Próximas (get_high_prices_anomaly) Esta função é responsável por identificar imóveis da Seazone cujos preços para os próximos 14 dias estão acima do praticado por concorrentes diretos, sinalizando um risco de perda de reservas de última hora. Lógica de Funcionamento Detalhada O processo é executado em etapas bem definidas, desde a coleta de dados até o envio do alerta. Conexão e Extração de Dados: A função inicia estabelecendo uma sessão com a AWS usando boto3. Quatro consultas paralelas são executadas no Athena com awswrangler para buscar: O mapeamento entre os imóveis da Seazone e seus concorrentes diretos (competitors_plus). Os preços diários dos concorrentes para os próximos 14 dias que não estão bloqueados ou ocupados. Os preços diários, categoria, estrato e preço mínimo dos imóveis da Seazone para o mesmo período. A taxa de ocupação mensal histórica dos imóveis da Seazone. Pré-processamento e Enriquecimento: Os dados de preços da Seazone e dos concorrentes são limpos, com os tipos de dados ajustados para numérico e data. A taxa de ocupação é vinculada aos dados diários da Seazone. É aplicado um filtro crucial: a análise prossegue apenas para imóveis cuja ocupação no mês é inferior a 60%. Isso foca a análise em imóveis que realmente precisam de atenção para garantir reservas. Análise de Sazonalidade: A função seasonality é chamada para classificar cada data do período de análise. Ela lê arquivos Parquet do S3 que contêm as regras de clima e temporada por localidade e atribui a cada dia um dos seguintes rótulos: Alta temporada, Média temporada ou Baixa temporada. Cálculo de Preços de Referência dos Concorrentes: A função repart_by_season calcula o preço de referência dos concorrentes de forma dinâmica, de acordo com a sazonalidade: Alta temporada: O preço de referência é o percentil 75 (P75) dos concorrentes. Espera-se que a Seazone esteja entre os mais caros, mas não acima de todos. Média temporada: O preço de referência é o percentil 60 (P60). Baixa temporada: O preço de referência é o percentil 50 (P50), ou seja, a mediana dos preços dos concorrentes. Identificação das Anomalias: Com os dados enriquecidos, a função aplica um conjunto de filtros para encontrar as anomalias. Um preço é considerado uma anomalia se todas as seguintes condições forem verdadeiras: O preço da Seazone é maior que o preço de referência do concorrente (calculado no passo anterior). A data analisada não está ocupada. O imóvel possui 5 ou mais concorrentes mapeados para garantir uma comparação robusta. O preço atual da Seazone não é o preço mínimo configurado, indicando que há margem para redução. Agrupamento e Formatação Final: As datas individuais com anomalias são agrupadas em períodos contínuos pela função agrupar_datas_continuas. Isso transforma uma sequência de alertas diários (ex: 10/07, 11/07, 12/07) em um único alerta de período (10/07/2025 - 12/07/2025), tornando a visualização mais limpa. Notificação via Slack: A função _send_slack_alert é acionada. Ela formata o DataFrame final, renomeando as colunas para maior clareza, gera um arquivo CSV e o envia para o canal #pricing-anomalies no Slack, junto com uma mensagem de alerta. Funções Auxiliares Principais seasonality(df, listings, today): Enriquece os dados da Seazone com a classificação de temporada (Alta, Média, Baixa) para cada dia. repart_by_season(df_seazone, df_competitor): Separa os dados por temporada e calcula os preços de referência dos concorrentes usando diferentes percentis. agrupar_datas_continuas(df): Agrupa dias anômalos consecutivos em um único período para facilitar a leitura do relatório. _send_slack_alert(anomalies_df): Formata e envia o relatório final em formato CSV para o Slack. Saída O resultado final é uma mensagem no Slack com um arquivo high_price_earlier.csv anexado. O arquivo lista os imóveis, os períodos de datas anômalas, o preço da Seazone, a média do preço dos concorrentes e o motivo da anomalia (baseado na temporada).

## Conceito Geral e Ambiente de Execução

Os scripts get_high_prices_anomaly e get_low_prices_anomaly são duas automações de monitoramento de preços projetadas para identificar e alertar sobre potenciais desalinhamentos na estratégia de precificação dos imóveis da Seazone em relação ao mercado. Cada script foca em um tipo específico de anomalia, baseado na antecedência da data.

Ambas as automações são implementadas como Cloud Functions no ambiente da **Google Cloud Platform (GCP)**, operando como recursos de dados que são acionados para processar informações e entregar insights. Elas se conectam a bancos de dados hospedados na AWS para coletar os dados necessários e, ao final, enviam os resultados para a equipe através do Slack.


1. **high_prices_earlier (get_high_prices_anomaly):**
   * **Objetivo:** Detectar imóveis da Seazone que estão com preços **muito altos** para **datas próximas** (nos próximos 14 dias).
   * **Justificativa:** Preços elevados em cima da hora, quando a ocupação do imóvel ainda está baixa, podem afastar potenciais clientes de última hora, resultando em diárias não vendidas. A função busca corrigir esses desvios para maximizar a ocupação de curto prazo.
2. **low_price_late (get_low_prices_anomaly):**
   * **Objetivo:** Detectar imóveis que estão com preços **muito baixos** para **datas distantes** (de 1 a 6 meses no futuro).
   * **Justificativa:** Preços baixos com muita antecedência, especialmente em períodos de alta temporada, representam uma perda de receita potencial. A função identifica essas oportunidades para ajustar os preços para cima, garantindo uma precificação mais estratégica e lucrativa a longo prazo.


---


## **Análise de Preços Altos em Datas Próximas (get_high_prices_anomaly)**

Esta função é responsável por identificar imóveis da Seazone cujos preços para os próximos 14 dias estão acima do praticado por concorrentes diretos, sinalizando um risco de perda de reservas de última hora.


### **Lógica de Funcionamento Detalhada**

O processo é executado em etapas bem definidas, desde a coleta de dados até o envio do alerta.


1. **Conexão e Extração de Dados:**
   * A função inicia estabelecendo uma sessão com a AWS usando boto3.
   * Quatro consultas paralelas são executadas no Athena com awswrangler para buscar:

     
     1. O mapeamento entre os imóveis da Seazone e seus concorrentes diretos (competitors_plus).
     2. Os preços diários dos concorrentes para os próximos 14 dias que não estão bloqueados ou ocupados.
     3. Os preços diários, categoria, estrato e preço mínimo dos imóveis da Seazone para o mesmo período.
     4. A taxa de ocupação mensal histórica dos imóveis da Seazone.
2. **Pré-processamento e Enriquecimento:**
   * Os dados de preços da Seazone e dos concorrentes são limpos, com os tipos de dados ajustados para numérico e data.
   * A taxa de ocupação é vinculada aos dados diários da Seazone. É aplicado um filtro crucial: a análise prossegue apenas para imóveis cuja **ocupação no mês é inferior a 60%**. Isso foca a análise em imóveis que realmente precisam de atenção para garantir reservas.
3. **Análise de Sazonalidade:**
   * A função seasonality é chamada para classificar cada data do período de análise. Ela lê arquivos Parquet do S3 que contêm as regras de clima e temporada por localidade e atribui a cada dia um dos seguintes rótulos: Alta temporada, Média temporada ou Baixa temporada.
4. **Cálculo de Preços de Referência dos Concorrentes:**
   * A função repart_by_season calcula o preço de referência dos concorrentes de forma dinâmica, de acordo com a sazonalidade:
     * **Alta temporada:** O preço de referência é o **percentil 75 (P75)** dos concorrentes. Espera-se que a Seazone esteja entre os mais caros, mas não acima de todos.
     * **Média temporada:** O preço de referência é o **percentil 60 (P60)**.
     * **Baixa temporada:** O preço de referência é o **percentil 50 (P50)**, ou seja, a mediana dos preços dos concorrentes.
5. **Identificação das Anomalias:**
   * Com os dados enriquecidos, a função aplica um conjunto de filtros para encontrar as anomalias. Um preço é considerado uma anomalia se todas as seguintes condições forem verdadeiras:
     * O preço da Seazone é **maior** que o preço de referência do concorrente (calculado no passo anterior).
     * A data analisada **não está ocupada**.
     * O imóvel possui **5 ou mais concorrentes** mapeados para garantir uma comparação robusta.
     * O preço atual da Seazone **não é o preço mínimo** configurado, indicando que há margem para redução.
6. **Agrupamento e Formatação Final:**
   * As datas individuais com anomalias são agrupadas em períodos contínuos pela função agrupar_datas_continuas. Isso transforma uma sequência de alertas diários (ex: 10/07, 11/07, 12/07) em um único alerta de período (10/07/2025 - 12/07/2025), tornando a visualização mais limpa.


### **Funções Auxiliares Principais**

* seasonality(df, listings, today): Enriquece os dados da Seazone com a classificação de temporada (Alta, Média, Baixa) para cada dia.
* repart_by_season(df_seazone, df_competitor): Separa os dados por temporada e calcula os preços de referência dos concorrentes usando diferentes percentis.
* agrupar_datas_continuas(df): Agrupa dias anômalos consecutivos em um único período para facilitar a leitura do relatório.
* _send_slack_alert(anomalies_df): Formata e envia o relatório final em formato CSV para o Slack.


**Saída**

O resultado final é armazenado no cloud storage para posteriormente ser usado na planilha de preços anomalos e no api-send-anomalies.

## Análise de Preços Baixos em Datas Distantes (get_low_prices_anomaly)

Esta função é a contraparte da anterior e seu objetivo é proteger a receita futura da Seazone. Ela identifica imóveis cujos preços para datas distantes (de 30 a 200 dias no futuro) estão muito abaixo do mercado, especialmente em períodos de alta demanda, sinalizando uma oportunidade de otimização de receita.


### **Lógica de Funcionamento Detalhada**

O fluxo de execução é semelhante ao do get_high_prices_anomaly, mas com diferenças cruciais nos filtros de data, na lógica de comparação e no foco da análise.


1. **Conexão e Extração de Dados:**
   * A função inicia uma sessão com a AWS e executa quatro consultas paralelas no Athena.
   * A principal diferença está no filtro de data das consultas: elas são configuradas para buscar dados de preços da Seazone e dos concorrentes em um intervalo futuro, começando em **30 dias a partir da data atual e se estendendo por até 200 dias** (current_date + INTERVAL '30' DAY e current_date + INTERVAL '200' DAY).
2. **Pré-processamento e Enriquecimento:**
   * Os passos de limpeza, conversão de tipos de dados e união com os dados de ocupação são idênticos aos do script anterior.
   * O filtro de **ocupação mensal inferior a 60%** também é aplicado, mantendo o foco em imóveis que historicamente possuem maior disponibilidade.
3. **Análise de Sazonalidade:**
   * A função seasonality é chamada para classificar cada data do período de análise como Alta temporada, Média temporada ou Baixa temporada. O mecanismo é o mesmo, garantindo que a lógica de negócio seja consistente.
4. **Cálculo de Preços de Referência dos Concorrentes:**
   * Aqui reside uma diferença fundamental na lógica. A função repart_by_season neste script foi ajustada para focar **exclusivamente na Alta temporada**.
   * O preço de referência dos concorrentes é definido como o **percentil 5 (P05)**. Isso significa que a análise busca comparar o preço da Seazone com os preços mais baixos praticados pelos concorrentes. O objetivo é garantir que a Seazone não esteja precificando abaixo até mesmo das opções mais baratas do mercado em datas de alta procura.
5. **Identificação das Anomalias:**
   * A função aplica um conjunto de filtros para encontrar os imóveis subprecificados. Um preço é considerado uma anomalia se todas as condições a seguir forem atendidas:
     * A data analisada está classificada como **Alta temporada**.
     * O preço da Seazone é significativamente **menor** que o preço de referência do concorrente. A regra específica é: seazone_price < (competitor_price \* 0.8), ou seja, o preço está pelo menos 20% abaixo do percentil 5 dos concorrentes.
     * A data analisada **não está ocupada**.
     * O imóvel possui **5 ou mais concorrentes** para uma comparação válida.
     * O preço atual da Seazone **não é o preço mínimo** configurado.
6. **Agrupamento e Formatação Final:**
   * A função agrupar_datas_continuas é utilizada da mesma forma para consolidar dias anômalos consecutivos em intervalos de datas, simplificando o relatório final.


### **Funções Auxiliares Principais**

* seasonality(df, listings, today): Enriquece os dados da Seazone com a classificação de temporada para cada dia.
* repart_by_season(df_seazone, df_competitor): Filtra os dados para focar apenas na **Alta Temporada** e calcula o preço de referência dos concorrentes usando o **percentil 5 (P05)**.
* agrupar_datas_continuas(df): Agrupa dias anômalos consecutivos em um único período para facilitar a leitura do relatório.
* _send_slack_alert(anomalies_df): Formata e envia o relatório final em formato CSV para o Slack.


### **Saída**

O resultado final é armazenado no cloud storage para posteriormente ser usado na planilha de preços anomalos e no api-send-anomalies.

## api-send-anomalies

### **Resumo** 


Esta é uma Google Cloud Function acionada por HTTP, projetada para gerenciar e notificar sobre anomalias de preços. A função recebe uma lista de anomalias que já foram tratadas, consulta os dados restantes de anomalias ativas no BigQuery, envia um alerta para um canal do Slack com os dados em anexo (CSV) e, por fim, atualiza os arquivos de estado no Google Cloud Storage (GCS) para refletir a lista de anomalias ativas.


### **Visão Geral do Fluxo de Trabalho** 



1. **Gatilho (Trigger)**: A função é iniciada por uma requisição HTTP POST.
2. **Entrada (Input)**: Ela espera um payload JSON contendo duas listas: `high_prices` e `low_prices`. Essas listas contêm as anomalias que foram resolvidas ou tratadas e devem ser removidas da lista de anomalias ativas.
3. **Processamento**:
   * A função carrega a lista completa de anomalias de preços altos e baixos de duas tabelas no BigQuery.
   * Ela filtra essas listas, removendo as anomalias cujos `id`s foram recebidos no payload da requisição. O resultado são dois DataFrames contendo apenas as anomalias que ainda estão ativas.
   * As listas de anomalias ativas são enviadas para um canal específico no Slack.
4. **Saída (Output)**:
   * **Notificação no Slack**: Duas mensagens são postadas no Slack, uma para preços altos e outra para preços baixos. Cada mensagem contém um resumo e um link para baixar um arquivo CSV com os detalhes completos.
   * **Armazenamento no GCS**: Os DataFrames de anomalias ativas são salvos em formato Parquet no Google Cloud Storage em dois locais:
     * Um local de **estado atual** (`state=current`), que contém um único arquivo sempre atualizado.
     * Um local de **histórico** (`state=historic`), que armazena os dados particionados pela data de execução, criando um log diário.
5. **Tratamento de Erros**: Se qualquer erro ocorrer durante a execução, uma mensagem detalhada com o traceback do erro é enviada para um webhook do Slack, notificando os desenvolvedores imediatamente.

### **Componentes Principais** 


#### **Configuração e Variáveis de Ambiente**


O script utiliza variáveis de ambiente e constantes para configurar seu comportamento:

* `WEBHOOK_URL`: (Variável de Ambiente) A URL do webhook do Slack para o envio de notificações de erro.
* `PROJECT_ID`: O ID do projeto no Google Cloud Platform.
* `SLACK_BOT_TOKEN`: (Variável de Ambiente) O token de autenticação do bot do Slack, necessário para enviar mensagens e arquivos.
* `SLACK_CHANNEL`: O ID do canal do Slack para onde as notificações de anomalias são enviadas.
* `HIGH_CURRENT_PREFIX`, `HIGH_HISTORIC_PREFIX`, `LOW_CURRENT_PREFIX`, `LOW_HISTORIC_PREFIX`: Caminhos no GCS para armazenar os arquivos Parquet com os dados de anomalias.


#### **Função** `**main(request)**`


É o ponto de entrada da Cloud Function. Ela orquestra todo o fluxo:


1. Recebe e interpreta o payload JSON da requisição HTTP.
2. Conecta-se ao BigQuery e executa duas queries para obter a lista completa de anomalias.
3. Filtra os DataFrames, removendo os `id`s recebidos no payload. A lógica `~job_high['id'].isin(high_prices['id'])` é usada para **manter** apenas as anomalias que **não estão** na lista de itens resolvidos.
4. Chama a função `_send_slack_alert` para notificar o Slack.
5. Salva os DataFrames filtrados no GCS, tanto no diretório de estado atual quanto no histórico. A data atual (`today`) é adicionada como uma coluna para permitir o particionamento no diretório histórico.


#### **Função** `**_send_slack_alert(high_prices, low_prices)**`


Esta função organiza o envio das notificações para o Slack, chamando a função `upload_and_message` duas vezes: uma para as anomalias de preços altos e outra para as de preços baixos.


#### **Função** `**upload_and_message(df, filename, title, msg)**`


É uma função utilitária responsável pela comunicação com a API do Slack:


1. Recebe um DataFrame do Pandas.
2. Seleciona e renomeia as colunas para um formato mais legível em português.
3. Converte o DataFrame para uma string no formato CSV.
4. Usa o método `files_upload_v2` do cliente Slack para enviar o CSV.
5. Obtém o link permanente (`permalink`) do arquivo recém-enviado.
6. Posta uma mensagem no canal do Slack contendo o texto informativo (`msg`) e o link para o download do arquivo.


## [planilha de preços anomalos](https://docs.google.com/spreadsheets/d/15aVijlOSPIk9CpoYn2Aslzr6RTpQryInboBBeSTB-LM/edit?gid=2010477181#gid=2010477181)