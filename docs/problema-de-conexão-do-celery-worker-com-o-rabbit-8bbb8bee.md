<!-- title: Problema de conexão do Celery Worker com o Rabbit | url: https://outline.seazone.com.br/doc/problema-de-conexao-do-celery-worker-com-o-rabbit-0Rf2YgsUbH | area: Tecnologia -->

# Problema de conexão do Celery Worker com o Rabbit

ID: SZRICDT-7 Data do Incidente: February 21, 2024 12:07 PM (GMT-4) → 1:17 PM Created by: Bernardo Ribeiro Created time: February 22, 2024 5:11 PM Tags: AWS, Backend, Celery, Lib/Dependência, RabbitMQ

## Resumo do Incidente

Entre às **13h07 e 14h17** do dia **21/02/2024**, nós detectamos através dos Logs do Worker que o mesmo estava sem conexão com o RabbitMQ.

O evento foi desencadeado por uma **Deploy** ao meio dia.

Devido a uma autalização da biblioteca **dnspython** que é uma dependencia de um pacote, acabou gerando problema na conexão entre o Worker e o RabbitMQ, gerando o seguinte erro: `[ ERROR/MainProcess] consumer: Cannot connect to amqp://seazone-reservas:**@ip-xxxxx.us-west-2.compute.internal:5672/seazone-reservas: [Errno -3] Lookup timed out.`

O evento foi detectado pelo Desenvolvedor Backend que estava monitorando o Deploy no momento em que foi realizado. A equipe começou a trabalhar no evento às 12:51, assim que foi visto o Log de Erro, iniciando uma video-chamada para investigar e resolver.

Este incidente de Alta afetou 1 dos usuário, o qual abriu 1 chamado pelo Jira.

## O que levou ao incidente

Às 11:31 do dia 21/02/24, (\~1h20min antes do incidente em questão), uma alteração foi introduzida na aplicação backend (API).

Coincidentemente 5 dias antes do dia do incidente, houve uma atualização de uma sub-dependencia de uma dependencia do projeto. Essa mudança resultou em impedir que o Celery se conectasse ao serviço de filas (RabbitMQ).

## O que não funcionou como esperado

Várias tentativas de conexão do Worker com o RabbitMQ foram realizadas, porém ocasionava em erro. Isso durou **1h10min**.

 ![Untitled](Problema%20de%20conexa%CC%83o%20do%20Celery%20Worker%20com%20o%20Rabbit%20c5f7744789144a19a8ee34557da8a54d/Untitled.png)

## Impacto

O serviço impedia as tarefas do Celery de rodar, impactando o a sincronização de dados como: Info de imóveis, reservas, pagamentos e sync com a Stays.

Foram enviados apenas 1 chamado no suporte do Jira

## Detecção do incidente

Este incidente foi detectado quando o Matheus (Dev) verificou os Logs do Worker após o Deploy. E o Desenvolvedor acionou o Gerente do Projeto (Bernardo), que em seguida comunicou no canal #website-support.

Em seguida, outro desenvolvedor foi acionado (Toni), para ajudar na resolução do problema.

## Causa raiz

Coincidentemente 5 dias antes do dia do incidente, houve uma atualização de uma sub-dependencia de uma dependencia do projeto. Essa mudança resultou em impedir que o Celery se conectasse ao serviço de filas (RabbitMQ).

 ![Untitled](Problema%20de%20conexa%CC%83o%20do%20Celery%20Worker%20com%20o%20Rabbit%20c5f7744789144a19a8ee34557da8a54d/Untitled%201.png)

## Resposta ao incidente

Após perceber os erros, Matheus entrou em contato com Bernardo e ambos se juntaram em uma video-chamada para resolver.

Juntos, investigaram e acabaram com os erros voltando a task definition do cluster para a última revisão estável até encontrar a causa raiz do problema.

Após resolver a situação, Matheus e Bernardo continuaram a investigar as possíveis causas, também foi enviado uma mensagem para o Toni que entrou na sala por volta das 17h para ajudar a achar a causa raiz.

