<!-- title: Refactor das tasks | url: https://outline.seazone.com.br/doc/refactor-das-tasks-oPtBABMjeP | area: Tecnologia -->

# Refactor das tasks

Created by: fernando Created time: August 13, 2024 10:11 AM Last edited: August 28, 2024 9:19 AM Tags: Disponibilidade, Preços, Propriedades, Reservas, Stays

# Problema

Tem-se enfrentando recorrentemente um problema recorrente dentro do serviço `seazone-reservas-api` referente ao tráfego de mensagens. Até o momento, o fluxo de mensagens é utilizado para execuções de tarefas assíncronas que são executadas no próprio serviço. O alto fluxo de mensagens compromete o funcionamento dessas tarefas que por sua vez não conseguem ser executadas.

Sendo assim, o cerne do problema está no fluxo assíncrono de mensagens para ativação das tarefas porém, o comprometimento do funcionamento das tarefas vêm a afetar o os fluxos vitais do serviço, o que compromete a estabilidade do website.

Tendo isso em vista, para manter a integridade dos nossos fluxo vitais precisamos: (i) resolver o problema corrente; (ii) tornar tais fluxos vitais imunes a problemas de fluxos adjacentes.

Entendendo melhor o ponto (i), tem-se que o problema está:

* Na configuração das tarefas assíncronas
* Na utilização de mensageria.
* Na configuração do envio de mensagens.

E então precisa-se elaborar soluções que possam atender os problemas elencados.

Analisando o ponto (ii), tem-se para atender o esperado precisa:

* Isolar os fluxos.
* Encapsular a responsabilidade de cada fluxo.

Com isso, será preciso analisar os subdomínios das aplicações e refatorar arquiteturalmente o funcionamento de cada um deles. Por isso, tomando o fluxo de reservas para exemplo, tem-se que o funcionamento ocorre da seguinte forma:

* A criação de uma reserva inicia-se no request POST para `/reservations/create` ;
* Os dados da reserva são validados;
* A reserva é criada no banco com status `pending`
* A reserva é enviada para as tarefas assíncronas:
  * A reserva é enviada a task `confirm_reservation_task` que faz uma requisição para stays para criar uma pré-reserva para aquele imóvel
  * A reserva é enviada para task `notify_reservation_confirmed` que notifica o usuário de que a reserva foi feita e está aguardando pagamento;
  * A reserva é enviada para task `update_availability` para marcar que aquela propriedade foi reservada.

# Solução

A primeira o ponto a ser tratado é de os princípios arquiteturais baseado em microsserviços, para isolar as responsabilidades presentes no fluxo. Sobre o fluxo brevemente comentado anteriormente, é possível observar 3 subdomínios agentes: um responsável pela escrita da reserva no nosso banco, criação da reserva na API externa (stays) e a de notificação do status da reserva ao usuário.

Para isso, cada um dos subdomínios será um serviço separado, das quais o serviço responsável para escrita da reserva terá um banco de dados dedicado. A comunicação entre ps serviços permaneceria assíncrona para manutenção do funcionamento do fluxo em um tempo baixo de resposta, principalmente nos serviços que se comunicam com clientes ou que dependem de APIs externas.

Uma alternativa para atender a comunicação assíncrona seria utilizar o serviço da AWS SQS para envio de mensagens entre os serviços. Com isso, seria possível respeitar os padrões arquiteturais de *[um banco por serviço](https://microservices.io/patterns/data/database-per-service.html)*. Em casos onde um serviço precise acessar um dado presente no banco de outro serviço, seria possível utilizar a [messageria para envio de cópia do registro do banco de um serviço para o outro](https://microservices.io/patterns/data/transactional-outbox.html).

Refere aos serviços:

* Seazone-reservas-api: Responsável por receber a request de criação ou cancelamento de reserva e registrar no banco:

 ![image.png](/api/attachments.redirect?id=82bbda94-1c9b-4328-a784-425caa56417a)

Imagem 1: Fluxo de criação da reserva no banco e envio para registro da reserva na stays através da fila `queue_confirm_reservation`

 ![image.png](/api/attachments.redirect?id=7c31a31e-41c6-44c1-87ab-a4837a33ec26)

Imagem 2: Fluxo para atualização de status de uma reserva.

* Daemon-stays-reservation

Serviço responsável por ler uma mensagem da fila com um registro de reserva e criar/cancelar essa reserva na Stays. Após a atualização da stays o serviço envia a reserva para atualização no banco e notificação do status de reserva ao usuário.

 ![image.png](/api/attachments.redirect?id=182acd3c-b6cc-43fb-8adf-9b49bfadba09)

Imagem 3: Fluxo de criação/cancelamento de reserva na stays.

* Daemon-notify-reservation

Serviço responsável por notificar usuário da atualização da reserva

 ![image.png](/api/attachments.redirect?id=4a643ae2-1bff-4298-af84-75cda81fe7c5)

Imagem 4: fluxo de notificação de reserva para o usuário.

## Referências:

<https://microservices.io/index.html>