<!-- title: Descrição de tabelas | url: https://outline.seazone.com.br/doc/descricao-de-tabelas-bTZhA01cUa | area: Tecnologia -->

# Descrição de tabelas

# Introdução

As tabelas do SAPRON estão divididas por aplicações, referentes ao contexto de desenvolvimento do backend.

Por exmplo:

* `account_` são tabelas referente ao app account, tabelas de serviço de contas do usuario
* `financial_` são tabelas referente ao app financial, tabelas de serviço financeiro

e assim por diante.

\*\* **Exceto algumas tabelas que não possuem prefixo.conciliada**

# Lista de Tabelas

## Account

### account_address

### Modelo `address` (Endereço)

**Campos**

* **street (Texto)**: Rua do endereço. Campo que armazena o nome da rua.
* **number (Texto)**: Número do endereço. Campo opcional para armazenar o número do local.
* **complement (Texto)**: Complemento do endereço. Informações adicionais sobre o endereço, como bloco, apartamento etc. É um campo opcional.
* **neighborhood (Texto)**: Bairro do endereço. Armazena o nome do bairro.
* **city (Texto)**: Cidade do endereço. Campo para armazenar o nome da cidade.
* **state (Texto)**: Estado do endereço. Armazena o nome do estado.
* **postal_code (Texto)**: Código postal do endereço. Campo para o CEP do endereço.
* **country (Texto)**: País do endereço. Campo para armazenar o nome do país.
* **condominium (Texto)**: Condomínio do endereço. Campo opcional para o nome do condomínio, se aplicável.

### account_attendant

### **Modelo** `Attendant` (Atendente)

**Campo**

* **user (Número)**: Associa o atendente a um único usuário. Define uma relação direta com o modelo `User`, garantindo que cada atendente seja vinculado a um único usuário.

### account_guest

### **Modelo** `Guest` (Hóspede)

**Campos**

* **user (Número)**: Associa o hóspede a um único usuário. Este campo cria uma relação direta com o modelo `User`, ligando cada hóspede a um único usuário.
* **nationality (Texto)**: Nacionalidade do hóspede. Campo opcional que armazena a nacionalidade do hóspede.

### account_host

### **Modelo** `Host` (Anfitrião)

**Campos**

* **user (Número)**: Associa o anfitrião a um único usuário. Vincula cada anfitrião a um usuário específico.
* **location (Número)**: Localização associada ao anfitrião. Campo opcional que cria uma relação com o modelo `Location`.
* **legacy_reservation_royalties (Número)**: Royalties de reservas legadas do anfitrião. Campo opcional.
* **legacy_cleaning_royalties (Número)**: Royalties de limpeza legadas do anfitrião. Campo opcional.
* **reservation_commission_fee (Número)**: Taxa de comissão de reservas do anfitrião. Valor padrão é 0.08.
* **cleaning_commission_fee (Número)**: Taxa de comissão de limpeza do anfitrião. Valor padrão é 1.
* **is_host_ops (Booleano)**: Indica se o anfitrião possui um papel especial em operações. Valor padrão é False.
* **default_bank_details (Número)**: Detalhes bancários padrão do anfitrião. Campo opcional que se relaciona com o modelo `Bank_details`.

### account_host_profile

### **Modelo** `HostProfile` (Perfil de Anfitrião)

**Campos**

* **user (Número)**: Associa o perfil de anfitrião a um único usuário. Vincula cada perfil de anfitrião a um usuário específico.
* **host (Número)**: Anfitrião associado ao perfil do anfitrião. Cria uma relação com o modelo `Host`.
* **type (Texto)**: Tipo do perfil do anfitrião. Campo que armazena o tipo de perfil, baseado em um conjunto de escolhas definidas.

### account_owner

### **Modelo** `Owner` (Proprietário)

**Campos**

* **user (Número)**: Associa o proprietário a um único usuário.
* **nationality (Texto)**: Nacionalidade do proprietário. Campo opcional.
* **marital_status (Texto)**: Estado civil do proprietário. Campo opcional com um conjunto definido de escolhas.
* **profession (Texto)**: Profissão do proprietário. Campo opcional.
* **email_for_operation (Texto)**: E-mail para operações do proprietário. Campo opcional.
* **invoice_address (Número)**: Endereço de faturamento do proprietário. Relaciona-se com o modelo `Address`.
* **default_bank_details (Número)**: Detalhes bancários padrão do proprietário. Relaciona-se com o modelo `Bank_details`.
* **default_invoice_details (Número)**: Detalhes padrão da fatura do proprietário. Relaciona-se com o modelo `Invoice_details`.
* **hometown (Texto)**: Cidade natal do proprietário. Campo opcional.
* **properties_owned (Número)**: Número de propriedades possuídas pelo proprietário. Campo opcional.
* **properties_to_rent (Número)**: Número de propriedades disponíveis para alugar pelo proprietário. Campo opcional.
* **instagram_profile (Texto)**: Perfil do Instagram do proprietário. Campo opcional.
* **income (Número)**: Renda do proprietário. Valor padrão é 0.
* **lives_same_town_as_property (Booleano)**: Indica se o proprietário vive na mesma cidade que a propriedade. Campo opcional.
* **meet_seazone (Texto)**: Como o proprietário conheceu a Seazone. Campo opcional com um conjunto definido de escolhas.
* **birth_city (Texto)**: Cidade de nascimento do proprietário. Campo opcional.
* **transfer_day (Número)**: Dia de transferência do proprietário. Campo opcional.

### account_owner_contacts

### **Modelo** `OwnerContact` (Contato do Proprietário)

**Campos**

* **owner (Número)**: Associa o contato ao proprietário. Relaciona-se com o modelo `Owner`.
* **contact_name (Texto)**: Nome do contato. Campo que armazena o nome da pessoa de contato.
* **phone_number (Texto)**: Número de telefone do contato.
* **email (Texto)**: E-mail do contato. Campo opcional.
* **contact_subject (Texto)**: Assunto do contato. Campo opcional.

### account_owner_profile

### **Modelo** `OwnerProfile` (Perfil do Proprietário)

**Campos**

* **user (Número)**: Associa o perfil do proprietário a um usuário específico. Relaciona-se com o modelo `User` através de uma relação um-para-um.
* **owner (Número)**: Vincula o perfil do proprietário a um proprietário específico. Relaciona-se com o modelo `Owner`.
* **type (Texto)**: Tipo do perfil do proprietário. Campo de caracteres com escolhas pré-definidas (`OPS`, `FULL_ACCESS`).

### account_partner

### **Modelo** `Partner` (Parceiro)

**Campos**

* **user (Número)**: Associa o parceiro a um único usuário. Relaciona-se com o modelo `User` através de uma relação um-para-um.
* **signed_contract (Booleano)**: Indica se o parceiro assinou o contrato. Campo opcional.
* **nationality (Texto)**: Nacionalidade do parceiro. Campo opcional.
* **marital_status (Texto)**: Estado civil do parceiro. Campo opcional com um conjunto definido de escolhas.
* **profession (Texto)**: Profissão do parceiro. Campo opcional.
* **executive (Número)**: Nome do executivo associado ao parceiro. Campo opcional que se relaciona com o modelo `Executive`.
* **attendant_name (Texto)**: Nome do atendente do parceiro. Campo opcional.
* **attendant_phone_number (Número)**: Número de telefone do atendente do parceiro. Campo opcional.
* **spreadhsheet_link (Texto)**: Link para a planilha do parceiro. Campo opcional.

### account_seazone

### **Modelo** `Seazone`

**Campos**

* **user (Número)**: Associa a Seazone a um único usuário. Relaciona-se com o modelo `User` através de uma relação um-para-um.
* **department (Texto)**: Departamento da Seazone. Campo que armazena o departamento, com um conjunto definido de escolhas.

### account_user

### **Modelo** `User` (Usuário)

**Campos**

* **first_name (Texto)**: Primeiro nome do usuário.
* **last_name (Texto)**: Sobrenome do usuário.
* **email (Texto)**: E-mail do usuário.
* **phone_number1 (Texto)**: Primeiro número de telefone do usuário.
* **phone_number2 (Texto)**: Segundo número de telefone do usuário. Campo opcional.
* **main_role (Texto)**: Papel principal do usuário no sistema Sapron. Campo de caracteres com escolhas pré-definidas.
* **gender (Texto)**: Gênero do usuário. Campo de caracteres com escolhas pré-definidas.
* **birth_date (Número)**: Data de nascimento do usuário. Campo de data.
* **main_address (Número)**: Endereço principal do usuário. Relaciona-se com o modelo `Address`.
* **postal_address (Número)**: Endereço postal do usuário. Relaciona-se com o modelo `Address` através de uma relação um-para-um.
* **is_individual (Booleano)**: Indica se o usuário é um indivíduo.
* **id_number (Texto)**: Número de identificação do usuário. Campo opcional.
* **cpf (Texto)**: CPF do usuário. Campo opcional.
* **cnpj (Texto)**: CNPJ do usuário. Campo opcional.
* **corporate_name (Texto)**: Nome corporativo do usuário. Campo opcional.
* **trading_name (Texto)**: Nome comercial do usuário. Campo opcional.
* **is_staff (Booleano)**: Indica se o usuário é um membro da equipe.
* **is_active (Booleano)**: Indica se o usuário está ativo.
* **nickname (Texto)**: Apelido do usuário. Campo opcional.
* **pipedrive_person_id (Texto)**: ID da pessoa no Pipedrive do usuário. Campo opcional.

## ChannelManager

### channel_manager_reservation_state

### **Modelo** `Reservation_State` (Estado da Reserva)

**Campos**

* **sapron_reserv_id (Número)**: Relaciona-se com o modelo `Reservation`. Chave estrangeira que referencia o ID da reserva no sistema Sapron.
* **stays_reserv_id (Texto)**: ID único da reserva no sistema Stays. Campo de texto com um identificador único.

## Files

### files_fileitem

### **Modelo** `FileItem` (Item de Arquivo)

**Campos**

* **uid (Texto)**: Identificador único para o `FileItem`. Campo de texto, não pode ser nulo e é único.
* **category (Texto)**: Indica a categoria do `FileItem`. Campo de texto com indexação para otimização de busca.
* **name (Texto)**: Nome do arquivo, incluindo a extensão. Campo de texto validado pela função `validate_file_extension`.
* **url (Arquivo)**: URL onde o arquivo está localizado. Campo de arquivo com um limite de 512 caracteres.
* **size (Número)**: Tamanho do arquivo em bytes. Campo numérico de grande porte.
* **content_type (Texto)**: Tipo MIME do arquivo, validado pela função `validate_content_type`.
* **uploaded (Booleano)**: Indica se o arquivo foi carregado ou não. Campo booleano com valor padrão `False`.
* **task_id (Texto)**: Campo opcional que pode conter o ID de uma tarefa relacionada a este arquivo. Campo de texto, opcional.

## Financial

### financial_airbnb_conciliation

### **Modelo** `AirbnbConciliation` (Conciliação Airbnb)

**Campos**

* **airbnb_payment (Número)**: Pagamento Airbnb associado. Relaciona-se com o modelo `AirbnbPayment`.
* **reservation (Número)**: Reserva associada. Relaciona-se com o modelo `Reservation`.
* **conciliation (Booleano)**: Confirmação de conciliação. Campo opcional com valor padrão como False.
* **modified_by (Número)**: Usuário que modificou. Relaciona-se com o modelo `User`, sendo opcional.

### financial_airbnb_payment

### **Modelo** `AirbnbPayment` (Pagamento Airbnb)

**Campos**

* **reservation (Número)**: Relaciona-se com o modelo `Reservation`. Chave estrangeira que associa o pagamento a uma reserva.
* **amount_paid (Número)**: Quantia paga. Armazena um número decimal, ideal para representar valores monetários.
* **confirmation_code (Texto)**: Código de confirmação na OTA (Online Travel Agency).
* **payment_date (Número)**: Data do pagamento na OTA. Campo de data.
* **payment_type (Texto)**: Tipo de pagamento. Campo de texto, opcional.
* **host_fee (Número)**: Taxa do anfitrião. Número decimal, opcional.
* **cleaning_fee (Número)**: Taxa de limpeza. Número decimal, opcional.

### financial_bank

### **Modelo** `Bank` (Banco)

**Campos**

* **bank_number (Texto)**: Número do banco. Campo que armazena o número de identificação do banco.
* **long_name (Texto)**: Nome completo do banco. Campo que armazena o nome completo do banco.
* **short_name (Texto)**: Nome abreviado do banco. Campo que armazena o nome abreviado do banco.

### financial_bank_details

### **Modelo** `Bank_details` (Detalhes Bancários)

**Campos**

