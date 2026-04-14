<!-- title: Migração Novo Fechamento | url: https://outline.seazone.com.br/doc/migracao-novo-fechamento-spDUU3lxVb | area: Tecnologia -->

# Migração Novo Fechamento

Este documento tem como objetivo registrar as mudanças necessárias para que o `backend` do Wallet use corretamente as novas tabelas e fluxos do Fechamento.

## Rotas afetadas

Os seguintes endpoints do `wallet-bff` serão afetados pelas mudanças do novo fluxo de fechamento e, por isso, devem ser validadas.

* `/owners/me/financial/summary`
* `/owners/me/properties`
* `/owners/me/properties/{property_id}/details`
* `/owners/me/financial/last-movements` (não utilizada)
* `/owners/me/financial/movements/summary`
* `/owners/me/financial/movements-xls`
* `/owners/me/financial/movements-csv`
* `/owners/me/financial/movements/discounts`
* `/owners/me/financial/movements/revenues`

## Ações necessárias

### Integração com o novo endpoint de resultados anuais

A rota `/proper_pay/property/annual-results/`, do `sapron-backend`, será atualizada em uma versão v2, que utilizará as novas tabelas do fechamento. Os fluxos do Wallet que utilizam esse endpoint devem passar a utilizar a nova rota, sendo eles:

* `/owners/me/financial/summary`
* `/owners/me/properties`
* `/owners/me/properties/{property_id}/details`

Vale ressaltar que a **atualização da rota de resultados anuais será de responsabilidade do Sapron,** sendo de responsabilidade do time do Wallet apenas a integração com a nova rota.

### Criação de rota de movimentações

A tabela `proper_pay_property_daily_transfer` deixará de ser utilizada como resultado da atualização do fechamento, assim como o endpoint `/proper_pay/property/daily/transfer/`, que disponibiliza os dados dela.

Com isso, torna-se necessário a criação de um novo endpoint que retorne as movimentações pertencentes às propriedades do `owner` utilizando a nova tabela de movimentações da propriedade, chamada `closing_property_resume`. A criação da API que acessa os dados da tabela será de **responsabilidade do time do Wallet.** 

Esse endpoint deve aceitar o tipo da movimentação como parâmetro de busca (`input` e `output`) e a categoria da movimentação ([documentação](https://outline.seazone.com.br/doc/novo-fechamento-via-sapron-CTEIfGYmW1#h-novo-tipo-enum-transfercategories)), assim como filtro de data de execução. Para melhor desempenho, a rota também deve ser paginada.

Parâmetros da pesquisa da rota:

| Nome | Tipo | Required | Observação |
|----|----|----|----|
| property_id | int | Não |    |
| accrual_date_start | date (YYYY-mm-dd) | Não |    |
| accrual_date_end | date (YYYY-mm-dd) | Não |    |
| cash_date_start | date (YYYY-mm-dd) | Não |    |
| cash_date_end | date (YYYY-mm-dd) | Não |    |
| type | string | Não |    |
| category | string | Não | Devem ser aceitos múltiplos valores |
| page | int | Sim |    |
| page_size | int | Não | Default 50 |

### Integração com a nova rota de movimentações

Todas as rotas que originalmente utilizam a API `/proper_pay/property/daily/transfer/` devem passar a utilizar a rota descrita [anteriormente](https://outline.seazone.com.br/doc/migracao-novo-fechamento-xwWLGOWgkr#h-criacao-de-rota-de-movimentacoes), sendo elas:

* `/owners/me/financial/last-movements` (não utilizada)
* `/owners/me/financial/movements/summary`
* `/owners/me/financial/movements-xls`
* `/owners/me/financial/movements-csv`

A criação da rota também deve possibilitar com que os endpoints `/owners/me/financial/movements/discounts` e `/owners/me/financial/movements/revenues` a utilizem, sendo assim, é preferível que esses fluxos passem a usar essa rota.


## :page_with_curl: DOCS relacionadas

* [Novo Fechamento via Sapron](/doc/novo-fechamento-via-sapron-CTEIfGYmW1)
* [Mapeamento Técnico - Fechamento AWS](/doc/mapeamento-tecnico-fechamento-aws-mlXql6AKi0#h-sobre-a-documentacao)