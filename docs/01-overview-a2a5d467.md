<!-- title: 01 - Overview | url: https://outline.seazone.com.br/doc/01-overview-ia3gNU1p7M | area: Tecnologia -->

# 01 - Overview

## Introdução

Este documento apresenta o fluxo automatizado de captura, qualificação e processamento de leads do **Marketplace** gerados por Facebook Ads para a Seazone Investimentos (SZI). A solução utiliza uma arquitetura unificada, parametrizável e escalável no n8n, com webhook único que processa todos os formulários de forma centralizada.

## Contexto de Negócio

O SZI captura leads de Facebook Lead Ads para empreendimentos imobiliários do portfólio Marketplace, segmentando automaticamente entre dois perfis distintos:

* **Investidores**: Pessoas interessadas em adquirir imóveis para investimento, buscando renda passiva através de aluguel ou valorização do patrimônio
* **Corretores/Parceiros**: Profissionais do mercado imobiliário interessados em parcerias comerciais com a Seazone

Os leads são automaticamente qualificados utilizando critérios de MQL (Marketing Qualified Lead) baseados em regras de negócio pré-definidas. Após a qualificação, são enviados para RD Station para tracking de conversão. Investidores MQL e todos os corretores são direcionados para a IA de vendas MIA via WhatsApp.

**Database:** 332 (Marketplace) | **Page ID:** 842763402253490

## Visão Macro do Fluxo

```mermaidjs
flowchart TD
    A([Facebook Lead Ads<br/>Webhook Único])
    B{Lead já existe?}
    C[GET Lead<br/>Valida e Normaliza<br/>Extrai Empreendimento]
    D[GET Config<br/>Busca no Baserow]
    E{Switch<br/>Segmento}
    F[Investor Journey<br/>RD + Avaliar MQL + MIA]
    G[Broker Journey<br/>RD + MIA]
    H[Create Lead Baserow]
    I[Notificação Slack]
    K[Old Lead<br/>Encerra]
    
    A --> B
    B -->|Sim| K
    B -->|Não| C --> D --> E
    E -->|Investidor| F --> H
    E -->|Corretor| G --> H
    H --> I
    
    style A fill:#6366F1,stroke:#4338CA,stroke-width:2px,color:#fff
    style B fill:#EF4444,stroke:#DC2626,stroke-width:2px,color:#fff
    style C fill:#EC4899,stroke:#DB2777,stroke-width:2px,color:#fff
    style D fill:#0EA5E9,stroke:#0284C7,stroke-width:2px,color:#fff
    style E fill:#F59E0B,stroke:#D97706,stroke-width:2px,color:#fff
    style F fill:#10B981,stroke:#059669,stroke-width:2px,color:#fff
    style G fill:#7C3AED,stroke:#5B21B6,stroke-width:2px,color:#fff
    style H fill:#3B82F6,stroke:#1D4ED8,stroke-width:2px,color:#fff
    style I fill:#EC4899,stroke:#DB2777,stroke-width:2px,color:#fff
    style K fill:#6B7280,stroke:#4B5563,stroke-width:2px,color:#fff
```

## Etapas do Fluxo

### 1. Captura e Verificação de Duplicidade

**Webhook Único:** Todos os formulários do Marketplace convergem para um único webhook no n8n.

**Verificação:** Sistema verifica se o `leadgen_id` já existe no Baserow (database 332):

* Se existe: descarta e encerra
* Se não existe: continua processamento

**Motivo:** Facebook pode enviar webhooks duplicados. Esta verificação garante processamento único.

### 2. Validação e Normalização

**SUB-WORKFLOW:** `[SUB] [MARKETPLACE] GET Leadgen_id`

O sistema processa os dados do lead:

* Normaliza telefone para formato E.164
* Valida DDDs brasileiros
* Mapeia campos do formulário
* Determina segmento (investidor/corretor)
* Extrai empreendimento do `ad_name`

#### Extração do Empreendimento

O nome do empreendimento é extraído automaticamente do `ad_name`:

**Padrão esperado:**

```
[TAG1] [TAG2] prefixo_NomeDoEmpreendimento_data
```

**Exemplo:**

```
[AD 2] [VÍDEO] swot_Santinho Spot Teste_03/11/2025
                prefixo_↑ NOME EXTRAÍDO ↑
```

**Lógica:**

```javascript
// Remove tags e divide por underscore
const parts = adName.replace(/^\[.*?\]\s*\[.*?\]\s*/, '').split('_');
const spot = parts[1].trim(); // Pega segunda parte
```

**Importante:** Se o ad_name não seguir o padrão, o empreendimento não será identificado e o lead não será processado.

**Campos do Formulário:**

```javascript
{
  "nome_completo": "string",
  "email": "string",
  "telefone": "string",
  "você_é_corretor_de_imóveis?": "Sim/Não",
  
  // Para investidores:
  "você_procura_investimento_ou_para_uso_próprio?": "string",
  "qual_o_valor_de_entrada_que_você_tem_hoje?": "string",
  
  // Para corretores:
  "região_de_atuação": "string"
}
```

### 3. Carregamento de Configuração

**SUB-WORKFLOW:** `[SUB] Get Config`

Busca configurações no Baserow (database 332, tabela Empreendimentos):

* Regras MQL (intenções válidas + valores de entrada válidos)
* Configs RD Station (source, medium, event)
* Configs MIA (instance ID, product ID, message template para investidor e corretor)
* Canal Slack para notificações

**Filtro:** Apenas empreendimentos com Status = "Ativo" são processados.

### 4. Segmentação e Roteamento

Com base na resposta "você é corretor de imóveis?":

