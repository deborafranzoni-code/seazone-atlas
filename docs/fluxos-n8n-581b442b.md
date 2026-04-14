<!-- title: Fluxos N8N | url: https://outline.seazone.com.br/doc/fluxos-n8n-gx8hFc6uby | area: Tecnologia -->

# Fluxos N8N

# Plano de Teste: Cadência de Leads (n8n)

## 1. Visão Geral

O objetivo deste plano é validar a lógica de progressão de leads através de uma cadência automatizada, garantindo que as mensagens sejam enviadas no tempo correto, respeitando as regras de transbordo e status do lead.

## 2. Abordagem de Fluxo de Grafos (Structural Testing)

Para garantir cobertura total, dividimos o fluxo em nós (nodes) e arestas (edges), identificando os caminhos críticos (Paths).


**Fluxo de Exemplo:  ==\[TRIGGER\] Cadência de Leads==**

### Grafo de Caminhos Críticos:


1. **Caminho Feliz (Novo Lead):** Trigger -> Normalized Input -> initial_step? (Sim) -> Run_Cadence_1.
2. **Caminho de Progressão (Lead em Andamento):** Trigger -> initial_step? (Não) -> get_step_executed -> step_age (Válido) -> next_step? (Sim) -> Run_Cadence_N.
3. **Caminho de Transbordo (Fim da Cadência):** Trigger -> next_step? (Não) -> get_labels_deal -> Transbordo.
4. **Caminho de Exceção (Parceria):** Trigger -> next_step? (Não) -> if_not_parc? (Não) -> lost_parc.
5. **Caminho de Bloqueio (Filtro de Idade):** Trigger -> deal_age (Não atingido) -> Filtro (Drop).


## 3. Tabela de Decisão (Logic Testing)

Esta tabela mapeia as combinações de entrada para as ações esperadas, focando nas regras de negócio extraídas dos nós IF e Filter.

| **ID** | **Is Test** | **Step Label** | **Deal Age** | **Step Age** | **Respondeu MIA** | **Tag** | **Ação Esperada** |
|----|----|----|----|----|----|----|----|
| TC01 | True | 0 ou 1 | N/A | N/A | N/A | any | Executa Run_Cadence_1 (Ignora filtros de tempo) |
| TC02 | False | 0 ou 1 | > 1470 | N/A | Não | any | Executa Run_Cadence_1 |
| TC03 | False | 0 ou 1 | < 1470 | N/A | Não | any | Lead Retido (Aguardando tempo de criação) |
| TC04 | False | > 1 | N/A | > 1470 | Não | any | Executa Run_Cadence_N |
| TC05 | False | > 1 | N/A | < 1470 | Não | any | Lead Retido (Aguardando intervalo entre passos) |
| TC06 | False | any | any | any | Sim | any | Lead Retido (Filtro deal_age barra quem respondeu) |
| TC07 | False | > Max | N/A | > 1470 | Não | !parc | Executa Transbordo (Finalização padrão) |
| TC08 | False | > Max | N/A | > 1470 | Não | parc | Executa lost_parc (Regra específica p/ parceiros) |


---

## 4. Estratégia de Teste por Subfluxo (Modular)

Cada subfluxo deve ser testado isoladamente utilizando a técnica de **Mocking**.

### Subfluxo A: Normalização e Tagging (normalized_input)

* **Entrada (Mock):** JSON com pipeline_id, Prédio B2B e labels do Pipedrive.
* **Execução:** Rodar apenas os nós de tag_definition e normalized_input.
* **Saída Esperada:** Objeto com tag (ex: 'szs_b2b'), max_step e step_from_label.
* **Assertion:** assert($json.tag).toBe('szs_b2b') se Prédio B2B for "Sim".

### Subfluxo B: Seleção de Template (select_message_template)

* **Entrada (Mock):** deal_id, step, tag.
* **Execução:** Chamada ao workflow iFW8k3OUID2LocKU.
* **Saída Esperada:** String message_template.
* **Assertion:** Verificar se o template retornado corresponde ao esperado para o step X da tag Y.

### Subfluxo C: Orquestrador de Disparo (Run_Cadence_N)

* **Entrada (Mock):** Payload completo do nó cadence_input.
* **Execução:** Chamada ao workflow 86BTNup3dpcIwcsq.
* **Saída Esperada:** Status de execução (Success/Error).
* **Assertion:** Validar se o instance_id e product_id foram passados corretamente para evitar disparos pela instância errada.

### Subfluxo D: Transbordo e Finalização (Transbordo)

* **Entrada (Mock):** deal_id, pipeline_id, tag.
* **Execução:** Chamada ao workflow gTxfU3O1chO1EEIf.
* **Saída Esperada:** Deal atualizado no Pipedrive.
* **Assertion:**

  
  1. Verificar se a label 4659 (Cadência concluída) foi adicionada.
  2. Verificar se a label de controle de step foi removida.


---

## 5. Guia para Novos Fluxos (Padrão de Qualidade)

Para manter a consistência em outros fluxos de cadência, os seguintes critérios devem ser seguidos:


1. **Sanitização Obrigatória:** Todo fluxo deve iniciar com um nó de "Set" ou "Code" que padroniza a entrada, tratando casos de null ou undefined (como feito no sanitize_test).
2. **Idempotência:** O fluxo deve ser capaz de rodar múltiplas vezes sem duplicar ações. (Uso do nó Remove Duplicates é mandatório).
3. **Logging de Execução:** Sempre salvar o estado da execução em um banco externo (Baserow/Redis) para que o nó step_age possa validar o intervalo entre interações.
4. **Error Handling:** Todo fluxo deve ter um Error Workflow configurado nas configurações do workflow para alertar o time de operações em caso de falha nos subfluxos de disparo.
5. **Timezone Lock:** Sempre forçar o fuso horário (ex: America/Sao_Paulo) nos cálculos de diff de minutos para evitar disparos em horários indevidos devido a variações de servidor.