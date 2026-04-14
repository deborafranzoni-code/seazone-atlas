<!-- title: POC Self cadastro de Parceiros | url: https://outline.seazone.com.br/doc/poc-self-cadastro-de-parceiros-wfGuFLfzui | area: Tecnologia -->

# POC Self cadastro de Parceiros

## O que é?

Uma solução que possibilite a um Parceiro impactado por uma campanha, MIA ou até organicamente possa entrar em uma página que explica o mundo de parceria da Seazone e possa fazer seu cadastro digital como parceiro Seazone sem a necessidade de interferência de alguém do time. 

## Objetivo com a POC

Criar uma alternativa simples e objetiva que destrave esse fluxo junto à área de Parcerias da Seazone, com esforço mínimo de tecnologia.

## Condições para se realizar a POC

* Não pode durar mais de 1 semana para ir ao ar.
* Não pode requerer grande esforço do Squad de desenvolvimento.
* Maximizar o esforço de Product Manager, Product Designer e Coordenador nas tarefas, quando possível.

## O que deve ser feito?

A solução deve ser o seguinte fluxo:


1. Deve ser criado o subdomínio parceiro.seazone.com.br.
2. Deve ser criada uma página web estática com a descrição e informações sobre o programa de parcerias da Seazone, opções para ganhar comissão e deve ter um link para um formulário onde o parceiro preenche os seguintes dados:

   
   1. E-mail
   2. Primeiro Nome
   3. Sobrenome
   4. Cidade
   5. Estado
   6. Telefone
3. Quando o parceiro preencher o form, deve ser disparado um evento para que via N8N seja seguido os fluxos seguintes.
4. Deve ser criada uma API de cadastro de parceiro, que recebe os dados informados anteriormente e cria uma nova conta de parceiros no BD da Seazone, retornando a senha (gerada aleatoriamente) associada ao cadastro ou a informação de usuário já cadastrado.
5. Deve ser disparado um e-mail ao Parceiro que se cadastrou com as informações que seu cadastro foi realizado com sucesso e com suas informações para login ou um email informando que o email cadastrado já possui conta na base de parceiros da Seazone, orientando a pessoa a recuperar seu email.PS: se o email vai ser disparado via nosso backend ou via N8N, são vocês quem definem o jeito mais simples.