<!-- title: Fluxo Inteligente de Aprovação de Despesas | url: https://outline.seazone.com.br/doc/fluxo-inteligente-de-aprovacao-de-despesas-hlVmIMY6HC | area: Tecnologia -->

# Fluxo Inteligente de Aprovação de Despesas

# **1. Contexto e Problema**


O processo atual de aprovação de despesas é inteiramente manual, sem validações automáticas de inconformidades. Isso gera os seguintes problemas recorrentes:

* Retrabalho elevado do time de auditoria para verificar documentação básica
* Risco de aprovações incorretas por ausência de evidências adequadas
* Falta de rastreabilidade das justificativas de aprovação e reprovação
* Ausência de padronização nos critérios de análise entre auditores
* Tempo médio de análise elevado, especialmente para despesas simples

| 💡  Oportunidade: automatizar a triagem de inconformidades com IA, reduzindo o esforço manual e aumentando a consistência das análises. |
|----|

# **2. Objetivos do Discovery**

| 🎯 | Implementar triagem automática de despesas com base em evidências anexadas |
|----|----|
| ⚡ | Aumentar a agilidade no processo de análise e aprovação |
| 🔍 | Reduzir o volume de revisões manuais desnecessárias |
| 📋 | Garantir rastreabilidade completa das justificativas de aprovação/reprovação |
| 📊 | Criar base de dados para metrificação contínua da qualidade da triagem |

# **3. Escopo**

### **3.1 Categorias com Fluxo Automatizado (IA)**

| **Categoria** | **Subcategoria / Observação** |
|----|----|
| Enxoval | Itens de cama, banho, cozinha etc  |
| Implantação | Chaves, limpeza e lavagem de goma etc |
| Reserva de Proprietário | Limpeza |
| Itens Mínimos | Compra de itens básicos da unidade |
| Manutenção | Reforma, melhorias, adequações, danos de hóspede |
| Serviços de Terceiros | Qualquer prestação de serviço terceirizado |
| Compra de Material | Materiais de consumo e reposição |

# **4. Definição de Status e Fluxo Geral**

### **4.1 Mapa de Status**


:::warning
Apenas as despesas de I**MPLANTAÇÃO** e **RESERVA DO PROPRIETÁRIO**, quando a subcategoria é **LIMPEZA,** não seguem a regra abaixo e são **aprovadas IMEDIATAMENTE**, sem passar pelo fluxo de pré-aprovado

:::

| **Status** | **Origem** | **Ação do Sistema** | **Próximos Passos** |
|----|----|----|----|
| **Em Análise** | Envio pelo lançador | Pré-processamento + IA classifica a despesa | IA retorna decisão |
| **Pré-aprovado** | IA aprova a despesa | Justificativa da IA registrada. Fila de confirmação do auditor | Auditor: Aprova → AprovadoAuditor: Reprova → ReprovadoAuditor: Devolve → Pendente (com motivo) |
| **Pendente** | IA não aprova (motivo registrado) ou auditor devolve do Pré-aprovado | Motivo da pendência registrado. Lançador notificado para correção | Lançador corrige e reenvia → volta a Em Análise |
| **Aprovado** | Auditor confirma o Pré-aprovado | Registro final com log completo | Financeiro processa |
| **Reprovado** | Auditor rejeita o Pré-aprovado | Justificativa obrigatória registrada | Lançador notificado |

| 📌  Nota sobre o status Pendente - O status Pendente é único e centraliza duas origens distintas:  1. IA não aprova a despesa → motivo identificado pela IA é registrado automaticamente no campo 'Motivo da Pendência'  2. Auditor devolve um Pré-aprovado → auditor informa o motivo manualmenteNão há status separado de 'Alerta de Inconformidade'. Qualquer inconformidade identificada pela IA resulta em Pendente com o motivo documentado. |
|----|

### **4.2 Fluxo Macro — Visão Geral**

