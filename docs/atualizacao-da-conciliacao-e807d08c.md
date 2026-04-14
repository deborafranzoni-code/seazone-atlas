<!-- title: Atualização da Conciliação | url: https://outline.seazone.com.br/doc/atualizacao-da-conciliacao-bhH7Iy5vEq | area: Administrativo Financeiro -->

# Atualização da Conciliação

\
Depois de atualizar todos os extratos com todos os recebimentos de cada reserva, é preciso fazer a devida conciliação entre o valor previsto e o valor recebido. Para fazer essa conferencia, nós utilizamos a planilha de [Conciliação Reservas Sapron](https://docs.google.com/spreadsheets/d/17vMaBCLcc7V1OpIjQMhf-OVI6fPEWkhMlDHMkn9G0N8/edit#gid=2097081422&fvid=1471231816), que é basicamente a planilha responsável por fazer a conexão entre as informações contidas nas diversas planilhas (entradas do admsys khanto, entradas do admsys serviços, controle de BO's, reservas Seazone e devoluções) e os dados registrados em nossos sistemas (Sapron e Stays).


## Objetivo

Checar se pagamentos recebidos estão de acordo com o recebido

## Prazo

**Diário**

## Fluxograma de processo

[\[OPE\] 04 - Processo de Conciliação e Inconsistências](https://lucid.app/lucidchart/de1dc4a3-5b4e-4eb8-acd6-3ef16dd3b472/edit?invitationId=inv_d18d2591-4546-481e-bece-b04819e812ae&referringApp=slack&page=0_0#)

## Função de cada aba

* **Dashboard**

  Serve para atualização das Macros. A atualização deve ser feita sempre na ordem dos passos e toda a vez que houver alguma atualização em alguma planilha ou no sistema.

  As macros mensais (passo 3 e 4), serão atualizadas somente nos períodos de fechamento.
* **Conciliação entradas**

  Serve para conciliar as reservas realizadas via Stays, site próprio e Decolar.

  Deve ser atualizada e conciliada diariamente.
* **Conciliação Airbnb**

  Concilia as reservas realizadas via Airbnb.

  Deve ser atualizada e conciliada diariamente.
* **Conciliação Booking/ Expedia**

  Concilia as reservas realizadas via Booking e Expedia.

  Deve ser atualizada e conciliada mensalmente.
* **Alterações**

  Essa aba é responsável por trazer as informações registradas na planilha de BO's. Ela servirá como base para "complementar" os pagamentos das reservas que tiveram algum desconto por BO.

  Deve ser atualizada diariamente informando os BO's que devem ser somados ao respectivos pagamentos.
* **Conciliação Fechamento**

  É um "extrato final" dos valores a serem repassados aos proprietários e anfitriões no fechamento em andamento. Ela soma apenas as diárias do mês em questão.

  Ela é alimentada pelas abas "conciliação Mês entradas", "conciliação Mês Airbnb", "conciliação Mês Booking/expedia" por fórmula.

  Não é necessário fazer atualizações manuais nela (nem pode! se não quebra a fórmula), essa aba serve para alimentar a planilha de fechamento.

  \
* **Conciliação mês entradas**

  É alimentada pela aba "Reservas" fazendo um filtro das reservas somente da Stays do mês do fechamento em andamento. Ela faz um match entre as abas "Stays Mês" e "Conciliação Entradas".

  Não é necessário fazer atualizações manuais nela, essa aba serve para alimentar a aba de "conciliação fechamento".

  Sua atualização se dá pela macro "Conciliação mensal Entradas"
* **Conciliação Mês Airbnb**

  É alimentada pela aba "Reservas" fazendo um filtro das reservas somente do Airbnb e das diárias do mês do fechamento em andamento. Ela faz um match entre as abas "Airbnb Mês" e "Conciliação Airbnb".

  Não é necessário fazer atualizações manuais nela, essa aba serve para alimentar a aba de "conciliação fechamento".

  Sua atualização se dá pela macro "Conciliação mensal Airbnb"
* **Conciliação Mês Booking/ Expedia**

  É alimentada pela aba "Reservas" fazendo um filtro das reservas somente do Booking e Expedia e das diárias do mês do fechamento em andamento. Ela faz um match entre as abas "Booking Mês", "Expedia Mês" e "Conciliação Booking/Expedia".

  Não é necessário fazer atualizações manuais nela, essa aba serve para alimentar a aba de "conciliação fechamento".

  Sua atualização se dá pela macro "Conciliação mensal Booking"
* **Stays Mês**

  É alimentada pelo extrato da stays via macro "Stays", ela faz um filtro com apenas as reservas do mês em fechamento.

  Não é necessário fazer atualizações manuais nela. É atualizada através da macro "Entrada Admsys"
* **Pagar.me Mês**

  É alimentada pela aba de "entradas pagar.me" no admsys da Khanto.

  Não é necessário fazer atualizações manuais nela. É atualizada através da macro "Entrada Admsys"
* **Airbnb Mês**

  É alimentada pela aba "entradas Airbnb" do admsys através da macro "Airbnb". Ela faz um filtro com apenas os pagamentos recebidos no mês do fechamento em andamento.

  Não é necessário fazer atualizações manuais nela, essa aba serve para alimentar a aba de "conciliação Mês Airbnb".
* **Paypal Mês**

  É alimentada pela aba de "entradas Paypal" no admsys da Serviços.

  Não é necessário fazer atualizações manuais nela. É atualizada através da macro "Entrada Admsys"
* **Entradas Mês**

  É alimentada pelas abas de "Entrada Inter", "Entrada Sicredi" no admsys da Serviços e "Entrada Khanto Reservas" no admsys da Khanto.

  Não é necessário fazer atualizações manuais nela. É atualizada através da macro "Entrada Admsys"
* **Devolução Mês**

  É alimentada pela aba "Devoluções" do admsys serviços através da macro "Crédito, Devoluções e realocações". Ela faz um filtro com as devoluções realizadas no mês do fechamento em andamento.

  Não é necessário fazer atualizações manuais nela, essa aba serve para alimentar a aba de "conciliação entradas".
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
* **Reservas Seazone**

  É alimentada pela aba "Reservas Seazone" da planilha de Controle de BOs, através da macro "Reservas Seazone". Ela faz um filtro com apenas as reservas do mês do fechamento em andamento.

  Não é necessário fazer atualizações manuais nela, essa aba serve para alimentar a aba de "conciliação entradas".
* **Crédito Mês**

  Não é mais usada
* **Realocação Mês**

  Não é mais usada
* **Repasse**


\
## Passo a Passo para conciliação

[Conciliação Entradas](/doc/conciliacao-entradas-pNZ6nn8o6w)

[Conciliação Airbnb](/doc/conciliacao-airbnb-qK4jcZaZ25)

[Conciliação Booking/ Expedia](/doc/conciliacao-booking-expedia-jWHbncEdQI)

[Alterações](/doc/alteracoes-S3EJ7vhzgk)