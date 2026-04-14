<!-- title: 2.3 - FAQ e Refências | url: https://outline.seazone.com.br/doc/23-faq-e-refencias-XNksyMBdoX | area: Tecnologia -->

# 2.3 - FAQ e Refências

# 2.5 - FAQ e Referências - Marketplace

> 💬 Perguntas frequentes e informações de referência


---

## Perguntas Frequentes

### 🔧 Operacionais

#### **Preciso mexer no n8n ou em código?**

> **Não!** Tudo é configurado através do Baserow. Você nunca precisa acessar o n8n ou mexer em código.


---

#### **O que acontece se o ad_name não seguir o padrão?**

> O sistema não conseguirá extrair o nome do empreendimento e o lead não será processado.
>
> **Padrão obrigatório:** `[TAG1] [TAG2] prefixo_NomeDoEmpreendimento_data`


---

#### **Posso mudar as regras MQL depois de configurar?**

> **Sim!** As mudanças afetam apenas **novos leads**. Leads já processados não são requalificados.


---

#### **Quanto tempo leva para processar um lead?**

> **Tempo médio:** 30-60 segundos


---

#### **Como sei se algo deu errado?**

> Verifique o **canal de erros no Slack**: **#n8n-marketing-marketplace**


---

#### **Leads antigos são afetados por mudanças nas regras?**

> **Não.** Mudanças nas regras MQL afetam apenas leads futuros.


---

#### **Por que meu lead foi descartado?**

> O sistema verifica duplicidade. Se o `leadgen_id` já existe no Baserow, o lead é descartado automaticamente.
>
> **Motivo:** Facebook pode enviar webhooks duplicados.


---

#### **O que significa cada tipo de intenção?**

| Intenção | Significado |
|----|----|
| **Investimento - uso esporádico** | Quer comprar para usar de vez em quando |
| **Investimento - renda** | Quer comprar para alugar e ter renda passiva |
| **Investimento - valorização** | Quer comprar para revender com lucro futuro |
| **Uso próprio - moradia** | Quer comprar para morar permanentemente |


---

### 🔧 Sobre Integrações

#### **Como funciona a integração com RD Station?**

> O sistema envia os leads com:
>
> * Dados básicos (nome, email, telefone)
> * Campos personalizados (empreendimento, intenção, valor entrada, etc)
> * UTMs configuradas (traffic_source, traffic_medium, traffic_campaign)
>
> Status de envio fica registrado na coluna "RD Status" (success/failure)


---

#### **Como funciona a MIA?**

> MIA é a IA de envio de WhatsApp. Para funcionar, você precisa:
>
> **Para Investidores (Instance 1292):**
>
> * Instance ID: 1292
> * Product ID (fornecido pela Morada)
> * Message Template (fornecido pela Morada)
>
> **Para Corretores (Instance 1527):**
>
> * Instance ID: 1527
> * Product ID (fornecido pela Morada)
> * Message Template (fornecido pela Morada)
>
> **Comum:**
>
> * Source (fornecido pela Morada)
>
> ⚠️ **Atenção:** Não invente esses valores! Eles devem ser fornecidos oficialmente.


---

#### **Investidor não-MQL recebe WhatsApp?**

> **Não.** Apenas investidores MQL recebem WhatsApp da MIA.


---

#### **Corretor recebe WhatsApp?**

> **Sim, sempre!** Corretor sempre vai para MIA, sem qualificação MQL.


---

#### **O Pipedrive ainda é usado?**

> **Não.** No Marketplace, Pipedrive não é mais utilizado. Os leads vão para:
>
> * RD Station (sempre)
> * MIA (investidores MQL + todos os corretores)
> * Baserow (sempre)


---

### 📊 Sobre o Baserow

#### **O que é o Baserow?**

> Baserow é um banco de dados no-code (similar ao Airtable). Ele armazena:
>
> * Configurações dos empreendimentos
> * Histórico de todos os leads
> * Status de integrações (RD, MIA)


---

#### **Qual database do Marketplace?**

> **Database 332**
>
> Diferente do Lançamentos que usa database 253.


---

#### **Posso editar os leads manualmente no Baserow?**

> **Sim, mas não é recomendado.** A tabela Leads é preenchida automaticamente.
>
> Se você editar um lead:
>
> * ❌ Ele **NÃO será reprocessado**
> * ❌ Mudanças **NÃO propagam** para RD/MIA
> * ✅ Útil apenas para **anotações internas**


---

#### **O que significa cada status no Baserow?**

| Status | Valores | Significado |
|----|----|----|
| **Telefone Status** | valid/invalid | Telefone passou validação de DDD? |
| **MQL Status** | unqualified | Status MQL (fixo no momento da criação) |
| **RD Status** | success/failure | RD Station recebeu o lead? |
| **MIA Status** | success/failure/not_applicable | MIA recebeu o lead? |


---

## Tabelas de Referência

