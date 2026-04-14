<!-- title: Documentação do Usuário | url: https://outline.seazone.com.br/doc/documentacao-do-usuario-DIlYkUgpKC | area: Tecnologia -->

# Documentação do Usuário

# 📄 Manual do Usuário: Gestão de Listings em Quarentena

Este documento tem como objetivo orientar o uso da planilha de controle de Listings, detalhando o fluxo de trabalho diário, o significado de cada status e o impacto nas metas e bloqueios.

## 1. Visão Geral e Atualização

A planilha é composta por **3 abas principais** de uso:


1. **Listings em Quarentena** (Aba de trabalho diário)
2. **Liberar da Quarentena** (Histórico de listings mantidos, mas verificados)
3. **Inativa da Meta** (Listings excluídos do cálculo)

**Horário de Atualização:** A aba **"Listings em Quarentena"** é atualizada automaticamente todos os dias entre **06:00 e 07:00 da manhã**. Novos listings detectados pelas regras aparecerão após esse horário.

## 2. Como Utilizar a Aba "Listings em Quarentena"

Esta é a aba principal onde a análise deve ser realizada. Ela contém 4 colunas, mas o fluxo de trabalho foca nas seguintes colunas principais:

* **airbnb_listing_id:** O código de identificação do concorrente no Airbnb.
* **rule:** A regra específica que gerou o alerta e colocou o listing em quarentena.
* **comentario:** Campo livre para deixar observações para outros analistas (ex: "Verificado por Fulano", "Dúvida sobre preço").

### O Fluxo de Decisão (Coluna Status e Check)

Para cada listing, você deve tomar uma decisão usando a coluna **Status** (botão suspenso) e confirmar a ação na coluna **Check**.

#### Passo a Passo:


1. Analise o listing e a regra (`rule`).
2. Selecione uma das 3 opções na coluna **Status**:
   * **Em análise:** Use quando estiver verificando o caso, mas ainda não tiver certeza. *Nenhuma ação de movimento é feita.*
   * **Liberar da meta:** Move o listing para a aba "Liberar da Quarentena".
   * **Inativar da Meta:** Move o listing para a aba "Inativar da Meta".
3. **IMPORTANTE:** Após selecionar o status (Liberar ou Inativar), você deve marcar a coluna **CHECK**.
   * *O "Check" é o gatilho que realiza o transporte do ID para a aba de destino.*

## 3. Entendendo as Consequências (Para onde vai o listing?)

É crucial entender a diferença entre "Liberar" e "Inativar", pois isso afeta o cálculo da meta e os bloqueios de calendário.

### A. Opção "Liberar da Meta"

* **Destino:** O listing vai para a aba **"Liberar da Quarentena"**.
* **Comportamento:** O sistema **continua bloqueando** as datas desse imóvel de acordo com a `rule` (regra) detectada.
* **Manutenção:** Esta aba é **resetada (limpa)** automaticamente na virada de cada mês.

### B. Opção "Inativar da Meta"

* **Destino:** O listing vai para a aba **"Inativar da Meta"**.
* **Comportamento:** O imóvel é **excluído por completo** de qualquer cálculo de meta. Ele deixa de ser considerado na estratégia atual.

## 4. Resumo Rápido

| Ação / Status | O que acontece na planilha? | Impacto no Negócio |
|----|----|----|
| **Em análise** | Nada muda. | Sinaliza que alguém está trabalhando no item. |
| **Liberar da meta** (+ Check) | Move para aba "Liberar da Quarentena". | Mantém o bloqueio de datas conforme a regra. Aba limpa mensalmente. |
| **Inativar da Meta** (+ Check) | Move para aba "Inativar da Meta". | Remove o listing totalmente do cálculo da meta. |

### Dica Importante

Sempre verifique se a coluna **Check** foi marcada após escolher o status. Sem o check, o listing permanecerá na aba de quarentena pendente de ação.