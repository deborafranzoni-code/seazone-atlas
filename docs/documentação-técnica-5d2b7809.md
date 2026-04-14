<!-- title: Documentação Técnica | url: https://outline.seazone.com.br/doc/documentacao-tecnica-4tGN8AcBgz | area: Tecnologia -->

# Documentação Técnica

# 1. Visão Geral

O `get-min-stay-kpi` é um Cloud Function em Python executado na Google Cloud Platform (GCP). Sua principal finalidade é processar e consolidar dados de "Min Stay" (mínimo de estadia) de diversas fontes, gerar um conjunto de dados final em formato Parquet e armazená-lo no Cloud Storage. Posteriormente, esses dados são disponibilizados no BigQuery como a tabela `kpi_min_stay` dentro do dataset `infos`, servindo de base para o dashboard de validação de Min Stay.

# 2. Gatilho e Agendamento

* **Scheduler:** `kpi-min-stay-schedule`
* **Frequência:** Diária
* **Horário de Execução:** 09:00 (9 AM)

# 3. Componentes e Tecnologias Envolvidas

* **Google Cloud Platform (GCP):**
  * **Cloud Functions:** `get-min-stay-kpi` (função serverless que executa o código Python).
  * **Cloud Scheduler:** `kpi-min-stay-schedule` (para agendar a execução do Cloud Function).
  * **Cloud Storage:** Armazena os arquivos Parquet gerados pelo script.
  * **BigQuery:** Armazena a tabela final `kpi_min_stay` (`infos.kpi_min_stay`) para consumo pelo dashboard.
* **Amazon Web Services (AWS):**
  * **S3:** `api-stays-bucketsheetscommunication-f9kp5bcv1kq0` (bucket de origem para os dados de Min Stay).
  * **Athena:** `pricingdata-pzprucbusfet` (banco de dados de onde são extraídas as datas de ofertas).
* **Python Libraries:**
  * `os`: Para interagir com variáveis de ambiente.
  * `boto3`: AWS SDK para Python, utilizado para interagir com S3 e Athena.
  * `gcsfs`: Sistema de arquivos para Google Cloud Storage, usado para escrever Parquet no GCS.
  * `requests`: Para fazer requisições HTTP (enviar notificações para o webhook).
  * `traceback`: Para obter informações detalhadas de erros.
  * `pandas`: Para manipulação e análise de dados.
  * `awswrangler`: Biblioteca Python para integração entre Pandas e AWS (S3, Athena, etc.).
  * `functions_framework`: Framework para o Cloud Functions.
  * `datetime`: Para manipulação de datas e horas.

# 4. Variáveis de Ambiente

As seguintes variáveis de ambiente devem ser configuradas para o Cloud Function:

* `AWS_ACCESS_KEY_ID`: Chave de acesso AWS para autenticação.
* `AWS_SECRET_ACCESS_KEY`: Chave secreta AWS para autenticação.
* `DEV_WEBHOOK_URL`: URL do webhook para notificações de erro (canal de Slack).

# 5. Fluxo de Execução do Código (`main` function)


1. **Inicialização da Sessão AWS:**
   * Uma sessão `boto3` é criada usando as credenciais AWS configuradas nas variáveis de ambiente, com a região `us-west-2`.

     \
