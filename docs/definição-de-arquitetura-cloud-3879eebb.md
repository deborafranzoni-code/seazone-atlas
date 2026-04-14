<!-- title: Definição de Arquitetura Cloud | url: https://outline.seazone.com.br/doc/definicao-de-arquitetura-cloud-vEzLMTj8BR | area: Tecnologia -->

# Definição de Arquitetura Cloud

O diagrama completo pode ser visualzado [aqui](https://miro.com/app/board/uXjVLItK9Eo=/)

## 1. Introdução: 


Esta seção descreve a arquitetura técnica do sistema Meta 2.0 implementada na Google Cloud Platform (GCP). A arquitetura foi projetada para ser escalável, automatizada e de fácil manutenção, utilizando serviços gerenciados da GCP para processamento, armazenamento e apresentação dos dados.


## 2. **Visão Geral da Arquitetura**

* **Data Lake (AWS):** Fonte de dados brutos, contendo informações de imóveis da Seazone e de concorrentes. Os dados são acessados via AWS Athena ou Google BigQuery (dependendo da localização e formato dos dados).
* **Workflows (GCP):** Orquestrador das etapas de processamento, responsável por iniciar e coordenar as Cloud Functions.
* **Cloud Functions (GCP):** Funções serverless que executam a lógica de cálculo das metas (mensais e trimestrais).
* **Cloud Storage (GCP):** Armazenamento de dados intermediários e resultados ("congelados") do cálculo das metas.
* **BigQuery (GCP):** Data warehouse para armazenamento e consulta eficiente dos dados processados.
* **App Script (Google Sheets):** Script responsável por acionar o cálculo das metas, obter os resultados e atualizar a planilha Google Sheets.
* **API Gateway (AWS):** Interface para o App Script se comunicar com as Cloud Functions.
* **Planilha Google Sheets (Meta 2.0):** Interface de usuário final para visualização e análise dos resultados.


## **3. Diagrama do Data Lake (AWS)**


* ![](/api/attachments.redirect?id=dc03191f-7656-4111-a8d8-06155d6e027f " =810x345")


O diagrama acima ilustra as tabelas relevantes no data lake (AWS) que servem como fonte de dados para o cálculo das metas. As tabelas, localizadas nas contas Sirius e PRD-LAKE da AWS, incluem:

* daily_revenue_sapron: Contém dados diários de bloqueios de imóveis da Seazone (fonte: Sapron).
* sapron_monthly_fat: Contém o faturamento mensal consolidado dos imóveis da Seazone (fonte: Sapron closing_property_resume, *sem* taxa de limpeza e *com* taxa de OTA).
* listing_status: Informações sobre o status de ativação/inativação dos imóveis Seazone.
* setup_groups: Tabela de configuração que relaciona imóveis Seazone a grupos/categorias.
* competitors_plus: Informações sobre os imóveis concorrentes.
* daily_revenue_competitors: Dados de faturamento diário dos imóveis concorrentes.


* Diagrama da estrutura de calculo referentes a M0, M1 e M2


## **4. Diagrama do Cálculo Mensal (M+0, M+1, M+2) - GCP**


 ![](/api/attachments.redirect?id=262c689c-257f-4275-8589-16687e826938 " =891x660")


**Descrição:**

* **Cloud Scheduler:** Agendador que inicia o processo automaticamente às 4:15 AM (horário a ser confirmado, e idealmente, configurável).
* **Workflows:** Orquestrador que gerencia a execução das Cloud Functions para o cálculo das metas mensais.
* **Cloud Functions (M+0, M+1, M+2):** Funções serverless, executadas em paralelo, responsáveis por calcular as metas para o mês corrente (M+0), o próximo mês (M+1) e o mês subsequente (M+2). Cada função:
  * Recebe como entrada o mês de referência para o cálculo.
  * Realiza consultas (queries) no data lake (usando boto3 + Athena).
  * Aplica as regras de negócio (definidas em documento separado) para calcular as metas.
  * Gera dois outputs:
    * **Dados Congelados (Cloud Storage):** Dados intermediários "congelados" do cálculo da meta, para auditoria e para uso no cálculo trimestral. Armazenados no Cloud Storage em formato adequado (ex: Parquet).
    * **Output Mensal (Cloud Storage):** Resultado final do cálculo da meta mensal, formatado para ser inserido na planilha. Armazenado no Cloud Storage.
* **Big Query:** O output de cada cloud function alimenta a tabela no bigquery, onde ficam os dados que podem ser consultados via Looker Studio, na camada de auditoria.


## **5. Diagrama do Cálculo Trimestral (Normal e Confirmado) - GCP**


 ![](/api/attachments.redirect?id=58b5193f-6274-484f-948d-ad0b3e65630a " =1020x525")


* **Cloud Function (Trimestre):**
  * Lê os dados "congelados" do Cloud Storage (output dos cálculos mensais).
  * Calcula a meta trimestral com base nos dados mensais já processados. *Não acessa diretamente o data lake*.
  * Salva o resultado no Cloud Storage (Output Trimestral).
  * Salva o resultado no BigQuery (Output Trimestral).
* **Cloud Function (Trimestre Confirmado):**
  * Consulta o data lake (boto3 + Athena) para obter o faturamento diário *até o dia anterior* à execução (D-1).
  * Calcula a meta trimestral "confirmada", que reflete o faturamento acumulado até o dia anterior.
  * Salva o resultado no Cloud Storage (Output Trimestral Confirmado).
  * Salva o resultado no BigQuery (Output Trimestral Confirmado).


## **6. Diagrama da Conexão GCP - Planilha**


 ![](/api/attachments.redirect?id=20f4fc5d-8133-44c6-9f42-a13c67c78f44)


**Descrição:**

* **Trigger (Agendamento):** Um gatilho (trigger) é configurado no App Script para executar diariamente entre 5:00 AM e 6:00 AM.
* **App Script:** O App Script faz uma requisição para a API Gateway (GCP).
* **API Gateway:** A API Gateway aciona a Cloud Function apropriada para obter o resultado do cálculo da meta.
* **Cloud Function (Pegar Resultado):** Esta função lê os dados do BigQuery (Output Mensal, Output Trimestral, Output Trimestral Confirmado).
* **Planilha Meta 2.0:** O App Script recebe os dados da Cloud Function e atualiza a planilha Meta 2.0 com os resultados.


## **7. Considerações Adicionais:**

* **Monitoramento e Tratamento de Erros:** *Importante:* O sistema atual **não possui alertas de erro no Slack**. É crucial implementar um sistema de monitoramento e alertas (ex: Cloud Monitoring + integração com Slack) para identificar e corrigir rapidamente falhas no processo.( Esta em desenvolvimento )
* **Execução Manual:** Em caso de falhas, é possível executar manualmente o Workflow ou as Cloud Functions.
* **Documentação:** Todo o código (Python, App Script) e a configuração da arquitetura devem ser devidamente documentados.