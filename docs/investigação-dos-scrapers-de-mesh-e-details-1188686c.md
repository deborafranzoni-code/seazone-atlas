<!-- title: Investigação dos Scrapers de Mesh e Details | url: https://outline.seazone.com.br/doc/investigacao-dos-scrapers-de-mesh-e-details-QFRpgT72uh | area: Tecnologia -->

# Investigação dos Scrapers de Mesh e Details

## Glossário

**Data Lake**

É um repositório centralizado de armazenamento que suporta grandes volumes de dados em diferentes formatos. Ele lida bem com dados estruturados, semiestruturados e não estruturados. No contexto de Data Ops, os dados coletados pelos scrapers são enviados e armazenados no Data Lake. Por exemplo, depois que o scraper coleta informações sobre anúncios dos imóveis (preço, avaliações, descrição), esses dados são enviados para o Data Lake e, a partir dos dados disponibilizados nele, podem ser gerados produtos ou ferramentas.


**SQS (Simple Queue Service)**

O SQS é um serviço de filas de mensagens da AWS que organiza e controla o fluxo de tarefas entre sistemas. Ele garante que as mensagens não se percam e possam ser processadas de forma assíncrona. Por exemplo, cada ID de anúncio coletado pelo scraper é enviado para uma fila do SQS. Caso falhe constantemente, ultrapassando o limite estabelecido de tentativas de processamento, é enviado para a fila de falha, o que garante que possa ser analisado depois.


**Firehose (Kinesis Data Firehose)**

É um serviço da AWS responsável por receber os dados em tempo real e entregar diretamente para armazenamento, tendo como destino, por exemplo, o Amazon S3. No contexto dos scrapers, ele pega os dados e envia para o Data Lake. Por exemplo, assim que o scraper coleta os detalhes de um anúncio, o Firehose envia os dados para o Data Lake.


**Timeout**

Timeout é o tempo máximo definido para uma tarefa ser executada. Se esse tempo for ultrapassado, a execução é interrompida e falha. Se o volume de dados solicitado for muito grande também, a operação pode levar mais tempo do que o limite configurado e dessa forma, ocorre timeout. 


**Scraping**

É o processo de extração automatizada de dados de páginas ou sistemas. No nosso contexto, os scrapers coletam dados da Airbnb, do Booking, da OLX, etc. 


## Por que Mesh/Details são críticos

O Mesh é um scraper que roda quinzenalmente e tem como principal função coletar os IDs dos listings do Brasil diretamente da API do Mapa do Airbnb. Esses IDs serão usados pelo scraper de Details para obter informações detalhadas de cada anúncio. Por isso, o Mesh é muito importante no fluxo de dados.

Quando o Mesh apresenta falhas, os impactos variam de acordo com o momento da quebra:

* Se ele quebra no ínicio, os listings podem ficar desatualizados, ou seja, IDs novos não são capturados.

  \
* Se ele apresenta mau funcionamento no meio do processo, ele pode coletar apenas parte dos listings, o que resulta em uma coleta de dados parcial.

A quebra do Mesh não causa um impacto imediato no dia a dia, mas a sua falha compromete a atualização contínua dos dados, o que afeta o time de Data Solutions que não consegue fornecer informações precisas para o time de RM (Revenue Management). Como anúncios são ativados e desativados diariamente no Airbnb, a falta de atualização faz com que fiquem armazenados muitos IDs inativos ao longo do tempo, dificultando a análise de concorrentes e a categorização correta dos imóveis.

Já o Details é um scraper que depende dos IDs capturados pelo Mesh. Ele coleta informações detalhadas de cada listing como preço, características do imóvel, avaliações. Sem fornecimento correto dos IDs do Mesh, o Details não processa a descrição dos novos listings ou acaba processando uma quantidade limitada de anúncios. A falta de dados detalhados também impede que o time de RM tenha informações atualizadas para tomada de decisão e estratégias. 

Em resumo, os scrapers de Mesh e Details possuem uma relação de dependencia: o Mesh fornece os IDs e o Details utiliza esses IDs para coletar os dados detalhados. A falha em um deles impacta o fluxo de informações que coletamos do Airbnb, prejudicando a atualização de listings, a análise de concorrência e a categorização dos imóveis. O monitoramento e a garantia do funcionamento correto de ambos os scrapers são necessários para manter a confiabilidade dos dados e a operação eficiente dos times de Data Solutions e RM.


\