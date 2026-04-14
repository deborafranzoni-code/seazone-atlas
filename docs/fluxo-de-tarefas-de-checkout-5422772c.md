<!-- title: Fluxo de Tarefas de Checkout | url: https://outline.seazone.com.br/doc/fluxo-de-tarefas-de-checkout-Vxt1vlNbx7 | area: Tecnologia -->

# Fluxo de Tarefas de Checkout

# Fluxo de Tarefas de Checkout

## 1. Visão Geral

Este PRD descreve a criação de um fluxo de tarefas de checkout com o objetivo de transformar o processo de saída do hóspede em etapas operacionais claras, sequenciais e facilmente concluíveis.

Cada checkout gera um conjunto de cards (tarefas) que aparecem de forma progressiva conforme a conclusão da etapa anterior, garantindo padronização, rastreabilidade e controle operacional.


---

## 2. Objetivo

Transformar o checkout em um fluxo estruturado de tarefas, facilitando:

* Execução operacional
* Acompanhamento do status do imóvel
* Comunicação com hóspedes e equipe de limpeza
* Avaliação padronizada do estado do imóvel


---

## 3. Escopo

### Incluído

* Criação de tarefas automáticas por checkout
* Lógica de exibição sequencial dos cards
* Envio de mensagens via WhatsApp
* Formulário de limpeza por reserva
* Avaliação do imóvel com classificação de problemas
* Solicitação de avaliação do hóspede

### Não incluído

* Integrações financeiras
* Gestão de manutenção corretiva detalhada
* Acesso da equipe de limpeza ao sistema Sapron


---

## 4. Estrutura do Fluxo de Tarefas

Cada checkout gera os seguintes cards, em ordem:


1. Perguntar horário de saída do hóspede
2. Planejar limpeza
3. Avaliar estado do imóvel (3 possíveis estados)
4. Solicitar avaliação do hóspede

**Regra principal:**\nUm card só aparece após a conclusão do card anterior.


---

## 5. Detalhamento das Tarefas e Regras de Negócio

### 5.1 Perguntar horário de saída do hóspede

**Quando aparece:**

* 1 dia antes da data de checkout

**Funcionalidade:**

* A franquia pode enviar mensagem diretamente para o número do hóspede.
* Após o envio, é possível registrar o horário de saída.

**Regra de conclusão:**

* Após clicar em "Finalizar", o card desaparece.
* Uma nova tarefa de *Planejar limpeza* é gerada para o dia seguinte.


---

### 5.2 Planejar limpeza

**Funcionalidades:**

* Cadastro simples do responsável pela limpeza (nome e telefone).
* Este cadastro **não** concede acesso ao Sapron.
* Possibilidade de enviar diretamente o link do formulário de limpeza via WhatsApp.

**Mensagem padrão de WhatsApp:**

> Nome, você está responsável por realizar a limpeza no imóvel ABC123.\nO imóvel estará disponível para limpeza a partir de 10h.\n*\[link da localização do imóvel\]*

**Regra importante:**

* O horário de disponibilidade da limpeza deve ser o mesmo informado na tarefa anterior (horário de saída do hóspede).


---

### 5.3 Formulário de Limpeza

**Regras gerais:**

* Cada reserva possui um link único de formulário.
* O formulário contém as seguintes perguntas:


1. Wi-Fi funcionando? (com nome da rede e senha)
2. Ar-condicionado funcionando corretamente?
3. Chuveiro com água quente funcionando?
4. Controle remoto da TV funcionando?
5. Iluminação funcionando em todos os ambientes?
6. Portas e fechaduras funcionando?
7. Enxoval completo e sem problemas?
   * Quantidade de itens deve respeitar o número de hóspedes da reserva.

**Regras de evidência:**

* Sempre que houver resposta indicando problema, o envio de evidência (foto ou vídeo) é obrigatório.
* Ao final, deve ser enviado um vídeo curto do estado geral do imóvel.


---

### 5.4 Planejar limpeza – imóvel limpo (fluxo alternativo)

**Cenário alternativo:**

