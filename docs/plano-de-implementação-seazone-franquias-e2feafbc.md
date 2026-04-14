<!-- title: Plano de Implementação — Seazone Franquias | url: https://outline.seazone.com.br/doc/plano-de-implementacao-seazone-franquias-Mcb16w4xse | area: Tecnologia -->

# Plano de Implementação — Seazone Franquias

## Premissas Arquiteturais

| Decisão | Valor |
|----|----|
| Perfil de acesso | **HOST** (franqueado = host no sapron-backend) |
| Backend Fase 1 | **sapron-backend** (rotas existentes) |
| Backend Fases 2+ | **Microserviço novo** (`franquias-api`) |
| Financeiro | **Misto** — despesas operacionais via sapron, fornecedores/estoque/reembolsos em serviço novo |
| Auth | JWT do sapron (`/account/login/token/`) compartilhado via gateway ou token relay |


---

## FASE 1 — Integração Frontend com Sapron-Backend

**Objetivo:** Substituir 100% dos dados mockados pelas APIs reais do sapron nas páginas que já possuem endpoints compatíveis. Zero código de backend novo.

### 1.1 Autenticação & Sessão

| Página | Endpoint Sapron | Método |
|----|----|----|
| Login | `/account/login/token/` | POST |
| Refresh token | `/account/login/token/refresh/` | POST |
| Dados do usuário logado | `/account/host/{id}/` | GET |
| Logout | `/account/logout/` | GET |

**Tarefas:**

* Criar `AuthContext` com JWT (access + refresh)
* Interceptor Axios para token refresh automático
* Guard de rotas protegidas
* Filtrar dados por `host_id` em todas as queries

### 1.2 Dash do Dia (`/`)

| Seção | Endpoint Sapron | Notas |
|----|----|----|
| KPIs (imóveis ativos) | `/property/active_properties/` | Filtrar por host |
| Resumo check-ins/outs | `/host_controller/dash/summary/` | Resumo diário |
| Checklist do dia | `/host_controller/dash/checklist/` | Checklist consolidado |
| Check-ins pendentes | `/host_controller/v2/checkin/?date=hoje` | Filtro por data |
| Incidentes do dia | `/guest_damage/?date=hoje` | Danos registrados |

> Seção de limpezas fica como "Em breve" ou apenas contadores do `dash/summary/`.

### 1.3 Operação (`/operacao`)

| Seção | Endpoint Sapron | Notas |
|----|----|----|
| Lista de imóveis + timeline | `/host_controller/v2/checkin/` + `/host_controller/checkout/` | Combinar 2 endpoints |
| Detalhes do imóvel | `/properties/details/{id}/` | Detalhes completos |
| Detalhes operacionais | `/property/operational_details/{id}/` | Horários, acesso |
| Checklists check-in | `/checkin/checklist/reservation/{id}/` | Por reserva |
| Checklists check-out | `/checkout/checklist/reservation/{id}/` | Por reserva |
| Iniciar check-in | `/check_in_controller/` | POST |
| Iniciar check-out | `/check_out_controller/` | POST |

> Timeline com 2 fases (check-out → check-in). Limpeza entra na Fase 2.

### 1.4 Reservas / Multicalendar (`/reservas`)

| Seção | Endpoint Sapron |
|----|----|
| Calendário de reservas | `/reservations/calendar/` |
| Calendário de imóveis | `/calendar/properties/` |
| Lista de reservas | `/reservations/list/` |
| Bloqueios | `/calendar/v2/blocking/` |
| Detalhes reserva | `/reservation/{id}/` |
| Resumo reserva | `/reservations/{id}/summary/` |

### 1.5 Check-in Control (`/checkin`)

| Seção | Endpoint Sapron |
|----|----|
| Cards de check-in | `/host_controller/v2/checkin/` |
| Checklist | `/checkin/checklist/reservation/{id}/` |
| Pré-checkin | `/precheckin/` |

### 1.6 Incidentes (`/incidentes`)

| Seção | Endpoint Sapron |
|----|----|
| Lista de danos | `/guest_damage/` |
| Evidências | `/guest_damage_evidence/` |
| Negociação | `/guest_damage_negotiation/` |
| Histórico | `/guest_damage_negotiation_history/` |
| Relatórios de incidentes | `/reservations/reservation_incident_reports/` |

