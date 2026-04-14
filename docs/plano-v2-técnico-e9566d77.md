<!-- title: Plano V2 - Técnico | url: https://outline.seazone.com.br/doc/plano-v2-tecnico-GV0967BqV2 | area: Tecnologia -->

# Plano V2 - Técnico

# Deep Dive FinOps - Seazone AWS Infrastructure

**Data:** 2026-04-02 | **Gasto atual:** \~$10,971/mo 


---

## SUMARIO EXECUTIVO

Apos auditoria completa de **7 contas AWS**, com analise de metricas CloudWatch de CPU/memoria/conexoes/IOPS em **39 instancias EC2**, **7 RDS**, **8 ElastiCache**, **\~100 Lambdas**, **\~170 S3 buckets** e toda a estrutura de custos por usage type, identifiquei **$2,200-4,200/mo em economia real** (20-38% do gasto atual) distribuida em:

| Categoria | Economia/mo | Confianca |
|----|---:|----|
| Compute (Spot + rightsizing + Graviton) | $1,500-3,200 | Alta |
| Storage (S3 lifecycle + EBS cleanup + snapshots) | $200-400 | Alta |
| Networking (VPC Endpoints nekt + NAT analysis) | $30-80 | Media |
| Servicos (Amazon Q + Config + CloudTrail) | $250-300 | Alta |
| Commitments (Savings Plans) | $600-800 | Media |

> **ERRATA (validacao pos-analise):** 3 recomendacoes iniciais foram INVALIDADAS por verificacao de campo:
>
> * ~~VPC Endpoints apps (-$400/mo)~~ -> Ja existem 9 endpoints configurados (S3, ECR, STS, SQS, SSM, EC2, DynamoDB)
> * ~~Tempo traces lifecycle (-$180/mo)~~ -> Ja tem expiracao de 14 dias (os 10.3 TB sao 2 semanas de traces)
> * ~~EKS Extended Support (-$365/mo)~~ -> Cluster esta na v1.33 (mais recente, Standard Support)
> * ~~Loki logs lifecycle~~ -> Ja tem 30d->IA, 90d->Glacier
>
> Isso demonstra a importancia de validar suposicoes antes de agir.


---

## PARTE 1: ANALISE DE UTILIZACAO REAL (Metricas CloudWatch 7 dias)

### 1.1 EC2 / EKS - Cluster "general-cluster" (sa-east-1)

**Arquitetura atual:** EKS com Karpenter gerenciando 4 NodePools + 1 managed node group. 39 instancias running.

#### ACHADO CRITICO #1: c6a.12xlarge a 3% de CPU

| Metrica | Valor |
|----|----|
| Instancia | i-00e5399eccf0933a4 (karpenter-system) |
| Tipo | c6a.12xlarge (48 vCPUs, 96 GB RAM) |
| CPU medio 7d | **3.27%** |
| CPU maximo 7d | **6.77%** |
| Network In | \~105 GB/dia |
| Custo estimado | **\~$1,300-1,500/mo on-demand em sa-east-1** |

**Diagnostico:** Esta instancia esta usando \~1.5 dos 48 vCPUs disponiveis. O alto throughput de rede (105 GB/dia) sugere que serve como node de ingress/sistema, mas isso nao justifica 48 vCPUs. Um c6a.4xlarge (16 vCPUs) ou c6a.2xlarge (8 vCPUs) atenderia com folga -- inclusive para rede, ja que c6a.2xlarge suporta ate 12.5 Gbps.

**Causa raiz provavel:** O NodePool `general-karpenter-system` nao tem constraints adequados de instance size. Karpenter provisionou a maior instancia para consolidar varios pods, mas a soma de requests dos pods e muito menor que a capacidade.

**Acao:**

```yaml
# Limitar instance sizes no NodePool system

apiVersion: karpenter.sh/v1

kind: NodePool

metadata:
  name: general-karpenter-system

spec:
  template:
    spec:
      requirements:
        - key: karpenter.k8s.aws/instance-size
          operator: NotIn
          values: ["8xlarge", "12xlarge", "16xlarge", "24xlarge", "metal"]
        - key: karpenter.k8s.aws/instance-size
          operator: In
          values: ["medium", "large", "xlarge", "2xlarge", "4xlarge"]
```

**Economia estimada:** $800-1,200/mo (swap para c6a.2xlarge ou c6a.4xlarge)

#### ACHADO CRITICO #2: openclaw m7g.xlarge a 0.3% de CPU

| Metrica | Valor |
|----|----|
| Instancia | i-05a410435fcca3183 |
| Tipo | m7g.xlarge (4 vCPUs, 16 GB RAM) |
| CPU medio 7d | **0.32%** |
| CPU maximo 7d | **26.18%** (spike pontual) |
| Compute Optimizer | OVER_PROVISIONED -> r7g.large |

**Diagnostico:** Usa 0.01 dos 4 vCPUs em media. Ate o spike de 26% caberia em um t4g.medium com burst. Nao e gerenciado por Karpenter (standalone EC2).

**Acao:** Migrar para t4g.small ou t4g.medium (Graviton, burstable).

* m7g.xlarge sa-east-1: \~$0.1608/hr = $117/mo
* t4g.medium sa-east-1: \~$0.0536/hr = $39/mo
* **Economia: \~$78/mo**

#### ACHADO CRITICO #3: Nodes t3a.medium em PROD esgotando CPU credits

Multiplos nodes de prod (karpenter-prod pool) atingem **90-99% de CPU max**:

| Node | Avg CPU | Max CPU |
|----|----|----|
| ip-10-0-1-139 (t3a.medium) | 26.67% | **98.89%** |
| ip-10-0-8-117 (t3a.medium) | 38.41% | **99.91%** |
| ip-10-0-15-252 (t3a.medium) | 24.13% | **99.35%** |
| ip-10-0-24-43 (t3a.medium) | 27.27% | **98.00%** |
| ip-10-0-1-125 (t3a.medium) | 30.19% | **90.11%** |
| ip-10-0-14-209 (t3a.medium) | 30.16% | **91.63%** |

