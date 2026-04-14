<!-- title: Atualização planilha de Faturamento Booking Expe | url: https://outline.seazone.com.br/doc/atualizacao-planilha-de-faturamento-booking-expe-nCNPgayR88 | area: Administrativo Financeiro -->

# Atualização planilha de Faturamento Booking Expe

\
As Ota's do Booking e do Expedia possuem uma regra de negócio um pouco diferente das outras.

Para a liberação dos extratos de pagamento da plataforma do Expedia, é preciso primeiro fazer uma solicitação de pagamento após a data de check-out da reserva. Depois de fazer esse pedido de pagamento, aproximadamente umas 12h depois, o extrato com a previsão dos recebimentos é liberado, sendo então esse o extrato que utilizamos para a conciliação. Dessa maneira, é possível fazer a conciliação de faturamento semanal para expedia (é solicitar os pagamentos e extrair o extrato 1x por semana, pegando os dados da semana anterior).

Já o Booking libera o extrato dos pagamentos das reservas que tiveram check-out neste mês, apenas no início do mês seguinte.

Por este motivo, precisamos esclarecer os seguintes termos:

**Faturamento Booking/ expedia** = a receita prevista para as reservas decorrentes deste mês

**Receita Booking/ expedia** = receita referente ás reservas do mês anterior (é com base neste valor que é feito os repasses aos proprietários e anfitriões no fechamento).

Para que possamos ir acompanhando o FATURAMENTO de booking e expedia, utilizamos então a planilha de "[Faturamento Booking/Expedia Sapron](https://docs.google.com/spreadsheets/d/1ZXksKirQvK6irEMsgra4ctEtbUUzyt05E6GjF7HYn78/edit#gid=1353793656)", que nada mais é do que uma cópia da planilha de conciliação, porém ela roda apenas as macros que interferem nas entradas de Booking e Expedia.

Lembrando que ela deverá estar sempre com a data do fechamento do próximo mês para que ela traga as reservas de Booking e Expedia deste mês (ex. se estamos efetivamente no fechamento de maio, ela deverá estar com data de 01/06/xxxx)

## Objetivo

Checar se pagamentos à serem recebidos do Booking e Expedia estão de acordo com o previsto em nosso sistema.

## Prazo

**Conciliação Expedia → Semanal**

**Conciliação Booking → Mensal**

## Fluxograma de processo

[\[OPE\] 04 - Processo de Conciliação e Inconsistências](https://lucid.app/lucidchart/de1dc4a3-5b4e-4eb8-acd6-3ef16dd3b472/edit?invitationId=inv_d18d2591-4546-481e-bece-b04819e812ae&referringApp=slack&page=0_0#)

## Função de cada aba

* **Dashboard**

  Serve para atualização das Macros. A atualização deve ser feita sempre na ordem dos passos e toda a vez que houver alguma atualização em alguma planilha ou no sistema.

  As macros mensais (passo 3 e 4), serão atualizadas somente nos períodos de fechamento.
* **Conciliação Booking/ Expedia**

  Concilia as reservas realizadas via Booking e Expedia.

  Deve ser atualizada e conciliada Semanalmente.
* **Alterações**

  Essa aba é responsável por trazer as informações registradas na planilha de BO's. Ela servirá como base para "complementar" os pagamentos das reservas que tiveram algum desconto por BO.

  Deve ser atualizada diariamente informando os BO's que devem ser somados ao respectivos pagamentos.
* **Conciliação Fechamento**

  É um "extrato final" dos valores a serem repassados aos proprietários e anfitriões no fechamento em andamento. Ela soma apenas as diárias do mês em questão.

  Ela é alimentada pelas abas "conciliação Mês entradas", "conciliação Mês Airbnb", "conciliação Mês Booking/expedia" por fórmula.

  Não é necessário fazer atualizações manuais nela (nem pode! se não quebra a fórmula), essa aba serve para alimentar a planilha de fechamento.

  \
* **Conciliação Mês Booking/ Expedia**

  É alimentada pela aba "Reservas" fazendo um filtro das reservas somente do Booking e Expedia e das diárias do mês do fechamento em andamento. Ela faz um match entre as abas "Booking Mês", "Expedia Mês" e "Conciliação Booking/Expedia".

  Não é necessário fazer atualizações manuais nela, essa aba serve para alimentar a aba de "conciliação fechamento".

  Sua atualização se dá pela macro "Conciliação mensal Booking"
* **Booking Mês**

  É alimentada pela aba "entradas Booking" do admsys serviços através da macro "Booking/ Expedia". Ela faz um filtro com apenas os pagamentos recebidos no mês do fechamento em andamento.

  Não é necessário fazer atualizações manuais nela, essa aba serve para alimentar a aba de "conciliação Mês Booking/expedia".
* **Expedia Mês**

  É alimentada pela aba "entradas Expedia" do admsys serviços através da macro "Booking/ Expedia". Ela faz um filtro com apenas os pagamentos recebidos no mês do fechamento em andamento.

  Não é necessário fazer atualizações manuais nela, essa aba serve para alimentar a aba de "conciliação Mês Booking/expedia".
* **Reservas**

  Traz as informações do CSV do Sapron.
* **Limpezas Mês**

  É um "extrato final" dos valores de limpeza a serem repassados aos anfitriões no fechamento em andamento. Ela soma apenas as limpezas de reservas com check-out no mês em questão.

  Não é necessário fazer atualizações manuais nela, essa aba serve para alimentar os valores da aba de anfitrião na planilha de fechamento.

  Essa aba busca as informações da aba "reservas", é um filtro
* **Reservas Mês**

  É um "extrato final" dos valores de diárias a serem repassados aos proprietários e anfitriões no fechamento em andamento. Ela soma apenas as diárias de reservas com check-out no mês em questão.

  Não é necessário fazer atualizações manuais nela, essa aba serve para alimentar as abas da planilha de fechamento.

  Essa aba busca as informações da aba "reservas", é um filtro.
* **Resumo Conciliação**

  É um dashboard com um resumo dos valores de conciliação
* **Faturamento Reservas Mês**

  É um resumo com todas as reservas de faturamento, ou seja, diárias do mês atual (inclusive Booking e expedia). É atualizada pela macro "faturamento mensal".

  Não é necessário fazer atualizações nela.
* **Conciliação Reservas**

  É um compilado com todas as reservas do fechamento. Ele pega a conciliação das reservas por inteiro (não filtra as diárias do mês).

  Ela é alimentada por uma fórmula, trazendo as informações das abas de conciliação das ota's


\
## Passo a Passo para conciliação do Faturamento

[Conciliação Booking/ Expedia](/doc/conciliacao-booking-expedia-RVKcPxTFRz)

[Alterações](/doc/alteracoes-LPCaaVU2Wf)