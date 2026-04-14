<!-- title: Banco de dados | url: https://outline.seazone.com.br/doc/banco-de-dados-IQBobc1hYn | area: Tecnologia -->

# Banco de dados

Documentação que descreve as tabelas e campos do banco de dados do Sapron.

# Tabelas

* **Account Address**

  *account_address* é a tabela onde armazena todos os endereços num geral do Sapron, desde endereços de usuário, até endereços de fatura e imóveis.

  *Forma de input de dados*:

  *Output*:

  Campos:

| **Nome do campo** | **Descrição** |
|----|----|
| id | identificador único do registro |
| street | rua do endereço |
| number | número do endereço |
| complement | informações adicionais do endereço |
| neighborhood | o bairro do endereço |
| city | a cidade do endereço |
| state | o estado do endereço |
| postal_code | o CEP do endereço |
| country | o país do endereço |
| condominium | o condomínio do endereço |
* **Account User**

  a*ccount_user* é a tabela onde armazena todos os usuários do Sapron e seus respectivos dados (um usuário pode ser qualquer entidade do negócio, como parceiro, hóspede, anfitrião, etc).

  *Forma de input de dados*:

  *Output*:

  Campos:

| **Nome do campo** | **Descrição** |
|----|----|
| id | identificador único do registro |
| password | senha do usuário |
| last_login | data de último login do usuário |
| is_superuser | informa se o usuário é super usuário e tem permissões de administrador (verdadeiro ou falso) |
| created_at | data de criação do registro |
| updated_at | data de atualização do registro |
| first_name | primeiro nome do usuário |
| last_name | sobrenome do usuário |
| e-mail | e-mail do usuário |
| phone_number | telefone principal do usuário |
| phone_number2 | telefone secundário do usuário |
| main_role | função principal do usuário |
| gender | sexo do usuário |
| birth_date | data de nascimento do usuário |
| is_individual | informa se o usuário é pessoa física (verdadeiro ou falso) |
| id_number | número de identificação do usuário (como RG) |
| cpf | CPF do usuário |
| cnpj | CNPJ do usuário (em caso de pessoa jurídica) |
| corporate_name | razão social (em caso de pessoa jurídica) |
| trading_name | nome fantasia (em caso de pessoa jurídica) |
| is_staff | informa se o usuário é colaborador ou não (verdadeiro ou falso) |
| is_active | informa se o usuário está ativo ou não (verdadeiro ou falso) |
| main_address_id | id da tabela de endereço referente ao usuário (endereço principal) |
| postal_address_id | id da tabela de endereço referente ao usuário (endereço postal) |
| nickname | apelido do usuário |
| pipedrive_person_id | id da pessoa no Pipedrive |
* A**ccount Attendant**

  a*ccount_attendant* é a tabela onde armazena todos os atendentes e seus respectivos dados (um atendente possui todos os dados de um usuário da tabela account_user).

  *Forma de input de dados*:

  *Output*:

  Campos:

| **Nome do campo** | **Descrição** |
|----|----|
| id | identificador único do registro |
| created_at | data de criação do registro |
| updated_at | data de atualização do registro |
| user_id | id da tabela account_user referente ao atendente |
* **Account Guest**

  a*ccount_guest* é a tabela onde armazena todos os hóspedes e seus respectivos dados (um hóspede possui todos os dados de um usuário da tabela account_user).

  *Forma de input de dados*:

  *Output*:

  Campos:

| **Nome do campo** | **Descrição** |
|----|----|
| id | identificador único do registro |
| created_at | data de criação do registro |
| updated_at | data de atualização do registro |
| user_id | id da tabela account_user referente ao hóspede |
* **Account Host**

  a*ccount_host* é a tabela onde armazena todos os anfitriões e seus respectivos dados (um hóspede possui todos os dados de um usuário da tabela account_user).

  *Forma de input de dados*:

  *Output*:

  Campos:

| **Nome do campo** | **Descrição** |
|----|----|
| id | identificador único do registro |
| created_at | data de criação do registro |
| updated_at | data de atualização do registro |
| legacy_reservation_royalties |    |
| legacy_cleaning_royalties |    |
| location_id | id da tabela reservation_location referente à localização de atuação do anfitrião |
| user_id | id da tabela account_user referente ao anfitrião |
| is_host_ops | indica se o anfitrião tem funções especiais de operação (verdadeiro ou falso) |
| cleaning_comission_fee |    |
| reservation_comission_fee |    |
| default_bank_details_id | id da tabela financial_bank_details referente aos dados bancários padrão do anfitrião |
* **Account Host Profile**
* **Account Owner**

  a*ccount_owner* é a tabela onde armazena todos os proprietários e seus respectivos dados (um hóspede possui todos os dados de um usuário da tabela account_user).

  *Forma de input de dados*:

  *Output*:

  Campos:

| **Nome do campo** | **Descrição** |
|----|----|
| id | identificador único do registro |
| created_at | data de criação do registro |
| updated_at | data de atualização do registro |
| nationality | nacionalidade do proprietário |
| marital_status | estado civil do proprietário |
| profession | profissão do proprietário |
| email_for_operation | e-mail do proprietário para contato com a operação |
| invoice_address_id | id da tabela de endereço referente à fatura do proprietário |
| user_id | id da tabela de usuário referente ao proprietário |
| default_bank_details_id | id da tabela de detalhes bancários referente ao proprietário (detalhes bancários padrão) |
| default_invoice_details_id | id da tabela de detalhes de fatura referente ao proprietário (detalhes de fatura padrão) |
| hometown | cidade natal do proprietário |
| income | renda do proprietário |
| instagram_profile | perfil do instagram do proprietário |
| lives_same_town_as_property | informa se o proprietário mora na mesma cidade que alguma propriedade |
| meet_seazone | por onde o proprietário conheceu a Seazone |
| properties_owned | o número de propriedades que o proprietário possui |
| properties_to_rent | o número de propriedades para alugar que o proprietário possui |
| birth_city | cidade natal do proprietário |
| transfer_day | data em que o proprietário recebe o fechamento de seus imóveis |

  EXISTEM 2 CAMPOS COM A MESMA INFORMAÇÃO: hometown e birth_city
* **Account Owner Contacts**
* **Account Owner Profile**
* **Account Partner**

  a*ccount_partner* é a tabela onde armazena todos os parceiros e seus respectivos dados (um parceiro possui todos os dados de um usuário da tabela account_user).

  *Forma de input de dados*:

  *Output*:

  Campos:

| **Nome do campo** | **Descrição** |
|----|----|
| id | identificador único do registro |
| created_at | data de criação do registro |
| updated_at | data de atualização do registro |
| signed_contract | informa se o parceiro assinou o contrato (verdadeiro ou falso) |
| nationality | nacionalidade do parceiro |
| marital_status | estado civil do parceiro |
| profession | profissão do parceiro |
| user_id | id da tabela de usuário referente ao parceiro |
| attendant_name | o nome do atendente responsável pelo parceiro |
| attendant_phone_number | o número de telefone do atendente responsável pelo parceiro |
| executive_name | o nome do executivo responsável pelo parceiro |
| pipedrive_partner_id | id do parceiro no Pipedrive |
| pipedrive_partner_id | id do usuário no Pipedrive |
| spreadsheet_link | link do sheets do parceiro |
|    |    |
* **Account Seazone**

  a*ccount_seazone* é a tabela onde armazena os usuários com alguns acessos administrativos e seus respectivos dados (um usuário 'Seazone' possui todos os dados de um usuário da tabela account_user).

  *Forma de input de dados*:

  *Output*:

  Campos:

| **Nome do campo** | **Descrição** |
|----|----|
| id | identificador único do registro |
| created_at | data de criação do registro |
| updated_at | data de atualização do registro |
| user_id | id da tabela de usuário referente ao parceiro |
| department | o departamento em que esse usuário atua, hoje pode ser 'Administrative' ou 'Onboarding' |
* **Account User Groups**
* **Account Group Permissions**
* A**uth Group**
* **Auth Group Permissions**
* **Auth Permission**
* **Channel Manager Reservation State**

  *channel_manager_reservation_state* é a tabela que faz o mapeamento das reservas Stays <> Sapron. Armazena o id de uma reserva no Sapron e o id dessa reserva na Stays.

  *Forma de input de dados*:

  *Output*:

  Campos:

