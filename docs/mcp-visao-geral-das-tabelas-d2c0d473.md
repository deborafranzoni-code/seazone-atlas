<!-- title: MCP — Visao Geral das Tabelas | url: https://outline.seazone.com.br/doc/mcp-visao-geral-das-tabelas-eUq5aT9vac | area: Tecnologia -->

# MCP — Visao Geral das Tabelas

# Tabelas MCP — Visao Geral

> Gerado automaticamente a partir de `mcp/table_metadata.py`. Nao edite diretamente.

## Conceitos e Termos do Dominio

* **Seazone (Nossa Empresa):** Nossa empresa. Gestão de imóveis para aluguel por temporada. Dados internos de listings, faturamento, performance e precificação. Presente nos sources sirius (dados operacionais) e gcp (KPIs, metas, relatórios). Sapron é uma aplicação interna que gerencia os imóveis da Seazone — dados do Sapron estão nas tabelas de saprondata.
* **Airbnb:** Dados externos de listings Airbnb coletados via web scraping próprio (Pipe) e dados comprados da AirDNA (descontinuado). Presente no source lake. AirDNA não é mais atualizado — preferir dados Pipe para análises atuais.
* **Booking.com:** Dados externos da plataforma Booking.com. Presente no source lake (tabela booking_details em brlink_seazone_clean_data).
* **PIC (Plataforma de Inteligência de Concorrentes):** Plataforma de inteligência competitiva da Seazone. Tabelas nos databases GCP `competitors` e Sirius `competitorsdata` são da PIC. Inclui análise de concorrentes, categorização, outliers e regras de pricing baseadas em competidores.
* **Meta (Sistema de Metas):** Sistema de metas e objetivos da Seazone (NÃO é Meta/Facebook). Database GCP `meta` contém KPIs, metas de faturamento e ocupação. Campo meta_result: 'bateu' (atingiu), 'nao bateu' (não atingiu), null (excluído por não passar filtros mínimos de qualidade). Para agregações e percentuais, filtrar WHERE meta_result IS NOT NULL.
* **OLX / VivaReal:** Marketplaces imobiliários de compra e venda. Dados coletados via scraping no lake (brlink_seazone_clean_data). VivaReal tem sale_price e rental_price; OLX tem price. Útil para análises de ROI: comparar preço de compra com faturamento anual de aluguel por temporada. Cruzar por cidade + bairro + quartos para comparação justa.
* **Markup Stays→Airbnb:** Sirius define um preco base para cada imovel. O Stays distribui esse preco para OTAs. Para o Airbnb, o Stays aplica um markup sobre o preco base. Historico de fatores:   - Antes de 22/10/2025: fator 1.10 (aumento de 10%)   - De 22/10/2025 ate 18/12/2025: fator 1.17 (aumento de 17%)   - A partir de 19/12/2025: fator 1.19 (aumento de 19%) Ao comparar precos base Sirius com precos de concorrentes Airbnb, multiplicar o preco Sirius pelo fator (ou dividir o preco Airbnb pelo fator). A data relevante e quando o preco foi enviado/capturado, NAO a data da estadia:   - Datas nao reservadas: usar price_aquisition_date (ou aquisition_date)   - Datas reservadas: usar booked_on (ou creation_date)
* **Dados de Preco Airbnb e Receita:** Dados de preco Airbnb nas nossas tabelas representam o valor da reserva EXCLUINDO taxas de limpeza e outras taxas do Airbnb. Exemplo: reserva total de R$1.000 com R$200 de taxa de limpeza = R$800 nos nossos dados. NAO chamar nossos dados de Airbnb de 'receita bruta' — ja estao sem taxas. O Airbnb cobra 15% de comissao sobre esse valor. Para receita liquida: multiplicar por 0.85 (ex: preco \* 0.85 para linhas ocupadas).

## Resumo por Source

| Source | Databases | Total Tabelas |
|----|----|----|
| sirius | 5 | 27 |
| lake | 3 | 34 |
| gcp | 6 | 75 |

## Chaves de Relacionamento (Join Keys)

| Source | Chave de listing | Observacao |
|----|----|----|
| sirius | id_seazone ou listing | ID/nome interno de imoveis Seazone |
| sirius | airbnb_listing_id | ID Airbnb (tabelas de concorrentes) |
| lake | airbnb_listing_id | ID Airbnb |
| gcp | id_seazone | ID interno Seazone |

Para cruzar dados sirius (id_seazone) com lake/concorrentes (airbnb_listing_id): use competitors_plus em competitorsdata (sirius).

## Referencia Rapida

