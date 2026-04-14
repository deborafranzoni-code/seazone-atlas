<!-- title: Tabelas GCP (BigQuery — sistema de precos) | url: https://outline.seazone.com.br/doc/tabelas-gcp-bigquery-sistema-de-precos-7Rpmvtk7RQ | area: Tecnologia -->

# Tabelas GCP (BigQuery — sistema de precos)

# Tabelas GCP (BigQuery)

> Gerado automaticamente a partir de `mcp/table_metadata.py`. Nao edite diretamente.

## competitors

### competitors_category

* **Proposito:** Categoriza concorrentes por poligono, tipo, strata e quartos. Fonte primaria — os dados sao replicados diariamente para competitors_output no Sirius/Athena.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** Para concorrentes ativos: WHERE passed_the_filters=true AND alive=true AND is_active=true.
* **Notas:** Tabela da PIC. category = '{polygon}-{listing_type}-{strata}-{bedrooms}Q'.

### competitors_category_historic

* **Proposito:** Historico de categorizacao de concorrentes. Cada execucao appenda o snapshot completo com categoria, poligono, strata, filtros e metricas de faturamento.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** Tabela grande (\~174M linhas). Filtre por acquisition_date para restringir o periodo.
* **Notas:** Tabela da PIC. Escrita por WRITE_APPEND no BigQuery. Versao snapshot (truncada) esta em competitors_category.

### competitors_health_score_historic

* **Proposito:** Historico diario do health score por categoria de concorrentes. Avalia qualidade dos dados de pricing.
* **View:** Nao
* **Particoes:** data_particao
* **Formato particao:** DATETIME, partition_id formato YYYYMMDD.
* **Dica de query:** Filtre por data_particao. Colunas principais: categoria, health_score, status ('verde'/'amarelo'), perc_preco_incompativel.
* **Notas:** Tabela da PIC. Gerada pela cloud function health-status-clusters.

### competitors_health_score_today

* **Proposito:** Snapshot diario de saude das categorias de concorrentes. Score ponderado: 30% quantidade + 40% consistencia + 30% frequencia de incompatibilidade.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** —
* **Notas:** Tabela da PIC. WRITE_TRUNCATE diario — sempre contem apenas o snapshot do dia atual. status: 'verde', 'amarelo', 'vermelho'.

### competitors_historical

* **Proposito:** Historico de calendario de concorrentes — preco, ocupacao e bloqueio por listing/data, com snapshot diario.
* **View:** Nao
* **Particoes:** acquisition_year_month
* **Formato particao:** STRING formato YYYY-MM (ex: '2026-03').
* **Dica de query:** Filtre por acquisition_year_month. Contem price, occupied, blocked e is_correct_price.
* **Notas:** Tabela da PIC. Gerada pela cloud function update_competitors_historical a partir de daily_revenue_competitors no Athena.

### competitors_inactive

* **Proposito:** Lista de concorrentes marcados como inativos. Usada para excluir listings inativos do calculo de categorias.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** Tabela simples com apenas airbnb_listing_id.
* **Notas:** Tabela da PIC. Consultada por calculate-competitors-category.

### competitors_no_strata

* **Proposito:** Concorrentes sem classificacao de strata — pool de backup quando uma categoria tem menos de 15 concorrentes.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** —
* **Notas:** Tabela da PIC.

### competitors_opportunities

* **Proposito:** Visao agregada de oportunidades por categoria — quantos concorrentes ativos, filtrados, manuais, backup existem por categoria.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** \~1268 linhas. Util para diagnosticar categorias com poucos concorrentes.
* **Notas:** Tabela da PIC. Gerada por calculate-competitors-category, cruzando listing_category, competitors_category, competitors_no_strata e strata.

### competitors_polygons

* **Proposito:** Mapeamento de concorrentes para poligonos geograficos. Associa cada airbnb_listing_id ao poligono onde esta localizado.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** Tabela simples de lookup (airbnb_listing_id, polygon).
* **Notas:** Tabela da PIC.

### competitors_quarantine

* **Proposito:** Concorrentes em quarentena — listings com regras de bloqueio ativas.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** Colunas: airbnb_listing_id, rule. Tabela de lookup.
* **Notas:** Tabela da PIC. Alimentada pelo pipeline de quarentena (competitors-quarantine-blocked).

