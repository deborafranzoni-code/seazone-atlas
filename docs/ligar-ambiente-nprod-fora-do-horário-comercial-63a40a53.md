<!-- title: Ligar ambiente NPROD fora do horário comercial | url: https://outline.seazone.com.br/doc/ligar-ambiente-nprod-fora-do-horario-comercial-rNYTfdDvKy | area: Tecnologia -->

# Ligar ambiente NPROD fora do horário comercial

# Workflow N8N - Gerenciamento de Ambientes KEDA

## 📋 Visão Geral

Workflow N8N para gerenciar habilitação/desabilitação de ambientes de staging/development fora do horário comercial via KEDA ScaledObject, acionado através de formulário web.

## 🎯 Objetivo

Permitir que desenvolvedores solicitem a ativação/desativação de ambientes fora do horário comercial de forma autônoma, com rastreamento via issues do GitHub e notificações no Slack.

## 📝 Formulário de Solicitação

### Campos do Formulário

| Campo | Tipo | Obrigatório | Validações/Opções |
|----|----|----|----|
| **Aplicação** | Select | ✅ Sim | `wallet`, `sapron`, `reservas` |
| **Componente** | Checkbox (múltipla seleção) | ✅ Sim | `frontend`, `api` |
| **Ambiente** | Select | ✅ Sim | `development`, `staging` |
| **Ação** | Select | ✅ Sim | `enable`, `disable` |
| **Quantidade de Réplicas** | Number | ✅ Sim (apenas se `enable`) | Mínimo: 1, Máximo: 3 (validação no form) |
| **Motivo** | Textarea | ✅ Sim | Descrição do motivo da solicitação |
| **Nome do Solicitante** | Text | ✅ Sim | Nome completo |
| **Email do Solicitante** | Email | ✅ Sim | Email válido |
| **Time** | Text | ✅ Sim | Nome do time/squad |

### Validações do Formulário

* **Réplicas**: Deve ser entre 1 e 3 (validação no frontend)
* **Email**: Formato de email válido
* **Réplicas obrigatórias**: Apenas quando ação for `enable`

## 🔄 Fluxo do Workflow N8N

```mermaidjs

graph TD
    A[Webhook Trigger - Recebe dados do formulário] --> B[Consultar Baserow - Buscar configs da aplicação]
    B --> C{Config encontrada?}
    C -->|Não| D[Erro: Aplicação não configurada]
    C -->|Sim| E[Validar Horário Comercial]
    
    E --> F{Fora do horário comercial?}
    F -->|Não| G[Enviar mensagem Slack:<br/>Ambiente já está funcionando<br/>Fluxo só funciona fora do horário]
    F -->|Sim| H[Validar Status Atual do Ambiente]
    
    H --> I{Ambiente já está no estado desejado?}
    I -->|Sim| J[Enviar mensagem Slack:<br/>Ambiente já está no estado solicitado]
    I -->|Não| K[Criar Issue no Repositório da Aplicação]
    
    K --> L[Enviar mensagem inicial no Slack<br/>Marcar @governanca-tech e @squad-app<br/>Salvar timestamp da mensagem]
    
    L --> M{Quantos componentes selecionados?}
    M -->|1| N[Executar para componente único]
    M -->|2| O[Loop: Para cada componente]
    
    O --> P[Set Variables: namespace, app_name, cluster_name]
    P --> Q[Acionar GitHub Workflow<br/>manage-keda-environment]
    Q --> R[Webhook: Receber status do GitHub]
    
    N --> P
    
    R --> S{Status = success?}
    S -->|Sim| T[Responder na thread do Slack:<br/>✅ Sucesso + detalhes]
    S -->|Não| U[Responder na thread do Slack:<br/>❌ Falha + detalhes]
    
    T --> V[Atualizar Issue com status]
    U --> V
    V --> W[Atualizar Baserow com novo status]
    
    G --> X[Fim]
    J --> X
    V --> X
    D --> X
```

## 🗄️ Estrutura da Tabela Baserow

A tabela no Baserow deve conter as seguintes colunas:

| Coluna | Tipo | Descrição |
|----|----|----|
| `app_name` | Text | Nome da aplicação (wallet, sapron, reservas) |
| `component_type` | Text | Tipo do componente (frontend, api) |
| `namespace` | Text | Namespace do Kubernetes (ex: stg-apps, dev-apps) |
| `cluster_name` | Text | Nome do cluster EKS (ex: general-cluster) |
| `slack_channel` | Text | Canal do Slack para notificações |
| `slack_squad_mention` | Text | Menção do squad no Slack (ex: @squad-wallet) |
| `repository_url` | Text | URL do repositório da aplicação |
| `repository_owner` | Text | Owner do repositório (ex: seazone-tech) |
| `repository_name` | Text | Nome do repositório (ex: wallet-api) |
| `status` | Text | Status atual (enabled, disabled) |
| `last_updated` | DateTime | Última atualização |
| `last_updated_by` | Text | Último usuário que atualizou |

## 🔍 Validações do Workflow

### 1. Validação de Horário Comercial

