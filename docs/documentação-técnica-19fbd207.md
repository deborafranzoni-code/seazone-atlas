<!-- title: Documentação Técnica | url: https://outline.seazone.com.br/doc/documentacao-tecnica-1XZpLpnx3A | area: Tecnologia -->

# Documentação Técnica

## Bibliotecas Utilizadas


Ambos os scripts utilizam um conjunto comum de bibliotecas para realizar suas funções, desde a manipulação de dados até a comunicação com serviços da AWS e Google Cloud, e tratamento de erros.


#### # Bibliotecas Principais


* **pandas**: Essencial para a manipulação e análise de dados. É utilizada para criar e operar DataFrames, que são a estrutura central de dados em todo o processo.
* **awswrangler**: Facilita a interação com serviços da AWS, sendo a principal ferramenta para a execução de consultas no Athena, integrando o poder do pandas com o ecossistema de dados da AWS.
* **boto3**: O SDK da AWS para Python, utilizado para criar e gerenciar a sessão com a AWS, permitindo que a aplicação interaja de forma segura com os serviços da nuvem.
* **requests**: Utilizada para enviar notificações de erro detalhadas para um webhook, garantindo que qualquer falha na execução seja comunicada à equipe de desenvolvimento.
* **gcsfs**: Fornece uma interface para interagir com o Google Cloud Storage (GCS), permitindo que os scripts leiam e escrevam arquivos (como Parquet) diretamente nos buckets.


#### # Módulos e Funções Específicas


* **os**: Utilizada para acessar variáveis de ambiente de forma segura, como credenciais da AWS e URLs de webhooks.
* **traceback**: Empregada para capturar e formatar as informações completas de exceções (stack trace), permitindo um *logging* de erro detalhado e eficaz.
* **functions_framework**: Framework do Google Cloud Functions que permite que as funções Python sejam acionadas por eventos, como requisições HTTP.
* **datetime**: Utilizada para manipulações de data e hora, cruciais para definir as janelas de análise, calcular antecedências (*lead times*) e particionar dados históricos.
* **numpy**: Usada para operações numéricas eficientes, como o cálculo de `np.ceil` para arredondamento de limiares de alerta.


## *Conceito Geral e Ambiente de Execução*


Os scripts `send-internals-peak-demand` e `send-competitors-peak-demand` são duas automações complementares de monitoramento de mercado, projetadas para identificar e sinalizar períodos de alta demanda (picos) para os imóveis da Seazone. Cada script aborda a detecção de picos a partir de uma perspectiva diferente: um olhando para os dados internos e o outro para o comportamento do mercado externo (concorrentes).

Ambas as automações são implementadas como **Cloud Functions** no ambiente da **Google Cloud Platform (GCP)**. Elas se conectam a bancos de dados e *data lakes* hospedados na **AWS (via Athena)** para coletar os dados necessários e, ao final do processamento, armazenam os resultados em formato Parquet no **Google Cloud Storage (GCS)**.

* `**send-internals-peak-demand**`:
  * **Objetivo**: Detectar picos de demanda com base na **velocidade de novas reservas internas** da Seazone.
  * **Justificativa**: Um aumento súbito no número de reservas para uma data futura específica é um forte indicador de demanda orgânica. Identificar isso cedo permite ajustar os preços para cima antes que o mercado reaja, maximizando a receita em datas que se tornam populares inesperadamente (ex: por causa de um evento local não mapeado).
* `**send-competitors-peak-demand**`:
  * **Objetivo**: Detectar picos de demanda analisando a **taxa de ocupação dos concorrentes** em datas futuras.
  * **Justificativa**: Muitas vezes, o mercado sinaliza uma alta demanda antes que a Seazone receba um volume significativo de reservas. Se os concorrentes estão ficando sem disponibilidade para uma data futura, isso indica uma oportunidade para a Seazone se posicionar com preços mais estratégicos. Essa função protege contra o risco de estar com preços muito baixos em períodos de alta procura.


---


