<!-- title: _Suporte - Resoluções Operacionais OP | url: https://outline.seazone.com.br/doc/_suporte-resolucoes-operacionais-op-p9pMvt2IcE | area: Tecnologia -->

# _Suporte - Resoluções Operacionais OP

🚨 **Para todos os suportes, caso seja necessário comunicação com o cliente, abra uma MD com o cliente,** @[Roberto Campos](mention://013edfea-d215-4798-bc64-fb0691448baa/user/7a820dce-f3c4-4cd0-9054-82f4b4d27bf7)  **e @Renata Domingues para que todos possam acompanhar o chamado.**

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


 ![](/api/attachments.redirect?id=519afb87-b5af-4d23-900b-e907ccbf47b6 " =1340x545")


 ![](/api/attachments.redirect?id=c7df7af5-5fc1-4af2-b762-c3d61deb70a1 " =1363x223")


## OPPRO001 - Alterar Proprietário (login) de uma propriedade

Dados necessários:


1. `property_id` ;
2. `owner_id` ;

O que fazer:

Na tabela `property_property_owners`, procure pelo `property_id`a linha da propriedade e altere o `owner_id` relacionado a ela. 

<https://metabase.seazone.com.br/question/1184-property-owners-by-property-code>


Na tabela  `property_property`procure pelo `property_id` e altera a coluna do `owner_id`


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


**Caso 1 - Editar dados da NF**

Identifique o id (`invoice_details_id` ou `default_invoice_details_id`) na Tabela `financial_invoice_details`

e edite os dados solicitados nesse registro  


**Caso 2 - Novos dados da NF**

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

\n

* Não adianta mudar/atualizar essas tabelas com nome `proper_pay_<descricao>` pois os dados serão atualizados todo dia no aws
* Para ver as reservas os detalhes estão no *Reservation Reservation*  nos cards eles enviam o code
* \
* \


## OPMIG002 - Migrar reservas de imóvel X para imóvel Y

**Dados necessários:**

* identificar O  `Property ID` dos imóveis (X e Y) . Nesta [consulta](https://metabase.sapron.com.br/question/1092-property-owner-user-by-property-code) pode encontrar pelo `CODE` da propriedade.

  \
* Sobre as reservas que precisam migrar, identificar na Tabela `Reservation Reservation` as colunas:
  *  `reservation_id` 


  *  `Property ID`
  *  `Listing ID`

  \
* Na tabela `Reservation Listing` identificar o `ID` . Filtre pelo `Property ID` dos dos imóveis (X e Y) 
  * `Ota ID`
  * `Property ID`

  
:::warning
  Prestar atenção no Ota ID. Se o imóvel **X** tiver **OtaID=1**, então procure o **ID** com **OtaID=1** do imovel **Y**

  :::

  \

**O que fazer**

 Na na Tabela `Reservation Reservation` identifique o registro pelo `reservation_id`  que deseja migrar. Atualize as seguintes colunas:

*  `Property ID` - novo id do ***imóvel Y***
*  `Listing ID` - novo id do `Reservation Listing` associado ao ***imóvel Y*** e ao ***OtaID*** correspondente


### Porque Não migram algumas reservas?

Quando é ativado o fluxo de migração as reservas, sempre é considerado a d**ata de Ativação ou inicio de contrato do novo imóvel**. 

Exemplo o Imóvel 3924- MRE801 foi ativado o dia ***15/02/2015***

 ![](/api/attachments.redirect?id=962bd979-7e81-4842-b08a-58dd357b47ae " =732x164")

Assim reservas anteriores a essa data **>>não são migradas<<** 

**Pois temos a regra:** *"Todas as reservas tem data de checkin igual ou maior a data de Ativação do Imóvel"*\nNeste caso uma reserva com check-in 02/02/2025 não será migrada pois a data é menor do que a data de ativação do imóvel.

\n

## OPEMAIL001 - Cadastrar e-mail para envio das reservas vendidas

Acessar na `AWS > Seazone Technology > Amazon S3 > Buckets > sapron-setup > locations/`

Abrir o arquivo `ilc.json` e verificar se o e-mail que precisa ser apagado/adicionado estiver no arquivo.

Atualizar conforme solicitado no suporte e carregar/upload novamente o arquivo \n

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


\
## OPPARTNER

## 


\

\