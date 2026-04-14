<!-- title: Método de Validação Whatsapp | url: https://outline.seazone.com.br/doc/metodo-de-validacao-whatsapp-b7j2m2ENGT | area: Tecnologia -->

# Método de Validação Whatsapp

## **Visão Geral**

Quando um proprietário envia uma mensagem pelo WhatsApp, o bot precisa saber quem é aquela pessoa antes de responder com dados financeiros ou de imóveis. Essa identificação acontece de forma transparente, no melhor caso, o usuário nem percebe que foi identificado.

A fonte de verdade dos dados do proprietário é o banco **SAPRON** (tabela `account_user`). O resultado da identificação, o vínculo entre número de WhatsApp e `user_id`, é armazenado no **DynamoDB** para consultas futuras instantâneas.


\