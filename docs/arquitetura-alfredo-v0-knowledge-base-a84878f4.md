<!-- title: Arquitetura — Alfredo v0 + Knowledge Base | url: https://outline.seazone.com.br/doc/arquitetura-alfredo-v0-knowledge-base-Gov7UtFLgX | area: Tecnologia -->

# Arquitetura — Alfredo v0 + Knowledge Base

# Arquitetura — Alfredo v0 + Knowledge Base

* **Status:** Em implementação
* **Repo:** `[seazone-tech/alfredo](https://github.com/seazone-tech/alfredo)`
* **Referência:** [Seazone Oracle](https://github.com/seazone-tech/seazone-oracle) (agente vencedor do Hackathon 2026)
* **Análise arquitetural:** [Single Agent vs Orchestrator](https://outline.seazone.com.br/doc/single-agent-vs-orchestrator-analise-arquitetural-33JfoKIFLS)


---

## 1. O que é o Alfredo

Agente de governança AI-First da Seazone. Interface principal via Slack (slash commands). Tudo que o Alfredo faz no Slack resulta em commit ou PR no GitHub — **GitHub é fonte de verdade, Slack é interface**.

### Comandos v0

| Comando | O que faz | Repo impactado |
|----|----|----|
| `/alfredo deploy` | Registra app, cria YAML, configura domínio | `sre-app-catalog` |
| `/alfredo rfc "descrição"` | Faz perguntas, monta RFC, abre PR | `sre-docs-governance` |
| `/alfredo bypass <ID>` | Coleta justificativa, notifica aprovadores | `sre-guardrails` + `sre-app-catalog` |
| `/alfredo status <app>` | Mostra último scan, tier, dependências | Lê `sre-app-catalog` |
| `/alfredo guardrails` | Lista regras ativas para o tier do app | Lê `sre-guardrails` |


---

## 2. Padrão Arquitetural: Routing + Agents-as-Tools

Baseado na [análise arquitetural](https://outline.seazone.com.br/doc/single-agent-vs-orchestrator-analise-arquitetural-33JfoKIFLS), o Alfredo usa **Routing Pattern** (nível 3 na hierarquia Anthropic) com **agents-as-tools** para raciocínio focado.

### Por que não Orchestrator multi-agent?

* Routing é determinístico (usuário define via slash command)
* Fluxos são sequenciais (sem paralelização no v0)
* Multi-agent amplifica erros em até 17.2x (Google DeepMind/MIT)
* 79% das falhas em produção de multi-agent são de coordenação

### O pattern agents-as-tools

Cada comando que precisa de raciocínio profundo chama um **sub-agente focado definido como AI SDK tool**. O sub-agente tem prompt próprio, modelo próprio, e RAG automático.

```mermaidjs
sequenceDiagram
    actor User
    participant Slack
    participant Router as Code Router
    participant Handler as Command Handler<br/>(state machine)
    participant Agent as Sub-Agent Tool<br/>(LLM focado)
    participant KB as Knowledge Base
    participant GH as GitHub API

    User->>Slack: /alfredo bypass SEC-003
    Slack->>Router: POST webhook
    Router->>Handler: bypass handler
    Handler->>Slack: Perguntas (app? justificativa?)
    User->>Slack: Respostas
    Handler->>Agent: assess_risk(guardrail, app, justificativa)
    Agent->>KB: RAG query automática
    KB-->>Agent: Contexto de negócio
    Agent-->>Handler: { risco: "alto", recomendação: "..." }
    Handler->>GH: Registra audit trail
    Handler->>Slack: Resultado formatado
```

### Mapeamento comando → sub-agents

```mermaidjs
graph TD
    subgraph Alfredo
        R["⚡ Code Router<br/>(determinístico)"]
        
        R --> S["/status<br/>Leitura pura<br/>Sem LLM"]
        R --> G["/guardrails<br/>Leitura pura<br/>Sem LLM"]
        R --> D["/deploy<br/>State machine"]
        R --> RF["/rfc<br/>State machine"]
        R --> B["/bypass<br/>State machine"]
    end
    
    subgraph SubAgents["Sub-Agents (tools)"]
        GA["🤖 generate_app_yaml<br/>modelo: fast<br/>prompt: YAML specialist"]
        DR["🤖 draft_rfc<br/>modelo: strong<br/>prompt: RFC writer"]
        AR["🤖 assess_risk<br/>modelo: strong<br/>prompt: risk assessor"]
    end
    
    D -->|"quando coleta completa"| GA
    RF -->|"quando coleta completa"| DR
    B -->|"quando coleta completa"| AR
    
    GA -.->|RAG auto| KB["📚 Knowledge Base"]
    DR -.->|RAG auto| KB
    AR -.->|RAG auto| KB
    
    style S fill:#94a3b8,color:#fff
    style G fill:#94a3b8,color:#fff
    style GA fill:#22c55e,color:#fff
    style DR fill:#3b82f6,color:#fff
    style AR fill:#ef4444,color:#fff
```

| Comando | Sub-agent | Modelo | Prompt focado em |
|----|----|----|----|
| `/alfredo deploy` | `generate_app_yaml` | fast | Gerar YAML do app catalog |
| `/alfredo rfc` | `draft_rfc` | strong | Redigir RFC com impacto de negócio |
| `/alfredo bypass` | `assess_risk` | strong | Avaliar risco do bypass |
| `/alfredo status` | nenhum | — | Leitura pura do GitHub |
| `/alfredo guardrails` | nenhum | — | Leitura pura do GitHub |

### Benefícios

* **Contexto isolado** — cada sub-agent tem prompt de \~200 tokens (vs prompt gigante)
* **Modelo certo pra task** — `assess_risk` usa modelo forte, `generate_app_yaml` usa rápido
* **Testável** — cada sub-agent é uma função input → output
* **Zero overhead** — é uma chamada de função, não coordenação entre agentes
* **Forward-compatible** — amanhã um sub-agent pode ganhar tools próprios


---

## 3. Arquitetura Geral

```mermaidjs
graph TD
    Slack["🗨️ Slack<br/>(slash commands + events)"] --> SI["Slack Interface Layer<br/>HMAC verification + ack"]
    
    subgraph Alfredo["Alfredo (Next.js 16 + TypeScript)"]
        SI --> Router["Code Router<br/>parseCommand()"]
        Router --> Handlers["Command Handlers<br/>(state machines)"]
        Handlers --> Agents["Sub-Agent Tools<br/>generate_app_yaml<br/>draft_rfc<br/>assess_risk"]
        Agents --> RAG["RAG Layer"]
        Agents --> LLM["LLM Layer<br/>Two-tier via Hub"]
    end
    
    Handlers --> GH["GitHub API<br/>sre-guardrails<br/>sre-docs-governance<br/>sre-app-catalog"]
    RAG --> PG["PostgreSQL<br/>pgvector + state"]
    LLM --> Hub["Seazone Hub<br/>hub.seazone.dev"]
    Handlers --> PG
```


---

## 4. Stack Técnica

| Camada | Tecnologia | Justificativa |
|----|----|----|
| **Framework** | Next.js 16 + TypeScript | Mesma stack do Oracle (referência) |
| **AI** | Vercel AI SDK v6 | `generateText()` + `tool()` para sub-agents |
| **LLM** | Seazone Hub (`hub.seazone.dev`) | Governança de custos built-in, OpenAI-compatible |
| **Modelos** | Two-tier via Hub | Fast (`gemini-3-flash`/`claude-haiku`) + Strong (`claude-sonnet`) |
| **Database** | PostgreSQL + pgvector | Estado persistente + RAG |
| **Slack** | Slack App dedicada | Slash commands + event subscriptions |
| **GitHub** | GitHub App | Commits/PRs via API. JWT + installation tokens |
| **Deploy** | EC2 ou EKS | A definir. App é stateless |


---

## 5. Componentes

### 5.1 Code Router

Routing determinístico por slash command. Sem LLM — é um `switch` no nome do comando.

### 5.2 Command Handlers (State Machines)

Cada comando multi-turn é uma state machine:

* **Estado** persiste no PostgreSQL (`conversations.state` JSONB)
* **Perguntas** são fixas (não geradas por LLM — mais previsível)
* **Quando coleta termina**, chama o sub-agent apropriado
* **Resultado** é formatado e postado no Slack

### 5.3 Sub-Agent Tools

Criados via factory `createAgentTool()`:

* Recebe parâmetros tipados (Zod schema)
* Injeta RAG context automaticamente (se `ragQuery` definido)
* Chama `generateText()` com prompt focado
* Aplica privacy scan no output
* Retorna texto estruturado

### 5.4 RAG Layer

* Embedding via modelo do Hub
* Vector search via pgvector (HNSW, cosine similarity)
* Top-6 chunks deduplicados por documento
* Contexto injetado no prompt do sub-agent


---

## 6. Modelo de Dados

```mermaidjs
erDiagram
    conversations ||--o{ messages : "has"
    conversations ||--o{ actions : "triggers"
    kb_documents ||--o{ kb_chunks : "contains"

    conversations {
        uuid id PK
        text slack_channel_id
        text slack_thread_ts
        text slack_user_id
        text command
        jsonb state
        text status
        timestamptz created_at
    }

    messages {
        uuid id PK
        uuid conversation_id FK
        text role
        text content
        int tokens_input
        int tokens_output
        text model
    }

    actions {
        uuid id PK
        uuid conversation_id FK
        text action_type
        text target_repo
        text github_url
        jsonb payload
    }

    kb_documents {
        uuid id PK
        text title
        text file_path
        text content
        jsonb metadata
    }

    kb_chunks {
        uuid id PK
        uuid document_id FK
        text content
        text section
        vector embedding
        int token_count
    }
```


---

## 7. Knowledge Base

### Pipeline de ingestão

```mermaidjs
flowchart LR
    MD["📄 Markdown files"] --> Parse["Parse<br/>heading hierarchy"]
    Parse --> Chunk["Chunk<br/>por seção h1/h2/h3"]
    Chunk --> Embed["Embed<br/>modelo do Hub"]
    Embed --> PG["PostgreSQL<br/>kb_chunks (pgvector)"]
    PG --> Search["Search<br/>cosine similarity<br/>top-6 chunks"]
    Search --> Prompt["Contexto injetado<br/>no sub-agent"]
```

### Fontes de conteúdo

| Fonte | Conteúdo |
|----|----|
| Outline: Base de Conhecimento | 100 cards em 13 categorias |
| Outline: Processo de Suportes | Fluxo Pipefy, prioridades, SLAs |
| Outline: Google Workspace | Criar/recuperar/remover contas (44% dos tickets) |
| Outline: Post-mortems | Sapron, Redis, Prometheus, ArgoCD |
| sre-docs-design | Spec completo da governança |


---

## 8. Segurança

| Camada | Controle |
|----|----|
| **Slack** | Verificação HMAC-SHA256 em todo webhook |
| **GitHub App** | JWT + installation tokens, permissões mínimas |
| **LLM** | Seazone Hub com budget por key |
| **Privacy** | Input screening + output scanning em todo sub-agent |
| **Secrets** | Tudo via variáveis de ambiente |


---

## 9. Relação com Outros Agentes

| Agente | Relação com Alfredo |
|----|----|
| **Oracle** | Referência de arquitetura. Sem interação direta. |
| **Argus** (`alfred-reviewer`) | Overlap na Fase 2+ (ambos em PRs). v0 sem conflito. |
| **Brisa** | Referência de orchestration. Alfredo usa pattern mais simples (Routing). |
| **Garra / Sherlog** (OpenClaw) | Sem overlap. Alfredo é Slack App dedicada. |


---

## 10. Roadmap pós-v0

```mermaidjs
gantt
    title Evolução do Alfredo
    dateFormat  YYYY-MM-DD
    section v0 (atual)
    Alfredo core + KB + agents-as-tools :active, v0, 2026-04-10, 4w
    section v1
    Análise de código em PRs             :v1a, after v0, 3w
    Parallelization (checks simultâneos) :v1b, after v0, 2w
    section v2
    KB expandida + ingest automático     :v2a, after v1a, 4w
    Coordenação com Argus                :v2b, after v1a, 2w
```