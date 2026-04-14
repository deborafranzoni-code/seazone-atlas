<!-- title: Documentação Técnica | url: https://outline.seazone.com.br/doc/documentacao-tecnica-ioZNZGYcF6 | area: Tecnologia -->

# Documentação Técnica

# Fonte de Dados

O dashboard foi construído utilizando o dataset **lake_observability** disponível no BigQuery. Para a construção do BI, foram utilizados as seguintes tabelas:

* mape_history: Tabela principal de auditoria. Contém os dados importantes para a análise do MAPE com a menor granularidade possível (diária).
* mape_granularity_analysis: Identificar ofensores macro (Estado, Strata, Quartos).
* mape_ranked_properties: Tabela de detalhe dos imóveis.


# Consultas personalizadas criadas no Looker Studio

Devido a utilização de parâmetros de períodos, foi necesário criar consultas personalizadas no Looker Studio, passando esses intervalos como parâmetros nas queries. Essas consultas personalizadas foram criadas em duas tabelas diferentes, disponíveis nas fontes adicionadas do BI.

## mape_global

Essa fonte de dados possui a consulta personalizada para filtrar os dados no intervalo escolhido pelo usuário. Os parâmetros são: `@intervalo_a` e `@intervalo_b`.

```sql
with mape_grouped_before as (
  select
    airbnb_listing_id,
    case
      when actual_revenue != 0
        then abs(estimated_revenue - actual_revenue) / actual_revenue
      when actual_revenue = 0 and estimated_revenue = 0
        then 0
      else null
    end as mape_global,
  	case
      when actual_occupied != 0
        then abs(actual_occupied - occupied) / actual_occupied
      when actual_occupied = 0 and occupied = 0
        then 0
      else null
    end as mape_occupied,
    case
      when actual_blocked != 0
        then abs(actual_blocked - blocked) / actual_blocked
      when actual_blocked = 0 and blocked = 0
        then 0
      else null
    end as mape_blocked,
  	case
      when actual_price != 0
        then abs(price - actual_price) / actual_price
  	  when actual_price = 0 and price = 0
  		then 0
      else null
    end as mape_price,
    case 
        when abs(estimated_revenue - actual_revenue) != 0 and actual_revenue = 0
        then 1
        else null
      end as is_inf
  from (
    select
    	airbnb_listing_id,
    	sum(actual_revenue) as actual_revenue,
      	sum(estimated_revenue) as estimated_revenue,
      	sum(case when occupied = true then 1 else 0 end) as occupied,
      	sum(case when actual_occupied = true then 1 else 0 end) as actual_occupied,
    	sum(case when blocked = true then 1 else 0 end) as blocked,
      	sum(case when actual_blocked = true then 1 else 0 end) as actual_blocked,
    	sum(case when occupied = true and actual_occupied = true then price else 0 end) as price,
    	sum(case when occupied = true and actual_occupied = true then actual_revenue else 0 end) as actual_price,
    from `data-resources-448418.lake_observability.mape_history`
    where
      date(updated_at) = current_date()
      and date between current_date() - interval (@intervalo_a + 1) day
                   and current_date() - interval '1' day
      and date_of_birth <= current_date() - interval (@intervalo_a + 1) day
      and (date_of_death is null or date_of_death >= current_date() - interval 1 day)
    group by airbnb_listing_id
  ) 
),

mape_grouped_after as (
  select
    airbnb_listing_id,
    case
      when actual_revenue != 0
        then abs(estimated_revenue - actual_revenue) / actual_revenue
      when actual_revenue = 0 and estimated_revenue = 0
        then 0
      else null
    end as mape_global,
    case
      when actual_occupied != 0
        then abs(actual_occupied - occupied) / actual_occupied
      when actual_occupied = 0 and occupied = 0
        then 0
      else null
    end as mape_occupied,
    case
      when actual_blocked != 0
        then abs(actual_blocked - blocked) / actual_blocked
      when actual_blocked = 0 and blocked = 0
        then 0
      else null
    end as mape_blocked,
    case
        when actual_price != 0
          then abs(price - actual_price) / actual_price
        when actual_price = 0 and price = 0
          then 0
        else null
      end as mape_price,
    case 
        when abs(estimated_revenue - actual_revenue) != 0 and actual_revenue = 0
        then 1
        else null
      end as is_inf
  from (
    select
      	airbnb_listing_id,
      	sum(actual_revenue) as actual_revenue,
      	sum(estimated_revenue) as estimated_revenue,
      	sum(case when occupied = true then 1 else 0 end) as occupied,
        sum(case when actual_occupied = true then 1 else 0 end) as actual_occupied,
    	sum(case when blocked = true then 1 else 0 end) as blocked,
      	sum(case when actual_blocked = true then 1 else 0 end) as actual_blocked,
    	sum(case when occupied = true and actual_occupied = true then price else 0 end) as price,
    	sum(case when occupied = true and actual_occupied = true then actual_revenue else 0 end) as actual_price,
    from `data-resources-448418.lake_observability.mape_history`
    where
      date(updated_at) = current_date()
      and date between current_date() - interval (@intervalo_b + 1) day
                   and current_date() - interval '1' day
      and date_of_birth <= current_date() - interval (@intervalo_b + 1) day
      and (date_of_death is null or date_of_death >= current_date() - interval 1 day)
    group by airbnb_listing_id
  ) 
)

select before.mape_global as before_mape_global, before.mape_occupied as before_mape_occupied,
	before.mape_blocked as before_mape_blocked, before.mape_price as before_mape_price, before.is_inf as before_is_inf,
	after.mape_global as after_mape_global, after.mape_occupied as after_mape_occupied, 
	after.mape_blocked as after_mape_blocked, after.mape_price as after_mape_price, after.is_inf as after_is_inf
from mape_grouped_before before
full outer join mape_grouped_after after
on before.airbnb_listing_id = after.airbnb_listing_id
```


## error_decomposition

Essa consulta foi criada para pegar a porcentagem dos erros de bloqueio, ocupação e preço.

```sql
SELECT 'Bloqueio' AS tipo_erro, block_mape_ratio AS media_ratio
FROM `data-resources-448418.lake_observability.mape_ranked_properties`
UNION ALL
SELECT 'Ocupação' AS tipo_erro, occupancy_mape_ratio AS media_ratio
FROM `data-resources-448418.lake_observability.mape_ranked_properties`
UNION ALL
SELECT 'Preço' AS tipo_erro, price_mape_ratio AS media_ratio
FROM `data-resources-448418.lake_observability.mape_ranked_properties`
```


Além disso, todas as métricas utilizaram as tabelas citadas anteriormente e foram seguidas de acordo com a documentação.

Link do dashboard: <https://lookerstudio.google.com/reporting/59bed237-fbc1-4006-81e3-50fc8964ba93/page/x0SkF>

Link da documentação: @[Auditoria do MAPE - DashBoard](mention://17b6bc25-eaf6-47e6-989c-e8be01b3107d/document/3a965f2d-d7d6-4571-abd5-c82971972eac)