## Análise de Picos de Demanda Interna (`send-internals-peak-demand`)


Esta função é responsável por identificar picos de demanda ao monitorar o volume de reservas recém-criadas para datas futuras, servindo como um "termômetro" do interesse orgânico nos imóveis da Seazone.


### Lógica de Funcionamento Detalhada


O processo é executado em etapas bem definidas, desde a coleta de dados até o armazenamento do alerta.


1. **Conexão e Extração de Dados**:
   * A função inicia estabelecendo uma sessão com a AWS usando `boto3`.
   * Uma consulta é executada no Athena (`get_reservations_data`) para buscar todas as reservas da Seazone realizadas no último ano.
2. **Pré-processamento e Cálculo de Capacidade**:
   * Os dados brutos são limpos e preparados (`prepare_reservations_data`), convertendo colunas de data e calculando o *lead time* (diferença entre a data de criação e o check-in).
   * A capacidade de cada região (polígono) é calculada (`calculate_and_prepare_polygon_capacity`), contando o número de imóveis únicos. Os polígonos são então classificados em faixas de capacidade (ex: "3-10 unidades", ">30 unidades"), o que é crucial para a definição de limiares de alerta dinâmicos.
3. **Detecção de Sobreposição (Lógica Principal)**:
   * A função filtra as reservas para analisar apenas aquelas criadas em uma janela de tempo recente (definida por `CREATION_WINDOW_DAYS`, geralmente 3 dias).
   * Para cada polígono, a função `get_overlapping_stay_dates_counts` "explode" os períodos de estadia dessas novas reservas em dias individuais e conta quantas se sobrepõem em cada data futura.
   * A função `check_alerts_type_1_v2` compara essa contagem de sobreposição com uma matriz de limiares (`ALERT_THRESHOLDS_V2`). O limiar a ser usado depende de dois fatores:
     * **Faixa de Capacidade** do polígono.
     * **Faixa de Antecedência** da data do pico (ex: "35-60 dias", "91+ dias").
   * Se a contagem de reservas sobrepostas para uma data excede o limiar correspondente, um alerta é gerado.
4. **Validação com Dados de Concorrentes**:
   * Para cada pico interno detectado, uma nova consulta (`get_competitors_poligon_occupancy`) é feita para buscar a taxa de ocupação dos concorrentes naquela mesma data.
   * É aplicado um filtro de relevância (`add_and_filter_by_occupancy`): **um alerta de pico interno só é mantido se a ocupação dos concorrentes para aquele período for de, no mínimo, 20%**. Isso valida o sinal, garantindo que não se trata de um acaso, mas de um movimento real de mercado.
5. **Agrupamento e Formatação Final**:
   * As datas individuais com alertas validados são agrupadas em períodos contínuos pela função `aggregate_and_format_alerts_v2`. Isso transforma múltiplos alertas diários (ex: 10/12, 11/12, 12/12) em um único alerta de período ("de 2025-12-10 a 2025-12-12"), tornando a visualização mais limpa.
   * Os alertas são enriquecidos com dados de feriados, se aplicável.
6. **Armazenamento e Tratamento de Erros**:
   * O DataFrame final de alertas é salvo em formato Parquet no Google Cloud Storage em dois locais: um para o estado atual (`state=current`) e outro para o histórico, particionado por dia (`state=historic`).
   * Se qualquer erro ocorrer, um traceback detalhado é enviado para o webhook de desenvolvimento.


### Funções Auxiliares Principais


* `**check_alerts_type_1_v2(...)**`: Implementa a lógica central de detecção, comparando a sobreposição de reservas recentes com limiares dinâmicos.
* `**get_overlapping_stay_dates_counts(...)**`: Calcula a contagem de reservas simultâneas para cada dia futuro, sendo o motor da detecção.
* `**add_and_filter_by_occupancy(...)**`: Valida os picos internos com dados de mercado, aplicando o filtro de 20% de ocupação dos concorrentes.
* `**aggregate_and_format_alerts_v2(...)**`: Agrupa dias de alerta consecutivos e formata a saída final para armazenamento.


