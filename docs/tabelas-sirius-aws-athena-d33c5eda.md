<!-- title: Tabelas Sirius (AWS Athena) | url: https://outline.seazone.com.br/doc/tabelas-sirius-aws-athena-bYkHXT1Bby | area: Tecnologia -->

# Tabelas Sirius (AWS Athena)

# Tabelas Sirius (AWS Athena)

> Gerado automaticamente a partir de `mcp/table_metadata.py`. Nao edite diretamente.

## competitorsdata

### blocked_listings_dates_temp

* **Proposito:** Tabela temporaria com datas bloqueadas por listing, gerada pelas regras de bloqueio (rules A-D). Cada regra appenda resultados; apply_rules consolida.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** Tabela temporaria — sobrescrita a cada execucao do pipeline. Coluna 'rule' e array<string> com nomes das regras.
* **Notas:** Tabela da PIC. Populada por rule_a (6m_ocup), rule_b, rule_c, rule_d e consolidada por apply_rules.

### competitors_no_strata

* **Proposito:** Pool de backup de concorrentes sem classificacao de strata. Usado quando uma categoria tem menos de 15 concorrentes.
* **View:** Nao
* **Particoes:** state, acquisition_date
* **Formato particao:** state: STRING 'current' ou 'historic'.
* **Dica de query:** Filtre por state='current'.
* **Notas:** Tabela da PIC.

### competitors_output

* **Proposito:** Lista curada de concorrentes com caracteristicas, strata e flags de filtragem. Espelho diario de competitors_category do GCP.
* **View:** Nao
* **Particoes:** state, acquisition_date
* **Formato particao:** state: STRING 'current' ou 'historic'. acquisition_date: STRING timestamp (ex: '2026-03-17 13:57:45'). Use DATE(acquisition_date) para filtrar por data.
* **Dica de query:** Para concorrentes ativos: WHERE state='current' AND passed_the_filters=true AND alive=true AND is_active=true.
* **Notas:** Tabela da PIC.

### competitors_plus

* **Proposito:** Mapeamento de listings Seazone (id_seazone/listing) para seus concorrentes no Airbnb (airbnb_listing_id). Use para JOINs entre dados sirius e lake.
* **View:** Nao
* **Particoes:** state, acquisition_date
* **Formato particao:** state: STRING 'current' ou 'historic'. acquisition_date: STRING timestamp.
* **Dica de query:** Filtre sempre por state='current' para o mapeamento vigente.
* **Notas:** Tabela da PIC. Chave de join: listing (= id_seazone) <-> airbnb_listing_id.

### daily_revenue_competitors

* **Proposito:** Preco, ocupacao e receita diaria dos concorrentes com regras de bloqueio aplicadas (4 regras: review inativo, preco anomalo, ocupacao alta, futuro bloqueado).
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** booked_on = data de criacao da reserva. Para contar reservas de concorrentes: identificar datas consecutivas com mesmo booked_on, mesmo listing ID e occupied=true — cada grupo de datas consecutivas = 1 reserva.
* **Notas:** Tabela da PIC. Volume: milhoes de linhas. block_reason contem ARRAY<STRING> com os motivos de bloqueio. block_reason = motivo do bloqueio da data no calendario. Util para distinguir bloqueios manuais de reservas.

### picos_de_demanda_em_concorrentes

* **Proposito:** Alertas de picos de demanda detectados entre concorrentes por regiao/poligono, indicando periodos com alta taxa de ocupacao.
* **View:** Nao
* **Particoes:** day_alert
* **Formato particao:** STRING formato YYYY-MM-DD.
* **Dica de query:** Filtre por day_alert para restringir o scan.
* **Notas:** Tabela da PIC.

## inputdata

### allowed_periods_current_unnested

* **Proposito:** Periodos permitidos para precificacao por listing, desnormalizados (uma linha por data). Versao current apenas.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** origin indica a fonte da regra. group_level define a hierarquia.
* **Notas:** Origem: api-stays/sheets_communication. Tabela desnormalizada a partir de allowed_periods.

### climate

* **Proposito:** Classificacao climatica por listing/categoria — mapeia imoveis para tipos de clima (tropical, subtropical, etc).
* **View:** Nao
* **Particoes:** state, timestamp
* **Formato particao:** state: STRING 'current' ou 'historic'. timestamp: STRING.
* **Dica de query:** Filtre por state='current'. climate_type define o tipo de clima.
* **Notas:** Origem: api-stays/sheets_communication. Usado para determinar sazonalidade.

### holidays

