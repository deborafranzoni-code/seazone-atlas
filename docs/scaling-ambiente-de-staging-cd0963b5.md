<!-- title: Scaling ambiente de staging | url: https://outline.seazone.com.br/doc/scaling-ambiente-de-staging-4f7DxOG6xW | area: Tecnologia -->

# Scaling ambiente de staging

Esse documento tem como objetivo documentar o processo de scaling do ambiente de staging que será utilizado para que os times consigam aumentar o provisionamento de recursos desse ambiente quando necessário 


## Quais serão os níveis de scaling 

`High`

Esse será o nível onde o provisionamento de recursos estará no máximo para o ambiente a ideia é que nessa configuração o ambiente seja capaz de aguente um volume razoável de testes e acessos acontecendo 

Número padrão de pods : 6

`Normal`

Esse será o nível comum dos ambientes, a ideia é que esse nível seja utilizado apenas para testes de desenvolvedores e coisas mais leves, não é indicado para testes em grande escala com stakeholders

Número padrão de pods : 2

`Off`

Esse nível é para horários onde o ambiente estará desligado, o objetivo é economizar custo desligando o ambiente a partir das 18h BRT e ligando novamente somente as 8h BRT

Número padrão de pods : 0