| **Nome do campo** | **Descrição** |
|----|----|
| id | identificador único do registro |
| stays_reserv_id | id da reserva na Stays |
| sapron_reserv_id | id referente à tabela 'reservation' do Sapron |
* **Django Admin Log**

  *django_admin_log* é a tabela que guarda informações de ações realizadas dentro do django admin. Essa tabela é utilizada apenas por administradores do sistema.

  *Forma de input de dados*:

  *Output*:

  Campos:

| **Nome do campo** | **Descrição** |    |
|----|----|----|
| id | identificador único do registro |    |
| action_time | data e horário da ação |    |
| object_id | id referente ao registro que sofreu a ação |    |
| object_repr | identificador do registro que sofreu alteração baseado em outro campo (ex: código) |    |
| action_flag | id da ação que foi tomada, podendo ser: 1 - ADDTION, 2 - CHANGE, 3 - DELETION (adição, alteração e exclusão) |    |
| change_message | informa quais campos e valores foram alterados |    |
| content_type_id | id da tabela 'content_type' referente ao registro |    |
| user_id | id da tabela de usuário referente ao registro |    |
* **Django Content Type**

  *django_content_type* é a tabela que faz o mapeamento dos aplicativos instalados no Django e seus respectivos modelos.

  *Forma de input de dados*:

  *Output*:

  Campos:

| **Nome do campo** | **Descrição** |
|----|----|
| id | identificador único do registro |
| app_label | nome do aplicativo instalado |
| model | nome do modelo referente ao aplicativo |
* **Django Migrations**

  *django_migrations* é a tabela que armazena as migrações que foram feitas no banco de dados pelo Django.

  *Forma de input de dados*:

  *Output*:

  Campos:

| **Nome do campo** | **Descrição** |
|----|----|
| id | identificador único do registro |
| app | nome do aplicativo em que a migração ocorreu |
| name | nome da migração |
| applied | data e hora que a migração foi aplicada |
* **Django Ses Sesstat**
* **Django Session**

  *django_session* é a tabela que armazena as sessões de usuário quando é feito o log in.

  *Forma de input de dados*:

  *Output*:

  Campos:

| **Nome do campo** | **Descrição** |
|----|----|
| session_key | identificador único do registro |
| session_data | armazena informações sobre a sessão. É um campo codificado, pode ser visualizado apenas decodificando com a chave de segredo |
| expire_date | data e hora de expiração da sessão |
* **Files** **Fileitem**

  *files_fileitem* é a tabela que armazena metadados (informações gerais) de arquivos.

  *Forma de input de dados*:

  *Output*:

  Campos:

| **Nome do campo** | **Descrição** |
|----|----|
| id | identificador único do registro |
| created_at | data de criação do registro |
| updated_at | data da última atualização do registro |
| uid | identificador único do registro mais complexo e não sequencial, o que o difere do 'id' |
| category | a categoria do arquivo (gastos, report, documento, etc) |
| name | nome do arquivo |
| url | a url do arquivo |
| size | o tamanho do arquivo |
| content_type | o formato do arquivo |
| uploaded | informa se o arquivo foi enviado ou não (verdadeiro ou falso) |
| task_id | o id de uma tarefa que roda internamente no sistema relacionada a esse arquivo (caso exista) |
* **Financial Airbnb Concilliation**
* **Financial Airbnb Payment**
* **Financial Bank**

  *financial_bank* é a tabela de registro de bancos.

  *Forma de input de dados*:

  *Output*:

  Campos:

| **Nome do campo** | **Descrição** |
|----|----|
| id | identificador único do registro |
| bank_number | o número do banco |
| long_name | nome completo do banco |
| short_name | nome curto do banco |
* **Financial Bank Details**

  *financial_bank_details* é a tabela de registra os dados bancários de um usuário.

  *Forma de input de dados*:

  *Output*:

  Campos:

