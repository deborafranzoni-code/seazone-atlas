<!-- title: Investigação de Custos CloudWatch | url: https://outline.seazone.com.br/doc/investigacao-de-custos-cloudwatch-f3zTZCiIxZ | area: Tecnologia -->

# Investigação de Custos CloudWatch

## Contexto

Custo do CloudWatch estava alto. Referência inicial: julho de 2025 custava **$200**. Investigação aberta pra entender de onde vem, por que cresceu, e o que cortar.

## 1. Histórico mensal 

Realizei a investigação pelo AWS CLI, pela facilidade de recuperar logs, jsons e retorno de custos.

 ![](/api/attachments.redirect?id=1e6d60d6-5fc7-45f9-8fbd-9b8d9b2f32c1 " =1025x432")

**Comando utilizado:**

```bash
aws ce get-cost-and-usage --profile manager \
  --time-period "Start=2025-06-01,End=2026-02-01" \
  --granularity MONTHLY \
  --metrics "UnblendedCost" \
  --filter '{"Dimensions":{"Key":"SERVICE","Values":["AmazonCloudWatch"]}}'
```

| Mês | Custo | Crescimento vs Junho |
|----|----|----|
| Jun 2025 | $==168.95== | baseline |
| Jul 2025 | $200.16 | +18% |
| Ago 2025 | $249.15 | +47% |
| Set 2025 | $378.49 | +124% |
| Out 2025 | $616.03 | +265% |
| Nov 2025 | $671.86 | +298% |
| Dez 2025 | $770.04 | +356% |
| **Jan 2026** | **$==910.74==** | **+439%** |

Não é estável, está acelerando. De junho a janeiro, cresceu **5.4x**.

## 2. Qual conta está gastando 

Após isso usei um comando para listar qual account estava tendo maior custo por período.

 ![](/api/attachments.redirect?id=1b53fece-be99-448c-84ce-e9f0b18e3367 " =1040x549")

```bash
aws ce get-cost-and-usage --profile manager \
  --time-period "Start=2025-07-01,End=2025-08-01" \
  --granularity MONTHLY \
  --metrics "UnblendedCost" \
  --filter '{"Dimensions":{"Key":"SERVICE","Values":["AmazonCloudWatch"]}}' \
  --group-by '[{"Type":"DIMENSION","Key":"LINKED_ACCOUNT"}]'
```

**Julho 2025:**

| Conta | Valor | % |
|----|----|----|
| Applications | $106.86 | 53.4% |
| Seazone Technology | $39.16 | 19.6% |
| Staging | $30.74 | 15.4% |
| PRD-Lake | $18.72 | 9.4% |
| Resto | < $5 | \~2% |

**Janeiro 2026** (mesmo comando, período diferente):

| Conta | Valor | % |
|----|----|----|
| **Applications** | **$852.49** | **93.6%** |
| Seazone Technology | $36.48 | 4.0% |
| PRD-Lake | $17.98 | 2.0% |
| Resto | < $3 | \~0.4% |

**Insights:**

* Applications foi de $107 pra $852 — cresceu **8x** em 6 meses.
* ==Seazone Technology e PRD-Lake ficaram estáveis.== O problema é **só** na conta Applications.

## 3. Onde exatamente o custo vai 

Em seguida, outro comando para extrair o breakdown por tipo de uso que está causando tais custos.

 ![](/api/attachments.redirect?id=d95f139b-c8d0-490a-9af0-6da2f3cc3d65 " =996x645")

```bash
aws ce get-cost-and-usage --profile manager \
  --time-period "Start=2026-01-01,End=2026-02-01" \
  --granularity MONTHLY \
  --metrics "UnblendedCost" \
  --filter '{"Dimensions":{"Key":"SERVICE","Values":["AmazonCloudWatch"]}}' \
  --group-by '[{"Type":"DIMENSION","Key":"USAGE_TYPE"}]'
```

**Julho 2025 vs Janeiro 2026, comparativo:**

| Usage Type | Jul 2025 | Jan 2026 | O que significa |
|----|----|----|----|
| USW2-VendedLog-Bytes | $110.55 | $0.09 | Logs de serviços AWS em us-west-2 **caiu pra zero** |
| USW2-DataProcessing-Bytes | $43.37 | $39.40 | Processamento logs us-west-2 — estável |
| SAE1-VendedLog-Bytes | $17.74 | **$209.08** | Logs RDS/EKS em sa-east-1 — **12x** |
| SAE1-DataProcessing-Bytes | $0.78 | **$420.18** | Ingestão logs customizados sa-east-1 — **540x** |
| SAE1-S3-Egress-Bytes | — | **$180.26** | Entrega de logs pro S3 — não existia em julho |
| SAE1-S3-Egress-InputBytes | — | $28.32 | Input da entrega S3 |
| SAE1-TimedStorage-ByteHrs | — | $10.27 | Armazenamento logs sa-east-1 |

