<!-- title: Plano de Otimização  AWS v2 | url: https://outline.seazone.com.br/doc/plano-de-otimizacao-aws-v2-IkvJgnSAuc | area: Tecnologia -->

# Plano de Otimização  AWS v2

# Plano de Otimizacao de Custos AWS - Seazone

#### [Versão Deep Dive técnica → ](https://outline.seazone.com.br/doc/plano-v2-tecnico-GV0967BqV2)@[Plano V2 - Técnico](mention://c4b5e4c1-3400-4d57-9636-2815f9e3682d/document/e9566d77-2370-4cf8-bb52-a187622e29bc)

### Versao Executiva | Abril 2026

> **Resumo:** Gastamos R$60 mil/mes com AWS. Podemos reduzir **R$15 mil/mes** (cenario provavel), com R$325/mo de investimento em upgrades de estabilidade. **Precisamos de:** aprovacao para iniciar e para contratar Savings Plan (\~R$16k/mo commitment).


---

## Onde nosso dinheiro vai

```mermaidjs

sankey-beta

Gasto Total 10.971,Applications,5004

Gasto Total 10.971,Nekt,2030

Gasto Total 10.971,PRD-Lake,1014

Gasto Total 10.971,Seazone Technology,860

Gasto Total 10.971,Compromissos SP-RI,977

Gasto Total 10.971,PRD-Sirius,282

Gasto Total 10.971,Ambientes Dev,300

Gasto Total 10.971,Outros,504

Applications,Computacao EKS,1700

Applications,NAT Rede EBS,2073

Applications,S3 Observabilidade,431

Applications,Banco de dados,441

Applications,Mensageria,359

Nekt,EMR Serverless Spark,1115

Nekt,S3 Data Lake 8.5TB,376

Nekt,Imposto NAT Outros,539

PRD-Lake,Glue Athena Lambda,694

PRD-Lake,S3 2.5TB,281

PRD-Lake,Outros PRD-Lake,39
```

A conta **Applications** sozinha responde por **46% do gasto**. Dentro dela, o maior custo nao e computacao -- e **rede e armazenamento** a R$11.300/mo.


---

## Antes de economizar: 3 riscos de estabilidade

Ha problemas em produção que afetam performance **hoje** e que precisam ser resolvidos independente do plano de custos:

```mermaidjs

flowchart LR
  A["Cache do Reservas<br/>94% memoria cheia<br/>82 mil chaves expulsas/sem"]
  B["App vai ao banco<br/>ao inves do cache"]
  C["Banco Sapron<br/>CPU bate 99.5%<br/>queries travam"]

  A -->|"dados uteis<br/>sao perdidos"| B
  B -->|"mais carga<br/>no banco"| C
  C -->|"lentidao<br/>para o usuario"| A

  style A fill:#e74c3c,color:#fff
  style B fill:#f39c12,color:#fff
  style C fill:#e74c3c,color:#fff
```

| O que | Solucao | Custo |
|----|----|---:|
| Cache do Reservas esta lotado (94% mem, expulsando dados) | Dobrar tamanho do cache (t4g.small -> t4g.medium) | +R$130/mo |
| Banco Sapron bate 99.5% CPU (throttling) | Trocar para instancia dedicada db.m7g.large | +R$195/mo |
| 8 maquinas de prod esgotam CPU burst | Configurar Karpenter para usar maquinas nao-burstable (m6a ao inves de t3a) | R$0 (mesmo preco) |

**Investimento: R$325/mo.** Retorno imediato em estabilidade e menos incidentes.


---

## O maior desperdício: uma maquina gigante ociosa

```mermaidjs
---
config:
  xyChart:
    xAxis:
      labelFontSize: 11
    yAxis:
      labelFontSize: 11
---
xychart-beta
  title "CPU real vs capacidade (media 7 dias)"
  x-axis ["c6a.12xlarge*\nR$7.100/mo", "openclaw\nR$640/mo", "r6g.2xlarge\n(dados)", "cluster-svc\n(gerencia)", "nodes prod\n(media 8 nodes)"]
  y-axis "% CPU utilizado" 0 --> 45
  bar [3.3, 0.3, 5.2, 36.3, 30.2]
```