### Saída


O resultado final são arquivos **Parquet** armazenados no Google Cloud Storage, contendo a lista de polígonos e períodos com picos de demanda interna validados.


---


## Análise de Picos de Demanda dos Concorrentes (`send-competitors-peak-demand`)


Esta função atua como um sistema de alerta precoce, identificando picos de demanda futuros através da análise estatística da ocupação do mercado de concorrentes.


### Lógica de Funcionamento Detalhada



1. **Coleta de Dados Iniciais**:
   * A função obtém a lista de todos os *listings* de concorrentes ativos e mapeados (`get_active_polygon_listings`).
   * Define-se uma janela de análise futura (por padrão, de 90 a 150 dias a partir da data atual).
2. **Detecção Estatística de Picos por Polígono**:
   * A função itera sobre cada polígono e executa o `pipeline_picos_por_poligono`.
   * Dentro do pipeline, é consultada a ocupação diária dos concorrentes para a janela de análise futura (`get_polygon_occupancy_interval`).
   * A função `detectar_picos` aplica uma análise estatística.
     * Cada dia é classificado de acordo com esses limiares.
3. **Filtragem e Validação Cruzada**:
   * **Filtro de Relevância**: Os picos detectados são filtrados para remover dias que são feriados conhecidos ou que possuem baixa liquidez (menos de 20 *listings* ativos).
   * **Filtro de Oportunidade**: É realizada uma consulta (`get_seazone_reservation`) para obter todas as datas em que a Seazone possui pelo menos uma reserva. Os picos de concorrentes são cruzados com essas datas (`INNER JOIN`). **Isso garante que os alertas sejam gerados apenas para mercados e períodos onde a Seazone já tem presença**, focando em oportunidades acionáveis.
4. **Supressão de Alertas Repetidos e Agrupamento**:
   * A análise foca apenas nos alertas de "Pico Forte".
   * A função `filtrar_alertas_repetidos` lê os alertas gerados no dia anterior e os compara com os atuais. Um alerta para o mesmo polígono e período só é reenviado se a taxa de ocupação tiver **aumentado em mais de 45%**. Isso evita a notificação diária sobre o mesmo evento, a menos que ele esteja se intensificando.
   * Os alertas que passam pelo filtro de repetição são agrupados em períodos contínuos pela função `agrupar_periodos`.
5. **Armazenamento e Tratamento de Erros**:
   * O DataFrame final, contendo apenas alertas novos ou intensificados, é salvo em formato Parquet no Google Cloud Storage (nos diretórios `state=current` e `state=historic`).
   * Qualquer falha no processo resulta no envio de uma notificação de erro para o webhook.


### Funções Auxiliares Principais


* `**detectar_picos(...)**`: O núcleo da análise, que usa média e desvio padrão para identificar estatisticamente os dias com ocupação anômala.
* `**pipeline_multiplos_poligonos(...)**`: Orquestra a execução da análise para todos os polígonos, aplicando os filtros iniciais.
* `**filtrar_alertas_repetidos(...)**`: Lógica de supressão que compara os alertas atuais com os do dia anterior para evitar notificações redundantes.
* `**agrupar_periodos(...)**`: Consolida dias de pico consecutivos em um único registro de período.


### Saída


O resultado final são arquivos **Parquet** armazenados no Google Cloud Storage, contendo a lista de polígonos e períodos futuros que apresentam picos de demanda de concorrentes e que representam uma oportunidade para a Seazone.

\n

## Cruzamento e Limpeza de Sinais de Demanda (`clean-peak-demand`)

Esta função atua como uma etapa intermediária, pegando os alertas brutos gerados anteriormente, cruzando as informações para adicionar contexto e salvando uma versão limpa e enriquecida dos dados.

**Lógica de Funcionamento Detalhada**

Carregamento de Dados Brutos:

