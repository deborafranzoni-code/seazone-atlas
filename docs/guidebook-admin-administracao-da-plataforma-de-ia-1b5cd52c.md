<!-- title: Guidebook Admin — Administracao da Plataforma de IA | url: https://outline.seazone.com.br/doc/guidebook-admin-administracao-da-plataforma-de-ia-aIuhcETrTq | area: Tecnologia -->

# Guidebook Admin — Administracao da Plataforma de IA

## Visao Geral

Voce administra a plataforma de IA da Seazone. Tudo passa pelo **hub.seazone.dev** — um gateway que controla quem usa, quanto gasta, e protege dados automaticamente.

```mermaidjs
graph TB
    subgraph quem["Quem usa"]
        DEV["Devs<br/><small>OpenClaude + Continue.dev</small>"]
        BOT["Agentes<br/><small>OpenClaw (Garra, Sherlog)</small>"]
        AP["Apps internos"]
    end

    subgraph voce["O que voce gerencia"]
        VK["Quem tem acesso<br/><small>Virtual Keys</small>"]
        BU["Quanto pode gastar<br/><small>Budgets</small>"]
        OB["O que esta acontecendo<br/><small>Langfuse</small>"]
    end

    subgraph auto["Protecoes automaticas"]
        PII["PII mascarado<br/><small>Presidio</small>"]
        SEC["Secrets bloqueados<br/><small>hide-secrets</small>"]
    end

    quem --> voce
    voce --> auto

    style voce fill:#2d6a4f,color:#fff
    style auto fill:#e63946,color:#fff
```

**Seus 2 paineis:**