### competitors_quarantine_inactive

* **Proposito:** Concorrentes em quarentena marcados como inativos, com status.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** Colunas: airbnb_listing_id, rule, status.
* **Notas:** Tabela da PIC. Escrita pela cloud function competitors-quarantine-blocked.

### competitors_quarantine_iqr_revenue

* **Proposito:** Concorrentes em quarentena por regra IQR de faturamento — listings cujo faturamento mensal excede o threshold (Q3 + 2\*IQR) da categoria.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** Colunas: airbnb_listing_id, month_revenue, category, threshold.
* **Notas:** Tabela da PIC. Regra IQR aplicada apos dia 20 de cada mes sobre o faturamento do mes corrente.

### competitors_quarantine_iqr_sheets

* **Proposito:** Extensao da quarentena IQR com informacoes adicionais para planilhas — inclui quantidade de concorrentes e status.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** Versao enriquecida de competitors_quarantine_iqr_revenue.
* **Notas:** Tabela da PIC. Usada para exportacao e revisao manual em planilhas.

### listing_category

* **Proposito:** Mapeamento de listings internos (Seazone) para suas categorias de concorrentes, estado e regiao. Fonte de verdade para saber a qual categoria cada imovel pertence.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** \~4800 linhas. Colunas: id_seazone, category, state, region, status.
* **Notas:** Tabela da PIC. Escrita por calculate-competitors-category a partir de setup_groups no Athena. Truncada e recriada a cada execucao.

### listings_health_details_historic

* **Proposito:** Historico diario de detalhes de saude por listing concorrente — frequencia de incompatibilidade de preco por listing.
* **View:** Nao
* **Particoes:** data_particao
* **Formato particao:** DATETIME, partition_id formato YYYYMMDD.
* **Dica de query:** Filtre por data_particao. Granularidade: um registro por listing por dia.
* **Notas:** Tabela da PIC. Gerada pela cloud function health-status-clusters.

### listings_health_details_today

* **Proposito:** Detalhes de saude por listing individual — meses com precos incompativeis e frequencia de incompatibilidade.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** —
* **Notas:** Tabela da PIC. WRITE_TRUNCATE diario. Usado na PIC para identificar outliers e concorrentes problematicos.

### polygons

* **Proposito:** Definicao geometrica dos poligonos (regioes) usados no sistema de concorrentes. Cada poligono tem um nome e sua geometria (GEOGRAPHY).
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** \~428 linhas. Colunas: polygon (STRING), geometry (GEOGRAPHY).
* **Notas:** Tabela da PIC. Usada para operacoes geoespaciais e mapeamento de regioes.

## gaps

### gaps_bi

* **Proposito:** Gaps de disponibilidade por listing para consumo do BI. Contem o tamanho do gap (em dias) por id_seazone, data e tipo (normal/prime).
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** Tabela sem particao; filtre por id_seazone e/ou date.
* **Notas:** —

### gaps_rm

* **Proposito:** Gaps de disponibilidade agregados por periodo para uso do Revenue Management. Inclui cidade, categoria, datas de inicio/fim do gap, tipo e data de aquisicao.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** Filtre por acquisition_date para o snapshot mais recente.
* **Notas:** —

## infos

### competitor_peak_demand

* **Proposito:** Alertas de pico de demanda baseados em ocupacao de concorrentes por regiao/poligono. Tabela externa apontando para GCS (parquet).
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** Tabela externa — pode retornar erro se o arquivo parquet no GCS nao existir.
* **Notas:** Arquivo fonte: gs://seazone-info/peak-demand/. Pode estar vazia se o pipeline nao gerou dados recentes.

### internal_peak_demand

* **Proposito:** Alertas de pico de demanda interno por poligono, com tipo de alerta, faixa de capacidade, ocupacao de concorrentes, lead time e eventos mapeados.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** Filtre por day_alert e/ou polygon.
* **Notas:** —

### kpi_min_stay

* **Proposito:** Regras de estadia minima por listing e data, incluindo origem da regra, temporada, tipo climatico e observacoes. Versao completa sem particao (tabela legada).
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** Tabela grande (\~3.7M linhas) sem particao. Preferir kpi_min_stay_current para dados atuais ou kpi_min_stay_historic com filtro em data_particao.
* **Notas:** Mesma estrutura de kpi_min_stay_current mas sem data_particao. Possivelmente versao legada.

