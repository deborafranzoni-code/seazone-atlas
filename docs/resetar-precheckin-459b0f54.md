<!-- title: Resetar PreCheckIn | url: https://outline.seazone.com.br/doc/resetar-precheckin-37jwucFzWQ | area: Tecnologia -->

# Resetar PreCheckIn

### Se precisasse resetar um pré-checkin JÁ preenchido

Caso fosse uma reserva que o hóspede **já completou** e quisesse zerar tudo, seria preciso alterar **4 locais**:

| # | Tabela | Ação |
|----|----|----|
| 1 | `reservation_reservation` | Setar `is_pre_checkin_completed = false`, `is_pre_checkin_link_sent = false`, `link_sent_at = null`, `pre_checkin_fullfilled_at = null` |
| 2 | `reservation_precheckin` | Deletar o registro com `reservation_id = <id>` |
| 3 | `reservation_guests` | Deletar os registros com `reservation_id = <id>` |
| 4 | `reservation_precheckin_message_attempts` | Opcional — são logs, podem ficar |

A API `**PATCH /precheckin/**` com o `PreCheckinUpdateSerializer` já permite atualizar as flags do item 1. Os itens 2 e 3 precisariam ser feitos via admin ou diretamente no banco.