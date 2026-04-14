<!-- title: Query para Fechamento do Mês | url: https://outline.seazone.com.br/doc/query-para-fechamento-do-mes-0fSD5UpGM0 | area: Tecnologia -->

# Query para Fechamento do Mês

**Visão do Imóvel:** Os dados referentes a a este cenário são disponibilizados no link <https://sapron.com.br/fechamentoimovel>

A query a seguir obtém os dados de faturamento de reservas para um imóvel em um mês:

```
select property_id, date_trunc('month', check_out_date) AS res_month,
  sum(total_price) as total_price,
  sum(daily_net_value) as faturamento,
  sum(paid_amount) as paid_amount,
  sum(ota_comission) as ota_comission,
  sum(net_cleaning_fee) as cleaning_fee,
  sum(pp.comission_fee*daily_net_value) as comission
from reservation_reservation rr
join reservation_listing rl on rr.listing_id = rl.id
join property_property pp on pp.id=rl.property_id
where date_trunc('month', rr.check_out_date) = '2024-04-01' 
  and rl.property_id = 901
  and rr.status<>'Canceled'
group by property_id, res_month;
```

* Saldo Inicial:
* Faturamento:
* Receita:
* Comissão:
* Despesas:
* Ajuste Imóvel Proprietário:
* Repasse:
* Saldo Final:
* \