<!-- title: SeaNotes - Documentação Técnica | url: https://outline.seazone.com.br/doc/seanotes-documentacao-tecnica-843uQm2NsW | area: Tecnologia -->

# SeaNotes - Documentação Técnica

## Visao Geral

SeaNotes e um sistema automatizado de inteligencia de reunioes que captura transcricoes do Google Meet, gera resumos estruturados com IA (Google Gemini) e entrega os resultados via Email e/ou Slack para os participantes.

O sistema e composto por duas camadas:

* **Frontend** — Aplicacao web (Lovable) onde o usuario configura suas preferencias
* **Backend** — Pipeline event-driven que processa transcricoes automaticamente via Cloud Functions, n8n e APIs do Google

**Repositorio:** [github.com/seazone-tech/seanotes](https://github.com/seazone-tech/seanotes/tree/main)


---

## Arquitetura Geral

```mermaidjs

graph TB
    subgraph Frontend["Frontend (Lovable)"]
        APP[Aplicacao Web SeaNotes]
    end

    subgraph Storage["Armazenamento de Config"]
        SHEETS[(Google Sheets<br/>SeanotesDB)]
    end

    subgraph Backend["Backend (Event-Driven)"]
        MEET[Google Meet<br/>Transcricao gerada]
        WSAPI[Workspace Events API]
        PUBSUB[Google Pub/Sub]
        N8N[n8n Workflow]
        CF[Cloud Function<br/>Cloud Run]
        GEMINI[Google Gemini<br/>IA]
    end

    subgraph APIs["APIs Google"]
        MEETAPI[Meet API]
        DOCSAPI[Docs API]
        ADMINAPI[Admin Directory API]
    end

    subgraph Entrega["Canais de Entrega"]
        EMAIL[Gmail]
        SLACK[Slack DM]
    end

    APP -->|Salva configuracoes| SHEETS
    MEET -->|Evento| WSAPI
    WSAPI -->|Publica| PUBSUB
    PUBSUB -->|Webhook| N8N
    N8N -->|Consulta config| SHEETS
    N8N -->|Solicita tokens| CF
    CF -->|Tokens OAuth| N8N
    N8N -->|Coleta dados| MEETAPI
    N8N -->|Le transcricao| DOCSAPI
    N8N -->|Resolve usuarios| CF
    CF -->|Consulta| ADMINAPI
    N8N -->|Envia contexto| GEMINI
    GEMINI -->|Resumo JSON| N8N
    N8N -->|Envia email| EMAIL
    N8N -->|Envia DM| SLACK
```


---

## Camada Frontend

### Stack

* Desenvolvido com **Lovable** (plataforma low-code/AI)
* Hospedado e versionado em `https://github.com/seazone-tech/seanotes`
* Conecta-se diretamente ao Google Sheets API para persistir configuracoes

### Fluxo do Frontend

```mermaidjs

sequenceDiagram
    actor User as Usuario
    participant App as SeaNotes App<br/>(Lovable)
    participant Sheets as Google Sheets<br/>(SeanotesDB)

    User->>App: Acessa o painel SeaNotes
    App->>User: Exibe tela de configuracoes
    User->>App: Define preferencias:<br/>- Canal (email/slack/ambos)<br/>- Enviar para participantes<br/>- Ativar/desativar
    App->>Sheets: Salva configuracoes<br/>na aba "Settings"
    Sheets-->>App: Confirmacao
    App->>User: Configuracoes salvas!
```

### O que o usuario configura

O frontend permite que cada usuario do dominio `seazone.com.br` gerencie suas preferencias pessoais do SeaNotes:

| Configuracao | Descricao |
|----|----|
| **Canal de entrega** | Escolhe receber resumos por Email, Slack ou ambos |
| **Enviar para participantes** | Define se os demais participantes da reuniao tambem recebem o resumo |
| **Ativar/Desativar** | Liga ou desliga o SeaNotes para o usuario |

Essas configuracoes sao salvas diretamente na planilha **SeanotesDB** (Google Sheets), que funciona como banco de dados de configuracoes do sistema.

### Estrutura da Planilha SeanotesDB

| Coluna | Tipo | Descricao |
|----|----|----|
| `email` | string | Email do usuario (`@seazone.com.br`) |
| `is_active` | boolean | Ativa ou desativa o processamento |
| `send_to_participants` | boolean | Envia resumo tambem para participantes |
| `output` | enum | Canal: `email`, `slack` ou `both` |


---

## Camada Backend

### Visao geral do pipeline

```mermaidjs

sequenceDiagram
    participant Meet as Google Meet
    participant WS as Workspace Events API
    participant PS as Pub/Sub
    participant N8N as n8n Workflow
    participant CF as Cloud Function
    participant API as Google APIs<br/>(Meet + Docs)
    participant Sheet as SeanotesDB
    participant AI as Google Gemini
    participant Out as Email / Slack

    Meet->>WS: Transcricao gerada
    WS->>PS: Publica evento
    PS->>N8N: Webhook CloudEvent
    N8N->>N8N: Parse base64, extrai userId e transcriptName
    N8N->>CF: POST /get-tokens (userId)
    CF-->>N8N: meetToken + docsToken
    N8N->>Sheet: Consulta config do usuario
    Sheet-->>N8N: is_active, output, send_to_participants

    alt Usuario ativo
        N8N->>API: GET transcript info + conference record + participants
        API-->>N8N: Dados da reuniao
        N8N->>API: GET documento de transcricao (Docs API)
        API-->>N8N: Conteudo da transcricao
        N8N->>CF: POST /resolve-users (participantIds)
        CF-->>N8N: Emails dos participantes
        N8N->>AI: Contexto completo da reuniao
        AI-->>N8N: Resumo estruturado (JSON)
        N8N->>Out: Entrega por email e/ou Slack
    else Usuario inativo
        N8N->>N8N: Processamento interrompido
    end
```


---

### Componente 1 — Subscriptions (Google Workspace Events API)

Cada usuario do dominio `seazone.com.br` possui uma subscription ativa que escuta o evento:

```
google.workspace.meet.transcript.v2.fileGenerated
```

* Eventos publicados no Pub/Sub topic: `projects/seanotes/topics/meet-events`
* TTL de **7 dias**, renovadas automaticamente a cada **6 dias** via Cloud Scheduler
* Utiliza **service account impersonation** para criar subscriptions em nome de cada usuario

```mermaidjs

graph LR
    CS[Cloud Scheduler<br/>a cada 6 dias] -->|GET /renew| CF[Cloud Function]
    CF -->|Impersona cada usuario| SA[Service Account]
    SA -->|Cria/renova subscription| WSAPI[Workspace Events API]
    WSAPI -->|Eventos futuros| PS[Pub/Sub Topic]
```

### Componente 2 — Cloud Function (Google Cloud Run)

Camada de autenticacao e resolucao de identidades entre o n8n e as APIs do Google.

**URL:** `https://renew-meet-subscriptions-334324474030.us-central1.run.app`

| Endpoint | Metodo | Descricao |
|----|----|----|
| `/renew` | GET | Renova subscriptions de todos os usuarios. Chamado pelo Cloud Scheduler |
| `/get-tokens` | POST | Recebe `userId`, retorna tokens OAuth com escopo (Meet + Docs) |
| `/resolve-users` | POST | Recebe lista de `userIds`, retorna email e nome de cada um |

**Autenticacao:** Header `X-API-Key` (Secret Manager)

**Secrets (GCP Secret Manager):**

| Secret | Descricao |
|----|----|
| `meet-events-sa-key` | Chave da service account |
| `meet-events-user-tokens` | Tokens OAuth dos usuarios |
| `meet-events-oauth-client-id` | Client ID OAuth |
| `meet-events-oauth-client-secret` | Client Secret OAuth |
| `meet-events-api-key` | API key dos endpoints |

**Storage:** Estado das subscriptions em `gs://seanotes-meet-subscriptions/subscriptions.json`

### Componente 3 — Workflow n8n (Orquestracao)

O workflow recebe o evento do Pub/Sub via webhook e executa o pipeline completo:

| Etapa | Descricao |
|----|----|
| 1. Webhook | Recebe CloudEvent via POST `/meet-transcription` |
| 2. Parse | Decodifica base64, extrai `userId`, `transcriptName`, `conferenceRecordId` |
| 3. Tokens | Chama Cloud Function `/get-tokens` |
| 4. Config | Consulta SeanotesDB para validar usuario |
| 5. Dados | Coleta via Google Meet API e Docs API |
| 6. Participantes | Resolve IDs via Cloud Function `/resolve-users` |
| 7. IA | Envia contexto ao Gemini, recebe resumo estruturado |
| 8. Entrega | Roteia para Email, Slack ou ambos |

**Estrutura do resumo gerado pelo Gemini:**

```json
{
  "resumo": "Resumo executivo em 3-5 frases",
  "topicos_discutidos": ["Topico 1", "Topico 2"],
  "decisoes": ["Decisao 1", "Decisao 2"],
  "acoes": [
    {
      "responsavel": "Nome",
      "acao": "Descricao da acao",
      "prazo": "Data ou null"
    }
  ],
  "proximos_passos": ["Passo 1", "Passo 2"],
  "sentimento_geral": "positivo | neutro | negativo"
}
```

### Componente 4 — Entrega (Email e Slack)

```mermaidjs

graph TB
    N8N[n8n - Build Final Output] --> SW{Roteamento<br/>por canal}

    SW -->|output = email| EM[Gmail API]
    SW -->|output = slack| SL[Slack API]
    SW -->|output = both| BOTH[Ambos]

    EM --> EMAIL_OUT["Email HTML formatado<br/>Para: owner + participantes"]
    SL --> SLACK_SPLIT[Split por destinatario]
    SLACK_SPLIT --> SLACK_LOOKUP[Lookup Slack User ID]
    SLACK_LOOKUP --> SLACK_DM["DM com Slack Blocks"]

    BOTH --> EM
    BOTH --> SL
```

**Conteudo entregue:**

* Metadados da reuniao (participantes, horarios, link da transcricao)
* Resumo executivo
* Topicos discutidos
* Decisoes tomadas
* Acoes com responsavel e prazo
* Proximos passos


---

## Servicos e APIs

| Servico | Finalidade |
|----|----|
| Google Meet API | Dados da conferencia, transcricao e participantes |
| Google Docs API | Conteudo do documento de transcricao |
| Google Workspace Events API | Subscriptions de eventos de transcricao |
| Google Admin Directory API | Listar e resolver usuarios do dominio |
| Google Gemini API | Sumarizacao inteligente (via LangChain) |
| Gmail API | Envio de emails formatados |
| Slack API | Envio de mensagens diretas |
| Google Pub/Sub | Streaming de eventos |
| Google Cloud Storage | Persistencia do estado das subscriptions |
| Google Secret Manager | Armazenamento seguro de credenciais |
| Google Cloud Scheduler | Trigger periodico para renovacao |
| Google Sheets API | Configuracoes de usuarios (SeanotesDB) |
| n8n | Orquestracao do workflow |


---

## Infraestrutura

| Recurso | Valor |
|----|----|
| GCP Project | `seanotes` |
| Cloud Run | `renew-meet-subscriptions` (us-central1) |
| Pub/Sub Topic | `projects/seanotes/topics/meet-events` |
| GCS Bucket | `seanotes-meet-subscriptions` |
| Cloud Scheduler | Executa `/renew` a cada 6 dias |
| n8n | Instancia self-hosted com webhook exposto |
| Google Sheets | Planilha "SeanotesDB" |
| Frontend | Lovable — repo `seazone-tech/seanotes` |


---

## Troubleshooting

| Problema | O que verificar |
|----|----|
| Usuario nao recebe resumo | `is_active = true` na SeanotesDB |
| Resumo nao chega para participantes | `send_to_participants = true` na SeanotesDB |
| Subscription expirou | Logs do Cloud Scheduler e endpoint `/renew` |
| Erro de token | Secrets no Secret Manager e validade dos tokens |
| Webhook nao dispara | Pub/Sub topic ativo e webhook do n8n acessivel |
| Erro no Gemini | Logs do n8n no no de sumarizacao e quota da API |
| Config nao salva pelo frontend | Verificar conexao do Lovable com Google Sheets API |


## Workflow N8N


[[Main] - SeaNotes.json 45034](/api/attachments.redirect?id=ca5273b6-d401-488a-b6b3-5fa1386ea767)