*A c6a.12xlarge tem 48 processadores e 96 GB de memoria. Na ultima semana, usou 3% -- ou seja, 1.5 dos 48 processadores. Custa R$7.100/mo.*

**Por que aconteceu:** Nosso orquestrador (Karpenter) nao tinha limite de tamanho configurado. Ele agrupou varias aplicacoes numa unica maquina gigante para "eficiencia", mas o resultado foi capacidade ociosa.

**Solucao:** Configurar um teto no Karpenter (maximo 4xlarge ao inves de 12xlarge). Ele redistribui automaticamente as aplicacoes em maquinas menores. **Economia: R$4.300-6.500/mo. Rollback: remover a configuracao (Karpenter reprovision automatico).**

A **openclaw** tem problema similar: 0.3% de CPU. Trocar por maquina 3x menor economiza R$425/mo.


---

## Quanto podemos economizar

A faixa depende de ate onde queremos ir:

| O que muda | Conservador | Provavel | Agressivo |
|----|----|----|----|
| Limpeza + quick wins  | Sim | Sim | Sim |
| Rightsizing Karpenter + downsizes | Sim | Sim | Sim |
| Spot em staging | Nao | Sim | Sim |
| Spot em producao (50-70%) | Nao | Parcial (30%) | Sim (70%) |
| Graviton (processadores ARM) | Nao | Parcial | Sim |
| Savings Plan de 1 ano | Nao | Sim | Sim |
| Reducao de sampling Tempo | Nao | Nao | Sim |

| Cenario | Economia/mo | Economia/ano |
|----|---:|---:|
| **Conservador** (limpeza + rightsizing) | R$8.200 | R$98.400 |
| **Provavel** (+ Spot parcial + SP) | **R$15.000** | **R$180.000** |
| **Agressivo** (tudo implementado) | R$23.000 | R$276.000 |

> **Recomendacao:** Mirar no cenario **provavel**. Se Spot funcionar bem em staging, expandir para producao gradualmente.


---

## Priorização: impacto vs esforço

```mermaidjs

quadrantChart
  title O que fazer primeiro
  x-axis "Baixo Esforco (< 8h)" --> "Alto Esforco (> 40h)"
  y-axis "Baixo Impacto (< R$500/mo)" --> "Alto Impacto (> R$2k/mo)"

  "Limitar Karpenter R$5.4k": [0.20, 0.92]
  "Spot staging R$1.1k": [0.35, 0.45]
  "Spot prod R$3.8k": [0.55, 0.80]
  "Savings Plan R$3.8k": [0.25, 0.75]
  "Graviton R$1.7k": [0.52, 0.55]
  "Deletar EBS R$710": [0.08, 0.28]
  "Limpar logs R$410": [0.10, 0.20]
  "Amazon Q R$1k": [0.05, 0.42]
  "Glue Flex R$710": [0.18, 0.28]
  "Openclaw R$425": [0.08, 0.20]
  "Limpar devs R$820": [0.40, 0.32]
```

Comecar pelo **canto superior esquerdo** (alto impacto, baixo esforco).


---

## Cronograma de implementacao

```mermaidjs

gantt
  title Roadmap (cenario provavel)
  dateFormat YYYY-MM-DD
  axisFormat %d/%m

  section Semana 1-2: Limpeza + Estabilidade
    Verificar Amazon Q com equipe (R$1k/mo)         :a0, 2026-04-03, 1d
    Upgrade Sapron DB + Cache Reservas               :crit, a1, 2026-04-03, 1d
    Deletar 41 volumes EBS orfaos (R$710/mo)         :a2, 2026-04-03, 2d
    Limitar NodePool Karpenter (R$5.4k/mo)           :a3, 2026-04-07, 3d
    Retention logs Nekt + lifecycle S3 backup         :a4, 2026-04-07, 2d
    Desabilitar Config/Trail dev + limpar stacks      :a5, 2026-04-08, 4d
    Downsize openclaw + deletar seaflow-db            :a6, 2026-04-10, 1d
    Limpar Lambdas mortas + Glue duplicados           :a7, 2026-04-08, 4d

  section Semana 3-4: Spot em Staging
    Configurar disruption budgets                     :b1, 2026-04-14, 2d
    Habilitar Spot staging 100%                       :b2, 2026-04-16, 1d
    Observar 2 semanas de estabilidade                :b3, 2026-04-16, 14d

  section Semana 5-6: Spot em Producao
    Habilitar Spot prod 30% (gradual)                 :c1, 2026-04-30, 3d
    Escalar para 50-70% se estavel                    :c2, 2026-05-05, 5d
    Avaliar build multi-arch para Graviton            :c3, 2026-04-30, 5d

  section Semana 7-8: Commitments + Pipeline
    Analisar SP recommendations                       :d1, 2026-05-11, 3d
    Contratar Compute Savings Plan 1 ano              :d2, 2026-05-14, 2d
    Migrar Glue jobs para Flex                        :d3, 2026-05-11, 5d
    S3 Intelligent-Tiering Nekt (8.5 TB)              :d4, 2026-05-14, 2d
```


