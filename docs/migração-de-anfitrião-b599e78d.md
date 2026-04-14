<!-- title: Migração de Anfitrião | url: https://outline.seazone.com.br/doc/migracao-de-anfitriao-tWz3bEgNmG | area: Tecnologia -->

# Migração de Anfitrião

Solicitado em [SAP-1845](https://seazone.atlassian.net/browse/SAP-1845)


# Processo operacional

Em <https://sapron.com.br/editardados/mudar-anfitriao>: selecionar:

* Imóvel; 
* Novo anfitrião;
* Data de alteração.


---

# A requisição

## O que acontece por baixo dos panos:

Quando uma solicitação é enviada, validamos nessa ordem:

### Se há reservas ativas na data sugerida

* Verificamos se nenhum dos listings da propriedade tem reservas com:
* `check_in_date < data_da_requisição`;
* E `check_out_date > data_da_requisição`;
* E NÃO `is_blocking`;
* E `status = Concluded`.

  Se qualquer registro for retornado dessa query\*, retornamos o erro `active reservation in date of replacement`.

### Se há outra troca agendada para esse mesmo dia

* Verificar se na tabela `property_host_time_in_property` há registros com:
* O `property_id = propriedade_da_requisição`;
* E `replacement_date = data_da_requisição`;
* E `status = 'Pending'`.

  Se qualquer registro for retornado dessa query\*\*, retornamos o erro `this property already has a host switch in this replacement date`.

*OBS: Há uma validação pra ver se o Anfitrião foi alterado, mas atualmente não é possível editar isso formulário.*


---

### Se todas essas condições forem cumpridas e a data da troca for **HOJE**, a task de troca é executada imediatamente.


---

# A Task

Ela é executada diariamente às 23h no horário configurado no servidor (assumo que seja GMT -3, Sao Paulo/America).


A task, chamada internamente de `change_property_host_task`, pode ser ativada diretamente pela API, via endpoint PUT `property/change_property_host`.


## O que a task faz:

* Busca por trocas válidas de Anfitrião, na tabela `property_host_time_in_property`, com:
  * `replacement_date <= hoje`;
  * E `status = 'Pending'`;
* Então, verificamos se elas são válidas com os parâmetros:
  * MESMA validação de data feita na primeira seção (Caso tenham surgido reservas nesse meio tempo);
  * Se o anfitrião atual e o novo anfitrião são diferentes (Caso tenham feito alguma alteração no BD);

    **__⚠️__ Se uma dessas validações der problema, a troca tem status CANCELADA e é interrompida.**


* Feitas as validações, são alterados os registros:
  * `host_id` na `property_property`;
  * `host_responsible_id` na `reservation_reservation` onde `check_in_date` é maior ou igual a hoje e `status` não é 'Canceled';
  * `status` na `property_host_time_in_property` como "Done".

    \


---

## Queries:

\*Query de validação de reserva:

> `SELECT "reservation_reservation".*`
>
> `FROM "reservation_listing"`
>
> `INNER JOIN "reservation_reservation" ON ("reservation_listing"."id" = "reservation_reservation"."listing_id")`
>
> `WHERE ("reservation_listing"."property_id" = ID` << PROPERTY_ID
>
> `AND "reservation_reservation"."check_in_date" < '2024-XX-XX'` << DATA DE TROCA
>
> `AND "reservation_reservation"."check_out_date" > '2024-XX-XX'` << DATA DE TROCA
>
> `AND NOT "reservation_reservation"."is_blocking"`
>
> `AND "reservation_reservation"."status" = 'Concluded')`


\*\*Query de validação para outras trocas agendadas:

> `SELECT "property_host_time_in_property".*`
>
> `FROM "property_host_time_in_property"`
>
> `WHERE ("property_host_time_in_property"."property_id" = ID` << PROPERTY_ID
>
> `AND "property_host_time_in_property"."replacement_date" = '2024-XX-XX'` << DATA DE TROCA
>
> `AND NOT ("property_host_time_in_property"."status" IN ('Canceled', 'Done')))`