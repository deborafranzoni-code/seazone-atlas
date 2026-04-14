<!-- title: 2.5 - FAQ e Referências | url: https://outline.seazone.com.br/doc/25-faq-e-referencias-uKBMtu2hKw | area: Tecnologia -->

# 2.5 - FAQ e Referências

> **Perguntas frequentes e informações de referência**


---

## Perguntas Frequentes

### 🔧 Operacionais

#### **Preciso mexer no n8n ou em código?**

> **Não!** Tudo é configurado através dos formulários do Baserow. Você nunca precisa acessar o n8n ou mexer em código.


---

#### **Posso ter vários formulários para o mesmo empreendimento?**

> **Sim!** Você pode criar múltiplos registros na tabela **Formulários** do Baserow, todos apontando para o mesmo empreendimento.

**Exemplo de uso:**

```
Empreendimento: Canas Beach Spot

Formulário 1: [SZI] Canas | Público Geral
Formulário 2: [SZI] Canas | Anúncio Stories
Formulário 3: [SZI] Canas | Anúncio Feed
```

Todos os leads cairão no mesmo empreendimento e usarão as mesmas regras MQL.


---

#### **Posso mudar as regras MQL depois de configurar?**

> **Sim!** As mudanças afetam apenas **novos leads**. Leads já processados não são requalificados.


---

#### **Quanto tempo leva para processar um lead?**

> **Tempo médio:** 30-60 segundos


---

#### **Como sei se algo deu errado?**

> Verifique o **canal de erros no Slack**: **#n8n-marketing-szi**


---

#### **Leads antigos são afetados por mudanças nas regras?**

> **Não.** Mudanças nas regras MQL afetam apenas leads futuros.


---


---

#### **O que significa cada tipo de intenção?**

| Intenção | Significado |
|----|----|
| **Investimento - renda com aluguel** | Quer comprar para alugar e ter renda passiva |
| **Investimento - valorização** | Quer comprar para revender com lucro futuro |
| **Uso próprio - moradia** | Quer comprar para morar permanentemente |
| **Uso próprio - uso esporádico** | Quer comprar para usar de vez em quando (casa de praia/campo) |


---

### 🔧 Sobre Integrações

#### **Como funciona a integração com RD Station?**

> O sistema envia os leads com:
>
> * Dados básicos (nome, email, telefone)
> * Campos personalizados (empreendimento, intenção, valor, etc)
> * UTMs configuradas (traffic_source, traffic_medium)


---

#### **Como funciona a MIA?**

> MIA é a IA de envio de WhatsApp. Para funcionar, você precisa:
>
> * **Instance ID**: Identificador da instância (fornecido pela SZI)
> * **Product ID**: ID do produto/empreendimento (fornecido pela Morada)
> * **Message Template**: Template de mensagem aprovado (fornecido pela Morada)
> * **Source**: Origem do lead (fornecido pela Morada)
>
> ⚠️ **Atenção:** Não invente esses valores! Eles devem ser fornecidos oficialmente.


---

#### **Como funciona a integração com Pipedrive?**

> O sistema cria deals automaticamente com:
>
> * Dados do lead
> * Estágio correto (investidor ou corretor)


---

### Sobre o Baserow

#### **O que é o Baserow?**

> Baserow é um banco de dados no-code (similar ao Airtable). Ele armazena:
>
> * Configurações dos empreendimentos
> * Configurações dos formulários
> * Histórico de todos os leads
> * Referências (hunters, stages do Pipedrive, etc)


---

#### **Posso editar os leads manualmente no Baserow?**

> **Sim, mas não é recomendado.** A tabela Leads é preenchida automaticamente.
>
> Se você editar um lead:
>
> * ❌ Ele **NÃO será reprocessado**
> * ❌ Mudanças **NÃO propagam** para RD/MIA/Pipedrive
> * ✅ Útil apenas para **anotações internas**


---

## Tabelas de Referência

### Tabela: Empreendimentos

| **Função** | **Quem preenche** | **Campos principais** |
|----|----|----|
| Define as regras de qualificação MQL para cada empreendimento | Time de Marketing | * Formulário vinculado* Regras MQL (3 seções)
* Configurações de integrações
* Nome do Empreendimento |

### Tabela: Formulários

| **Função** | **Quem preenche** | **Campos principais** |
|----|----|----|
| Conecta Form IDs do Facebook aos empreendimentos | Time de Marketing | * Nome do Formulário
* Form ID (Facebook) |

### Tabela: Hunters

| **Função** | **Quem preenche** | Quando Usar? | **Você manipula?** |
|----|----|----|----|
| Lista de hunters por região para atribuição de corretores | Time de Marketing   | Consultar quando precisar saber quem é o hunter de uma região | * Raramente. Apenas se mudar hunters ou regiões. |


---

### Tabela: Stage Pipedrive

