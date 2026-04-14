<!-- title: Mapeamento Técnico - Fechamento AWS | url: https://outline.seazone.com.br/doc/mapeamento-tecnico-fechamento-aws-TgjdJWLhVl | area: Tecnologia -->

# Mapeamento Técnico - Fechamento AWS

# Sobre a documentação

Essa documentação tem o objetivo de mapear quais endpoints existem e quais são utilizados atualmente (06/01/2025), referente ao fechamento executado na AWS, bem como dar uma noção geral dos seus usos.

Ela não visa dar detalhes da implementação, visto que algumas ações são extensas e complicadas o suficiente pra ser mais intuitivo ler o código do que traduzir pra linguagem natural, visto que a maior parte das operações são pesquisas no banco de dados e ordenação dos dados em questão.

É feita para servir de base para os desenvolvedores que vão refatorar o código para o novo fechamento, não para ser compartilhada com pessoas de fora do time de desenvolvimento. 


---

# Endpoints


 1. [/host/monthly/](https://outline.seazone.com.br/doc/mapeamento-tecnico-fechamento-aws-mlXql6AKi0#h-hostmonthly) → GET em `/fechamentoanfitriao` 

    
    1. 1ª chamada é geral, ao abrir a página;
    2. 2ª e 3ª chamadas são para detalhes, ao expandir Anfitrião. Uma para ano < 2024, outra para o resto.
 2. ~~/host/daily/balance/~~ → Não é utilizado
 3. ~~/host/daily/revenue/~~ → Não é utilizado
 4. ~~/host/daily/transfer/~~ → Não é utilizado
 5. ~~/host/daily/manual_fit/~~ → Não é utilizado
 6. ~~/host/daily/commission/~~ → Não é utilizado
 7. ~~/host/daily/onboarding_expenses/~~ → Não é utilizado
 8. ~~/host/daily/cleaning/~~ → Não é utilizado
 9. ~~/host/daily/fee/~~ → Não é utilizado
10. ~~/host/ted/nf_value/~~ → Não é utilizado
11. ~~/partner/monthly/~~ → Não é utilizado
12. ~~/partner/daily/balance/~~ → Não é utilizado
13. ~~/partner/daily/commission/~~ → Não é utilizado
14. ~~/partner/daily/revenue/~~ → Não é utilizado
15. ~~/property/monthly/~~ → Não é utilizado
16. ~~/property/daily/balance/~~ → Não é utilizado
17. ~~/property/daily/revenue/~~ → Não é utilizado
18. ~~/property/daily/transfer/~~ → Não é utilizado
19. ~~/property/daily/manual_fit/~~ → Não é utilizado
20. ~~/property/daily/implantation_fee/~~ → Não é utilizado
21. ~~/property/ted_value/~~ → Não é utilizado
22. ~~/property/daily/net_cleaning_fee/~~ → Não é utilizado
23. ~~/property/daily/expenses/~~ → Não é utilizado
24. ~~/property/nf_value/~~ → Não é utilizado
25. ~~/seazone/daily/commission/~~ → Não é utilizado
26. [/property/monthly/closing/](https://outline.seazone.com.br/doc/mapeamento-tecnico-fechamento-aws-mlXql6AKi0#h-propertymonthlyclosing) → GET em `/fechamentoimovel`
27. [/property/annual-results/](https://outline.seazone.com.br/doc/mapeamento-tecnico-fechamento-aws-mlXql6AKi0#h-v2hostannual-results) → GET em `/proprietario`
28. ~~/host/annual-results/~~ → Não é utilizado
29. [/v2/host/annual-results/](/doc/mapeamento-tecnico-fechamento-aws-mlXql6AKi0) → GET em `/dashboard`
30. [/host/annual-results/export/](https://outline.seazone.com.br/doc/mapeamento-tecnico-fechamento-aws-mlXql6AKi0#h-hostannual-resultsexport) → POST em `/dashboard`
31. [/host/franchise-fee/](https://outline.seazone.com.br/doc/mapeamento-tecnico-fechamento-aws-mlXql6AKi0#h-hostfranchise-fee) → GET em `/fechamentoanfitriao` 

    
    1. Mesmas condições do endpoint 1.
32. ~~/host/financial/summary/~~ → Não é utilizado
33. ~~/host/dashboard/~~ → Não é utilizado
34. ~~/host/statement/~~ → Presente no Front, mas componente está oculto
35. ~~/owner/dashboard/~~ → Não é utilizado
36. ~~/owner/financial/summary/~~ → Não é utilizado
37. [/owner/financial/statement/monthly/](https://outline.seazone.com.br/doc/mapeamento-tecnico-fechamento-aws-mlXql6AKi0#h-ownerfinancialstatementmonthly) → GET em `/proprietario` (extrato da propriedade)
38. [/financial_closing/execute/](/doc/mapeamento-tecnico-fechamento-aws-mlXql6AKi0) → PUT nas rotas do fechamento

    
    1. Visível apenas `d.frazoni@seazone.com.br` e `arilo.claudio@seazone.com.br`
39. [/financial_closing/status/](https://outline.seazone.com.br/doc/mapeamento-tecnico-fechamento-aws-mlXql6AKi0#h-financialclosingstatus) → GET nas rotas do fechamento

    
    1. Mesmas condições do endpoint 38.


# Resumo

### /host/monthly/

* Retorna um resultado paginado em cima da tabela `proper_pay_host_monthly`, agregando instâncias da `financial_cleaning_fee_manual_fit`, com informações sobre o fechamento do anfitrião, separado por imóvel. 
* Pode ser filtrado por ID do anfitrião, código da propriedade, nome do anfitrião e mês de referência do fechamento.
* Exemplo:

 ![](/api/attachments.redirect?id=1140d618-66e5-4284-b1ed-5736948b7b2c)


---

### /property/monthly/closing/

* Retorna um agregado (majoritariamente) das tabelas `proper_pay_property_daily_transfer`, `proper_pay_property_daily_revenue` e `proper_pay_property_daily_balance` para TODAS as propriedades. Paginação feita pelo Frontend.
* Cada objeto da resposta tem seu método próprio dentro do construtor e também inclui algumas outras tabelas (como `financial_expenses`)
* Exemplo:

  ![](/api/attachments.redirect?id=ead01940-db48-4188-a8d7-9e236196684c)


---

### /property/annual-results/

* Retorna um agregado das tabelas `proper_pay_property_daily_transfer` e `proper_pay_property_daily_balance` para todas as propriedades de um Proprietário (ou uma única propriedade, se `property_id` estiver presente na requisição), separando a resposta final por mês.
* Contendo ou não `property_id`, o formato da resposta final é o mesmo, a fim de alimentar o dashboard da página inicial do Proprietário. A diferença é se os números representam uma ou a soma das propriedades do proprietário.
* Exemplo:

  ![](/api/attachments.redirect?id=7b6740d8-82ea-431a-ac8c-2e87b68bbaa7)


---

### /v2/host/annual-results/

* Retorna um agregado de valores da tabela `proper_pay_host_daily_transfer`. 
* Cada objeto tem seu método e é separado por mês, a fim de preencher o dashboard do Anfitrião para o ano requisitado. 
* Exemplo:

  ![](/api/attachments.redirect?id=a681e1d6-1ecf-43bb-9262-5e528dcc2a88)


---

### /host/annual-results/export/

* Exporta um arquivo .xlsx com lógica similar ao endpoint anterior, mas construido de maneira independente. Ele é feito a partir da classe `HostFinancialResultsReportGenerator`.
* Exemplo do arquivo:

  ![](/api/attachments.redirect?id=bf5d40d3-b9c2-433f-a441-1446cc3291b9)


---

### /host/franchise-fee/

Atualmente esse endpoint é chamado, mas o parâmetro de mês-ano está sempre como HOJE, independente do modal de calendário. Não foi investigado o impacto disso, porém o retorno está consistentemente vazio.

* Retorna dados filtrados da tabela `proper_pay_host_daily_transfer` onde os resultados estão entre o período selecionado e o tipo do registro é `franchise_fee` para o Anfitrião em questão.


---

### /owner/financial/statement/monthly/

* Retorna 3 objetos que são agregados das tabelas `proper_pay_property_daily_transfer`, `proper_pay_property_daily_revenue`, onde cada um compõe uma parte do extrato de uma única propriedade.
* Exemplo:

  ![](/api/attachments.redirect?id=0be153b9-fa68-47ce-8288-a8c7214219ac)


---

### /financial_closing/execute/

* Envia uma requisição para iniciar o Step Functions na AWS. 
* Cumpre a mesma função que: 

  > `curl -X POST 'https://1lk6ly5kx7.execute-api.us-west-2.amazonaws.com/production/execute' -H 'X-API-Key: XXXXXXXXXXXXXXX' --compressed`

  OBS: Esse é o url do ambiente de Produção, o de Staging é diferente.

  Se precisar da API-Key ou do url de Staging, contate alguém do time.


---

### /financial_closing/status/

* Envia uma requisição para checar o status da execução mais recente na AWS.
* Cumpre a mesma função que:

  > `curl -X POST 'https://1lk6ly5kx7.execute-api.us-west-2.amazonaws.com/production/execution_state' -H 'X-API-Key: XXXXXXXXXXXXXXX' --compressed`

  OBS: Esse é o url do ambiente de Produção, o de Staging é diferente.

  Se precisar da API-Key ou do url de Staging, contate alguém do time.


---