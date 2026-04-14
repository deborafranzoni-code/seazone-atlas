<!-- title: 02 - Fluxos de Desenvolvimento | url: https://outline.seazone.com.br/doc/02-fluxos-de-desenvolvimento-kXTaneNn7X | area: Tecnologia -->

# 02 - Fluxos de Desenvolvimento

## 🎯 Visão Geral

Este documento detalha todos os fluxos de desenvolvimento na Seazone, desde a criação de features até o deploy em produção. Cada fluxo é otimizado para diferentes cenários e ambientes.

## 🌿 Estratégia de Branches

### Branch Model

```
main (produção)
├── staging (release candidates)
│   ├── develop (desenvolvimento)
│   │   ├── feature/nova-funcionalidade
│   │   ├── feature/outra-feature
│   │   └── bugfix/corrigir-bug
│   └── hotfix/emergencia
└── hotfix/bug-critico
```

### Regras de Proteção

 ![Regras de proteção / Overview](/api/attachments.redirect?id=d911effc-342f-4a74-912d-13fd94f4f31f)

| Branch | Proteção | PR Obrigatório | Deploy Automático |
|----|----|----|----|
| **develop** | ✅ | ✅ | 🔜 Em breve |
| **staging** | ✅ | ✅ | ✅ staging |
| **main** | ✅ | ✅ | ✅ production |
| **hotfix/**\* | ✅ | ❌ (push direto) | ✅ production |

## Fluxo 1: Desenvolvimento Normal (Feature)

### Cenário

Você precisa desenvolver uma nova funcionalidade ou corrigir um bug não crítico.

### Passo a Passo

#### 1. Preparação

```bash
# Atualizar develop

git checkout develop

git pull origin develop

# Criar feature branch

git checkout -b feature/sistema-notificacoes
```

#### 2. Desenvolvimento

```bash
# Desenvolver normalmente

git add .
git commit -m "feat: implementar sistema de notificações push"
git push origin feature/sistema-notificacoes
```

#### 3. Pull Request para develop

* **Base**: `develop`
* **Título**: `feat: implementar sistema de notificações push`
* **Reviewers**: 1 pessoa da equipe

#### 4. Build Automático (dev)

Após merge:

```
✅ Merge aprovado
📦 CI faz o build e push para o registry (ECR) com a tag: dev-{hash}
📱 Slack envia notificação no canal #app-pipeline
```

## Fluxo 2: Release Candidate (Staging)

### Cenário

Sua feature foi testada em dev e está pronta para ir para staging (pre-production).

### Passo a Passo

#### 1. Pull Request para staging

```bash
# Garantir que develop está atualizado

git checkout develop

git pull origin develop
```

Criar PR:

* **Base**: `staging`
* **Head**: `develop`
* **Título**: `feat: implementar sistema de notificações push`
* **Reviewers**: 1 pessoa

#### 2. Análise de Versionamento

O workflow analisa automaticamente o título do PR:

```
Título: feat: implementar sistema de notificações push

Tipo: feat (nova funcionalidade)
Incremento: minor (0.1.0 → 0.2.0)
Tag gerada: 0.2.0-rc.0
```

#### 3. Deploy Automático (staging)

Após merge:

```
✅ Merge aprovado  
🏷️ Semantic Version cria a release candidate: 0.2.0-rc.0 e dispara o workflow `CI`
🏗️ CI faz o build e push para o registry (ECR) com a tag gerada pelo Semantic Version
🔄 CI atualiza o repositório gitops da aplicação com a nova versão (values-stg.yaml)
📱 Slack envia notificação no canal #app-pipeline (com detalhes da RC)
🤖 ArgoCD sincroniza a aplicação com a nova versão (namespace: stg-apps)
🌐 Disponível em: stg.app.seazone.com.br
```

### Múltiplas RCs

Se você precisa fazer correções após a primeira RC:

```bash
# Nova correção em develop

git checkout develop

git commit -m "fix: corrigir erro de validação"

# PR develop → staging
# Título: fix: corrigir erro de validação
# Resultado: 0.2.0-rc.1 (incrementa RC number)
```

## ✅ Fluxo 3: Release Final (Production)

### Cenário

Sua RC foi completamente testada em staging e está pronta para produção.

### Passo a Passo

#### 1. Pull Request para main

* **Base**: `main`
* **Head**: `staging`
* **Título**: `release: sistema de notificações v0.2.0`
* **Reviewers**: 1 pessoa

#### 2. Promoção Automática

O sistema promove a RC existente:

```
RC encontrada: 0.2.0-rc.1

Release final: 0.2.0 (remove sufixo -rc)
Análise de título: IGNORADA (sempre promove RC)
```

#### 3. Deploy Automático (prd)

```
✅ Merge aprovado
🎯 Promoção: 0.2.0-rc.1 → 0.2.0  
🏷️ Tag criada: 0.2.0 (release final)
🔐 Build e push para o registry (ECR) com a tag: 0.2.0
🔄 CI atualiza o repositório gitops da aplicação com a nova versão (values.yaml)
🤖 ArgoCD sincroniza a aplicação com a nova versão (namespace: prd-apps)
📱 Slack envia notificação no canal #app-pipeline (PRODUCTION RELEASE)
🌐 Disponível em: app.seazone.com.br
```

## Fluxo 4: Hotfix (Emergência)

### Cenário

Bug crítico em produção que precisa ser corrigido **IMEDIATAMENTE**.

### Passo a Passo

#### 1. Criar Hotfix Branch

```bash
# Criar direto do main (importante!)
git checkout main

git pull origin main

git checkout -b hotfix/corrigir-login-critico
```

#### 2. Fazer Correção

```bash
# Fazer apenas a correção necessária

git add .
git commit -m "fix: corrigir erro crítico de autenticação"

# Push direto (sem PR!)
git push origin hotfix/corrigir-login-critico
```

#### 3. Deploy Automático DIRETO para Produção

```
🚨 Push detectado em hotfix/*
⚡ Análise: fix = patch increment
🏷️ Tag criada: 0.2.1-hf.0 (hotfix suffix)
🔐 Build e push para o registry (ECR) com a tag: 0.2.1-hf.0
🔄 CI atualiza o repositório gitops da aplicação com a versão do hotfix (values.yaml)
🤖 ArgoCD sincroniza a aplicação com a versão do hotfix (namespace: prd-apps)
📱 Slack envia notificação no canal #app-pipeline (🚨 HOTFIX environment)
🌐 Disponível em: app.seazone.com.br
```

#### 4. Pós-Hotfix

```bash
# Limpar branch após confirmação

git checkout main

git branch -d hotfix/corrigir-login-critico

git push origin --delete hotfix/corrigir-login-critico

# Sincronizar hotfix com outras branches (se necessário)
git checkout develop

git merge main

git push origin develop
```

### ⚠️ Cuidados com Hotfix

* ⛔ **Apenas para bugs críticos**
* 📢 **Comunicar no Slack** antes de fazer
* 🔍 **Monitorar intensivamente** após deploy
* 📋 **Documentar** o que foi corrigido
* 🧹 **Limpar branches** após confirmação

## 🔄 Cenários Especiais

### Multiple RCs (Várias Release Candidates)

#### Cenário: Múltiplas correções em staging

```bash

Estado: 0.1.1 (última release)

# 1ª mudança

develop → staging: "fix: corrigir bug"
Resultado: 0.1.2-rc.0

# 2ª mudança

develop → staging: "docs: atualizar documentação"
Resultado: 0.1.2-rc.1 (incrementa RC)

# 3ª mudança  
develop → staging: "feat: nova funcionalidade"
Resultado: 0.2.0-rc.0 (não incrementa RC, mas incrementa minor e zera a RC)

# 4ª mudança

develop → staging: "feat: outra funcionalidade"  
Resultado: 0.2.0-rc.2 (incrementa RC)

# Release final

staging → main: "release: v0.2.0"
Resultado: 0.2.0
```

### Breaking Changes

#### Cenário: Mudança que quebra compatibilidade

```bash
# PR Title: feat!: alterar estrutura da API de usuários


develop → staging

Análise: feat! = breaking change

Incremento: major (0.2.0 → 1.0.0)
Tag gerada: 1.0.0-rc.0
```

## 📊 Comparação de Fluxos

| Aspecto | Feature → Dev | Dev → Staging | Staging → Prod | Hotfix |
|----|----|----|----|----|
| **Aprovações** | 1 | 1 | 1 | 0 |
| **Versionamento** | `dev-{hash}` | `X.Y.Z-rc.N` | `X.Y.Z` | `X.Y.Z-hf.N` |

## 🎯 Boas Práticas por Fluxo

### Para Features

* ✅ Fazer commits pequenos e frequentes
* ✅ Testar localmente antes do PR
* ✅ Escrever testes para nova funcionalidade
* ✅ Atualizar documentação se necessário
* ✅ Usar títulos descritivos nos commits

### Para Staging

* ✅ QA completo da funcionalidade
* ✅ Testes de performance se aplicável
* ✅ Validação com equipe de produto
* ✅ Verificar integração com outras features
* ✅ Confirmar que não quebra funcionalidades existentes

### Para Production

* ✅ Deploy em horário de menor movimento
* ✅ Ter plano de rollback pronto
* ✅ Monitorar métricas pós-deploy
* ✅ Comunicar release para stakeholders

### Para Hotfix

* ⚡ Comunicar ANTES de fazer o hotfix
* ⚡ Fazer apenas a correção mínima necessária
* ⚡ Monitorar intensivamente após deploy
* ⚡ Documentar causa raiz do problema
* ⚡ Acompanhar métricas críticas

## 📈 Métricas e Monitoramento

### KPIs por Ambiente

#### Development

* **Deploy Frequency**: Múltiplos por dia
* **Lead Time**: < 1 hora (commit → deploy)
* **Failure Rate**: < 10%
* **Recovery Time**: < 30min

#### Staging

* **Deploy Frequency**: Diário
* **Lead Time**: < 4 horas
* **Failure Rate**: < 5%
* **Recovery Time**: < 15min

#### Production

* **Deploy Frequency**: Semanal
* **Lead Time**: < 1 dia
* **Failure Rate**: < 2%
* **Recovery Time**: < 5min