---

## O que encontramos de "morto" na infraestrutura

Recursos que existem mas ninguem usa -- confirmado por metricas de 7-30 dias:

| Recurso | Evidencia | Custo | Acao |
|----|----|---:|----|
| **41 volumes de disco orfaos** | Desconectados desde Jul-Out/2025 (1.6 TB) | R$710/mo | Snapshot de seguranca e deletar |
| **1.147 log groups sem expiracao** | 68 GB acumulados na conta Nekt, crescendo indefinidamente | R$410/mo | Definir expiracao de 30 dias |
| **seaflow-db (banco PostgreSQL)** | Zero conexoes em 7 dias. Unico banco sem criptografia | R$75/mo | Confirmar com time (pode ser batch mensal?), snapshot e desligar |
| **42 funcoes Lambda** | Zero execucoes em 30 dias. Nomes como `terste_scraper_DELETAR` | R$0 direto | Limpeza de higiene. Reduz log groups |
| **181 jobs Glue duplicados (dev)** | Stacks CloudFormation nunca deletadas apos merge | R$450/mo | Deletar stacks antigas |
| **212 buckets S3 de feature branches (dev)** | Buckets criados por CI/CD e nunca removidos | R$400/mo | Deletar stacks + implementar cleanup automatico |
| **Amazon Q Business** | R$1.020/mo. Verificar se ha usuarios ativos | R$1.020/mo | Perguntar ao time. Se ninguem usa, cancelar |
| **AWS Config em contas dev** | Servico de compliance rodando em ambiente de desenvolvimento | R$225/mo | Desabilitar (verificar politica de seguranca antes) |
| **Backup S3 com regra desabilitada** | 1.3 TB sem mover para storage barato. Regra Glacier existe mas esta OFF | R$215/mo | Habilitar a regra existente |


---

## Estrategias que estamos propondo

### Spot Instances (maior economia individual)

Todas as 39 maquinas do cluster rodam no modelo **on-demand** (preco cheio). A AWS oferece as mesmas maquinas por **60-75% menos** no modelo Spot -- com a condicao de que podem ser interrompidas com 2 minutos de aviso.

Nosso orquestrador (Karpenter) ja sabe lidar com isso: se uma maquina Spot e interrompida, ele automaticamente provisiona outra em \~30 segundos. A chave e usar 15+ tipos de maquina diferentes para que sempre haja opcao disponivel.

**Rollout gradual:** staging primeiro (2 semanas), depois producao incremental (30% -> 50% -> 70%). Se qualquer problema surgir, revertemos em minutos.

**Nota sobre sa-east-1:** Sao Paulo tem menor diversidade de Spot que regioes americanas. Mitigamos usando 15+ instance types + fallback automatico para on-demand.

### Savings Plan (compromisso de 1 ano)

Apos estabilizar o uso de Spot, o gasto on-demand residual pode ser comprometido por 1 ano com desconto de \~30%. Usaremos **Compute Savings Plan**, que e o mais flexivel -- cobre EKS, EMR, Lambda e Fargate sem travar em tipo de maquina ou regiao.

### Processadores Graviton (ARM)

A AWS fabrica processadores proprios (Graviton) que sao \~20% mais baratos com performance igual ou melhor. A geracao mais recente ja esta disponivel em Sao Paulo. **Pre-requisito:** nosso pipeline de build precisa compilar imagens para ARM alem de x86.

### Glue Flex (ETL mais barato)

Nossos jobs de transformacao de dados podem rodar no modo Flex, que e **34% mais barato**. O trade-off: o job pode demorar mais para iniciar. Para jobs noturnos, isso e perfeitamente aceitavel.