### kpi_min_stay_current

* **Proposito:** Snapshot atual das regras de estadia minima por listing e data. Sobrescrito (WRITE_TRUNCATE) a cada execucao.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** Sempre contem apenas o snapshot mais recente. Filtre por id_seazone ou date.
* **Notas:** Gerada por cloud-functions/get-min-stay-kpi. Coluna data_particao contem o timestamp da execucao.

### kpi_min_stay_historic

* **Proposito:** Historico de regras de estadia minima por listing e data, com append diario.
* **View:** Nao
* **Particoes:** data_particao
* **Formato particao:** YYYYMMDD
* **Dica de query:** Sempre filtre por data_particao para evitar full scan. Tabela grande com append diario.
* **Notas:** Gerada por cloud-functions/get-min-stay-kpi com WRITE_APPEND.

### kpi_system_price

* **Proposito:** KPI de preco do sistema vs preco sugerido por listing e data, com detalhamento de categoria, cidade, poligono, estrato, feriado, tipo climatico.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** Filtre por acquisition_date para snapshot mais recente e por id_seazone ou polygon.
* **Notas:** —

### listings_in_quarantine

* **Proposito:** Lista simples de listings (id_seazone) atualmente em quarentena.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** Tabela pequena. Use para JOIN/filtro de listings em quarentena.
* **Notas:** —

### listings_star_rating

* **Proposito:** Classificacao por estrelas (star rating) dos listings no Airbnb e Booking, com IDs de cada OTA e URL.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** Filtre por id_seazone. Dados cruzados de Airbnb e Booking via Lake.
* **Notas:** Gerada por cloud-functions/get-listings-star-rating. Snapshot atual (TRUNCATE).

### listings_star_rating_for_bi

* **Proposito:** Versao simplificada do star rating para consumo do BI, contendo apenas id_seazone, star_rating_airbnb e star_rating_booking.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** Tabela pequena. Versao resumida de listings_star_rating.
* **Notas:** —

### min_stay_for_bi

* **Proposito:** Regras de estadia minima formatadas para consumo do BI. Mesma estrutura de kpi_min_stay_current.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** Filtre por id_seazone e/ou date. Snapshot para BI.
* **Notas:** —

### quarantine_listings

* **Proposito:** Listings em quarentena com indicadores de reserva nos primeiros 7, 15 e 30 dias apos ativacao.
* **View:** Nao
* **Particoes:** acquisition_date
* **Formato particao:** YYYY-MM-DD
* **Dica de query:** Filtre por acquisition_date para snapshot mais recente. Colunas days_7/days_15/days_30 contem 'Sim'/'Nao'.
* **Notas:** Gerada por cloud-functions/get-quarantine-listings.

### quarantine_listings_real-activation_date_historical

* **Proposito:** Historico da data real de ativacao dos listings em quarentena, com contagem de datas disponiveis, bloqueadas e datas de ativacao.
* **View:** Nao
* **Particoes:** acquisition_date
* **Formato particao:** YYYY-MM-DD
* **Dica de query:** Filtre por acquisition_date. Gerada com append diario.
* **Notas:** real_activation_date pode ser NULL se o listing nao atendeu os criterios.

### stuck_min_price

* **Proposito:** Listings ou grupos com preco minimo 'travado' acima do preco medio praticado, indicando possivel problema de configuracao.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** Filtre por group_or_listing. Coluna period contem intervalos de datas em texto.
* **Notas:** —

## lake_observability

### anomaly_mape_report

* **Proposito:** Relatorio diario de anomalias no MAPE de receita. Contem estatisticas descritivas (percentis, media, desvio padrao) e contagem de diferencas.
* **View:** Nao
* **Particoes:** date
* **Formato particao:** YYYYMMDD
* **Dica de query:** Filtrar por date. Cada particao tem \~1 linha (relatorio agregado).
* **Notas:** Gerado pelo pipe-lake (reports/anomaly_mape_report). Dados desde out/2025.

### anomaly_price_metrics

