<!-- title: Fluxo de Bloqueios entre Sapron e Stays | url: https://outline.seazone.com.br/doc/fluxo-de-bloqueios-entre-sapron-e-stays-ORYk3DfRJr | area: Tecnologia -->

# Fluxo de Bloqueios entre Sapron e Stays

# Fluxo Atual de Cadastro de Bloqueios

O processo atual é feito apenas pelo Multicalendar (Backoffice e Anfitriões) ou pelo calendário da Propriedade (visto diretamente pelo proprietário) quando acionado pelos usuários, através do endpoint `calendar/blocking/`.

A integração primeiro faz verificação pra saber se a propriedade tem tempo de preparo cadastrado pra poder agir de acordo, cria o bloqueio no Sapron e aí parte para a task assíncrona na Stays.

A task cria bloqueios adjascentes no sapron caso haja a necessidade, e independente disso cria o bloqueio principal na Stays. Faz o mesmo com os adjascentes em seguida.

Existem Logs durante o processo para comunicar de problemas, via Email, Slack e Console.

O processo dentro do sapron e na interação com a stays pode ser mais bem estudado nesse diagrama:

 ![](/api/attachments.redirect?id=80bdc727-1468-4c84-a882-33771d9513cf)

[criacao_de_bloqueios_sapron_stays_20_fev_2025.excalidraw 93528](/api/attachments.redirect?id=3e6e89f3-3eee-4fbf-a60d-3ce653751215)

*(Para importar, baixe o arquivo e abra-o no [excalidraw.com](https://excalidraw.com))*

# Fluxo Atual de Atualização/Cancelamento de Bloqueios

O processo atual é feito apenas pelo Multicalendar (Backoffice e Anfitriões) ou pelo calendário da Propriedade (visto diretamente pelo proprietário). Atualmente existem a rota e a task (`stays_update_blocking_task`) para atualização, mas não é possível fazer essa requisição via Frontend, **por esse motivo optei por mapear somente o de cancelamento.** Todas as operações desta documentação são feitas através do endpoint `reservations/calendar`.

A integração atualiza/cancela o bloqueio no Sapron e depois procede para a task respectiva.

A task de cancelamento verifica a existência de bloqueios adjascentes, caso haja, cancela eles primeiro no Sapron, depois na Stays. Independente disso, é enviada a mesma requisição de DELETE para a stays com o bloqueio da requisição original logo em sequência.

Existem Logs durante o processo para comunicar de problemas, via Email, Slack e Console.

O processo dentro do sapron e na interação com a stays pode ser mais bem estudado nesse diagrama:

 ![](/api/attachments.redirect?id=641b77ae-1702-477f-a730-9857ed471e43)

[atualizacao_cancelamento_de_bloqueios_sapron_stays_21_fev_2025.excalidraw 108565](/api/attachments.redirect?id=e4da3e5f-64d4-46a8-83dd-3d5e5b4e498a)

*(Para importar, baixe o arquivo e abra-o no [excalidraw.com](https://excalidraw.com))*


# Conclusão

A única sugestão que posso dar, e isso foi discutido na Daily que deveria ser abordado com a PM no seu retorno de férias por que depende do ponto de vista de produto, é inverter a ordem do cancelamento de bloqueios ou usar um status intermediário (que já existe, mas é exibido igual ao confirmado no Frontend) para o bloqueio que ainda não foi cancelado na Stays, por causa das tarefas serem assíncronas. De resto, o processo faz sentido pras regras atuais e não aparenta ser problemático.