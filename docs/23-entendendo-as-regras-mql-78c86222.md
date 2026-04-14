<!-- title: 2.3 - Entendendo as Regras MQL | url: https://outline.seazone.com.br/doc/23-entendendo-as-regras-mql-HuoVnk9Bi5 | area: Tecnologia -->

# 2.3 - Entendendo as Regras MQL

> **Como funciona a qualificação automática de Marketing Qualified Leads**


---

## O que é um MQL?

**MQL (Marketing Qualified Lead)** é um lead que atende aos critérios de qualificação definidos pela empresa e está pronto para ser contactado pela equipe de vendas via WhatsApp.

**Diferença prática:**

* ✅ **MQL:** Recebe mensagem automática no WhatsApp via MIA, vai para o Pipedrive
* ❌ **Não-MQL:** Não recebe WhatsApp, apenas vai para RD Station 


---

## 🔄 Como Funciona a Qualificação

Um lead **investidor** é considerado MQL quando atende **TODOS os 3 critérios** simultaneamente:

```mermaidjs
%%{init: {'theme':'base', 'themeVariables': {
  'primaryColor':'#0f172a',
  'primaryTextColor':'#fff',
  'primaryBorderColor':'#334155',
  'lineColor':'#64748b',
  'secondaryColor':'#0ea5e9',
  'tertiaryColor':'#f43f5e'
}}}%%

flowchart TD
    Start["👤<br/>LEAD INVESTIDOR"]:::inputStyle
    
    subgraph Validacao["🔍 VALIDAÇÃO MQL"]
        direction TB
        Step1["1️⃣ Intenção de Compra"]:::stepStyle
        Step2["2️⃣ Faixa de Investimento"]:::stepStyle
        Step3["3️⃣ Forma de Pagamento"]:::stepStyle
        
        Step1 --> Step2
        Step2 --> Step3
    end
    
    Result{"Passou em<br/>TODOS?"}:::decisionStyle
    
    MQL["✅<br/>MQL CONFIRMADO<br/>🚀 Envio via MIA"]:::successStyle
    NotMQL["❌<br/>NÃO QUALIFICADO<br/>📊 RD Station Only"]:::failStyle
    
    Start --> Validacao
    Validacao --> Result
    Result -->|Sim| MQL
    Result -->|Não| NotMQL
    
    classDef inputStyle fill:#1e293b,stroke:#475569,stroke-width:2px,color:#fff,font-weight:bold
    classDef stepStyle fill:#0ea5e9,stroke:#0284c7,stroke-width:2px,color:#fff
    classDef decisionStyle fill:#f59e0b,stroke:#d97706,stroke-width:3px,color:#fff,font-weight:bold
    classDef successStyle fill:#10b981,stroke:#059669,stroke-width:4px,color:#fff,font-size:16px,font-weight:bold
    classDef failStyle fill:#f43f5e,stroke:#e11d48,stroke-width:3px,color:#fff,font-size:14px
    
    style Validacao fill:#f8fafc,stroke:#cbd5e1,stroke-width:2px,color:#1e293b,stroke-dasharray: 5 5
```

### Os 3 Critérios:

#### 1️⃣ Intenção de Compra

O lead deve ter uma das intenções marcadas como válidas no Baserow.

**Opções possíveis:**

* Investimento - renda com aluguel
* Investimento - valorização
* Uso próprio - moradia
* Uso próprio - uso esporádico

#### 2️⃣ Faixa de Investimento

O lead deve ter uma das faixas marcadas como válidas no Baserow.

**Opções possíveis:**

* R$ 50.000 a R$ 100.000
* R$ 100.001 a R$ 200.000
* R$ 200.001 a R$ 300.000
* R$ 300.001 a R$ 400.000
* Acima de R$ 400.000
* Não consigo atender

#### 3️⃣ Forma de Pagamento

O lead deve ter uma das formas marcadas como válidas no Baserow.

**Opções possíveis:**

* À vista
* Parcelado
* Financiamento
* Permuta


