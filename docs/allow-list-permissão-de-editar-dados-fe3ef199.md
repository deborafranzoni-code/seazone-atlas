<!-- title: Allow List - permissão de editar dados | url: https://outline.seazone.com.br/doc/allow-list-permissao-de-editar-dados-rxJ8yua6Qn | area: Tecnologia -->

# Allow List - permissão de editar dados

## Adicionar novos usuarios

Verificar que no Banco de Dados (ou Django) o registro do usuário tenha os seguintes campos:

* Main Role = Admin
* `Is Staff = true`
* `Is Active = true`


 ![](/api/attachments.redirect?id=cdee50d9-59a5-41e4-af5c-3dc1392ed79b " =338x395")


Depois, para incluir novos emails na lista de Allow-List do Front-End, acessar a FF do PostHog neste link

<https://us.posthog.com/project/127887/feature_flags/172729>


1. Clicar em editar 
2. Adicionar os emails solicitados e 
3. Depois salvar


:::info
Precisam ter acesso a FF é do Sapron Production.

:::


 ![](/api/attachments.redirect?id=26e830ef-e498-4a66-b7ff-449a04d1f8cc " =1725x502")


Para a allow list do backend (pós-crise), é necessário logar na AWS, navegar até o serviço **Systems Manager**, acessar a aba de **Parameter Store** e procurar pela variável de ambiente: `[/sapron-api/prd/DATA_EDIT_ALLOW_LIST](https://sa-east-1.console.aws.amazon.com/systems-manager/parameters/%252Fsapron-api%252Fprd%252FDATA_EDIT_ALLOW_LIST/description?region=sa-east-1&tab=Table#list_parameter_filters=Name:Contains:allow)`


 ![](/api/attachments.redirect?id=b2c64991-0c7d-445f-b127-e4979424222e " =589x217")

Feito isso, pode clicar nela, depois em **Edit** e adicionar o e-mail do solicitante no final\n\n ![](/api/attachments.redirect?id=fe2caa4e-fd06-484c-8212-2ae0b58d585c " =1898x906")


:::warning
Após salvar a edição, é necessário syncar os pods no Argo CD

:::


## Deletar usuários

* No mesmo link do posthog, clicar em editar, procurar o e-mail e deletar da list