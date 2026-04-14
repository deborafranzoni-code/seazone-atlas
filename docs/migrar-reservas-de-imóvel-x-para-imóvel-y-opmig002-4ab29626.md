<!-- title: Migrar reservas de imóvel X para imóvel Y - OPMIG002 | url: https://outline.seazone.com.br/doc/migrar-reservas-de-imovel-x-para-imovel-y-opmig002-DFmdM4yNHl | area: Tecnologia -->

# Migrar reservas de imóvel X para imóvel Y - OPMIG002

**Dados necessários:**

* identificar O  `Property ID` dos imóveis (X e Y) . Nesta [consulta](https://metabase.seazone.com.br/question/1092-property-owner-user-by-property-code) pode encontrar pelo `CODE` da propriedade.

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

 Na na Tabela `Reservation Reservation` identifique o registro pelo `reservation_id`  que deseja migrar. Atualize as seguintes colunas:

*  `Property ID` - novo id do ***imóvel Y***
*  `Listing ID` - novo id do `Reservation Listing` associado ao ***imóvel Y*** e ao ***OtaID*** correspondente


### Porque não migram algumas reservas?

Quando é ativado o fluxo de migração as reservas, sempre é considerado a **Data** **de Ativação ou Inicio de Contrato do novo imóvel**. 

Exemplo o Imóvel 3924- MRE801 foi ativado o dia ***15/02/2015***


 ![](/api/attachments.redirect?id=962bd979-7e81-4842-b08a-58dd357b47ae " =732x164")


Assim reservas anteriores ou dentro dessa data **>>não são migradas<<** 

**Pois temos a regra:** *"Todas as reservas que tenham data de check-in igual ou maior a data de Ativação do Imóvel"*\nNeste caso uma reserva com check-in 02/02/2025 não será migrada pois a data é menor do que a data de ativação do imóvel.


### **Método Recente para Migrar Reservas**


**Verificação de Datas:** Verifique se as datas de ***check-in*** na tabela `Reservation Reservation` estão de acordo com as datas nas colunas ***Activation_Date***, ***Inactivation_Date*** e *Contract_Start_Date* na tabela `Property Property`.

==Caso as datas não estejam de acordo, altere-as conforme as orientações do setor financeiro e reimporte a reserva via Sapron.==


**Verificação da Coluna "Conciliada":**

Sempre verifique a coluna ***Conciliada*** na tabela `Reservation Reservation`. Se a reserva estiver com o valor ***false*** ou em branco, pode-se alterar normalmente, pois ainda não passou pelo fechamento. Caso esteja com ***true***, será necessário alterar o valor para ***false*** no banco para permitir a modificação e reimportação da reserva.

==Após realizar a alteração e a importação, não se esqueça de colocar o valor da coluna ***Conciliada*** de volta para ***true***.==


OUtras informações importantes

**Migração de Reservas na Troca de Proprietários**

**[Migração de Reservas na Troca de Proprietários](/doc/migracao-de-reservas-na-troca-de-proprietarios-LREa34Xflm)**