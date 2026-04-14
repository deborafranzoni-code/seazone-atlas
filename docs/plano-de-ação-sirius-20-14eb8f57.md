<!-- title: Plano de ação - Sirius 2.0 | url: https://outline.seazone.com.br/doc/plano-de-acao-sirius-20-fOoO7oRtOU | area: Tecnologia -->

# Plano de ação - Sirius 2.0

# Quais problemas tentaremos resolver?

Aumentar a velocidade de precificação de RM

* RM não consegue precificar muitos imóveis com muita frequência e qualidade alta
* Não existe visibilidade quanto à reservas realizadas com preço muito baixo (geralmente quem descobre é o proprietário, que bate em CS e que bate em RM)
* Não existe visibilidade quanto à diárias definidas com preço muito baixo (o que acaba criando o problema acima)
* A precificação não olha para os preços e ocupação dos concorrentes, logo não é possível saber onde os listings da Seazone estão frente à concorrência
* Não existem alertas de anúncios que estão com avaliações muito negativas ou comentários que degradam seu resultado final

# Quais os objetivos de cada módulo?

### Avaliação de anúncios:

Ver quais anúncios da Seazone estão bons ou ruins, com tendência de melhora ou piora. "Bom" ou "ruim" é basicamente a nota consolidada do imóvel.

*Também podemos avaliar os comentários com um dicionário de palavras "proibidas" ou análise de sentimento.*

### Seleção de Concorrentes:

Selecionar concorrentes de cada imóvel da Seazone que fazem sentido e são significativos para comparar os faturamentos e para auxiliar na precificação.

### Sistema Supervisório:

Ver se estamos vendendo reservas muito barato.

### Precificação:

Objetivo é definir o "melhor" preço possível para cada data no futuro, para cada imóvel, respeitando as regras de preço definidas por diversos agentes externos (Operação da Seazone, Proprietários, CS etc), garantindo que não fiquemos com preços de diárias abaixo do mercado, ou muito acima (evitando que a gente alugue).

# Quais KPIs do RM o Sirius 2.0 deve ser capaz de ajudar a medir ou de executar o processo?

| **KPI** | **Módulo do Sirius 2.0** |    |
|----|----|----|
| Número de erros de precificação detectados na semana | Sistema supervisório |    |
| Número de reservas com erro de precificação detectadas | Sistema supervisório |    |
| Número de reservas canceladas por erro na semana | Sistema supervisório |    |
| Número total de erros de precificação detectados pelo supervisório | Sistema supervisório |    |
| Número de pedidos de preço mínimo na semana | Precificação |    |
| Número de pedidos de recriação de anúncio Airbnb na semana | Avaliação de anúncios |    |
| Número de solicitações de CS na semana | Avaliação de desempenho |    |
| Imóveis sem reservas futuras |    |    |
| Número de imóveis ativos |    |    |
| % do portfolio sem reservas futuras |    |    |
| Imóveis sem venda de reservas na última semana |    |    |
| % do portifólio sem reservas na última semana |    |    |
| Diária média executada da semana |    |    |
| Número de imóveis com desempenho abaixo do esperado no mês | Avaliação de desempenho |    |
| Número de imóveis com desempenho dentro do esperado no mês | Avaliação de desempenho |    |
| Número de imóveis com desempenho acima do esperado no mês | Avaliação de desempenho |    |
| Taxa de ocupação média dos imóveis na semana (excluindo bloqueios) |    |    |
| Revpar executado da semana |    |    |
| Faturamento liquido executado na semana |    |    |
| Faturamento líquido vendido na semana |    |    |
| Faturamento mensal de diárias |    |    |
| % da meta do mês |    |    |

# Quais são as tasks principais?