* **Proposito:** Metricas diarias de anomalias de preco. Contem contagem total e distinta de IDs, alem de percentis do numero de linhas com anomalias.
* **View:** Nao
* **Particoes:** date
* **Formato particao:** YYYYMMDD
* **Dica de query:** Filtrar por date. Cada particao tem \~1 linha.
* **Notas:** Dados desde out/2025.

### mape_granularity_analysis

* **Proposito:** Analise de MAPE segmentada por diferentes granularidades (cidade, estado, tipo de imovel). Identifica segmentos criticos.
* **View:** Nao
* **Particoes:** created_at
* **Formato particao:** YYYYMMDD
* **Dica de query:** Filtrar por created_at. Usar is_critical=True para filtrar segmentos problematicos.
* **Notas:** Dados desde nov/2025. granularity_type indica a dimensao (state, city, listing_type).

### mape_history

* **Proposito:** Historico detalhado de MAPE por listing e por dia. Contem receita real vs estimada, preco, erro, status de bloqueio/ocupacao e metadados do imovel.
* **View:** Nao
* **Particoes:** created_at
* **Formato particao:** YYYYMMDD
* **Dica de query:** Tabela grande (\~2400 linhas/dia). Filtrar por created_at e opcionalmente por airbnb_listing_id ou state/city.
* **Notas:** Dados desde nov/2025.

### mape_ranked_properties

* **Proposito:** Ranking de imoveis por MAPE e score de impacto. Identifica imoveis com maior erro de previsao de receita.
* **View:** Nao
* **Particoes:** created_at
* **Formato particao:** YYYYMMDD
* **Dica de query:** Filtrar por created_at. Ordenar por impact_score DESC para imoveis mais criticos.
* **Notas:** Dados desde nov/2025. \~2400-2700 linhas/dia.

### priceav_mape_report

* **Proposito:** Relatorio diario de MAPE comparando precos e disponibilidade entre Lake e Sirius. Mede divergencia de preco medio e RMSE.
* **View:** Nao
* **Particoes:** date
* **Formato particao:** YYYYMMDD
* **Dica de query:** Filtrar por date. Cada particao tem \~1 linha. Dados desde out/2024.
* **Notas:** Gerado pelo pipe-lake (reports/priceav_mape_report). Historico longo.

### revenue_mape_monthly_big_errors

* **Proposito:** Imoveis com grandes erros mensais de MAPE de receita. Lista listings com MAPE elevado e a reducao de MAPE ao excluir o imovel.
* **View:** Nao
* **Particoes:** aquisition_date
* **Formato particao:** YYYYMMDD
* **Dica de query:** Filtrar por aquisition_date. Usar mape_reduction para priorizar imoveis com maior impacto.
* **Notas:** Dados desde set/2024.

### revenue_mape_monthly_last_years

* **Proposito:** Evolucao mensal do MAPE de receita ao longo do tempo. Contem MAPE global, de bloqueio, de ocupacao e contagem de outliers por mes.
* **View:** Nao
* **Particoes:** aquisition_date
* **Formato particao:** YYYYMMDD
* **Dica de query:** Filtrar por aquisition_date para snapshot mais recente.
* **Notas:** Dados desde set/2024.

### revenue_mape_report_last_days

* **Proposito:** Relatorio de MAPE de receita para diferentes janelas de dias recentes (ex: ultimos 7, 14, 30 dias).
* **View:** Nao
* **Particoes:** aquisition_date
* **Formato particao:** YYYYMMDD
* **Dica de query:** Filtrar por aquisition_date. Cada particao tem \~4 linhas (uma por janela de n_days).
* **Notas:** Gerado pelo pipe-lake. Dados desde set/2024.

### scrapers_health

* **Proposito:** Monitoramento diario da saude dos scrapers. Registra para cada tabela/database o numero de linhas inseridas, IDs unicos e flag de erro.
* **View:** Nao
* **Particoes:** date
* **Formato particao:** YYYYMMDD
* **Dica de query:** Filtrar por date. Usar error=True para encontrar scrapers com falha.
* **Notas:** Dados desde ago/2024.

### vw_mape_history_grouped

* **Proposito:** View agrupada do historico de MAPE por listing. Contem colunas essenciais sem detalhes de segmentacao.
* **View:** Sim
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** View sem particoes — filtrar por date ou airbnb_listing_id. Tabela base: mape_history.
* **Notas:** —

