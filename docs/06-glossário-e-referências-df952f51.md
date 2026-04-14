<!-- title: 06 - Glossário e Referências | url: https://outline.seazone.com.br/doc/06-glossario-e-referencias-emn6sGKDZQ | area: Tecnologia -->

# 06 - Glossário e Referências

![Glossario Overview](image-07-01.png)

## 📋 Visão Geral

Esta seção é seu dicionário de termos técnicos e referências da arquitetura CI/CD da Seazone. Use quando precisar entender um conceito específico ou buscar documentação oficial.

 ![Glossario Tecnico](image-07-02.png)

## 📖 Glossário Técnico

### A

**ArgoCD**

> Ferramenta de Continuous Deployment que monitora repositórios Git e sincroniza automaticamente mudanças com clusters Kubernetes seguindo a metodologia GitOps.

**Action (GitHub)**

> Componente reutilizável que executa uma tarefa específica em um workflow do GitHub Actions. Pode ser oficial (do GitHub) ou custom (da comunidade/empresa).

**ApplicationSet (ArgoCD)**

> Resource do ArgoCD que permite criar múltiplas Applications baseadas em templates e generators, útil para deploy em múltiplos ambientes.

### B

**Branch Protection**

> Regras configuradas no GitHub que protegem branches importantes (main, staging, develop) exigindo aprovações, status checks e outras validações antes do merge.

**Breaking Change**

> Mudança no código que quebra compatibilidade com versões anteriores, resultando em incremento major no versionamento semântico (ex: 0.2.1 → 1.0.0).

### C

**Conventional Commits**

> Especificação para padronizar mensagens de commit seguindo o formato `type: description`, facilitando automações e geração de changelogs. Exemplo: `feat: add user authentication`

**CI/CD (Continuous Integration/Continuous Deployment)**

> Práticas de desenvolvimento onde código é automaticamente testado, construído e deployado através de pipelines automatizados.

**Composite Action**

> Tipo de GitHub Action que combina múltiplos steps em um único action reutilizável, definido via `action.yaml` com `using: composite`.

### D

**Dev Version**

> Versão de desenvolvimento gerada automaticamente quando há merge para branch develop, no formato `dev-{commit-hash}`. Não segue semantic versioning.

**Dockerfile**

> Arquivo texto com instruções para construir uma imagem Docker, definindo base image, dependências, comandos e configurações.

### E

**ECR (Elastic Container Registry)**

> Serviço AWS para armazenar e gerenciar imagens Docker de forma privada, integrado com IAM para controle de acesso.

**Environment**

> Ambiente de execução da aplicação. Na Seazone: **dev** (desenvolvimento), **stg** (staging/homologação), **prd** (produção).

### F

**Feature Branch**

> Branch temporária criada para desenvolver uma funcionalidade específica, seguindo padrão `feature/nome-da-funcionalidade`.

**Feature Flag**

> Técnica para controlar features em produção via configuração, permitindo ativar/desativar funcionalidades sem deploy.

### G

**GitOps**

> Metodologia onde Git é a fonte da verdade para configurações de infraestrutura e deployments, com ferramentas como ArgoCD aplicando mudanças automaticamente.

**GitHub Actions**

> Plataforma de CI/CD do GitHub que executa workflows automaticamente baseados em eventos do repositório (push, PR, etc.).

### H

**Helm**

> Gerenciador de pacotes para Kubernetes que usa templates (charts) para definir, instalar e gerenciar aplicações no cluster.

**Hotfix**

> Correção urgente aplicada diretamente em produção para resolver bugs críticos, no formato `hotfix/nome-do-fix` com tag `X.Y.Z-hf.N`.

### I

**Image Tag**

> Identificador único de uma imagem Docker, usado para versionamento. Ex: `app:0.2.0-rc.1`, `app:latest`, `app:dev`. Tag path: `/apps/app/0.2.0-rc.1`.

**Ingress**

> Resource Kubernetes que gerencia acesso externo aos services no cluster, tipicamente HTTP/HTTPS, incluindo SSL termination e routing.

### J

**JWT (JSON Web Token)**

> Padrão para representar claims de forma segura entre partes, comumente usado para autenticação e autorização em APIs.

### K

**kubectl**

