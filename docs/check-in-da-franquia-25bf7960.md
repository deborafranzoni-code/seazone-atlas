<!-- title: Check-in da Franquia | url: https://outline.seazone.com.br/doc/check-in-da-franquia-bWdkcZTWzT | area: Tecnologia -->

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


Segue a versão otimizada do prompt, mais objetiva, estruturada para IA de prototipação (Lovable), com instruções claras, sem ambiguidade e com foco em componentes de interface:


---

# SYSTEM PROMPT

Você é um gerador de protótipos SaaS B2B orientado a fluxos operacionais, regras de negócio e estados de sistema.

Gere um protótipo funcional de alta fidelidade para o módulo:

# "Fluxo de Check-in da Franquia"

O sistema é utilizado por franquias que operam imóveis de temporada.

O fluxo deve ser orientado por tarefas sequenciais com dependência lógica entre etapas.

Cada tarefa só pode ser executada se a anterior estiver concluída.

O sistema deve aplicar bloqueios visuais quando regras não forem atendidas.


---

# OBJETIVOS DO SISTEMA

O protótipo deve demonstrar:

* Cumprimento de exigências legais (documentação obrigatória)
* Redução de contato manual
* Padronização de comunicação
* Rastreabilidade da entrega de acesso
* Registro completo de logs


---

# ESTRUTURA DO PROTÓTIPO

Criar duas telas principais:

## 1. Tela de Listagem de Reservas

Exibir:

* Nome do hóspede
* Imóvel
* Data de check-in
* Tipo de entrada (Self Check-in ou Presencial)
* Status do check-in (badge visual colorido)
* Botão: "Abrir Reserva"


---

## 2. Tela de Detalhe da Reserva

Layout dividido em três blocos:


1. Informações do hóspede
2. Checklist sequencial de atividades
3. Histórico / Log de auditoria


---

# ESTADOS DA RESERVA (OBRIGATÓRIO)

O sistema deve suportar e exibir claramente:

* Check-in Pendente
* Pré-check-in Concluído
* Check-in Não Concluído
* Liberar Acesso
* Acesso Liberado
* Check-in Finalizado

Estados devem atualizar automaticamente conforme ações.


---

# FLUXO DE ATIVIDADES

As atividades devem ser exibidas como checklist vertical progressivo.

Cada atividade deve possuir:

* Condição de ativação
* Botão de ação
* Regras de bloqueio
* Atualização automática de status
* Registro obrigatório de log


---

## ATIVIDADE 1 — Mensagem D-1

Condição:\nDisponível apenas 1 dia antes do check-in.

Botão:\n"Enviar Mensagem D-1"

Sistema deve verificar:

### Se hóspede preencheu formulário:

Exibir:

* Documento enviado
* Horário de chegada
* Placa do carro (se houver)
* Indicação de pet

Após envio:

* Status → Pré-check-in Concluído
* Registrar log (data, hora, usuário)

### Se hóspede NÃO preencheu:

Enviar mensagem de obrigatoriedade.

Após envio:

* Status → Check-in Não Concluído
* Aplicar alerta visual na reserva


---

## ATIVIDADE 2 — Mensagem Dia do Check-in

Condição:\nDisponível somente na data do check-in.

Botão:\n"Enviar Mensagem Dia D"

Mensagem contém:

* Localização do imóvel
* Instruções gerais

Após envio:

* Registrar log obrigatório

Se tipo de entrada = Self Check-in:\nLiberar automaticamente a Atividade 3.


---

## ATIVIDADE 3 — Liberar Acesso (Somente Self Check-in)

Condições para habilitar botão:

* Data = dia do check-in
* Atividade 2 concluída
* Documentação obrigatória preenchida

Botão:\n"Liberar Acesso"

Regras:

* Apenas perfil "Host" pode executar
* Ao executar:
  * Registrar data e hora
  * Registrar usuário
  * Atualizar status → Acesso Liberado
  * Exibir senha somente após liberação

Senha nunca pode ser exibida antes do dia do check-in.


---

## ATIVIDADE 4 — Finalizar Check-in

Condição:\nDisponível após:

* Acesso Liberado (self check-in)\nou
* Mensagem Dia D (presencial)

Pergunta obrigatória:\n"Hóspede entrou no imóvel?"

Opções:

* Sim
* Não
* Problema identificado

Ao confirmar:

* Status → Check-in Finalizado
* Registrar log com data, hora e usuário


---

# REGRAS DE NEGÓCIO CRÍTICAS

O sistema deve bloquear:


1. Exibição da senha antes do dia do check-in
2. Finalização do check-in sem documentação obrigatória
3. Ações sem geração de log
4. Alterações de horário sem histórico

Deve indicar conformidade com LGPD:

* Dados sensíveis protegidos
* Acesso restrito por perfil


---

# EXPECTATIVA DE INTERFACE

* Layout SaaS B2B
* Checklist vertical com progresso visual
* Badges coloridos por estado
* Botões desabilitados quando regra não for atendida
* Alertas visuais para bloqueios
* Área fixa de histórico/auditoria
* Interface clara, operacional e orientada a tarefas