<!-- title: Perspectiva do Proprietário | url: https://outline.seazone.com.br/doc/perspectiva-do-proprietario-VLEbqbbmma | area: Tecnologia -->

# Perspectiva do Proprietário

# Fluxo Atual

Atualmente, o fluxo de perspectiva do proprietário funciona da seguinte maneira:


1. O usuário com role de admin se autentica no Sapron, recebendo um JWT de acesso contendo os seus dados
2. O usuário então acessa a perspectiva e o *front-end* fica encarregado de chamar as rotas do `sapron-backend` passando como `query params` o ID do `owner` alvo da visualização

Tal fluxo pode ser observado no seguinte fluxograma:


 ![](/api/attachments.redirect?id=2a659090-6e29-46aa-bbcf-a7791c85728c)


\
Essa implementação, por mais que simples, traz alguns problemas, como por exemplo a necessidade de lógica adicional para suportar essas `query params` tanto no *front* quanto no *back end.*\n\nTal implementação também inviabiliza a implementação dessa *feature* no recém adicionado serviço Wallet, onde os filtros por usuário baseiam-se no ID contido no `access_token`. Com esse ID sendo do usuário admin, fica impossível identificar o usuário alvo da visualização.


Por esses motivos, torna-se necessário a implementação de mudanças no fluxo de geração de `access_token` a fim de tornar possível a identificação do usuário alvo pelo JWT, tal como o tipo de acesso para controle mais preciso do fluxo. 

# Fluxo novo

O novo fluxo visa ajustar os tópicos abordados a cima. Isso será feito através da alteração dos dados contidos no JWT fornecido ao usuário com o intuito de identificar o alvo da visualização.

O novo fluxo começará da mesma forma do anterior: o usuário se autentica no Sapron e recebe um JWT contendo suas informações. Uma vez autenticado, ao acessar a perspectiva do proprietário, uma  para o *endpoint* de geração de *token* de visualização deve ser realizada, send passado no *payload* o ID do usuário  de destino. Isso indicará ao serviço que o token a ser gerado deve conter informações do usuário destino, mas será autenticado pelo usuário administrador. A rota então retorna o novo `access_token` para o usuário, que é redirecionado para o Wallet já autenticado pelo novo JWT.


\
 

 ![](/api/attachments.redirect?id=a7f4c685-18c3-4d75-ac91-3307cda266b2)