<!-- title: Documentação de Integração - Pipedrive | url: https://outline.seazone.com.br/doc/documentacao-de-integracao-pipedrive-ws4QRiKQFe | area: Tecnologia -->

# Documentação de Integração - Pipedrive

# Visão Geral

Este documento mapeia todos os campos que estão integrados entre o sistema interno e o Pipedrive. O objetivo é facilitar a manutenção, evitar falhas de integração e identificar possíveis conflitos ou campos obsoletos.

## Como Usar Esta Documentação

* **Chave do Campo no Pipedrive**: Identificador único usado pela API do Pipedrive para este campo
* **Nome do Campo Interno**: Nome usado no sistema interno (backend) para armazenar este dado
* **Nome do Campo no Pipedrive**: Nome legível que aparece na interface do Pipedrive

⚠️ **Nota Importante sobre Campos em Branco**: Quando a coluna "Nome do Campo no Pipedrive" está em branco, isso indica que:

* O campo provavelmente existia anteriormente no Pipedrive mas foi deletado
* A integração pode ter sido descontinuada
* É recomendado revisar se esse campo ainda é necessário no sistema interno


---

## Mapeamento de Campos de Negócio (Deals)

Esta seção documenta todos os campos relacionados aos negócios (deals) no Pipedrive e como eles são mapeados no sistema interno.

### Campos de Negócios

