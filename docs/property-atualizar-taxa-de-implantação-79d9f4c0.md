<!-- title: Property - Atualizar Taxa de Implantação | url: https://outline.seazone.com.br/doc/property-atualizar-taxa-de-implantacao-qKGuahQTRV | area: Tecnologia -->

# Property - Atualizar Taxa de Implantação

A taxa de Implantação é salva na **Property Handover Detail**

Procurar pelo PropertyCode 

<https://metabase.seazone.com.br/question/1363-property-handover-details-by-property-code>


## Regras de negocio

O projeto do fechamento, usa a `contract_start_date`  (se esse estiver vazio), usa a `activation_date`  do imóvel na `property_property`

 

Se houver algum saldo devedor pendente do mês anterior, ele fica para o mês subsequente. Isso se aplica também  a taxa de implantação

As opções de Taxa de Implantação:

* **Bank_Slip = Boleto**
* **Credit_Card**
* **Discount_Rate = Abatimento**
* **Installments = Parcelas**
* **On_Budget = À vista (PIX)**


 ![](/api/attachments.redirect?id=b9facee3-10a6-4cfb-a02a-fb631edcda12 " =150x228")

### Pedidos de suporte

Alguns tipos de suporte solicitados no canal #suporte-sapron

### **Mudança de tipo de pagamento do onboarding ou Taxa de Implantação.**

* Na tabela `Property Handover Details > Payment Method` guarda o tipo de pagamento 
* Ex. O pagamento era a vista `On_Budget` porém estava `Installments`


### **Mudança na data de inicio  de pagamento da taxa de implantação**

* Na tabela `Property Handover Details > Payment Method` guarda a data no campo **Created At** 
* Ex. O pagamento precisa iniciar em 01/01/2025, verificar a regra.
  * Considerar essa regra aqui: O projeto do fechamento, usa a `contract_start_date`  (se esse estiver vazio), usa a `activation_date`  do imóvel na `property_property`

     


Nota:

* Para todos os imoveis que sejam pagos a **vista(On_Budget)** ou P**ix**,  vamos ter valores **positivos** e **negativos** em
  * **Proper Pay Property Daily Implantation Fee**
  * **Proper Pay Property Daily Transfer**


* Para todos os imoveis que sejam pagos a **Abatimento(Discount_Rate)** ,  vamos ter valores apenas **positivos** em
  * **Proper Pay Property Daily Implantation Fee** 
  * **Proper Pay Property Daily Transfer**


### Mudança no valor da taxa de Implantação

Nesses casos precisa atualizar o campo `Property Handover Details > Implantation Fee Total Value `conforme o valor solicitado.


### **Exclusão de taxa de implantação**

Se o dado solicitado estiver na `Financial_property_owner_ted` tem que deletar. 

\n

\n