<!-- title: Diário de Bordo - Amenities | url: https://outline.seazone.com.br/doc/diario-de-bordo-amenities-LxtM5v16Bj | area: Tecnologia -->

# Diário de Bordo - Amenities

Inicialmente foi verificado com o @[Alexandre Heckert Lentz (Xande)](mention://e08b779a-9fb1-447d-aaa8-bec6c292824a/user/f585b7b9-86fc-4a54-a960-e7fd1328338f) a implementação legada do fluxo de amenities e verificado como isso poderia ser útil para o novo fluxo automático de criação de amenities de anúncio na Stays. Sem muitos retornos, o que o código do AppScript de criação de anúncios fazia era algo muito parecido com o tratamento que já fazemos, então só seguimos o plano.


---

Verificamos também o que o backend do Sapron fazia no fluxo de criação de anúncios, relacionado à parte de amenities. Foram verificados na `pleno.py` e no `pleno_api.py` que o fluxo utilizava a tabela `amenity_item` do banco de dados, que tem todos os de → para do que vem na pleno e o que cada um referencia na Stays, com algumas informações acessórias:


 ![](/api/attachments.redirect?id=647eae3b-7880-41fe-a564-c267c86d3360 " =1536x381")


Contudo, essas definições estão defasadas - por algum motivo. Hoje, na pleno, os IDs do item estão totalmente diferentes. Contudo, foi possível reaproveitar toda a lógica d próprio backend do Sapron de `Buscar ID do Item no JSON → Olhar para a descrição do Item → Filtrar por "Possui" ou "Em bom estado" → Considerar como válido para o PATCH`. \n\nPara perpassar a problemática dos enums, foi criado uma tabela no database `hosting`, chamada `listing_amenities_rules` dentro do baserow com os De → Para com os IDs atuais da pleno:


 ![](/api/attachments.redirect?id=481f5f87-f482-4dd6-b0f4-ee52c3c71c90 " =1013x168")


\