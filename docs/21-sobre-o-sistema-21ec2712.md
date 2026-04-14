<!-- title: 2.1 - Sobre o Sistema | url: https://outline.seazone.com.br/doc/21-sobre-o-sistema-xV4c2WMBXn | area: Tecnologia -->

# 2.1 - Sobre o Sistema

> **Entenda como funciona o sistema completo de captura e qualificação de leads do Marketplace**


---

## Visão Geral

O sistema automatiza todo o processo desde a captura do lead no Facebook até o envio para RD Station e MIA (WhatsApp) para leads MQL investidores.

```mermaidjs
flowchart TD
    A["📱 Facebook Lead Ads<br/>(Formulário)"]
    B["🔗 Webhook n8n<br/><i>Todos os formulários chegam aqui</i>"]
    B1["🔍 Verifica Duplicidade<br/><i>Lead já existe?</i>"]
    C["🗄️ Baserow (DB 332)<br/>Marketplace<br/><i>Busca configurações</i>"]
    D["⚙️ Processamento Automático"]
    D1["✓ Extrai empreendimento do ad_name"]
    D2["✓ Valida dados"]
    D3["✓ Qualifica MQL"]
    D4["✓ Envia para integrações"]
    
    A --> B
    B --> B1
    B1 -->|Novo| C
    B1 -->|Duplicado| E["❌ Descarta"]
    C --> D
    D --> D1
    D1 --> D2
    D2 --> D3
    D3 --> D4
    
    style A fill:#1877f2,stroke:#0a4d99,stroke-width:3px,color:#fff
    style B fill:#ff6b35,stroke:#c44920,stroke-width:3px,color:#fff
    style B1 fill:#ef4444,stroke:#dc2626,stroke-width:2px,color:#fff
    style C fill:#4ecdc4,stroke:#2a9d8f,stroke-width:3px,color:#fff
    style D fill:#95e1d3,stroke:#5cb8a8,stroke-width:3px,color:#000
    style D1 fill:#e8f5e9,stroke:#66bb6a,stroke-width:2px,color:#000
    style D2 fill:#e8f5e9,stroke:#66bb6a,stroke-width:2px,color:#000
    style D3 fill:#e8f5e9,stroke:#66bb6a,stroke-width:2px,color:#000
    style D4 fill:#e8f5e9,stroke:#66bb6a,stroke-width:2px,color:#000
    style E fill:#6b7280,stroke:#4b5563,stroke-width:2px,color:#fff
```

```mermaidjs

flowchart TD
    A["📱 Facebook Lead Ads<br/>(Formulário)"]
    B["🔗 Webhook n8n<br/><i>Todos os formulários chegam aqui</i>"]
    B1["🔍 Verifica Duplicidade<br/><i>Lead já existe?</i>"]
    C["🗄️ Baserow (DB 332)<br/>Marketplace<br/><i>Busca configurações</i>"]
    D["⚙️ Processamento Automático"]
    D1["✓ Extrai empreendimento do ad_name"]
    D2["✓ Valida dados"]
    D3["✓ Qualifica MQL"]
    D4["✓ Envia para integrações"]
    
    A --> B
    B --> B1
    B1 -->|Novo| C
    B1 -->|Duplicado| E["❌ Descarta"]
    C --> D
    D --> D1
    D1 --> D2
    D2 --> D3
    D3 --> D4
    
    style A fill:#1877f2,stroke:#0a4d99,stroke-width:3px,color:#fff
    style B fill:#ff6b35,stroke:#c44920,stroke-width:3px,color:#fff
    style B1 fill:#ef4444,stroke:#dc2626,stroke-width:2px,color:#fff
    style C fill:#4ecdc4,stroke:#2a9d8f,stroke-width:3px,color:#fff
    style D fill:#95e1d3,stroke:#5cb8a8,stroke-width:3px,color:#000
    style D1 fill:#e8f5e9,stroke:#66bb6a,stroke-width:2px,color:#000
    style D2 fill:#e8f5e9,stroke:#66bb6a,stroke-width:2px,color:#000
    style D3 fill:#e8f5e9,stroke:#66bb6a,stroke-width:2px,color:#000
    style D4 fill:#e8f5e9,stroke:#66bb6a,stroke-width:2px,color:#000
    style E fill:#6b7280,stroke:#4b5563,stroke-width:2px,color:#fff
```


