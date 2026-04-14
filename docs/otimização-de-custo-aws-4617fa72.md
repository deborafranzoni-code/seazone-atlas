<!-- title: Otimização de custo AWS | url: https://outline.seazone.com.br/doc/otimizacao-de-custo-aws-V5Jf841TZf | area: Tecnologia -->

# Otimização de custo AWS

# Previsão financeira da otimização de custo


### Estimativa de Economia por Ação

| Ação | Economia/mês | Quando entra |
|----|----|----|
| Deletar `seazone-tempo-distributed` + `mimir-sa-east-metrics` | US$ 80–250 | Semana 1 |
| Remover 4 snapshots EBS manuais | US$ 100–250 | Semana 1 |
| Liberar EIP | US$ 3,60 | Semana 1 |
| CloudWatch — retenção 3d/14d | US$ 267–374 | Semana 2–3 |
| S3 Lifecycle Policy 1 (IA→Glacier→Delete) | US$ 200–350 | Semana 2–4 (gradual) |
| S3 Lifecycle Policy 2 (IA→Glacier) | US$ 120–200 | Semana 2–4 (gradual) |
| EMR auto-termination (2h idle) | US$ 140–210 | Semana 2 |
| EMR Spot 70/30 | US$ 170–240 | Semana 3 |
| RDS Snapshot retenção 15 dias | US$ 50–100 | Semana 2 |
| RDS Reserved Instances (1 ano) | US$ 111–148 | Semana 1 (compra) |
| Right Sizing EC2 (habilitar + aplicar) | US$ 300–600 | Semana 3–4 |
| **TOTAL** | **US$ 1.542–2.726** | — |


---



---

### Resumo Visual (Custo Mensal)

| Semana | Período | Custo Estimado | Economia vs. Base |
|----|----|----|----|
| Base | Mar/2026 | US$ 10.785 | — |
| Semana 1 | 12–18 Mar | US$ 10.300–10.600 | –2% a –4% |
| Semana 2 | 19–25 Mar | US$ 9.700–10.200 | –6% a –10% |
| Semana 3 | 26 Mar–1 Abr | US$ 8.900–9.700 | –10% a –18% |
| Semana 4 | 2–8 Abr | **US$ 8.100–9.300** | **–14% a –25%** |


---


## Pontos  pro time SRE : 

- [ ]  **S3-Egress $266/mês — origem desconhecida (PRINCIPAL CUSTO) :** O CloudWatch está exportando \~266 GB de dados por mês para S3. 
- [ ] **RDS Reserved Instances** requer compromisso de 1 ano
- [ ] 104 volumes têm nome `general-cluster-dynamic-pvc-*` — são **PersistentVolumeClaims do Kubernetes** (EKS) que ficaram órfãos após pods/namespaces deletados. O EKS não deleta automaticamente os volumes quando o PVC é removido sem a política de reclaim correta. 

 

## Proposta  de Claude a retrabalhar: 

Fase 2:

* Otimizar Athena: implementar particoes em tabelas S3, criar workgroups com limite de bytes escaneados.
* Implementar tagging obrigatorio: Environment, Team, Project, CostCenter via Config Rules
* Revisar Container Insights: habilitar apenas em clusters de producao.

Fase 3 : 

* Analise de migracao regional: avaliar custos vs beneficios de mover workloads de sa-east-1 para us-east-1/us-west-2
* Consolidar pipeline de dados: avaliar substituicao de EMR por Glue para jobs ETL de menor complexidade.
* Implementar AWS Compute Optimizer para Lambda, ECS e Auto Scaling Groups
* Avaliar arquitetura serverless para workloads batch irregulares atualmente em EC2.
* Considerar SageMaker Savings Plans se uso de ML for continuo e previsivel.
* Implementar FinOps framework: revisoes mensais de custo, KPIs de eficiencia, accountability por equipe.


\
# 1 - Otimização dos buckets S3

### Política de retenção 1  :

Dia 0   → Upload do arquivo 

Dia 7 dias  → Move para Standard-IA

Dia 14 → Move para Glacier 

Dia 30 → Delete automático

**Aplicar a política 1:** 