* **bank (Número)**: Banco associado. Relaciona-se com o modelo `Bank`.
* **entity_name (Texto)**: Nome da entidade. Campo que armazena o nome da entidade associada à conta bancária.
* **branch_number (Texto)**: Número da agência. Campo que armazena o número da agência bancária.
* **account_number (Texto)**: Número da conta. Campo que armazena o número da conta bancária.
* **account_type (Texto)**: Tipo de conta. Campo com um conjunto definido de escolhas para o tipo de conta bancária.
* **cpf (Texto)**: CPF do usuário. Campo que armazena o CPF associado à conta bancária.
* **cnpj (Texto)**: CNPJ do usuário. Campo que armazena o CNPJ associado à conta bancária.
* **pix_key (Texto)**: Chave Pix. Campo que armazena a chave Pix associada à conta bancária.
* **user (Número)**: Usuário associado. Relaciona-se com o modelo `User`.
* **pix_key_type (Texto)**: Tipo de chave Pix. Campo com um conjunto definido de escolhas para o tipo de chave Pix.

### financial_billed_reservation

### **Modelo** `BilledReservation` (Reserva Faturada)

**Campos**

* **revenue_ota (Número)**: Associa a reserva faturada a uma receita específica da OTA (Online Travel Agency). Relaciona-se com o modelo `RevenueOTA`.
* **reservation (Número)**: Vincula a reserva faturada a uma reserva específica. Relaciona-se com o modelo `Reservation`.

### financial_cleaning_fee_manual_fit

### **Modelo** `CleaningFeeManualFit` (Ajuste Manual da Taxa de Limpeza)

**Campos**

* **date_ref (Data)**: Data de referência do ajuste manual da taxa de limpeza. Campo que armazena a data do ajuste.
* **value (Número)**: Valor do ajuste manual da taxa de limpeza. Campo que armazena o valor do ajuste.
* **is_adding (Booleano)**: Indica se o valor é somado. Valor padrão é True.
* **description (Texto)**: Descrição do ajuste manual da taxa de limpeza. Campo opcional que armazena uma descrição detalhada do ajuste.
* **reservation (Número)**: Reserva associada ao ajuste manual. Relaciona-se com o modelo `Reservation`.
* **problem_type (Texto)**: Tipo de problema do ajuste manual. Campo com um conjunto definido de escolhas para categorizar o tipo de problema.
* **problem_description (Texto)**: Descrição do problema do ajuste manual. Campo opcional que fornece detalhes adicionais sobre o problema.

### financial_expenses

### **Modelo** `Expenses` (Despesas)

**Campos**

* **property (Número)**: Relaciona-se com o modelo `Property`. Chave estrangeira que associa as despesas a uma propriedade específica.
* **register_date (Número)**: Data de registro da despesa.
* **expense_date (Número)**: Data em que a despesa foi efetuada.
* **reason (Texto)**: Motivo da despesa. Campo de caracteres com escolhas pré-definidas.
* **description (Texto)**: Descrição breve da despesa.
* **supplier (Texto)**: Nome do fornecedor.
* **supplier_phonenumber (Texto)**: Número de telefone do fornecedor.
* **value (Número)**: Valor da despesa. Número decimal.
* **expense_status (Texto)**: Status da despesa. Campo de caracteres com escolhas pré-definidas.
* **refund (Número)**: Data de reembolso da despesa.
* **registered_by (Número)**: Usuário que registrou a despesa. Relaciona-se com o modelo `User`.
* **responsible_user (Número)**: Usuário responsável pela despesa. Relaciona-se com o modelo `User`.
* **statement_image (Número)**: Imagem do extrato associada à despesa. Relaciona-se com o modelo `FileItem`.
* **maintenance_image (Número)**: Imagem de manutenção associada à despesa. Relaciona-se com o modelo `FileItem`.
* **owner_approval (Booleano)**: Aprovação do proprietário para a despesa.
* **pending_reason (Texto)**: Descrição do motivo pelo qual a despesa está pendente.
* **paid_by (Texto)**: Quem pagou a despesa. Campo de caracteres com escolhas pré-definidas.
* **received_by (Texto)**: Quem recebeu a despesa. Campo de caracteres com escolhas pré-definidas.
* **supplier_rating (Número)**: Avaliação do fornecedor. Número decimal.
* **approval_date (Número)**: Data e hora da aprovação da despesa.
* **approval_user (Número)**: Usuário que aprovou a despesa. Relaciona-se com o modelo `User`.

### financial_expensesfiles

### **Modelo** `ExpensesFiles` (Arquivos de Despesas)

**Campos**

* **expense (Número)**: Despesa associada. Relaciona-se com o modelo `Expenses`.
* **file (Número)**: Arquivo associado. Relaciona-se com o modelo `FileItem`.
* **category (Texto)**: Categoria do arquivo. Campo com um conjunto definido de escolhas para categorizar o tipo de arquivo, como "Maintenance File" ou "Statement File".

### financial_host_manual_fit

### **Modelo** `Host_Manual_Fit` (Ajuste Manual do Anfitrião)

**Campos**

* **date_ref (Número)**: Data de referência para o ajuste. Campo de data.
* **value (Número)**: Valor do ajuste. Número decimal.
* **is_adding (Booleano)**: Indica se o valor está sendo somado (verdadeiro) ou subtraído (falso).
* **description (Texto)**: Descrição breve do ajuste.
* **host (Número)**: Relaciona-se com o modelo `Host`. Chave estrangeira que associa o ajuste a um anfitrião específico.

### financial_host_revenues

### **Modelo** `Host_Revenues` (Receitas do Anfitrião)

**Campos**

* **date_ref (Data)**: Data de referência para a receita (mês-ano).
* **reservations_amount (Número)**: Número de reservas.
* **cleaning_amount (Número)**: Número de limpezas.
* **reservations_incomes (Número)**: Valor da receita proveniente das reservas.
* **cleaning_incomes (Número)**: Valor da receita proveniente das limpezas.
* **refund_expenses (Número)**: Valor de reembolso por despesas.
* **onboarding_incomes (Número)**: Valores provenientes da Comissão de Onboarding.
* **onboarding_laundry (Número)**: Valores provenientes da lavanderia de Onboarding.
* **onboarding_key_cleaning (Número)**: Valores provenientes da limpeza de chaves de Onboarding.
* **onboarding_expenses (Número)**: Valores provenientes de despesas administrativas de Onboarding.
* **legacy_royalties_seazone (Número)**: Taxa da Seazone.
* **transfer (Número)**: Valor a ser transferido em Reais (R$).
* **status (Texto)**: Status atual. Campo com um conjunto definido de escolhas para o status.
* **host (Número)**: Anfitrião associado. Relaciona-se com o modelo `Host`.
* **property (Número)**: Propriedade associada. Relaciona-se com o modelo `Property`.

### financial_invoice_details

### **Modelo** `Invoice_details` (Detalhes da Fatura)

**Campos**

* **invoice_entity_name (Texto)**: Nome da entidade da fatura.
* **cpf (Texto)**: CPF associado à fatura.
* **cnpj (Texto)**: CNPJ associado à fatura.
* **email (Texto)**: E-mail associado à fatura.
* **phone_number (Texto)**: Número de telefone associado à fatura.
* **postal_code (Texto)**: Código postal associado à fatura.
* **address (Texto)**: Endereço associado à fatura.
* **address_number (Texto)**: Número do endereço associado à fatura.
* **complement (Texto)**: Complemento do endereço associado à fatura.
* **district (Texto)**: Distrito ou bairro associado à fatura.
* **city (Texto)**: Cidade associada à fatura.
* **state (Texto)**: Estado associado à fatura.
* **user (Número)**: Relaciona-se com o modelo `User`. Chave estrangeira que associa os detalhes da fatura a um usuário específico.

### financial_match_payment

### **Modelo** `Match_payment` (Correspondência de Pagamento)

**Campos**

* **payment (Número)**: Pagamento associado. Relaciona-se com o modelo `Ota_payment`.
* **reservation (Número)**: Reserva associada. Relaciona-se com o modelo `Reservation`.

### financial_monthly_seazone_kpi

### **Modelo** `MonthlySeazoneKPI` (KPI Mensal da Seazone)

**Campos**

* **date_ref (Número)**: Data de referência para o KPI. Campo de data.
* **active_properties (Número)**: Quantidade de propriedades ativas. Campo que armazena um número inteiro grande.

### financial_nf

### **Modelo** `NF` (Nota Fiscal)

**Campos**

* **owner (Número)**: Relaciona-se com o modelo `Owner`. Chave estrangeira que associa a nota fiscal a um proprietário específico.
* **host (Número)**: Relaciona-se com o modelo `Host`. Chave estrangeira que associa a nota fiscal a um anfitrião específico.
* **invoice_details (Número)**: Relaciona-se com o modelo `Invoice_details`. Chave estrangeira que associa a nota fiscal a detalhes de faturamento específicos.
* **date_ref (Número)**: Data de referência da nota fiscal. Campo de data.
* **commission (Número)**: Valor da comissão. Número decimal.
* **status (Texto)**: Status da nota fiscal. Campo de caracteres com escolhas pré-definidas (`Not_Concluded`, `Concluded`, `Pending`).
* **concluded_at (Número)**: Data e hora de conclusão da nota fiscal. Campo opcional.

### financial_nf_host

### **Modelo** `NFHost` (Nota Fiscal do Anfitrião)

**Campos**

* **date_ref (Data)**: Data de referência para a nota fiscal.
* **host (Número)**: Anfitrião associado. Relaciona-se com o modelo `Host`.
* **invoice_details (Número)**: Detalhes da fatura associada. Relaciona-se com o modelo `Invoice_details`. Campo opcional.
* **value (Número)**: Valor da nota fiscal.

### financial_ota_payment

### **Modelo** `Ota_payment` (Pagamento OTA)

**Campos**

* **id_payout (Texto)**: Identificador do pagamento.
* **ota_name (Texto)**: Nome da OTA (Online Travel Agency) associada ao pagamento.
* **payout (Número)**: Valor do pagamento.
* **check_in_date (Data)**: Data de check-in associada ao pagamento.
* **check_out_date (Data)**: Data de check-out associada ao pagamento.
* **pay_date (Data)**: Data do pagamento.
* **listing_id (Texto)**: Identificador do anúncio.
* **bank_account (Texto)**: Informação da conta bancária.
* **booker_first_name (Texto)**: Primeiro nome do responsável pela reserva.
* **booker_last_name (Texto)**: Sobrenome do responsável pela reserva.
* **guest_first_name (Texto)**: Primeiro nome do hóspede.
* **guest_last_name (Texto)**: Sobrenome do hóspede.
* **reservation_code (Texto)**: Código da reserva.
* **entry_type (Texto)**: Tipo de entrada. Campo opcional.
* **final_amount (Número)**: Valor final do pagamento.

### financial_owner_manual_fit

### **Modelo** `Owner_Manual_Fit` (Ajuste Manual do Proprietário)

**Campos**

* **date_ref (Número)**: Data de referência para o ajuste. Campo de data.
* **value (Número)**: Valor do ajuste. Número decimal.
* **is_adding (Booleano)**: Indica se o valor está sendo somado (verdadeiro) ou subtraído (falso).
* **description (Texto)**: Descrição breve do ajuste.
* **owner (Número)**: Relaciona-se com o modelo `Owner`. Chave estrangeira que associa o ajuste a um proprietário específico.

### financial_owner_property_ted

### **Modelo** `OwnerPropertyTed` (TED de Proprietário de Propriedade)

**Campos**

* **property (Número)**: Relaciona-se com o modelo `Property`. Chave estrangeira que referencia a propriedade associada à transferência TED.
* **date_ref (Data)**: Data de referência para a TED.
* **value (Número)**: Valor transferido na TED. Número de ponto flutuante.

### financial_partner_commission_allotment

### **Modelo** `CommissionsAllotment` (Comissão de Alocação)

**Campos**

* **value (Número)**: Valor da comissão. Campo herdado do modelo `Commission`, armazena o valor da comissão.
* **date_ref (Data)**: Data de referência da comissão. Campo herdado do modelo `Commission`, armazena a data relacionada à comissão.
* **allotment_indication (Número)**: Indicação de alocação associada. Relaciona-se com o modelo `IndicationsAllotment`.

### financial_partner_commission_property

### **Modelo** `CommissionsProperty` (Comissão de Propriedade)

**Campos**

* **value (Número)**: Valor da comissão. Campo que armazena um número de ponto flutuante.
* **date_ref (Número)**: Data de referência da comissão. Campo de data.
* **property_indication (Número)**: Relaciona-se com o modelo `IndicationsProperty`. Chave estrangeira que associa a comissão de propriedade a uma indicação de propriedade específica.
* **property (Número)**: Relaciona-se com o modelo `Property`. Chave estrangeira que associa a comissão à propriedade específica.
* **partner (Número)**: Relaciona-se com o modelo `Partner`. Chave estrangeira que associa a comissão ao parceiro responsável.

### financial_partner_withdraw

### **Modelo** `CommissionsWithdraw` (Retirada de Comissão)

**Campos**