| **Nome do campo** | **Descrição** |
|----|----|
| id | identificador único do registro |
| entity_name | nome do beneficiário da conta |
| branch_number | número da agênccia |
| account_number | número da conta |
| account_type | tipo de conta (poupança, corrente, etc) |
| cpf | cpf do beneficário |
| cnpj | cnpj do beneficiário |
| pix_key | chave pix do beneficiário |
| user_id | id da tabela de usuário referente ao registro |
| bank_id | id da tabela de banco referente ao registro |
| pix_key_type | tipo de chave do pix (cpf, cnpj, email, número de telefone, etc) |
* **Financial Billed Reservation**
* **Financial Expenses**

  *financial_expenses* é a tabela de registro de gastos de um imóvel/propriedade.

  *Forma de input de dados*:

  *Output*:

  Campos:

| **Nome do campo** | **Descrição** |
|----|----|
| id | identificador único do registro |
| register_date | data e horário do registro do gasto |
| expense_date | data da ocorrência do gasto em si |
| reason | motivo do gasto |
| description | descrição do gasto |
| supplier | fornecedor (entidade que recebeu o valor) |
| value | valor do gasto |
| expense_status | status do gasto |
| refund | data do reembolso |
| owner_approval | informa se o proprietário aprovou o gasto ou não |
| property_id | id da tabela de propriedade referente ao gasto |
| maintenance_image_uid | uid da tabela de arquivos referente à imagem de manutenção do gasto |
| statement_image_uid |    |
| registered_by | id da tabela de usuário referente ao usuário que registrou o gasto |
| responsible_user | id da tabela de usuário referente ao usuário responsável pelo gasto |
| pending_reason | motivo pelo qual o gasto está pendente de ser aprovado |
| paid_by | entidade que fez o reembolso do gasto (Seazone, proprietário, etc) |
| supplier_rating |    |
| approval_date | data e hora de aprovação do gasto |
| approval_user | id da tabela de usuário referente ao usuário que aprovou o reembolso |
| supplier_phonenumber | número de telefone do fornecedor |
* **Financial Expenses Files**
* **Financial Host Manual Fit**

  *financial_host_manual_fit* é a tabela de registro de ajustes manuais para anfitriões.

  *Forma de input de dados*:

  *Output*:

  Campos:

| **Nome do campo** | **Descrição** |
|----|----|
| id | identificador único do registro |
| created_at | data e horário de criação do registro |
| updated_at | data e horário da última atualização do registro |
| date_ref | data de referência do ajuste (a que mês será aplicado) |
| value | o valor em reais do ajuste |
| is_adding |    |
| host_id | id na tabela de anfitriões referente ao ajuste (a qual anfitrião o ajuste foi aplicado) |
| description | descrição do ajuste |
* **Financial Host Revenues**

  *financial_host_revenues* é a tabela de registros de receitas dos anfitriões.

  *Forma de input de dados*:

  *Output*:

  Campos:

| **Nome do campo** | **Descrição** |
|----|----|
| id | identificador único do registro |
| created_at | data e horário de criação do registro |
| updated_at | data e horário da última atualização do registro |
| reservations_amount | número de reservas realizadas pelo anfitrião |
| cleaning_amount | número de limpezas realizadas pelo anfitrião |
| onboarding_incomes | ganhos provenientes onboarding em reais |
| reservations_incomes | ganhos provenientes de reserva em reais |
| cleaning_incomes | ganhos provenientes de limpeza em reais |
| refund_expenses |    |
| onboarding_expenses | despesas de onboarding |
| legacy_royalties_seazone |    |
| transfer |    |
| host_id | id da tabela de anfitrião referente à receita |
| property_id | id da tabela de propriedade referente à receita |
| date_ref | data de referência das receitas (a que mês serão aplicadas) |
| status | status das receitas (aberta ou fechada) |
| onboarding_ley_cleaning |    |
| onboarding_laundry |    |

*financial_host_manual_fit* é a tabela de registro de ajustes manuais para anfitriões.

*Forma de input de dados*:

*Output*:

Campos:

| **Nome do campo** | **Descrição** |
|----|----|
| id | identificador único do registro |
| created_at | data e horário de criação do registro |
| updated_at | data e horário da última atualização do registro |
| date_ref | data de referência do ajuste (a que mês será aplicado) |
| value | o valor em reais do ajuste |
| is_adding | Campo que indica se o ajuste adiciona ou subtrai do saldo |
| host_id | id na tabela de anfitriões referente ao ajuste |
| description | descrição do ajuste |

