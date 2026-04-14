<!-- title: Alertas | url: https://outline.seazone.com.br/doc/alertas-ie2LfoRJtl | area: Tecnologia -->

# Alertas

documentação voltada a mapear e organizar os alertas que temos atualmente que tem como fonte alguma ferramenta suportada pelo time de infra 

Primeiro vamos sugerir uma classificação de criticidade para esses alertas, o objetivo é ter pontos claros e concretos para padronizar a classificação de um alerta 


# Critérios

Primeiro vamos definir os critérios que serão analisados para essa classificação de criticidade 

## Impacto no negócio

**Impacto no negócio** é o critério que avalia a extensão e a profundidade dos efeitos que um problema técnico na aplicação pode causar sobre as operações, receita, imagem e experiência dos usuários da empresa.

## Gravidade técnica 

**Gravidade técnica** é o critério que avalia a severidade do problema do ponto de vista técnico, considerando o tipo e a magnitude da falha detectada na aplicação.

## Segurança

**Segurança** é o critério que avalia o risco que o problema ou alerta representa para a integridade, confidencialidade e disponibilidade dos dados e sistemas da empresa.

## Alcance funcional

**Alcance funcional** refere-se à extensão e à importância das funcionalidades da aplicação que são impactadas por um problema ou falha. Esse critério avalia quais partes do produto estão comprometidas e quantos usuários dependem dessas funções no uso cotidiano.

| Critério |  Baixa | Média | Alta |
|----|----|----|----|
| Impacto no negócio | 	< 5% usuários = 1 pts | 	5% a 20% = 3 pts | 	> 20% = 5 pts |
| Gravidade técnica | erro pequeno/isolado = 1 pts | Erro funcional = 3 pts | Falha crítica/parada total = 5 pts |
| Segurança | Nenhuma = 0 pts | Potencial vulnerabilidade = 3 pts | Vulnerabilidade confirmada = 5 pts |
| Alcance Funcional | Afeta funcionalidades secundárias, pouco usadas = 1 | Afeta funcionalidades importantes, usadas por grupos significativos = 3 | Afeta funcionalidades críticas e amplamente usadas por  todos os usuários = 5 |

**Nota de corte** 

| Total de pontos | Criticidade |
|----|----|
| 1 a 5 | baixa |
| 6 a 10 | média |
| 11 a 15 | alta |


## **Organização de canais e alertas** 

o objetivo dessa seção é organizarmos como esses alertas serão endereçados conforme a sua criticidade 

## Uptime

Primeiro vamos organizar nossos alertas de uptime, que indicam se um serviço ou rota está funcionando ou não 

### Criticidade Alta :red_circle:

**Direcionamento**

Alertas classificados com uma  criticidade alta devem ser direcionados ao canal **#alerts-critics,** além disso dependendo da importância da aplicação afetada esse alerta também deve ser direcionado a pessoas chave de tecnologia via push notification

**Ações** 

Em casos assim uma war room deve ser criada com membros do time da aplicação e um membro do time de infra, após a resolução um relatório do ocorrido deve ser gerado e compartilhado com interessados 

### Criticidade Média :large_yellow_circle:

**Direcionamento**

Alertas com uma criticidade média ou baixa devem ser direcionados a um canal de uptime do time seguindo o seguinte padrão de nomenclatura **#alerts-nomedavertical-ambiente-tipodoalerta** exemplo (#alerts-backoffice-prod-uptime)

**Ações** 

Em casos assim o time responsável pela aplicação deve entender a criticidade do alerta olhando na [planilha de classificação](https://docs.google.com/spreadsheets/d/1bdINVr2G31-eOse6IEyA79ahJdSSkNyWfrK7qFhpCg0/edit?gid=0#gid=0)  para entender se a criticidade é média ou baixa,avisar lideranças e stakeholders da aplicação para entender a urgência de agir em cima disso e por fim investigar e entender o problema,nesse caso não há obrigatoriedade de war room para resolução e o time fica encarregado de solicitar a ajuda de infra caso seja necessária 

## Infra

Aqui é onde teremos alertas relacionados a recursos de infraestrutura, a ideia é conseguirmos saber se estamos prestes a ter um problema de recursos em algum componente do nosso ambiente, isso abrange problemas de memória, processamento e disco em diversos componentes que utilizamos, desde servidores que rodam as aplicações até banco de dados

Nesse caso específico enviaremos todos os alertas relacionados a infra em canais padronizados com a nomenclatura **#alerts-ambiente-tipodoalerta (#alerts-prod-infra)**

**Ações**

Se um problema em um componente de infra for identificado, o time de infra deve marcar o time de aplicação e agir na investigação do problema visando evitar possíveis downtimes e problemas maiores.


\