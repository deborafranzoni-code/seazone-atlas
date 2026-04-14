<!-- title: [Parceiros][Formulário terrenos | url: https://outline.seazone.com.br/doc/parceirosformulario-terrenos-fRgZdRYrJc | area: Tecnologia -->

# [Parceiros][Formulário terrenos

**Estudo da API do Pipefy para a Integração com a Indicação de Terrenos**


## **1. Objetivo**

Este documento tem como objetivo analisar e documentar a API GraphQL do Pipefy para a integração com o sistema SAPRON. O foco é automatizar a criação de cards nos pipelines de **Teste** e **Produção** a partir de uma indicação de terreno no SAPRON, mapeando os campos e estabelecendo um plano de ação.

## **2. Análise da API e Ambientes**

A API do Pipefy é baseada em **GraphQL**. A operação principal será a mutação `createCard` para criar uma nova indicação de terreno.

### **2.1. Detalhes dos Pipelines**

A integração deverá ser capaz de apontar para dois pipelines distintos, um para testes e outro para produção.

| **Ambiente** | **Nome do Pipeline** | **ID do Pipeline** |
|----|----|----|
| Teste | (Teste) SZI - Terrenos | `306654506` |
| Produção | SZI - Terrenos | `304543320` |

## **3. Mapeamento de Campos (SAPRON -> Pipefy)**

A seguir está o mapeamento detalhado dos campos do formulário inicial do Pipefy para os campos do modelo `PartnerIndicationAllotment` do SAPRON.

**Nota:** A estrutura de campos (`start_form_fields`) é **idêntica** entre os pipelines de Teste e Produção, então este mapeamento é válido para ambos.

| **ID Pipefy** | **Label Pipefy** | **Campo SAPRON (Origem)** | **Opções Válidas** | **Observações / Mapeamento** |
|----|----|----|----|----|
| `id_sapron` | ID Sapron | `id` | N/A | Mapear diretamente do ID da instância `PartnerIndicationAllotment`. |
| `estado` | Estado | `state` | `"AC", "AL", "AP", ...` | Mapear diretamente. |
| `cidade` | Cidade | `city` | `"Abaré, BA", "Acrelândia, AC", ...` | Mapear diretamente. |
| `bairro` | Bairro | `neighborhood` | `"Centro", "Zona Rural", ...` | Mapear diretamente. |
| `endere_o` | Endereço | `street`, `number` | N/A | Concatenar: `f"{instance.street}, {instance.number}"`. |
| `coordenadas` | Coordenadas | `latitude`, `longitude` | N/A | Concatenar: `f"{instance.latitude}, {instance.longitude}"`. |
| `rea_total_m` | Área Total (m²) | `total_area` | N/A | Mapear diretamente. |
| `valor` | Valor | `appraisal_value` | N/A | Mapear diretamente. |
| `dimens_o_do_terreno` | Dimensão do terreno | `width`, `length` | N/A | Formatar como string, ex: `f"C={instance.length}, L={instance.width}"`. |
| `canal` | Canal | N/A | `"Seazone Serviços", "Parceiro B2B", ...` | Usar valor fixo. Sugestão: `"Plataforma"`. |
| `executivo_de_canais` | Executivo de Canais | N/A | N/A | Usar valor fixo. Sugestão: `"SAPRON API"`. |
| `parceiro` | Parceiro | `partner.name` | N/A | A partir da relação `partner`, buscar o nome. |
| `contato_do_parceiro` | Contato do Parceiro | `partner.user.phone` | N/A | A partir da relação `partner`, buscar o telefone. |
| `id_do_parceiro` | ID do Parceiro | `partner_id` | N/A | Mapear diretamente. |
| `matricula` | Matricula | `registry_number` | `"Sim", "Não", "Não sabemos"` | Se `registry_number` tiver valor, enviar `"Sim"`; senão, `"Não sabemos"`. **Este campo não recebe o número**, apenas indica a existência. |
| `obs_indicador` | OBS Indicador | `notes` | N/A | Mapear diretamente do campo `notes` do SAPRON. |
| `caracter_stica` | Característica | N/A | `"Pé na Areia", "Frente Mar", ...` | Mapear se a informação existir no SAPRON. |
| `poligono` | Poligono | `files` | N/A | **Avançado:** Se houver `PartnerIndicationAllotmentFile` com `document_type='area_sketch'`, requer upload de anexo. |

**Observação: Campos Obrigatórios sem Mapeamento Direto**

Os seguintes campos são obrigatórios no Pipefy mas não existem no modelo `PartnerIndicationAllotment` do SAPRON. Eles precisarão de um valor padrão ou serem adicionados ao modelo de dados do SAPRON. Para a integração, é necessário enviar uma das opções válidas para cada campo.

* `**tomadores_de_decis_o**` (Label: "Tomadores de Decisão:")
  * **Tipo:** `select`
  * **Opções:** "Único Decisor", "Vários Decisores", "Sem informação"
* `**interface_de_negocia_o**` (Label: "Interface de Negociação:")
  * **Tipo:** `select`
  * **Opções:** "Direto com Proprietário", "Único Parceiro", "Vários Parceiros", "Sem Informação"
* `**o_terreno_est_dentro_do_pol_gono**` (Label: "O terreno está dentro do polígono?")
  * **Tipo:** `radio_vertical`
  * **Opções:** "Sim", "Não"

## **4. Exemplo de Mutation GraphQL**

Abaixo, um exemplo de como a query GraphQL para a mutação `createCard` deve ser estruturada.

`mutation createCard ($input: CreateCardInput!) {`

`createCard (input: $input) {`

`card {`

`age`

`attachments_count`

`checklist_items_checked_count`

`checklist_items_count`

`comments_count`

`createdAt`

`creatorEmail`

`current_phase_age`

`done`

`due_date`

`emailMessagingAddress`

`expired`

`finished_at`

`id`

`inboxEmailsRead`

`late`

`overdue`

`path`

`public_form_submitter_email`

`started_current_phase_at`

`suid`

`title`

`updated_at`

`url`

`uuid`

`}`

`}`

`}`

**Exemplo de variáveis JSON para a mutação:**

O valor de `pipe_id` no exemplo (`306654506`) corresponde ao pipeline de **Teste**. Em um ambiente de produção, este valor deve ser alterado para o ID do pipeline de produção (`304543320`).

`{`

`"input": {`

`"pipe_id": "306654506",`

`"title": "[SAPRON] Indicação - Avenida Beira Mar, 1000",`

`"fields_attributes": [`

`{ "field_id": "id_sapron", "value": "12345" },`

`{ "field_id": "estado", "value": "SC" },`

`{ "field_id": "cidade", "value": "Florianópolis, SC" },`

`{ "field_id": "bairro", "value": "Centro" },`

`{ "field_id": "endere_o", "value": "Avenida Beira Mar, 1000" },`

`{ "field_id": "coordenadas", "value": "-27.59537, -48.54805" },`

`{ "field_id": "rea_total_m", "value": "5000" },`

`{ "field_id": "valor", "value": "10000000" },`

`{ "field_id": "canal", "value": "Plataforma" },`

`{ "field_id": "executivo_de_canais", "value": "SAPRON API" },`

`{ "field_id": "parceiro", "value": "Nome do Parceiro" },`

`{ "field_id": "contato_do_parceiro", "value": "+5548999998888" },`

`{ "field_id": "id_do_parceiro", "value": "54321" },`

`{ "field_id": "matricula", "value": "Sim" },`

`{ "field_id": "tomadores_de_decis_o", "value": "Sem Informação" },`

`{ "field_id": "interface_de_negocia_o", "value": "Sem Informação" },`

`{ "field_id": "o_terreno_est_dentro_do_pol_gono", "value": "Não" }]`

`}`

`}`

## **5. Plano de Ação**


1. **\[Backend\] Análise de Gaps:**
   * Analisar os campos obrigatórios do Pipefy que não existem no modelo `PartnerIndicationAllotment` (listados na observação da Seção 3) e definir uma estratégia: adicionar ao modelo ou usar valores padrão.
2. **\[Backend\] Configuração do Cliente GraphQL:**
   * Adicionar uma biblioteca Python para requisições GraphQL (ex: `gql`).
   * Configurar as variáveis de ambiente para o token da API e para os IDs dos pipelines. A aplicação deve determinar qual ID usar com base no ambiente (ex: `settings.DEBUG`).
     * `PIPEFY_API_TOKEN=...`
     * `PIPEFY_ALLOTMENT_TEST_PIPE_ID=306654506`
     * `PIPEFY_ALLOTMENT_PROD_PIPE_ID=304543320`
3. **\[Backend\] Desenvolvimento do Serviço de Integração:**
   * Criar um novo módulo/serviço (ex: `pipefy_integration_service.py`).
   * Implementar uma função `send_allotment_to_pipefy(allotment: PartnerIndicationAllotment)` que:
     * Recebe uma instância do modelo `PartnerIndicationAllotment`.
     * **Monta o payload** `**input**` conforme o mapeamento detalhado da Seção 3.
     * **Gera um título dinâmico para o card** (ex: `f"[SAPRON] {allotment.street}, {allotment.number}"`).
     * Executa a mutação `createCard`, usando o `pipe_id` correto para o ambiente.
     * Salva o ID do card retornado (`card.id`) no campo `pipefy_card_external_id` da instância `allotment`.

\n

\n