<!-- title: 2.2 - Troubleshooting | url: https://outline.seazone.com.br/doc/22-troubleshooting-yac1qZtls5 | area: Tecnologia -->

# 2.2 - Troubleshooting

# 2.4 - Troubleshooting - Marketplace

> 🔧 Soluções para problemas comuns no sistema de automação


---

## ❌ Lead não qualificou como MQL

### 🔍 Diagnóstico

O lead foi processado, mas não é MQL.

### Verificações

#### 1. Revisar configurações do empreendimento


1. Acesse Baserow > Empreendimentos (database 332)
2. Encontre o empreendimento
3. Verifique as 2 seções de regras MQL:
   * Intenções Válidas
   * Valores de Entrada Válidos

#### 2. Comparar com as respostas do lead


1. Acesse Baserow > Leads
2. Encontre o lead
3. Verifique as colunas "Intenção" e "Valor Entrada"
4. Compare com as regras configuradas

### Lembre-se:

> Um lead precisa atender os 2 critérios SIMULTANEAMENTE:
>
> * Intenção válida E
> * Valor de entrada válido
>
> Se falhar em 1 único critério = NÃO é MQL

### Soluções

**Se as regras estão muito restritivas:**


1. Edite o empreendimento no Baserow
2. Marque mais opções nas 2 seções
3. Novos leads serão qualificados com as novas regras

**Se o lead realmente não deveria ser MQL:**

* Está funcionando corretamente
* O lead vai para RD Station normalmente
* Investidor não-MQL não vai para MIA


---

## 📱 MIA não enviou WhatsApp

### 🔍 Diagnóstico

O lead foi processado, mas não recebeu mensagem no WhatsApp.

### Checklist de Verificação

#### 1. Para investidores: Lead qualificou como MQL?

No Baserow > Leads, verifique:

- [ ] Coluna "MIA Status" = success

**Se não:**

* Verifique coluna "MQL Status"
* Se "unqualified", o problema é qualificação MQL (veja seção acima)

#### 2. Para corretores: Sempre deveria receber

Corretor sempre vai para MIA, sem qualificação.

No Baserow > Leads, verifique:

- [ ] Coluna "MIA Status" = success

#### 3. Configurações MIA estão preenchidas?

No Baserow > Empreendimentos, verifique:

**Para investidores:**

- [ ] MIA \[Investidor\]: Instance ID preenchido (1292)
- [ ] MIA \[Investidor\]: Product ID preenchido
- [ ] MIA \[Investidor\]: Message Template preenchido

**Para corretores:**

- [ ] MIA \[Corretor\]: Instance ID preenchido (1527)
- [ ] MIA \[Corretor\]: Product ID preenchido
- [ ] MIA \[Corretor\]: Message Template preenchido

**Comum a ambos:**

- [ ] MIA: Source preenchido

**Se estiver vazio:**

* Entre em contato com a Morada para obter os valores corretos
* Preencha as configurações
* Envie novo lead de teste

#### 4. Telefone é válido?

No Baserow > Leads, verifique:

- [ ] Coluna "Telefone Status" = valid

**Se invalid:**

* MIA não consegue enviar WhatsApp
* DDD inválido ou telefone mal formatado
* Problema está no dado fornecido pelo lead

#### 5. Verifique canal de erros

Slack #n8n-marketing-marketplace:

* Busque por erros relacionados a MIA
* Verifique se há problema de integração


---

## 🔍 Lead não apareceu no Baserow

### 🔍 Diagnóstico

Você enviou o formulário no Facebook, mas o lead não apareceu na tabela Leads do Baserow.

### Verificações

#### 1. Aguardou tempo suficiente?

* Tempo normal: 30-60 segundos
* Tempo máximo: 2-5 minutos

**Aguarde 3 minutos antes de investigar**

#### 2. Empreendimento está ativo?

No Baserow > Empreendimentos:


1. Encontre seu empreendimento
2. Verifique a coluna "Status"
3. Confirme que está marcado como "Ativo"

**Se não estiver ativo:**

* O sistema não processa leads desse empreendimento
* Marque como "Ativo"
* Envie novo lead de teste

#### 3. Nomenclatura do anúncio está correta?

Verifique se o ad_name segue o padrão:

```
[TAG1] [TAG2] prefixo_NomeDoEmpreendimento_data
```

**Exemplo correto:**

```
[AD 2] [VÍDEO] swot_Santinho Spot Teste_03/11/2025
```

**Erros comuns:**

* Falta prefixo antes do nome
* Falta underscore após prefixo
* Nome extraído diferente do cadastrado no Baserow

**Teste:**


