<!-- title: Plataforma Centralizada de IA — Seazone | url: https://outline.seazone.com.br/doc/plataforma-centralizada-de-ia-seazone-blLBvsNAmP | area: Tecnologia -->

# Plataforma Centralizada de IA — Seazone

## Contexto

A Seazone adotou a diretriz **AI First**. Hoje o cenario e caotico: multiplas IAs, API keys soltas. Este plano centraliza tudo via **LiteLLM** como gateway unico.

**Decisoes-chave:**

* **MiniMax M2.7** como modelo padrao ($0.30/$1.20 por M tokens, supera Claude Sonnet em tool use)
* **OpenClaude** como coding agent (testado e escolhido no piloto)
* **Continue.dev** como coding IDE (testado e validado)
* **LibreChat** como chat corporativo (substitui ChatGPT/Claude/Gemini web)
* **OpenClaw** mantido com hardening (ja em uso)
* **Langfuse** para observabilidade de LLM (deployado e funcionando)
* Sem Claude no catalogo padrao (disponivel sob demanda)


---

## 1. Arquitetura

### Estado Atual (hub.seazone.dev)

O LiteLLM ja esta no **Railway** (projeto `llm-hub-seazone`, repo `seazone-tech/llm-hub`):

* LiteLLM **v1.83.3.rc.1** (deployado 2026-04-07), PostgreSQL, Redis (tudo Railway managed)
* 7 providers, 15+ modelos, fallback chains
* Claude Code routing transparente: `claude-sonnet-4-6` -> MiniMax M2.7 -> GLM-4.7 -> DeepSeek
* Use-case aliases: `apps-*`, `sia-*`, `claws-*`, `pipeline-*`
* Dominio: **hub.seazone.dev**
* `STORE_MODEL_IN_DB=true` — virtual keys habilitadas
* Provider prefix nativo `minimax/` — cost tracking funcionando
* Routing strategy: `usage-based-routing-v2`
* Custom pricing MiniMax M2.7/M2.5 — spend tracking validado
* **Guardrails**: Presidio PII masking + secrets detection (hide-secrets)
* **Observabilidade**: Langfuse callbacks (cloud.langfuse.com)

### Diagrama

```mermaidjs
graph TB
    subgraph consumers["Consumidores"]
        LC["LibreChat<br/><small>Chat corporativo</small>"]
        OC["OpenClaude<br/><small>Coding agent (escolhido)</small>"]
        CD["Continue.dev<br/><small>IDE (validado)</small>"]
        CW["OpenClaw<br/><small>Agentes Slack/WA</small>"]
        AP["Apps internos<br/><small>SDK OpenAI-compat</small>"]
    end

    subgraph gateway["LiteLLM Proxy — hub.seazone.dev (Railway)"]
        direction TB
        VK["Virtual Keys + Budgets"]
        GR["Guardrails<br/><small>Presidio PII + hide-secrets</small>"]
        RT["Routing + Fallbacks"]
        LF["Langfuse callback"]
    end

    subgraph providers["Provedores"]
        MM["MiniMax M2.7<br/><small>DEFAULT $0.30/M</small>"]
        ZH["Zhipu GLM-4.7 / GLM-5<br/><small>Fallback</small>"]
        GE["Gemini 2.5 Flash<br/><small>Compliance $0.15/M</small>"]
        DS["DeepSeek V3.1 / Qwen3 Coder / Kimi K2 / Devstral<br/><small>Ollama Cloud</small>"]
        OR["OpenRouter<br/><small>Free tier</small>"]
    end

    subgraph obs["Observabilidade"]
        LFU["Langfuse Cloud<br/><small>Traces + Evals + Cost</small>"]
    end

    consumers --> gateway
    gateway --> providers
    gateway --> obs

    style MM fill:#2d6a4f,color:#fff
    style gateway fill:#1a1a2e,color:#fff
    style GR fill:#e63946,color:#fff
    style LFU fill:#2d6a4f,color:#fff
```

### Conexoes

```bash
# Claude Code (JA FUNCIONA — alias transparente pra M2.7)
export ANTHROPIC_BASE_URL="https://hub.seazone.dev"
export ANTHROPIC_API_KEY="sk-sz-..."

# OpenClaude (escolhido no piloto)
export CLAUDE_CODE_USE_OPENAI=1
export OPENAI_API_KEY="sk-sz-..."
export OPENAI_BASE_URL="https://hub.seazone.dev/v1"
export OPENAI_MODEL="minimax-m2.7"

# Continue.dev (~/.continue/config.yaml)
models:
  - name: MiniMax M2.7
    provider: openai
    model: minimax-m2.7
    apiBase: https://hub.seazone.dev/v1
    apiKey: sk-sz-...

# Apps internos
client = OpenAI(base_url="https://hub.seazone.dev/v1", api_key="sk-sz-app-...")
```


