<!-- title: Atualização automática de dados (Celery) | url: https://outline.seazone.com.br/doc/atualizacao-automatica-de-dados-celery-xuyJd9XQMI | area: Tecnologia -->

# Atualização automática de dados (Celery)

Tarefas que hoje rodam de tempos em tempos no Sapron para atualização/consolidação de dados:

| **"Traduzido"** | **Nome da task** | **Frequência** | **Frequência** |
|----|----|----|----|
| Atualiza/Importa reservas da Stays (criadas entre ontem e hoje) | import_new_reservations | 900s | 15min |
| Atualiza/Importa reservas |    |    |    |
| (Importa reservas do passado) | update_reservations | 86400s | 24h |
| Atualiza reservas deletadas | update_deleted_reservations | 21600s | 6h |
| Atualiza KPIs do anfitrião | dispatch_host_kpi_consolidation | 3600s | 1h |
| Atualização dos dados financeiros | financial_consolidations | 6h | 6h |
| Atualização da lista de TEDs | financial_dispatch_ted_consolidations | 3600s | 1h |
| Atualização da lista de NFs | financial_dispatch_nfs_consolidations | 3600s | 1h |
| Verifica pedidos de bloqueios | check_owner_blocks | 28800s | 8h |
|    |    |    |    |

> Fonte: <https://github.com/Khanto-Tecnologia/sapron-pms-web/blob/main/backend/config/settings.py>