<!-- title: Mongo DB - Tools | url: https://outline.seazone.com.br/doc/mongo-db-tools-YUxPPPRKnu | area: Tecnologia -->

# Mongo DB - Tools

# Documentação Técnica: MongoDB Tools

Este documento descreve a implementação do MongoDB compartilhado para ferramentas internas ("MongoDB Tools") no cluster Kubernetes. Atualmente, ele é o banco de dados principal do **GrowthBook**.

## Visão Geral

O "MongoDB Tools" é uma instância MongoDB implantada utilizando um Helm Chart reutilizável desenvolvido internamente pela Seazone. Ele serve como um banco de dados NoSQL compartilhado para aplicações de ferramentas (Tools) que residem no mesmo cluster.

### Links Importantes

* **Repositório de GitOps:** [seazone-tech/gitops-governanca](https://github.com/seazone-tech/gitops-governanca)
* **Repositório do Chart:** [seazone-tech/helm-charts](https://github.com/seazone-tech/helm-charts) (Pasta: `mongodb`)
* **Endereço Interno:** `mongodb-tools.tools.svc.cluster.local:27017`

## Arquitetura

 ![](/api/attachments.redirect?id=fd7dfacf-c32a-41c7-907b-3a2a603a88e9 " =1408x768")


## Detalhes da Implementação

### 1. Helm Chart Reutilizável

Utilizamos um chart próprio (`seazone-tech/helm-charts/mongodb`) que encapsula as melhores práticas para deploy de MongoDB na Seazone.

* **Tipo de Workload:** `StatefulSet` (garante identidade única e persistência estável).
* **Imagem:** `mongo:8.0`.
* **Monitoramento:** Sidecar `percona/mongodb_exporter` integrado para métricas no Prometheus.

### 2. Configuração (Values)

A instância "MongoDB Tools" está configurada em `gitops-governanca/argocd/applications/databases/mongodb-tools/values.yaml`:

* **Recursos:**
  * Requests: 100m CPU / 256Mi Memória.
  * Limits: 500m CPU / 512Mi Memória.
* **Persistência:** PVC de 10Gi (StorageClass `gp3`).
* **Scheduling:**
  * `nodeSelector`: `node-pool: general-karpenter-data` (Garante execução em nós de dados otimizados).
  * `tolerations`: Aceita taints de workloads `stateful`.
* **Autenticação:** Habilitada (`auth.enabled: true`). Usuário `root`.

### 3. Segredos (External Secrets)

As credenciais são gerenciadas via External Secrets:

* **Origem AWS:** `/sre/databases/mongodb/*`
* **Secret Gerada:** `mongodb-tools-secrets`
* **Aplicação:** O chart monta essa secret para definir a senha do usuário root.

## Como Acessar e Usar

### Acesso Interno (Mesmo Cluster)

Serviços rodando no mesmo cluster (ex: GrowthBook) devem usar a seguinte URI de conexão:

```
mongodb://root:<SENHA>@mongodb-tools.tools.svc.cluster.local:27017/growthbook?authSource=admin
```

> **Nota:** A senha deve ser recuperada da secret `mongodb-tools-secrets` no namespace `tools`.

### Acesso Externo

**Por padrão, não há acesso externo (Ingress) habilitado para este banco de dados por motivos de segurança.**

Para acesso administrativo temporário (ex: depuração via `mongosh` ou Compass), utilize `kubectl port-forward`:

```bash
# Redireciona a porta 27017 do cluster para sua máquina local

kubectl port-forward svc/mongodb-tools -n tools 27017:27017
```

Conecte-se localmente: `mongodb://localhost:27017`

## Reutilizando o Chart do MongoDB

Este padrão de deploy pode ser replicado para outras aplicações ou ambientes. Para usar o chart da Seazone em outro projeto:


1. **Adicione o repositório Helm (se estiver usando localmente/manualmente):** O chart está no repositório `seazone-tech/helm-charts`.
2. **No ArgoCD:** Configure a `source` da sua Application apontando para o repositório de charts e o caminho `mongodb`.
3. **Exemplo de** `**values.yaml**` **mínimo para nova instância:**

   ```yaml
   nameOverride: "meu-novo-mongo"
   
   auth:
     enabled: true
     rootUsername: "admin"
     existingSecret: "minha-secret-com-senha" # Crie essa secret via ExternalSecret
     database: "minha-app-db"
   
   persistence:
     enabled: true
     size: "5Gi"
     storageClass: "gp3"
   ```