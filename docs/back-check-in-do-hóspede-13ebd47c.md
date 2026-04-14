<!-- title: [Back] Check-in do hóspede | url: https://outline.seazone.com.br/doc/back-check-in-do-hospede-hjBuf9kUEK | area: Tecnologia -->

# [Back] Check-in do hóspede

# Checkin do Hóspede

Fluxo onde o hóspede preenche informações pessoais e preferências de estadia antes da data de check-in.

## Rotas

| Método | Rota | UseCase | Descrição |
|----|----|----|----|
| POST | `/checkin/start` | CheckinStartUseCase | Inicia o pré-checkin |
| POST | `/checkin/guest/` | CheckinGuestUseCase | Cria hóspede |
| GET | `/checkin/guest/` | CheckinGuestUseCase | Lista hóspedes |
| GET | `/checkin/guest/{id}` | CheckinGuestUseCase | Detalha hóspede |
| PATCH | `/checkin/guest/{id}` | CheckinGuestUseCase | Atualiza hóspede |
| POST | `/checkin/arrival-info` | CheckinArrivalInfoUseCase | Cria info de chegada |
| GET | `/checkin/arrival-info` | CheckinArrivalInfoUseCase | Consulta info de chegada |
| PATCH | `/checkin/arrival-info` | CheckinArrivalInfoUseCase | Atualiza info de chegada |
| POST | `/checkin/bed-arrangement` | CheckinBedArrangementUseCase | Cria arranjo de camas |
| GET | `/checkin/bed-arrangement` | CheckinBedArrangementUseCase | Consulta arranjo de camas |
| PATCH | `/checkin/bed-arrangement` | CheckinBedArrangementUseCase | Atualiza arranjo de camas |
| GET | `/checkin/complete` | CheckinCompleteUseCase | Consulta status do checkin |
| POST | `/checkin/complete` | CheckinCompleteUseCase | Finaliza o checkin |

## Fluxo

O checkin é composto por três etapas:


1. **Início** (`POST /start`) — inicializa o pré-checkin para a reserva
2. **Preenchimento** — consumo e atualização de dados via rotas de hóspedes, informações de chegada e arranjo de camas
3. **Conclusão** (`POST /complete`) — valida e finaliza o checkin

### Início do Checkin

```mermaidjs

sequenceDiagram
    actor Guest as Hóspede
    participant API as Checkin API
    participant Start as CheckinStartUseCase
    participant ReservationRepo as ReservationRepository

    Guest->>API: POST /checkin/start
    API->>Start: start_checkin(reservation_id)
    Start->>ReservationRepo: init_precheckin()
    ReservationRepo-->>Start: precheckin criado
    Start-->>Guest: StartCheckinResponse
```

### Hóspedes

```mermaidjs

sequenceDiagram
    actor Guest as Hóspede
    participant API as Checkin API
    participant GuestUC as CheckinGuestUseCase
    participant ReservationRepo as ReservationRepository

    Guest->>API: POST /checkin/guest/
    API->>GuestUC: create_guest(reservation_id, payload)
    GuestUC->>ReservationRepo: create_reservation_guest()
    ReservationRepo-->>GuestUC: guest criado
    GuestUC-->>Guest: CheckinGuestResponse

    Guest->>API: GET /checkin/guest/
    API->>GuestUC: get_guests(reservation_id)
    GuestUC->>ReservationRepo: get_guests_by_reservation_id()
    ReservationRepo-->>GuestUC: lista de guests
    GuestUC-->>Guest: ListCheckinGuestsResponse

    Guest->>API: GET /checkin/guest/{id}
    API->>GuestUC: get_guest(reservation_id, id)
    GuestUC->>ReservationRepo: get_guest_by_id_and_reservation()
    ReservationRepo-->>GuestUC: guest
    GuestUC-->>Guest: CheckinGuestResponse

    Guest->>API: PATCH /checkin/guest/{id}
    API->>GuestUC: patch_guest(reservation_id, id, payload)
    GuestUC->>ReservationRepo: update_reservation_guest()
    ReservationRepo-->>GuestUC: guest atualizado
    GuestUC-->>Guest: CheckinGuestResponse
```

### Informações de Chegada

```mermaidjs

sequenceDiagram
    actor Guest as Hóspede
    participant API as Checkin API
    participant Arrival as CheckinArrivalInfoUseCase
    participant ReservationRepo as ReservationRepository

    Guest->>API: POST /checkin/arrival-info
    API->>Arrival: create_arrival_info(reservation_id, payload)
    Arrival->>ReservationRepo: patch_precheckin()
    ReservationRepo-->>Arrival: arrival info criado
    Arrival-->>Guest: CheckinArrivalInfoResponse

    Guest->>API: GET /checkin/arrival-info
    API->>Arrival: get_arrival_info(reservation_id)
    Arrival->>ReservationRepo: get_precheckin_by_reservation_id()
    ReservationRepo-->>Arrival: arrival info
    Arrival-->>Guest: CheckinArrivalInfoResponse

    Guest->>API: PATCH /checkin/arrival-info
    API->>Arrival: patch_arrival_info(reservation_id, payload)
    Arrival->>ReservationRepo: patch_precheckin()
    ReservationRepo-->>Arrival: arrival info atualizado
    Arrival-->>Guest: CheckinArrivalInfoResponse
```

