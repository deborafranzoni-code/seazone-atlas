<!-- title: Puxar os dados da AWS / Metabase | url: https://outline.seazone.com.br/doc/puxar-os-dados-da-aws-metabase-YHPFJWcbk8 | area: Administrativo Financeiro -->

# Puxar os dados da AWS / Metabase

---

## Descrição

Todas as tabelas usadas para a construção do fechamento pelo Sapron são criadas e alteradas pela AWS fechamento-staging, porém para facilitar o acesso, todos os dados serão dispostos no Metabase, com os mesmos nomes de tabelas


## Pontos Relevantes

Os dados da Seazone são inseridos na tabela daily_property_transfer

* **Lista de Termos** (Definição dos termos utilizados)

  Descrição dos Stakeholders do Fechamento

| Termos | Descrição |
|:---|:---|
| Host | informações sobre o anfitrião |
| Owner | informações sobre o proprietário |
| Property | informações sobre a propriedade |
| Partner | informações sobre o parceiro |
| Seazone | informações sobre a Seazone |

  \
  Formas de consolidação dos dados

| Termos | Descrição |
|:---|:---|
| Monthly | dados consolidados por mês |
| Daily | dados gerados por dia |
| Financial | dados originais ou dados brutos |

  \
  Dados analisados

| Termos | Descrição |
|:---|:---|
| Account | dados iniciais dos stakeholdes do fechamento |
| Reservation | dados sobre as reservas |
| Time | período em que o stakeholder esteve responsável pelo imóvel |
| Indications | parceiro responsável pela indicação do imóvel |
| Handover | dados sobre as imóvel |
| NF | dados de Notas Fiscais |
| Balance | saldo inicial (termo equivalente do sheets) |
| Cleaning | limpeza (termo equivalente do sheets) |
| Expenses | despesas (termo equivalente do sheets) |
| Commission | comissão (termo equivalente do sheets) |
| Fee | taxa cobrada pela Seazone, parceiro ou anfitrião pelos serviços prestados |
| Manual-Fit | ajustes (termo equivalente do sheets) |
| Revenue | receita de todas as OTAs (termo equivalente do sheets) |
| Transfer | valor de repasse |
| Implantation Fee | taxa de implantação do imóvel (termo equivalente do sheets) |
| **OTA** | são as os sites de reservas utilizados pela Seazone para controle de reservas (Booking, Airbnb, Decolar, etc) |
| **Audit** | as tabelas com "Audit", são tabelas que mostram os Logs (alterações realizadas na tabela original) |

  \


## Links

Para acessar o **Metabase**, utilize o seguinte link: <https://metabase.sapron.com.br/>

E para login e senha, utilize o **Vault**: <https://vault.sapron.com.br/ui/vault/auth?with=userpass>

Para a relação entre imóvel, proprietário, anfitrião e parceiro, com seus respectivos IDs **property-owner-host-partner:** <https://metabase.sapron.com.br/question/220-property-owner-host-partner>

Para acessar o **Sanity Check**: <https://docs.google.com/spreadsheets/d/1TxUPzQfoDuWA5AzUbO-L_hkJEN-ouq7l-wvi82n-L1I/edit#gid=118163771>

E para ver o **extrato dos imóveis**: <https://metabase.sapron.com.br/question/247-extrato-imoveis>