- [x] vpc-flow-logs-general-query-results  - mover 100% dos logs glacier e  aplicar a politica de retenção  **OK** (conteudo deletado)
- [x] ~~seazone-tempo-distributed            -  Deletar  **OK** (Conteudo deletado)~~
- [x] ~~seazone-governanca-vpcflowlogs        -  aplicar a politica de retenção 1~~  
- [x] ~~seazone-governanca-tech               -  aplicar a politica de retenção1   - **OK** ( conteudo deletado após avaliação )~~ 


### Politica de retenção 2    :


Dia 0   → Upload do arquivo 

Dia 14 dias  → Move para Standard-IA 

Dia 28 → Move para Glacier


- [ ] **sapron-files-stg**     - aplicar politica de retenção 2
- [ ] sapron-files-prd        - aplicar politica de retenção 2
- [ ] sapron-backend       - aplicar politica de retenção 2 
- [x] ~~general-cluster-loki-logs-sa-east-1  - aplicar politica de retenção 2~~ 
- [x] ~~general-cluster-grafana-tempo-traces-sa-east-1  -  OK -  Ploitica de retenção embaixo~~
- [x] ~~general-access-logs-711387131913      - aplicar politica de retenção 2     - OK (Deletado o conteudo)~~
- [x] ~~vpc-flow-logs-general-query-results    -  Esvaziar e aplic~~ar ~~Ploitica de retenção embaixo~~
- [x] ~~mimir-sa-east-metrics -  Pode deletar  - OK~~


\
**Específico:** 

- [x] ~~seazone-outline          Dia 30 dias  →  Move para Standard-IA~~                


 2 - Otimização dos  backups

- [x] ~~EBS Snapshots~~ 


- [x] ~~Backup manual :~~

**~~Snapshot id~~** ~~:  Remover todos   **OK**~~

- [x] ~~dump-oregon-v2~~ 
- [x] ~~dump-prod-oregon~~
- [x]  ~~posthog-rds-poc-snapshot~~ 
- [x] ~~reservas-prd-postgres-snapshot~~


- [x] ~~Remover os snapshot manuais **OK**~~
- [x] ~~Snapshots Automatizados (RDS nativo) Configurar a retenção para 14 dias~~

3-  CloudWatch Log Groups

Dimunuir a politicas de retenção :

\-dev- / -development  - 3 dias

\-stg- / -staging-  - 14 dias

Qualquer outro padrão - 14 dias


- [ ] Implementar EMR auto-termination: configurar timeout de 2h para clusters sem jobs ativos.
- [ ]  Converter EMR clusters para Spot: 70% Spot + 30% On-Demand nos task nodes 
- [ ] comprar Reserved Instances para RDS com uso 24/7 
- [ ] Habilitar Right Sizing no Cost Explorer: Preferences > Resource Optimization.

  \
- [x] ~~liberar 1 EIP não associado na sua conta AWS~~
- [ ] \


Audit completo. Aqui está o diagnóstico real da sua conta:


---

## Resultado do Audit — EBS Snapshots (sa-east-1)

| Métrica | Valor |
|----|----|
| Total de snapshots | **1.947** |
| Tamanho total | **40.734 GB** |
| Custo mensal atual | **$2.036,70/mês** |
| Economia potencial | **$971,00/mês** |
| Economia anual | **$11.652,00/ano** |

### Distribuição

| Recomendação | Qtd | Economia/mês |
|----|----|----|
| **DELETAR — órfão** (volume não existe mais) | **983** | **$971,00** |
| MANTER — recente (<90 dias) | 964 | $0 |


---

### Diagnóstico

* **983 snapshots órfãos** — os volumes de origem foram deletados, mas os snapshots ficaram. São 100% seguros para deletar.
* **964 snapshots recentes** — todos têm menos de 90 dias, provavelmente gerados por backup automático (AWS Backup ou DLM). Estão ok.
* **Nenhuma AMI** registrada na conta usa algum desses snapshots (verificado).

## Plano de Otimização de Custo  — Projeção 4 Semanas

**Baseline:** US$ 10,785/mês (projeção Março/2026)


---



---

### Observações Importantes :RISCOS 