### vw_scrapers_health_data

* **Proposito:** View consolidada de saude dos scrapers com comparacao entre ingestao de ontem e ultima ingestao bem-sucedida. Mostra variacao de volume.
* **View:** Sim
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** View sem particoes — retorna snapshot atual. Usar error=True para scrapers com falha.
* **Notas:** View sobre scrapers_health.

### vw_scrapers_health_delta

* **Proposito:** View de delta diario dos scrapers: compara rows_inserted de hoje vs ontem para detectar quedas ou aumentos anomalos.
* **View:** Sim
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** View sem particoes — retorna snapshot atual. Usar delta_pct_vs_ontem para detectar variacoes.
* **Notas:** View sobre scrapers_health.

## meta

### berlinda_dash

* **Proposito:** Dashboard de performance com score de prioridade por listing — combina faturamento, metas, bloqueios e potencial de receita.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** Multiplos snapshots com coluna timestamp — filtrar pelo mais recente: QUALIFY MAX(timestamp) OVER (PARTITION BY year_month) = timestamp. QUALIFY nao funciona com agregacoes (COUNT/AVG/SUM) — nesse caso, filtrar o snapshot numa CTE/subquery primeiro e agregar depois. priority_status indica urgencia. score_normal e o score normalizado.
* **Notas:** Extensao de performance_dash com campos adicionais: score, potencial, prioridade. Usado no dashboard Berlinda.

### frozen_competitors_data

* **Proposito:** Snapshot mensal dos dados de concorrentes usados para calculo de metas (baseline congelado).
* **View:** Nao
* **Particoes:** year_month
* **Formato particao:** STRING formato 'YYYY-MM'.
* **Dica de query:** —
* **Notas:** —

### output_monthly

* **Proposito:** Performance mensal de listings Seazone vs meta baseada em percentis dos concorrentes.
* **View:** Nao
* **Particoes:** year_month
* **Formato particao:** STRING formato 'YYYY-MM' (ex: '2026-02').
* **Dica de query:** Multiplos snapshots por mes — filtrar pelo mais recente: QUALIFY MAX(timestamp) OVER (PARTITION BY year_month) = timestamp. QUALIFY nao funciona com agregacoes (COUNT/AVG/SUM) — nesse caso, filtrar o snapshot numa CTE/subquery primeiro e agregar depois. Para percentuais de KPIs, usar WHERE meta_result IS NOT NULL. Manter nulls apenas para dumps completos.
* **Notas:** meta_result: 'bateu', 'nao bateu', null = listing excluido dos KPIs de meta (nao passou filtros minimos de qualidade, ex: menos de 7 concorrentes).

### output_quarter

* **Proposito:** Performance trimestral completa — calculo de metas do trimestre inteiro agregado a partir dos dados mensais.
* **View:** Nao
* **Particoes:** quarter
* **Formato particao:** STRING formato 'YYYY-Q#' (ex: '2025-Q1').
* **Dica de query:** Multiplos snapshots por trimestre — filtrar pelo mais recente: QUALIFY MAX(timestamp) OVER (PARTITION BY quarter) = timestamp. QUALIFY nao funciona com agregacoes (COUNT/AVG/SUM) — nesse caso, filtrar o snapshot numa CTE/subquery primeiro e agregar depois. Para percentuais de KPIs, usar WHERE meta_result IS NOT NULL.
* **Notas:** meta_result: 'bateu', 'nao bateu', null = listing excluido dos KPIs de meta.

### output_quarter_confirmed

* **Proposito:** Performance trimestral parcial — dados confirmados do inicio do trimestre ate hoje. Util para acompanhamento em tempo real do trimestre corrente.
* **View:** Nao
* **Particoes:** quarter
* **Formato particao:** STRING formato 'YYYY-Q#' (ex: '2025-Q1').
* **Dica de query:** Multiplos snapshots por trimestre — filtrar pelo mais recente: QUALIFY MAX(timestamp) OVER (PARTITION BY quarter) = timestamp. QUALIFY nao funciona com agregacoes (COUNT/AVG/SUM) — nesse caso, filtrar o snapshot numa CTE/subquery primeiro e agregar depois. Para percentuais de KPIs, usar WHERE meta_result IS NOT NULL.
* **Notas:** Mesmas colunas de output_quarter. meta_result segue a mesma logica: null = excluido dos KPIs.