### 1.7 Imóveis (`/imoveis`)

| Seção | Endpoint Sapron |
|----|----|
| Lista de imóveis do host | `/properties/host/` |
| Detalhes | `/properties/details/{id}/` |
| Amenidades | `/property/amenities/` |
| Imagens | `/property/images/` |
| Regras | `/property/rules/` |
| Documentos | `/property/documents/` |

### 1.8 Financeiro — Parcial (`/financeiro`)

| Seção | Endpoint Sapron |
|----|----|
| Despesas operacionais | `/expenses/` |
| Categorias de despesas | `/expenses/categories/` |
| Anexos de despesas | `/expenses_files/` |
| Taxa de franquia | `/host_franchise_fee/` |
| Pagamento taxa | `/financial-host-franchise-fee-payment/` |
| Relatório financeiro | `/reports/property_financial_audit/` |
| Relatório despesas | `/reports/property_expenses/` |

### 1.9 Process Wizard

| Processo | Endpoints Sapron |
|----|----|
| Check-in | POST `/check_in_controller/` + `/checkin/checklist/reservation/` |
| Check-out | POST `/check_out_controller/` + `/checkout/checklist/reservation/` |
| Dano | POST `/guest_damage/` + `/guest_damage_evidence/` |
| Upload fotos | POST `/files/` |

### 1.10 Infraestrutura Fase 1

**Criar na camada frontend:**

* `src/services/api.ts` — Axios instance com baseURL do sapron, interceptors JWT
* `src/services/auth.ts` — Login, refresh, logout
* `src/hooks/useAuth.ts` — Context + hook de autenticação
* `src/hooks/queries/` — React Query hooks por domínio (`useProperties`, `useReservations`, `useOperations`, `useFinancial`, `useIncidents`)
* Variável de ambiente `VITE_SAPRON_API_URL`
* CORS no sapron para o domínio do franquias

### Páginas com placeholder "Em breve" na Fase 1

`/limpezas`, `/vistorias`, `/planejamento`, `/score/*`, `/manutencoes`, `/ocorrencias`, `/visitas`, `/configuracoes`, `/configuracoes/pessoas`, `/financeiro/lancamentos`, `/financeiro/contas-recorrentes`, `/financeiro/recibos`, `/financeiro/fornecedores`, `/financeiro/compras-estoque`, `/financeiro/reembolsos`


---

## FASE 2 — Microserviço Core + Limpezas

**Objetivo:** Criar o microserviço `franquias-api`, entidade de franquia, gestão de pessoas, planejamento D-1 e módulo completo de limpezas.

### 2.1 Tabelas — Franchise Core

```
franchise
├── id (UUID)
├── name, city, state
├── sapron_host_id (referência ao host no sapron)
├── contract_start_date
├── status (active, suspended, cancelled)
├── created_at, updated_at

franchise_member
├── id (UUID)
├── franchise_id (FK)
├── sapron_user_id (referência externa)
├── role (admin, operator, cleaner, maintenance)
├── permissions (JSONB)
├── invite_status (pending, accepted, revoked)
├── invited_at, accepted_at

franchise_collaborator
├── id (UUID)
├── franchise_id (FK)
├── name, phone, email
├── role (cleaner, maintenance_tech, inspector)
├── availability (JSONB — dias/horários)
├── active (bool)

planning_assignment
├── id (UUID)
├── franchise_id (FK)
├── collaborator_id (FK)
├── sapron_property_id, sapron_reservation_id
├── date
├── task_type (checkin, checkout, cleaning, inspection)
├── scheduled_time, estimated_duration_min
├── route_order (int)
├── status (planned, in_progress, completed, cancelled)
├── notes
```

### 2.2 Tabelas — Limpezas