| **FLUXO MACRO DE APROVAÇÃO**<br>1. Lançador submete despesa (categoria + descrição + valor + evidências)         ↓2. Pré-processamento: validação de NF/recibo, descrição, categoria e valor         *↓  (falhas no pré-processamento → Pendente com motivo registrado + notificação ao lançador)*3. Status: Em Análise — aguardando classificação da IA         ↓4. IA avalia evidências com prompt parametrizado por categoria e retorna decisão + justificativa         ↓5a. IA aprova → status Pré-aprovado → justificativa registrada → fila de confirmação do auditor5b. IA não aprova → status Pendente → motivo da IA registrado → lançador notificado para correção         *↓  (lançador corrige → volta a Em Análise)*6. Auditor revisa o Pré-aprovado:      → Confirma: status Aprovado      → Reprova: status Reprovado (justificativa obrigatória)      → Devolve: status Pendente (motivo obrigatório → lançador corrige → volta a Em Análise)         ↓7. Status final: Aprovado ou Reprovado → Financeiro processa |
|----|

# **5. Avaliação por IA — Prompts por Categoria**

O prompt é construído e enviado à IA pelo código de backend. Cada chamada compõe o prompt-base injetando o bloco de regras específico da categoria no campo {category_rules}. A IA recebe as evidências como anexos (imagens, PDFs, notas fiscais, conversas) e retorna exclusivamente um objeto JSON — sem texto adicional. O código deve fazer JSON.parse() direto na resposta.

### **5.1 Prompt-Base — System Prompt**

Enviado como system prompt em todas as chamadas, independente da categoria:

| You are a financial auditing AI for a short-term rental property management platform.Your job is to evaluate expense records submitted by property managers based on theattached evidence files (images, PDFs, receipts, invoices, and conversation screenshots).You must respond ONLY with a valid JSON object — no markdown, no explanation, no text outside the JSON.Any response that is not a parseable JSON object will be treated as a system error. |
|----|

### **5.2 Prompt — User Message (parametrized per request)**

Enviado como user message. Os campos entre chaves são substituídos pelo código antes do envio:

| Evaluate the following expense record based on the attached evidence files.## Expense Data- category:            {category}- subcategory:         {subcategory}- item:                {item}- description:         {description}- amount:              BRL {amount}- max_cleaning_fee:    BRL {max_cleaning_fee}   // null if not applicable## General Rules (apply to ALL categories)1. Fiscal evidence (receipt or invoice) must be present and must reasonably match the declared   amount and description. Minor naming differences are acceptable   (e.g., "soup spoons" vs "kitchen spoons").2. Service evidence must be consistent with the description provided.3. Both fiscal evidence and service evidence must be present, unless the category rules say otherwise.4. If amount > 300 BRL AND category is NOT in the exempt list, owner pre-approval evidence   (screenshot, email, or message) must be present and contextually aligned with the expense.   Exempt from owner approval rule: \[Owner Reservation, Implantation Cleaning, Linen Washing\]## Category-Specific Rules{category_rules}## Required JSON Response SchemaRespond ONLY with this JSON object — no markdown, no backticks, no surrounding text:{  "decision":       "approved" \| "pending",  "reason":         "One or two sentences explaining the decision. Must be specific and actionable.",  "missing_fields": \["array of specific missing or invalid fields — empty array \[\] if approved"\],  "rules_checked":  \["array of rule IDs that were evaluated, e.g. R1, R2, R3"\]}Rules for filling the response:- Use "approved" only when ALL rules are clearly satisfied by the evidence.- Use "pending" when ANY rule fails or cannot be confirmed from the evidence.- "reason" must be actionable: the submitter will read it to understand exactly what to fix.- "missing_fields" must list field names or evidence types that are absent or insufficient.- Do NOT infer, assume, or guess beyond what the evidence explicitly shows. |
|----|

### **5.3 Exemplo de Resposta Esperada da IA**

Exemplos do que o código deve receber e processar via JSON.parse():

| ✅  Aprovado — exemplo de resposta: |
|----|

| {  "decision":       "approved",  "reason":         "Receipt matches declared amount and description. Service photo confirms execution.",  "missing_fields": \[\],  "rules_checked":  \["R1", "R2", "R3"\]} |
|----|

| ⏳  Pendente — exemplo de resposta: |
|----|

