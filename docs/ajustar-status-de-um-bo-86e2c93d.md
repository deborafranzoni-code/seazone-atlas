<!-- title: Ajustar Status de um BO | url: https://outline.seazone.com.br/doc/ajustar-status-de-um-bo-QGzjCedkQx | area: Tecnologia -->

# Ajustar Status de um BO

Quando um  BO foi aprovado por engano e deve voltar a um status prévio deve seguir as seguientes ações:

* Se a mudança do status do BO é:  "Aprovado"  → "Em Analise"
  * Identificar o ID do BO na `**Reservation Incident Reports**`
  * Verificar em quais colunas tem dado de um ID associado, as colunas podem ser:
    * financial_seazone_manual_fit_id,

      financial_cleaning_fee_manual_fit_id,

      financial_host_manual_fit_id,

      financial_property_manual_fit_id,

      financial_reservation_manual_fit_id,

      \
  * identificar o ID associado na Tabela correspondente
  * Apagar o registro com ID encontrado no passo anterior
  * Mudar o `status` do BO na `**Reservation Incident Reports **`de"Aproved" → "Under Review"


\

Campos de um BO em `reservation_incident_reports`

* id, created_at, updated_at, status, incident_type, amount, report_date, description, reason, created_by_user_id, reservation_id, 
* under_review_description,
* under_review_reason,
* financial_cleaning_fee_manual_fit_id,
* financial_host_manual_fit_id,
* financial_property_manual_fit_id,
* financial_reservation_manual_fit_id,
* financial_seazone_manual_fit_id,
* fit_type,
* has_applied_early_checkout_manual_fit,
* denied_date,
* denied_reason,
* approval_date,
* manual_fit_payload


\