* **partner (Número)**: Parceiro que solicitou a retirada. Relaciona-se com o modelo `Partner`.
* **bank_details (Número)**: Detalhes bancários para a retirada da comissão. Relaciona-se com o modelo `Bank_details`.
* **value (Número)**: Valor da retirada. Campo que armazena o valor a ser retirado.
* **invoice_notice (Booleano)**: Indica se há aviso de fatura. Valor padrão é False.
* **status (Texto)**: Status da retirada. Campo com um conjunto definido de escolhas para o status, como "Paid", "Requested", "Approved" ou "Denied".
* **date_requested (Data)**: Data do pedido de retirada. Valor padrão é a data atual.
* **date_paid (Data)**: Data em que a comissão foi paga. Campo opcional.
* **payment_method (Texto)**: Método de pagamento da retirada. Campo com um conjunto definido de escolhas, como "PIX" ou "TED".

### financial_property_manual_fit

### **Modelo** `Property_Manual_Fit` (Ajuste Manual da Propriedade)

**Campos**

* **date_ref (Número)**: Data de referência para o ajuste. Campo de data.
* **value (Número)**: Valor do ajuste. Número decimal.
* **is_adding (Booleano)**: Indica se o valor está sendo somado (verdadeiro) ou subtraído (falso).
* **description (Texto)**: Descrição breve do ajuste.
* **property (Número)**: Relaciona-se com o modelo `Property`. Chave estrangeira que associa o ajuste a uma propriedade específica.

### financial_reservation_manual_fit

### **Modelo** `ReservationManualFit` (Ajuste Manual da Reserva)

**Campos**

* **date_ref (Número)**: Data de referência para o ajuste manual. Campo de data.
* **value (Número)**: Valor do ajuste manual. Número de ponto flutuante.
* **is_adding (Booleano)**: Indica se o valor está sendo somado (verdadeiro) ou subtraído (falso).
* **problem_type (Texto)**: Tipo de problema que motivou o ajuste. Campo de caracteres com escolhas pré-definidas (`DISCOUNT`, `CANCELLATION_FEE`, `ADJUSTMENT`, `EARLY_CHECK_OUT`, `OTHER`).
* **problem_description (Texto)**: Descrição do problema que levou ao ajuste. Campo de texto, opcional.
* **guest_departure_date (Número)**: Data de partida do hóspede da reserva associada ao ajuste. Campo de data, opcional.
* **description (Texto)**: Descrição detalhada do motivo do ajuste. Campo de texto, opcional.
* **reservation (Número)**: Relaciona-se com o modelo `Reservation`. Chave estrangeira que associa o ajuste manual a uma reserva específica.

### financial_reservation_payment

### **Modelo** `Reservation_Payment` (Pagamento de Reserva)

**Campos**

* **reservation (Número)**: Relaciona-se com o modelo `Reservation`. Chave estrangeira que associa o pagamento a uma reserva específica.
* **depositor (Texto)**: Nome da pessoa ou entidade que realizou o pagamento.
* **date (Número)**: Data e hora do registro do pagamento. Campo de data e hora.
* **value (Número)**: Valor do pagamento. Número de ponto flutuante.
* **receipt_image (String)**: Relaciona-se com o modelo `FileItem`. Chave estrangeira que associa o pagamento a uma imagem do recibo.
* **payment_method (Texto)**: Método de pagamento utilizado. Campo de caracteres com escolhas pré-definidas (`TED`, `PIX`, `PAYPAL`, `CREDIT_CARD`, `DEPOSIT`).
* **destination_bank_account (Texto)**: Conta bancária de destino do pagamento. Campo de caracteres com escolhas pré-definidas (`SEAZONE_SERVICES`, `KHANTO_RESERVATIONS`).

### financial_revenues

### **Modelo** `Revenues` (Receitas)

**Campos**

* **date_ref (Data)**: Data de referência para a receita (mês-ano). Atenção: ignorar o dia deste campo.
* **initial_balance (Número)**: Valor do saldo inicial em Reais (R$).
* **final_balance (Número)**: Valor do saldo final em Reais (R$).
* **transfer (Número)**: Valor a ser transferido em Reais (R$).
* **expenses_owner (Número)**: Despesas da propriedade pagas pelo proprietário em Reais (R$).
* **expenses_host (Número)**: Despesas da propriedade pagas pelo anfitrião em Reais (R$). Valor padrão é 0.
* **expenses_seazone (Número)**: Despesas da propriedade pagas pela Seazone em Reais (R$). Valor padrão é 0.
* **commission (Número)**: Comissão do anfitrião em Reais (R$). Valor padrão é 0.
* **seazone_commission (Número)**: Comissão da Seazone em Reais (R$). Valor padrão é 0.
* **status (Texto)**: Status da receita. Campo com um conjunto definido de escolhas para o status, como "Open" (não verificado pela Seazone) ou "Closed" (verificado).
* **status_owner (Texto)**: Status da receita para o proprietário. Indica se a receita para o proprietário foi verificada.
* **property (Número)**: Propriedade associada. Relaciona-se com o modelo `Property`.

### financial_revenues_ota

### **Modelo** `Revenues_OTA` (Receitas OTA)

**Campos**

* **revenues_date_ref (Data)**: Data de referência para a receita (mês-ano).
* **income_date_ref (Data)**: Data de referência para o rendimento (mês-ano).
* **value (Número)**: Valor em Reais (R$). Campo que armazena o valor da receita.
* **status (Texto)**: Status da receita. Campo com um conjunto definido de escolhas para o status, como "Open" (não verificado pela Seazone) ou "Closed" (verificado).
* **property (Número)**: Propriedade associada. Relaciona-se com o modelo `Property`.
* **ota (Número)**: OTA associada. Relaciona-se com o modelo `OTA`.

### financial_ted_host

### **Modelo** `TedHost` (TED do Anfitrião)

**Campos**

* **host (Número)**: Referência ao anfitrião da conta. Relaciona-se com o modelo `Host`.
* **bank_details (Número)**: Referência aos detalhes bancários associados à TED. Relaciona-se com o modelo `Bank_details`.
* **date_ref (Data)**: Data de referência para a TED.
* **transfer (Número)**: Valor transferido na TED.
* **status (Texto)**: Status da TED. Campo com um conjunto definido de escolhas para o status, incluindo opções como "Not Concluded", "Concluded", "Pending" ou "Exception".
* **concluded_at (Data)**: Data e hora em que a TED foi concluída. Campo opcional.
* **statement_image (Número)**: Referência à imagem do extrato da TED. Relaciona-se com o modelo `FileItem`.

### financial_ted_owner

### **Modelo** `TedOwner` (Proprietário de TED)

**Campos**

* **owner (Número)**: Relaciona-se com o modelo `Owner`. Chave estrangeira que referencia o proprietário da conta associada à transferência TED.
* **bank_details (Número)**: Relaciona-se com o modelo `Bank_details`. Chave estrangeira que referencia os detalhes bancários associados à TED.
* **date_ref (Data)**: Data de referência para a TED. Campo de data.
* **transfer (Número)**: Valor transferido na TED. Número decimal.
* **status (Texto)**: Status da TED. Campo de caracteres com escolhas pré-definidas (`NOT_CONCLUDED`, `CONCLUDED`, `PENDING`, `EXCEPTION`).
* **concluded_at (Data)**: Data e hora de conclusão da TED. Campo de data e hora, opcional.
* **statement_image (String)**: Relaciona-se com o modelo `FileItem`. Chave estrangeira que referencia a imagem do extrato da TED.

### financial_ted_property_host

### **Modelo** `TedPropertyHost` (TED do Anfitrião da Propriedade)

**Campos**

* **property (Número)**: Referência à propriedade associada à TED. Relaciona-se com o modelo `Property`.
* **bank_details (Número)**: Referência aos detalhes bancários associados à TED. Relaciona-se com o modelo `Bank_details`.
* **date_ref (Data)**: Data de referência para a TED.
* **transfer (Número)**: Montante transferido na TED.
* **status (Texto)**: Status da TED. Campo com um conjunto definido de escolhas para o status, incluindo opções como "Not Concluded", "Concluded", "Pending" ou "Exception".
* **concluded_at (Data e Hora)**: Data e hora em que a TED foi concluída. Campo opcional.
* **statement_image (Número)**: Referência à imagem do extrato da TED. Relaciona-se com o modelo `FileItem`.

### financial_ted_property_owner

### **Modelo** `TedPropertyOwner` (TED do Proprietário da Propriedade)

**Campos**

* **property (Número)**: Relaciona-se com o modelo `Property`. Chave estrangeira que referencia a propriedade associada à transferência TED.
* **bank_details (Número)**: Relaciona-se com o modelo `Bank_details`. Chave estrangeira que referencia os detalhes bancários associados à TED.
* **date_ref (Data)**: Data de referência para a TED.
* **transfer (Número)**: Valor transferido na TED. Número decimal.
* **status (Texto)**: Status da TED. Campo de caracteres com escolhas pré-definidas (`NOT_CONCLUDED`, `CONCLUDED`, `PENDING`, `EXCEPTION`).
* **concluded_at (Data)**: Data e hora de conclusão da TED. Opcional.
* **statement_image (String)**: Relaciona-se com o modelo `FileItem`. Chave estrangeira que referencia a imagem do extrato da TED.

## Partner

### partners_executive

### **Modelo** `Executive` (Executivo de Indicação)

**Campos**

* **full_name (Texto)**: O nome completo do executivo. Este campo é usado para armazenar o nome completo do executivo responsável por indicações ou outras tarefas relacionadas.
* **pipedrive_person_id (Texto)**: O ID da pessoa no Pipedrive do executivo. Este campo opcional é usado para armazenar o identificador único do executivo no sistema Pipedrive, facilitando a integração e o rastreamento de atividades relacionadas a ele no CRM.
* **option_id (Texto)**: ID de opção do executivo no Pipedrive. Este campo é utilizado para identificar especificamente o executivo dentro de opções ou listas no sistema Pipedrive, ajudando na organização e na referência cruzada de informações.

### partners_indications_allotment

### **Modelo** `IndicationsAllotment` (Indicação de Loteamento)

**Campos**

* **allotment_city (Texto)**: Cidade do loteamento. Armazena a cidade onde o loteamento está localizado.
* **allotment_state (Texto)**: Estado do loteamento. Guarda o estado onde o loteamento está situado.
* **allotment_street (Texto)**: Rua do loteamento. Registra o nome da rua do loteamento.
* **allotment_address_number (Texto)**: Número do endereço do loteamento. Indica o número do local do loteamento.
* **geographical_coordinate (Texto)**: Coordenada geográfica do loteamento. Fornece as coordenadas geográficas do loteamento.
* **allotment_area (Texto)**: Área do loteamento. Descreve a área total do loteamento.
* **allotment_dimension (Texto)**: Dimensão do loteamento. Detalha as dimensões específicas do loteamento.
* **document_link (Texto)**: Link para o documento do loteamento. Fornece um link para acessar documentos relacionados ao loteamento.
* **allotment_value (Número)**: Valor do loteamento. Indica o valor financeiro atribuído ao loteamento.
* **allow_barter (Booleano)**: Permite permuta. Especifica se a permuta é permitida para o loteamento.
* **allotment_neighborhood (Texto)**: Bairro do loteamento. Identifica o bairro onde o loteamento está localizado.

### partners_indications_allotment_file

### **Modelo** `IndicationsAllotmentFile` (Arquivo de Indicação de Loteamento)

**Campos**

* **allotment_indication (Número)**: Chave estrangeira que se relaciona com o modelo `IndicationsAllotment`. Representa uma ligação para uma indicação de loteamento específica.
* **file (Número)**: Chave estrangeira que se relaciona com o modelo `FileItem`. Representa um arquivo associado a uma indicação de loteamento, identificado pelo campo `uid` do modelo `FileItem`.

### partners_indications_investment

### **Modelo** `IndicationsInvestment` (Indicação de Investimento)

**Campos**

* **partner (Número)**: Chave estrangeira que se relaciona com o modelo `Partner`. Representa o parceiro que indicou o investimento. Campo opcional.
* **enterprise_unit (Número)**: Chave estrangeira para o modelo `EnterpriseUnit`. Representa a unidade empresarial associada à indicação de investimento.
* **enterprise (Número)**: Chave estrangeira para o modelo `Enterprise`. Representa a empresa associada à indicação de investimento.
* **investor_name (Texto)**: Nome do investidor. Campo de texto, opcional.
* **investor_email (Texto)**: Email do investidor. Campo de texto, opcional.
* **investor_phone (Texto)**: Telefone do investidor. Campo de texto, opcional.
* **status (Texto)**: O status atual da indicação. Campo de texto com escolhas pré-definidas como `IN_PROGRESS`, `WON`, etc.
* **comment (Texto)**: Comentário adicional sobre a indicação. Campo de texto, opcional.
* **commission (Número)**: Porcentagem de comissão do parceiro. Número decimal, valor padrão 0.02.
* **pipedrive_stage (Texto)**: Etapa no Pipedrive. Campo de texto com escolhas pré-definidas como `NEW_LEAD`, `CONNECTION`, etc.
* **pipedrive_deal_id (Texto)**: Identificador do negócio no Pipedrive. Campo de texto, opcional.
* **lost_reason (Texto)**: Motivo da perda da indicação. Campo de texto, opcional.

