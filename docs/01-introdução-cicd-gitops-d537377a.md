<!-- title: 01 - Introdução CI/CD & GitOps | url: https://outline.seazone.com.br/doc/01-introducao-cicd-gitops-a6PG7byuUE | area: Tecnologia -->

# 01 - Introdução CI/CD & GitOps

## 📋 Visão Geral

Esta documentação é o guia completo do pipeline CI/CD da Seazone, implementado com **GitOps** e **ArgoCD**. Se você é um desenvolvedor na Seazone, este é seu ponto de partida para entender como funciona todo o fluxo de desenvolvimento, desde o código até a produção.

## 🎯 Para quem é esta documentação?

* **Desenvolvedores** que chegaram na empresa
* **Novos membros** da equipe em onboarding
* **Qualquer pessoa** que trabalha com código na Seazone
* **Todos que querem** entender como funciona o pipeline

## 🤔 O que você vai aprender?


1. **Conceitos básicos** de CI/CD e GitOps
2. **Como fazer PRs** da forma correta
3. **Como acompanhar** seus deployments
4. **Como resolver** problemas comuns
5. **Workflows** e automações existentes
6. **Templates** prontos para usar

## 💡 Conceitos Fundamentais

### O que é CI/CD?

**CI/CD** significa **Continuous Integration** e **Continuous Deployment**:

* **CI (Integração Contínua)**: Seu código é automaticamente testado e "buildado" sempre que você faz um commit
* **CD (Deploy Contínuo)**: Seu código vai automaticamente para produção após passar por todos os testes

### O que é GitOps?

**GitOps** é uma metodologia onde:

* **Git é a fonte da verdade** para tudo
* **Mudanças na infra** são feitas via Pull Requests
* **ArgoCD monitora** os repositórios e aplica mudanças automaticamente
* **Rollbacks** são simples: basta reverter o commit

### Como funciona na Seazone?

```mermaidjs
graph LR
    A["👨‍💻 Você escreve código"] --> B["📦 CI constrói imagem"]
    B --> C["🔄 GitOps atualiza manifests"]
    C --> D["🤖 ArgoCD detecta mudança"]
    D --> E["☸️ Deploy no Kubernetes"]
    E --> F["🌐 App disponível"]
```

## 🏗️ Arquitetura Simplificada

### Repositórios na Seazone

Temos **3 tipos** de repositórios:


1. **App Repos** (`reservas-api`): Seu código da aplicação
2. **GitOps Repos** (`gitops-reservas`): Configurações de deployment
3. **Governança Repo** (`gitops-governanca`): Templates e workflows reutilizáveis

### Ambientes

* **Development** (`dev`): Para testar suas features (🔜 Em breve)
* **Staging** (`stg`): Para testar releases candidates
* **Production** (`prd`): O ambiente de produção dos usuários

### Branches e Ambientes

 ![Branching Model - Seazone](/api/attachments.redirect?id=3ab814a5-6ff2-4828-95b4-62696074d594 " =1920x1080")

| Branch | Ambiente | Release/RC | Build/CI | Deploy |
|----|----|----|----|----|
| `develop` | **dev** | 🚫 | ✅ Build imagem/CI `dev-{hash}` | 🚫 (🔜 Em breve) |
| `staging` | **stg** | Release Candidate `0.2.0-rc.1` | ✅ Build imagem/CI `0.2.0-rc.1` | ✅ Deploy automático |
| `main` | **prd** | Release Final `0.2.0` | ✅ Build imagem/CI `0.2.0` | ✅ Deploy automático |
| `hotfix/*` | **prd** | Hotfix `0.2.1-hf.0` | ✅ Build imagem/CI `0.2.1-hf.0` | ✅ Deploy automático |

## 🚦 Seu primeiro PR

### 1. Criar sua branch

```bash
# Sempre partindo do develop

git checkout develop

git pull origin develop

# Crie sua feature branch

git checkout -b feature/minha-nova-funcionalidade
```

### 2. Fazer suas mudanças

```bash
# Desenvolva normalmente

git add .
git commit -m "feat: adicionar nova funcionalidade"
git push origin feature/minha-nova-funcionalidade
```

### 3. Abrir Pull Request

