<!-- title: Tabelas Lake (Data Lake — AWS Athena cross-account) | url: https://outline.seazone.com.br/doc/tabelas-lake-data-lake-aws-athena-cross-account-oeDFYmvetS | area: Tecnologia -->

# Tabelas Lake (Data Lake — AWS Athena cross-account)

# Tabelas Lake (AWS Athena cross-account)

> Gerado automaticamente a partir de `mcp/table_metadata.py`. Nao edite diretamente.

## brlink_seazone_clean_data

### booking_details

* **Proposito:** Detalhes de anuncios do Booking.com (quartos, banheiros, area, facilidades). Dados coletados por scraping periodico.
* **View:** Nao
* **Particoes:** aquisition_date_partition
* **Formato particao:** aquisition_date_partition e STRING no formato 'YYYY-MM-DD'.
* **Dica de query:** Filtrar por aquisition_date_partition para evitar full scan.
* **Notas:** —

### clean_comments

* **Proposito:** Comentarios/avaliacoes de hospedes em anuncios Airbnb, limpos e normalizados. Inclui nota, idioma e identificacao do avaliador.
* **View:** Nao
* **Particoes:** ano, mes
* **Formato particao:** ano e mes sao STRING SEM zero a esquerda (ex: ano='2024', mes='3').
* **Dica de query:** Filtrar por ano e mes.
* **Notas:** —

### comments_booking

* **Proposito:** Comentarios e avaliacoes de hospedes vindos do Booking.com, incluindo notas por categoria (limpeza, instalacoes, localizacao, servicos, valor).
* **View:** Nao
* **Particoes:** data
* **Formato particao:** data e STRING no formato 'YYYY-MM-DD'.
* **Dica de query:** Filtrar por data. Dados disponiveis de out/2023 a abr/2024.
* **Notas:** —

### details

* **Proposito:** Detalhes completos dos listings Airbnb — anuncio, caracteristicas do imovel, host. Particionado por data de aquisicao.
* **View:** Nao
* **Particoes:** ano, mes, dia
* **Formato particao:** STRING SEM zero a esquerda: ano='2026', mes='3', dia='9'. NUNCA use '03' ou '09'.
* **Dica de query:** Para dados mais recentes use details_last_aquisitiondetails (sem particoes, um registro por listing).
* **Notas:** Volume: milhoes de linhas. Atualizacao: semanal.

### internal_airbnb_details

* **Proposito:** Detalhes de anuncios Airbnb internos (Seazone): nome, descricao, amenidades, localizacao, regras, fotos, notas, tipo de listing e status de superhost.
* **View:** Nao
* **Particoes:** ano, mes, dia
* **Formato particao:** STRING SEM zero a esquerda (ex: ano='2025', mes='3', dia='5').
* **Dica de query:** Filtrar por ano, mes e dia. Coleta diaria desde abr/2024.
* **Notas:** —

### internal_clean_comments

* **Proposito:** Comentarios/avaliacoes de hospedes em anuncios Airbnb internos (Seazone), limpos.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** Tabela sem particoes. Usar LIMIT para evitar full scan.
* **Notas:** —

### internal_conversion_rate

* **Proposito:** Taxa de conversao de anuncios Airbnb internos (Seazone): conversao do anuncio, anuncios similares, global, impressoes de busca.
* **View:** Nao
* **Particoes:** data_alvo
* **Formato particao:** data_alvo e STRING no formato 'YYYY-MM-DD'.
* **Dica de query:** Filtrar por data_alvo. Dados disponiveis de dez/2023 a mai/2024.
* **Notas:** —

### internal_views

* **Proposito:** Visualizacoes de anuncios Airbnb internos (Seazone): views do anuncio, views de similares e impressoes de busca.
* **View:** Nao
* **Particoes:** data_alvo
* **Formato particao:** data_alvo e STRING no formato 'YYYY-MM-DD'.
* **Dica de query:** Filtrar por data_alvo. Dados de jan/2024 a nov/2025.
* **Notas:** —

### olx

* **Proposito:** Anuncios de imoveis da OLX coletados por scraping: preco, IPTU, condominio, area, quartos, banheiros, localizacao e dados do anunciante.
* **View:** Nao
* **Particoes:** ano, mes, dia
* **Formato particao:** STRING COM zero a esquerda (ex: ano='2023', mes='03', dia='07'). ATENCAO: diferente do padrao lake.
* **Dica de query:** Filtrar por ano, mes e dia. Dados de set/2022 a mar/2026. ATENCAO: usa zero a esquerda.
* **Notas:** —

### price_av

