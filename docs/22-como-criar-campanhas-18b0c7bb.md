<!-- title: 2.2 - Como Criar Campanhas | url: https://outline.seazone.com.br/doc/22-como-criar-campanhas-VxQ1IQMvMi | area: Tecnologia -->

# 2.2 - Como Criar Campanhas

> **Guia completo para criar campanhas, formulários e encontrar IDs necessários**


---

## Estrutura de Campanhas 

No Facebook Ads, a hierarquia funciona assim:

```mermaidjs
%%{init: {'theme':'base', 'themeVariables': { 'primaryColor':'#4267B2','primaryTextColor':'#fff','primaryBorderColor':'#29487d','lineColor':'#666','secondaryColor':'#42B72A','tertiaryColor':'#1877F2'}}}%%
graph TD
    A[📢 Campanha]:::campanha --> B1[📊 Conjunto de Anúncios 1]:::conjunto
    A --> B2[📊 Conjunto de Anúncios 2]:::conjunto
    A --> B3[📊 Conjunto de Anúncios 3]:::conjunto
    
    B1 --> C1[📱 Anúncio 1]:::anuncio
    B1 --> C2[📱 Anúncio 2]:::anuncio
    
    B2 --> C3[📱 Anúncio 3]:::anuncio
    B2 --> C4[📱 Anúncio 4]:::anuncio
    
    B3 --> C5[📱 Anúncio 5]:::anuncio
    
    classDef campanha fill:#4267B2,stroke:#29487d,stroke-width:3px,color:#fff
    classDef conjunto fill:#42B72A,stroke:#2d7a1f,stroke-width:2px,color:#fff
    classDef anuncio fill:#1877F2,stroke:#0c5ccc,stroke-width:2px,color:#fff
```

**Resumo:** Campanha → Conjunto de Anúncios → Anúncios

Uma campanha pode ter vários conjuntos, e cada conjunto pode ter vários anúncios.


---

## Como Encontrar uma Campanha 

### Passo 1: Acessar o Facebook Ads Manager


