<!-- title: Proteção de Namespaces contra Cascade Deletion no ArgoCD | url: https://outline.seazone.com.br/doc/protecao-de-namespaces-contra-cascade-deletion-no-argocd-bZAEEaxGTQ | area: Tecnologia -->

# Proteção de Namespaces contra Cascade Deletion no ArgoCD

## Contexto

O cluster GKE (`cluster-tools-prod-gke`) tem seus workloads gerenciados pelo ArgoCD que roda no EKS (`general-cluster`). Essa auditoria identificou que a combinação de `resources-finalizer` + `CreateNamespace=true` nas Applications permite que a deleção de uma Application destrua namespaces compartilhados inteiros.


---

## 1. Investigação

### Métodos utilizados

**No cluster GKE**, acesso direto via `kubectl` (contexto `gke_tools-440117_us-central1-a_cluster-tools-prod-gke`):

* `kubectl get namespaces -o json` para inspecionar annotations, labels, `tracking-id` e `managedFields` de cada namespace
* `kubectl get all -n tools -o json` para identificar quais recursos são rastreados pelo ArgoCD e quais não
* `kubectl get clusterrole argocd-manager-role -o yaml` para verificar permissões RBAC do ArgoCD no cluster

**Nos repositórios GitOps**, análise no repositório:

* `seazone-tech/gitops-governanca` 

Em cada `application.yaml`  analisei a presença de:

```
resources-finalizer.argocd.argoproj.io   → habilita cascade deletion ao remover a Application
CreateNamespace=true                     → faz o ArgoCD criar e rastrear o namespace como recurso da app
```

### Resultado da varredura

| Repositório | Total | resources-finalizer | CreateNamespace=true | Ambos |
|----|----|----|----|----|
| gitops-governanca | 29 | 29 | 27 | 27 |

27 de 29 Applications combinam ambos os campos.

### Estado real dos namespaces no GKE (confirmado via kubectl)

 ![](/api/attachments.redirect?id=21dbc2cb-ac8a-44cb-804d-0e248e41acbf " =1217x249")

| Namespace | tracking-id ArgoCD | instance label | managedFields.manager | Risco |
|----|----|----|----|----|
| `tools` | `n8n-dev:/Namespace:tools/tools` | `n8n-dev` | `argocd-controller` | Ativo |
| `dev-n8n` | nenhum | nenhum | `kubectl-create` | Sem risco atual |
| `prd-n8n` | nenhum | nenhum | `kubectl-create` | Sem risco atual |
| `external-secrets` | nenhum | nenhum | — | Sem risco atual |
| `traefik-system` | nenhum | nenhum | — | Sem risco atual |
| `kestra-poc` | nenhum | nenhum | `kubectl-create` | Sem risco atual |

Apenas `tools` está sendo rastreado ativamente pelo ArgoCD no GKE.

 ![](/api/attachments.redirect?id=a8461c1b-841c-4c59-aa39-32cd77900fa6 " =1367x57")

### O que está rodando em `tools` (confirmado via kubectl)

| Serviço | Rastreado por qual Application | Observação |
|----|----|----|
| baserow  | `baserow` | Deployments e Services tracked |
| outline | `outline` | Deployment e Service tracked |
| n8n-dev | `n8n-dev` | Apenas Services, ConfigMaps e HPAs tracked |

O namespace `tools` contém workloads de 3 Applications diferentes (baserow, outline, n8n-dev) mais recursos n8n não gerenciados pelo ArgoCD. Se o namespace for deletado, tudo cai como aconteceu no incidente n8n.

### RBAC do ArgoCD no cluster GKE

O ArgoCD acessa o GKE via `argocd-manager-role`:

 ![](/api/attachments.redirect?id=3fa43ed2-1453-494b-b0a4-df017f62bb57 " =893x461")

```yaml
rules:
- apiGroups: ['*']
  resources: ['*']
  verbs: ['*']
- nonResourceURLs: ['*']
  verbs: ['*']
```

Equivalente a cluster-admin. O ArgoCD pode criar, deletar e modificar qualquer recurso em qualquer namespace do GKE.


---

## 2. O Problema

### Como o risco funciona

```mermaidjs
graph LR
    GIT["gitops-governanca"]
    ARGO["ArgoCD (EKS)"]
    APP["Application com\nfinalizer + CreateNamespace"]
    NS["Namespace compartilhado"]
    PODS["Pods / PVCs / Deployments\nde varias apps"]

    GIT -->|"lê manifests"| ARGO
    ARGO -->|"aplica no cluster"| APP
    APP -->|"cria e rastreia"| NS
    NS --> PODS
```

### Cascade deletion

```mermaidjs
sequenceDiagram
    actor Dev
    participant ArgoCD
    participant Cluster

    Dev->>ArgoCD: deleta qualquer Application do namespace
    Note over ArgoCD: detecta resources-finalizer
    ArgoCD->>Cluster: deleta todos os recursos gerenciados
    ArgoCD->>Cluster: deleta o Namespace
    Note over Cluster: NAMESPACE REMOVIDO
    Cluster-->>Cluster: todos os servicos do namespace down
```

### Por que namespaces compartilhados são pontos de atenção?

Quando uma Application usa `CreateNamespace=true`, o ArgoCD cria o namespace e o rastreia como recurso seu. Com o `resources-finalizer` presente, deletar a Application destrói tudo que ela rastreia, incluindo o namespace.

