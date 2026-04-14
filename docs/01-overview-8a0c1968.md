<!-- title: 01 - Overview | url: https://outline.seazone.com.br/doc/01-overview-eOQxGZg5pQ | area: Tecnologia -->

# 01 - Overview

# Documentação Técnica: Sistema de Automação de Leads SZI

## Introdução

Este documento apresenta o fluxo automatizado de captura, qualificação e processamento de leads gerados por Facebook Ads para a Seazone Investimentos (SZI). A solução utiliza uma arquitetura unificada, parametrizável e escalável no n8n, com webhook único que processa todos os formulários de forma centralizada.

## Contexto de Negócio

O SZI captura leads de Facebook Lead Ads para empreendimentos imobiliários, segmentando automaticamente entre dois perfis distintos:

* **Investidores**: Pessoas interessadas em adquirir imóveis para investimento, buscando renda passiva através de aluguel ou valorização do patrimônio
* **Corretores/Parceiros**: Profissionais do mercado imobiliário interessados em parcerias comerciais com a Seazone

Os leads são automaticamente qualificados utilizando critérios de MQL (Marketing Qualified Lead) baseados em regras de negócio pré-definidas. Após a qualificação, são enviados para RD Station para tracking de conversão, direcionados para a IA de vendas MIA (apenas investidores qualificados como MQL) e integrados ao Pipedrive para gestão do pipeline comercial.

## Visão Macro do Fluxo

```mermaidjs
flowchart TD
    A([📱 Facebook Lead Ads<br/>Webhook Único])
    
    B[🔄 GET Lead<br/>Validate & Normalize<br/>Telefone + Segmento]
    
    C[🔄 GET Config<br/>4 Buscas Baserow<br/>Empreend. + Forms + Stage + Hunter]
    
    D{⚡ Switch<br/>lead_segment}
    
    E[🔄 Investor Journey<br/>RD + Avaliar MQL + MIA]
    
    F[🔄 Broker Journey<br/>RD + Pipedrive Deal]
      
    G[💾 Baserow Insert/Update<br/>Tabela: Leads]
    
    H[📢 Notificação Slack<br/>Sucesso ou Erro]
    
    I[➡️ Continue<br/>Consolidar Status]
  
    
    A --> B --> C --> D
    D -->|Investidor| E --> G
    D -->|Corretor| F --> G
    G --> H --> I
    
    style A fill:#6366F1,stroke:#4338CA,stroke-width:3px,color:#fff
    style B fill:#EC4899,stroke:#DB2777,stroke-width:2px,color:#fff
    style C fill:#0EA5E9,stroke:#0284C7,stroke-width:2px,color:#fff
    style D fill:#F59E0B,stroke:#D97706,stroke-width:2px,color:#fff
    style E fill:#10B981,stroke:#059669,stroke-width:2px,color:#fff
    style F fill:#7C3AED,stroke:#5B21B6,stroke-width:2px,color:#fff
    style G fill:#3B82F6,stroke:#1D4ED8,stroke-width:2px,color:#fff
    style H fill:#EC4899,stroke:#DB2777,stroke-width:2px,color:#fff
    style I fill:#F97316,stroke:#EA580C,stroke-width:2px,color:#fff
```

O fluxo opera em etapas sequenciais bem definidas:


### **0. Organização dos fluxos**

 ![](/api/attachments.redirect?id=914f6741-176c-4d13-b82a-84337b95ae39 " =1687x513")