| Source | Database | Tabela | Proposito |
|----|----|----|----|
| gcp | competitors | competitors_category | Categoriza concorrentes por poligono, tipo, strata e quartos. Fonte primaria — os dados sao replicados diariamente para competitors_output no Sirius/Athena. |
| gcp | competitors | competitors_category_historic | Historico de categorizacao de concorrentes. Cada execucao appenda o snapshot completo com categoria, poligono, strata, filtros e metricas de faturamento. |
| gcp | competitors | competitors_health_score_historic | Historico diario do health score por categoria de concorrentes. Avalia qualidade dos dados de pricing. |
| gcp | competitors | competitors_health_score_today | Snapshot diario de saude das categorias de concorrentes. Score ponderado: 30% quantidade + 40% consistencia + 30% frequencia de incompatibilidade. |
| gcp | competitors | competitors_historical | Historico de calendario de concorrentes — preco, ocupacao e bloqueio por listing/data, com snapshot diario. |
| gcp | competitors | competitors_inactive | Lista de concorrentes marcados como inativos. Usada para excluir listings inativos do calculo de categorias. |
| gcp | competitors | competitors_no_strata | Concorrentes sem classificacao de strata — pool de backup quando uma categoria tem menos de 15 concorrentes. |
| gcp | competitors | competitors_opportunities | Visao agregada de oportunidades por categoria — quantos concorrentes ativos, filtrados, manuais, backup existem por categoria. |
| gcp | competitors | competitors_polygons | Mapeamento de concorrentes para poligonos geograficos. Associa cada airbnb_listing_id ao poligono onde esta localizado. |
| gcp | competitors | competitors_quarantine | Concorrentes em quarentena — listings com regras de bloqueio ativas. |
| gcp | competitors | competitors_quarantine_inactive | Concorrentes em quarentena marcados como inativos, com status. |
| gcp | competitors | competitors_quarantine_iqr_revenue | Concorrentes em quarentena por regra IQR de faturamento — listings cujo faturamento mensal excede o threshold (Q3 + 2\*IQR) da categoria. |
| gcp | competitors | competitors_quarantine_iqr_sheets | Extensao da quarentena IQR com informacoes adicionais para planilhas — inclui quantidade de concorrentes e status. |
| gcp | competitors | listing_category | Mapeamento de listings internos (Seazone) para suas categorias de concorrentes, estado e regiao. Fonte de verdade para saber a qual categoria cada imovel pertence. |
| gcp | competitors | listings_health_details_historic | Historico diario de detalhes de saude por listing concorrente — frequencia de incompatibilidade de preco por listing. |
| gcp | competitors | listings_health_details_today | Detalhes de saude por listing individual — meses com precos incompativeis e frequencia de incompatibilidade. |
| gcp | competitors | polygons | Definicao geometrica dos poligonos (regioes) usados no sistema de concorrentes. Cada poligono tem um nome e sua geometria (GEOGRAPHY). |
| gcp | gaps | gaps_bi | Gaps de disponibilidade por listing para consumo do BI. Contem o tamanho do gap (em dias) por id_seazone, data e tipo (normal/prime). |
| gcp | gaps | gaps_rm | Gaps de disponibilidade agregados por periodo para uso do Revenue Management. Inclui cidade, categoria, datas de inicio/fim do gap, tipo e data de aquisicao. |
| gcp | infos | competitor_peak_demand | Alertas de pico de demanda baseados em ocupacao de concorrentes por regiao/poligono. Tabela externa apontando para GCS (parquet). |
| gcp | infos | internal_peak_demand | Alertas de pico de demanda interno por poligono, com tipo de alerta, faixa de capacidade, ocupacao de concorrentes, lead time e eventos mapeados. |
| gcp | infos | kpi_min_stay | Regras de estadia minima por listing e data, incluindo origem da regra, temporada, tipo climatico e observacoes. Versao completa sem particao (tabela legada). |
| gcp | infos | kpi_min_stay_current | Snapshot atual das regras de estadia minima por listing e data. Sobrescrito (WRITE_TRUNCATE) a cada execucao. |
| gcp | infos | kpi_min_stay_historic | Historico de regras de estadia minima por listing e data, com append diario. |
| gcp | infos | kpi_system_price | KPI de preco do sistema vs preco sugerido por listing e data, com detalhamento de categoria, cidade, poligono, estrato, feriado, tipo climatico. |
| gcp | infos | listings_in_quarantine | Lista simples de listings (id_seazone) atualmente em quarentena. |
| gcp | infos | listings_star_rating | Classificacao por estrelas (star rating) dos listings no Airbnb e Booking, com IDs de cada OTA e URL. |
| gcp | infos | listings_star_rating_for_bi | Versao simplificada do star rating para consumo do BI, contendo apenas id_seazone, star_rating_airbnb e star_rating_booking. |
| gcp | infos | min_stay_for_bi | Regras de estadia minima formatadas para consumo do BI. Mesma estrutura de kpi_min_stay_current. |
| gcp | infos | quarantine_listings | Listings em quarentena com indicadores de reserva nos primeiros 7, 15 e 30 dias apos ativacao. |
| gcp | infos | quarantine_listings_real-activation_date_historical | Historico da data real de ativacao dos listings em quarentena, com contagem de datas disponiveis, bloqueadas e datas de ativacao. |
| gcp | infos | stuck_min_price | Listings ou grupos com preco minimo 'travado' acima do preco medio praticado, indicando possivel problema de configuracao. |
| gcp | lake_observability | anomaly_mape_report | Relatorio diario de anomalias no MAPE de receita. Contem estatisticas descritivas (percentis, media, desvio padrao) e contagem de diferencas. |
| gcp | lake_observability | anomaly_price_metrics | Metricas diarias de anomalias de preco. Contem contagem total e distinta de IDs, alem de percentis do numero de linhas com anomalias. |
| gcp | lake_observability | mape_granularity_analysis | Analise de MAPE segmentada por diferentes granularidades (cidade, estado, tipo de imovel). Identifica segmentos criticos. |
| gcp | lake_observability | mape_history | Historico detalhado de MAPE por listing e por dia. Contem receita real vs estimada, preco, erro, status de bloqueio/ocupacao e metadados do imovel. |
| gcp | lake_observability | mape_ranked_properties | Ranking de imoveis por MAPE e score de impacto. Identifica imoveis com maior erro de previsao de receita. |
| gcp | lake_observability | priceav_mape_report | Relatorio diario de MAPE comparando precos e disponibilidade entre Lake e Sirius. Mede divergencia de preco medio e RMSE. |
| gcp | lake_observability | revenue_mape_monthly_big_errors | Imoveis com grandes erros mensais de MAPE de receita. Lista listings com MAPE elevado e a reducao de MAPE ao excluir o imovel. |
| gcp | lake_observability | revenue_mape_monthly_last_years | Evolucao mensal do MAPE de receita ao longo do tempo. Contem MAPE global, de bloqueio, de ocupacao e contagem de outliers por mes. |
| gcp | lake_observability | revenue_mape_report_last_days | Relatorio de MAPE de receita para diferentes janelas de dias recentes (ex: ultimos 7, 14, 30 dias). |
| gcp | lake_observability | scrapers_health | Monitoramento diario da saude dos scrapers. Registra para cada tabela/database o numero de linhas inseridas, IDs unicos e flag de erro. |
| gcp | lake_observability | vw_mape_history_grouped | View agrupada do historico de MAPE por listing. Contem colunas essenciais sem detalhes de segmentacao. |
| gcp | lake_observability | vw_scrapers_health_data | View consolidada de saude dos scrapers com comparacao entre ingestao de ontem e ultima ingestao bem-sucedida. Mostra variacao de volume. |
| gcp | lake_observability | vw_scrapers_health_delta | View de delta diario dos scrapers: compara rows_inserted de hoje vs ontem para detectar quedas ou aumentos anomalos. |
| gcp | meta | berlinda_dash | Dashboard de performance com score de prioridade por listing — combina faturamento, metas, bloqueios e potencial de receita. |
| gcp | meta | frozen_competitors_data | Snapshot mensal dos dados de concorrentes usados para calculo de metas (baseline congelado). |
| gcp | meta | output_monthly | Performance mensal de listings Seazone vs meta baseada em percentis dos concorrentes. |
| gcp | meta | output_quarter | Performance trimestral completa — calculo de metas do trimestre inteiro agregado a partir dos dados mensais. |
| gcp | meta | output_quarter_confirmed | Performance trimestral parcial — dados confirmados do inicio do trimestre ate hoje. Util para acompanhamento em tempo real do trimestre corrente. |
| gcp | meta | performance_dash | Dashboard de performance mensal por listing — faturamento vs meta, ocupacao, bloqueios e preco medio. |
| gcp | system_price | aggressiveness_levels_unnested_active | Niveis de agressividade ativos com intervalos de antecedencia para precificacao dinamica por categoria. |
| gcp | system_price | aggressiveness_prices_and_levels_and_reactive_price_by_id_seazone | Resultado final do calculo de precos do system price por id_seazone. Contem niveis de agressividade, percentis de ocupacao/disponibilidade, preco do sistema, preco reativo (sapron) e preco final aplicado. |
| gcp | system_price | aggressiveness_prices_and_levels_by_id_seazone | Precos calculados para todos os niveis de agressividade por listing e data. Tabela central do sistema de precos GCP. |
| gcp | system_price | cluster_category | Mapeamento de clusters para categorias de precificacao. |
| gcp | system_price | cluster_matrix | Matriz de regras de precificacao por cluster e tipo climatico. Define percentis e tipos de preco para cada combinacao de sazonalidade, tipo de ocorrencia, sigla, ocupacao e intervalo de antecedencia. |
| gcp | system_price | cluster_matrix_active | Matriz de precificacao ativa com regras de sazonalidade e niveis de ocupacao por cluster. |
| gcp | system_price | fill_category_price | Mapeamento de preco de preenchimento automatico por prefixo de categoria normalizado. Usado quando nao ha preco calculado para uma categoria. |
| gcp | system_price | listings_system_price | Visao consolidada de todos os listings ativos com seus grupos (Cidade, Poligono, Categoria, Clima) e flag indicando se participam do system price. |
| gcp | system_price | listings_system_price_and_matrix | Extensao de listings_system_price com informacoes adicionais de elegibilidade: se possui matriz, se e elegivel, status, quantidade de concorrentes e flag de Florianopolis. |
| gcp | system_price | listings_system_price_by_category | Agregacao de listings por categoria com flag de system price. Util para visao resumida de quais categorias estao no system price. |
| gcp | system_price | prices_sent_sirius | Historico de precos enviados do GCP (system price) para o Sirius (AWS). Registra cada envio com preco, limites e motivo. |
| gcp | system_price | system_price_listings | Lista de id_seazone habilitados para o system price. Tabela de referencia usada como lookup. |
| gcp | system_price | warning_not_eligible_categories | Alerta de categorias nao elegiveis para o system price. Contem categoria, numero de concorrentes e motivo da inelegibilidade. |
| gcp | system_price | warning_not_eligible_categories_pending | Alertas pendentes de revisao para categorias nao elegiveis. |
| gcp | system_price | warning_not_eligible_categories_status | Historico de status dos alertas de categorias nao elegiveis. Inclui colunas Status e Comentario. |
| gcp | system_price | warning_prices_lower_range | Alerta de precos calculados abaixo do limite inferior do intervalo permitido. |
| gcp | system_price | warning_prices_lower_range_pending | Alertas pendentes de revisao para precos abaixo do limite inferior. |
| gcp | system_price | warning_prices_lower_range_status | Historico de status dos alertas de precos abaixo do limite inferior. |
| gcp | system_price | warning_prices_outside_strata | Alerta de precos que ultrapassam o limite do estrato superior. Detecta inversoes de hierarquia de strata. |
| gcp | system_price | warning_prices_outside_strata_pending | Alertas pendentes de revisao para precos fora do estrato. |
| gcp | system_price | warning_prices_outside_strata_status | Historico de status dos alertas de precos fora do estrato. |
| gcp | system_price | warning_prices_over_range | Alerta de precos calculados acima do limite superior do intervalo permitido. |
| gcp | system_price | warning_prices_over_range_pending | Alertas pendentes de revisao para precos acima do limite superior. |
| gcp | system_price | warning_prices_over_range_status | Historico de status dos alertas de precos acima do limite superior. |
| lake | brlink_seazone_clean_data | booking_details | Detalhes de anuncios do Booking.com (quartos, banheiros, area, facilidades). Dados coletados por scraping periodico. |
| lake | brlink_seazone_clean_data | clean_comments | Comentarios/avaliacoes de hospedes em anuncios Airbnb, limpos e normalizados. Inclui nota, idioma e identificacao do avaliador. |
| lake | brlink_seazone_clean_data | comments_booking | Comentarios e avaliacoes de hospedes vindos do Booking.com, incluindo notas por categoria (limpeza, instalacoes, localizacao, servicos, valor). |
| lake | brlink_seazone_clean_data | details | Detalhes completos dos listings Airbnb — anuncio, caracteristicas do imovel, host. Particionado por data de aquisicao. |
| lake | brlink_seazone_clean_data | internal_airbnb_details | Detalhes de anuncios Airbnb internos (Seazone): nome, descricao, amenidades, localizacao, regras, fotos, notas, tipo de listing e status de superhost. |
| lake | brlink_seazone_clean_data | internal_clean_comments | Comentarios/avaliacoes de hospedes em anuncios Airbnb internos (Seazone), limpos. |
| lake | brlink_seazone_clean_data | internal_conversion_rate | Taxa de conversao de anuncios Airbnb internos (Seazone): conversao do anuncio, anuncios similares, global, impressoes de busca. |
| lake | brlink_seazone_clean_data | internal_views | Visualizacoes de anuncios Airbnb internos (Seazone): views do anuncio, views de similares e impressoes de busca. |
| lake | brlink_seazone_clean_data | olx | Anuncios de imoveis da OLX coletados por scraping: preco, IPTU, condominio, area, quartos, banheiros, localizacao e dados do anunciante. |
| lake | brlink_seazone_clean_data | price_av | Precos e disponibilidade diaria de anuncios Airbnb (calendario). Inclui preco, fonte do preco, estadia minima e flags de checkin/checkout. |
| lake | brlink_seazone_clean_data | price_resolved | Precos resolvidos/consolidados de anuncios Airbnb: um preco final por listing e data, apos resolucao de conflitos entre fontes. |
| lake | brlink_seazone_clean_data | seazone_listings | Mapeamento entre airbnb_listing_id e id_seazone. Tabela de referencia para vincular anuncios Airbnb aos imoveis do portfolio Seazone. |
| lake | brlink_seazone_clean_data | seazone_listings_historic | Historico de mapeamento airbnb_listing_id para id_seazone ao longo do tempo. |
| lake | brlink_seazone_clean_data | vivareal | Anuncios de imoveis do VivaReal/ZAP coletados por scraping: precos de venda/aluguel, IPTU, condominio, area, quartos, vagas, amenidades. |
| lake | brlink_seazone_clean_data | vivareal_listing_type | Tabela de referencia/de-para para tipos de anuncio VivaReal: mapeia unit_type e usage_type para um new_type normalizado. |
| lake | brlink_seazone_enriched_data | analise_faturamento | Faturamento mensal enriquecido com strata, localizacao e detalhes do imovel. Tabela final para analise de faturamento e treinamento de modelos. |
| lake | brlink_seazone_enriched_data | block_and_occupancy | Dados enriquecidos de bloqueio e ocupacao por listing/dia: preco atual, preco de reserva, taxa de limpeza, motivo de bloqueio e status de ocupacao. |
| lake | brlink_seazone_enriched_data | booked_on_snapshot | Snapshot de reservas detectadas: compara estado anterior e atual do calendario Airbnb para identificar momento e preco da reserva. |
| lake | brlink_seazone_enriched_data | daily_fat | Tabela fato diaria consolidada: preco, ocupacao, bloqueio, receita diaria (day_fat) e receita apos desconto por listing/dia. Principal tabela de metricas operacionais. |
| lake | brlink_seazone_enriched_data | dead_alive | Status de vida/morte de anuncios Airbnb: data de nascimento, ultima aquisicao, flag alive/dead e data de morte. |
| lake | brlink_seazone_enriched_data | details_last_aquisitiondetails | Snapshot mais recente dos detalhes de cada listing. Um registro por airbnb_listing_id, sem particoes. |
| lake | brlink_seazone_enriched_data | fato_block_occupancy | View sobre tabela fato de receita e ocupacao mensal por listing. Combina dados do Pipe (web scraping proprio da Seazone) e AirDNA (dados comprados de terceiros — descontinuado, nao mais atualizado). A view faz CAST(ano/mes AS integer). |
| lake | brlink_seazone_enriched_data | location_last_aquisition | Ultima localizacao conhecida de cada listing. Um registro por airbnb_listing_id, sem particoes. |
| lake | brlink_seazone_enriched_data | reservations | Reservas detectadas e consolidadas: datas de checkin/checkout, preco total, estadia minima, duracao, antecedencia e status da reserva. |
| lake | rm_agent | rm_booking_curve_insights | Insights de curva de reserva por evento — ocupacao atual, forca de reserva e comparacao com edicao anterior. Uma linha por evento x cidade. |
| lake | rm_agent | rm_booking_curves | Curvas de reservas acumuladas por evento — compara edicao atual vs anterior para avaliar velocidade de locacao. Uma linha por evento x days_before_event x edicao. |
| lake | rm_agent | rm_booking_pace | Velocidade de reservas (booking pace) por poligono x checkin_date. Detecta quando a taxa de reservas dos ultimos 7 dias supera o P90 historico. |
| lake | rm_agent | rm_competitor_baseline | Baseline estatistico de ocupacao dos concorrentes por poligono. Media, desvio padrao e percentis (P65-P95) calculados sobre janela de 2 anos. |
| lake | rm_agent | rm_competitor_occupancy | Ocupacao diaria dos concorrentes por poligono. Total de listings, ocupados e taxa de ocupacao. |
| lake | rm_agent | rm_daily_report | Relatorio diario gerado por IA (Claude via OpenRouter). Uma coluna por secao: resumo, dinheiro na mesa, eventos proximos, oportunidades de pricing, etc. Coluna report_markdown contem o relatorio completo em Markdown. |
| lake | rm_agent | rm_demand_signals | Sinais de demanda anomala detectados por percentil adaptativo (sigma_distance vs baseline). Inclui tipo de sinal, nivel de alerta, confianca IA e nome de evento quando identificado. |
| lake | rm_agent | rm_holidays | Calendario de feriados e eventos agrupados por group_name. Usado como input para correlacionar sinais de demanda com eventos conhecidos. |
| lake | rm_agent | rm_internal_occupancy | Ocupacao diaria dos imoveis Seazone por poligono. Total de imoveis, ocupados, bloqueados e taxa de ocupacao interna. |
| lake | rm_agent | rm_pricing_alerts | Alertas de pricing comparando Seazone vs concorrentes. Inclui sigma_distance, tipo de sinal, nivel de alerta, confianca IA e status em portugues. |
| sirius | competitorsdata | blocked_listings_dates_temp | Tabela temporaria com datas bloqueadas por listing, gerada pelas regras de bloqueio (rules A-D). Cada regra appenda resultados; apply_rules consolida. |
| sirius | competitorsdata | competitors_no_strata | Pool de backup de concorrentes sem classificacao de strata. Usado quando uma categoria tem menos de 15 concorrentes. |
| sirius | competitorsdata | competitors_output | Lista curada de concorrentes com caracteristicas, strata e flags de filtragem. Espelho diario de competitors_category do GCP. |
| sirius | competitorsdata | competitors_plus | Mapeamento de listings Seazone (id_seazone/listing) para seus concorrentes no Airbnb (airbnb_listing_id). Use para JOINs entre dados sirius e lake. |
| sirius | competitorsdata | daily_revenue_competitors | Preco, ocupacao e receita diaria dos concorrentes com regras de bloqueio aplicadas (4 regras: review inativo, preco anomalo, ocupacao alta, futuro bloqueado). |
| sirius | competitorsdata | picos_de_demanda_em_concorrentes | Alertas de picos de demanda detectados entre concorrentes por regiao/poligono, indicando periodos com alta taxa de ocupacao. |
| sirius | inputdata | allowed_periods_current_unnested | Periodos permitidos para precificacao por listing, desnormalizados (uma linha por data). Versao current apenas. |
| sirius | inputdata | climate | Classificacao climatica por listing/categoria — mapeia imoveis para tipos de clima (tropical, subtropical, etc). |
| sirius | inputdata | holidays | Calendario de feriados e eventos por regiao — define periodos de alta demanda com datas de inicio/fim e fator prime. |
| sirius | inputdata | listings_info | Informacoes completas do imovel do sistema Stays — tipo, subtipo, capacidade, quartos, banheiros, endereco, coordenadas. |
| sirius | inputdata | seasonality | Definicao de temporadas por tipo de clima — mapeia periodos (datas inicio/fim) para estacoes (alta, baixa, media). |
| sirius | inputdata | setup_groups | Define a qual categoria cada listing pertence. Tabela central de categorizacao de imoveis Seazone. |
| sirius | inputdata | special_prices | Precos minimo/maximo/fixo configurados pelo proprietario para intervalos de datas especificas. |
| sirius | pricingdata | f_prices_sirius_stays | View que cruza last_offered_raw_price (preco bruto) com last_offered_price (preco final) para mostrar o impacto de cada regra de stays. |
| sirius | pricingdata | historical_prices | Historico completo de todos os precos oferecidos, com metadados detalhados de cada calculo. |
| sirius | pricingdata | historical_raw_prices | Historico de precos brutos — versao simplificada sem variacoes de desconto/min_stay. |
| sirius | pricingdata | last_offered_price | Ultimo preco oferecido por listing+data. Filtrado onde discount=False, deduplicado pelo timestamp mais recente. |
| sirius | pricingdata | last_offered_raw_price | Ultimo preco bruto por listing+data. Lookback de 7 dias. Full refresh diario. |
| sirius | pricingdata | price_before_stays_temp | Tabela de staging temporaria para novos registros de preco antes da consolidacao em historical_prices. |
| sirius | pricingdata | raw_price_temp | Tabela de staging temporaria para precos brutos antes da consolidacao em historical_raw_prices. |
| sirius | pricingdata | staircase | Classificacao de listings em clusters de faturamento (staircase) por categoria. Calcula z-score do faturamento percentual de cada listing dentro da categoria e atribui clusters: Muito Baixo, Baixo, Medio, Alto, Muito Alto. |
| sirius | revenuedata | daily_revenue_sapron | Receita diaria completa por listing do sistema Sapron — inclui todos os registros (ativos e inativos). Versao nao filtrada de daily_revenue_sapron_active. |
| sirius | revenuedata | daily_revenue_sapron_active | Receita diaria por listing do sistema Sapron — precos, ocupacao, bloqueios e metricas de reservas. |
| sirius | revenuedata | reservations_sapron | Reservas do sistema Sapron com detalhes de preco, taxas, datas de check-in/out e plataforma. |
| sirius | saprondata | listing_franchises | Mapeamento de franquias por listing — indica qual franquia/anfitriao opera cada imovel, com localizacao. |
| sirius | saprondata | listing_otas | Mapeamento de listings para plataformas OTA (Airbnb, Booking, etc) — indica em quais OTAs cada imovel esta listado. |
| sirius | saprondata | listing_status | Status de ativacao/inativacao de listings — indica se o imovel esta ativo, data de ativacao, churn e data de churn. |

