<!-- title: Tabelas usadas nos suportes | url: https://outline.seazone.com.br/doc/tabelas-usadas-nos-suportes-cyfAndE52q | area: Tecnologia -->

# Tabelas usadas nos suportes

O Sapron usa o Framework Django no seu backend, o que cria uma convenção de nomenclatura das tabelas separados por um prefixo do seu devido app (como account, property, etc). Aqui vou listar as que mais vejo uso cotidianamente na resolução de suportes.

# Account

As tabelas Account são as que dão permissão e armazenam dados específicos dessas funções. 

Por exemplo: Se um User é referenciado na tabela "account_owner", ele tem permissões de Proprietário. 


* ***account_user***: Registro de usuário, todas as tabelas de roles (funções) referenciam ela.

  \- Dados notáveis:
  * Email;
  * Nomes (first_name, last_name, trading_name, corporate_name);
  * Último Login;
  * Person ID (para a integração com o Pipedrive no caso de parceiros);
  * Dados pessoais.


* **account_user_audit:** Registro de alterações na account_user. 

  \- Dados notáveis:
  * Qual campo foi alterado (fields_changed);
  * Quando foi a alteração (changed_at);
  * Quem alterou (changed_by_user_id).


* **account_address:** Registro de endereços. É criado e editado junto com os formulários de Onboarding e Inserir/Editar Dados.


* **account_owner:** Registro de Proprietários. O ID é geralmente referenciado nas tabelas `property_property` e `property_property_owners`. 

  Um novo Proprietário pode ser criado através da rota `/onboarding`, sempre junto com uma propriedade e editado na rota `/editardados/proprietario`.

  \- Dados notáveis:
  * Nota Fiscal padrão do proprietário (default_invoice_address_id);
  * Dado Bancário padrão do proprietário (default_bank_details_id);
  * user_id .


* **account_host:** Registro de Anfitriões/Franqueado. O ID é geralmente referenciado nas tabelas `property_property` e `account_host_profile`. 

  Um novo Anfitrião pode ser criado através da rota `/inserirdados/anfitriao` e editado na rota `/editardados/anfitriao`.

  \- Dados notáveis:
  * user_id.

  OBS: A grande maioria dos dados (como os de royalties e commission) são legado. A grande maioria das vezes que usamos essa tabela é pra dar consultar o user_id do anfitrião e vice-versa.

  \
* **account_host_profile:** Registro de Co-Anfitrião (co-host).

  \- Dados notáveis:
  * user_id
  * host_id: referencia a qual Anfitrião esse co-host responde. Ele só poderá registrar reembolsos, danos e visualizar dados referentes as propriedades que estão atribuídas ao host_id que estão registrados aqui.


* account_partner: Registro de Parceiros/Corretores. O ID é geralmente referenciado nas tabelas `partners_indications_property` e `partners_indications_investments`.

  Um novo Parceiro pode ser criado através da rota `/inserirdados/parceiro` e editado na rota `/editardados/parceiro`.

  \- Dados notáveis:
  * user_id.


* account_seazone: Registro de Seazoners que não são Admin (como devs). Cada um tem permissões diferentes de visibilidade e ação dentro do Sapron, são separados por Onboarding e Administrative.

  \- Dados notáveis:
  * user_id.


# Financial

* **financial_bank:** Registros de Bancos. A inclusão de novos bancos é feita aqui. Os nomes podem ser pesquisados e validados com o time Financeiro ou com a PM.


* **financial_bank_details:** Registros de Dados Bancários de usuários. São referenciados no módulo do Proprietário, na seção de "Meus Dados", rota `/meusdados`.


* **financial_expenses:** Registros de Despesas/Reembolsos. São referenciadas no módulo do Backoffice como "Despesas" e no módulo de Anfitrião/Franqueado como "Reembolso", nas rotas `/despesas` e `/reembolso`, respectivamente.


* **financial_host_franchise_fee:** Registros de Taxas de Implantação de Anfitrião/Franqueado. São levados em consideração para o Fechamento na rota `/fechamentoanfitriao`.


* **financial_invoice_details:** Registros de dados de Nota Fiscal (NF). São referenciados na rota `/listadenfs`.

# Property