> Interface de linha de comando para interagir com clusters Kubernetes, usado para gerenciar recursos e debugar aplicações.

**Kubernetes (K8s)**

> Plataforma de orquestração de containers que automatiza deploy, scaling e gerenciamento de aplicações containerizadas.

### L

**Liveness Probe**

> Health check do Kubernetes que verifica se um container está rodando. Se falhar, o container é restartado.

**Load Balancer**

> Componente que distribui tráfego de rede entre múltiplas instâncias de uma aplicação, melhorando disponibilidade e performance.

### M

**Merge Strategy**

> Estratégia usada para integrar branches. Seazone usa **Squash and Merge** que combina todos commits de uma branch em um único commit.

**Microservice**

> Arquitetura onde aplicação é dividida em serviços pequenos, independentes e deployáveis separadamente.

### N

**Namespace**

> Mecanismo de isolamento no Kubernetes que permite separar recursos por ambiente, projeto ou equipe.

### O

**OIDC (OpenID Connect)**

> Protocolo de autenticação baseado em OAuth2, usado para autenticação segura entre GitHub Actions e AWS sem armazenar credentials.

### P

**Pod**

> Menor unidade deployável no Kubernetes, contendo um ou mais containers que compartilham rede e storage.

**Pull Request (PR)**

> Funcionalidade do Git para propor mudanças, permitindo code review e validações antes do merge.

### Q

**Quality Gates**

> Critérios automatizados que código deve passar (testes, security scans, lint) antes de avançar no pipeline.

### R

**RC (Release Candidate)**

> Versão candidata a se tornar release final, no formato `X.Y.Z-rc.N`. Passa por testes em staging antes de virar release.

**Readiness Probe**

> Health check que verifica se container está pronto para receber tráfego. Controla se Pod recebe requests.

**Repository Dispatch**

> Event customizado do GitHub Actions que permite disparar workflows programaticamente, usado para integração entre workflows.

**Rollback**

> Processo de reverter deploy para versão anterior, restaurando estado funcional da aplicação.

### S

**Semantic Versioning (SemVer)**

> Sistema de versionamento que usa formato `MAJOR.MINOR.PATCH` com regras específicas para incremento baseado no tipo de mudança.

**Service Account**

> Identidade não-humana no Kubernetes usada por Pods para acessar recursos do cluster e APIs externas.

**SSM Parameter Store**

> Serviço AWS para armazenar dados de configuração e secrets de forma hierárquica e segura.

**Status Check**

> Validação automática (testes, lint, security) que deve passar antes de permitir merge de PR.

### T

**Tag (Git)**

> Referência imutável para commit específico, usada para marcar releases e versões importantes do código.

**Trivy**

> Scanner de segurança que identifica vulnerabilidades em imagens Docker, filesystems e repositórios Git.

### U

**Upstream**

> Repositório ou branch principal de onde você deriva seu trabalho, tipicamente `origin/main` ou `origin/develop`.

### V

**Values.yaml**

> Arquivo de configuração do Helm que define valores para templates, customizando deployment por ambiente.

**Version Bump**

> Incremento automático de versão baseado no tipo de mudança (major, minor, patch) seguindo semantic versioning.

### W

**Workflow**

> Processo automatizado definido em `.github/workflows/` que executa jobs e steps baseados em triggers específicos.

**Webhook**

> Mecanismo de callback HTTP que permite integração entre sistemas, enviando dados quando eventos específicos ocorrem.

### Y

