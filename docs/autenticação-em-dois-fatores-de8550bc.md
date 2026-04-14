<!-- title: Autenticação em Dois Fatores | url: https://outline.seazone.com.br/doc/autenticacao-em-dois-fatores-nakWN5hSvS | area: Tecnologia -->

# Autenticação em Dois Fatores

Com finalidade de aumentar a segurança em fluxos críticos, um fluxo de **Autenticação em Dois Fatores** (2FA) será implementada.

O fluxo enviará uma chave de confirmação composta por um número de 4 dígitos aleatórios para o email cadastrado do usuário. Essa chave então será utilizada para validar a identidade do usuário em fluxos sensíveis.


# Fluxos Sensíveis

Fluxos que demonstrem a necessidade da utilização do 2FA devem seguir o fluxograma a baixo.

 ![Fluxograma de fluxos sensíveis](/api/attachments.redirect?id=4a10b68a-3d13-4400-b4f6-28d9c110ca60 " =1282x469")

# Geração de código e envio por email


 ![](/api/attachments.redirect?id=055fdaa9-35a9-4280-9cef-9f32561435d0)

# Validação do código


 ![](/api/attachments.redirect?id=81cc754e-0cf8-4f54-b7c3-886b49b45d5d)


---

## Links úteis

* :pencil2: [Diagramas](https://drive.google.com/file/d/1M9b6202yL91slAOYPPGjr6zhQzESMPZz/view?usp=sharing)