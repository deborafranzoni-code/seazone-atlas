<!-- title: Processo de Suporte Wallet | url: https://outline.seazone.com.br/doc/processo-de-suporte-wallet-lHkCQrClTd | area: Tecnologia -->

# Processo de Suporte Wallet

O processo de suporte Wallet, foca no produto direcionado para os proprietários de imoveis.

O link do produto em STG é <https://stg-wallet.seazone.com.br/sign-in>

Os suportes serão abertos desde o Pipefy no seguinte formulário 



:::info
Link Formulário do Pipefy - <https://app.pipefy.com/public/form/4K3MfNKM>

:::


### **Abertura do suporte**

Um **proprietário** ou **seazoner** identifica um problema/pedido/duvida e abre um card de suporte, respondendo o formulário de coleta de detalhes:

* Resumo do problema.
* Descrição detalhado do problema
* Passos para reproduzir o bug (se houver).
* Capturas de tela, logs ou vídeos (se aplicável).

Os card abertos chegam no Kanban do Pipefy *==Suporte Wallet==*


:::info
Link Kanban Pipefy - <https://app.pipefy.com/pipes/305658493>

:::


### **Caixa de Entrada**

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
* P2 - Medium - 1 a 3 dias
* P3 - Low - 5 a 7 dias
* P4 - Lowest - mais de 15 dias


Nesta fase também é informado o tipo de suporte e qual a subcategoria do card

Os tipos atuais são:

* Bug no Wallet \*\*
* Pedido Operacional \*\*
* Falso positivo
* Falha Infra
* Duvidas
* Erro de Processo
* Dados inconsistentes
* Sugestão de melhoria \*\*
* Outros

Após serem categorizados, dependendo do tipo escolhido podem ser enviados para:

* Fase - Escalar ao Jira (Responsável Dev) 
* Fase - Em atendimento (Responsável PM/Lider)



:::tip
Todos os tipos de suporte podem ser Escalados ao Jira

:::


### **Escalar ao Jira:**

* Ao escalar ao Jira serão criados 2 tipos de *Issues* no Jira
  * `Bug` - Caso o Tipo seja `Bug no Wallet` 
  * `Task` - Caso o Tipo seja `Pedido Operacional ou Sugestão de melhoria` 


### **Em atendimento**

Ao mudar para `Em atendimento`, o suporte é resolvido pelo PM ou encaminhado ao outro time/líder/pessoa


### **Concluído**

* Suporte validado em produção e movido para **Concluído**.
* Comunicado ao cliente, e concluir no Slack


O processo a seguir segue o seguinte fluxo:

 ![](/api/attachments.redirect?id=aad170f9-8687-4257-a7cb-a82d4d7baa4a)


 ![](/api/attachments.redirect?id=83ad9ba8-4681-43ec-849f-6e9c0a6bc7d6 " =1850x465")

 ![](/api/attachments.redirect?id=4fdbbec5-ec02-40b1-bee7-a957bea3959e "left-50 =295x219")


\

\

\

O Fluxograma - <https://app.pipefy.com/pipes/305658493/flow> 


Miro - 

[https://miro.com/app/board/uXjVLqoP5uE=/?share%5Flink%5Fid=583534529717](https://miro.com/app/board/uXjVLqoP5uE=/?share%5Flink%5Fid=583534529717)


\
[https://miro.com/app/board/uXjVINSgjZ0=/?share%5Flink%5Fid=23755557411](https://miro.com/app/board/uXjVINSgjZ0=/?share%5Flink%5Fid=23755557411)