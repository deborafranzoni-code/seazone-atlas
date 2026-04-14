<!-- title: Criação de um secret Vault | url: https://outline.seazone.com.br/doc/criacao-de-um-secret-vault-GzZ0tbfISR | area: Tecnologia -->

# Criação de um secret Vault

## Criando um Secret pela UI

### Passo 1: Navegar até o Local Correto


1. No menu lateral, clique em **"Secrets Engines"**
2. Clique no engine **"secret/"** (KV v2)
3. Navegue até a pasta do seu time, exemplo: `marketing/`

   ![](/api/attachments.redirect?id=24d296fc-bbcd-4f69-ade8-09a616c7cf33 " =1152x648")

### Passo 2: Criar um Novo Secret


1. Clique no botão **"Create secret +"** (canto superior direito)

   ![](/api/attachments.redirect?id=b4a393c3-ed67-4a18-a121-700849ec2594 " =665x236")
2. Preencha os campos:

   \

**Path (Caminho):**

```
marketing/rd-station
```

* Use kebab-case (letras minúsculas com hífen)
* Exemplo: `facebook-leads`, `baserow-tokens`, `n8n-webhooks`

  ![](/api/attachments.redirect?id=2fee0f46-8852-439e-97d8-062a8237c7c4 " =696x388")

**Version data (Dados):**

Adicione pares chave-valor clicando em **"+ Add"**:

| Key (Chave) | Value (Valor) |
|----|----|
| `api_key` | sua-api-key-aqui |
| `client_id` | seu-client-id-aqui |
| `client_secret` | seu-client-secret-aqui |


3. Clique em **"Save"** (canto inferior)

### Passo 3: Verificar o Secret


1. O secret aparecerá na lista
2. Clique nele para ver os detalhes
3. ![](/api/attachments.redirect?id=bdfad5ff-ab99-48ae-8f03-e4c5421e84e3 " =625x179")
4. Use o ícone de **olho** (👁️) para revelar valores ocultos


---

## Editando um Secret


1. Abra o secret que deseja editar
2. Clique em **"Create new version +"** (canto superior direito)
3. Modifique os campos necessários
4. Clique em **"Save"**

**Importante:** Isso cria uma nova versão, mantendo histórico


---

## Deletando um Secret


1. Abra o secret
2. Clique no menu **"⋮"** (três pontos)
3. Escolha:
   * **"Delete"** - Remove a versão atual (recuperável)
   * **"Destroy"** - Remove permanentemente (não recuperável)


---

## Estrutura de Caminhos Recomendada

Na UI, navegue e organize seus secrets seguindo este padrão:

```
secret/
├── marketing/
│   ├── facebook-ads
│   ├── rd-station
│   ├── pipedrive
│   └── n8n
├── devops/
│   ├── aws
│   ├── gcp
│   └── cloudflare
└── [seu-time]/
    └── [seu-projeto]
```


---

## Boas Práticas

**Nomenclatura:**

* Use kebab-case: `rd-station` não `RD_STATION`
* Seja descritivo: `facebook-leads-prod` não `fb-1`

**Organização:**

* Crie pastas por time/projeto navegando e clicando em "Create secret +"
* Separe ambientes: `-prod`, `-staging`, `-dev` no nome

**Segurança:**

* Nunca tire screenshot dos valores dos secrets
* Nunca compartilhe secrets por Slack/email
* Use o botão copiar (📋) ao invés de digitar
* Rotacione secrets periodicamente

**Chaves comuns para APIs:**

* `api_key` - Chave de API
* `client_id` - ID do cliente
* `client_secret` - Secret do cliente
* `token` - Token de acesso
* `webhook_url` - URL de webhook


---

## Copiando Valores


1. Abra o secret
2. Clique no ícone **👁️** para revelar o valor
3. Clique no ícone **📋** (copiar) ao lado do valor
4. Cole no n8n ou onde precisar


---

## Versionamento

O Vault mantém histórico automático de todas as alterações:


1. Abra o secret
2. Clique na aba **"Version History"**
3. Veja todas as versões anteriores
4. Clique em uma versão para ver os valores daquele momento

**Útil para:** Recuperar valores antigos ou auditar mudanças


---

## Troubleshooting

**Não consigo criar secret:**

* Verifique se sua solicitação de permissão foi aprovada
* Confirme se está na pasta correta do seu time

**Não vejo o botão "Create secret +":**

* Você não tem permissão de escrita nesse caminho
* Solicite permissão ao DevOps

**Secret não aparece no n8n:**

* Confirme o caminho correto no Vault
* Verifique se o n8n está configurado para ler desse caminho
* Aguarde alguns minutos para sincronização.