<!-- title: Suportes Operacionais - Battle Card | url: https://outline.seazone.com.br/doc/suportes-operacionais-battle-card-YXgySMB0dS | area: Tecnologia -->

# Suportes Operacionais - Battle Card

🚨 **Para todos os suportes, caso seja necessário comunicação com o cliente, abra uma MD com o cliente,**   **e o PM para que todos possam acompanhar o chamado.**

🚨 Sempre tente deixar registros no card da solicitação visto que nem todas as alterações são salvas em tabelas com sufixo `_audit` , tanto do que foi alterado quanto de conversas que aconteceram por causa da solicitação

# Suportes com resoluções conhecidas


---

## OPMIG001 - Migrar indicação

Dados necessários:


1. `partner_id` (tabela `account_partner`, geralmente a partir do campo `email` em `account_user` ) do parceiro antigo e do parceiro novo.
   * <https://metabase.seazone.com.br/question/1233-account-partner-user>

O que fazer:

Dependendo do suporte

Alterar nas tabelas

*  `partners_indication_investment` - indicação de investimento
* `partners_indication_property` - indicação de propriedade
* `partners_indication_allotment` - indicação de terreno

o campo `partner_id`  do antigo para o novo.

>  ⚠️ É normal que uma ou duas tabelas estejam sem indicações pro partner_id, eles podem fazer indicação em somente um formulário, mas se nas 3 tabelas não forem encontrados registros de indicação, um de três problemas aconteceu:
>
> 
> 1. O usuário mencionou o parceiro errado;
> 2. O dev pegou o partner_id errado;
> 3. Por algum motivo, as indicações foram associadas com o partner_id errado (se o pipedrive_person_id não é encontrado na account_user, o SAPRON deixa partner_id = 1 nas indicações. Use essa informação para debuggar e conversar com o cliente). Nesses casos, verifique os campos pipedrive_deal_id nas tabelas que o possuem.


---

## OPSYN001 - Importar/Sincronizar extensão

Dados necessários:


1. `stays_reservation_code` (formato **AA1234I**, sendo que o "i" maiúsculo do final é fixo e podem ter de 2 a 4 números no meio).

OBS: As vezes o pessoal do fechamento também passa `code` , onde ambos os dados podem ser convertidos entre si na tabela `reservation_reservation` .

O que fazer:

No [Swagger](https://api.sapron.com.br/swagger/),  no endpoint `/channel_manager/import_stays_reservation/`, inserir como informação o `stays_reservation_code` .

> 🚨 Problemas conhecidos
>
> 
> 1. Existe, no backend, uma verificação pelo first_name + last_name do guest_id com o que está registrado na Stays, então se em um lugar tivermos "Marco Aurélio" e no outro "marco Aurélio" (ou qualquer outra diferença, pode ser bem discrepante), você receba o erro "NoOriginalReservationFound".
>
>    Ajustando o nome para que eles estejam iguais em ambos os lugares, a importação tende a funcionar como esperado.
> 2. A reserva NÃO PODE estar conciliada (flag no banco como true) para que ela seja importada novamente.


---

## OPSYN002 - Importar/Sincronizar reservas 404

Durante uma vez por mês a equipe de fechamento necessita que os dados todas as reservas estejam corretos nas tabelas certas para que concluam seus cálculos. Uma das tabelas que que a equipe usa é a `Closing Property Resume`, reservas que estão presentes nessa tabela são listadas no Sapron: Financeiro > Fechamento > Imóvel.

**Problemas:** Quando uma reserva de `status=Concluded` que existe na tabela `Reservation Reservation` estiver contando no fechamento, mas ela não aparece na tabela `Closing Property Resume` e nem no front do Sapron.

**Causa do problema:** Quando uma reserva é inicialmente cancelada na Stays, mas depois foi reservada novamente. Por já ter sido cancelada, a reserva deixa de contar na `Closing Property Resume` e fica "perdida", pois o sistema contabiliza ela no fechamento (por ter sido reservada de novo) ao mesmo tempo em que não consegue identifica-la (por que já foi cancelada).

**Como identificar:** Não é tão comum de acontecer problemas deste tipo, mas caso aconteça, alguém da equipe de fechamento vai abrir um suporte com evidências do acontecimento. 

**O que fazer:** Neste caso, apenas importar no Painel de Gerenciamento não irá funcionar e no inspecionar pode retornar `404 - reserva não encontrada`. Então você deve atualizar algum atributo da reserva que provoque a importação forçada da reserva. Aqui está o passo a passo:


 1. Abra uma conexão com o banco de dados em produção;
 2. Localize a reserva na tabela `reservation_reservation`;
 3. Encontre o atributo conciliada e marque como `false` (se estiver `true`);
 4. Acrescente +R$ 0,01 (1 centavo) no atributo `daily_net_value`;
 5. Salve as alterações e faça o `commit`;
 6. Remova o 1 centavo adicionado no atributo `daily_net_value`, preservando o valor original;
 7. Encontre o atributo concliada e marque como `true` novamente;
 8. Salve as alterações e faça o `commit` de novo;
 9. Abra o Painel de Gerenciamento no Sapron;
10. Importe a reserva pelo `Stays Reservation Code`;
11. É esperado que a reserva que antes não aparecia, agora seja listada no fechamento do imóvel reportado e também deve aparecer na tabela `closing_property_resume`.

 ![ANTES - Filtro: Imóvel CAR0201 - Dez 2025](/api/attachments.redirect?id=f0e42131-016b-48d6-8de7-5386adac3d38 " =684x305")

 ![DEPOIS - Filtro: Imóvel CAR0201 - Dez 2025](/api/attachments.redirect?id=f2eef60b-40c2-443e-9738-da1642fe0d98 " =570x233")

## OPCOM002 - Alterar comissão do passado nas Reservas

**Dados necessários:**


1. `property_id` ou `code` do imóvel;
2. Data de início para a alteração.
3. Dado da nova comissão

Verificar se a comissão estiver certa na `Property Audit`  pelo `property_id` ou `code` do imóvel;

Identificar o `code` das reservas na `Proper Pay Property Daily Transfer`  Filtrando pelo `property_id`   e pelo `type=revenue`, e pela data(mês inteiro) da nova comissão  em `Cash Date`

Verificar na `Reservation` se a comissão nas reservas estão conforme


**O que fazer**

Atualizar na `reservation` a `Property Fee` é `Seazone Fee` conforme o necessário

**Exemplo**

Ex. Comissão de 25% para março e abril.

* Na `Property Audit` parece ok
* A somatória dos valores da  `Proper Pay Property Daily Transf ` deve dar o soma da receita do mês de abril
* Na `reservation` procurar pelo `code` extraindo da coluna `Proper Pay Property Daily Transf > Description>reservationcode` 
* Na tabela `Reservation` o comissão esta 0,2 (20%)


 ![](/api/attachments.redirect?id=5bfbf50e-8d8f-4341-84f9-5378cec57675 " =1142x246")


\

 ![](/api/attachments.redirect?id=519afb87-b5af-4d23-900b-e907ccbf47b6 " =1340x545")


\

 ![](/api/attachments.redirect?id=c7df7af5-5fc1-4af2-b762-c3d61deb70a1 " =1363x223")


\

## OPPRO001 - Alterar Proprietário (login) de uma propriedade

Dados necessários:


1. `property_id` ;
2. `owner_id` ;

O que fazer:

Na tabela `property_property_owners`, procure pelo `property_id`a linha da propriedade e altere o `owner_id` relacionado a ela. 

<https://metabase.seazone.com.br/question/1184-property-owners-by-property-code>


Na tabela  `property_property`procure pelo `property_id` e altera a coluna do `owner_id`

Na tabela `property_property`, caso já exista valor preenchido para a coluna `bank_details_id`, alterar para o valor de `default_bank_details_id` (encontrado na tabela `account_owner`- no registro filtrado por `owner_id`).


Caso o endereço existente no `financial_invoice_details` do owner (encontrado com base na coluna `invoice_address_id`, da tabela de `account_owner`) seja brasileiro, alterar `invoice_details_id` (tabela `property_property`)  para o valor de `financial_invoice_detail`(owner).


---

## OPNF001 - Alterar dados da Nota Fiscal

Dados necessários:


1. `property_id` ou `owner_id`
2. Dados que compõem a Nota Fiscal (Nome, CPF ou CNPJ, email, `user_id`, endereço, número do endereço, cidade, complemento, bairro, número de telefone, CEP e estado)

O que fazer:

Caso seja a nota fiscal da propriedade:

* Procure por `property_id` na tabela `property_property` e altere o dado necessário a partir do campo `invoice_details_id`

Caso seja a nota fiscal do proprietário:

* Procure por `owner_id` na tabela `account_owner` e altere o dado necessário a partir do campo `default_invoice_details_id`

Se for necessário, crie um novo registro de nota fiscal na tabela `financial_invoice_details`

> 🚨 CUIDADO: Ao alterar dados da nota, tenha ciência de que isso pode afetar um ou mais propriedades/proprietários. Se for preciso manter os dados de um e alterar de outros, crie um novo registro.
>
> ⚠️ As notas fiscais sempre levam em consideração primeiros os dados anexados a propriedade. Os dados que estiverem vazios ou nulos serão buscados nos dados anexados ao proprietário, necessariamente nessa ordem.


---

## OPROL001 - Alterar Função (Role)

Dados necessários:


1. `user_id`

O que fazer:

Na tabela `account_user`, altere o campo `main_role` para um dos argumentos válidos:


1. Admin
2. Seazone
3. Attendant
4. Host (Anfitrião/Franquia)
5. Owner (Proprietário)
6. Partner (Parceiro/Corretor)
7. Guest (Hóspede)

> 🚨 Preste MUITA atenção nas outras tabelas com prefixo `account_`. Se elas tiverem um registro com o `user_id` do suporte em questão, em alguns casos o Front ainda concede acesso ao outro módulo. Por exemplo:
>
> * Se o `user_id = 1` tiver `main_role` como *"Host"* e, ao mesmo tempo, tiver um registro na `account_partner` e outro na `account_host` onde `user_id = 1`, ele terá acesso aos dois módulos e poderá transitar livremente entre eles.
>
> Se foi solicitado a migração de Host pra Partner, ou vice-versa, verifique as duas tabelas e mantenha somente o registro necessário pra solicitação.
>
> Atualmente (30/08) não conheço outro caso entre duas Roles que exijam essa verificação fora esse.


---


## OPFEC001 - Fechamento

Ó fechamento é executado todos os dias na madrugada no AWS-lambda (que gera os dados de toda a base do Seazone)

Esse procedimento preenche todas as tabelas com nome `proper_pay_<descricao>`


* Não adianta mudar/atualizar essas tabelas com nome `proper_pay_<descricao>` pois os dados serão atualizados todo dia no aws
* Para ver as reservas os detalhes estão no *Reservation Reservation*  nos cards eles enviam o code
* \
* \


## OPMIG002 - Migrar reservas de imóvel X para imóvel Y

**Existem duas formas de fazer a migração:  pelo Sapron de forma mais automática e pela base, de forma mais 100% manual. Vamos ver as duas formas.**

**Dados necessários:**

* identificar O `Property ID` dos imóveis (X e Y) . Nesta [consulta](https://metabase.sapron.com.br/question/1092-property-owner-user-by-property-code) pode encontrar pelo `CODE` da propriedade.
* Sobre as reservas que precisam migrar, identificar na Tabela `Reservation Reservation` as colunas:
  *  `reservation_id` 


  *  `Property ID`
  *  `Listing ID`

  
:::tip
  Os Listing IDs do imóvel Y devem ser criados pelo solicitando ou equipe Sapron/Stays. Pois os mesmos anúncios não são aceitos pela base na migração.

  :::

  \
* Na tabela `Reservation Listing` identificar o `ID` . Filtre pelo `Property ID` dos dos imóveis (X e Y)
  * `Ota ID`
  * `Property ID`

  
:::warning
  Prestar atenção no Ota ID. Se o imóvel **X** tiver **OtaID=1**, então procure o **ID** com **OtaID=1** do imovel **Y**

  :::

  \

**O que fazer (versão Sapron)?**

Na tabela `Reservation Reservation` identifique a reserva que deseja migrar, faça os passos a seguir:

* troque o **Property ID** do **imóvel X** para o novo id do **imóvel Y**
* Copie o `Stays Reservation Code` da reserva, sincronizar pelo Sapron
* Cole o `Stays Reservation Code` no Painel de Gerenciamento e clique em "**Importar**"
* Aguarde e depois confira se a reserva foi migrada com sucesso

 ![Painel de Gerenciamento do Sapron](/api/attachments.redirect?id=7091d973-7532-451a-a355-3c6ff22522ad " =494x214")

**O que fazer (versão manual)?**

Na Tabela `Reservation Reservation` identifique o registro pelo `reservation_id`  que deseja migrar. Atualize as seguintes colunas:

*  `Property ID` - novo id do ***imóvel Y***
*  `Listing ID` - novo id do `Reservation Listing` associado ao ***imóvel Y*** e ao ***OtaID*** correspondente

### Porque Não migram algumas reservas?

1 - Se a reserva for cancelada, não há necessidades de serem migradas, pois não tem influência no fechamento.

2 - Quando é ativado o fluxo de migração as reservas, sempre é considerado a d**ata de Ativação ou inicio de contrato do novo imóvel**. 

Exemplo o Imóvel 3924- MRE801 foi ativado o dia ***15/02/2015***


 ![](/api/attachments.redirect?id=962bd979-7e81-4842-b08a-58dd357b47ae " =732x164")


Assim reservas anteriores a essa data **>>não são migradas<<** 

**Pois temos a regra:** *"Todas as reservas tem data de checkin igual ou maior a data de Ativação do Imóvel"*\nNeste caso uma reserva com check-in 02/02/2025 não será migrada pois a data é menor do que a data de ativação do imóvel.

## OPEMAIL001 - Cadastrar e-mail para envio das reservas vendidas

Acessar na `AWS > Seazone Technology > Amazon S3 > Buckets > sapron-setup > locations/`

Abrir o arquivo `ilc.json` e verificar se o e-mail que precisa ser apagado/adicionado estiver no arquivo.

Atualizar conforme solicitado no suporte e carregar/upload novamente o arquivo 

## OPDATA001

Algumas tarefas precisam serem corrigidas, por diversos motivos, erro no cadastramento, etc. Aqui alguns exemplos de tarefas operacionais

### **Mudança de tipo de pagamento do onboarding ou Taxa de Implantação.**

* Na tabela `Property Handover Details > Payment Method` guarda o tipo de pagamento 
* Ex. O pagamento era a vista `On_Budget` porém estava `Installments`


### **Mudança na data de inicio  de pagamento da taxa de implantação**

* Na tabela `Property Handover Details > Payment Method` guarda a data no campo **Created At** 
* Ex. O pagamento precisa iniciar em 01/01/2025, alterar o `Created At` no registro do codigo do imovel **Property ID**


Nota:

* Para todos os imoveis que sejam pagos a **vista(On_Budget)** ou P**ix**,  vamos ter valores **positivos** e **negativos** em
  * **Proper Pay Property Daily Implantation Fee**
  * **Proper Pay Property Daily Transfer**


* Para todos os imoveis que sejam pagos a **Abatimento(Discount_Rate)** ,  vamos ter valores apenas **positivos** em
  * **Proper Pay Property Daily Implantation Fee** 
  * **Proper Pay Property Daily Transfer**

### Cancelamento de despesas

Editar em `Financial Expense > Expense Status` conforme solicitado


### **Alterar Tempo de Preparo**

É importante que essa alteração seja feita pelo endpoint `property/manager/<property_id>`, por quê ele faz duas alterações:


1. Edita o registro atual na tabela `Property Property`;
2. Cria um novo registro de alteração na tabela de auditoria `Property Audit`.

Pra fazer alterações disso em sequência sem ter que utilizar o formulário do Front, podemos usar Swagger ou Postman com o body: `{"extra_day_preparation": 0}`, substituindo o 0 pelo valor desejado. Para fazer isso com muitas propriedades de uma vez, o ideal seria até uma confecção de um endpoint que faça esse loop ao enviar uma lista de propriedades a editar (aceitando tanto property.code quanto property.id)


### **Alterar Anfitrião de um imóvel para reservas passadas**

Quando tem migração de proprietários, também tem mudanças de anfitrião


### Deletar repasse que foi inserido por engano 

Procurar na `Financial Owner Property Ted`  pelo `PropertyID` e verificar quais registros precisam ser deletados, apos o fechamento deve refletir no sapron


## OPINATIVE - Desativar conta sapron


Para desativar contas de usuarios no sapron seguir os seguintes passos:

Desativar no django

Account user > IsActive = false 

Account host > IsHostActive= false 


teste


\

## OPPARTNER

## OPCNFS - Cidades sem o código em notas fiscais (NFs)

### Contexto

Algumas vezes pode acontecer de registros de NFs Seazoner da equipe de fechamento virem sem o código da cidade como neste [suporte](https://seazone-fund.slack.com/archives/C02H5GM0VB5/p1760368145228089) e na imagem abaixo:

 ![imagem do suporte](/api/attachments.redirect?id=7b46b4c0-3ad8-4a13-ae19-77bc0d4aad02 " =401x107")

Isso acontece devido ao preenchimento incorreto do atributo `State`, na tabela `Financial_Invoice_Details`. 

O sistema espera o padrão de sigla do estado como SC, SP, PR… e não a escrita do estado por extenso, como Santa Catarina, São Paulo, Paraná… Abaixo, o preenchimento incorreto no primeiro e terceiro registro:

 ![listagem de registros problemáticos](/api/attachments.redirect?id=b93db28b-17f2-4462-9c06-8a54f1501053 " =1434x316")

O Sapron define o código da cidade seguindo os padrões listados no repositório privado abaixo:

`https://github.com/seazone-tech/sapron-backend/blob/develop/src/account/ibgecodes.py`

 ![imagem do repositório privado de cidades](/api/attachments.redirect?id=4b72ce6d-444b-4d8f-a159-00fdd31e8481 " =342x265")

Como pode ver, é esperado que os estados estejam em formato de sigla, para que a atribuição de código da cidade seja processada da forma esperada.

### Como consertar?

Em breve, uma atualização irá obrigar que o preenchimento dos estados sejam em formato de sigla (SC, SP, PR…). Porém, caso alguma cidade ainda seja processada sem o código por algum outro motivo desconhecido, aqui está o passo a passo de como corrigir de forma manual:


1. Conecte-se a base de dados do Sapron Produção;
2. Acesse a tabela `Financial_Invoice_Details`;
3. Encontre o registro que deseja corrigir pelo `ID` ou pesquisando pelo `State` incorreto;
4. Substitua o nome do estado pela forma de sigla;
5. Salve as alterações se estiver tudo certo.

Com essas ações, ao gerar a NF novamente, as cidades que estavam sem códigos devem receber a devida numeração.


## OPTAXAF - Valores e datas das Taxas de Franquia Incorretos

Pode acontecer de valores ou datas de pagamentos da taxa de franquia apresentarem inconsistências por algum erro. Se isto acontecer, um Seazoner do financeiro apresentará o problema com a relação de datas e valores dos abatimentos corretos se for o caso, algo como a planilha abaixo:

 ![planilha fornecida com descontos corretos](/api/attachments.redirect?id=29ae876b-64c8-4ee3-8012-927f68affbb4 " =380x377")

No Sapron, essas informações podem ser visualizadas em Financeiro > Fechamento > Anfitrião; Em seguida insira o ID do anfitrião no input, ajuste o filtro para "ID Anfitrião", escolha o mês e ano, e então pesquise.

> \nVocê também pode verificar de forma mais direta, acessando a tabela `financial_host_franchise_fee_payment`, filtrando pelo ID e ordenando a data de referência (`date_ref`) em ordem crescente que ficará como a planilha então verifique os dados;\n

Em três suportes operacionais deste tipo em uma semana, o erro apresentado foi o mesmo, as últimas taxas de abatimento ficaram somadas em um único mês, em vez de ficarem distribuídas de acordo com seus descontos. Ex: na imagem de cima, as linhas 2 até a 11 constavam no Sapron conforme a planilha, enquanto os valores da 3 linhas vermelhas estavam somados em 2 meses sequênciais \[==jan/25 = R$ 2.344,22== e ==fev/25 = R$ 2.488,66==\].

O que fazer é ajustar os valores e as datas para que fique de acordo com a planilha fornecida pelo financeiro: ==abri/25 = R$ 2.542,88==; ==mai/25 = R$ 1.717,34==; e ==jun/25 = R$ 572,66==.

**Query de suporte caso precise inserir novos dados (SQL e modelo para planilhas):** 

`*INSERT INTO financial_host_franchise_fee_payment (created_at, updated_at, host_id, value, date_ref, payment_date, payment_method) VALUES (now(), now(), 194, 2000, '2025-03-01', '2025-04-10', 'commission_abatement');*`

`=CONCATENAR("INSERT INTO financial_host_franchise_fee_payment (created_at, updated_at, host_id, value, date_ref, payment_date, payment_method) VALUES (now(), now(), ";A2;", ";E2;", '";B2;"', '";C2;"', '";D2;"');")`

**Causa do problema:**

Ainda está sendo investigada, o que há em comum nestes casos, é que as inconsistências aconteceram sempre com as últimas parcelas, todas foram somadas em 1 ou 2 meses, e houve um salto entre datas. *==No exemplo da imagem acima, houveram abatimentos diretos do mês 03 até o 12 de 2024 conforme a primeira coluna, o Sapron continuou descontando em janeiro e fevereiro de 2025 incorretamente (sem imagens), já que os abatimentos da taxa de franquia reais voltaram somente em abril de 2025, ficando os meses janeiro, fevereiro e março sem descontos, como pode ver na imagem anexada.==* O Sapron parece não ter lidado bem com o período onde não houve descontos, somando os valores restantes do abatimento onde não havia movimentação da franquia.


\