Em namespaces exclusivos isso parece ok. O risco surge nos namespaces compartilhados, onde múltiplos serviços independentes convivem. Qualquer uma das apps pode derrubar o namespace inteiro.

**Caso concreto no GKE:** 5 Applications (baserow, postgres-tools, redis-automacao, redis-n8n-prd, outline) têm destination `tools` + `CreateNamespace=true` + `resources-finalizer`. Deletar qualquer uma delas com cascade pode remover o namespace `tools`, derrubando todos os outros serviços.


---

## 3. A Solução

### Antes e depois

|    | Antes | Depois |
|----|----|----|
| Quem cria `tools` | Apps individuais via `CreateNamespace=true` ou manual | Application dedicada `namespaces-gke` |
| Proteção do namespace | Nenhuma | `Delete=false, Prune=false` |
| `resources-finalizer` na app dona | Sim | Não (intencional) |
| Risco de cascade deletion | Qualquer app pode arrastar o namespace | Namespace protegido independente das apps |

### Como a annotation protege na prática

```mermaidjs
sequenceDiagram
    actor Dev
    participant ArgoCD
    participant GKE

    Dev->>ArgoCD: deleta uma Application
    Note over ArgoCD: detecta resources-finalizer
    ArgoCD->>GKE: deleta recursos gerenciados
    ArgoCD->>GKE: tenta deletar Namespace tools
    Note over GKE: annotation Delete=false detectada
    GKE-->>ArgoCD: ignorado
    Note over GKE: Namespace tools intacto
    GKE-->>GKE: todos os servicos ok
```

### Por que aplicar num namespace existente é seguro?

Aplicar um manifesto de Namespace via `kubectl apply` num namespace que já existe não o recria nem afeta os recursos internos. O Kubernetes faz apenas um merge nos metadados (labels e annotations). Pods, PVCs e Deployments continuam intactos.


---

## 4. Plano de Implementação

### Namespaces em risco por cluster

**GKE (confirmado via kubectl):**

| Namespace | Apps com destination aqui + CreateNamespace + finalizer | Risco |
|----|----|----|
| `tools` | baserow, postgres-tools, redis-automacao, redis-n8n-prd, outline | Ativo |
| `dev-n8n` | sem tracking do ArgoCD | Sem risco atual |
| `prd-n8n` | sem tracking do ArgoCD | Sem risco atual |
| `external-secrets` | sem tracking do ArgoCD | Sem risco atual |
| `traefik-system` | sem tracking do ArgoCD | Sem risco atual |
| `kestra-poc` | sem tracking do ArgoCD | Sem risco atual |

### Sequência de execução

**Fase 1 - GKE (prioridade, dados confirmados)**


1. Criar namespace manifests em `argocd/namespaces/gke/` com annotation `Delete=false, Prune=false`
2. Criar Application `namespaces-gke` (sem finalizer, `prune: false`)
3. ArgoCD sincroniza — adiciona annotations nos namespaces existentes sem downtime
4. Remover `CreateNamespace=true` das 5 apps que têm destination `tools` no GKE
5. Resolver a criação do namespace `tools` pelo helm chart do n8n (override `global.namespace` nos values ou remover o template)

### Arquivos a criar e modificar

**Novos -** `**gitops-governanca**`

```
argocd/namespaces/
  gke/
    tools.yaml

argocd/applications/
  namespaces-gke/application.yaml
```

**Modificados —** `**gitops-governanca**` (remover `CreateNamespace=true`)

```
GKE / tools:      baserow, postgres-tools, redis-automacao, redis-n8n-prd, outline                         (após validação)
```

**Modificados —** `**helm-charts**`

```
n8n: resolver a criação do namespace tools pelo helm chart
     (override global.namespace nos values ou remover o template)
```


---

## 5. Manifests de referência/exemplo

### Namespace protegido

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: tools
  annotations:
    argocd.argoproj.io/sync-options: Prune=false,Delete=false
  labels:
    managed-by: argocd-namespace-protection
```

### Application dedicada de namespaces

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: namespaces-gke
  namespace: argocd
  annotations:
    argocd.argoproj.io/sync-wave: "-1"
  # sem resources-finalizer — intencional
spec:
  project: default
  source:
    repoURL: https://github.com/seazone-tech/gitops-governanca
    path: argocd/namespaces/gke
    targetRevision: HEAD
  destination:
    server: 'https://34.60.64.40'
    namespace: default
  syncPolicy:
    automated:
      prune: false
      selfHeal: true
```


---

## 6. Referência

> O Red Hat Developer publica esse padrão como prática recomendada para clusters multi-tenant — criar uma Application separada para gerenciar namespaces com sync-wave: "-1" (sincroniza antes de tudo), separando o ciclo de vida do namespace do ciclo de vida das aplicações:

* <https://developers.redhat.com/articles/2022/04/13/manage-namespaces-multitenant-clusters-argo-cd-kustomize-and-helm>

Outras referencias

* [ArgoCD Sync Options — Delete=false e Prune=false](https://argo-cd.readthedocs.io/en/stable/user-guide/sync-options/)
* <https://argo-cd.readthedocs.io/en/stable/user-guide/app_deletion/> 
* <https://argo-cd.readthedocs.io/en/stable/operator-manual/security/#cluster-rbac>