<!-- title: Descrição | url: https://outline.seazone.com.br/doc/descricao-bX1jn7OTef | area: Tecnologia -->

# Descrição

Explicação da Meta 1.0 em diagrama.


### Faturamento dos concorrentes

O cálculo do faturamento dos concorrentes inicia-se com a recuperação de dados de preços de imóveis concorrentes a partir de tabelas no data lake (Athena). Estes dados incluem informações como preços praticados, status de ocupação e eventuais bloqueios. Após a coleta, é aplicada uma taxa da OTA (Online Travel Agency) para simular o valor líquido do faturamento. Em seguida, realiza-se uma série de agregações e transformações para preparar os dados para comparação com o faturamento dos imóveis da Seazone.


1. Recuperação dos dados do lake

   A etapa inicial do processamento do faturamento dos concorrentes envolve a recuperação de dados brutos de tabelas específicas no data lake (Athena). As tabelas daily_revenue_competitors e competitors_plus são consultadas para obter informações detalhadas sobre os imóveis concorrentes. Esta etapa garante que tenhamos acesso aos preços, status de ocupação e outras informações necessárias para os cálculos seguintes.

 ![](/api/attachments.redirect?id=a8ca3fb3-f056-41db-b41a-c5e490577ed0)



2. Tratamento do p25 até estar pronto para merge com dados dos imóveis seazone

   Após a recuperação dos dados dos concorrentes, um processamento específico é realizado para obter um valor representativo para comparação. O cálculo do percentil 25 dos preços dos concorrentes ocupados é realizado. Esse percentil, juntamente com a taxa de ocupação dos concorrentes, é usado para calcular uma estimativa de faturamento diário dos concorrentes. Os dados são então agregados e preparados para serem combinados com dados de faturamento dos imóveis da Seazone.

 ![](/api/attachments.redirect?id=2cedff8e-c76e-415f-8985-3522d81cb5d6)


### Faturamento dos Imóveis Seazone

O cálculo do faturamento dos imóveis da Seazone inicia-se com a recuperação de dados de preços e reservas a partir do data lake. Além dos preços, são também obtidos dados de ocupação, datas de reservas e informações sobre preços especiais. Complementarmente, busca-se o faturamento real dos imóveis no Sapron, para utilizar como um valor de referência. Os dados são então agregados e processados de forma a obter o faturamento diário e mensal para cada imóvel da Seazone.


1. Recuperação dos dados do Sapron em tabelas no lake

   A etapa de recuperação de dados do Sapron envolve a consulta de tabelas específicas no data lake para obter o faturamento mensal real dos imóveis. As tabelas sapron_monthly_fat e listing_status são consultadas para coletar informações sobre o faturamento real e status de atividade de cada imóvel. Esses dados são cruciais para a avaliação final das metas, sendo utilizados como base de comparação para o faturamento estimado.

 ![](/api/attachments.redirect?id=5f222c34-a16d-4e7f-a2c6-d197dcc1afb9)



2. Merge dos faturamentos seazone com de competidores

Após o processamento individual dos dados de faturamento de concorrentes e imóveis da Seazone, é realizado um *merge* (combinação) desses conjuntos de dados. O *merge* é baseado nas informações de categoria e data, garantindo que os dados de concorrentes e os da Seazone sejam comparados corretamente. O resultado dessa combinação é um conjunto de dados consolidado, que inclui informações sobre o faturamento estimado dos concorrentes e os dados dos imóveis da Seazone.

 ![](/api/attachments.redirect?id=e68598e1-5c23-4422-8a36-f57164c60d39)


Sendo o month_fat_competitor o faturamento dos imóveis concorrentes, e as informações abaixo, todos os dados relacionados à imóveis seazone.


### Comunicação entre Lambda x Api Gateway x AppScript

O processo de análise e cálculo de metas envolve a comunicação entre diferentes camadas e serviços da AWS e Google. Após o processamento no AWS Lambda, os resultados são armazenados no S3. Para disponibilizar esses dados no Google Sheets, um script do App Script envia uma requisição POST para o API Gateway da AWS. O API Gateway, por sua vez, aciona a função Lambda que disponibiliza o arquivo JSON com os dados. O App Script recebe este JSON e transfere os dados para a planilha. Essa arquitetura garante uma comunicação eficiente entre os diferentes ambientes.

 ![](/api/attachments.redirect?id=6151d2ed-3b0e-4b11-8559-ced8f408116a)


\
### Organização dos Dados nas metas batidas

Os dados processados e calculados são então organizados na planilha do Google Sheets, dentro da aba Database. Para cada imóvel, é criado um registro com informações sobre o status da meta (bateu ou não bateu), taxas de ocupação, faturamento real, faturamento dos concorrentes, dias com preço especial, status do imóvel (ativo, inativo, onboarding) e outras métricas. Os dados são agregados e atualizados diariamente, mantendo um histórico completo do desempenho para acompanhamento e análise.

 ![](/api/attachments.redirect?id=fabb55d9-d616-4473-9656-9d4d2fada9b3)


### Esquema geral:


 ![](/api/attachments.redirect?id=9fe994bb-1e54-4080-9894-b4a981921f62)


### Referência completa do esquema no Miro:

[https://miro.com/app/board/uXjVLItK9Eo=/](https://miro.com/app/board/uXjVLItK9Eo=/)