Para uma **descrição de cada coluna**: [https://www.notion.so/Descri-o-de-tabelas-055a588f8ded44f88f7d5348a87530b4#12a6b2bff03440f99b188959ee5e5c96](https://www.notion.so/055a588f8ded44f88f7d5348a87530b4?pvs=21)


# Tabelas Ativas


---

* **Tabelas Gerais** (tabelas de conexões com outras tabelas, ou dados iniciais/brutos)

| AWS ⇒ Metabase | Colunas | Definição |
|:---|:---|:---|
| account_user<br><br>[Account User](https://metabase.sapron.com.br/question#eyJkYXRhc2V0X3F1ZXJ5Ijp7ImRhdGFiYXNlIjoyLCJ0eXBlIjoicXVlcnkiLCJxdWVyeSI6eyJzb3VyY2UtdGFibGUiOjc3fX0sImRpc3BsYXkiOiJ0YWJsZSIsInZpc3VhbGl6YXRpb25fc2V0dGluZ3MiOnt9fQ==) | id<br>password<br>last_login<br>is_superuser<br>created_at<br>updated_at<br>first_name<br>last_name<br>email<br>phone_number1<br>phone_number2<br>main_role<br>gender<br>birth_date<br>is_individual<br>id_number<br>cpf<br>cnpj<br>corporate_name<br>trading_name<br>is_staff<br>is_active<br>main_address_id<br>postal_address_id<br>nickname<br>pipedrive_person_id<br> | tabela com todos os dados gerais sobre todos os stakeholders externos da Seazone, contendo informações de contato, dados pessoais e IDs para conexão com outras tabelas.<br><br><br>\*\*\*Obs:\*\* para usar essa tabela, é necessário conecta-la as tabelas de Account (Owner, Host e Partner), pois são elas que possuem o IDs que conectam as demais tabelas Daily e Monthly com a Account User<br><br><br>**Ex:<br><br>**Tabelas Account User (Coluna ID)<br>🔃<br>(Coluna user_id)<br><br>Tabela Account Host<br>(Coluna user_id)<br>🔃<br><br>Tabela daily_host_balance<br>(Coluna host_id)<br><br> |
| property_property_owners<br><br>[Property Property Owners](https://metabase.sapron.com.br/question#eyJkYXRhc2V0X3F1ZXJ5Ijp7ImRhdGFiYXNlIjoyLCJ0eXBlIjoicXVlcnkiLCJxdWVyeSI6eyJzb3VyY2UtdGFibGUiOjczfX0sImRpc3BsYXkiOiJ0YWJsZSIsInZpc3VhbGl6YXRpb25fc2V0dGluZ3MiOnt9fQ==) | id<br>property_id<br>owner_id<br> | Tabela para identificação de relação entre imóvel e proprietário |
| owner_time_in_property<br><br>[Property Owner Time In Property](https://metabase.sapron.com.br/question#eyJkYXRhc2V0X3F1ZXJ5Ijp7ImRhdGFiYXNlIjoyLCJ0eXBlIjoicXVlcnkiLCJxdWVyeSI6eyJzb3VyY2UtdGFibGUiOjE3fX0sImRpc3BsYXkiOiJ0YWJsZSIsInZpc3VhbGl6YXRpb25fc2V0dGluZ3MiOnt9fQ==)\* | date<br>property_id<br>owner_id<br> | Tabela para identificação de relação entre imóvel e proprietário, por dia |
| property_host_time_in_property<br><br>[Property Host Time In Property](https://metabase.sapron.com.br/question#eyJkYXRhc2V0X3F1ZXJ5Ijp7ImRhdGFiYXNlIjoyLCJ0eXBlIjoicXVlcnkiLCJxdWVyeSI6eyJzb3VyY2UtdGFibGUiOjE0fX0sImRpc3BsYXkiOiJ0YWJsZSIsInZpc3VhbGl6YXRpb25fc2V0dGluZ3MiOnt9fQ==) | id<br>property_id<br>new_host_id<br>old_host_id<br>replacement_date<br>created_at<br>updated_at<br> | Tabela para identificação de relação entre imóvel e anfitrião, por dia |
| host_time_in_property | date<br>host_id<br>property_id<br> | Tabela para identificação de relação entre imóvel e anfitrião, por dia |
| reservation_listing<br><br>[Reservation Listing](https://metabase.sapron.com.br/question#eyJkYXRhc2V0X3F1ZXJ5Ijp7ImRhdGFiYXNlIjoyLCJ0eXBlIjoicXVlcnkiLCJxdWVyeSI6eyJzb3VyY2UtdGFibGUiOjMxfX0sImRpc3BsYXkiOiJ0YWJsZSIsInZpc3VhbGl6YXRpb25fc2V0dGluZ3MiOnt9fQ==) | id<br>created_at<br>updated_at<br>ota_fee<br>id_in_ota<br>title_in_ota<br>ota_id<br>property_id<br> | Tabela que mostra a relação do valor da taxa da OTA, e demais dados das OTAs por reserva de cada imóvel |
| reservation_reservation<br><br>[Reservation Reservation](https://metabase.sapron.com.br/question#eyJkYXRhc2V0X3F1ZXJ5Ijp7ImRhdGFiYXNlIjoyLCJ0eXBlIjoicXVlcnkiLCJxdWVyeSI6eyJzb3VyY2UtdGFibGUiOjI4fX0sImRpc3BsYXkiOiJ0YWJsZSIsInZpc3VhbGl6YXRpb25fc2V0dGluZ3MiOnt9fQ==) | id<br>created_at<br>updated_at<br>code<br>check_in_date<br>check_out_date<br>check_in_time<br>check_out_time<br>total_price<br>is_blocking<br>blocking_reason<br>recommended_by<br>comment<br>paid_amount<br>guest_name_ota<br>adult_guest_quantity<br>child_guest_quantity<br>daily_net_value<br>ota_comission<br>net_cleaning_fee<br>status<br>has_pet<br>is_late_extension<br>has_late_extension<br>is_early_extension<br>has_early_extension<br>added_by_id<br>early_extension_reservation_id<br>guest_id<br>host_responsible_id<br>late_extension_reservation_id<br>listing_id<br>original_reservation_id<br>is_pre_checkin_completed<br>conciliada<br>bed_arrangement<br>is_monthly<br>monthly_contract_uid<br>child_0_6_guest_quantity<br>child_6_12_guest_quantity<br>early_checkin_at<br>late_checkout_at<br>need_cradle<br>baby_guest_quantity<br>stays_creation_date<br>is_pre_checkin_link_sent<br>link_sent_at<br>pre_checkin_fullfilled_at<br>cleaning_fee_value<br>extra_fee<br>gross_daily_value<br>ota_fee<br>cupom_discount<br>manual_discount<br> | Tabela com o histórico das reservas dos imóveis de todas as OTAs, administrados pela Seazone e por seu parceiro<br><br>Essa tabela detalha as informações de hospedagem<br> |
| financial_expenses<br><br>[Financial Expenses](https://metabase.sapron.com.br/question#eyJkYXRhc2V0X3F1ZXJ5Ijp7ImRhdGFiYXNlIjoyLCJ0eXBlIjoicXVlcnkiLCJxdWVyeSI6eyJzb3VyY2UtdGFibGUiOjg0fX0sImRpc3BsYXkiOiJ0YWJsZSIsInZpc3VhbGl6YXRpb25fc2V0dGluZ3MiOnt9fQ==) | id<br>register_date<br>expense_date<br>reason<br>description<br>supplier<br>value<br>expense_status<br>refund<br>owner_approval<br>property_id<br>maintenance_image_uid<br>statement_image_uid<br>registered_by<br>responsible_user<br>pending_reason<br>paid_by<br>supplier_rating<br>approval_date<br>approval_user<br>supplier_phonenumber<br> | Tabela que contem todo o histórico de despesas dos imóveis administrados pela Seazone<br><br>Essas despesa são registradas pelo respectivo anfitrião do imóvel, e são divididas por diversas categorias e direcionado ao responsável de reembolsar o valor pago pelo anfitrião<br> |
| financial_host_manual_fit<br><br>[Financial Host Manual Fit](https://metabase.sapron.com.br/question#eyJkYXRhc2V0X3F1ZXJ5Ijp7ImRhdGFiYXNlIjoyLCJ0eXBlIjoicXVlcnkiLCJxdWVyeSI6eyJzb3VyY2UtdGFibGUiOjUyfX0sImRpc3BsYXkiOiJ0YWJsZSIsInZpc3VhbGl6YXRpb25fc2V0dGluZ3MiOnt9fQ==) | id<br>created_at<br>updated_at<br>date_ref<br>value<br>is_adding<br>host_id<br>description<br> | Tabela com os ajustes manuais direcionados para o anfitrião |
| financial_owner_manual_fit<br><br>[Financial Owner Manual Fit](https://metabase.sapron.com.br/question#eyJkYXRhc2V0X3F1ZXJ5Ijp7ImRhdGFiYXNlIjoyLCJ0eXBlIjoicXVlcnkiLCJxdWVyeSI6eyJzb3VyY2UtdGFibGUiOjU3fX0sImRpc3BsYXkiOiJ0YWJsZSIsInZpc3VhbGl6YXRpb25fc2V0dGluZ3MiOnt9fQ==) | id<br>created_at<br>updated_at<br>date_ref<br>value<br>is_adding<br>owner_id<br>description<br> | Tabela com os ajustes manuais direcionados para o proprietário |
| financial_property_manual_fit<br><br>[Financial Property Manual Fit](https://metabase.sapron.com.br/question#eyJkYXRhc2V0X3F1ZXJ5Ijp7ImRhdGFiYXNlIjoyLCJ0eXBlIjoicXVlcnkiLCJxdWVyeSI6eyJzb3VyY2UtdGFibGUiOjExfX0sImRpc3BsYXkiOiJ0YWJsZSIsInZpc3VhbGl6YXRpb25fc2V0dGluZ3MiOnt9fQ==) | id<br>created_at<br>updated_at<br>date_ref<br>value<br>is_adding<br>property_id<br>description<br> | Tabela com os ajustes manuais direcionados para os imóveis |
| financial_owner_property_ted<br><br>[Financial Owner Property Ted](https://metabase.sapron.com.br/question#eyJkYXRhc2V0X3F1ZXJ5Ijp7ImRhdGFiYXNlIjoyLCJ0eXBlIjoicXVlcnkiLCJxdWVyeSI6eyJzb3VyY2UtdGFibGUiOjE0Nn19LCJkaXNwbGF5IjoidGFibGUiLCJ2aXN1YWxpemF0aW9uX3NldHRpbmdzIjp7fX0=) | id<br>created_at<br>updated_at<br>date_ref<br>value<br>property_id<br> | Tabela com o histórico dos TEDs realizados aos proprietários, divididos por imóvel |

  \
  \


---

* **Tabelas Property** (tabelas que contêm apenas dados relacionados às propriedades)

| Tabela AWS ⇒ Metabase | Colunas | Definição |
|:---|:---|:---|
| property_monthly_data<br><br>[Proper Pay Property Monthly Data](https://metabase.sapron.com.br/question#eyJkYXRhc2V0X3F1ZXJ5Ijp7InF1ZXJ5Ijp7InNvdXJjZS10YWJsZSI6MTkzLCJmaWx0ZXIiOlsiYW5kIixbIj0iLFsiZmllbGQiLDIzMTksbnVsbF0sNTMxXV19LCJ0eXBlIjoicXVlcnkiLCJkYXRhYmFzZSI6Mn0sImRpc3BsYXkiOiJ0YWJsZSIsInZpc3VhbGl6YXRpb25fc2V0dGluZ3MiOnt9fQ==) | property_id<br>revenue<br>cleaning_fee<br>expenses<br>manual_fit<br>implantation_fee<br>owner_ted<br>month_ref<br> | Tabela de valores consolidados os valores diários por mês por imóvel |
| daily_property_balance<br><br>[Proper Pay Property Daily Balance](https://metabase.sapron.com.br/question#eyJkYXRhc2V0X3F1ZXJ5Ijp7ImRhdGFiYXNlIjoyLCJ0eXBlIjoicXVlcnkiLCJxdWVyeSI6eyJzb3VyY2UtdGFibGUiOjE3MH19LCJkaXNwbGF5IjoidGFibGUiLCJ2aXN1YWxpemF0aW9uX3NldHRpbmdzIjp7fX0=) | date<br>value<br>property_id<br> | Tabela de saldos de cada dia por imóvel |
| daily_property_manual_fit<br><br>[Proper Pay Property Daily Manual Fit](https://metabase.sapron.com.br/question#eyJkYXRhc2V0X3F1ZXJ5Ijp7ImRhdGFiYXNlIjoyLCJ0eXBlIjoicXVlcnkiLCJxdWVyeSI6eyJzb3VyY2UtdGFibGUiOjE4M319LCJkaXNwbGF5IjoidGFibGUiLCJ2aXN1YWxpemF0aW9uX3NldHRpbmdzIjp7fX0=) | accrual_date<br>cash_date<br>value<br>property_id<br> | Tabela com o histórico dos ajustes manuais de cada dia para cada imóvel |
| daily_property_cleaning<br><br>[Proper Pay Property Daily Net Cleaning Fee](https://metabase.sapron.com.br/question#eyJkYXRhc2V0X3F1ZXJ5Ijp7ImRhdGFiYXNlIjoyLCJ0eXBlIjoicXVlcnkiLCJxdWVyeSI6eyJzb3VyY2UtdGFibGUiOjE5Nn19LCJkaXNwbGF5IjoidGFibGUiLCJ2aXN1YWxpemF0aW9uX3NldHRpbmdzIjp7fX0=) | accrual_date<br>cash_date<br>net_cleaning_fee<br>listing_id<br>code<br>reservation_id<br>has_extension<br>property_id<br> | Tabela com todas as limpeza geradas por reservas de cada imóvel por dia<br><br>\*Obs: o valor das limpezas descem para o último dia de reserva + extesões, porém o código da reserva é o código da reserva original<br> |
| daily_property_expenses<br><br>[Proper Pay Property Daily Expenses](https://metabase.sapron.com.br/question#eyJkYXRhc2V0X3F1ZXJ5Ijp7ImRhdGFiYXNlIjoyLCJ0eXBlIjoicXVlcnkiLCJxdWVyeSI6eyJzb3VyY2UtdGFibGUiOjE5OH19LCJkaXNwbGF5IjoidGFibGUiLCJ2aXN1YWxpemF0aW9uX3NldHRpbmdzIjp7fX0=) | accrual_date<br>cash_date<br>value<br>reason<br>paid_by<br>responsible_user<br>property_id<br> | Tabela que contem todo o histórico de despesas dos imóveis administrados pela Seazone<br><br>Essas despesa são registradas pelo respectivo anfitrião do imóvel, e são divididas por diversas categorias e direcionado ao responsável de reembolsar o valor pago pelo anfitrião<br> |
| daily_property_implantation_fee<br><br>[Proper Pay Property Daily Implantation Fee](https://metabase.sapron.com.br/question#eyJkYXRhc2V0X3F1ZXJ5Ijp7ImRhdGFiYXNlIjoyLCJ0eXBlIjoicXVlcnkiLCJxdWVyeSI6eyJzb3VyY2UtdGFibGUiOjE2OX19LCJkaXNwbGF5IjoidGFibGUiLCJ2aXN1YWxpemF0aW9uX3NldHRpbmdzIjp7fX0=) | accrual_date<br>cash_date<br>implantation_fee<br>property_id<br> | Tabela que consolida todos os valores referentes a taxa de implantação dos imóveis (valor negativo) e seus abatimentos, parcelamentos e pagamentos (valores positivos). |
| daily_property_revenue<br><br>[Proper Pay Property Daily Revenue](https://metabase.sapron.com.br/question#eyJkYXRhc2V0X3F1ZXJ5Ijp7ImRhdGFiYXNlIjoyLCJ0eXBlIjoicXVlcnkiLCJxdWVyeSI6eyJzb3VyY2UtdGFibGUiOjE4OH19LCJkaXNwbGF5IjoidGFibGUiLCJ2aXN1YWxpemF0aW9uX3NldHRpbmdzIjp7fX0=) | accrual_date<br>cash_date<br>daily_net_value<br>listing_id<br>code<br>reservation_id<br>is_extension<br>property_id<br> | Tabela com todas as receita geradas pelas reservas e extensões por imóvel de todas as OTAs, sendo o valor total da reserva, dividido igualmente pelos dias totais da reserva |
| property_handover_details<br><br>[Property Handover Details](https://metabase.sapron.com.br/question#eyJkYXRhc2V0X3F1ZXJ5Ijp7ImRhdGFiYXNlIjoyLCJ0eXBlIjoicXVlcnkiLCJxdWVyeSI6eyJzb3VyY2UtdGFibGUiOjIzfX0sImRpc3BsYXkiOiJ0YWJsZSIsInZpc3VhbGl6YXRpb25fc2V0dGluZ3MiOnt9fQ==) | id<br>implantation_items_description<br>onboarding_contact_phonenumber<br>onboarding_contact_name<br>comment<br>indicator_name<br>setup_value<br>photographer_value<br>bed_linen_value<br>full_inspection_value<br>amenities_id<br>bed_linen_photo_uid<br>property_id<br>rules_id<br>plan<br>created_at<br>implantation_fee_total_value<br>payment_installments<br>payment_method<br>pipedrive_deal_id<br>property_area_size_m2<br>updated_at<br> | Tabela que contem todos os dados sobre cada imóvel |
| daily_property_transfer<br><br>[Proper Pay Property Daily Transfer](https://metabase.sapron.com.br/question#eyJkYXRhc2V0X3F1ZXJ5Ijp7ImRhdGFiYXNlIjoyLCJ0eXBlIjoicXVlcnkiLCJxdWVyeSI6eyJzb3VyY2UtdGFibGUiOjE3Nn19LCJkaXNwbGF5IjoidGFibGUiLCJ2aXN1YWxpemF0aW9uX3NldHRpbmdzIjp7fX0=) | date<br>value<br>property_id<br>description<br>type<br> | Tabela consolidando todos os valores referente ao imóvel, em forma de extrato |
| property_nf<br><br>[Proper Pay Property Nf Value](https://metabase.sapron.com.br/question#eyJkYXRhc2V0X3F1ZXJ5Ijp7ImRhdGFiYXNlIjoyLCJ0eXBlIjoicXVlcnkiLCJxdWVyeSI6eyJzb3VyY2UtdGFibGUiOjE3OH19LCJkaXNwbGF5IjoidGFibGUiLCJ2aXN1YWxpemF0aW9uX3NldHRpbmdzIjp7fX0=) | property_id<br>value<br>month_ref<br> | Tabela de valor da NF por imóvel |
| property_property<br><br>[Property Property](https://metabase.sapron.com.br/question#eyJkYXRhc2V0X3F1ZXJ5Ijp7ImRhdGFiYXNlIjoyLCJ0eXBlIjoicXVlcnkiLCJxdWVyeSI6eyJzb3VyY2UtdGFibGUiOjc2fX0sImRpc3BsYXkiOiJ0YWJsZSIsInZpc3VhbGl6YXRpb25fc2V0dGluZ3MiOnt9fQ==) | id<br>created_at<br>updated_at<br>code<br>comission_fee<br>single_bed_quantity<br>double_bed_quantity<br>queen_bed_quantity<br>king_bed_quantity<br>single_sofa_bed_quantity<br>double_sofa_bed_quantity<br>pillow_quantity<br>bedroom_quantity<br>bathroom_quantity<br>lavatory_quantity<br>cleaning_fee<br>bond_amount<br>guest_capacity<br>property_type<br>status<br>activation_date<br>inactivation_date<br>contract_start_date<br>contract_end_date<br>address_id<br>category_location_id<br>host_id<br>partner_id<br>cover_image_uid<br>balance_discount_rate<br>bank_details_id<br>invoice_details_id<br>extra_day_preparation<br>category_id<br>region<br>is_to_keep_funds_in_seazone<br>host_cleaning_comission_fee<br>host_reservation_comission_fee<br> | Tabela de dados sobre imóvel |
| property_audit<br><br>[Property Audit](https://metabase.sapron.com.br/question#eyJkYXRhc2V0X3F1ZXJ5Ijp7ImRhdGFiYXNlIjoyLCJ0eXBlIjoicXVlcnkiLCJxdWVyeSI6eyJzb3VyY2UtdGFibGUiOjE1NX19LCJkaXNwbGF5IjoidGFibGUiLCJ2aXN1YWxpemF0aW9uX3NldHRpbmdzIjp7fX0=) | id<br>created_at<br>updated_at<br>property_id<br>property_created_at<br>property_updated_at<br>code<br>category_location_id<br>category_id<br>region<br>address_id<br>comission_fee<br>single_bed_quantity<br>double_bed_quantity<br>queen_bed_quantity<br>king_bed_quantity<br>single_sofa_bed_quantity<br>double_sofa_bed_quantity<br>pillow_quantity<br>bedroom_quantity<br>bathroom_quantity<br>lavatory_quantity<br>cleaning_fee<br>bond_amount<br>guest_capacity<br>property_type<br>status<br>activation_date<br>inactivation_date<br>contract_start_date<br>contract_end_date<br>host_id<br>partner_id<br>cover_image_uid<br>balance_discount_rate<br>bank_details_id<br>invoice_details_id<br>extra_day_preparation<br>is_to_keep_funds_in_seazone<br>host_reservation_comission_fee<br>host_cleaning_comission_fee<br>operation<br>changed_at<br>modifier<br>changed_by_user_id<br>changed_by_celery_task<br>fields_changed<br> | Tabela de dados sobre imóvel que foram editados |


---

* **Tabelas Seazone** (tabelas que contêm apenas dados relacionados à Seazone)

| Nome da Tabela | Colunas | Definição |
|:---|:---|:---|
| daily_seazone_commissions<br><br>[Proper Pay Seazone Daily Commission](https://metabase.sapron.com.br/question#eyJkYXRhc2V0X3F1ZXJ5Ijp7ImRhdGFiYXNlIjoyLCJ0eXBlIjoicXVlcnkiLCJxdWVyeSI6eyJzb3VyY2UtdGFibGUiOjE4MX19LCJkaXNwbGF5IjoidGFibGUiLCJ2aXN1YWxpemF0aW9uX3NldHRpbmdzIjp7fX0=) | date<br>value<br>fee<br>property_id<br> | Tabela com a comissão cobrada pela Seazone por cada imóvel gerenciado, com seu respectivo valor e taxa |
| daily_seazone_fee | date<br>fee<br>property_id<br> | Tabela com a taxa de comissão cobrada pela Seazone por cada imóvel gerenciado |


---

* **Tabela Host** (tabelas que contêm apenas dados relacionados ao anfitrião)

| Nome da Tabela | Colunas | Definição |
|:---|:---|:---|
| host_monthly_data<br><br>[Proper Pay Host Monthly](https://metabase.sapron.com.br/question#eyJkYXRhc2V0X3F1ZXJ5Ijp7ImRhdGFiYXNlIjoyLCJ0eXBlIjoicXVlcnkiLCJxdWVyeSI6eyJzb3VyY2UtdGFibGUiOjE3Mn19LCJkaXNwbGF5IjoidGFibGUiLCJ2aXN1YWxpemF0aW9uX3NldHRpbmdzIjp7fX0=) | host_id<br>revenue<br>cleaning_fee<br>onboarding_expenses<br>manual_fit<br>commission<br>refund_expenses<br>debited_expenses<br>transfer<br>month_ref<br> | Tabela de valores consolidados por mês por anfitrião |
| daily_host_balance<br><br>[Proper Pay Host Daily Balance](https://metabase.sapron.com.br/question#eyJkYXRhc2V0X3F1ZXJ5Ijp7ImRhdGFiYXNlIjoyLCJ0eXBlIjoicXVlcnkiLCJxdWVyeSI6eyJzb3VyY2UtdGFibGUiOjE4NH19LCJkaXNwbGF5IjoidGFibGUiLCJ2aXN1YWxpemF0aW9uX3NldHRpbmdzIjp7fX0=) | date<br>value<br>host_id<br> | Tabela de dados de saldo inicial por dia de cada anfitrião |
| daily_host_cleaning<br><br>[Proper Pay Property Daily Net Cleaning Fee](https://metabase.sapron.com.br/question#eyJkYXRhc2V0X3F1ZXJ5Ijp7ImRhdGFiYXNlIjoyLCJ0eXBlIjoicXVlcnkiLCJxdWVyeSI6eyJzb3VyY2UtdGFibGUiOjE5Nn19LCJkaXNwbGF5IjoidGFibGUiLCJ2aXN1YWxpemF0aW9uX3NldHRpbmdzIjp7fX0=) | accrual_date<br>cash_date<br>value<br>host_id<br> | Tabela de dados de limpeza por dia de cada anfitrião |
| daily_host_commission<br><br>[Proper Pay Host Daily Commission](https://metabase.sapron.com.br/question#eyJkYXRhc2V0X3F1ZXJ5Ijp7ImRhdGFiYXNlIjoyLCJ0eXBlIjoicXVlcnkiLCJxdWVyeSI6eyJzb3VyY2UtdGFibGUiOjE4OX19LCJkaXNwbGF5IjoidGFibGUiLCJ2aXN1YWxpemF0aW9uX3NldHRpbmdzIjp7fX0=) | date<br>value<br>property_id<br>host_id<br> | Tabela de dados de comissão por dia de cada anfitrião, por imóvel |
| daily_host_commissions | date<br>value<br>fee<br>property_id<br> | Tabela de taxa de comissão de anfitrião por propriedade |
| daily_host_fee | date<br>fee<br>host_id<br>property_id<br> | Tabela de taxa de comissão de cada anfitrião por imóvel, por dia |
| daily_host_manual_fit<br><br>[Proper Pay Host Daily Manual Fit](https://metabase.sapron.com.br/question#eyJkYXRhc2V0X3F1ZXJ5Ijp7ImRhdGFiYXNlIjoyLCJ0eXBlIjoicXVlcnkiLCJxdWVyeSI6eyJzb3VyY2UtdGFibGUiOjE3MX19LCJkaXNwbGF5IjoidGFibGUiLCJ2aXN1YWxpemF0aW9uX3NldHRpbmdzIjp7fX0=) | accrual_date<br>cash_date<br>value<br>host_id<br> | Tabela de ajuste manuais diretos para o anfitrião |
| daily_host_onboarding_expenses | accrual_date<br>cash_date<br>value<br>reason<br>property_id<br>host_id<br> | Tabela de despesas relacionadas a Onboarding |
| daily_host_refund_expenses | accrual_date<br>cash_date<br>value<br>property_id<br>host_id<br> | Tabela de despesas consideradas como pagas |
| daily_host_revenue<br><br>[Proper Pay Host Daily Revenue](https://metabase.sapron.com.br/question#eyJkYXRhc2V0X3F1ZXJ5Ijp7ImRhdGFiYXNlIjoyLCJ0eXBlIjoicXVlcnkiLCJxdWVyeSI6eyJzb3VyY2UtdGFibGUiOjE4NX19LCJkaXNwbGF5IjoidGFibGUiLCJ2aXN1YWxpemF0aW9uX3NldHRpbmdzIjp7fX0=) | accrual_date<br>cash_date<br>value<br>host_id<br> | Tabela de todas as receitas (reservas) que o anfitrião foi responsável |
| daily_host_transfer<br><br>[Proper Pay Host Daily Transfer](https://metabase.sapron.com.br/question#eyJkYXRhc2V0X3F1ZXJ5Ijp7ImRhdGFiYXNlIjoyLCJ0eXBlIjoicXVlcnkiLCJxdWVyeSI6eyJzb3VyY2UtdGFibGUiOjE3OX19LCJkaXNwbGF5IjoidGFibGUiLCJ2aXN1YWxpemF0aW9uX3NldHRpbmdzIjp7fX0=) | date<br>value<br>type<br>Description<br>host_id<br> | Tabela consolidando todos os valores referente ao anfitrião, em forma de extrato |
| account_host<br><br>[Account Host](https://metabase.sapron.com.br/question#eyJkYXRhc2V0X3F1ZXJ5Ijp7ImRhdGFiYXNlIjoyLCJ0eXBlIjoicXVlcnkiLCJxdWVyeSI6eyJzb3VyY2UtdGFibGUiOjcyfX0sImRpc3BsYXkiOiJ0YWJsZSIsInZpc3VhbGl6YXRpb25fc2V0dGluZ3MiOnt9fQ==) | id<br>created_at<br>updated_at<br>legacy_reservation_royalties<br>legacy_cleaning_royalties<br>location_id<br>user_id<br>is_host_ops<br>cleaning_commission_fee<br>reservation_commission_fee<br>default_bank_details_id<br> | Tabela dados gerais sobre o anfitrião |
| account_host_audit<br><br>[Account Host Audit](https://metabase.sapron.com.br/question#eyJkYXRhc2V0X3F1ZXJ5Ijp7ImRhdGFiYXNlIjoyLCJ0eXBlIjoicXVlcnkiLCJxdWVyeSI6eyJzb3VyY2UtdGFibGUiOjE1Nn19LCJkaXNwbGF5IjoidGFibGUiLCJ2aXN1YWxpemF0aW9uX3NldHRpbmdzIjp7fX0=) | id<br>created_at<br>updated_at<br>host_id<br>host_created_at<br>host_updated_at<br>user_id<br>location_id<br>legacy_reservation_royalties<br>legacy_cleaning_royalties<br>reservation_commission_fee<br>cleaning_commission_fee<br>is_host_ops<br>default_bank_details_id<br>operation<br>changed_at<br>modifier<br>changed_by_user_id<br>changed_by_celery_task<br>fields_changed<br> | Tabela de dados sobre o anfitrião que foram editados |
| "Não está na AWS"<br><br>[Proper Pay Host Ted Nf Value](https://metabase.sapron.com.br/question#eyJkYXRhc2V0X3F1ZXJ5Ijp7ImRhdGFiYXNlIjoyLCJ0eXBlIjoicXVlcnkiLCJxdWVyeSI6eyJzb3VyY2UtdGFibGUiOjE5Mn19LCJkaXNwbGF5IjoidGFibGUiLCJ2aXN1YWxpemF0aW9uX3NldHRpbmdzIjp7fX0=) | Month Ref<br>Value<br>Host ID<br> | Tabelas dos valores gerados das notas fiscais para o anfitrião |
| daily_host_franchise_fee | accrual_date<br>cash_date<br>value<br>host_id<br> | Tabelas dos valores atualizados, descontados o devido valor da taxa de franquia |
| financial_host_franchise_fee | id<br>created_at<br>updated_at<br>franchise_fee_amount<br>have_grace_period<br>final_date_franchise_fee<br>rebate_percentage<br>month_ref<br>host_id<br> | Informações gerais sobre a taxa de franquia |


\
## Tabelas Desativadas


---

* **Tabela Partner** (tabelas que contêm apenas dados relacionados ao parceiro) ⇒ Desligada

| Nome da Tabela | Colunas | Definição |
|:---|:---|:---|
| partner_monthly_data<br><br>[Proper Pay Partner Monthly](https://metabase.sapron.com.br/question#eyJkYXRhc2V0X3F1ZXJ5Ijp7ImRhdGFiYXNlIjoyLCJ0eXBlIjoicXVlcnkiLCJxdWVyeSI6eyJzb3VyY2UtdGFibGUiOjE3NH19LCJkaXNwbGF5IjoidGFibGUiLCJ2aXN1YWxpemF0aW9uX3NldHRpbmdzIjp7fX0=) | partner_id<br>revenue<br>commission<br>month_ref<br> | Tabela de valores consolidados por mês por parceiro |
| daily_partner_balance<br><br>[Proper Pay Partner Daily Balance](https://metabase.sapron.com.br/question#eyJkYXRhc2V0X3F1ZXJ5Ijp7ImRhdGFiYXNlIjoyLCJ0eXBlIjoicXVlcnkiLCJxdWVyeSI6eyJzb3VyY2UtdGFibGUiOjE5MX19LCJkaXNwbGF5IjoidGFibGUiLCJ2aXN1YWxpemF0aW9uX3NldHRpbmdzIjp7fX0=) | date<br>value<br>partner_id<br> | Tabela de saldo do parceiro |
| daily_partner_commission<br><br>[Proper Pay Partner Daily Commission](https://metabase.sapron.com.br/question#eyJkYXRhc2V0X3F1ZXJ5Ijp7ImRhdGFiYXNlIjoyLCJ0eXBlIjoicXVlcnkiLCJxdWVyeSI6eyJzb3VyY2UtdGFibGUiOjE5N319LCJkaXNwbGF5IjoidGFibGUiLCJ2aXN1YWxpemF0aW9uX3NldHRpbmdzIjp7fX0=) | date<br>value<br>property_id<br>partner_id<br> | Tabela de valor de comissão do parceiro por imóvel indicado, por dia |
| daily_property_partner_commissions | date<br>value<br>fee<br>property_id<br> | Tabela de comissão do parceiro, por propriedade |
| daily_partner_revenue<br><br>[Proper Pay Partner Daily Revenue](https://metabase.sapron.com.br/question#eyJkYXRhc2V0X3F1ZXJ5Ijp7ImRhdGFiYXNlIjoyLCJ0eXBlIjoicXVlcnkiLCJxdWVyeSI6eyJzb3VyY2UtdGFibGUiOjE3M319LCJkaXNwbGF5IjoidGFibGUiLCJ2aXN1YWxpemF0aW9uX3NldHRpbmdzIjp7fX0=) | accrual_date<br>cash_date<br>value<br>partner_id<br> | Tabela com o total das receitas geradas dos imóveis indicados pelo parceiros |
| partners_indications_property<br><br>[Partners Indications Property](https://metabase.sapron.com.br/question#eyJkYXRhc2V0X3F1ZXJ5Ijp7ImRhdGFiYXNlIjoyLCJ0eXBlIjoicXVlcnkiLCJxdWVyeSI6eyJzb3VyY2UtdGFibGUiOjM5fX0sImRpc3BsYXkiOiJ0YWJsZSIsInZpc3VhbGl6YXRpb25fc2V0dGluZ3MiOnt9fQ==) | id<br>created_at<br>updated_at<br>owner_name<br>owner_phone_number<br>status<br>status_change_date<br>property_city<br>property_state<br>property_type<br>partner_id<br>comment<br>pipedrive_deal_id<br>due_date<br>property_id<br>commission<br>owner_email<br>pipedrive_stage<br>property_complement<br>property_neighborhood<br>property_number<br>property_street<br>owner_is_aware_of_indication<br>owner_received_the_ebook<br>property_has_furniture<br>property_is_in_coverage_area<br>property_under_construction<br>lost_reason<br> | Tabela com o ID do parceiro e informações sobre o imóvel e proprietário indicado por ele |
| account_partner<br><br>[Account Partner](https://metabase.sapron.com.br/question#eyJkYXRhc2V0X3F1ZXJ5Ijp7ImRhdGFiYXNlIjoyLCJ0eXBlIjoicXVlcnkiLCJxdWVyeSI6eyJzb3VyY2UtdGFibGUiOjI1fX0sImRpc3BsYXkiOiJ0YWJsZSIsInZpc3VhbGl6YXRpb25fc2V0dGluZ3MiOnt9fQ==) | id<br>created_at<br>updated_at<br>signed_contract<br>nationality<br>marital_status<br>profession<br>user_id<br>attendant_name<br>attendant_phone_number<br>spreadhsheet_link<br>executive_id<br> | Tabela de informações pessoais sobre o parceiro |


---

* **Tabelas Owner** (tabelas que contêm apenas dados relacionados ao proprietário) ⇒ Desligada

| Nome da Tabela | Colunas | Definição |
|:---|:---|:---|
| owner_monthly_data | owner_id<br>revenue<br>expenses<br>manual_fit<br>commission<br>transfer<br>month_ref<br> | Tabela de valores consolidados por mês por proprietário |
| daily_owner_balance | date<br>value<br>owner_id<br> | Tabela de valores referentes ao saldo inicial, do proprietário |
| daily_owner_commission | date<br>value<br>owner_id<br> | Tabela de comissão do proprietário |
| daily_owner_expenses | accrual_date<br>cash_date<br>value<br>owner_id<br> | Tabela de despesas do proprietário |
| daily_owner_manual_fit | accrual_date<br>cash_date<br>value<br>owner_id<br> | Tabela de ajustes manuais do proprietário |
| daily_owner_revenue | accrual_date<br>cash_date<br>value<br>owner_id<br> | Tabela de receita do proprietário |
| daily_owner_property_ted | accrual_date<br>cash_date<br>value<br>property_id<br> | Tabela de TEDs realizados para os proprietários |
| daily_owner_transfer | date<br>value<br>owner_id<br> | Tabela de valor de repasse ao proprietário |
| account_owner ⇒ [Account Owner](https://metabase.sapron.com.br/question#eyJkYXRhc2V0X3F1ZXJ5Ijp7ImRhdGFiYXNlIjoyLCJ0eXBlIjoicXVlcnkiLCJxdWVyeSI6eyJzb3VyY2UtdGFibGUiOjg3fX0sImRpc3BsYXkiOiJ0YWJsZSIsInZpc3VhbGl6YXRpb25fc2V0dGluZ3MiOnt9fQ==) | id<br>created_at<br>updated_at<br>nationality<br>marital_status<br>profession<br>email_for_operation<br>invoice_address_id<br>user_id<br>default_bank_details_id<br>default_invoice_details_id<br>hometown<br>income<br>instagram_profile<br>lives_same_town_as_property<br>meet_seazone<br>properties_owned<br>properties_to_rent<br>birth_city<br>transfer_day<br> | Tabela de dados gerais sobre o proprietário |


\