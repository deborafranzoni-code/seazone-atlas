<!-- title: payments | url: https://outline.seazone.com.br/doc/payments-mhkr05EksG | area: Tecnologia -->

# payments

Created by: Bernardo Ribeiro Created time: September 6, 2023 12:46 AM Description: A tabela de Pagamentos registra informações relacionadas aos pagamentos para as reservas realizadas pelo Site de Reservas da Seazone. Cada registro nesta tabela corresponde a um pagamento específico a uma determinada reserva e inclui uma série de campos que fornecem detalhes sobre o pagamento, como o status, o método de pagamento, informações do gateway de pagamento, bem como informações sobre notificações de pagamento e timestamps. Tags: Pagamentos, Reservas

## Payments


 1. **id**: Identificador único do pagamento (inteiro).
 2. **reservation_id**: Identificador da reserva associada a este pagamento (inteiro).
 3. **status**: Status do pagamento (texto). Opções: `Pending`, `Paid` e `Failed`
 4. **gateway**: Gateway de pagamento utilizado para processar a transação (texto). **Opções:** `Pagarme`, `Paypal`
 5. **gateway_ref**: Referência (ID) do gateway de pagamento para este pagamento (texto).
 6. **gateway_metadata**: Metadados do gateway de pagamento (JSON).
 7. **pending_at**: Data e hora de pendência do pagamento (data e hora).
 8. **paid_at**: Data e hora de confirmação do pagamento (data e hora).
 9. **canceled_at**: Data e hora de cancelamento do pagamento (data e hora).
10. **created_by**: Nome do usuário responsável pela criação do registro (texto).
11. **changed_by**: Nome do usuário que realizou a última modificação do registro (texto).
12. **created_at**: Data e hora de criação do registro de pagamento (data e hora).
13. **updated_at**: Data e hora da última modificação do registro de pagamento (data e hora).
14. **failed_at**: Data e hora de falha no pagamento (data e hora).
15. **gateway_payment_metadata**: Metadados específicos do pagamento do gateway (JSON).
16. **payment_notified**: Indica se o pagamento foi notificado (booleano).
17. **payment_notified_at**: Data e hora da notificação de pagamento (data e hora).
18. **chargedback_at**: Data e hora de chargeback (quando um pagamento é contestado pelo cliente) (data e hora).
19. **payment_failed_notified**: Indica se a falha no pagamento foi notificada (booleano).
20. **payment_failed_notified_at**: Data e hora da notificação de falha no pagamento (data e hora).

* **Campos e Descrição**

| Field | Type | Description |
|----|----|----|
|    |    |    |
|    |    |    |
|    |    |    |