<!-- title: Recuperação de Carrinho | url: https://outline.seazone.com.br/doc/recuperacao-de-carrinho-cfBvxlbfa7 | area: Tecnologia -->

# Recuperação de Carrinho

# Utilização do Take Blip para Recuperação de Reservas

## Contexto

O Take Blip é uma plataforma robusta para integração com o WhatsApp, permitindo a automação de mensagens e a criação de fluxos inteligentes de comunicação. Este documento analisa a viabilidade técnica de utilizar o Take Blip para enviar mensagens automatizadas pelo WhatsApp com o objetivo de recuperar reservas não concluídas em um website.

## Objetivo

Implementar uma solução que envie mensagens automáticas via WhatsApp para clientes que iniciaram uma reserva, mas não a finalizaram. O objetivo é aumentar a taxa de conversão de reservas.


<complementar com a mari>


## Detalhamento Técnico

### 1. Integração com a API do Take Blip

1\.1 Setup

- [ ] Acesso a Blip no chatbot roteador (<https://seazone.blip.ai/application/detail/hospedesseazone1/home>)\nLista de templates: <https://seazone.blip.ai/application/detail/hospedesseazone1/contents/messagetemplate>
- [ ] Coleção da Blip no Postman 

  [Blip.postman_collection.json 308515](/api/attachments.redirect?id=56fd209e-ecf7-4d9e-85a1-46940fd8dc10)

- [ ] **API_KEY** no vault: <https://vault.sapron.com.br/ui/vault/secrets/secrets/show/Tecnology/BLIP>


1\.2 Conceitos Básicos da BLIP

No Take Blip, as mensagens enviadas pelo WhatsApp podem ser classificadas em dois tipos principais:


1. **Mensagens Ativas**
   * São mensagens enviadas de forma proativa pela empresa para o cliente, sem que ele tenha iniciado a conversa.
   * Devem seguir um **template** aprovado pelo WhatsApp.
   * São cobradas de acordo com a precificação do WhatsApp Business.
   * Exemplos: lembrete de reserva, atualização de pedido, mensagens promocionais permitidas.
2. **Mensagens Passivas (Sessão de Atendimento)**
   * São mensagens enviadas dentro de uma janela de 24 horas após o cliente iniciar a conversa.
   * Podem ser mensagens livres, sem necessidade de template.
   * Não há cobrança adicional além do custo da sessão ativa.
   * Exemplos: respostas a dúvidas do cliente, suporte técnico, acompanhamento de pedidos.

As mensagens para recuperação de reserva seriam **mensagens ativas**, pois são enviadas mesmo sem o cliente iniciar contato. Isso implica a necessidade de **opt-in do cliente** e uso de **templates** aprovados pelo WhatsApp.


1\.3 Enviado a mensagem

Docs referencia: <https://help.blip.ai/hc/pt-br/articles/4474382664855-Como-enviar-notifica%C3%A7%C3%B5es-WhatsApp-via-API-do-Blip>\n

 ![](/api/attachments.redirect?id=953da893-d5f5-4d48-8e2c-878fdb293191)


as variáveis dessa requisição são as seguintes:\n