A função inicia lendo os dois arquivos Parquet gerados pela etapa anterior (picos internos e picos de concorrentes) diretamente do GCS.

Expansão de Períodos ("Explode"):

Os alertas brutos vêm em períodos (ex: "2025-12-10 a 2025-12-15"). Para poder comparar os dois conjuntos de dados dia a dia, a função explode é utilizada para transformar cada linha de período em múltiplas linhas, uma para cada data individual.

Cruzamento de Sinais:

É feito um merge entre os dados internos (já explodidos) e os dados dos concorrentes (também explodidos).

Usando o parâmetro indicator=True, a função cria uma nova coluna, competitor_same_day, que marca "sim" para cada data de pico interno que também corresponde a uma data de pico de concorrente no mesmo polígono.

O processo é repetido na direção oposta, criando a coluna same_internal_date nos dados dos concorrentes.

Reagrupamento Inteligente de Períodos:

Após o cruzamento diário, os dados precisam ser agrupados de volta em períodos. A função agrupar_periodos_com_precedencia faz isso de forma inteligente:

Ela agrupa novamente as datas consecutivas para formar os intervalos.

Durante o agrupamento, ela aplica uma regra de precedência: se pelo menos um dia dentro de um período agrupado foi marcado com "sim" no cruzamento, o período inteiro herda a marcação "sim". Isso garante que o sinal de sobreposição não seja perdido.

Armazenamento dos Dados Limpos:

Os dois DataFrames finais, agora enriquecidos com as colunas de validação (competitor_same_day e same_internal_date), são salvos em formato Parquet em um novo diretório no GCS (peak-demand-clean), prontos para serem consumidos pela API.

### Funções Auxiliares Principais

explode(...): Transforma os períodos de datas em registros diários, sendo a etapa preparatória crucial para o cruzamento de dados.

agrupar_periodos_com_precedencia(...): Agrupa os registros diários de volta em períodos contínuos, garantindo que a informação de sobreposição seja preservada no período agregado.

### Saída

O resultado final são dois novos arquivos Parquet no Google Cloud Storage, contendo os alertas internos e de concorrentes, agora com uma coluna adicional em cada um indicando se há um alerta correspondente no outro conjunto de dados para o mesmo período.

## API de Notificação e Gestão de Alertas (`api-peak-demand`)

Esta função é o ponto final do fluxo, responsável por interagir com o usuário (via API), filtrar alertas já tratados e notificar a equipe sobre as pendências.

### Lógica de Funcionamento Detalhada

Gatilho e Entrada de Dados:

A função é acionada por uma requisição HTTP POST. Ela espera receber um payload JSON contendo duas listas de IDs (internal e competitor), que representam os alertas que já foram analisados e tratados pela equipe (provavelmente a partir de uma planilha ou outra interface de gestão).

Carga dos Alertas Ativos:

A função se conecta ao BigQuery e carrega as tabelas completas de picos de demanda internos e de concorrentes, que servem como a "fonte da verdade" de todos os alertas gerados.

Filtragem de Alertas Tratados:

Esta é a lógica central de gestão. A função utiliza os IDs recebidos no payload para filtrar os DataFrames carregados do BigQuery.

A lógica \~(job_internal\['id'\].isin(internal\['id'\])) remove todas as linhas cujos IDs foram informados, resultando em dois novos DataFrames que contêm apenas os alertas que ainda estão ativos e pendentes de análise.

Notificação no Slack:

A função _send_slack_alert é chamada com os DataFrames de alertas pendentes.

Ela formata os dados, renomeando as colunas para português e selecionando as mais relevantes.

Dois arquivos CSV são gerados em memória e enviados para dois canais distintos no Slack: um para picos internos e outro para picos de concorrentes.

A mensagem no Slack inclui um resumo, um link para a planilha de gestão e o link para download do CSV completo com os alertas ativos.

Atualização do Estado no GCS:

Os DataFrames com os alertas pendentes (já filtrados) são salvos de volta no GCS, substituindo os arquivos em state=current e adicionando ao histórico em state=historic. Isso garante que o estado do sistema seja atualizado para a próxima execução.