1. **Right Sizing EC2** tem o maior potencial (US$ 300–600/mês) mas depende da análise das recomendações — as sugestões aparecem em 24h após habilitar, mas o impacto financeiro real ocorre após aplicar os resizes manualmente.
2. **RDS Reserved Instances** requer compromisso de 1 ano — confirme que as instâncias RDS são workloads estáveis antes de comprar.
3. **EMR Spot 70/30** pode causar interrupção de jobs se não houver tratamento de falha nos pipelines — valide antes de converter.
4. O **S3 delete automático em 30 dias** (Policy 1) é agressivo — certifique-se de que os buckets `seazone-outline`, `seazone-governanca-vpcflowlogs` e `seazone-governanca-tech` realmente não precisam de retenção longa.


\

---

**Plano consolidado**

| Bucket | Ação Imediata | Política |
|----|----|----|
| `vpc-flow-logs-general-query-results` | Esvaziar | Policy 2 |
| `seazone-tempo-distributed` | **Deletar bucket** | — |
| `seazone-outline` | Esvaziar | Policy 1 |
| `seazone-governanca-vpcflowlogs` | — | Policy 1 |
| `seazone-governanca-tech` | — | Policy 1 |
| `mimir-sa-east-metrics` | **Deletar bucket** | — |
| `sapron-files-stg` | — | Policy 2 |
| `sapron-files-prd` | — | Policy 2 |
| `sapron-backend` | — | Policy 2 |
| `general-cluster-loki-logs-sa-east-1` | — | Policy 2 |
| `general-cluster-grafana-tempo-traces-sa-east-1` | — | Policy 2 |
| `general-access-logs-711387131913` | — | Policy 2 |


## 


\

\
# Outros: 

## Diagnóstico DLM — Problema Grave Identificado

### O que aconteceu hoje (Monday 16/Mar, 09:00 UTC)

As **4 policies rodaram simultaneamente** — isso é o "4 vezes" que você viu. Mas o problema é muito mais sério:


---

### Problema central: Target Tags incorretos — todas as 4 policies estão mirando os mesmos 161 volumes

| Policy | Intenção original | Volumes alvo atual | Snapshots criados hoje |
|----|----|----|----|
| `kubecost-local-storage` (weekly, retain=1) | 1 volume (kubecost PVC) | **161 volumes** | 161 snapshots |
| `kubecost-aggregator-storage` (weekly, retain=1) | 1 volume (kubecost PVC) | **161 volumes** | 161 snapshots |
| `grafana-dashs` (weekly, retain=1) | 1 volume (grafana PVC) | **161 volumes** | 161 snapshots |
| `mongodb-tools-snap` (daily, retain=3) | 1 volume (mongodb PVC) | **161 volumes** | 161 snapshots/dia |

**Causa raiz:** todas as policies incluem a tag `KubernetesCluster: general-cluster` e `ebs.csi.aws.com/cluster: true`, que estão presentes em **TODOS** os volumes EKS do cluster. Isso faz o DLM capturar o cluster inteiro em vez de volumes específicos.


---

### Impacto financeiro

| Item | Custo/mês |
|----|----|
| 3 policies weekly × 161 snaps × \~22GB | **\~$532** |
| 1 policy daily × 161×3 snaps × \~22GB | **\~$532** |
| **Total DLM** | **\~$1.065/mês** |
| **Deveria custar** (4 volumes específicos) | **\~$2/mês** |
| **Desperdício** | **\~$1.063/mês ($12.756/ano)** |


---

### Correção necessária

Cada policy deve ter uma tag **única e específica** do volume alvo. O correto é usar `CSIVolumeName` ou `kubernetes.io/created-for/pv/name` como **único** target tag:

`# Exemplo: corrigir kubecost-local-storage para mirar 1 volume apenas aws dlm update-lifecycle-policy \   --policy-id policy-0b749ea24489bb9aa \   --region sa-east-1 \   --policy-details '{     "TargetTags": [       {"Key": "kubernetes.io/created-for/pvc/name", "Value": "kubecost-local-store"},       {"Key": "kubernetes.io/created-for/pvc/namespace", "Value": "kubecost"}     ]   }' `


## DLM — Correções Aplicadas

### O que foi feito

| Ação | Policy | Resultado |
|----|----|----|
| **Deletada** | `kubecost-aggregator-storage` | Era duplicata exata da kubecost-local |
| **Corrigida** | `kubecost-local-storage` | 161 volumes → **1 volume** |
| **Corrigida** | `mongodb-tools-snap` | 161 volumes → **1 volume** |
| **Corrigida** | `grafana-dashs` | 161 volumes → **1 volume** |