| Painel | URL | Pra que |
|----|----|----|
| **LiteLLM Admin** | [hub.seazone.dev/ui](https://hub.seazone.dev/ui) | Gerenciar keys, teams, budgets, modelos |
| **Langfuse** | [cloud.langfuse.com](https://cloud.langfuse.com) | Ver quem usou, quanto gastou, traces |


---

## 1. Como os Usuarios Conseguem Acesso

### Self-service via SSO (ate 5 usuarios)

Usuarios com `@seazone.com.br` podem acessar [hub.seazone.dev/ui](https://hub.seazone.dev/ui), clicar **Login with SSO**, e criar suas proprias keys. Budget padrao: $100/mes.

O SSO free do LiteLLM tem limite de **5 usuarios simultaneos**. Esses slots sao pra admins e tech leads.

### Criacao manual (sem limite)

Pra qualquer pessoa que nao consiga logar via SSO, voce cria a key manualmente:


1. Acesse [hub.seazone.dev/ui](https://hub.seazone.dev/ui) como admin
2. Va em **Virtual Keys** > **+ Create New Key**
3. Preencha:

| Campo | O que colocar | Exemplo |
|----|----|----|
| **Key Alias** | Nome descritivo | `dev-maria-silva` |
| **User ID** | Email da pessoa | `maria.silva@seazone.com.br` |
| **Team** | Time da pessoa (opcional) | `team-reservas` |
| **Max Budget** | Limite mensal em dolares | `100` |
| **Budget Duration** | Periodo do budget | `30d` |
| **Models** | Quais modelos pode usar | `minimax-m2.7, minimax-m2.5, gemini-2.5-flash` |


4. Clique **Create Key**
5. **Copie a key gerada** e envie pra pessoa

```mermaidjs
graph LR
    A["Pessoa solicita<br/>acesso"] --> B{"Consegue<br/>SSO?"}
    B -->|Sim| C["Self-service<br/>hub.seazone.dev/ui"]
    B -->|Nao| D["Admin cria key<br/>manualmente"]
    C --> E["Cria propria key"]
    D --> E

    style B fill:#1a1a2e,color:#fff
    style D fill:#2d6a4f,color:#fff
```

### Revogar acesso


1. Em **Virtual Keys**, encontre a key
2. Clique no icone de lixeira
3. Confirme — a key para de funcionar imediatamente


---

## 2. Criar Times (Teams)

Times agrupam pessoas e compartilham um budget coletivo.


1. Em [hub.seazone.dev/ui](https://hub.seazone.dev/ui), va em **Teams**
2. Clique **+ Create New Team**
3. Preencha:

| Campo | Exemplo |
|----|----|
| **Team Alias** | `team-reservas` |
| **Max Budget** | Limite mensal pro time inteiro |
| **Models** | `minimax-m2.7, minimax-m2.5, gemini-2.5-flash` |


4. Depois de criar, clique no team pra **adicionar membros**

### Times que ja existem

| Time | Quem esta | Uso |
|----|----|----|
| team-sre | Eos, Guilherme | SRE |
| claws-assistants | OpenClaw | Agentes Slack/WhatsApp |


---

## 3. Ver Quem Esta Usando (Langfuse)

O [Langfuse](https://cloud.langfuse.com) registra **cada conversa** que passa pelo gateway.

### Como acessar


1. Acesse [cloud.langfuse.com](https://cloud.langfuse.com)
2. Login com Google
3. Selecione o projeto `seazone-ai-hub`

### O que olhar

```mermaidjs
graph TD
    Q["O que voce quer saber?"]
    Q -->|"Quem mais usou<br/>esse mes?"| A["Traces > agrupar por userId"]
    Q -->|"Qual modelo mais<br/>usado?"| B["Traces > agrupar por model"]
    Q -->|"Teve algum erro?"| C["Traces > filtrar level: ERROR"]
    Q -->|"Quanto gastamos<br/>no total?"| D["Dashboard > Cost"]

    style Q fill:#1a1a2e,color:#fff
```

| Pergunta | Onde encontrar |
|----|----|
| Quem mais usou esse mes? | **Traces** > agrupar por `userId` |
| Qual modelo mais usado? | **Traces** > agrupar por `model` |
| Quanto gastamos no total? | **Dashboard** > Cost |
| Teve algum erro? | **Traces** > filtrar `level: ERROR` |
| De qual ferramenta veio? | **Traces** > ver tag `User-Agent` |


---

## 4. Protecoes Automaticas

Ja estao ativas, voce nao precisa configurar nada:

### PII Masking (Presidio)

Mascara dados pessoais **antes** de enviar pro modelo:

```mermaidjs
graph LR
    IN["O que o usuario digitou<br/><small>Cliente Joao Silva<br/>CPF 123.456.789-00<br/>email joao@gmail.com</small>"]
    
    PR["Presidio<br/><small>Detecta e mascara</small>"]
    
    OUT["O que chega no modelo<br/><small>Cliente PERSON<br/>CPF BR_CPF<br/>email EMAIL_ADDRESS</small>"]

    IN --> PR --> OUT

    style PR fill:#e63946,color:#fff
```

| Dado | Fica como |
|----|----|
| Nome de pessoa | `<PERSON>` |
| Email | `<EMAIL_ADDRESS>` |
| Telefone | `<PHONE_NUMBER>` |
| Cartao de credito | `<CREDIT_CARD>` |
| CPF | `<BR_CPF>` |
| CNPJ | `<BR_CNPJ>` |

### Deteccao de Secrets (hide-secrets)

Detecta e bloqueia credenciais coladas no prompt: AWS keys, GitHub tokens, Stripe keys, senhas de banco, chaves privadas.


---

## 5. Modelos Disponiveis

| Modelo | Melhor pra |
|----|----|
| **MiniMax M2.7** (padrao) | Codigo, raciocinio, agentes |
| **MiniMax M2.5** | Chat rapido, classificacao |
| **Gemini 2.5 Flash** | Documentos longos, dados sensiveis (Google/compliance) |

Fallbacks automaticos (DeepSeek, GLM, Qwen, Kimi) entram se o principal cair.


---

## 6. Login Admin

| Campo | Valor |
|----|----|
| URL | [hub.seazone.dev/ui](https://hub.seazone.dev/ui) |
| Username | `admin` |
| Password | Valor da env var `UI_PASSWORD` no Railway |

Ou use **Login with SSO** se sua conta Google ja tem role `proxy_admin`.


---

## 7. Se Algo Der Errado

| Problema | O que fazer |
|----|----|
| Alguem nao consegue acessar | Crie a key manualmente em [hub.seazone.dev/ui](https://hub.seazone.dev/ui) > Virtual Keys |
| Modelo respondendo errado/vazio | Trocar pra outro modelo. M2.5 e mais estavel pra chat |
| Gasto alto inesperado | [Langfuse](https://cloud.langfuse.com) > ver quem consumiu. Reduza budget da key |
| hub.seazone.dev fora do ar | [Railway dashboard](https://railway.com) — pode ser deploy em andamento |
| "Model not allowed" | Edite a key e adicione o modelo |
| SSO limite atingido (5 users) | Crie keys manuais — nao tem limite |

**Problemas complexos**: abra issue em [seazone-tech/llm-hub](https://github.com/seazone-tech/llm-hub).


---

## Links Rapidos

| O que | Link |
|----|----|
| **Admin LiteLLM** | [hub.seazone.dev/ui](https://hub.seazone.dev/ui) |
| **Langfuse** | [cloud.langfuse.com](https://cloud.langfuse.com) |
| Guia de Uso (devs) | [Ver guia](/doc/guia-de-uso-seazone-ai-hub-litellm-EjPZKrqBbX) |
| Politica de IA | [Ver politica](/doc/politica-de-uso-de-ia-seazone-vYpId6f8Es) |
| Governanca | [Ver governanca](/doc/governanca-de-ia-padroes-e-processos-5WottySYWA) |
| Repo | [seazone-tech/llm-hub](https://github.com/seazone-tech/llm-hub) |