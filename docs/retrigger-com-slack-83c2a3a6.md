<!-- title: Retrigger com Slack | url: https://outline.seazone.com.br/doc/retrigger-com-slack-idbEGyyaKf | area: Tecnologia -->

# Retrigger com Slack

### Fluxo

```
Erro no Pipedrive 
  ↓
Django detecta o erro
  ↓
Django manda mensagem pro Slack com botão (Deal ID no value)
  ↓
Usuário clica no botão
  ↓
Slack chama sua API Django
  ↓
Django reexecuta o processo com aquele Deal ID
```

### Mensagem mandada pro Slack

```
# No seu Django

from slack_sdk import WebClient

def quando_da_erro_pipedrive(deal_id):
    client = WebClient(token="seu-token-slack")
    
    client.chat_postMessage(
        channel="#erros-pipedrive",
        text=f"Erro no Deal {deal_id}",
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"❌ *Erro no Deal {deal_id}*\nClique para reprocessar"
                },
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Reexecutar"},
                    "value": str(deal_id),  # Deal ID dinâmico aqui!
                    "action_id": "reexecutar_deal"
                }
            }
        ]
    )
```

### Endpoint que processa o clique de reexecução

```
# views.py

from django.views.decorators.csrf import csrf_exempt

import json

@csrf_exempt

def slack_interacao(request):
    payload = json.loads(request.POST.get('payload'))
    
    action = payload['actions'][0]
    
    if action['action_id'] == 'reexecutar_deal':
        deal_id = action['value']  # Pega o Deal ID!
        
        # Chama sua função que reprocessa
        reprocessar_deal(deal_id)
        
        return JsonResponse({"text": f"Deal {deal_id} reprocessado!"})
```


---

### Block sugerido

```javascript
[
  {
    "type": "header",
    "text": {
      "type": "plain_text",
      "text": "⚠️ Falha no Onboarding Automatizado",
      "emoji": true
    }
  },
  {
    "type": "section",
    "fields": [
      {
        "type": "mrkdwn",
        "text": "*Onboarding Record ID:*\n`365`"
      },
      {
        "type": "mrkdwn",
        "text": "*Pipedrive Deal ID:*\n`227185`"
      }
    ]
  },
  {
    "type": "section",
    "text": {
      "type": "mrkdwn",
      "text": "*Título do Deal:*\n[227185] Luciano Pereira de Freitas"
    }
  },
  {
    "type": "divider"
  },
  {
    "type": "section",
    "text": {
      "type": "mrkdwn",
      "text": "*Mensagem de erro:*\n```email: Email já cadastrado```"
    }
  },
  {
    "type": "divider"
  },
  {
    "type": "actions",
    "elements": [
      {
        "type": "button",
        "text": {
          "type": "plain_text",
          "text": "🔄 Reprocessar Deal",
          "emoji": true
        },
        "style": "primary",
        "value": "227185",
        "action_id": "reprocessar_deal"
      },
      {
        "type": "button",
        "text": {
          "type": "plain_text",
          "text": "Ver no Pipedrive",
          "emoji": true
        },
        "url": "https://app.pipedrive.com/deal/227185",
        "action_id": "ver_pipedrive"
      }
    ]
  },
  {
    "type": "context",
    "elements": [
      {
        "type": "mrkdwn",
        "text": "cc: @Gabriel Zonatto"
      }
    ]
  }
]
```

 ![Preview](/api/attachments.redirect?id=1a95e491-f504-4efb-8258-62681717247d " =428x337")


\