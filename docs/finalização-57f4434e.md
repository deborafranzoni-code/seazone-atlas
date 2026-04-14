<!-- title: finalização | url: https://outline.seazone.com.br/doc/finalizacao-TcbXnLVz3B | area: Tecnologia -->

# finalização

**Cluster:** cluster-tools-prod-gke (us-central1-a, GCP) **Pré-condição:** Todas as aplicações de negócio devem ter sido migradas para o EKS (general-cluster, sa-east-1) antes de executar este documento.

> **Claude Code executa todo o descomissionamento** — kubectl, argocd cli, gcloud e verificações de limpeza. O engenheiro valida cada etapa antes de avançar e confirma o comando final de deleção do cluster.


---

## Sumário


1. [Por Que a Ordem Importa](#1-por-que-a-ordem-importa)
2. [Desligar o Loki GKE](#2-desligar-o-loki-gke)
3. [Desligar o Traefik GKE](#3-desligar-o-traefik-gke)
4. [Remover o External Secrets GKE](#4-remover-o-external-secrets-gke)
5. [Remover o Incident Agent](#5-remover-o-incident-agent)
6. [Checklist Final — Antes de Deletar o Cluster](#6-checklist-final--antes-de-deletar-o-cluster)
7. [Deletar o Cluster GKE](#7-deletar-o-cluster-gke)
8. [Limpeza de Recursos GCP Pós-Deleção](#8-limpeza-de-recursos-gcp-p%C3%B3s-dele%C3%A7%C3%A3o)


---

## 1. Por Que a Ordem Importa

O descomissionamento deve seguir uma ordem específica para evitar interrupções em cascata e garantir que nenhum serviço seja removido antes de seu dependente estar pronto.

```
Grafo de dependências (de cima para baixo = ordem de remoção):

    [Outline]           ← remover primeiro (doc 04)
         |
    [Loki GKE]          ← sem dependentes diretos, pode ser removido cedo
         |
  [Apps migradas]       ← cada app precisa estar no EKS antes de remover
         |
  [Traefik GKE]         ← só remover após TODAS as apps estarem no EKS
         |
 [External Secrets]     ← só remover após nenhum ExternalSecret ativo
         |
  [Incident Agent]      ← remover antes de deletar o cluster
         |
   [Cluster GKE]        ← deleção final — confirmada pelo engenheiro
```

| Componente | Pré-requisito para Remoção |
|----|----|
| Outline | Exportação concluída + usuários comunicados |
| Loki GKE | Nenhum (não há dados para migrar) |
| Traefik GKE | Todas as apps com IngressRoute no GKE migradas para EKS |
| External Secrets | Nenhum ExternalSecret ativo no cluster GKE |
| Incident Agent | Nenhum (pode ser removido a qualquer momento) |
| Cluster GKE | Todos os itens acima concluídos |


---

## 2. Desligar o Loki GKE

**Tempo estimado com Claude Code: \~5 minutos.**

### 2.1 Contexto

O Loki no GKE possui 8 PVCs de 10Gi (80Gi total), DaemonSet de coleta (canary) em 27 nodes e os componentes backend (4 pods), write (4 pods), read (2 pods) e gateway.

**Não há necessidade de migrar logs** — o EKS já possui sua própria stack Loki configurada e operacional. O objetivo é apenas parar a coleta e liberar os recursos.

### 2.2 Verificar Estado Atual

Claude Code executa e exibe o estado atual para validação do engenheiro:

```bash
# Confirmar que estamos no contexto GKE

kubectl config use-context <gke-context>
kubectl config current-context

# Verificar pods e PVCs do Loki

kubectl get pods -n loki

kubectl get pvc -n loki

kubectl get daemonset -n loki  # canary

# Verificar o DaemonSet em quantos nodes está rodando

kubectl get daemonset -n loki -o wide
```

### 2.3 Remover a Application Loki no ArgoCD

```bash
# Identificar o nome da Application

kubectl get application -n argocd | grep loki

# Deletar com cascade (remove todos os recursos Kubernetes gerenciados)
argocd app delete loki-gke --cascade --yes
# ou

argocd app delete loki --cascade --yes  # ajuste o nome conforme o ArgoCD do GKE
```

### 2.4 Verificar Remoção dos PVCs

```bash
# Os PVCs podem não ser removidos automaticamente — verificar

kubectl get pvc -n loki

# Se ainda existirem, remover manualmente

kubectl delete pvc --all -n loki

# Deletar o namespace

kubectl delete namespace loki
```

### 2.5 Verificar PersistentVolumes (PVs) Órfãos

```bash
# PVs podem ficar com status "Released" após deleção dos PVCs

kubectl get pv | grep loki

# Deletar PVs órfãos

kubectl delete pv <nome-do-pv>
```

**Atenção:** Os discos GCP (GCE Persistent Disks) associados aos PVCs podem ser deletados automaticamente se a StorageClass tiver `reclaimPolicy: Delete`. Verificar antes de deletar o namespace.

```bash
# Verificar a StorageClass dos PVCs do Loki

kubectl get pvc -n loki -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.storageClassName}{"\n"}{end}'
```


---

## 3. Desligar o Traefik GKE

**Tempo estimado com Claude Code: \~5 minutos** (após confirmar que todas as apps foram migradas).

### 3.1 Contexto

O Traefik roda no namespace `traefik-system` com 1 pod e gerencia os IngressRoutes de **todas as aplicações do GKE**. Removê-lo antes de migrar as apps derrubaria o acesso externo a elas.

### 3.2 Pré-requisito — Verificar Apps Migradas

```bash
# Listar todos os IngressRoutes ativos no GKE

kubectl get ingressroute -A

# Listar todos os serviços com IngressRoute (verificar se ainda há apps rodando no GKE)
kubectl get ingressroute -A -o jsonpath='{range .items[*]}{.metadata.namespace}{"\t"}{.metadata.name}{"\n"}{end}'
```

**Todos os IngressRoutes devem ter sido removidos (junto com as apps migradas) antes de continuar.**

### 3.3 Verificar que Não Há Mais IngressRoutes Ativos

```bash
# Verificar que o único namespace com IngressRoute é o próprio traefik-system (ou nenhum)
kubectl get ingressroute -A | grep -v "NAMESPACE\|traefik-system"
# Resultado esperado: nenhuma linha
```

### 3.4 Remover a Application Traefik no ArgoCD

```bash
# Identificar o nome da Application

kubectl get application -n argocd | grep traefik

# Deletar com cascade

argocd app delete traefik-gke --cascade --yes
```

### 3.5 Limpeza Manual (se necessário)

```bash
# Verificar recursos restantes

kubectl get all -n traefik-system

# Se a Application ArgoCD não gerenciava CRDs, remover manualmente

kubectl delete namespace traefik-system

# Remover CRDs do Traefik (IngressRoute, Middleware, etc.)
kubectl get crd | grep traefik

kubectl delete crd ingressroutes.traefik.io

kubectl delete crd middlewares.traefik.io
# ... demais CRDs do Traefik
```

### 3.6 Remover Load Balancer GCP

O Traefik cria um Load Balancer no GCP. Verificar no console GCP ou via gcloud:

```bash

gcloud compute forwarding-rules list --project=<gcp-project>
gcloud compute backend-services list --project=<gcp-project>
```

O Load Balancer deve ser removido automaticamente quando o Service do Traefik for deletado. Se ficar órfão, deletar manualmente pelo Console GCP → Network Services → Load Balancing.


---

## 4. Remover o External Secrets GKE

**Tempo estimado com Claude Code: \~5 minutos** (após confirmar que não há ExternalSecrets ativos).

### 4.1 Contexto

O External Secrets Operator (ESO) possui 3 pods: `external-secrets`, `cert-controller` e `webhook`. Ele gerencia a sincronização de segredos do GCP Secret Manager (ou AWS SSM) para o cluster GKE.

### 4.2 Verificar ExternalSecrets Ativos

```bash
# Listar todos os ExternalSecret no cluster

kubectl get externalsecret -A

# Verificar o status de cada um

kubectl get externalsecret -A -o wide
```

**Resultado esperado antes de remover:** nenhum ExternalSecret com status `Ready` ou `InSync` — todos devem ter sido removidos junto com as aplicações que os utilizavam.

### 4.3 Verificar ClusterSecretStores

```bash
# Listar ClusterSecretStores configurados

kubectl get clustersecretstore

# Verificar detalhes (qual backend de segredos cada um usa)
kubectl describe clustersecretstore <nome>
```

### 4.4 Remover a Application External Secrets no ArgoCD

```bash
# Identificar o nome da Application

kubectl get application -n argocd | grep external-secret

# Deletar com cascade

argocd app delete external-secrets-gke --cascade --yes
```

### 4.5 Limpeza Manual

```bash
# Verificar recursos restantes

kubectl get all -n external-secrets

# Se necessário, deletar namespace

kubectl delete namespace external-secrets

# Remover CRDs do ESO

kubectl get crd | grep "external-secrets\|secretstores"
kubectl delete crd externalsecrets.external-secrets.io

kubectl delete crd clustersecretstores.external-secrets.io

kubectl delete crd secretstores.external-secrets.io
# ... demais CRDs do ESO
```


---

## 5. Remover o Incident Agent

### 5.1 Contexto

O incident-agent está no namespace `incident-agent` com 1 pod. É um agente em desenvolvimento — não há dados persistentes para preservar.

### 5.2 Remover a Application ArgoCD

```bash
# Verificar a Application no ArgoCD

kubectl get application -n argocd | grep incident

# Deletar com cascade

argocd app delete incident-agent --cascade --yes
```

### 5.3 Remover o Namespace

```bash
# Verificar se ainda há recursos

kubectl get all -n incident-agent

# Deletar namespace

kubectl delete namespace incident-agent
```

### 5.4 Limpeza de RBAC

```bash
# Verificar ClusterRoles e ClusterRoleBindings do incident-agent

kubectl get clusterrole | grep incident

kubectl get clusterrolebinding | grep incident

# Remover se existirem

kubectl delete clusterrole incident-agent

kubectl delete clusterrolebinding incident-agent
```


---

## 6. Checklist Final — Antes de Deletar o Cluster

Claude Code verifica automaticamente cada item deste checklist e exibe o resultado. O engenheiro valida a saída antes de autorizar a deleção do cluster.

### 6.1 Aplicações

- [ ] Outline desligado (ver doc `04-outline-canvas.md`)
- [ ] Todas as aplicações de negócio migradas para o EKS
- [ ] Nenhum pod rodando além dos namespaces de infra (kube-system, argocd)
- [ ] Nenhum IngressRoute ativo fora do traefik-system

```bash
# Verificar pods em todos os namespaces

kubectl get pods -A | grep -v "kube-system\|argocd\|NAMESPACE"
# Resultado esperado: nenhuma linha (ou apenas infra básica)
```

### 6.2 Infraestrutura

- [ ] Loki GKE removido + PVCs deletados
- [ ] Traefik GKE removido + Load Balancer GCP removido
- [ ] External Secrets removido + CRDs removidos
- [ ] Incident Agent removido

```bash
# Confirmar que não há PVCs órfãos

kubectl get pvc -A

# Confirmar que não há PVs com status Released

kubectl get pv | grep Released
```

### 6.3 DNS e Certificados

- [ ] Entradas DNS do GKE removidas do Cloudflare
- [ ] Certificados TLS removidos do cluster
- [ ] Nenhum domínio [seazone.com.br](http://seazone.com.br) ainda aponta para IPs do GKE

```bash
# Verificar certificados restantes

kubectl get certificate -A

kubectl get certificaterequest -A
```

### 6.4 Dados e Backups

- [ ] Export do Outline salvo em local seguro (S3 ou Google Drive)
- [ ] Snapshot final do banco de dados do Outline criado (se aplicável)
- [ ] Confirmação de que o EKS está recebendo logs/métricas normalmente

```bash
# Verificar no EKS que Loki está recebendo logs
# (executar no contexto do EKS, não do GKE)
kubectl config use-context <eks-context>
kubectl get pods -n loki

kubectl logs -n loki deployment/loki-gateway --tail=20
```

### 6.5 Acesso e Autenticação

- [ ] Chaves de serviço GCP utilizadas pelas apps foram rotacionadas ou removidas
- [ ] Service Accounts GCP específicas do GKE documentadas para remoção
- [ ] Workload Identity configurações limpas (se aplicável)

### 6.6 Verificação Final

Claude Code executa todos os comandos abaixo e exibe um resumo consolidado para o engenheiro revisar antes de avançar:

```bash
# Listar TODOS os namespaces e seus recursos

kubectl get all -A | grep -v "kube-system"

# Listar todos os nós do cluster

kubectl get nodes

# Verificar se o ArgoCD do GKE não tem mais Applications gerenciadas

kubectl get application -n argocd
```


---

## 7. Deletar o Cluster GKE

**Passo final — confirmado pelo engenheiro.** Claude Code prepara e exibe o comando; o engenheiro dá a autorização explícita antes da execução.

### 7.1 Confirmar Contexto e Projeto GCP

```bash
# Confirmar projeto GCP ativo

gcloud config get-value project

# Listar clusters GKE no projeto

gcloud container clusters list --project=<gcp-project>

# Confirmar detalhes do cluster

gcloud container clusters describe cluster-tools-prod-gke \
  --zone=us-central1-a \
  --project=<gcp-project>
```

### 7.2 Remover o Node Pool Antes (opcional mas recomendado)

```bash
# Listar node pools

gcloud container node-pools list \
  --cluster=cluster-tools-prod-gke \
  --zone=us-central1-a \
  --project=<gcp-project>

# Deletar cada node pool individualmente (escala para 0 primeiro)
gcloud container clusters resize cluster-tools-prod-gke \
  --node-pool=<nome-do-pool> \
  --num-nodes=0 \
  --zone=us-central1-a \
  --project=<gcp-project>
```

### 7.3 Comando de Deleção do Cluster

**O engenheiro confirma este passo antes da execução — é irreversível.**

```bash

gcloud container clusters delete cluster-tools-prod-gke \
  --zone=us-central1-a \
  --project=<gcp-project> \
  --quiet
```

**O flag** `**--quiet**` **pula a confirmação interativa.** Para um ambiente de produção, remova `--quiet` e confirme manualmente.

### 7.4 Verificar Deleção

```bash
# Verificar que o cluster não existe mais

gcloud container clusters list --project=<gcp-project>

# Verificar que não há discos GCP órfãos

gcloud compute disks list --project=<gcp-project> --filter="status=READY"
```

### 7.5 Remover Entrada do kubeconfig Local

```bash
# Verificar contextos locais

kubectl config get-contexts | grep gke

# Remover contexto do GKE do kubeconfig local

kubectl config delete-context <gke-context-name>
kubectl config delete-cluster <gke-cluster-name>
kubectl config delete-user <gke-user-name>
```


---

## 8. Limpeza de Recursos GCP Pós-Deleção

### 8.1 Verificar Recursos Residuais Imediatos

Após a deleção do cluster, Claude Code executa os comandos abaixo e lista o que precisa ser limpo manualmente:

```bash
# Discos persistentes (PVCs não limpos podem deixar discos)
gcloud compute disks list --project=<gcp-project>

# Load Balancers e regras de firewall

gcloud compute forwarding-rules list --project=<gcp-project>
gcloud compute firewall-rules list --project=<gcp-project> | grep gke

# Endereços IP reservados

gcloud compute addresses list --project=<gcp-project>

# Buckets GCS (Loki pode ter usado bucket para armazenamento)
gsutil ls -p <gcp-project>
```

### 8.2 Remover Service Accounts GKE

```bash
# Listar Service Accounts do projeto

gcloud iam service-accounts list --project=<gcp-project>

# Identificar e deletar SAs criadas especificamente para o GKE
# Exemplos comuns: loki@, external-secrets@, outline@, etc.
gcloud iam service-accounts delete <sa-email> --project=<gcp-project>
```

### 8.3 Revogar Permissões de IAM

```bash
# Verificar bindings de IAM no projeto relacionadas ao cluster

gcloud projects get-iam-policy <gcp-project> \
  --format="table(bindings.role,bindings.members)" | grep serviceAccount
```

### 8.4 Decisão sobre o Projeto GCP

| Cenário | Ação Recomendada |
|----|----|
| Projeto usado exclusivamente pelo GKE | Encerrar o projeto GCP |
| Projeto compartilhado com outros serviços | Manter o projeto, remover apenas recursos do GKE |
| Projeto com dados históricos (Cloud Storage, BigQuery) | Manter por período de retenção definido |

**Para encerrar o projeto GCP:**


1. Acesse o Console GCP → IAM & Admin → Manage Resources
2. Selecione o projeto
3. Clique em "Delete"
4. O projeto fica em estado de encerramento por **30 dias** antes da deleção permanente
5. Durante esses 30 dias, é possível restaurar o projeto se necessário

```bash
# Via gcloud (alternativa)
gcloud projects delete <gcp-project> --quiet
```

### 8.5 Billing GCP

- [ ] Verificar se há custos pendentes no Console GCP → Billing
- [ ] Aguardar a fatura final do mês de encerramento
- [ ] Se o projeto for encerrado, verificar se o billing account pode ser desassociado
- [ ] Documentar o custo final do GKE para registro histórico

### 8.6 Comunicação Pós-Deleção

Após a deleção do cluster e limpeza dos recursos:

```bash
# Template de mensagem Slack #tech-infra
```

```
:white_check_mark: *Cluster GKE descomissionado com sucesso*

O cluster cluster-tools-prod-gke (us-central1-a) foi deletado em [DATA].

*O que foi feito:*
• Outline migrado para Notion
• Loki, Traefik, External Secrets e Incident Agent removidos
• Cluster GKE deletado
• Recursos GCP residuais limpos

*Impacto:* Nenhum — todas as cargas de trabalho estão no EKS (general-cluster, sa-east-1).

Qualquer dúvida: [RESPONSAVEL] no canal #tech-infra.
```


---

*Documento criado em: 2026-03-26* *Responsável pelo descomissionamento: Time SRE — Seazone*