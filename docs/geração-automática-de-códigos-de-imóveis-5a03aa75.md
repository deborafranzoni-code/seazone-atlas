<!-- title: Geração automática de códigos de imóveis | url: https://outline.seazone.com.br/doc/geracao-automatica-de-codigos-de-imoveis-WXeRKhehwi | area: Tecnologia -->

# 🔢 Geração automática de códigos de imóveis

🖥️ **Projeto/Sistema:** Onboarding/n8n \n🗓️ **Criado em:** 6 de janeiro de 2026 \n🔄 **Atualizado em:** 6 de janeiro de 2026 às 15:35 \n👥 **Autores:** @[Aridan Silva Pantoja](mention://7f472257-656e-4b8f-86de-5fb70d6453a2/user/15233988-fd3f-4e3d-977a-932d59e65f23) @[Karol Wojtyla Sousa Nascimento](mention://54046304-6a2e-4368-a035-c096f1df4006/user/a171b710-1218-4034-9406-e6b14888bd9f) \n✅ **Status:** Homologação 


---

### 📝 Descrição

Este fluxo automatizado no n8n gera códigos de identificação únicos (SKUs) para imóveis cadastrados no Pipedrive. O sistema utiliza Inteligência Artificial (Google Gemini) para comparar os dados do novo imóvel com uma base de conhecimento no Google Sheets ("Base V2 - Homologação").

O objetivo é evitar duplicidade de cadastros e padronizar as siglas dos condomínios. O fluxo recebe o ID do negócio, consulta os detalhes (endereço, número, complemento), verifica a base histórica e decide se reutiliza uma sigla existente ou cria uma nova. Ao final, o código gerado é atualizado no Pipedrive e notificado no canal do Slack.


---

### 🚦 Status de Retorno da IA

A IA analisa a similaridade semântica entre o imóvel de entrada e a base de dados. Abaixo estão os status possíveis e seus gatilhos:

#### 1. `MATCH_FOUND` (Correspondência Encontrada)

* **Quando ocorre:** A IA identifica que o **nome do condomínio** e o **endereço (rua + número)** são idênticos ou extremamente similares a um registro já existente na planilha.
* **Ação do Sistema:** O fluxo recupera a sigla existente (ex: "RSO") e gera o código final apenas adicionando o número do apartamento/unidade do novo negócio.

#### 2. `REVIEW_REQUIRED` (Revisão Necessária)

* **Quando ocorre:**
* O endereço (Logradouro + Número) coincide com um registro da base, mas o nome do condomínio é diferente (ex: "Edifício Solar" vs "Residencial Solar").
* A similaridade detectada pela IA está numa zona cinzenta (ambiguidade entre 70% e 90%).
* **Ação do Sistema:** O sistema opta pela segurança e reutiliza a sigla vinculada ao endereço encontrado para manter a consistência, mas marca o registro com um alerta para conferência humana posterior.

#### 3. `NEW_CODE` (Novo Código)

* **Quando ocorre:** Não foi encontrada nenhuma correspondência de endereço ou nome de condomínio na base de dados atual.
* **Ação do Sistema:**
* A IA gera uma **nova sigla** de 3 letras baseada no nome do empreendimento (ex: "Torres do Bosque" -> "TDB").
* O sistema formata o número da unidade (apto). Caso seja uma casa ou não tenha número de unidade, aplica a regra de sufixo `0000`.
* Um novo registro é criado na planilha "Base V2".


---

### 🔌 Manual de Integração (Webhook)

Este fluxo deve ser acionado via requisição HTTP (Webhook). Abaixo estão os detalhes técnicos para configuração no Pipedrive (Automações) ou via Postman/Insomnia.

**Detalhes do Endpoint:**

* **URL de Teste:** `https://webhook-n8n.seazone.com.br/webhook/generate-property-code`
* **Método HTTP:** `POST`
* **Autenticação:** Basic Auth
  * User: `generate-bot`
  * Password: `pSE3zCzo7UWVzcwurePWMSQ0xAH3AbMy`

**Estrutura do Body (JSON):** O sistema espera receber um objeto JSON contendo a chave `dealId` (número inteiro).

```json
{
  "dealId": 203745
}
```

**Respostas da API:**

| Código HTTP | Significado | Descrição |
|----|----|----|
| **201 Created** | **Sucesso** | O código foi gerado e o imóvel atualizado no Pipedrive. Retorna o `propertyCode` gerado. |
| **400 Bad Request** | **Erro de Requisição** | O `dealId` não foi enviado ou não é um número válido. |
| **404 Not Found** | **Não Encontrado** | O ID do negócio informado não existe no Pipedrive. |
| **409 Conflict** | **Conflito/Duplicidade** | O imóvel já possui um código preenchido anteriormente OU o código que o sistema tentou gerar já existe na base para outro imóvel (prevenção de colisão). |


---

### 🔔 Notificações

* **Canal:** `#teste-gerador` (Slack)
* **Gatilho:** Enviado sempre que um novo registro é adicionado à base (`NEW_CODE`) ou quando um código é gerado com sucesso.
* **Conteúdo:** Informa o Nome do Imóvel, a Sigla Gerada e o Link para o Pipedrive.