Em julho, o custo principal era em **us-west-2**. Em janeiro, migrou tudo pra **sa-east-1**. O us-west-2 VendedLog caiu de $110 pra $0.09, provavelmente porque o cluster EKS prod foi deletado de lá. ==Os três maiores custos em janeiro somam **$809 (89% do total)** e são todos sa-east-1, todos conta Applications.==

## 4. Varredura de log groups 

Rodei varredura em todas as contas acessíveis e todas as regiões:

 ![](/api/attachments.redirect?id=e6c9374e-a3fe-497a-99b9-07d4813d5eb8 " =1429x538")

```bash
for profile in applications sandbox sirius dev-sirius prd-lake dev-lake prd-backup; do
  for region in us-east-1 us-west-2 sa-east-1 eu-west-1; do
    aws logs describe-log-groups --profile $profile --region $region \
      --query 'logGroups[?storedBytes>`0`].{Name:logGroupName, Bytes:storedBytes, Ret:retentionInDays}' \
      --output json
  done
done
```

**Conta Applications  sa-east-1:**

| Log Group | Tamanho | Retenção | Status |
|----|----|----|----|
| /aws/eks/general-cluster/cluster | 100 GB | 90 dias | Ativo |
| /aws/rds/instance/tools-postgres/postgresql | 100 GB | **sem limite**   | Export desabilitado no RDS |
| /aws/rds/instance/sapron-prd-postgres-replica/postgresql | 48 GB | **sem limite** | Ativo, exportando |
| /aws/rds/instance/sapron-prd-postgres/postgresql | 35 GB | **sem limite** | Ativo, exportando |
| /aws/rds/instance/reservas-prd-postgres/postgresql | 12 GB | **sem limite** | Ativo, exportando |
| /aws/rds/instance/stg-postgres/postgresql | 9 GB | **sem limite** | Export desabilitado no RDS |
| /aws/rds/instance/reservas-prd-postgres-replica/postgresql | 99 MB | **sem limite** | Ativo, exportando |
| RDSOSMetrics | 174 MB | 30 dias | OK |

**Conta Applications — us-west-2:**

| Log Group | Tamanho | Retenção | Status |
|----|----|----|----|
| /aws/eks/eks_seazone_prod/cluster | **150 GB** | **sem limite** | **órfão, cluster foi deletado** |
| /aws/lambda/lambda-loki-logger | 4 MB | sem limite | OK |
| RDSOSMetrics | 339 MB | 30 dias | OK |

Dois log groups totalmente orphanados: ==o EKS prod (cluster não existe mais, mas o log group com 150 GB permanece) e tools-postgres (export desabilitado, mas 153 GB acumulados).== Juntos são **303 GB de dados mortos** cobrando storage.

## 5. Descartando CloudFront como fonte

 ![](/api/attachments.redirect?id=7165234d-1b19-4c00-b872-deec0a29c6f5 " =1218x579")

```bash
aws cloudfront list-distributions --profile applications \
  --query 'DistributionList.Items[*].{Id:Id, Domain:DomainName, Logging:Logging.Enabled}'
```

 4 distribuições, **nenhuma com logging ativo**. CloudFront não está mandando dados pra nenhum lugar. Custo do CloudFront na organização foi $9.50 em julho.

## 6. Investigando o lambda-loki-logger

Esse Lambda poderia estar processando logs:

 ![](/api/attachments.redirect?id=499ed144-a414-4dae-801e-33bec71a9dc7 " =1174x582")

```bash
aws lambda get-function --profile applications --region us-west-2 \
  --function-name lambda-loki-logger
```

É uma instância de **Promtail** rodando como Lambda (imagem ECR). A descrição diz: *"Promtail instance to collect logs from ALB Logs in S3"*. Ele lê logs do ALB diretamente do S3 e manda pra Loki (`https://loki-lambda.seazone.com.br`). Estado atual: **Inactive** (idle). ==Não está contribuindo pra nada.== 


## 7. Medindo o volume real de ingestão de CloudWatch metrics

Usei a métrica IncomingBytes do namespace AWS/Logs pra medir o que realmente está sendo ingestado, não só o que está armazenado:

 ![](/api/attachments.redirect?id=c49fe775-f241-4b13-8d84-968d56be109f " =1452x426")

