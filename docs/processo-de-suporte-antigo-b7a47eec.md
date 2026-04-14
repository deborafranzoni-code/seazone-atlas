<!-- title: Processo de suporte antigo | url: https://outline.seazone.com.br/doc/processo-de-suporte-antigo-nxXRA5ifQp | area: Tecnologia -->

# Processo de suporte antigo

# Hoje

## Onboarding de automatizações do Ticket

Atualmente o processo de suporte do Site Reservas se parece com isso:


 ![](/api/attachments.redirect?id=a7971d00-738d-4c2f-9432-11c13a489a29 " =591x322")


## Priorizações e Categorizações

Não existe nenhum documento com os tipos de priorização, a motivação delas e como acontecem. No entanto, dentro do JIRA eles são categorizados como P0, P1, P2, P3 ou P4

# Expectativa

## Onboarding de automatizações do Ticket

O ideal enquanto processo é que o onboarding do ticket passe por um processo similar a este:

 ![](/api/attachments.redirect?id=cfd6f842-0234-4f29-8089-2e993167de73 " =760x312")


## Priorizações e Categorizações

Os tickets podem ser categorizados em 3 diferentes tipos:

* Bug
* Operacional
* Falso positivo

### BUG

| Tipo | Descrição | SLA |
|----|----|----|
| P0 | É quando uma funcionalidade de um fluxo essencial do nosso produto para de funcionar, atinge a mais de 50% dos usuários e não há outro caminho alternativo para se realizar a mesma tarefa. | 8h |
| P1 | É quando uma funcionalidade essencial do nosso produto não está funcionando, atinge a mais de 50% dos usuários, porém existe um caminho alternativo para realizar a mesma tarefa. | 3d |
| P2 | É quando uma funcionalidade não essencial não está funcionando adequadamente e este problema ocorre com mais de 50% dos nossos usuários. | 15d |
| P3 | É quando um problema atinge menos de 50% da nossa base, não é um problema em um fluxo essencial e/ou existe um caminho alternativo para realizar a mesma tarefa. | Backlog |


### Operacional

Um ticket é categorizado como operacional quando há a necessidade do time de desenvolvimento intervir para que seja solucionado um fluxo esperado, que não foi previamente codificado, priorizado ou é visto como débito técnico.

É interessante mapeá-los e gerenciá-los para que, através de dados, se consiga entender quando serão priorizados para o time codificá-lo.

Se faz mais do que necessários identificá-los e documentá-los para que qualquer pessoa consiga reproduzir os passos e resolve-lo em menor tempo possível.

Observação: Tickets operacionais tem um SLA de 1d


### Falso Positivo

Foi criado um ticket com alguma evidencia de que era um bug, porém o sistema fez o esperado.

Um ticket de falso positivo refere-se a uma situação em que um sistema ou processo identifica uma anomalia ou problema (como um erro, falha ou alerta), mas, após investigação, conclui-se que essa detecção era incorreta. Ou seja, o problema indicado não era real ou não representava risco ou impacto.