---

## 2. Guardrails

### Guardrails Ativos

| Guardrail | Provider | Custo | Status |
|----|----|----|----|
| **PII masking** | Presidio (Railway) | \~$10/mes | Funcionando — mascara nomes, CPF, CNPJ, email, telefone, cartao |
| **Secrets detection** | LiteLLM built-in (hide-secrets) | $0 | Funcionando — detecta AWS keys, GitHub tokens, DB URLs |

### Estrategia por Tipo de Uso

| Tipo | PII (Presidio) | Secrets |
|----|----|----|
| **Devs (coding)** | MASK | On |
| **Chat (LibreChat)** | MASK | On |
| **OpenClaw (input externo)** | MASK | On |
| **Apps (backend)** | MASK | On |

### PII — Entidades Detectadas

* Nativo Presidio: CREDIT_CARD, PHONE_NUMBER, EMAIL_ADDRESS, PERSON
* Custom BR: **BR_CPF** (xxx.xxx.xxx-xx), **BR_CNPJ** (xx.xxx.xxx/xxxx-xx)

### Seguranca (OWASP LLM Top 10)

| Risco | Controle |
|----|----|
| **Sensitive Info Disclosure** | Presidio MASK + hide-secrets em todos os requests |
| **Unbounded Consumption** | Budget hard limits + rate limits |
| **Excessive Agency** | OpenClaw tool allowlists |

### Futuro (quando necessario)

* **Prompt injection**: Lakera (free tier 100K/mes) — adicionar quando tiver input externo (LibreChat publico, chatbots)
* **Slack alerts**: Configurar SLACK_WEBHOOK_URL pra budget alerts, outage alerts


---

## 3. Catalogo de Modelos

### Modelos Configurados (hub.seazone.dev — config real)

**MiniMax (default):**

* `minimax-m2.7` — MiniMax M2.7 ($0.30/$1.20/M) — **modelo padrao pra tudo**
* `minimax-m2.5` — MiniMax M2.5 ($0.30/$2.40/M) — chat, apps, SIA WhatsApp

**Zhipu AI:**

* `zhipu-glm5` — GLM-5 (mais recente)
* `zhipu-glm4.7` — GLM-4.7 (fallback Claude Code)
* `zhipu-glm4.7-flash` — GLM-4.7 Flash
* `zhipu-glm4.5` — GLM-4.5-Air
* `zhipu-glm4.5-flash` — GLM-4.5 Flash

**Google:**

* `gemini-2.5-flash` — Gemini 2.5 Flash ($0.15/$0.60/M) — compliance, contexto 1M

**Ollama Cloud (open-source hospedados):**

* `ollama-deepseek` — DeepSeek V3.1 671B
* `ollama-qwen-coder` — Qwen3 Coder 480B
* `ollama-kimi` — Kimi K2 1T
* `ollama-devstral` — Devstral 2 123B

**OpenRouter (free tier):**

* `openrouter-free` — Qwen3 Coder (free)
* `openrouter-minimax` — MiniMax M2.5 (free)
* `openrouter-nemotron` — Nemotron 3 Super 120B (free)

### Fallback Chains

| Modelo | Fallback 1 | Fallback 2 |
|----|----|----|
| `claude-sonnet` | GLM-4.7 | DeepSeek V3.1 |
| `claude-opus` | GLM-4.7 | M2.7 |
| `claude-haiku` | GLM-4.5 | OpenRouter free |
| `minimax-m2.7` | DeepSeek V3.1 | OpenRouter free |
| `gemini-2.5-flash` | Qwen3 Coder | OpenRouter free |

### Use-Case Aliases

| Alias | Uso | Primary | Fallback |
|----|----|----|----|
| `apps-classify` | Classificacao | GLM-4.5-Air | MiniMax M2.5 |
| `apps-chat` | Chat/sumarizacao | MiniMax M2.5 | OpenRouter M2.5 free |
| `apps-premium` | PT-BR premium | MiniMax M2.5 | GLM-4.5-Air |
| `apps-extract` | Structured output | GLM-4.5-Air | — |
| `apps-batch` | Batch processing | DeepSeek V3.1 | MiniMax M2.5 |
| `sia-default` | SIA WhatsApp | MiniMax M2.5 | GLM-4.5-Air |
| `claws-default` | OpenClaw agentes | MiniMax M2.5 | GLM-4.5-Air |
| `pipeline-default` | CI/CD agentes | MiniMax M2.7 | DeepSeek V3.1 |
| `pipeline-complex` | Tarefas complexas | MiniMax M2.7 | GLM-4.7 |