| Chave do Campo no Pipedrive | Nome do Campo Interno | Nome do Campo no Pipedrive |
|----|----|----|
| id | id | ID |
| title | title | Título |
| creator_user_id | creator_user_id | Criado por |
| user_id | partner_id | Proprietário |
| value | value | Valor |
| currency | currency | Moeda |
| weighted_value | weighted_value | Valor ponderado |
| weighted_value_currency | weighted_value_currency | Moeda do valor ponderado |
| probability | probability | Probabilidade |
| org_id | org_id | Organização |
| pipeline | pipeline | Funil |
| pipeline_id | pipeline_id | ID do Funil |
| person_id | person_id | Pessoa de contato |
| stage_id | stage_id | Etapa |
| status | status_id | Status |
| add_time | created_at | Negócio criado em |
| update_time | updated_at | Atualizado em |
| stage_change_time | last_stage_change_at | Última alteração de etapa |
| next_activity_date | next_activity_date | Próxima atividade em |
| last_activity_date | last_activity_date | Data da última atividade |
| won_time | won_time | Ganho em |
| last_incoming_mail_time | last_incoming_mail_time | Último e-mail recebido |
| last_outgoing_mail_time | last_outgoing_mail_time | Último e-mail enviado |
| lost_time | lost_time | Data de perda |
| close_time | close_time | Negócio fechado em |
| lost_reason | lost_reason_id | Motivo da perda |
| visible_to | visible_to_id | Visível para |
| activities_count | activities_count | Total de atividades |
| done_activities_count | done_activities_count | Atividades concluídas |
| undone_activities_count | undone_activities_count | Atividades para fazer |
| email_messages_count | email_messages_count | Número de mensagens de e-mail |
| expected_close_date | expected_close_date | Data de fechamento esperada |
| product_quantity | product_quantity | Quantidade de produtos |
| product_amount | product_amount | Valor de produtos |
| label | label_id | Etiqueta |
| product_name | product_name | Nome do produto |
| 93b3ada8b94bd1fc4898a25754d6bcac2713f835 | channel_id | Canal |
| 45a56c6ae1f43dad4992c3c23d4a2a32787d93d6 | city_state | Cidade |
| ce82c3dbb939c391578abeeb1737a04090c1fc7f | region_id | Região |
| ee7b1a2521cc3a95eefdaa47611ad18572bd1a2f | partner | Parceiro |
| b57803776a6cd6e6b2b0cb8eecaa34b03e3d3eee | partner_executive_id | Executivo de Parceiros (Novíssimo) |
| cd271d69fe261eeed5603fe8a8b67a57d6df92af | pre_seller_id | Pré Vendedor(a) |
| 9febb1135cb019af2ea4149d12a0f4d97166a397 | property_type_id | Tipo de Imóvel |
| bc74bcc4326527cbeb331d1697d4c8812d68506e | qualification_date | Data de Qualificação |
| 450d78a6dd5adcce45644cba36598aca90204016 | room_numbers_id | Número de Quartos |
| f7b72a884163f016d2f27fd7fc6b63d584982415 | category_id |    |
| 045b835b9180724125743b8f64abfdab73149946 | property_size | Tamanho do imóvel (m²) |
| c4724633ea54f919d14c00257a3520dfaf412176 | bathroom_quantity |    |
| f905ad7b8f348704fc3fa6c27150d444f0686625 | toilets_quantity |    |
| 989d09a197bb143247fd76591175424fa7f770c2 | single_bed_quantity |    |
| a1bfc65c011149944bb7a9bc4083928c69bbaee0 | double_bed_quantity |    |
| 16ddde2bed3975efb3c9c7ac29f7ebf9daf253c9 | queen_bed_quantity |    |
| 150149ea0332a8d8098967c9325fe7dc976bc52b | king_bed_quantity |    |
| 0ab5925374c7adfe2515cc6406a5095683b0b936 | single_sofa_bed_quantity |    |
| e02978bec5fd3c9670b311cf864ef1104517731f | double_sofa_bed_quantity |    |
| 098777fe93b8f0fd6211b063d1d0d30975d7d151 | contact_method_id | MétodoContato |
| efeaf16b0bc4ca4f43cc2cce7522886cc47995b3 | property_address | Endereço do Imóvel |
| efeaf16b0bc4ca4f43cc2cce7522886cc47995b3_lat | property_address_latitude | Latitude de Endereço do Imóvel |
| efeaf16b0bc4ca4f43cc2cce7522886cc47995b3_long | property_address_longitude | Longitude de Endereço do Imóvel |
| efeaf16b0bc4ca4f43cc2cce7522886cc47995b3_subpremise | property_complement | Nº de apartamento de Endereço do Imóvel |
| efeaf16b0bc4ca4f43cc2cce7522886cc47995b3_street_number | property_number | Número da casa de Endereço do Imóvel |
| efeaf16b0bc4ca4f43cc2cce7522886cc47995b3_route | property_street | Nome da rua de Endereço do Imóvel |
| efeaf16b0bc4ca4f43cc2cce7522886cc47995b3_sublocality | property_neighborhood | Distrito/sub-localidade de Endereço do Imóvel |
| efeaf16b0bc4ca4f43cc2cce7522886cc47995b3_locality | property_locality | Cidade/município/vila/localidade de Endereço do Imóvel |
| efeaf16b0bc4ca4f43cc2cce7522886cc47995b3_admin_area_level_1 | property_region_state | Estado de Endereço do Imóvel |
| efeaf16b0bc4ca4f43cc2cce7522886cc47995b3_admin_area_level_2 | property_region_city | Região de Endereço do Imóvel |
| efeaf16b0bc4ca4f43cc2cce7522886cc47995b3_country | property_country | País de Endereço do Imóvel |
| efeaf16b0bc4ca4f43cc2cce7522886cc47995b3_postal_code | property_postal_code | CEP/Código postal de Endereço do Imóvel |
| efeaf16b0bc4ca4f43cc2cce7522886cc47995b3_formatted_address | property_formatted_address | Endereço completo/combinado de Endereço do Imóvel |
| 5ae1b70b2c84cb6af6ca817167bed75a47cbeca4 | property_code | Código do imóvel / Unidade |
| c7fb17c8bfe729b09349723461250f3b3133066d | condominium_id |    |
| 0b8546d3ab3156224126675b930d5d5c4061fa04 | plan_id | Plano |
| ba4ef52ee7f02f22ba933da067b00d9c9ec807ea | implantation_total_value | Taxa de Adesão |
| ba4ef52ee7f02f22ba933da067b00d9c9ec807ea_currency | implantation_currency | Moeda de Taxa de Adesão |
| a7c77267b3676bc817ce23ce4b0d72c16018540e | seazone_commission | Comissão Seazone |
| 1f91c7451cf87c5f7e69b4af88e04ee0b3655358 | property_comment | Observações - longo |
| ef15468498ed62ef0785a2b9b9230832a83b6d73 | original_id | ID Original |
| f3cdd699709458ba3a87920b0056f88475ba4889 | seazone_id | IdSeazone (add na org) |
| 246d5d76742448ec804a227160510af7fd0410da | lead_reactivated_id | Lead Reativado? |
| 837653ab193c6a293b346fb464a8a89c6259bc0b | rd_convertion | \[RD\] Conversão |
| 4050905156f071d7c38fccc673d29dcd630a2ddb | rd_region_specification | \[RD\] Região especificada |
| ff53f6910138fa1d8969b686acb4b1336d50c9bd | rd_source | \[RD\] Source |
| 5560779bb633df6c9916f48ad4062d76ffcd2d06 | rd_other_city | \[RD\] Outra cidade |
| 96b9fd6fbe295819b12eac4a1d4a8d0b5a6a4f7f | site |    |
| b865dc9db6a6f527cbde2f5ccfcb6748c1af6afd | social_media_id | Redes Sociais (add na org) |
| 482743d11858b0b2fe9998647f468a3f05a81969 | indicate_properties_id | Indica Imóveis? // \[B2B\] Pronto para operar? |
| 41f06695ced8025559b2795edee9df97aff8f047 | indicate_allotments_id |    |
| f06f042452d68bd8b3815643382d7ed5ab5039c4 | sells_spe_id | Vende SPE? (add na org) |
| f0552384ddb5188742c24f92c586ffd08bdec76e | document_type_id | Tipo do Cadastro? |
| baf019ccd4c4c4032c5a821b5a24265f3243c3b5 | conversion_step_id | Etapa de Conversão |
| 0991df803259514d51f357faf6c34a88dea9408a | condominium_name | Nome do Condomínio |
| be1b51ee4b6b8789ace3f5aea8984c132c357ddf | payment_id | Forma de Pagamento |
| 42dfa3c3d13841cef91ffd180528fb57da35778e | rd_partner_phone_number | \[RD\] Número parceiro PF |
| 0adfea58c96df1a21eee3b0da8462bbe58a9d029 | onboarding_contact | Contato para Onboarding |
| 29da9f727ff0dcf5b897598f226aa6d4bc4daff9 | host_visit_id | Teve Visita da Franquia? |
| 95d024f3ecb12760726d846dd0c0201eba17dd5d | host_id | Franquia |
| e446c37fb126d0a122ae3a1d2f6a5b5716038731 | rd_campaign | \[RD\] Campanha |
| bfafc352c5c6f2edbaa41bf6d1c6daa825fc9c16 | meeting_date | Data da reunião |
| 55bb0bbb3ffd7ac235c453d8c237fa2edcf6fb44 | invest_amount_id | Qual o valor total que você pretende investir? |
| 104f48682c832ae0da9c7fef2ab611bcbb110839 | work_with_investment_id |    |
| f9b23753a78ed314d9ad42f51a9dd02da0b8c751 | investment_type_id | Você procura investimento ou para uso próprio? |
| 40092ba51dc1f608466216a68da647d456c4b259 | achieves_payment_term_id | Nosso prazo de pagamento é de até 36 meses. Esse prazo é possível para você? |
| 38f50c904c135ea1a2d32163913a88344a8c00df | user_registered_id | Usuário cadastrado? // Cross-Sell? |
| 735817cc8c69cf68d0c4ffd8fd14b4f5df400253 | property_furnished_id | O imóvel está mobiliado? |
| 6d565fd4fce66c16da078f520a685fa2fa038272 | enterprise_id | Empreendimento |
| 77dbb0c50d355b98c0a4ad56cfd1ed1322bf0001 | interest_enterprise_id |    |
| 7c49d85470c1c8a553fa0faee757883157b7830b | sell_type_id | Tipo de Venda |
| 354081d444f8028911d9a5408df1fd595d5a0c5a | szs_contact_id | Tem interesse em contato com a SZS? // É grande operação? |
| 1d144b4cff4159b9d8ff1b2db0546c4db53d814c | generate_contract_id | Gerar Contrato |
| f9ebed6077eeb3a35095c7fd91622232cee83340 | payment_flow_link |    |
| ae6483dc5ef03956b84f8970092359c7b5304b65 | trained_by |    |
| 430cf451d798f5005150fb3094d15effd08893d2 | creci_number |    |
| 9f8adce5d4c5bf336f6462039dd44499a395c460 | location_id | Location |
| 8d0bd03aea93c04be6576cd6704be03bff44953f | service_type_id | Tipo do Serviço |
| f10ec751f11bedf31ac2fe7406450332f84a0239 | net_promoter_score |    |
| 92b196fb1b3ea4ec19e682f6fa932db0f2a34e08 | google_drive_link | Link Pasta Google Drive |
| efca3a50c6b5809b514466e8de37d93cb0dd8d90 | project_id |    |
| 8664205ce176e80b52c58ba3b8935d73bdb679d8 | qualification_score |    |
| 06b8065d60ead44cf748bc592d75f67e6cdfb0b5 | ambassador_id | Embaixador |
| d8a8e0ee6135f606fc8028b865b6630a6397d175 | marketplace_category_id | Categoria SPOT |
| 2f69d6d079f566c78a57f9a2ec4a21a0ffd330b0 | operation_comments | Comentários para operação |
| 27ae1e0fa32528a40878bec9a9e4ae06b2fef73f | test_id |    |
| 4861c7a2d0ffb9a7623f5992f69b00b592f0e5d0 | ambassador_id_number |    |
| bc5189ab694b798cd4d006853659449dc6c65404 | partner_score | Score do Parceiro/Reunião |
| 29d280e981ec92af1324e924541265c177d05817 | webinar_id |    |
| 0453a336c5b47ac53c6199a9fb2704bcf7656143 | franchise_offering_circular_send_date | Data de envio da COF |
| 00c1c0fad0e97c3d7d9c8d08c7cc9cf1c474a11f | account_management_membership | Gestão de Contas - Adesão |
| 602d767eee5a8dd5777105efc67c440edb078f64 | non_account_management_reason_id | Gestão de Contas - Motivo de não adesão |
| 0290ee701297c890409c8b015c193eedcdcfebd2 | lead_entry_week_id |    |
| 0dd2e7cefd18c944b57d37341af44e4f9fb3c25a | expected_delivery_date | Data prevista de entrega/conexão |
| 3cb36fe6e0d7f93fc2f7714c865b02e618d98895 | effective_delivery_date |    |
| 1c22e75484f5cd7471d76cd002ce0a773688d644 | properties_quantity |    |
| 2a062c5a71efa915d3d54c92acd9c0e21a1396c3 | host_commission | Comissão Anfitrião |
| 0fc5bd6f32888da0c4d5e1dc6333f72ce25c24f8 | is_owner_contact | Contato para onboarding / Proprietário? |
| d7dadb61cca3e75c733dacf964c67a34ae2f05a5 | onboarding_name | Contato para onboarding/Nome |
| 2f1355b7d1e415ccc1ec577cba5374edbfa8efdd | units_quantity | Quantidade de imóveis |
| 6a67dcd2a5eb768783594f34fe04e3b11eecbcf6 | proof_of_residence_file_url | Link Comprovante de residencia |
| 90b3ed79d43aa61d48754fa30ae6ac71f9aa5c40 | cnh_file_url | Link Documento Identidade / CPF |
| 3572b09c1953442131354333cc4123a321f342f2 | property_code_select | Unidade SPOT |
| 03fd3594ff0804d2b16d5410c2fc1552c5dd24c9 | b2b_building | Prédio B2B |
| 96b09dbfa04d9e933b3a4c5482fc21b70d72a00a | commission_value_type | Valor da comissão (parceiros) |
| 99ac7cd8c5d6af9bd0a1273521a973810ec286c4 | commission_period | Comissão Vitalícia? |

