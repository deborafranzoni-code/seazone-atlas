<!-- title: Precificação | url: https://outline.seazone.com.br/doc/precificacao-3T2llaVJmf | area: Tecnologia -->

# Precificação

# Precificação heurística

As planilhas da precificação heurística se encontram em <https://drive.google.com/drive/u/2/folders/1hNHdvGakocHzPI_koTq7iaug3KvHXo0g>.

Esse tipo de precificação ocorrerá para todos os imóveis que na planilha de setup estão com a modalidade de precificação "Por Concorrente" desmarcada.

Ela utiliza regras de negócio conhecidas no mercado para aplicar descontos ou aumentar o preço dependendo da ocasião. As funcionalidades se encontram adiante:

1 - Preços Base - Períodos

* Essa página dirá ao Sirius qual o preço inicial do imóvel para cada período. Esse preço será transferido para uma granularidade diária para a aplicação das regras posteriores. A primeira data criada será sempre hoje e a última data virá da aba 'Janelas' da planilha de Setup. Caso um imóvel, no intervalo dentre hoje e a última data de 'Janelas', não possua preço em pelo menos 1 dia, ele irá ser descartado e não será precificado (até os outros dias com preço serão descartados).
* Essa aba também aceita um Grupo. Caso seja fornecido dois preços base para um imóvel no mesmo período (as vezes por permitir grupo isso pode acontecer, exemplo: preço base pro JBV108 e grupo JBV) o Sirius crasha e nenhum imóvel é precificado.

2 - Definição de Períodos

* Aqui são definidos quais dias compõe quais períodos da aba Preços Base - Períodos.
* Detalhes:
  * O nome do período pode ser qualquer string.
  * A data de FIM não cria preço, então no exemplo abaixo o período "Fevereiro" cria preços para os dias dentre 2024-02-01 e 2024-02-29.
  * Caso haja datas duplicadas (mais de um período tentando criar preço base para a mesma data), o Sirius não crasha, mas esses imóveis não serão precificados.

| Período | Início | **Fim** |
|----|----|----|
| 1 | 2024-01-01 | 2024-02-01 |
| Fevereiro | 2024-02-01 | 2024-03-01 |
| 3 | 2024-03-01 | 2024-04-01 |

3 - Preços Incremento - (período, dia de semana, antecedência)

* Essas regras aplicaram uma porcentagem em cima do preço das diárias do imóvel. Por serem porcentagem, a ordem de aplicação não importa, então se o preço base em um mês for 200 e houver duas regras de -5% e -10%, o preço final será 200*0.95*0.90 == 200*0.90*0.95 == 171. Isso se aplica tanto para regras em páginas diferentes como para regras na mesma página.
* Para regras de período, o dia do FIM não aplica mudança de preço. Exemplo: Se uma regra do dia 1 ao 10 fala pra ter redução de preço em 10%, o dia 10 NÃO terá seu preço reduzido, apenas os dias entre 1 e 9.

Depois de aplicadas as regras da heurística, [todas as regras da Planilha de Setup](/doc/precificacao-XIV8Y9Mul6) são aplicadas para depois serem enviadas a Stays.

### Infraestrutura

A aplicação das regras da precificação heurística acontece através do step function mostrado abaixo:

 ![Untitled](Precificac%CC%A7a%CC%83o%20846cc170fb3a443a9f1f7dfe405916f2/Untitled.png)

Existe um lambda que irá processar todas as regras de heurística, na ordem e lógica comentada acima, para depois salvar o resultado em uma tabela no path "bucketpricing/heuristic/". O path do parquet será enviado para um SQS que ativa o Lambda das [Regras do Setup](/doc/precificacao-XIV8Y9Mul6), sendo que junto do path também é enviado a origem da mensagem, no caso da heurística a origem é '"heuristic", mas no caso da precificação por concorrente a origem é o nome do operador (exemplo: "m.fazolin"). Se o lambda de heurística não falhar, também será enviado uma mensagem para uma fila com o status da execução da heurística.

Essa segunda fila é utilizada para retornar o status da execução para a Planilha da heurística, fornecendo um retorno visual para o analista. A recuperação dessa informação é feita através de um loop de "get" requests no AppScript no endpoint [pricing/heuristic/apply-pricing](/doc/comunicacao-e-dados-aWFByTFvPo). Se acontecer muitas iterações, ou seja, demorar por exemplo 10 minutos, quer dizer que um erro aconteceu e a planilha retornará um erro. Além disso, caso aconteça algum erro no StepFunction, o erro é capturado e enviado para o bloco "PassSNS" ou "PassSNS2" que avisa sobre o problema em um canal do Slack.

