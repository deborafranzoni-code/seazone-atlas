<!-- title: Edição de um secret Vault | url: https://outline.seazone.com.br/doc/edicao-de-um-secret-vault-w0Qqhnpsca | area: Tecnologia -->

# Edição de um secret Vault

## Passo 1: Localizar o Secret

 ![](/api/attachments.redirect?id=24d296fc-bbcd-4f69-ade8-09a616c7cf33 " =1152x648")


1. No menu lateral, clique em "Secrets Engines"
2. Clique no engine "secret/" (KV v2)
3. Navegue até a pasta do seu time (ex: `marketing/`)
4. Localize e clique no secret que deseja editar

## Passo 2: Criar Nova Versão

 ![](/api/attachments.redirect?id=74932ac4-d210-4b94-9a77-35005c961fed " =1920x1080")



1. Clique na aba "Secret" do secret

   ![](/api/attachments.redirect?id=5d96fd4a-e77d-44b5-bfca-4745d1f66a02 " =1029x345")

   \
2. Clique em "Create new version +" (canto superior direito)

   ![](/api/attachments.redirect?id=d593f8df-daf7-4577-9f72-26a41f48d24a " =1434x493")
3. A tela mostrará os valores atuais do secret
4. Modifique os campos necessários:

   ![](/api/attachments.redirect?id=5055fd9e-e986-4a0f-aae9-18ed6fed8045 " =1920x1080")

   \
   * **Para editar um valor existente:** Altere o campo "Value"
   * **Para adicionar nova chave:** Clique em "+ Add" e preencha
   * **Para remover uma chave:** Clique no ícone "🗑️" ao lado dela

**Exemplo de atualização:**

| Key | Value Atual | Novo Value |
|----|----|----|
| `api_key` | antiga-key-123 | nova-key-456 |
| `client_id` | abc123 | abc123 (mantido) |


4. Clique em "Save" (canto inferior)

## Passo 3: Verificar a Atualização


1. O secret mostrará "Version 2" (ou número sequencial)
2. Use o ícone 👁️ para confirmar os novos valores
3. Verifique a data de atualização no topo da página

## Quando Editar vs. Quando Criar Novo Secret

**Edite o secret existente quando:**

* Atualizar credenciais que expiraram (rotação de senha/token)
* Corrigir valores incorretos
* Adicionar novas chaves ao mesmo serviço
* O caminho/propósito do secret permanece o mesmo

**Crie um novo secret quando:**

* For um serviço/projeto completamente diferente
* Precisar separar ambientes (`-prod`, `-staging`)
* A estrutura de dados for muito diferente

**→ Para o seu contexto: Se está apenas atualizando credenciais do mesmo serviço (ex: nova API key do RD Station), EDITE o existente. Só crie novo se for outro projeto/ambiente.**

## Importante: Sistema de Versionamento

* Cada edição cria uma **nova versão** automaticamente
* Versões anteriores são **preservadas** (não são apagadas)
* Você pode **recuperar** valores antigos via "Version History"

**Analogia:** É como um Google Docs - cada "Save" cria um checkpoint que pode ser recuperado depois.

## Recuperando Versão Anterior

Se precisar voltar para valores antigos:


1. Abra o secret
2. Clique na aba "Version History"
3. Selecione a versão desejada (ex: "Version 1")
4. Clique em "Copy version data" (📋)
5. Volte para a versão atual
6. Clique "Create new version +"
7. Cole os dados antigos
8. Clique "Save"

## Boas Práticas de Edição

**Quando editar:**

* Notifique o time se o secret for compartilhado
* Teste a nova credencial antes de salvar (se possível)

**Após editar:**

* Verifique se aplicações que usam esse secret continuam funcionando
* \