## Mapeamento de Campos de Pessoa (Person)

Esta seção documenta todos os campos relacionados às pessoas no Pipedrive e como eles são mapeados no sistema interno.

### Campos de Pessoa

| Chave do Campo no Pipedrive | Nome do Campo Interno | Nome do Campo no Pipedrive |
|----|----|----|
| id | id | ID |
| company_id | company_id |    |
| owner_id | owner_id | Proprietário |
| org_id | org_id | Organização |
| name | name | Nome |
| first_name | first_name | Primeiro nome |
| last_name | last_name | Sobrenome |
| open_deals_count | open_deals_count | Negócios em aberto |
| related_open_deals_count | related_open_deals_count |    |
| closed_deals_count | closed_deals_count | Negócios fechados |
| related_closed_deals_count | related_closed_deals_count |    |
| participant_open_deals_count | participant_open_deals_count |    |
| participant_closed_deals_count | participant_closed_deals_count |    |
| email_messages_count | email_messages_count | Número de mensagens de e-mail |
| activities_count | activities_count | Total de atividades |
| done_activities_count | done_activities_count | Atividades concluídas |
| undone_activities_count | undone_activities_count | Atividades para fazer |
| files_count | files_count |    |
| notes_count | notes_count |    |
| followers_count | followers_count |    |
| won_deals_count | won_deals_count | Negócios ganhos |
| related_won_deals_count | related_won_deals_count |    |
| lost_deals_count | lost_deals_count | Negócios perdidos |
| related_lost_deals_count | related_lost_deals_count |    |
| active_flag | active_flag |    |
| phone | phone | Telefone |
| email | email | E-mail |
| first_char | first_char |    |
| update_time | update_time | Atualizado em |
| delete_time | delete_time |    |
| add_time | add_time | Pessoa criada |
| visible_to | visible_to | Visível para |
| picture_id | picture_id | Foto de perfil |
| next_activity_date | next_activity_date | Próxima atividade em |
| next_activity_time | next_activity_time |    |
| next_activity_id | next_activity_id |    |
| last_activity_id | last_activity_id |    |
| last_activity_date | last_activity_date | Data da última atividade |
| last_incoming_mail_time | last_incoming_mail_time | Último e-mail recebido |
| last_outgoing_mail_time | last_outgoing_mail_time | Último e-mail enviado |
| label | label | Etiqueta |
| im | im | Mensageiro instantâneo |
| postal_address | postal_address | Endereço postal |
| postal_address_subpremise | postal_address_subpremise | Nº de apartamento de Endereço postal |
| postal_address_street_number | postal_address_street_number | Número da casa de Endereço postal |
| postal_address_route | postal_address_route | Nome da rua de Endereço postal |
| postal_address_sublocality | postal_address_sublocality | Distrito/sub-localidade de Endereço postal |
| postal_address_locality | postal_address_locality | Cidade/município/vila/localidade de Endereço postal |
| postal_address_admin_area_level_1 | postal_address_admin_area_level_1 | Estado de Endereço postal |
| postal_address_admin_area_level_2 | postal_address_admin_area_level_2 | Região de Endereço postal |
| postal_address_country | postal_address_country | País de Endereço postal |
| postal_address_postal_code | postal_address_postal_code | CEP/Código postal de Endereço postal |
| postal_address_formatted_address | postal_address_formatted_address | Endereço completo/combinado de Endereço postal |
| notes | notes | Anotações |
| birthday | birthday | Aniversário |
| job_title | job_title | Cargo |
| org_name | org_name |    |
| marketing_status | marketing_status |    |
| doi_status | doi_status |    |
| cc_email | cc_email |    |
| primary_email | primary_email |    |
| owner_name | owner_name |    |
| 136f1cf23f30538fe0622dbcd20fa48f6ec3b4fa | person_type_id | Tipo da Pessoa |
| 9a618cc7586f354a35863064bdbbddcada0dbd10 | cpf_cnpj | CPF/CNPJ (SÓ NÚMEROS) |
| ee02ba7f9a43a4df22335dd7980ba6a9589e5303 | cpf |    |
| db5e91b29a8e7855f57e3a226421496bdb508b2b | cnpj |    |
| 3a42c36605aae8cc51551d4b443850b6c013ba39 | address | Endereço Cliente |
| 3a42c36605aae8cc51551d4b443850b6c013ba39_subpremise | address_complement | Nº de apartamento de Endereço Cliente |
| 3a42c36605aae8cc51551d4b443850b6c013ba39_street_number | address_number | Número da casa de Endereço Cliente |
| 3a42c36605aae8cc51551d4b443850b6c013ba39_route | address_street | Nome da rua de Endereço Cliente |
| 3a42c36605aae8cc51551d4b443850b6c013ba39_sublocality | address_neighborhood | Distrito/sub-localidade de Endereço Cliente |
| 3a42c36605aae8cc51551d4b443850b6c013ba39_locality | address_region | Cidade/município/vila/localidade de Endereço Cliente |
| 3a42c36605aae8cc51551d4b443850b6c013ba39_admin_area_level_1 | address_state | Estado de Endereço Cliente |
| 3a42c36605aae8cc51551d4b443850b6c013ba39_admin_area_level_2 | address_city | Região de Endereço Cliente |
| 3a42c36605aae8cc51551d4b443850b6c013ba39_country | address_country | País de Endereço Cliente |
| 3a42c36605aae8cc51551d4b443850b6c013ba39_postal_code | address_postal_code | CEP/Código postal de Endereço Cliente |
| 3a42c36605aae8cc51551d4b443850b6c013ba39_formatted_address | address_formatted | Endereço completo/combinado de Endereço Cliente |
| 40eccae3fb6a7dc21ad46a75a161c2824170383d | nationality | Nacionalidade |
| 0a4735cb21559c9ef5368d4805dfc0769bd38fde | profession | Profissão |
| b0fad6f6c3617bae5bb1f886c30ea71d7fb66a0d | marital_status | Estado Civil |
| bf222dc5c838ecc6296bcc6cfff087fa23994067 | representative_cpf | CPF do Representante |
| 89d741132c3a4f2a6c486986c442c3669f8fa93a | representative_name | Nome do Representante |
| 6752f288b3407f72842c3575006c06244f01aa5c | corporate_name | Razão Social |
| e7c949ab7cbe1bccfc1cf76d1d8999dff8eaf1fd | whatsapp_link | Whatsapp chat link |
| 7c92f78f8eee09dea4156bdca462dc24439c237c | product_training |    |
| 10c7750c1add0f50383eddab55abe16fbaf2fc25 | position |    |

