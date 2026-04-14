<!-- title: Check-in Franquia | url: https://outline.seazone.com.br/doc/check-in-franquia-xkd5v5I3L8 | area: Tecnologia -->

# Check-in Franquia

# Check-in da Franquia

## Objetivos do Fluxo da Franquia

* Garantir cumprimento de exigências legais.
* Reduzir contato manual.
* Padronizar comunicação.
* Garantir rastreabilidade da entrega de acesso.


---

## Estrutura por Atividades

O fluxo da franquia é orientado por tarefas diárias que contemplam o escopo do check-in. A liberação de cada tarefa depende da completude da tarefa anterior.


---

## Atividade 1 — Mensagem 1 Dia Antes

### Gatilho para envio manual através do sistema:

* D-1 do check-in

### Cenários:

#### Cenário A — Hóspede já preencheu formulário

* Mensagem:
  * Confirmação de recebimento
  * Reforço do horário informado
* Interface da franquia:
  * Visualizar:
    * Documentos
    * Horário de chegada
    * Carro
    * Pet

#### Cenário B — Hóspede NÃO preencheu

* Mensagem:
  * Reforçar obrigatoriedade do check-in digital
  * Informar que acesso poderá ser bloqueado sem preenchimento

Sistema deve:

* Destacar reserva como "Check-in não concluído"


---

## Atividade 2 — Mensagem do Dia do Check-in

### Gatilho para envio manual através do sistema:

* Data do check-in

### Ação:

* Enviar mensagem do DIA D contendo:
  * Localização do imóvel
  * Instruções gerais

### Se for Self Check-in:

* Criar tarefa automática → Atividade 3


---

## Atividade 3 — Liberação da Senha (Self Check-in)

* * Manual (franquia clica em "Liberar Acesso")

Regra:

* Registrar:
  * Data e hora de liberação
  * Atividade só pode ser feita pelo host

Status muda para:

* "Acesso Liberado"


---

## Atividade 4 — Finalizar Check-in

A franquia deve confirmar:

* Hóspede entrou no imóvel?
  * Sim
  * Não
  * Problema identificado

Ao confirmar:

Status da reserva muda para:

* "Check-in Finalizado"

Log obrigatório:

* Data e hora
* Usuário responsável


---

# 4. Estados da Reserva

* Check-in Pendente
* Pré-check-in Concluído
* Check-in Não Concluído
* Liberar acesso
* Acesso Liberado
* Check-in Finalizado


---

# 5. Regras de Negócio Críticas


1. Senha nunca pode ser exibida antes do dia do check-in.
2. Check-in não pode ser finalizado sem documentação obrigatória.
3. Toda comunicação deve ser logada.
4. Alterações de horário devem gerar histórico.
5. Dados devem seguir LGPD.