<!-- title: reservations | url: https://outline.seazone.com.br/doc/reservations-JM2xyHeLzQ | area: Tecnologia -->

# reservations

Created by: Bernardo Ribeiro Created time: September 6, 2023 12:48 AM Description: A tabela de Reservas armazena informações detalhadas sobre as reservas de propriedades de aluguel por temporada feitas pelo Site de Reservas da Seazone. Cada registro nesta tabela representa uma reserva específica e contém uma variedade de campos que incluem detalhes como datas de check-in e check-out, informações sobre hóspedes, preços, status de pagamento e muito mais. Tags: Reservas

## Reservations


 1. **id**: Identificador único do registro (inteiro).
 2. **status**: Status da reserva (texto). **Opções**: `Pending`, `Waiting_Confirmation`, `Confirmed`, `Confirmation_Failed`, `Waiting_Payment_Confirmation`, `Paid`, `Expired`, `Waiting_Cancellation` e `Canceled`
 3. **check_in_date**: Data de check-in (data).
 4. **check_in_time**: Hora de check-in (hora).
 5. **check_out_date**: Data de check-out (data).
 6. **check_out_time**: Hora de check-out (hora).
 7. **guests_quantity**: Quantidade de hóspedes (inteiro).
 8. **total_price**: Preço total da reserva (decimal). `diarias + limpeza` *sem considerar o cupom*
 9. **cleaning_fee**: Taxa de limpeza (decimal).
10. **property_id**: Identificador da propriedade (inteiro).
11. **user_id**: Identificador do usuário (inteiro).
12. **user_is_main_guest**: Indica se o usuário é o principal hóspede (booleano).
13. **created_by**: Nome do criador do registro (texto).
14. **changed_by**: Nome do último a modificar o registro (texto).
15. **created_at**: Data e hora de criação do registro (data e hora).
16. **updated_at**: Data e hora da última modificação do registro (data e hora).
17. **stays_id**: ID da Reserva Na Stays (texto).
18. **pending_at**: Data e hora de pendência da reserva (data e hora).
19. **waiting_confirmation_at**: Data e hora de espera para confirmação (data e hora).
20. **confirmed_at**: Data e hora de confirmação (data e hora).
21. **confirmed_failed_at**: Data e hora de falha na confirmação (data e hora).
22. **paid_at**: Data e hora de pagamento (data e hora).
23. **expired_at**: Data e hora de expiração (data e hora).
24. **adults**: Quantidade de adultos (inteiro).
25. **kids**: Quantidade de crianças (inteiro).
26. **babies**: Quantidade de bebês (inteiro).
27. **promo_code**: Código de promoção; Cupom (texto).
28. **effective_price**: Preço efetivo após promoção (decimal). `diarias + cleaning_fee - cupom`
29. **promo_info**: Informações da promoção (JSON).
30. **waiting_cancellation_at**: Data e hora de espera para cancelamento (data e hora).
31. **canceled_at**: Data e hora de cancelamento (data e hora).
32. **total_paid**: Total pago (decimal). `effective_price + juros_parcelamento`
33. **waiting_payment_confirmation_at**: Data e hora de espera para confirmação de pagamento (data e hora).
34. **confirmation_notified**: Indica se a confirmação foi notificada (booleano).
35. **confirmation_notified_at**: Data e hora de notificação de confirmação (data e hora).
36. **canceled_notified**: Indica se o cancelamento foi notificado (booleano).
37. **canceled_notified_at**: Data e hora de notificação de cancelamento (data e hora).
38. **nights_price**: Preço total de diarias, desconiderando taxa de limpeza (decimal). `diarias`
39. **confirmation_failure_cause**: Causa da falha na confirmação (texto).
40. **confirmation_failure_details**: Detalhes da falha na confirmação (texto).
41. **payment_gateway_fee**: Taxa da operadora de pagamento (decimal).
42. **net_value**: Valor líquido após taxas (decimal). `total_paid - payment_gateway_fee`
43. **ota_fee**: Taxa da OTA (Online Travel Agency) (decimal). `net_value * 0.15`
44. **payment_method**: Método de pagamento (texto). **Opções**: `paypal`, `pix`, `credit_card`
45. **installments**: Número de parcelas (inteiro). **Opções**: `1 a 12`. 1 é pagamento à vista.
46. **tracking_utm_medium**: Fonte média de rastreamento (texto).
47. **tracking_utm_source**: Fonte de rastreamento (texto).
48. **tracking_utm_campaign**: Campanha de rastreamento (texto).
49. **tracking_raw_data**: Dados brutos de rastreamento (JSON).

* **Campos e Descrição**

| Field | Type | Description |
|----|----|----|
| id |    |    |
| status |    |    |
| check_in_date |    |    |
| check_in_time |    |    |
| check_out_date |    |    |
| check_out_time |    |    |
| guests_quantity |    |    |
| total_price |    |    |
| cleaning_fee |    |    |
| property_id |    |    |
| user_id |    |    |
| user_is_main_guest |    |    |
| created_by |    |    |
| changed_by |    |    |
| created_at |    |    |
| updated_at |    |    |
| stays_id |    |    |
| pending_at |    |    |
| waiting_confirmation_at |    |    |
| confirmed_at |    |    |
| confirmed_failed_at |    |    |
| paid_at |    |    |
| expired_at |    |    |
| adults |    |    |
| kids |    |    |
| babies |    |    |
| promo_code |    |    |
| effective_price |    |    |
| promo_info |    |    |
| waiting_cancellation_at |    |    |
| canceled_at |    |    |
| total_paid |    |    |
| waiting_payment_confirmation_at |    |    |
| confirmation_notified |    |    |
| confirmation_notified_at |    |    |
| canceled_notified |    |    |
| canceled_notified_at |    |    |
| nights_price |    |    |
| confirmation_failure_cause |    |    |
| confirmation_failure_details |    |    |
| payment_gateway_fee |    |    |
| net_value |    |    |
| ota_fee |    |    |
| payment_method |    |    |
| installments |    |    |
| tracking_utm_medium |    |    |
| tracking_utm_source |    |    |
| tracking_utm_campaign |    |    |
| tracking_raw_data |    |    |