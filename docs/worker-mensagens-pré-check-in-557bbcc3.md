<!-- title: Worker mensagens pré check-in | url: https://outline.seazone.com.br/doc/worker-mensagens-pre-check-in-EYfvMGz7Ej | area: Tecnologia -->

# Worker mensagens pré check-in

# Descrição de funcionamento

O worker de envio de mensagens de pré check-in, com nome "Pre Check-in Messenger", é mantido no Argo Workflow como cron worker, executado todos os dias às 10h (BRT).

O papel desse worker é enviar mensagens de pré check-in para reservas com check-in para daqui três dias. Ou seja, caso o worker seja executado no dia `01/01/2026` , deve buscar reservas com check-in para dia `04/01/2026`.

Conforme são realizadas tentativas de envio de mensagens, o worker persiste informações de sucessos e falhas de envio na tabela `reservation_precheckin_message_attempts`, no banco de dados `sapron-api`.

O worker ignora reservas que já possuam tentativas de envio de mensagens com status de sucesso; também ignora reservas que já possuem registro de pré-checkin (`reservation_precheckin`). 

No caso de falhas, alertas são enviados via slack, ao canal `#``**precheckin-messenger-alerts**`**.**

## Tabelas utilizadas

* `reservation_precheckin_message_attempts` - armazena informações de tentativas de envios de mensagens para reservas. Inclui coluna booleana que informa se a tentativa foi bem sucedida, ou não.
* `reservation_precheckin` - armazena informações de pré check-in de reservas.

## Links importantes

* [Dashboard de monitoramento no Grafana](https://monitoring.seazone.com.br/d/e74ab1a4-da69-4f73-958b-47d89ac47a1e/pre-check-in-messenger)
* [Dashboard de monitoramento no Metabase](https://metabase.seazone.com.br/dashboard/162-pre-check-in-messenger?data=thisday&tab=69-production)
* [Argo Workflow (Cron workflows)](https://argowf.seazone.com.br/cron-workflows/prd-apps)

# Requisitos para Suporte

* Acesso à ferramentas em [Links importantes](https://outline.seazone.com.br/doc/worker-mensagens-pre-check-in-EYfvMGz7Ej#h-links-importantes)
* Acesso à visualização e edição de tabela `reservation_precheckin_message_attempts`
* Acesso à canal `#``**precheckin-messenger-alerts **`no Slack.