### performance_dash

* **Proposito:** Dashboard de performance mensal por listing — faturamento vs meta, ocupacao, bloqueios e preco medio.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** Multiplos snapshots com coluna timestamp — filtrar pelo mais recente: QUALIFY MAX(timestamp) OVER (PARTITION BY year_month) = timestamp. QUALIFY nao funciona com agregacoes (COUNT/AVG/SUM) — nesse caso, filtrar o snapshot numa CTE/subquery primeiro e agregar depois. meta_achieved = faturamento / meta_value.
* **Notas:** Subconjunto de colunas de berlinda_dash (sem scores/prioridade). Usado no dashboard de performance.

## system_price

### aggressiveness_levels_unnested_active

* **Proposito:** Niveis de agressividade ativos com intervalos de antecedencia para precificacao dinamica por categoria.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** —
* **Notas:** aggressiveness_level: standard, aggressive, very_aggressive, moderate, very_moderate.

### aggressiveness_prices_and_levels_and_reactive_price_by_id_seazone

* **Proposito:** Resultado final do calculo de precos do system price por id_seazone. Contem niveis de agressividade, percentis de ocupacao/disponibilidade, preco do sistema, preco reativo (sapron) e preco final aplicado.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** Tabela nao particionada. Contem uma linha por id_seazone+category+date+antecedence. Filtrar por id_seazone ou category para reduzir volume.
* **Notas:** Gerada pela cloud function calculate-aggressiveness-prices. Inclui colunas de preco reativo do Sapron.

### aggressiveness_prices_and_levels_by_id_seazone

* **Proposito:** Precos calculados para todos os niveis de agressividade por listing e data. Tabela central do sistema de precos GCP.
* **View:** Nao
* **Particoes:** date
* **Formato particao:** TIMESTAMP (BigQuery). Filtre por date >= CURRENT_DATE.
* **Dica de query:** system_price e o preco efetivamente usado. Campos very_aggressive/aggressive/standard/moderate/very_moderate mostram alternativas.
* **Notas:** Atualizacao: diaria.

### cluster_category

* **Proposito:** Mapeamento de clusters para categorias de precificacao.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** —
* **Notas:** Full refresh (WRITE_TRUNCATE). Clustering por category.

### cluster_matrix

* **Proposito:** Matriz de regras de precificacao por cluster e tipo climatico. Define percentis e tipos de preco para cada combinacao de sazonalidade, tipo de ocorrencia, sigla, ocupacao e intervalo de antecedencia.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** Tabela pequena (\~33 linhas). Coluna 'matrix' e do tipo RECORD. Nao requer filtro de particao.
* **Notas:** Gerenciada pela cloud function insert-new-matrix. Campo origin indica a fonte da matriz. timestamp indica quando foi inserida.

### cluster_matrix_active

* **Proposito:** Matriz de precificacao ativa com regras de sazonalidade e niveis de ocupacao por cluster.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** Use UNNEST para expandir o campo aninhado 'matrix'.
* **Notas:** season e coluna top-level (nao aninhada em matrix).

### fill_category_price

* **Proposito:** Mapeamento de preco de preenchimento automatico por prefixo de categoria normalizado. Usado quando nao ha preco calculado para uma categoria.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** Tabela muito pequena. Consulta direta sem filtros.
* **Notas:** Contem category_normalized_prefix (STRING) e fill_system_price (INTEGER).

### listings_system_price

* **Proposito:** Visao consolidada de todos os listings ativos com seus grupos (Cidade, Poligono, Categoria, Clima) e flag indicando se participam do system price.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** Filtrar por is_system_price=true para obter apenas listings no system price.
* **Notas:** Recriada pela cloud function update-listings-system-price. Cruza setup_groups, climate e system_price_listings.

### listings_system_price_and_matrix

* **Proposito:** Extensao de listings_system_price com informacoes adicionais de elegibilidade: se possui matriz, se e elegivel, status, quantidade de concorrentes e flag de Florianopolis.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** Usada nos alertas de KPI. Filtrar por eligible=true ou status para analises.
* **Notas:** Colunas: has_matrix (BOOLEAN), eligible (BOOLEAN), status (STRING), qtd_concorrentes (INTEGER), is_florianopolis (BOOLEAN).

