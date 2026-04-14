<!-- title: Reservas - migrar reservas de Imovel X para Y | url: https://outline.seazone.com.br/doc/reservas-migrar-reservas-de-imovel-x-para-y-ynOAwq8AV4 | area: Tecnologia -->

# Reservas - migrar reservas de Imovel X para Y

**Dados necessários:**

* identificar O  `Property ID` dos imóveis (X e Y) . Nesta [consulta](https://metabase.sapron.com.br/question/1092-property-owner-user-by-property-code) pode encontrar pelo `CODE` da propriedade.

  \
* Sobre as reservas que precisam migrar, identificar na Tabela `Reservation Reservation` as colunas:
  *  `reservation_id` 


  *  `Property ID`
  *  `Listing ID`

  \
* Na tabela `Reservation Listing` identificar o `ID` . Filtre pelo `Property ID` dos dos imóveis (X e Y) 
  * `Ota ID`
  * `Property ID`

  
:::warning
  Prestar atenção no Ota ID. Se o imóvel **X** tiver **OtaID=1**, então procure o **ID** com **OtaID=1** do imovel **Y**

  :::

  \

**O que fazer**

 Na Tabela `Reservation Reservation` identifique o registro pelo `reservation_id`  que deseja migrar. Atualize as seguintes colunas:

*  `Property ID` - novo id do ***imóvel Y***
*  `Listing ID` - novo id do `Reservation Listing` associado ao ***imóvel Y*** e ao ***OtaID*** correspondente


### Porque Não migram algumas reservas?

Quando é ativado o fluxo de migração as reservas, sempre é considerado a d**ata de Ativação ou inicio de contrato do novo imóvel**. 

Exemplo o Imóvel 3924- MRE801 foi ativado o dia ***15/02/2015***


 ![](/api/attachments.redirect?id=962bd979-7e81-4842-b08a-58dd357b47ae " =732x164")


Assim reservas anteriores a essa data **>>não são migradas<<** 

**Pois temos a regra:** *"Todas as reservas tem data de checkin igual ou maior a data de Ativação do Imóvel"*\nNeste caso uma reserva com check-in 02/02/2025 não será migrada pois a data é menor do que a data de ativação do imóvel.


##