<!-- title: Conexão Pipefy | url: https://outline.seazone.com.br/doc/conexao-pipefy-nIsit60mam | area: Tecnologia -->

# Conexão Pipefy

Este guia explica como configurar a integração entre o **Pipefy** e o **n8n**.\nUsaremos como referência um fluxo já existente no nó de atendimento de suporte:\n[Exemplo de workflow](https://workflows.seazone.com.br/workflow/pjsnCdUpPP0i1R08)


---

## Passo 1 – Criar formulário com automação no Pipefy

No Pipefy, crie um formulário e configure uma automação.

* Defina o **trigger** desejado (card é criado, atualizado, etc).
* Selecione o tipo **HTTP Request**.

📹 Exemplo em vídeo:

[[TESTES-MIGRACAO] - Suporte governança - Pipefy _ The operations excellence platform.mp4 1280x698](/api/attachments.redirect?id=30000e4e-05f2-4d37-aaaf-a029e50bfa3a)

## Passo 2 – Configurar o Webhook no n8n

No n8n, adicione um **nó Webhook** para escutar a automação do Pipefy.


---

 ![](/api/attachments.redirect?id=0991f885-ca11-4c99-aa6c-91e426f40e03 " =1879x869")

* Copie a **Webhook URL** do n8n e cole na automação do Pipefy.

 ![](/api/attachments.redirect?id=83370b26-8503-4fbb-891d-c50e9eb11f39 " =899x360")

* O **método da requisição** deve ser o mesmo configurado no Pipefy (no exemplo, `POST`).

 ![](/api/attachments.redirect?id=136717d3-c3d1-4165-9936-6f05cb163398 " =1879x869")


## Passo 3 – Configuração no Pipefy

Na automação do Pipefy, configure:

* **Headers**

```http

Content-Type: application/json
```

                                                                                                                                                                                 ![](/api/attachments.redirect?id=56d75c31-844d-4b6c-83df-ba219cf5558a " =699x103")

* **Request Body**

  Use sintaxe **JSON**.\nOs campos podem ser definidos conforme mostrado no vídeo, outros campos como Json schema devem permanecer sem alterações:

[[TESTES-MIGRACAO] - Suporte governança - Pipefy _ The operations excellence platform (1).mp4 1280x720](/api/attachments.redirect?id=6cbc5c06-3097-4354-8470-5912347af7ac)

## Passo 4 – Teste da conexão


1. Deixe o nó do n8n em modo de escuta.
2. Preencha o formulário ou execute a ação automatizada configurada.
3. A resposta será retornada em **JSON**, podendo ser manipulada nos próximos nós do n8n.

📹 Exemplo prático:

[▶️ My workflow 16 - n8n.mp4 1280x698](/api/attachments.redirect?id=b0901e8b-8671-4102-ab15-8ccc15656647)


* Exemplo completo de fluxo com a conexão
* ![](/api/attachments.redirect?id=6e66a52f-ac57-4bb1-b424-2938017bc110 " =1470x490")


### \n**Extra - Pipefy Community Bundle**

Fica muito mais simples manipular informações de cards do Pipefy (ou de outras funcionalidades) utilizando o *bundle* de nós customizados do Pipefy, disponibilizado pela equipe de Governança.\nBasta informar o **ID do card**  que pode ser incluído no *request body* ao configurar a automação no Pipefy e repassá-lo para os nós do Pipefy ao receber no webhook n8n.

Esse processo está exemplificado em vídeo para facilitar o entendimento.


[nós customizados 1280x720](/api/attachments.redirect?id=4987e0dd-be49-4532-824d-88a73e4a1cd2)