### Por que MiniMax M2.7 como default

* $0.30/$1.20 por M tokens (50x mais barato que Claude Opus)
* 88% win-rate vs M2.5, supera Claude Sonnet em tool calling
* SWE-Pro 56.2% (mesmo nivel do GPT-5.3-Codex)
* Contexto 204.8K, 100 tok/s output speed
* Open-weight (self-host via Ollama/vLLM se data residency for concern)

**Dados sensiveis/PII -> Gemini via Vertex AI** (SOC2, ISO 27001, HIPAA). MiniMax e empresa chinesa — Presidio mascara automaticamente antes de enviar.

```mermaidjs
graph LR
    subgraph tier1["Tier 1 — Default"]
        M27["MiniMax M2.7<br/>$0.30 / $1.20<br/>204K ctx<br/><b>88% win vs M2.5</b>"]
        GF["Gemini 2.5 Flash<br/>$0.15 / $0.60<br/>1M ctx"]
        DS["DeepSeek V3.1<br/>Ollama Cloud"]
    end

    subgraph tier2["Tier 2 — Compliance / Fallback"]
        G3F["Gemini 3 Flash<br/>$0.50 / $3.00<br/>1M ctx"]
        G25P["Gemini 2.5 Pro<br/>$1.25 / $10.00<br/>1M ctx"]
    end

    subgraph tier3["Tier 3 — Premium"]
        G31P["Gemini 3.1 Pro<br/>$2.00 / $12.00<br/>1M ctx<br/><b>80.6% SWE-bench</b>"]
    end

    M27 -->|fallback| G3F
    G3F -->|fallback| GF
    G31P -->|fallback| M27

    style M27 fill:#2d6a4f,color:#fff
    style tier1 fill:#1a1a2e,color:#fff
```


---

## 4. Coding Assistant

### OpenClaude (escolhido no piloto)

| Aspecto | Detalhe |
|----|----|
| **Base** | Fork do Claude Code (multi-provider) |
| **Providers** | 200+ (via OpenAI-compatible) |
| **Tools** | Identicas ao Claude Code (Read, Edit, Bash, Grep, etc.) |
| **Conexao** | `OPENAI_BASE_URL=hub.seazone.dev/v1` + virtual key |

**OpenCode** (clean-room em Go, 95-120k stars) foi testado no piloto mas o OpenClaude se mostrou melhor fit pro case atual da Seazone — interface familiar, mesmo toolset do Claude Code, transicao transparente pros devs.

### Continue.dev (validado no piloto)

| Aspecto | Detalhe |
|----|----|
| **Tipo** | Extensao VS Code / JetBrains |
| **Funcoes** | Chat (Ctrl+L), inline edit (Ctrl+I), tab autocomplete |
| **Config** | `~/.continue/config.yaml` — M2.7 chat/edit, M2.5 autocomplete |
| **Status** | Testado e funcionando com hub.seazone.dev |

### Economia

| Cenario | Custo/mes (20 devs) | Custo/ano |
|----|----|----|
| Claude Code Max 5x | $2.000 | $24.000 |
| **OpenClaude + Continue.dev + M2.7** | **$300-600** | **$3.600-7.200** |
| **Economia** |    | **70-85%** |


---

## 5. OpenClaw — Hardening

Agentes em uso: Garra, Sherlog, Re-Vision, Triago, Dalton, suporte-bizops.

**Ja concluido (2026-04-06):**

- [x] Atualizado para **v2026.4.5** (versao mais recente, CVE-2026-25253 corrigido)
- [x] Migrado de OpenRouter para **hub.seazone.dev** (config EC2 atualizada)

### Acoes Pendentes

| Acao | Prioridade |
|----|----|
| Habilitar OpenTelemetry export para observabilidade | **P2** |
| Adicionar NetworkPolicy no EKS (restringir egress) | **P2** |


---

## 6. Politica de API Keys

> **Ninguem usa chave direta de provedor. Tudo via virtual keys do LiteLLM.**

