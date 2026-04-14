<!-- title: Franquia - Atualizar Taxa de franquia | url: https://outline.seazone.com.br/doc/franquia-atualizar-taxa-de-franquia-Q3CiPd96Rc | area: Tecnologia -->

# Franquia - Atualizar Taxa de franquia

Os dados da taxa de Franquia são salvos na tabela `Financial Host Franchise Fee` 


Procurar o ID  do Host a partir dos dados no suporte, pode ser nome, email

<https://metabase.seazone.com.br/question/1146-account-host-user-by-hostid>


Quando é cobrança da taxa de Franquia é na Tabela `financial_host_franchise_fee_payment`

Query para deletar registro da taxa: `DELETE FROM public.financial_host_franchise_fee_payment`

`WHERE id= ;`