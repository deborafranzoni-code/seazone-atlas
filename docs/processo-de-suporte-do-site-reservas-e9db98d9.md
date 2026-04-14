<!-- title: Processo de Suporte do Site Reservas | url: https://outline.seazone.com.br/doc/processo-de-suporte-do-site-reservas-Ocnrhae0IV | area: Tecnologia -->

# Processo de Suporte do Site Reservas

O processo de suporte Website, foca no produto direcionado as reservas no website  de Seazone.

O link do produto em STG:  <https://stg.seazone.com.br/>

O link do produto em PROD: https://seazone.com.br/


O fluxo completo a ser seguido é o seguinte:

 ![](/api/attachments.redirect?id=35562b92-fd44-4a89-869d-c2717b10b873)


## **Abertura do suporte**

O fluxo de suportes de Reservas no website  possui dois fontes de abertura  de solicitações, cada um tem um projeto no Pipefy. 

* Kanban do Pipefy *==Suporte Website==*   ***(Projeto Principal)***

  Suportes abertos no Slack via canal **#suporte-website** 


:::info
Link Kanban Pipefy - <https://app.pipefy.com/pipes/305862008>

:::


* Kanban do Pipefy  *==Suporte Reservas==*

  Suportes abertos diretamente no Web seazone.com.br


:::info
Link Kanban Pipefy - <https://app.pipefy.com/pipes/305900382>

:::

Os cards abertos pelo site de reservas chegam no Kanban do Pipefy *==Suporte Reservas==*  e são redirecionados para o *==Suporte Website==*


Os dados coletados por um **seazoner** do atendimento ou um *usuário final,* ao identificar um problema/pedido/duvida, são os seguintes:

* Resumo do problema.
* Descrição detalhado do problema
* Passos para reproduzir o bug (se houver).
* Capturas de tela, logs ou vídeos (se aplicável).

Formulário de pedido de suporte *==Suporte Website==*


:::info
[https://app.pipefy.com/public/form/b-Xwjj7W](https://app.pipefy.com/public/form/b-Xwjj7W  )

:::


Formulário de pedido de suporte  *==Suporte Reservas==*  


:::info
<https://app.pipefy.com/public/form/SyEKgAnB>

:::


## Fluxo de Atendimento do Suporte

### **Fase: Caixa de Entrada**

O Suporte é revisado para:

* Confirmar se o suporte é aceito
* Confirmar se todas as informações estão completas

**Opções:**

* Caso não tiver informações completas, continua na`Caixa de entrada` até ter todas as informações
* Caso seja aceito e tiver todas as Informações, vai para a fase `Priorização`
* Caso o suporte não é aceito, vai para a fase `Cancelado`

### **Fase: Priorização e Tempo de Resposta** 

Os cards são priorizados com base em impacto e urgência e movidos para:

* P0 - Highest      - ½ hora
* P1 - High            - 1 dia
* P2 - Medium      - 2 a 5 dias
* P3 - Low            - 7 a 15 dias
* P4 - Lowest       - mais de 15 dias


### Fase: Categorização

Nesta fase também é informado o tipo de suporte e qual a subcategoria do suporte

Os tipos atuais são:

* *==Reservas==*
* *==Pagamento==*
* *==Duvidas==*
* *==Sugestão de melhoria==*

  \

### Escalar

Após serem categorizados, dependendo do responsável pela solução do suporte, são enviados para uma das seguintes fases:

* Fase - Escalar ao Jira    - Responsável Dev
* Fase - Em atendimento - Responsável PM/Líder

### **Fase: Escalar ao Jira:**

* Ao escalar ao Jira serão criados 2 tipos de *Issues* no Jira
  * `Bug` - Caso a prioridade seja `P0, P1` 
  * `Task` - Caso a prioridade seja `P2, P3, P4` 

  \


:::tip
Todos os tipos de suporte podem ser Escalados ao Jira

:::


### **Fase: Em atendimento**

Ao mudar para `Em atendimento`, o suporte é resolvido pelo PM ou encaminhado ao outro time/líder/pessoa e segue seu fluxo normal de atendimento até ser finalizado ou cancelado


### **Fase: Concluído**

* Um suporte validado em produção é movido para **Concluído**.
* Comunicar ao usuário que reportou sobre a finalização do card, e concluir no Slack e no Pipefy


### **Fase: Cancelado**

* Todos os cards podem ser movidos para  **Cancelado,** caso identificou-se a não necessidade de ação nenhuma.
* Comunicar ao usuário que reportou sobre o cancelamento no Slack e no Pipefy


### Fluxo completo

Visão Geral das fases no processo de Suporte

 ![](/api/attachments.redirect?id=bacb7cb1-f8f1-4bed-ab13-91a53ca1c94c " =1851x360")


\