### partners_indications_investment_file

### **Modelo** `IndicationsInvestmentFile` (Arquivo de Indicação de Investimento)

**Campos**

* **investment_indication (Número)**: Chave estrangeira para o modelo `IndicationsInvestment`. Vincula o arquivo a uma indicação de investimento específica.
* **file (Número)**: Chave estrangeira para o modelo `FileItem`. Relaciona o arquivo com um item de arquivo específico, permitindo o armazenamento e referência a documentos ou imagens associadas à indicação de investimento.

### partners_indications_property

### **Modelo** `IndicationsProperty` (Indicação de Propriedade)

**Campos**

* **property_city (Texto)**: Cidade da propriedade. Armazena a cidade onde a propriedade está localizada.
* **property_state (Texto)**: Estado da propriedade. Guarda o estado onde a propriedade está situada.
* **property_street (Texto)**: Rua da propriedade. Registra o nome da rua da propriedade.
* **property_neighborhood (Texto)**: Bairro da propriedade. Identifica o bairro onde a propriedade está localizada.
* **property_number (Texto)**: Número da propriedade. Indica o número do local da propriedade.
* **property_complement (Texto)**: Complemento do endereço da propriedade. Fornece informações adicionais sobre o endereço da propriedade.
* **property_type (Texto)**: Tipo da propriedade (Casa, Apartamento, Hotel). Especifica o tipo da propriedade.
* **due_date (Data)**: Data de vencimento. Indica a data limite para a indicação.
* **property (Número)**: Chave estrangeira para o modelo `Property`. Vincula a indicação a uma propriedade específica.
* **property_is_in_coverage_area (Booleano)**: A propriedade está na área de cobertura da Seazone? Especifica se a propriedade está na área de cobertura.
* **property_under_construction (Booleano)**: A propriedade está em construção? Indica se a propriedade está atualmente em construção.
* **property_has_furniture (Booleano)**: A propriedade possui mobília? Especifica se a propriedade já está mobiliada.
* **owner_is_aware_of_indication (Booleano)**: O proprietário está ciente da indicação? Indica se o proprietário da propriedade tem conhecimento da indicação.
* **owner_received_the_ebook (Booleano)**: O proprietário recebeu o e-book? Especifica se o e-book foi enviado ao proprietário.
* **pipedrive_stage (Texto)**: Estágio no Pipedrive. Identifica em qual estágio do funil do Pipedrive a indicação se encontra.
* **pipedrive_deal_id (Texto)**: Identificador de negócio no Pipedrive. Fornece o identificador do negócio associado no Pipedrive.
* **owner_name (Texto)**: Nome do proprietário da propriedade. Armazena o nome do proprietário.
* **owner_phone_number (Texto)**: Telefone do proprietário da propriedade. Registra o número de telefone do proprietário.
* **owner_email (Texto)**: Email do proprietário da propriedade. Fornece o endereço de email do proprietário.
* **status (Texto)**: Status atual da indicação. Indica o status atual da indicação, como em andamento, ganho, perdido ou cancelado.
* **status_change_date (Data e hora)**: Data e hora da última mudança de status. Registra quando foi a última vez que o status da indicação foi alterado.

### partners_indications_property_file

### **Modelo** `IndicationsPropertyFile` (Arquivo de Indicação de Propriedade)

**Campos**

* **property_indication (Número)**: Chave estrangeira que se relaciona com o modelo `IndicationsProperty`. Representa uma ligação para uma indicação de propriedade específica.
* **file (Número)**: Chave estrangeira que se relaciona com o modelo `FileItem`. Representa um arquivo associado a uma indicação de propriedade, identificado pelo campo `uid` do modelo `FileItem`.

## ProperPay

### proper_pay_host_daily_balance

### **Modelo** `HostDailyBalance` (Saldo Diário do Anfitrião)

**Campos**

* **date (Data)**: Data do saldo diário. Campo que armazena a data a que se refere o saldo.
* **value (Número)**: Valor do saldo diário. Campo que armazena o valor do saldo para o anfitrião na data especificada.
* **host (Número)**: Anfitrião associado aos dados do saldo diário. Relaciona-se com o modelo `Host`.

### proper_pay_host_daily_commission

### **Modelo** `HostDailyCommission` (Comissão Diária do Anfitrião)

**Campos**

* **date (Data)**: Data da comissão diária.
* **value (Número)**: Valor da comissão diária. Número de ponto flutuante.
* **property (Número)**: Relaciona-se com o modelo `Property`. Chave estrangeira que referencia a propriedade associada à comissão diária.
* **host (Número)**: Relaciona-se com o modelo `Host`. Chave estrangeira que referencia o anfitrião associado aos dados da comissão diária.

### proper_pay_host_daily_manual_fit

### **Modelo** `HostDailyManualFit` (Ajuste Manual Diário do Anfitrião)

**Campos**

* **accrual_date (Data)**: Data de competencia em caixa do ajuste manual. Campo que armazena a data em que o ajuste manual se reflete no caixa.
* **cash_date (Data)**: Data de caixa para o ajuste manual. Campo que armazena a data em que o ajuste manual é reconhecido contabilmente.
* **value (Número)**: Valor do ajuste manual. Campo que armazena o valor do ajuste manual para o anfitrião nas datas especificadas.
* **host (Número)**: Anfitrião associado aos dados do ajuste manual diário. Relaciona-se com o modelo `Host`.

### proper_pay_host_daily_revenue

### **Modelo** `HostDailyRevenue` (Receita Diária do Anfitrião)

**Campos**

* **accrual_date (Data)**: Data de competência para a receita. Indica quando a receita é reconhecida contabilmente.
* **cash_date (Data)**: Data de caixa para a receita. Refere-se à data em que a receita foi efetivamente realizada ou registrada no caixa.
* **value (Número)**: Valor da receita. Número de ponto flutuante.
* **host (Número)**: Relaciona-se com o modelo `Host`. Chave estrangeira que referencia o anfitrião associado aos dados da receita diária.

### proper_pay_host_daily_transfer

### **Modelo** `HostDailyTransfer` (Transferência Diária do Anfitrião)

**Campos**

* **value (Número)**: Valor da transferência diária. Número de ponto flutuante.
  * **date (Data)**: Data da transferência diária.
* **property (Número)**: Relaciona-se com o modelo `Property`. Chave estrangeira que referencia a propriedade associada à transferência diária.
* **host (Número)**: Relaciona-se com o modelo `Host`. Chave estrangeira que referencia o anfitrião associado aos dados da transferência diária.

### proper_pay_host_monthly

### **Modelo** `HostMonthly` (Dados Mensais do Anfitrião)

**Campos**

* **host (Número)**: Relaciona-se com o modelo `Host`. Chave estrangeira que referencia o anfitrião associado aos dados mensais.
* **revenue (Número)**: Receita gerada. Número de ponto flutuante.
* **cleaning_fee (Número)**: Valor da taxa de limpeza. Número de ponto flutuante.
* **onboarding_expenses (Número)**: Valor das despesas de integração. Número de ponto flutuante.
* **manual_fit (Número)**: Valor do ajuste manual. Número de ponto flutuante.
* **commission (Número)**: Valor da comissão. Número de ponto flutuante.
* **refund_expenses (Número)**: Valor das despesas de reembolso. Número de ponto flutuante.
* **debited_expenses (Número)**: Valor das despesas debitadas. Número de ponto flutuante.
* **transfer (Número)**: Valor da transferência. Número de ponto flutuante.
* **month_ref (Data)**: Mês de referência para os dados. Campo de data.

### proper_pay_host_ted_nf_value

### **Modelo** `HostTedNFValue` (Valor da TED NF do Anfitrião)

**Campos**

* **month_ref (Data)**: Mês de referência para os dados da TED NF. Campo que armazena o mês ao qual se refere o valor da TED NF.
* **value (Número)**: Valor da TED NF. Campo que armazena o valor da TED (Transferência Eletrônica Disponível) para o anfitrião no mês especificado.
* **host (Número)**: Anfitrião associado aos dados da TED NF. Relaciona-se com o modelo `Host`.

### proper_pay_owner_daily_balance

### **Modelo** `OwnerDailyBalance` (Saldo Diário do Proprietário)

**Campos**

* **date (Data)**: Data do saldo diário.
* **value (Número)**: Valor do saldo diário. Número de ponto flutuante.
* **owner (Número)**: Relaciona-se com o modelo `Owner`. Chave estrangeira que referencia o proprietário associado aos dados do saldo diário.

### proper_pay_owner_daily_commission

### **Modelo** `OwnerDailyCommission` (Comissão Diária do Proprietário)

**Campos**

* **date (Data)**: Data da comissão diária.
* **value (Número)**: Valor da comissão diária. Número de ponto flutuante.
* **owner (Número)**: Relaciona-se com o modelo `Owner`. Chave estrangeira que referencia o proprietário associado aos dados da comissão diária.

### proper_pay_owner_daily_expenses

### **Modelo** `OwnerDailyExpenses` (Despesas Diárias do Proprietário)

**Campos**

* **accrual_date (Data)**: Data de competência para as despesas. Indica quando as despesas são reconhecidas contabilmente.
* **cash_date (Data)**: Data de caixa para as despesas. Refere-se à data em que as despesas são efetivamente realizadas ou registradas no caixa.
* **value (Número)**: Valor das despesas diárias. Número de ponto flutuante.
* **owner (Número)**: Relaciona-se com o modelo `Owner`. Chave estrangeira que referencia o proprietário associado aos dados das despesas diárias.

### proper_pay_owner_daily_manual_fit

### **Modelo** `OwnerDailyManualFit` (Ajuste Manual Diário do Proprietário)

**Campos**

* **accrual_date (Data)**: Data de competência. Refere-se à data em que o ajuste manual é reconhecido contabilmente.
* **cash_date (Data)**: Data de caixa. Indica a data em que o ajuste manual se reflete no caixa.
* **value (Número)**: Valor do ajuste manual diário. Campo que armazena o valor do ajuste manual para o proprietário nas datas especificadas.
* **owner (Número)**: Proprietário associado aos dados do ajuste manual diário. Relaciona-se com o modelo `Owner`.

### proper_pay_owner_daily_revenue

### **Modelo** `OwnerDailyRevenue` (Receita Diária do Proprietário)

**Campos**

* **accrual_date (Data)**: Data de competência. Refere-se à data em que a receita é reconhecida contabilmente, independentemente de quando o dinheiro é fisicamente recebido.
* **cash_date (Data)**: Data de caixa. Indica a data em que a receita é efetivamente recebida e refletida no caixa.
* **value (Número)**: Valor da receita diária. Campo que armazena o valor da receita diária associada ao proprietário nas datas especificadas.
* **owner (Número)**: Proprietário associado aos dados da receita diária. Relaciona-se com o modelo `Owner`.

### proper_pay_owner_daily_transfer

### **Modelo** `OwnerDailyTransfer` (Transferência Diária do Proprietário)

**Campos**

* **date (Data)**: Data da transferência diária. Campo que armazena a data a que se refere a transferência.
* **value (Número)**: Valor da transferência diária. Campo que armazena o valor da transferência para o proprietário na data especificada.
* **owner (Número)**: Proprietário associado aos dados da transferência diária. Relaciona-se com o modelo `Owner`.

### proper_pay_owner_monthly

### **Modelo** `OwnerMonthly` (Dados Mensais do Proprietário)

**Campos**

* **owner (Número)**: Proprietário associado aos dados mensais. Relaciona-se com o modelo `Owner`.
* **revenue (Número)**: Receita gerada. Campo que armazena o valor da receita gerada pelo proprietário no mês de referência.
* **expenses (Número)**: Valor das despesas. Campo que armazena o valor das despesas do proprietário no mês de referência.
* **manual_fit (Número)**: Valor do ajuste manual. Campo que armazena o valor de ajustes manuais para o proprietário no mês de referência.
* **commission (Número)**: Montante da comissão. Campo que armazena o valor da comissão paga ao proprietário no mês de referência.
* **transfer (Número)**: Montante transferido. Campo que armazena o valor transferido para o proprietário no mês de referência.
* **month_ref (Data)**: Mês de referência para os dados. Campo que armazena o mês ao qual se referem os dados financeiros.

### proper_pay_partner_daily_balance

### **Modelo** `PartnerDailyBalance` (Saldo Diário do Parceiro)

**Campos**

* **date (Data)**: Data do saldo diário.
* **value (Número)**: Valor do saldo diário. Número de ponto flutuante.
* **partner (Número)**: Relaciona-se com o modelo `Partner`. Chave estrangeira que referencia o parceiro associado aos dados do saldo diário.

### proper_pay_partner_daily_commission

### **Modelo** `PartnerDailyCommission` (Comissão Diária do Parceiro)

**Campos**

* **date (Data)**: Data da comissão diária.
* **value (Número)**: Valor da comissão diária. Número de ponto flutuante.
* **property (Número)**: Relaciona-se com o modelo `Property`. Chave estrangeira que referencia a propriedade associada aos dados da comissão diária.
* **partner (Número)**: Relaciona-se com o modelo `Partner`. Chave estrangeira que referencia o parceiro associado aos dados da comissão diária.

