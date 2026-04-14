<!-- title: Queda do serviço de filas RabbitMQ | url: https://outline.seazone.com.br/doc/queda-do-servico-de-filas-rabbitmq-iDn2Ji1r5i | area: Tecnologia -->

# Queda do serviço de filas RabbitMQ

ID: SZRICDT-8 Created by: Bernardo Ribeiro Created time: September 10, 2024 9:06 AM

## Resumo do Incidente

Entre **22h00** do dia **09/09/2024 e 09h18** do dia **10/09/2024**, **{NÚMERO}** usuários encontraram problemas ao reservar ou mesmo finalizar seu cadastro no site de reservas.

O evento foi desencadeado pela **queda do serviço de filas (RabbitMQ)** em **09/09/2024 às 21:55**, a princípio **pela falta de armazenamento na máquina** que executa este serviço.

Essa falta de armazenamento levou ao interrompimento do seriviço e consequentemente, o interrompimento do processamento de reservas, sync de imóveis e de novos cadastros.

O evento foi detectado pelo Uptime ao enviar um alerta no canal `#website-alerts`, onde o time após receber o alerta, consultou os logs dos serviços da API, Worker e tentativa de acesso à máquina do Rabbit. A equipe começou a trabalhar no evento às 08h58 do dia 10/09/2024.

Este incidente de nível **Crítico (P0)** afetou {X%} dos usuários.

Houve impacto adicional, conforme observado pela abertura de **3 suportes** enviados por hóspedes através do Jira Service Managament do site relacionados a este incidente.

## O que levou ao incidente

> *Este tópico relata uma suspeita, mas não certeza do que levou ao incidente, haja visto que não conseguimos acessar a máquina EC2 que roda o RabbitMQ.*

Há a suspeita que a máquina que roda o RabbitMQ ficou sem espaço de armazenamento e travou às 21:55 do dia 09/09/2024. Levando a queda por completo deste serviço.

## Impacto

Descreva como o incidente afetou os usuários internos e externos durante o incidente. Inclua quantos casos de suporte foram abertos.

### **EXEMPLO:**

Por {XX horas XX minutos} entre {XX:XX UTC e XX:XX UTC} do dia {MM/DD/AA}, {RESUMO DO INCIDENTE} nossos usuários enfrentaram este incidente.

Este incidente afetou {XX} clientes (X% DOS USUÁRIOS DO {SISTEMA OU SERVIÇO}), que experimentaram {DESCRIÇÃO DOS SINTOMAS}.

Foram enviados {XX NÚMERO DE CHAMADOS DE SUPORTE E XX NÚMERO DE POSTS EM MÍDIAS SOCIAIS}.

## Detecção do incidente

Este incidente foi detectado quando o alerta de Downtime da API de produção pingou um alerta no canal `#website-alerts`, o dev Bernardo que estava online no momento, verificou os logs e identificou a perda de conexão entre o worker e rabbit.

Em seguida, o Bernar (SRE) foi acionada, porque Bernardo não possuía a chave de acesso à máquina do RabbiMQ.

{DESCREVA A MELHORIA} será implementada por {RESPONSÁVEL DA EQUIPE DA MELHORIA} para que {MELHORIA ESPERADA}.

## Causa raiz

Indeterminada (até o momento).

## Resposta ao incidente

Após receber um alerta às 22:00 UTC-3, Bernardo Ribeiro entrou online às 22:51 UTC-3 no Slack e em seguida no Cloud Watch par analisar logs dos serviços API e Worker, onde foi detectado a causa do alerta e problema de reservar.

Esse engenheiro escalou para o time de SRE para que a correção fosse realizada ao começar o dia de trabalho, no dia seguida (10/09), pois o desenvolvedor não possuía a chave de acesso à máquina.

## Como o incidente foi resolvido

Foi necessário criar uma nova instância no EC2 para executar o RabbiMQ. Foi utilizada uma chave de acesso à máquina que já era usada nas demais instâncias.

Após a criação da instância, foi atualizados nos serviços ECS de produção a URL do Celery Broker (rabbitmq no nosso caso), para que ele passasse a se conectar com a nova instância criada.

## Cronograma

Detalhe o cronograma do incidente. Recomendamos o uso de UTC para padronizar os fusos horários.

Inclua quaisquer eventos relevantes anteriores, início de atividades, o primeiro impacto conhecido e escalonamentos. Registre quaisquer decisões ou alterações feitas e quando o incidente terminou, j

**MODELO:**

XX:XX UTC - ATIVIDADE DO INCIDENTE; AÇÃO TOMADA

XX:XX UTC - ATIVIDADE DO INCIDENTE; AÇÃO TOMADA

XX:XX UTC - ATIVIDADE DO INCIDENTE; AÇÃO TOMADA

## Backlog Check

Atualmente estamos trabalhando no Épico "[\*\*Workers](https://seazone.atlassian.net/browse/SZRDEV-653) (SZRDEV-653)\*\* que já visa resolver esses problemas de instabilidades com os workers e rabbitMQ, mudando a arquitetura de como é atualmente.

Agora, estamos estudando a possibilidade de migrar provistoriamente (até a finalização do épico mencionado) para o SQS, que é um serviço de filas da AWS.

## Recorrência (incidentes semelhantes)

Houve já outros incidentes semelhantes porém não registrados. Um correlacionado seria o [Problema de conexão do Celery Worker com o RabbitMQ](/doc/problema-de-conexao-do-celery-worker-com-o-rabbit-SxYHmgFKFS)

## Lições aprendidas

* Necessidade de um sistema de monitoramento mais eficiente. O alerta que nos levou a descobrir a queda não tem relação direta com o rabbitmq ou worker.
* Evitar sempre que possível o uso de serviços que tenham que ser gerenciados por nós, e dar preferência para serviços gerenciados pelo Cloud Provider (AWS).
* Centralizar em um só lugar todas as chaves de acesso às instâncias para evitar dependência entre times.

## Ações para mitigar esse tipo de incidente

* Pensar em soluções resolver esse problema de filas, como por exeplo, migrar para o SQS ou AmazonMQ, por exemplo.
* \


---

**Artigos relacionados**

‣