<!-- title: Mapeamento de bancos e discos críticos | url: https://outline.seazone.com.br/doc/mapeamento-de-bancos-e-discos-criticos-AB9wA1C3Ik | area: Tecnologia -->

# Mapeamento de bancos e discos críticos

Relatório elaborado após a crise em que perdemos todos os workflows do n8n. O objetivo é listar os bancos e armazenamentos utilizados para aplicações críticas, mapear a política de backup e fazer ajustes caso algum não tenha backup configurado.

## Mapeamento inicial 

listagem inicial dos recursos e como os backups deles estavam configurados inicialmente : 

| Aplicação | Tipo de persistência | Backup | Retenção |
|----|----|----|----|
| Baserow | Banco Gerenciado | diário | 30d |
| Outline | Banco Gerenciado | diário | 30d |
| n8n | Pod - postgres | diário | 7d |
| vault  | Disco | diário | 3d |
| kuma | Disco | sem backup | - |
| vpn | Disco | diário | 2d |
| Growthbook | Pod - Mongo | sem backup | - |
| Metabase | Banco Gerenciado | diário | 30d |
| wallet-produção | Banco Gerenciado | diário | 30d |
| sapron-produção | Banco Gerenciado | diário | 30d |
| reservas-produção | Banco Gerenciado | diário | 30d |
| wallet-staging | Banco Gerenciado | diário | 7d |
| sapron-staging | Banco Gerenciado | diário | 7d |
| reservas-staging | Banco Gerenciado | diário | 7d |
| open panel - poc | Pod - postgres \| Clickhouse \| mongo | sem backup | - |
| Kubecost | Disco | sem backup | - |
| Grafana  | Disco | sem backup | - |

## Ações tomadas 

* criada política de snapshot diária para o disco utilizado pelo [uptime-kuma](https://uptime.seazone.com.br/dashboard/42) visando a retenção das nossas métricas de uptime em caso de eventual acidente - retenção  configurada para 4 dias 
* criada política de snapshot diária para o disco utilizado pelo mongodb que temos rodando no cluster, esse mongodb hoje armazena dados do growthbook - retenção configurada  3 dias (esse vale discutir sobre aumentar a retenção)
* criada política de snapshot semanal para discos usados pelo kubecost (aggregator-db-storage-kubecost-aggregator-0, aggregator-db-storage-kubecost-aggregator-0 ) - retenção configurada para guardar somente a última snapshot entendendo que é um sistema menos crítico

  \

## Panorama final 

| Aplicação | Tipo de persistência | Backup | Retenção |
|----|----|----|----|
| Baserow | Banco Gerenciado | diário | 30d |
| Outline | Banco Gerenciado | diário | 30d |
| n8n | Pod - postgres | diário | 7d |
| vault  | Disco | diário | 3d |
| kuma | Disco | diário | 4d |
| vpn | Disco | diário | 2d |
| Growthbook | Pod - Mongo | diário | 3d |
| Metabase | Banco Gerenciado | diário | 30d |
| wallet-produção | Banco Gerenciado | diário | 30d |
| sapron-produção | Banco Gerenciado | diário | 30d |
| reservas-produção | Banco Gerenciado | diário | 30d |
| wallet-staging | Banco Gerenciado | diário | 7d |
| sapron-staging | Banco Gerenciado | diário | 7d |
| reservas-staging | Banco Gerenciado | diário | 7d |
| open panel - poc | Pod - postgres \| Clickhouse \| mongo | sem backup | - |
| Kubecost | Disco | semanal | 7d |
| Grafana | Disco | semanal | 7d |


## Observações

* acho que vale discutirmos se vale a pena manter esse mongodb de tools que hoje é usado pelo growthbook mas que pode vir a ser usado por outros tools em um pod, acho que poderíamos pensar em outras opções como o [mongoDB Atlas](https://aws.amazon.com/partners/mongodb/)  ou o [documentDB](https://aws.amazon.com/pt/documentdb/)  da própria AWS que pesquisando aqui parece ser compatível e pode ser usado como mongo para o growthbook
* nosso monitoramento é configurado para fazer a retenção das métricas em buckets, entendendo isso não me aprofundei muito na pesquisa desses componentes específicos 
* o Open panel não apliquei nenhum tipo de política por que ainda é um recurso que está em fase de POC, entendo que se optarmos por realmente seguir com essa ferramenta podemos definir melhor como será configurada a persistência