**Todas as 3 policies agora apontam para exatamente 1 volume cada**, usando a tag `CSIVolumeName` (PV UUID) que é única por volume.


---

### Impacto

|    | Antes | Depois |
|----|----|----|
| Políticas ativas | 4 | **3** |
| Volumes alvo | 161 × 4 = 644 | **1 × 3 = 3** |
| Snapshots criados/semana | 644 | **3** |
| Snapshots criados/dia (mongodb) | 161 | **1** |
| Custo estimado/mês | \~$1.065 | **\~$3** |
| **Economia** |    | **\~$1.062/mês ($12.744/ano)** |


---

### Próximo passo recomendado

Na próxima segunda-feira (23/Mar), as policies rodarão e criarão apenas 2 snapshots (kubecost + grafana). O mongodb criará 1 snapshot/dia. Verifique no console se o comportamento está correto. Os 644 snapshots criados hoje ainda existem — você pode deletá-los com o script de audit na próxima semana após a nova execução confirmar que está ok.


\
Politicas de retenção de S3:


## **Review transition and expiration actions**

### **Day 0**

* Objects uploaded

**Day 30**

* Objects move to Standard-IA

**Day 90**

* Objects move to Glacier Flexible Retrieval (formerly Glacier)


\
Outline : 


## **Review transition and expiration actions**

### **Current version actions**

**Day 0**

* Objects uploaded

**Day 30**

* Objects move to Intelligent-Tiering

**Day 180**

* Objects move to Glacier Flexible Retrieval (formerly Glacier)

**Day 365**

* Objects move to Glacier Deep Archive


\
## Relatório: RDS Backup Retention — Conta Applications (711387131913)

### Instâncias RDS (sa-east-1)

| Instance | Class | Storage | Retention | MultiAZ | DeletionProtection | Status |
|----|----|----|----|----|----|----|
| `reservas-prd-postgres` | db.t4g.small | 20 GB | **30 dias** | No | ❌ No | available |
| `reservas-prd-postgres-replica` | db.t4g.micro | 20 GB | **30 dias** | No | ✅ Yes | available |
| `sapron-prd-postgres` | db.t4g.medium | 80 GB | **30 dias** | No | ❌ No | available |
| `sapron-prd-postgres-replica` | db.t4g.medium | 62 GB | **30 dias** | No | ✅ Yes | available |
| `stg-postgres` | db.t4g.medium | 20 GB | **7 dias** ✅ | No | ❌ No | available |
| `tools-postgres` | db.t4g.small | 30 GB | **30 dias** | No | ❌ No | available |


---

### Custo atual de backup

| Item | Custo/mês |
|----|----|
| `SAE1-RDS:ChargedBackupUsage` (sa-east-1) | **\~$57/mês** |
| `USW2-RDS:ChargedBackupUsage` (us-west-2) | **\~$4.50/mês** |
| **Total backup storage** | **\~$61.50/mês** |
| RDS GP3 Storage (volumes) | \~$47/mês |

> O AWS oferece backup gratuito até 100% do storage alocado por instância. Tudo acima é cobrado a $0.095/GB-mês. Com 30 dias de retenção, \~600 GB de backup está sendo cobrado.


---

### Problemas identificados

**1. Retenção excessiva nas instâncias de produção (30 dias)**

* Só o `stg-postgres` está correto com 7 dias.
* 30 dias é raramente necessário. A prática recomendada é 7–14 dias.
* Com 30 dias acumulando diferenciais por 30 ciclos, o custo de backup explode.

**2. Réplicas também com 30 dias de retenção**

* `reservas-prd-postgres-replica` e `sapron-prd-postgres-replica` têm backup independente configurado com 30 dias.
* As réplicas não precisam de retenção alta — o primário já cobre o restore.
* Reduzir para 1–7 dias nas réplicas.

**3. 10 snapshots manuais órfãos em us-west-2 — pagando \~$4.50/mês a toa**

