<!-- title: Politica de Uso de IA — Seazone | url: https://outline.seazone.com.br/doc/politica-de-uso-de-ia-seazone-vYpId6f8Es | area: Tecnologia -->

# Politica de Uso de IA — Seazone

## TL;DR

**Toda IA na Seazone passa pelo [hub.seazone.dev](https://hub.seazone.dev).** Voce recebe uma virtual key do SRE, configura na ferramenta aprovada, e usa. Simples.


---

## Por que isso existe?

A Seazone adotou **AI First**. Pra isso funcionar sem virar bagunca, centralizamos tudo num gateway unico. Isso garante:

* Custo controlado (budgets por time e por pessoa)
* Dados protegidos (PII mascarado automaticamente antes de sair)
* Visibilidade total (cada request e rastreado)

```mermaidjs
graph LR
    DEV["Voce"] --> HUB["hub.seazone.dev<br/><small>Gateway unico</small>"]
    HUB --> AI["Modelos de IA"]
    
    style HUB fill:#2d6a4f,color:#fff
    style DEV fill:#1a1a2e,color:#fff
```


---

## Ferramentas Aprovadas

| Ferramenta | Pra que | Como acessar |
|----|----|----|
| OpenClaude | Coding agent no terminal | `openclaude` no terminal ([ver guidebook dev](/doc/guidebook-dev-ia-na-seazone-EjPZKrqBbX)) |
| [Continue.dev](https://continue.dev) | IA dentro do VS Code / JetBrains | Extensao + config ([ver guidebook dev](/doc/guidebook-dev-ia-na-seazone-EjPZKrqBbX)) |
| OpenClaw | Agentes corporativos (Slack/WhatsApp) | Ja configurado — Garra, Sherlog, etc. |


---

## O que NAO usar

| Proibido | Por que |
|----|----|
| ChatGPT web (chat.openai.com) | Sem controle, sem masking de PII, sem audit trail |
| Claude web (claude.ai) | Mesmo problema |
| Gemini web (gemini.google.com) | Idem |
| API keys diretas de qualquer provedor | Bypass do gateway = sem protecao, sem visibilidade |

**Se voce precisa de algo que as ferramentas aprovadas nao cobrem**, fale com seu Tech Lead. A gente resolve.


---

## Classificacao de Dados

```mermaidjs
graph TD
    Q["Que tipo de dado<br/>voce vai enviar?"]
    Q -->|"Publico / interno<br/>(codigo, docs, specs)"| OK["Qualquer modelo<br/>via gateway"]
    Q -->|"Confidencial<br/>(contratos, estrategia)"| REST["Apenas Gemini<br/>(Vertex AI)"]
    Q -->|"PII de clientes<br/>(nome, CPF, email)"| PII["Masking automatico<br/>(Presidio ativo)"]
    
    OK --> USE["Pode usar"]
    REST --> USE
    PII --> USE
    
    style Q fill:#1a1a2e,color:#fff
    style PII fill:#e63946,color:#fff
    style OK fill:#2d6a4f,color:#fff
    style REST fill:#e9c46a,color:#000
```

| Tipo de dado | Pode usar IA? | Condicoes |
|----|----|----|
| **Publico / interno** (codigo, docs, specs) | Sim | Qualquer modelo via gateway |
| **Confidencial** (contratos, estrategia, financeiro) | Com restricoes | Apenas Gemini (Google Vertex AI) |
| **PII de clientes** (nome, CPF, email, telefone) | Com protecao automatica | O Presidio mascara automaticamente |

**Na duvida, use normalmente.** O gateway tem protecoes ativas:

* **Presidio** mascara nomes, CPF, CNPJ, emails, telefones e cartoes automaticamente
* **hide-secrets** detecta e bloqueia AWS keys, tokens do GitHub, senhas de banco


---

## Como Pedir Acesso

```mermaidjs
graph LR
    A["Voce pede<br/>pro Tech Lead"] --> B["Tech Lead aprova"]
    B --> C["SRE cria sua<br/>virtual key"]
    C --> D["Voce configura<br/>na ferramenta"]
    D --> E["Usa!"]
    
    style C fill:#2d6a4f,color:#fff
```


1. Fale com seu **Tech Lead**
2. O Tech Lead aprova e pede pro **SRE**
3. Voce recebe uma **virtual key** (`sk-sz-...`) com budget mensal
4. Configura na ferramenta ([ver guidebook dev](/doc/guidebook-dev-ia-na-seazone-EjPZKrqBbX))


---

## Modelos Disponiveis

| Modelo | Quando usar |
|----|----|
| **MiniMax M2.7** (padrao) | Coding, chat, agentes |
| **MiniMax M2.5** | Chat rapido, classificacao, autocomplete |
| **Gemini 2.5 Flash** | Contexto longo (1M tokens), compliance, dados sensiveis |


---

## Responsabilidades

* **Voce revisa** o que a IA gera antes de committar, publicar ou enviar
* **A IA nao substitui** code review, QA ou decisoes de negocio
* **Se algo parecer errado**, confira. Modelos alucinam
* **Seus requests sao rastreados** — nao pra te vigiar, mas pra controle e seguranca


---

## Duvidas?

* **Tecnico**: fale com o time de SRE no Slack
* **Politica**: fale com seu Tech Lead
* **Bug nas ferramentas**: abra issue em [seazone-tech/llm-hub](https://github.com/seazone-tech/llm-hub)