* **Proposito:** Precos e disponibilidade diaria de anuncios Airbnb (calendario). Inclui preco, fonte do preco, estadia minima e flags de checkin/checkout.
* **View:** Nao
* **Particoes:** ano, mes, dia
* **Formato particao:** STRING SEM zero a esquerda (ex: ano='2024', mes='3', dia='27').
* **Dica de query:** Filtrar por ano, mes e dia. Coleta diaria desde 2019. Cada particao e uma data de aquisicao.
* **Notas:** —

### price_resolved

* **Proposito:** Precos resolvidos/consolidados de anuncios Airbnb: um preco final por listing e data, apos resolucao de conflitos entre fontes.
* **View:** Nao
* **Particoes:** ano, mes, dia
* **Formato particao:** STRING SEM zero a esquerda (ex: ano='2024', mes='6', dia='9').
* **Dica de query:** Filtrar por ano, mes e dia. Derivada de price_av.
* **Notas:** —

### seazone_listings

* **Proposito:** Mapeamento entre airbnb_listing_id e id_seazone. Tabela de referencia para vincular anuncios Airbnb aos imoveis do portfolio Seazone.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** Tabela sem particoes, apenas 2 colunas. Pode ser usada em JOINs livremente.
* **Notas:** —

### seazone_listings_historic

* **Proposito:** Historico de mapeamento airbnb_listing_id para id_seazone ao longo do tempo.
* **View:** Nao
* **Particoes:** ano, mes, dia
* **Formato particao:** STRING COM zero a esquerda (ex: ano='2024', mes='03', dia='19'). ATENCAO: diferente do padrao lake.
* **Dica de query:** Filtrar por ano, mes e dia. ATENCAO: usa zero a esquerda.
* **Notas:** —

### vivareal

* **Proposito:** Anuncios de imoveis do VivaReal/ZAP coletados por scraping: precos de venda/aluguel, IPTU, condominio, area, quartos, vagas, amenidades.
* **View:** Nao
* **Particoes:** ano, mes, dia
* **Formato particao:** STRING COM zero a esquerda (ex: ano='2023', mes='05', dia='06'). ATENCAO: diferente do padrao lake.
* **Dica de query:** Filtrar por ano, mes e dia. Dados desde nov/2021. ATENCAO: usa zero a esquerda.
* **Notas:** —

### vivareal_listing_type

* **Proposito:** Tabela de referencia/de-para para tipos de anuncio VivaReal: mapeia unit_type e usage_type para um new_type normalizado.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** Tabela pequena sem particoes, apenas 3 colunas.
* **Notas:** —

## brlink_seazone_enriched_data

### analise_faturamento

* **Proposito:** Faturamento mensal enriquecido com strata, localizacao e detalhes do imovel. Tabela final para analise de faturamento e treinamento de modelos.
* **View:** Nao
* **Particoes:** ano, mes
* **Formato particao:** STRING SEM zero a esquerda: ano='2026', mes='3'. NUNCA use '03'.
* **Dica de query:** Taxa de ocupacao: occupied_dates / (days_in_month - blocked_dates). Filtre is_dead=false implicitamente (ja filtrado na tabela).
* **Notas:** Filtros ja aplicados: is_dead=false, faturamento > 0, days_in_month >= 10, ano >= 2022. JOIN com details, location e competitors_output.

### block_and_occupancy

* **Proposito:** Dados enriquecidos de bloqueio e ocupacao por listing/dia: preco atual, preco de reserva, taxa de limpeza, motivo de bloqueio e status de ocupacao.
* **View:** Nao
* **Particoes:** date
* **Formato particao:** date e STRING no formato 'YYYY-MM-DD'.
* **Dica de query:** Filtrar por date. Dados desde 2019. Colunas month/year sao INT (nao sao particoes). booked_on = data de criacao da reserva. Para contar reservas de concorrentes: identificar datas consecutivas com mesmo booked_on, mesmo listing ID e occupied=true — cada grupo de datas consecutivas = 1 reserva.
* **Notas:** Cruza price_av, booked_on e regras de bloqueio. block_reason = motivo do bloqueio da data no calendario. Util para distinguir bloqueios manuais de reservas.

### booked_on_snapshot

* **Proposito:** Snapshot de reservas detectadas: compara estado anterior e atual do calendario Airbnb para identificar momento e preco da reserva.
* **View:** Nao
* **Particoes:** date
* **Formato particao:** date e DATE (nao string). Tabela Delta Lake — particoes gerenciadas pelo transaction log, nao aparecem em list_partitions.
* **Dica de query:** Filtrar por date para reduzir scan. Tabela Delta Lake particionada por date. booked_on = data de criacao da reserva. Para contar reservas de concorrentes: identificar datas consecutivas com mesmo booked_on, mesmo listing ID e occupied=true — cada grupo de datas consecutivas = 1 reserva.
* **Notas:** Tabela Delta Lake (spark.sql.sources.provider=delta). Usada como base para block_and_occupancy.

