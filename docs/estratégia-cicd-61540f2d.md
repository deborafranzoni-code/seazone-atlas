<!-- title: Estratégia CI/CD | url: https://outline.seazone.com.br/doc/estrategia-cicd-7MqVYs4Ode | area: Tecnologia -->

# Estratégia CI/CD

## 📋 Visão Geral

Estratégia de CI/CD otimizada para o novo pattern de repositórios, utilizando **workflows reutilizáveis**, **ArgoCD GitOps** e **infraestrutura como código** em um cluster único.

## 🔄 Arquitetura Completa

### **Fluxo Principal**

```mermaidjs

graph TD
    A["👨‍💻 Developer Push/Tag"] -->|1| B["📦 CI Build"]
    B -->|2a| C["💬 Notifications"]
    B -->|2b| D["🔄 GitOps Update"]
    D -->|3| E["📝 Commit to GitOps Repo"]
    E -->|4| F["🤖 ArgoCD Sync"]
    F -->|5| G["☸️ Kubernetes Deploy"]
    
    C -.->|paralelo| I["👥 Team Notified"]
    
    style A fill:#1e3a8a
    style B fill:#dc2626
    style C fill:#7c3aed
    style D fill:#059669
    style E fill:#059669
    style F fill:#059669
    style G fill:#059669
    style I fill:#7c3aed
```

### **Separação de Responsabilidades**

```mermaidjs

graph LR
    subgraph "💻 Time de Produto"
        A1["Desenvolvimento de Código"]
        A2["Teste de Funcionalidades"]
        A3["Correção de Bugs"]
    end
    
    subgraph "🏛️ Time de Governança/Infra"
        B1["Gestão GitOps"]
        B2["Terraform/Terragrunt"]
        B3["Configuração ArgoCD"]
        B4["Monitoramento e Alertas"]
    end
    
    subgraph "🤖 Automação"
        C1["Workflows CI/CD"]
        C2["Sincronização ArgoCD"]
        C3["Aplicação Terraform"]
    end
    
    A1 -->|push código| C1
    C1 -->|atualizar manifests| B1
    B1 -->|disparar| C2
    C2 -->|deploy| D1["☸️ Kubernetes"]
    
    B2 -->|provisionar| C3
    C3 -->|criar| D1
    
    style A1 fill:#1e3a8a
    style A2 fill:#1e3a8a
    style A3 fill:#1e3a8a
    style B1 fill:#7c3aed
    style B2 fill:#7c3aed
    style B3 fill:#7c3aed
    style B4 fill:#7c3aed
    style C1 fill:#dc2626
    style C2 fill:#dc2626
    style C3 fill:#dc2626
    style D1 fill:#059669
```

### **Arquitetura de Repositórios e Workflows**

```mermaidjs

graph TB
    subgraph "📦 App Repository"
        A1["reservas-api-sa-east-1"]
        A2["ci.yaml"]
        A3["semantic-version.yaml"]
    end
    
    subgraph "🏛️ GitOps Governança"
        B1["gitops-governanca"]
        B2["Workflows Templates"]
        B3["Actions"]
        B4["app-ci-build.yaml"]
        B5["app-ci-gitops-update.yaml"]
        B6["app-ci-slack.yaml"]
        B7["semantic-version action"]
    end
    
    subgraph "🔄 GitOps App"
        C1["gitops-reservas"]
        C2["helm/api/values-*.yaml"]
        C3["argocd/applicationSet"]
    end
    
    subgraph "🤖 ArgoCD"
        D1["Application Sets"]
        D2["Sync Policy"]
    end
    
    subgraph "☸️ Kubernetes"
        E1["general-cluster"]
        E2["Namespace: dev"]
        E3["Namespace: stg"]
        E4["Namespace: prd"]
    end
    
    A1 -->|chama| B2
    B2 -->|usa| B3
    B4 -->|atualiza| C2
    B5 -->|commit| C1
    C1 -->|monitora| D1
    D1 -->|aplica| E1
    
    style A1 fill:#1e3a8a
    style B1 fill:#7c3aed
    style C1 fill:#059669
    style D1 fill:#dc2626
    style E1 fill:#059669
```

## 🛠️ Workflows Implementados

### **📦 Semantic Version Workflow**

**Arquivo**: `.github/workflows/semantic-version.yaml`

**Propósito**: Gera versões semânticas automaticamente baseadas no título do PR.

**Triggers**:

```yaml

on:
  pull_request:
    types: [closed]
    branches:
      - "staging"
      - "main"
      - "hotfix/*"
  workflow_dispatch:  # Para execução manual
```

**Funcionalidades**:

* ✅ **Análise do título do PR** seguindo Conventional Commits
* ✅ **Geração automática de tags** semânticas
* ✅ **Criação de GitHub Releases** (pré-release ou release)
* ✅ **Disparo do CI Pipeline** via `repository_dispatch`
* ✅ **Suporte a hotfixes** com sufixo `-hf`
* ✅ **Validação de duplicatas** antes de criar releases

**Exemplo de execução**:

```bash
# PR: feat: Implementar sistema de notificações
# Branch: develop → staging
# Resultado: 0.2.0-rc.0 (incrementa minor)
# GitHub Release: Criada como pré-release
# CI Pipeline: Disparado automaticamente
```

### **🏗️ CI Pipeline Workflow**

**Arquivo**: `.github/workflows/ci.yaml`

**Propósito**: Pipeline principal de CI/CD com build, deploy e notificações.

**Triggers**:

```yaml

on:
  repository_dispatch:
    types: [semantic-version-completed]
  workflow_dispatch:  # Para execução manual
```

**Jobs**:


1. **Build Development** (`develop` branch)
2. **Build Staging** (`staging` branch)
3. **Build Production** (`main` branch)
4. **Slack Notifications** (todos os ambientes)
5. **GitOps Updates** (todos os ambientes)