```
cleaning_team
├── id (UUID)
├── franchise_id (FK)
├── name (ex: "Equipe A - Praia")
├── leader_id (FK → franchise_collaborator)
├── active, created_at, updated_at

cleaning_team_member
├── id (UUID)
├── team_id (FK)
├── collaborator_id (FK)
├── role (leader, cleaner, helper)
├── joined_at

cleaning_checklist_template
├── id (UUID)
├── franchise_id (FK)
├── name (ex: "Padrão Studio", "Padrão 2Q")
├── property_type (studio, 1q, 2q, 3q, house, all)
├── items (JSONB — [{order, category, description, required, photo_required}])
├── estimated_duration_min (int)
├── version (int), active

cleaning_task
├── id (UUID)
├── franchise_id (FK)
├── sapron_property_id
├── sapron_reservation_checkout_id (nullable)
├── sapron_reservation_checkin_id (nullable)
├── template_id (FK)
├── team_id (FK nullable)
├── assigned_to (FK nullable)
├── date
├── scheduled_start_time, scheduled_end_time
├── actual_start_time, actual_end_time
├── status (pending, assigned, in_progress, review, completed, cancelled, rescheduled)
├── priority (normal, urgent, express)
├── origin (checkout, preventive, deep_clean, guest_request, manual)
├── notes, created_at, updated_at

cleaning_task_execution
├── id (UUID)
├── task_id (FK)
├── started_by (FK)
├── checklist_results (JSONB — [{item_id, checked, photo_url, notes}])
├── completion_percentage (decimal 0-100)
├── started_at, completed_at
├── quality_score (decimal 0-10, nullable)
├── reviewed_by (FK nullable), review_notes, reviewed_at

cleaning_task_photo
├── id (UUID)
├── execution_id (FK)
├── checklist_item_id (nullable)
├── photo_url (S3)
├── photo_type (before, after, issue)
├── room_area, uploaded_at

cleaning_supply_usage
├── id (UUID)
├── execution_id (FK)
├── item_id (FK → inventory_item, nullable até Fase 3)
├── quantity_used, notes

cleaning_schedule_rule
├── id (UUID)
├── franchise_id (FK)
├── sapron_property_id (nullable — null = regra global)
├── rule_type (post_checkout, preventive, deep_clean)
├── frequency (nullable — weekly, biweekly, monthly)
├── day_of_week (nullable)
├── preferred_team_id (FK nullable)
├── template_id (FK)
├── buffer_after_checkout_min (int, default 30)
├── buffer_before_checkin_min (int, default 60)
├── auto_assign (bool), active
```

### 2.3 Endpoints — Franchise Core

```
GET/POST   /api/v1/franchises/
GET/PUT    /api/v1/franchises/{id}/

GET/POST   /api/v1/franchises/{id}/members/
PUT/DELETE /api/v1/franchises/{id}/members/{member_id}/
POST       /api/v1/franchises/{id}/members/invite/

GET/POST   /api/v1/franchises/{id}/collaborators/
PUT/DELETE /api/v1/franchises/{id}/collaborators/{collab_id}/

GET/POST   /api/v1/planning/assignments/
PUT/DELETE /api/v1/planning/assignments/{id}/
GET        /api/v1/planning/daily/?date=YYYY-MM-DD
POST       /api/v1/planning/optimize-route/
```

### 2.4 Endpoints — Limpezas

```
# Equipes
GET/POST   /api/v1/cleaning/teams/
GET/PUT/DEL /api/v1/cleaning/teams/{id}/
POST       /api/v1/cleaning/teams/{id}/members/
DELETE     /api/v1/cleaning/teams/{id}/members/{member_id}/

# Templates de Checklist
GET/POST   /api/v1/cleaning/templates/
GET/PUT/DEL /api/v1/cleaning/templates/{id}/
POST       /api/v1/cleaning/templates/{id}/duplicate/

# Tarefas de Limpeza
GET/POST   /api/v1/cleaning/tasks/
GET/PUT    /api/v1/cleaning/tasks/{id}/
POST       /api/v1/cleaning/tasks/{id}/assign/
POST       /api/v1/cleaning/tasks/{id}/start/
POST       /api/v1/cleaning/tasks/{id}/complete/
POST       /api/v1/cleaning/tasks/{id}/review/
GET        /api/v1/cleaning/tasks/daily/?date=YYYY-MM-DD
GET        /api/v1/cleaning/tasks/by-property/{property_id}/
GET        /api/v1/cleaning/tasks/by-team/{team_id}/
GET        /api/v1/cleaning/tasks/overdue/

# Execução
GET/POST   /api/v1/cleaning/tasks/{id}/execution/
PUT        /api/v1/cleaning/tasks/{id}/execution/checklist/
POST       /api/v1/cleaning/tasks/{id}/execution/photos/

# Consumo de Suprimentos
POST       /api/v1/cleaning/tasks/{id}/execution/supplies/

# Regras de Agendamento
GET/POST   /api/v1/cleaning/schedule-rules/
GET/PUT/DEL /api/v1/cleaning/schedule-rules/{id}/

# Dashboard de Limpeza
GET        /api/v1/cleaning/dashboard/?date=YYYY-MM-DD
GET        /api/v1/cleaning/dashboard/performance/?from=&to=

# Auto-geração
POST       /api/v1/cleaning/tasks/generate-from-checkouts/
```