**Diagnostico:** Instancias burstable (t3a) em prod com carga sustentada > 20% avg esgotam CPU credits e passam a ser throttled. O custo de CPU credits ($50.69/mo no billing) confirma isso. Nodes de prod nao devem usar instancias burstable.

**Acao:** No NodePool `general-karpenter-prod`, excluir familia `t` e usar apenas `m`, `c`, `r`:

```yaml

requirements:
  - key: karpenter.k8s.aws/instance-family
    operator: In
    values: ["m6a", "m7g", "c6a", "c7g", "m8g", "c8g"]  # sem T-series
  - key: karpenter.sh/capacity-type
    operator: In
    values: ["spot", "on-demand"]  # habilitar spot!
```

**Economia:** $50/mo em CPU credits + performance improvement + spot savings

#### ACHADO CRITICO #4: Nenhum Spot Instance em uso

**Todos os 39 nodes sao on-demand.** Karpenter esta configurado mas sem Spot habilitado nos NodePools.

Com Spot em sa-east-1 (desconto tipico de 60-75% vs on-demand) e diversificacao de 15+ instance types:

| Pool | Nodes | Spot Elegivel? | Economia Spot |
|----|----|----|----|
| karpenter-system (13 nodes) | m6a.large, c6a.large/xlarge | Sim (stateless) | \~$200-400/mo |
| karpenter-prod (10 nodes) | t3a.medium/xlarge | Sim (com fallback on-demand) | \~$300-600/mo |
| karpenter-staging (8 nodes) | t3a, t4g | **Sim (100% spot)** | \~$150-300/mo |
| karpenter-data (4 nodes) | m6g.large, r6g.2xlarge | Parcial (stateful cauteloso) | \~$50-100/mo |
| cluster-services (2 nodes) | t3a.large (managed) | Nao (critico) | $0 |

**Economia total estimada com Spot:** $700-1,400/mo

**Pre-requisitos:**


1. Diversificar instance types (minimo 15) em cada NodePool
2. Habilitar `SpotToSpotConsolidation` feature gate
3. Instalar AWS Node Termination Handler
4. Configurar disruption budgets por pool
5. Build de container images multi-arch (amd64 + arm64) para usar Graviton em spot

#### ACHADO #5: Graviton nao esta sendo utilizado nos pools system/prod

Os pools `system` e `prod` usam exclusivamente x86 (c6a, m6a, t3a). O pool `data` ja usa Graviton (m6g, r6g, t4g) corretamente.

**Graviton4 (c8g, m8g, r8g) esta disponivel em sa-east-1 desde Dez/2025** com \~20% de economia vs x86 equivalente.

**Acao:** Adicionar familias Graviton nos NodePools:

```yaml
# Para system e prod pools
- key: karpenter.k8s.aws/instance-family
  operator: In
  values: ["m6a", "m7g", "c6a", "c7g", "m8g", "c8g", "r7g", "r8g"]
```

**Pre-requisito:** Container images precisam ser multi-arch. Verificar com o time se o build pipeline ja suporta arm64.

**Economia estimada:** $200-400/mo (20% sobre compute dos pools que migrarem)

#### ACHADO #6: Sem visibilidade de memoria (CWAgent ausente)

Nenhuma metrica `mem_used_percent` encontrada no CloudWatch. **Estamos voando cegos sobre memoria** - especialmente critico para nodes m6a/r6g que sao memory-optimized.

**Acao:** Instalar CloudWatch Agent ou Prometheus node-exporter (provavelmente ja roda no cluster via Grafana stack) e alimentar Karpenter com pod resource requests realistas.

#### Resumo EC2/EKS Completo

| Node | Tipo | CPU Avg | CPU Max | Status | Acao |
|----|----|----|----|----|----|
| cluster-services (1) | t3a.large | 14% | 25% | OK | Manter |
| cluster-services (2) | t3a.large | 58% | 94% | HOT | Monitorar |
| bastion | t2.micro | 1% | 37% | OK | Manter |
| **c6a.12xlarge (system)** | c6a.12xlarge | **3%** | **7%** | **WASTE** | **Limitar tamanho** |
| **openclaw** | m7g.xlarge | **0.3%** | 26% | **WASTE** | **Downsize p/ t4g.medium** |
| r6g.2xlarge (data) | r6g.2xlarge | 5% | 90% | OK | Manter (spikes justificam) |
| m6g.large (data) x3 | m6g.large | 5-8% | 16-50% | OVER | Avaliar r6g.medium |
| t4g.xlarge (staging) | t4g.xlarge | 10% | 58% | OVER | Permitir downsize por Karpenter |
| m6a.large (system) x7 | m6a.large | 12-24% | 27-73% | OK | Candidatos a Graviton |
| c6a.large/xlarge (system) x4 | c6a.\* | 10-12% | 29-53% | OK | Candidatos a Graviton + Spot |
| t3a.medium (prod) x8 | t3a.medium | 24-39% | **67-100%** | **BURST RISK** | **Trocar por m6a/c6a** |
| t3a.medium (staging) x5 | t3a.medium | 27-38% | 70-100% | BURST RISK | Spot + non-burstable |
| t3a.xlarge (prod) x2 | t3a.xlarge | 19-23% | 95-99% | **BURST RISK** | Trocar por m6a.xlarge |


---

### 1.2 RDS PostgreSQL - Analise de Utilizacao Real

#### ACHADO CRITICO #7: sapron-prd-postgres SUB-PROVISIONADO