2. **Coleta de Dados de Min Stay:**
   * `get_min_stay_period(session)`:
     * Lê dados de Min Stay por período do S3 (`s3://api-stays-bucketsheetscommunication-f9kp5bcv1kq0/inputs/min_stay_period/state=current/`).
     * Expande os intervalos de `start_date` e `end_date` em datas individuais.
     * Adiciona a coluna `origin` com o valor 'Periodo'.
   * `get_dates(session)`:
     * Consulta o Athena (`pricingdata-pzprucbusfet.last_offered_raw_price`) para obter IDs de imóveis e datas futuras (`date >= current_date`).
     * Calcula o dia da semana (`weekday`) e o mês (`month`) para cada data.
   * `get_min_stay_weekdays(dates, session)`:
     * Lê dados de Min Stay por dia da semana do S3 (`s3://api-stays-bucketsheetscommunication-f9kp5bcv1kq0/inputs/min_stay_weekdays/state=current/`).
     * Transforma a estrutura (melt) para ter uma linha por `weekday`.
     * Agrupa e calcula o `min_stay` máximo por imóvel, dia da semana e nível de grupo.
     * Mescla com o dataframe `dates` para associar as datas aos dias da semana e imóveis.
     * Adiciona a coluna `origin` com o valor 'Dias da Semana'.
   * `get_min_stay_months(dates, session)`:
     * Lê dados de Min Stay por mês do S3 (`s3://api-stays-bucketsheetscommunication-f9kp5bcv1kq0/inputs/min_stay_month/state=current/`).
     * Agrupa e calcula o `min_stay` máximo por imóvel, mês e nível de grupo.
     * Mescla com o dataframe `dates` para associar as datas aos meses e imóveis.
     * Adiciona a coluna `origin` com o valor 'Mês'.
   * `get_min_stay_calendar(session)`:
     * Lê dados de Min Stay do calendário do S3 (`s3://api-stays-bucketsheetscommunication-f9kp5bcv1kq0/inputs/min_stay_calendar/state=current/`).
     * Renomeia `advance_min_stay` para `min_stay`.
     * Agrupa e calcula o `min_stay` máximo por imóvel, data e nível de grupo.
     * Adiciona a coluna `origin` com o valor 'Calendário'.

       \
3. **Processamento e Consolidação dos Dados:**
   * `ignore_group_level`:
     * Identifica os registros de `min_stay_period` onde `ignore_group_level` é `True`.
     * Agrupa por `id_seazone` e `date` para obter o `group_level` mínimo que deve ser ignorado para aquele imóvel/data.
     * Renomeia a coluna `group_level` para `group_level_limit`.
   * **Concatenação:** Todos os dataframes de Min Stay (`min_stay_month`, `min_stay_weekdays`, `min_stay_period`, `min_stay_calendar`) são concatenados em um único dataframe `min_stay`.
   * **Aplicação de** `ignore_group_level`:
     * `min_stay` é mesclado com `ignore_group_level`.
     * Para registros onde há correspondência (`_merge == 'both'`) e o `group_level` atual é maior ou igual ao `group_level_limit`, o `group_level` é ajustado para o `group_level_limit`. Isso garante que configurações com um `group_level` "menos específico" (menor valor) sejam priorizadas ou sobrescritas por um `group_level` limitante.
   * **Criação de** `min_stay_all` (Não Aplicadas):
     * Uma cópia dos dados iniciais (`id_seazone`, `date`, `min_stay`, `origin`) é feita para `min_stay_all`. Essa cópia será usada para identificar as configurações de Min Stay que *não* foram aplicadas ao final do processo.
   * **Determinação do Min Stay Aplicado:**
     * Os dados de `min_stay` são filtrados para manter apenas as linhas onde o `group_level` é o mínimo para cada `(id_seazone, date)`. Isso seleciona a regra de Min Stay mais prioritária/específica para cada imóvel em cada data.
     * Os dados são ordenados por `id_seazone`, `date` e `min_stay`.
     * Agrupa-se por `id_seazone` e `date`, pegando o `min_stay` e `origin` "last" (o último após a ordenação), efetivamente selecionando a regra aplicada final.
   * **Classificação como "Aplicado" ou "Não Aplicado":**
     * `min_stay_all` é mesclado com o `min_stay` final.
     * Registros em `min_stay_all` que não foram encontrados em `min_stay` (indicador `_merge == 'left_only'`) são marcados como `'Não'` na coluna `applied`.
     * Os registros de `min_stay` final são marcados como `'Sim'` na coluna `applied`.
     * Os dois dataframes são concatenados para formar o resultado final.

       \