**YAML (YAML Ain't Markup Language)**

> Formato de serialização de dados humano-legível usado para configurações (Kubernetes, GitHub Actions, Helm).

**yq**

> Ferramenta CLI para processar arquivos YAML/JSON, permitindo queries, edições e validações programáticas.

## 🏗️ Arquitetura da Seazone

### Repositórios

#### App Repositories

```
Padrão: {project_name}-{component}
Exemplos:
- reservas-api
- reservas-frontend  
- wallet-api
- sapron-backend
```

#### GitOps Repositories

```
Padrão: gitops-{project_name}
Exemplos:
- gitops-reservas
- gitops-wallet
- gitops-sapron
```

#### Governança Repository

```
Nome: gitops-governanca

Função: Workflows templates, actions reutilizáveis
```

### Ambientes e Domains (Padrão)

| Ambiente | Namespace | Domain Pattern | Exemplo Frontend | Exemplo API |
|----|----|----|----|----|
| **Development** | `dev` | `dev-{app}.seazone.com.br` | `dev-wallet.seazone.com.br` | `dev-wallet-api.seazone.com.br` |
| **Staging** | `stg` | `stg-{app}.seazone.com.br` | `stg-wallet.seazone.com.br` | `stg-wallet-api.seazone.com.br` |
| **Production** | `prd` | `{app}.seazone.com.br` | `wallet.seazone.com.br` | `wallet-api.seazone.com.br` |

#### Para o projeto de reservas, o domain pattern é:

| Ambiente | Namespace | Domain Pattern | Exemplo Frontend | Exemplo API |
|----|----|----|----|----|
| **Development** | `dev` | `dev-{app}.seazone.com.br` | `dev.seazone.com.br` | `dev-api.seazone.com.br` |
| **Staging** | `stg` | `stg-{app}.seazone.com.br` | `stg.seazone.com.br` | `stg-api.seazone.com.br` |
| **Production** | `prd` | `{app}.seazone.com.br` | `seazone.com.br` | `api.seazone.com.br` |

### Versionamento Patterns

| Branch | Pattern | Exemplo | Tipo |
|----|----|----|----|
| `develop` | `dev-{hash}` | `dev-a1b2c3d` | Dev Version |
| `staging` | `X.Y.Z-rc.N` | `0.2.0-rc.1` | Release Candidate |
| `main` | `X.Y.Z` | `0.2.0` | Release Final |
| `hotfix/*` | `X.Y.Z-hf.N` | `0.2.1-hf.0` | Hotfix |

 ![Convenções](image-07-03.png)

## 📋 Convenções e Padrões

### Naming Conventions

#### Git Branches

```bash
# Feature branches

feature/user-authentication

feature/payment-integration

feature/admin-dashboard

# Bug fixes

fix/login-timeout-error

fix/memory-leak-issue

# Hotfixes

hotfix/critical-security-patch

hotfix/payment-processing-bug
```

#### Docker Images

```bash
# ECR naming pattern
{account-id}.dkr.ecr.{region}.amazonaws.com/{app-name}:{tag}

# Examples

711387131913.dkr.ecr.sa-east-1.amazonaws.com/reservas-api:latest     # latest version

711387131913.dkr.ecr.sa-east-1.amazonaws.com/reservas-api:0.2.0      # tag path: /apps/reservas-api/0.2.0

711387131913.dkr.ecr.sa-east-1.amazonaws.com/reservas-api:0.2.0-rc.1 # tag path: /apps/reservas-api/0.2.0-rc.1

711387131913.dkr.ecr.sa-east-1.amazonaws.com/reservas-api:dev        # tag path: /apps/reservas-api/dev-a1b2c3d

711387131913.dkr.ecr.sa-east-1.amazonaws.com/reservas-api:0.2.0-hf.1 # tag path: /apps/reservas-api/0.2.0-hf.1
```

#### Slack Channels

```bash
# Deploy notifications e alerts
#app-pipeline

# Team specific
#team-frontend
#team-backend
#team-infra
```

### Commit Message Patterns

#### Conventional Commits Format

```bash

type(scope): description

body (optional)

footer (optional)
```

#### Types Hierarchy

```bash
# Breaking changes (major)
feat!: alterar estrutura da API

fix!: remover endpoint deprecated

# New features (minor)  
feat: implementar autenticação OAuth

feat: adicionar filtros de pesquisa

# Bug fixes (patch)
fix: corrigir timeout na conexão

fix: resolver memory leak

# Maintenance (patch)
docs: atualizar README

style: corrigir formatação

refactor: melhorar performance

test: adicionar testes unitários

chore: atualizar dependências

ci: otimizar pipeline

build: atualizar Dockerfile
```

 ![Documentação Externa](image-07-04.png)

## 🔗 Documentação Externa

### Oficial

#### CI/CD & GitOps

* [GitHub Actions Documentation](https://docs.github.com/en/actions)
* [ArgoCD Documentation](https://argoproj.github.io/argo-cd/)
* [Helm Documentation](https://helm.sh/docs/)

#### Kubernetes

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [kubectl Reference](https://kubernetes.io/docs/reference/kubectl/)
* [Kubernetes API Reference](https://kubernetes.io/docs/reference/kubernetes-api/)

#### AWS Services

* [EKS User Guide](https://docs.aws.amazon.com/eks/latest/userguide/)
* [ECR User Guide](https://docs.aws.amazon.com/AmazonECR/latest/userguide/)
* [IAM User Guide](https://docs.aws.amazon.com/IAM/latest/UserGuide/)
* [SSM User Guide](https://docs.aws.amazon.com/systems-manager/latest/userguide/)

#### Standards

* [Semantic Versioning 2.0.0](https://semver.org/)
* [Conventional Commits](https://www.conventionalcommits.org/)
* [GitOps Principles](https://www.gitops.tech/)

### Community Resources

#### Best Practices

* [12-Factor App](https://12factor.net/)
* [Container Best Practices](https://cloud.google.com/architecture/best-practices-for-building-containers)
* [Kubernetes Best Practices](https://kubernetes.io/docs/concepts/configuration/overview/)

#### Learning Resources

* [GitHub Actions Learning Path](https://github.com/actions/starter-workflows)
* [ArgoCD Getting Started](https://argoproj.github.io/argo-cd/getting_started/)
* [Kubernetes Tutorials](https://kubernetes.io/docs/tutorials/)

 ![Quick Reference](image-07-05.png)

## 🔍 Quick Reference

### Essential Commands

#### Git

```bash
# Branch management

git checkout -b feature/nova-funcionalidade

git branch -d feature/funcionalidade-merged

git push origin --delete feature/funcionalidade-merged

# Version checking

git tag --sort=version:refname

git log --oneline -10

git show HEAD

# Reset and revert

git reset --hard HEAD~1  # ⚠️ Destructive

git revert HEAD          # ✅ Safe
```

#### Kubernetes

```bash
# Pod management

kubectl get pods -n stg

kubectl describe pod <pod-name> -n stg

kubectl logs -f deployment/app-name -n stg

# Service debugging

kubectl get svc -n stg

kubectl port-forward svc/app-name 8080:80 -n stg

# ConfigMaps and Secrets

kubectl get configmaps -n stg

kubectl get secrets -n stg

kubectl describe secret app-name-secret -n stg
```

#### Docker

```bash
# Image management

docker images | grep app-name

docker pull 711387131913.dkr.ecr.sa-east-1.amazonaws.com/app-name:0.2.0-rc.1  # tag path: /apps/app-name/0.2.0-rc.1

docker run -p 3000:3000 app-name:latest

# Cleanup

docker system prune -a

docker image prune -a
```

#### AWS CLI

```bash
# ECR

aws ecr get-login-password --region sa-east-1

aws ecr describe-repositories

aws ecr describe-images --repository-name app-name

# SSM

aws ssm get-parameter --name "/seazone/app-name/stg/database-url"
aws ssm get-parameters-by-path --path "/seazone/app-name/"

# Identity

aws sts get-caller-identity
```

#### GitHub CLI

```bash
# Workflow management

gh run list --limit=10

gh run view <run-id>
gh workflow run ci.yaml -f environment=stg -f tag=0.2.0

# Repository management

gh repo view --web

gh pr list --state=open

gh pr create --title "feat: nova funcionalidade" --body "Descrição..."
```

### Status Codes Reference

#### HTTP Status Codes

* **2xx Success**: 200 OK, 201 Created, 204 No Content
* **4xx Client Error**: 400 Bad Request, 401 Unauthorized, 404 Not Found
* **5xx Server Error**: 500 Internal Server Error, 502 Bad Gateway, 503 Service Unavailable

#### Kubernetes Pod Phases

* **Pending**: Pod aceito mas containers não foram criados
* **Running**: Pod bound a node e pelo menos um container está rodando
* **Succeeded**: Todos containers terminaram com sucesso
* **Failed**: Todos containers terminaram, pelo menos um falhou
* **Unknown**: Estado do Pod não pode ser obtido

#### Git Exit Codes

* **0**: Success
* **1**: General error
* **128**: Invalid command line option
* **129**: Repository not found


---

**Anterior**: [🔧 Troubleshooting e FAQ](./05-troubleshooting-faq.md)