| Metrica | Valor |
|----|----|
| Instancia | sapron-prd-postgres (db.t4g.medium, 4GB RAM, 80GB storage) |
| CPU medio | **13.62%** |
| CPU maximo | **99.51%** |
| Conexoes media | 55.2 |
| Conexoes maximo | 121 |
| Freeable Memory avg | 1,796 MB (de 4,096 MB) |
| Storage usado | 11.6 GB de 80 GB (14.5%) |
| Compute Optimizer | **UNDERPROVISIONED -> db.m7g.large** |

**Diagnostico:** Database de producao em instancia burstable (T-class) atingindo 99.5% CPU. Quando esgota CPU credits, queries ficam lentas, timeouts aumentam, e a aplicacao inteira degrada. **Isso e um risco de producao, nao apenas custo.**

**Acao URGENTE:**

```bash
# Migrar para m7g.large (Graviton3, dedicated CPU, nao burstable)
aws rds modify-db-instance --profile apps --region sa-east-1 \
  --db-instance-identifier sapron-prd-postgres \
  --db-instance-class db.m7g.large \
  --apply-immediately
```

**Custo:** db.t4g.medium (\~$59/mo) -> db.m7g.large (\~$95/mo). **Aumento de $36/mo** mas elimina o risco de throttling. A alternativa seria db.m6g.large (\~$87/mo).

**Storage:** 80 GB alocados, 11.6 GB usados. RDS nao permite reduzir storage. Para futuras instancias, alocar mais conservadoramente com autoscaling habilitado.

#### ACHADO CRITICO #8: seaflow-db COMPLETAMENTE MORTO

| Metrica | Valor |
|----|----|
| Instancia | seaflow-db (db.t3.micro, 1GB RAM, 20GB gp2) |
| Conexoes 7 dias | **ZERO** |
| CPU medio | 6.67% (apenas overhead do PostgreSQL) |
| Storage | gp2 (nao gp3) |
| Encriptacao | **NAO** (unica instancia sem encriptacao) |
| Backup retention | 1 dia apenas |

**Diagnostico:** Nenhuma conexao em 7 dias. O custo de CPU de 6.67% e puramente o processo PostgreSQL rodando idle. Esta instancia e um artefato morto.

**Acao:**


1. Verificar com o time se alguem usa "seaflow"
2. Se ninguem usa: criar snapshot final e deletar
3. Se alguem usa esporadicamente: considerar parar a instancia e usar on-demand start

```bash
# Criar snapshot antes de deletar

aws rds create-db-snapshot --profile apps --region sa-east-1 \
  --db-instance-identifier seaflow-db \
  --db-snapshot-identifier seaflow-db-final-backup-2026-04-02

# Apos confirmacao, deletar

aws rds delete-db-instance --profile apps --region sa-east-1 \
  --db-instance-identifier seaflow-db \
  --skip-final-snapshot  # ja fizemos snapshot acima
```

**Economia:** \~$12-15/mo

#### ACHADO #9: stg-postgres SOBRECARREGADO

| Metrica | Valor |
|----|----|
| Instancia | stg-postgres (db.t4g.medium) |
| CPU maximo | **99.54%** |
| Conexoes media | **124.3** (mais que qualquer DB de producao!) |
| Storage | 53% utilizado (10.6 GB de 20 GB) |

**Diagnostico:** O banco de staging tem MAIS conexoes que producao. Isso sugere que todos os ambientes stg/dev compartilham este unico banco. Nao e um problema de custo, mas de estabilidade de staging. Se staging fica lento, todos os devs sao afetados.

**Acao:** Nao reduzir - monitorar. Se necessario, considerar separar bancos por time ou fazer scheduling fora de horario.

#### ACHADO #10: reservas-prd-postgres-replica subutilizada

| Metrica | Valor |
|----|----|
| Instancia | reservas-prd-postgres-replica (db.t4g.micro) |
| CPU medio | 4.03% |
| CPU maximo | 7.13% |
| Conexoes media | **3.5** |
| Conexoes maximo | 10 |

**Diagnostico:** Apenas 3.5 conexoes em media. Se e usada so para read replicas de queries analiticas leves, esta OK. Mas se nao e usada ativamente, pode ser removida.

**Acao:** Confirmar com o time se esta replica e necessaria. $12/mo nao justifica investigacao profunda.

#### Resumo RDS Completo

| Instancia | Classe | CPU Avg/Max | Conex. Avg | Mem Livre | Storage Livre | Veredicto |
|----|----|----|----|----|----|----|
| reservas-prd-postgres | db.t4g.small | 4.6/37% | 70.6 | 399MB/2GB | 16.3/20GB | **OK** |
| reservas-prd-replica | db.t4g.micro | 4.0/7% | 3.5 | 86MB/1GB | 16.5/20GB | Questionar necessidade |
| **sapron-prd-postgres** | db.t4g.medium | **13.6/99.5%** | 55.2 | 1.8GB/4GB | 68.4/80GB | **UPGRADE URGENTE** |
| sapron-prd-replica | db.t4g.medium | 11.7/83% | 23.7 | 1.9GB/4GB | 50.7/62GB | Monitorar |
| **seaflow-db** | db.t3.micro | 6.7/51% | **0** | 197MB/1GB | 18.9/20GB | **DELETAR** |
| stg-postgres | db.t4g.medium | 4.6/99.5% | 124.3 | 1.9GB/4GB | 9.4/20GB | Sobrecarregado |
| tools-postgres | db.t4g.small | 4.6/12% | 39.2 | 402MB/2GB | 25/30GB | OK |


---

### 1.3 ElastiCache Valkey - Analise de Utilizacao Real

#### ACHADO CRITICO #11: reservas-valkey-prd EVICTING KEYS

