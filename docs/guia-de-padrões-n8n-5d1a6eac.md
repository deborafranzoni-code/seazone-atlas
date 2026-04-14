<!-- title: Guia de Padrões n8n | url: https://outline.seazone.com.br/doc/guia-de-padroes-n8n-ujOTJaCjYI | area: Tecnologia -->

# Guia de Padrões n8n

# 📘 Guia de Padrões n8n

```mermaidjs
graph TB
    A[Organização n8n] --> B[Conta BU]
    A --> C[Conta Automação/Suporte]
    A --> D[Conta ADM]
    
    B --> B1[Workflows específicos da BU]
    C --> C1[Automação]
    D --> D1[Configurações]
    
    style A fill:#e1f5ff
    style B fill:#fff4e1
    style C fill:#e8f5e9
    style D fill:#fce4ec
```


---

## 📁 Estrutura de Pastas

A numeração garante ordenação visual consistente, independente da ordem alfabética.

### Hierarquia Raiz

```
/ (Raiz)
├── 00_Global_Utils      # Funções usadas por vários projetos (Formatadores, Error Handlers globais)
├── 10_Projects          # Pasta mãe de todos os projetos ativos
├── 90_Playground        # (Opcional) Área de testes/rascunhos — limpeza mensal
└── 99_Archived          # Projetos descontinuados — nunca apague, apenas arquive
```

### Regra de Arquivamento

Mova para `99_Archived` quando o projeto se enquadrar em **qualquer** um dos critérios abaixo:

* Foi **abandonado** — sem previsão de continuidade
* Foi **substituído** por outro workflow ou projeto

### Anatomia de um Projeto

Dentro de `10_Projects`, cada projeto tem sua própria pasta raiz.

```
/10_Projects
   └── [PROJ-CRM] Integração HubSpot       # Pasta do projeto
       ├── [MAIN] Sync Novos Leads          # Workflow principal (orquestrador)
       ├── Sub-workflows                    # Pasta interna
       │   ├── [SUB] Tratar Dados
       │   └── [SUB] Enriquecer Email
       └── Project_Utils                    # Pasta interna (opcional)
           └── [UTIL] Format Date CRM
```

> **Dica:** Projetos simples (menos de 3 workflows) não precisam de subpastas. Mantenha os workflows soltos na pasta do projeto com a nomenclatura correta. Over-engineering de pastas atrapalha a navegação rápida.

### O papel do `00_Global_Utils`

Workflows que podem ser reutilizados a departamento ou projeto:

* **Error Handler Global** — recebe erros de todos os workflows e notifica Slack/Teams
* **Auth Refresher** — renova tokens de APIs e salva no KV store
* **Formatadores complexos** — scripts JS/Python reutilizáveis, grandes demais para um nó de Code


---

## 🔄 Nomenclatura de Workflows

**Formato**:`[TIPO] - Nome Descritivo`

### Prefixos de Tipo

| Prefixo | Significado | Quando usar |
|----|----|----|
| `[MAIN]` | Workflow principal | Orquestra o processo completo |
| `[SUB]` | Sub-workflow | Chamado por outro workflow |
| `[UTIL]` | Utilitário | Função reutilizável |
| `[POC]` | Proof of Concept | Em teste, não usar em prod |
| `[MIG]` | Migração | Processo temporário de migração |

### Exemplos Práticos

```
✅ [Spots][MAIN] - Lead Capture to CRM
✅ [Hospedagem][SUB] - Validate Check-in Data
✅ [Global][UTIL] - Format Brazilian Phone
✅ [Dados][POC] - Test Baserow Sync
✅ [RevOps][MIG] - Old Pipedrive to New Schema
```


---

## 🧩 Nomenclatura de Nodes

**Formato**: `[Tipo] Ação Específica`

Precisa ser claro o que está acontecendo naquele momento.

```mermaidjs
graph LR
    A[📥 HTTP Fetch Customer Data] --> B[⚙️ Transform Calculate Revenue]
    B --> C[🔍 Filter Active Subscriptions Only]
    C --> D[📧 Gmail Send Welcome Email]
    
    style A fill:#e3f2fd
    style B fill:#fff9c4
    style C fill:#f3e5f5
    style D fill:#e8f5e9
```

### Exemplos por Categoria

| Categoria | Exemplo |
|----|----|
| **HTTP Requests** | `[HTTP] Fetch Customer Data` |
| **Transformações** | `[Transform] Calculate Revenue` |
| **Filtros** | `[Filter] Active Subscriptions Only` |
| **Integrações** | `[Gmail] Send Welcome Email` |
| **Condicionais** | `[IF] Check Subscription Status` |
| **Loops** | `[Loop] Process Each Order` |


---

## 📝 Documentação In-Code (Note Node)

Todo workflow `[MAIN]` **deve** ter um Note Node logo no início do canvas com as seguintes informações:

| Campo | Descrição |
|----|----|
| **Objetivo** | O que esse workflow faz? |
| **Owner** | Quem criou/mantém? |
| **Dependências** | Quais credenciais ou sub-workflows ele chama? |

### Exemplo

```
• Projeto: Sincronização de Vendas
• Trigger: Webhook do Stripe
• Saída: Cria linha no Google Sheets e notifica Slack
• Owner: team-revops
• Dependências: [SUB] Tratar Dados, [UTIL] Format Brazilian Phone
```

> **Obrigatório:** Workflows `[MAIN]` sem Note Node não devem ir para produção.

**Formato**: `[PRODUTO] - [USO] - [OWNER]`

### Exemplos

```
Pipedrive - Automação - RevOps
Baserow - Marketing - Governance
Morada - HeaderAuth - Integrations
Slack - Notifications - TeamOps
```


---

## 🏷️ Sistema de Labels

### Tabela de Labels

| Label | Formato | Exemplos | Uso Principal |
|----|----|----|----|
| **bu** | `bu:<nome>` | `bu:spots` `bu:hospedagem` `bu:dados` | Identificar proprietário |
| **type** | `type:<tipo>` | `type:integration` `type:automation` `type:data-sync` | Classificação funcional |
| **status** | `status:<estado>` | `status:active` `status:testing` `status:deprecated` | Lifecycle do workflow |
| **product** | `product:<nome>` | `product:sapron` `product:bi` | Rastreio de impacto |
| **owner** | `owner:<pessoa>` | `owner:arilo` `owner:team-data` | Responsável técnico |
| **tool** | `tool:<ferramenta>` | `tool:pipedrive` `tool:slack` | Dependências externas |

### Exemplo de Combinação

```none
Workflow: [Spots][MAIN] - Lead Capture to CRM

Labels aplicadas:
• bu:spots
• type:integration
• status:active
• product:crm
• owner:team-sales
• tool:pipedrive
• tool:webhook
```


---

## 🔢 Versionamento

**Formato**: `v<MAJOR>.<MINOR>`

```mermaidjs
graph LR
    A[v1.0] -->|Mudança pequena| B[v1.1]
    B -->|Mudança pequena| C[v1.2]
    C -->|Mudança grande| D[v2.0]
    
    style A fill:#e8f5e9
    style B fill:#e8f5e9
    style C fill:#e8f5e9
    style D fill:#fff9c4
```

### Quando incrementar

* **MAJOR** (v1.x → v2.x): Mudanças estruturais, breaking changes
* **MINOR** (vx.1 → vx.2): Melhorias, novos recursos, ajustes

### Exemplos

```
v1.0 → Versão inicial em produção
v1.1 → Adicionado filtro de status
v1.2 → Otimizado tratamento de erros
v2.0 → Reestruturação completa do fluxo
```


---