---

## Exemplos Práticos

### Exemplo 1: Lead Qualifica

**Configuração no Baserow:**

```
Intenções marcadas como válidas:
☑️ Investimento - renda com aluguel
☑️ Investimento - valorização

Faixas marcadas como válidas:
☑️ R$ 200.001 a R$ 300.000
☑️ R$ 300.001 a R$ 400.000
☑️ Acima de R$ 400.000

Formas marcadas como válidas:
☑️ À vista
☑️ Parcelado
```

**O que o lead respondeu no formulário:**

```
Intenção: Investimento - valorização ✅
Valor: Acima de R$ 400.000 ✅
Forma: À vista via PIX ✅
```

**Resultado:**

```
✅ É MQL! (atendeu os 3 critérios)

Ações automáticas:
→ Enviado para RD Station
→ Enviado para MIA (WhatsApp) 📱
→ Deal criado no Pipedrive
```


---

### Exemplo 2: Lead NÃO Qualifica

**Configuração no Baserow:**

```
Intenções marcadas como válidas:
☑️ Investimento - renda com aluguel
☑️ Investimento - valorização

Faixas marcadas como válidas:
☑️ R$ 200.001 a R$ 300.000
☑️ R$ 300.001 a R$ 400.000
☑️ Acima de R$ 400.000

Formas marcadas como válidas:
☑️ À vista
☑️ Parcelado
```

**O que o lead respondeu no formulário:**

```
Intenção: Investimento - renda com aluguel ✅
Valor: R$ 100.001 a R$ 200.000 ❌ (não está marcado como válido)
Forma: À vista ✅
```

**Resultado:**

```
❌ NÃO é MQL (falhou no critério de valor)

Ações automáticas:
→ Enviado para RD Station
→ NÃO enviado para MIA ⛔
→ Deal NÃO criado no Pipedrive
→ Email de não qualificação
```


---

## Caso Especial: Corretores

Leads que marcam **"Sim"** em **"É corretor de imóveis?"** seguem um fluxo diferente:

```
Lead marcou: É corretor? = Sim

Resultado:
→ Enviado para RD Station
→ NÃO enviado para MIA (corretores não recebem WhatsApp)
→ Atribuído ao hunter da região
```

> 💡 **Nota:** Corretores **NUNCA** são considerados MQL, independente das outras respostas.


---

## Como Configurar Regras

As regras são configuradas no Baserow, no formulário de cadastro de Empreendimentos.

**Seção: "Intenções que qualificam como MQL"**

Para cada empreendimento, você escolhe:


1. **Quais intenções** são válidas
2. **Quais faixas de investimento** são válidas
3. **Quais formas de pagamento** são válidas


---

## Mudando Regras

### ⚠️ Importante Saber:

* ✅ Você **PODE** mudar as regras a qualquer momento
* ✅ Mudanças afetam **APENAS leads futuros**
* ❌ Leads antigos **NÃO** são reprocessados


---

## Visualizando Qualificação

No Baserow, tabela **Leads**, você pode ver:

| Coluna | O que mostra |
|----|----|
| **É MQL?** | `True` ou `False` |
| **MQL - Motivo** | Se `False`, explica qual critério falhou |
| **MIA Enviado?** | Se `True`, WhatsApp foi enviado |


---

## 🔗 Links Relacionados

* [← Voltar ao guia rápido](https://outline.seazone.com.br/doc/02-como-utilizar-ffCnjThwo0)
* [Sobre o sistema →](https://outline.seazone.com.br/doc/21-sobre-o-sistema-xV4c2WMBXn)
* [Como criar campanhas →](https://outline.seazone.com.br/doc/22-como-criar-campanhas-VxQ1IQMvMi)
* [Troubleshooting →](https://outline.seazone.com.br/doc/24-troubleshooting-G6sGiwpXSp)
* [FAQ →](https://outline.seazone.com.br/doc/25-faq-e-referencias-uKBMtu2hKw)