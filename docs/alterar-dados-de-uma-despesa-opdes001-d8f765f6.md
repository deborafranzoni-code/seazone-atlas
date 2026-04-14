<!-- title: Alterar dados de uma despesa - OPDES001 | url: https://outline.seazone.com.br/doc/alterar-dados-de-uma-despesa-opdes001-i7YEfrZU0T | area: Tecnologia -->

# Alterar dados de uma despesa - OPDES001

## OPDES001 - Alterar despesa

Dados necessários:

Qualquer informação que confirme a linha a ser alterada na tabela `financial_expenses` , as mais comuns são:


1. `financial_expanses id` procurar pelo código se estiver nos dados do suporte;
2. `property_id` (tabela `property_property` a partir da coluna `code` Ex: "BEL105");
3. `expense_date` (geralmente na print da despesa);
4. `value` (geralmente na print da despesa);
5. `description` ou outras informações adicionais(opcional).

**OBS**: O que não estiver no chamado ou na print precisa ser solicitado a quem abriu o chamado, sem essas 3 primeiras informações não é certo o que precisa ser alterado. Em caso das 3 primeiras serem iguais, peça também pela descrição ou outros campos que possam distinguir a despesa.

O que fazer:

Com essas informações, altere a informação solicitada na tabela e deixe um registro da alteração no card da solicitação por que a tabela `financial_expenses_audit` não registra alterações feitas a partir do banco.



1. \


## ==REGRAS PARA DESPESAS== 

### **==Sobre o E CASH DATE==**

Se a data de registro da despesa (**Register Date) <= 31/12/2023**

* Cash_Date = **Register_Data**

Se a data de registro da despesa (**Register Date) >= 01/01/2024**

* Cash_Date = **Approval Date**


### **==Sobre Status Pre_approved :==**

Ao alterar o status da despesa para `Pre_approved`, por exemplo, os campos **Approved By** e **Approved Data** devem ser mantidos em branco.


### Códigos de ID usados

É importante considerar sempre o **User ID** como referência principal:

* **==User ID==** ==→ **Host ID** → Seazone==
* **==User ID==** ==→ **Owner ID** → Proprietário==

  \

Caso o usuário não consiga cancelar e refazer o processo, podemos ajustar manualmente alterando as seguintes colunas com as informações fornecidas:

`Received By` e `Paid By`  = os valores trocam Seazone <> Owner

`Received By User`e `Paid By User` = os valores trocam user ID <> user ID


Campos que devem ser sincronizados, o ID e nome devem ser da mesma pessoa/usuário/

* `Received By`  `Received By User`
* `Paid By`  `Paid By User` 


\
## Cancelar Despesas

Query para atualizar status:\n`UPDATE public.financial_expenses SET expense_status='Canceled' WHERE id=<codigo_da_depesa>;`


### Para os suportes de mudanças nos códigos de despesa

Nesses casos, o ideal é sempre **cancelar e refazer o processo**, pois os IDs enviados nem sempre são os corretos, o que pode gerar inconsistências e erros no suporte.