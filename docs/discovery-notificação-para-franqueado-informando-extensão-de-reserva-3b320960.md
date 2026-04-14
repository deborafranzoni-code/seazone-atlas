<!-- title: Discovery: Notificação para franqueado informando extensão de reserva | url: https://outline.seazone.com.br/doc/discovery-notificacao-para-franqueado-informando-extensao-de-reserva-E3E5k8MNpt | area: Tecnologia -->

# Discovery: Notificação para franqueado informando extensão de reserva

# Discovery Técnico: Late-Checkout (Extensão de Reserva) e Notificação via WhatsApp para Franqueado

## 1. Objetivo

Enviar mensagem de WhatsApp para o franqueado quando houver uma extensão de reserva do tipo late-checkout.

## 2. Contexto e premissas

* Late-checkout: hóspede já hospedado estende a permanência e adia o checkout.
* Na Stays, a extensão chega como uma nova reserva relacionada à reserva "mãe".
* A identificação futura também poderá usar `internal_notes` com valor como `late checkout`.
* A integração atual de WhatsApp via NewByte é voltada para persona hóspede e não será usada nesse fluxo.
* O novo fluxo deve usar Blip (persona franqueado).

## 3. Estado atual do sistema

### 3.1 Entrada das reservas da Stays no backend

As reservas entram por dois caminhos principais:


1. Webhook da Stays:

* Endpoint: `src/webhook/apis/stays.py`
* Roteamento do evento: `src/webhook/tasks.py::stays_handler_webhook_task`
* Para eventos `reservation.created|modified|reactivated`, o fluxo chama:
  * `stays_dispatch_create_update_reserv_event_task`
  * que localiza a reserva na Stays e chama `stays_handle_reservation_task`.


2. Importação agendada/manual:

* Tasks em `src/channel_manager/tasks_stays.py`:
  * `stays_import_new_reservations_task`
  * `stays_update_reservations_task`
  * `stays_dispatch_reservations_by_date_task`
* Todas convergem para `stays_handle_reservation_task`.

### 3.2 Ponto central de processamento

* Task central: `src/channel_manager/tasks_stays.py::stays_handle_reservation_task`
* Essa task:
  * aplica lock por `stays_id` (evita processamento concorrente duplicado),
  * registra status em `ReservationProcessingReport`,
  * delega regra de negócio para `StaysHandler.handle(...)`.

### 3.3 Como extensões são tratadas hoje

* Classe: `src/channel_manager/action/stays/stays_handler.py`
* Regra principal:
  * se `stays_reservation.partnerName == "Extensão"`, entra no branch de extensão;
  * chama `StaysExtender.extend(...)`.
* Classe: `src/channel_manager/action/stays/stays_extender.py`
  * Valida que `partnerName` é `Extensão`.
  * Cria/atualiza a reserva de extensão no Sapron.
  * Tenta localizar reserva original (mãe) por ordem de prioridade:


1. `partnerCode` da Stays (quando presente),
2. heurística por propriedade + datas limítrofes + hóspede.

* Faz o vínculo entre extensão e original:


1. Late extension quando `new_extension.check_in_date == original.check_out_date`
2. Early extension quando `new_extension.check_out_date == original.check_in_date`

* Atualiza flags/relacionamentos:


1. `is_late_extension`, `has_late_extension`, `late_extension_reservation`
2. `is_early_extension`, `has_early_extension`, `early_extension_reservation`
3. `original_reservation`

### 3.4 Estrutura de dados já existente para extensão

Modelo `Reservation` (`src/reservation/models.py`) já contém:

* `is_late_extension`, `has_late_extension`
* `is_early_extension`, `has_early_extension`
* `original_reservation`
* `late_extension_reservation`
* `early_extension_reservation`

Ou seja, o domínio de extensão já está modelado e operacional no backend.

### 3.5 Sobre `internal_notes`

* Atualmente não há uso de `internal_notes/internalNotes` na pipeline de processamento de reserva.
* Isso está alinhado com a premissa informada: esse dado passará a existir/ser usado após a evolução da tarefa.

### 3.6 Estado atual do envio de WhatsApp

* Existe task genérica de envio: `src/messaging/tasks.py::send_whatsapp_message`.
* O provider atual está em `src/messaging/whatsapp.py` e usa NewByte.
* Há template configurado para cenário de hóspede (`reservation_canceled_resell_on_szn_website`).
* Não existe hoje integração Blip para envio de WhatsApp ao franqueado.