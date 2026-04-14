<!-- title: Proprietário - Extrato | url: https://outline.seazone.com.br/doc/proprietario-extrato-e1vg14HhKW | area: Tecnologia -->

# Proprietário - Extrato

Regras existentes (12/02/25) para o extrato.

* É possível selecionar de 2024 para frente até o mês atual.


Novas regras adicionadas para a visualização do Extrato dos imóveis do proprietário ([SAP-1919](https://seazone.atlassian.net/browse/SAP-1919)):

* Pode visualizar extrato de meses futuros, sempre que cumprir as seguintes regras:
  * Se existir reservas concluídas com datas de `check-out` para o mês selecionado;
  * Se existir despesas no mês do `Approval_Date` e com o `Expense_Status = Approved`.