1. Pegue o ad_name do anúncio
2. Remova as tags iniciais \[TAG1\] \[TAG2\]
3. Divida por underscore "_"
4. A segunda parte é o nome extraído
5. Confira se é exatamente igual ao nome no Baserow

#### 4. Lead é duplicado?

Sistema descarta automaticamente leads duplicados.

Verifique na tabela Leads se o `leadgen_id` já existe.

#### 5. Webhook está funcionando?

* Verifique canal de erros no Slack
* Busque por mensagens de webhook indisponível

### Soluções

**Problema de nomenclatura:**


1. Corrija o ad_name seguindo o padrão
2. OU atualize o nome do empreendimento no Baserow para corresponder ao extraído
3. Envie novo lead de teste

**Problema de status:**


1. Marque empreendimento como "Ativo"
2. Envie novo lead de teste


---

## 📧 RD Station não recebeu o lead

### 🔍 Diagnóstico

Lead apareceu no Baserow, mas não foi para RD Station.

### Verificações

No Baserow > Leads:

- [ ] Coluna "RD Status" = success

**Se failure:**

* Houve erro no envio
* Verifique canal de erros no Slack

### Soluções


1. Verifique configurações no empreendimento:
   * RD Station: Traffic Source
   * RD Station: Traffic Medium
   * RD Station: Traffic Campaign
2. Confirme com time de Marketing se os valores estão corretos
3. Verifique se há erro de integração no Slack

**Valores comuns:**

```
Traffic Source: Facebook Ads

Traffic Medium: cpc
```


---

## 🔄 Lead duplicado foi descartado

### 🔍 Diagnóstico

Lead foi enviado pelo Facebook, mas sistema descartou por duplicidade.

### Comportamento esperado

**Isso é normal e correto.**

Facebook pode enviar o mesmo webhook múltiplas vezes. O sistema:


1. Verifica se `leadgen_id` já existe
2. Se sim, descarta automaticamente
3. Evita dados duplicados e múltiplos contatos ao mesmo lead

### Verificação

No Baserow > Leads:

* Busque pelo `leadgen_id`
* Se já existe, a duplicidade foi corretamente identificada

**Não é necessária ação.**


---

## ⚠️ Empreendimento não foi encontrado

### 🔍 Diagnóstico

Sistema não encontrou configuração do empreendimento.

### Verificações

#### 1. Nome do empreendimento no Baserow

No Baserow > Empreendimentos:

* Nome cadastrado deve ser EXATAMENTE igual ao extraído do ad_name

#### 2. Extração do ad_name


1. Pegue o ad_name: `[AD 2] [VÍDEO] swot_Santinho Spot Teste_03/11/2025`
2. Remove tags: `swot_Santinho Spot Teste_03/11/2025`
3. Divide por "_": `["swot", "Santinho Spot Teste", "03/11/2025"]`
4. Pega segunda parte: `"Santinho Spot Teste"`

Este nome deve estar EXATAMENTE assim no Baserow (inclusive maiúsculas/minúsculas).

#### 3. Status do empreendimento

- [ ] Status = "Ativo"

### Soluções

**Nome diferente:**


1. Atualize o nome no Baserow para corresponder ao extraído
2. OU corrija o ad_name para corresponder ao cadastrado
3. Envie novo lead de teste

**Status inativo:**


1. Marque como "Ativo"
2. Envie novo lead de teste


---

## ☎️ Telefone inválido

### 🔍 Diagnóstico

No Baserow > Leads, coluna "Telefone Status" = invalid

### Comportamento

* Lead é processado normalmente
* RD Station recebe o lead
* MIA não consegue enviar WhatsApp (telefone inválido)
* Sistema registra flag de telefone inválido

### Causas comuns

* DDD inválido (não brasileiro)
* Número mal formatado
* Lead forneceu telefone incorreto

### Solução

**Não há solução automática.**

O problema está no dado fornecido pelo lead. Você pode:


1. Entrar em contato via email
2. Solicitar telefone correto
3. Adicionar manualmente na MIA


---

## 🆘 Problemas Não Listados

Se você enfrentou um problema não coberto aqui:

### 💬 Canal de Erros no Slack

Canal: #n8n-marketing-marketplace


1. Busque pela execução
2. Verifique timestamp do erro
3. Leia a mensagem de erro completa
4. Acesse o link da execução no n8n

### Informações úteis para reportar

* `leadgen_id` do lead
* Nome do empreendimento
* Timestamp
* Mensagem de erro do Slack
* Comportamento esperado vs obtido


---

**Versão:** 2.0\n**Última atualização:** 13/11/2025\n**Elaborado para:** Equipe de Marketing SZI - Marketplace