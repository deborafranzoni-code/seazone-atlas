<!-- title: Propriedade não aparece em site reservas | url: https://outline.seazone.com.br/doc/propriedade-nao-aparece-em-site-reservas-fsGUSyKJQ5 | area: Tecnologia -->

# Propriedade não aparece em site reservas

# Decrição de padrão

Em alguns casos onde a propriedade não é encontrada dentro do site da Seazone, ou links que deveriam levar à página de detalhamentos da propriedade no site de reservas resulta em "404" (Não encontrado), é possível que o anúncio da propriedade esteja como *hidden*.


Dentro do banco de dados do Sapron, isso pode ser verificado na tabela `property_listing`, na coluna `status_stays`. Já no banco de dados de reservas, a coluna `status_stays` se encontrará na tabela de propriedade.


# Solução

A fim de solucionar a problemática, deve ser suficiente alterar o status do anúncio da propriedade alterando-o através da Stays.

Dentro das configurações do imóvel, na Stays, ao selecionar "Distribuição" e "ChannelManager", o card com título "Site" deve estar com status "Não conectado" (conforme imagem a seguir)

 ![](/api/attachments.redirect?id=e29bce90-af35-4d1c-ae51-aaf54d27040d " =1127x934")

Acessando as configurações do card "Site" (clicando no card, ou em uma seta no canto extremo direito) é possível acessar a seguinte página, onde mostra-se um botão com texto "Conectar":

 ![](/api/attachments.redirect?id=7ecd564b-a1df-482e-b3f8-2e30a0c42527 " =2260x1139")

Selecionando o botão "Conectar", o status do anúncio deve ser alterado para "active" na API da stays. No entanto, a alteração desse status nos sistemas da Seazone podem ser demorados - uma vez que dependem ou de webhooks ou de workers periódicos.

 ![](/api/attachments.redirect?id=99395bc9-404c-4abd-905f-972c5ad8358a " =2260x1139")

No momento em que o status da propriedade for alterado, no banco de dados de Reservas, para "active" (ao invés de "hidden"), espera-se que o imóvel esteja acessível no site, e que os links para esse estejam operacionais.


\