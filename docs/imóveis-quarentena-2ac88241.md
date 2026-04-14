<!-- title: Imóveis quarentena | url: https://outline.seazone.com.br/doc/imoveis-quarentena-XhFHgE5Kn1 | area: Tecnologia -->

# Imóveis quarentena

# Documentação Técnica: `get-quarantine-listings`

## Objetivo Geral

A solução tem como objetivo monitorar o desempenho inicial de imóveis recém-ativados (em "quarentena"). O script identifica imóveis ativados nos últimos 30 dias e verifica se eles receberam alguma reserva dentro de janelas de 7, 15 e 30 dias a partir da data de ativação (as reservas podem ser em qualquer data do calendario, o que importa é a data de criação delas estarem nessa janela de tempo).

O resultado é um relatório que classifica cada imóvel com "Sim" ou "Não" para cada janela de tempo. Este relatório é enviado como um arquivo CSV para um canal do Slack e também é armazenado no Google Cloud Storage (GCS) em duas formas: um snapshot "current" (atual) e um "historic" (histórico particionado) para análises futuras.

## Funções presentes no projeto

| Nome da função | O que a função realiza |
|:---|:---|
| `**send_slack_alert(df: pd.DataFrame)**` | Envia um alerta para o canal de Slack configurado (SLACK_CHANNEL).* Renomeia as colunas do DataFrame para nomes em português (ex: 'Imóvel', 'Tem reserva em 7 dias?').
* Converte o DataFrame para um arquivo CSV em memória.
* Faz o upload deste CSV para o Slack usando a API files_upload_v2.
* Posta uma mensagem no canal contendo um link para o download do arquivo CSV. |
| `**necessary_data_query()**` | Extrai e prepara os dados de disponibilidade e ativação dos imóveis via AWS Athena.* Consulta 1: Busca na tabela listing_status (database saprondata-9dkamzx2grjg) os imóveis com status 'Active' e data de ativação (activation_date) nos últimos 90 dias.
* Consulta 2: Busca na tabela daily_revenue_sapron_active (database revenuedata-ljkritvzunqm) os dados diários de ocupação (blocked, occupied, available, creation_date) para todas as datas após hoje dos imóveis encontrados na consulta 1.
* Combina os resultados das duas consultas.
* Regra de Negócio (Correção): Garante que qualquer data anterior à activation_date de um imóvel seja marcada como blocked=True e available=False, corrigindo a disponibilidade histórica. |
| `**get_real_activation_date(**``**necessary_data)**` | Determina a "data de início" real para a contagem da quarentena (real_activation_date).* Calcula se todas as datas dentre hoje e 90 dias no futuro estão bloqueadas.
  * Se sim, então o imóvel fica com a data de ativação nula.
  * Caso contrário, então a data de ativação TALVEZ será HOJE.
  * Esses 90 dias veio de uma regra de negócio que o próprio RM passou para a gente.
* O script lê da tabela quarantine-listings-real-activation-date a última data de ativação dos imóveis.
  * Se o imóvel não tinha data de ativação, então é confirmado que a data de ativação é HOJE, ou seja, de ontem para hoje foram removidos os bloqueios então por isso que a data de ativação é hoje.
  * Se o imóvel já tinha data de ativação nessa tabela, então a data de ativação real permanece a que existia na tabela, visto que isso implica que o imóvel já havia sido desbloqueado alguns dias atrás. |
| `**check_reservations(final_df, df, days)**` | Função auxiliar que verifica se um imóvel teve reservas dentro de uma janela de tempo específica (days).* Verifica se pelo menos uma data teve reserva na janela de dias.
* Se sim, então edita o dataframe final_df com "Sim" ou "Não" na respectiva coluna de dias. |
| `**get_reservations_info(merged)**` | Compila o relatório final de reservas.* Cria um dataframe base com todos os listings chamado "final_df".
* Chama a função check_reservations três vezes, para janelas de 7, 15 e 30 dias. |
| `**main(request)**` | Ponto de entrada (entrypoint) da Google Cloud Function; orquestra todo o processo de ETL.* Executa a sequência de funções: necessary_data_query -> get_real_activation_date -> get_reservations_info (antes de executar a get_reservations_info, é removido imóveis ativados a mais de 30 dias atrás, visto que eles não entram no warning).
* O script salva as datas de ativação nas tabelas quarantine-listings-real-activation-date (usada para pegar a última data de ativação real) e quarantine-listings-real-activation-date-historical (possuí todo o histórico)
* Conecta-se ao Google Cloud Storage (GCS) usando gcsfs.
* Remove o arquivo de snapshot "current" anterior (CURRENT_PREFIX).
* Envia o novo relatório para o Slack via send_slack_alert.
* Salva o novo relatório (snapshot) como quarantine_listings.parquet no GCS (CURRENT_PREFIX).
* Adiciona a coluna acquisition_date (com a data atual) e anexa o relatório ao dataset histórico particionado no GCS (HISTORIC_PREFIX).
* Tratamento de Erro: Captura qualquer exceção (Exception), formata o traceback completo, envia um alerta de erro detalhado para o WEBHOOK_URL (Slack) e retorna um status HTTP 500. |

