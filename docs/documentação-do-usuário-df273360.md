<!-- title: Documentação do Usuário | url: https://outline.seazone.com.br/doc/documentacao-do-usuario-FDxgugH2DK | area: Tecnologia -->

# Documentação do Usuário

# O que é o Dashboard de Observabilidade do Lake

É um painel de monitoramento que permite acompanhar, de forma centralizada, se os principais pipelines de dados do Lake estão:

* Executando corretamente;
* Atualizados dentro do esperado;
* Apresentando volumes e métricas consistentes.

O dashboard funciona como uma **torre de controle** do Lake, ajudando a identificar rapidamente problemas que podem impactar análises, modelos e decisões de negócio.

# Estrutura do Dashboard

## Visão Geral do Dashboard

O dashboard está organizado em três páginas principais, seguindo um fluxo de análise progressivo: do geral para o detalhado. 

## Página 1 — Visão Geral (Torre de Controle)

Voltada para leitura rápida e tomada de decisão imediata. O objetivo desta página é responder rapidamente à pergunta: *"Está tudo saudável hoje?"*

### Componentes

#### Topo da Página

==KPI de Saúde Global dos Scrapers:== Indica o status geral das execuções, mostrando a porcentagem (%) de execuções sem falhas no dia atual.

 ![](/api/attachments.redirect?id=d3fadcd9-f2ba-4ff8-b9f2-5317e84a14a5 " =128.5x43.5")

==Status de Execução dos Scrapers:== Visualização do número de scrapers com execução bem-sucedida versus falhas no período selecionado.

 ![](/api/attachments.redirect?id=6ba6e61a-b824-417c-ba6d-a516bed774a8 " =133.5x40.5")==OBS:== O período pode ser escolhido pelo usuário:

 ![](/api/attachments.redirect?id=a588f842-7291-44f2-a879-15447456902c " =305.5x186.5")

==Data de Última Atualização:== Informa qual a data mais recente de aquisição dos dados, auxiliando na identificação de atrasos de atualização dos dados. 


#### Restante da Página

==Gráfico de Execução das Base de Dados:== Esse gráfico é responsável por apontar o status de execução de cada base de dados dado o período desejado de observação, e apontat o número de execuções em que se obteve sucesso e o número de execuções em que se obteve falha. 

==OBS:== Por padrão, ele mostra os dados do dia atual.

 ![](/api/attachments.redirect?id=22881da0-57bb-496c-902a-303139864312 " =538x139")

Mas também é possível mudar o intervalo do período de visualização, por exemplo foi selecionado um intervalo de 30 dias:

 ![](/api/attachments.redirect?id=fa50c60c-5dfb-4fda-a499-5b81d088d58c " =538.5x135.5")

==Gráfico de Falha na Execução das Tabelas:== Fornece uma visualização mais granular, ao invés de focar nas bases de dados, foca mais especificamente nas tabelas. Ele mostra somente tabelas que possuíram falhas de execução nos últimos 30 dias. 

 ![](/api/attachments.redirect?id=20e360e0-65f3-4e1e-8c7e-ff8c3a6e8fc1 " =210.5x188.5")

==Tabela de Volumetria Crítica:== Compara o volume de linhas inseridas **Ontem vs Última Ingestão de Sucesso**, destacando automaticamente quedas/aumentos relevantes (ex.: variações maiores de +15% ou -15%).

 ![](/api/attachments.redirect?id=cf419e55-3a60-4c14-bba3-58479540e1bc " =865x198.5")

## Página 2 — Qualidade e Anomalias de Receita (MAPE)

Página focada em avaliar a **qualidade das métricas de receita**, utilizando o Mean Absolute Percentage Error (MAPE).

### Componentes

#### ==Componente de Janela:==  

Esse componente permite a visualização de dados no Gráfico "Mean Absolute Percentage Error (MAPE) de Receita ao Longo da Janela de Dias" considerando diferentes intervalos de tempo. No caso os possíveis intervalos são: Os últimos 30, 15 ou 7 dias. 

 ![Componente sem expansão](/api/attachments.redirect?id=f080a339-14d5-4d5f-b068-e5017851491c " =103x35")

 ![Componente com expansão](/api/attachments.redirect?id=c8d9685a-f72c-43cb-ac06-2be3b39e4c6f " =104x68.5")

#### ==Componente de MAPE Médio de Receita na Janela de Dias:== 