* **Proposito:** Calendario de feriados e eventos por regiao — define periodos de alta demanda com datas de inicio/fim e fator prime.
* **View:** Nao
* **Particoes:** state, timestamp
* **Formato particao:** state: STRING 'current' ou 'historic'. timestamp: STRING.
* **Dica de query:** Filtre por state='current'. holiday_type diferencia feriados nacionais, regionais e eventos. prime contem array de fatores.
* **Notas:** Origem: api-stays/sheets_communication. Usado no calculo de precos para periodos de pico.

### listings_info

* **Proposito:** Informacoes completas do imovel do sistema Stays — tipo, subtipo, capacidade, quartos, banheiros, endereco, coordenadas.
* **View:** Nao
* **Particoes:** state, date
* **Formato particao:** state: STRING 'current' ou 'historic'. date: STRING formato YYYY-MM-DD.
* **Dica de query:** Filtre por state='current'. Campos aninhados: address (struct), latlng (struct), _mstitle/_msdesc (struct multilingual).
* **Notas:** Origem: API Stays. Contem structs complexos. id = id_seazone. instantbooking indica reserva instantanea.

### seasonality

* **Proposito:** Definicao de temporadas por tipo de clima — mapeia periodos (datas inicio/fim) para estacoes (alta, baixa, media).
* **View:** Nao
* **Particoes:** state, timestamp
* **Formato particao:** state: STRING 'current' ou 'historic'. timestamp: STRING.
* **Dica de query:** Filtre por state='current'. season define a estacao. climate_type vincula a tabela climate.
* **Notas:** Origem: api-stays/sheets_communication. Join com climate via climate_type.

### setup_groups

* **Proposito:** Define a qual categoria cada listing pertence. Tabela central de categorizacao de imoveis Seazone.
* **View:** Nao
* **Particoes:** state, timestamp
* **Formato particao:** state: STRING 'current' ou 'historic'. timestamp: STRING.
* **Dica de query:** Para categorias ativas: WHERE state='current' AND group_type='Categoria'.
* **Notas:** group_name = nome da categoria (ex: 'Floripa-2Q-SUP'). Origem: S3/planilhas.

### special_prices

* **Proposito:** Precos minimo/maximo/fixo configurados pelo proprietario para intervalos de datas especificas.
* **View:** Nao
* **Particoes:** state, timestamp
* **Formato particao:** state: STRING 'current' ou 'historic'.
* **Dica de query:** Filtre por state='current' para regras ativas. type pode ser: 'Fixo', 'Minimo', 'Maximo'.
* **Notas:** Origem: S3/planilhas.

## pricingdata

### f_prices_sirius_stays

* **Proposito:** View que cruza last_offered_raw_price (preco bruto) com last_offered_price (preco final) para mostrar o impacto de cada regra de stays.
* **View:** Sim
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** Disponivel apenas em producao. percentage_rules = impacto combinado de todas as regras de stays. Precos finais Stays — ao comparar com concorrentes Airbnb, aplicar markup Stays→Airbnb (ver glossario).
* **Notas:** Filtra discount=False. Valores nulos em increment_agc/discount_rate/price_change_gapper = regra nao aplicada (equivale a 0).

### historical_prices

* **Proposito:** Historico completo de todos os precos oferecidos, com metadados detalhados de cada calculo.
* **View:** Nao
* **Particoes:** acquisition_date
* **Formato particao:** STRING formato YYYY-MM-DD (ex: '2025-01-15'). Obrigatorio filtrar.
* **Dica de query:** Sempre filtre: WHERE acquisition_date >= '2025-01-01'. Volume: milhoes de linhas. Precos finais Stays — ao comparar com concorrentes Airbnb, aplicar markup Stays→Airbnb (ver glossario).
* **Notas:** Consolidado em batch a partir de price_before_stays_temp. origin pode ser: 'heuristica', 'sistema', 'manual', 'staircase'.

### historical_raw_prices

* **Proposito:** Historico de precos brutos — versao simplificada sem variacoes de desconto/min_stay.
* **View:** Nao
* **Particoes:** acquisition_date
* **Formato particao:** STRING formato YYYY-MM-DD. Obrigatorio filtrar.
* **Dica de query:** Sempre filtre: WHERE acquisition_date >= 'YYYY-MM-DD'.
* **Notas:** Consolidado em batch a partir de raw_price_temp.

### last_offered_price

* **Proposito:** Ultimo preco oferecido por listing+data. Filtrado onde discount=False, deduplicado pelo timestamp mais recente.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** Precos finais Stays — ao comparar com concorrentes Airbnb, aplicar markup Stays→Airbnb (ver glossario).
* **Notas:** Full refresh diario. Inclui todas as colunas de metadados de historical_prices.

