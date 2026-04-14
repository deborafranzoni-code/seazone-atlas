<!-- title: Vibe Friday - Piloto | url: https://outline.seazone.com.br/doc/vibe-friday-piloto-FcitXgnmrG | area: Tecnologia -->

# Vibe Friday | Piloto

## 💡 Definição do Problema

Os proprietários de imóveis por temporada não possuem uma forma simples e centralizada de visualizar quais hóspedes se hospedaram em seus imóveis e em quais períodos. Essa informação é necessária para a correta emissão de notas fiscais e adequação às novas normas de hospedagem.

O problema consiste em desenvolver uma aplicação que consolide os dados de reservas e hóspedes em um resumo claro, acessível e confiável, permitindo que o proprietário gere suas notas fiscais com autonomia e em conformidade com as exigências legais.

## 📝 Diário de Bordo


---

Iniciamos o trabalho a partir do protótipo da @[Natália Bessa Ribeiro](mention://673d277d-f1af-48c0-81c0-646e5f397da9/user/8641c00b-f2e6-4a5b-8f8f-ba137416e209), implementando primeiramente a exclusão dos mocks e a adição de dados reais para consumo da aplicação. 

Nesse ponto, foi encontrado o primeiro problema: como ter todas as informações necessárias para a tela, sem mexer no backend?

Para isso, foram elencadas as rotas:

* `**SAPRON**` `/reservations/calendar/`: responsável por retornar os dados referentes às reservas de um imóvel, incluindo informações básicas do hóspede;
* `**SAPRON**` `/account/guest/`: responsável pelo detalhamento das informações do hóspede, incluindo dados como CPF/CNPJ, necessários para a emissão de NF.

A ideia é fazer uma mesclagem das respostas de ambas as rotas para conseguir ter todos os dados que a tela demanda, sem construir uma rota nova para isso.


---

## :white_check_mark: Pontos positivos


## :construction: Desafios

* O Gemini, por algum motivo, estava demorando muito para realizar os pedidos, fazendo com que a celeridade fosse baixa para a atividade executada.
* A ausência de conexão direta ao banco de dados (está sendo) um impeditivo, já que a ferramenta dependia que um endpoint prévio existisse para ter os dados da forma que nós precisamos.

  \

————

1º - Rota: reservations/calendar

| **id** | **IDinteger**<br>***title: ID***<br>***readOnly: true*** |
|----|----|
| **check_in_date** | **Check in datestring($date)**<br>***title: Check in date***<br>***x-nullable: true*****The check-in date for the reservation.** |
| **check_out_date** | **Check out datestring($date)**<br>***title: Check out date***<br>***x-nullable: true*****The check-out date for the reservation.** |
| **daily_net_value** | **Daily net valuestring($decimal)**<br>***title: Daily net value***<br>***x-nullable: true*****The daily net value of the reservation.** |
| **is_blocking\*** | **Is blockingboolean**<br>***title: Is blocking*****Whether the reservation is blocking.** |
| **blocking_reason** | **Blocking reasonstring**<br>***title: Blocking reason*****The reason for blocking, if applicable.****Enum:**<br>**Array \[ 5 \]** |
| **status** | **Statusstring**<br>***title: Status*****The status of the reservation.****Enum:**<br>**Array \[ 7 \]** |
| **is_last_minute** | **Is last minutestring**<br>***title: Is last minute***<br>***readOnly: true*** |
| **is_block_for_pricing** | **Is block for pricingstring**<br>***title: Is block for pricing***<br>***readOnly: true*** |
| **guest** | **Gueststring**<br>***title: Guest***<br>***readOnly: true*** |
| **property** | **Propertystring**<br>***title: Property***<br>***readOnly: true*** |
| **ota** | **Otastring**<br>***title: Ota***<br>***readOnly: true*** |

2º - Rota : account/guest/

| **id** | **IDinteger**<br>***title: ID***<br>***readOnly: true*** |
|----|----|
| **user\*** | **GuestUserCreate{**
| **id** | **ID\[...\]** |
|----|----|
| **first_name\*** | **First name\[...\]** |
| **last_name\*** | **Last name\[...\]** |
| **email** | **Email address\[...\]** |
| **main_role\*** | **Main role\[...\]** |
| **gender** | **Gender\[...\]** |
| **phone_number1** | **Phone number1\[...\]** |
| **phone_number2** | **Phone number2\[...\]** |
| **birth_date** | **Birth date\[...\]** |
| **is_individual** | **Is individual\[...\]** |
| **cpf** | **Cpf\[...\]** |
| **cnpj** | **Cnpj\[...\]** |
| **corporate_name** | **Corporate name\[...\]** |
| **trading_name** | **Trading name\[...\]** |
| **main_address\*** | **Address{...}** |
|   |    |
**}** |
| **nationality** | **Nationalitystring**<br>***title: Nationality***<br>***maxLength: 255*****The nationality of the guest.** |
| **source** | **Sourcestring**<br>***title: Source*****The source of the guest.****Enum:**<br>**Array \[ 2 \]** |
| **created_from_workflow_name** | **Created from workflow namestring**<br>***title: Created from workflow name*****The workflow name of the guest.****Enum:**<br>**Array \[ 3 \]** |