**Funcionalidades**:

* ✅ **Build automático** por ambiente
* ✅ **Push para ECR** com tags semânticas
* ✅ **Notificações Slack** com status e comandos Docker
* ✅ **Atualização GitOps** com versões corretas
* ✅ **Controle de ambiente** via `repository_dispatch`

### **🔄 GitOps Update Workflow**

**Arquivo**: `gitops-governanca/.github/workflows/app-ci-gitops-update.yaml`

**Propósito**: Atualiza repositórios GitOps com novas versões.

**Inputs**:

```yaml

inputs:
  gitops_repo: "gitops-reservas"
  app_name: "reservas-frontend"
  version: "0.2.0-rc.0"
  values_path: "helm/frontend/values-stg.yaml"
  tag_path: "app.image.tag"
```

**Funcionalidades**:

* ✅ **Atualização flexível** de qualquer arquivo values
* ✅ **Controle total** sobre caminho da tag no YAML
* ✅ **Validação de mudanças** antes do commit
* ✅ **Backup automático** do arquivo original
* ✅ **Commit e push** automático

**Exemplo de atualização**:

```yaml
# Antes

app:
  image:
    tag: "0.1.0-rc.2"

# Depois

app:
  image:
    tag: "0.2.0-rc.0"
```

### **💬 Slack Notification Workflow**

**Arquivo**: `gitops-governanca/.github/workflows/app-ci-slack.yaml`

**Propósito**: Envia notificações detalhadas para o Slack.

**Funcionalidades**:

* ✅ **Notificações por ambiente** (dev, stg, prd)
* ✅ **Status do build** (success, failure, cancelled)
* ✅ **Comandos Docker** para pull da imagem
* ✅ **Links para workflow** no GitHub
* ✅ **Canais específicos** por ambiente

**Exemplo de notificação**:

```
✅ Build reservas-frontend 0.2.0-rc.0

Build da versão 0.2.0-rc.0 de reservas-frontend foi concluído com sucesso para stg.

Environment: stg

Tag: 0.2.0-rc.0

Status: sucesso

📦 Comandos Docker ECR:
docker pull 711387131913.dkr.ecr.sa-east-1.amazonaws.com/reservas-frontend:0.2.0-rc.0
```

### **🔍 PR Title Validator Workflow**

**Arquivo**: `.github/workflows/pr-title-validator.yaml`

**Propósito**: Valida títulos de PR seguindo Conventional Commits.

**Triggers**:

```yaml

on:
  pull_request:
    types: [opened, edited, synchronize]
```

**Configuração**:

```yaml
- name: Validate PR title format
  uses: amannn/action-semantic-pull-request@v5.5.3
  with:
    types: |
      feat
      fix
      docs
      style
      refactor
      test
      chore
      perf
      ci
      build
      revert
    requireScope: false
    subjectPattern: ^[A-Z].+$
    wip: true
```

**Funcionalidades**:

* ✅ **Validação de tipos** de commit permitidos
* ✅ **Verificação de formato** do título
* ✅ **Suporte a WIP** (Work in Progress)
* ✅ **Mensagens em português** para erros
* ✅ **Bloqueio de merge** se título inválido

## 🏷️ Semantic Versioning Detalhado

### **📊 Estratégia de Versionamento por Branch**