### last_offered_raw_price

* **Proposito:** Ultimo preco bruto por listing+data. Lookback de 7 dias. Full refresh diario.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** —
* **Notas:** —

### price_before_stays_temp

* **Proposito:** Tabela de staging temporaria para novos registros de preco antes da consolidacao em historical_prices.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** —
* **Notas:** Deletada apos processamento. Normalmente vazia ou com dados parciais. Mesmas colunas de historical_prices.

### raw_price_temp

* **Proposito:** Tabela de staging temporaria para precos brutos antes da consolidacao em historical_raw_prices.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** —
* **Notas:** Deletada apos processamento. Normalmente vazia. Mesmas colunas de historical_raw_prices.

### staircase

* **Proposito:** Classificacao de listings em clusters de faturamento (staircase) por categoria. Calcula z-score do faturamento percentual de cada listing dentro da categoria e atribui clusters: Muito Baixo, Baixo, Medio, Alto, Muito Alto.
* **View:** Nao
* **Particoes:** state, timestamp
* **Formato particao:** state: STRING ('current' ou 'historic'). timestamp: STRING formato 'YYYY-MM-DD HH:MM:SS'.
* **Dica de query:** Filtre por state='current' para obter a classificacao vigente. Categorias com menos de 7 listings sao excluidas no calculo.
* **Notas:** Gerado pelo Lambda staircase/lambda_function.py. Usa faturamento dos ultimos 20 dias + proximos 40 dias. Particionado por state+timestamp para manter historico.

## revenuedata

### daily_revenue_sapron

* **Proposito:** Receita diaria completa por listing do sistema Sapron — inclui todos os registros (ativos e inativos). Versao nao filtrada de daily_revenue_sapron_active.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** O campo 'listing' e equivalente a id_seazone. Para dados apenas ativos, use daily_revenue_sapron_active.
* **Notas:** Escrita como parquet unico (sem particoes). Origem: api-stays via Sapron API. Atualizacao: diaria.

### daily_revenue_sapron_active

* **Proposito:** Receita diaria por listing do sistema Sapron — precos, ocupacao, bloqueios e metricas de reservas.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** O campo 'listing' e equivalente a id_seazone. Use reservation_avg_net_price para receita liquida.
* **Notas:** Atualizacao: diaria. Origem: sistema Sapron (externo).

### reservations_sapron

* **Proposito:** Reservas do sistema Sapron com detalhes de preco, taxas, datas de check-in/out e plataforma.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** O campo 'listing' e equivalente a id_seazone. blocked=true indica bloqueio (nao reserva real).
* **Notas:** Atualizacao: diaria. ota pode ser: 'Airbnb', 'Booking', 'Direto', etc.

## saprondata

### listing_franchises

* **Proposito:** Mapeamento de franquias por listing — indica qual franquia/anfitriao opera cada imovel, com localizacao.
* **View:** Nao
* **Particoes:** state, aquisition_date
* **Formato particao:** state: STRING 'current' ou 'historic'. aquisition_date: STRING timestamp (ex: '2026-03-16 08:00:20').
* **Dica de query:** Filtre por state='current' para o mapeamento vigente. code = id_seazone (nome do imovel).
* **Notas:** Origem: api-stays via Metabase API. Atualizacao: quinzenal. Campos: code, anfitriao, host_id, status, bairro, estado, endereco_completo, city, state.

### listing_otas

* **Proposito:** Mapeamento de listings para plataformas OTA (Airbnb, Booking, etc) — indica em quais OTAs cada imovel esta listado.
* **View:** Nao
* **Particoes:** state, aquisition_date
* **Formato particao:** state: STRING 'current' ou 'historic'. aquisition_date: STRING timestamp.
* **Dica de query:** Filtre por state='current'. code = id_seazone (nome do imovel). id_in_ota = id do listing na OTA.
* **Notas:** Origem: api-stays via Metabase API. Atualizacao: semanal. Join com listing_franchises via code.

### listing_status

* **Proposito:** Status de ativacao/inativacao de listings — indica se o imovel esta ativo, data de ativacao, churn e data de churn.
* **View:** Nao
* **Particoes:** Nenhuma
* **Formato particao:** N/A
* **Dica de query:** Tabela pequena (overwrite completo). code = id_seazone (nome do imovel). internal_property_id = id do listing no Sapron. churn=true indica imovel que saiu da carteira.
* **Notas:** Origem: api-stays via Metabase API. Escrita com mode='overwrite' (sem historico). Campos: internal_property_id (id Sapron), code (id_seazone), status, activation_date, inactivation_date, host_id, churn, churn_date.