1. Faça login no [Facebook Ads Manager](https://business.facebook.com/adsmanager)
2. Acesse a seção [Campanhas](https://adsmanager.facebook.com/adsmanager/manage/campaigns)
3. Visualize as campanhas ativas 
4. ![Lista de campanhas ativas ](/api/attachments.redirect?id=8bf48f8a-3d55-4b76-b0b5-3b8b4fb981e9 " =1284x893")

**Você verá uma tela assim:**

!\[Lista de campanhas no Facebook Ads Manager\]

> 💡 **Dica:** Use os filtros no topo para encontrar campanhas específicas por nome, status ou data.


---

## Como Encontrar o ID da Campanha

### Passo 1: Adicionar a coluna de ID

No painel de campanhas:

 ![](/api/attachments.redirect?id=3705db72-1105-422a-8dc1-b3cd07b321c9 " =1020x603")


1. Clique no ícone **"+"** na tabela de campanhas
2. ![](/api/attachments.redirect?id=58085d9c-e324-4832-9e9c-e39624088a6f " =286x147")
3. No campo "Colunas sugeridas", busque por **"Identificador"**
4. Selecione **"Identificador da campanha"**
5. Clique em **"Ativar"**

 ![Ativando IDs](/api/attachments.redirect?id=1c625e61-b48b-4ae9-b2d8-cfabaa5d1582 " =1026x661")

 ![VIsualização de IDs ativados](/api/attachments.redirect?id=f7c415c7-9f4d-419d-b814-84f9db9942f9 " =886x398")

### Passo 2: Copiar o ID

Agora você verá uma nova coluna com os IDs das campanhas.

**Exemplo de ID:** `192198393899319`

> ⚠️ **Importante:** Copie o ID completo, sem espaços extras.


---

## Como Acessar Formulários 

### Opção 1: Via Campanhas

 ![](/api/attachments.redirect?id=59053bc8-7fca-4fe3-b94a-5e739a55e42e " =1920x1080")


1. No painel de **Campanhas**, localize a campanha desejada
2. Clique em **"Anúncios para campanha"**
3. Os formulários vinculados aparecerão

 ![Formulários criados](/api/attachments.redirect?id=f8a06905-cea7-42d6-b8d3-156ff73d0ee1 " =911x672")

### Opção 2: Via Business Manager


1. Acesse [Business Manager > Formulários](https://business.facebook.com/latest/instant_forms/forms/)
2. Veja todos os formulários criados
3. Clique em um formulário para editá-lo


---

## Como Criar um Novo Formulário 


### Passo 1: Acessar criação de formulários


1. Tenha uma **campanha ativa**
2. Acesse [Criação de Formulários](https://business.facebook.com/latest/instant_forms/forms/?asset_id=144663558738581&business_id=3062589203783816&nav_source=flyout_menu&nav_id=2246342505)
3. Clique em **"Criar Novo Formulário"**
4. ![Criando um novo formulário](/api/attachments.redirect?id=a47b28df-c7cb-4abe-8b7a-785ed0e98154 " =1920x1080")

### Passo 2: Duplicar formulário existente

> 💡 **Recomendação:** Duplique um formulário existente e edite os campos. Isso mantém o padrão e evita erros.


1. Selecione um formulário similar
2. Clique em **"Duplicar"**
3. Edite o nome e campos conforme necessário

### Passo 3: Configurar campos

Adicione/edite os campos necessários (veja seção abaixo).

### Passo 4: Salvar e publicar


1. Revise todos os campos
2. Clique em **"Criar formulário"**
3. Anote o **Form ID** da URL

**Exemplo de URL:**

```
https://business.facebook.com/.../forms/1984062249106864/...
                                        └─── Este é o Form ID
```


---

## Campos Obrigatórios 

**TODOS os formulários devem ter estes campos:**

```
✅ Nome completo
✅ Email  
✅ Telefone
✅ Empreendimento (campo parâmetro)
✅ Você é corretor de imóveis? (Sim/Não)
```

### Campos Adicionais (Recomendados)

Para qualificação MQL, adicione:

```
☑️ Intenção de compra (dropdown):
   - Investimento - renda com aluguel
   - Investimento - valorização
   - Uso próprio - moradia
   - Uso próprio - uso esporádico

☑️ Faixa de investimento (dropdown):
   - R$ 50.000 a R$ 100.000
   - R$ 100.001 a R$ 200.000
   - R$ 200.001 a R$ 300.000
   - R$ 300.001 a R$ 400.000
   - Acima de R$ 400.000
   - Não consigo atender

☑️ Forma de pagamento (dropdown):
   - À vista via PIX ou Boleto
   - Parcelado via PIX ou Boleto
```

### Exemplo de Dropdown "Empreendimento"

O nome do empreendimento no dropdown **DEVE SER EXATAMENTE IGUAL** ao cadastrado no Baserow.

**Exemplos:**

```
✅ Correto: "Canas Beach Spot"
❌ Errado: "canas beach spot" (minúsculas)
❌ Errado: "Canas Beach Spot " (espaço extra)
❌ Errado: "Canas Beach" (incompleto)
```


---

## Onde Usar Essas Informações

Após criar/localizar sua campanha e formulário, você precisará destas informações para configurar no Baserow:

| Informação | Como Obter | Onde Usar |
|----|----|----|
| Form ID | URL do formulário no Business Manager | Cadastro de Formulários no Baserow |
| Nome do Empreendimento | Opção EXATA do dropdown | Cadastro de Empreendimentos no Baserow |
| Nome da Campanha | Nome visível no Ads Manager | Cadastro de Empreendimentos no Baserow |
| ID da Campanha | Coluna "ID da campanha" | Cadastro de Empreendimentos no Baserow |


---

## 🔗 Próximos Passos

Agora que você tem todas as informações:

👉 [Voltar ao guia de configuração](#link-pagina-principal) para cadastrar no Baserow


---

## 🔗 Links Relacionados

* [← Voltar ao guia rápido](https://outline.seazone.com.br/doc/02-como-utilizar-ffCnjThwo0)
* [Sobre o sistema →](https://outline.seazone.com.br/doc/21-sobre-o-sistema-xV4c2WMBXn)
* [Entender regras MQL →](https://outline.seazone.com.br/doc/23-entendendo-as-regras-mql-HuoVnk9Bi5)
* [Troubleshooting →](https://outline.seazone.com.br/doc/24-troubleshooting-G6sGiwpXSp)