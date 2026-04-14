<!-- title: Comunicação e Dados | url: https://outline.seazone.com.br/doc/comunicacao-e-dados-yi5tQoMa4W | area: Tecnologia -->

# Comunicação e Dados

Github: <https://github.com/Khanto-Tecnologia/api-stays>

# Comunicação Sheets ↔ AWS

A comunicação com o Sheets é feita sempre a partir de um AppScript na própria Planilha. Os Scripts podem ser acessados entrando na Planilha em questão → Extensões → App Script.

 ![Untitled](Comunicac%CC%A7a%CC%83o%20e%20Dados%2089946bfbd0584383aca79db3425fa651/Untitled.png)

Não há versionamento do código ou scripts salvos no github, então é necessário tomar cuidado para acidentalmente não deleta-los.

Outro detalhes é que as funções parecem ser globais entre arquivos, então cuidado ao copiar o código de um arquivo para um novo, lembre de mudar os nomes das funções nestes casos.

## API Gateway

Quando o script for executado no AppScript, por padrão é acionado um endpoint no API Gateway, que integra com uma Lambda via proxy para tratar o request e salvar as diversas tabelas de input na AWS.

O inverso também se aplica, as vezes o AppScript pode fazer um request para ler uma tabela da AWS (utilizando essa integração descrita previamente) e salvá-la nas diversas planilhas de Output.

Hoje é utilizado a **mesma API** para todos os requests, sendo que é necessário um **token** de autenticação (que também é o mesmo para todos).

O link e token podem ser visualizados acessando a API Gateway pela AWS. O link aparece ao clicar na aba Stages e no nome do Stage em questão, enquanto que o token fica na aba API Keys.

Hoje em prod o link é: <https://hmcagntdi6.execute-api.us-west-2.amazonaws.com/sheets-comunication-v0>

Todos os recursos e métodos podem ser visualizados abaixo, sendo que para usa-los basta colocar o link do Stage + o path do recurso.

 ![Untitled](Comunicac%CC%A7a%CC%83o%20e%20Dados%2089946bfbd0584383aca79db3425fa651/Untitled%201.png)

 ![Untitled](Comunicac%CC%A7a%CC%83o%20e%20Dados%2089946bfbd0584383aca79db3425fa651/Untitled%202.png)

# blocks

## write_input

# competitors

Esse recurso é relacionado a Seleção de Concorrentes.

## write_input

