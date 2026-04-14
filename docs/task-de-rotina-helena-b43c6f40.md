<!-- title: Task de Rotina - Helena | url: https://outline.seazone.com.br/doc/task-de-rotina-helena-1IG2sy6Y6N | area: Administrativo Financeiro -->

# Task de Rotina - Helena

\
Esse é o layout para imputar dados no Sapron.

<https://docs.google.com/spreadsheets/d/1n6cYWvBOwoHG8_IcbY081Ivb7EmzDFpu3uaGnWpDcqE/edit#gid=523501175>


Sheets automatizado, para preenchimento dos dados de imput no sapron

<https://docs.google.com/spreadsheets/d/1I0MF6sTD5RA3wLU1SgfwRHJs-QU0HGw754egVh5SgAM/edit#gid=0>


## Task de Rotina

* **Lançamento de TEDs do host, na tabela** ***financial_host_property_ted***

  Os dados deverão ser imputados seguindo a seguinte ordem e formato:
  * **created_at:** 2024-05-21 00:00:00 (data da inserção dos dados no Dbeaver)
  * **updated_at:** 2024-05-21 00:00:00 (data da inserção dos dados no Dbeaver)
  * **date_ref:** 2024-05-01 (data do mês de referência de imput dos dados)
  * **value:** 24536,52 (valores a serem imputados no Dbeaver, podendo deixar com vírgula, mas os números não podem conter o "." que separa os valores a cada 3 casas )
  * **host_id:** 123 (valor inteiro do id do host disponibilizado na tabela account host, no metabase)

  \
  \*Necessário ter baixado o DBeaver no computador

  \*\*Necessário ter acesso no Sapron

  \
* **Lançamento de TEDs do owner, na tabela** ***financial_owner_property_ted***

  Os dados deverão ser imputados seguindo a seguinte ordem e formato:
  * **created_at:** 2024-05-21 00:00:00 (data da inserção dos dados no Dbeaver)
  * **updated_at:** 2024-05-21 00:00:00 (data da inserção dos dados no Dbeaver)
  * **date_ref:** 2024-05-10 (data de pagamento)
  * **value:** 24536,52 (valores a serem imputados no Dbeaver, podendo deixar com vírgula, mas os números não podem conter o "." que separa os valores a cada 3 casas )
  * **property_id:** 123 (valor inteiro do id do imóvel disponibilizado na tabela property property, no metabase)

  \
  \*Necessário ter baixado o DBeaver no computador

  \*\*Necessário ter acesso no Sapron
* **Lançamento de Despesas da Gestão de Contas, na tabela financial_expense**

  Os dados deverão ser imputados seguindo a seguinte ordem e formato:
  * **id**: deixar essa coluna em branco
  * **register_date**: 2024-05-21 00:00:00 (data da inserção dos dados no Dbeaver)
  * **expense_date**: 2024-05-21 00:00:00 (data da despesa)
  * **reason**: Account_Management_Water (motivo da despesa)
  * **description**: Limpeza onboarding EMF1003 (descrição da despesa)
  * **supplier**: Portal material de construção (suprimento)
  * **value**: 10029,80 (valor)
  * **expense_status**: Approved (tem que ser colocado como approved)
  * **refund**: deixar essa coluna em branco
  * **owner_Approval**: true (se o proprietário aprovou a despesa, adicione o true)
  * **property_id**: 1452 (id da propriedade)
  * **maintenance_image_uid**: deixar essa coluna em branco
  * **statement_image_uid**: deixar essa coluna em branco
  * **registered_by**: 15789 (o ID do responsável pela informação - se não souber seu ID, puxe pela tabela account_user)
  * **responsible_user**: 15785 (id do host, na tabela do account_user)
  * **pending_reason**: deixar essa coluna em branco
  * **paid_by**: Owner (se for o proprietário que for pagar, deixar como owner)
  * **supplier_rating**: 5 (nota dada ao supplier)
  * **approval_date**: 2024-05-21 00:00:00 (data de aprovação)
  * **approval_user**: 14856 (id do user que aprovou)
  * **supplier_phonenumber**: +00 (00) 00000-0000 (deixar esse padrão)
  * **received_by**: deixar essa coluna em branco

  \