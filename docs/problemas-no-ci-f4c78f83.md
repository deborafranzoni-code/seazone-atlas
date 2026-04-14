<!-- title: Problemas no CI | url: https://outline.seazone.com.br/doc/problemas-no-ci-PNe0NMgPRT | area: Tecnologia -->

# Problemas no CI

Essa página visa documentar alguns problemas que tivemos no novo fluxo de CI o objetivo também é documentar as soluções desses problemas

# **Semantic Version**

## Problema

O workflow de versionamento semântico estava gerando a mesma versão quando o CI era executado duas vezes seguidas para *staging*. Isso resultava em erros de duplicação, impedindo a finalização do CI. ![](/api/attachments.redirect?id=c2d0d5df-d0fa-4c59-9556-4be5bc41e30b " =602x248")

## Causa

As versões em **staging** estavam sendo geradas com base na versão da **main**. Quando dois merges aconteciam em **staging**, a segunda execução gerava uma versão duplicada, pois a versão da **main** permanecia a mesma até o deploy. Isso causava a criação de uma tag no ECR com a mesma versão, originando o erro de duplicação.

## Impacto 

Os desenvolvedores não conseguiam subir novas features em *staging*, bloqueando o processo de desenvolvimento e obrigando-os a realizar o deploy ou a criação manual da release da *main* para rodar o CI de *staging*.

## Solução

Passamos a basear os updates nas versões da release candidate e também passamos a incrementar o RC sempre que um novo merge é feito independente de qual seja a semantica desse merge, dessa forma garantimos que não haja duplicatas de versões nesse fluxo 


\
# Branch develop deployada em prod

## Problema

Durante os deploys para produção, o CI estava realizando builds com base na branch `develop`.

 ![](/api/attachments.redirect?id=3f37ff6e-fe54-42ce-b855-8939d9f68bee " =549x192")


## Causa

O problema estava relacionado ao uso da variável `github.ref` nos workflows, que retorna a referência da branch padrão configurada no repositório. No caso do repositório "reservas", a Default Branch estava configurada como `develop`, e não como `main`, o que fez com que os builds fossem gerados com base na branch `develop` em vez da `main`.

 ![](/api/attachments.redirect?id=a449e6ab-e9d2-49e3-9fe6-8a20028f920b " =1030x317")

## Impacto 

Site quebrando por conta de features em develop que subiram para main

Devs travados de fazer novos deploys até que o problema fosse ajustado

## Solução

Ajustamos para utilizar a variável `github.base_ref`que pega a branch base da PR como referência para o build, corrigindo então essa questão e garantindo que o build sempre será feito a partir da branch base