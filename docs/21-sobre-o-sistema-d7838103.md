<!-- title: 2.1 - Sobre o Sistema | url: https://outline.seazone.com.br/doc/21-sobre-o-sistema-7m4zlzxtKS | area: Tecnologia -->

# 2.1 - Sobre o Sistema

> Entenda como funciona o sistema completo de captura e qualificação de leads do Marketplace


---

## Visão Geral

O sistema automatiza todo o processo desde a captura do lead no Facebook até o envio para RD Station e MIA via WhatsApp.

```mermaidjs
flowchart TD
    A[Facebook Lead Ads]
    B[Webhook n8n]
    B1[Verifica Duplicidade]
    C[Baserow DB 332<br/>Busca Configurações]
    D[Processamento]
    D1[Extrai empreendimento]
    D2[Valida dados]
    D3[Qualifica MQL]
    D4[Envia integrações]
    
    A --> B --> B1
    B1 -->|Novo| C
    B1 -->|Duplicado| E[Descarta]
    C --> D
    D --> D1 --> D2 --> D3 --> D4
    
    style A fill:#1877f2,stroke:#0a4d99,stroke-width:2px,color:#fff
    style B fill:#ff6b35,stroke:#c44920,stroke-width:2px,color:#fff
    style B1 fill:#ef4444,stroke:#dc2626,stroke-width:2px,color:#fff
    style C fill:#4ecdc4,stroke:#2a9d8f,stroke-width:2px,color:#fff
    style D fill:#95e1d3,stroke:#5cb8a8,stroke-width:2px,color:#000
```


---

## Como Funciona

 ![Fluxo Main - Orquestrador](/api/attachments.redirect?id=a7f0160f-cc1f-4c51-b57a-cb8a28f889ed " =1257x405")

### 1. Captura


Usuário preenche formulário no Facebook Lead Ads

### 2. Recebimento

Webhook n8n recebe os dados automaticamente

### 3. Verificação de Duplicidade

Sistema verifica se o lead já foi processado anteriormente:

```mermaidjs
flowchart LR
    A[Webhook] --> B{Lead existe?}
    B -->|Sim| C[Descarta]
    B -->|Não| D[Continua]

    style B fill:#F59E0B,stroke:#D97706,stroke-width:2px,color:#fff
    style C fill:#6B7280,stroke:#4B5563,stroke-width:2px,color:#fff
    style D fill:#10B981,stroke:#059669,stroke-width:2px,color:#fff
```

* Novo: continua processamento
* Duplicado: descarta e encerra

**Motivo:** Facebook pode enviar webhooks duplicados.

### 4. Extração do Empreendimento

 ![Sub workflow - GetleadID](/api/attachments.redirect?id=c5a31b0a-6107-4936-b98e-8f77a8ed3e1c " =1275x270")

Sistema extrai o nome do empreendimento automaticamente do `ad_name` do Facebook

### 5. Configuração

 ![](/api/attachments.redirect?id=929e1c4b-57b5-4d2e-8adc-c09bf6453f71 " =1313x336")

Sistema busca as regras do empreendimento no Baserow (database 332)

**Filtro:** Apenas empreendimentos com Status = "Ativo" são processados.

### 6. Validação

Valida dados obrigatórios e qualifica como MQL ou não-MQL

### 7. Distribuição

Envia para as integrações apropriadas:

* Sempre: RD Station + Slack
* Se MQL Investidor: MIA (WhatsApp)
* Se Corretor: MIA (WhatsApp) - sempre, sem qualificação


---

## Estrutura do Baserow

O Baserow (database 332) contém:

| Tabela | Função | Você Edita? |
|----|----|----|
| Empreendimentos | Define regras MQL, configs de integrações e status | Sim |
| Leads | Histórico de leads processados | Não (automático) |

**Atenção:** Apenas empreendimentos com Status = "Ativo" são processados.


---

## Tipos de Lead

 ![Fluxo do Investidor - Marketplace](/api/attachments.redirect?id=e184b1d1-3510-4c79-90fc-d433c9983545 " =1581x297")

### Investidor MQL

**Critérios:** Atende todas as regras configuradas (Intenção + Valor de Entrada)

**Ações:**

* Enviado para RD Station
* Enviado para MIA (WhatsApp)
* Notificação no Slack (canal MQL)

### Investidor Não-MQL

**Critérios:** Falha em pelo menos 1 regra configurada

**Ações:**

* Enviado para RD Station
* Não enviado para MIA
* Notificação no Slack (canal Non-MQL)

### Corretor

**Critérios:** Marcou "Sim" em "É corretor de imóveis?"

**Ações:**

* Enviado para RD Station
* Sempre enviado para MIA (WhatsApp) - sem qualificação
* Notificação no Slack

**Diferença do Investidor:** Corretor não passa por avaliação MQL e sempre vai para MIA.


---

## Tecnologias Utilizadas

* **Facebook Lead Ads:** Captura de leads
* **n8n:** Automação de workflows
* **Baserow (DB 332):** Banco de dados e configurações
* **RD Station:** CRM e nutrição de leads
* **MIA:** Envio de mensagens no WhatsApp (investidores MQL + todos os corretores)
* **Slack:** Notificações e alertas

**Destaque:** MIA está profundamente integrada neste fluxo, recebendo contexto completo do lead (perguntas qualificadoras preenchidas) para personalizar o primeiro contato via WhatsApp. Investidores MQL e todos os corretores são automaticamente direcionados para a MIA.


---

## Monitoramento

**Canal Slack (#n8n-marketing-marketplace):**

* Falhas de processamento
* Integrações indisponíveis
* Dados inválidos
* Nomenclatura de ad_name incorreta
* Leads duplicados
* Leads processados com sucesso (MQL e Non-MQL)

**Baserow (tabela Leads):**

* Telefone Status: valid/invalid
* MQL Status: unqualified
* RD Status: success/failure
* MIA Status: success/failure/not_applicable


---

## Diferenciais

**Verificação de Duplicidade**\nFacebook pode enviar webhooks duplicados. O sistema identifica e descarta automaticamente.

**Extração Automática**\nNome do empreendimento é extraído do ad_name, eliminando erros de digitação no formulário.

**MIA com Contexto**\nMIA recebe perguntas qualificadoras já preenchidas, acelerando qualificação sem reperguntar.

**Processamento Rápido**\nLeads são processados em 30-60 segundos após preenchimento do formulário.


---

## Nota Importante

Você não precisa mexer no n8n ou código. Tudo é configurado através do Baserow.

**Mas você precisa garantir que os ad_names sigam o padrão correto:**

```
[TAG1] [TAG2] prefixo_NomeDoEmpreendimento_data
```

**Exemplo:** `[AD 2] [VÍDEO] swot_Santinho Spot Teste_03/11/2025`\nExtrai: "Santinho Spot Teste"


---

**Versão:** 2.0\n**Última atualização:** 13/11/2025\n**Elaborado para:** Equipe de Marketing SZI - Marketplace