### Tabela: Empreendimentos

| **Função** | **Quem preenche** | **Campos principais** |
|----|----|----|
| Define regras MQL e configs de integrações | Time de Marketing | - Nome do Empreendimento<br>- Status (Ativo/Inativo)<br>- Regras MQL (2 seções)<br>- Configs RD/MIA/Slack |

**Importante:** Apenas empreendimentos com Status = "Ativo" são processados.


---

### Tabela: Leads

| **Função** | **Quem preenche** | **Quando Usar?** | Você manipula? |
|----|----|----|----|
| Histórico completo de leads processados | Sistema (automático) | - Verificar se lead foi processado<br>- Ver status de integrações<br>- Debugar problemas<br>- Análises e relatórios | Não. Apenas leitura. |


---

## 🔗 Links Úteis

### Facebook

* [Facebook Ads Manager](https://business.facebook.com/adsmanager)
* [Gerenciar Campanhas](https://adsmanager.facebook.com/adsmanager/manage/campaigns)
* [Criar Formulários](https://business.facebook.com/latest/instant_forms/forms/?asset_id=842763402253490)

### Baserow

* [Baserow Marketplace (DB 332)](https://baserow.seazone.com.br/database/332)
* [Tabela: Empreendimentos](https://baserow.seazone.com.br/database/332/table/1325)
* [Tabela: Leads](https://baserow.seazone.com.br/database/332/table/1330)

### Slack

* [Canal: #n8n-marketing-marketplace](https://seazone.slack.com)


---

## 📖 Glossário

| Termo | Significado |
|----|----|
| **MQL** | Marketing Qualified Lead - Lead qualificado (2 dimensões: intenção + valor entrada) |
| **Form ID** | Identificador único do formulário no Facebook |
| **leadgen_id** | ID único do lead gerado pelo Facebook |
| **ad_name** | Nome do anúncio no Facebook (usado para extrair empreendimento) |
| **n8n** | Plataforma de automação de workflows |
| **Baserow** | Banco de dados no-code (database 332 para Marketplace) |
| **Webhook** | URL que recebe dados automaticamente |
| **RD Station** | Plataforma de automação de marketing e CRM |
| **MIA** | IA de vendas via WhatsApp (instance 1292 investidor, 1527 corretor) |
| **Traffic Source** | Parâmetro UTM de origem do tráfego |
| **Traffic Medium** | Parâmetro UTM do tipo de mídia (ex: cpc) |
| **E.164** | Formato internacional de telefone (+5548999999999) |
| **Page ID** | ID da página Facebook (842763402253490 para Marketplace) |


---

## ✅ Checklist: Antes de Lançar Campanha

Use este checklist antes de ativar qualquer campanha:

### Facebook

- [ ] Campanha criada e ativa
- [ ] Formulário criado com campos obrigatórios
- [ ] Form ID anotado
- [ ] **Ad_name segue padrão:** `[TAG1] [TAG2] prefixo_Nome_data`
- [ ] Nome da campanha anotado
- [ ] ID da campanha anotado

### Baserow

- [ ] Empreendimento cadastrado
- [ ] Nome EXATAMENTE igual ao extraído do ad_name
- [ ] **Status = "Ativo"**
- [ ] Regras MQL configuradas (2 seções: intenção + valor entrada)
- [ ] Configs RD Station preenchidas
- [ ] Configs MIA Investidor preenchidas (instance 1292)
- [ ] Configs MIA Corretor preenchidas (instance 1527)
- [ ] Canal Slack configurado

### Validação de Nomenclatura

- [ ] Ad_name tem tags no início: `[TAG1] [TAG2]`
- [ ] Ad_name tem prefixo + underscore: `swot_`
- [ ] Nome do empreendimento vem após primeiro underscore
- [ ] Existe segundo underscore antes da data
- [ ] Extração manual confirma: nome extraído = nome no Baserow

### Teste

- [ ] Lead de teste enviado
- [ ] Lead apareceu no Baserow (1-2 min)
- [ ] Telefone Status = valid
- [ ] MQL Status = unqualified
- [ ] RD Status = success
- [ ] MIA Status = success (se MQL) ou not_applicable (se não-MQL)
- [ ] WhatsApp recebido (se investidor MQL ou corretor)
- [ ] Slack notificou sucesso

### ✅ Tudo OK? Campanha pronta para rodar!


---

## 🔗 Navegação

* [← Voltar ao guia rápido](https://outline.seazone.com.br/doc/02-como-utilizar-mIaj3t3hak)
* ← [Sobre o sistema](https://outline.seazone.com.br/doc/21-sobre-o-sistema-7m4zlzxtKS)
* ← [Troubleshooting ](https://outline.seazone.com.br/doc/22-troubleshooting-yac1qZtls5)


---

**Versão:** 2.0\n**Última atualização:** 13/11/2025\n**Elaborado para:** Equipe de Marketing SZI - Marketplace