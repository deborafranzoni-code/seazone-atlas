<!-- title: Documentação Técnica | url: https://outline.seazone.com.br/doc/documentacao-tecnica-NVTfqAp8dX | area: Tecnologia -->

# Documentação Técnica

# **1. Visão Geral**

Este documento descreve o processo de ETL (Extração, Transformação e Carga) implementado em Python, projetado para ser executado como uma Google Cloud Function. O objetivo principal do script é consolidar dados de precificação de sistemas, enriquecê-los com informações contextuais (feriados, clima) e prepará-los para análise do [KPI da System Price](https://lookerstudio.google.com/reporting/8702a806-21cc-4d33-9997-c369b0b4408c/page/ADLRF).

O arquivo salvo no Parquet da GCP é transformado em uma tabela da BigQuery chamada "infos.kpi_system_price" que é direcionado para o dashboard.

# **2. Arquitetura e Ambiente**

* **Linguagem:** Python 3
* **Bibliotecas Principais:**
  * `pandas` / `numpy`: Para manipulação e transformação de dados.
  * `awswrangler` / `boto3`: Para interagir com serviços da AWS (Athena e S3).
  * `gcsfs`: Para interagir com o Google Cloud Storage.
  * `functions_framework`: Para o deploy como uma Google Cloud Function.
  * `requests`: Para enviar notificações de erro via webhook.
* **Fontes de Dados (AWS):**
  * AWS Athena (Data Lake Query Engine)
  * AWS S3 (Simple Storage Service)
* **Destino dos Dados (GCP):**
  * Google Cloud Storage (GCS)

# **3. Fluxo de Execução Detalhado**

A execução é iniciada por um gatilho HTTP e segue os seguintes passos:


1. **Ponto de Entrada:** A função `main(request)` é acionada.
2. **Sessão AWS:** Uma sessão `boto3` é criada utilizando credenciais de ambiente para autenticar as chamadas aos serviços da AWS.
3. **Execução do ETL:** A função `get_info()` é invocada para realizar o pipeline de dados: a. **Extração:** Dados brutos de preços são consultados no AWS Athena. b. **Transformação:** Os dados são limpos, pivotados e enriquecidos. c. **Enriquecimento:** Dados adicionais de feriados e clima são lidos do S3 e integrados ao conjunto de dados principal. d. **Engenharia de Features:** Novas colunas analíticas (`tipo_dia`, `antecedencia_cat`) são calculadas.
4. **Carga no GCS:** a. A conexão com o Google Cloud Storage é estabelecida via `gcsfs`. b. O diretório de destino é limpo para remover dados antigos (`fs.rm(PREFIX)`). c. O DataFrame final é salvo em formato Parquet no GCS.
5. **Finalização:** A função retorna uma resposta de sucesso (`"ok"`, status 200).
6. **Tratamento de Erro:** Se qualquer exceção ocorrer, ela é capturada, uma notificação detalhada é enviada para um webhook e a função retorna uma resposta de erro (status 500).


---

# **4. Descrição dos Componentes**

## **4.1. Configuração (Variáveis de Ambiente e Constantes)**

| Nome | Tipo | Descrição |
|----|----|----|
| `AWS_ACCESS_KEY_ID` | Secret | Chave de acesso da AWS. |
| `AWS_SECRET_ACCESS_KEY` | Secret | Chave secreta da AWS. |
| `WEBHOOK_URL` | Secret | URL para notificação de erros. |
| `INPUT_DATABASE` | Constante | Nome do banco de dados Athena para dados de grupos. |
| `PRICING_DATABASE` | Constante | Nome do banco de dados Athena para dados de preços. |
| `REVENUE_DATA` | Constante | Nome do banco de dados Athena usado como contexto da query principal. |
| `BUCKET_SHEETS_COMMUNICATION` | Constante | Bucket S3 que armazena arquivos de entrada (feriados, clima). |
| `PROJECT_ID` | Constante | ID do projeto no Google Cloud. |
| `PREFIX` | Constante | Prefixo no bucket GCS onde o artefato final será salvo. |

## **4.2. Ponto de Entrada (**`main`)

* **Assinatura:** `@functions_framework.http def main(request)`
* **Responsabilidade:** Orquestrar o pipeline completo e gerenciar a execução. É o wrapper que integra a lógica de ETL com a infraestrutura da nuvem (autenticação, I/O e logging de erros).

## **4.3. Função Principal de ETL (**`get_info`)

Esta é a função central que encapsula toda a lógica de transformação.

* **Passo 1: Extração (AWS Athena)**
  * Executa uma query SQL que une a tabela de grupos de imóveis (`setup_groups`) com a tabela de preços (`last_offered_price`).
  * Filtra os dados para incluir apenas os preços para os próximos 180 dias.
* **Passo 2: Pivotagem (Transformação)**
  * Utiliza `pandas.pivot_table` para transformar linhas de `group_type` em colunas (`Categoria`, `Cidade`, `Polígono`, etc.), criando um formato de tabela "larga" que é mais adequado para análise.
* **Passo 3: Enriquecimento (Funções Auxiliares)**
  * Invoca `get_holidays()` para adicionar informações sobre feriados.
  * Invoca `get_climate()` para adicionar o tipo de clima de cada imóvel.
* **Passo 4: Engenharia de Features**
  * `tipo_dia`: Classifica cada data como "Final de Semana" ou "Dia de Semana".
  * `antecedencia_cat`: Categoriza a antecedência da reserva em faixas: `0-15 dias`, `16-60 dias`, `61+ dias`.
* **Passo 5: Limpeza e Padronização**
  * Renomeia as colunas para um padrão consistente em inglês (e.g., `Cidade` -> `city`).
  * Remove quaisquer registros com dados ausentes (`dropna`).
  * Adiciona a coluna `acquisition_date` com a data atual da execução.
* **Retorno:** Um DataFrame `pandas` final, pronto para ser carregado.

## **4.4. Funções Auxiliares (**`get_holidays`, `get_climate`)

* `get_holidays(df, listings, session)`: Lê dados de feriados do S3, expande os intervalos de datas e os integra ao DataFrame principal com base no `id_seazone` e na `date`.
* `get_climate(df, listings, session)`: Lê dados de clima do S3 e os integra ao DataFrame principal com base no `id_seazone`.

# **5. Estrutura de Dados**

## **5.1. Fontes de Dados (Entrada)**


1. **Tabela Athena:** `{INPUT_DATABASE}.setup_groups`
2. **Tabela Athena:** `{PRICING_DATABASE}.last_offered_price`
3. **Arquivo S3:** `s3://{BUCKET_SHEETS_COMMUNICATION}/inputs/holidays/state=current/` (Parquet)
4. **Arquivo S3:** `s3://{BUCKET_SHEETS_COMMUNICATION}/inputs/climate/state=current/` (Parquet)

## **5.2. Artefato de Saída (Saída)**

* **Formato:** Parquet
* **Localização:** `gs://{PREFIX}/system_price.parquet`
* **Schema Final (Colunas):**
  * `id_seazone`: Identificador único do imóvel.
  * `date`: Data a que o preço se refere (formato YYYY-MM-DD).
  * `price`: Preço final ofertado.
  * `suggested_price`: Preço sugerido pelo sistema.
  * `category`: Categoria do imóvel.
  * `city`: Cidade do imóvel.
  * `macroregion`: Macrorregião do imóvel.
  * `polygon`: Polígono geográfico do imóvel.
  * `strata`: Classificação de estrato do imóvel.
  * `holiday`: Nome do feriado (ou "Dia Normal").
  * `holiday_type`: Tipo de feriado (ou "Dia Normal").
  * `climate_type`: Tipo de clima associado ao imóvel.
  * `tipo_dia`: "Dia de Semana" ou "Final de Semana".
  * `antecedencia_cat`: Categoria da antecedência (`0-15 dias`, `16-60 dias`, `61+ dias`).
  * `acquisition_date`: Data em que o dado foi processado (formato YYYY-MM-DD).

## **6. Tratamento de Erros e Monitoramento**

O mecanismo de tratamento de erros é robusto, garantindo que falhas sejam rapidamente identificadas.

* **Captura:** Um bloco `try...except Exception` envolve a lógica principal da função `main`.
* **Formatação:** Em caso de erro, o traceback completo é capturado usando o módulo `traceback`.
* **Notificação:** Um payload JSON formatado em Markdown é enviado para a `WEBHOOK_URL` configurada. A mensagem inclui:
  * Nome da função que falhou.
  * Mensagem da exceção.
  * O traceback completo do erro.
* **Resposta:** A Cloud Function retorna um código de status HTTP `500` para indicar a falha na execução.