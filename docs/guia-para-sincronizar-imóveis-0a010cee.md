<!-- title: Guia para sincronizar imóveis | url: https://outline.seazone.com.br/doc/guia-para-sincronizar-imoveis-Z3bwe6GbJd | area: Tecnologia -->

# Guia para sincronizar imóveis

# Objetivo

Este documento tem como objetivo explicar como acionar manualmente o processo de sincronização dos imóveis. Essa etapa é necessária no ambiente de staging (STG), pois ele é desligado durante a noite (período em que, normalmente, a sincronização ocorre de forma automática). Como o ambiente não está disponível nesse horário, ás vezes é necessário executar o processo manualmente na manhã do dia seguinte.



:::info
O tutorial a seguir funciona em qualquer um dos ambientes, desde que você tenha a permissão correspondente no Auth0 para o ambiente em questão. Por padrão, essa permissão foi concedida a todos os membros da squad apenas no ambiente de staging (STG), já que é nele que a execução manual é necessária com maior frequência.

:::

# Passo a Passo

Para executar os passos a seguir, é necessário possuir uma permissão específica no Auth0. Caso você ainda não tenha essa permissão, basta solicitá-la a alguém da equipe.


1. Acesse o ambiente de stg **<https://web-stg.seazone.com.br/>;**
2. Logue com a sua conta que tenha a permissão (provavelmente será seu @seazone);
3. Ao logar, um token aparecerá na url, copie ele;
4. Acesse o Swagger de stg <https://api-staging.seazone.com.br/docs>;
5. No Swagger, localize o botão "Authorize" e cole o token no input que irá abrir ao clicar no botão;
6. Depois de autenticar localize o endpoint `/tasks/sync_properties`, expanda-o para localizar o botão "Try it out" e depois "Execute";
7. Se tudo der certo, o retorno aparecerá como "ok".

Abaixo, está disponível um vídeo com o passo a passo do processo.

[[Tutorial] Sync de Imoveis em STG .mp4 1920x1080](/api/attachments.redirect?id=bd18ccff-e0d5-433c-a32e-97dac4c5bd41)


\