| Metrica | Valor |
|----|----|
| Cluster | reservas-valkey-prd-001 (cache.t4g.small, \~1.37GB) |
| CPU medio | 3.22% |
| **Memoria media** | **94.07%** |
| **Evictions 7d** | **82,290** (\~11,750/dia) |
| Items medio | 134,987 |

**Diagnostico:** Cache operando em memoria critica. 82k evictions em 7 dias significa que chaves uteis estao sendo expulsas para dar espaco a novas. Isso degrada a taxa de cache hit e faz a aplicacao bater mais no banco (sapron-prd-postgres, que ja esta sub-provisionado). **Esses dois problemas se retroalimentam.**

**Acao URGENTE:**

```bash
# Upgrade para cache.t4g.medium (3 GB) ou cache.r7g.large (13.07 GB) se crescer mais
# Nota: ElastiCache Valkey t4g.small -> t4g.medium requer criacao de novo cluster
# ou modification se for replication group
```

**Custo:** t4g.small (\~$24/mo) -> t4g.medium (\~$48/mo). **Aumento de $24/mo** mas essencial para performance.

#### ACHADO #12: Caches com utilizacao trivial

| Cluster | Tipo | CPU | Mem% | Items | Evictions | Veredicto |
|----|----|----|----|----|----|----|
| **reservas-valkey-prd** | t4g.small | 3.2% | **94%** | 134,987 | **82,290** | **UPGRADE** |
| reservas-valkey-stg | t4g.micro | 2.0% | 62% | 44,039 | ? | Monitorar |
| sapron-valkey-prd | t4g.small | 2.4% | 1.9% | 27,430 | 0 | OK |
| sapron-valkey-stg | t4g.micro | 2.4% | 1.9% | 3,418 | 0 | OK |
| wallet-valkey-prd | t4g.small | 2.3% | 0.9% | 451 | 0 | **OVER** (micro bastaria) |
| wallet-valkey-stg | t4g.micro | 2.2% | 1.7% | \~0 | 0 | Quase vazio |
| openpanel-valkey-prd | t4g.micro | 2.9% | 2.1% | 106 | 0 | OK |
| fluxo-cadencia | t4g.micro | 2.8% | 5.4% | **8** | 0 | **8 items no cache?!** |

**Nota sobre fluxo-cadencia:** Um cluster ElastiCache para armazenar 8 items custa \~$12/mo. Avaliar se pode ser substituido por cache in-memory da aplicacao.

**Nota sobre wallet-valkey-prd:** 451 items e 0.9% memoria em t4g.small. Um t4g.micro bastaria.


---

### 1.4 Lambda Functions - Artefatos Mortos

#### 42 Lambdas MORTAS em prd-lake (0 invocacoes em 30 dias)

Muitas com nomes que indicam abandono:

* `terste_scraper_DELETAR` (typo + "DELETAR" no nome)
* `teste-dataQualityReport`, `test-LambdaMAPE`, `test-rawfeesstays`...
* `PASSAR_PRA_CICD_slack_send_booking_queries` (nunca migrou)
* `scraper_teste`, `teste-apagavel-dead-listings`
* APIs antigas: `price_av_api`, `diagnostico_faturamento_api`, `operacao-monitoramento-imovel-api`

**Custo direto:** Lambdas paradas custam $0. MAS cada uma cria log groups no CloudWatch que acumulam storage indefinidamente.

**Acao:** Listar e comunicar ao time. Deletar apos confirmacao.

```bash
# Listar todas as mortas com ultimo deploy

aws lambda list-functions --profile prd-lake --region us-west-2 \
  --query 'Functions[?LastModified<`2025-06-01`].{Name:FunctionName,Last:LastModified,Runtime:Runtime}' \
  --output table
```

#### 1 Lambda morta em nekt

* `nekt-a6bb943b-dbb3-4775-b4e5-8153ddd225d1-webhook` (webhook antigo)


---

## PARTE 2: DEEP DIVE POR CONTA

### 2.1 Nekt - O Misterio dos $2,030/mo Revelado

| Servico | Custo | % |
|----|---:|---:|
| **EMR Serverless (Spark ARM)** | **$1,114.54** | 55% |
| S3 (nekt-lakehouse 8.5TB) | $376.47 | 19% |
| Tax | $247.17 | 12% |
| EC2-Other (NAT instance + EBS) | $207.00 | 10% |
| ECS/Fargate (nekt-mcp-server) | $22.26 | 1% |
| Outros | $63 | 3% |

#### EMR Serverless ($1,114/mo)

* 100% ARM/Graviton (bom!)
* $711 em vCPU-hours + $400 em memory-hours
* EMR Serverless nao suporta Spot, entao nao ha desconto adicional possivel por essa via
* **Alternativa:** Migrar para EMR on EKS (reusa cluster existente, habilita Spot para executors)
  * Driver on-demand + executors Spot = **40-60% economia** = $450-670/mo
  * MAS: requer refatoracao dos jobs e experiencia com Spark on K8s
  * **Recomendacao:** Manter EMR Serverless por ora, avaliar migracao no medio prazo
* **Alternativa 2:** Compute Savings Plan cobre EMR Serverless. Com SP, economia de \~20-30% = $220-335/mo

#### S3 nekt-lakehouse (8.5 TB, 13.2M objetos)

* Sem lifecycle policy detectada
* Tudo em Standard Storage
* **Acao:** Habilitar S3 Intelligent-Tiering
  * 8.5 TB Standard: \~$195/mo
  * Com IT (estimando 40% infrequent, 20% archive instant): \~$120/mo
  * **Economia: \~$75/mo**

#### NAT Instance (c6gn.medium)

* Nekt usa um EC2 self-managed como NAT ($207/mo em data transfer + compute)
* **Acao:** Avaliar VPC Gateway Endpoint para S3 (trafego EMR -> S3 passando pelo NAT e puro desperdicio)
  * S3 Gateway Endpoint: **GRATIS**
  * Economia estimada: **$50-100/mo** dependendo do % de trafego NAT que e para S3