**Trigger:** O StepFunction tem seu Arn no parameter store e o método POST no endpoint da API criada no repositorio api-stays [pricing/heuristic/apply-pricing](/doc/comunicacao-e-dados-aWFByTFvPo) ativará o StepFunction.

# Precedência de Aplicação das Regras da Planilha de Setup

As regra de setup são aquelas que todos os imóveis possuem, independente se a precificação é por concorrentes, heurística ou direta.

É muito comum que haja sobreposição de condições no Sirius quanto a um imóvel em uma determinada data. Essa sobreposição pode ocorrer com praticamente qualquer regra, sejam regras de preços, estadia ou condições de desconto por duração de estadia (todas essas regras estão definidas na Planilha de Setup do Sirius).

Ex.: Pode ser que haja um preço mínimo de R$150 para a categoria CANSUP1Q e R$180 para o imóvel TPS212, que pertence a essa categoria, em uma mesma data. Que decisão o algoritmo de formação de preços toma?

A seguir são destacadas as regras em que essas sobreposições podem ocorrer, assim como a ordem em que as condições são consideradas e outros detalhes importantes referentes a cada regra:

1 - **Min. Stay (definido por mês, dia da semana ou período)**

* Independentemente do método usado para calcular o Mín Stay do imóvel em um determinado dia, prevalece sempre **o maior valor registrado** para aquele imóvel naquele dia.
* Para regras de período, o dia do FIM não aplica valores de estadia mínima. Exemplo: Se uma regra do dia 1 ao 10 fala pra ter estadia mínima 5, o dia 10 NÃO terá estadia mínima 5, apenas os dias entre 1 e 9.

2- **Min Stay - Gapper**

* O gapper é uma exceção das regras de estadia mínima acima. O objetivo é, quando detectar um gap, diminuir o número da estadia mínima para o valor fornecido na regra do gapper.
* Lógica: Através da daily_revenue, contar datas indisponíveis seguidas, o número de datas seguidas indisponíveis é o tamanho do gap. Caso a estadia mínima numa data seja maior ou igual ao tamanho do gap, essa data se enquadra nas condições de aplicação da regra, então o valor final da estadia mínima será **reduzido** para o valor do gapper (se o valor do gapper for maior que o da estadia mínima, nada acontece, visto que não daria para reduzir).

3 - **Desconto - Stay**

* Considerando um mesmo imóvel em um mesmo dia em uma mesma condição de tamanho de estadia, caso haja sobreposição de descontos diferentes, **prevalece aquele que for menor em módulo** (ex.: o desconto de -10% prevalece sobre o desconto de -15%)
* Considerando um mesmo imóvel em uma mesma data com regras para tamanhos de estadia diferentes, caso haja um desconto maior (em módulo) para uma condição de estadia menor, **esse desconto prevalece sobre o desconto do tamanho de estadia menor** (ex.: considere um imóvel-data com alteração de preço de -15% para estadias ≥ 7 dias e -10% para estadias ≥ 15 dias. No fim das contas, o desconto para estadias ≥ 7 dias será de -15% e o desconto para estadias ≥ 15 dias também será de -15%, ignorando-se aqui o desconto de -10%. O percentual de desconto - em módulo - deve sempre crescer ou se manter igual com o tamanho da estadia. Por esse motivo que essa regra ocorre no caso dessa sobreposição de condições).
* Se depois de aplicado essas regras, aconteça de existir um tamanho da tarifa (tamanho da estadia) para o desconto menor ou igual a estadia mínima definida em ["Min. Stay"](/doc/precificacao-XIV8Y9Mul6), então esse desconto para essa tarifa deverá ser desconsiderado. Qualquer outra tarifa para essa mesma data que seja maior que a estadia mínima definida em  mantem-se aplicando o desconto.
* A data do FIM não aplica valores de desconto. Exemplo: Se uma regra do dia 1 ao 10 fala pra ter desconto de 15% na tarifa 15, o dia 10 NÃO terá esse desconto pra essa tarifa, apenas os dias entre 1 e 9.

<aside> 💡 **Muito importante: As regras de estadia mínima, bem como as regras de preços mínimos e fixos devem sempre prevalecer sobre as estadias mínimas (tarifas) e preços com desconto gerados pela regra de desconto Stay.**

</aside>

4 - **Preços Especiais (Mínimo, Máximo ou Fixo)**