### proper_pay_partner_daily_revenue

### **Modelo** `PartnerDailyRevenue` (Receita Diária do Parceiro)

**Campos**

* **accrual_date (Data)**: Data de competência para a receita. Indica quando a receita é reconhecida contabilmente.
* **cash_date (Data)**: Data de caixa para a receita. Refere-se à data em que a receita foi efetivamente realizada ou registrada no caixa.
* **value (Número)**: Valor da receita diária. Número de ponto flutuante.
* **partner (Número)**: Relaciona-se com o modelo `Partner`. Chave estrangeira que referencia o parceiro associado aos dados da receita diária.

### proper_pay_partner_monthly

### **Modelo** `PartnerMonthly` (Dados Mensais do Parceiro)

**Campos**

* **partner (Número)**: Parceiro associado aos dados mensais. Relaciona-se com o modelo `Partner`.
* **revenue (Número)**: Receita mensal. Campo que armazena o valor da receita gerada pelo parceiro no mês de referência.
* **commission (Número)**: Comissão mensal. Campo que armazena o valor da comissão atribuída ao parceiro no mês de referência.
* **month_ref (Data)**: Mês de referência para os dados. Campo que armazena o mês ao qual se referem os dados financeiros.

### proper_pay_property_daily_balance

### **Modelo** `PropertyDailyBalance` (Saldo Diário da Propriedade)

**Campos**

* **date (Data)**: Data do saldo diário da propriedade.
* **value (Número)**: Valor do saldo diário. Número de ponto flutuante.
* **property (Número)**: Relaciona-se com o modelo `Property`. Chave estrangeira que referencia a propriedade associada ao saldo diário.

### proper_pay_property_daily_expenses

### **Modelo** `PropertyDailyExpenses` (Despesas Diárias da Propriedade)

**Campos**

* **accrual_date (Data)**: Data de competência. Refere-se à data em que a despesa foi reconhecida contabilmente para a propriedade.
* **cash_date (Data)**: Data de caixa. Indica a data em que a despesa foi efetivamente paga e refletida no caixa para a propriedade.
* **value (Número)**: Valor líquido da despesa diária. Campo que armazena o valor da despesa diária associada à propriedade nas datas especificadas.
* **reason (Texto)**: Motivo da despesa. Campo opcional que explica o motivo da despesa.
* **paid_by (Texto)**: Quem pagou a despesa. Campo opcional que identifica quem foi o responsável pelo pagamento da despesa.
* **responsible_user (Número)**: Usuário responsável pela despesa. Campo que armazena um identificador único para o usuário responsável pela despesa.
* **property (Número)**: Propriedade associada aos dados da despesa diária. Relaciona-se com o modelo `Property`.

### proper_pay_property_daily_implantation_fee

### **Modelo** `PropertyDailyImplantationFee` (Taxa Diária de Implantação da Propriedade)

**Campos**

* **accrual_date (Data)**: Data de competência para a taxa de implantação. Indica quando a taxa é reconhecida contabilmente.
* **cash_date (Data)**: Data de caixa para a taxa de implantação. Refere-se à data em que o ajuste de caixa para a taxa ocorreu.
* **implantation_fee (Número)**: Valor da taxa de implantação. Pode ser um número positivo ou negativo, representando o valor da taxa.
* **property (Número)**: Relaciona-se com o modelo `Property`. Chave estrangeira que referencia a propriedade associada aos dados da taxa de implantação diária.

### proper_pay_property_daily_manual_fit

### **Modelo** `PropertyDailyManualFit` (Ajuste Manual Diário da Propriedade)

**Campos**

* **accrual_date (Data)**: Data de competência. Refere-se à data em que o ajuste manual foi reconhecido contabilmente para a propriedade.
* **cash_date (Data)**: Data de caixa. Indica a data em que o ajuste manual foi refletido no caixa para a propriedade.
* **value (Número)**: Valor do ajuste manual. Campo que armazena o valor do ajuste manual para a propriedade na data especificada. Este valor pode ser negativo.
* **property (Número)**: Propriedade associada aos dados do ajuste manual diário. Relaciona-se com o modelo `Property`.

### proper_pay_property_daily_net_cleaning_fee

### **Modelo** `PropertyDailyNetCleaningFee` (Taxa Diária Líquida de Limpeza da Propriedade)

**Campos**

* **accrual_date (Data)**: Data em que a taxa de limpeza foi reconhecida contabilmente.
* **cash_date (Data)**: Data em que o valor em dinheiro foi recebido.
* **net_cleaning_fee (Número)**: Valor líquido da taxa de limpeza diária. Número de ponto flutuante.
* **listing (Número)**: Relaciona-se com o modelo `Listing`. Chave estrangeira que referencia uma listagem única.
* **reservation (Número)**: Relaciona-se com o modelo `Reservation`. Chave estrangeira que referencia uma reserva única.
* **code (Texto)**: Identificador universalmente único (UUID) para a entrada de reserva.
* **has_extension (Booleano)**: Indica se a reserva tem uma extensão. Campo booleano.
* **property (Número)**: Relaciona-se com o modelo `Property`. Chave estrangeira que referencia a propriedade associada aos dados da taxa de limpeza diária.

### proper_pay_property_daily_revenue

### **Modelo** `PropertyDailyRevenue` (Receita Diária da Propriedade)

**Campos**

* **accrual_date (Data)**: Data de competência para a receita. Indica quando a receita é reconhecida contabilmente.
* **cash_date (Data)**: Data de caixa para a receita. Refere-se à data em que a receita foi efetivamente realizada ou registrada no caixa.
* **daily_net_value (Número)**: Valor líquido da receita diária. Número de ponto flutuante.
* **listing (Número)**: Relaciona-se com o modelo `Listing`. Chave estrangeira que referencia uma listagem única.
* **reservation (Número)**: Relaciona-se com o modelo `Reservation`. Chave estrangeira que referencia uma reserva única.
* **code (Texto)**: Identificador universalmente único (UUID) para a entrada de receita.
* **is_extension (Booleano)**: Indica se a entrada é uma extensão. Campo booleano.
* **property (Número)**: Relaciona-se com o modelo `Property`. Chave estrangeira que referencia a propriedade associada aos dados da receita diária.

### proper_pay_property_daily_ted

### **Modelo** `PropertyDailyTed` (TED Diário da Propriedade)

**Campos**

* **accrual_date (Data)**: Data de competência. Refere-se à data em que o TED (Transferência Eletrônica Disponível) é reconhecido contabilmente para a propriedade.
* **cash_date (Data)**: Data de caixa. Indica a data em que o valor do TED é efetivamente recebido e refletido no caixa para a propriedade.
* **value (Número)**: Valor do TED diário da propriedade. Campo que armazena o valor do TED diário associado à propriedade nas datas especificadas.
* **property (Número)**: Propriedade associada aos dados do TED diário. Relaciona-se com o modelo `Property`.

### proper_pay_property_daily_transfer

### **Modelo** `PropertyDailyTransfer` (Transferência Diária da Propriedade)

**Campos**

* **date (Data)**: Data da transferência diária da propriedade.
* **value (Número)**: Valor da transferência diária. Número de ponto flutuante.
* **property (Número)**: Relaciona-se com o modelo `Property`. Chave estrangeira que referencia a propriedade associada à transferência.
* **type (Texto)**: Tipo da transferência. Campo de texto, opcional.
* **description (Texto)**: Descrição da transferência. Campo de texto, opcional.

### proper_pay_property_monthly_data

### **Modelo** `PropertyMonthly` (Dados Mensais da Propriedade)

**Campos**

* **property (Número)**: Propriedade associada aos dados mensais. Relaciona-se com o modelo `Property`.
* **revenue (Número)**: Receita total do mês. Campo que armazena o valor total da receita gerada pela propriedade no mês de referência.
* **cleaning_fee (Número)**: Total das taxas de limpeza para o mês. Campo que armazena o valor total das taxas de limpeza no mês.
* **expenses (Número)**: Outras despesas diversas para o mês. Campo que armazena o valor total de outras despesas no mês.
* **manual_fit (Número)**: Ajustes manuais feitos aos dados mensais. Campo que armazena o valor de ajustes manuais nos dados do mês.
* **implantation_fee (Número)**: Taxas relacionadas à implantação da propriedade. Campo que armazena o valor das taxas de implantação no mês.
* **owner_ted (Número)**: TED (Transferência Eletrônica Disponível) para o proprietário da propriedade. Campo que armazena o valor transferido para o proprietário no mês.
* **month_ref (Data)**: Data de referência indicando o mês do registro. Campo que armazena o mês ao qual os dados financeiros se referem.

### proper_pay_property_nf_value

### **Modelo** `PropertyNFValue` (Valor da Nota Fiscal da Propriedade)

**Campos**

* **month_ref (Data)**: Mês de referência para o valor da Nota Fiscal (NF). Campo que armazena o mês ao qual se refere o valor da NF.
* **value (Número)**: Valor monetário da NF. Campo que armazena o valor da Nota Fiscal associada à propriedade para o mês especificado.
* **property (Número)**: Propriedade associada aos dados da NF. Relaciona-se com o modelo `Property`.

### proper_pay_property_ted_value

### **Modelo** `PropertyTedValue` (Valor TED da Propriedade)

**Campos**

* **month_ref (Data)**: Mês de referência para o valor TED.
* **value (Número)**: Valor monetário da TED. Número de ponto flutuante.
* **property (Número)**: Relaciona-se com o modelo `Property`. Chave estrangeira que referencia a propriedade associada aos dados TED.

### proper_pay_seazone_daily_commission

### **Modelo** `SeazoneDailyCommission` (Comissão Diária da Seazone)

**Campos**

* **date (Data)**: Data da comissão diária. Refere-se à data em que a comissão é aplicada.
* **value (Número)**: Valor da comissão diária. Campo que armazena o valor da comissão associada à Seazone na data especificada.
* **fee (Número)**: Taxa associada à comissão diária. Campo que armazena o valor da taxa relacionada à comissão.
* **property (Número)**: Propriedade associada aos dados da comissão diária. Relaciona-se com o modelo `Property`.

## Property

### property_attendant_time_in_property

### **Modelo** `Attendant_time_in_property` (Tempo de Permanência do Atendente na Propriedade)

**Campos**

* **property (Número)**: Relaciona-se com o modelo `Property`. Chave estrangeira que referencia a propriedade associada.
* **attendant (Número)**: Relaciona-se com o modelo `Attendant`. Chave estrangeira que referencia o atendente associado.
* **attendant_start_date (Data)**: Data de início da permanência do atendente na propriedade. Campo de data, opcional.
* **attendant_end_date (Data)**: Data de término da permanência do atendente na propriedade. Campo de data, opcional.

### property_audit

### **Modelo** `PropertyAudit` (Auditoria da Propriedade)

**Campos**

* **property_id (Número)**: ID da propriedade associada ao log.
* **property_created_at (Data e Hora)**: Data e hora de criação da propriedade.
* **property_updated_at (Data e Hora)**: Data e hora da última atualização da propriedade.
* **code (Texto)**: Código único da propriedade.
* **category_location_id, category_id, address_id, etc. (Número)**: IDs associados a diferentes aspectos da propriedade, como localização, categoria e endereço.
* **comission_fee, single_bed_quantity, double_bed_quantity, etc. (Número/Decimal)**: Diversas informações quantitativas e financeiras sobre a propriedade.
* **property_type, status, etc. (Texto)**: Informações descritivas sobre a propriedade.
* **activation_date, inactivation_date, etc. (Data)**: Datas relevantes para o ciclo de vida da propriedade.
* **host_id, partner_id (Número)**: IDs associados ao anfitrião e ao parceiro da propriedade.
* **cover_image_uid (Texto)**: Identificador único da imagem de capa da propriedade.
* **bank_details_id, invoice_details_id (Número)**: IDs associados a detalhes bancários e de faturamento.
* **extra_day_preparation, is_to_keep_funds_in_seazone (Booleano)**: Informações sobre a preparação da propriedade e gestão de fundos.
* **host_reservation_comission_fee, host_cleaning_comission_fee (Número)**: Taxas de comissão associadas ao anfitrião.
* **operation (Texto)**: Ação realizada no log (Criar, Atualizar, Excluir).
* **changed_at (Data e Hora)**: Data e hora da mudança no log.
* **modifier (Texto)**: Identifica o agente da mudança (Usuário, Celery, BD).
* **changed_by_user_id (Número)**: ID do usuário que realizou a mudança.
* **changed_by_celery_task (Texto)**: Tarefa do Celery que realizou a mudança.
* **fields_changed (Texto)**: Campos que foram alterados.

### property_bed_arrangement

### **Modelo** `PropertyBedArrangement` (Arranjo de Camas da Propriedade)

**Campos**

* **property (Número)**: Propriedade associada. Relaciona-se com o modelo `Property`. Este campo estabelece uma referência à propriedade à qual o arranjo de camas pertence.
* **bed_arrangement (Texto)**: Tipo de arranjo de cama na propriedade. Campo que armazena o tipo de arranjo de cama, com opções como "Cama de Casal", "Duas Camas de Solteiro", "Cama Extra", "Sofá-Cama" e "Berço".

