<!-- title: Categorias de Despesa/Reembolso | url: https://outline.seazone.com.br/doc/categorias-de-despesareembolso-DQgJ99zK0C | area: Tecnologia -->

# Categorias de Despesa/Reembolso

## Estrutura do banco

As novas categorias são armazenadas usando uma "lista encadeada" no banco, apartir da tabela de item.

A tradução de categoria também  é salva na coluna "reason".


**financial_expenses_item**

| **Nome** | **Tipo** | **Nullable**   | **Descrição** |
|----|----|----|----|
| id | PK | False | Identificação única |
| name | varchar | False | nome do item |
| name_en | varchar | False | tradução em inglês |
| subcategory_id | FK | False | Identificação de subcategoria |
| has_group | bool | False | Informa se o campo é de seleção múltipla |


\
**financial_expenses_subcategory**

| **Nome** | **Tipo** | **Nullable**   | **Descrição** |
|----|----|----|----|
| id | PK | False | Identificação única |
| name | varchar | False | nome da subcategoria |
| name_en | varchar | False | tradução em inglês |
| category_id | FK | False | Identificação de categoria |


\
**financial_expenses_category**

| **Nome** | **Tipo** | **Nullable**   | **Descrição** |
|----|----|----|----|
| id | PK | False | Identificação única |
| name_en | varchar | False | tradução em inglês |
| name | varchar | False | Descrição do categoria |


\
**financial_expenses_item_breakdown**

| **Nome** | **Tipo** | **Nullable**   | **Descrição** |
|----|----|----|----|
| id | PK | False | Identificação única |
| expense_id | varchar | False | identificação de despesa |
| item_id | FK | False | Identificação de item |


\
## Adicionando novas categorias, subcategorias ou itens


\
Exemplo de migration adicionando um novo campo de categoria, já com o link para subcategoria e item:

[0127_add_material_purchase.py 1127](/api/attachments.redirect?id=451ab8e7-9b7a-4024-8052-554c60e60d50)