```bash
aws cloudwatch get-metric-statistics --profile applications --region sa-east-1 \
  --namespace AWS/Logs \
  --metric-name IncomingBytes \
  --dimensions Name=LogGroupName,Value="/aws/rds/instance/sapron-prd-postgres/postgresql" \
  --start-time 2026-01-01T00:00:00Z \
  --end-time 2026-02-01T00:00:00Z \
  --period 2678400 \
  --statistics Sum
```

**Resultados de ingestão em janeiro:**

| Log Group | GB Ingestado no Mês |
|----|----|
| /aws/eks/general-cluster/cluster | **294 GB** |
| /aws/rds/instance/sapron-prd-postgres-replica/postgresql | **269 GB** |
| /aws/rds/instance/sapron-prd-postgres/postgresql | **256 GB** |
| /aws/rds/instance/reservas-prd-postgres/postgresql | 20 GB |
| **Total sa-east-1** | **\~840 GB/mês** |

O storedBytes mostrava dezenas de GB nos log groups, mas a ingestão real era centenas de GB por mês. Sapron sozinho: **525 GB/mês**. Aqui está gerando 100x mais.


---

## 8. Configuração do PostgreSQL

Com esse volume muito alto em metrics Sapron, chequei os parameter groups do RDS:

 ![](/api/attachments.redirect?id=c96761c4-a6ce-4a96-981d-3ba5449f73a6 " =1397x865")

```bash
aws rds describe-db-parameter-groups --profile applications --region sa-east-1 \
  --query 'DBParameterGroups[*].{Name:DBParameterGroupName}'
  
# Pegar parametros customizados 
aws rds describe-db-parameters --profile applications --region sa-east-1 \
  --db-parameter-group-name "sapron-prd-postgres-20250905184047115700000002" \
  --source user
```

**Resultado para o sapron:**

| Parametro | Valor | O que significa |
|----|----|----|
| `log_statement` | **all** | Loga **cada SQL** — SELECT, INSERT, UPDATE, DELETE, DDL |
| `log_min_duration_statement` | 1000 | Loga duração de queries > 1s |

Verifiquei **todos** os parameter groups:

| sapron-prd-postgres | log_mentstate | all  ✗ |
|----|----|----|
| sapron-prd-postgres-replica | log_mentstate | all  ✗ |
| reservas-prd-postgres | log_mentstate | all  ✗ |
| reservas-prd-postgres-replica | log_mentstate | all  ✗ |
| tools-postgres | log_mentstate | all  ✗ |
| stg-postgres | log_mentstate | all  ✗ |

**Todos os seis parameter groups têm** `**log_statement = all**`**.**

`log_statement = all` é o pior cenário pra volume de logs. Cada query que qualquer aplicação executa contra esse banco gera uma linha de log. Em um ambiente de produção com tráfego constante, isso explica os 525 GB/mês do sapron.