## Exemplos de Queries

### Ultimo preco oferecido para um listing

```sql
-- source='sirius'
SELECT id_seazone, date, price, origin, min_stay
FROM last_offered_price
WHERE id_seazone = 'ABC12'
ORDER BY date, min_stay
```

### Categoria de um listing

```sql
-- source='sirius'
SELECT id_seazone, group_name as categoria
FROM setup_groups
WHERE state = 'current' AND group_type = 'Categoria'
  AND id_seazone = 'ABC12'
```

### Preco do sistema GCP para um listing

```sql
-- source='gcp'
SELECT id_seazone, date, system_price, aggressive, standard, moderate
FROM system_price.aggressiveness_prices_and_levels_by_id_seazone
WHERE id_seazone = 'ABC12' AND date >= CURRENT_DATE
```

### Concorrentes ativos de uma categoria

```sql
-- source='sirius'
SELECT airbnb_listing_id, polygon, listing_type, number_of_bedrooms, strata
FROM competitors_output
WHERE state = 'current'
  AND passed_the_filters = true AND alive = true AND is_active = true
  AND polygon = 'poligono' AND listing_type = 'apartamento'
  AND strata = 'JR' AND number_of_bedrooms = 1
```

### Ocupacao mensal de listings no Lake (fato_block_occupancy)

