<!-- title: Guia de deploy | url: https://outline.seazone.com.br/doc/guia-de-deploy-6GBaEAjicS | area: Tecnologia -->

# Guia de deploy

Aqui você encontra um guia sobre como são realizados os deploys do Site de Reservas

## Frontend


---

* **[Processo de Deploy](https://miro.com/app/board/uXjVMpeh4To=/?moveToWidget=3458764563679291591&cot=14)**

## Backend


---

* **[Processo de Deploy](https://miro.com/app/board/uXjVMpeh4To=/?moveToWidget=3458764563679291591&cot=14)**
* ***\[desatualizado\]*** Qtd. de Tarefas Desejadas (Desired Tasks) que devem estar rodando pra cada Serviço do Cluster no ECS
  * Staging

| [seazone-reservas-worker-user](https://us-west-2.console.aws.amazon.com/ecs/v2/clusters/staging-seazone-reservas/services/seazone-reservas-worker-user/health?region=us-west-2) | 1/1 |
|----|----|
| [seazone-reservas-api](https://us-west-2.console.aws.amazon.com/ecs/v2/clusters/staging-seazone-reservas/services/seazone-reservas-api/health?region=us-west-2) | 1/1 |
| [seazone-reservas-worker](https://us-west-2.console.aws.amazon.com/ecs/v2/clusters/staging-seazone-reservas/services/seazone-reservas-worker/health?region=us-west-2) | 1/1 |
| [seazone-reservas-scheduler](https://us-west-2.console.aws.amazon.com/ecs/v2/clusters/staging-seazone-reservas/services/seazone-reservas-scheduler/health?region=us-west-2) | 1/1 |
  * Produção

| [seazone-reservas-worker-user](https://us-west-2.console.aws.amazon.com/ecs/v2/clusters/prod-seazone-reservas/services/seazone-reservas-worker-user/health?region=us-west-2) | 2/2 |
|----|----|
| [seazone-reservas-scheduler](https://us-west-2.console.aws.amazon.com/ecs/v2/clusters/prod-seazone-reservas/services/seazone-reservas-scheduler/health?region=us-west-2) | 1/1 |
| [seazone-reservas-api](https://us-west-2.console.aws.amazon.com/ecs/v2/clusters/prod-seazone-reservas/services/seazone-reservas-api/health?region=us-west-2) | 2/2 |
| [seazone-reservas-worker](https://us-west-2.console.aws.amazon.com/ecs/v2/clusters/prod-seazone-reservas/services/seazone-reservas-worker/health?region=us-west-2) | 2/2 |
* **Como adicionar/alterar variáveis de ambiente**

  [\[Veja até o Final\] Como alterar a Variável de Ambiente na AWS (Staging e Produção)](https://drive.google.com/file/d/1p2qjR5w2Ljr76Rzk6kHRWSypouItAnun/view?usp=drivesdk)

[Deploy quando houver novos campos no opensearch](/doc/deploy-quando-houver-novos-campos-no-opensearch-tFCKIQ8frj)

[Deploy quando há alterações nos Scripts do OpenSearch](/doc/deploy-quando-ha-alteracoes-nos-scripts-do-opensearch-b9MTOvfoPM)

[Como realizar um deploy do Backend que possui alteração de tabela no Banco de Dados](/doc/como-realizar-um-deploy-do-backend-que-possui-alteracao-de-tabela-no-banco-de-dados-5DD5E36PX9)