```mermaidjs
graph LR
    DEV["Dev solicita"] --> TL["Tech Lead aprova"]
    TL --> SRE["SRE cria virtual key"]
    SRE --> KEY["Key com budget + modelos + rate limit"]
    KEY --> DEV2["Dev configura ferramenta"]
    DEV2 --> MON["Plataforma monitora uso"]

    style SRE fill:#2d6a4f,color:#fff
```

| Tipo | Destinatario | Budget |
|----|----|----|
| **Personal** | Dev individual | $50-100/mes |
| **Service** | App/agente producao | Por projeto |
| **OpenClaw** | Agente especifico | $50-100/agente |
| **Sandbox** | Experimentacao | $20/mes, auto-expira 30d |

**Administracao**: Time de SRE cria/revoga keys via API ou UI do LiteLLM.


---

## 7. Observabilidade

### Langfuse (principal) — ATIVO

* **URL**: cloud.langfuse.com (free tier)
* **Integracao**: success_callback + failure_callback no LiteLLM
* **Dados**: cada request individual, traces de agentes, custo por user/team
* **Tags automaticas**: User-Agent, seazone, hub

```mermaidjs
graph TB
    LLM["LiteLLM Proxy"] --> LF["Langfuse Cloud<br/><small>Traces, cost por request,<br/>prompts, evals, sessoes</small>"]
    LF --> DASH["Dashboard Langfuse"]

    style LF fill:#2d6a4f,color:#fff
```

### KPIs

| KPI | Meta |
|----|----|
| % requests via gateway | 100% |
| Gasto total mensal | Dentro do budget |
| % gasto em Tier 1 (M2.7) | > 60% |
| Shadow AI incidents | Zero |
| PII detections/mes | Tendencia de queda |


---

## 8. Politica de Uso de IA

Tom pragmatico — primeira politica da empresa.

**O padrao e usar o hub.seazone.dev pra tudo.** Se precisar de excecao, fale com seu Tech Lead.

### Ferramentas Aprovadas

| Ferramenta | Uso |
|----|----|
| LibreChat | Chat com IA |
| OpenClaude | Coding agent (terminal) |
| Continue.dev | Coding IDE (VS Code / JetBrains) |
| OpenClaw | Agentes corporativos (Slack) |

### Classificacao de Dados

| Dados | Pode usar IA? | Condicoes |
|----|----|----|
| Publicos/internos | Sim | Qualquer modelo via gateway |
| Confidenciais | Com restricoes | Apenas Gemini (Vertex AI). PII masking automatico. |
| PII de clientes | Com aprovacao | Masking obrigatorio (Presidio ativo). |


---

## 9. Plano de Implementacao

```mermaidjs
graph TB
    subgraph f0["Fase 0 — Fundacao ✅"]
        F0A["✅ LiteLLM v1.83.3"]
        F0B["✅ STORE_MODEL_IN_DB"]
        F0C["✅ Virtual keys"]
        F0D["✅ OpenClaw v2026.4.5"]
        F0E["✅ minimax/ nativo"]
        F0F["✅ usage-based-v2"]
    end

    subgraph f1["Fase 1 — Piloto ✅"]
        F1A["✅ Virtual keys pilotos"]
        F1B["✅ Teams piloto"]
        F1C["✅ OpenClaude escolhido"]
        F1D["✅ OpenClaw no hub"]
        F1E["✅ Continue.dev"]
        F1F["✅ Spend tracking"]
    end

    subgraph f2["Fase 2 — Guardrails + Obs ✅"]
        F2A["✅ Presidio PII"]
        F2B["✅ hide-secrets"]
        F2C["✅ Langfuse"]
        F2D["⏳ Slack alerts"]
    end

    subgraph f3["Fase 3 — Rollout Dev"]
        F3A["Virtual keys todos devs"]
        F3B["Deploy LibreChat"]
        F3C["Handbook"]
    end

    subgraph f4["Fase 4 — Rollout Empresa"]
        F4A["LibreChat empresa"]
        F4B["Politica de IA"]
        F4C["DNS blocking"]
    end

    subgraph f5["Fase 5 — Maturidade"]
        F5A["Apps no gateway"]
        F5B["Evals Langfuse"]
        F5C["Revisao trimestral"]
    end

    f0 --> f1 --> f2 --> f3 --> f4 --> f5
```

### Fase 0 — Fundacao ✅ CONCLUIDA

