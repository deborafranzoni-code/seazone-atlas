<!-- title: Sync de Tempo de Preparo | url: https://outline.seazone.com.br/doc/sync-de-tempo-de-preparo-rJQ0AyXVNt | area: Tecnologia -->

# Sync de Tempo de Preparo

# O que é o tempo de preparo?

É uma informação que a Seazone atribui aos imóveis quando eles tem, entre reservas, dias para limpeza/preparação antes ou depois de uma reserva (ou ambos). Essa informação possui um problema que gira em torno da dupla fonte de verdade: Stays e Banco de Dados. Essa informação, mesmo quando atualizada na Stays, pode não refletir para a Wallet do proprietário ou Sapron da Franquia, e isso gera os tickets.

 ![](/api/attachments.redirect?id=6553a263-c71b-4106-bd89-b91901053bb5 " =1898x860")

# Como resolver?

Quando um chamado nesse sentido cai, é necessário que seja feita a sincronização manual diretamente no banco de dados:

* Busque a propriedade problemática pelo ID/Code na `property_property`
* Atualize a coluna `extra_day_preparation` dessa property para o valor correspondente à Stays, na mesma tabela
* Acesse tabela `property_audit` e busque pelo ÚLTIMO registro de mudança de dados referente à property (pode usar o `created_at` para isso)
* No último registro, também atualize o campo `extra_day_preparation` para o mesmo valor adicionado anteriormente na `property_property`
* (Opcional) Verifique na perspectiva do proprietário se as mudanças foram aplicadas corretamente e o tempo de preparo já é exibido.