### property_category

### **Modelo** `Category` (Categoria)

**Campos**

* **code (Texto)**: Código da categoria. Campo de texto com um máximo de 255 caracteres. Cada categoria tem um código único.

### property_categorylocation

### **Modelo** `CategoryLocation` (CategoriaLocalização)

**Campos**

* **category (Número)**: Relaciona-se com o modelo `Category`. Chave estrangeira que referencia a categoria associada.
* **location (Número)**: Relaciona-se com o modelo `Location`. Chave estrangeira que referencia a localização associada.
* **revenue_goal (Número)**: Meta de receita para a combinação específica de categoria e localização. Número decimal, sendo opcional.

### property_comments

### **Modelo** `PropertyComment` (Comentário da Propriedade)

**Campos**

* **property (Número)**: Propriedade associada. Relaciona-se com o modelo `Property`. Este campo estabelece uma referência à propriedade à qual o comentário pertence.
* **user (Número)**: Usuário que fez o comentário. Relaciona-se com o modelo `User`. Indica o autor do comentário.
* **status (Texto)**: Status do comentário. Campo que armazena o status do comentário, com opções como "Ativo" ou "Inativo".
* **comment (Texto)**: Texto do comentário. Campo que armazena o conteúdo do comentário feito sobre a propriedade.

### property_documents

### **Modelo** `PropertyDocument` (Documento da Propriedade)

**Campos**

* **property (Número)**: Relaciona-se com o modelo `Property`. Chave estrangeira que referencia a propriedade associada.
* **category (Texto)**: Categoria do documento. Campo de caracteres com escolhas pré-definidas, como `CONTRACT`, `INSURANCE_POLICY`, `PROFESSIONAL_INSPECTION`, `HOST_INSPECTION`, `OTHER`.
* **document (Número)**: Relaciona-se com o modelo `FileItem`. Chave estrangeira que referencia o documento associado à propriedade.

### property_handover_details

### **Modelo** `PropertyHandoverDetails` (Detalhes de Entrega da Propriedade)

**Campos**

* **property (Número)**: Propriedade associada. Relaciona-se com o modelo `Property`. Campo que estabelece a referência à propriedade em questão.
* **amenities (Número)**: Comodidades associadas. Relaciona-se com o modelo `Property_amenities`. Campo opcional.
* **rules (Número)**: Regras associadas. Relaciona-se com o modelo `Property_rules`. Campo opcional.
* **bed_linen_photo (Número)**: Foto da roupa de cama. Relaciona-se com o modelo `FileItem`. Campo opcional.
* **implantation_items_description (Texto)**: Descrição dos itens de implantação.
* **onboarding_contact_phonenumber (Texto)**: Número de telefone do contato de onboarding.
* **onboarding_contact_name (Texto)**: Nome do contato de onboarding.
* **comment (Texto)**: Comentários.
* **indicator_name (Texto)**: Nome do indicador.
* **setup_value, photographer_value, bed_linen_value, full_inspection_value (Número)**: Valores de configuração, fotógrafo, roupa de cama e inspeção completa.
* **plan (Texto)**: Plano de entrega. Campo com um conjunto definido de escolhas para o plano.
* **property_area_size_m2 (Número)**: Tamanho da área da propriedade em metros quadrados. Campo opcional.
* **payment_method (Texto)**: Método de pagamento. Campo com um conjunto definido de escolhas para o método de pagamento.
* **payment_installments (Número)**: Número de parcelas do pagamento. Campo opcional.
* **implantation_fee_total_value (Número)**: Valor total da taxa de implantação. Campo opcional.
* **pipedrive_deal_id (Número)**: Identificador do negócio no Pipedrive. Campo opcional.

### property_host_time_in_property

### **Modelo** `Host_time_in_property` (Tempo de Permanência do Anfitrião na Propriedade)

**Campos**

* **property (Número)**: Relaciona-se com o modelo `Property`. Chave estrangeira que referencia a propriedade afetada.
* **old_host (Número)**: Relaciona-se com o modelo `Host` (como `old_host`). Chave estrangeira que referencia o anfitrião que foi substituído.
* **new_host (Número)**: Relaciona-se com o modelo `Host` (como `new_host`). Chave estrangeira que referencia o novo anfitrião da propriedade.
* **replacement_date (Data)**: Data em que a substituição do anfitrião tornou-se efetiva. Campo de data, opcional.

### property_location

### **Modelo** `Location` (Localização)

**Campos**

* **code (Texto)**: Código único da localização. Campo que armazena um identificador único para cada localização.
* **neighborhood (Texto)**: Bairro. Campo que armazena o nome do bairro da localização.
* **region (Texto)**: Região. Campo que armazena o nome da região da localização.
* **city (Texto)**: Cidade. Campo que armazena o nome da cidade da localização.
* **state (Texto)**: Estado. Campo que armazena o nome do estado da localização.
* **country (Texto)**: País. Campo que armazena o nome do país da localização.

### property_location_bed_arrangement

### **Modelo** `PropertyLocationBedArrangement` (Arranjo de Camas da Localização da Propriedade)

**Campos**

* **location (Número)**: Relaciona-se com o modelo `Location`. Chave estrangeira que referencia a localização associada.
* **bed_arrangement (Texto)**: Tipo de arranjo de cama na localização. Campo de caracteres com escolhas pré-definidas, como `DOUBLE_BED`, `TWO_SINGLE_BEDS`, `EXTRA_BED`, `SOFA_BED`, `CRADLE`.

### property_onboarding

### **Modelo** `PropertyOnboarding` (Onboarding da Propriedade)

**Campos**

* **property (Número)**: Propriedade submetida ao processo de onboarding. Relaciona-se com o modelo `Property`.
* **key_available_at, key_collect_scheduled_at, key_collected_at (Data)**: Datas relacionadas à disponibilidade, agendamento e coleta da chave da propriedade.
* **info_collected_at (Data)**: Data em que as informações foram coletadas.
* **is_adequacy_necessary (Booleano)**: Indica se a adequação da propriedade é necessária.
* **adequacy_available_at, adequacy_finished_at (Data)**: Datas relacionadas à disponibilidade e conclusão do processo de adequação da propriedade.
* **inspection_scheduled_at, inspection_received_at, inspection_signed_at (Data)**: Datas relacionadas ao agendamento, recebimento e assinatura da inspeção da propriedade.
* **photo_scheduled_at, photo_received_at, photo_added_at (Data)**: Datas relacionadas ao agendamento, recebimento e adição de fotografias da propriedade.
* **advertise_airbnb_created_at, advertise_booking_created_at, advertise_stays_created_at (Data)**: Datas de criação dos anúncios da propriedade em diferentes plataformas.
* **is_onboarding_completed (Booleano)**: Indica se o processo de onboarding foi concluído.
* **pipefy_card_id (Texto)**: ID do cartão Pipefy associado ao onboarding. (Campo comentado no modelo original)

### property_owner_time_in_property

### **Modelo** `Owner_time_in_property` (Tempo do Proprietário na Propriedade)

**Campos**

* **property (Número)**: Propriedade associada. Relaciona-se com o modelo `Property`.
* **owner (Número)**: Proprietário associado. Relaciona-se com o modelo `Owner`.
* **owner_start_date (Data)**: Data de início do período em que o proprietário está associado à propriedade. Campo opcional que armazena a data de início da associação do proprietário com a propriedade.
* **owner_end_date (Data)**: Data de término do período em que o proprietário está associado à propriedade. Campo opcional que armazena a data de término da associação do proprietário com a propriedade.

### property_property

Modelo `Property` (Propriedade)

Campos

* **code (Texto)**: Código identificador da propriedade.
* **category_location (Número)**: Categoria de localização associada à propriedade. Relaciona-se com o modelo `CategoryLocation`.
* **category (Número)**: Categoria da propriedade. Relaciona-se com o modelo `Category`.
* **region (Texto)**: Região da propriedade.
* **address (Número)**: Endereço da propriedade. Relaciona-se com o modelo `Address`.
* **comission_fee (Número)**: Taxa de comissão da propriedade.
* **single_bed_quantity (Número)**: Quantidade de camas simples.
* **double_bed_quantity (Número)**: Quantidade de camas duplas.
* **queen_bed_quantity (Número)**: Quantidade de camas queen.
* **king_bed_quantity (Número)**: Quantidade de camas king.
* **single_sofa_bed_quantity (Número)**: Quantidade de sofá cama simples.
* **double_sofa_bed_quantity (Número)**: Quantidade de sofá cama duplo.
* **pillow_quantity (Número)**: Quantidade de travesseiros.
* **bedroom_quantity (Número)**: Quantidade de quartos.
* **bathroom_quantity (Número)**: Quantidade de banheiros.
* **lavatory_quantity (Número)**: Quantidade de lavatórios.
* **cleaning_fee (Número)**: Taxa de limpeza da propriedade.
* **bond_amount (Número)**: Valor do título da propriedade.
* **guest_capacity (Número)**: Capacidade máxima de hóspedes.
* **property_type (Texto)**: Tipo da propriedade, com opções como "Casa", "Apartamento", "Hotel".
* **status (Texto)**: Status da propriedade, com opções como "Ativo", "Inativo", "Em onboarding".
* **activation_date (Data)**: Data de ativação da propriedade.
* **inactivation_date (Data)**: Data de inativação da propriedade.
* **contract_start_date (Data)**: Data de início do contrato.
* **contract_end_date (Data)**: Datas de fim do contrato.
* **host (Número)**: Anfitrião associado à propriedade. Relaciona-se com o modelo `Host`.
* **owners (Número)**: Proprietários associados à propriedade. Relaciona-se com o modelo `Owner` (muitos para muitos).
* **partner (Número)**: Parceiro associado à propriedade. Relaciona-se com o modelo `Partner`.
* **cover_image (Número)**: Imagem de capa da propriedade. Relaciona-se com o modelo `FileItem`.
* **balance_discount_rate (Número)**: Taxa de desconto de saldo, taxa de comissão de reserva e limpeza do anfitrião.
* **host_reservation_comission_fee (Número)**: Taxa de comissão de reserva do anfitrião.
* **host_cleaning_comission_fee (Número)**: Taxa de comissão de limpeza do anfitrião.
* **bank_details (Número)**: Detalhes bancários da propriedade. Relacionam-se com o modelo `Bank_details`.
* **invoice_details (Número)**: Detalhes da fatura da propriedade. Relacionam-se com o modelo `Invoice_details`.
* **extra_day_preparation (Booleano)**: Se a propriedade precisa de um dia extra de preparação apos um check out.
* **is_to_keep_funds_in_seazone (Booleano)**: Se o proprietário deseja depósito automático dos rendimentos.
* **churn (Booleano)**: Mostra se está ou não em processo de churn
* **churn date (data)**: Data que foi colocado em processo de churn.

### property_property_amenities

### **Modelo** `Property_amenities` (Comodidades da Propriedade)

**Campos**

Este modelo contém uma lista extensiva de comodidades para uma propriedade, com cada comodidade representada por um campo booleano. Os campos indicam a presença (True) ou ausência (False) de cada comodidade na propriedade. Aqui estão alguns dos campos principais e seu significado:

* **property (Número)**: Relaciona-se com o modelo `Property`. Chave estrangeira que referencia a propriedade associada.
* **basic (Booleano)**: Indica se a propriedade tem comodidades básicas.
* **air_conditioning, kitchen, wifi, etc. (Booleanos)**: Indicam a presença de comodidades específicas, como ar-condicionado, cozinha, Wi-Fi, etc.
* **jacuzzi, swimming_pool, tv, etc. (Booleanos)**: Indicam comodidades especiais como jacuzzi, piscina, televisão, etc.
* **security features (Booleanos)**: Indicam a presença de recursos de segurança como alarme de monóxido de carbono, extintor de incêndio, kit de primeiros socorros, etc.
* **family amenities (Booleanos)**: Indicam comodidades para famílias, como banheira para bebês, portões de segurança para bebês, jogos de tabuleiro, etc.
* **kitchen amenities (Booleanos)**: Indicam comodidades específicas da cozinha, como máquina de café, micro-ondas, geladeira, etc.
* **outdoor amenities (Booleanos)**: Indicam comodidades ao ar livre, como churrasqueira, área de jantar ao ar livre, jardim ou quintal, etc.
* **parking and accessibility (Booleanos)**: Indicam opções de estacionamento e acessibilidade, como carregador elétrico para carros, estacionamento na rua gratuito ou pago, etc.

### property_property_daily_price

### **Modelo** `Property_daily_price` (Preço Diário da Propriedade)

**Campos**

* **property (Número)**: Relaciona-se com o modelo `Property`. Chave estrangeira que referencia a propriedade associada.
* **date (Data)**: Data para a qual o preço é definido.
* **price (Número)**: Preço de referência para a data especificada. Número decimal com duas casas decimais.
* **min_stays (Número)**: Número mínimo de estadias (noites) exigido. Um número inteiro positivo.