### daily_fat

* **Proposito:** Tabela fato diaria consolidada: preco, ocupacao, bloqueio, receita diaria (day_fat) e receita apos desconto por listing/dia. Principal tabela de metricas operacionais.
* **View:** Nao
* **Particoes:** date
* **Formato particao:** date e STRING no formato 'YYYY-MM-DD'.
* **Dica de query:** Filtrar por date. Colunas month/year sao INT (nao sao particoes). Tabela central para analises de receita e ocupacao. booked_on = data de criacao da reserva. Para contar reservas de concorrentes: identificar datas consecutivas com mesmo booked_on, mesmo listing ID e occupied=true — cada grupo de datas consecutivas = 1 reserva.
* **Notas:** block_reason = motivo do bloqueio da data no calendario. Util para distinguir bloqueios manuais de reservas.

### dead_alive

* **Proposito:** Status de vida/morte de anuncios Airbnb: data de nascimento, ultima aquisicao, flag alive/dead e data de morte.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** Tabela sem particoes (arquivo Parquet unico). alive=true indica listing ativo.
* **Notas:** —

### details_last_aquisitiondetails

* **Proposito:** Snapshot mais recente dos detalhes de cada listing. Um registro por airbnb_listing_id, sem particoes.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** Use esta tabela ao inves de 'details' quando precisar apenas dos dados mais recentes de cada listing.
* **Notas:** is_dead=true indica listing inativo (sem aquisicao ha mais de 15 dias).

### fato_block_occupancy

* **Proposito:** View sobre tabela fato de receita e ocupacao mensal por listing. Combina dados do Pipe (web scraping proprio da Seazone) e AirDNA (dados comprados de terceiros — descontinuado, nao mais atualizado). A view faz CAST(ano/mes AS integer).
* **View:** Sim
* **Particoes:** ano, mes
* **Formato particao:** Herdado da tabela base (ano/mes sao STRING na base, CAST para INT na view). Filtrar por ano e mes SEM aspas e SEM zero a esquerda: WHERE ano = 2025 AND mes = 2.
* **Dica de query:** ano e mes aparecem como INT na view, mas filtrar por eles ainda reduz o scan (predicate pushdown para a tabela base particionada).
* **Notas:** View sobre fato_block_occupancy_b3adca05d771535a362f7e2b069ba0d5 (particionada por ano/mes STRING). Inclui logica de interpolacao para meses incompletos. fonte_pipe=true indica dados Pipe (web scraping); false indica AirDNA (descontinuado). Colunas sem sufixo pipe/airdna (ex: faturamento) ja selecionam a melhor fonte automaticamente. Preferir fonte_pipe=true para dados atuais.

### location_last_aquisition

* **Proposito:** Ultima localizacao conhecida de cada listing. Um registro por airbnb_listing_id, sem particoes.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** —
* **Notas:** Campos: country, state, city, suburb, latitude, longitude.

### reservations

* **Proposito:** Reservas detectadas e consolidadas: datas de checkin/checkout, preco total, estadia minima, duracao, antecedencia e status da reserva.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** Tabela sem particoes. Filtrar por booked_on, checkin ou airbnb_listing_id com LIMIT. booked_on = data de criacao da reserva. Para contar reservas de concorrentes: identificar datas consecutivas com mesmo booked_on, mesmo listing ID e occupied=true — cada grupo de datas consecutivas = 1 reserva.
* **Notas:** Derivada de booked_on_snapshot.

## rm_agent

### rm_booking_curve_insights

* **Proposito:** Insights de curva de reserva por evento — ocupacao atual, forca de reserva e comparacao com edicao anterior. Uma linha por evento x cidade.
* **View:** Nao
* **Particoes:** report_date
* **Formato particao:** YYYY-MM-DD (STRING)
* **Dica de query:** Filtrar por report_date. Coluna booking_strength indica ritmo (ex: forte/fraco). Coluna insight contem texto descritivo.
* **Notas:** Gerado pelo pipeline Lambda rm-agent. Complementa rm_booking_curves com resumo por evento.

### rm_booking_curves

* **Proposito:** Curvas de reservas acumuladas por evento — compara edicao atual vs anterior para avaliar velocidade de locacao. Uma linha por evento x days_before_event x edicao.
* **View:** Nao
* **Particoes:** report_date
* **Formato particao:** YYYY-MM-DD (STRING)
* **Dica de query:** Filtrar por report_date e event_name. Coluna edition distingue 'atual' vs 'anterior'. Usar days_before_event como eixo X e cumulative_occ_pct como Y.
* **Notas:** Gerado pelo pipeline Lambda rm-agent. Usado na Tela 2 do Lovable para graficos de booking curve.