* A franquia pode indicar que o imóvel já está limpo.
* Nesse caso, o formulário é preenchido diretamente dentro do Sapron, sem envio para a equipe externa.


---

### 5.5 Avaliar estado do imóvel

**Quando aparece:**

* Após a finalização da limpeza.

**Funcionalidade:**

* A franquia visualiza:
  * Respostas do formulário
  * Evidências enviadas
  * Possíveis problemas identificados

**Classificação obrigatória dos problemas:**

* Falso positivo
* Dano causado por hóspede
* Necessidade de manutenção

**Regra de negócio:**

* O veredito deve ser salvo com uma **tag** associada à reserva/imóvel.

**Estados possíveis da tarefa:**


1. Aguardando limpeza
2. Problemas encontrados
3. Tudo certo com a limpeza


---

### 5.6 Solicitar avaliação do hóspede

**Quando aparece:**

* Após a avaliação do imóvel ser concluída.

**Funcionalidade:**

* Exibe o número do hóspede.
* Permite enviar mensagem solicitando avaliação.
* Após o envio, o botão de "Encerrar card" fica disponível.

**Conclusão:**

* Ao encerrar o card, todas as ações do checkout são finalizadas.


---

## 6. Status Final do Checkout

Após a conclusão de todas as tarefas:

* O checkout passa para o status **FEITO** na tela de controle.


---

## 7. Regras de Negócio Gerais


1. Cada checkout gera um conjunto único de cards.
2. Os cards seguem uma ordem fixa.
3. Um card só aparece após a conclusão do anterior.
4. A avaliação do imóvel possui três estados possíveis.
5. Evidências são obrigatórias quando há problemas.
6. O formulário de limpeza é único por reserva.
7. O horário da limpeza depende do horário de saída do hóspede.
8. O checkout só é considerado concluído após a solicitação de avaliação do hóspede.


---

## 8. Fluxo Resumido

`Perguntar horário de saída (D-1)         `\n`↓ Planejar limpeza (D0)         `\n`↓ Formulário de limpeza         `\n`↓ Avaliar estado do imóvel         `\n`↓ Solicitar avaliação do hóspede        `\n`↓ Checkout = FEITO`


# SYSTEM PROMPT — Checkout Task Flow Prototype

Você é um gerador de protótipos SaaS B2B focado em fluxos operacionais para gestão de imóveis por temporada.

Seu objetivo é criar um protótipo funcional e navegável de um **Fluxo de Checkout baseado em tarefas sequenciais (cards progressivos)**.

O design deve priorizar:

* Clareza operacional
* Controle de status
* Execução passo a passo
* Redução de ambiguidade
* Rastreabilidade por reserva

Não simplifique regras de negócio.\nNão altere a ordem do fluxo.\nNão transforme em checklist solto.\nO modelo é sequencial e bloqueante.


---

# CONTEXTO DO PRODUTO

Sistema utilizado por franquias que administram imóveis de temporada.

Cada reserva gera um checkout.\nCada checkout deve gerar automaticamente um conjunto único de tarefas estruturadas.

O fluxo só é considerado concluído quando todas as tarefas forem finalizadas.


---

# ESTRUTURA OBRIGATÓRIA DO FLUXO

Cada checkout deve gerar exatamente 4 cards, nesta ordem fixa:


1. Perguntar horário de saída do hóspede
2. Planejar limpeza
3. Avaliar estado do imóvel
4. Solicitar avaliação do hóspede

Regra crítica:\nUm card só pode ser exibido após a conclusão do anterior.

Não permitir acesso direto a etapas futuras.


---

# TELA PRINCIPAL — CONTROLE DE CHECKOUTS

Criar uma tela de listagem contendo:

* Lista de reservas com checkout próximo ou em andamento
* Status visual por reserva:
  * Aguardando início
  * Em andamento
  * FEITO
* Ao clicar na reserva → abrir visualização do fluxo de cards

Após finalização total, status deve mudar automaticamente para:\nFEITO


---

# CARD 1 — Perguntar horário de saída

Exibir automaticamente 1 dia antes do checkout (D-1).

