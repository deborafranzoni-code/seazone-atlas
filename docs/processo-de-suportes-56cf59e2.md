<!-- title: Processo de Suportes | url: https://outline.seazone.com.br/doc/processo-de-suportes-rsIComiBZr | area: Tecnologia -->

# Processo de Suportes

O processo de suporte em cada time foca em diferentes clientes sejam internos ou externos (seazoners, franqueados, propietarios)


### **==Abertura do suporte==**

Os suportes são abertos desde ==um único Pipefy -== [==Suporte Tech Web==](https://app.pipefy.com/public/form/o5iZPqLi), o link é disponibilizado nos canais de slack, na aba "Pedido de Suporte":

* #suporte-bu-comercial
* #suporte-bu-hospedagem
* #suporte-bu-reservas

Um **proprietário** ou **seazoner** identifica um problema/pedido/duvida e abre um card de suporte, respondendo o formulário de coleta de detalhes:

* Resumo do problema.
* Descrição detalhado do problema
* As perguntas podem variar dependendo do cliente final
  * Passos para reproduzir o bug (se houver).
  * Capturas de tela, logs ou vídeos (se aplicável).

Os card abertos chegam no [Kanban](https://app.pipefy.com/pipes/306984316) do Pipefy


### ==Triagem do Card==

O OnCall, PM, QA, Dev podem fazer triagem dos cards. A Triagem tem 2 passos, conforme a imagem:

 ![](/api/attachments.redirect?id=400ab013-caec-4662-ab4d-705867d828c5 " =897x355")



1. Selecionar a BU responsável pelo card
2. Escalar para a BU:

   
   1. Escalar BU Comercial
   2. Escalar BU Hospedagem
   3. Escalar BU Reservas


O card vai ser enviado ao kanban da BU correspondente

*==Kandan dos times:==*


:::info
BU Hospedagem -  Kanban Pipefy - <https://app.pipefy.com/pipes/305658493>

BU Comercial       - Kanban Pipefy - **<https://app.pipefy.com/pipes/304437472>**

BU Reservas       - Kanban Pipefy - **<https://app.pipefy.com/pipes/305862008>**

:::


A partir daqui o fluxo por cada time segue da mesma forma.

### **Caixa de Entrada e Cada Time**

O Suporte é revisado para:

* Confirmar se o suporte é aceito
* Confirmar se todas as informações estão completas

Opções:

* Caso não tiver informações completas, vai para a fase `Em espera`
* Caso o suporte não é aceito, vai para a fase `Cancelado`
* Caso seja aceito e tiver todas as Informações, vai para a fase `Priorização`

### **Priorização e Tempo de Resposta** 

Os cards são priorizados com base em impacto e urgência e movidos para:

* P0 - Highest - 1 a 4 horas
* P1 - High - 1 dia
* P2 - Medium - 1 a 5 dias
* P3 - Low - 5 a 15 dias
* P4 - Lowest - mais de 15 dias


Nesta fase também é informado o tipo de suporte e qual a subcategoria do card

Os tipos atuais são:

* Bug no Wallet/Sapron/Reservas 
* Pedido Operacional 
* Falso positivo
* Falha Infra
* Duvidas
* Erro de Processo
* Dados inconsistentes
* Sugestão de melhoria 
* Outros

Após serem categorizados, dependendo do tipo escolhido podem ser enviados para:

* Fase - Escalar ao Jira (Responsável Dev) 
* Fase - Em atendimento (Responsável PM/Lider)



:::tip
Todos os tipos de suporte podem ser Escalados ao Jira

:::


### **Escalar ao Jira:**

* Ao escalar ao Jira serão criados 2 tipos de *Issues* no Jira
  * `Bug` - Caso a prioridade seja P0 ou P1
  * `Task` - Caso a prioridade seja P2, P3 ou P4

### **Em atendimento**

Para o atendimento de cada syporte, deve ser feito em cada pipefy do time

Ao mudar para `Em atendimento`, o suporte é resolvido pelo PM ou encaminhado ao outro time/líder/pessoa


### **Concluído**

* Suporte validado em produção e movido para **Concluído**.
* Comunicado ao cliente, e concluir no Slack


O processo a seguir segue o seguinte fluxo:

 ![](/api/attachments.redirect?id=d35bcb56-d25e-4dee-9ff1-2fdaf40cc1a3)