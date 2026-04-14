<!-- title: _Suporte Sapron - Processo Atual | url: https://outline.seazone.com.br/doc/_suporte-sapron-processo-atual-veviSpCLkH | area: Tecnologia -->

# _Suporte Sapron - Processo Atual

> *Ultima atualização: 18 de novembro de 2024* 

## Processo das ferramentas para Solicitar chamado de suporte 


1. **==PIPEFY==**: o chamado é aberto via formulário neste link,  <https://app.pipefy.com/public/form/rqkWznfg> 

   
   1. Assim que o formulário é preenchido é criado um card no [pipefy-sapron suporte](https://app.pipefy.com/pipes/304437472)
   2. ***==SLACK==***: é enviado uma menagem no canal slack #suporte-sapron

      \
2. **==PIPEFY==**: No card criado é preciso aprovar pedido (Sim / Não)

   link Pipefy: <https://app.pipefy.com/pipes/304437472>

   **Não**: é transferido para outra área / Avisa no canal #suporte-sapron

   **Sim**: Designar uma prioridade (P0, P1, P2, P3, P4)

   \
3. **==MAKE==**: Se for priorizado, aciona a automação de Enviar/criar o card no Jira como *"Bug"*

   link make: <https://www.make.com/en/login>

   link do scenario pipefy-jira <https://us1.make.com/164467/scenarios/2711072/edit>

   link Jira: <https://seazone.atlassian.net/jira/software/projects/SAP/boards/3>


\
## Como abrir um chamado 

* Para abrir os chamados no #suporte-sapron o usuário*(parceiro/anfitrião/proprietário)* deve acessar esse link <https://app.pipefy.com/public/form/rqkWznfg> que está disponível no o acesso ao sapron.
* Preencher os dados no formulário. Os dados solicitados, dependem do tipo de usuário. 


 ![](/api/attachments.redirect?id=062c2c83-0eb5-4b5f-8c97-01d88260201e " =380x444")

* Após o envio do formulário:
  * Uma mensagem é recebida no canal #suporte-sapron do Slack e
  * Um card é criado na Caixa de Entrada do Board [Suporte Sapron do Pipefy](https://app.pipefy.com/pipes/304437472)  

## Categorização dos chamados - WIP

Todos os cards que chegam no canal #suporte-sapron passam por algumas etapas antes de serem enviadas ao board do time para ser resolvido.


1. Entender se o card realmente precisa de suporte e ser priorizado.
2. Categorizar o card. O detalhe das categorizações podem ser encontradas neste link [Categorização de cards - suporte](/doc/categorizacao-de-cards-suporte-8ecV2TvypN)

## Resolução de chamados - WIP

Alguns de os casos mais conhecidos podem ser encontrados neste link

* **[Resoluções operacionais de suportes](https://outline.seazone.com.br/doc/resolucoes-operacionais-de-suportes-f50LK6T3f4)**
* [Investigação de suportes](/doc/investigacao-de-suportes-zP7O5MeuAE)
* [Tabelas usadas nos suportes](/doc/tabelas-usadas-nos-suportes-X705acq6Ml)

  \

Temos essa documentação, que foi migrada do Notion, porem algumas das informações são de processos antigos ou legados, ainda é necessário uma revisão para identificar o que é valido para o cenário atual.

* **[Resoluções de Suportes Sapron (Legado)](https://outline.seazone.com.br/doc/resolucoes-de-suportes-sapron-legado-nuFF3FHrxN)**


## KPIs do Suporte 

[KPIs do Suporte](/doc/kpis-do-suporte-iViffHxTXw)


\
## Dashboard Relatório Semanal Last7D


Pode ser visualizado neste link <https://app.pipefy.com/pipes/304437472/dashboards/139561>

* **Total Last7D:** indica o total de cards abertos nos últimos 7 dias.
* **Abertos (CxP{0-4}):** Indica todos os cards que foram abertos nos últimos 7 dias e estão na Caixa de Entrada e priorizados como P0, P1, P2, P3 e P4 
* **Finalizados:** Indica que os cards terminaram o fluxo de atendimento, assim eles podem ser cancelados ou concluídos.
  * **Cancelados**: São todos os cards que foram cancelados por serem tarefas que podem ser feitas via sapron, ou por falta de informação/resposta
  * **Concluídos**: São os cards que o time precisou investigar e fazer alguma ação.


Os próximos serão todos relacionados aos **Cards** **Concluídos**

* **Concluídos x Origem do Problema:** Cards separados pelos diferentes tipos de problema que foi categorizado por um membro do time (PM, Dev, QA).
* **Concluídos x Origem do Problema & OP:** Mostra o código Operacional relacionado á categoria da tarefa operacional usada para resolver o suporte, por cada tipo de Origem de problema.
* **Concluído - Bug Sapron  x Setor:** Numero de bugs por setor que reportou o card.
* **Concluído - Erro Processo x Setor:** Numero de Erros de processo por setor que reportou o card.
* **Concluídos -  Bug Sapron x Prioridade:** Numero de bugs por prioridade.
* **Concluídos -  Erro Processo x Prioridade:** Numero de Erros de processo por prioridade.
* **Concluídos x Código OP:** Tipos de Operacionais usados nos cards concluídos.


Exemplo gerado do dia 10/12/2024

 ![](/api/attachments.redirect?id=8bc9583d-aca1-4932-b6f1-bb1d617a1dc4)

 ![](/api/attachments.redirect?id=2b25fc16-7f2c-47dd-94bb-88f723d2f6ee)


[Relatorio Semanal Finalizados Last7Dfinal.pdf 14534705](/api/attachments.redirect?id=d932c81f-8528-418b-bc87-93def5a3ecb8)


\