## Datasets Gerados (Google Cloud Storage)

O script gera dois datasets em formato Parquet no GCS.

### 1. Snapshot Atual

**Path:** `gs://seazone-info/quarantine-listings/state=current/`

**Descrição:** Armazena um único arquivo Parquet (`quarantine_listings.parquet`) que contém o *snapshot mais recente* do status de quarentena. Este arquivo é sobrescrito a cada execução.

| Nome do campo | Tipo | Descrição |
|:---|:---|:---|
| `listing` | STRING | Código do imóvel. |
| `days_7` | STRING | "Sim" ou "Não", indica se teve reserva nos primeiros 7 dias. |
| `days_15` | STRING | "Sim" ou "Não", indica se teve reserva nos primeiros 15 dias. |
| `days_30` | STRING | "Sim" ou "Não", indica se teve reserva nos primeiros 30 dias. |

### 2. Histórico Particionado

**Path:** `gs://seazone-info/quarantine-listings/state=historic/`

**Descrição:** Armazena o *histórico de todos os relatórios* gerados, sendo particionado por data. Cada execução anexa os dados do dia a este dataset.

| Nome do campo | Tipo | Descrição |
|:---|:---|:---|
| `listing` | STRING | Código do imóvel. |
| `days_7` | STRING | "Sim" ou "Não", indica se teve reserva nos primeiros 7 dias. |
| `days_15` | STRING | "Sim" ou "Não", indica se teve reserva nos primeiros 15 dias. |
| `days_30` | STRING | "Sim" ou "Não", indica se teve reserva nos primeiros 30 dias. |
| `acquisition_date` | DATE | Data da execução do script (usada como partição). |

### 3. Últimas Datas de Ativação

**Path:** `gs://seazone-info/quarantine-listings-real-activation-date/df.parquet`

**Descrição:** Possuí a última data de ativação usada na lógica da quarentena.

| Nome do campo | Tipo | Descrição |
|----|----|----|
| `listing` | STRING | Código do imóvel. |
| `count_datess` | INTEGER | Número de dias dentre hoje e 90 dias no futuro. (só é salvo para auditória) |
| `blocked_dates` | INTEGER | Número de dias bloqueados dentre hoje e 90 dias no futuro. (só é salvo para auditória) |
| `sapron_activation_date` | DATE | Data de ativação no Sapron. (só é salvo para auditória) |
| `real_activation_date` | DATE | Data de ativação real usada na lógica da quarentena. |

### 4. Histórico de Datas de Ativação

**Path:** `gs://seazone-info/quarantine-listings-real-activation-date-historical/`

**Descrição:** Mesmas colunas da "Últimas Datas de Ativação", mas essa tabela tem todas as aquisições particionadas por "acquisition_date" (data que o script rodou). É usada só para Auditória.

## Funcionalidades e Regras de Negócio

* **Monitoramento de Quarentena:** O objetivo principal é identificar se imóveis ativados nos últimos 30 dias estão conseguindo gerar tração (reservas) logo após sua ativação.
* **Janela de Análise:** Apenas imóveis cuja `real_activation_date` tenha ocorrido nos **últimos 30 dias** são incluídos no relatório.
* **Correção de Disponibilidade Histórica:** A lógica na função `necessary_data_query` é crucial. Ela força os dias anteriores à data de ativação de um imóvel como `blocked=True`, garantindo que os cálculos de "primeira disponibilidade" sejam precisos e não considerem datas em que o imóvel ainda não estava no sistema.
* **Notificação Proativa:** Um CSV completo é enviado ao Slack a cada execução, permitindo que o time responsável (ex: Revenue Management) tenha visibilidade imediata e possa tomar ações sobre os imóveis que não estão performando.
* **Persistência de Dados:** O sistema mantém dois conjuntos de dados no GCS:
  * **Current:** Um snapshot do último relatório, para consumo imediato (provavelmente por dashboards ou outras ferramentas).
  * **Historic:** Um log de todos os relatórios, particionado por data, para análises de tendência e performance histórica.

## Execução e Deploy

* **Plataforma:** O script é empacotado como uma **Google Cloud Function**, indicado pelo uso da biblioteca `functions_framework` e o decorador `@functions_framework.http`.
* **Trigger (Acionador):** Por ser uma função HTTP (`@functions_framework.http`), ela é acionada via requisição web. É provável que seja invocada por um serviço de agendamento, como o **Google Cloud Scheduler**, para execuções diárias.
* **Monitoramento de Erros:** O script possui um bloco `try...except` global. Qualquer falha durante a execução aciona um envio de mensagem para um `WEBHOOK_URL` do Slack, detalhando a mensagem de erro e o traceback completo. Isso permite que a equipe de desenvolvimento seja notificada imediatamente sobre falhas.


\