| {  "decision":       "pending",  "reason":         "Quantity of items purchased is missing from both the description and the receipt.",  "missing_fields": \["item_quantity"\],  "rules_checked":  \["R1", "R2", "R3"\]} |
|----|

### **5.4 Blocos de Regras por Categoria — {category_rules}**

Os blocos abaixo são injetados no campo {category_rules} do user message. O código deve selecionar o bloco correto com base na categoria e subcategoria antes de montar o prompt.

## **5.4.1 Enxoval**

| CATEGORY RULES — LINEN (Enxoval):  R1 \[item_type\]     The description or receipt must specify the type of item                     (e.g., bed sheet, towel, pillowcase, duvet).  R2 \[item_quantity\] The quantity of items purchased must be present in the description or receipt.                     If absent in both → pending.  R3 \[category_fit\]  The item described must be coherent with the Linen category.                     If the description refers to unrelated items (e.g., tools, repairs) → pending. |
|----|

## **5.4.2 Implantação — Chaves**

| CATEGORY RULES — IMPLANTATION: KEYS (Implantação — Chaves):  R1 \[key_quantity\]  The number of key copies made must be stated in the description or receipt.  R2 \[key_type\]      The type of key must be specified (e.g., conventional, electronic, key card).                     If either is missing from both description and receipt → pending. |
|----|

## **5.4.3 Implantação — Limpeza**

| CATEGORY RULES — IMPLANTATION: CLEANING (Implantação — Limpeza): This category uses a SEQUENTIAL validation chain. Evaluate rules in order. Stop at the first failure and report it immediately. Do NOT continue to the next rule after a failure. System data pre-computed and injected by the backend: property_cleaning_fee : BRL {property_cleaning_fee} property_in_onboarding : {property_in_onboarding} --- STEP 1: Declared amount equals the property cleaning fee --- R1 \[amount_matches_cleaning_fee\] Compare: amount vs property_cleaning_fee (allow ±0.01 BRL tolerance for rounding). IF property_cleaning_fee is null → STOP. Return: decision : "pending" missing_fields : \["property_cleaning_fee"\] reason : "Cleaning fee not configured for this property. Manual review required." IF amount != property_cleaning_fee → STOP. Return: decision : "pending" missing_fields : \["amount_mismatch"\] reason : "Declared amount (BRL {amount}) does not match the property cleaning fee (BRL {property_cleaning_fee}). Adjust the amount or justify the difference with additional evidence." --- STEP 2: Property was in onboarding status within the last 30 days --- R2 \[property_in_onboarding\] Only evaluate if R1 passed. Check: property_in_onboarding value. IF "false" → STOP. Return: decision : "pending" missing_fields : \["onboarding_status"\] reason : "This property was not in onboarding status in the last 30 days. Implantation cleaning is only applicable during the onboarding period." IF "unavailable" → STOP. Return: decision : "pending" missing_fields : \["onboarding_status"\] reason : "Could not verify onboarding status for this property. Manual review required." --- STEP 3: Owner approval --- R3 \[owner_approval_exempt\] Owner pre-approval is NEVER required for this category, even if amount > 300 BRL. Do not check, mention, or flag owner approval under any circumstances. --- FINAL DECISION --- IF R1 + R2 both pass → Return: decision : "approved" missing_fields : \[\] reason : "Declared amount matches the property cleaning fee and property was confirmed in onboarding status within the last 30 days." |
|----|

## **5.4.4 Implantação — Lavagem de Goma**

| CATEGORY RULES — IMPLANTATION: LINEN WASHING (Implantação — Lavagem de Goma):  R1 \[items_and_qty\]  The description or receipt must list the items washed and their quantities.                      Acceptable example: "2 duvets, 4 pillowcases, 3 bath towels".                      If items and quantities are absent in both → pending.  R2 \[owner_approval\] |
|----|

## **5.4.5 Reserva de Proprietário — Limpeza**

| ⚙️  ATENÇÃO AO TIME DE DESENVOLVIMENTO - Esta categoria exige que o código execute consultas ao sistema de reservas ANTES de chamar a IA.Os resultados dessas consultas devem ser injetados no prompt como campos adicionais (ver abaixo).A IA não tem acesso direto ao sistema — ela avalia apenas os dados que o código fornecer. |
|----|

