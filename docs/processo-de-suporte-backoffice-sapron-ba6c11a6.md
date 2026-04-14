<!-- title: Processo de Suporte Backoffice (Sapron) | url: https://outline.seazone.com.br/doc/processo-de-suporte-backoffice-sapron-JYRU37pBM8 | area: Tecnologia -->

# Processo de Suporte Backoffice (Sapron)

## 🗺️ Objetivo

Este documento descreve o processo de atendimento a solicitações de suporte relacionadas ao sistema Sapron, garantindo uma abordagem padronizada e eficiente para resolução de problemas.

O link do produto em STG é <https://test.staging.sapron.com.br/home>

## ⚖️ Abertura do Suporte

O suporte do Sapron é aberto via Pipefy:

**Formulário Pipefy:** <https://app.pipefy.com/public/form/rqkWznfg>

O formulário deve ser preenchido com:

* Resumo do problema
* Descrição detalhada
* Passos para reproduzir (se aplicável)
* Evidências: prints, logs ou vídeos

Os cards abertos caem no Kanban de **Suporte Sapron**:

**Pipefy Sapron:** <https://app.pipefy.com/pipes/304437472>

## 🛠️ Escopo

Aplica-se a todas as solicitações de suporte referentes ao Sapron, incluindo:

* Erros no sistema
* Problemas operacionais
* Dúvidas sobre funcionalidade
* Sugestões de melhoria

## 📂 Caixa de Entrada

O suporte é revisado para:

* Validar se é um suporte válido
* Verificar se está completo

### Ações Possíveis:

* **Incompleto**: colocar a etiqueta "Aguardando Resposta"
* **Não aceito**: vai para "Cancelado"
* **Aceito e completo**: vai para "Priorizacão"

  \

## ⏳ Priorizacão e Tempo de Resposta

A classificação dos cards segue o impacto e urgência:

| Prioridade | Tempo Estimado |
|----|----|
| P0 - Highest | 1 a 4 horas |
| P1 - High | 1 dia |
| P2 - Medium | 1 a 3 dias |
| P3 - Low | 5 a 7 dias |
| P4 - Lowest | +15 dias |


## 💾 Destino dos Cards

Dependendo do tipo, os cards podem ser movidos para:

* **Escalar ao Jira** (quando exige dev)
* **Em atendimento** (quando o próprio responsável resolve)

### Escalar ao Jira

Criação de Issues:

* **Bug**: Quando o tipo é "Bug no Sapron"
* **Task**: Quando é "Pedido Operacional" ou "Sugestão de melhoria"

### Em Atendimento

O Responsável analisa e resolve ou encaminha ao time correto.


## ✅ Conclusão do Suporte

* Validação feita em produção
* Card movido para "Concluído"
* Cliente é comunicado (Slack ou outro canal)


## 🔹 Fluxograma do Processo

* Pipefy (Kanban e Flow): https://app.pipefy.com/pipes/304437472/flow

  \

*O processo a seguir segue o seguinte fluxo:*

 ![](/api/attachments.redirect?id=1b620b8e-12cc-44ce-b42f-d99a56b2d8bd)

 ![](/api/attachments.redirect?id=ea0e6b78-0751-41e2-b59d-78dcffd501ff)

 ![](/api/attachments.redirect?id=4fdbbec5-ec02-40b1-bee7-a957bea3959e "left-50 =295x219")