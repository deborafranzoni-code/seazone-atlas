<!-- title: Devoluções de Pagamentos | url: https://outline.seazone.com.br/doc/devolucoes-de-pagamentos-NiLK2xNamz | area: Administrativo Financeiro -->

# Devoluções de Pagamentos

\
Toda a solicitação de devolução de pagamento e/ou estorno parcial de uma reserva passa pelo canal #realocações-devolução-crédito, de lá, uma parte dessa informação é inserida de forma automática na aba de "devoluções" no admsys serviços, ficando assim o registro para posterior conciliação.

Informações que precisam ser lançadas manualmente na aba de "Devoluções" na planilha do **[Admsys Serviços](https://docs.google.com/spreadsheets/d/1YHvus3u692wr75lO_SDJgYuCo6kPqcLh9VxJ5WQ7GhQ/edit#gid=362456799)**:

* coluna "Data" = data efetiva do estorno
* coluna de "desc extrato" = descrever se foi um estorno de pix ou cartão, identificar o titular do cartão
* coluna "Atividade" = Informar se o estorno foi parcial ("Devolução Parcial de reserva") ou integral ("Devolução de reserva")
* coluna "ID Devolução" = ID do pagamento no [pagar.me](http://pagar.me/)


**\* Quando o estorno for parcial, é necessário fazer a substituição do ID de reserva Stays pelo ID de reserva sapron na coluna "Reserva". Salvar o ID de reserva Stays na coluna de "comentário"**

## Objetivo

Identificar e registrar os pagamentos estornados, bem como relacionar com as respectivas entradas

## Prazo:

**Diário**

## Fluxos do processo

[\[OPE\] 03 - Processo de Controle e Categorização de BO's](https://lucid.app/lucidchart/b112e7fa-064f-4f3a-a7ce-595825d7534a/edit?invitationId=inv_998f1d8a-e3e8-4b66-b67e-1c8dcf37e896&referringApp=slack&page=6m.YNQxnXhGT#)

## Ajustes no Admsys Khanto

Além de ajustar o registro dos dados da devolução na aba de devoluções do Admsys Serviços, também será necessário ajustar esses estornos no registro de suas respectivas entradas na planilha do **[Admsys Khanto Reservas](https://docs.google.com/spreadsheets/d/1L6vm5RINTTpXV-80Hih0-W2GIFoCX8jlYhflEtACguc/edit#gid=819800630)**

* **Ajuste de estorno Total**
* **Ajuste de estorno Parcial**