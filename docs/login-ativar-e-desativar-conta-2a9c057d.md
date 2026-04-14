<!-- title: Login - Ativar e desativar conta | url: https://outline.seazone.com.br/doc/login-ativar-e-desativar-conta-fjRzIEa7q1 | area: Tecnologia -->

# Login - Ativar e desativar conta

\

:::warning
ATENÇÃO

Não pode desativar contas que estejam associadas a imoveis com status `ativo/onboarding` 

:::


\
## Via API DJANGO



1. Acesse o link segundo o ambiente

* Ambiente de **Produção** PROD: <https://api.sapron.com.br/admin/account/user/>
* Ambiente de T**este STG**: <https://stg-api.sapron.com.br/admin/account/user/>

*Se não tiver acesso, pode pedir com Gui ou seu lider*



2. Digite o e-mail e clic em "Buscar" 
3. Na seção ==Permissions== o check "Is active"


 ![](/api/attachments.redirect?id=b7cfd794-ea21-456e-ac7a-337d18f5a641 " =180x210")


## Via Banco de Dados 

Acesse ao banco e procure a Tabela `Account User > is_active`

Identifique o registro pelo UserID ou pelo e-mail. No campo `is_active` pode mudar para `true` / `false` dependendo do suporte.



:::info
Lembrar o ponto de atenção, sobre não desativar contas com imoveis ativos

:::