### property_property_images

### **Modelo** `Property_images` (Imagens da Propriedade)

**Campos**

* **property (Número)**: Relaciona-se com o modelo `Property`. Chave estrangeira que referencia a propriedade associada.
* **image (Número)**: Relaciona-se com o modelo `FileItem`. Chave estrangeira que referencia a imagem associada à propriedade.

### property_property_owners

### **Modelo Abstrato** `PropertyOwners` criado a partir de relacionamento muitos para muitos

**Campos**

* **property (Número)**: Relaciona-se com o modelo `Property`. Chave estrangeira que referencia a propriedade associada.
* **owner (Número)**: Relaciona-se com o modelo `Owner`. Chave estrangeira que referencia proprietário associada à propriedade.

### property_property_rules

### **Modelo** `Property_rules` (Regras da Propriedade)

**Campos**

* **property (Número)**: Propriedade associada. Relaciona-se com o modelo `Property`. Este campo estabelece uma relação um-para-um, significando que cada propriedade tem um conjunto único de regras.
* **check_in_time (Texto)**: Horário de check-in. Campo que armazena o horário estipulado para o check-in na propriedade.
* **check_out_time (Texto)**: Horário de check-out. Campo que armazena o horário estipulado para o check-out na propriedade.
* **suitable_for_babies (Booleano)**: Adequado para bebês. Campo que indica se a propriedade é apropriada para hospedar bebês.
* **suitable_for_children (Booleano)**: Adequado para crianças. Campo que indica se a propriedade é apropriada para hospedar crianças.
* **allow_pet (Booleano)**: Permite animais de estimação. Campo que indica se animais de estimação são permitidos na propriedade.
* **smoking_permitted (Booleano)**: Permite fumar. Campo que indica se é permitido fumar na propriedade.
* **events_permitted (Booleano)**: Permite eventos. Campo que indica se a realização de eventos é permitida na propriedade.

### property_status_log

### **Modelo** `PropertyStatusLog` (Registro de Status da Propriedade)

**Campos**

* **created_at (Data e Hora)**: Data e hora da criação do registro. Preenchido automaticamente com a data e hora atuais.
* **property (Número)**: Relaciona-se com o modelo `Property`. Chave estrangeira que referencia a propriedade associada.
* **status (Texto)**: Status atual da propriedade. Campo de caracteres com escolhas pré-definidas, como `ACTIVE`, `INACTIVE`, `ONBOARDING`, `SIGNED_CONTRACT`.
* **exchange_date (Data)**: Data da mudança de status.
* **user_who_changed (Número)**: Relaciona-se com o modelo `User`. Chave estrangeira que referencia o usuário responsável pela alteração do status.

## Reservation

### reservation_authorization

### **Modelo** `ReservationAuthorization` (Autorização de Reserva)

**Campos**

* **reservation (Número)**: Reserva associada à autorização. Estabelece uma relação um-para-um com o modelo `Reservation`. Este campo cria um vínculo direto entre uma reserva específica e sua autorização correspondente.
* **email_sent (Booleano)**: Indica se um e-mail foi enviado. Campo que armazena a informação de se um e-mail de autorização foi ou não enviado para a reserva associada.

### reservation_category_month_price

### **Modelo** `Category_month_price` (Preço Mensal da Categoria)

**Campos**

* **category_location (Número)**: Relaciona-se com o modelo `CategoryLocation`. Chave estrangeira que referencia a localização da categoria associada.
* **month (Número)**: Número do mês, variando de 1 a 12. Campo inteiro positivo, opcional.
* **price (Número)**: Preço mensal de aluguel para a categoria. Número decimal com duas casas decimais.

### reservation_check_in_controller

### **Modelo** `Check_in_controller` (Controlador de Check-in)

**Campos**

* **reservation (Número)**: Reserva associada ao controle de check-in. Relaciona-se com o modelo `Reservation` em uma relação um-para-um.
* **was_contacted (Booleano)**: Indica se houve contato com o hóspede. Campo que armazena se o hóspede foi contatado em relação ao check-in.
* **check_in_date (Data)**: Data do check-in. Campo opcional para armazenar a data de check-in efetiva.
* **check_in_time (Tempo)**: Horário do check-in. Campo opcional para armazenar o horário de check-in efetivo.
* **guest_observation (Texto)**: Observações sobre o hóspede. Campo opcional para anotar observações relevantes sobre o hóspede no check-in.
* **checklist (JSON)**: Checklist de check-in. Campo opcional em formato JSON para armazenar um checklist relacionado ao processo de check-in.
* **card_concluded (Booleano)**: Indica se o cartão (tarefa) foi concluído. Campo que armazena se todas as tarefas de check-in foram concluídas.
* **concluded_at (Data)**: Data de conclusão do cartão. Campo opcional que armazena a data em que todas as tarefas de check-in foram concluídas.

### reservation_check_out_controller

### **Modelo** `Check_out_controller` (Controlador de Check-out)

**Campos**

* **reservation (Número)**: Relaciona-se com o modelo `Reservation`. Chave estrangeira que referencia a reserva associada ao check-out.
* **was_contacted (Booleano)**: Indica se o hóspede foi contatado. Campo booleano com valor padrão `False`.
* **check_out_date (Data)**: Data do check-out. Campo de data, opcional.
* **check_out_time (Hora)**: Hora do check-out. Campo de hora, opcional.
* **guest_feedback (Texto)**: Feedback do hóspede. Campo de texto, opcional.
* **checklist (JSON)**: Checklist para o check-out. Campo de JSON, opcional.
* **card_concluded (Booleano)**: Indica se o processo de check-out foi concluído. Campo booleano com valor padrão `False`.
* **concluded_at (Data)**: Data em que o check-out foi concluído. Campo de data, opcional.

### reservation_cleaning_controller

### **Modelo** `Cleaning_controller` (Controlador de Limpeza)

**Campos**

* **reservation (Número)**: Reserva associada ao controle de limpeza. Estabelece uma relação um-para-um com o modelo `Reservation`.
* **was_checked (Booleano)**: Indica se a limpeza foi verificada. Campo que armazena se a limpeza foi checada ou inspecionada.
* **cleaning_date (Data)**: Data da limpeza. Campo opcional para armazenar a data em que a limpeza foi realizada.
* **cleaning_time (Tempo)**: Horário da limpeza. Campo opcional para armazenar o horário em que a limpeza foi realizada.
* **cleaning_duration (Texto)**: Duração da limpeza. Campo opcional para armazenar a duração estimada ou real da limpeza.
* **maid_name (Texto)**: Nome da empregada/doméstica. Campo opcional para armazenar o nome da pessoa responsável pela limpeza.
* **cleaning_price (Número)**: Preço da limpeza. Campo opcional para armazenar o custo da limpeza.
* **bedsheets_quantity (Número)**: Quantidade de lençóis. Campo opcional para armazenar a quantidade de lençóis usados na limpeza.
* **checklist (JSON)**: Checklist de limpeza. Campo opcional em formato JSON para armazenar um checklist relacionado ao processo de limpeza.
* **card_concluded (Booleano)**: Indica se o cartão (tarefa) de limpeza foi concluído.
* **concluded_at (Data)**: Data de conclusão do cartão de limpeza. Campo opcional que armazena a data em que todas as tarefas de limpeza foram concluídas.

### reservation_guests

### **Modelo** `ReservationGuest` (Hóspede da Reserva)

**Campos**

* **reservation (Número)**: Relaciona-se com o modelo `Reservation`. Chave estrangeira que referencia a reserva à qual o hóspede pertence.
* **is_principal (Booleano)**: Indica se o hóspede é o principal para a reserva. Campo booleano com valor padrão `False`.
* **name (Texto)**: Nome do hóspede. Campo de texto.
* **document (Texto)**: Número do documento do hóspede. Campo de texto, opcional.
* **email (Texto)**: Email do hóspede. Campo de texto, opcional.
* **phone_number (Texto)**: Número de telefone do hóspede. Campo de texto, opcional.
* **front_document_photo (Número)**: Relaciona-se com o modelo `FileItem`. Chave estrangeira que referencia a foto da frente do documento do hóspede.
* **back_document_photo (Número)**: Relaciona-se com o modelo `FileItem`. Chave estrangeira que referencia a foto do verso do documento do hóspede.

### reservation_host_kpi_compiled

### **Modelo** `HostKpiCompiled` (KPI Compilado do Anfitrião)

**Campos**

* **host (Número)**: Relaciona-se com o modelo `Host`. Chave estrangeira que referencia o anfitrião associado.
* **date (Data)**: Data para a qual os KPIs (Indicadores-chave de Desempenho) são compilados. Campo de data com indexação para otimização de busca.
* **total_reservations_made (Número)**: Total de reservas feitas. Campo inteiro com valor padrão 0.
* **total_check_in (Número)**: Total de check-ins programados. Campo inteiro com valor padrão 0.
* **total_check_out (Número)**: Total de check-outs programados. Campo inteiro com valor padrão 0.
* **total_cleaning (Número)**: Total de limpezas programadas. Campo inteiro com valor padrão 0.
* **total_check_in_done (Número)**: Total de check-ins realizados. Campo inteiro com valor padrão 0.
* **total_check_out_done (Número)**: Total de check-outs realizados. Campo inteiro com valor padrão 0.
* **total_cleaning_done (Número)**: Total de limpezas realizadas. Campo inteiro com valor padrão 0.

### reservation_listing

### **Modelo** `Listing` (Listagem)

**Campos**

* **property (Número)**: Relaciona-se com o modelo `Property`. Chave estrangeira que referencia a propriedade associada à listagem.
* **ota (Número)**: Relaciona-se com o modelo `Ota` (Online Travel Agency). Chave estrangeira que referencia a OTA onde a propriedade está listada.
* **ota_fee (Número)**: Taxa da OTA. Número de ponto flutuante, opcional.
* **id_in_ota (Texto)**: Identificador único da listagem na OTA. Campo de texto, opcional.
* **title_in_ota (Texto)**: Título da listagem na OTA. Campo de texto, opcional.

### reservation_ota

### **Modelo** `Ota` (Online Travel Agency - Agência de Viagens Online)

**Campos**

* **name (Texto)**: Nome da OTA (Agência de Viagens Online). Campo que armazena o nome completo da agência, sendo um identificador único.
* **initials (Texto)**: Iniciais da OTA. Campo que armazena as iniciais da agência, também sendo um identificador único.
* **phone_number (Texto)**: Número de telefone da OTA. Campo opcional para armazenar o número de telefone de contato da agência.
* **account_manager (Texto)**: Gerente de conta da OTA. Campo opcional para armazenar o nome do gerente de conta responsável pela OTA.
* **account_manager_email (Texto)**: Email do gerente de conta. Campo opcional para armazenar o email do gerente de conta da OTA.
* **img_url (Texto)**: URL da imagem da OTA. Campo opcional para armazenar a URL de uma imagem associada à agência.

### reservation_ota_listing_id

### **Modelo** `Ota_listing_id` (ID de Listagem OTA)

**Campos**

* **ota_listing_id (Texto)**: Identificador da listagem na OTA (Online Travel Agency). Campo de texto com um máximo de 255 caracteres.
* **original_listing (Número)**: Relaciona-se com o modelo `Listing`. Chave estrangeira que referencia a listagem original associada.

### reservation_ota_listing_title

### **Modelo** `Ota_listing_title` (Título de Listagem OTA)

**Campos**

* **ota_listing_title (Texto)**: Título da listagem na OTA (Agência de Viagens Online). Campo que armazena o título específico usado na OTA para a listagem.
* **original_listing (Número)**: Listagem original associada ao título. Relaciona-se com o modelo `Listing`. Este campo estabelece uma referência à listagem original à qual o título da OTA está associado.

### reservation_ota_setup

### **Modelo** `Ota_Setup` (Configuração de OTA)

**Campos**

* **payment_delay (Número)**: Atraso no pagamento, em meses, após a reserva. Campo inteiro, indicando o número de meses até o pagamento ser realizado após uma reserva.
* **ota (Número)**: Relaciona-se com o modelo `OTA` (Online Travel Agency). Chave estrangeira que referencia a OTA associada à configuração.

### reservation_reservation

### **Modelo** `Reservation` (Reserva)

**Campos**

