<!-- title: Cronograma de redução | url: https://outline.seazone.com.br/doc/cronograma-de-reducao-1r4MM9g1Gh | area: Tecnologia -->

# Cronograma de redução

[Gráfico gantt para visualizar Andamento](https://docs.google.com/spreadsheets/d/1VCWz-1Sh7PQzrB4OMPr6FAEwgrmIJs66QdtHdKDwcG4/edit?gid=219602075#gid=219602075)

### Baseline: US$ 10.338/mês — Objetivo: redução de custos


---

### SEMANA 1 — Quick Wins Zero-Risk + Rightsizing Seguro (Fase 1)

*Início: 2026-03-24 | Economia acumulada: US$ 419/mês*

| # | Ação | Conta | Economia | Esforço | Risco |
|----|----|----|----|----|----|
| 1.1 | **Desativar Amazon Q Business** — Starter Index fixo, verificar uso real e desligar | PRD-Lake | US$ 169 | 5 min | Baixo |
| 1.2 | **Desativar CloudWatch S3 Export** — Metric Streams/Log subscriptions redundantes com Loki+Prometheus+Mimir | Applications | US$ 130 | 30 min | Baixo |
| 1.3 | **Implementar EBS Snapshot lifecycle** — reter 7d para non-critical, 30d para DBs | Applications | US$ 40 | 1h | Baixo |
| 1.4 | **Rightsizing Growthbook** — backend minReplicas 8→2, CPU 200m→100m, mem 512Mi→300Mi; frontend CPU 100m→50m | Applications | US$ 18 | 30 min | Baixo |
| 1.5 | **Rightsizing Kubecost** — local-store CPU 1000m→50m, finopsagent CPU 500m→200m, forecasting CPU 200m→50m | Applications | US$ 15 | 30 min | Baixo |
| 1.6 | **Rightsizing OpenPanel** — api CPU 250m→100m, dashboard CPU 250m→50m, worker CPU 250m→100m + ajuste de memória | Applications | US$ 12 | 30 min | Baixo |
| 1.7 | **Fixes urgentes** — reservas-api mem→1Gi, sapron-api mem→700Mi, tempo-distributor mem→1Gi (custo neutro) | Applications | US$ 0 | 30 min | Baixo |
| 1.8 | **Remover S3 Interface Endpoint** — redundante com S3 Gateway já existente | Applications | US$ 22 | 15 min | Baixo |
| 1.9 | **Rightsizing Metabase** — CPU 500m→250m, mem 1500Mi→1200Mi | Applications | US$ 13 | 15 min | Baixo |

**Custo projetado fim da semana 1: US$ 9.919**

> **Nota:** Os itens 1.4-1.9 são rightsizing seguro (uso real < 50% do request) aplicados via GitOps neste repositório. A economia em compute se materializa quando Karpenter consolida nodes (24-72h).


---

### SEMANA 2 — Rightsizing Monitoring Stack + PRD Apps

*Economia acumulada: US$ 741/mês*

| # | Ação | Conta | Economia | Esforço | Risco |
|----|----|----|----|----|----|
| 2.1 | **Migrar t2.large → t4g.medium** — $0.1152/h → $0.0408/h (Graviton, 65% mais barato) | Seazone Tech | US$ 115 | 2h | Médio |
| 2.2 | **Rightsizing Loki** — read CPU 400m→150m, write mem 900Mi→600Mi, caches CPU 500m→100m | Applications | US$ 30 | 1h | Baixo |
| 2.3 | **Rightsizing Tempo** — compactor maxReplicas 10→4, metrics-gen min 4→2 + mem 3Gi→2Gi | Applications | US$ 40 | 1h | Baixo |
| 2.4 | **Rightsizing OTel Collector** — CPU 250m→100m | Applications | US$ 5 | 15 min | Baixo |
| 2.5 | **Rightsizing Prometheus** — mem 6Gi→5Gi | Applications | US$ 10 | 15 min | Baixo |
| 2.6 | **Reduzir VPC Endpoints** — remover EC2 endpoint se Karpenter não depende, avaliar SQS endpoint | Applications | US$ 22 | 2h | Médio |
| 2.7 | **Rightsizing PRD apps** — reservas-worker CPU 800m→250m, reservas-frontend CPU 400m→200m, reservas-worker-user CPU 450m→200m, sapron-frontend min 5→2 — via gitops-reservas/sapron | Applications | US$ 100 | 3h | Baixo |

**Custo projetado fim da semana 2: US$ 9.597**

> **Nota:** Os rightsizing do monitoring (itens 2.2-2.5) devem liberar \~8 vCPU + \~20Gi mem no system NodePool. O rightsizing PRD (item 2.7) libera \~9 vCPU no prod NodePool. Karpenter deve eliminar 5-7 nodes em 24-72h.


---

### SEMANA 3 — SQS + Public IPs + S3 Lifecycle

*Economia acumulada: US$ 1.121/mês*

| # | Ação | Conta | Economia | Esforço | Risco |
|----|----|----|----|----|----|
| 3.1 | **Implementar SQS long-polling** — WaitTimeSeconds=20 nas queues (reduz requests 50-70%) | Applications | US$ 130 | 1 dia | Baixo |
| 3.2 | **Reduzir Public IPs** — migrar Fargate tasks para private subnets, eliminar \~40 IPs em us-west-2 | Seazone Tech | US$ 110 | 1 dia | Médio |
| 3.3 | **Configurar S3 Lifecycle Policies** — Loki→IA 30d/Glacier 90d, Tempo→IA 14d, Mimir→IA 60d | Applications | US$ 100 | 3h | Baixo |
| 3.4 | **Reduzir Loki minReplicas** — write 5→3, read 5→3, backend 5→3 (HPA escala de volta se necessário) | Applications | US$ 28 | 1h | Baixo |
| 3.5 | **Desabilitar loki-canary** — DaemonSet em 37 nodes, pouco valor se Loki está estável | Applications | US$ 12 | 15 min | Baixo |

**Custo projetado fim da semana 3: US$ 9.217**


---

### SEMANA 4 — Topology-Aware Routing + Retention

*Economia acumulada: US$ 1.251/mês*

| # | Ação | Conta | Economia | Esforço | Risco |
|----|----|----|----|----|----|
| 4.1 | **Topology-aware routing no EKS** — configurar preferência same-AZ nos Services K8s | Applications | US$ 50 | 3h | Baixo |
| 4.2 | **Reduzir Loki retention 28d → 14d** — menos dados em S3 | Applications | US$ 50 | 30 min | Médio |
| 4.3 | **Reduzir Tempo block_retention 14d → 7d** — menos traces em S3 | Applications | US$ 30 | 30 min | Médio |
| 4.4 | **Cancelar CloudFront Security Bundle** — solicitar não-renovação do contrato | dotted-SP | US$ 0\* | 1h | Alto |

*\*Economia de US$ 291/mês se materializa na expiração do commitment*

**Custo projetado fim da semana 4: US$ 9.087**


---

### SEMANA 5 — NAT Gateway Consolidação + Glue

*Economia acumulada: US$ 1.601/mês*

| # | Ação | Conta | Economia | Esforço | Risco |
|----|----|----|----|----|----|
| 5.1 | **Consolidar NAT Gateways** — reduzir para 1 NAT em non-prod subnets, ou implementar fck-nat (\~$3/mês) | Applications | US$ 250 | 1 dia | Médio |
| 5.2 | **Migrar Glue jobs para Flex** — mover Standard→Flex (35% mais barato), reduzir Crawlers para daily | PRD-Lake | US$ 100 | 1 dia | Baixo |

**Custo projetado fim da semana 5: US$ 8.737**


---

### ⚡ SEMANAS 6-8 — MIGRAÇÃO DE REGIÃO: sa-east-1 → us-west-2 (Applications)

> **Esta é a ação de maior impacto do plano inteiro: US$ 1.424/mês de economia.**
>
> Migrar o cluster EKS da conta Applications de São Paulo para Oregon gera economia tripla:
>
> * **Instâncias \~25% mais baratas** — preços On-Demand e Spot significativamente menores
> * **Impostos BR eliminados** — 12,2% de tax sobre todos os serviços em sa-east-1 deixa de existir
> * **EBS, NAT, S3, SQS, CloudWatch** — todos 20-30% mais baratos em us-west-2
>
> Sozinha, essa ação representa **50% de toda a meta de redução**.

#### Breakdown da economia por componente

| Componente | sa-east-1 | us-west-2 | Economia |
|----|----|----|----|
| EC2 Compute (Spot + OD) | US$ 1.074 | US$ 805 | US$ 269 |
| EC2-Other (NAT, EBS, DT) | US$ 1.488 | US$ 1.246 | US$ 242 |
| **Tax (impostos BR)** | **US$ 547** | **US$ 0** | **US$ 547** |
| S3 Storage | US$ 307 | US$ 214 | US$ 93 |
| SQS | US$ 267 | US$ 213 | US$ 54 |
| CloudWatch | US$ 248 | US$ 186 | US$ 62 |
| VPC | US$ 190 | US$ 152 | US$ 38 |
| RDS | US$ 124 | US$ 93 | US$ 31 |
| ELB | US$ 67 | US$ 53 | US$ 14 |
| EKS Control Plane | US$ 53 | US$ 73 | -US$ 20 |
| Outros | US$ 134 | US$ 40 | US$ 94 |
| **TOTAL Applications** | **US$ 4.499** | **US$ 3.075** | **US$ 1.424** |

#### Considerações críticas

| Aspecto | Impacto | Mitigação |
|----|----|----|
| **Latência para usuários BR** | +80-120ms (de \~20ms para \~140ms) | Aceitável para apps B2B/internas; CDN (CloudFront) para assets estáticos |
| **Latência para APIs internas** | Crítico se backends em sa-east-1 chamam o EKS | Migrar backends dependentes junto, ou manter proxy |
| **Savings Plans** | SP atual cobre compute em qualquer região | Sem impacto — SP é region-agnostic |
| **Dados S3 existentes** | Precisa migrar buckets ou criar novos | S3 Cross-Region Replication durante transição |
| **RDS** | Criar nova instância em us-west-2 | Snapshot + restore, downtime planejado |
| **Secrets/SSM** | Recriar em us-west-2 | Script de migração automática |
| **DNS/Traefik/NLB** | Recriar NLB em us-west-2, atualizar DNS | Blue-green com weighted routing |
| **cert-manager** | Funciona igual (DNS-01 Cloudflare) | Sem impacto |


---

### SEMANA 6 — Migração de Região: Infraestrutura Base

*Economia acumulada: US$ 1.601/mês (economia da migração se materializa na semana 8)*

| # | Ação | Conta | Economia | Esforço | Risco |
|----|----|----|----|----|----|
| 6.1 | **Provisionar EKS cluster + VPC em us-west-2** — IaC (Terraform/eksctl), mesma topologia de rede e Karpenter NodePools | Applications | US$ 0 | 3 dias | Médio |
| 6.2 | **Configurar S3 Cross-Region Replication** — buckets de Loki, Tempo, Mimir de sa-east-1 → us-west-2 | Applications | US$ 0 | 3h | Baixo |
| 6.3 | **Recriar Secrets/SSM em us-west-2** — script para copiar todos os parâmetros do SSM | Applications | US$ 0 | 3h | Baixo |
| 6.4 | **Deploy ArgoCD + core services** no novo cluster — Traefik, cert-manager, External Secrets, Karpenter | Applications | US$ 0 | 1 dia | Médio |

**Custo projetado fim da semana 6: US$ 8.810** *(custo temporariamente sobe \~$73 pelo novo EKS control plane)*


---

### SEMANA 7 — Migração de Região: Workloads + Dados

*Economia acumulada: US$ 1.601/mês (dois clusters rodando em paralelo)*

| # | Ação | Conta | Economia | Esforço | Risco |
|----|----|----|----|----|----|
| 7.1 | **Migrar monitoring stack** — Prometheus, Grafana, Loki, Tempo, Mimir para us-west-2 | Applications | US$ 0 | 1 dia | Médio |
| 7.2 | **Migrar RDS** — snapshot sa-east-1 → restore us-west-2, janela de manutenção planejada | Applications | US$ 0 | 4h | Alto |
| 7.3 | **Migrar workloads de aplicação** — deploy via ArgoCD no novo cluster | Applications | US$ 0 | 2 dias | Alto |
| 7.4 | **DNS weighted routing** — 10%→50%→100% tráfego para us-west-2 | Applications | US$ 0 | 3h | Médio |

**Custo projetado fim da semana 7: US$ 8.883** *(dois clusters rodando = custo extra temporário)*


---

### SEMANA 8 — Migração de Região: Cutover + Decommission

*Economia acumulada: US$ 3.025/mês*

| # | Ação | Conta | Economia | Esforço | Risco |
|----|----|----|----|----|----|
| 8.1 | **Cutover DNS 100%** — apontar todo tráfego para us-west-2 | Applications | US$ 0 | 2h | Alto |
| 8.2 | **Decommission cluster sa-east-1** — desligar nodes, remover EKS, deletar NAT Gateway, EBS volumes, S3 buckets | Applications | **US$ 1.424** | 1 dia | Alto |

**Custo projetado fim da semana 8: US$ 7.313**

> **Checkpoint:** A conta Applications cai de US$ 4.499 para US$ 3.075/mês. Combinado com as otimizações das semanas 1-5 (incluindo rightsizing do cluster), a economia acumulada é de US$ 3.025.


---

### SEMANA 9 — EMR Serverless + Data Transfer Nekt

*Economia acumulada: US$ 3.475/mês*

| # | Ação | Conta | Economia | Esforço | Risco |
|----|----|----|----|----|----|
| 9.1 | **Habilitar Spot em EMR Serverless** — workers com Spot (até 60% economia em vCPU) | Nekt | US$ 150 | 3h | Médio |
| 9.2 | **Rightsizing EMR workers** — reduzir over-provisioning de memória ($326/mês em memory) | Nekt | US$ 100 | 3h | Médio |
| 9.3 | **Reduzir Data Transfer Regional Nekt** — consolidar EMR+S3 na mesma AZ | Nekt | US$ 200 | 1 dia | Baixo |

**Custo projetado fim da semana 9: US$ 6.863**


---

### SEMANA 10 — Sirius + Início Migração Seazone Technology

*Economia acumulada: US$ 3.575/mês*

| # | Ação | Conta | Economia | Esforço | Risco |
|----|----|----|----|----|----|
| 10.1 | **PRD-Sirius: otimizar Lambda** — consolidar invocações, adicionar partições Athena | PRD-Sirius | US$ 100 | 1 dia | Médio |

**Custo projetado fim da semana 10: US$ 6.763**


---

### SEMANA 11 — Migração Seazone Technology + Governança

*Economia acumulada: US$ 3.875/mês*

| # | Ação | Conta | Economia | Esforço | Risco |
|----|----|----|----|----|----|
| 11.1 | **Migrar workloads ECS → EKS us-west-2** — mover containers do Fargate para o novo EKS | Seazone Tech | US$ 200 | 3 dias | Alto |
| 11.2 | **Eliminar IPs públicos residuais** — deprovisionar IPs não necessários pós-migração | Seazone Tech | US$ 100 | 2h | Baixo |
| 11.3 | **Implementar alertas Cost Anomaly Detection** — threshold US$ 50 por serviço | Manager | US$ 0 | 2h | — |

**Custo projetado fim da semana 11: US$ 6.463**


---

### SEMANA 12 — Cleanup + Ajuste Fino

*Economia acumulada: US$ 4.245/mês*

| # | Ação | Conta | Economia | Esforço | Risco |
|----|----|----|----|----|----|
| 12.1 | **Desligar recursos residuais** Seazone Tech — VPC, EC2, CloudWatch | Seazone Tech | US$ 100 | 1 dia | Médio |
| 12.2 | **EKS pod rightsizing round 2** — ajustar requests/limits com dados do novo cluster | Applications | US$ 150 | 1 dia | Baixo |
| 12.3 | **Prometheus 3→2 replicas** — reduzir com dados do novo cluster | Applications | US$ 20 | 1h | Médio |
| 12.4 | **Marcar não-renovação** dos Savings Plans que ficaram oversized | Commitments | US$ 0 | 30 min | — |

**Custo projetado fim da semana 12: US$ 6.093**


---

## 5. Visão Consolidada — Curva de Redução

```
Semana  | Economia Nova | Acumulada | Custo Projetado | Status
--------|---------------|-----------|-----------------|---------------------------
   0    |       —       |     —     |    US$ 10.338   | Baseline (Fev/26)
   1    |    US$ 419    |  US$ 419  |    US$  9.919   | Quick wins + rightsizing apps
   2    |    US$ 322    |  US$ 741  |    US$  9.597   | Monitoring + t2→t4g + PRD apps
   3    |    US$ 380    | US$ 1.121 |    US$  9.217   | SQS + IPs + S3 + Loki min
   4    |    US$ 130    | US$ 1.251 |    US$  9.087   | Topology routing + retention
   5    |    US$ 350    | US$ 1.601 |    US$  8.737   | NAT consol. + Glue
  -----  -------------- ----------- -----------------  ----------------------------
   6    |       —       | US$ 1.601 |    US$  8.810   | ⚡ Infra us-west-2 (custo sobe)
   7    |       —       | US$ 1.601 |    US$  8.883   | ⚡ Migração workloads (paralelo)
   8    |  US$ 1.424    | US$ 3.025 |    US$  7.313   | ⚡ Cutover + decommission ✅
  -----  -------------- ----------- -----------------  ----------------------------
   9    |    US$ 450    | US$ 3.475 |    US$  6.863   | EMR + Data Transfer Nekt
  10    |    US$ 100    | US$ 3.575 |    US$  6.763   | Sirius
  11    |    US$ 300    | US$ 3.875 |    US$  6.463   | Migração SeaTech
  12    |    US$ 370    | US$ 4.245 |    US$  6.093   | Rightsizing final + cleanup
```

### Cenários ao Final da Semana 12

| Cenário | Fator | Economia Total | Custo Final |
|----|----|----|----|
| **Conservador** | 75% | US$ 3.184 | **US$ 7.154** |
| **Realista** | 90% | US$ 3.821 | **US$ 6.517** |
| **Otimista** | 100% | US$ 4.245 | **US$ 6.093** |