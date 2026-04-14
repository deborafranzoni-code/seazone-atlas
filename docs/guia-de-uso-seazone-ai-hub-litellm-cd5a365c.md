<!-- title: Guia de Uso — Seazone AI Hub (LiteLLM) | url: https://outline.seazone.com.br/doc/guia-de-uso-seazone-ai-hub-litellm-EjPZKrqBbX | area: Tecnologia -->

# Guia de Uso — Seazone AI Hub (LiteLLM)

## O que e o Hub?

O **Seazone AI Hub** ([hub.seazone.dev](https://hub.seazone.dev)) e o gateway centralizado de IA da Seazone. Toda interacao com modelos de IA passa por ele — seja via terminal, IDE, agente ou API.

```mermaidjs
graph LR
    VC["Voce + sua key"] --> HUB["hub.seazone.dev"]
    HUB --> M["Modelos de IA<br/><small>MiniMax, Gemini, DeepSeek, etc.</small>"]

    style HUB fill:#2d6a4f,color:#fff
```


---

## 1. Como Conseguir Seu Acesso

### Opcao 1: Self-service (recomendado)


1. Acesse [hub.seazone.dev/ui](https://hub.seazone.dev/ui)
2. Clique em **Login with SSO** (use sua conta Google `@seazone.com.br`)
3. Va em **API Keys** e crie sua key

```mermaidjs
graph LR
    A["Acessa<br/>hub.seazone.dev/ui"] --> B["Login with SSO<br/>(Google @seazone)"]
    B --> C["API Keys ><br/>Create Key"]
    C --> D["Copia sua key<br/>sk-sz-..."]
    D --> E["Configura na<br/>ferramenta"]

    style B fill:#2d6a4f,color:#fff
```

### Opcao 2: Se nao conseguir fazer login

Solicite sua key ao administrador da plataforma. Ele cria pra voce e te envia.

### O que vem com sua key

* **Budget mensal** — limite de uso
* **Modelos**: minimax-m2.7, minimax-m2.5, gemini-2.5-flash
* **Rastreamento** individual pra governanca

**Guarde sua key** — e pessoal e intransferivel.


---

## 2. Como Usar

O hub e **100% compativel com a API da OpenAI**. Basta apontar qualquer ferramenta ou SDK pra:

| Campo | Valor |
|----|----|
| **Base URL** | `https://hub.seazone.dev/v1` |
| **API Key** | Sua virtual key (`sk-sz-...`) |
| **Modelo** | `minimax-m2.7` (padrao) |

### Teste rapido (terminal)

```bash
curl https://hub.seazone.dev/v1/chat/completions \
  -H "Authorization: Bearer sk-sz-SUA-KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"minimax-m2.7","messages":[{"role":"user","content":"oi"}]}'
```

### Python (SDK OpenAI)

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://hub.seazone.dev/v1",
    api_key="sk-sz-SUA-KEY"
)

response = client.chat.completions.create(
    model="minimax-m2.7",
    messages=[{"role": "user", "content": "Explique o que e uma API REST"}]
)

print(response.choices[0].message.content)
```

### Node.js (SDK OpenAI)

```javascript
import OpenAI from 'openai';

const client = new OpenAI({
  baseURL: 'https://hub.seazone.dev/v1',
  apiKey: 'sk-sz-SUA-KEY'
});

const response = await client.chat.completions.create({
  model: 'minimax-m2.7',
  messages: [{ role: 'user', content: 'Explique o que e uma API REST' }]
});

console.log(response.choices[0].message.content);
```

### Streaming

```python
stream = client.chat.completions.create(
    model="minimax-m2.7",
    messages=[{"role": "user", "content": "Conte uma historia curta"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

### Structured Output (JSON)

```python
response = client.chat.completions.create(
    model="minimax-m2.7",
    messages=[{"role": "user", "content": "Liste 3 linguagens de programacao"}],
    response_format={"type": "json_object"}
)
```


---

## 3. Modelos Disponiveis

| Modelo | Forte em | Contexto |
|----|----|----|
| **minimax-m2.7** (padrao) | Coding, raciocinio, tool use | 204K tokens |
| **minimax-m2.5** | Chat rapido, classificacao, sumarizacao | 1M tokens |
| **gemini-2.5-flash** | Documentos longos, compliance, multimodal | 1M tokens |

Alem desses, existem modelos de fallback (DeepSeek, GLM, Qwen, Kimi) — se o principal estiver fora, o hub troca automaticamente.

### Listar todos os modelos

```bash
curl https://hub.seazone.dev/v1/models \
  -H "Authorization: Bearer sk-sz-SUA-KEY"
```

### Escolher modelo por tarefa

```mermaidjs
graph TD
    Q["O que voce precisa?"]
    Q -->|"Codigo, agente,<br/>raciocinio complexo"| M27["minimax-m2.7"]
    Q -->|"Chat rapido,<br/>classificacao,<br/>autocomplete"| M25["minimax-m2.5"]
    Q -->|"Documento enorme,<br/>contexto longo,<br/>dados sensiveis"| GF["gemini-2.5-flash<br/><small>1M tokens de contexto</small>"]

    style M27 fill:#2d6a4f,color:#fff
    style Q fill:#1a1a2e,color:#fff
```


---

## 4. Verificar Seu Uso

No painel [hub.seazone.dev/ui](https://hub.seazone.dev/ui) voce ve suas keys, uso e budget restante.

Ou via terminal:

```bash
curl -sv https://hub.seazone.dev/v1/chat/completions \
  -H "Authorization: Bearer sk-sz-SUA-KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"minimax-m2.7","messages":[{"role":"user","content":"oi"}],"max_tokens":5}' \
  2>&1 | grep x-litellm-key
```

Retorna:

* `x-litellm-key-spend` — quanto voce ja usou
* `x-litellm-key-max-budget` — seu limite


---

## 5. Protecoes Ativas

O hub protege seus requests automaticamente:

| Protecao | O que faz |
|----|----|
| **PII Masking** | Mascara nomes, CPF, CNPJ, emails e telefones antes de enviar pro modelo |
| **Secrets Detection** | Detecta e bloqueia AWS keys, GitHub tokens, senhas de banco no prompt |
| **Budget** | Limita seu uso mensal |
| **Fallback** | Se o modelo principal cair, troca automaticamente pra outro |


---

## 6. Integracoes Sugeridas

O hub funciona com **qualquer ferramenta compativel com a API da OpenAI**. Algumas que ja validamos:

### OpenClaude (coding agent no terminal)

Fork do Claude Code com suporte a multiplos modelos. Mesmas ferramentas (Read, Edit, Bash, Grep).

```bash
# Instalar
npm install -g @gitlawb/openclaude
ln -sf ~/.npm-global/lib/node_modules/@gitlawb/openclaude/bin/openclaude ~/.local/bin/openclaude

# Configurar (~/.bashrc ou ~/.zshrc)
export CLAUDE_CODE_USE_OPENAI=1
export OPENAI_API_KEY="sk-sz-SUA-KEY"
export OPENAI_BASE_URL="https://hub.seazone.dev/v1"
export OPENAI_MODEL="minimax-m2.7"

# Usar
openclaude
```

### Continue.dev (IA no VS Code / JetBrains)

Extensao com chat (`Ctrl+L`), inline edit (`Ctrl+I`) e tab autocomplete.

```bash
code --install-extension continue.continue
```

Configurar `~/.continue/config.yaml`:

```yaml
name: Seazone AI Hub
version: 1.0.0
schema: v1
models:
  - name: MiniMax M2.7
    provider: openai
    model: minimax-m2.7
    apiBase: https://hub.seazone.dev/v1
    apiKey: sk-sz-SUA-KEY
    roles: [chat, edit]
tabAutocomplete:
  - name: MiniMax M2.5
    provider: openai
    model: minimax-m2.5
    apiBase: https://hub.seazone.dev/v1
    apiKey: sk-sz-SUA-KEY
```

### OpenClaw (agentes corporativos)

Agentes como Garra e Sherlog ja estao integrados ao hub. Se voce desenvolve agentes com OpenClaw:

```json
{
  "provider": {
    "type": "openai-compatible",
    "baseUrl": "https://hub.seazone.dev/v1",
    "apiKey": "sk-sz-SUA-KEY"
  }
}
```

### Qualquer outro SDK ou ferramenta

Se aceita `base_url` e `api_key` no formato OpenAI, basta apontar pra `https://hub.seazone.dev/v1` com sua key. Funciona com LangChain, LlamaIndex, Vercel AI SDK, etc.


---

## Troubleshooting

| Problema | Solucao |
|----|----|
| SSO nao funciona / limite atingido | Solicite sua key ao administrador da plataforma |
| Erro 401 | Key errada, expirada ou sem budget. Crie nova em [hub.seazone.dev/ui](https://hub.seazone.dev/ui) ou solicite ao admin |
| Erro "model not allowed" | Sua key nao tem acesso a esse modelo. Solicite ao admin |
| Resposta vazia | Alguns modelos usam reasoning tokens — tente `minimax-m2.5` |
| Timeout | Requests longos podem levar ate 60s. Tente um modelo mais leve |
| `openclaude: command not found` | `ln -sf ~/.npm-global/lib/node_modules/@gitlawb/openclaude/bin/openclaude ~/.local/bin/openclaude` |


---

## Links

| O que | Link |
|----|----|
| Hub (painel) | [hub.seazone.dev/ui](https://hub.seazone.dev/ui) |
| Hub (API) | [hub.seazone.dev](https://hub.seazone.dev) |
| Politica de IA | [Ver politica](/doc/politica-de-uso-de-ia-seazone-vYpId6f8Es) |
| Governanca | [Ver governanca](/doc/governanca-de-ia-padroes-e-processos-5WottySYWA) |
| Repo | [seazone-tech/llm-hub](https://github.com/seazone-tech/llm-hub) |