<!-- title: Dados Bancarios - Proprietário ou Franqueado | url: https://outline.seazone.com.br/doc/dados-bancarios-proprietario-ou-franqueado-80F4Fg7ycN | area: Tecnologia -->

# Dados Bancarios - Proprietário ou Franqueado

Um dos dados sensíveis dos usuários seja proprietários ou franqueados é os dados bancários vinculados a cada registro. Todos os registros de dados bancários estão registrados na tabela `Financial Bank Details` esses registros podem estar vinculados a:

* Proprietário  - `account_owner > default_bank_details_id`
* Imóvel          -  `property_property > bank_details_id`
* Fraqueado   -  `account_host > default_bank_details_id`


Ao registrar os dados bancários de um proprietário, também deve ser vinculado ao imóvel ou imoveis do proprietário. 

No Sapron, ao editar os dados bancários do proprietário, devem ser vinculados ao imóvel.   


### Tarefa operacional: Vincular os dados bancários do proprietário aos imóveis dele. 

Neste exemplo do proprietário de e-mail `antoniod.leite@hotmail.com` tem UserID `**263826**`


\
 ![](/api/attachments.redirect?id=084c97bc-70d8-4fd0-ac8f-fd1c9326365b " =1092x145")


\
Pesquisar os imóveis associados ao proprietário.

O registro do `account_owner > default_bank_details_id = 2706` deve ser inserido na Tabela `property_property > bank_details_id` ficando de essa forma


\
 ![](/api/attachments.redirect?id=9ebfe9fc-2eae-41ee-9b65-0834f829d596 " =1255x224")


\
Os dados na tabela `Financial Bank Details `ficaram assim, vinculadas ao `UserID` do proprietário


 ![](/api/attachments.redirect?id=ac12da21-e4ed-4cd9-9d27-1c1205143049 " =1556x200")


\