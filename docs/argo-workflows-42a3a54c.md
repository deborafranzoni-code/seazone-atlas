<!-- title: Argo Workflows | url: https://outline.seazone.com.br/doc/argo-workflows-FA1PSYLHAE | area: Tecnologia -->

# Argo Workflows

# Documentação Técnica

## Sumário


1. [Introdução](#introdu%C3%A7%C3%A3o)
2. [Arquitetura](#arquitetura)
3. [Tipos de Recursos](#tipos-de-recursos)
4. [Configuração de Autenticação e Autorização](#configura%C3%A7%C3%A3o-de-autentica%C3%A7%C3%A3o-e-autoriza%C3%A7%C3%A3o)
5. [Armazenamento e Persistência](#armazenamento-e-persist%C3%AAncia)
6. [Execução de Workflows](#execu%C3%A7%C3%A3o-de-workflows)
7. [Resolução de Problemas](#resolu%C3%A7%C3%A3o-de-problemas)
8. [Referências](#refer%C3%AAncias)

## Introdução

O Argo Workflows é um orquestrador de workflows baseado em Kubernetes, projetado para coordenar trabalhos paralelos. Esta documentação descreve as configurações implementadas no ambiente de produção da Seazone, incluindo configurações de segurança, persistência e execução.

**Versão atual: v3.6.5**

## Arquitetura

O Argo Workflows consiste em dois componentes principais:


1. **Workflow Controller** - Responsável por gerenciar os workflows, monitorar seu estado e criar os pods associados.
2. **Argo Server** - Fornece uma API RESTful e uma interface de usuário web para interação com workflows.

### Componentes Instalados

```
Namespace: tools

Deployment: argo-workflows-server - Servidor UI/API

Deployment: argo-workflows-workflow-controller - Controller
```

## Tipos de Recursos

O Argo Workflows possui diferentes recursos para definir e executar fluxos de trabalho:

### Workflow

Um Workflow é a unidade básica de execução no Argo, representando uma série de etapas que devem ser executadas.

```yaml

apiVersion: argoproj.io/v1alpha1

kind: Workflow

metadata:
  generateName: exemplo-
spec:
  entrypoint: main
  templates:
  - name: main
    container:
      image: alpine
      command: [echo, "Olá Mundo"]
```

**Características**:

* Execução única
* Escopo limitado a um namespace
* Executa imediatamente quando criado

### WorkflowTemplate

Um WorkflowTemplate define um modelo reutilizável que pode ser referenciado por outros workflows.

```yaml

apiVersion: argoproj.io/v1alpha1

kind: WorkflowTemplate

metadata:
  name: template-exemplo

spec:
  templates:
  - name: main
    container:
      image: alpine
      command: [echo, "Template reutilizável"]
```

**Características**:

* Não executa por si só (apenas um template)
* Escopo limitado a um namespace
* Pode ser referenciado por workflows usando `templateRef`

### ClusterWorkflowTemplate

Similar ao WorkflowTemplate, mas com escopo de cluster.

```yaml

apiVersion: argoproj.io/v1alpha1

kind: ClusterWorkflowTemplate

metadata:
  name: cluster-template-exemplo

spec:
  templates:
  - name: main
    container:
      image: alpine
      command: [echo, "Template para todo o cluster"]
```

**Características**:

* Disponível em todos os namespaces do cluster
* Útil para padronização organizacional
* Requer permissões de cluster para gerenciar

### CronWorkflow

Um CronWorkflow permite a execução programada e recorrente de workflows.

```yaml

apiVersion: argoproj.io/v1alpha1

kind: CronWorkflow

metadata:
  name: cron-exemplo

spec:
  schedule: "*/5 * * * *"
  timezone: "America/Sao_Paulo"
  suspend: false
  workflowSpec:
    entrypoint: main
    templates:
    - name: main
      container:
        image: alpine
        command: [echo, "Executado a cada 5 minutos"]
```

**Características**:

* Execução automática e periódica
* Utiliza formato crontab (`* * * * *`) para agendamento
* Pode ser suspenso/retomado conforme necessário

## Configuração de Autenticação e Autorização

### Modos de Autenticação

O Argo Server está configurado para utilizar autenticação via SSO (Single Sign-On) através do Google:

```yaml

server:
  extraArgs:
    - --auth-mode=sso
  sso:
    enabled: true
    issuer: https://accounts.google.com
    redirectUrl: "https://argo-workflows.seazone.com.br/oauth2/callback"
    scopes:
      - email
      - profile
```

### Service Accounts e RBAC

O Argo Workflows utiliza o sistema de RBAC (Role-Based Access Control) do Kubernetes para controlar o acesso aos recursos.

#### Service Accounts para Usuários

Foram configuradas várias service accounts para autenticação via UI:


1. **argo-workflows-admin-user** - Acesso administrativo completo
   * ClusterRole: `argo-workflows-admin`
   * Regra RBAC: `email == 'john.paiva@seazone.com.br'`
   * Precedência: 10
2. **argo-workflows-edit-user** - Acesso de edição
   * ClusterRole: `argo-workflows-edit`
   * Regra RBAC: `hasSuffix(email, '@seazone.com.br') && email != 'john.paiva@seazone.com.br'`
   * Precedência: 5
3. **argo-workflows-view-user** - Acesso somente leitura
   * ClusterRole: `argo-workflows-view`
   * Regra RBAC: `true` (regra de fallback)
   * Precedência: 0

#### Service Account para Execução de Workflows

A service account utilizada para executação dos workflows é a `argo-workflow`:

* Tem permissões para criar e gerenciar pods e outros recursos necessários
* Possui binding com a role `argo-workflows-workflow-agent` para permissões específicas do agente
* Configurada como padrão para todos os workflows através de `workflowDefaults`

```yaml

workflowDefaults:
  spec:
    serviceAccountName: argo-workflow
```

#### Tokens de Service Account

Cada service account possui um token associado, configurado como Secret:

```yaml

apiVersion: v1

kind: Secret

metadata:
  name: argo-workflow.service-account-token
  namespace: tools
  annotations:
    kubernetes.io/service-account.name: argo-workflow

type: kubernetes.io/service-account-token
```

### Permissões Necessárias para Workflows

Os workflows requerem permissões específicas para operar corretamente:


1. **Controller** - Precisa de permissões para gerenciar workflows, pods e outros recursos
2. **Agent** - Precisa de permissões para atualizar workflowtasksets

A configuração correta das roles é essencial para o funcionamento adequado dos workflows. A service account `argo-workflow` possui todas as permissões necessárias para executar workflows, incluindo:

* Criação e gerenciamento de pods
* Leitura e escrita de workflowtasksets
* Acesso ao armazenamento de artefatos

## Armazenamento e Persistência

### Armazenamento de Artefatos

O Argo Workflows está configurado para armazenar artefatos no Amazon S3:

```yaml

artifactRepository:
  archiveLogs: true
  s3:
    bucket: seazone-argo-workflows-artifacts-prod
    region: us-west-2
    endpoint: s3.us-west-2.amazonaws.com
    useSDKCreds: true
    keyFormat: "{{workflow.namespace}}/{{workflow.name}}/{{pod.name}}"
    encryptionOptions:
      enableEncryption: true
```

**Características**:

* Utiliza autenticação via IAM Role (`ArgoWorkflowsS3AccessRole`)
* Armazena artefatos e logs em buckets S3
* Suporta estrutura de diretórios dinâmica baseada no namespace, nome do workflow e nome do pod
* Ativa criptografia para artefatos

### Ciclo de Vida dos Logs no S3

Os logs armazenados no bucket S3 possuem uma política de ciclo de vida configurada via Terraform:

```terraform

resource "aws_s3_bucket_lifecycle_configuration" "logs_lifecycle" {
  bucket = aws_s3_bucket.argo_workflows_logs_prod.id

  rule {
    id     = "logs-expiration"
    status = "Enabled"

    filter {
      prefix = ""  # Apply rule to all objects in the bucket
    }

    expiration {
      days = 60
    }
  }
}
```

**Características**:

* Rotação automática de logs após 60 dias
* Aplicada a todos os objetos no bucket de logs
* Otimiza custos de armazenamento a longo prazo
* Complementa a política de arquivamento interno (7 dias)

### Multiple Artifact Repositories

Configuramos múltiplos repositórios de artefatos para diferentes propósitos:

```yaml

artifactRepositoryRef:
  artifact-repositories:
    annotations:
      workflows.argoproj.io/default-artifact-repository: default-aws-s3-artifact-repository
    default-aws-s3-artifact-repository:
      archiveLogs: true
      s3:
        bucket: seazone-argo-workflows-artifacts-prod
        # ...
    log-storage-s3-repository:
      archiveLogs: true
      s3:
        bucket: seazone-argo-workflows-logs-prod
        # ...
```

**Características**:

* Repositório padrão para artefatos gerais
* Repositório otimizado para logs
* Selecionável por workflow ou template

### Volume Persistence

A configuração padrão de volume foi desabilitada para evitar dependência do EFS, que apresentava problemas de estabilidade. Os workflows devem:


1. Utilizar armazenamento temporário (`/tmp`) para arquivos locais
2. Utilizar artefatos S3 para compartilhar dados entre steps
3. Especificar explicitamente PVCs quando necessário

```yaml
# Exemplo de workflow usando apenas armazenamento temporário e S3

apiVersion: argoproj.io/v1alpha1

kind: Workflow

metadata:
  generateName: example-s3-
spec:
  entrypoint: main
  templates:
  - name: main
    container:
      image: alpine
      command: [sh, -c]
      args: ["echo 'Hello' > /tmp/hello.txt"]
    outputs:
      artifacts:
      - name: hello
        path: /tmp/hello.txt
        s3:
          key: examples/hello.txt
```

### Arquivamento de Workflows

Os workflows completos são arquivados em um banco de dados PostgreSQL:

```yaml

persistence:
  postgresql:
    host: postgres-postgresql.tools.svc.cluster.local
    port: 5432
    database: workflows
    tableName: argo_workflows
    userNameSecret:
      name: argo-workflows-postgresql
      key: postgresql-username
    passwordSecret:
      name: argo-workflows-postgresql
      key: postgresql-password
  archive: true
  archiveTTL: 168h # 7 dias
```

**Características**:

* Preserva o histórico completo de execução dos workflows
* Permite consultas e buscas por workflows concluídos
* Mantém registros por 7 dias antes da limpeza automática

## Execução de Workflows

### Padrões e Boas Práticas

Para execução eficiente de workflows no ambiente, siga estas práticas:


1. **Evite Volumes Persistentes**: Use `/tmp` e artefatos S3 sempre que possível
2. **Configure Timeouts**: Use `activeDeadlineSeconds` para evitar workflows presos
3. **Arquive Logs**: Defina `archiveLogs: true` para preservar logs
4. **Utilize Paralelismo**: Use DAGs para execução concorrente

### Configurações Padrão

Todos os workflows herdam estas configurações padrão:

```yaml

workflowDefaults:
  spec:
    serviceAccountName: argo-workflow
    podGC:
      strategy: OnWorkflowCompletion
    activeDeadlineSeconds: 7200  # 2 horas
    ttlStrategy:
      secondsAfterCompletion: 86400  # 1 dia
    artifactGC:
      serviceAccountName: "argo-workflow"
    artifactRepositoryRef:
      key: default-aws-s3-artifact-repository
      configMap: artifact-repositories
```

### Limites de Recursos

O Argo Workflows possui configurações de limites de recursos para garantir estabilidade:

* **Workflow Controller**: 200m CPU, 256Mi memória
* **Argo Server**: 100m CPU, 128Mi memória
* **Executor**: 100m CPU, 128Mi memória

### Políticas de Retenção

```yaml

retentionPolicy:
  completed: 100  # Máximo de workflows completos
  failed: 50      # Máximo de workflows falhos
  errored: 50     # Máximo de workflows com erro
```

## Resolução de Problemas

### Problemas Comuns

#### Workflows Presos em Status "Running"

Geralmente causado por:


1. **Problemas de permissões**: Verifique se a service account tem permissões adequadas

   ```bash
   kubectl get rolebinding -n tools | grep argo
   ```
2. **Falha de volume**: Se usando PVC, verifique se o volume pode ser montado

   ```bash
   kubectl describe pod <pod-name> -n tools
   ```
3. **Token ausente**: Verifique se existe um token para a service account

   ```bash
   kubectl get secret -n tools | grep service-account-token
   ```

#### Falhas em Artefatos S3

Possíveis causas:


1. **Permissões IAM**: Verifique se a role `ArgoWorkflowsS3AccessRole` tem permissões adequadas
2. **Configuração de Bucket**: Verifique se os buckets existem e estão acessíveis

#### Erros de "workflowtasksets forbidden"

Significa que a service account do workflow não tem permissões para atualizar workflowtasksets.

Solução:


1. Use `argo-workflow` como service account
2. Verifique se o RoleBinding `argo-workflows-workflow-agent` está correto

### Comandos Úteis

```bash
# Verificar logs do controller

kubectl logs -n tools deployment/argo-workflows-workflow-controller

# Verificar pods de um workflow

kubectl get pods -n tools -l workflows.argoproj.io/workflow=<workflow-name>

# Verificar detalhes de um workflow

kubectl get workflow <workflow-name> -n tools -o yaml

# Reiniciar o controller (em caso de problemas persistentes)
kubectl rollout restart deployment argo-workflows-workflow-controller -n tools
```

## Referências

* [Documentação Oficial do Argo Workflows](https://argo-workflows.readthedocs.io/en/latest/)
* [Configuração de Artefatos](https://argo-workflows.readthedocs.io/en/latest/configure-artifact-repository/)
* [Arquivamento de Workflows](https://argo-workflows.readthedocs.io/en/latest/workflow-archive/)
* [Configuração de SSO](https://argo-workflows.readthedocs.io/en/latest/argo-server-sso/)
* [Workflow RBAC](https://argo-workflows.readthedocs.io/en/latest/workflow-rbac/)
* [Service Accounts](https://argo-workflows.readthedocs.io/en/latest/service-accounts/)



---

# CI/CD 

O objetivo do CI/CD é implementar os workflows no argo de forma dinâmica e automatizada, além disso conseguimos manter uma padronização desses deploys e versionamento ativo em todos os workflows implantados 

## Como funciona :question:

O workflow é ativado quando algum push é feito na branch `main` ou na `staging` em uma das pastas  predefinidas para os times que atualmente são `Governança`, `Backoffice`, `Hosting`, `Reservas`

### Então qual é o fluxo ideal :question:

Vamos trazer aqui uma situação onde desejamos criar um novo workflow para o time de governança 

:one: Crie uma branch nova para fazer a criação desse workflow 

 ![](/api/attachments.redirect?id=ba5aa0c6-2dff-4692-b15b-9e6cc2009ecb "left-50 =656x65")


\
:two: Adicione o novo workflow na pasta do time que fará uso e será responsável por aquele fluxo, no nosso caso será a pasta `governanca`

 ![](/api/attachments.redirect?id=e9f75c3d-1617-40de-9b0b-fe92d1f67311 "left-50 =284x90")


\

:three: Faça o commit e faça uma PR da nova branch para a `staging` ![](/api/attachments.redirect?id=08b69f84-3912-4ae6-bd1a-301b812bbf7f "left-50 =724x74")


\

Quando a Pull Request for mergeada e o push for feito o workflow para deploy em staging iniciará, significa que após a action de deploy ser finalizada você já poderá visualizar seu workflow no ambiente de staging do argo : <https://argo-workflows-stg.seazone.com.br/>

 ![](/api/attachments.redirect?id=508cba3b-51b5-4b4b-8c2a-2e798b3f0a04 "left-50 =821x186")


\

\

\
:five: Após testado e validado o workflow no ambiente de staging a PR pode ser aberta pra branch main, onde o processo será basicamente o mesmo, porém agora o workflow será deployado no ambiente de produção : <https://argo-workflows.seazone.com.br/login?redirect=https://argo-workflows.seazone.com.br/>

 ![](/api/attachments.redirect?id=308abd2a-c4f9-449d-9972-d2f1c4e89034 " =996x109")