### rm_booking_pace

* **Proposito:** Velocidade de reservas (booking pace) por poligono x checkin_date. Detecta quando a taxa de reservas dos ultimos 7 dias supera o P90 historico.
* **View:** Nao
* **Particoes:** report_date
* **Formato particao:** YYYY-MM-DD (STRING)
* **Dica de query:** Filtrar por report_date. score > 100 indica acima do historico. Coluna alerta: FORTE, MODERADO ou NORMAL.
* **Notas:** Gerado pelo pipeline Lambda rm-agent. Usado na secao 'demanda acelerada' do rm_daily_report.

### rm_competitor_baseline

* **Proposito:** Baseline estatistico de ocupacao dos concorrentes por poligono. Media, desvio padrao e percentis (P65-P95) calculados sobre janela de 2 anos.
* **View:** Nao
* **Particoes:** report_date
* **Formato particao:** YYYY-MM-DD (STRING)
* **Dica de query:** Filtrar por report_date. Cada linha = poligono + day_of_year. Usar p90_occupancy como threshold de alta demanda.
* **Notas:** Gerado pelo pipeline Lambda rm-agent (cron 6h BRT). Dados no S3 bucket seazone-rm-agent.

### rm_competitor_occupancy

* **Proposito:** Ocupacao diaria dos concorrentes por poligono. Total de listings, ocupados e taxa de ocupacao.
* **View:** Nao
* **Particoes:** report_date
* **Formato particao:** YYYY-MM-DD (STRING)
* **Dica de query:** Filtrar por report_date. Coluna date indica o dia da ocupacao.
* **Notas:** Gerado pelo pipeline Lambda rm-agent.

### rm_daily_report

* **Proposito:** Relatorio diario gerado por IA (Claude via OpenRouter). Uma coluna por secao: resumo, dinheiro na mesa, eventos proximos, oportunidades de pricing, etc. Coluna report_markdown contem o relatorio completo em Markdown.
* **View:** Nao
* **Particoes:** report_date
* **Formato particao:** YYYY-MM-DD (STRING)
* **Dica de query:** Filtrar por MAX(report_date) para relatorio mais recente. Coluna report_markdown tem o texto completo.
* **Notas:** Gerado pelo pipeline Lambda rm-agent. Injeta feedbacks do analista no prompt.

### rm_demand_signals

* **Proposito:** Sinais de demanda anomala detectados por percentil adaptativo (sigma_distance vs baseline). Inclui tipo de sinal, nivel de alerta, confianca IA e nome de evento quando identificado.
* **View:** Nao
* **Particoes:** report_date
* **Formato particao:** YYYY-MM-DD (STRING)
* **Dica de query:** Filtrar por report_date. Usar alert_level para priorizar (high/medium/low). signal_type indica a natureza do sinal.
* **Notas:** Gerado pelo pipeline Lambda rm-agent. Eventos nao mapeados investigados via Perplexity + Claude.

### rm_holidays

* **Proposito:** Calendario de feriados e eventos agrupados por group_name. Usado como input para correlacionar sinais de demanda com eventos conhecidos.
* **View:** Nao
* **Particoes:** report_date
* **Formato particao:** YYYY-MM-DD (STRING)
* **Dica de query:** Filtrar por report_date. start_date e end_date delimitam o periodo do evento.
* **Notas:** Gerado pelo pipeline Lambda rm-agent a partir de dados de inputdata (sirius).

### rm_internal_occupancy

* **Proposito:** Ocupacao diaria dos imoveis Seazone por poligono. Total de imoveis, ocupados, bloqueados e taxa de ocupacao interna.
* **View:** Nao
* **Particoes:** report_date
* **Formato particao:** YYYY-MM-DD (STRING)
* **Dica de query:** Filtrar por report_date. Comparar sz_occupancy_rate com comp_occupancy_rate de rm_competitor_occupancy.
* **Notas:** Gerado pelo pipeline Lambda rm-agent a partir de dados de revenuedata (sirius).

### rm_pricing_alerts

* **Proposito:** Alertas de pricing comparando Seazone vs concorrentes. Inclui sigma_distance, tipo de sinal, nivel de alerta, confianca IA e status em portugues.
* **View:** Nao
* **Particoes:** report_date
* **Formato particao:** YYYY-MM-DD (STRING)
* **Dica de query:** Filtrar por report_date. Usar alert_level para priorizar e status_pt para exibicao.
* **Notas:** Gerado pelo pipeline Lambda rm-agent. Schema similar a rm_demand_signals com contexto de pricing.