<!-- title: Gmail - Service Account | url: https://outline.seazone.com.br/doc/gmail-service-account-LZgz8cd1aj | area: Tecnologia -->

# Gmail - Service Account

**Para que serve:** Autenticar automações do N8N que precisam acessar Gmail (enviar/ler emails) usando uma conta de serviço do Google Cloud.


---

## Informações da Conta

### Identificação

* **Email da Service Account:** `qa-relatorios-automaticos-spri@tecnologia-465914.iam.gserviceaccount.com`
* **Project ID:** `tecnologia-465914`
* **Escopo:** Apesar do nome mencionar "relatórios", esta conta pode ser usada em **qualquer automação que envolva Gmail**

### Chave Privada

A chave privada completa está disponível no secret Vault no seguinte link 

[https://vault.seazone.com.br/ui/vault/secrets/secret/kv/Ferramentas%2Fn8n_gmail_service_account(key)/details](https://vault.seazone.com.br/ui/vault/secrets/secret/kv/Ferramentas%2Fn8n_gmail_service_account(key)/details?version=1)

> ⚠️ **SEGURANÇA:** Mantenha esta key em local seguro. Nunca compartilhe publicamente ou versione em repositórios públicos.


---

## 🔧 Como Configurar no N8N

### 1. Adicionar Credencial Gmail


1. No N8N, vá em **Credentials** → **Add Credential** → **Gmail OAuth2 API**
2. Selecione **Service Account**

   ![](/api/attachments.redirect?id=9f5ba720-87aa-40f8-b93f-ecfb33e618e2 " =1168x758")
3. Mantenha o campo `'Region'` com o valor original setado pelo n8n, outros campos preencha com as informações fornecidas nessa documentação.

### 2. Configurar Impersonation (Personificação)

Para enviar emails **como se fosse outro usuário**:

✅ **RECOMENDAÇÃO PARA SEU CONTEXTO:**

* Marque a opção **"Impersonate User"** no node do Gmail
* Use o email: `automacao.governanca@seazone.com.br`

**Analogia:** A Service Account é como um "cartão de acesso universal" que pode agir em nome de qualquer funcionário autorizado. O "Impersonate User" define qual funcionário ela está representando naquele momento.

### 3. Mensagem de Erro Conhecida

> 🐛 **Bug conhecido:** O N8N pode exibir erro de configuração da credencial durante o teste, mas **a credencial funcionará normalmente**. Ignore o alerta e prossiga.


---

## 💡 Quando Usar Esta Conta

**Use esta Service Account quando:**

* Precisa enviar emails automáticos do Gmail
* Precisa gerenciar labels Gmail
* Precisa ler/buscar emails programaticamente
* Está criando workflows de automação que interagem com Gmail

**Diferença de OAuth normal:**

* OAuth normal = usuário autoriza pessoalmente
* Service Account = autorização programática, sem interação humana


---

## Notas Adicionais

* > * A conta está no projeto Google Cloud `tecnologia-465914`
  > * O Client ID é: `104712109136178137347`
  > * Todas as permissões necessárias já estão configuradas no Google Cloud Console