| **Função** | **Quem preenche** | Quando Usar? | **Você manipula?** |
|----|----|----|----|
|  IDs dos estágios do Pipedrive para criação de deals | Time de Marketing   |  Ao configurar um novo empreendimento | * Raramente. Apenas se criar novos estágios no Pipedrive. |

### Tabela: Leads

| **Função** | **Quem preenche** | **Quando Usar?** | Você manipula? |
|----|----|----|----|
| Histórico completo de leads processados | Sistema (automático) | * Verificar se lead foi processado
* Ver se qualificou como MQL
* Debugar problemas
* Análises e relatórios   | Não. Apenas leitura. |


---

## 🔗 Links Úteis

### Facebook

* [Facebook Ads Manager](https://business.facebook.com/adsmanager)
* [Gerenciar Campanhas](https://adsmanager.facebook.com/adsmanager/manage/campaigns)
* [Criar Formulários](https://business.facebook.com/latest/instant_forms/forms/?asset_id=144663558738581&business_id=3062589203783816&nav_source=flyout_menu&nav_id=2246342505)

### Baserow

* [Baserow SZI](https://baserow.seazone.com.br)
* [Formulário: Novo Empreendimento](https://baserow.seazone.com.br/form/dmI_h-9CoNgaK0S4ZmoBjvRUAbzabe_W37C41-N5CV0)
* [Formulário: Novo Formulário](https://baserow.seazone.com.br/form/owzhl7ZQbTwn358HWdCqlQWoXQLQZtt7B-xazos9UJo)
* [Tabela: Empreendimentos](https://baserow.seazone.com.br/database/253/table/1207/5209)
* [Tabela: Formulários](https://baserow.seazone.com.br/database/253/table/1209/5211)
* [Tabela: Leads](https://baserow.seazone.com.br/database/253/table/1210/5212)

### Documentação Relacionada

* [Guia Rápido de Configuração](#link-pagina-principal)
* [Sobre o Sistema](#link-subpagina-1)
* [Como Criar Campanhas no Facebook](#link-subpagina-2)
* [Entendendo Regras MQL](#link-subpagina-3)
* [Troubleshooting](#link-subpagina-4)


---

## 📖 Glossário

| Termo | Significado |
|----|----|
| **MQL** | Marketing Qualified Lead - Lead qualificado para ser contactado por vendas |
| **Form ID** | Identificador único do formulário no Facebook (número longo) |
| **n8n** | Plataforma de automação de workflows (como Zapier) |
| **Baserow** | Banco de dados no-code (similar ao Airtable) |
| **Webhook** | URL que recebe dados automaticamente quando algo acontece |
| **RD Station** | Plataforma de automação de marketing e CRM |
| **MIA** | Plataforma de envio de mensagens no WhatsApp |
| **Pipedrive** | CRM de vendas com pipeline visual |
| **Deal** | Oportunidade de venda no Pipedrive |
| **Stage** | Etapa do funil de vendas no Pipedrive |
| **Hunter** | Vendedor responsável por prospecção ativa de corretores |
| **Traffic Source** | Parâmetro UTM que indica de onde veio o tráfego |
| **Traffic Medium** | Parâmetro UTM que indica o tipo de mídia (ex: cpc, organic) |


---

## Checklist Rápido: Antes de Lançar Campanha

Use este checklist antes de ativar qualquer campanha:

### Facebook

- [ ] Campanha criada e ativa
- [ ] Formulário criado com todos os campos obrigatórios
- [ ] Form ID anotado
- [ ] Nome do empreendimento no dropdown (exato)
- [ ] Nome da campanha anotado
- [ ] ID da campanha anotado

### Baserow

- [ ] Empreendimento cadastrado
- [ ] Nome EXATAMENTE igual ao Facebook
- [ ] Regras MQL configuradas (3 seções)
- [ ] Configurações de integrações preenchidas
- [ ] Formulário cadastrado
- [ ] Form ID correto
- [ ] Formulário vinculado ao empreendimento

### Teste

- [ ] Lead de teste enviado
- [ ] Lead apareceu no Baserow (1-2 min)
- [ ] Qualificação MQL correta (True/False)
- [ ] Lead no RD Station
- [ ] WhatsApp recebido (se MQL)
- [ ] Deal criado no Pipedrive

### ✅ Tudo OK? Campanha pronta para rodar!


---

## 🔗 Navegação

* [← Voltar ao guia rápido](https://outline.seazone.com.br/doc/02-como-utilizar-ffCnjThwo0)
* [Sobre o sistema →](#link-subpagina-1)
* [Como criar campanhas →](https://outline.seazone.com.br/doc/22-como-criar-campanhas-VxQ1IQMvMi)
* [Troubleshooting →](https://outline.seazone.com.br/doc/24-troubleshooting-G6sGiwpXSp)