### 2.5 Job de Integração Limpeza ↔ Sapron

Job diário (cron) que:


1. Consulta sapron: `GET /host_controller/checkout/?date=amanhã`
2. Consulta sapron: `GET /host_controller/v2/checkin/?date=amanhã`
3. Para cada checkout → cria `cleaning_task` com `origin=checkout`
4. Aplica `cleaning_schedule_rule` para definir equipe, template e horários
5. Calcula `scheduled_start_time` = checkout_time + buffer
6. Calcula `scheduled_end_time` = checkin_time - buffer
7. Se `auto_assign=true`, atribui equipe/colaborador disponível

**Comunicação com sapron:** REST server-to-server usando API Key (`X-Sapron-API-Key`).


---

## FASE 3 — Financeiro Independente + Estoque

**Objetivo:** Módulo financeiro completo da franquia, independente do sapron, com fornecedores, estoque e reembolsos.

### 3.1 Tabelas

```
financial_supplier
├── id, franchise_id (FK)
├── name, cnpj, phone, email
├── category (cleaning, maintenance, supplies, other)
├── bank_name, bank_agency, bank_account, pix_key
├── active, notes

financial_category
├── id, franchise_id (FK)
├── name, type (income, expense)
├── parent_id (FK self — subcategorias)
├── color, icon

financial_transaction
├── id, franchise_id (FK)
├── type (income, expense)
├── category_id (FK), supplier_id (FK nullable)
├── sapron_property_id (nullable), sapron_reservation_id (nullable)
├── description, amount (decimal)
├── date, due_date, paid_date
├── status (pending, paid, overdue, cancelled)
├── payment_method (pix, transfer, cash, card, boleto)
├── receipt_url (S3), notes, created_by

financial_recurring_bill
├── id, franchise_id (FK)
├── category_id (FK), supplier_id (FK nullable)
├── description, amount (decimal)
├── frequency (monthly, weekly, biweekly, quarterly, yearly)
├── day_of_month / day_of_week
├── start_date, end_date (nullable)
├── auto_generate (bool), active

financial_receipt
├── id, franchise_id (FK)
├── transaction_id (FK nullable)
├── file_url (S3)
├── type (nf, receipt, invoice, other)
├── issued_at, notes

financial_reimbursement
├── id, franchise_id (FK)
├── requested_by (user_id), transaction_id (FK nullable)
├── amount, description
├── receipt_urls (JSONB)
├── status (pending, approved, rejected, paid)
├── reviewed_by, reviewed_at, paid_at

inventory_item
├── id, franchise_id (FK)
├── name, category, unit (un, kg, L, pack)
├── current_quantity, min_quantity (alerta)
├── cost_per_unit
├── supplier_id (FK nullable), sapron_property_id (nullable)

inventory_movement
├── id, item_id (FK)
├── type (purchase, usage, adjustment, return)
├── quantity (+ ou -)
├── sapron_property_id (nullable)
├── date, notes, created_by

purchase_order
├── id, franchise_id (FK), supplier_id (FK)
├── items (JSONB — [{item_id, qty, unit_price}])
├── total_amount
├── status (draft, ordered, received, cancelled)
├── ordered_at, received_at, notes
```

### 3.2 Endpoints

