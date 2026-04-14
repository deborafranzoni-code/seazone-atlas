<!-- title: Airbnb Image Scraper | url: https://outline.seazone.com.br/doc/airbnb-image-scraper-4cda2oeY6w | area: Tecnologia -->

# Airbnb Image Scraper

# Airbnb Image Scraper: Pipeline de Extração de Imagens

Este projeto implementa um pipeline distribuído para extrair metadados e imagens de anúncios do Airbnb. A solução é projetada para ser executada na Google Cloud Platform (GCP), utilizando serviços como Cloud Run Jobs, Pub/Sub e Cloud Storage para criar um fluxo de trabalho robusto, escalável e assíncrono.

O sistema também se integra com AWS (para buscar a lista de anúncios) e BigQuery (para evitar processamento duplicado).

## Arquitetura

O fluxo de trabalho segue uma arquitetura de pipeline em três estágios, orquestrada por mensagens do Pub/Sub. Cada estágio é executado como um Job independente no Cloud Run.


1. **Refiller**: Inicia o processo consultando uma view no AWS Athena para obter uma lista de IDs de anúncios (listings) a serem processados. Para cada ID, publica uma mensagem em um tópico Pub/Sub.
2. **Image Metadata Scraper**: Consome os IDs do tópico, verifica se o anúncio já foi processado consultando uma tabela no BigQuery. Caso contrário, acessa a API do Airbnb para extrair os metadados de todas as imagens (URLs, legendas, etc.), salva esses metadados em um arquivo Parquet no Cloud Storage e publica uma mensagem para *cada imagem* em um segundo tópico Pub/Sub.
3. **Images Scraper**: Consome as mensagens com os metadados das imagens, faz o download de cada imagem a partir da URL fornecida, a converte para o formato JPEG e a armazena no Cloud Storage.

### Diagrama do Fluxo

```
  AWS Athena      ┌────────────────────────┐   BigQuery (Deduplicação)
(Lista de IDs)    |     Tópico Pub/Sub     |        ▲
      │           | image-metadata-input   |        │
      │           └────────────────────────┘        │
      ▼                       │                      │
┌───────────────┐   (2. Consome ID)    ┌────────────────────────┐
|   Refiller    |───────────────────► |  Image Metadata Scraper|
└───────────────┘   (1. Publica IDs)  └────────────────────────┘
      ▲                                            │  │
      │                               (3. Salva .parquet) │
      │                                            │  ▼
      │                                            │  Cloud Storage
      │                                            │ (Metadados)
      │                                            │
      │                  (4. Publica metadados de cada imagem)
      │                                            ▼
      │                                  ┌──────────────────┐
      └─────────────────────────────────►|  Tópico Pub/Sub  |
                                        |   images-input   |
                                        └──────────────────┘
                                                  │
                                        (5. Consome msg)
                                                  │
                                                  ▼
                                        ┌──────────────────┐
                                        |  Images Scraper  |
                                        └──────────────────┘
                                                  │
                                        (6. Salva imagem .jpg)
                                                  │
                                                  ▼
                                           Cloud Storage
                                             (Imagens)
```

## Componentes

A execução de cada componente é feita através do ponto de entrada `airbnb.py`.

### 1. Refiller

Este componente inicia o pipeline. Ele se conecta ao AWS Athena para buscar uma lista de `airbnb_listing_id` com base em critérios de negócio pré-definidos (ex: tipo de imóvel, número de quartos, cidades específicas). Os IDs resultantes são publicados como mensagens individuais no tópico Pub/Sub para a próxima etapa.

* **Comando de Execução:**

  ```bash
  python3 airbnb.py refiller --topic=image-metadata-input
  ```
* **Entrada:** Consulta no AWS Athena.
* **Saída:** Mensagens no tópico `image-metadata-input`. Cada mensagem é um JSON no formato: `{'id_airbnb': '...'}`.

### 2. Image Metadata Scraper

