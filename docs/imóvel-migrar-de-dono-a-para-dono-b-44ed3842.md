<!-- title: Imóvel - Migrar de Dono A para Dono B | url: https://outline.seazone.com.br/doc/imovel-migrar-de-dono-a-para-dono-b-dznFzJN5Un | area: Tecnologia -->

# Imóvel - Migrar de Dono A para Dono B

## Alterar Proprietário (login) de uma propriedade

Dados necessários:


1. `property_id` ; Do imóvel que deseja migrar
2. `owner_id` ; Do novo Dono


O que fazer:

Alterar nas **==2 tabelas==** os seguintes campos com o novo OwnerID

* **==Property Property Owners ==**

Na tabela `property_property_owners`, procure pelo `property_id`a linha da propriedade e altere o `owner_id` relacionado a ela. 

<https://metabase.seazone.com.br/question/1184-property-owners-by-property-code>


* **==Property Property==** 

  Procure pelo `property_id` que é para migrar e altere o campo `owner_id` com o novo ID do novo dono


\
## Erros de Criação de imóvel


Algumas vezes são criadas imoveis com os donos errados nesses casos precisamos migrar para uma conta de teste que tem os seguintes dados

* **Account_Owner_ID 311  - userID 17402  - email teste@seazone.com.br** 
* Mude o código do imovel adicionando o TST na frente, exemplo se o imóvel for RFM0018 mude para TSTRFM0018