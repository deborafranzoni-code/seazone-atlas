<!-- title: Redirecionamento do parceiro para o domínio wallet.seazone.com.br | url: https://outline.seazone.com.br/doc/redirecionamento-do-parceiro-para-o-dominio-walletseazonecombr-lf63Y9oMYI | area: Tecnologia -->

# Redirecionamento do parceiro para o domínio wallet.seazone.com.br

* <https://seazone.atlassian.net/browse/SAP-2515>

# Objetivo

Quando um parceiro acessa a plataforma a partir de [sapron.com.br/login](https://sapron.com.br/login), ele atualmente é redirecionado para [sapron.com.br/parceiro/painel](https://sapron.com.br/parceiro/painel). 

A partir de agora, todas as requisições feitas para o domínio **sapron.com.br/parceiro** devem ser redirecionadas para **wallet.seazone.com.br/parceiro**.

# Opção 1 – Criar um proxy reverso

A ideia é manter o código na mesma aplicação e adicionar um proxy reverso na infraestrutura que redireciona para o domínio correto dependendo do acesso feito. Exemplo:

* Usuário parceiro acessa o domínio __[sapron.com.br/login](http://sapron.com.br/login)__ e informa suas credenciais;
* Aplicação redireciona para a rota **/parceiros/painel**;
* Proxy reverso identifica o acesso ao domínio __[sapron.com.br/parceiros/painel](http://sapron.com.br/parceiros/painel)__ e redireciona o acesso para __[wallet.seazone.com.br/parceiros/painel](http://wallet.seazone.com.br/parceiros/painel)__ utilizando HTTP 302.
* Dessa forma, todo acesso ao domínio __[sapron.com.br/parceiros/](http://sapron.com.br/parceiros/)__ será redirecionado para o domínio __[wallet.seazone.com.br/parceiros](http://wallet.seazone.com.br/parceiros)__.

## Prós

* Pouca/nenhuma alteração no código do Sapron;
* Não é necessária autenticação entre sistemas, visto que a aplicação continua a mesma.

## Contras

* Adição de camada na infraestrutura que pode ficar invisível aos desenvolvedores;
* A depender da implantação, testar localmente pode não ser possível;
* Provavelmente o CI/CD deverá ser ajustado para adicionar o proxy reverso;
* Como o domínio será o mesmo da Wallet, pode ser que haja conflito no roteamento da aplicação. 
* Para que isso não ocorra, a aplicação Wallet **NÃO PODERÁ** construir rotas com no domínio __[wallet.seazone.com.br/parceiros](http://wallet.seazone.com.br/parceiros)__, visto que será usado para o Sapron.

# Opção 2 – Migrar o código relacionado para o app da wallet

A ideia é migrar toda a codebase que monta as rotas com prefixo **/parceiros** no Sapron para a codebase da Wallet. Dessa forma, a aplicação Sapron deixa de ter responsabilidade com parceiros, e passa o escopo para a Wallet.

## Prós

* Nenhuma alteração na infraestrutura da aplicação;
* Melhor organização: aplicações de mesmo domínio estão na mesma codebase.

## Contras

* Migração de código: muitas alterações serão feitas tanto no Sapron quanto na Wallet. Deveremos fazer testes regressivos para verificar que tudo continua funcionando.
* Deverá ser implementada uma forma de autenticação na Wallet durante o