*ano e mes sao colunas INT — sem aspas, sem zero a esquerda.*

```sql
-- source='lake'
SELECT airbnb_listing_id, ano, mes, faturamento, occupied_dates,
       available_dates, days_in_month, blocked_dates,
       CASE WHEN days_in_month = blocked_dates THEN null
            ELSE CAST(occupied_dates AS DOUBLE) / (days_in_month - blocked_dates)
       END as taxa_ocupacao
FROM fato_block_occupancy
WHERE ano = 2025 AND mes = 2
LIMIT 100
```

### Numero de listings por cidade no decorrer dos meses

*ano='2025' e STRING. mes em details e STRING sem zero a esquerda.*

```sql
-- source='lake'
SELECT det.ano, CAST(det.mes AS INTEGER) as mes,
       COUNT(DISTINCT det.airbnb_listing_id)
FROM brlink_seazone_clean_data.details det
JOIN brlink_seazone_enriched_data.location_last_aquisition loc
  USING (airbnb_listing_id)
WHERE loc.city = 'Florianópolis' AND det.ano = '2025'
GROUP BY det.ano, det.mes
ORDER BY det.ano, CAST(det.mes AS INTEGER)
```

### Metas mensais — snapshot mais recente, sem agregacao (GCP)

*QUALIFY funciona direto quando NAO ha agregacao (COUNT/AVG/SUM). Para agregar, usar CTE (ver exemplo abaixo).*