```
# Fornecedores
GET/POST   /api/v1/financial/suppliers/
GET/PUT/DEL /api/v1/financial/suppliers/{id}/

# Categorias
GET/POST   /api/v1/financial/categories/
GET/PUT/DEL /api/v1/financial/categories/{id}/

# Lançamentos
GET/POST   /api/v1/financial/transactions/
GET/PUT/DEL /api/v1/financial/transactions/{id}/
GET        /api/v1/financial/transactions/summary/?month=&year=
GET        /api/v1/financial/transactions/export/csv/

# Contas Recorrentes
GET/POST   /api/v1/financial/recurring-bills/
GET/PUT/DEL /api/v1/financial/recurring-bills/{id}/
POST       /api/v1/financial/recurring-bills/generate/

# Recibos
GET/POST   /api/v1/financial/receipts/
GET/DEL    /api/v1/financial/receipts/{id}/

# Notas Fiscais (complementar ao sapron)
GET/POST   /api/v1/financial/invoices/
GET/PUT    /api/v1/financial/invoices/{id}/

# Reembolsos
GET/POST   /api/v1/financial/reimbursements/
GET/PUT    /api/v1/financial/reimbursements/{id}/
POST       /api/v1/financial/reimbursements/{id}/approve/
POST       /api/v1/financial/reimbursements/{id}/reject/

# Estoque
GET/POST   /api/v1/inventory/items/
GET/PUT/DEL /api/v1/inventory/items/{id}/
GET        /api/v1/inventory/items/low-stock/
POST       /api/v1/inventory/movements/
GET        /api/v1/inventory/movements/?item_id=&date_from=&date_to=

# Compras
GET/POST   /api/v1/inventory/purchase-orders/
GET/PUT    /api/v1/inventory/purchase-orders/{id}/
POST       /api/v1/inventory/purchase-orders/{id}/receive/

# Dashboard Financeiro (agregação mista sapron + microserviço)
GET        /api/v1/financial/dashboard/?year=&month=
GET        /api/v1/financial/dashboard/by-property/
GET        /api/v1/financial/dashboard/by-category/
```


---

## FASE 4 — Score, Manutenções, Ocorrências + Vistorias & Implantação

**Objetivo:** 4 domínios distintos, altamente paralelizáveis (até 4 agentes simultâneos).

### 4.1 Tabelas — Score

```
franchise_score
├── id, franchise_id (FK)
├── period (YYYY-MM)
├── operational_score, financial_score, review_score
├── cleanliness_score, response_time_score
├── total_score (decimal 0-100)
├── ranking_position (int)
├── classification (ouro, prata, bronze)
├── calculated_at

franchise_score_detail
├── id, score_id (FK)
├── metric_name, metric_value, weight, weighted_value, notes
```

### 4.2 Tabelas — Manutenções Preventivas

```
maintenance_plan
├── id, franchise_id (FK), sapron_property_id
├── name (ex: "Revisão ar-condicionado")
├── category (electrical, plumbing, hvac, structural, appliance, general)
├── frequency (monthly, quarterly, semiannual, annual)
├── last_executed_at, next_due_date
├── estimated_cost
├── assigned_to (FK → franchise_collaborator nullable)
├── active

maintenance_execution
├── id, plan_id (FK)
├── executed_at, executed_by (FK)
├── status (scheduled, in_progress, completed, skipped)
├── cost_actual, notes, photos (JSONB — S3 URLs)
```

### 4.3 Tabelas — Ocorrências

```
occurrence
├── id, franchise_id (FK)
├── sapron_property_id (nullable), sapron_reservation_id (nullable)
├── type (guest_complaint, neighbor_complaint, noise, rule_violation,
│         equipment_failure, safety, other)
├── priority (low, medium, high, critical)
├── title, description
├── reported_by, reported_at
├── status (open, investigating, resolved, closed)
├── resolution_notes, resolved_at, resolved_by
├── impacts_score (bool)

occurrence_comment
├── id, occurrence_id (FK), author_id, body, created_at

occurrence_attachment
├── id, occurrence_id (FK), file_url, file_type (image, document, video)
```

### 4.4 Tabelas — Visitas

```
visit_report
├── id, franchise_id (FK), sapron_property_id
├── visitor_id (FK → franchise_collaborator)
├── visit_date
├── type (routine, post_checkout, pre_checkin, maintenance, inspection)
├── checklist_results (JSONB), notes, photos (JSONB)
├── status (scheduled, completed, cancelled)
```