* **property_property**: Registros de Propriedades/Imóvel. **O ID é referenciado em inúmeras tabelas como property_id.**

  Uma nova Propriedade pode ser criada na rota `/onboarding` e editada na rota `/editardados/propriedade`.

  \- Dados notáveis:
  * ***code***: O código é usado pra especificar uma propriedade entre Seazoners de maneira universal. Está presente nos anúncios nas OTAs, Stays, Saprons, Planilhas, etc;
  * ***comission_fee***: Taxa de comissão geral do imóvel. Subtraído de 1 é o decimal que representa a porcentagem do que é dividido entre o Anfitrião e a Seazone;
  * ***host_reservation_comission_fee***: Taxa de comissão do Anfitrião. A taxa de Comissão da Seazone é `comission_fee - host_reservation_comission_fee`.
  * status: Pode ser Onboarding, Active ou Inactive. Ele determina a exibição em algumas telas do Frontend e algumas filtragens de endpoints no Backend;
  * host_id: Qual anfitrião é responsável pelo atendimento na propriedade;
  * owner_id: De qual proprietário é a propriedade;
  * extra_day_preparation: Quantos dias de preparação são necessários para uma propriedade está pronta para uma reserva ou bloqueio de uso próprio do Proprietário. É referenciado em rotas de calendário no Frontend, como `/multicalendar` pro Backoffice e Anfitriões.


* **property_audit:** Registro de alterações na property_property

  \- Dados notáveis:
  * Qual campo foi alterado (fields_changed);
  * Quando foi a alteração (changed_at);
  * Quem alterou (changed_by_user_id).


* **property_property_owners:** Tabela utilizada antigamente para referenciar qual propriedade é de qual proprietário. Se não me engano alguns endpoints usam essa tabela como referência ainda, então alterações no dado `owner_id` da tabela property_property devem ser replicados aqui ao transferir propriedades.


* **property_host_time_in_property:** Registro de data para migrações de anfitrião, bem como os IDs de qual o antigo e o novo anfitrião. 


# Reservation

* **reservation_reservation**: Registro de Reservas.

  \- Dados notáveis:
  * ***code***: hash único pra cada reserva, é comumente usado pelo fechamento para especificar uma reserva.
  * ***stays_reservation_code***: Código da reserva na Stays. Frequentemente utilizado para referenciar a reserva.
  * ***check_in_date***: Data de check-in.
  * ***check_out_date***: Data de check-out.
  * ***is_blocking***: Se é um bloqueio.
  * ***status***: Pode ser "Concluded", "Canceled" e mais alguns, mas esses são os mais comuns. Reservas com status "Canceled" não são exibidas no calendário de Propriedade, não é incomum que bloqueios para implantação estejam com status "Concluded" no Sapron mas já tenham sido apagados na Stays.
  * ***conciliada***: Se essa reserva já foi verificada pelo time de Fechamento. Caso essa flag esteja marcada como `True`, não sofrerá mais atualizações.
  * ***listing_id***: De qual anúncio essa reserva originada. Se a reserva não está aparecendo no calendário da propriedade, devido a migração de reservas de uma propriedade que foi transferida de proprietário, geralmente é por quê o listing não está referenciando a nova propriedade.


* **reservation_audit**: Registro de alterações na reservation_reservation

  \- Dados notáveis:
  * Qual campo foi alterado (fields_changed);
  * Quando foi a alteração (changed_at);
  * Quem alterou (changed_by_user_id).


* **reservation_listing**: Registro de Anúncios. 


* **reservation_ota**: Registros de OTAs (Online Travel Agency, como AirBNB, Expedia, Booking, etc.)


* **reservation_cleaning_controller**: Registro de limpezas realizadas pelo Anfitrião. Ele é preenchido manualmente na rota `/controle`.


* **channel_manager_reservation_state**: Antigamente utilizada para fazer a relação entre o código de reserva da Stays e o id na tabela reservation_reservation. Hoje é utilizada para administrar o estado das extensões no caso do AirBNB.
  * Contexto: Na API da Stays as extensões de reservas das outras OTAs são registros separados, mas as extensões do AirBNB só alteram a original, então para que o Sapron tenha o registro separado das extensões, criamos códigos artificiais. Se o código da reserva na Stays é GR61I e ela teve uma extensão, nessa tabela chamaremos ela de GR61I-EX1.


# Não categorizadas

* files_fileitem: Registro de inserção de arquivos na AWS. Todas as tabelas que contém "file" no nome acabam tendo uma chave estrangeira de `uid` que é originária daqui. Mais notoriamente `financial_expensesfiles`


* **partners_indications_investment**: Registros de indicação de SPOT feita por parceiros através da rota `/parceiros/indicar/formulario/spot` 


* **partners_indications_property**: Registro de indicação de Propriedade feita por parceiros através da rota `/parceiros/indicar/formulario/locacao`

⚠️⚠️ Pras duas tabelas: Indicações com `partner_id = 1` são registradas assim por quê foram importadas diretamente do Pipedrive e não tiveram parceiro encontrado no banco de dados.


* **financial_cleaning_fee_manual_fit**: Registro de ajustes manuais de limpeza, feito pelo time de fechamento na rota `/fechamentoimovel`.


\