### **Campos adicionais obrigatórios — injetar no prompt desta categoria:**

| **Campo no Prompt** | **Tipo** | **Como obter** |
|----|----|----|
| **{reservation_date_from_description}** | string \| null | Extraído da descrição via parse de data pelo código antes de chamar a IA |
| **{owner_block_found}** | "true" \| "false" \| "unavailable" | Consulta à API de reservas: existe bloqueio de proprietário no imóvel para a data informada? |
| **{property_cleaning_fee}** | number \| null | Taxa de limpeza cadastrada para o imóvel. Null se não cadastrada. |

### **Bloco {category_rules} — injetado no user message:**

| CATEGORY RULES — OWNER RESERVATION: CLEANING (Reserva de Proprietário — Limpeza):This category uses a SEQUENTIAL validation chain.Evaluate rules in order. Stop at the first failure and report it immediately.Do NOT continue to the next rule after a failure.System data pre-computed and injected by the backend:  reservation_date_from_description : {reservation_date_from_description}  owner_block_found                  : {owner_block_found}  property_cleaning_fee              : BRL {property_cleaning_fee}--- STEP 1: Reservation date in description ---R1 \[reservation_date_present\]  Check: is reservation_date_from_description a valid date (not null)?  IF null → STOP. Return:    decision       : "pending"    missing_fields : \["reservation_date"\]    reason         : "Reservation date not found in the description. Include the date of                      the owner reservation this cleaning refers to."--- STEP 2: Owner block confirmed in the system ---R2 \[owner_block_confirmed\]  Only evaluate if R1 passed.  Check: owner_block_found value.  IF "false" → STOP. Return:    decision       : "pending"    missing_fields : \["owner_block"\]    reason         : "No owner block found on {reservation_date_from_description} for this                      property. Verify the date or check if the block is registered."  IF "unavailable" → STOP. Return:    decision       : "pending"    missing_fields : \["owner_block"\]    reason         : "Reservations system unavailable — could not verify owner block.                      Manual review required."--- STEP 3: Declared amount equals the property cleaning fee ---R3 \[amount_matches_cleaning_fee\]  Only evaluate if R1 and R2 passed.  Compare: amount vs property_cleaning_fee (allow ±0.01 BRL tolerance for rounding).  IF property_cleaning_fee is null → STOP. Return:    decision       : "pending"    missing_fields : \["property_cleaning_fee"\]    reason         : "Cleaning fee not configured for this property. Manual review required."  IF amount != property_cleaning_fee → STOP. Return:    decision       : "pending"    missing_fields : \["amount_mismatch"\]    reason         : "Declared amount (BRL {amount}) does not match the property cleaning                      fee (BRL {property_cleaning_fee}). Adjust the amount or justify the                      difference with additional evidence."--- STEP 4: Owner approval ---R4 \[owner_approval_exempt\]  Owner pre-approval is NEVER required for this category, even if amount > 300 BRL.  Do not check, mention, or flag owner approval under any circumstances.--- FINAL DECISION ---  IF R1 + R2 + R3 all pass → Return:    decision       : "approved"    missing_fields : \[\]    reason         : "Reservation date confirmed, owner block verified, and amount matches                      the property cleaning fee." |
|----|

## **5.4.6 Reserva de Proprietário — Comissão**

| CATEGORY RULES — OWNER RESERVATION: COMMISSION (Reserva de Proprietário — Comissão):  R1 \[reservation_date\] The reservation date must be present in the description or receipt.  R2 \[guest_name\]       The name of the guest who was served must be stated in the                        description or receipt. If either is missing → pending. |
|----|

## **5.4.7 Itens Mínimos**

| CATEGORY RULES — MINIMUM ITEMS (Itens Mínimos):  R1 \[purchase_reason\]  The description must explain why the items were purchased                        (e.g., item ran out, replacement after damage).  R2 \[item_quantity\]    The quantity purchased must be informed.  R3 \[item_photo\]       A photo of the purchased items must be present in the evidence.                        If any of the above are missing → pending. |
|----|

## **5.4.8 Manutenção**