## Como o incidente foi resolvido

Utilizamos uma abordagem de 3 etapas para a recuperação do sistema:

* Apagar o fogo
* Investigação da causa raiz
* Solução para a causa raiz.

### **Apagar o fogo**

Para apagar o fogo (problema), realizamos um *rollback* voltamos o Cluster para a **última task definition estável** (a do último deploy), com isso, os erros de conexão pararam e tudo voltou ao normal, nos dando tempo para investigar.

### **Investigação da causa raiz**

Testamos várias hipóteses que falharam:

* Testar versões anteriores do código,
* Comentar pedaços do código que tinham subido
* Revisar as alterações que haviam subido
* Testar conexão do projeto local com o worker de staging (aqui conseguimos reproduzir o erro, com o worker local não era possível replicar)

Por fim, fizemos um último teste que consistia em: Baixar a imagem docker da revisão que funcionava e tentar identificar **Qual a diferença da imagem da versão que funcionava com a que estava subindo.**

Logo, identificamos que as versões de algumas sub-dependencias do projeto estavam diferentes. Descobrimos então que o problema estava na biblioteca [\*\*dnspython](https://pypi.org/project/dnspython/#history)\*\* que atualizou da versão 2.5.0 para a 2.6.1, ocasionando o erro de conexão.

> *Os testes da imagem foi realizado em ambiente local, rodando a imagem localmente porém apontando para o BROKER (RabbitMQ) de staging.*

### **Solução para a causa raiz**

Com isso, resolvemos o problema **fixando a versão** desta biblioteca na versão 2.5.0 no arquivo **requirements.txt ([PR #144](https://github.com/Khanto-Tecnologia/seazone-reservas-api/pull/144/files)).** Após isso, realizamos novos deploys para staging e produção, onde não foram mais identificados os problemas anteriores.

Outro ponto interessante de se comentar, é que antes dos deploys, nossos testes no Github Actions havia começado falhar misteriosamente (pois funcionava 100% no ambiente local, todos passavam), por ter concluído que era algum bug dos testes, nós os comentamos para conseguir subir as alterações.

No entanto, após ter descoberto a causa raiz e corrigí-la, descomentamos os testes e para nossa surpresa eles voltaram a funcionar. Então, o problema dos testes também era por causa da biblioteca.

## Cronograma

**21-02-2023**

11:31 - INICIADO DEPLOY DO BACKEND PARA PRODUÇÃO

11:46 - WORKFLOW DE DEPLOY FOI CONCLUIDO

12:51 - IDENTIFICADO LOGS DE ERRO EM STAGING E PRODUÇÃO

13:08 - INICIO DA REUNIAO PARA INVESTIGAR E CORRIGIR O INCIDENTE

14:17 - APLICADO ROLLBACK PARA PARAR O ERRO

19:30 - DESCOBERTO A CAUSA RAIZ

**22-02-2023**

14:22 - LIBERADO CORREÇÃO DA CAUSA RAIZ PARA STAGING

17:12 - LIBERADO CORREÇÃO DA CAUSA RAIZ PARA PRODUÇÃO

18:30 - SEM NOVOS ERROS, INCIDENTE RESOLVIDO.

## Backlog Check

Não há itens no backlog que poderiam ter melhorado este serviço.

## Recorrência (incidentes semelhantes)

Não houve incidentes semelhantes anteriormente.

## Lições aprendidas

* Não ignorar erros misteriosos dos testes e não comentá-los.
* Bibliotecas também causam problemas. Nem sempre um incidente é erro de código ou problema de infra.
* sub-dependencias de Bibliotecas usadas no projeto, podem atualizar sozinhas e gerar problemas.
* Fixar as versões das bibliotecas no requirements.txt e só atualizar se realmente for necessário.
* Continuar monitorando os logs a cada deploy pra mitigar problemas e/ou descobri-los antes dos usuários.

## Ações para mitigar esse tipo de incidente

Fixar as versões das dependencias (e dependencias de dependencias) no requirements.txt e só atualizar se **realmente** for necessário.


---

**Artigo Gerado:**