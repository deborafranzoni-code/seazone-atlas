<!-- title: Encontrar Logs de Envio do Primeiro Acesso | url: https://outline.seazone.com.br/doc/encontrar-logs-de-envio-do-primeiro-acesso-XHr6Kqbv12 | area: Tecnologia -->

# Encontrar Logs de Envio do Primeiro Acesso

## Pré requisitos


1. Ter o ID do usuário criado
2. Saber o período de tempo em que o email foi enviado (pode-se ter uma ideia pela coluna `created_at` da tabela `account_customer`)


## Passo a passo


1. Acessar o [Grafana](https://grafana.seazone.com.br/explore?schemaVersion=1&panes=%7B%22ii7%22%3A%7B%22datasource%22%3A%22be0girbf6b4zkc%22%2C%22queries%22%3A%5B%7B%22refId%22%3A%22A%22%2C%22expr%22%3A%22%22%2C%22queryType%22%3A%22range%22%2C%22datasource%22%3A%7B%22type%22%3A%22loki%22%2C%22uid%22%3A%22be0girbf6b4zkc%22%7D%7D%5D%2C%22range%22%3A%7B%22from%22%3A%22now-1h%22%2C%22to%22%3A%22now%22%7D%7D%7D&orgId=1), na aba `Explore`
2. Nos filtros, filtrar por `ecs_cluster = sapron_production`, como indicado na imagem a baixo
3. No filtro `Line contains`, adicionar o seguinte filtro: `[send_temporary_credentials][<USER_ID>]`

   ![](/api/attachments.redirect?id=d67c163f-857e-4f77-921a-0ccb258ae331)
4. Por fim, no filtro de datas (canto superior direito), filtre pelo período em que o email foi disparado. Isso pode ser feito clicando no botão do período (default `Last 1 hour`) e clicando no ícone do calendário do compo  `From`.

   ![](/api/attachments.redirect?id=4bb2f6f4-6829-4396-90d6-f84546c3281a)
5. Clique em `Run query` para rodar a query

Se tudo ocorrer certo, os logs serão mostrados na parte de baixo da tela


:::info
Certifique-se o serviço selecionado é o Loki. Isso pode ser visto no botão ao lado de `Outline` no canto superior esquerdo  

:::


:::info
No passo 4, é interessante filtrar por um período um pouco maior do que só o dia de envio. Então, se o envio deveria ter sido enviado dia 10, filtre pelo período do dia 8 ao dia 12

:::

### Exemplo

Levando em consideração um usuário de ID 1234 onde o email deveria ter sido enviado no dia 22/03/2025, sua query deveria ser algo como o mostrado a baixo ([link](https://grafana.seazone.com.br/explore?schemaVersion=1&panes=%7B%22ii7%22:%7B%22datasource%22:%22be0girbf6b4zkc%22,%22queries%22:%5B%7B%22refId%22:%22A%22,%22expr%22:%22%7Becs_cluster%3D%5C%22sapron-production%5C%22%7D%20%7C%3D%20%60%5Bsend_temporary_credentials%5D%5B1234%5D%60%22,%22queryType%22:%22range%22,%22datasource%22:%7B%22type%22:%22loki%22,%22uid%22:%22be0girbf6b4zkc%22%7D,%22editorMode%22:%22builder%22%7D%5D,%22range%22:%7B%22from%22:%221742526000000%22,%22to%22:%221742785199000%22%7D%7D%7D&orgId=1)).

 ![](/api/attachments.redirect?id=e807eef4-f30c-4cce-9f32-b225cdca6ec7)