* **Título**: Use [Conventional Commits](#conventional-commits)
* **Base**: `develop` (para features)
* **Workflow PR Title Validator** valida o título do PR

### 4. Aguardar aprovação e merge

* O PR será revisado
* Após aprovação, será feito merge para `develop`
* **Workflow Semantic Version** gera a tag `0.2.0-rc.1`
* **Workflow CI** gera a imagem `0.2.0-rc.1`
* **Workflow GitOps** atualiza o values.yaml no repositório **gitops** (ex: `gitops-reservas/helm/{COMPONENT}/values-stg.yaml`)
* **Workflow Slack** envia notificação no canal **#app-pipeline** (ex: `#reservas-pipeline`)

## 📝 Conventional Commits

**IMPORTANTE**: Os títulos dos PRs devem seguir este padrão:

```bash
<tipo>: descricao
```

Exemplo: 

 ![exemplo de titulo de PR](/api/attachments.redirect?id=0492d1e2-a5ce-456c-8197-8cb39d278020 "left-50")


\

\

| Tipo | Incremento | Exemplo |    |
|----|----|----|----|
| `feat:` | **minor** | `feat: adicionar sistema de login` |    |
| `fix:` | **patch** | `fix: corrigir erro de validação` |    |
| `feat!:` | **major** | `feat!: alterar estrutura da API` |    |
| `docs:` | **patch** | `docs: atualizar documentação` |    |
| `style:` | **patch** | `style: ajustar formatação` |    |
| `refactor:` | **patch** | `refactor: melhorar código` |    |
| `test:` | **patch** | `test: adicionar testes` |    |
| `chore:` | **patch** | `chore: atualizar dependências` |    |

Para mais detalhes sobre versionamento, consulte [🏷️ Versionamento Semântico](https://outline.seazone.com.br/doc/03-versionamento-semantico-Gn3hcwdk2m).

### Exemplos de bons títulos:

✅ **Correto**:

* `feat: implementar autenticação via OAuth`
* `fix: resolver erro de timeout na API`
* `docs: adicionar guia de instalação`

❌ **Incorreto**:

* `adicionar login` (sem tipo)
* `Fix bug` (não especifica o que)
* `WIP: trabalhando nisso` (muito genérico)

## 📊 Fluxo de Deployment

 ![](/api/attachments.redirect?id=1b71698c-82b9-4f3f-b2a8-498994a4916b)

### Development (develop → dev)


1. **Merge PR** para `develop`
2. **Build e Push** da imagem Docker para o registry (ECR) com a tag `dev-{hash}`
3. **Slack notifica** o time no canal **#app-pipeline** (ex: `#reservas-pipeline`)
4. \
   > Em breve: **Deploy automático** para o ambiente de **dev**

### Staging (develop → staging)


1. **PR de develop** para `staging`
2. **Título da PR analisado** para versionamento semântico ex: `fix: corrigir erro de validação`
3. **Release Candidate** gerada ex: `0.2.0-rc.1`
4. **Build e Push** da imagem Docker para o registry (ECR) ex: `0.2.0-rc.1`
5. **GitOps atualiza** `values-stg.yaml` no repositório **gitops** (ex: `gitops-reservas/helm/{COMPONENT}/values-stg.yaml`)
6. **ArgoCD sync automático** realiza o deploy da nova imagem no namespace `stg-apps`
7. **Slack notifica** status da pipeline no canal **#app-pipeline** (ex: `#reservas-pipeline`)
8. **Disponível** em `stg.app.seazone.com.br`

Para entender melhor este fluxo, consulte [📋 Fluxos de Desenvolvimento](https://outline.seazone.com.br/doc/02-fluxos-de-desenvolvimento-wPJkOaGgtp).

### Production (staging → main)


1. **PR de staging** para `main`
2. **Promove Release Candidate** removendo o sufixo `-rc` ex: `0.2.0-rc.1` ➡️ `0.2.0`
3. **Build e Push** da imagem Docker para o registry (ECR) ex: `0.2.0`
4. **GitOps atualiza** `values.yaml` no repositório **gitops** (ex: `gitops-reservas/helm/{COMPONENT}/values.yaml`)
5. **ArgoCD sync automário** realiza o deploy da nova imagem no namespace `prd-apps`
6. **Slack notifica** status da pipeline no canal **#app-pipeline** (ex: `#reservas-pipeline`)
7. **Disponível** em `app.seazone.com.br`

## 🔍 Como acompanhar

### Slack

* **#app-pipeline**: Canal específico da sua aplicação (ex: #reservas-pipeline)  - (**⚠️ ainda será implementado**)
  * Recebe notificações e mostra status de build e deploy

 ![](/api/attachments.redirect?id=14d9ff07-8a41-4952-a053-330f69c35477)

### GitHub Actions

* Vá no seu repositório (ex: `gitops-reservas`)
* Clique em **Actions**
* Procure pelo workflow que está rodando
  * **Semantic Version**: Gera releases semânticas e dispara o workflow `CI`
  * **CI**: Build e atualização do gitops da aplicação
  * **PR Title Validator**: Valida títulos de PR
* Acompanhe/consulte os logs da execução

 ![Actions  e Workflows](/api/attachments.redirect?id=e9d4d788-6c96-4c53-b2b7-8d17e4633843)

Para mais detalhes sobre workflows, consulte [⚙️ Workflows e Pipelines](https://outline.seazone.com.br/doc/04-workflows-e-pipelines-F62on5Cstu).

### ArgoCD

* Acesse o dashboard do ArgoCD (<https://argocd.seazone.com.br/>)
* Encontre sua aplicação (ex: `reservas-api-stg`)
* Ao clicar na aplicação você poderá acompanhar o **deploy**, **sincronização** e **logs** de execução.

 ![ArgoCD Overview](/api/attachments.redirect?id=f1a2234a-d1ee-43d8-83bf-e19325c48fdd)

## 🚨 Emergências e Hotfixes

### Quando usar hotfix?

* **Bug crítico** em produção
* **Problema de segurança**
* **Sistema fora do ar**

### Como fazer um hotfix?

```bash
# 1. Criar branch hotfix

git checkout -b hotfix/corrigir-bug-critico

# 2. Fazer a correção

git add .
git commit -m "fix: corrigir bug crítico de autenticação"

# 3. Push direto (SEM PR!)
git push origin hotfix/corrigir-bug-critico
```

⚡ **Deploy automático** direto para produção!

Para mais detalhes sobre hotfixes, consulte [🚨 Fluxo de Hotfix](https://outline.seazone.com.br/doc/02-fluxos-de-desenvolvimento-wPJkOaGgtp).

## 🔧 Comandos úteis no dia a dia

### Git

```bash
# Status das suas mudanças

git status

# Ver histórico de commits

git log --oneline -10

# Atualizar sua branch com develop

git checkout develop && git pull

git checkout sua-branch && git merge develop

# Reverter commit

git revert HEAD
```

Para mais comandos úteis, consulte [🔧 Comandos de Referência](https://outline.seazone.com.br/doc/06-glossario-e-referencias-s17R31h4ZZ).

## ❗ Problemas Comuns

### "Meu PR não está fazendo deploy"


1. ✅ Verificar se o título segue Conventional Commits
2. ✅ Verificar se fez merge (não apenas push)
3. ✅ Verificar Actions no GitHub
4. ✅ Perguntar marcando @squad-governanca no Slack

### "Deploy falhou"


1. ✅ Ver logs no GitHub Actions
2. ✅ Verificar ArgoCD dashboard
3. ✅ Verificar se não há conflitos no Git
4. ✅ Pedir ajuda marcando @squad-governanca no Slack

> ℹ️ Para mais soluções de problemas, consulte [🔧 Troubleshooting e FAQ](https://outline.seazone.com.br/doc/05-troubleshooting-e-faq-ChpeXso2Fg).

### Documentação adicional

* [📋 Fluxos Detalhados](./02-fluxos-desenvolvimento.md)
* [🔧 Troubleshooting](./06-troubleshooting-faq.md)
* [🏷️ Versionamento Semântico](./03-versionamento-semantico.md)
* [📱 Templates e Checklists](./05-templates-checklists.md)
* [⚙️ Workflows e Pipelines](./04-workflows-pipelines.md)
* [📚 Glossário e Referências](./07-glossario-referencias.md)