<!-- title: Fluxo de sincronização de propriedades | url: https://outline.seazone.com.br/doc/fluxo-de-sincronizacao-de-propriedades-ncjHwNr82X | area: Tecnologia -->

# Fluxo de sincronização de propriedades

## Regras de Negócio

A sincronização de propriedades é o processo de manter atualizado o campo `stays_listing_id` na `property_property`, que é o que permite que tenhamos uma comunicação clara com a API da Stays.

Quando um imóvel é criado no Sapron via Onboarding, ele vem com o campo vazio e é sincronizado a partir do campo:

* `code` (Sapron)
* `internalName` (Stays)

  Ter o campo stays_listing_id atualizado no banco de dados nos permite não ter que pesquisar pelo `code` toda vez na lista completa de propriedades.

Quando um imóvel é criado  na Stays, comumente é criado no formato de negócio B2C. Ou seja, um único apartamento em um prédio inteiro assinou contrato com a Seazone. No entanto, as vezes há erro de cadastrado, caracterizando o formato de negócio para B2B: várias unidades em um prédio assinaram contrato com a Seazone. Isso faz com que seja criado um novo calendário na Stays para a mesma propriedade.\nO imóvel permanece com o mesmo id na `property_property`, no entanto o listing da stays (que é vinculado com o banco de dados) é alterado. \nÉ comum que esta alteração seja realizada durante o onboarding do imóvel. Isso significa que na stays há um bloqueio de implantação maior que 30 dias.\nO que ocorre é que este bloqueio (pertencente ao listing "antigo") permanece ativo no calendário, mesmo quando há criação de um novo calendário, onde o bloqueio não está mais ativo.\n\n**Portanto, o comportamento esperado é:**\n- **Quando** identificado a mudança de `stays_listing_id`;\n- **E** `code` do listing antigo é igual ao `code` do novo listing;\n- **Então** o `stays_listing_id` deve ser atualizado,\n**Garantindo** que todas as reservas e bloqueios ativos no calendário do Sapron sejam pertencentes **apenas** ao calendário novo criado (novo `stays_listing_id`)\n

## Parte Técnica

Existem 2 casos de GET `external/v1/content/listings`:

O primeiro é um signal de `post_save` a partir da `reservation_reservation` que atualmente não está em utilização, por tanto não será documentado. Acredito que ele servia pra criar reservas a partir do Sapron.

O segundo é uma task (`stays_sync_sapron_properties_task`) que tem dois gatilhos:


1. Cronjob a cada 1h (apesar de no código estar comentado que seria a cada 6h);
2. Através de uma requisição direta em PUT `/channel_manager/stays/sync/listings`.

   \nEssa task, `stays_sync_sapron_properties_task`, busca todos os listings presentes na stays, fazendo a pesquisa por status (da stays), retornando de 20 em 20, que é o limite da API.

Após essa série de requisições, caso os imóveis não sejam JP02I e ES01I (hardcoded pra ser ignorado), é feita a validação, verificação e atualização do campo `stays_listing_id` dentro dos registros da `property_property` seguindo o caminho descrito no diagrama:

 ![](/api/attachments.redirect?id=c1321dc9-558f-49af-96fd-452459c0b5f1)

[atualizacao_de_listings_sapron_stays_24_fev_2025.excalidraw 94594](/api/attachments.redirect?id=ad2a6297-aa33-4316-b91b-a7811d915322)


*(Para importar, baixe o arquivo e abra-o no [excalidraw.com](https://excalidraw.com))*

## Fluxo pelo Webhook

O Sapron também possui uma lógica para receber e processar eventos da Stays relacionados a listings. A imagem abaixo mostra esse fluxo:

 ![](/api/attachments.redirect?id=4d8838ae-17fa-4285-829e-def5dd29eab9)

[atualizacao_de_listings_stays_webhook.excalidraw 112377](/api/attachments.redirect?id=ebc3e308-bb6d-47f0-9e12-cb7b1e9032e8)

Esse fluxo é muito semelhante ao que foi descrito na seção anterior. A principal diferença é que não precisamos fazer uma requisição para a Stays, no endpoint `GET external/v1/content/listings`, pois a Stays já está enviando os dados do listing via webhook.