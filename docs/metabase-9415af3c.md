<!-- title: Metabase | url: https://outline.seazone.com.br/doc/metabase-Ih3wD6F8VB | area: Administrativo Financeiro -->

# Metabase

# **==__________________Sobre_______________________==**

## *==———Descrição———————————-==*

* Código de requisição dos dados do metabase

## *==———Planilha Base———————————-==*

* [10.0 - Conciliação Reservas Sapron](https://docs.google.com/spreadsheets/d/1fbeqpusr2c2_wROOmLrDVAGxKMpo15MOrG1dPflrTFU/edit?gid=1748321476#gid=1748321476)
* [9.0 - Conciliação Reservas Sapron](https://docs.google.com/spreadsheets/d/1lP2f1RLk3aV0bhwHFbHG92_ORe36NNlCmUnRg-_tIQs/edit?gid=2097081422#gid=2097081422)

## *==———Documentação———————————-==*

* [Link da documentação](https://www.metabase.com/docs/latest/api#tag/apicard/GET/api/card/{id})

## *==———Sugestão———————————-==*

* "api/card"
  * É um código muito lento para requisição, além de precisar criar uma pergunta
  * O código via requisição de csv, permite a requisição de dados acima de 2000 linhas, porém o metabase tem o limite de requisição por csv que está por volta de 10.000 linhas
* "api/dataset"
  * Requer conhecimentos em SQL, mas é mais rápido para executar e não precisa criar perguntas

# **==__________________Scripts______________________==**

## *==———Puxar Dados do Metabase==*

### `v1` \*Desativado

* **Objetivo**: puxar dados via card

```jsx
function metabaseV1(){
  var optionsMetabase= {
    'method': 'post',
    'headers': { 'X-Metabase-Session': metabaseToken() }
  }

  var response = UrlFetchApp.fetch('https://metabase.seazone.com.br/api/card/726/query/csv', optionsMetabase);
  var metabaseFull = Utilities.parseCsv(response.getContentText())
}

/*---------------------------------------------------*/

function metabaseToken(){
  var metabaseURLToken = 'https://metabase.seazone.com.br/api/session'
  var metabaseUsername = 'administrativo@seazone.com.br'
  var metabasePassword = 'QKYNYqq5DzHDg6H'

  var optionsAPIMetabasekey = {
    'method': 'get',
    'headers': { 'Content-Type': 'application/json' },
    'payload': JSON.stringify({ 'username': metabaseUsername, 'password': metabasePassword })
  };
  var responsekey = UrlFetchApp.fetch(metabaseURLToken, optionsAPIMetabasekey);
  var key = JSON.parse(responsekey.getContentText())['id'];
  return key
}
```

### `v2`

* **Objetivo**: puxar os dados via card

```jsx
function metabaseV2(){
  var optionsMetabase= {
    'method': 'post',
    'headers': { 'X-API-KEY': "mb_shcnjo+0EYGKwXkKuCBmhF+z0R5Iy4Kb3VlnQkg0wRc=" }
  }

  var response = UrlFetchApp.fetch('https://metabase.seazone.com.br/api/card/574/query/csv', optionsMetabase);
  var metabaseFull = Utilities.parseCsv(response.getContentText())

  console.log(metabaseFull[1])
}
```

### `v3`

* **Objetivo**: puxar os dados via SQL

```jsx
function requestClosingSeazoneRevenue(){
  const url = 'https://metabase.seazone.com.br/api/dataset/json';
  const apiKey = 'mb_shcnjo+0EYGKwXkKuCBmhF+z0R5Iy4Kb3VlnQkg0wRc='; 

  var queryRequest =  `
    select 
      csr.reservation_id, 
      rr.code as reservation_code, 
      rr.stays_reservation_code, 
      
      case 
        when ro.name = 'Website Seazone' then 'Stays' 
        when ro.name = 'Madego' then 'Stays'
        else ro.name
      end as name_ota_ajustado,
        
      accs.first_name || ' ' || accs.last_name AS full_name,
      pp.code as property_code, 

      sum(
        case
          when transfer_category IN ('property_revenue', 'reservation_manual_fit') then
            case
              when transfer_type = 'output' then value
              else (-1) * value
            end
          else 0
        end
      ) as month_revenue,

      to_char(rr.seazone_fee, '999990.9999') as seazone_fee,
      to_char(rr.host_fee, '999990.9999') as host_fee, 
      count(csr.id) as diarias
   
    from 
      closing_seazone_resume csr 
      left join property_property pp on pp.id = csr.property_id  
      left join reservation_reservation rr on rr.id = csr.reservation_id  
      left join reservation_ota ro on ro.id = rr.ota_id 
      left join account_guest ag on ag.id = rr.guest_id 
      left join account_user accs on accs.id = ag.user_id 
      left join property_property_owners ppo on ppo.property_id = csr.property_id
    
    where 
      transfer_category in ('cleaning_fee', 'reservation_manual_fit','property_revenue','cleaning_manual_fit') 
      and date_trunc('month', cash_date) = TO_DATE('${2025-01-01}', 'YYYY-MM-DD') 
    
    group by 
      date_trunc('month', cash_date),
      csr.reservation_id,
      rr.code,
      rr.stays_reservation_code,
      accs.first_name, 
      accs.last_name,
      pp.code
 
    order by 
      csr.property_id
  `

  var optionsBase = {
    'method': 'POST',
    'contentType': 'application/x-www-form-urlencoded', // Define o Content-Type
    'muteHttpExceptions': true, // Para capturar erros HTTP e não deixar o script parar
    'followRedirects': true,  // Equivalente ao --location do cURL (já é o padrão)
    'headers': {'X-API-KEY': apiKey},
    'payload': {
      'query': JSON.stringify({
        database: 2, // ID do BD no metabase
        type: "native",
        native: {
          query: queryRequest
        }
      })
    }
  }

  var response = UrlFetchApp.fetch(url, optionsBase);  
  var metabaseFull = JSON.parse(response.getContentText())
  //console.log(metabaseFull)
  
  return metabaseFull
}
```