* **Investidor:** Avalia MQL → envia RD Station → envia MIA se MQL
* **Corretor:** Envia RD Station → envia MIA (sempre)

### 5. Jornada do Investidor

**SUB-WORKFLOW:** `[SUB] Investidor`

**Fluxo:**

```mermaidjs
flowchart LR
    A([Lead<br/>Investidor])
    B[RD Station]
    C{Avaliar<br/>MQL}
    D[Enviar<br/>para MIA]
    E[Slack<br/>MQL]
    F[Slack<br/>Non-MQL]
    G[Status]
    
    A --> B --> C
    C -->|É MQL| D
    C -->|É MQL| E
    C -->|Não MQL| F
    D --> G
    E --> G
    F --> G
    
    style A fill:#6366F1,stroke:#4338CA,stroke-width:2px,color:#fff
    style B fill:#FF6B35,stroke:#C44D30,stroke-width:2px,color:#fff
    style C fill:#F59E0B,stroke:#D97706,stroke-width:2px,color:#fff
    style D fill:#8B5CF6,stroke:#6D28D9,stroke-width:2px,color:#fff
    style E fill:#10B981,stroke:#059669,stroke-width:2px,color:#fff
    style F fill:#EF4444,stroke:#DC2626,stroke-width:2px,color:#fff
    style G fill:#10B981,stroke:#059669,stroke-width:2px,color:#fff
```


1. Calculate MQL (2 dimensões: intenção + valor de entrada)
2. POST RD Station (sempre)
3. If MQL → POST MIA (com special instructions)
4. If error → notifica Slack
5. Create Lead Baserow

**Special Instructions MIA:**

```json
{
  "specialInstructions": "Perguntas qualificadoras já preenchidas:
    1- Você procura investimento ou para uso próprio? R: [resposta]
    2- Qual o valor de entrada que você tem hoje? R: [resposta]"
}
```

**Campos salvos no Baserow:**

* Status telefone: valid/invalid
* MQL Status: unqualified (fixo no momento da criação)
* RD Status: success/failure
* MIA Status: success/failure/not_applicable

### 6. Jornada do Corretor

**SUB-WORKFLOW:** `[SUB] Corretor`

**Fluxo:**

```mermaidjs
flowchart LR
    A([Lead<br/>Corretor])
    B[RD Station]
    C[MIA<br/>sempre]
    D[Status]
    
    A --> B --> C --> D
    
    style A fill:#6366F1,stroke:#4338CA,stroke-width:2px,color:#fff
    style B fill:#FF6B35,stroke:#C44D30,stroke-width:2px,color:#fff
    style C fill:#8B5CF6,stroke:#6D28D9,stroke-width:2px,color:#fff
    style D fill:#10B981,stroke:#059669,stroke-width:2px,color:#fff
```


1. POST RD Station (sempre)
2. POST MIA (sempre, sem gate MQL)
3. If error → notifica Slack
4. Create Lead Baserow

**Diferença do Investidor:** Corretor não passa por avaliação MQL e sempre vai para MIA.

### 7. Armazenamento

Dados salvos na tabela Leads (database 332):

```javascript
{
  "Lead Ads ID": "string",
  "Data de Criação": "datetime",
  "Nome": "string",
  "Email": "string",
  "Telefone": "string",
  "Telefone Status": "valid/invalid",
  "Segmento": "Investidor/Corretor",
  "Intenção": "string",
  "Valor Entrada": "string",
  "Região": "string", // apenas corretor
  "MQL Status": "unqualified",
  "RD Status": "success/failure",
  "MIA Status": "success/failure/not_applicable",
  "Nome do Empreendimento": "string",
  "Campaign ID": "string",
  "Campaign Name": "string",
  "Ad ID": "string",
  "Form ID": "string",
  "Plataforma": "string",
  "Tráfego Orgânico": boolean,
  "Page ID": "842763402253490"
}
```

### 8. Notificações

**Error Handling:** Sistema detecta falhas específicas em RD Station e MIA, enviando notificação Slack com:

* URL da execução no n8n
* Serviços que falharam
* Dados do lead
* Timestamp

## Ferramentas e Integrações

| Ferramenta | Função |
|----|----|
| **Baserow (DB 332)** | Banco de dados: empreendimentos, configurações e leads |
| **n8n** | Orquestração de workflows |
| **RD Station** | Marketing automation e tracking de conversões |
| **MIA** | IA de vendas via WhatsApp (investidores MQL + todos os corretores) |
| **Slack** | Notificações de erro e sucesso |
| **Facebook Lead Ads** | Captura de leads via formulários |

## Regras MQL

**Dimensões (operador AND):**


1. Intenção válida
2. Valor de entrada válido

**Valores exemplo:**

**Intenções válidas:**

* Investimento - uso esporádico
* Investimento - renda
* Investimento - valorização

**Valores de entrada válidos:**

* Acima de R$ 150.000
* R$ 80.001 a R$ 150.000
* R$ 50.001 a R$ 80.000
* R$ 30.001 a R$ 50.000

## Diferenças vs Lançamentos

| Aspecto | Marketplace | Lançamentos |
|----|----|----|
| Database ID | 332 | 253 |
| Page ID | 842763402253490 | 144663558738581 |
| Identificação Spot | Extraído do ad_name | Campo no formulário |
| Verificação duplicidade | Sim | Não |
| MIA Corretor | Sim (sempre) | Não |
| GET Config | 1 busca única | 4 buscas |
| Campos telefone | 1 campo | 3 campos |


---

**Versão:** 2.0\n**Última atualização:** 13/11/2025\n**Database:** 332 (Marketplace)