## Mapeamento de Campos de Organização (Organization)

Esta seção documenta todos os campos relacionados às organizações no Pipedrive e como eles são mapeados no sistema interno.

### Campos de Organização

| Chave do Campo no Pipedrive | Nome do Campo Interno | Nome do Campo no Pipedrive |
|----|----|----|
| 22fb1ccf66d8990166ad99d8ef22fb4a538020ff | partnership_tier | Nível do Parceiro |


## Mapeamento de Opções de Campos

Esta seção documenta os valores possíveis para campos do tipo "opção" (dropdown/select) e como eles são mapeados entre o Pipedrive e o sistema interno.

### Opções de Status do Negócio (status - Campo padrão)

| ID da Opção | Rótulo no Pipedrive | Valor de Mapeamento Interno | Status Interno |
|----|----|----|----|
| open | Aberto | IN_PROGRESS | Em Progresso |
| won | Ganho | WON | Ganho |
| lost | Perdido | LOST | Perdido |
| deleted | Excluído | CANCELED | Cancelado |

### Opções de Tipo de Imóvel (property_type_id)

| ID da Opção | Rótulo no Pipedrive | Chave de Mapeamento Interno | Rótulo Interno |
|----|----|----|----|
| 39 | Apartamento | Apartment | Apartamento |
| 40 | Casa | House | Casa |
| 42 | Resort/Hotel | Hotel | Resort/Hotel |
| 163 | Pousada | Inn | Pousada |
| 117 | Prédio Inteiro | Entire Building | Prédio Inteiro |
| 508 | SPOT | Spot | SPOT |
| 509 | Lançamento | Launch | Lançamento |
| 621 | Vistas | Views | Vistas |
| 3167 | Studio | Studio | Studio |

### Opções de Nível de Parceria (partnership_tier)

| ID da Opção | Rótulo no Pipedrive | Chave de Mapeamento Interno | Rótulo Interno |
|----|----|----|----|
| 3496 | Básico | Basic | Básico |
| 3497 | Premium | Premium | Premium |

### Opções de Etiqueta de Estágio do Edifício (label - Etiqueta)

| ID da Opção | Rótulo no Pipedrive | Chave de Mapeamento Interno | Rótulo Interno |
|----|----|----|----|
| 1799 | Pronto | Pronto | Pronto |
| 3495 | em obra | Em obras | Em obras |
| 2071 | Lançamento | Em Lançamento | Em Lançamento |