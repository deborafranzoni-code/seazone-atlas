<!-- title: 02 - Como Utilizar | url: https://outline.seazone.com.br/doc/02-como-utilizar-mIaj3t3hak | area: Tecnologia -->

# 02 - Como Utilizar

## Pré-requisitos

Antes de começar:

* ✅ **Campanha ativa no Facebook Ads** → [Como criar campanha](https://outline.seazone.com.br/doc/22-como-criar-campanhas-VxQ1IQMvMi)
* ✅ **Formulário Lead Ads criado** → [Como criar formulário](https://outline.seazone.com.br/doc/22-como-criar-campanhas-VxQ1IQMvMi)
* ✅ **Acesso ao Baserow Marketplace** → [Acesso ao Baserow (database 332)](https://baserow.seazone.com.br/database/332/table/1325/5808)


---

> ⚠️ Detalhes e visualizaçẽos de campanhas marketplace em [2.4 - VIsualizações](/doc/24-visualizacoes-ehfMPvnAtf#link-pagina-principal)

## Nomenclatura do Anúncio

O nome do empreendimento é extraído automaticamente do `ad_name`. O padrão é obrigatório:

```
[TAG1] [TAG2] prefixo_NomeDoEmpreendimento_data
```

**Exemplo correto:**

```
[AD 2] [VÍDEO] swot_Santinho Spot Teste_03/11/2025
                prefixo_↑ ESTE NOME SERÁ EXTRAÍDO ↑
```

**Estrutura:**

* `[TAG1] [TAG2]` → Tags de identificação (removidas automaticamente)
* `prefixo_` → Identificador do criativo (ex: swot_, ace_)
* `NomeDoEmpreendimento` → Extraído pelo sistema (segunda parte após split por underscore)
* `_data` → Data da campanha (opcional)

**Se não seguir o padrão, o lead não será processado.**


---

## Passo 1: Coletar Informações

Anote estas informações antes de configurar no Baserow:

| Informação | Onde Encontrar |
|----|----|
| Nome do Formulário | Facebook Business Manager > Formulários > Nome |
| Form ID | Facebook Business Manager > Formulários > URL |
| Nome da Campanha | Facebook Ads Manager > Nome da campanha |
| ID da Campanha | Facebook Ads Manager > Coluna "ID da campanha" |

**Exemplo:**

```
Form ID: 1984062249106864
Nome da Campanha: [MKTPLACE] [LEAD] [RS/SC/PR] [CBO] Santinho Spot Teste_03/11/2025
ID da Campanha: 192198393899319
Ad Name: [AD 2] [VÍDEO] swot_Santinho Spot Teste_03/11/2025
         Sistema extrairá: "Santinho Spot Teste"
```

O nome do empreendimento vem após o primeiro underscore e antes do segundo underscore.


---

## Passo 2: Cadastrar no Baserow

### 2.1 Cadastrar Empreendimento

Acesse: https://baserow.seazone.com.br/database/332/table/1325

**Informações necessárias:**

**Seção: Informações Básicas**

* Nome do Empreendimento (deve ser exatamente igual ao extraído do ad_name)
* Status: marque como "Ativo" (apenas empreendimentos ativos são processados)

**Seção: Regras MQL**

* Intenções válidas (ex: Investimento - renda, Investimento - valorização)
* Valores de entrada válidos (ex: R$ 30k-50k, R$ 50k-80k)

**Seção: Configurações**

* RD Station: Traffic Source, Traffic Medium, Event
* MIA Investidor: Instance ID (1292), Product ID, Message Template
* MIA Corretor: Instance ID (1527), Product ID, Message Template
* MIA: Source
* Slack: Canal de notificações

### 2.2 Verificar Formulário

Verifique se o formulário já está cadastrado na tabela de empreendimentos. Se não estiver, adicione as informações:

* Nome do Formulário
* Form ID do Facebook

**Importante:** Verifique se o empreendimento já existe antes de criar duplicatas.


---

## Passo 3: Validar Nomenclatura dos Anúncios

Antes de ativar a campanha, valide que todos os anúncios seguem o padrão:

**Checklist:**

- [ ] Ad name tem tags no formato `[TAG]` no início
- [ ] Existe prefixo seguido de underscore (ex: swot_, ace_)
- [ ] Nome do empreendimento vem após o primeiro underscore
- [ ] Existe segundo underscore separando empreendimento da data
- [ ] Nome do empreendimento no ad_name = nome cadastrado no Baserow

**Exemplos:**

```
CORRETO: [AD 2] [VÍDEO] swot_Santinho Spot Teste_03/11/2025
         Tags OK | Prefixo OK | Nome: "Santinho Spot Teste"

ERRADO: [AD 2] [VÍDEO] Santinho Spot Teste_03/11/2025
        Falta prefixo antes do nome

ERRADO: [AD 2] [VÍDEO] swot Santinho Spot Teste_03/11/2025
        Falta underscore após prefixo
```


---

## Resolução de Problemas

**Erros comuns:**

* Ad name não segue padrão → Lead não processa
* Nome no Baserow diferente do ad_name → Config não encontrada
* Status não está "Ativo" → Empreendimento não processa
* Lead duplicado → Sistema descarta automaticamente

**Onde verificar:**

* Canal Slack: #n8n-marketing-marketplace
* Baserow tabela Leads: status de RD e MIA
* Execuções n8n: logs detalhados


---

## Pronto

Sua campanha está configurada. O sistema processa leads em 30-60 segundos.


---

**Versão:** 2.0\n**Última atualização:** 13/11/2025\n**Elaborado para:** Equipe de Marketing SZI - Marketplace