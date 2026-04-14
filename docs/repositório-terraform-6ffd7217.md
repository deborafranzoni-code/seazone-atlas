<!-- title: Repositório Terraform | url: https://outline.seazone.com.br/doc/repositorio-terraform-7kfSRsa3Da | area: Tecnologia -->

# Repositório Terraform

O repositório Terraform é composto por arquivos terraform, ele possui as informações dos recursos criados pela infraestrutura desde o momento que iniciamos o nosso trabalho na Aws. 


## Estrutura do repositório

Nos diretórios mais externos (iniciais), a divisão é feita por contas das Aws, onde cada recurso, serviço ou aplicação pertencente aquela conta é encaixado no mesmo. As contas que temos atualmente são:

* Produção 
* Staging
* Prd-sapron
* Seazone-technology


:::warning
Outras pastas como módules e gcp também estão neste diretório, porém estão incorretas e aguardando a alteração de repositório.

:::

 ![](/api/attachments.redirect?id=07560ae5-85bc-499c-92bb-68bd6c0f4c57)

Na próxima camada temos a divisão por serviços da Aws ou aplicações. Nesta área o interessante é manter as informações globais da Seazone, como Vpc, Eks e as aplicações dentro do cluster como no exemplo abaixo:

 ![](/api/attachments.redirect?id=57c58361-894c-4a61-823f-ea80d2d4deed)

Na camada das aplicações/helm, é importante que cada serviço/ferramenta seja divida por pastas para facilitar o acesso e manter a organização.

 ![](/api/attachments.redirect?id=c56aeca4-2218-471b-8c7f-7dc5cbcd45fb)