<!-- title: 2.4 - Troubleshooting | url: https://outline.seazone.com.br/doc/24-troubleshooting-G6sGiwpXSp | area: Tecnologia -->

# 2.4 - Troubleshooting

> **Soluções para problemas comuns no sistema de automação**


---

## Lead não qualificou como MQL

### 🔍 Diagnóstico

O lead foi processado, mas a coluna **"É MQL?"** no Baserow mostra `False`.

### ✅ Verificações

#### 1. Revisar configurações do empreendimento


1. Acesse **Baserow > Empreendimentos**
2. Encontre o empreendimento
3. Verifique as **3 seções de regras MQL**:
   * Intenções Válidas
   * Faixas de Investimento
   * Formas de Pagamento

#### 2. Comparar com as respostas do lead


1. Acesse **Baserow > Leads**
2. Encontre o lead
3. Verifique a coluna **"MQL - Motivo"**
4. Compare as respostas com as regras configuradas

### Lembre-se:

> **Um lead precisa atender os 3 critérios SIMULTANEAMENTE:**
>
> * ✅ Intenção válida **E**
> * ✅ Faixa de valor válida **E**
> * ✅ Forma de pagamento válida
>
> Se falhar em **1 único critério** = NÃO é MQL

### Soluções

**Se as regras estão muito restritivas:**


1. Edite o empreendimento no Baserow
2. Marque mais opções nas 3 seções
3. Novos leads serão qualificados com as novas regras

**Se o lead realmente não deveria ser MQL:**

* Está funcionando corretamente ✅
* O lead vai para RD Station e Pipedrive normalmente


---

## MIA não enviou WhatsApp 

### 🔍 Diagnóstico

O lead foi qualificado como MQL, mas não recebeu mensagem no WhatsApp.

### ✅ Checklist de Verificação

#### 1. Lead qualificou como MQL?

No Baserow > Leads, verifique:

- [ ] Coluna **"É MQL?"** = `True`

**Se não:**