### 4.5 Tabelas — Vistorias & Implantação

```
inspection_template
├── id, franchise_id (FK)
├── name (ex: "Vistoria de Implantação", "Vistoria Trimestral")
├── type (implantation, periodic, post_damage, pre_season, checkout_audit)
├── sections (JSONB — [{section_name, items: [{id, description,
│     type (boolean|rating|text|photo), required, weight}]}])
├── passing_score (decimal nullable)
├── version (int), active

inspection
├── id, franchise_id (FK), sapron_property_id
├── template_id (FK)
├── type, scheduled_date, executed_date (nullable)
├── inspector_id (FK → franchise_collaborator)
├── status (scheduled, in_progress, completed, approved, failed, requires_action)
├── overall_score (decimal 0-100 nullable), passed (bool nullable)
├── notes, created_by, created_at, updated_at

inspection_result
├── id, inspection_id (FK)
├── section_name, item_id, item_description
├── result_value (varchar), result_type (boolean, rating, text, photo)
├── conformity (conform, non_conform, na), notes

inspection_photo
├── id, inspection_id (FK), result_id (FK nullable)
├── photo_url (S3), caption, room_area
├── photo_type (evidence, before, after), uploaded_at

inspection_action_item
├── id, inspection_id (FK), result_id (FK nullable)
├── description
├── priority (low, medium, high, critical)
├── assigned_to (FK nullable), due_date
├── status (open, in_progress, completed, cancelled)
├── resolution_notes, resolved_at
├── creates_maintenance (bool)
├── maintenance_plan_id (FK nullable)

property_implantation
├── id, franchise_id (FK), sapron_property_id
├── started_at, target_go_live_date
├── status (not_started, documentation, inspection, furnishing,
│           photography, listing, review, live, blocked)
├── current_phase (int 1-8), completed_at (nullable), notes

implantation_phase
├── id, implantation_id (FK)
├── phase_number (int 1-8)
├── phase_name (documentação, vistoria_inicial, mobília_enxoval,
│               fotografia, criação_anúncio, revisão_final, go_live, primeira_reserva)
├── status (pending, in_progress, completed, blocked)
├── responsible_id (FK nullable)
├── started_at, completed_at
├── checklist (JSONB), blocking_reason (nullable)
├── inspection_id (FK → inspection, nullable)
```

### 4.6 Endpoints

```
# Score
GET        /api/v1/score/dashboard/
GET        /api/v1/score/history/?from=&to=
GET        /api/v1/score/ranking/
GET        /api/v1/score/details/{period}/
GET        /api/v1/score/reviews/           (proxy → sapron reviews)
GET        /api/v1/score/reports/
GET        /api/v1/score/faq/

# Manutenções Preventivas
GET/POST   /api/v1/maintenance/plans/
GET/PUT/DEL /api/v1/maintenance/plans/{id}/
GET/POST   /api/v1/maintenance/executions/
GET/PUT    /api/v1/maintenance/executions/{id}/
GET        /api/v1/maintenance/calendar/?month=&year=
GET        /api/v1/maintenance/overdue/

# Ocorrências
GET/POST   /api/v1/occurrences/
GET/PUT    /api/v1/occurrences/{id}/
POST       /api/v1/occurrences/{id}/comments/
POST       /api/v1/occurrences/{id}/attachments/
POST       /api/v1/occurrences/{id}/resolve/

# Visitas
GET/POST   /api/v1/visits/
GET/PUT    /api/v1/visits/{id}/
GET        /api/v1/visits/calendar/?month=&year=

# Templates de Vistoria
GET/POST   /api/v1/inspections/templates/
GET/PUT/DEL /api/v1/inspections/templates/{id}/
POST       /api/v1/inspections/templates/{id}/duplicate/

# Vistorias
GET/POST   /api/v1/inspections/
GET/PUT    /api/v1/inspections/{id}/
POST       /api/v1/inspections/{id}/start/
POST       /api/v1/inspections/{id}/complete/
POST       /api/v1/inspections/{id}/approve/
POST       /api/v1/inspections/{id}/fail/
GET        /api/v1/inspections/by-property/{property_id}/
GET        /api/v1/inspections/calendar/?month=&year=
GET        /api/v1/inspections/overdue/

# Resultados
GET/POST   /api/v1/inspections/{id}/results/
PUT        /api/v1/inspections/{id}/results/{result_id}/
POST       /api/v1/inspections/{id}/photos/

# Action Items (pendências)
GET/POST   /api/v1/inspections/{id}/action-items/
PUT        /api/v1/inspections/{id}/action-items/{item_id}/
POST       /api/v1/inspections/{id}/action-items/{item_id}/resolve/
GET        /api/v1/inspections/action-items/open/

# Implantação
GET/POST   /api/v1/implantations/
GET/PUT    /api/v1/implantations/{id}/
GET        /api/v1/implantations/{id}/phases/
PUT        /api/v1/implantations/{id}/phases/{phase_number}/
POST       /api/v1/implantations/{id}/phases/{phase_number}/complete/
POST       /api/v1/implantations/{id}/phases/{phase_number}/block/
GET        /api/v1/implantations/active/

# Dashboard Vistorias
GET        /api/v1/inspections/dashboard/
```