Validadas com o Probst e Campana em 20/07/2023: [Link](https://drive.google.com/file/d/128piLzpPkcQu-Us1uM67Hayj1C1Qz0Nm/view)

### Comunicação com a Stays e CRUD:


1. Comunicação com a Stays

   
   1. Márcio: Stays ↔ AWS

      
      1. Pegar tabela de imóveis com todos os imóveis da Stays (levando em consideração que existem imóveis que estão na Stays MAS não estão ativos, não devem ser precificados!)
      2. Colocar uma diária em um imóvel da Seazone, na Stays
      3. Ler as diárias de um imóvel da Seazone
      4. No caso da precificação, gravar no S3 uma cópia dos [dados enviados para a Stays](/doc/plano-de-acao-sirius-20-dl5J2DXUVE), com a timestamp (data/hora/minuto) de precificação
   2. Hideki: AWS ↔ Sheets

      
      1. Três botões: "Executar Sirius para tudo", "Executar Sirius para selecionados", "Enviar diárias para Stays"
      2. Também deve ter uma rodagem automática 1x ao dia (ou seja, um "Executar Sirius para tudo" automaticamente 1x por dia)
      3. Salvar as regras que estão sendo aplicadas em um imóvel sempre que os preços forem enviados para a Stays. Exemplo: JBV108 é precificado individualmente às 10:00 do dia 01/08/2023 → as regras que estavam sendo aplicadas nele são salvas na AWS. Depois o JBV108, JBV110 e ILC2412 são precificados às 14:00 do mesmo dia → as regras que estavam sendo aplicadas neles são salvas na AWS.

         
         1. Sugestão: salvar as regras do imóvel com a timestamp (data/hora/minuto) de precificação
2. Planilha setup groups

   
   1. Deve ter uma planilha, **separada**, a "setup_groups" que é o "inventário" de imóveis da Seazone e os seus respectivos grupos de pertencimento
   2. Inserção manual dos imóveis nesta planilha

      
      1. consequência: inserção manual dos mesmos imóveis em todas as outras planilhas
      2. Para amenizar este problema, fazer um esquema de **"warnings"**, onde será feito um "diff" entre a planilha "setup_groups" e as outras planilhas que também utilizam a lista de imóveis da Seazone. Caso algum imóvel esteja na planilha setup_groups e não esteja em uma planilha de um módulo específico, é lançado um alerta (e vice-versa)
   3. Exemplo da planilha: 1 imóvel pode participar de mais de um grupo, 1 grupo pode ter mais de 1 imóvel.

| **Lista de Imóveis** | **Lista de Grupos** |
|----|----|
| ABC102 | Fase2 |
| ABC102 | ITA |
| ABC102 | Todas as Regras |
| ABC102 | Todos os imóveis |
| ABC1301 | Fase2 |
| ABC1301 | ITA |
| ABC1301 | Todos os imóveis |
| ABC1303 | Fase2 |
| ABC1303 | ITA |
| ABC1303 | ITAMASTER2Q |

### Avaliação de Anúncios:


1. Criar planilha no Sheets com três abas: Inputs, Análise 1 ~~e Análise 2~~
2. Queriar todos os listings da Seazone no Lake do Pipe para pegar os dados de avaliação (*rating*)
3. Análise 1: selecionar quais listings estão com notal total abaixo de **X** (**input**)

   
   1. desconsiderar anúncios com nota indisponível (geralmente são anúncios novos que ainda não possuem nota)
4. ~~Análise 2: selecionar quais listings, nos últimos 21 dias (input) estão com uma nota média menor ou igual 3 (input)~~
5. Salvar os resultados no S3
6. Colocar resultados nas abas correspondentes do Sheets

Frequência de execução desse processo: 1x por semana

Planilha de input/output de exemplo: <https://docs.google.com/spreadsheets/d/19KL-xB2-fI7xUcUzzxxDDZNqmWXW7AtT_tiwwTTEGvI/edit#gid=789146069>

Extra: (aparentemente já existe na Operação então melhor nem se preocupar com isso)

* mais fácil - adicionar um dicionário *hardcoded* de palavras que não deveriam aparecer normalmente num comentário do Airbnb (por exemplo "esgoto"), que também irá gerar alertas no Sheets
* mais difícil - análise de sentimentos nos comentários

### Seleção de concorrentes


1. Criar uma planilha no Sheets, que terá uma lista de todos os imóveis da Seazone (inserido pelos analistas do RM). Cada imóvel terá alguns "atributos" para selecionar seus concorrentes:

   
   1. **concorrentes gerais ALL STRATA**:

      
      1. Cidades
      2. Bairros de cada uma dessas cidades
      3. Listing types
      4. Quartos
   2. **concorrentes gerais:**

      
      1. Cidades
      2. Bairros de cada uma dessas cidades
      3. Listing types
      4. Quartos
      5. Strata
   3. **concorrentes PLUS**:

      
      1. Atributos de **concorrentes gerais** e
      2. Número mínimo de reviews
      3. Número mínimo de star rating
      4. Número mínimo de noites vendidas, nos últimos 30 dias, em qualquer período (quantas "creation_date"s foram criadas nos últimos 30 dias)
      5. Se precisa ser superhost ou não
2. Queriar no Lake os concorrentes correspondentes de cada imóvel

   
   1. inicialmente é suficiente fazer isso 1x ao mês automaticamente
   2. \
3. Os concorrentes selecionados devem ser salvos no Lake

   
   1. Aqui optamos por não deixar output no Sheets pois um único imóvel da Seazone pode ter centenas ou até milhares de concorrentes, o que tornaria inviável mostrar no Sheets

Exemplo de planilha de Input:

| **Imóvel** | **Cidade** | **Bairro** | **Listing Type** | **Quartos** | **Strata** | **MinReviews** | **MinRating** | **MinSoldNightLast30Days** | **IsSuperHost** |
|----|----|----|----|----|----|----|----|----|----|
| VST025 | Anitápolis; Urubici | ALL | Casa; Apartamento | 1 | Jr | 50 | 4,5 | 28 | T |
| JBV108 | Florianópolis | Jurerê | Hotel | 1 | Top | 40 | 4,1 | 10 | T |
| SPC101 | São Paulo; São Caetano | Vila Prudente; Fundação | Casa | 3 | Master | 50 | 4,1 | 10 | T |
| SPC101 | São Paulo (Vila Prudente); São Caetano (Fundação) |    | Casa | 3 | Sup | 50 | 4,1 | 10 | T |

### Sistema supervisório


1. Criar planilha no Sheets com duas abas: inputs e outputs
2. Para cada imóvel da Seazone, seleciona os seus **concorrentes da mesma strata** (**concorrentes gerais,** a partir dos resultados da Seleção de Concorrentes)
3. Identifica, na granularidade diária, o valor das diárias dos imóveis da Seazone VS as dos seus concorrentes
4. Ver em qual percentil as diárias dos imóveis da Seazone se encontram frente aos concorrentes
5. Se estiver abaixo de um certo threshold (**input do usuário**), emite um alerta
6. Salva os resultados (alertas) no Lake
7. Coloca os resultados (alertas) na aba de output do Sheets

Frequência do processamento:

Exemplo de apresentação dos resultados na aba de outputs: <https://docs.google.com/spreadsheets/d/1Ly5AZV2drEYwzj1B9WOlnmpVPG3ZB5bW91Tik4T1-xQ/edit#gid=1770300547>

| **listing id** | **data** | **preço da diária** | **percentil 5** | **percentil 10** | **percentil 20** | **percentil 40** | **less than** |
|----|----|----|----|----|----|----|----|
| JBV108 | 13/06/2023 | R$250,00 | R$100,00 | R$150,00 | R$220,00 | R$400,00 | percentil 40 |
| JBV120 | 13/06/2023 | R$80,00 | R$100,00 | R$150,00 | R$220,00 | R$400,00 | percentil 5 |
| … | … | … | … | … | … | … | … |
| JBV108 | 19/12/2023 | R$550,00 | R$300,00 | R$350,00 | R$520,00 | R$600,00 | percentil 40 |
| JBV120 | 19/12/2023 | R$280,00 | R$300,00 | R$350,00 | R$520,00 | R$600,00 | percentil 5 |
| … | … | … | … | ... | ... | ... | … |
| … | … | … | ... | … | … | … | … |

### Avaliação de desempenho

Esta avaliação de desempenho é o mesmo método que será executado:


1. dentro do processo de precificação
2. por conta própria, separadamente

A ideia é um método que recebe como input: daily_fat do imóvel que o desempenho está sendo avaliado (tabela verdade, ou seja, valor que vem da Stays), daily_fat's dos concorrentes, período inicial e período final.

No processo de precificação o período inicial e período final são o início e fim de cada período quente, respectivamente.

Quando é feita "por conta própria" o período inicial e período final serão o começo e o fim do mês, respectivamente.

Passo a passo:


1. Cria planilha no Sheets que irá apresentar os resultados da avaliação de desempenho
2. Criar aba com os inputs

   
   1. faz a ingestão dos inputs na AWS
3. Para cada imóvel da Seazone, seleciona os seus **concorrentes gerais ALL STRATA**
4. Verificar, para os períodos definidos pelo analista na aba de input, como está o faturamento previsto (reservas realizadas e executadas) do imóvel da Seazone frente aos seus concorrentes
5. Classificar quantos estão "dentro do esperado", "abaixo do esperado", "acima do esperado" etc
6. Salvar os resultados no Lake
7. Apresentar os últimos resultados (última execução) na planilha do Sheets

Este processo é executado manualmente 1 ou 2x por semana.

Exemplo de apresentação dos resultados:

<https://docs.google.com/spreadsheets/d/1DxuX_GQQzhrOjUfYtoLEJLSjX6bLenvDrkn2QUV0DoY/edit#gid=0>

### Precificação (do cluster principal)

Diagrama do fluxo de precificação: [Link](https://app.diagrams.net/#G1xG0wn-335aLkGkoZim8h2Jea5SlqouF6)

A ideia é rodar esse processo 2x por semana, de maneira manual (analista precisa clicar num botão).


1. Configurar na planilha "Setup" quais imóveis serão precificados **manualmente** ou **automaticamente**

### Precificação manual

Frequência: é feita manualmente (por demanda) E todos os dias à meia-noite

### Precificação automática

Frequência: é feita manualmente quando o analista for executar o processo, que hoje é executado 2x na semana

DAG precificação automática: <https://app.diagrams.net/#G1xG0wn-335aLkGkoZim8h2Jea5SlqouF6>

Documentação das colunas da planilha de precificação automática:

## ABAS

## dashboard

## concorrentes(Preço e Ocupação)

### Date

Esta coluna deve trazer todas os dias no formato dd-mm-aaaa, no intervalo de dia_atual + 1 até dia atual +180 dias.

### percentile_(5 a 95)

O calculo de cada percentil, é feito em cima **dos preços de todos os concorrentes do imóvel para cada dia.** Cada coluna indica o percentil de preço caculado para o grupo de concorrentes com o valor do percentil, os percentis calculados são(5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 95).  OBS:. Diferente do desempenho, aqui é neceesario usar o filtro de strata.(região, bairro, tipo, numero de quartos e strata).

Os preços considerados dos concorrentes, serão apenas dos **imóveis não bloqueados**, ou seja, imóveis onde blocked é false OU que estão disponíveis. Exceção: Apesar de bloqueios com motivo 'dead' possuírem datas disponíveis, eles continuam sendo dropados.

```python
def calculate_percentiles(dataframe):
    # Convertendo as strings de data para o tipo datetime.date
    #dataframe['date'] = pd.to_datetime(dataframe['date'], format='%Y-%m-%d').dt.date
    dataframe= dataframe.loc[dataframe.blocked == False]
    # Definindo e calculando percentis
    percentiles = [0.05, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 0.95]  
    percentiles.sort()
    result = dataframe.groupby('date')['price'].quantile(percentiles).unstack()
    result.columns = [f'percentile_{int(p*100)}' for p in percentiles]
    
    return result
```

### %occupation

Para o calculo de ocupação, é **considerado todos os imóveis da região**, definidas pela planilha 'setup grupos' da pagina concorrentes.  Ex:. os imóveis JUR, serão levandos em conta os concorrentes  de FlorianópolisJurerê; Jurerê Internacional.

O caclulo é feito pegando a ocupação predita na BAO, sobre **o número de imóveis scrapados pela BAO que não estejam bloqueados,** ou seja, imóveis onde blocked é false OU que estão disponíveis. Exceção: Apesar de bloqueios com motivo 'dead' possuírem datas disponíveis, eles continuam sendo dropados.

```python
def calculate_occupation(dataframe):     
    occupied = dataframe[['date', 'airbnb_listing_id', 'occupied', 'blocked']]
    occupied['occupied'] = occupied['occupied'].replace({'true': '1', 'false': '0'}).astype(int)
    occupied = occupied.loc[occupied['blocked'] == False]
    occupied = occupied.groupby('date').agg({
        'occupied': lambda x: x.sum(),
        'airbnb_listing_id': 'nunique'
    }).reset_index()
    occupied.columns = ['date', 'occupation', 'active_listings']
    occupied['%occupation'] = ((occupied.occupation/occupied.active_listings).round(2)*100)   

    return occupied[['date', '%occupation', 'active_listings']]
```

### date_last_year

É considerado o mesmo intervalo do date, porém as datas referentes ao ano anterior. ( Verificar se ocorrera erro no ano bissexto ).

```python
def separeted_future_passad_region(select_id_category):
    competitors_region = filtered_competitors_region_parquet(select_id_category) 
    competitors_region = competitors_region.loc[competitors_region.blocked == False]
    competitors_region['date'] = pd.to_datetime(competitors_region['date'], format='%Y-%m-%d')
    # Df com datas futuras
    today_date =  datetime.now()
    competitors_future_dates = competitors_region[competitors_region['date'] > today_date]

    # DF com datas ano - 1
    initial_date = competitors_future_dates.date.min()
    end_date =  competitors_future_dates.date.max()
    start_date_last_year = initial_date - pd.DateOffset(years=1)
    end_date_last_year = end_date - pd.DateOffset(years=1)
    competitors_last_year_dates = competitors_region[(competitors_region['date'] >= 
                                                                start_date_last_year) & (competitors_region['date'] <= end_date_last_year)]
    
    return competitors_future_dates, competitors_last_year_dates
```

### %occ_last_year

Para o calculo de ocupação last year, é **considerado todos os imóveis da região**, definidas pela planilha 'setup grupos' da pagina concorrentes.  Ex:. os imóveis JUR, serão levados em conta os concorrentes  de Florianópolis Jurerê; Jurerê Internacional.

O caclulo é feito pegando a ocupação predita na BAO, sobre **o número de imóveis scrapados pela BAO que não estejam bloqueados,** ou seja, imóveis onde blocked é false OU que estão disponíveis. Exceção: Apesar de bloqueios com motivo 'dead' possuírem datas disponíveis, eles continuam sendo dropados\*\*. Neste caso levando em conta as datas definidas na coluna date_last_year.\*\*

### period

Nesta coluna são definidos os períodos quentes e frios, onde os **períodos frios estão representados pela numeração de 1 a 9** e os quentes pela **numeração de 11,19.**

Para facilitar o entendimento, será separado em etapas:


1. **Preparação dos DataFrame para geração dos períodos.**

   
   1. São usados os concorrentes de toda a região, ou seja o Dataframe de entrada **é o mesmo usado para gerar os cálculos de ocupação**. As colunas necessárias são ('airbnb_listing_id', 'date', 'available', 'blocked', 'occupied')

      ```python
      competitors_seazone_region = filtered_competitors_region_parquet(selected_seazone_category)
      df_periods_hz = competitors_seazone_region[['airbnb_listing_id', 'date', 'available', 'blocked', 'occupied']]
      ```
   2. Também como na ocupação são desconsiderados os dias bloqueados, e é feita o agrupamento por id para cada dia, com intervalo de **date_now + 1 até date_now +180.** Somando o total de ids 'ativos' em cada dia e o de ocupação. Lembrando que o conceito de ativos aqui são listings scrapados na BAO que não estão bloqueados.

      ```python
      df_warm_periods_hz = df_periods_hz[df_periods_hz['date'] >= datetime.now()]
      df_warm_periods_hz.loc[:, 'blocked'] = (df_warm_periods_hz['blocked'] == 'False')
      df_warm_periods_hz.loc[:, 'occupied'] = (df_warm_periods_hz['occupied'] == 'true').astype(int)
      df_warm_periods_hz = df_warm_periods_hz.groupby('date').agg({
           'occupied': lambda x: x.sum(),
            'airbnb_listing_id': 'nunique'
       }).reset_index()
       df_warm_periods_hz.columns = ['date', 'occupation', 'active_listings']
      ```
   3. São geradas as colunas: ''%occupation', '%occupation_mean_c', ''%occupation_std', '%occupation_mean_20', ''z_score''. Onde a **%occupation é a mesma usada no calculo da aba concorrentes** e as colunas com indices são ***mean_c( media central 7 períodos ), std( desvio padrão 7 períodos ), mean_20( media móvel simples 20 períodos ).*** *A coluna **z_score** é calculada **dividindo a diferença entre a ocupação percentual e a media central 7 períodos pelo desvio padrão de 7 períodos A seguir temos como foram feitos os cálculos em python.***

   ```python
   df['%occupation'] = ((df_warm_periods.occupation/df_warm_periods.active_listings).round(2)*100)
   df['%occupation_mean_c'] = df['%occupation'].rolling(window=7, center=True).mean()
   df['%occupation_std'] = df['%occupation'].rolling(window=7).std()
   df['%occupation_mean_20'] = df['%occupation'].rolling(window=12).mean()
   df['z_score'] = (df['%occupation'] - df['%occupation_mean_c']) / df['%occupation_std']
   ```
2. **Definição das regiões 'mornas'( warm_zones )**

   
   1. Aqui é realizada o primeiro filtro, para definirmos os períodos onde temos **destaques de demanda de ocupação usando o z_score**, chamamos ainda de períodos mornos.
   2. Para esta definição, é **verificado se o zscore calculado é positivo**, caso seja, esta data é definida como uma data pertencente ao período morno.
   3. Nesta etapa também é usado **a coluna '%occupation_mean_20',** indica se cada dia esta em **'tendência de alta',** para isto comparamos a coluna **'%occupation_mean_c'** que deve ser maior que a de 20. Na pratica indicamos que **a média móvel 7 período central deve ser maior que a de 20 períodos** para considerarmos o período como um período morno.

   ```python
   def calculate_warm_zone(df, z_score_column, warm_zone_column):
       group_detected = False
       group_start = None
       positive_count = 0
       warm_zone_indices = []  # Lista para armazenar os índices da zona quente
       min_potive_group = 2
       
       for idx, row in df.iterrows():
           if row[z_score_column] > 0:
               if not group_detected:
                   group_detected = True
                   group_start = idx
                   positive_count = 0
               positive_count += 1
           else:
               if positive_count >= min_potive_group:
                   warm_zone_indices.extend(range(group_start, idx))
               group_detected = False
               positive_count = 0
   
       # Defina a coluna warm_zone com base nos índices armazenados
       df[warm_zone_column] = False
       df.loc[warm_zone_indices, warm_zone_column] = True
       df[warm_zone_column]= np.where(df['%occupation_mean_20'] > df['%occupation_mean_c'], False, df[warm_zone_column] )
       return df
   ```
3. **Numerando os períodos e aplicando filtros para remoção de períodos mornos não significativos.**

   
   1. Inicialmente é dado uma **numeração para cada período**, onde damos **0 para períodos que não foram considerados até aqui mornos** estes consideramos **como um período frio únic**. Este pode não ter dada sequencial.
   2. É feito um **agrupamento pelo índice numerado definido**, calculando **a media e o desvio padrão de cada período numerado**, onde temos todos os períodos **que não são mornos, agrupados como um período frio.**
   3. É feito um filtro onde indicamos que se um **período possuir a média de ocupação menor do que a de um período frio** este deixa de ser um período morno e **passa a ser um período frio.**
   4. Um novo filtro é aplicado para **remover períodos mornos que não são significativamente diferentes dos períodos normais.** Para isso, calculamos a **mediana da média das ocupações de todos os períodos mornos e a mediana dos desvios padrões de todos os períodos mornos.** Um período morno é considerado não significativo se sua **ocupação for menor do que a mediana da média das ocupações de todos os períodos mornos menos a mediana dos desvios padrões de todos os períodos mornos.**

   ```
   def calculate_wam_zone_2(warm_zones):
           number_wz = number_zone(warm_zones, 'warm_zone')    
           number_wz = number_wz.groupby('number_wz').agg({
           '%occupation': ['mean', 'std']
           }).reset_index()
           number_wz.columns = ['number_wz', 'mean_occupation_wz', 'std_occupation_wz']
           warm_zones_numerate = warm_zones.merge(number_wz, on ='number_wz', how = 'left')
   
           # FIltros nas warm zones > media de ocupacao do perido cold e apos considerar warm_zones tudo que esta acima da media das warm_zones - std
           mean_occupation_cold = number_wz.loc[number_wz['number_wz'] == '0']['mean_occupation_wz'].iloc[0]
           warm_zones_numerate['warm_zone'] = np.where(warm_zones_numerate.mean_occupation_wz < mean_occupation_cold, False, warm_zones_numerate['warm_zone'] )
           mean_occupation_warm = number_wz.loc[number_wz['number_wz'] != '0']['mean_occupation_wz'].median()
           std_occupation_warm = number_wz.loc[number_wz['number_wz'] != '0']['std_occupation_wz'].median()
           warm_zones_numerate['warm_zone'] = np.where(warm_zones_numerate['%occupation'] >= (mean_occupation_warm - (std_occupation_warm)), True, warm_zones_numerate['warm_zone'])
   
           # Renumerar: 
           columns_to_remove = ['number_wz', 'mean_occupation_wz', 'std_occupation_wz']
           warm_zones_renumerate = warm_zones_numerate.copy()
           warm_zones_renumerate = warm_zones_renumerate.drop(columns=columns_to_remove)
           number_wz = number_zone(warm_zones_renumerate, 'warm_zone')    
           number_wz = number_wz.groupby('number_wz').agg({
           '%occupation': ['mean', 'std']
           }).reset_index()
           number_wz.columns = ['number_wz', 'mean_occupation_wz', 'std_occupation_wz']    
           warm_zones_renumerate = warm_zones_renumerate.merge(number_wz, on ='number_wz', how = 'left')
           return warm_zones_renumerate, number_wz
   ```
4. Definição dos períodos quentes

   
   1. Na primeira versão, definimos três categorias de períodos: frios, quentes e mornos. No entanto, decidimos eliminar os períodos mornos e **deixar apenas frios e quentes**. Para isso, aplicamos um **novo filtro nos períodos mornos,** removendo aqueles que não são significativamente diferentes dos períodos normais.
   2. Assim, consideramos os **períodos quentes os mornos que possuem média % de ocupação maior que a mediana da % de ocupação dos períodos mornos**, a baixo o código usada.

   ```python
   meadian_occupation_warm = number_wz.loc[number_wz['number_wz'] != '0']['mean_occupation_wz'].median()
   hot_zones['hot_zone'] = hot_zones['warm_zone']
   #Filtro para definir Hot Zones
   hot_zones['hot_zone'] = np.where(hot_zones.mean_occupation_wz < (meadian_occupation_warm  ), False, hot_zones['hot_zone']) 
   ```
5. Expandir e juntar os períodos quentes.

   
   1. Foi definido que os períodos quentes **não poderiam ter menos de 7 dias**, os períodos quentes formados com menos de 7 dias tiveram que ser expandidos, aqui é necessário **usar lógica para pegar as datas adjacentes a direita e a esquerda até o período estar com 7 ou mais dias**. OBS:. O código feito deixou a execução mais lenta por usar muito loop para respeitar esta regra, talvez aqui possamos usar uma lógica mais eficiente tentando eliminar a quantidade de loops, assim não vou usar o código usado como exemplo.
   2. Foi definido que **períodos quente próximos deveriam ser anexados entre si.** Para isso, usamos o critério de que **não pode haver um período frio com menos de 7 dias** entre dois períodos quentes. EX:. período 12: Do dia 12/01 até dia 20/01, período 2: do dia 21/01 até 23/01 e período 13: Do dia 24/01 até 13/02. Juntamos os 3 períodos e ficamos com o período 12: Do dia 12/01 até 13/02.

   ```python
   def convert_false_sequence(df):
           false_count = 0
           for i in range(1, len(df['hot_zone']) - 1):
               if df['hot_zone'][i] == False:
                   false_count += 1
               else:
                   if df['hot_zone'][i - false_count - 1] == True and false_count < 7:
                       for j in range(i - false_count, i):
                           df['hot_zone'][j] = True
                   false_count = 0
           return df
   ```

### num_active_competitors

São os imóveis que estão na bao e não possuem bloqueios. Ou seja são todos os imóveis que foram considerados para o calulo de ocupação.(Região).

OBS:. Talvez seja interessante trazer a informação de número de imóveis usados no calculo dos percentis e ocupação last year.

### num_competitors

São os imóveis que estão na BAO e não possuem bloqueios e são concorrentes o imóvel que esta sendo precificado.(cidade, bairro, tipo, numero de quartos, strata). Retorna o número de concorrentes em cada date.

## **seazone(Preços)**

### imóvel

Lista dos ids do imóvel que esta sendo precificado.

### date

Data today + 1 até today + 180 dias

### preço

Preço do imóvel sendo precificado, que é puxado da tabela real_seazone_data.daily_revenue coluna '**price_last_aquisition**' .

Houve uma mudança no dia 05-09-2023, agora esta coluna também **inclui os imóveis que ainda não foram precificados**, estes **devem retornar preço 0 até** terem sua primeira precificação.

No código a baixo as **alterações feitas no código** para cumprir esta nova regra de negócio, estão em negrito, onde foi criado um dataframe 'default_df', que antes de fazer o merge com o dataframe onde estão as informações de preço e ocupação, pega as datas dos mesmos, após o merge quando for nulo consideramos 0.

```python
def get_prices_seazone(selected_seazone_category):
    df_seazone_open_calendar = pd.read_parquet('data_imports/seazone_open_calendar.parquet')
    df_seazone_open_calendar = df_seazone_open_calendar.rename(columns={'listing':'id_seazone'})
    # Cria um DataFrame "padrão" com todos os IDs e datas
    **unique_dates = df_seazone_open_calendar['date'].drop_duplicates()
    default_df = selected_seazone_category.assign(key=1).merge(pd.DataFrame({'date': unique_dates, 'key': 1}), on='key').drop('key', axis=1)
    today_date = datetime.now()
    default_df['date']= pd.to_datetime(default_df['date'], format='%Y-%m-%d')
    default_df = default_df[default_df['date'] > today_date][['id_seazone', 'date']]**
    # Faz o merge com df_seazone_open_calendar
    df_seazone_open_calendar['date'] = pd.to_datetime(df_seazone_open_calendar['date'], format='%Y-%m-%d')
    seazone_oc_selected_id = default_df.merge(df_seazone_open_calendar, how='left', on=['id_seazone', 'date'])
    seazone_oc_selected_id = seazone_oc_selected_id[['id_seazone', 'date', 'price',	'occupied', 'blocked']]
    **# Substitui valores nulos por 0
    seazone_oc_selected_id[['price', 'occupied', 'blocked']] = seazone_oc_selected_id[['price', 'occupied', 'blocked']].fillna(0)**

    return seazone_oc_selected_id
```

### occ (1 ou 0)

É puxado da mesma tabela do athena, real_seazone_data.daily_revenue, da coluna 'occupancy'. Onde 1 é ocupado e 0 desocupado.

### block (1 ou 0)

É puxado da mesma tabela do athena, real_seazone_data.daily_revenue, da coluna 'blocked'. Onde 1 é ocupado e 0 desocupado.

## desempenho

### Período

Período calculado na coluna period. O período vai ser a granularidade minima desta tabela.

### Imóvel

Imóvel Seazone que esta sendo precificado **e os que terão sua primeira precificação.**

Aqui, assim como na aba de preços, **houve alterações para incluírem imóveis que não foram precificados.** Agora são imóveis sendo precificados e os que terão sua primeira precificação. Para incluir esta alteração a função que calcula o faturameto do imóvel teve alterações.

### Fat.Imóvel

É a soma do faturamento para aquele período. Esta soma é feita usando o preço da tabela real_seazone_data.daily_revenue da coluna **'price'** quando **occuped == True**

A baixo foi colocada a função completa que abrange as colunas que depois serão especificadas como a '%occup_5days' e '%occup_10days'.

Assim, nesta parte foi destacada além da parte onde calculamos a coluna fat.imovel,  **em negrito a parte modificada para incluir imóveis ainda não precificados,** aqui como na função preços, tivemos que incluir um DataFrame intermediário, que chamamos de 'default_df'.

```python
  def fat_seazone_periods(hot_zones_plot_spand):
    df_seazone_open_calendar = pd.read_parquet('data_imports/seazone_open_calendar.parquet')
    df_seazone_open_calendar = df_seazone_open_calendar.rename(columns={'listing':'id_seazone'})

    **unique_dates = df_seazone_open_calendar['date'].drop_duplicates()
    default_df = selected_seazone_category.assign(key=1).merge(pd.DataFrame({'date': unique_dates, 'key': 1}), on='key').drop('key', axis=1)
    today_date = datetime.now()
    default_df['date']= pd.to_datetime(default_df['date'], format='%Y-%m-%d')
    default_df = default_df[default_df['date'] > today_date][['id_seazone', 'date']]**

    df_seazone_open_calendar['date'] = pd.to_datetime(df_seazone_open_calendar['date'], format='%Y-%m-%d')
    seazone_oc_selected_id = default_df.merge(df_seazone_open_calendar, how='left', on = ['id_seazone', 'date']).fillna(0)
    **seazone_oc_selected_id['daily_fat'] = seazone_oc_selected_id.price_fat * seazone_oc_selected_id.occupied**
    seazone_oc_selected_id = seazone_oc_selected_id[['id_seazone', 'date', 'daily_fat', 'occupied',	'occup_5days',	'occup_10days']]
    hot_zones_plot_spand['date'] = pd.to_datetime(hot_zones_plot_spand['date'])
    seazone_fat_periods = seazone_oc_selected_id.merge(hot_zones_plot_spand, on = 'date')
    seazone_fat_periods = seazone_fat_periods[['period', 'id_seazone', 'daily_fat', 'occupied',	'occup_5days',	'occup_10days']]
    seazone_fat_periods = seazone_fat_periods.groupby(['period', 'id_seazone']).sum().reset_index()
    seazone_fat_periods['%occup_5days'] = np.where(seazone_fat_periods.daily_fat == 0, 0, 1 - seazone_fat_periods.occup_5days / seazone_fat_periods.occupied)
    seazone_fat_periods['%occup_10days'] = np.where(seazone_fat_periods.daily_fat == 0, 0, 1 - seazone_fat_periods.occup_10days / seazone_fat_periods.occupied)
    seazone_fat_periods = seazone_fat_periods[['period', 'id_seazone', 'daily_fat', '%occup_5days',	'%occup_10days' ]]    

    return seazone_fat_periods
```

### percentile_(50, 60, 75, 90 )

É calculado o percentil dos imóveis concorrentes( cidade, bairro, tipo, número de quartos) para cada período onde cada coluna representa um percentil(50, 60, 75 e 90 ).

```python
def calculate_fat_percentiles(dataframe, hot_zones_plot_spand):
    future_precentile = dataframe.copy()
    future_precentile['available'] = future_precentile['available'].astype(str).replace({'true': '1', 'false': '0'})
    future_precentile['daily_fat'] = np.where(future_precentile.available == '0', future_precentile.price, 0)
    
    competitors_fat_periods = future_precentile.merge(hot_zones_plot_spand, on = 'date')
    competitors_fat_periods = competitors_fat_periods[['airbnb_listing_id', 'daily_fat', 'period']]
    competitors_fat_periods = competitors_fat_periods.groupby(['airbnb_listing_id', 'period'])['daily_fat'].sum().reset_index()

    percentiles = [50, 60, 75, 90]
    result = []
    for period in competitors_fat_periods['period'].unique():
        period_data = competitors_fat_periods[competitors_fat_periods['period'] == period]
        percentiles_data = period_data['daily_fat'].quantile([p / 100 for p in percentiles]).values
        result.append([period] + percentiles_data.tolist())

    result_df = pd.DataFrame(result, columns=['period'] + [f'percentile_{p}' for p in percentiles])

    return result_d
```

### ganho_%_últ_5_dias

A diferença da ocupação do imóvel da seazone gerada no dia da analise de preços e deste mesmo imóvel a 5 dias atrás. Em cima desta diferença é calculado o ganho percentual de ocupação.

```python
seazone_fat_periods['%occup_5days'] = np.where(seazone_fat_periods.daily_fat == 0, 0, 1 - seazone_fat_periods.occup_5days / seazone_fat_periods.occupied)
    
```

```sql
query_seazone_open_calendar = f'''(
    SELECT 
    listing,
    date,
    "booked_on", 
    price_last_aquisition as price,
    price as price_fat,
    CASE WHEN blocked THEN 1 ELSE 0 END AS blocked,
    CASE WHEN occupied THEN 1 ELSE 0 END AS occupied,
    ***CASE WHEN occupied = TRUE AND DATE_DIFF('day', booked_on, current_date) > 5 THEN 1 ELSE 0 END AS occup_5days,
    CASE WHEN occupied = TRUE AND DATE_DIFF('day', booked_on, current_date) > 10 THEN 1 ELSE 0 END AS occup_10days***

    FROM 
        seazone_real_data.seazone_daily_revenue
    WHERE  
        date BETWEEN date_add('day', -360, current_date) AND date_add('day', 180, current_date)   
)'''
```

### ganho_%_últ_10_dias

A diferença da ocupação do imóvel da Seazone gerada no dia da analise de preços e deste mesmo imóvel a 10 dias atrás. Em cima desta diferença é calculado o ganho percentual de ocupação.

```python

    seazone_fat_periods['%occup_10days'] = np.where(seazone_fat_periods.daily_fat == 0, 0, 1 - seazone_fat_periods.occup_10days / seazone_fat_periods.occupied)
```

Exemplo planilha de precificação pré-envio da Stays:

| **listing** | **date** | **min_stay (tarifa)** | **price** | **bloqueio_checkin** | **bloqueio_checkout** |
|----|----|----|----|----|----|
| JBV108 | 02/08/2023 | 2 | 200 | False | False |
| JBV108 | 02/08/2023 | 7 | 160 | False | False |
| … | … | … | … | … | … |
| ILC2412 | 02/08/2023 | 2 | 350 | False | False |
| ILC2412 | 02/08/2023 | 7 | 280 | False | False |
|    |    |    |    |    |    |

### Onboarding

# Quais são as dependências?

Exceto pela Avaliação de Anúncios, todas as outras tasks principais dependem da seleção de concorrentes!

Para verificar isso de forma visual melhor fizemos um diagrama:


# Quais são os recursos que serão utilizados?

Tabelas do S3 que hoje estão no Lake do Pipe

Infrastructure as a code (IaC)

# Quais são os milestones e entregáveis?

Os entregáveis são as planilhas no Sheets funcionando, testadas e documentadas.

Quais dados foram utilizados (inputs do usuário, tabelas do S3 no Lake etc), qual o processamento feito em cima deles, onde o processamento é feito (Lambda, Glue etc) e quais resultados são salvos no S3 e/ou apresentados no Sheets.

# Quando deverão ser entregues (prazos)?

Temos um Gantt para acompanhar os diferentes módulos.

[Gantt Sirius 2.0](https://docs.google.com/spreadsheets/d/13bJW_B85LhzAJ2N0upvpPsAQbcMzn_tBtO4YBYtkqKc/edit?usp=drivesdk)

# Quem estará envolvido no projeto?

Pipe: Márcio Fazolin, Augusto Hideki, Francisco Burigo, Artur Brito, Nícolas Campana, André Padilha

RM: Gabriel Probst, Lucas Abel, Rodrigo Ribeiro, Júlio Monteiro

# Quais serão as responsabilidades de cada um?

Checar no Gantt. As pessoas que não aparecem no Gantt mas possuem responsabilidades são:

* André Padilha - gestão do projeto
* Nícolas Campana - liderança técnica
* Gabriel Probst - gestão do projeto e PO
* Bill - PO
* Burigo - auxiliar todos os outros Devs em todas as etapas de CI/CD, IaC

# Quem irá revisar e aceitar?

Probst e Bill