* O problema não é na MIA, veja seção [Lead não qualificou como MQL](#lead-nao-mql)

#### 2. Lead é investidor (não corretor)?

No Baserow > Leads, verifique:

- [ ] Coluna **"É Corretor?"** = `False` ou vazio

**Se for corretor:**

* ✅ **Normal!** Corretores nunca recebem WhatsApp, mesmo se qualificarem como MQL

#### 3. Configurações MIA estão preenchidas?

No Baserow > Empreendimentos, verifique se o empreendimento tem:

- [ ] **MIA: Instance ID** preenchido
- [ ] **MIA: Product ID** preenchido
- [ ] **MIA: Message Template** preenchido
- [ ] **MIA: Source** preenchido

**Se estiver vazio:**

* Entre em contato com a **Morada** para obter os valores corretos
* Preencha as configurações
* Envie novo lead de teste

#### 4. Coluna "MIA Enviado?" está preenchida?

No Baserow > Leads, verifique:

- [ ] Coluna **"MIA Enviado?"** = `True`

**Se estiver** `**False**` **ou vazio:**

* Houve erro no envio
* Verifique o canal de erros no Slack


---

## Deal não criado no Pipedrive 

### 🔍 Diagnóstico

O lead foi processado, mas não apareceu deal no Pipedrive.

### ✅ Verificações

#### 1. Lead é de "uso próprio"?

No Baserow > Leads, verifique:

* Coluna **"Intenção"**: Se for "Uso próprio - moradia" 

**Comportamento:**

* ⚠️ Leads de uso próprio - moradia **NÃO geram deals** automaticamente
* Eles vão apenas para RD Station

#### 2. Stage ID está configurado?

No Baserow > Empreendimentos, verifique:

**Para investidores:**

- [ ] **Pipedrive: Stage Name (Investidor)** está preenchido

**Para corretores:**

- [ ] **Pipedrive: Stage Name (Corretor)** está preenchido

**Se estiver vazio:**


1. Acesse **Baserow > Stage Pipedrive**
2. Encontre o estágio correto
3. Copie o nome exato
4. Cole no empreendimento

#### 3. Stage ID está correto?

Verifique se o nome do estágio no Baserow corresponde a um estágio real no Pipedrive:


1. Acesse o Pipedrive
2. Entre em Configurações > Funis e Estágios
3. Confirme que o nome está **exatamente igual** (maiúsculas/minúsculas)

**Exemplos:**

```
✅ Correto: "Novo Lead - Qualificado"
❌ Errado: "novo lead - qualificado" (minúsculas)
❌ Errado: "Novo Lead Qualificado" (sem hífen)
❌ Errado: "Novo Lead - Qualificado " (espaço extra)
```

### 🔧 Soluções

**Se o Stage ID está errado ou vazio:**


1. Edite o empreendimento no Baserow
2. Preencha com o nome correto do estágio
3. Envie novo lead de teste

**Se o problema persistir:**

* Verifique o canal de erros no Slack
* Pode haver problema de integração com Pipedrive


---

##  Lead não apareceu no Baserow 

### 🔍 Diagnóstico

Você enviou o formulário no Facebook, mas o lead não apareceu na tabela Leads do Baserow.

### ✅ Verificações

#### 1. Aguardou tempo suficiente?

* ⏱️ **Tempo normal:** 30-60 segundos
* ⏱️ **Tempo máximo:** 2- 5 minutos

**Aguarde 3 minutos antes de investigar**

#### 2. Formulário está vinculado ao empreendimento?

No Baserow > Empreendimentos:


1. Encontre seu empreendimento
2. Verifique a coluna **"Formulário"**
3. Confirme que o formulário correto está selecionado

**Se estiver vazio:**


1. Edite o empreendimento
2. Selecione o formulário da lista
3. Envie novo lead de teste

#### 3. Form ID está correto?

No Baserow > Formulários:


1. Encontre seu formulário
2. Verifique se o **Form ID** está correto
3. Compare com o ID da URL do Facebook

**Como pegar o Form ID correto:**

```
URL do formulário:
https://business.facebook.com/.../forms/1984062249106864/...
                                        └─── Este é o Form ID
```

#### 4. Webhook está funcionando?

* Verifique o canal de erros no Slack
* Busque por mensagens de webhook indisponível

### 🔧 Soluções

**Problema de vinculação:**


1. Certifique-se que Form ID está correto
2. Certifique-se que formulário está vinculado ao empreendimento
3. Envie novo lead de teste


---

## RD Station não recebeu o lead 

### 🔍 Diagnóstico

Lead apareceu no Baserow, mas não foi para RD Station.

### ✅ Verificações

No Baserow > Leads:

- [ ] Coluna **"RD Enviado?"** = `True`

**Se estiver** `**False**` **ou vazio:**

* Houve erro no envio
* Verifique canal de erros no Slack

### 🔧 Soluções


1. Verifique configurações de **Traffic Source** e **Traffic Medium** no empreendimento
2. Confirme com time de Marketing se os valores estão corretos
3. Verifique se há erro de integração no Slack

**Valores comuns:**

```
Traffic Source: facebook

Traffic Medium: cpc
```


---

## Problemas Não Listados

Se você enfrentou um problema não coberto aqui:

### 1. Canal de Erros no Slack

👉 **#n8n-marketing-szi**

* Busque pela execução
* Verifique timestamp do erro
* Leia a mensagem de erro completa
* Acesse a execução


---

## 🔗 Links Relacionados

* [← Voltar ao guia rápido](https://outline.seazone.com.br/doc/02-como-utilizar-ffCnjThwo0)
* [Sobre o sistema →](https://outline.seazone.com.br/doc/21-sobre-o-sistema-xV4c2WMBXn)
* [Como criar campanhas →](https://outline.seazone.com.br/doc/22-como-criar-campanhas-VxQ1IQMvMi)
* [FAQ →](https://outline.seazone.com.br/doc/25-faq-e-referencias-uKBMtu2hKw)