| Branch | Trigger | Tag Gerada | Exemplo | Observações |
|----|----|----|----|----|
| **develop** | PR Merge | `dev-{sha}` | `dev-a1b2c3d` | Apenas identificação, não semantic version |
| **staging** | PR Merge | `{version}-rc.{n}` | `0.2.1-rc.3` | Pré-release com semantic version |
| **main** | PR Merge | `{version}` | `0.2.1` | Release final com semantic version |
| **hotfix/**\* | PR Merge | `{version}-hf.{n}` | `0.2.2-hf.0` | Hotfix com semantic version |

### **🔢 Lógica de Incremento Detalhada**

#### **Para Branch** `staging`:

| Tipo de PR | Análise | Incremento | Exemplo |
|----|----|----|----|
| `feat:` | Nova funcionalidade | **Minor** | `0.1.0` → `0.2.0-rc.0` |
| `fix:` | Correção de bug | **Patch** | `0.1.0` → `0.1.1-rc.0` |
| `feat!:` | Breaking change | **Major** | `0.1.0` → `1.0.0-rc.0` |
| `docs:`, `style:`, `refactor:`, `test:`, `chore:` | Mudanças internas | **RC apenas** | `0.1.0-rc.1` → `0.1.0-rc.2` |

#### **Para Branch** `main`:

| Cenário | Lógica | Resultado | Exemplo |
|----|----|----|----|
| **Com RC existente** | Usa versão base da RC | Remove sufixo `-rc` | `0.2.1-rc.3` → `0.2.1` |
| **Sem RC** | Incrementa minor | Nova versão | `0.2.1` → `0.3.0` |

#### **Para Branch** `hotfix/*`:

| Cenário | Lógica | Resultado | Exemplo |
|----|----|----|----|
| **Qualquer tipo** | Sempre incrementa patch | Adiciona sufixo `-hf` | `0.2.1` → `0.2.2-hf.0` |

### **🎯 Tags Especiais para Forçar Incremento**

Você pode forçar o tipo de incremento usando tags especiais no **título do PR**:

| Tag | Incremento | Exemplo PR Title | Resultado |
|----|----|----|----|
| `#major` | **Major** | `feat: nova API #major` | `0.1.0` → `1.0.0-rc.0` |
| `#minor` | **Minor** | `feat: nova funcionalidade #minor` | `0.1.0` → `0.2.0-rc.0` |
| `#patch` | **Patch** | `fix: correção #patch` | `0.1.0` → `0.1.1-rc.0` |

### **📋 Cenários Detalhados de Versionamento**

#### **Cenário 1: Nova Funcionalidade (staging)**

```
Atual: 0.2.1-rc.2

PR: feat: Adicionar sistema de notificações

Análise: feat = nova funcionalidade = minor bump

Resultado: 0.3.0-rc.0 (incrementa minor)
GitHub Release: Criada como pré-release

CI Pipeline: Disparado para staging
```

#### **Cenário 2: Correção de Bug (staging)**

```
Atual: 0.2.1-rc.2

PR: fix: Corrigir erro de login

Análise: fix = correção de bug = patch bump

Resultado: 0.2.2-rc.0 (incrementa patch)
GitHub Release: Criada como pré-release

CI Pipeline: Disparado para staging
```

#### **Cenário 3: Breaking Change (staging)**

```
Atual: 0.2.1-rc.2

PR: feat!: Refatorar API de usuários

Análise: feat! = breaking change = major bump

Resultado: 1.0.0-rc.0 (incrementa major)
GitHub Release: Criada como pré-release

CI Pipeline: Disparado para staging
```

#### **Cenário 4: Documentação (staging)**

```
Atual: 0.2.1-rc.2

PR: docs: Atualizar README

Análise: docs = documentação = RC apenas

Resultado: 0.2.1-rc.3 (apenas incrementa RC)
GitHub Release: Criada como pré-release

CI Pipeline: Disparado para staging
```

#### **Cenário 5: Staging → Main (Release Final)**

```
Atual: 0.2.1-rc.3

PR: release: User authentication v0.2.1

Análise: RC existente, converte para release

Resultado: 0.2.1 (remove sufixo -rc)
GitHub Release: Criada como release final

CI Pipeline: Disparado para production
```

#### **Cenário 6: Hotfix Urgente**

```
Atual: 0.2.1

PR: fix: Corrigir bug crítico em produção

Análise: hotfix = sempre patch + sufixo hf

Resultado: 0.2.2-hf.0 (hotfix)
GitHub Release: Criada como pré-release

CI Pipeline: Disparado para production
```

#### **Cenário 7: Desenvolvimento (develop)**

```
Atual: 0.2.1

PR: feat: Implementar nova funcionalidade

Análise: develop = apenas identificação

Resultado: dev-a1b2c3d (hash do commit)
GitHub Release: Não criada

CI Pipeline: Disparado para development
```

### **🔄 Fluxo Completo por Ambiente**

#### **🛠️ Fluxo de Desenvolvimento**

```mermaidjs

sequenceDiagram
    participant DEV as "👨‍💻 Desenvolvedor"
    participant FEAT as "🌿 Feature Branch"
    participant DEVELOP as "📘 Develop Branch"
    participant CI as "📦 CI Workflow"
    participant GITOPS as "🔄 GitOps Repo"
    participant ARGO as "🤖 ArgoCD"
    participant K8S as "☸️ Kubernetes"
    
    DEV->>FEAT: git checkout -b feature/user-login
    DEV->>FEAT: git commit -m "feat: implement login"
    DEV->>DEVELOP: Pull Request (feature → develop)
    
    Note over DEVELOP: Revisão e Aprovação do PR
    DEVELOP->>CI: Merge dispara CI
    
    par Build & Test
        CI->>CI: Gerar tag: dev-a1b2c3d
        CI->>CI: Build Docker Image
        CI->>CI: Executar Unit Tests
        CI->>CI: Push para ECR (dev-a1b2c3d)
    and Notificações
        CI->>CI: Enviar Notificação Slack
    end
    
    CI->>GITOPS: Atualizar values-dev.yaml
    GITOPS->>ARGO: Mudança Git detectada
    ARGO->>K8S: Deploy para namespace dev
    K8S->>DEV: ✅ Disponível em dev.app.seazone.com.br
    
    Note over FEAT: Auto-delete feature branch
    
    rect rgb(30, 58, 138)
        Note over DEV,FEAT: Desenvolvimento
    end
    rect rgb(220, 38, 38)
        Note over CI: CI/CD Pipeline
    end
    rect rgb(5, 150, 105)
        Note over GITOPS: GitOps
    end
    rect rgb(5, 150, 105)
        Note over ARGO,K8S: Deploy
    end
```

#### **🚀 Fluxo de Staging**

```mermaidjs

sequenceDiagram
    participant DEV as "👨‍💻 Desenvolvedor"
    participant DEVELOP as "📘 Develop Branch"
    participant STAGING as "🚦 Staging Branch"
    participant SEM as "📦 Semantic Version"
    participant CI as "📦 CI Workflow"
    participant GITOPS as "🔄 GitOps Repo"
    participant ARGO as "🤖 ArgoCD"
    participant K8S as "☸️ Kubernetes"
    
    DEV->>STAGING: Pull Request (develop → staging)
    Note over DEV: Título: "feat: user authentication system"
    
    Note over STAGING: Revisão e Aprovação do PR
    STAGING->>SEM: Analisar título do PR para versionamento semântico
    SEM->>SEM: Gerar tag: 0.2.0-rc.0 (feat = minor bump)
    
    STAGING->>CI: Tag dispara CI
    
    par Build & Security
        CI->>CI: Build Docker Image
        CI->>CI: Security Scan (Trivy)
        CI->>CI: Integration Tests
        CI->>CI: Push para ECR (0.2.0-rc.0)
    and Quality Gates
        CI->>CI: Performance Tests
        CI->>CI: E2E Tests
    end
    
    CI->>GITOPS: Atualizar values-stg.yaml
    GITOPS->>ARGO: Mudança Git detectada
    ARGO->>K8S: Deploy para namespace stg
    K8S->>DEV: ✅ Disponível em stg.app.seazone.com.br
    
    Note over DEVELOP: Auto-delete merged branch
    
    rect rgb(30, 58, 138)
        Note over DEV,DEVELOP: Desenvolvimento
    end
    rect rgb(124, 58, 237)
        Note over STAGING,SEM: Versionamento
    end
    rect rgb(220, 38, 38)
        Note over CI: CI/CD Pipeline
    end
    rect rgb(5, 150, 105)
        Note over GITOPS: GitOps
    end
    rect rgb(5, 150, 105)
        Note over ARGO,K8S: Deploy
    end
```

#### **✅ Fluxo de Produção**

```mermaidjs

sequenceDiagram
    participant DEV as "👨‍💻 Desenvolvedor"
    participant STAGING as "🚦 Staging Branch"
    participant MAIN as "🎯 Main Branch"
    participant SEM as "📦 Semantic Version"
    participant CI as "📦 CI Workflow"
    participant GITOPS as "🔄 GitOps Repo"
    participant ARGO as "🤖 ArgoCD"
    participant K8S as "☸️ Kubernetes"
    
    DEV->>MAIN: Pull Request (staging → main)
    Note over DEV: Título: "release: user authentication v0.2.0"
    
    Note over MAIN: Revisão e Aprovação do PR (Obrigatório)
    MAIN->>SEM: Converter tag RC para release
    SEM->>SEM: Gerar tag: 0.2.0 (remover sufixo -rc)
    
    MAIN->>CI: Tag dispara CI
    
    par Build & Security
        CI->>CI: Build Production Image
        CI->>CI: Full Security Scan
        CI->>CI: Compliance Checks
        CI->>CI: Push para ECR (0.2.0)
    and Quality Gates
        CI->>CI: Final Integration Tests
        CI->>CI: Performance Validation
    end
    
    CI->>GITOPS: Atualizar values.yaml
    GITOPS->>ARGO: Mudança Git detectada
    ARGO->>K8S: Deploy para namespace prd
    K8S->>DEV: ✅ Disponível em app.seazone.com.br
    
    Note over STAGING: Auto-delete merged branch
    
    rect rgb(30, 58, 138)
        Note over DEV,STAGING: Desenvolvimento
    end
    rect rgb(124, 58, 237)
        Note over MAIN,SEM: Release
    end
    rect rgb(220, 38, 38)
        Note over CI: CI/CD Pipeline
    end
    rect rgb(5, 150, 105)
        Note over GITOPS: GitOps
    end
    rect rgb(5, 150, 105)
        Note over ARGO,K8S: Deploy
    end
```

## 📊 Estratégia de Branching e Deploys

### **🌿 Branch Protection Strategy**

```mermaidjs

gitGraph
    commit id: "Initial"
    branch develop
    checkout develop
    commit id: "ci: setup develop"
    branch feature/user-auth
    checkout feature/user-auth
    commit id: "feat: login"
    commit id: "feat: logout"
    checkout develop
    merge feature/user-auth
    commit id: "ci: auto-deploy dev"
    branch staging
    checkout staging
    commit id: "0.2.0-rc.0"
    commit id: "ci: auto-deploy stg"
    checkout main
    merge staging
    commit id: "0.2.0"
    commit id: "ci: auto-deploy prd"
```

#### **Branch Protection Rules**

| Branch | Protection | Direct Push | Auto-Deploy | Tag Strategy |
|----|----|----|----|----|
| **develop** | ✅ Protegida | ❌ Só via PR\* | ✅ Automático | `dev-{commit-sha}` |
| **staging** | ✅ Protegida | ❌ Só via PR | ✅ Automático | `{major}.{minor}.{patch}-rc` |
| **main** | ✅ Protegida | ❌ Só via PR | ✅ Automático | `{major}.{minor}.{patch}` |

\**Exceção: develop permite push direto apenas para hot-fixes urgentes*

## 🏷️ Semantic Versioning e Conventional Commits

### **📋 Estratégia de Versionamento**

O versionamento semântico é aplicado **apenas** em branches `staging` e `main`, seguindo o padrão [Semantic Versioning 2.0.0](https://semver.org/).

#### **🎯 Regras de Versionamento por Branch**

| Branch | Trigger | Tag Gerada | Exemplo | Observações |
|----|----|----|----|----|
| **develop** | Push/Merge | `dev-{sha}` | `dev-a1b2c3d` | Apenas identificação, não semantic version |
| **staging** | Push/Merge | `{version}-rc` | `0.1.10-rc` | Pré-release com semantic version |
| **main** | Push/Merge | `{version}` | `0.1.10` | Release final com semantic version |
| **hotfix/**\* | Push/Merge | `{version}-hf` | `0.1.11-hf` | Hotfix com semantic version |

#### **🔢 Incremento de Versão**

O incremento é determinado pelo **título do PR** seguindo Conventional Commits:

| Tipo de Commit | Incremento | Exemplo PR Title | Nova Versão |
|----|----|----|----|
| `feat:` | **Minor** | `feat: nova funcionalidade` | `0.1.0` → `0.2.0` |
| `fix:` | **Patch** | `fix: correção de bug` | `0.1.0` → `0.1.1` |
| `BREAKING CHANGE:` | **Major** | `feat!: breaking change` | `0.1.0` → `1.0.0` |
| `docs:`, `style:`, `refactor:`, `test:`, `chore:` | **Patch** | `docs: atualizar README` | `0.1.0` → `0.1.1` |

#### **🏷️ Tags Especiais para Forçar Incremento**

Você pode forçar o tipo de incremento usando tags especiais no **título do PR**:

| Tag | Incremento | Exemplo PR Title | Resultado |
|----|----|----|----|
| `#major` | **Major** | `feat: nova API #major` | `0.1.0` → `1.0.0` |
| `#minor` | **Minor** | `feat: nova funcionalidade #minor` | `0.1.0` → `0.2.0` |
| `#patch` | **Patch** | `fix: correção #patch` | `0.1.0` → `0.1.1` |

### **✅ Validação de PRs**

#### **📋 Template de Pull Request**

```markdown
## 📝 Descrição
<!-- Descreva as mudanças realizadas -->

## 🏷️ Tipo de Mudança
- [ ] `feat:` Nova funcionalidade (incrementa minor)
- [ ] `fix:` Correção de bug (incrementa patch)
- [ ] `docs:` Documentação (incrementa patch)
- [ ] `style:` Formatação (incrementa patch)
- [ ] `refactor:` Refatoração (incrementa patch)
- [ ] `test:` Testes (incrementa patch)
- [ ] `chore:` Tarefas de manutenção (incrementa patch)
- [ ] `BREAKING CHANGE:` Mudança que quebra compatibilidade (incrementa major)

## 🔍 Checklist
- [ ] Código testado localmente
- [ ] Testes passando
- [ ] Documentação atualizada
- [ ] Título do PR segue Conventional Commits
- [ ] Branch atualizada com a base

## 🚀 Impacto no Versionamento
<!-- Descreva qual será o impacto no versionamento semântico -->
```

#### **🤖 Validação Automática**

O workflow `semantic-version.yaml` valida automaticamente:


1. **Formato do título**: Deve seguir Conventional Commits
2. **Presença de tags especiais**: `#major`, `#minor`, `#patch`
3. **Tipo de branch**: Determina se gera tag semantic ou apenas identificação

## 🔐 Configuração de Variáveis e Secrets

### **📋 Variáveis de Organização**

As variáveis estão configuradas no nível da organização GitHub para centralizar a configuração e facilitar a manutenção.

#### **🏗️ Apps Repository (**`reservas-api-sa-east-1`)

```yaml
# AWS Credentials - Cluster Único

AWS_GENERAL_ACCOUNT_ID: "711387131913"
AWS_GENERAL_ACCOUNT_REGION: "sa-east-1"
AWS_GENERAL_DEPLOYMENT_ROLE: "GitHubActions-General"
AWS_GENERAL_CLUSTER_NAME: "general-cluster"

# Notifications

SLACK_BOT_TOKEN: "xoxb-..."  # Token do bot Slack

# GitOps Access

GH_TOKEN: "ghp_..."  # Token para acessar repositórios GitOps
```

#### **🔧 GitOps Repository (**`gitops-reservas`)

```yaml
# AWS Credentials (mesmas do Apps Repository)
AWS_GENERAL_ACCOUNT_ID: "711387131913"
AWS_GENERAL_ACCOUNT_REGION: "sa-east-1"
AWS_GENERAL_DEPLOYMENT_ROLE: "GitHubActions-General"
AWS_GENERAL_CLUSTER_NAME: "general-cluster"
```

### **🔐 Secrets de Organização**

```yaml
# Secrets de Organização

SLACK_BOT_TOKEN: "xoxb-your-slack-bot-token"
GH_TOKEN: "ghp-your-github-token"
```

### **🛠️ Como Configurar**

#### **1. No GitHub Organization Settings:**


1. Vá para **Settings** → **Secrets and variables** → **Actions**
2. Clique em **Variables** (não Secrets)
3. Adicione cada variável:

```bash
# Variáveis de Organização

AWS_GENERAL_ACCOUNT_ID=711387131913

AWS_GENERAL_ACCOUNT_REGION=sa-east-1

AWS_GENERAL_DEPLOYMENT_ROLE=GitHubActions-General

AWS_GENERAL_CLUSTER_NAME=general-cluster
```

#### **2. Secrets (privados):**

```bash
# Secrets de Organização

SLACK_BOT_TOKEN=xoxb-your-slack-bot-token

GH_TOKEN=ghp-your-github-token
```

## 🛡️ IAM Roles e Permissões

### **🔐 GitHubActions-General Role**

Esta role é utilizada pelos workflows do GitHub Actions para autenticar com a AWS e realizar operações no cluster EKS.

#### **Trust Policy:**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::711387131913:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
        },
        "StringLike": {
          "token.actions.githubusercontent.com:sub": "repo:seazone-tech/*"
        }
      }
    }
  ]
}
```

#### **Permissions Policy:**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ecr:GetAuthorizationToken",
        "ecr:BatchCheckLayerAvailability",
        "ecr:GetDownloadUrlForLayer",
        "ecr:BatchGetImage",
        "ecr:PutImage",
        "ecr:InitiateLayerUpload",
        "ecr:UploadLayerPart",
        "ecr:CompleteLayerUpload",
        "ecr:DescribeImages",
        "ecr:BatchDeleteImage"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "eks:DescribeCluster",
        "eks:ListClusters"
      ],
      "Resource": "arn:aws:eks:sa-east-1:711387131913:cluster/general-cluster"
    },
    {
      "Effect": "Allow",
      "Action": [
        "ssm:GetParameter",
        "ssm:GetParameters",
        "ssm:GetParametersByPath"
      ],
      "Resource": "arn:aws:ssm:sa-east-1:711387131913:parameter/seazone/*"
    }
  ]
}
```

### **🎯 Por que essa configuração?**


1. **OIDC Federation**: Permite autenticação segura sem armazenar credenciais AWS no GitHub
2. **Principle of Least Privilege**: A role tem apenas as permissões necessárias
3. **ECR Access**: Para push/pull de imagens Docker
4. **EKS Access**: Para verificar status do cluster
5. **SSM Access**: Para obter parâmetros de configuração

## 🗂️ Workflows Reutilizáveis

### **Estrutura dos Templates**

```
gitops-governanca/workflows-templates/.github/
├── workflows/
│   ├── app-ci-build.yaml           # 🏗️ Build & Push universal
│   ├── app-ci-slack.yaml           # 💬 Notificações Slack
│   ├── app-ci-gitops-update.yaml   # 🔄 Update GitOps repos
└── actions/
    ├── semantic-version/            # 📦 Version bumping
    ├── run-tests/                   # 🧪 Test execution
    └── notification/                # 📢 Multi-channel notifications
```

### **🔐 Branch Protection Configuration**

```yaml
# .github/branch-protection.yaml (aplicado via GitHub CLI ou API)
branches:
  develop:
    protection:
      required_status_checks:
        strict: true
        contexts: ["ci/build", "ci/test"]
      enforce_admins: false
      required_pull_request_reviews:
        required_approving_review_count: 1
        dismiss_stale_reviews: true
        require_code_owner_reviews: true
      restrictions: null
      allow_force_pushes: true  # Apenas para hot-fixes
      allow_deletions: false
    auto_delete_head_branches: true
    
  staging:
    protection:
      required_status_checks:
        strict: true
        contexts: ["ci/build", "ci/security-scan", "ci/integration-tests"]
      enforce_admins: true
      required_pull_request_reviews:
        required_approving_review_count: 2
        dismiss_stale_reviews: true
        require_code_owner_reviews: true
      restrictions:
        users: []
        teams: ["time-governanca-infra"]
      allow_force_pushes: false
      allow_deletions: false
    auto_delete_head_branches: true
    
  main:
    protection:
      required_status_checks:
        strict: true
        contexts: ["ci/build", "ci/security-scan", "ci/compliance-check"]
      enforce_admins: true
      required_pull_request_reviews:
        required_approving_review_count: 2
        dismiss_stale_reviews: true
        require_code_owner_reviews: true
      restrictions:
        users: []
        teams: ["time-governanca-infra", "tech-leads"]
      allow_force_pushes: false
      allow_deletions: false
    auto_delete_head_branches: true
```

## 🏗️ Terraform Management

### **Terraform Deployment**

O Terraform será gerenciado **manualmente** pelo Time de Governança/Infra, sem workflows automáticos. Isso garante maior controle sobre mudanças de infraestrutura crítica.

```bash
# Deploy manual via Terragrunt

cd terraform-governanca/environments/dev

terragrunt run-all plan

terragrunt run-all apply

# Deploy específico por produto

cd terraform-governanca/environments/prd/wallet

terragrunt run-all plan

terragrunt run-all apply
```

## 🔐 Secrets Management

### **SSM Parameter Store Structure**

```
# Centralizado via Terraform - Padrão: servico/ambiente
/seazone/
├── reservas-api/
│   ├── dev/
│   │   ├── database-url
│   │   ├── jwt-secret
│   │   ├── redis-url
│   │   └── api-key
│   ├── stg/
│   │   ├── database-url
│   │   ├── jwt-secret
│   │   ├── redis-url
│   │   └── api-key
│   └── prd/
│       ├── database-url
│       ├── jwt-secret
│       ├── redis-url
│       └── api-key
├── reservas-frontend/
│   ├── dev/
│   │   ├── api-endpoint
│   │   └── analytics-key
│   ├── stg/
│   └── prd/
├── wallet-api/
│   ├── dev/
│   ├── stg/
│   └── prd/
└── sapron-api/
    ├── dev/
    ├── stg/
    └── prd/
```

**📋 Padrão de Nomenclatura:**

* **Formato**: `/servico/ambiente/variavel`
* **Exemplos**:
  * `/reservas-api/stg/database-url`
  * `/reservas-frontend/prd/api-endpoint`
  * `/wallet-api/dev/redis-url`

**🎯 Benefícios do Padrão:**

* **Organização clara** por serviço e ambiente
* **Isolamento** de configurações por ambiente
* **Facilita gestão** de permissões por serviço
* **Padronização** para automação

## 📊 Performance e Benefícios

### **⏱️ Comparação Temporal por Ambiente**

#### **🔧 Development Environment**

| Etapa | Fluxo Atual | Novo Fluxo | Economia |
|----|----|----|----|
| **PR Merge** | Manual | Automático | ✅ Integração contínua |
| **CI Build** | \~8min | \~5min | ✅ -3min (cache + paralelo) |
| **Image Tag** | manual/latest | `dev-{sha}` | ✅ Rastreabilidade |
| **GitOps Update** | \~2min | \~1min | ✅ -1min |
| **ArgoCD Sync** | Manual | \~30s | ✅ Automático |
| **Total** | **\~10min** | **\~6.5min** | **✅ -3.5min (35%)** |

#### **🚀 Staging Environment**

| Etapa | Fluxo Atual | Novo Fluxo | Economia |
|----|----|----|----|
| **PR Review** | Manual | Automático + Gates | ✅ Quality gates |
| **Tag Generation** | Manual | Semantic Version | ✅ Automático |
| **CI Build** | \~10min | \~8min | ✅ -2min |
| **Security Scan** | Manual | Automático | ✅ Integrado |
| **Deploy** | Manual | Automático | ✅ Zero-touch |
| **Total** | **\~20min** | **\~10min** | **✅ -10min (50%)** |

#### **✅ Production Environment**

| Etapa | Fluxo Atual | Novo Fluxo | Economia |
|----|----|----|----|
| **Release Prep** | \~30min | Automático | ✅ -30min |
| **Tag Creation** | Manual | Auto from RC | ✅ Sem erros |
| **Security Scan** | Manual | Automático | ✅ Compliance |
| **Deploy** | Manual | Automático pós-approval | ✅ Consistente |
| **Rollback** | \~15min | \~2min | ✅ -13min (87%) |
| **Total** | **\~45min** | **\~12min** | **✅ -33min (73%)** |

### **🎯 Principais Melhorias Alcançadas**

#### **🚀 Performance & Automação**

* **⚡ 35% mais rápido** em Development (10min → 6.5min)
* **⚡ 50% mais rápido** em Staging (20min → 10min)
* **⚡ 73% mais rápido** em Production (45min → 12min)
* **🤖 Zero-touch deploys** em todos os ambientes
* **📦 Semantic versioning** automático baseado em PR titles

#### **🛡️ Qualidade & Segurança**

* **🔒 Branch protection** com quality gates obrigatórios
* **🔍 Security scanning** automático em staging/prod
* **✅ Compliance checks** integrados no pipeline
* **🎯 Rastreabilidade completa** via tags semânticas
* **🔄 Rollback automático** em caso de falhas

#### **🧹 Organização & Governança**

* **🌿 Auto-delete branches** após merge aprovado
* **📋 PR templates** com conventional commits
* **👥 RBAC granular** por time e ambiente
* **📊 Observabilidade** completa do pipeline
* **📈 Workflows reutilizáveis** centralizados

## 🛡️ Rollback e Recuperação

### **📜 Rollback via Git** (Recomendado)

```bash
# No repositório GitOps

cd gitops-reservas

git log --oneline -5  # Ver últimos deploys

# Reverter para versão anterior

git revert HEAD

git push origin main

# ArgoCD detecta e faz rollback automático
```

### **⚡ Rollback via ArgoCD** (UI/CLI)

```bash
# Via CLI

argocd app rollback reservas-api-prd

# Via UI
# ArgoCD Dashboard → App → History → Rollback
```

### **🏗️ Rollback de Infraestrutura**

```bash
# Rollback manual via Terragrunt

cd terraform-governanca/environments/prd

git revert HEAD  # Reverter mudanças

terragrunt run-all plan  # Verificar changes

terragrunt run-all apply  # Aplicar rollback

# Ou aplicar versão específica

terragrunt run-all apply -target=module.specific_resource
```

## 🛠️ Workflows Implementados

### **📦 Semantic Version Workflow**

**Arquivo**: `.github/workflows/semantic-version.yaml`

**Propósito**: Gera versões semânticas automaticamente baseadas no título do PR.

**Triggers**:

```yaml

on:
  pull_request:
    types: [closed]
    branches:
      - "staging"
      - "main"
      - "hotfix/*"
  workflow_dispatch:  # Para execução manual
```

**Funcionalidades**:

* ✅ **Análise do título do PR** seguindo Conventional Commits
* ✅ **Geração automática de tags** semânticas
* ✅ **Criação de GitHub Releases** (pré-release ou release)
* ✅ **Disparo do CI Pipeline** via `repository_dispatch`
* ✅ **Suporte a hotfixes** com sufixo `-hf`
* ✅ **Validação de duplicatas** antes de criar releases

**Exemplo de execução**:

```bash
# PR: feat: Implementar sistema de notificações
# Branch: develop → staging
# Resultado: 0.2.0-rc.0 (incrementa minor)
# GitHub Release: Criada como pré-release
# CI Pipeline: Disparado automaticamente
```

### **🏗️ CI Pipeline Workflow**

**Arquivo**: `.github/workflows/ci.yaml`

**Propósito**: Pipeline principal de CI/CD com build, deploy e notificações.

**Triggers**:

```yaml

on:
  repository_dispatch:
    types: [semantic-version-completed]
  workflow_dispatch:  # Para execução manual
```

**Jobs**:


1. **Build Development** (`develop` branch)
2. **Build Staging** (`staging` branch)
3. **Build Production** (`main` branch)
4. **Slack Notifications** (todos os ambientes)
5. **GitOps Updates** (todos os ambientes)

**Funcionalidades**:

* ✅ **Build automático** por ambiente
* ✅ **Push para ECR** com tags semânticas
* ✅ **Notificações Slack** com status e comandos Docker
* ✅ **Atualização GitOps** com versões corretas
* ✅ **Controle de ambiente** via `repository_dispatch`

### **🔄 GitOps Update Workflow**

**Arquivo**: `gitops-governanca/.github/workflows/app-ci-gitops-update.yaml`

**Propósito**: Atualiza repositórios GitOps com novas versões.

**Inputs**:

```yaml

inputs:
  gitops_repo: "gitops-reservas"
  app_name: "reservas-frontend"
  version: "0.2.0-rc.0"
  values_path: "helm/frontend/values-stg.yaml"
  tag_path: "app.image.tag"
```

**Funcionalidades**:

* ✅ **Atualização flexível** de qualquer arquivo values
* ✅ **Controle total** sobre caminho da tag no YAML
* ✅ **Validação de mudanças** antes do commit
* ✅ **Backup automático** do arquivo original
* ✅ **Commit e push** automático

**Exemplo de atualização**:

```yaml
# Antes

app:
  image:
    tag: "0.1.0-rc.2"

# Depois

app:
  image:
    tag: "0.2.0-rc.0"
```

### **💬 Slack Notification Workflow**

**Arquivo**: `gitops-governanca/.github/workflows/app-ci-slack.yaml`

**Propósito**: Envia notificações detalhadas para o Slack.

**Funcionalidades**:

* ✅ **Notificações por ambiente** (dev, stg, prd)
* ✅ **Status do build** (success, failure, cancelled)
* ✅ **Comandos Docker** para pull da imagem
* ✅ **Links para workflow** no GitHub
* ✅ **Canais específicos** por ambiente

**Exemplo de notificação**:

```
✅ Build reservas-frontend 0.2.0-rc.0

Build da versão 0.2.0-rc.0 de reservas-frontend foi concluído com sucesso para stg.

Environment: stg

Tag: 0.2.0-rc.0

Status: sucesso

📦 Comandos Docker ECR:
docker pull 711387131913.dkr.ecr.sa-east-1.amazonaws.com/reservas-frontend:0.2.0-rc.0
```

### **🔍 PR Title Validator Workflow**

**Arquivo**: `.github/workflows/pr-title-validator.yaml`

**Propósito**: Valida títulos de PR seguindo Conventional Commits.

**Triggers**:

```yaml

on:
  pull_request:
    types: [opened, edited, synchronize]
```

**Configuração**:

```yaml
- name: Validate PR title format
  uses: amannn/action-semantic-pull-request@v5.5.3
  with:
    types: |
      feat
      fix
      docs
      style
      refactor
      test
      chore
      perf
      ci
      build
      revert
    requireScope: false
    subjectPattern: ^[A-Z].+$
    wip: true
```

**Funcionalidades**:

* ✅ **Validação de tipos** de commit permitidos
* ✅ **Verificação de formato** do título
* ✅ **Suporte a WIP** (Work in Progress)
* ✅ **Mensagens em português** para erros
* ✅ **Bloqueio de merge** se título inválido

## 🏷️ Semantic Versioning Detalhado

### **📊 Estratégia de Versionamento por Branch**

| Branch | Trigger | Tag Gerada | Exemplo | Observações |
|----|----|----|----|----|
| **develop** | Push/Merge | `dev-{sha}` | `dev-a1b2c3d` | Apenas identificação, não semantic version |
| **staging** | PR Merge | `{version}-rc.{n}` | `0.2.1-rc.3` | Pré-release com semantic version |
| **main** | PR Merge | `{version}` | `0.2.1` | Release final com semantic version |
| **hotfix/**\* | PR Merge | `{version}-hf.{n}` | `0.2.2-hf.0` | Hotfix com semantic version |

### **🔢 Lógica de Incremento Detalhada**

#### **Para Branch** `staging`:

| Tipo de PR | Análise | Incremento | Exemplo |
|----|----|----|----|
| `feat:` | Nova funcionalidade | **Minor** | `0.1.0` → `0.2.0-rc.0` |
| `fix:` | Correção de bug | **Patch** | `0.1.0` → `0.1.1-rc.0` |
| `feat!:` | Breaking change | **Major** | `0.1.0` → `1.0.0-rc.0` |
| `docs:`, `style:`, `refactor:`, `test:`, `chore:` | Mudanças internas | **RC apenas** | `0.1.0-rc.1` → `0.1.0-rc.2` |

#### **Para Branch** `main`:

| Cenário | Lógica | Resultado | Exemplo |
|----|----|----|----|
| **Com RC existente** | Usa versão base da RC | Remove sufixo `-rc` | `0.2.1-rc.3` → `0.2.1` |
| **Sem RC** | Incrementa minor | Nova versão | `0.2.1` → `0.3.0` |

#### **Para Branch** `hotfix/*`:

| Cenário | Lógica | Resultado | Exemplo |
|----|----|----|----|
| **Qualquer tipo** | Sempre incrementa patch | Adiciona sufixo `-hf` | `0.2.1` → `0.2.2-hf.0` |

### **🎯 Tags Especiais para Forçar Incremento**

Você pode forçar o tipo de incremento usando tags especiais no **título do PR**:

| Tag | Incremento | Exemplo PR Title | Resultado |
|----|----|----|----|
| `#major` | **Major** | `feat: nova API #major` | `0.1.0` → `1.0.0-rc.0` |
| `#minor` | **Minor** | `feat: nova funcionalidade #minor` | `0.1.0` → `0.2.0-rc.0` |
| `#patch` | **Patch** | `fix: correção #patch` | `0.1.0` → `0.1.1-rc.0` |

### **📋 Cenários Detalhados de Versionamento**

#### **Cenário 1: Nova Funcionalidade (staging)**

```
Atual: 0.2.1-rc.2

PR: feat: Adicionar sistema de notificações

Análise: feat = nova funcionalidade = minor bump

Resultado: 0.3.0-rc.0 (incrementa minor)
GitHub Release: Criada como pré-release

CI Pipeline: Disparado para staging
```

#### **Cenário 2: Correção de Bug (staging)**

```
Atual: 0.2.1-rc.2

PR: fix: Corrigir erro de login

Análise: fix = correção de bug = patch bump

Resultado: 0.2.2-rc.0 (incrementa patch)
GitHub Release: Criada como pré-release

CI Pipeline: Disparado para staging
```

#### **Cenário 3: Breaking Change (staging)**

```
Atual: 0.2.1-rc.2

PR: feat!: Refatorar API de usuários

Análise: feat! = breaking change = major bump

Resultado: 1.0.0-rc.0 (incrementa major)
GitHub Release: Criada como pré-release

CI Pipeline: Disparado para staging
```

#### **Cenário 4: Documentação (staging)**

```
Atual: 0.2.1-rc.2

PR: docs: Atualizar README

Análise: docs = documentação = RC apenas

Resultado: 0.2.1-rc.3 (apenas incrementa RC)
GitHub Release: Criada como pré-release

CI Pipeline: Disparado para staging
```

#### **Cenário 5: Staging → Main (Release Final)**

```
Atual: 0.2.1-rc.3

PR: release: User authentication v0.2.1

Análise: RC existente, converte para release

Resultado: 0.2.1 (remove sufixo -rc)
GitHub Release: Criada como release final

CI Pipeline: Disparado para production
```

#### **Cenário 6: Hotfix Urgente**

```
Atual: 0.2.1

PR: fix: Corrigir bug crítico em produção

Análise: hotfix = sempre patch + sufixo hf

Resultado: 0.2.2-hf.0 (hotfix)
GitHub Release: Criada como pré-release

CI Pipeline: Disparado para production
```

#### **Cenário 7: Desenvolvimento (develop)**

```
Atual: 0.2.1

PR: feat: Implementar nova funcionalidade

Análise: develop = apenas identificação

Resultado: dev-a1b2c3d (hash do commit)
GitHub Release: Não criada

CI Pipeline: Disparado para development
```

## 🚀 Próximos Passos


### **🔧 Melhorias Futuras**


1. **Cache inteligente**: Build cache entre branches
2. **Paralelização**: Builds simultâneos
3. **Quality gates**: Testes automáticos obrigatórios
4. **Blue-green deployments**: Zero downtime
5. **Canary releases**: Deploys progressivos
6. **Auto-rollback**: Rollback em caso de falha
7. **Cost optimization**: Análise de custos automática