- [x] LiteLLM deployado no Railway (hub.seazone.dev)
- [x] PostgreSQL + Redis provisionados
- [x] Catalogo de modelos (15+ modelos, 7 providers, fallback chains)
- [x] Claude Code routing transparente
- [x] Use-case aliases configurados
- [x] **LiteLLM atualizado para v1.83.3.rc.1** (2026-04-07)
- [x] **STORE_MODEL_IN_DB=true** — virtual keys habilitadas e testadas
- [x] **Provider prefix** `**minimax/**` **nativo** — cost tracking funcionando
- [x] **Routing strategy** `**usage-based-routing-v2**`
- [x] **GPT-4.1-nano removido** (OpenAI sem saldo) — fallbacks ajustados
- [x] **OpenClaw atualizado para v2026.4.5** (CVE-2026-25253 corrigido)
- [x] **Custom pricing MiniMax M2.7/M2.5** — spend tracking validado

### Fase 1 — Piloto ✅ CONCLUIDA

- [x] Virtual keys criadas para pilotos: Eos Xavier, Guilherme (devs), OpenClaw (servico)
- [x] Teams piloto criados: `team-sre` (Eos, Guilherme), `claws-assistants` (OpenClaw) — budget $800/mes
- [x] OpenClaude e OpenCode testados com M2.7 — **OpenClaude escolhido**
- [x] OpenClaw migrado de OpenRouter para hub.seazone.dev
- [x] Continue.dev instalado e validado (VS Code Insiders, M2.7 chat/edit + M2.5 autocomplete)
- [x] Spend tracking validado — custom pricing aplicado, custo por user/team visivel
- [x] Feedback do piloto: OpenClaude escolhido, Continue.dev aprovado, M2.7 confirmado

### Fase 2 — Guardrails + Observabilidade ✅ CONCLUIDA

- [x] **Presidio PII masking** — 2 containers Railway (analyzer + anonymizer), mascaramento de nomes, CPF, CNPJ, email, telefone, cartao de credito validado
- [x] **hide-secrets** — deteccao de AWS keys, GitHub tokens, DB URLs nos prompts
- [x] **Langfuse** — callbacks success/failure configurados, traces visiveis em cloud.langfuse.com
- [ ] Slack alerts — config preparado, falta SLACK_WEBHOOK_URL

### Fase 3 — Rollout Dev (proximo)

- [ ] Virtual keys pra todos os devs
- [ ] Deploy LibreChat apontando pra hub.seazone.dev
- [ ] Documentar setup no handbook
- [ ] Treinar Tech Leads no acompanhamento de budgets

### Fase 4 — Rollout Empresa

- [ ] LibreChat pra toda a empresa (nao so devs)
- [ ] Publicar politica corporativa de IA
- [ ] Bloquear DNS/firewall pra APIs diretas dos provedores

### Fase 5 — Maturidade

- [ ] Onboarding de apps internos no gateway
- [ ] Evals automatizados via Langfuse
- [ ] Avaliar novos modelos conforme lancamentos


---

## 10. Recomendacoes

### Fazer


1. **MiniMax M2.7 como default.** Melhor custo-beneficio do mercado. Gemini como fallback/compliance.
2. **OpenClaude pro time de dev.** Testado no piloto, economia de 70-85% vs Claude Code.
3. **Bloquear DNS pra APIs diretas.** Politica sem enforcement tecnico e sugestao. So o gateway sai.
4. **LibreChat mata uso de ChatGPT/Claude web.** Maior driver de adocao entre nao-devs.
5. **Langfuse ativo.** Monitorar traces, custos e PII detections.

### Apendice: Comparativo de Modelos (Abril 2026)

| Modelo | Provider | In $/M | Out $/M | Ctx | Coding | Residency |
|----|----|----|----|----|----|----|
| DeepSeek V3.2 | DeepSeek | $0.14 | $0.28 | 128K | \~72% SWE | China |
| Gemini 2.5 Flash | Google | $0.15 | $0.60 | 1M | Bom | US/EU |
| **MiniMax M2.7** | **MiniMax** | **$0.30** | **$1.20** | **204K** | **SWE-Pro 56.2%** | **China/Self-host** |
| Gemini 3 Flash | Google | $0.50 | $3.00 | 1M | Supera 2.5 Pro | US/EU |
| Gemini 2.5 Pro | Google | $1.25 | $10.00 | 1M | \~67% SWE | US/EU |
| Gemini 3.1 Pro | Google | $2.00 | $12.00 | 1M | 80.6% SWE | US/EU |
| Claude Sonnet 4 | Anthropic | $3.00 | $15.00 | 200K | \~70% SWE | US |
| Claude Opus 4.6 | Anthropic | $15.00 | $75.00 | 200K | 80.8% SWE | US |