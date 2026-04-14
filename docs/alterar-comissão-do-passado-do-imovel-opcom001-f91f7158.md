<!-- title: Alterar comissão do passado do Imovel - OPCOM001 | url: https://outline.seazone.com.br/doc/alterar-comissao-do-passado-do-imovel-opcom001-mYMyhjoz4f | area: Tecnologia -->

# Alterar comissão do passado do Imovel - OPCOM001

### Dados necessários:


1. `property_id` ou `code` do imóvel;
2. Data de início para a alteração.
3. Dado da nova comissão

### O que fazer:


1. A partir da tabela `property_audit` , procure pelas linhas da propriedade e as ordene por `changed_at` ascendente; [link metabase](https://metabase.sapron.com.br/question/1087-comision-property-audit-by-propertycode) 
2. Altere o campo de comissão (seja `comission_fee` ou `host_cleaning_comission_fee`) e garanta que a data do campo `changed_at` bata com a data de início.

Ex:

Foi solicitado que a propriedade VEC112 tenha comissão de 20% até 30/04/2024 e 22% a partir dali, então o resultado da `property_audit` vai de:


 ![](/api/attachments.redirect?id=f3fd9700-f173-4941-9ee9-bd911fca3651)


Para:


 ![](/api/attachments.redirect?id=9669046f-0fd7-4118-a5d4-cee759ef7af9)


Desse modo, pra cálculos até a data de `changed_at` na linha 3 vão ser calculadas com a comissão de 20%.

> 🚨  Problemas conhecidos
>
> Atualmente (05/08/2024), por causa do processo de fechamento precisar ser calculado na AWS, as alterações só são visíveis depois dele rodar novamente. No momento, isso acontece automaticamente todo dia pelo início da madrugada, mas também pode ser feito manualmente 


---

Se o mês da data `changed_at` é março, as reservas pegam a comission-fee para março e é fechamento em em abril


## OPCOM002 - Alterar comissão do passado nas Reservas


**Dados necessários:**


1. `property_id` ou `code` do imóvel;
2. Data de início para a alteração.
3. Dado da nova comissão

Verificar se a comissão estiver certa na `Property Audit`  pelo `property_id` ou `code` do imóvel;

Identificar o `code` das reservas na `Proper Pay Property Daily Transfer`  Filtrando pelo `property_id`   e pelo `type=revenue`, e pela data(mês inteiro) da nova comissão  em `Cash Date`

Verificar na `Reservation` se a comissão nas reservas estão conforme


**O que fazer**

Atualizar na `reservation` a `Property Fee` é `Seazone Fee` conforme o necessário

**Exemplo**

Ex. Comissão de 25% para março e abril.

* Na `Property Audit` parece ok
* A somatória dos valores da  `Proper Pay Property Daily Transf ` deve dar o soma da receita do mês de abril
* Na `reservation` procurar pelo `code` extraindo da coluna `Proper Pay Property Daily Transf > Description>reservationcode` 
* Na tabela `Reservation` o comissão esta 0,2 (20%)


 ![](/api/attachments.redirect?id=5bfbf50e-8d8f-4341-84f9-5378cec57675 " =1142x246")


\

 ![](/api/attachments.redirect?id=519afb87-b5af-4d23-900b-e907ccbf47b6 " =1340x545")


\

 ![](/api/attachments.redirect?id=c7df7af5-5fc1-4af2-b762-c3d61deb70a1 " =1363x223")


\
##