```sql
-- source='gcp'
SELECT *
FROM `meta.output_monthly`
WHERE year_month = '2026-02'
QUALIFY MAX(timestamp) OVER (PARTITION BY year_month) = timestamp
```

### Metas mensais — agregacao sobre snapshot mais recente (GCP)

*QUALIFY nao funciona com agregacoes no mesmo nivel — filtrar o snapshot numa CTE primeiro, depois agregar.*

```sql
-- source='gcp'
WITH latest AS (
  SELECT *
  FROM `meta.output_monthly`
  WHERE year_month = '2026-02'
  QUALIFY MAX(timestamp) OVER (PARTITION BY year_month) = timestamp
)
SELECT
  COUNT(DISTINCT listing) AS total_listings,
  COUNT(DISTINCT CASE WHEN meta_result = 'bateu' THEN listing END) AS bateram_meta,
  ROUND(COUNT(DISTINCT CASE WHEN meta_result = 'bateu' THEN listing END) * 100.0
    / NULLIF(COUNT(DISTINCT CASE WHEN meta_result IS NOT NULL THEN listing END), 0), 1) AS pct_bateram
FROM latest
```

### Preco medio e receita liquida: Seazone vs concorrentes Airbnb (ultimo ano)

*Substitua {inputdata}, {revenuedata}, {competitorsdata} pelos nomes reais obtidos via list_databases(source='sirius'). O fator 1.19 e o markup Stays→Airbnb vigente — consulte o glossario 'Markup Stays→Airbnb' para o historico de fatores.*

