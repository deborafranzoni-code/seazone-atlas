<!-- title: Mesh | url: https://outline.seazone.com.br/doc/mesh-RiDXjKWOU4 | area: Tecnologia -->

# Mesh

### Scraper Mesh para Localização de Anúncios

O scraper Mesh utiliza a API de localização para encontrar IDs dos anúncios em diferentes regiões do Brasil, dividindo o país em quadrantes para cobrir áreas específicas com mais precisão. Esse processo ajuda a organizar a coleta de dados, aumentando a eficiência e permitindo que a consulta aos anúncios seja mais direcionada. Podemos ver na imagem de qual parte do site retiramos os dados. 

 ![](/api/attachments.redirect?id=2d0680d9-e0e1-4755-bc7c-fb7ff3d7e7d1)

#### Lógica dos Quadrantes

Para cobrir o Brasil inteiro, rodamos o scraper Mesh dividindo o território em quadrantes de diferentes tamanhos, conforme a necessidade de precisão. À medida que o quadrante fica menor, a precisão dos anúncios coletados para cada área aumenta, mas a API de localização apresenta algumas limitações e características particulares que influenciam a lógica de busca:

* **Quadrantes Grandes**: Quando dividimos o Brasil em áreas amplas, como 45 quadrantes cobrindo grandes regiões, a API limita o retorno a no máximo 30 IDs por consulta.
* **Quadrantes Pequenos**: Ao diminuir o tamanho dos quadrantes para áreas menores que uma cidade, a API pode retornar até 100 IDs. No entanto, esses IDs geralmente se concentram em um único ponto de alta densidade, o que pode distorcer a distribuição esperada.

Dado esse comportamento, é essencial aplicar uma lógica de adaptação: sempre que o retorno da API para um quadrante é maior que 30 IDs (exceto quando o quadrante está em 1 m² ou menor), o quadrante é automaticamente dividido em áreas menores. Esses quadrantes menores são então re-enviados para a fila, para que o scraper processe a área em partes menores até que a consulta de cada quadrante individual retorne menos de 30 IDs, mantendo a precisão sem sobrecarregar os dados.

Para evitar sobreposição e perdas, configuramos um limite mínimo de tamanho de 1 m² para cada quadrante. Quando a área consultada é menor que 1 m², consideramos os IDs retornados pela API como representativos da área e processamos esses dados diretamente, uma vez que a suposição é que representam todos os anúncios relevantes em um único ponto.

A imagem abaixo demonstra a distribuição inicial dos quadrantes criados pelo refiller para cobrir o Brasil e ilustrar como o sistema se adapta ao número de IDs por quadrante.

 ![](/api/attachments.redirect?id=915b6043-fa4d-4353-93af-a301ffa5dc62)


\
## Arquitetura do Scraper Mesh

A arquitetura do scraper Mesh é única em comparação aos outros scrapers, pois utiliza um refiller que não busca IDs em um bucket do S3. Em vez disso, o refiller se conecta à API de localização do Nominatim para obter dados iniciais de área e gerar quadrantes, alimentando a fila de IDs necessária para que o scraper principal inicie a coleta detalhada dos anúncios.


1. **Refiller Mesh com API Nominatim**: O refiller consulta a API Nominatim para localizar as coordenadas de áreas específicas (como regiões do Brasil) e transforma essas áreas em quadrantes. Esses quadrantes são então enviados para uma fila SQS, onde os dados são divididos para otimizar a coleta pelo scraper principal.
2. **Scraper Principal e Firehose**: Assim que o refiller preenche a fila SQS com os quadrantes, o scraper principal começa a rodar. Ele utiliza os dados dessa fila para consultar os IDs de anúncios em cada área quadrante, extraindo informações detalhadas. Esses dados são então enviados ao Firehose, que escreve os dados no bucket S3 do Data Lake para processamento e armazenamento futuros.
3. **Orquestração e Automatização**: Como outros scrapers, a execução do scraper Mesh é orquestrada por uma Step Function, que dispara o fluxo de trabalho diariamente por meio de um trigger no EventBridge, garantindo que o refiller, o scraper principal e o armazenamento de dados ocorram automaticamente em uma frequência regular.

 ![](/api/attachments.redirect?id=71c22fce-8d79-432f-a062-e57f5fd03532)

### Principais Serviços e Componentes

* [S3 Bucket Essential Files](https://us-west-2.console.aws.amazon.com/s3/object/pipe-essential-files?region=us-west-2&bucketType=general&prefix=Pipe-scrapers/external/environment/booking_scrapers.env): Armazena o .env para o scraper utilizar
* [SQS - Fila de Inputs](https://us-west-2.console.aws.amazon.com/sqs/v3/home?region=us-west-2#/queues/https%3A%2F%2Fsqs.us-west-2.amazonaws.com%2F452791833956%2Fbooking-mesh-input.fifo): Fila de IDs para o scraper
* [SQS - Fila de Falhas](https://us-west-2.console.aws.amazon.com/sqs/v3/home?region=us-west-2#/queues/https%3A%2F%2Fsqs.us-west-2.amazonaws.com%2F452791833956%2Fbooking-mesh-failure.fifo): Registra falhas de processamento
* [Kinesis Data Firehose](https://us-west-2.console.aws.amazon.com/firehose/home?region=us-west-2#/details/brlink-listing_booking_mesh-PUT-S3-q57qR/monitoring): Processamento e envio de dados
* [AWS Step Functions](https://us-west-2.console.aws.amazon.com/states/home?region=us-west-2#/statemachines/view/arn%3Aaws%3Astates%3Aus-west-2%3A452791833956%3AstateMachine%3Ascraper_booking_mesh?type=padr%C3%A3o): Orquestração do pipeline
* [EventBridge](https://us-west-2.console.aws.amazon.com/scheduler/home?region=us-west-2#schedules/default/scraper_booking_mesh): Trigger semanal para Step Functions
* [ECS - Scraper Principal](https://us-west-2.console.aws.amazon.com/ecs/v2/clusters/galadriel/services/pipe-booking-scraper-mesh/health?region=us-west-2): Execução do scraper principal
* [ECS - Refiller](https://us-west-2.console.aws.amazon.com/ecs/v2/task-definitions/pipe-booking-refiller?status=ACTIVE&region=us-west-2): Execução do refiller de IDs
* [Pipe Lake S3 Bucket](https://us-west-2.console.aws.amazon.com/s3/buckets/brlink-seazone-raw-data?region=us-west-2&bucketType=general&prefix=listing_booking_mesh/&showversions=false): Armazena os dados processados no Data Lake