Esse componente, como o nome já descreve, é relacionado ao MAPE Médio de Receita na Janela de Dias. Ele aponta a média de acordo com a janela de dias selecionada.

 ![](/api/attachments.redirect?id=1ed1a0f3-530d-4ecc-8edc-150d62ebd968 " =121.5x37.5")

#### ==Componente de MAPE Médio de Receita Mensal nos Últimos Anos:== 

Esse componente, como o nome já descreve, é relacionado ao MAPE Médio de Receita Mensal nos Últimos Anos. Ele não varia de acordo com a janela. 

 ![](/api/attachments.redirect?id=9e14493c-cb82-428c-9f88-a567d676afd8 " =141.5x36.5")


#### ==Gráfico de Mean Absolute Percentage Error (MAPE) de Receita ao Longo da Janela de Dias:== 

Mostra a variação do MAPE durante a janela de dias selecionada. Seguem exemplos: ![Gráfico considerando uma janela de 30 dias](/api/attachments.redirect?id=71805909-8603-4466-b3de-7cb187072594 " =616x101.5")

 ![Gráfico considerando uma janela de 15 dias](/api/attachments.redirect?id=fa160e9b-ccaf-4cdd-9faf-cb9e8ad222ae " =619x98.5")

 ![Gráfico considerando uma janela de 7 dias](/api/attachments.redirect?id=9486768b-1add-4dbd-9fb8-41d13a0bd7fa " =618.5x103")

#### ==Tabela com Maiores Erros de MAPE(Mean Absolute Percentage Error):== 

Aponta casos críticos de erros em relação ao MAPE. 

 ![](/api/attachments.redirect?id=2cd6acfc-5692-44f1-bb70-8234f612a4c2 " =443.5x125") 

#### ==Componentes de anomalias:== 

informam os números relacionados a ID's e registros com preços anômalos na data atual.

 ![](/api/attachments.redirect?id=1b2dce54-007d-4f1e-a09b-44b6301860e4 " =126x63.5")

#### ==Componente MAPE Médio de Preço dos Últimos 15 dias:== 

Calcula a média de preço no intervalo dos últimos 15 dias e informa.

 ![](/api/attachments.redirect?id=f9076f1e-d4e6-4d19-861b-2198f1a4831d " =122.5x32.5")

#### ==Gráfico de Variação do Preço Médio Diário ao Longo dos Últimos 30 dias:== 

Compara os preços do lake e do sirius ao longo dos últimos 30 dias.

 ![](/api/attachments.redirect?id=eda76176-90eb-47e0-b145-5bd06182abb4 " =616x103")

#### ==Gráfico de Variação do Mean Absolute Percentage Error (MAPE) por ano/mês:== 

Demonstra o comportamento variacional do MAPE ao longo dos anos e meses num intervalo amplo e ambrangente. 

 ![](/api/attachments.redirect?id=2bb219a1-cf81-442b-8be0-543b07cadd2a " =618x156.5")

**O que é possível analisar:**

* Evolução do MAPE ao longo do tempo;
* Identificação de janelas com erros elevados;
* Volume de registros impactados por erros críticos;
* Comparação entre diferentes períodos.

Essa página é útil para:

* validar a confiabilidade dos modelos de receita;
* identificar regressões;
* priorizar investigações de dados.

## Página 3 — Diagnóstico e Logs

### Componentes

#### ==Checkbox de erro:==

Ele permite filtrar apenas por registros em que o erro ocorreu. 

 ![Checkbox inativo](/api/attachments.redirect?id=c1019c48-debf-47ca-bd25-5b265b8a4bd1 " =143.5x33")

 ![Checkbox ativo](/api/attachments.redirect?id=05f8211c-0b05-4317-b326-66ccab010643 " =140.5x32.5")

#### ==Tabela Detalhada com Logs de Execução por Scraper:==  

Criada para possibilitar a investigação da causa raiz de um erro sem precisar rodar queries manuais no BigQuery ou ler logs brutos na AWS.

 ![Tabela com todas as execuções de modo geral](/api/attachments.redirect?id=60cf1d63-4c6b-4c1e-8bc4-f34dc3fe9d81 " =727.5x221.5")

 ![Tabela com o checkbox de erro ativado](/api/attachments.redirect?id=8d1e78b1-2857-4f44-ac6e-dcf606d22307 " =726x221.5")


Link do Dashboard: <https://lookerstudio.google.com/u/0/reporting/9af9c18c-0790-4068-84d9-b93b52db580b/page/p_rh740aejzd>