```sql
-- source='sirius'
-- Substitua {inputdata}, {revenuedata}, {competitorsdata} pelos nomes reais
-- via list_databases(source='sirius') antes de executar.
-- Markup Stays→Airbnb: usar fator vigente (ver glossario para historico).
-- Airbnb comissao: 15% sobre o preco listado (net = preco * 0.85).
WITH listings_categoria AS (
    SELECT id_seazone, group_name AS category
    FROM "{inputdata}".setup_groups
    WHERE state = 'current' AND group_type = 'Categoria'
      AND group_name = 'Florianopolis-UFSC-apartamento-TOP-1Q'
),
receita_seazone AS (
    SELECT lc.category,
           date_trunc('month', dr.date) AS mes,
           AVG(dr.reservation_avg_net_price) AS avg_price_seazone,
           -- Preco que o hospede ve no Airbnb (base * markup vigente)
           AVG(dr.reservation_avg_net_price) * 1.19 AS avg_price_seazone_airbnb,
           -- Receita liquida Seazone (preco Airbnb - 15% comissao)
           AVG(dr.reservation_avg_net_price) * 1.19 * 0.85 AS avg_net_revenue_seazone
    FROM listings_categoria lc
    JOIN "{revenuedata}".daily_revenue_sapron_active dr
      ON lc.id_seazone = dr.listing
    WHERE date_trunc('month', dr.date)
          BETWEEN DATE_TRUNC('month', DATE_ADD('year', -1, CURRENT_DATE))
          AND DATE_TRUNC('month', DATE_ADD('month', -1, CURRENT_DATE))
    GROUP BY lc.category, date_trunc('month', dr.date)
),
concorrentes_ids AS (
    SELECT lc.category, cp.airbnb_listing_id
    FROM listings_categoria lc
    JOIN "{competitorsdata}".competitors_plus cp ON lc.id_seazone = cp.listing
    WHERE cp.state = 'current'
    GROUP BY lc.category, cp.airbnb_listing_id
),
receita_concorrentes AS (
    SELECT ci.category,
           date_trunc('month', drc.date) AS mes,
           -- Preco Airbnb dos concorrentes (ja inclui markup da OTA)
           AVG(drc.price) AS avg_price_concorrentes,
           -- Receita liquida concorrentes (preco Airbnb - 15% comissao)
           AVG(drc.price) * 0.85 AS avg_net_revenue_concorrentes
    FROM concorrentes_ids ci
    JOIN "{competitorsdata}".daily_revenue_competitors drc
      ON ci.airbnb_listing_id = drc.airbnb_listing_id
    WHERE (drc.price_source = 'correct_price' OR drc.price_source IS NULL)
      AND drc.price IS NOT NULL
      AND date_trunc('month', drc.date)
          BETWEEN DATE_TRUNC('month', DATE_ADD('year', -1, CURRENT_DATE))
          AND DATE_TRUNC('month', DATE_ADD('month', -1, CURRENT_DATE))
    GROUP BY ci.category, date_trunc('month', drc.date)
)
SELECT rs.category, rs.mes,
       rs.avg_price_seazone_airbnb,
       rc.avg_price_concorrentes,
       rs.avg_net_revenue_seazone,
       rc.avg_net_revenue_concorrentes
FROM receita_seazone rs
JOIN receita_concorrentes rc ON rs.category = rc.category AND rs.mes = rc.mes
ORDER BY rs.mes
```

