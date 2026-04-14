<!-- title: Back-end | url: https://outline.seazone.com.br/doc/back-end-vgRSnPudqZ | area: Tecnologia -->

# Back-end

Uma agência de viagem online (OTA) **é um site que atua como um mecanismo de pesquisa para viagens** e esta é nesta página que iremos discorrer um pouco sobre o funcionamento do back-end da aplicação do website - seazone-reservas-api

> **Repositório**: <https://github.com/Khanto-Tecnologia/seazone-reservas-api>

O backend consiste nesses principais serviços.

* Rest API ([FastAPI](https://fastapi.tiangolo.com/))
* Processador de tarefas assíncronas ([Celery](https://docs.celeryq.dev/en/stable/getting-started/introduction.html))
* Executor de tarefas periódicas ([Celery Beat](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html))
* Banco de dados ([Postgresql](https://www.postgresql.org/))
* Engine de busca ([OpenSearch](https://opensearch.org/))
* Cache ([Redis](https://redis.io/))
* Serviço de mensageria ([RabbitMQ](https://www.rabbitmq.com/))

## Por que criar um backend se já temos as API's da Stays?

Quando criamos o backend a Seazone já utilizava a Stays (sistema terceiro para gerenciamento de anúncios de imóveis). Importante destacar que a Stays por si só já disponibiliza API's para fazer quase tudo o que precisaríamos para o website, porém como uma estratégia para não ficar tão amarrados e limitados com a Stays e também pela lentidão e complexidade de algumas API's deles, decidimos criar o nosso próprio backend. Desse modo, no ecossistema do website, o backend é o único sistema que de fato "conhece" a existência da Stays (o frontend apenas conhece o backend).

## Sincronização periódica com a Stays

Como a Seazone continua usando a Stays, precisamos alimentar nosso banco de dados com alguns dados que vem da Stays, para isso utilizamos a seguinte abordagem:

* Executamos tarefas periódicas diariamente para buscar todas as informações que precisamos da Stays.
* Essas informações consistem basicamente em imóveis, disponibilidade, preços, etc.
* Armazenamos essas informações no nosso banco de dados relacional (tabelas `properties`, `destinations`, etc).
* Indexamos parte dessas informações no OpenSearch para prover um mecanismo de busca de imóveis mais eficiente.
* Utilizamos webhooks da Stays para sincronizar os dados em tempo quase real.

## FastAPI, Celery e Celery Beat

Podemos considerar que o código fonte do backend é divido em três serviços: **FastAPI**, para prover endpoints HTTP, **Celery**, uma biblioteca Python para processamento de tarefas assíncronas, e o **Celery Beat**, uma parte do Celery capaz de executar tarefas periódicas.

Todos os três rodam de maneira completamente individual, no entanto mantivemos ambos no mesmo repositório pois o Celery utiliza algumas funções globais do projeto e também porque manter no mesmo repositório simplifica a comunicação entre eles.

De grosso modo, a iteração entre esses 3 componentes acontece mais ou menos assim:

* O **FastAPI** recebe uma requisição do front.
* O **FastAPI** processa alguma coisa simples (salvar algo no banco de dados).
* O **FastAPI** manda algum processamento mais demorado para o **Celery** processar de maneira assíncrona e já retorna para o front imediatamente.
* De tempos em tempos o **Celery Beat** envia alguma tarefa para o **Celery** processar (exemplo: sincronizar com a Stays).

### FastAPI

Para expor endpoints HTTP, decidimos utilizar o Web Framework Python FastApi. A motivação dessa escolha foi por que o FastApi é um framework moderno e já consolidado no mercado, e também já provê o Swagger por padrão, facilitando a documentação dos endpoints.

**Utilização do Async**

O FastApi foi pensando para permitir utilizar a tecnologia [AsynIo](https://docs.python.org/3/library/asyncio.html) introduzida no Python3. [Nessa documentação](https://fastapi.tiangolo.com/async/) do FastAPI é possível entender mais detalhes de como isso funciona e porque isso é bom.

De modo geral, é possível utilizar ou não funções async nos endpoints, no entanto, para esse projeto é recomendado sempre utilizar, pois isso faz com que a API seja capaz de servir muito mais requisições de maneira mais eficiente, porém **é essencial entender melhor como AsyncIO funciona lendo as documentações.**

### Celery

Para processamento de tarefas assíncronas utilizamos a biblioteca Celery. O Celery trabalha como uma espécie de consumidor de filas (RabbitMQ), sempre esperando uma tarefa chegar, para assim processá-la. O uso mais intenso do Celery no projeto é para sincronizar os dados da Stays, porém também é utilizado em outros contextos.

Com o Celery podemos:

* Definir uma tarefa assíncrona.
* Definir estratégias de retentativas (em caso de falha).
* Encadear tarefas.
* Dentre outras coisas. **É imprescindível ler a documentação do Celery, fazer algum projeto de teste para aprender bem como o Celery funciona.**

## OpenSearch

Utilizamos o OpenSearch para prover um mecanismo de busca mais poderoso. Os dados do OpenSearch são efêmeros, ou seja, podemos excluir todos os dados e ainda assim é possível re-gerar tudo de novo. Toda sincronização com a Stays atualiza os dados do OpenSearch.

***Nota: OpenSearch ou ElasticSearch?***

*Com frequência no inicio do projeto, ao falar sobre a engine de busca, falávamos "ElasticSearch". Isso aconteceu porque o OpenSearch na verdade é um fork do ElasticSearch, porém é um erro considerar que são a mesma coisa, com o tempo ambos se tornaram produtos similares porém com diferenças, de modo que nunca devemos consultar a documentação do ElasticSearch achando que vamos encontrar as mesmas funcionalidades do OpenSearch. Sempre devemos consultar a documentação do OpenSearch.*

[Casos de Uso do OpenSearch no Site de Reservas](/doc/casos-de-uso-do-opensearch-no-site-de-reservas-RjU1Dc8D0B)

## Redis

O Redis é um banco de dados não relacional que tem como uma de suas principais características o armazenamento de informações na memória, o que o torna altamente versátil, dinâmico, ágil e faz com que consigamos processar dados em uma velocidade muito mais alta da do que com outras aplicações, mesmo que seus volumes sejam muito altos.

Para ser capaz de funcionar com armazenamento em alta velocidade, o Redis trabalha, basicamente, com dois tipos de processamento: **armazenamento de chave-valor e banco de dados na memória.**

A criação das chaves além de prover uma maior escalabilidade, torna a estrutura do banco de dados mais simplificada e o armazenamento na memória torna toda a atividade muito mais rápida, já que o processamento das informações leva muito menos tempo do que estruturas tradicionais.

Atualmente **possuímos instância na EC2 da AWS** que estão responsáveis pelo gerenciamento das estruturas do Redis da nossa aplicação back-end.

* Alguns de seus principais benefícios são:
  * Desempenho muito rápido;
  * Estrutura de dados na memória;
  * Compatibilidade com diversas linguagens de programação como: Java, Python, PHP, C, C++, C#, JavaScript, Node.js, Ruby, R, Go e muitas outras.
* Casos de uso
  * Armazenamento em cache;
  * Gerenciamento de sessões;
  * Filas;
  * Sistemas de mensagens.

## CloudWatch

Cloudwatch é um **serviço de monitoramento da AWS** para os recursos da nuvem e aplicações que executamos dentro do ecossistema.

Utilizamos o back-end para rastrear, investigar e mitigar cenários indesejados;

## RabbitMQ

O **RabbitMQ** é uma espécie de servidor de **mensageria** que utiliza o padrão AMQP e permite o **envio** e **recebimento** de dados de forma **assíncrona**, e utiliza o modelo de sistema de enfileiramento de mensagens.

No nosso sistema, utilizamos o Celery como ferramenta de fila de tarefas. Ou seja, usamos o Celery para enviar as tarefas a serem tratadas para as filas do RabbitMQ para que ele possa processar essas mensagens de forma assíncrona e, se necessário, nos retornar essas informações.

Uma das vantagens de utilizarmos o Celery e o RabbitMQ hoje em nossa aplicação é que ela também é orientada a eventos.

## Rodar localmente

Ler [README](https://github.com/Khanto-Tecnologia/seazone-reservas-api/blob/main/README.md#seazone-reservas-api) do projeto para saber como rodar localmente, alterar o banco de dados, etc.

* **pip freeze (backup)**

  Este é um backup para debugs futuros em caso de incidente no site de reservas.

  Data do backup: 27-02-2024 18h46

  ```
  aiohttp==3.9.2
  aioredis==2.0.1
  aiosignal==1.3.1
  alembic==1.9.2
  amqp==5.2.0
  anyio==4.3.0
  astroid==3.1.0
  asttokens==2.4.1
  async-timeout==4.0.3
  asyncpg==0.27.0
  attrs==23.2.0
  Authlib==1.2.0
  billiard==3.6.4.0
  boto3==1.26.79
  botocore==1.29.165
  cachetools==5.3.3
  celery==5.2.7
  certifi==2024.2.2
  cffi==1.16.0
  charset-normalizer==3.3.2
  click==8.1.7
  click-didyoumean==0.3.0
  click-plugins==1.1.1
  click-repl==0.3.0
  cryptography==42.0.5
  decorator==5.1.1
  Deprecated==1.2.14
  dill==0.3.8
  dnspython==2.5.0
  email_validator==2.1.1
  eventlet==0.33.3
  exceptiongroup==1.2.0
  executing==2.0.1
  fastapi==0.89.1
  fire==0.5.0
  freezegun==1.1.0
  frozenlist==1.4.1
  greenlet==3.0.3
  gunicorn==20.1.0
  h11==0.14.0
  httpcore==1.0.4
  httptools==0.6.1
  httpx==0.27.0
  idna==3.6
  importlib_resources==6.1.2
  iniconfig==2.0.0
  ipython==8.22.1
  isort==5.13.2
  itsdangerous==2.1.2
  jedi==0.19.1
  Jinja2==3.1.3
  jmespath==1.0.1
  kombu==5.3.5
  limits==3.9.0
  Mako==1.3.2
  MarkupSafe==2.1.5
  matplotlib-inline==0.1.6
  mccabe==0.7.0
  multidict==6.0.5
  opensearch-py==2.1.1
  orjson==3.9.15
  packaging==23.2
  parso==0.8.3
  pexpect==4.9.0
  platformdirs==4.2.0
  pluggy==1.4.0
  prompt-toolkit==3.0.43
  psycopg2-binary==2.9.5
  ptyprocess==0.7.0
  pure-eval==0.2.2
  pycparser==2.21
  pydantic==1.10.14
  Pygments==2.17.2
  PyJWT==2.6.0
  pylint==3.1.0
  pytest==8.0.2
  pytest-env==1.1.3
  python-dateutil==2.8.2
  python-dotenv==1.0.1
  python-multipart==0.0.9
  pytz==2024.1
  PyYAML==6.0.1
  redis==4.4.4
  requests==2.31.0
  ruff==0.0.259
  s3transfer==0.6.2
  six==1.16.0
  slowapi==0.1.8
  sniffio==1.3.1
  SQLAlchemy==2.0.1
  stack-data==0.6.3
  starlette==0.22.0
  termcolor==2.4.0
  tomli==2.0.1
  tomlkit==0.12.4
  traitlets==5.14.1
  typing_extensions==4.10.0
  ujson==5.9.0
  Unidecode==1.3.8
  urllib3==1.26.18
  uvicorn==0.20.0
  uvloop==0.19.0
  vine==5.1.0
  watchfiles==0.21.0
  wcwidth==0.2.13
  websockets==12.0
  wrapt==1.16.0
  yarl==1.9.4
  
  ```