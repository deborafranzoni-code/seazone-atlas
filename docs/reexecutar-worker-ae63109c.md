<!-- title: Reexecutar worker | url: https://outline.seazone.com.br/doc/reexecutar-worker-JIBBZbqpEA | area: Tecnologia -->

# Reexecutar worker

No caso e falhas em envios de mensagens, é possível realizar a reexecução do worker para nova tentativa de envios.

É importante notar que ==ENVIOS BEM SUCEDIDOS NÃO SERÃO REEXECUTADOS==, apenas os mal sucedidos. O worker utiliza a coluna `was_message_sent_successfully` da tabela `reservation_precheckin_message_attempts` para desconsiderar reservas que já possuem mensagens enviadas com sucesso.

# Preparação para reexecução

Todos os registros de erros são informados no canal `#``**precheckin-messenger-alerts **`(Slack). Antes da reexecução, é importante que o motivo da causa dos erros seja endereçado, antes da tentativa de reexecutar o worker.

# Reexecutando

No momento da reexecução, deve-se acessar a [página de workflows do Argo Worfklow](https://argowf.seazone.com.br/workflows/prd-apps), buscando o último registro de execução para o worker. 

 ![](/api/attachments.redirect?id=7034c265-74dc-4f58-802b-ee28759f1d70 " =805x351")

Os registros de execução de workflows do worker sempre iniciarão com o prefixo `pre-check-in-messenger` em seu nome.

Ao clicar no nome do último workflow executado, para o worker de envio de mensagens de pré check-in, será apresentada a seguinte tela:

 ![](/api/attachments.redirect?id=878f30ce-833e-444b-b2fd-de0cebfa6fa8 " =1910x729")

Para realizar a reexecução, deve-se clicar no botão com o texto "RESUBMIT"

 ![](/api/attachments.redirect?id=7ca57ec1-3435-4e9b-b3af-abcc43d8244a " =1382x398")

Ao clique do botão um painel lateral será aberto, com o seguinte conteúdo:\n ![](/api/attachments.redirect?id=edd5b714-a4fe-4db0-9f79-9ff57d7cb77e " =428x258")

# Tipos de reexecução

É possível realizar três tipos de reexecução:

* Parâmetros padrões do worker
* Parâmetros personalizado de data do worker
* Reexecutando apenas para algumas reservas com falha

## Parâmetros padrões do worker

Por padrão, o worker busca reservas válidas com pré check-in para daqui três dias.

Caso esse comportamento seja adequado, basta clicar no botão "RESUBMIT", presente no painel lateral de "Resubmit Workflow". Após isso o worker será reexecutado com sucesso:

 ![](/api/attachments.redirect?id=526e0455-7bf4-4f60-b343-0a29e9caffd1 " =428x264")

Esse formato de reexecução é adequado quando se busca tratar erros de envio que ocorreram hoje (no dia em que está se realizando o suporte).

## Parâmetros personalizado de data do worker

Caso exista a necessidade de reexecução utilizando uma data diferente da calculada por padrão pelo worker, é possível utilizar o parâmetro de data, acessível pela interface de resubmissão do Argo Workflow.

Para isso, é preciso selecionar o checkbox "Override Parameters", presente no painel lateral de "Resubmit Workflow":

 ![](/api/attachments.redirect?id=537442e9-e3a1-4478-afd6-697afb935302 " =428x264")

Em seguida, será apresentada uma lista de parâmetros editáveis. Deve-se, então, informar ==a data de check-in das reservas que se deseja enviar==. O formato de data aceito é "YYYY-MM-DD".

Exemplo de preenchimento para a data de "5 de janeiro de 2026" seria: "2026-01-05" (no Argo, não deve-se inserir aspas - ""):

 ![](/api/attachments.redirect?id=97ab206a-ec80-4b2f-8b30-4b388c02c03a " =428x342")Com a data desejada preenchida, basta clicar no botão "RESUBMIT". Um novo workflow, com o parâmetro informado, será iniciado.

## Reexecutando apenas para algumas reservas com falha

Caso seja necessário realizar a reexecução de envio para um conjunto selecionado de reservas, é possível utilizar o parâmetro `reservation_ids`. Esse parâmetro permite a seleção de reservas através da inserção de seus IDs. Pode ser inserido um ou mais IDs. A separação de IDs deve ser feita por `,`. Não deve haver caracteres de espaço no valor inserido.

 ![](/api/attachments.redirect?id=423b7477-3ea6-436f-82cd-ed14bcfa4621 " =428x397")

A pesquisa por reservas com os IDs selecionados ocorrerá apenas na data considerada pelo worker para envio. No exemplo da imagem acima sendo `2026-01-05`. Caso nenhum valor seja inserido no parâmetro de data (`date`), o worker pesquisará as reservas com os referentes IDs na data padrão de envio (3 dias após a data atual de execução). Ou seja, a pesquisa por reservas com IDs selecionados sempre ocorre em uma data específica. Deve-se atentar para que, caso as reservas que deseja-se enviar não estejam na data padrão, seja inserido parâmetro de data correto, referente a data de check-in da reserva intendida.

Outra possibilidade de seleção é a exclusão de determinadas reservas para a operação de envio. Para isso é necessário realizar uma modificação nos dados da tabela `reservation_precheckin_message_attempts`.

Para todas as reservas com falha no envio que ==NÃO== devem ser consideradas no momento da reexecução do worker, deve-se alterar a coluna  `was_message_sent_successfully` para `true`. Ao fazê-lo, essas reservas serão desconsideradas no momento da reexecução, pois o worker considerará que já enviou mensagens relativas a essas.

Após essa preparação, pode-se prosseguir normalmente para as etapas de reexecução com [Parâmetros padrões do worker](https://outline.seazone.com.br/doc/reexecutar-worker-JIBBZbqpEA#h-parametros-padroes-do-worker) ou com [Parâmetros personalizado de data do worker](https://outline.seazone.com.br/doc/reexecutar-worker-JIBBZbqpEA#h-parametros-personalizado-de-data-do-worker).

É importante que, após finalização da reexecução, os dados alterados sejam retornados à seu estado original.