<!-- title: Repasses | url: https://outline.seazone.com.br/doc/repasses-AsgC7uJAaa | area: Tecnologia -->

# Repasses

## Inserir Repasse via Template

Usar o template  [link](https://docs.google.com/spreadsheets/d/1wF_Bv-I4bu8OolivpHJT0jpF7hJgi6PyAwP11hEo5kM/edit?usp=sharing)

[https://docs.google.com/spreadsheets/d/1wF%5FBv-I4bu8OolivpHJT0jpF7hJgi6PyAwP11hEo5kM/edit?usp=sharing](https://docs.google.com/spreadsheets/d/1wF%5FBv-I4bu8OolivpHJT0jpF7hJgi6PyAwP11hEo5kM/edit?usp=sharing)


## Deletar repasse que foi inserido por engano 

Procurar na `Financial Owner Property Ted`  pelo `PropertyID` e verificar quais registros precisam ser deletados, após o fechamento deve refletir no sapron.

==Caso não encontre na== `Financial Owner Property Ted`==, olhar também a coluna *source* da== `Closing Host Resume` ==para identificar onde está o dado que precisa ser alterado ou deletado.==


*Query para Deletar Repasse:* `DELETE FROM public.financial_owner_property_ted`

`WHERE id=000;`