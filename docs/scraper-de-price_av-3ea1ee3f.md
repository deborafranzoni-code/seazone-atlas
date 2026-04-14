<!-- title: Scraper de Price_Av | url: https://outline.seazone.com.br/doc/scraper-de-price_av-FWh9dqpgqj | area: Tecnologia -->

# Scraper de Price_Av

O scraper price_av é responsável por coletar dados detalhados sobre **datas**, **disponibilidade** e **preços** das propriedades no Booking.com. Ele utiliza uma API de calendário, que permite acessar informações não apenas sobre datas atuais, mas também sobre **disponibilidade futura** — essencial para a previsão e análise de ocupação.

#### Características e Funcionamento

* **API de Calendário**: O scraper faz chamadas na API de calendário para obter informações sobre cada propriedade, incluindo datas futuras disponíveis.
* **IDs em Uso**: Atualmente, ele está configurado para processar apenas IDs de propriedades da Seazone, facilitando o foco em um subset específico de dados.
* **Limitações de Preço**: No momento, o preço extraído corresponde **somente ao quarto mais barato** da propriedade, o que limita a visão dos diferentes tipos de acomodações disponíveis.

Podemos ver a imagem do calendário para um melhor entendimento. 

 ![](/api/attachments.redirect?id=71678b2f-44c9-409b-a789-be1a947579a5)

#### Problemas Conhecidos


1. **Preço Limitado ao Quarto Mais Barato**: Atualmente, só é coletado o valor referente ao quarto de menor preço, o que pode não refletir a faixa completa de opções de hospedagem.
2. **Dependência da Seazone**: Como o scraper está configurado para buscar apenas IDs da Seazone, isso reduz a diversidade de propriedades monitoradas, que poderiam trazer insights mais amplos do mercado. (Já está sendo estudado uma ampliação para pegar ids do Rio de Janeiro).

## Arquitetura do Pipeline de Scraping

A arquitetura desse pipeline foi projetada para garantir uma coleta, processamento e armazenamento eficazes dos dados de propriedades do Booking.com, utilizando uma série de serviços AWS em conjunto.

#### Visão Geral


1. **Refiller**: O processo começa com o refiller, que coleta IDs de propriedades armazenados em um bucket S3. Esses IDs são organizados e enviados para uma fila **SQS**. Este passo é essencial para alimentar o fluxo de dados e garantir que os scrapers tenham uma fonte contínua de IDs de propriedades a serem processados.
2. **Scraper Principal**: Com a fila SQS preenchida, o scraper principal é acionado. Ele lê os IDs da fila, acessa a API do Booking.com e realiza a extração dos dados. Após coletar as informações, o scraper envia esses dados para o **Amazon Kinesis Data Firehose**, que os processa e armazena no bucket S3 do **Data Lake**.
3. **Step Functions**: Todo o pipeline é orquestrado por uma **AWS Step Function**. Esse componente define a ordem das operações, controla o fluxo entre refiller e scraper e monitora o processo para garantir o sucesso das execuções diárias.
4. **Trigger Diário com EventBridge**: A execução da Step Function é automatizada com o **Amazon EventBridge**, que dispara o processo diariamente.


 ![](/api/attachments.redirect?id=2923daba-fa86-4689-8108-a014e5376d83)

### Principais Serviços e Componentes

* [S3 Bucket Refiller](https://us-west-2.console.aws.amazon.com/s3/buckets/pipe-listings?region=us-west-2&bucketType=general&prefix=booking/priceav/&showversions=false): Armazena arquivos de IDs
* [S3 Bucket Essential Files](https://us-west-2.console.aws.amazon.com/s3/object/pipe-essential-files?region=us-west-2&bucketType=general&prefix=Pipe-scrapers/external/environment/booking_scrapers.env): Armazena o .env para o scraper utilizar
* [SQS - Fila de Inputs](https://us-west-2.console.aws.amazon.com/sqs/v3/home?region=us-west-2#/queues/https%3A%2F%2Fsqs.us-west-2.amazonaws.com%2F452791833956%2Fbooking-priceav-input.fifo): Fila de IDs para o scraper
* [SQS - Fila de Falhas](https://us-west-2.console.aws.amazon.com/sqs/v3/home?region=us-west-2#/queues/https%3A%2F%2Fsqs.us-west-2.amazonaws.com%2F452791833956%2Fbooking-priceav-failure.fifo): Registra falhas de processamento
* [Kinesis Data Firehose](https://us-west-2.console.aws.amazon.com/firehose/home?region=us-west-2#/details/brlink-listing_booking_priceav-PUT-S3-EhXrt/monitoring): Processamento e envio de dados
* [AWS Step Functions](https://us-west-2.console.aws.amazon.com/states/home?region=us-west-2#/statemachines/view/arn%3Aaws%3Astates%3Aus-west-2%3A452791833956%3AstateMachine%3Ascraper_booking_priceav?type=padr%C3%A3o): Orquestração do pipeline
* [EventBridge](https://us-west-2.console.aws.amazon.com/scheduler/home?region=us-west-2#schedules/default/scraper_booking_priceav): Trigger diário para Step Functions
* [ECS - Scraper Principal](https://us-west-2.console.aws.amazon.com/ecs/v2/clusters/galadriel/services/pipe-booking-scraper-priceav/health?region=us-west-2): Execução do scraper principal
* [ECS - Refiller](https://us-west-2.console.aws.amazon.com/ecs/v2/task-definitions/pipe-booking-refiller?status=ACTIVE&region=us-west-2): Execução do refiller de IDs
* [Pipe Lake S3 Bucket](https://us-west-2.console.aws.amazon.com/s3/buckets/brlink-seazone-raw-data?region=us-west-2&bucketType=general&prefix=listing_booking_priceav/&showversions=false): Armazena os dados processados no Data Lake