* **code (Texto)**: Identificador único da reserva. Gerado automaticamente.
* **added_by (Número)**: Usuário que adicionou a reserva. Relaciona-se com o modelo `User`.
* **listing (Número)**: Lista associada à reserva. Relaciona-se com o modelo `Listing`.
* **stays_creation_date (Data)**: Data de criação da reserva na plataforma STAYS.
* **check_in_date (Data)**: Data do check-in do hóspede.
* **check_out_date (Data)**: Data do check-out do hóspede.
* **check_in_time (Data)**: Hora do check-in do hóspede.
* **check_out_time (Data)**: Hora do check-out do hóspede.
* **total_price (Número)**: Valor total da reserva em R$.
* **paid_amount (Número)**: Valor total pago pelo hóspede em R$.
* **gross_daily_value (Número)**: Soma dos valores bruto das diária em R$.
* **daily_net_value (Número)**: Valor liquido da reserva em R$.
* **ota_comission (Número)**: Valor da comissão da OTA em R$.
* **extra_fee (Número)**: Taxa extra cobrada na reserva em R$.
* **manual_discount (Número)**: Desconto manual inserido na reserva em R$.
* **net_cleaning_fee (Número)**: Valor liquido da limpeza do imóvel em R$.
* **cleaning_fee_value (Número)**: Valor bruto da limpeza do imóvel em R$.
* **is_blocking (Booleano)**: Indica se a reserva é um bloqueio.
* **blocking_reason (Texto)**: Motivo pelo qual o bloqueio foi realizado.
* **recommended_by (Texto)**: Quem recomendou a reserva.
* **comment (Texto)**: Comentários adicionais relacionados à reserva.
* **guest (Número)**: Hóspede associado à reserva. Relaciona-se com o modelo `Guest`.
* **guest_name_ota (Texto)**: Nome do hóspede conforme fornecido pela OTA (Agência de Viagens Online).
* **adult_guest_quantity (Número)**: Quantidade de hóspedes adultos.
* **child_guest_quantity (Número)**: Quantidade de hóspedes crianças.
* **baby_guest_quantity (Número)**: Quantidade de hóspedes bebês.
* **child_0_6_guest_quantity (Número)**: Quantidade de hóspedes bebês, entre 0 e 6 anos.
* **child_6_12_guest_quantity (Número)**: Quantidade de hóspedes crianças, entre 6 e 12 anos.
* **status (Texto)**: Status da reserva, com opções como "Ativa", "Concluída", "Cancelada".
* **has_pet (Número)**: Indica se o hóspede tem um animal de estimação.
* **host_responsible (Número)**: Anfitrião responsável pela reserva. Relaciona-se com o modelo `Host`.
* **owners_atm (Número)**: Proprietários associados à reserva. Relaciona-se com o modelo `Owner`.
* **is_late_extension (Booleano)**: Indica se é uma extensão após o check-out original.
* **has_late_extension (Booleano)**: Indica se possui uma extensão após do check-out original.
* **is_early_extension (Booleano)**: Indica se é uma extensão antes do check-in original.
* **has_early_extension (Booleano)**: Indica se possui uma extensão antes do check-in original.
* **original_reservation (Número)**: Quando for uma reserva do tipo extensão, indicará a reserva original que gerrou essa extensão. Relaciona-se com o modelo `Reservation`.
* **early_extension_reservation (Número)**: Indica qual é a reserva do tipo extensão. Relaciona-se com o modelo `Reservation`.
* **late_extension_reservation (Número)**: Indica qual é a reserva do tipo extensão. Relaciona-se com o modelo `Reservation`.
* **is_pre_checkin_completed (Booleano)**: Registra se o formulário de pre-check-in foi preenchido.
* **is_pre_checkin_link_sent (Booleano)**: Indica se o link para preenchimento do pre-check-in foi enviado ao hóspede.
* **conciliada (Booleano)**: Se a reserva foi conciliada.
* **bed_arrangement (Texto)**: Arranjo de cama para a reserva.
* **is_monthly (Booleano)**: Indica se a reserva é mensal.
* **monthly_contract (Número)**: Contrato mensal associado à reserva. Relaciona-se com o modelo `FileItem`.
* **need_cradle (Booleano)**: Indica se é necessário um berço.
* **early_checkin_at (Data)**: Horários de check-in antecipado.
* **late_checkout_at (Data)**: Horários de check-out tardio, se aplicável.
* **link_sent_at (Data)**: Horário que o link para preenchimento do precheckin foi enviado.
* **pre_checkin_fullfilled_at (Data)**: Data e horário que o pré-check-in foi preenchido.
* **ota_fee (Número)**: Taxa de comissão da OTA em %.
* **cupom_discount (Número)**: Taxa da OTA e descontos de cupom associados à reserva.

### reservation_reservation_owners_atm

### **Modelo Abstrato** `ReservationOwners` criado a partir de relacionamento muitos para muitos

**Campos**

* **reservartion (Número)**: Relaciona-se com o modelo `Reservation`. Chave estrangeira que referencia a reserva associada.
* **owner (Número)**: Relaciona-se com o modelo `Owner`. Chave estrangeira que referencia proprietário associada à propriedade da reserva.

### reservation_voucher

### **Modelo** `ReservationVoucher` (Voucher de Reserva)

**Campos**

* **reservation (Número)**: Reserva associada ao voucher. Este campo cria uma relação um-para-um com o modelo `Reservation`, vinculando o voucher a uma reserva específica.
* **voucher_sent (Booleano)**: Indica se o voucher foi enviado. Campo que armazena a informação de se um voucher foi ou não enviado para a reserva associada.

## Sem Prefixo

### reservation_daily_values

**APP Financial**

### **Modelo** `ReservationDailyValues` (Valores Diários da Reserva)

**Campos**

* **property (Texto)**: Propriedade associada. Campo que armazena o identificador da propriedade.
* **date_ref (Data)**: Data de referência. Campo que armazena a data a que se refere o valor diário.
* **ota (Texto)**: OTA (Online Travel Agency) associada. Campo que armazena o identificador da OTA.
* **daily_value (Número)**: Valor diário. Campo que armazena o valor diário associado à propriedade e OTA na data especificada.

### household_linen

**APP Reserrvation**

### **Modelo** `HouseholdLinen` (Roupa de Casa)

**Campos**

* **name (Texto)**: Nome do item. Campo que armazena o nome da peça de roupa de casa, como lençóis, toalhas, etc.
* **price (Número)**: Preço do item. Campo que armazena o valor monetário da peça de roupa de casa, com precisão de duas casas decimais.

### guest_damage

**APP Reserrvation**

### **Modelo** `GuestDamage` (Dano Causado pelo Hóspede)

**Campos**

* **reservation (Número)**: Relaciona-se com o modelo `Reservation`. Chave estrangeira que referencia a reserva associada ao dano.
* **description (Texto)**: Descrição do dano. Campo de texto, opcional.
* **damage_type (Texto)**: Tipo do dano. Campo de caracteres com escolhas pré-definidas, como `HOUSEHOLD_LINEN`, `DAMAGED_ITEMS`, etc.
* **item_type (Texto)**: Tipo (classificação) do item danificado. Campo de caracteres com escolhas pré-definidas, como `FURNITURE`, `UTENSILS`, etc. Campo opcional.
* **item_quantity (Número)**: Quantidade de itens danificados. Campo numérico inteiro positivo.
* **item_name (Texto)**: Nome do item danificado. Campo de texto.
* **resolution (Texto)**: Solução necessária para o dano. Campo de caracteres com escolhas pré-definidas, como `REPLACE_ITEM`, `REPAIR`, etc.
* **quotation_link (URL)**: Link para o orçamento associado ao dano. Campo de URL, opcional.
* **quotation_file (Número)**: Relaciona-se com o modelo `FileItem`. Chave estrangeira que referencia o arquivo do orçamento associado ao dano. Campo opcional.
* **item_price (Número)**: Preço a ser pago pelo dano. Número decimal com duas casas decimais.
* **observation (Texto)**: Comentários adicionais sobre o dano. Campo de texto, opcional.
* **refund_holder (Texto)**: Quem receberá o reembolso. Campo de caracteres com escolhas pré-definidas, como `SEAZONE`, `OWNER`. Campo opcional.
* **are_evidences_and_quotation_validated (Booleano)**: Indica se as evidências foram validadas por um atendente. Campo booleano, opcional.
* **missing_information (Texto)**: Informações ausentes sobre o dano. Campo de texto, opcional.

### guest_damage_evidence

**APP Reserrvation**

### **Modelo** `GuestDamageEvidence` (Evidência de Dano Causado pelo Hóspede)

**Campos**

* **guest_damage (Número)**: Relaciona-se com o modelo `GuestDamage`. Chave estrangeira que referencia o dano causado pelo hóspede associado à evidência.
* **evidence (Número)**: Relaciona-se com o modelo `FileItem`. Chave estrangeira que referencia o arquivo de evidência associado ao dano.

### guest_damage_negotiation

**APP Reserrvation**

### **Modelo** `GuestDamageNegotiation` (Negociação de Dano de Hóspede)

**Campos**

* **reservation (Número)**: Reserva associada à negociação de dano. Relaciona-se com o modelo `Reservation` em uma relação um-para-um.
* **status (Texto)**: O status da negociação. Opções variadas indicando a fase atual da negociação de dano.
* **last_status_change (Data/Tempo)**: Horário da última atualização de status. Registra quando o status foi alterado pela última vez.
* **stage (Texto)**: Estágio da negociação. Indica a fase atual da negociação de dano.
* **aircover_code (Texto)**: Código do Aircover do Airbnb, se aplicável.
* **amount_received (Número)**: Valor recebido associado ao dano pelo hóspede.
* **guest_payment_status (Texto)**: Status de pagamento do hóspede. Indica a fase atual do pagamento por parte do hóspede.
* **is_to_inform_owner (Booleano)**: Se é necessário informar o proprietário sobre a negociação.
* **is_receiving_confirmed (Booleano)**: Se o pagamento do hóspede foi confirmado pela equipe financeira.
* **is_refunded (Booleano)**: Se o reembolso foi concluído para o detentor do reembolso.

### guest_damage_negotiation_history

**APP Reserrvation**

### **Modelo** `GuestDamageNegotiationHistory` (Histórico de Negociação de Dano de Hóspede)

**Campos**

* **guest_damage_negotiation (Número)**: Negociação de dano de hóspede associada. Estabelece uma relação com o modelo `GuestDamageNegotiation`, vinculando o histórico à negociação específica.
* **contact_date (Data)**: Data do contato com o hóspede. Campo opcional para registrar a data em que ocorreu o contato com o hóspede durante o processo de negociação.
* **history (Texto)**: Histórico da interação. Campo que armazena detalhes sobre o que foi conversado ou negociado com o hóspede.

### seazone_enterprise

**APP channel_manager**

### **Modelo** `Enterprise` (Spot)

**Campos**

* **name (Texto)**: Nome do Spot. Este campo armazena o nome do Spot, sendo um identificador único para cada empresa cadastrada no sistema.
* **status (Texto)**: Status do Spot. O campo que indica se o Spot está ativo ou inativo, com opções pré-definidas no `EnterpriseStatus`.

### seazone_enterprise_unit

**APP channel_manager**

### **Modelo** `EnterpriseUnit` (Unidade Spot)

**Campos**

* **enterprise (Número)**: Relaciona-se com o modelo `Enterprise`. Chave estrangeira que referencia o Spot à qual a unidade pertence.
* **number (Texto)**: Número ou identificador da unidade Spot. Campo de texto.
* **status (Texto)**: Status da unidade Spot. Campo de caracteres com escolhas pré-definidas, como `ACTIVE` e `INACTIVE`, com valor padrão `ACTIVE`.

### damage_negotiation_guest_payment_receipt

**APP Reserrvation**

### **Modelo** `DamageNegotiationGuestPaymentReceipt` (Recibo de Pagamento do Hóspede na Negociação de Danos)

**Campos**

* **guest_damage_negotiation (Número)**: Relaciona-se com o modelo `GuestDamageNegotiation`. Chave estrangeira que referencia a negociação de danos associada ao recibo de pagamento do hóspede.
* **guest_payment_receipt (Número)**: Relaciona-se com o modelo `FileItem`. Chave estrangeira que referencia o arquivo do recibo de pagamento associado ao dano pago pelo hóspede.

### damage_negotiation_owner_payment_receipt

**APP Reserrvation**

### **Modelo** `DamageNegotiationOwnerPaymentReceipt` (Recibo de Pagamento do Proprietário em Negociação de Danos)

**Campos**

* **guest_damage_negotiation (Número)**: Negociação de dano de hóspede associada. Este campo estabelece uma relação com o modelo `GuestDamageNegotiation`, vinculando o recibo de pagamento ao caso específico de negociação de dano.
* **owner_payment_receipt (Arquivo)**: Arquivo de recibo de pagamento do dano do hóspede associado ao pagamento ao proprietário. Este campo associa um recibo de pagamento (referenciado pelo modelo `FileItem`) ao pagamento feito ao proprietário no contexto da negociação de danos.

### pipefy_pipe

**APP channel_manager**

### **Modelo** `PipefyPipe` (Pipe do Pipefy)

**Campos**

* **pipe_id (Texto)**: ID do Pipe do Pipefy. Campo que armazena o identificador único do tubo no sistema Pipefy.
* **pipe_name (Texto)**: Nome do Pipe do Pipefy. Campo que armazena o nome do tubo, facilitando a identificação e referência.
* **pipe_type (Texto)**: Tipo do Pipe do Pipefy. Campo que define o tipo do tubo com base em um conjunto de opções pré-definidas na classe `PipeType`.

[Tabelas e Planilhas ](/doc/tabelas-e-planilhas-9jv0naHKtq)