### Contar reservas de concorrentes (datas consecutivas)

*booked_on = data de criacao da reserva. Datas consecutivas com mesmo booked_on e occupied='true' formam 1 reserva. occupied e STRING ('true'/'false').*

```sql
-- source='lake'
SELECT airbnb_listing_id,
       CAST(booked_on AS DATE) AS booked_on_date,
       MIN(date) AS checkin, MAX(date) AS checkout,
       COUNT(*) AS noites
FROM brlink_seazone_enriched_data.daily_fat
WHERE occupied = 'true'
  AND booked_on IS NOT NULL
  AND date >= '2025-01-01' AND date < '2025-01-15'
GROUP BY airbnb_listing_id, CAST(booked_on AS DATE)
ORDER BY airbnb_listing_id, checkin
LIMIT 20
```

### Análise de ROI — preço de compra (VivaReal) vs faturamento anual Airbnb

*ROI = (faturamento_anual / preco_compra) \* 100. Particoes: vivareal usa STRING COM zero a esquerda (mes='01'); fato_block_occupancy usa INT (mes = 1); details usa STRING SEM zero (mes='1'). Nomenclaturas de bairro podem variar entre VivaReal e Airbnb.*

```sql
-- source='lake'
WITH purchase_prices AS (
    SELECT city, suburb, bedrooms,
           COUNT(*) AS num_listings_venda,
           AVG(sale_price) AS avg_sale_price
    FROM brlink_seazone_clean_data.vivareal
    WHERE ano = '2025' AND mes = '01' AND dia = '15'
      AND sale_price > 0 AND bedrooms > 0
    GROUP BY city, suburb, bedrooms
),
annual_revenue AS (
    SELECT loc.city, loc.suburb,
           CAST(det.number_of_bedrooms AS smallint) AS bedrooms,
           COUNT(DISTINCT bo.airbnb_listing_id) AS num_listings_airbnb,
           SUM(bo.faturamento)
               / COUNT(DISTINCT bo.airbnb_listing_id) AS avg_annual_revenue
    FROM brlink_seazone_enriched_data.fato_block_occupancy bo
    JOIN brlink_seazone_enriched_data.location_last_aquisition loc
      ON bo.airbnb_listing_id = loc.airbnb_listing_id
    JOIN brlink_seazone_clean_data.details det
      ON bo.airbnb_listing_id = det.airbnb_listing_id
      AND det.ano = '2025' AND det.mes = '1' AND det.dia = '6'
    WHERE bo.ano = 2025
      AND det.number_of_bedrooms > 0
    GROUP BY loc.city, loc.suburb, det.number_of_bedrooms
)
SELECT pp.city, pp.suburb, pp.bedrooms,
       pp.num_listings_venda, pp.avg_sale_price,
       ar.num_listings_airbnb, ar.avg_annual_revenue,
       ROUND((ar.avg_annual_revenue / pp.avg_sale_price) * 100, 2)
           AS roi_pct
FROM purchase_prices pp
JOIN annual_revenue ar
  ON pp.city = ar.city
  AND pp.suburb = ar.suburb
  AND pp.bedrooms = ar.bedrooms
WHERE ar.avg_annual_revenue > 0
ORDER BY roi_pct DESC
LIMIT 30
```

## Dicas

* Se precisar buscar uma tabela em multiplos sources ou databases, peca ao assistente para usar um agente em paralelo — economiza contexto e e mais rapido.