* Preço Mínimo **Maior** prevalece sobre Preço **Menor**
* Preço Fixo **Maior** prevalece sobre Preço Fixo **Menor**
* Preço Máximo **Menor** prevalece sobre Preço Máximo **Maior**
* Preço Mínimo prevalece sobre Preço Fixo **e** sobre Preço Máximo (caso esse preço mínimo seja maior)
* Preço Fixo prevalece sobre Preço Máximo (caso esse preço fixo seja maior)
* A data do FIM não aplica valores de desconto. Exemplo: Se uma regra do dia 1 ao 10 fala pra ter desconto de 15% na tarifa 15, o dia 10 NÃO terá esse desconto pra essa tarifa, apenas os dias entre 1 e 9.

5 - **Demais regras**

* Em todas as outras regras, caso haja sobreposição de condições, o Sirius não roda e o usuário é alertado sobre a sua quebra. Exemplo de condição que faz o Sirius quebrar: duas regras de bloqueio para um mesmo imóvel em uma mesma data, sendo que uma marca "Sim" para check-in e a outra marca "Não" para check-in.

### Infraestrutura

**LambdaPricingApplySetupRules**

A aplicação das regras de Setup consiste em apenas um lambda. Esse lambda é disparado sempre que houver uma mensagem no SQS "**SQSQueuePricingApplySetupRules".**  Na mensagem é esperado dois campos, um de "path" e outro de "origin".

 ![Untitled](Precificac%CC%A7a%CC%83o%20846cc170fb3a443a9f1f7dfe405916f2/Untitled%201.png)

O campo "**path**" pode ser uma string ou lista de strings. Cada string é um path de um parquet, sendo que é esperado que esse parquet possua 3 colunas, "price" (float ou int), "date" (se date for string é necessário que esteja no formato YYYY-mm-dd, ela também pode ser datetime) e "id_seazone" ou "listing" (um ou o outro, é esperado uma string).

O campo "**origin**" é para diferenciar a origem dessa precificação. Caso a origem for a Precificação Heurística, é esperado que o campo seja preenchido com "heuristic". Caso a origem seja Precificação por Concorrentes, é esperado que o campo seja o nome do analista. Esse campo é usado apenas para manter controle e termos um histórico de que mudanças foram feitas e por quem.

Caso **"origin" seja igual "last_offered_raw_price", o campo path não é necessário.** Esse evento implica que está sendo aplicado uma regra de **gap**, então o script puxa os últimos preços ofertados na tabela **last_offered_raw_price** para os reaplicarem. Neste casto, o script faz um merge com a setup_groups para garantir que apenas imóveis sendo precificados hoje estão sendo reaplicados. O campo "origin" do dataframe da tabela last_offered_raw_price é mantido, então se está rodando regra de gap em cima de um preço com origem 'heuristic', a origem 'heuristic' é mantido.

Depois de lido, o dataframe de preço (resultante do "path" ou do "last_offered_raw_price") é realizado um **append na tabela "s3://bucketpricing}/raw_price_temp/"** com o dataframe.

será usado como base para aplicação das regras de Setup, segundo o roteiro de precendências descrito acima.

O output do script é um append na tabela "bucketpricing/price_before_stays_temp/". O intuito da tabela é salvarmos as precificações para depois construírmos um histórico. O path do parquet gerado é enviado para uma fila que ativará o envio dos preços para a Stays [(PatchPrices)](/doc/comunicacao-e-dados-aWFByTFvPo).

Além disso, o Lambda também levanta alguns **erros**. Caso haja imóveis com um ou mais dias sem estadia mínima, mesmo depois de passarem por todas as regras de estadia mínima, é levantado um erro. Caso haja regras de bloqueio que apontem para um imóvel numa mesma data bloquear e não bloquear o checkin/out também é levantado um erro. Esses dois tipos de erro vão parar o processo de precificação e nenhum imóvel será precificado.

**LambdaConsolidação**

Esse lambda ainda não foi implementado, mas o objetivo dele é consolidar numa tabela histórica particionada por aquisição os multiplos parquets que serão salvos na tabela bucketpricing/price_before_stays_temp/.

Depois ele irá deletar os arquivos temporários para futuramente, quando o script rodar de novo, não adicionar arquivos duplicados na tabela histórica.

# Precificação por concorrentes