[Fluxos](https://workflows.seazone.com.br/projects/bl22UQN438d0cmZ5/folders/jbY6atVQH4EVFDPX/workflows) organizados em `Novo Lead Ads - Lançamento SPOT` e `utils`

### 1. Captura e Orquestração - `[MAIN] Trigger Facebook Ads`

 ![](/api/attachments.redirect?id=5d2d117a-d7df-42b4-b9da-44ef4bbbb980 " =969x282")

**Webhook Único**: Todos os formulários do Facebook Lead Ads convergem para um único webhook no n8n,  que capura esses dados e repassa para sub-workflows.

O fluxo de orquestração manipula todos os outros sub-workflows, baseando-se em divisão de responsabilidades.

### 2. Validação e Normalização

 ![](/api/attachments.redirect?id=4cf6ef51-d2a5-44a6-91c4-275f3c2f5b89 " =1421x569")

**SUB-WORKFLOW:** `**\[SUB\] Get Lead**`

O n8n captura automaticamente os dados através do webhook do Facebook Lead Ads e processa as informações:

* Normaliza o número de telefone para o formato internacional E.164 (sub-workflow `[RUN] Normalize Phone` )
* Valida DDDs brasileiros
* Mapeia campos do formulário para a estrutura padrão do sistema
* Determina o segmento do lead (investidor ou corretor)
* Identifica o empreendimento através do campo do formulário

**Campos Esperados do Formulário:**

```javascript
{
  "full_name": "Nome Completo",
  "email": "email@exemplo.com",
  "phone_number": "+5548999999999",
  "empreendimento": "Nome do Empreendimento", // Deve corresponder ao cadastrado no Baserow
  "você_é_corretor_de_imóveis?": "Sim" ou "Não",
  // Para investidores:
  "você_procura_investimento_ou_para_uso_próprio?": "Investimento - renda com aluguel",
  "qual_o_valor_total_que_você_pretende_investir_dentro_de_54_meses?": "R$ 200.001 a R$ 300.000",
  "qual_a_forma_de_pagamento?": "À vista via PIX ou boleto",
  // Para corretores:
  "região_de_atuação": "Sul"
}
```

### 3. Carregamento de Configuração

 ![](/api/attachments.redirect?id=77c5e893-ca26-406e-8c96-64e34e182fc1 " =1421x569")

**SUB-WORKFLOW:** `**\[SUB\] Get Config**`

O sistema busca as configurações necessárias no Baserow através de consultas sequenciais em 4 tabelas:

**1. Get Empreendimento** - Regras MQL + Configs RD/MIA/Slack\n**2. Get Forms** - Configurações técnicas do formulário\n**3. Get Stage Pipedrive** - Stage ID (investidor ou corretor)\n**4. GET Hunters** - Owner ID do hunter por região

### Validação

Se qualquer busca retornar vazio, o workflow para com erro: **"Formulário ou Empreendimento não foram encontrados"**

### Output

Todas as configurações são consolidadas em um único objeto pelo node `SET`

### 4. Segmentação e Roteamento

Com base na resposta do lead à pergunta "você é corretor de imóveis?", o sistema direciona automaticamente para a jornada apropriada:

* **Jornada do Investidor**: Aplica regras MQL, integra com RD Station, envia para MIA se qualificado
* **Jornada do Corretor**: Integra com RD Station, identifica hunter responsável pela região, cria deal no Pipedrive

### 5. Armazenamento e Atualização

Todos os dados são persistidos na tabela **Leads** do Baserow ao final do processamento, incluindo:

```javascript
{
  // Informações do Lead
  "Lead Ads ID": "1525680915225592",
  "Data de Criação (Ads)": "2025-10-28T20:00:37+0000",
  "Nome": "Ana Silva",
  "Email": "ana.silva@exemplo.com",
  "Telefone": "+5548999998888",
  "Telefone Inválido?": false,
  
  // Classificação
  "Segmento": "Investidor",
  "Intenção": "Investimento - renda com aluguel",
  "Investimento": "R$ 300.001 a R$ 400.000",
  "Forma de Pagamento": "À vista via PIX ou boleto",
  "Regiao": "Sudeste",
  "É MQL?": true,
  
  // Metadados da Campanha
  "Nome do Empreendimento": "Ponta das Canas Spot II",
  "ID do Formulario": "1120563570283236",
  "Nome do Formulário": "[TESTE] - [Formulário] [SZI]...",
  "ID da Campanha": "120246218009620555",
  "Nome da Campanha": "[SI] [LEAD ADS] [RS/SC/PR]...",
  
  // Origem Facebook
  "Plataforma": null,
  "Tráfego Organico": true,
  "ID do Anuncio": null,
  "ID do Grupo de Anuncio": null,
  "ID da Página": "144663558738581",
  
  // Status Integrações
  "RD Enviado?": true,
  "MIA Enviado?": true,
  "Pipedrive Deal ID": "deal_1234",
  "Pipedrive Person ID": "person_567"
}
```

### 6. Notificação de Erros

 ![](/api/attachments.redirect?id=479bc7ab-3c12-4cb7-88da-be776c2cb2e3 " =868x275")

**SUB-WORKFLOW:** `**\[ERROR\] Slack Notification**`

Todos os erros ocorridos durante qualquer execução em qualquer workflow do fluxo SZI são capturados com:

* Mensagem de erro detalhada
* Stack trace quando disponível
* Link direto para a execução no n8n
* Contexto do lead sendo processado

As notificações são enviadas para o canal configurado em `slack_channel_error`.

## Ferramentas e Integrações Utilizadas

 ![](/api/attachments.redirect?id=8c0ae9aa-e8bb-4e2c-91a6-90203631fc2b " =1920x1080")



| Ferramenta | Função |
|----|----|
| **==Baserow==** | Banco de dados no-code para armazenamento de leads, configurações de formulários, empreendimentos e regras MQL |
| **==n8n==** | Plataforma de orquestração de workflows, responsável por conectar todas as ferramentas e executar a lógica de negócio |
| **==RD Station==** | Plataforma de marketing automation para registro de conversões e nurturing de leads |
| **==Pipedrive==** | CRM para gerenciamento do pipeline de vendas e acompanhamento de deals |
| **==MIA==** | Inteligência artificial de vendas da Seazone para primeiro contato automatizado via WhatsApp com leads MQL |
| **==Slack==** | Canal de comunicação para notificações em tempo real de erros, alertas e status de processamento |
| **==Facebook Lead Ads==** | Plataforma de captura de leads através de formulários integrados aos anúncios |

## Estrutura de Dados no Baserow

O banco **SZO** no Baserow possui tabelas relacionadas ao Empreendimento (informações como ID, configurações e regras MQL), Formulário (IDs, nomes), Hunters (dados como região, hunters de tal regão), Leads (todas as informações de leads processados pelo n8n) e outras que podem ser verificadas em [https://baserow.seazone.com.br](https://baserow.seazone.com.br/database/253/table/1209/5799)

## Jornadas de Lead

### Jornada do Investidor

 ![](/api/attachments.redirect?id=1e1ed4ed-04f4-4aae-9c6f-96405d01e94f " =1404x483")

**SUB-WORKFLOW:** `**\[SUB\] Investor Journey**`

A jornada do investidor foi desenhada para maximizar a taxa de conversão através de qualificação precisa e contato rápido com leads de alta qualidade.

#### Processo de Qualificação MQL

Um lead investidor passa por avaliação automática baseada em três dimensões configuradas na tabela **Empreendimentos** do Baserow:

**Dimensões:** 

* Todas detalhadas em @[02 - Como Utilizar](mention://676aaaf3-be2a-4b75-bfb4-a811feb00c2b/document/bf033984-6915-478b-9a7a-25dbdcff1791)

**Lógica de Qualificação:**

```javascript

const is_mql = (
  mql_intencoes_validas.includes(lead.intencao) &&
  mql_faixas_investimento.includes(lead.faixa_investimento) &&
  mql_formas_pagamento.includes(lead.forma_pagamento)
);
```

O lead só é considerado MQL se passar nas três dimensões simultaneamente (operador ==AND==).

#### Fluxo de Processamento

```mermaidjs
flowchart LR
    A([🎯 Lead<br/>Investidor])
    B[📧 RD Station]
    C{🔍 Avaliar<br/>MQL}
    D[🤖 Enviar<br/>para MIA]
    E[✅ Slack<br/>MQL]
    F[⚠️ Slack<br/>Non-MQL]
    G[✅ Status]
    
    A --> B --> C
    C -->|✅ É MQL| D
    C -->|✅ É MQL| E
    C -->|❌ Não MQL| F
    D --> G
    E --> G
    F --> G
    
    style A fill:#6366F1,stroke:#4338CA,stroke-width:3px,color:#fff
    style B fill:#FF6B35,stroke:#C44D30,stroke-width:2px,color:#fff
    style C fill:#F59E0B,stroke:#D97706,stroke-width:2px,color:#fff
    style D fill:#8B5CF6,stroke:#6D28D9,stroke-width:2px,color:#fff
    style E fill:#10B981,stroke:#059669,stroke-width:2px,color:#fff
    style F fill:#EF4444,stroke:#DC2626,stroke-width:2px,color:#fff
    style G fill:#10B981,stroke:#059669,stroke-width:2px,color:#fff
```


1. **Envio para RD Station**: Todos os leads investidores (MQL ou não) têm suas conversões registradas no RD Station com os parâmetros configurados (source, medium, campaign).
2. **Avaliação MQL**: O sistema aplica as regras configuradas no Baserow para determinar se o lead é qualificado.
3. **Roteamento Condicional**:
   * **Se MQL**:
     * Envia para a MIA para contato via WhatsApp
     * Notifica canal Slack de MQLs
     * Marca flag `e_mql = true` no Baserow
   * **Se Non-MQL**:
     * Apenas notifica canal Slack de Non-MQLs
     * Marca flag `e_mql = false` no Baserow

#### Integração com MIA

 ![](/api/attachments.redirect?id=e0317152-51fe-4e67-a8b7-2cbd563b94e8 " =1261x933")

A MIA (IA de vendas da Seazone) recebe leads MQL através de API com payload estruturado:

```javascript
{
  "product_id": "ba7630e5-ada0-4ada-af51-c10e2d9baecf",
  "instance_id": "1292",
  "source": "Busca Paga | Facebook Ads",
  "message_template": "szi_canasbeach_1709",
  "lead": {
    "name": "Ana Silva",
    "email": "ana.silva@exemplo.com",
    "phone": "+5548999998888",
    "intencao": "Investimento - renda com aluguel",
    "faixa_investimento": "R$ 300.001 a R$ 400.000",
    "forma_pagamento": "À vista via PIX ou boleto",
    "empreendimento": "Canas Beach Spot"
  }
}
```

A MIA inicia automaticamente uma conversa via WhatsApp, utilizando as respostas do formulário para personalizar o primeiro contato e acelerar o processo de vendas.

### Jornada do Corretor

 ![](/api/attachments.redirect?id=d62c90c9-bdb9-4b90-b475-d52f7b3034b2 " =1084x266")

**SUB-WORKFLOW:** `**\[SUB\] Broker Journey**`

A jornada do corretor foi otimizada para distribuição rápida de leads para os hunters responsáveis por cada região geográfica.

#### Processo de Atribuição

```mermaidjs
flowchart LR
    A([🎯 Lead<br/>Corretor])
    B[📧 RD Station]
    C{🔍 Person<br/>existe?}
    D[👤 Criar<br/>Person]
    E[💼 Criar<br/>Deal]
    F[👨‍💼 Atribuir<br/>Hunter]
    G[✅ Status]
    
    A --> B --> C
    C -->|Sim| E
    C -->|Não| D --> E
    E --> F --> G
    
    style A fill:#6366F1,stroke:#4338CA,stroke-width:3px,color:#fff
    style B fill:#FF6B35,stroke:#C44D30,stroke-width:2px,color:#fff
    style C fill:#F59E0B,stroke:#D97706,stroke-width:2px,color:#fff
    style D fill:#8B5CF6,stroke:#6D28D9,stroke-width:2px,color:#fff
    style E fill:#7C3AED,stroke:#5B21B6,stroke-width:2px,color:#fff
    style F fill:#7C3AED,stroke:#5B21B6,stroke-width:2px,color:#fff
    style G fill:#10B981,stroke:#059669,stroke-width:2px,color:#fff
```


1. **Registro de Conversão**: Lead é enviado para RD Station com marcador específico de corretor
2. **Identificação de Hunter**: Sistema utiliza o campo `hunter_owner_id` da tabela **Configurações de Formulário** para determinar o responsável
3. **Criação de Deal**: Deal é automaticamente criado no Pipedrive com:
   * Pessoa (corretor) como contato principal
   * Hunter identificado como owner do deal
   * Stage configurado em `pipedrive_stage_id_broker`
   * Campos customizados preenchidos com dados da origem

#### Payload Pipedrive

```javascript
// Criar Person
{
  "name": "Bruno Costa",
  "email": "bruno.costa@exemplo.com",
  "phone": "+5511988887777",
  "custom_fields": {
    "regiao_atuacao": "Sul",
    "origem": "Facebook Ads",
    "campanha": "[SI] [LEAD ADS] [RS/SC/PR] [CBO] Canas beach Spot"
  }
}

// Criar Deal
{
  "title": "Parceria - Bruno Costa - Canas Beach Spot",
  "person_id": 12345,
  "stage_id": 396,
  "user_id": 1001, // hunter_owner_id
  "custom_fields": {
    "empreendimento": "Canas Beach Spot",
    "origem_lead": "Facebook Lead Ads",
    "data_captura": "2025-10-27T14:30:00Z"
  }
}
```

## Arquitetura de Sub-Workflows

### Arquitetura Modular

O sistema é composto por vários sub-workflows independentes.

### Vantagens da Arquitetura Modular

| **Manutenibilidade** | * Cada sub-workflow pode ser testado e debugado isoladamente
* Mudanças em uma jornada não afetam outras partes do sistema |
|----|----|
| **Reutilização** | * Sub-workflows podem ser chamados de múltiplos workflows principais
* Evita duplicação de código e lógica |
|   **Escalabilidade** | * Novos tipos de jornadas podem ser adicionados sem modificar workflows existentes
* Novas integrações podem ser incluídas de forma modular |
| **Testabilidade** | * Cada módulo pode ser testado com dados mock* Testes de integração podem focar em pontos específicos do fluxo |
|  **Idempotência** | * Todas as operações críticas são idempotentes, ou seja, podem ser executadas múltiplas vezes sem causar efeitos colaterais indesejados. |
| ###  Resiliência | * Falhas em integrações não críticas não bloqueiam o fluxo principal. Erros são logados, notificados via Slack, mas o lead continua sendo processado e armazenado. |

## Observabilidade e Monitoramento

O sistema fornece visibilidade completa do processamento de leads através de múltiplos canais:

### Notificações Slack

**Canal de Erros** (

* Alertas imediatos quando qualquer parte do fluxo falha
* Inclui mensagem de erro detalhada
* Link direto para execução no n8n
* Contexto do lead (nome, email, empreendimento)

**Canal de Notificações**

* Confirmações de leads processados com sucesso
* Separados por MQL e Non-MQL
* Resumo das integrações executadas

### Histórico no Baserow

A tabela **Leads** mantém registro completo de cada lead processado.

### Logs do n8n

Cada execução do workflow é logada no n8n com:

* Dados de entrada de cada node
* Dados de saída de cada node
* Erros e stack traces
* Tempo de execução de cada etapa

## Casos de Uso Especiais

### Caso 1: Telefone Inválido

**Cenário**: Lead fornece telefone com DDD inválido

**Comportamento**:


1. Validação detecta DDD inválido
2. Notificação enviada ao Slack com alerta
3. Campo telefone salvo como fornecido (sem normalização)
4. Lead continua sendo processado normalmente
5. MIA não tenta enviar WhatsApp (sem telefone válido)

### Caso 2: Empreendimento Não Cadastrado

**Cenário**: Lead seleciona empreendimento que não existe no Baserow

**Comportamento**:


1. Query no Baserow retorna vazio
2. Erro é capturado e logado
3. Notificação enviada ao Slack com detalhes
4. Lead não é processado pelas jornadas

### Caso 3: Falha na MIA

**Cenário**: API da MIA está indisponível

**Comportamento**:


1. Timeout ou erro na chamada da MIA
2. Erro é capturado mas não interrompe fluxo
3. RD Station recebe conversão normalmente
4. Notificação de erro enviada ao Slack
5. Lead pode ser reprocessado manualmente depois

## Notas Importantes

> **Baserow como Fonte da Verdade**
>
> O Baserow atua como o repositório central de dados do sistema. Todas as informações de campanhas, leads e configurações estão organizadas e acessíveis através da API do Baserow. 

> **n8n como Camada de Orquestração**
>
> O n8n não armazena estado persistente. Ele apenas orquestra o fluxo de dados entre as diferentes plataformas (Facebook, RD Station, Pipedrive, MIA) e persiste o resultado final no Baserow. Isso garante que mesmo se o n8n estiver temporariamente indisponível, nenhum dado é perdido.

## Glossário Técnico

| Termo | Definição |
|----|----|
| **Webhook** | Endpoint HTTP que recebe dados automaticamente quando um evento ocorre |
| **Sub-workflow** | Workflow modular que encapsula uma responsabilidade específica |
| **Idempotência** | Propriedade de operações que podem ser executadas múltiplas vezes com o mesmo resultado |
| **MQL** | Marketing Qualified Lead - lead que passou por critérios de qualificação |
| **Form ID** | Identificador único do formulário no Facebook Lead Ads |
| **E.164** | Padrão internacional para números de telefone (+5548999999999) |
| **Upsert** | Operação que insere se não existir, ou atualiza se já existir |
| **Payload** | Dados enviados em uma requisição HTTP |
| **Stack Trace** | Rastro de execução que mostra onde um erro ocorreu |


---

**Versão**: 3.0\n**Última atualização**: 30/10/2025