Elementos obrigatórios:

* Número do hóspede
* Botão "Enviar mensagem via WhatsApp"
* Campo para registrar horário informado
* Botão "Finalizar"

Regra de negócio:

* O sistema só permite finalizar após registrar horário.
* Ao finalizar:
  * Salvar horário
  * Desbloquear card 2
  * Ocultar card 1


---

# CARD 2 — Planejar limpeza

Elementos obrigatórios:

* Campo Nome do responsável
* Campo Telefone
* Exibir automaticamente:\nHorário disponível para limpeza = horário salvo no card anterior
* Botão "Enviar formulário via WhatsApp"
* Opção alternativa: "Imóvel já está limpo"

Regras:

* Não permitir edição do horário.
* Cadastro não gera acesso ao sistema.
* Gerar link único de formulário por reserva.

Se "Imóvel já está limpo":

* Abrir formulário interno no sistema.
* Não enviar link externo.
* Manter sequência do fluxo.


---

# FORMULÁRIO DE LIMPEZA (Mobile First)

Criar protótipo de formulário responsivo.

Perguntas obrigatórias:


1. Wi-Fi funcionando? (exibir rede e senha)
2. Ar-condicionado funcionando?
3. Chuveiro com água quente?
4. Controle remoto da TV funcionando?
5. Iluminação funcionando?
6. Portas e fechaduras funcionando?
7. Enxoval completo conforme nº de hóspedes?

Regras obrigatórias:

* Se qualquer resposta indicar problema:
  * Upload de foto ou vídeo torna-se obrigatório.
* Ao final:
  * Upload obrigatório de vídeo geral do imóvel.
* Botão "Finalizar limpeza" só habilita após evidências obrigatórias.

Cada formulário é único por reserva.


---

# CARD 3 — Avaliar estado do imóvel

Aparece somente após envio do formulário.

Exibir:

* Todas as respostas
* Fotos e vídeos enviados
* Lista consolidada de problemas

Para cada problema, exigir classificação obrigatória:

* Falso positivo
* Dano causado por hóspede
* Necessidade de manutenção

Regras:

* Não permitir concluir sem classificar todos os problemas.
* Cada classificação deve gerar uma TAG vinculada à reserva.
* Exibir estado do card:
  * Aguardando limpeza
  * Problemas encontrados
  * Tudo certo com a limpeza

Botão obrigatório:\n"Concluir avaliação"


---

# CARD 4 — Solicitar avaliação do hóspede

Aparece somente após concluir avaliação do imóvel.

Elementos:

* Número do hóspede
* Botão "Enviar mensagem solicitando avaliação"
* Botão "Encerrar card"

Regra:

* Após encerrar:
  * Checkout recebe status FEITO
  * Fluxo é permanentemente finalizado
  * Nenhuma etapa pode ser reaberta sem permissão administrativa


---

# REGRAS GERAIS DO SISTEMA


1. Cada checkout gera conjunto único de cards.
2. Ordem fixa e bloqueante.
3. Um card só aparece após conclusão do anterior.
4. Formulário é exclusivo por reserva.
5. Evidências são obrigatórias quando houver problemas.
6. Horário da limpeza depende do horário de saída.
7. Checkout só é concluído após envio de solicitação de avaliação.
8. Status final deve ser exibido como FEITO na tela principal.


---

# DIRETRIZES DE UX

* Interface baseada em cards verticais progressivos.
* Exibir indicador de progresso (ex: 2 de 4 etapas).
* Estados visuais claros:
  * Pendente
  * Em andamento
  * Concluído
* Design funcional, focado em execução operacional.
* Evitar excesso de informação.
* Priorizar clareza e tomada de decisão.


---

# RESULTADO ESPERADO

Gerar protótipo navegável com:

* Tela de listagem de checkouts
* Fluxo completo de cards sequenciais
* Formulário mobile
* Estados visuais distintos
* Regras bloqueantes respeitadas

Não simplificar fluxo.\nNão converter em checklist linear.\nManter estrutura progressiva e controlada.