---

## FASE 5 — Configurações, Gestão de Pessoas & Comunicação

**Objetivo:** Escopo menor, fecha o sistema.

### 5.1 Tabelas

```
franchise_config
├── id, franchise_id (FK)
├── default_checkin_time, default_checkout_time
├── cleaning_buffer_minutes (int)
├── auto_assign_cleaning (bool)
├── notification_channels (JSONB)
├── score_goals (JSONB)
├── financial_closing_day (int 1-28)

franchise_notification
├── id, franchise_id (FK)
├── recipient_id
├── channel (whatsapp, email, push, sms)
├── type (checkin_reminder, checkout_alert, cleaning_assigned, etc.)
├── title, body, sent_at
├── status (pending, sent, delivered, failed)

message_template
├── id, franchise_id (FK)
├── name, channel (whatsapp, email)
├── trigger_event, subject, body_template (com {{variáveis}})
├── active
```

### 5.2 Endpoints

```
# Configurações
GET/PUT    /api/v1/config/
GET/PUT    /api/v1/config/notifications/
GET/PUT    /api/v1/config/score-goals/

# Gestão de Pessoas
POST       /api/v1/members/invite/
POST       /api/v1/members/{id}/resend-invite/
PUT        /api/v1/members/{id}/permissions/
POST       /api/v1/members/{id}/deactivate/

# Templates de Mensagem
GET/POST   /api/v1/messages/templates/
GET/PUT/DEL /api/v1/messages/templates/{id}/
POST       /api/v1/messages/send/
GET        /api/v1/messages/history/
```


---

## Resumo Consolidado

### Cronograma

| Fase | Escopo | Tabelas | Endpoints |
|:---:|----|:---:|:---:|
| **1** | Frontend ↔ Sapron (auth, dash, operação, reservas, checkin, incidentes, imóveis, financeiro parcial) | 0 | 0 (consome \~40 do sapron) |
| **2** | Microserviço core + Limpezas completo | 14 | \~35 |
| **3** | Financeiro independente + Estoque | 9 | \~30 |
| **4** | Score + Manutenções + Ocorrências + Vistorias & Implantação | 16 | \~40 |
| **5** | Config + Pessoas + Notificações | 3 | \~12 |
| **Total** |    | **42** | **\~117** |

### Desbloqueio de Páginas por Fase

| Fase | Páginas Desbloqueadas |
|:---:|----|
| 1 | Login, Dash do Dia (parcial), Operação (2 fases), Reservas, Check-in, Incidentes, Imóveis, Financeiro (dashboard + despesas sapron) |
| 2 | Dash do Dia (completo), Operação (3 fases com limpeza), Limpezas, Planejamento D-1 |
| 3 | Financeiro completo (lançamentos, recorrentes, fornecedores, estoque, reembolsos, recibos) |
| 4 | Score (5 sub-páginas), Manutenções Preventivas, Ocorrências, Visitas, Vistorias & Implantação |
| 5 | Configurações, Gestão de Pessoas |

###