<!-- title: Despesas - atualizar recibo de pagamento | url: https://outline.seazone.com.br/doc/despesas-atualizar-recibo-de-pagamento-pFiOkOelJg | area: Tecnologia -->

# Despesas - atualizar recibo de pagamento

Tabelas envolvidas

* **Financial expenses**
  * ID
* **Financial Expensesfiles**
  * **Expense ID**
  * **File UID**


* **Files Fileitem**
  * **UID**


O que fazer

S3 - Subir o novo documento

* No Path:
  *  **Seazone Technology > Sapron > sapron-files > Statement/**


No banco

* identificar a `DespesaID`
* Na `Financial Expensesfiles` **procurar pelo** `ExpenseID` **e encontrar a** `FileUID`
* Procurar o registro do documento pelo **UID** na **Files Fileitem**
* Os dados que devem ser atualizados do novo documento são nesta tabela são
  * **Name**
  * URL (conforme foi subido nO S3