### Arranjo de Camas

```mermaidjs

sequenceDiagram
    actor Guest as Hóspede
    participant API as Checkin API
    participant Bed as CheckinBedArrangementUseCase
    participant ReservationRepo as ReservationRepository

    Guest->>API: POST /checkin/bed-arrangement
    API->>Bed: create_bed_arrangement(reservation_id, payload)
    Bed->>ReservationRepo: update_bed_arrangement()
    ReservationRepo-->>Bed: bed arrangement criado
    Bed-->>Guest: CheckinBedArrangementResponse

    Guest->>API: GET /checkin/bed-arrangement
    API->>Bed: get_bed_arrangement(reservation_id)
    Bed->>ReservationRepo: get_precheckin_by_reservation_id()
    ReservationRepo-->>Bed: bed arrangement
    Bed-->>Guest: CheckinBedArrangementResponse

    Guest->>API: PATCH /checkin/bed-arrangement
    API->>Bed: patch_bed_arrangement(reservation_id, payload)
    Bed->>ReservationRepo: update_bed_arrangement()
    ReservationRepo-->>Bed: bed arrangement atualizado
    Bed-->>Guest: CheckinBedArrangementResponse
```

### Conclusão do Checkin

```mermaidjs

sequenceDiagram
    actor Guest as Hóspede
    participant API as Checkin API
    participant Complete as CheckinCompleteUseCase
    participant ReservationRepo as ReservationRepository

    Guest->>API: GET /checkin/complete
    API->>Complete: get_checkin_status(reservation_id)
    Complete->>ReservationRepo: get_precheckin_by_reservation_id()
    ReservationRepo-->>Complete: status atual
    Complete-->>Guest: CompleteCheckinResponse

    Guest->>API: POST /checkin/complete
    API->>Complete: complete_checkin(reservation_id)
    Complete->>ReservationRepo: valida dados e finaliza
    ReservationRepo-->>Complete: checkin completo
    Complete-->>Guest: CompleteCheckinResponse
```

## Diagrama de Classes — UseCases e Repositories

```mermaidjs

classDiagram
    class ReservationRepository {
        +get_reservation_by_id()
        +init_precheckin()
        +get_precheckin_by_reservation_id()
        +create_precheckin()
        +patch_precheckin()
        +get_guests_by_reservation_id()
        +get_guest_by_id_and_reservation()
        +create_reservation_guest()
        +update_reservation_guest()
        +update_bed_arrangement()
        +get_expected_guest_count()
        +save_file_and_generate_uid()
    }

    class UserRepository {
        +get_user()
        +get_user_by_email()
        +update_email()
        +update_phone_number()
    }

    class GuestRepository {
        +get_guest_by_user_id()
        +get_by_id()
        +update_user_id()
    }

    class UserIdentifierMappingRepository {
        +create_identifier_mapping()
    }

    class FeatureFlagService {
        +is_enabled()
    }

    class CheckinStartUseCase {
        +start_checkin(reservation_id)
    }

    class CheckinGuestUseCase {
        +create_guest(reservation_id, payload)
        +get_guests(reservation_id)
        +get_guest(reservation_id, reservation_guest_id)
        +patch_guest(reservation_id, reservation_guest_id, payload)
    }

    class CheckinArrivalInfoUseCase {
        +get_arrival_info(reservation_id)
        +create_arrival_info(reservation_id, payload)
        +patch_arrival_info(reservation_id, payload)
    }

    class CheckinBedArrangementUseCase {
        +get_bed_arrangement(reservation_id)
        +create_bed_arrangement(reservation_id, payload)
        +patch_bed_arrangement(reservation_id, payload)
    }

    class CheckinCompleteUseCase {
        +get_checkin_status(reservation_id)
        +complete_checkin(reservation_id)
    }

    %% Start route
    CheckinStartUseCase --> ReservationRepository

    %% Guest route
    CheckinGuestUseCase --> ReservationRepository
    CheckinGuestUseCase --> UserRepository
    CheckinGuestUseCase --> GuestRepository
    CheckinGuestUseCase --> UserIdentifierMappingRepository
    CheckinGuestUseCase --> FeatureFlagService

    %% Arrival Info route
    CheckinArrivalInfoUseCase --> ReservationRepository

    %% Bed Arrangement route
    CheckinBedArrangementUseCase --> ReservationRepository

    %% Complete route
    CheckinCompleteUseCase --> ReservationRepository
    CheckinCompleteUseCase --> UserRepository
    CheckinCompleteUseCase --> GuestRepository
    CheckinCompleteUseCase --> UserIdentifierMappingRepository
    CheckinCompleteUseCase --> FeatureFlagService
```