### listings_system_price_by_category

* **Proposito:** Agregacao de listings por categoria com flag de system price. Util para visao resumida de quais categorias estao no system price.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** Tabela muito pequena. Consulta direta sem filtros.
* **Notas:** Contem apenas Categoria (STRING) e is_system_price (BOOLEAN).

### prices_sent_sirius

* **Proposito:** Historico de precos enviados do GCP (system price) para o Sirius (AWS). Registra cada envio com preco, limites e motivo.
* **View:** Nao
* **Particoes:** acquisition_date
* **Formato particao:** DATE formato YYYY-MM-DD.
* **Dica de query:** Sempre filtre por acquisition_date para evitar full scan. Dados diarios desde dez/2025.
* **Notas:** Gerada pela cloud function send-prices-to-aws. Contem id_seazone, category, date, price, reason, limites.

### system_price_listings

* **Proposito:** Lista de id_seazone habilitados para o system price. Tabela de referencia usada como lookup.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** Tabela muito pequena (apenas coluna id_seazone). Consulta direta sem filtros.
* **Notas:** Referenciada por update-listings-system-price via LEFT JOIN para definir is_system_price.

### warning_not_eligible_categories

* **Proposito:** Alerta de categorias nao elegiveis para o system price. Contem categoria, numero de concorrentes e motivo da inelegibilidade.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** Tabela pequena. Consulta direta sem filtros.
* **Notas:** Tabela base do alerta. Reescrita (WRITE_TRUNCATE) a cada execucao. Variantes: _pending (pendentes de revisao) e _status (historico com Status/Comentario).

### warning_not_eligible_categories_pending

* **Proposito:** Alertas pendentes de revisao para categorias nao elegiveis.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** —
* **Notas:** Variante _pending da warning_not_eligible_categories. Consumida pela API new-warnings-api.

### warning_not_eligible_categories_status

* **Proposito:** Historico de status dos alertas de categorias nao elegiveis. Inclui colunas Status e Comentario.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** —
* **Notas:** Variante _status. Colunas adicionais: Status, Comentario, acquisition_date. Gerenciada pela API new-warnings-api.

### warning_prices_lower_range

* **Proposito:** Alerta de precos calculados abaixo do limite inferior do intervalo permitido.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** —
* **Notas:** Tabela base do alerta. Reescrita a cada execucao. Variantes: _pending e _status.

### warning_prices_lower_range_pending

* **Proposito:** Alertas pendentes de revisao para precos abaixo do limite inferior.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** —
* **Notas:** Variante _pending da warning_prices_lower_range.

### warning_prices_lower_range_status

* **Proposito:** Historico de status dos alertas de precos abaixo do limite inferior.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** —
* **Notas:** Variante _status. Colunas adicionais: Status, Comentario, acquisition_date.

### warning_prices_outside_strata

* **Proposito:** Alerta de precos que ultrapassam o limite do estrato superior. Detecta inversoes de hierarquia de strata.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** —
* **Notas:** Tabela base do alerta. Contem colunas da categoria superior (category_upper, strata_upper_limit). Variantes: _pending e _status.

### warning_prices_outside_strata_pending

* **Proposito:** Alertas pendentes de revisao para precos fora do estrato.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** —
* **Notas:** Variante _pending da warning_prices_outside_strata.

### warning_prices_outside_strata_status

* **Proposito:** Historico de status dos alertas de precos fora do estrato.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** —
* **Notas:** Variante _status. Colunas adicionais: Status, Comentario, acquisition_date.

### warning_prices_over_range

* **Proposito:** Alerta de precos calculados acima do limite superior do intervalo permitido.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** —
* **Notas:** Tabela base do alerta. Reescrita a cada execucao. Variantes: _pending e _status.

### warning_prices_over_range_pending

* **Proposito:** Alertas pendentes de revisao para precos acima do limite superior.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** —
* **Notas:** Variante _pending da warning_prices_over_range.

### warning_prices_over_range_status

* **Proposito:** Historico de status dos alertas de precos acima do limite superior.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** —
* **Notas:** Variante _status. Colunas adicionais: Status, Comentario, acquisition_date.