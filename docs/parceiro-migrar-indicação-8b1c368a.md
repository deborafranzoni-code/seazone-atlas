<!-- title: Parceiro - Migrar indicação | url: https://outline.seazone.com.br/doc/parceiro-migrar-indicacao-5l95GqoD5f | area: Tecnologia -->

# Parceiro - Migrar indicação

# Migrar indicação

Dados necessários:


1. `partner_id` (tabela `account_partner`, geralmente a partir do campo `email` em `account_user` ) do parceiro antigo e do parceiro novo.
   * <https://metabase.seazone.com.br/question/1233-account-partner-user>

O que fazer:

Dependendo do suporte

Alterar nas tabelas, encontrar o registro pelo `partner_ID` do antigo parceiro

*  `partners_indication_investment` - indicação de investimento
* `partners_indication_property` - indicação de propriedade
* `partners_indication_allotment` - indicação de terreno

Mudar o campo `partner_id`  do antigo parceiro para o novo partnerid do novo parceiro.

>  ⚠️ É normal que uma ou duas tabelas estejam sem indicações pro partner_id, eles podem fazer indicação em somente um formulário, mas se nas 3 tabelas não forem encontrados registros de indicação, um de três problemas aconteceu:
>
> 
> 1. O usuário mencionou o parceiro errado;
> 2. O dev pegou o partner_id errado;
> 3. Por algum motivo, as indicações foram associadas com o partner_id errado (se o pipedrive_person_id não é encontrado na account_user, o SAPRON deixa partner_id = 1 nas indicações. Use essa informação para debuggar e conversar com o cliente). Nesses casos, verifique os campos pipedrive_deal_id nas tabelas que o possuem.


\