<!-- title: Looker Studio (Data Studio) | url: https://outline.seazone.com.br/doc/looker-studio-data-studio-jQv4Eud1oE | area: Tecnologia -->

# Looker Studio (Data Studio)

## Sobre


---

O Looker Studio é uma ferramenta **gratuita** que transforma seus dados em relatórios e painéis informativos totalmente personalizáveis, fáceis de ler e de compartilhar. *Saiba mais sobre [como criar relatórios](https://support.google.com/looker-studio/answer/6309867).*

Com o Looker Studio, você tem fácil acesso às informações de uma ampla variedade de fontes sem a necessidade de programação. É possível se conectar rapidamente a conjuntos de dados. *Saiba mais sobre [como se conectar aos seus dados](https://support.google.com/looker-studio/answer/6268208).*

***Fonte: ****<https://support.google.com/looker-studio/answer/6283323?hl=pt-BR>*

[Looker Studio: visualizações do Business Insights | Google Cloud](https://cloud.google.com/looker-studio?hl=pt_br)

## Conexões do Dashboard | [Site Seazone | Analytics e Reservas](https://lookerstudio.google.com/u/0/reporting/a2475a55-acd3-4374-9dea-c26c74968272/page/p_rchy3q9hcd)


---

### Conexão com o Google Analytics 4


---

Conectado ao GA4 do Website (seazone.com.br)

### Conexão com BD do Sapron


---

***Obs.:*** *Necessário adicionar os IPs do Looker Studio no Security Group do BD.*

* Query Customizada de conexão

  ```sql
  SELECT reservation_reservation.id, 
         reservation_reservation.created_at, 
         reservation_reservation.updated_at, 
         reservation_reservation.check_in_date, 
         reservation_reservation.check_out_date, 
         reservation_reservation.total_price as valor_liquido_gateway,
         reservation_reservation.daily_net_value as valor_liquido_seazone, 
         reservation_reservation.ota_comission as comissao_ota, 
         reservation_reservation.status, 
         reservation_ota."name" as ota, 
         property_property.code as codigo_imovel, 
         account_address.street, 
         account_address."number", 
         account_address.complement, 
         account_address.neighborhood, 
         account_address.city, 
         account_address.state, 
         account_address.postal_code, 
         account_address.country
  FROM reservation_reservation
  LEFT JOIN reservation_listing ON reservation_reservation.listing_id = reservation_listing.id 
  LEFT JOIN reservation_ota ON reservation_listing.ota_id = reservation_ota.id 
  LEFT JOIN property_property ON reservation_listing.property_id = property_property.id 
  LEFT JOIN account_address ON property_property.address_id = account_address.id
  WHERE reservation_reservation.status = 'Concluded'
     AND (reservation_ota.name <> 'Blocking' OR reservation_ota.name IS NULL)
     AND property_property.code <> 'TST001'
  ;
  ```

### Links Úteis


---

[Connect to PostgreSQL - Looker Studio Help](https://support.google.com/looker-studio/answer/7288010?sjid=3980168794673537174-SA)