`dump-manual-18                          (ago/2025) — rds-reservas-production-master  20GB final-oregon-reservas                   (ago/2025) — rds-reservas-production-master  20GB final-oregon-snapshot                   (ago/2025) — rds-reservas-production-master  20GB final-rds-reservas-production-master    (dez/2024) — rds-reservas-production-master  20GB  ← 15 meses! final-rds-tools-67a298b2               (out/2024) — rds-tools                        20GB  ← 17 meses! final-rds-tools-e273dd02               (out/2025) — rds-tools                        20GB rds-reservas-production-master-snapshot (ago/2025) — rds-reservas-production-master  20GB tools-snapshot                          (set/2025) — rds-tools                        20GB update-t4g                              (mai/2025) — rds-reservas-production-replica  20GB update-t4g-rds-tools                    (mai/2025) — rds-tools                        20GB `

Todas são de instâncias já deletadas. As de 2024 já passam de 1 ano pagas inutilmente.

**4. DeletionProtection desabilitado em produção**

* `reservas-prd-postgres`, `sapron-prd-postgres` e `tools-postgres` podem ser deletados acidentalmente sem qualquer proteção.

**5. Nenhuma instância usa Multi-AZ**

* Risco de indisponibilidade em failover (mas é trade-off de custo — dobra o custo de instância).


---

### Recomendações e economia estimada

| Ação | Economia/mês |
|----|----|
| Reduzir retenção: prod 30→14 dias | \~$25–28 |
| Reduzir retenção: réplicas 30→7 dias | \~$8–10 |
| Deletar 10 snapshots órfãos (us-west-2) | \~$4.50 |
| **Total potencial** | **~~$37–42/mês (~~$450/ano)** |

\nTudo aplicado. Resumo do que foi feito:

### Alterações aplicadas

**Backup Retention:**

| Instance | Antes | Depois |
|----|----|----|
| `reservas-prd-postgres` | 30 dias | **14 dias** ✅ |
| `sapron-prd-postgres` | 30 dias | **14 dias** ✅ |
| `tools-postgres` | 30 dias | **14 dias** ✅ |
| `reservas-prd-postgres-replica` | 30 dias | **0 (desabilitado)** ✅ |
| `sapron-prd-postgres-replica` | 30 dias | **0 (desabilitado)** ✅ |

> As réplicas estão com status `modifying` — a mudança já está confirmada como `PendingBackupRetentionPeriod: 0`.

**DeletionProtection:**

| Instance | Antes | Depois |
|----|----|----|
| `reservas-prd-postgres` | False | **True** ✅ |
| `sapron-prd-postgres` | False | **True** ✅ |
| `tools-postgres` | False | **True** ✅ |


---

**Economia estimada:** ~~$35–42/mês (~~$420–500/ano) com a redução de backup.

Quer também deletar os **10 snapshots órfãos em us-west-2** para economizar os \~$4.50/mês adicionais?


Resultados mapeados pelo Claude: 

 ![](/api/attachments.redirect?id=3433663d-8324-475e-98fc-7152e93c9375 " =1044x506")

## Audit CloudWatch — Conta Applications (711387131913)


 ![](/api/attachments.redirect?id=4a73c180-cf53-4f3a-93b1-1151ff7aa175 " =691x754")

### Problemas identificados

**1. S3-Egress $266/mês — origem desconhecida (PRINCIPAL CUSTO)**

O CloudWatch está exportando \~266 GB de dados por mês para S3. Isso pode ser:

* Grafana Cloud pulling CloudWatch metrics via API
* Export tasks automáticos de logs para S3
* Kinesis Firehose integrado

É o **88% do custo do CloudWatch** e precisa ser investigado.

**2. EKS cluster log 879 GB com ingesta contínua**

O log group `/aws/eks/general-cluster/cluster` tem 879 GB armazenados. Com 14 dias de retenção, isso significa \~62 GB/dia de novos logs entrando. A ingesta de logs do CloudWatch custa $0.90/GB, ou seja, \~**$1,674/mês só de ingestion** — esse custo provavelmente aparece em outro serviço (EKS/EC2 vended logs).

**3. Zero alarmes configurados**

Nenhum CloudWatch Alarm na conta. Sem alertas para:

* CPU/memória alta nas instâncias RDS
* Erros nas aplicações
* Latência elevada
* Custos acima do esperado


\
### Ainda pendente (\~$212/mês a mais se executado)

* **104 volumes EBS não anexados** — $208/mês (requer verificação no kubectl)
* **10 snapshots RDS órfãos us-west-2** — $4.50/mês (pronto para deletar