| CATEGORY RULES — MAINTENANCE (Manutenção):  R1 \[maintenance_reason\]  The reason for the maintenance must be clearly described.  R2 \[service_detail\]      The service performed must be detailed: what was done, where, and how.  R3 \[execution_photo\]     A photo showing the maintenance execution or result must be in the evidence.                           If any of the above are missing → pending. |
|----|

## **5.4.9 Serviços de Terceiros**

| CATEGORY RULES — THIRD-PARTY SERVICES (Serviços de Terceiros):  R1 \[service_reason\]   The reason for hiring the service must be described.  R2 \[service_detail\]   The service performed must be described in detail.  R3 \[execution_photo\]  A photo or visual proof of the service execution must be in the evidence.                        If any of the above are missing → pending. |
|----|

# **6. Fluxo de Dano de Hóspede**

| 🔴  Esta é a validação mais sensível do sistema. Requer cruzamento com a base de reservas e verificação de duplicidade. |
|----|

### **6.1 Gatilhos de Identificação**

O fluxo de Dano de Hóspede é ativado quando a descrição ou categoria contiver termos relacionados a:

* Dano  /  Avaria  /  Quebra
* Hóspede danificou  /  Hóspede quebrou
* Reparo por uso indevido
* Ressarcimento de dano

### **6.2 Dados Obrigatórios para Prosseguimento**

Ao identificar um dano de hóspede, o sistema exige ao menos um dos seguintes dados:

| **Dado Obrigatório** | **Observação** |
|----|----|
| **Nome do hóspede** | Deve ser suficiente para cruzamento com reserva |
| **Data de checkout** | Data em que o hóspede deixou a unidade |
| **Descrição do dano** | O que foi danificado, onde, condição anterior |

| 🚫  Se nenhum dos dados acima estiver presente → status Pendente.Motivo registrado: 'Identificação do hóspede ausente — informe o nome do hóspede ou a data de checkout e descreva o dano ocorrido'.O lançador é notificado para complementar antes de nova análise. |
|----|

### **6.3 Cruzamento com Base de Reservas**

Com os dados fornecidos, o sistema consulta a base de reservas e tenta identificar a reserva correspondente:

* Por nome do hóspede (busca textual, tolera variações ortográficas menores)
* Por data de checkout (tolerância de ±1 dia para cobrir horários de virada)
* A unidade do lançamento é usada como filtro adicional

| **Resultado do Cruzamento** | **Status** | **Ação** |
|----|----|----|
| Reserva encontrada com match | **Segue para avaliação da IA** | IA avalia evidências do dano |
| Reserva NÃO encontrada | **Pendente** | Motivo: 'Nenhuma reserva compatível localizada com os dados informados' → Auditor analisa manualmente |

### **6.4 Verificação de Duplicidade de Dano**

Antes de finalizar, o sistema verifica se já existe lançamento anterior vinculado à mesma:

* Reserva (ID)  /  Data de checkout  /  Nome do hóspede
* Tipo de dano semelhante (verificação semântica)

| ⚠️  Se duplicidade detectada → status Pendente.Motivo registrado: 'Possível lançamento duplicado — já existe registro de dano vinculado a esta reserva ou hóspede'.O auditor deve analisar manualmente antes de qualquer aprovação. |
|----|

### **6.5 Prompt Específico para Dano de Hóspede**

| REGRAS ESPECÍFICAS — DANO DE HÓSPEDE:  1. Deve haver identificação do hóspede (nome) ou data de checkout nas evidências ou descrição.  2. A descrição do dano deve ser clara: o que foi danificado, estado anterior e estado atual.  3. Deve haver evidência visual (foto) do dano.  4. O valor lançado deve ser compatível com o tipo de reparo/reposição descrito.  5. Cruzamento com reserva: {resultado_cruzamento_reserva}  6. Verificação de duplicidade: {resultado_verificacao_duplicidade}  7. Se qualquer item acima estiver ausente ou inconsistente → Não Aprovado. |
|----|

# **7. Fluxo Pós-Avaliação e Aprovação Final**

\n

### **7.1 Quando a IA Aprova — Status: Pré-aprovado**