[O valor padrão recomendado pra produção é ](https://www.postgresql.org/docs/current/runtime-config-logging.html)`[error](https://www.postgresql.org/docs/current/runtime-config-logging.html)`[ (só loga erros) ou ](https://www.postgresql.org/docs/current/runtime-config-logging.html)`[ddl](https://www.postgresql.org/docs/current/runtime-config-logging.html)`[ (só loga comandos DDL como CREATE/ALTER/DROP).](https://www.postgresql.org/docs/current/runtime-config-logging.html) `all` é normalmente usado por curtos períodos de debugging.


---

## 9. Confirmando a infraestrutura do Grafana

Ao listar os S3 buckets da conta Applications, vi o setup completo do Grafana:

| general-cluster-loki-logs-sa-east-1 | Loki (logs) |
|----|----|
| general-cluster-grafana-mimir-metrics-sa-east-1 | → Mimir (métricas) |
| general-cluster-grafana-tempo-backend-sa-east-1 | → Tempo (traces) |
| seazone-loki-production | → Loki produção |
| seazone-grafana-mimir-production | → Mimir produção |

O Grafana stack (Loki, Mimir, Tempo) roda no EKS general-cluster em sa-east-1. Os logs das aplicações vão diretamente pra Loki (não passam pelo CloudWatch). O CloudWatch está sendo usado apenas pra:


1. Logs automáticos do RDS (não dá pra desativar sem desativar o export no RDS)
2. Logs de control plane do EKS (automático quando habilitado no cluster)

## 10. Confirmando qual RDS está exportando e qual não está

 ![](/api/attachments.redirect?id=a8865edb-bf2f-48e4-a66e-12e6e9dfa6b8 " =921x570")

```bash
aws rds describe-db-instances --profile applications --region sa-east-1 \
  --query 'DBInstances[*].{Name:DBInstanceIdentifier, Logs:EnabledCloudwatchLogsExports}'
```

| Instância | Exporta logs? |
|----|----|
| reservas-prd-postgres | Sim (`postgresql`) |
| reservas-prd-postgres-replica | Sim (`postgresql`) |
| sapron-prd-postgres | Sim (`postgresql`) |
| sapron-prd-postgres-replica | Sim (`postgresql`) |
| stg-postgres | **Não** |
| tools-postgres | **Não** |

`stg-postgres` e `tools-postgres` não exportam mais, mas os log groups ainda existem com dados históricos acumulados (9 GB e 100 GB respectivamente). ==Esses são dados mortos==

## 11. Isolando custos por conta + usage type 

Agora olhando usage types no agregado da organização. Parte dos custos não vinha da Applications. Fiz queries no Cost Explorer com filtro duplo (serviço + usage type) agrupado por conta:

 ![](/api/attachments.redirect?id=bbb14d47-a894-4c2a-ad79-3500fbc21aa6 " =1197x681")

> ```bash
> aws ce get-cost-and-usage --profile manager \
>   --time-period "Start=2026-01-01,End=2026-02-01" \
>   --granularity MONTHLY \
>   --metrics "UnblendedCost" \
>   --filter '{"And":[
>     {"Dimensions":{"Key":"SERVICE","Values":["AmazonCloudWatch"]}},
>     {"Dimensions":{"Key":"USAGE_TYPE","Values":["USW2-DataProcessing-Bytes"]}}
>   ]}' \
>   --group-by '[{"Type":"DIMENSION","Key":"LINKED_ACCOUNT"}]'
> ```

Rodei isso pra cada usage type suspeito. Resultados:

> 
| Usage Type | Total | Conta principal | Valor |
|----|----|----|----|
| USW2-DataProcessing-Bytes | $39.40 | **Seazone Technology** | $36.06 |
| USW2-CW:MetricMonitorUsage | $15.65 | **PRD-Lake** | $15.12 |
| USW2-CW:AlarmMonitorUsage | $0.66 | Seazone Technology | $0.42 |
| CW:AlarmMonitorUsage | $0.20 | Seazone-Manager | $0.15 |
| SAE1-S3-Egress-Bytes | $180.26 | **Applications** | $180.26 (100%) |
| SAE1-CW:MetricMonitorUsage | $2.95 | Applications | $2.95 |

 O $39 de DataProcessing em us-west-2 não é da Applications, é da Seazone Technology. E o $15 de MetricMonitor é do PRD-Lake. Isso significa precisava adicionar mais duas contas a mais além da Applications.

## 12. Conta Seazone Technology 

Pegando os log groups da conta tecnologia em us-west-2 (onde tava o $36 de DataProcessing):

 ![](/api/attachments.redirect?id=e3df32eb-9f78-4fc0-ab2c-8e502f88df40 " =1217x634")

> ```bash
> aws logs describe-log-groups --profile tecnologia --region us-west-2 \
>   --query 'logGroups[*].{Name:logGroupName, Bytes:storedBytes, Ret:retentionInDays}' \
>   --output table
> ```

**Números:**

* 370 log groups no total
* **354 sem retenção** (96%)
* **433 GB acumulados**

> **Por categoria:**

| Categoria | Storage |
|----|----|
| ECS pipe-\* (scrapers Airbnb/OLX/Booking) | 187 GB |
| ECS airbnb-fargate-price-\* (um por cidade) | 156 GB |
| ECS outros (sirius, galadriel, metabase...) | 85 GB |
| RDS | 4 GB |
| SageMaker | 1 GB |
>
> **Top 10 por tamanho:**

| Log Group | Tamanho | Retenção |
|----|----|----|
| /ecs/pipe-olx-scraper-data | 90 GB | sem limite |
| /ecs/sirius-prod | 36 GB | sem limite |
| /ecs/sirius | 32 GB | sem limite |
| /ecs/pipe-airbnb-scraper-instant-book | 23 GB | sem limite |
| /ecs/pipe-olx-scraper | 20 GB | sem limite |
| /ecs/airbnb-fargate-price-sp | 11 GB | sem limite |
| /ecs/airbnb-fargate-price-florianopolis | 11 GB | sem limite |
| /ecs/airbnb-fargate-price-ubatuba-sp | 9 GB | sem limite |
| /ecs/airbnb-fargate-price-rio-rj | 9 GB | sem limite |
| /ecs/pipe-airbnb-scraper-ranking-location-open-calendar | 10 GB | sem limite |

Além disso, essa conta tem:

* `/aws/kinesisfirehose/DatadogCWLogsforwarder`  Kinesis Firehose pra Datadog
* 3 Lambdas de `DatadogIntegration`  forwarders que processam logs
* `/ecs/ecs-firelens-container`  FireLens (roteador de logs ECS)
* `/aws/rds/instance/khanto-pipe/postgresql`  3.7 GB sem retenção
* `/aws/lambda/mylambatest`  530 MB de logs de teste esquecido

Essa conta tem o mesmo problema de logs acumulando sem retenção. Ainda custava $36/mês em janeiro, mas com 433 GB acumulados e os scrapers ativos, ela pode crescer tal qual Applications.

# Resumo do que aconteceu

**1 - Julho 2025:** CloudWatch custava $200/mês. Infraestrutura principal em us-west-2. EKS prod lá, logs indo pra CloudWatch. Já tinha `log_statement = all` nos bancos, mas o volume era menor.

**2 - Ago/Set 2025:** Migração pra sa-east-1. EKS general-cluster criado em julho, bancos sapron e reservas começando a exportar logs com `log_statement = all`. Sapron-replica adicionado em setembro. Volume de ingestão aumenta. O custo passa de $200 pra $378 em setembro.

**3 - Out 2025 a Jan 2026:** Volume continua crescendo. Os bancos sapron geram 525 GB/mês de logs com `log_statement = all`. EKS gera 294 GB. Sem retenção nos log groups, dados acumulam. ==Custo chega a $910 em janeiro.==

## Causa principal

`log_statement = all` nos seis parameter groups PostgreSQL. ==Essa configuração sozinha é responsável pela maior parte dos 525 GB/mês de ingestão dos bancos sapron e reservas.==

## Secundários

* Log groups sem política de retenção, dados acumulam indefinidamente
* Log group orfão do EKS prod (150 GB) em us-west-2
* Log groups com export desabilitado mas dados históricos ainda sentados (tools: 90 GB, stg: 9 GB)
* EKS general-cluster com `audit` logging que gera volume alto
* **Seazone Technology** 370 log groups, 354 sem retenção, 433 GB acumulados. São scrapers ECS (pipe-olx, airbnb-fargate, sirius).

# Plano de Ação

### 1 - Cortar o volume de ingestão (impacto: \~$400-500/mês)

Alterar `log_statement` nos parameter groups, para cada parameter group

**Valores novos:**`log_statement = error`, só loga erros. Se precisar de mais visibilidade, usar `ddl` (loga erros + comandos DDL).

* `log_min_duration_statement = 5000` (ou 10000), pra ter slow query logging sem logar tudo. 


---

### 2 - Definir retenção nos log groups (impacto: corta storage acumulado)

Estimo que 10 dias é suficiente pra troubleshooting. Se precisar de histórico mais longo, os logs já vão pra Loki via infraestrutura do Grafana.

### 3 - Limpar dados mortos (impacto: \~312 GB de storage eliminado)

* EKS prod, cluster não existe mais
* Log groups com export desabilitado, dados históricos sem valor

### 4 - Revisar logging do EKS general-cluster (impacto: potencial corte de parte dos 294 GB)

O cluster tem `api`, `audit` e `authenticator` habilitados. O `audit` é o mais verboso.

Se o Grafana/Loki já está coletando logs do cluster, é possível:

* Desativar `audit` no CloudWatch e manter só no Loki
* Ou pelo menos adicionar retenção no log group (já tem 90 dias, podemos reduzir pra 30)

### 5 - Limpar Seazone Technology (impacto: \~$30-40/mês)

370 log groups, 354 sem retenção, 433 GB acumulados. Os maiores são scrapers ECS. Os scrapers ativos continuam gerando logs sem limite, tá na mesma trajetória que a Applications seguiu antes de aumentar. Cleanup de órfãos, retenção definida são úteis.

## Economia estimada

| Ação | O que corta | Economia estimada |
|----|----|----|
| `log_statement = error` | \~525 GB/mês de ingestão RDS | \~$400/mês |
| Retenção 14 dias nos log groups | Storage acumulado (corte gradual) | \~$10-20/mês (crescente) |
| Deletar log groups orphanados | 312 GB de storage morto | \~$5-10/mês |
| Revisar audit EKS | Parte dos 294 GB | \~$50-100/mês |
| Prioridade 5 — Retenção + cleanup Seazone Technology | 433 GB storage + DataProcessing us-west-2 | \~$30/mês |
| **Total potencial** |    | **\~$450-530/mês** |

De $910/mês, dá pra chegar em algo entre **$360-440/mês** com essas mudanças.