* **Financial Invoice Details**

*financial_invoice_details* é a tabela de registro dos dados da fatura de um usuário.

*Forma de input de dados*:

*Output*:

Campos:

| **Nome do campo** | **Descrição** |
|----|----|
| id | identificador único do registro |
| invoice_entity_name | nome do beneficiário na fatura |
| cpf | cpf do beneficiário na fatura |
| cnpj | cnpj do beneficiário na fatura |
| email | email do beneficiário na fatura |
| user_id | id na tabela de usuário referente à fatura (usuário ao qual os dados da fatura pertencem) |
| address | endereço do beneficiário da fatura |
| address_number | número do endereço do beneficiário da fatura |
| city | cidade do endereço do beneficiário da fatura |
| complement | complemento do endereço do beneficiário da fatura |
| district | bairro do endereço do beneficiário da fatura |
| phone_number | número de telefone do beneficiário da fatura |
| postal_code | CEP do endereço do beneficiário da fatura |
| state | estado do endereço do beneficiário da fatura |

* **Financial Match Payment**
* **Financial Monthly Seazone KPI**

  *financial_monthly_seazone_kpi* é a tabela de registro do kpi de propriedades ativas

  *Forma de input de dados*:

  *Output*:

  Campos:

| **Nome do campo** | **Descrição** |
|----|----|
| id | identificador único do registro |
| created_at | data e horário de criação do registro |
| updated_at | data e horário da última atualização do registro |
| date_ref | data de referência do kpi (a que mês será aplicado) |
| active_properties | número de propriedades ativas |
* **Financial NF**

  *financial_nf* é a tabela de registro das notas fiscais.

  *Forma de input de dados*:

  *Output*:

  Campos:

| **Nome do campo** | **Descrição** |
|----|----|
| id | identificador único do registro |
| created_at | data e horário de criação do registro |
| updated_at | data e horário da última atualização do registro |
| date_ref | data de referência da nota fiscal (a que mês será aplicado) |
| comission |    |
| status |    |
| concluded_at |    |
| host_id |    |
| invoice_details_id |    |
| owner_id |    |
* **Financial NF Host**

  *financial_nf_host* é a tabela de registro ….

  *Forma de input de dados*:

  *Output*:

  Campos:

| **Nome do campo** | **Descrição** |
|----|----|
| id | identificador único do registro |
| created_at | data e horário de criação do registro |
| updated_at | data e horário da última atualização do registro |
| date_ref | data de referência da nota fiscal (a que mês será aplicado) |
| value | valor da nota fical em reais |
| host_id |    |
| invoice_details_id |    |
* **Financial OTA Payment**
* **Financial Owner Manual Fit**

  *financial_owner_manual_fit* é a tabela de registro de ajustes manuais para proprietários.

  *Forma de input de dados*:

  *Output*:

  Campos:

| **Nome do campo** | **Descrição** |
|----|----|
| id | identificador único do registro |
| created_at | data e horário de criação do registro |
| updated_at | data e horário da última atualização do registro |
| date_ref | data de referência do ajuste (a que mês será aplicado) |
| value | o valor em reais do ajuste |
| is_adding |    |
| owner_id | id na tabela de proprietário referente ao ajuste (a qual proetário o ajuste foi aplicado) |
| description | descrição do ajuste |
* **Financial Partners Comissions Allotment**
* **Financial Partners Comissions Reservation**
* **Financial Partners Comissions Withdraw Paid**
* **Financial Partners Comissions Withdraw Request**
* **Financial Property Financial Audit**

  *financial_property_financial_audit* é a tabela de custos, comissões, faturamento, receita, repasses e previsões relacionadas ao financeiro. É uma tabela que ajuda o time do faturamento e financeiro a fazer uma auditoria dos valores e pagamentos a serem realizados.

  *Forma de input de dados*:

  *Output*:

  Campos:

