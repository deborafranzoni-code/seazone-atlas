<!-- title: S3-Timed-Storage-Bytes | url: https://outline.seazone.com.br/doc/s3-timed-storage-bytes-IgkT7giGxQ | area: Tecnologia -->

# S3-Timed-Storage-Bytes

Documentação criada para investigar o aumento de Timed-storage-bytes na conta de applications durante os meses de dezembro e janeiro

## Causa Principal

Principal ofensor identificado, sendo o bucket que o tempo utilizar para armazenar blocos de traces 

 ![](/api/attachments.redirect?id=a29163ba-350f-472e-8dd1-c6acf7034e03 " =837x350") 

No gŕafico é possível observar a barra azul claro que representa o bucket **general-cluster-grafana-tempo-traces-sa-east-1** aumentando bruscamente a partir de novembro, chegando um custo de $270 durante o mês de janeiro.

Identificamos que esse aumento foi ocasionado por conta de uma configuração que fizemos em dezembro, onde aumentamos o período de retenção dos traces que estava em 48h (2 dias), para 720h (30 dias) esse ajuste foi feito visando aumentar a visibilidade de traces pelo time de desenvolvimento e acabou gerando um aumento bem relevante no volume de dados armazenados no bucket

## Ações

* [Ajuste no período de retenção dos traces](https://github.com/seazone-tech/gitops-governanca/pull/99/changes), de 30 dias para 14 dias
* [Adicionada compressão para os blocos de métricas](https://github.com/seazone-tech/gitops-governanca/pull/99/changes) visando diminuir o tamanho dos blocos armazenados
* [Criado report no billing](https://us-east-1.console.aws.amazon.com/costmanagement/home?region=sa-east-1#/cost-explorer?chartStyle=STACK&costAggregate=unBlendedCost&endDate=2026-02-05&excludeForecasting=false&filter=%5B%7B%22dimension%22:%7B%22id%22:%22Service%22,%22displayValue%22:%22Service%22%7D,%22operator%22:%22INCLUDES%22,%22values%22:%5B%7B%22value%22:%22Amazon%20Simple%20Storage%20Service%22,%22displayValue%22:%22S3%22%7D%5D%7D,%7B%22dimension%22:%7B%22id%22:%22UsageType%22,%22displayValue%22:%22Usage%20type%22%7D,%22operator%22:%22INCLUDES%22,%22values%22:%5B%7B%22value%22:%22APN1-TimedStorage-ByteHrs%22,%22displayValue%22:%22APN1-TimedStorage-ByteHrs%22%7D,%7B%22value%22:%22APN2-TimedStorage-ByteHrs%22,%22displayValue%22:%22APN2-TimedStorage-ByteHrs%22%7D,%7B%22value%22:%22APS1-TimedStorage-ByteHrs%22,%22displayValue%22:%22APS1-TimedStorage-ByteHrs%22%7D,%7B%22value%22:%22APS2-TimedStorage-ByteHrs%22,%22displayValue%22:%22APS2-TimedStorage-ByteHrs%22%7D,%7B%22value%22:%22APS3-TimedStorage-ByteHrs%22,%22displayValue%22:%22APS3-TimedStorage-ByteHrs%22%7D,%7B%22value%22:%22EU-TimedStorage-ByteHrs%22,%22displayValue%22:%22EU-TimedStorage-ByteHrs%22%7D,%7B%22value%22:%22EUC1-TimedStorage-ByteHrs%22,%22displayValue%22:%22EUC1-TimedStorage-ByteHrs%22%7D,%7B%22value%22:%22EUW2-TimedStorage-ByteHrs%22,%22displayValue%22:%22EUW2-TimedStorage-ByteHrs%22%7D,%7B%22value%22:%22SAE1-IATimedStorage-ET-ByteHrs%22,%22displayValue%22:%22SAE1-IATimedStorage-ET-ByteHrs%22%7D,%7B%22value%22:%22SAE1-IATimedStorage-ET-SmallFiles%22,%22displayValue%22:%22SAE1-IATimedStorage-ET-SmallFiles%22%7D,%7B%22value%22:%22SAE1-TimedStorage-ByteHrs%22,%22displayValue%22:%22SAE1-TimedStorage-ByteHrs%22%7D,%7B%22value%22:%22TimedStorage-ByteHrs%22,%22displayValue%22:%22TimedStorage-ByteHrs%22%7D,%7B%22value%22:%22USE1-TimedStorage-ByteHrs%22,%22displayValue%22:%22USE1-TimedStorage-ByteHrs%22%7D,%7B%22value%22:%22USE2-TimedStorage-ByteHrs%22,%22displayValue%22:%22USE2-TimedStorage-ByteHrs%22%7D,%7B%22value%22:%22USW1-TimedStorage-ByteHrs%22,%22displayValue%22:%22USW1-TimedStorage-ByteHrs%22%7D,%7B%22value%22:%22USW2-FeatureStore:TimedAndPITRStorage%22,%22displayValue%22:%22USW2-FeatureStore:TimedAndPITRStorage%22%7D,%7B%22value%22:%22USW2-TimedStorage-ByteHrs%22,%22displayValue%22:%22USW2-TimedStorage-ByteHrs%22%7D,%7B%22value%22:%22USW2-TimedStorage-GlacierByteHrs%22,%22displayValue%22:%22USW2-TimedStorage-GlacierByteHrs%22%7D,%7B%22value%22:%22USW2-TimedStorage-INT-FA-ByteHrs%22,%22displayValue%22:%22USW2-TimedStorage-INT-FA-ByteHrs%22%7D%5D%7D,%7B%22dimension%22:%7B%22id%22:%22LinkedAccount%22,%22displayValue%22:%22Linked%20account%22%7D,%22operator%22:%22INCLUDES%22,%22values%22:%5B%7B%22value%22:%22711387131913%22,%22displayValue%22:%22711387131913%22%7D%5D%7D%5D&futureRelativeRange=CUSTOM&granularity=Daily&groupBy=%5B%22TagKeyValue:BucketName%22%5D&historicalRelativeRange=MONTH_TO_DATE&isDefault=false&reportArn=arn:aws:ce::834181448060:ce-saved-report%2Fd9ab76b0-45b5-45b9-88e3-120101c43c2c&reportId=d9ab76b0-45b5-45b9-88e3-120101c43c2c&reportMode=STANDARD&reportName=Plataforma%20-%20Timed-Storage-Bytes%20di%C3%A1rio&showOnlyUncategorized=false&showOnlyUntagged=false&startDate=2026-02-01&usageAggregate=usageQuantity&useNormalizedUnits=false) para acompanharmos se os ajustes tiveram algum efeito prático 
* Lifecyle policy adicionada ao bucket para remover objetos com mais de 14 dias de idade, otimizando o tamanho total do bucket 

  ![](/api/attachments.redirect?id=64a495ed-48cf-4512-b84a-418a9dc83a6a "left-50 =652x315")

 ![](/api/attachments.redirect?id=6ac45df7-188a-482e-baf0-ea5ff5afa2e2 " =1146x571")

## Ações extras

*Ações não relacionadas ao principal ofensor mas que também geram economia*

* Limpeza total dos dados do  bucket [general-cluster-grafana-mimir-metrics-sa-east-1](https://sa-east-1.console.aws.amazon.com/s3/buckets/general-cluster-grafana-mimir-metrics-sa-east-1?region=sa-east-1) , visto que esses dados não estavam sendo utilizados por nenhuma ferramenta e que o Mimir atualmente está desativado
* Remoção de buckets de monitoramento de oregon, apesar de não aparecerem como grandes ofensores, somados chegavam na casa do $1,50 por dia, batendo pouco mais de $30 no mês
  * seazone-tempo-distributed
  * seazone-grafana-mimir-production
  * seazone-loki-production
  * seazone-grafana-tempo