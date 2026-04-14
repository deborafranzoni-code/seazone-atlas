<!-- title: Processo de suportes | url: https://outline.seazone.com.br/doc/processo-de-suportes-hbZYh5w3h0 | area: Tecnologia -->

# Processo de suportes

* [Kanban DataSolutions](https://drive.google.com/file/d/1OxqVO0ZjdVZbYAw_dbnqVWxZDviXOkhX/view)
* \

Quick links:

* Processo em fluxograma: [lucidchart](https://lucid.app/lucidchart/608869a4-a85c-4e9a-b54d-277f4cf9ea54/edit?viewport_loc=-5277,-2496,10658,5621,Nww7JK3gOfbp&invitationId=inv_54dff279-31d7-42b0-8fab-459568386594)
* Google Forms para pedidos de suporte: [forms](https://forms.gle/HxPrP9uqv1gn6rk7A)
* Automação:
  * [Planilha](https://docs.google.com/spreadsheets/d/1duRLB_SYTZ9y5qNHbcrZgI4pElSEktG4Fk0EcB9ybSU/edit?resourcekey=&gid=1556687773#gid=1556687773)
  * [Make](https://us1.make.com/164467/scenarios/1079301/edit)

# Motivação do processo:

Um processo de suportes é necessário para contornar d

* **Lentidão:** muitos suportes demoravam para serem resolvidos.
* **Falta de visibilidade:** os suportes eram pouco visíveis para a gestão do Pipe, não sendo fácil a identificação de quais suportes já tinham sido resolvidos, quais precisavam ser resolvidos, quais eram mais prioritários.
* **Responsividade:** muitas vezes o Pipe não era a primeira área que ficava sabendo quando um problema acontecia com os dados, e sim algum cliente do Pipe.

# O que é um suporte?

Pela atual definição que usamos, **um suporte é toda task que é**:

* **urgente** ⚠️ **OU**
* **pode ser resolvida muito rapidamente (até 1 hora)** ⏱️

Então se o scrapper da price_av quebra, mesmo que leve 2 dias para arrumar, é um suporte, pois é urgente ⚠️. Se pedem uma nova view que leva uns 30 minutos para criar ⏱️, é um suporte, mesmo que não seja urgente.

Porém se pedirem uma nova tabela, uma nova maneira de limpar/enriquecer os dados, um novo scrapper, uma alteração sistemática em vários jobs, que não seja urgente, não é um suporte, pois são tarefas que demoram mais que 1 hora!

# Tipos de suporte:

Um suporte pode ser dividido em:

* **problema:** alguma coisa quebrou ou algum dado está estranho
* **pedido de dados:** pedido de dados filtrados/agrupados de uma certa maneira
* **outro pedido:** uma nova tabela/view, ajuda com entendimento de algum dado

Também pode ser dividido em:

* **recorrente:** suporte que vem acontecendo várias vezes (o mesmo job sempre quebra toda semana, os mesmos dados são pedidos a cada 15 dias etc)
* **isolado:** algo quebrou e é muito raro de acontecer, um dado muito específico foi solicitado e provavelmente não será pedido novamente

# O processo em si:

**O processo de suportes do Pipe está descrito em um fluxograma em:**

[DAG do pipe | Lucidchart](https://lucid.app/lucidchart/608869a4-a85c-4e9a-b54d-277f4cf9ea54/edit?viewport_loc=-5277,-2496,10658,5621,Nww7JK3gOfbp&invitationId=inv_54dff279-31d7-42b0-8fab-459568386594)

Não irei explicar cada mínimo detalhe do fluxograma aqui, porém irei explicar como o atual processo tenta acabar com os problemas descritos em *[Motivação do processo](https://www.notion.so/Processo-de-suportes-1-3237629eaf5841669289a89190764fa6?pvs=21)*.

## Detecção:

A parte de *Detecção* tenta identifica quando um suporte é gerado, dando ao gestor **visibilidade** e **responsividade** dos suportes que acontecem. Esses suportes são identificados de várias maneiras diferentes: um alerta do Ferbot no Slack (que precisa ser refatorado!), alguém do próprio Pipe que detecta algum problema, alguém de fora do Pipe que detecta um problema (isso gera um KPI), ou então pessoas de fora do Pipe que pedem dados ou ajuda com alguma coisa. Todas essas diferentes formas são resolvidas com um Forms, que criar card automáticos no Trello e manda mensagens no Slack.

## Atribuição de responsabilidade:

Com um suporte devidamente detectado e visível, a próxima etapa é atribuir uma pessoa para resolvê-lo. Isso foi feito com a definição de uma tabela de *Data Owners*, que torna os diferentes *devs* do Pipe responsáveis por diferentes tabelas/jobs. Há sempre um DO titular e um DO reserva para cada tabela/job, mas **a responsabilidade deve ser atribuída a somente um** deles para evitar o famoso "deixa que eu deixo", melhorando a **velocidade** de resolução. Claro, há casos em que nenhum DO estará disponível, então caberá ao gestor definir outra pessoa.

Isso é válido tanto para suportes do tipo **problema** ou **pedido**, logo, cada dev deve ser responsável por manter funcionando suas respectivas tabelas/jobs e também por compartilhar os dados delas com o solicitante.

Tabela de Data Owners:

[Data Owners](https://docs.google.com/spreadsheets/d/1bfWTde23oAPP-yhd-iWSpCyy6F5dBH8eK5KNdxoSOzU/edit#gid=0)

## Avaliação do suporte:

O dev que foi atribuído para o suporte do tipo problema deve avaliá-lo e, caso descubra que a causa raiz não é de uma tabela/job seu, deverá informar o DO responsável para a troca de responsabilidade. Isso não deve demorar, já que a avalição é apenas uma avaliação preliminar do problema, que não deve comprometer a **velocidade** de resolução.

## Resolução do suporte:

Esta é a etapa de resolução do suporte e testes pelo dev, ficando livre para ele decidir a melhor maneira de fazer isso. Quando o suporte estiver resolvido, caso seja do tipo pedido, o dev deverá enviar a solução (por exemplo os dados solicitados) para o solicitante; caso seja do tipo problema, deverá avisar o solicitante que o problema foi resolvido.

## Fechamento do suporte:

Após o suporte ser concluído, há ainda alguns passos que melhoram a **responsividade**. Caso o gestor ou dev identifique que é um suporte recorrente, é necessário avaliar se é possível criar um sabor de sorvete (no caso de suporte do tipo pedido) ou então um alerta no Ferbot (no caso de suporte do tipo problema).

# Padronização dos pedidos:

Os suportes chegam ao Pipe de várias maneiras diferentes: o Bill pede diretamente para o gestor da área, alguém de outra área pede para algum dev do Pipe, um alerta no Slack chama a atenção etc.

Os pedidos que surgem precisam ser padronizadas e por isso a partir de agora eles serão criados por meio de um **Google Forms**, que é o mesmo forms utilizado para novos pedidos de sabor de sorvete.

Este Forms será utilizado tanto para as pessoas de fora do Pipe quanto para as pessoas internas ao Pipe.

Link para o **Google Forms**:


# Integração com Trello e Slack:

Uma vez que os pedidos estão padronizados, foi possível integrar o Forms com o Trello e o Slack, para criação de cards e mensagens automáticas. Essa integração foi feita pelo [Make.com](http://Make.com) (antigo Integromat), uma ferramenta low-code utilizada pela Seazone:

Link da integração low-code: <https://us1.make.com/164467/scenarios/1079301/edit>

# Prazos e Prioridades:

Os suportes do tipo **problema** não possuem prazo, pois são problemas apenas as coisas que precisam ser resolvidas **o mais rápido possível.**

Os suportes do tipo **pedido** possuem prazo, e são classificados com os seguintes níveis de prioridade:

* Prioridade 3\*\*:\*\* 10 dias úteis
* Prioridade 2: 5 dias úteis
* Prioridade 1: 3 dias úteis
* Prioridade 0: 1 dia útil

# KPI

Por enquanto dois KPIs que começarão a ser medidos são:

* Número de suportes do tipo problema enviados por pessoas fora do Pipe: o objetivo é que este KPI seja 0
* Porcentagem de suportes do tipo pedido resolvidos dentro do prazo: o objetivo é que a porcentagem seja maior que 90%