### 2.2 Apps - O Gigante ($5,004/mo)

| Servico | Custo | Comentario |
|----|---:|----|
| EC2 Compute (EKS nodes) | \~$1,700 | Spot + Graviton = $700-1,400 economia |
| EC2-Other (NAT $772, EBS $446, snaps $162) | \~$2,073 | VPC Endpoints + EBS cleanup |
| S3 ($431) | $431 | **Tempo traces 10.3TB!!** |
| RDS | \~$330 | sapron upgrade + seaflow delete |
| CloudWatch | \~$310 |    |
| SQS | \~$300 | Essencial, nao otimizar |
| ECS (cadencia) | \~$257 |    |
| ElastiCache | \~$111 | reservas upgrade |

#### ~~ACHADO #13: Grafana Tempo Traces~~ (CORRIGIDO - JA GERENCIADO)

> **CORRECAO:** O bucket `general-cluster-grafana-tempo-traces-sa-east-1` (10.3 TB) **ja tem lifecycle de 14 dias de expiracao**. Os 10.3 TB representam apenas 2 semanas de dados (\~740 GB/dia de traces).

Isso levanta outra questao: **740 GB/dia de traces e um volume muito alto**. Pode valer a pena revisar:

* Sampling rate do Tempo (reduzir de 100% para 10-25% em endpoints de alta frequencia)
* Quais servicos/namespaces estao gerando mais traces
* Se todos os traces precisam de 14 dias de retencao

A $280/mo em storage, se reduzir sampling para 25% = **economia de \~$210/mo**. Mas isso e uma decisao de observabilidade, nao puramente de custo.

#### ~~Grafana Loki Logs~~ (CORRIGIDO - JA GERENCIADO)

> **CORRECAO:** Loki logs (212 GB) ja tem lifecycle: 30d -> Standard-IA, 90d -> Glacier. Corretamente configurado.

#### Sapron Files - 468 GB

* `sapron-files-prd`: 468 GB de arquivos da aplicacao
* Verificar se todos sao necessarios ou se versoes antigas podem ser movidas

### 2.3 PRD-Lake ($1,014/mo) - Data Pipeline

**Breakdown S3 (maior custo):**

| Bucket | Tamanho | Lifecycle | Acao |
|----|----|----|----|
| seazone-raw-data-backup | 1,307 GB | Glacier rule **DISABLED** | **HABILITAR** |
| aws-glue-assets | 413 GB | Nenhum | Expirar > 30 dias |
| brlink-seazone-enriched-data | 276 GB | IT habilitado | OK |
| brlink-seazone-clean-data | 163 GB | IT habilitado | OK |
| seazone-data-delivery | 124 GB | **Nenhum** | Adicionar lifecycle |
| test-anomaly-analysis | 72 GB | ? | **Dados de teste?** |
| seazone-data-sync-destination | ? | ? |    |
| aws-athena-query-results | 37 GB | ? | **Expirar > 7 dias** |
| databricks-poc-rfb | 19 GB | ? | **POC - deletar?** |
| sagemaker-blockdetection | 15 GB | ? |    |
| brlink-seazone-historicos-temp | 13 GB | 1d (PanoramaMKT) | Parcial |

**Acoes de alto impacto:**


1. **Habilitar lifecycle no seazone-raw-data-backup** (1.3TB): A regra Glacier IR para o prefixo `historic/` esta DESABILITADA.

```bash
# Verificar regras atuais

aws s3api get-bucket-lifecycle-configuration --profile prd-lake \
  --bucket seazone-raw-data-backup
# Habilitar a regra existente (editar Status de "Disabled" para "Enabled")
```

Economia: \~$30-50/mo


2. **Limpar aws-glue-assets (413 GB):** Esses sao JARs, logs e artifacts de Glue jobs. A maioria e descartavel.

```bash

aws s3api put-bucket-lifecycle-configuration --profile prd-lake \
  --bucket aws-glue-assets-011528361483-us-west-2 \
  --lifecycle-configuration '{
    "Rules": [{
      "ID": "cleanup-old-assets",
      "Status": "Enabled",
      "Filter": {},
      "Expiration": {"Days": 30}
    }]
  }'
```

Economia: \~$8-10/mo


3. **Expirar Athena query results (37 GB):**

```bash

aws s3api put-bucket-lifecycle-configuration --profile prd-lake \
  --bucket aws-athena-query-results-us-west-2-011528361483 \
  --lifecycle-configuration '{
    "Rules": [{
      "ID": "expire-athena-results",
      "Status": "Enabled",
      "Filter": {},
      "Expiration": {"Days": 7}
    }]
  }'
```


4. **Investigar** `**test-anomaly-analysis**` **(72 GB)** e `databricks-poc-rfb` (19 GB) - provavelmente dados de POC que podem ser deletados.

**Glue Jobs ($390/mo org-wide):**

* 67 jobs em prd-lake us-west-2 com workers G.1X, G.2X, G.4X
* Nenhum usa **Glue Flex** (34% mais barato)
* Jobs nao-criticos (nightly ETL, backfills) devem migrar para Flex

**Acao Glue Flex:**

```bash
# Para cada job nao-critico, modificar execution class

aws glue update-job --profile prd-lake --region us-west-2 \
  --job-name "BookedOnFullRefreshSeazone-7Mw1RnRmSBE3" \
  --job-update '{"ExecutionClass": "FLEX"}'
```

Economia estimada: \~$130/mo (34% de $390)

### 2.4 Seazone Technology ($860/mo) - Sem Profile Direto

Breakdown via Cost Explorer:

| Servico | Custo |
|----|---:|
| ECS | $232 |
| VPC | $172 |
| EC2-Other | $97 |
| CloudWatch | $96 |
| EC2 Compute | $89 |
| Tax | $105 |

**VPC a $172/mo** fortemente sugere NAT Gateways (possivelmente 2-3). Mesma oportunidade de VPC Endpoints.

**Acao:** Obter acesso a esta conta para auditoria completa. Potencial de $50-100/mo em economia so com VPC Endpoints.

### 2.5 Dev-Lake ($191/mo) - Crescimento de 127%

| Servico | Custo | Acao |
|----|---:|----|
| Glue | $82 | **181 jobs duplicados - limpar stacks** |
| S3 | $61 | **100 buckets de stacks velhas** |
| Tax | $23 |    |
| AWS Config | $11 | **Desabilitar** |
| CloudTrail | $9 | **Reduzir para free tier** |

**Causa raiz:** Cada feature branch cria uma stack CloudFormation com 8-10 Glue jobs e buckets. As stacks nunca sao deletadas apos merge.

**Acao preventiva:** Implementar cleanup automatico:

```bash
# Script para listar stacks com mais de 90 dias sem update

aws cloudformation list-stacks --profile dev-lake --region us-west-2 \
  --stack-status-filter CREATE_COMPLETE UPDATE_COMPLETE \
  --query 'StackSummaries[?LastUpdatedTime<`2026-01-01`].StackName' --output text
```

### 2.6 Dev-Sirius ($109/mo)

| Servico | Custo | Acao |
|----|---:|----|
| AWS Config | $31 | **Desabilitar** |
| CloudTrail | $18 | **Reduzir** |
| Lambda | $16 | OK |
| S3 | $13 | 112 buckets de stacks velhas |
| Glue | $9 | OK (4 jobs apenas) |

### 2.7 PRD-Sirius ($282/mo) - Serverless Puro

| Servico | Custo |
|----|---:|
| Lambda | $134 |
| S3 | $60 |
| Athena | $47 |
| Tax | $34 |
| Glue | $5 |

**Sem recursos para otimizar** significativamente. Lambda e Athena sao pay-per-use. Possivel economia via Athena query optimization (scan menos dados) ou Lambda right-sizing de memoria, mas ROI baixo.


---

## PARTE 3: ESTRATEGIAS DE VANGUARDA

### 3.1 Karpenter + Spot (Impacto: $700-1,400/mo)

**O que muda:** Hoje todos os 39 nodes EKS rodam on-demand. Com Spot habilitado nos NodePools e diversificacao de 15+ instance types, staging pode rodar 100% Spot, prod com 50-70% Spot, e system com 30-50% Spot.

**Referencia:** Tinybird cortou custos AWS em 20% overall e ate 90% em workloads CI/CD usando EKS + Karpenter + Spot. Media da industria e 30-60% de economia em compute.

**Disruption Budgets recomendados:**

```yaml
# Prod - conservador

disruption:
  budgets:
    - nodes: "20%"
    - nodes: "0"
      schedule: "0 9-18 * * MON-FRI"  # sem disruption em horario comercial

# Staging - agressivo

disruption:
  budgets:
    - nodes: "50%"

# System - moderado

disruption:
  budgets:
    - nodes: "30%"
```

### 3.2 Graviton4 em sa-east-1 (Impacto: $200-400/mo)

Disponivel desde Dez/2025: **c8g, m8g, r8g**. \~20% mais barato que x86 com \~30% mais performance.

**Roadmap de adocao:**


1. Build pipeline multi-arch (amd64 + arm64)
2. Testes em staging com Graviton
3. Adicionar ao NodePool como preferencia
4. Karpenter migrara automaticamente para Graviton quando for mais barato

### 3.3 Glue Flex (Impacto: $130/mo)

34% mais barato que Standard. Ideal para jobs nao-criticos (nightly ETL, backfills, enrichment). Jobs podem ser pre-empted e restartados, entao so para workloads idempotentes.

**Jobs candidatos em prd-lake:**

* Todos os `*FullRefresh*` (ja sao batch pesados)
* `ConsolidacaoArquivos` (batch de consolidacao)
* `MonthlyFat*`, `MonthlyRevenue*`, `MonthlyOccupancy*` (monthly batch)
* `airbnb_cleaning_fee_*`, `enrich-listings`, `reconcile-blocks`

### 3.4 Compute Savings Plans (Impacto: $600-800/mo)

**Situacao atual:** SP existentes cobrem 63-68% do spend elegivel. $384-451/mo roda on-demand puro. RIs cobrem 9.4% das horas.

**Recomendacao:** Compute Savings Plan de 1 ano, No Upfront.

* Cobre EC2, Fargate, Lambda E EMR Serverless
* Commitment de \~$3-4/hr adicional = \~$2,200-2,900/mo de on-demand equivalent
* Desconto de \~30% = **$660-870/mo de economia**
* Flexibilidade total: se mudar de instancia, regiao, ou servico, o SP continua valido

```bash
# Ver recomendacoes atuais

aws ce get-savings-plans-purchase-recommendation --profile manager \
  --savings-plans-type COMPUTE_SP --term-in-years ONE_YEAR \
  --payment-option NO_UPFRONT --lookback-period-in-days SIXTY_DAYS
```

**IMPORTANTE:** Fazer DEPOIS de implementar Spot, porque Spot reduz o baseline on-demand e altera o commitment ideal.

### 3.5 EMR on EKS (Impacto Futuro: $450-670/mo)

A Nekt gasta $1,114/mo em EMR Serverless. Migrar para EMR on EKS reutilizaria o cluster EKS existente, habilitaria Spot para executors, e eliminaria o overhead do EMR Serverless.

