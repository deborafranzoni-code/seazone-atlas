<!-- title: Primeiro Acesso | url: https://outline.seazone.com.br/doc/primeiro-acesso-geIgBnXKKd | area: Tecnologia -->

# Primeiro Acesso

## Sobre o Vault

O HashiCorp Vault é nossa plataforma centralizada para gerenciamento de secrets (credenciais, tokens, API keys, etc.). Com ele você pode:

* Armazenar credenciais de forma segura
* Compartilhar secrets com o time sem exposição
* Manter histórico de alterações
* Rotacionar credenciais facilmente

> **⚠️ Política de Acesso:** a Seazone permite login APENAS via OIDC (Single Sign-On). Não use outros métodos de autenticação.


---

## Passo 1: Primeiro Login

### 1.1 Acessar a Interface Web


1. Abra seu navegador
2. Acesse a URL do Vault: <https://vault.seazone.com.br> 
3. Você verá a tela de login

### 1.2 Tela de Login - Método OIDC

 ![](/api/attachments.redirect?id=955778e8-9622-4ad9-8dd8-14fd72bacb2b " =1179x734")

Você verá uma tela com:

* **Method:** Já selecionado como "OIDC", caso não tiver: **selecione.**
* **Role:** pode deixar em branco
* **Botão azul:** "Sign in with Google"

> **🚨 IMPORTANTE:** Use APENAS o método OIDC. Outros métodos não funcionarão!

### 1.3 Fazer Login


1. Confirme que o campo **"Method"** está como **"OIDC"**
2. **Campo "Role":** Deixe em branco (o Vault usará o role padrão automaticamente)
3. Clique no botão azul **=="Sign in with Google"==**

### 2.4 Autenticar via Google Workspace


1. Você será redirecionado para a página de login do Google
2. Faça login com suas credenciais Seazone:
   * **E-mail Seazone** (@seazone.com.br)
   * **Senha** 
3. Autorize o acesso quando solicitado
4. Você será redirecionado automaticamente de volta ao Vault
5. ![Tela inicial - Vault](/api/attachments.redirect?id=c61b9b0a-1a38-4fd6-b5f8-83f082f6b8f8 " =1851x907")

**✅ Pronto!** Você está logado no Vault.



---

## Passo 3: Navegar pela Interface

### 3.1 Entendendo o Menu Lateral

Após o login, você verá o menu lateral com opções:

* **🏠 Secrets Engines** - Onde ficam seus secrets

**Para o dia a dia, você usará principalmente "Secrets Engines".**

### 3.2 Acessar Seus Secrets

 ![](/api/attachments.redirect?id=2cefb3d3-6715-40bd-be94-accf22f70170 " =769x517")


1. Clique em **"Secrets Engines"** no menu lateral
2. Clique no engine **"secret/"** (tipo KV v2)
3. Navegue até a pasta do seu time:

   ![](/api/attachments.redirect?id=ad12795f-4583-4c31-8bb6-74354f3cc68b " =1152x648")
   * Se você é do Marketing: `marketing/`
   * Se você é de Franquias: `franquias/`
   * Se você é do Produto: `produto/`

**Você só poderá as pastas para as quais tem permissão.**

## Como encontrar meu código OIDC?

Para liberar algumas pastas no Vault, as equipes de suporte geralmente precisarão do seu OIDC, abaixo como encontrar.

Documentação completa: @[Como localizar o código OIDC](mention://5132ac51-c2c9-4023-beef-bb29581b4e38/document/8600fd1b-d548-4436-80fc-580c65b9e3ae)

## Primeiros Passos Recomendados

### 1. Explorar os Secrets Existentes

Antes de criar novos secrets, veja o que já existe:


1. Navegue pela pasta do seu time
2. Clique em alguns secrets para ver a estrutura
3. Observe como as chaves estão organizadas (ex: `api_key`, `client_id`)

**Isso ajuda a manter consistência ao criar novos secrets.**

### 2. Criar Seu Primeiro Secret

Se você tem permissão de escrita, siga o guia: → @[Criação de um secret Vault](mention://369d4ec0-fa89-4a01-bb52-ec8a39df6def/document/1755f36a-03bd-4ac3-8d0f-43bf2cbaea63)


---

## Próximos Passos

Agora que você tem acesso ao Vault:


1. ✅ **Explorar** - Navegue pelos secrets do seu time
2. ✅ **Criar** - Siga o guia @[Criação de um secret Vault](mention://ac914719-d662-428f-9f06-306da89b5e49/document/1755f36a-03bd-4ac3-8d0f-43bf2cbaea63)
3. ✅ **Editar** - Aprenda a atualizar secrets existentes @[Edição de um secret Vault](mention://53031d39-eb6c-4373-9feb-36943f863d0a/document/b98da699-ba03-4f2c-944d-dd29cfbc7f5f)