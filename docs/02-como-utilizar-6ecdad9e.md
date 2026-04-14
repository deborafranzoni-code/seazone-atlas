<!-- title: 02 - Como Utilizar | url: https://outline.seazone.com.br/doc/02-como-utilizar-ffCnjThwo0 | area: Tecnologia -->

# 02 - Como Utilizar

Pré-requisitos

Antes de começar, você precisa ter:

* ✅ **Campanha ativa no Facebook Ads** → [Como criar campanha](https://outline.seazone.com.br/doc/22-como-criar-campanhas-VxQ1IQMvMi)
* ✅ **Formulário Lead Ads criado** → [Como criar formulário](https://outline.seazone.com.br/doc/22-como-criar-campanhas-VxQ1IQMvMi)
* ✅ **Acesso ao Baserow Marketplace** → [Acessar database 332](https://baserow.seazone.com.br/database/332)


---

## ⚠️ CRÍTICO: Nomenclatura do Anúncio

O nome do empreendimento é **automaticamente extraído do nome do anúncio**. O ad_name DEVE seguir o padrão:

```
[TAG1] [TAG2] NomeDoEmpreendimento_Complemento
```

**Exemplo correto:**

```
[SI] [LEAD ADS] Jurere Beach Village_Marketplace
                ↑ Isso será extraído como nome do empreendimento
```

❌ **Se não seguir esse padrão, o lead NÃO será processado!**


---

## Passo 1: Coletar Informações da Campanha

Você precisará anotar estas informações antes de configurar no Baserow:

| Informação | Onde Encontrar |
|----|----|
| **1. Nome do Formulário** | Facebook Business Manager > Formulários > Nome |
| **2. Form ID** | Facebook Business Manager > Formulários > URL |
| **3. Nome da Campanha** | Facebook Ads Manager > Nome da campanha |
| **4. ID da Campanha** | Facebook Ads Manager > Coluna "ID da campanha" |

**Exemplo de valores:**

```
Form ID: 1984062249106864

Nome da Campanha: [SI] [LEAD ADS] Jurere Beach Village_Marketplace | Out/2025

ID da Campanha: 192198393899319

Ad Name: [SI] [LEAD ADS] Jurere Beach Village_Marketplace
         → O sistema extrairá: "Jurere Beach Village"
```

> 💡 **O nome do empreendimento NÃO vem do formulário, é extraído automaticamente do ad_name**


---

## Passo 2: Cadastrar no Baserow

### 2.1 Cadastrar Empreendimento

👉 **[Acessar formulário de cadastro](https://baserow.seazone.com.br/database/332/table/1209)**

**Informações necessárias:**

**Seção: Informações Básicas**

* Nome do Empreendimento (**DEVE ser exatamente igual ao extraído do ad_name**)
* Formulário Facebook Ads (selecione da lista)
* Nome da Campanha
* ID da Campanha

**Seção: Regras MQL** → [Entender regras MQL](https://outline.seazone.com.br/doc/23-entendendo-as-regras-mql-HuoVnk9Bi5)

* Intenções válidas (ex: Investimento - renda, valorização)
* Faixas de investimento (ex: R$ 200k-300k, R$ 300k-400k)

**Seção: Configurações**

* RD Station: Traffic Source e Medium
* MIA: Configurações (fornecidas pela Morada)
* Slack: Canais de notificação

> 💡 **Dica:** Cadastre o formulário primeiro no passo 2.2 se ainda não existe


---

### 2.2 Cadastrar Formulário

👉 **[Acessar formulário de cadastro](https://baserow.seazone.com.br/database/332)**

**Informações necessárias:**

* Nome do Formulário (ex: `[MARKETPLACE] Jurere Beach Village | 14/10/2025`)
* Form ID do Facebook (ex: `1984062249106864`)

> ⚠️ **Importante:** Verifique se o formulário ou empreendimento já existem antes de criar duplicatas


---

## Passo 3: Validar Nomenclatura dos Anúncios

Antes de ativar a campanha, **valide que TODOS os anúncios** seguem o padrão:

**Checklist de validação:**

- [ ] Ad name tem tags no formato `[TAG]`
- [ ] Nome do empreendimento vem após as tags
- [ ] Existe underscore `_` separando empreendimento do complemento
- [ ] Nome do empreendimento no ad_name = nome cadastrado no Baserow


---

## Algo deu errado?

Se alguma verificação falhou:

* Verifique o **canal de erros no Slack** (#n8n-marketing-marketplace)
* Consulte o guia de **[Troubleshooting](https://outline.seazone.com.br/doc/24-troubleshooting-G6sGiwpXSp)**
* Entre em contato com o time de Marketing

**Erros comuns:**

* ❌ Ad name não segue padrão → Lead não processa
* ❌ Nome no Baserow diferente do ad_name → Config não encontrada
* ❌ Lead duplicado → Sistema descarta automaticamente


---

## Pronto!

Sua campanha está configurada e funcionando automaticamente.

**Tempo médio de processamento:** 30-60 segundos por lead


---

## 📚 Para Saber Mais

* [Como funciona o sistema completo](https://outline.seazone.com.br/doc/21-sobre-o-sistema-xV4c2WMBXn)
* [Entender regras de qualificação MQL](https://outline.seazone.com.br/doc/23-entendendo-as-regras-mql-HuoVnk9Bi5)
* [Perguntas frequentes (FAQ)](https://outline.seazone.com.br/doc/25-faq-e-referencias-uKBMtu2hKw)
* [Glossário e referências](https://outline.seazone.com.br/doc/25-faq-e-referencias-uKBMtu2hKw)


---

**Versão:** 1.0\n**Última atualização:** 10/11/2025\n**Elaborado para:** Equipe de Marketing SZI - Marketplace