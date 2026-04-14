<!-- title: Reservas canceladas - Envio de whatsapp | url: https://outline.seazone.com.br/doc/reservas-canceladas-envio-de-whatsapp-dbD5agLLUW | area: Tecnologia -->

# Reservas canceladas - Envio de whatsapp

**__Notificação:__**

Quando chegar uma notificação no canal ==#**suporte-bu-reservas **==sobre erro ao envio de mensagem a Whatsapp, para reservas canceladas

 ![Exemplo de Notificação](/api/attachments.redirect?id=35f5d3d8-dcb0-486e-870e-cc64004a2046 " =428x240")

**__Dashboard de envios:__**

Link:  <https://monitoring.seazone.com.br/d/4a6f9af1-74cf-4646-a15a-daff8d431542/4c30033?orgId=1&from=now%2Fd&to=now%2Fd&timezone=browser&var-namespace=prd-apps>


**__O que fazer:__**

Como Suporte Operacional, será re-enviando a mensagem, via Postman, seguindo essas instruções:


**Endpoint:**

`POST ``<https://autowebhook.newbyte.net.br/webhook/techCancelamentoReserva/seazone>`

\n**Headers:**

`Authorization: K6GBHvbd!mYx&^&Xq4Etm5r8g9iFefmR`

\n**Body (JSON)**


> {   
>
> "phone":"+5538998203313",      // contato com "+" e DDI  
>
> "name": "Bernardo Ribeiro",         // Nome do hóspede  
>
> "ota_name": "Website Seazone", // OTA da Reserva Cancelada   
>
> "property_code": "TST001"          // Imóvel da Reserva Cancelada 
>
> }


Como baixar um CSV do Dashboard

[Como emitir CSV de Números Estrangeiros - Abordagem de Cancelamentos_2026-02-27_11-03-55.mp4 1920x1080](/api/attachments.redirect?id=50be60ec-b088-42a6-9fa6-6034033e8dba)