| **Nome do campo** | **Descrição** |
|----|----|
| id | identificador único do registro |
| created_at | data e horário de criação do registro |
| updated_at | data e horário da última atualização do registro |
| date_ref | data de referência para auditoria dos valores (a que mês será aplicado) |
| expenses_owner_prev |    |
| expenses_owner | gastos do proprietário no mês |
| expenses_seazone_prev |    |
| expenses_seazone | gastos da Seazone no mês |
| comission_prev |    |
| comission |    |
| initial_balance_prev |    |
| initial_balance | saldo inicial da propriedade no mês |
| final_balance_prev |    |
| final_balance | saldo final da propriedade no mês |
| transfer_prev |    |
| transfer | valor de repasse para o proprietário no mês |
| revenue_prev |    |
| revenue |    |
| income_prev |    |
| income |    |
| property_id | id da propriedade referente à auditoria dos valores |
* **Financial Property Manual Fit**

  *financial_property_manual_fit* é a tabela de registro de ajustes manuais para proprietários.

  *Forma de input de dados*:

  *Output*:

  Campos:

| **Nome do campo** | **Descrição** |
|----|----|
| id | identificador único do registro |
| created_at | data e horário de criação do registro |
| updated_at | data e horário da última atualização do registro |
| date_ref | data de referência do ajuste (a que mês será aplicado) |
| value | o valor em reais do ajuste |
| is_adding |    |
| property_id | id na tabela de propriedade referente ao ajuste (a qual propriedade o ajuste foi aplicado) |
| description | descrição do ajuste |
* **Financial Reservation Payment**
* **Financial Revenues**

  *financial_revenues* é a tabela …

  *Forma de input de dados*:

  *Output*:

  Campos:

| **Nome do campo** | **Descrição** |
|----|----|
| id | identificador único do registro |
| created_at | data e horário de criação do registro |
| updated_at | data e horário da última atualização do registro |
| date_ref | data de referência para auditoria dos valores (a que mês será aplicado) |
| status |    |
| status_owner |    |
| expenses_owner |    |
| expenses_seazone |    |
| expenses_host |    |
| comission |    |
| seazone_comission |    |
| initial_balance |    |
| final_balance |    |
| transfer |    |
| property_id |    |
* **Financial Revenues OTA**

  *financial_revenues_ota* é a tabela de registro de faturamento por OTA.

  *Forma de input de dados*:

  *Output*:

  Campos:

| **Nome do campo** | **Descrição** |
|----|----|
| id | identificador único do registro |
| created_at | data e horário de criação do registro |
| updated_at | data e horário da última atualização do registro |
| income_date_ref | data de referência da receita |
| revenues_date_ref | data de referência do faturamento (entrará para a receita no próximo mês) |
| value | o valor em reais do ajuste |
| ota_id | id na tabela de OTA referente ao faturamento |
| property_id | id na tabela de propriedade referente ao faturamento |
| status | status do registro (aberto ou fechado) |
* **Financial Ted Host**

  *financial_ted_host* é a tabela de registro de TEDs para anfitriões.

  *Forma de input de dados*:

  *Output*:

  Campos:

| **Nome do campo** | **Descrição** |
|----|----|
| id | identificador único do registro |
| created_at | data e horário de criação do registro |
| updated_at | data e horário da última atualização do registro |
| date_ref | data de referência da ted |
| transfer | valor do repasse em reais para o anfitrião |
| status | status do registro |
| concluded_at | data e horário da conclusão do repasse |
| bank_details_id | dados da conta bancário para qual a ted deve ser feita |
| host_id | id na tabela de anfitrião referente à TED (para qual anfitrião a ted será feita) |
| statement_image_uid |    |
* **Financial Ted Owner**

  *financial_ted_host* é a tabela de registro de TEDs para proprietários.

  *Forma de input de dados*:

  *Output*:

  Campos:

| **Nome do campo** | **Descrição** |
|----|----|
| id | identificador único do registro |
| created_at | data e horário de criação do registro |
| updated_at | data e horário da última atualização do registro |
| date_ref | data de referência da ted |
| transfer | valor do repasse em reais para o proprietário |
| status | status do registro |
| concluded_at | data e horário da conclusão do repasse |
| bank_details_id | dados da conta bancário para qual a ted deve ser feita |
| owner_id | id na tabela de proprietário referente à TED (para qual proprietário a ted será feita) |
| statement_image_uid |    |