**Pros:** 40-60% economia, reusa infra existente, Spot para executors **Contras:** Complexidade de setup, requer expertise Spark on K8s **Recomendacao:** Medio prazo (Q3 2026). Priorizar Spot + SP primeiro.

### 3.6 VPC Endpoints + NAT (CORRIGIDO)

> **CORRECAO:** A conta apps JA POSSUI 9 VPC Endpoints (S3 GW+IF, ECR api+dkr, STS, SQS, SSM, EC2, DynamoDB GW). Os $662/mo de NAT data processing sao trafego para a **internet publica**, nao para servicos AWS. Nao ha mais endpoints a criar nesta conta.

**Oportunidade remanescente - conta Nekt:** A conta nekt so tem S3 Gateway Endpoint. O NAT instance (c6gn.medium, $207/mo) processa trafego para ECR, CloudWatch, etc. Adicionar endpoints:

* ECR (api + dkr): \~$14.40/mo
* CloudWatch Logs: \~$7.20/mo
* STS: \~$7.20/mo **Economia estimada na nekt:** $30-80/mo (parcela do $207 que e para servicos AWS)

**Para apps (NAT $662/mo em internet traffic):** Investigar o que esta gerando tanto trafego de saida para internet. Possivelmente:

* Webhooks para servicos externos
* Scrapers/crawlers
* APIs de terceiros
* Container image pulls de registries nao-AWS

Otimizacao requer analise de VPC Flow Logs para identificar destinos.

### 3.7 CAST AI vs Kubecost (Decisao Estrategica)

| Ferramenta | O que faz | Custo | Savings |
|----|----|----|----|
| **Kubecost** | Visibilidade + recomendacoes | Free tier disponivel | 10-25% (manual) |
| **CAST AI** | Automacao completa (spot, rightsizing, bin-packing) | % do savings | 50-75% |
| **AWS Compute Optimizer** | Recomendacoes de rightsizing | Gratis | 10-25% |

**Recomendacao para Seazone:** Comecar com Kubecost (free) para visibilidade de custo por namespace/workload. Se o time nao tiver bandwidth para otimizacao manual continua, avaliar CAST AI. Mas **CAST AI conflita com Karpenter** - escolher um ou outro.

### 3.8 EKS Version - Evitar Extended Support Surcharge

EKS cobra **$0.60/hr ($438/mo)** por cluster em Extended Support (versoes K8s < 1.29). Standard Support custa $0.10/hr ($73/mo).

```bash
# Verificar versao atual

aws eks describe-cluster --profile apps --region sa-east-1 \
  --name general-cluster --query 'cluster.version' --output text
```

**Se estiver em versao < 1.29, upgrade urgente para evitar $365/mo adicional.**


---

## PARTE 4: PLANO DE ACAO CONSOLIDADO

### Semana 1 (Quick Wins - $320-420/mo)

| # | Acao | Economia | Risco | Comando/Nota |
|----|----|---:|----|----|
| 1 | Deletar 41 EBS orfaos (apps sa-east-1, 1.6TB) | $130/mo | Baixo | Snapshot dos >= 100GB antes |
| 2 | Retention CW Logs nekt 30d (1,147 log groups, 68GB) | $75/mo | Baixo | Script batch na secao 1B |
| 3 | Habilitar lifecycle seazone-raw-data-backup (1.3TB) | $30-50/mo | Baixo | Regra Glacier IR ja existe, so habilitar |
| 4 | Lifecycle aws-glue-assets (413GB) + athena-results (37GB) | $15/mo | Baixo | Expirar 30d e 7d |
| 5 | Liberar EIP nao-associado us-west-2 | $4/mo | Nulo | 1 comando |
| 6 | Desabilitar AWS Config em dev-lake + dev-sirius | $41/mo | Baixo\* | \*Verificar politica compliance |
| 7 | Reduzir CloudTrail em contas dev | $27/mo | Baixo | Remover data events, manter free trail |
|    | ~~Lifecycle Tempo traces~~ | ~~$180/mo~~ | -- | *JA TEM expiracao 14d* |
|    | ~~VPC Endpoints apps~~ | ~~$400/mo~~ | -- | *JA TEM 9 endpoints* |

### Semana 2 (Rightsizing + Stability - $830-1,300/mo)

| # | Acao | Economia | Risco | Nota |
|----|----|---:|----|----|
| 8 | **Upgrade sapron-prd-postgres -> db.m7g.large** | **+$36/mo** | **URGENTE** | CPU 99.5%, throttling producao |
| 9 | **Upgrade reservas-valkey-prd -> t4g.medium** | **+$24/mo** | **URGENTE** | 82k evictions/semana |
| 10 | **Limitar instance size NodePool system (max 4xlarge)** | **$800-1,200/mo** | Medio | c6a.12xlarge a 3% CPU! |
| 11 | Downsize openclaw m7g.xlarge -> t4g.medium | $78/mo | Baixo | 0.3% CPU avg |
| 12 | Deletar seaflow-db (0 conexoes 7 dias) | $15/mo | Baixo | Snapshot final antes |
| 13 | VPC Endpoints nekt (ECR, CW, STS) | $30-50/mo | Baixo | Reduz trafego NAT instance |
|    | ~~EKS version check~~ | ~~$365/mo~~ | -- | *JA NA v1.33 (Standard Support)* |

### Semana 3 (Spot + Graviton - $700-1,800/mo)

| # | Acao | Economia | Risco | Nota |
|----|----|---:|----|----|
| 14 | Habilitar Spot nos NodePools (staging 100%, prod 50-70%) | $700-1,400/mo | Medio | 15+ instance types, disruption budgets |
| 15 | Adicionar Graviton (m7g/c7g/m8g/c8g) aos NodePools | $200-400/mo | Baixo | Requer container images multi-arch |
| 16 | Remover T-series do NodePool prod | $50/mo + stability | Baixo | Elimina CPU credit exhaustion |
| 17 | Limpar stacks CF stale em dev-lake + dev-sirius | $150/mo | Baixo | Comunicar time 7d antes |