* A despesa entra automaticamente na fila de confirmação do auditor
* O campo 'Justificativa da IA' é preenchido com o texto retornado pela IA
* Um indicador visual distingue lançamentos 'Pré-aprovados por IA' dos analisados manualmente\n

A partir do status Pré-aprovado, o auditor tem três caminhos:

| **Ação do Auditor** | **Status Resultante** | **Obrigações** |
|----|----|----|
| **Confirmar** | **Aprovado** | Nenhuma — apenas confirmação da decisão da IA |
| **Reprovar** | **Reprovado** | Justificativa obrigatória. Lançador notificado. |
| **Devolver para Pendente** | **Pendente** | Motivo obrigatório. Lançador notificado para corrigir e reenviar. Despesa retorna a Em Análise após correção. |

### **7.2 Quando a IA Não Aprova — Status: Pendente**

* A despesa vai automaticamente para status Pendente
* O campo 'Motivo da Pendência' é preenchido com a justificativa retornada pela IA
* O lançador é notificado com o motivo exato identificado pela IA
* O lançador corrige os problemas apontados e reenvia a despesa
* Ao reenviar, a despesa retorna ao status Em Análise e passa novamente pela avaliação completa

| 📌  O motivo da pendência fica sempre visível no histórico do lançamento, independentemente de quantas vezes ele seja reenviado. Isso garante rastreabilidade completa do ciclo de vida da despesa. |
|----|

### **7.3 Reversão Manual pelo Auditor (Pré-aprovado → Reprovado ou Pendente)**

| 📌  REGRA DE NEGÓCIO CRÍTICAQuando o auditor devolver ou reprovar um Pré-aprovado, o sistema deve:  1. Exigir preenchimento obrigatório do campo 'Motivo' (Reprovação ou Devolução)  2. Registrar: usuário, timestamp, decisão original da IA e nova decisão do auditor  3. Marcar o lançamento com a flag 'Decisão Revertida Manualmente'  4. Contabilizar a reversão nas métricas de performance da IA para retreinamento futuro |
|----|

# **8. Rastreabilidade e Métricas**

### **8.1 Log de Auditoria — Campos Obrigatórios por Lançamento**

| **Campo** | **Descrição** |
|----|----|
| **decision_ia** | Resultado da IA: Aprovado \| Não Aprovado |
| **justificativa_ia** | Texto completo retornado pela IA (aprovação ou motivo da pendência) |
| **motivo_pendencia** | Motivo registrado quando status = Pendente (da IA ou do auditor) |
| **origem_pendencia** | Quem gerou a pendência: 'IA' \| 'Auditor' \| 'Pré-processamento' |
| **status_final** | Status definido após ação do auditor: Aprovado \| Reprovado |
| **revertida_manualmente** | Boolean — indica se o auditor reverteu o Pré-aprovado (Reprovado ou Pendente) |
| **motivo_reversao** | Texto obrigatório quando revertida_manualmente = true |
| **usuario_revisao** | ID do auditor que revisou |
| **timestamp_ia** | Data/hora da avaliação pela IA |
| **timestamp_revisao** | Data/hora da ação do auditor |
| **categoria_detectada_ia** | Categoria que a IA classificou para validação |

### **8.2 Métricas de Performance da IA**

| **Métrica** | **Fórmula** | **Meta Inicial** |
|----|----|----|
| **Taxa de Acerto da IA** | 1 - (reversões do auditor / total pré-aprovados pela IA) | **> 80%** |
| **Taxa de Pendência por IA** | Pendentes originados pela IA / total avaliado | **Monitoramento** |
| **Taxa de Pendência por Auditor** | Pré-aprovados devolvidos pelo auditor / total pré-aprovados | **< 10%** |
| **Tempo Médio de Triagem** | timestamp_revisão - timestamp_envio (para pré-aprovados) | **< 2h** |
| **Taxa de Reenvio** | Lançamentos com ciclos_reenvio > 1 / total enviados | **< 20%** |
| **Motivos de Pendência Mais Frequentes** | Agrupamento por motivo_pendencia | **Alimenta melhoria de UX** |

### 

\n