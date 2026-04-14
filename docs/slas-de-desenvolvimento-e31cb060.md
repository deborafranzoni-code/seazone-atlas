<!-- title: SLAs de Desenvolvimento | url: https://outline.seazone.com.br/doc/slas-de-desenvolvimento-X46PKBSF7d | area: Tecnologia -->

# SLAs de Desenvolvimento

Antes de iniciarmos a definição dos SLAs utilizados em desenvolvimento do time de Delivery do Sapron, vamos primeiro entender sobre como chegam as demandas.

Atualmente, temos duas formas de demandas de desenvolvimento, podendo ser elas na seguinte ordem de prioridade:


1. Correções de bugs de funcionalidades já existentes no ambiente de produção.
2. Novas funcionalidades.
3. Divida técnica.

> Mas afinal, de onde vem essas demandas?

As correções de bugs são levantadas pelo nosso Q.A @Pedro Paulo Sanches Figueiredo **(que é um dos responsáveis por** **garantir a qualidade no desenvolvimento do produto, através de testes ele verifica se tudo está sendo entregue conforme a expectativa do cliente),** em que quando os códigos são entregues no ambiente de staging pelos nossos desenvolvedores, o Pedro já realiza todos os testes necessários e caso necessário elenca quais correções devemos realizar antes da funcionalidade ficar disponível aos nossos usuários finais.

As novas funcionalidades, em sua maioria, são elencadas pelo time de Discovery liderado pela @Renata Domingues, que são os responsáveis por entender os objetivos de negócio, adaptar métodos, negociar com os envolvidos e avaliar se as decisões a serem tomadas irão trazer os resultados esperados. Após elencar todas as necessidades dos stakeholders, o próximo passo é realizar todas as etapas documentadas [aqui](/doc/discovery-to-delivery-a-jornada-p3gUJawYRM) e iniciar o desenvolvimento das funcionalidades.

Já dividas técnicas são pequenas correções, GAPs e refatorações elencadas ao decorrer do tempo pelo próprio time ou gestor responsável, em que por conta de prioridades ou demandas da Sprint, acabaram ficando para trás.

> Agora que já entendemos sobre as demandas do time de delivery, como podemos definir os SLAs de desenvolvimento?

SLA significa "Service Level Agreement" (Acordo de Nível de Serviço, em português) no contexto de desenvolvimento de software. Um SLA é um contrato formal que estabelece os níveis de serviço que um fornecedor de serviços deve atender. Ele define as expectativas do cliente em relação à qualidade, desempenho e disponibilidade do serviço ou produto fornecido.

No desenvolvimento de software, um SLA pode abordar vários aspectos, incluindo:


1. **Tempo de resposta:** Define o tempo máximo permitido para que a equipe de desenvolvimento responda a uma solicitação ou problema.
2. **Tempo de resolução:** Estabelece o prazo para corrigir ou resolver um problema após a sua identificação.
3. **Disponibilidade do sistema:** Especifica a porcentagem do tempo em que o sistema ou serviço deve estar disponível para uso.
4. **Desempenho:** Define métricas relacionadas ao desempenho do software, como tempo de carregamento, tempo de resposta de consulta, etc.
5. **Manutenção:** Estabelece períodos e procedimentos para manutenção preventiva e atualizações do software.

Estabelecer SLAs claros é essencial para garantir a satisfação do cliente, promover a transparência e fornecer diretrizes mensuráveis para a equipe de desenvolvimento. Além disso, os SLAs também são úteis para resolver disputas e gerenciar expectativas entre as partes envolvidas.

## E como as utilizaremos no SAPRON?

Primeiramente é necessário entender sobre que contexto é inserido uma equipe de desenvolvimento de software. Dentre as diversas metodologias disponiveis, hoje utilizamos o SCRUM que consite em  um framework ágil utilizado no desenvolvimento de software e em projetos complexos. Ele proporciona uma abordagem flexível e iterativa para o gerenciamento de projetos, com ênfase na colaboração, transparência e adaptação contínua.

Dentre seus vários componentes, nesse caso vamos falar sobre seus eventos em que incluem o Sprint Planning (Planejamento da Sprint), Daily Scrum (Reunião Diária), Sprint Review (Revisão da Sprint) e Sprint Retrospective (Retrospectiva da Sprint). Cada uma dessas reuniões tem um propósito específico para garantir a colaboração eficiente, a comunicação e a melhoria contínua.

Agora voltando ao Sapron, durante a realização da Sprint Planning, o gestor responsável explica ao time o que deverá ser desenvolvido em cada uma das tasks, deixando claro a importancia, implicações e afins, e ao final, cada um dos desenvolvedores deverá pontuar essas tasks da seguinte forma:

* PP: Menos de 1 dia útil.
* P: Menos de 3 dias úteis.
* M: De 5 à 6 dias úteis.
* G: 10 dias úteis.

E, ao final, levando em consideração que atualmente nossas sprints possuem 5 dias úteis, é possível identificar quais funcionalidades serão entregues dentro da Sprint e quais deverão ser remanejadas para as próximas.

> Agora que temos os SLAs como é possivel levantar métricas?

Após a Sprint Planning e todas as tasks estarem devidamente mensuradas é possivel levantarmos algumas métricas quanto a nossa velocidade de desenvolvimento, sendo elas:


1. Qual a % de U.S (user stories/ estórias de usuários / tasks) foram entregues dentro do prazo estimado, sendo possivel fazer uma consulta rápida através dessa consulta no nosso Jira Software:
2. Média de dias realizado por estimativas, consulte neste link:
3. Nosso Lead Time, ou seja, o tempo gasto em cada um das etapas, consulte neste link:

<https://seazone.atlassian.net/jira/software/projects/SAP/boards/3/reports/cumulative?atlOrigin=eyJpIjoiMGMxMGQ0OTk4OWM4NDRiOThlMjlkNzQ2NmJjYWQxOGUiLCJwIjoiaiJ9>