* **Horário Comercial**: Segunda a Sexta, 08:00 - 18:00 (America/Sao_Paulo)
* **Se dentro do horário comercial**:
  * Enviar mensagem no Slack informando que o ambiente já está funcionando normalmente
  * Informar que o fluxo só funciona fora do horário comercial
  * **Não executar** o workflow do GitHub
  * **Não criar** issue

### 2. Validação de Status Atual

* **Se ação =** `**disable**` **e status atual =** `**disabled**`:
  * Enviar mensagem no Slack informando que o ambiente já está desativado
  * **Não executar** o workflow do GitHub
  * **Não criar** issue
* **Se ação =** `**enable**` **e status atual =** `**enabled**`:
  * Enviar mensagem no Slack informando que o ambiente já está ativado
  * **Não executar** o workflow do GitHub
  * **Não criar** issue

## 📦 Processamento de Múltiplos Componentes

Quando o usuário seleciona múltiplos componentes (ex: frontend + api):


1. **Loop para cada componente**:
   * Buscar configuração específica no Baserow (app + component_type)
   * Definir variáveis: `app_name`, `namespace`, `cluster_name`
   * Acionar workflow do GitHub para cada componente
   * Aguardar resposta de cada execução
2. **Consolidar resultados**:
   * Responder na thread do Slack com status de cada componente
   * Atualizar issue com resumo de todas as execuções

## 🔔 Notificações no Slack

### Mensagem Inicial

```
🚀 Solicitação de Gerenciamento de Ambiente

👤 Solicitante: {nome} ({email})
🏢 Time: {time}
📦 Aplicação: {aplicacao}
🔧 Componentes: {componentes}
🌍 Ambiente: {ambiente}
⚡ Ação: {acao}
📊 Réplicas: {replicas}
📝 Motivo: {motivo}

⏳ Processando...
```

**Canais**: Canal configurado no Baserow\n**Menções**: `@governanca-tech` + `@squad-app` (do Baserow)

### Resposta na Thread (Sucesso)

```
✅ Ambiente {acao} com sucesso!

📦 Componente: {app_name}
🌍 Namespace: {namespace}
📊 Réplicas: {replicas}
🔗 Issue: {issue_url}
```

### Resposta na Thread (Falha)

```
❌ Falha ao {acao} ambiente

📦 Componente: {app_name}
🌍 Namespace: {namespace}
⚠️ Erro: {mensagem_erro}
🔗 Issue: {issue_url}
```

## 📝 Criação de Issue no GitHub

### Template da Issue

**Título**: `[KEDA] {acao} ambiente {ambiente} - {aplicacao} {componente}`

**Corpo**:

```markdown
## Solicitação de Gerenciamento de Ambiente

- **Aplicação**: {aplicacao}
- **Componente**: {componente}
- **Ambiente**: {ambiente}
- **Ação**: {acao}
- **Réplicas**: {replicas}
- **Solicitante**: {nome} ({email})
- **Time**: {time}
- **Motivo**: {motivo}

## Status

- [ ] Workflow acionado
- [ ] Ambiente {acao}
- [ ] Notificação enviada

## Logs

{logs_do_workflow}
```

## 🔗 Integração com GitHub Workflow

### Payload Enviado ao Workflow

```json
{
  "app_name": "wallet-api",
  "namespace": "stg-apps",
  "action": "enable",
  "replicas": "2",
  "cluster_name": "general-cluster",
  "resumeUrl": "https://workflows.seazone.com.br/webhook/{workflow_id}"
}
```

### Webhook de Resposta

O workflow do GitHub chama o `resumeUrl` com:

```json
{
  "status": "success|failure",
  "message": "Mensagem descritiva",
  "app_name": "wallet-api",
  "namespace": "stg-apps",
  "action": "enable",
  "workflow_job_status": "success"
}
```

## 🔄 Atualização do Baserow

Após execução bem-sucedida:

* Atualizar campo `status` (enabled/disabled)
* Atualizar `last_updated` com timestamp atual
* Atualizar `last_updated_by` com email do solicitante

## ⚠️ Tratamento de Erros


1. **Aplicação não encontrada no Baserow**:
   * Enviar mensagem de erro no Slack
   * Não criar issue
   * Não executar workflow
2. **Falha na criação da issue**:
   * Continuar execução
   * Registrar erro nos logs
   * Notificar no Slack sobre falha na criação da issue
3. **Falha no workflow do GitHub**:
   * Responder na thread do Slack com erro
   * Atualizar issue com status de falha
   * Não atualizar Baserow

## 📊 Rastreabilidade

* **Issue no GitHub**: Histórico completo da solicitação
* **Mensagens no Slack**: Thread com todas as atualizações
* **Baserow**: Status atual e histórico de mudanças
* **Logs do N8N**: Execução completa do workflow

## 🔐 Segurança

* Validação de horário comercial para evitar execuções desnecessárias
* Validação de status atual para evitar operações redundantes
* Rastreamento completo via issues e logs
* Notificações para times responsáveis


Criado por @[John Paulo da Silva Paiva](mention://9a8cb110-78c4-4e45-8213-c870ac4de9ee/user/fe961e04-fb16-4dab-b8b9-0d6428861ad2)