### Mes 2 (Commitments + Pipeline - $600-1,100/mo)

| # | Acao | Economia | Risco | Nota |
|----|----|---:|----|----|
| 18 | Comprar Compute Savings Plan 1yr No Upfront | $600-800/mo | Medio | Fazer DEPOIS de implementar Spot |
| 19 | Migrar Glue jobs nao-criticos para Flex | $130/mo | Baixo | 34% desconto, jobs idempotentes |
| 20 | S3 Intelligent-Tiering no nekt-lakehouse (prefixo data/) | $75/mo | Baixo | 8.5TB, lifecycle so cobre prefixos auxiliares |
| 21 | Verificar Amazon Q (cancelar se nao usado) | $187/mo | Baixo | Confirmar com equipe primeiro |
| 22 | Auditar conta Seazone Technology (precisa profile) | $50-100/mo? | ? | Obter acesso para auditoria |
| 23 | Avaliar reducao sampling Grafana Tempo (740 GB/dia!) | $210/mo | Medio | Trade-off: observabilidade vs custo |


---

## PARTE 5: TOTAIS CONSOLIDADOS

### Economia por Horizonte (CORRIGIDO pos-validacao)

| Horizonte | Economia Mensal | Economia Anual | % Reducao |
|----|---:|---:|---:|
| Semana 1 (quick wins) | $320-420 | $3,840-5,040 | 3-4% |
| Semana 2 (infra fixes) | $1,150-1,700 | $13,800-20,400 | 10-15% |
| Semana 3 (spot + graviton) | $1,800-3,100 | $21,600-37,200 | 16-28% |
| Mes 2 (commitments + pipeline) | **$2,200-4,200** | **$26,400-50,400** | **20-38%** |

> **Nota:** Reducao de \~$945/mo vs estimativa original por 3 recomendacoes que ja estavam implementadas (VPC Endpoints apps, Tempo lifecycle, EKS version).

### Investimentos Necessarios (custos que AUMENTAM)

| Item | Custo Adicional | Justificativa |
|----|---:|----|
| Upgrade sapron-prd-postgres | +$36/mo | Elimina throttling de producao |
| Upgrade reservas-valkey-prd | +$24/mo | Elimina 82k evictions/semana |
| VPC Endpoints nekt (3 endpoints) | +$29/mo | ROI positivo se >$29 em NAT traffic |
| **Total investimento** | **+$89/mo** |    |

### Economia Liquida Final: **$2,111-4,111/mo ($25,332-49,332/ano)**

> Economia conservadora de 20% e altamente provavel com acoes de baixo risco. Economia agressiva de 38% requer Spot instances + Savings Plans (maior commitment).


---

## PARTE 6: AUTO-CRITICA E REVISAO

### O que este plano NAO cobre:


1. **Otimizacao de queries Athena ($143/mo):** Requer analise dos queries individuais (particoes, formato de dados, compressao). Potencial de 50-80% de reducao com Parquet + partition pruning, mas precisa de engenheiro de dados dedicado.
2. **SQS ($298/mo):** Custo proporcional ao volume de mensagens. Nao ha "desperdicio" - e pay-per-use. Otimizar requer mudanca de arquitetura.
3. **CloudWatch ($369/mo):** Alem da retention de logs, ha custo de metricas custom, dashboards, e alarms. O stack Grafana (Mimir, Loki, Tempo) ja e uma alternativa ao CloudWatch - mas os 10.3 TB de Tempo traces sugerem que a observabilidade precisa de governance de retencao.
4. **CloudFront Security Bundle ($291/mo):** E um commitment anual. Nao pode ser reduzido ate expirar. Verificar data de vencimento para decisao de renovacao.
5. **ECS na Seazone Technology ($232/mo):** Sem profile de acesso, nao consigo auditar.

### Suposicoes que DEVEM ser validadas:

| Suposicao | Como Validar | Risco se Errada |
|----|----|----|
| Containers sao multi-arch (arm64) | `docker manifest inspect <image>` | Graviton nao funciona |
| Workloads toleram interrupcao Spot | Testar em staging primeiro | Downtime em prod |
| seaflow-db e realmente nao usado | Perguntar ao time | Perda de dados |
| Amazon Q nao tem usuarios ativos | Verificar metricas Q Business | Usuarios perdem acesso |
| AWS Config nao e mandatorio em dev | Verificar politica de compliance | Violacao de compliance |
| EKS nao esta em Extended Support | Verificar versao do cluster | Cobra $438/mo vs $73/mo |
| VPC Flow Logs ja estao habilitados | Verificar antes de criar endpoints | Sem visibilidade do trafego NAT |

### Trade-offs importantes aceitos neste plano:


1. **Spot = risco de interrupcao:** Mitigado por Karpenter (failover automatico) + disruption budgets + mix de instance types. Aceitavel para stateless workloads.
2. **Savings Plans = lock de 1 ano:** Mitigado por usar Compute SP (mais flexivel). Mas se a empresa mudar significativamente de stack, o commitment pode ficar subutilizado.
3. **S3 Glacier = latencia de acesso:** Dados em Glacier IR tem acesso em milissegundos (diferente do Glacier normal). Aceitavel para traces/backups > 90 dias.
4. **Upgrade do sapron-prd custa mais:** O custo de $36/mo adicional e necessario para estabilidade. Throttling de banco afeta toda a aplicacao Sapron e o custo indireto (incidentes, degradacao) e muito maior.
5. **Karpenter system pool sem 12xlarge:** Se houver um workload que realmente precisa de 48 vCPUs (batch ML, processamento pesado), o limit vai impedir. Validar com o time antes de aplicar.