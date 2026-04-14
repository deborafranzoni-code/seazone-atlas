<!-- title: Configurar Webhooks no OpenClaw (EC2) | url: https://outline.seazone.com.br/doc/configurar-webhooks-no-openclaw-ec2-f5fuauqdVl | area: Tecnologia -->

# Configurar Webhooks no OpenClaw (EC2)

> Webhooks permitem que serviços externos (GitHub Actions, Pipefy, Slack, CI/CD, etc.) enviem eventos para o OpenClaw, que roteia para o agente correto e executa uma ação automaticamente.
>
> **Endpoint:** `https://garra.seazone.com.br/hooks` **Autenticação:** `Authorization: Bearer <token>` (token no [Vault](https://vault.seazone.com.br/ui/vault/secrets/secret/kv/Ferramentas%2Facesso_Openclaw))


---

## Como funciona

```
Serviço externo (GitHub, Pipefy, etc.)
        │
        │  POST /hooks
        │  Authorization: Bearer <token>
        │  Body: { "source": "github-actions", "payload": {...} }
        │
        ▼
   OpenClaw Gateway
        │
        │  Compara "source" com hooks.mappings[].match.source
        │
        ▼
   Mapping encontrado
        │
        │  Roteia para o agente configurado
        │  Cria/resume sessão com sessionKey definido
        │
        ▼
   Agente processa e responde
        │
        │  Se deliver: true → envia resposta no canal configurado (Slack)
        │
        ▼
   Resposta entregue
```


---

## 1. Conectar na EC2

Siga os mesmos passos da [documentação de criação de agentes](https://outline.seazone.com.br/doc/openclaw-NZIt63TVw1):


1. Acesse o **[AWS Console](https://sa-east-1.console.aws.amazon.com/console/home?region=sa-east-1#)** (conta applications)
2. Navegue até **EC2 > Instances** → selecione `openclaw` (`i-05a410435fcca3183`)
3. **Connect** → **Session Manager** → **Connect**

Ou via terminal:

```bash
aws ssm start-session --target i-05a410435fcca3183 --region sa-east-1
```


---

## 2. Entrar no container

```bash
sudo docker exec -it openclaw-gateway sh
```


---

## 3. Entender a estrutura de um webhook

Cada webhook é um **mapping** dentro de `hooks.mappings` no `openclaw.json`. Um mapping define:

| Campo | Obrigatório | Descrição |
|----|:---:|----|
| `id` | ✅ | Identificador único do mapping (ex: `github-actions-trusted`) |
| `match.source` | ✅ | Valor do campo `source` no body do POST que aciona este mapping |
| `action` | ✅ | Sempre `"agent"` (executa um agente) |
| `agentId` | ✅ | ID do agente que vai processar o evento |
| `sessionKey` | ✅ | Chave da sessão (ex: `hook:meu-webhook`). Prefixo `hook:` obrigatório |
| `wakeMode` | ✅ | `"now"` (executa imediatamente) |
| `deliver` | ❌ | `true` = envia resposta no canal configurado |
| `channel` | ❌ | Canal de resposta (ex: `"slack"`) |
| `name` | ❌ | Nome descritivo do mapping |
| `model` | ❌ | Override de modelo para este hook (ex: `"openrouter/anthropic/claude-sonnet-4.6"`) |
| `thinking` | ❌ | Nível de reasoning: `"off"`, `"low"`, `"medium"`, `"high"` |
| `timeoutSeconds` | ❌ | Timeout em segundos (default: 300) |
| `allowUnsafeExternalContent` | ❌ | `true` = permite conteúdo externo no prompt (necessário para payloads grandes) |


---

## 4. Criar um webhook (passo a passo)

### 4.1. Escolher o agente

O agente que vai processar o webhook precisa existir. Se não existe, [crie primeiro](https://outline.seazone.com.br/doc/openclaw-NZIt63TVw1).

```bash
# Verificar agentes disponíveis
openclaw agents list
```

### 4.2. Autorizar o agente nos hooks

O agente precisa estar na lista `hooks.allowedAgentIds`. Edite o `openclaw.json`:

```bash
# Visualizar agentes autorizados
cat /home/node/.openclaw/openclaw.json | node -e "
  const d=JSON.parse(require('fs').readFileSync('/dev/stdin','utf8'));
  console.log('Agentes autorizados:', d.hooks.allowedAgentIds);
"
```

Para adicionar um agente:

```bash
node -e "
  const fs = require('fs');
  const f = '/home/node/.openclaw/openclaw.json';
  const d = JSON.parse(fs.readFileSync(f, 'utf8'));
  if (!d.hooks.allowedAgentIds.includes('meu-agente')) {
    d.hooks.allowedAgentIds.push('meu-agente');
    fs.writeFileSync(f, JSON.stringify(d, null, 2));
    console.log('Agente meu-agente autorizado nos hooks');
  } else {
    console.log('Agente já autorizado');
  }
"
```

### 4.3. Criar o mapping

```bash
node -e "
  const fs = require('fs');
  const f = '/home/node/.openclaw/openclaw.json';
  const d = JSON.parse(fs.readFileSync(f, 'utf8'));

  const novoMapping = {
    id: 'meu-webhook-id',           // ID único
    match: { source: 'meu-servico' }, // Match no body do POST
    action: 'agent',
    wakeMode: 'now',
    name: 'Meu Webhook Descritivo',
    agentId: 'meu-agente',           // Agente que processa
    sessionKey: 'hook:meu-webhook',   // Prefixo hook: obrigatório
    deliver: true,                    // Entrega resposta
    channel: 'slack',                 // Entrega via Slack
    timeoutSeconds: 300
  };

  d.hooks.mappings.push(novoMapping);
  fs.writeFileSync(f, JSON.stringify(d, null, 2));
  console.log('Mapping criado:', novoMapping.id);
"
```

### 4.4. Verificar o config

```bash
cat /home/node/.openclaw/openclaw.json | node -e "
  const d=JSON.parse(require('fs').readFileSync('/dev/stdin','utf8'));
  d.hooks.mappings.forEach(m => {
    console.log(m.id, '|', 'source:', m.match.source, '|', 'agent:', m.agentId);
  });
"
```

O OpenClaw faz **hot reload** automático — não precisa reiniciar o gateway.


---

## 5. Testar o webhook

### Via curl (de dentro do container)

```bash
# Obter o token
TOKEN=$(cat /home/node/.openclaw/openclaw.json | node -e "
  const d=JSON.parse(require('fs').readFileSync('/dev/stdin','utf8'));
  console.log(d.hooks.token);
")

# Enviar evento de teste
curl -X POST http://localhost:18789/hooks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "source": "meu-servico",
    "payload": {
      "message": "Evento de teste do webhook",
      "data": {"key": "value"}
    }
  }'
```

### Via curl (externo, pela internet)

```bash
curl -X POST https://garra.seazone.com.br/hooks \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "source": "meu-servico",
    "payload": {
      "message": "Teste externo"
    }
  }'
```

### Verificar nos logs

```bash
# Dentro do container
cat /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log | grep "hook\|webhook" | tail -10

# Ou via CloudWatch (fora do container)
aws logs tail /ec2/openclaw --since 5m --region sa-east-1 --profile apps | grep hook
```


---

## 6. Configurar o serviço externo

No serviço que vai enviar eventos, configure:

| Campo | Valor |
|----|----|
| **URL** | `https://garra.seazone.com.br/hooks` |
| **Método** | `POST` |
| **Header** | `Authorization: Bearer <token do Vault>` |
| **Header** | `Content-Type: application/json` |
| **Body** | JSON com campo `source` matching o `match.source` do mapping |

### Exemplo: GitHub Actions

No workflow `.github/workflows/meu-workflow.yml`:

```yaml
- name: Notificar OpenClaw
  run: |
    curl -X POST https://garra.seazone.com.br/hooks \
      -H "Authorization: Bearer ${{ secrets.OPENCLAW_HOOKS_TOKEN }}" \
      -H "Content-Type: application/json" \
      -d '{
        "source": "github-actions",
        "payload": {
          "repository": "${{ github.repository }}",
          "event": "${{ github.event_name }}",
          "ref": "${{ github.ref }}",
          "actor": "${{ github.actor }}",
          "run_url": "${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}"
        }
      }'
```

### Exemplo: Pipefy (Automação)

Na automação do Pipefy, configure um "Send HTTP Request":

* URL: `https://garra.seazone.com.br/hooks`
* Method: POST
* Headers: `Authorization: Bearer <token>`, `Content-Type: application/json`
* Body:

```json
{
  "source": "pipefy",
  "payload": {
    "card_id": "{{card.id}}",
    "pipe_name": "{{card.pipe.name}}",
    "phase": "{{card.current_phase.name}}",
    "title": "{{card.title}}"
  }
}
```

### Exemplo: N8N (Webhook node)

Use o node **HTTP Request**:

* Method: POST
* URL: `https://garra.seazone.com.br/hooks`
* Authentication: Header Auth → Name: `Authorization`, Value: `Bearer <token>`
* Body: JSON com `source` e `payload`


---

## 7. Webhooks ativos atualmente

| ID | Source | Agente | Descrição |
|----|----|----|----|
| `github-actions-trusted` | `github-actions` | Re-Vision | Review automático de PRs e deploys |
| `slack-thread-sherlog` | `slack` | Sherlog | Mensagens encaminhadas do Slack |
| `pipefy-dalton` | `pipefy` | Suporte BizOps (Dalton) | Card criado no pipe de suporte |


---

## 8. Opções avançadas

### Override de modelo por webhook

Para usar um modelo específico (ex: Claude para análise complexa):

```json
{
  "id": "analise-complexa",
  "match": { "source": "analise" },
  "agentId": "meu-agente",
  "model": "openrouter/anthropic/claude-sonnet-4.6",
  "thinking": "medium",
  "timeoutSeconds": 600
}
```

### Permitir conteúdo externo no prompt

Para webhooks que enviam payloads grandes (PRs, docs):

```json
{
  "allowUnsafeExternalContent": true
}
```

> ⚠️ Use com cuidado — permite que o payload externo seja injetado no prompt do agente.

### Session key personalizada

Cada webhook cria uma sessão com a `sessionKey` definida. Se quiser sessões separadas por evento:

```json
{
  "sessionKey": "hook:github-pr-{{payload.pull_request.number}}"
}
```


---

## 9. Troubleshooting

| Problema | Causa provável | Solução |
|----|----|----|
| `401 Unauthorized` | Token inválido | Verificar token no Vault e no `hooks.token` do config |
| `404 Not Found` | Path errado ou hooks desabilitado | Verificar `hooks.enabled: true` e `hooks.path: "/hooks"` |
| `No matching hook` nos logs | `source` não bate com nenhum mapping | Verificar `match.source` no config vs `source` no body |
| Agente não responde | `agentId` não está em `allowedAgentIds` | Adicionar agente na lista de permitidos |
| Timeout | Agente demora mais que `timeoutSeconds` | Aumentar timeout ou simplificar o prompt |
| Resposta não chega no Slack | `deliver: false` ou `channel` não configurado | Setar `deliver: true` e `channel: "slack"` |


---

## Referência rápida

```bash
# Listar webhooks configurados
cat /home/node/.openclaw/openclaw.json | node -e "
  const d=JSON.parse(require('fs').readFileSync('/dev/stdin','utf8'));
  d.hooks.mappings.forEach(m => console.log(m.id, '→', m.agentId, '(source:', m.match.source + ')'));
"

# Testar webhook localmente
curl -X POST http://localhost:18789/hooks \
  -H "Authorization: Bearer $(node -e \"const d=JSON.parse(require('fs').readFileSync('/home/node/.openclaw/openclaw.json','utf8')); console.log(d.hooks.token)\")" \
  -H "Content-Type: application/json" \
  -d '{"source": "meu-servico", "payload": {"test": true}}'

# Ver logs de hooks em tempo real
tail -f /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log | grep hook
```