A precificação por concorrentes precisa abastecer diversas abas em Planilha. [Link das Planilhas](https://drive.google.com/drive/u/2/folders/1QxkhI0aUyEYyTqzTmsT2fUx_Rrq4vaSr). Como são várias informações diferentes, é necessário calcula-las a priori para o analista apenas ler o resultado final, reduzindo bastante o tempo de processamento para atualizar as páginas em Planilha.

As informações necessárias são:

## ABAS

### concorrentes(Preço e Ocupação)

### Date

Esta coluna traz todas os dias no formato dd-mm-aaaa, no intervalo de dia_atual + 1 até dia atual +180 dias.

### percentile_(5 a 95)

O calculo de cada percentil, é feito em cima **dos preços de todos os concorrentes do imóvel para cada dia.** Cada coluna indica o percentil de preço caculado para o grupo de concorrentes com o valor do percentil, os percentis calculados são(5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 95).  OBS:. Os concorrentes utilizados são os competitors_general (filtro em cidade, bairro, tipo, numero de quartos e strata).

Os preços considerados dos concorrentes serão apenas dos **imóveis não bloqueados**, ou seja, imóveis onde blocked é false OU que estão disponíveis. Exceção: Apesar de bloqueios com motivo 'dead' possuírem datas disponíveis, eles continuam sendo dropados pois implicam que o imóvel já está inativo.

### %occupation

Para o calculo de ocupação, é **considerado todos os imóveis da região**, definidas pela planilha 'setup grupos' da pagina concorrentes, ou seja, serão os competitors_region (filtro em cidade e bairro).

O caclulo é feito pegando a ocupação predita na BAO, sobre **o número de imóveis scrapados pela BAO que não estejam bloqueados,** ou seja, imóveis onde blocked é false OU que estão disponíveis. Exceção: Apesar de bloqueios com motivo 'dead' possuírem datas disponíveis, eles continuam sendo dropados.

### date_last_year

É considerado o mesmo intervalo do date, porém as datas referentes ao ano anterior. Se for ano bissexto então será considerado o dia 28/02.

### %occ_last_year

Para o calculo de %occ_last_year, é **considerado todos os imóveis da região**, definidas pela planilha 'setup grupos' da pagina concorrentes, ou seja, serão os competitors_region (filtro em cidade e bairro).

O caclulo é feito pegando a ocupação predita na BAO para as date_last_year, sobre **o número de imóveis scrapados pela BAO que não estejam bloqueados,** ou seja, imóveis onde blocked é false OU que estão disponíveis. Exceção: Apesar de bloqueios com motivo 'dead' possuírem datas disponíveis, eles continuam sendo dropados.

### num_active_competitors

São os imóveis que estão na bao e não possuem bloqueios. Ou seja são todos os imóveis que foram considerados para o calulo de ocupação.(Região).

### num_listings_percentiles

É o número de concorrentes sendo utilizados para a precificação (cidade, bairro, tipo, numero de quartos, strata).

### period

Nesta coluna são definidos os períodos quentes e frios, onde os **períodos frios estão representados pela numeração de 1 a 9** e os quentes pela **numeração de 11,19.**

Para facilitar o entendimento, será separado em etapas:


1. **Preparação dos DataFrame para geração dos períodos.**

   
   1. São usados os concorrentes de toda a região, ou seja, os **mesmos concorrentes usados para gerar os cálculos de ocupação**. As colunas necessárias são 'date', 'occupied' e 'num_active_competitors', onde 'occupied' pode é o número de concorrentes ocupados para aquela data. Aqui também são desconsiderados os casos onde blocked é false OU que estão disponíveis. Exceção: Apesar de bloqueios com motivo 'dead' possuírem datas disponíveis, eles continuam sendo dropados..
   2. São geradas as colunas: ''%occupation', '%occupation_mean_c', ''%occupation_std', '%occupation_mean_20', ''z_score''. Onde a **%occupation é a mesma usada no calculo da aba concorrentes** e as colunas com indices são ***mean_c( media central 7 períodos ), std( desvio padrão 7 períodos ), mean_20( media móvel simples 20 períodos ).*** *A coluna **z_score** é calculada **dividindo a diferença entre a ocupação percentual e a media central 7 períodos pelo desvio padrão de 7 períodos A seguir temos como foram feitos os cálculos em python.***

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

### **ImóveisOperador**

### **Imóveis**

Lista de imóveis que o operador da Planilha deve precificar. Essa lista será todos os imóveis que na planilha de setup estão com a modalidade de precificação "Por Concorrente" marcada e que o nome do operador é o da planilha.

### **seazone(Preços)**

### imóvel

É o id_seazone do imóvel sendo precificado.

### date

Data today + 1 até today + 180 dias, é a mesma data da aba concorrentes(Preço e Ocupação).

### preço

Preço do imóvel sendo precificado, que é puxado da tabela real_seazone_data.daily_revenue coluna '**price_last_aquisition**'. Esse é o preço que **vai pra Stays.**

Essa coluna também **inclui os imóveis que ainda não foram precificados**, estes **devem retornar preço 0 até** terem sua primeira precificação.

No código a baixo as **alterações feitas no código** para cumprir esta nova regra de negócio, estão em negrito, onde foi criado um dataframe 'default_df', que antes de fazer o merge com o dataframe onde estão as informações de preço e ocupação, pega as datas dos mesmos, após o merge quando for nulo consideramos 0.

### occ (1 ou 0)

É puxado da mesma tabela do athena, real_seazone_data.daily_revenue, da coluna 'occupancy'. Onde 1 é ocupado e 0 desocupado.

Essa coluna também **inclui os imóveis que ainda não foram precificados**, estes **devem retornar preço 0 até** terem sua primeira precificação.

### block (1 ou 0)

É puxado da mesma tabela do athena, real_seazone_data.daily_revenue, da coluna 'blocked'. Onde 1 é ocupado e 0 desocupado.

Essa coluna também **inclui os imóveis que ainda não foram precificados**, estes **devem retornar preço 0 até** terem sua primeira precificação.

### desempenho

### Período

Período calculado na coluna period. O período vai ser a granularidade minima desta tabela.

### Imóvel

Imóvel Seazone que esta sendo precificado, **até mesmo** **os que terão sua primeira precificação.**

### Fat.Imóvel

É a soma do faturamento para aquele período. Esta soma é feita usando o preço da tabela real_seazone_data.daily_revenue da coluna **'price'** quando **occuped == True**

Caso seja a primeira precificação do imóvel, então é necessário retornar 0.

### percentile_(50, 60, 75, 90 )

É calculado o percentil de faturamento dos imóveis concorrentes para cada período onde cada coluna representa um percentil(50, 60, 75 e 90 ). Aqui são considerados os competitors_all_strata (filtro em cidade, bairro, tipo, número de quartos) .

### ganho_%_últ_5_dias

A diferença da ocupação do imóvel da seazone gerada no dia da analise de preços e deste mesmo imóvel a 5 dias atrás.

Para obter esse valor, durante a leitura da tabela real_seazone_data.daily_revenue, também é gerado uma coluna 'occup_5days'. Ela vale 1 ou 0 dependendo se a data passou a ser ocupada antes de 5 dias atrás ou não. Depois, esse dado é multiplicado pelo faturamento e a query retorna a coluna fat_5days.

'ganho_%_últ_5_dias'  = 'fat_5days'/'fat'.

### ganho_%_últ_10_dias

A diferença da ocupação do imóvel da seazone gerada no dia da analise de preços e deste mesmo imóvel a 10 dias atrás.

Para obter esse valor, durante a leitura da tabela real_seazone_data.daily_revenue, também é gerado uma coluna 'occup_10days'. Ela vale 1 ou 0 dependendo se a data passou a ser ocupada antes de 5 dias atrás ou não. Depois, esse dado é multiplicado pelo faturamento e a query retorna a coluna fat_10days.

'ganho_%_últ_10_dias'  = 'fat_10days'/'fat'.

## Infraestrutura

### **StepFunctionFetchPricing**

Existe o StepFunction '**StepFunctionFetchPricing'** que irá calcular todos os dados usados para abastacer as páginas acima. Se em qualquer etapa acontecer um erro o próximo estado será 'PassSNS', no futuro esse será o sistema de alertas.

 ![Untitled](Precificac%CC%A7a%CC%83o%20846cc170fb3a443a9f1f7dfe405916f2/Untitled%202.png)

**Trigger:** O StepFunctionFetchPricing possuí trigger diário às 7h15. Existem planos para existir um botão de ativação manual, visto que se um imóvel novo entrar que precise ser precificado os analistas precisam esperar até "amanhã" pra conseguir precifica-lo.

### LambdaPricingFetchPriceAndOccupancy

Esse lambda irá juntar todas as informações referentes a preço e ocupação dos concorrentes, ou seja, ele gera os dados das abas **concorrentes(Preço e Ocupação).**

Como os dados dos concorrentes vêm da BAO, as queries realizadas no Athena para ler os dados referentes aos concorrentes de um imóvel e aos de todos os imóveis custarão o mesmo, visto que os dados escaneados dependem da partição 'date' e as partições lidas são iguais. Por esse motivo, as queries desse lambda SEMPRE irão calcular os dados de todos os imóveis ao mesmo tempo. O ponto negativo é que elas acabam demorando um pouco mais.

O Lambda vai fazer um join entre os competitors_region e a BAO para pegar a ocupação dos próximos 180 dias e também das datas do último ano. Depois, ele faz uma segunda query na BAO para pegar o percentil de preço, então aqui é feito um join com competitors_general. Por último, é calculado os periodos.

O lambda escreve o resultado final na tabela bucketpricing/price_and_occupancy. Essa é apenas uma tabela intermediária para o StepFunction comuniar as saídas de cada estado.

### LambdaPricingStartPerformanceAnalysis

Esse lambda é muito simples, ele vai apenas ler os períodos únicos gerados anteriormente para começar a analise de desempenho. Ele retorna esses periodos únicos. Essa analise será usada para preencher a aba **desempenho.**

### LambdaPerformanceGetQuantiles

Esse é o lambda que calcula a analise de desempenho. Ele recebe de parametros uma data inicial, final e uma lista de percentils para calcular. A lista nesse caso será \[0.5, 0.6, 0.75, 0.9\] e ela está hardcoded no StepFunction.

Esse lambda é ativado através de uma função MAP, onde cada uma das lambdas são acionadas com um dos períodos únicos definidos no **LambdaPricingStartPerformanceAnalysis**.

Esse lambda também precisa fazer uma query na BAO para pegar o faturamento dos concorrentes, fazendo um join com a competitors_all_strata. Detalhe: Ele sempre calcula os quantils de todos concorrentes de todos os imóveis da Seazone, mas no contexto de precificação, apenas alguns imóveis realmente vão possuír aquele período. Entretanto, isso não é necessariamente um problema, visto que os dados escaneados no Athena são os mesmos pra 1 ou todos os imóveis, então por simplificação sempre calculamos para todos os imóveis.

No final o lambda irá escrever os resultados na tabela bucketperformanceanalysis/performance_quantiles_temp e retornar o path escrito. Essa é apenas uma tabela temporária para guardar a informação entre os estados do StepFunction.

**Detalhe:** Hoje irão existir cerca de 130 períodos únicos, então esse lambda irá ser disparado 130 vezes, o que não é o ideal.

### LambdaPricingFinishPerformanceAnalysis

Esse lambda vai pegar o resultado da função **MAP do LambdaPerformanceGetQuantiles**, vai reler o resultado de **LambdaPricingFetchPriceAndOccupancy** para pegar a relação entre os períodos e imóveis e juntar tudo. Depois ele também vai gerar as colunas faltantes para preencher a aba **desempenho**, como ganho_%*últ_5_dias e ganho*%_últ_10_dias.

O resultado será salvo na tabela bucketpricing/performance_analysis_pricing. Dentro dela existe a partição 'state'.

Dentro de 'state=historic', haverá outra partição em 'acquisition_date' e serão salvos parquets para mantermos o historico de dados.

Dentro de 'state=current', haverá outra partição em 'listing', onde cada um é o id_seazone. Aqui os arquivos também serão salvos em json. O motivo dessa partição e deles serem salvos em json é porque isso facilitará depois na hora da planilha ler os resultados, visto que a precificação é sempre feita por imóvel e o arquivo json é mais fácil de converter no AppScript.

### LambdaPricingPreparePartitions

Esse lambda vai pegar o resultado de **LambdaPricingFetchPriceAndOccupancy** e irá junta-lo com as informações de preço e ocupação dos imóveis da Seazone, sendo que essas informações da Seazone vão abastecer a página **seazone(Preços)**. Por enqaunto essas informações vêm da tabela seazone_real_data.seazone_daily_revenue.

O resultado será salvo na tabela bucketpricing/partitioned_price_and_occupancy. Dentro dela existe a partição 'state'.

Dentro de 'state=historic', haverá outra partição em 'acquisition_date' e serão salvos parquets para mantermos o historico de dados.

Dentro de 'state=current', haverá outra partição em 'listing', onde cada um é o id_seazone. Aqui os arquivos também serão salvos em json. O motivo dessa partição e deles serem salvos em json é porque isso facilitará depois na hora da planilha ler os resultados, visto que a precificação é sempre feita por imóvel e o arquivo json é mais fácil de converter no AppScript.

Detalhe: Percebe-se que os dados que irão para a página **concorrentes(Preço e Ocupação)** e **seazone(Preços)** são salvos juntos, isso é feito porque as duas possuem granularidade listing e date, então elas podem ficar juntas através de um join e isso depois aceleraria o processo do AppScript lêr os dados, pois só teria que realizar 1 request em vez de 2.

## Botões na Planilha

Hoje a planilha possuí três botões.

### Começar Precificação

Esse botão vai apenas ativar o endpoint da API [price/competitors-by-user](/doc/comunicacao-e-dados-aWFByTFvPo). Ele retorna a lista de imóveis do operador da Planilha que estão configurados com precificação "Por Concorrente" na planilha de Setup.

### Executar

Esse botão irá ativar o endpoint [price/generate-url](/doc/comunicacao-e-dados-aWFByTFvPo). Esse request pega o nome do imóvel sendo precificado e envia como argumento. A API dispara um lambda que lê a partição "state=current" e "listing=imóvel_sendo_precificado" das tabelas **partitioned_price_and_occupancy** e **performance_analysis_pricing** do **bucketpricing.**

Depois, ele gera 2 links para o AppScript baixar em 2 futuros requests. O AppScript irá então atualizar os dados da Planilha com o novo imóvel.

### Enviar Imóvel pra Stays

Depois do analista alterar os preços do imóvel, ele pode apetar esse botão para enviar os preços pra Stays. Isso ativará o endpoint [price/period-price-modifier](/doc/comunicacao-e-dados-aWFByTFvPo) que por sua vez ativará o lambda **LambdaPeriodPriceModifier**.

O papel desse lambda é salvar o histórico dos preços na tabela period_price_modifier, mas também ele envia uma mensgem para a fila **SQSQueuePricingApplySetupRules,** que ativa a aplicação das regras da planilha Setup através do Lambda [\*\*LambdaPricingApplySetupRules](/doc/precificacao-XIV8Y9Mul6).\*\* Lembrando que **depois da aplicação dessas regras o preço** **vai direto pra Stays**.

# Precificação direta

A precificação direta é realizada através da [Planilha de Precificação Direta](https://docs.google.com/spreadsheets/d/1b5_dOnaIqLBOKe6GOITSyIq8AJ2dnrA3qynBR-E3oRc/edit#gid=0). Nela, o analista pode simplesmente inputar o preço desejado para cada **dia** para acelerar o processo de precificação, sem precisar se preocupar com criação de regras para a heurística ou analisar os competidores na precificação por concorrentes.

Apesar do analista não precisar definir concorrentes ou uma modalidade de precificação para os imóveis precificados nesse módulo, as regras da planilha Setup continuam sendo aplicadas e precisam ser atualizadas conforme a necessidade.

## Aba **Preços**

A aba preços consegue precificar imóveis individualmente.

**Trazer Grupo/Imóvel**

Esse botão da Planilha irá ler o grupo/imóvel inserido pelo analista e trará todos os imóveis com esse nome ou grupo da aba Grupos da Planilha Setup. Além disso, ele também traz o último preço ofertado (tabela last_offered_price) dentre hoje e o número de dias da "Janela de dias" para auxiliar o analista. Caso o imóvel nunca tenha sido precificado no Sirius 2.0 ele traz um valor nulo.

**Enviar Preços**

Esse botão irá pegar todos os preços inseridos pelo analista e enviará para a aplicação das regras da Planilha de Setup para depois serem enviados para a Stays. Caso uma linha possua preço nulo ela será **ignorada** e esse dia não será precificado.

## Infraestrutura

A Infraestrutura se divide em duas partes. O lambda que traz os dados pra Planilha e o Lamda que envia os dados pra fila **SQSQueuePricingApplySetupRules.** Os dois se encontram no repositório api-stays e são trigados por endpoint na API.

O endopint [pricing/direct/bring-data](/doc/comunicacao-e-dados-aWFByTFvPo) dispara o processamento do botão **Trazer Grupo/Imóvel.** Ele recebe de parâmetro o valor da celula "Grupo/Imóvel" e "Janela de Tempo".

O endopint [pricing/direct/send-data](/doc/comunicacao-e-dados-aWFByTFvPo) dispara o processamento do botão **Enviar Preços.** No final, o lambda salva os preços no s3 bucketsheetscommunication/outputs/direct_pricing/ particionado pelo timestamp e envia uma mensagem pra fila **SQSQueuePricingApplySetupRules** que é o trigger do Lambda [\*\*LambdaPricingApplySetupRules](/doc/precificacao-XIV8Y9Mul6).\*\* A mensagem contem o path do parquet salvo no s3 e o valor 'direct' no campo 'origin' pra mantermos controle de onde o preço veio.

## Aba **Preços Categoria**

Essa aba precifica imóveis por categoria.

**Trazer Grupo**

Esse botão da Planilha irá apenas limpar e gerar novas datas para serem preenchidas dentre hoje e o número de dias da "Janela de dias".

**Enviar Preços**

Esse botão irá pegar todos os preços inseridos pelo analista e enviará para a aplicação das regras da Planilha de Setup para depois serem enviados para a Stays. Será precificado com o mesmo preço todos os imóveis presentes no campo "Grupo", sendo que neste campo é esperado um dos grupos da aba Grupos da Planilha Setup. Caso uma linha possua preço nulo ela será **ignorada** e esse dia não será precificado. Caso um grupo não exista a planilha retornará erro.

## Infraestrutura

A Infraestrutura é apenas o Lamda que envia os dados pra fila **SQSQueuePricingApplySetupRules.** Ele se encontra no repositório api-stays e são trigados por endpoint na API.

O endopint [pricing/direct/send_category_data](/doc/comunicacao-e-dados-aWFByTFvPo) dispara o processamento do botão **Enviar Preços.** No final, o lambda salva os preços no s3 bucketsheetscommunication/outputs/direct_pricing_category/ particionado pelo timestamp e envia uma mensagem pra fila **SQSQueuePricingApplySetupRules** que é o trigger do Lambda [\*\*LambdaPricingApplySetupRules](/doc/precificacao-XIV8Y9Mul6).\*\* A mensagem contem o path do parquet salvo no s3 e o valor 'direct_category' no campo 'origin' pra mantermos controle de onde o preço veio.

## Planilha da Madego

Também foi criado uma planilha da Madego. Ela possuí as mesmas informações da da [Aba Preços](/doc/precificacao-XIV8Y9Mul6), mas a diferença é que ela só funciona para o grupo "CENTRO-OESTE", que são os imóveis da Madego.

# Tabelas de Preço

As tabelas de preço ([https://www.notion.so/Tabelas-Athena-c114c4f9ef604d00bdd3567fd2541fde?pvs=4#e965c90692da4a7999bd78ae536aff21](/doc/tabelas-athena-Z3CWJyDwVO)), são geradas todas dentro dos StepFunctions **StepFunctionConsolidatePrices** e **StepFunctionConsolidateRawPrices.** Os dois StepFunctions são criados com o mesmo objetivo, de gerar uma tabela com o último preço ofertado para cada data e o de gerar uma tabela historica com todos os preços gerados pelo Sirius. A diferença é que um são os preços depois da aplicação das regras da planilha de setup e outro são os preços antes.

**Por que usar os StepFunctions?**

O Lambda apply_setup_rules salva os preços calculados em uma tabela temporaria para depois o script que envia para Stays ler do parquet.

**Problemas:**

* O lambda apply_setup_rules não pode também salvar esses preços numa tabela histórica, pois é importante que essa tabela seja usada no Athena. Se toda vez que a precificação for utilizada for gerado um parquet novo, haveriam muitos parquets pequenos na tabela histórica do Athena prejudicando as queries.
* Existem várias partes do Sirius que precisam de apenas o último preço ofertado para cada diária. Esse tipo de update é fácil fazer em bancos de dados relacionais com o comando UPDATE, mas em parquet é díficil.

**Solução Proposta: StepFunctionConsolidatePrices** e **StepFunctionConsolidateRawPrices.**

Eles são equivalente, sendo que a única diferença notável é o nome das tabelas que eles criam. O esquema abaixo mostra o digrama:

 ![Untitled](Precificac%CC%A7a%CC%83o%20846cc170fb3a443a9f1f7dfe405916f2/Untitled%203.png)


1. O StepFunction verifica se existe a tabela temporaria price_before_stays_temp. Caso não exista, ele roda um crawler que a cria (a primeira vez que o stepfunction rodar a tabela não existe, por isso há essa verificação).
2. Dispara o lambda de consolidação. Esse lambda roda apenas uma vez por dia e lê TODOS os parquets da tabela temporaria e os adiciona nas tabelas de historicas e de último preço ofertado. Depois, o lambda **deleta todos** os parquets da tabela temporária.

   
   1. Para criar a tabela historical_last_offered_price, o lambda lê o conteúdo dela, lê o conteúdo novo da tabela temporaria e junta os dois mantendo a última aquisição para cada data.
   2. Para criar a tabela historical_prices, o lambda apenas da um append na tabela historica e depois, caso a tabela exista no glue catalog, ele já adiciona a nova partição criada com o add_partition do awswrangler. Como esse lambda roda apenas uma vez por dia, cada partição da tabela terá apenas 1 parquet facilitando futuras queries no Athena.
3. O StepFunction verifica se existem as tabelas de último preço ofertado e historicas. Caso não existam, ele roda os crawlers (a primeira vez que o stepfunction rodar a tabela não existe, por isso há essa verificação).
4. É criado a view last_offered_price que junta o conteúdo da tabela de último preço ofertado com a temporária, mas mantendo sempre a última aquisição para cada dia. Dessa forma, a view é quase idêntica com a tabela de último preço ofertado, mas enquanto a tabela se atualiza uma vez por dia, essa view está sempre atualizada.