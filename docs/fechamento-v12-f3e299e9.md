<!-- title: Fechamento v1.2 | url: https://outline.seazone.com.br/doc/fechamento-v12-9hV9yo6vW6 | area: Tecnologia -->

# 📃 Fechamento v1.2

> Autores:  
>
> Revisores: 
>
> Última Alteração:


## TL;DR

O propósito deste documento é explicar e quebrar em acionáveis uma primeira entrega de Novo Fechamento. Aqui chamado de Fechamento v1.2


# 1. O que é o Fechamento

<falar o que faz, pq é um problema e a motivação pra refatora-lo, assim como os custos>

# 2. Panorama técnico atual

Atualmente o Fechamento é um processo custoso, que utilizada a arquitetura Serverless da AWS para processar os dados, de maneira assíncrona. Atualmente são usados os seguintes Serviços:\n

* Step Functions;
* Lambdas;
* S3,
* Banco de Dados Postgres

  \

 ![Fluxo atual usado nas StepFunctions](/api/attachments.redirect?id=f5f262f4-37f7-4ae2-a3b0-1617cb0c0e47 " =1283x1057")

Atualmente todos os lambdas são feitos em Python e o fluxo todo é em batch a partir do banco de dados.

### 2.1 Ingestion Batcher

### 2.2 Prepare Properties

### 2.3 Property Batcher

### 2.4 Process Host & Partner

### 2.5 Aggregations

### 2.6 S3 Paths to Save

### 2.7 Save to Sapron Batcher


# 3. Proposta técnica

A ideia aqui é dividir em possíveis *User Stories* para sem atacadas pelo squad **Sapron** para entregar esse trabalho. Ele é dividido em 2 etapas aqui chamadas de **Procedures** e **Nova Arquitetura, mas nem tão nova**.

## 3.1 Procedures

Atualmente, já existem no banco de dados de produção Triggers e Procedures até então inativas criadas pelo CTO Arilo, aqui fazendo o papel de DBA, onde fazem o trabalho de um Fechamento, nesse caso já de maneira síncrona. É possível ver o documento técnico proposto [aqui](/doc/novo-fechamento-via-sapron-CTEIfGYmW1).

Em fins práticos, a ideia é habilitar as procedures e triggers para começar a gerar o Fechamento a partir delas, e começar a medir sua acurácia, em comparação ao Fechamento Atual. Tudo isto para já termos um novo fechamento rodando e assim diminuir custos e batermos nossa meta Trimestral.

Existem já alguns quadros de acompanhamento via metabase para medir a acurácia e performance entre os dois Fechamentos:

Performance: 

Acurácia: <https://metabase.sapron.com.br/question/927-diferenca-do-velho-e-novo-fechamento-property>

O principal ponto negativo dessa abordagem, é a falta de **manutenibilidade** dos códigos que ficam dentro do banco de dados, ocasionando em aumento de tempo para resolução de bugs e unificando somente na figura do Arilo para possíveis resoluções de problemas/bugs.

O que contrapõe esse ponto, é que, atualmente no modelo Serverless já passamos pelos mesmos problemas, sendo que não temos a figura de um "Arilo" para debuggar e solucionar os problemas, além do custo maior para rodar.


## 3.2 Nova Arquitetura, mas nem tão nova

Neste segunda etapa, afim de resolver os problemas que ainda não foram resolvidos na primeira, a ideia é refatorar o fluxo de fechamento de Procedures para uma arquitetura onde seja mais pulverizada o entendimento entre todos e que tira o workload do banco de dados. Sendo assim, pensei em uma estrutura de Filas, utilizando já o SQS ao invés do atual RabbitMQ, onde se fazer o uso dessa estrutura para mesmo que assíncrono, garante maior qualidade manutenção, com menor bugs e com toda a estrutura que uma Fila pode oferecer a mais que StepFuncions e Procedures - como por exemplo utilizar as *dead-letters* (dlq's) para re-rodar possíveis problemas, além de ter suporte to time de infra para gerenciar e monitorar código por meio do Grafana, para possíveis problemas. Tudo isso a um custo inferior ao atual.

Para isso, seriam necessários os seguintes passos (possíveis US's)

### 3.2.1 Roadmap   


\