Esse método irá salvar os concorrentes da Aba Concorrentes, link: [\[S2.0\] Modelo da Planilha de Setup (Concorrentes)](https://docs.google.com/spreadsheets/d/1Px1rW8jTy7UqcUmHUNE7uGMUUAWzYQvt3zPErk4glJI/edit#gid=748807682).

### **AppScript**

O papel do AppScript é converter os dados vindos da Planilha do formato:

 ![Untitled](Comunicac%CC%A7a%CC%83o%20e%20Dados%2089946bfbd0584383aca79db3425fa651/Untitled%203.png)

Para o formato:

 ![Untitled](Comunicac%CC%A7a%CC%83o%20e%20Dados%2089946bfbd0584383aca79db3425fa651/Untitled%204.png)

* Os ";" são convertidos para multiplas linhas.
* A Strata é convertida pra MinFaturamento e MaxFaturamento, isso é um dicionário hardcoded no AppScript.
* Converter a coluna com Cidade e Bairro em duas colunas diferentes também adicionando novas linhas quando necessário.

**Trigger:**

* Acionamento manual (Sirius → Procurar Concorrentes) ;
* Cron todo dia 01 do mês às 6h00 da manhã

### **Lambda**

O lambda salva as informações particionado pela coluna "date" no bucket sheets communication no path inputs/competitors. Também existe coluna timestamp com hora, minuto e segundo pra diferenciar aquisições do mesmo dia.

Por último, o Lambda dispara o [\*\*FetchCompetitors](https://www.notion.so/Sele-o-de-Concorrentes-5057316f32a54052a147f30067609dc8?pvs=21).\*\* Em ambiente de 'dev' ou de uma feature, ele aciona o Arn do StepFunction existente em 'dev' da stack do repositório sirius-precificação, enquanto que em ambiente de 'prod' ele aciona o Arn de 'prod'.

# discounts

## write_input

# dynamic-blocks

Esse recurso é relacionado aos [bloqueios dinâmicos](/doc/comunicacao-e-dados-aWFByTFvPo) na parte da Stays

## write_input

Esse método irá salvar as regras dos bloqueios dinâmicos da Aba Janelas, link: [\[S2.0\] Modelo da Planilha de Setup (Janelas).](https://docs.google.com/spreadsheets/d/1Px1rW8jTy7UqcUmHUNE7uGMUUAWzYQvt3zPErk4glJI/edit#gid=182326611)

### **AppScript**

O papel do AppScript é apenas enviar os dados do jeito que estão pra AWS.

**Trigger:**

* Acionamento manual (via botão na planilha);

### **Lambda**

O Lambda recebe as informações do AppScript e faz um join com o [setup_groups](/doc/comunicacao-e-dados-aWFByTFvPo). A função salva os parâmetros dos bloqueios dinâmicos já separados por imóvel, facilitando a integração no cálculo dos intervalos em [dynamic_block_intervals](/doc/comunicacao-e-dados-aWFByTFvPo).

O output do lambda é uma tabela salva em formato parquet no path bucketsheetscommunication/inputs/dynamic_block_rules/. As partições são 'state' ('current' ou 'historic') e a data de aquisição utcnow. Além disso, também é adicionado a coluna 'timestamp' com hora, minuto e segundo. Toda ingestão é feita com append na partição 'historic' e overwrite na 'current'.

# listings-evaluation

## analysis

Esse método é responsável por retornar os dados de reviews de anúncios com notas abaixo do desejado com base na nota mínima passada na aba Input, link: [\[S2.0\] Modelo da Planilha de Avaliação de Anúncios](https://docs.google.com/spreadsheets/d/1Px1rW8jTy7UqcUmHUNE7uGMUUAWzYQvt3zPErk4glJI/edit#gid=2135658376)

### **AppScript**

O AppsScript envia os dados da coluna Nota Mínima para AWS através de uma chamada de API e escreve os dados de reviews dos anúncios retornados na aba de Output e metadados de execução na aba de Input (data e hora da última execução, data da última aquisição de reviews e status da chamada de API).

**Trigger:**

* Acionamento manual (via botão)

### **Lambda**

O Lambda recebe a nota mínima do AppScript e consulta a tabela de Reviews no Data Lake filtrando para apenas pegar informações de anúncios com nota "overall" abaixo da nota selecionada. Os dados são pegos da última aquisição de reviews, ou seja, da partição mais recente. Também é feito a adição da coluna "link", com o link para a página do anúncio no Airbnb montada usando o valor "id_airbnb" do imóvel. Os dados consultados as informações de data e timestamp de execução são armazenados na AWS no formato parquet no path "bucketsheetscommunication/outputs/listings_evaluation/". O output da função são os dados consultados de reviews (com a coluna "link", porém sem a informação de data/hora de execução) e a data da última aquisição de reviews.

# min-stay-period

## write_input

# min-stay-weekdays

## write_input

# min-stay-month

## write_input

# performance

## analysis

### get

### post

# pricing

## competitors-by-user

## direct

### bring-data

Esse método é responsável por retornar os imóveis, datas e últimos preços ofertados dos imóveis do grupo que o usuário selecionar, link: [\[S2.0\] Planilha de Precificação Direta](https://docs.google.com/spreadsheets/d/1b5_dOnaIqLBOKe6GOITSyIq8AJ2dnrA3qynBR-E3oRc/edit#gid=0)

### **AppScript**

O AppsScript lê a celula do "Grupo/Imóvel\*\*"\*\* e a envia para AWS através de uma chamada de API.

A chamda dispara um lambda que retorna um link de download de json. O AppScript realiza um segundo request para baixar o arquivo json e o resultado é inserido na Planilha.

**Trigger:**

* Acionamento manual (via botão);

### **Lambda**

O Lambda lê a tabela de grupos e a partir do event, ele filtra essa tabela para ter apenas os imóveis que o usuário gostaria de precificar. Depois, ele expande esse dataframe para ter todas as datas entre hoje e 180 dias para frente. Em seguida, é lida a tabela de preços históricos e é feito um merge com o dataframe anteriormente comentado. Caso uma data não possua preço histórico ela é mantida nula.

Detalhe: Hoje a tabela de preços históricos é a tabela temporária bucketpricing/price_before_stays_temp/, essa tabela não possuí o último preço ofertado de cada imóvel, então é necessário ler a tabela inteira e manter a última aquisição de cada data. Além disso, ela também mistura os preços de desconto de estadia mínima, então é necessário descarta-los também.

Por último, o resultado é salvo em bucketsheetscommunication/inputs/direct_pricing/ com um overwrite e no formato json (orientação split). É criado então um link para download do arquivo e esse link é retornado ao AppScript.

### send-data

Esse método é responsável por receber os imóveis, datas e preços desejados inseridos na planilha [\[S2.0\] Planilha de Precificação Direta](/doc/precificacao-XIV8Y9Mul6) e seu papel é aplicar as regras da Planilha de Setup para depois enviar os preços pra Stays.

### **AppScript**

O AppsScript lê os dados preenchidos na aba "Preços" e os envia para a AWS no formato json (orientação split), ou seja, o json é um dicionário contendo as chaves "data" (lista de lista contendo cada valor das celulas) e "columns" (lista contendo o nome das colunas).

A chamda dispara um lambda que retorna 200 se conseguiu enviar a mensagem pra fila **SQSQueuePricingApplySetupRules** sem erros e o AppScript informa isso ao analista.

**Trigger:**

* Acionamento manual (via botão);

### **Lambda**

O Lambda lê o json enviado e cria um dataframe a partir dele. É retirado as linhas que possuem a coluna "price" nula. O resultado é salvo em bucketsheetscommunication/outputs/direct_pricing/ particionado pelo timestamp. Por último, é enviado uma mensagem pra fila **SQSQueuePricingApplySetupRules.** A mensagem contem o path do parquet salvo no s3 e o valor 'direct' no campo 'origin' pra mantermos controle de onde o preço veio.

### send_category_data

## generate-url

## heuristic

### apply-pricing

### get

### post

### base-prices

### increment-antecedence

### increment-period

### increment-weekday

## period-price-modifier

# pricing-modality

## write_input

Esse método irá salvar a modalidade de precificação da Aba Modalidade de Precificação, link: [\[S2.0\] Modelo da Planilha de Setup (Modalidade de Precificação).](https://docs.google.com/spreadsheets/d/1Px1rW8jTy7UqcUmHUNE7uGMUUAWzYQvt3zPErk4glJI/edit#gid=2123050768)

### **AppScript**

O papel do AppScript é apenas enviar os dados do jeito que estão pra AWS.

**Trigger:**

* Sem Trigger.

### **Lambda**

O único trabalho do Lambda é salvar a tabela particionada.

O output do lambda é uma tabela salva em formato parquet no path bucketsheetscommunication/inputs/pricing_modality/. As partições são 'state' ('current' ou 'historic') e a data de aquisição utcnow. Além disso, também é adicionado a coluna 'timestamp' com hora, minuto e segundo. Toda ingestão é feita com append na partição 'historic' e overwrite na 'current'.

# setup_groups

## make_diff

Esse método é responsável por criar os warnings da aba Outputs de Warnings baseado nos inputs da aba Grupos, link: [\[S2.0\] Modelo da Planilha de Setup](https://docs.google.com/spreadsheets/d/1Px1rW8jTy7UqcUmHUNE7uGMUUAWzYQvt3zPErk4glJI/edit#gid=2135658376)

### **AppScript**

O AppsScript envia os dados da coluna Lista de Imóveis para AWS através de uma chamada de API e escreve os warnings retornados na aba de outputs e metadados de execução na aba de grupos (data e hora da última execução e status da chamada de API).

**Trigger:**

* Acionamento manual (via botão);
* Cron todo dia às 7h00 da manhã

### **Lambda**

O Lambda recebe as informações do AppScript e armazena os inputs junto as informações de data e timestamp de execução na AWS salvos no formato parquet no path bucketsheetscommunication/inputs/setup_groups/. Os inputs mais atuais são salvos em "current" e o histórico de inputs fica salvo em "historic". Após isso, a função lambda compara os ids únicos enviados como inputs com os ids adquiridos em [listings_info](/doc/comunicacao-e-dados-aWFByTFvPo), gerando uma tabela com a diferença entre as duas listas de ids. O output da função é a tabela de diferenças recém comentada.

# special-prices

## write_input

# supervisory

## get

## post

# Comunicação AWS ↔ Stays

Como muitas partes do Sirius iriam utilizar ou escrever dados na Stays, foi criado uma interface para realizar essa comunicação. Todos os scripts do Sirius irão utilizar essa interfaçe pra usar a API da Stays.

Existem duas contas da Stays, uma de prod e outra pra dev. Para utilizar as contas é necessário o url e o token, sendo que os dois variam dependendo da conta.

Essa infomações estam salvos dentro do **[AWS Systems Manager Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html)**, no path /Secrets/ENVIRONMENT/StaysToken e /Secrets/ENVIRONMENT/StaysUrl, onde o ENVIRONMENT pode ser 'dev' ou 'prod' dependendo do ambiente que o Lambda se encontra. Caso o token tenha que ser alterado, basta mudar no Parameter Store.

# ingestion

A parte de ingestão é responsável por ler informações da Stays e salva-las na AWS.

## listings_info

**Descrição:** Essa é uma lambda que faz um get na seguinte API da Stays: https://ssl.stays.com.br/external/v1/content/listings. Essa API irá retornar várias informações referentes a cada imóvel, como seu id e _id (esses são ids únicos que a Stays usa para armezar os imóveis, acredito que id é único para os imóveis da Seazone e _id é único para todos os imóveis da Stays), internalName (nome que colocamos pro imóvel, ILC1110) e status (active, inactive, draft, hidden). A API possuí os parametros skip, status e limit.

O output do lambda é uma tabela salva em formato parquet no path bucketstaysraw/listings_info/. As partições são 'state' ('current' ou 'historic') e a data de aquisição utcnow. Além disso, também é adicionado a coluna 'timestamp' com hora, minuto e segundo. Toda ingestão é feita com append na partição 'historic' e overwrite na 'current'.

**Detalhes:** Esse recurso tem por default um valor máximo de imóveis retornados de 100, sendo que não funciona tentar aumentar esse valor através do parametro limit, portanto, é necessário rodar várias vezes o request pra conseguirmos as informações de todos os imóveis da Seazone. Outro detalhe é que essa API não retorna se existe ou não uma nova página de imóveis, então é necessário sempre que realizar o request, ver se o resultado teve tamanho menor que 100, se sim então não existe mais imóveis, se não então precisa skipar 100 imóveis e fazer o request de novo. Por último, caso não seja especificado, a API apenas retornará os imóveis com status Active, então precisamos especificar todos os outros também.

**Trigger:** Diário 6:00 da manha.

## reservations

**Descrição:** A API da Stays possuí diferentes recursos para conseguirmos as reservas, sendo que os dados que elas retornam são praticamente o mesmo (a príncipal diferença está nos nomes de colunas ou forma como o dado é apresentado).

* Endpoint: booking/reservations, com método GET: O problema desse recurso é que, para usá-lo, é necessário especificar o id do imóvel + conjunto de datas. Se com esses parâmetros o resultado possuir mais que 100 reservas, a API irá retornar as 100 primeiras reservas e não irá dizer que existe mais, sendo necessário sempre analisar o tamanho do resultado e usar o parâmetro "skip" pra iterativamente pular 100 reservas, caso o tamanho do resultado seja 100. Essa API também possuí o parâmetro limit, mas o seu valor máximo é 100 (mesmo que coloque um número maior que 100 o resultado será as 100 primeiras reservas). Ou seja, esse "skip" não serve como paginação, mas com um índice de onde parte a listagem das reservas. Se você quiser recuperar todas as 350 reservas de um determinado listing, será necessário realizar 4 chamadas a API, enviando valor de skip 0, 100, 200 e 300, respectivamente.
* Endpoint: booking/reservations-export, com método POST: O único parâmetro obrigatório deste recurso é o conjunto de datas, mas ele não tem limite de número de imóveis usados no request e também não possuí nenhum limite explícito de tamanho. Por causa disso, esse método é **mais rápido** que o de cima, porém ainda é necessário dividir o request em várias partes porque existe um limite implícito de bytes que o método pode retornar.

O lambda que puxa as reservas lê a tabela listings_info pra obter os ids da Stays dos imóveis e então é feito vários posts assíncronos (um por id) sobre todas as datas de criação das reservas no método booking/reservations-export.

O output é uma tabela de reservas no path "bucketstaysraw/reservations/". As partições são 'state' ('current' ou 'historic') e a data de aquisição "datetime.utcnow". Além disso, também é adicionado a coluna 'timestamp' com hora, minuto e segundo. Toda ingestão é feita com append na partição 'historic' e overwrite na 'current'.

**Detalhes:** Também foi explorado a opção de usar Webhooks, mas a Stays fornece no mesmo Webhook TODAS as notificações que existem, ou seja, reservas criadas/modificadas, assim como mudanças DIÁRIAS de preço. Visto que o Sirius precifica até 180 dias pra frente de cada imóvel, talvez até mais de uma vez por dia, o Webhook iria ficar caro pra usar com API Gateway + Lambda.

**Trigger:** Diário 6:05 da manha.

# patch

O patch é a parte que insere dados na Stays.  Todos eles precisam de uma lógica de **retry** porque é bem comum que requests com a Stays sofram de timeout. Além disso, eles também precisam diferenciar os ambientes de teste com os de produção. Hoje existem duas contas da Stays, uma de 'prod' e outra de 'dev', as credenciais se encontram no parameter store.

Essas filtragens são feitas a partir da variável de ambiente 'Environment'. Em ambiente de teste ela é 'dev' ou o nome da stack. Em ambiente de produção ela é 'prod'.

## dynamic_blocks

O dynamic_blocks realiza os bloqueios dinâmicos (se hoje é dia 01/01/2023 e for configurado pra bloquear após 30 dias, então o Sirius irá bloquear TODAS as datas depois de 30/01/2023, ou seja, todos os dias de 31/01/2023 até o tamanho máximo de bloqueio serão bloqueadas. O tamanho máximo sendo considerado é 360 dias, então 26/01/2024).

Para fazer os bloqueios é utilizado o recurso booking/reservations.

* Endpoint: booking/reservations, método POST: Cria um bloqueio com o payload fornecido no post.
* Endpoint: booking/reservations/{reservation_id}, método PATCH: Altera o bloqueio do id fornecido com o payload fornecido.
* Endpoint: booking/reservations/{reservation_id}, método DELETE: Deleta o bloqueio do id fornecido

**Problema:** Para criar um bloqueio usando essa API, deve-se fornecer uma data de checkin e checkout, mas não pode já existir uma data reservada ou bloqueada dentro desse período, então pra deixar o script robusto precisamos "contornar" essas reservas ou bloqueios que talvez já existam.

A solução do Problema é o script abaixo [dynamic_blocks_intervals](/doc/comunicacao-e-dados-aWFByTFvPo), seu papel é justamente ler os parâmetros que a Comunicação Sheets ↔ AWS salvou no bucket, ler a tabela de reservas e fazer uma lógica inteligente pra contornar os bloqueios pra depois o **[dynamic_blocks](/doc/comunicacao-e-dados-aWFByTFvPo)** rodar, cujo papel é apenas usar a API da Stays pra deletar, atualizar ou criar bloqueios. Além disso, também não é possível bloquear imóveis inativos, então o script ignora esses imóveis. Tudo isso é orquestrado por uma StepFunction.

 ![Untitled](Comunicac%CC%A7a%CC%83o%20e%20Dados%2089946bfbd0584383aca79db3425fa651/Untitled%205.png)

**Trigger:** O trigger é diário às 6h30 da manhã.

### dynamic_blocks_intervals


1. Lê as regras (dynamic_block_rules), setup_groups (pra relacionar os grupos das regras com os imóveis) e listings_info (pra pegar o id da stays saber quais imóveis são inativos).
2. A partir dos dados acima, gera-se uma tabela com o checkin e checkout ideal pra cada imóvei. A internalNote ideal também é gerada:

   'Sirius API - Lead - {dias da regra} days'

   Essa internalNote é importante pra depois relacionar quais reservas foram criados por esse modulo do Sirius.
3. O script lê as reservas/bloqueios já existentes e irá contorna-los caso necessário. Ele também adiciona um número a direita da internalNote dizendo qual parte do bloqueio foi criado, exemplo:

 ![Untitled](Comunicac%CC%A7a%CC%83o%20e%20Dados%2089946bfbd0584383aca79db3425fa651/Untitled%206.png)

No imóvel acima, os dias 14-18 estavam bloqueados, então o script gerou intervalos com checkout dia 14 e checkin dia 18, sendo que as internalNote eram, respectivamente, 'Sirius API - Lead - 30 days 0' e 'Sirius API - Lead - 30 days 1'


1. Com os intervas gerados, o script irá acessar os bloqueios criados anteriormente a partir da tabela de reservations e irá gerar as seguintes tabelas:

   
   1. dynamic_blocks_delete: São os bloqueios que existiam antes, mas não existem agora, isso pode acontecer se um imóvel ter sua regra apagada, alterada, ou se não é mais necessário contornar um bloqueio (ao contornar uma reserva/bloqueio é gerado os bloqueio 0 e 1, se essa reserva/bloqueio não existe mais o bloqueio 1 pode ser deletado e o bloqueio 0 extendido).
   2. dynamic_blocks_post: São os bloqueios que não existiam antes, mas existem agora. Normalmente devido a criação/alteração de uma regra.
   3. dynamic_blocks_patch: São os bloqueios que já existiam antes, mas que precisam ser alterados. Normalmente porque o dia mudou e precisamos deslizar o bloqueio um dia pra frente.

### dynamic_blocks

Esse script irá ler as tabelas dynamic_blocks_delete, dynamic_blocks_post e dynamic_blocks_patch pra usar nos seus respectivos métodos delete, post ou patch da API.

É essencial pra lógica funcionar que eles rodem nessa ORDEM:

delete → post → patch.

Isso porque pra criar um bloqueio é necessário primeiro deletar o antigo, senão a API retorna erro.

**Retries:** O script também utiliza uma lógica de retries, visto que é bem comum que a API da Stays de timeout, pra tentar realizar os bloqueios. A lógica é simples, caso não retorne 200 o lambda da um sleep pra depois o ser tentado de novo o request.

Se depois de algumas iterações o erro persistir, o lambda retorna quais listings/bloqueios não conseguiram fazer o delete, post e patch.

**Detalhs:** Caso a variável de ambiente 'Environment' não for 'prod', então o script irá atuar apenas em cima dos imóveis de teste.

## prices

O patch_prices é a parte da comunicação com a Stays que precifica os imóveis. O endpoint utilizado é o "calendar/listing/{id}/batch" com o método PATCH, sendo que o id é o identificador do imóvel na Stays. A vantagem dela é que ela permite juntar várias datas de um imóvel em apenas um request. Um detalhe dessa API é que ela retorna erro caso um preço com estadia maior seja menor que o preço de uma estadia menor, ou seja, o desconto de estadia mínima é mais caro que o preço normal do imóvel. É necessário então filtrar esses casos pra evitar do script crashar.

A lógica é:


1. ler a tabela de preços que terá todas as informações necessárias pra usar no request, como id_seazone, data, estadia mínima, preço, bloqueio de checkin e checkout.
2. Ler a tabela listings_info para obter o id do imóvel da Stays.
3. Ver se existem linhas duplicadas em id, dia e estadia mínima, caso sim algo deu errado com esse imóvel durante a lógica de precificação e ele será retornado. Os outros imóveis precificam normal.
4. É filtrado os casos onde o preço com desconto de estadia mínima é maior que o preço normal.
5. O dataframe é os requests são feitos de forma assíncrona. É feito uma lógica de retries caso o request não retorne 200.
6. Caso haviam datas duplicadas, descontos mais caros ou algum imóvel não foi atualizado, o lambda retorna um dicionário de erro, onde cada chave é um dos tipos de erro citado acima e os valores são a lista de ids no respectivo erro.

**Trigger:** O trigger é a fila SQS "**SQSQueuePricingApplySetupRules".** Toda vez que uma mensagem for escrita nessa fila o Lambda é disparado.