Este job consome os IDs do tópico `image-metadata-input`. Para cada ID, ele primeiro verifica se o anúncio já existe na tabela de predições do BigQuery para evitar reprocessamento. Se for um novo anúncio, ele faz uma requisição à API interna do Airbnb para obter os metadados de todas as imagens associadas. Os metadados coletados são salvos em um único arquivo `.parquet` no Cloud Storage e, para cada imagem, uma nova mensagem é enviada ao tópico `images-input`.

* **Comando de Execução:**

  ```bash
  python3 airbnb.py image_metadata
  ```
* **Entrada:** Mensagens do tópico `image-metadata-input`.
* **Saída:**

  
  1. Um arquivo `.parquet` em `gs://categorizacao_pipeline/metadata_parquet/{id_airbnb}-metadata.parquet`.
  2. Múltiplas mensagens no tópico `images-input`, uma para cada imagem, com a estrutura:

     ```json
     {
       "id_airbnb": "...",
       "id_image": "...",
       "url": "...",
       "label": "...",
       "caption": "...",
       "is_professional": true,
       "is_verified": true
     }
     ```

### 3. Images Scraper

A etapa final do pipeline. Consome as mensagens do tópico `images-input`, que contêm a URL de cada imagem. O job faz o download da imagem, a converte para o formato JPEG (garantindo consistência) e a salva no Cloud Storage, organizada em pastas por ID do anúncio.

* **Comando de Execução:**

  ```bash
  python3 airbnb.py images
  ```
* **Entrada:** Mensagens do tópico `images-input`.
* **Saída:** Arquivos de imagem `.jpg` salvos em `gs://categorizacao_pipeline/{id_airbnb}/images/{id_image}.jpg`.

## Configuração

O projeto utiliza variáveis de ambiente para configurar a conexão com os serviços GCP e AWS, além de outros parâmetros de execução.

### Variáveis de Ambiente (apenas exemplos)

| Variável | Descrição | Exemplo |
|----|----|----|
| `GOOGLE_CLOUD_PROJECT` | ID do projeto no Google Cloud Platform. | `data-resources-448418` |
| `GOOGLE_APPLICATION_CREDENTIALS` | Caminho para o arquivo JSON da Service Account do GCP com as permissões necessárias. | `./sandbox-439302-e5ebce15d501.json` |
| `AWS_ACCESS_KEY_ID` | Chave de acesso da AWS para autenticação (usada pelo `refiller`). | `ABCDEFGHIJ` |
| `AWS_SECRET_ACCESS_KEY` | Chave de acesso secreta da AWS (usada pelo `refiller`). |    |
| `USER_AGENTS_BUCKET` | Nome do bucket no Cloud Storage onde o arquivo de User-Agents está localizado. | `categorizacao_pipeline` |
| `AIRBNB_SCRAPERS_USER_AGENTS_KEY` | Caminho completo (key) para o arquivo JSON de User-Agents dentro do bucket. | `pipe-essential-files/user-agents/mesh-user-agents.json` |

### Arquivos de Credenciais

* **GCP:** Um arquivo de credenciais de Service Account (`.json`) é necessário para autenticação nos serviços do Google Cloud. O caminho para este arquivo deve ser definido na variável `GOOGLE_APPLICATION_CREDENTIALS`.
* **AWS:** As credenciais da AWS (`AWS_ACCESS_KEY_ID` e `AWS_SECRET_ACCESS_KEY`) são necessárias para que o `refiller` possa consultar o Athena.

Por razões de segurança, esses arquivos e valores não devem ser versionados no repositório.

## Monitoramento e Alertas

O sistema possui um mecanismo de alertas integrado que envia notificações para uma Cloud Function central (`receive_alert`) em caso de falhas críticas.

* **Componente:** `cloud_function_alert_sender.py`
* **Funcionamento:** Em caso de exceção não tratada nos jobs principais (`refiller`, `image_metadata`, `images`), uma instância de `CloudFunctionAlertSender` é criada para enviar um payload detalhado do erro.
* **Payload do Alerta:** Inclui `severity`, `message`, `app_name`, `execution_id` e um dicionário `details` com o traceback do erro.