4. **Agrupamento e Consolidação de Períodos:**
   * O dataframe `min_stay` (já com a coluna `applied`) é processado para agrupar datas consecutivas com o mesmo `id_seazone`, `min_stay`, `origin` e `applied`.
   * Uma coluna `group` é criada para identificar esses blocos contínuos.
   * O dataframe `result` é gerado agrupando por `group`, `id_seazone`, `min_stay`, `origin` e `applied`, obtendo as datas `start_date` (mínima) e `end_date` (máxima) para cada bloco.
   * As colunas `start_date` e `end_date` são expandidas para criar uma linha para cada dia dentro do período, facilitando a visualização por dia no dashboard.
   * Uma coluna `acquisition_date` é adicionada com a data UTC atual da execução.

     \
5. **Armazenamento no Cloud Storage:**
   * Um objeto `gcsfs.GCSFileSystem` é inicializado para interagir com o Cloud Storage.
   * **Limpeza:** O diretório `gs://data-resources-448418/seazone-info/kpi/min-stay` é limpo recursivamente antes de salvar novos dados (para o `current`).
   * **Salvando "current":** O dataframe `result` é salvo como arquivo Parquet no caminho `gs://data-resources-448418/seazone-info/kpi/min-stay/current/min_stay.parquet`.
   * **Salvando "historic":** O dataframe `result` é salvo como arquivo Parquet no caminho `gs://data-resources-448418/seazone-info/kpi/min-stay/historic/`, com particionamento pela coluna `acquisition_date`.

     \
6. **Resposta e Tratamento de Erros:**
   * Em caso de sucesso, a função retorna "ok".
   * Em caso de erro, uma mensagem detalhada de erro, incluindo o traceback, é enviada para o `DEV_WEBHOOK_URL` configurado, e a função retorna a mensagem de erro com status 500.

# 6. Estrutura de Saída (Parquet / BigQuery)

O arquivo Parquet final e a tabela `kpi_min_stay` no BigQuery terão as seguintes colunas:

| Coluna | Tipo de Dados | Descrição |
|:---|:---|:---|
| `id_seazone` | String | Identificador único do imóvel. |
| `date` | Date | Data individual à qual a regra de Min Stay se aplica. |
| `start_date` | Date | Data de início do período contínuo da regra de Min Stay. |
| `end_date` | Date | Data de término do período contínuo da regra de Min Stay. |
| `min_stay` | Integer | O valor de mínimo de estadia aplicado. |
| `origin` | String | A origem da regra de Min Stay (ex: 'Calendário', 'Mês', 'Periodo', 'Dias da Semana'). |
| `applied` | String | Indica se a regra de Min Stay foi a "aplicada" final ('Sim') ou não ('Não') após a lógica de prioridade. |
| `acquisition_date` | Date | Data em que o dado foi processado e salvo (UTC). |
| `season` | String | Aponta a sazonalidade da região à qual o imóvel pertence dado o período observado (ex: 'Baixa temporada', 'Alta temporada'). |
| `climate_type` | String | Indica o clima da região à qual o imóvel pertence (ex: Região quente). |
| `occurence_day` | String | Indica se a data é dia de semana ou fim de semana. |
| `occurence` | String | Detalha a ocorrência no período observado (ex: Carnaval, Dia normal, Reveillon). |
| `observation` | String | Observações relacionadas ao gapper (ex: Condomínio não aceita estadia menor que 7). |
| `gapper` | Integer | Número de dias disponíveis entre datas com reservas. |

# 7. Dependências

Para a execução deste Cloud Function, as seguintes dependências devem ser especificadas no arquivo `requirements.txt`:

```
boto3
gcsfs
requests
pandas
awswrangler
functions-framework
google-cloud-bigquery
fsspec
pyarrow
```


\