### Funções Auxiliares Principais

upload_and_message_internal(...) e upload_and_message_competitor(...): Funções especializadas que cuidam de todo o processo de comunicação com o Slack: formatam os dados, fazem o upload do arquivo CSV e postam a mensagem no canal correto.

_send_slack_alert(...): Orquestra o processo de notificação, chamando as funções de upload para cada tipo de alerta.

### Saída

Primária: Duas mensagens postadas em canais específicos do Slack, cada uma com um resumo e um arquivo CSV anexado contendo apenas os alertas de pico de demanda ainda ativos.

Secundária: Arquivos Parquet atualizados no Google Cloud Storage, refletindo a nova lista de alertas pendentes.

## Serviços do Google Apps Script Utilizados

Este conjunto de scripts opera inteiramente dentro do ecossistema do Google Workspace e utiliza os seguintes serviços nativos para interagir com a planilha e serviços externos:

SpreadsheetApp: É o serviço central, utilizado para obter acesso à planilha ativa, selecionar abas (Sheets) por nome, definir e ler valores de células e intervalos (Ranges), e obter informações sobre a estrutura da planilha, como a última coluna.

UrlFetchApp: Utilizado para realizar chamadas HTTP. Neste caso, é o responsável por se comunicar com a API externa no Google Cloud Platform, enviando os dados dos alertas que foram tratados.

Triggers Simples (Simple Triggers): O script utiliza o gatilho onEdit(e), uma função especial do Apps Script que é executada automaticamente sempre que um usuário modifica o valor de qualquer célula na planilha. Ele é o motor da automação de arquivamento.

Logger: Usado para fins de depuração. As saídas de Logger.log() podem ser visualizadas no editor de scripts para verificar o comportamento da API e outras variáveis durante a execução.

### Conceito Geral e Ambiente de Execução

Este código é um Google Apps Script projetado para ser executado no ambiente de uma Planilha Google específica, que funciona como a interface de gestão e ação para todo o pipeline de Picos de Demanda. Enquanto os scripts em Python no GCP cuidam da geração, limpeza e notificação inicial dos alertas, este script transforma a planilha em uma ferramenta interativa para a equipe de precificação.

O fluxo de trabalho que este script viabiliza é o seguinte:

Recebimento de Alertas: As abas "Alertas_Internos_Ativos" e "Alertas_Externos_Ativos" são populadas diariamente pelo script api-peak-demand, que envia um CSV para o Slack. A equipe copia e cola (ou importa) esses dados para a planilha.

Análise e Ação Humana: Um analista de precificação revisa os alertas ativos na planilha. Para cada alerta, ele realiza uma ação (ex: ajusta o preço no sistema, bloqueia datas) e preenche uma coluna de "Status" (ex: "Preço ajustado em +15%").

Arquivamento Automático: Ao final da análise de uma linha, o analista marca uma caixa de seleção (checkbox). A função onEdit detecta essa ação instantaneamente e, se a coluna de status estiver preenchida, copia a linha inteira da aba "Ativos" para a respectiva aba "Arquivado".

Fechamento do Ciclo: Periodicamente (de forma manual ou com um gatilho de tempo), a função enviarDadosParaGCP é executada. Ela coleta todos os alertas das abas "Arquivado" e os envia de volta para a api-peak-demand. A API, ao receber essa lista, saberá quais alertas já foram tratados e não os incluirá nas próximas notificações, "limpando" a lista de pendências.

Em resumo, este script operacionaliza os dados, criando um ciclo de feedback entre a análise automatizada e a intervenção humana.

### Automação da Planilha de Picos de Demanda (Google Apps Script)

Esta automação é responsável por facilitar o trabalho do analista, automatizando o processo de arquivamento e sincronizando o status dos alertas tratados com o backend no GCP.

### Lógica de Funcionamento Detalhada

