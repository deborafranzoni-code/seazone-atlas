<!-- title: Solução para Cálculo de Diárias em Reservas com Taxa de Limpeza Embutida | url: https://outline.seazone.com.br/doc/solucao-para-calculo-de-diarias-em-reservas-com-taxa-de-limpeza-embutida-UuWnd4CjmO | area: Tecnologia -->

# Solução para Cálculo de Diárias em Reservas com Taxa de Limpeza Embutida

# Contexto

Atualmente, todos os imóveis gerenciados pela Seazone possuem em seus anúncios a separação dos valores de diárias do valor da taxa de limpeza. Essa separação de valores é importante ao negócio Seazone, pois o valor de taxa de limpeza é o principal valor recebido pelos anfitriões dos imóveis (eles também recebem um percentual do valor da diária, mas em geral é a parte menor de seu faturamento em cima de uma reserva). No entanto, essa separação de valores no anúncio pode se tornar um problema em alguns imóveis cujos concorrentes são anúncios não profissionais e que em geral costumam ou embutir o valor de limpeza dentro das diárias ou reduzem significativamente o valor de taxa de limpeza, diluindo parte de seu valor nas diárias.

Dado este cenário, é desejo da Seazone poder diferenciar os imóveis, com alguns que possuem o valor de taxa de limpeza separado da diária, e outros com o valor da taxa de limpeza diluído nas diárias. Para isso, um experimento está sendo conduzido com alguns imóveis a fim de aprimorar a operação nesse novo modelo de precificação e analisar os benefícios com esta opção.

Esta documentação apresenta a proposta de solução a ser implantada na estrutura do Sapron para viabilizar a operação de reservas com o modelo de precipitação com taxa de limpeza diluída nos valores das diárias.

# Como é Hoje

Atualmente, as reservas são importadas da Stays, e dentro dos dados retornados de uma reserva vem a informação com os valores pagos para a Seazone e para a OTA, e em cima disso é feito o cálculo da Taxa de Limpeza e Valor das Diárias.

A partir do cálculo da Taxa de Limpeza, a distribuição das receitas entre todos os envolvidos (Seazone, Proprietário e Anfitrião) se torna relativamente simples. A única exceção ocorre com reservas originadas na **OTA Expedia**, na qual o valor do OTA não vem destacado dentro da reserva, e com isso não é possível inferir qual o valor de Taxa de Limpeza da reserva. Então, cabe à Seazone fazer o cálculo retirando-a do valor total de diárias antes de fazer a distribuição das receitas entre os envolvidos.

O objetivo com a solução proposta para o cenário descrito neste documento onde o valor de taxa de limpeza estará diluído no valor das diárias é, uma vez identificado que a reserva faz parte deste grupo de imóveis que possui o valor de taxa de limpeza diluído nas diárias, aplicar a mesma solução de cálculo já implementada para a OTA Expedia.

# Solução Proposta

A solução proposta passa por três tarefas a serem realizadas.

### Ajuste na Tabela `property_property`

Nesta tabela, deve ser adicionada uma nova coluna booleana chamada `is_cleaning_fee_embedded` indicando forma de cálculo de taxa de limpeza do imóvel, seguindo a seguinte regra:

* `false`**:** indica que o cálculo da taxa de limpeza ocorre externamente à Seazone, e cabe ao Sapron apenas aceitar o valor que já é informado pela Stays. Esse é a opção que representa a forma atual de obtenção da taxa de limpeza de uma reserva.
* `true`**:** indica que o cálculo da taxa de limpeza deve ser feito pela Seazone, pois o valor está diluído nas diárias da reserva.

### Criação da Tabela `property_embedded_cleaning_fee`

Uma nova tabela deve ser criada, e ela gerencia períodos no qual um imóvel está adotado o modelo de cálculo de taxa de limpeza diluída nas diárias das reservas. Sua estrutura é a seguinte:

| **coluna** | **tipo** | **descrição** |
|----|----|----|
| id | bigint | chave primária e autoincrementada |
| created_at | datetime | data e hora da criação do registro para fins de auditoria |
| updated_at | datetime | data e hora da última atualização do registro para fins de auditoria |
| property_id | bigint | chave estrangeira para a tabela property_property |
| start_date | date | data de início do período em que o imóvel está adotando o modelo de cálculo de taxa de limpeza diluída nas diárias das reservas |
| finish_date | date | data de término do período em que o imóvel está adotando o modelo de cálculo de taxa de limpeza diluída nas diárias das reservas. Caso esteja com o valor NULL, indica que o período de adoção ainda está ativo |
| cleaning_fee_value | float | valor de taxa de limpeza a ser extraído das reservas durante o período de adoção do modelo de cálculo de taxa de limpeza diluída nas diárias das reservas |

Os registros dessa tabela serão, inicialmente, criados a partir de solicitação de suporte feito junto ao time de tecnologia.

### Ajuste no worker que importa reservas da Stays

Ao chegar uma nova reserva a partir do worker de importação de reservas da Stays, deve ser seguido o seguinte algoritmo:

```bash
identificar qual o imóvel da reserva (isso já ocorre hoje)

checar se a flag is_cleaning_fee_embedded da tabela property_property é TRUE
Se sim
    obter o registro ativo para o imóvel na tabela property_embedded_cleaning_fee
        SELECT * FROM property_embedded_cleaning_fee 
        WHERE property_id = [id do imóvel da reserva] 
            AND start_date <= [data de criação da reserva na stays]
            AND (finish_date >= [data de criação da reserva na stays] OR finish_date is null);
    se foi encontrado registro do experimento então
        aplicar a mesma regra de cálculo de valores de reserva, com o valor de TL obtido 
        na coluna cleaning_fee_value no passo anterior
    senão
          segue o fluxo desconsiderando que o imóvel está no experimento
Senão
    segue o fluxo já adotado atualmente desconsiderando que o imóvel no experimento
```

### Exemplo de reserva real com taxa de limpeza embutida

A seguir é descrita uma reserva real que está participando do experimento de ter a taxa de limpeza embutida nas diárias, indicando como ocorre hoje o cálculo a partir dos dados obtidos da Stays e como deveria ficar:

| **Dados** | **Valores sem extrair TL** | **Valores com TL extraída** |
|----|----|----|
| reservation_id | 435878 | 435878 |
| stays_reservation_code | SM411I | SM411I |
| total_price | 1070,00 | 1070,00 |
| ota_commission | 165,29 | 165,29 |
| gross_value | 1070,00 | 783 |
| ota_fee | 0 | 0,1544766355 |
| cleaning_fee | 0 | 287 (valor obtido da property_audit) |
| net_cleaning_fee | 0 | 242,6652056 |
| daily_net_value | 904,71 | 662,0447944 |
| extra_fee | 0 | 0 |

Um segundo exemplo com uma reserva que possui taxa extra adicionada em seus valores:

| **Dados** | **Valores sem extrair TL** | **Valores com TL extraída** |
|----|----|----|
| reservation_id | 442480 | 442480 |
| stays_reservation_code | TJ148I | TJ148I |
| total_price | 480,76 | 480,76 |
| ota_commission | 0 (expedia) | 0 (expedia) |
| gross_value | 480,76 | 193,76 |
| ota_fee | 0 (expedia) | 0 (expedia) |
| cleaning_fee | 0 | 287 (valor hipotético) |
| net_cleaning_fee | 0 | 242,6652056 |
| daily_net_value | 480,76 | 193,76 |
| extra_fee | 22,90 | 22,90 |