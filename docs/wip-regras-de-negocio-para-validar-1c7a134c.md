<!-- title: WIP - Regras de Negocio para Validar | url: https://outline.seazone.com.br/doc/wip-regras-de-negocio-para-validar-aAtY7Wswbf | area: Tecnologia -->

# WIP - Regras de Negocio para Validar

**Datas de Limpeza erradas -** Card no pipefy - <https://app.pipefy.com/open-cards/1017830939>

* *Pedido: As datas de limpeza devem ser iguais a data de checkout. Em algumas reservas a data de limpeza é posterior a data de checkout.*
  * Revisar a tabela `Reservation` para verificar se teve extensão
  * ![](/api/attachments.redirect?id=defe7dcb-9901-4a8c-9101-8852e0f96963 " =1260x209")
  * Depois verificar em `Financial Cleaning Fee Manual Fit a DataRef` da limpeza
  * ![](/api/attachments.redirect?id=99d36d0f-4e97-459d-a922-5fd881ee1eeb " =1016x128")
  * Os Dados de Fechamento sobre limpeza podem ser visto em **Proper Pay Property Daily Net Cleaning Fee**

 ![](/api/attachments.redirect?id=c00cd9a5-553d-4cea-8193-618f7f971ddf " =680x126")

**Conclusão: A data esta certa, pois a data final de checkout foi 27/10/24 e não 19/10/2024**

***Fechamento***

* \