Gatilho de Edição ([código.gs](http://xn--cdigo-0ta.gs) -> onEdit):

Esta é a função principal que dispara a automação. Sempre que qualquer célula da planilha é editada, ela é acionada.

Ela atua como um "despachante", chamando imediatamente as funções enviarcompetitor(e) e enviarinternal(e) para verificar se a edição corresponde a uma ação de arquivamento.

Movimentação de Alertas ([internal.gs](http://internal.gs) e [competitor.gs](http://competitor.gs)):

As funções enviarinternal e enviarcompetitor contêm lógicas idênticas, mas apontam para abas e colunas diferentes.

Verificação de Contexto: A função primeiro verifica se a edição ocorreu na aba correta ("Alertas_Internos_Ativos" ou "Alertas_Externos_Ativos") e na coluna específica da caixa de seleção (coluna 15 para internos, 11 para externos). Se não, a função para imediatamente.

Validação da Ação: Em seguida, ela verifica duas condições para prosseguir:

O valor da caixa de seleção deve ser true (marcada).

O valor da célula de "Status" adjacente não pode estar vazio. Isso força o analista a registrar a ação tomada antes de arquivar o alerta.

Cópia para Arquivamento: Se todas as condições forem atendidas, a função lê a linha inteira que foi marcada e a anexa (appendRow) ao final da aba de arquivamento correspondente ("Alertas_Internos_Arquivado" ou "Alertas_Externos_Arquivado").

Nota: O script não apaga a linha da aba "Ativos". A remoção da lista de pendências é gerenciada pelo backend na próxima vez que a api-peak-demand for executada, após receber a lista de itens arquivados.

Sincronização com o Backend ([código.gs](http://xn--cdigo-0ta.gs) -> enviarDadosParaGCP):

Esta função é projetada para ser executada manualmente (através do menu de scripts) ou por um gatilho de tempo (ex: uma vez por dia).

Ela lê o conteúdo completo das duas abas de arquivamento ("...Arquivado").

Converte os dados de cada aba para o formato JSON, que é o formato esperado pela API.

Monta uma requisição HTTP POST, incluindo o payload JSON e a chave de API (x-api-key) no cabeçalho para autenticação.

Envia os dados para o endpoint da api-peak-demand no GCP e registra a resposta para fins de depuração.

Função Utilitária ([código.gs](http://xn--cdigo-0ta.gs) -> limparColunasJKL):

Uma função de manutenção simples que limpa o conteúdo de colunas específicas nas abas de alertas ativos. Sua finalidade provável é limpar colunas de preenchimento manual (como Status e a caixa de seleção) caso seja necessário reiniciar a análise de um lote de alertas.

### Detalhamento dos Arquivos e Funções

[código.gs](http://xn--cdigo-0ta.gs):

onEdit(e): O ponto de entrada da automação de arquivamento. Dispara com qualquer edição na planilha.

enviarDadosParaGCP(): A função que "fecha o ciclo", enviando os IDs dos alertas tratados de volta para o backend para que eles sejam removidos das futuras notificações.

limparColunasJKL(): Ferramenta de apoio para a limpeza manual de dados na planilha.

[internal.gs](http://internal.gs):

enviarinternal(e): Gerencia especificamente o arquivamento de alertas da aba Alertas_Internos_Ativos. Verifica a coluna 15 (O) para a caixa de seleção e a coluna 14 (N) para o status.

[competitor.gs](http://competitor.gs):

enviarcompetitor(e): Gerencia o arquivamento de alertas da aba Alertas_Externos_Ativos. Verifica a coluna 11 (K) para a caixa de seleção e a coluna 10 (J) para o status.

### Saída

Ação Primária: Linhas de dados são copiadas das abas "Ativos" para as abas "Arquivado" dentro da própria Planilha Google em tempo real, conforme o analista marca as caixas de seleção.

Ação Secundária: Um payload JSON é enviado para uma API no GCP quando a função enviarDadosParaGCP é executada, contendo todos os alertas que foram arquivados desde a última sincronização.