---

## Sobre o NAT Gateway ($2.073/mo na conta Applications)

O NAT Gateway e o item mais caro dentro de "EC2-Other" e merece explicacao:

* **O time ja implementou VPC Endpoints** para S3, ECR, STS, SQS e outros servicos AWS (9 endpoints ativos). Isso ja eliminou a parcela de trafego para servicos internos da AWS.
* Os **R$3.600/mo restantes de NAT** sao trafego para a **internet publica** -- webhooks, APIs de terceiros, scrapers, etc. Esse trafego e inerente ao negocio.
* **Nao ha mais endpoints a criar** nesta conta. A otimizacao aqui seria reduzir trafego de saida (ex: cachear respostas de APIs externas), o que requer analise caso-a-caso com os times de produto.

Na conta **Nekt**, o cenario e diferente: la temos apenas 1 endpoint (S3). Adicionar ECR e CloudWatch pode economizar R$215/mo no trafego do NAT instance.


---

## Riscos e rollback

| Acao | Risco | Rollback |
|----|----|----|
| Limitar NodePool Karpenter | Apps temporariamente sem node | Remover o limite, Karpenter reprovision automatico |
| Spot em producao | Interrupcao de maquina | Karpenter provisiona on-demand automatico. Disruption budgets bloqueiam em horario comercial |
| Savings Plan 1 ano | Workload muda, SP fica subutilizado | Compute SP e flexivel (cobre EKS, EMR, Lambda). Sem rollback de contrato, mas flexivel de uso |
| Deletar EBS/seaflow-db | Alguem precisa do recurso | Snapshot de seguranca antes de deletar. Restauravel rapidamente |
| Graviton (ARM) | App incompativel com ARM | Karpenter ignora Graviton automaticamente e usa x86. Sem impacto |


---

## Como medimos sucesso

| Metrica | Hoje | Meta 30 dias | Meta 60 dias |
|----|---:|---:|---:|
| Gasto mensal total | R$60.000 | R$52.000 | R$45.000 |
| % de capacidade Spot | 0% | 15% (staging) | 40% (staging + prod) |
| Evictions/semana (cache Reservas) | 82.290 | < 100 | < 100 |
| CPU max banco Sapron | 99.5% | < 70% | < 70% |
| Volumes EBS orfaos | 41 | 0 | 0 |

**Monitoramento:** Dashboard no Grafana (ja temos stack) com custo diario por conta + metricas de utilizacao.


---

## Proximos passos

**O que precisamos de aprovacao:**


1. Aprovacao para upgrade do banco Sapron e cache Reservas (+R$325/mo)
2. Aprovacao para contratar Savings Plan em \~6 semanas (commitment de \~R$16k/mo por 1 ano, que gera economia de \~R$3.800/mo -- break-even em \~4.2 meses, economia liquida de \~R$29.600 no restante do contrato)

**O que ja podemos fazer amanha (sem aprovacao adicional):**

* Perguntar ao time sobre Amazon Q (R$1.020/mo)
* Deletar volumes EBS orfaos (R$710/mo)
* Definir retention nos log groups da Nekt (R$410/mo)


---

## Anexo: O que ja esta bem feito

Ao validar nossas recomendacoes, descobrimos que o time ja havia implementado 6 otimizacoes que iam ser sugeridas novamente:

* 9 VPC Endpoints configurados (S3, ECR, STS, SQS, SSM, EC2, DynamoDB)
* Grafana Tempo com expiracao automatica de 14 dias
* Grafana Loki com tiering para storage barato apos 30/90 dias
* EKS na versao 1.33 (mais recente, sem cobranca extra de suporte)
* ElastiCache ja usa Valkey (alternativa open-source ate 60% mais barata que Redis)
* EMR Serverless ja roda em processadores Graviton (ARM)

Isso nos poupou de recomendar mudancas que ja existiam -- e reforça que o time de infraestrutura tem feito boas escolhas tecnologicas. Credito para a equipe que configurou esses itens.


---

*Documento baseado em auditoria real: AWS Cost Explorer (Jan-Mar/2026), CloudWatch Metrics (7 dias), Compute Optimizer. Valores em reais a R$5.45/USD.*