---

## Como Funciona

### 1️⃣ Captura

Usuário preenche formulário no Facebook Lead Ads

### 2️⃣ Recebimento

Webhook n8n recebe os dados automaticamente

### 3️⃣ Verificação de Duplicidade

Sistema verifica se o lead já foi processado anteriormente

* ✅ **Novo:** Continua processamento
* ❌ **Duplicado:** Descarta e encerra

### 4️⃣ Extração do Empreendimento

Sistema extrai o nome do empreendimento automaticamente do **ad_name** do Facebook

### 5️⃣ Configuração

Sistema busca as regras do empreendimento no Baserow (database 332)

### 6️⃣ Validação

Valida dados obrigatórios e qualifica como MQL ou não-MQL

### 7️⃣ Distribuição

Envia para as integrações apropriadas:

* ✅ **Sempre:** RD Station + Slack
* ✅ **Se MQL Investidor:** MIA (WhatsApp)


---

## Estrutura do Baserow

O Baserow (database 332) é o "cérebro" do sistema. Ele contém as tabelas principais:

| Tabela | Função | Você Edita? |
|----|----|----|
| **Empreendimentos** | Define regras de qualificação MQL | ✅ Sim |
| **Formulários** | Conecta Form IDs aos empreendimentos | ✅ Sim |
| **Hunters** | Lista de hunters por região | ⚠️ Raramente |
| **Leads** | Histórico de leads processados | ❌ Não (automático) |


---

## Tipos de Lead

### 👨‍💼 Investidor MQL

**Critérios:** Atende TODAS as regras configuradas (Intenção + Valor)

**Ações:**

* ✅ Enviado para RD Station
* ✅ Enviado para MIA (WhatsApp)


---

### 👨‍💼 Investidor Não-MQL

**Critérios:** Falha em pelo menos 1 regra configurada

**Ações:**

* ✅ Enviado para RD Station
* ❌ NÃO enviado para MIA


---

### 🏢 Corretor

**Critérios:** Marcou "Sim" em "É corretor de imóveis?"

**Ações:**

* ✅ Enviado para RD Station
* ❌ NÃO enviado para MIA


---

## Tecnologias Utilizadas

* **Facebook Lead Ads:** Captura de leads
* **n8n:** Automação de workflows
* **Baserow (DB 332):** Banco de dados e configurações
* **RD Station:** CRM e nutrição de leads
* **MIA:** Envio de mensagens no WhatsApp (apenas MQL investidor)
* **Slack:** Notificações e alertas


---

## Monitoramento

O sistema envia notificações automáticas para:

**Canal de Erros** (#n8n-marketing):

* Falhas de processamento
* Integrações indisponíveis
* Dados inválidos
* Nomenclatura de ad_name incorreta
* Leads duplicados

**Canal de Notificações:**

* Leads MQL processados com sucesso
* Leads Non-MQL processados com sucesso


---

## 🎯 Diferenciais do Sistema

**✅ Verificação de Duplicidade**\nFacebook pode enviar webhooks duplicados. O sistema identifica e descarta leads já processados automaticamente.

**✅ Extração Automática**\nO nome do empreendimento é extraído do ad_name, eliminando erros de digitação no formulário.

**✅ Processamento Rápido**\nLeads são processados em 30-60 segundos após o preenchimento do formulário.


---

## 📝 Nota Importante

> **Você NÃO precisa mexer no n8n ou código!**\nTudo é configurado através do Baserow.
>
> **MAS você PRECISA garantir que os ad_names sigam o padrão correto:**\n`[TAG1] [TAG2] NomeDoEmpreendimento_Complemento`


---

## 🔗 Links Relacionados

* [← Voltar ao guia rápido](https://outline.seazone.com.br/doc/02-como-utilizar-ffCnjThwo0)
* [Como criar campanhas no Facebook →](https://outline.seazone.com.br/doc/22-como-criar-campanhas-VxQ1IQMvMi)
* [Entender regras MQL →](https://outline.seazone.com.br/doc/23-entendendo-as-regras-mql-HuoVnk9Bi5)
* [FAQ →](https://outline.seazone.com.br/doc/25-faq-e-referencias-uKBMtu2hKw)


---

**Versão:** 1.0\n**Última atualização:** 10/11/2025\n**Elaborado para:** Equipe de Marketing SZI - Marketplace