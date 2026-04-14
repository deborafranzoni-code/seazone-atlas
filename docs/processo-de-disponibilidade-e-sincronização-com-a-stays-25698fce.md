<!-- title: Processo de disponibilidade e sincronização com a stays | url: https://outline.seazone.com.br/doc/processo-de-disponibilidade-e-sincronizacao-com-a-stays-LlewlXyrF3 | area: Tecnologia -->

# Processo de disponibilidade e sincronização com a stays

# Objetivo

Esse documento tem como objetivo entender o processo de sincronização da disponibilidade dos imóveis do website de reservas com a stays. Devido a nossa expectativa de conseguir aumentar a janela de disponibilidade dos imóveis, surgiu a necessidade de entender esse processo. A ideia é ter em mente principalmente os possíveis triggers desse sync que seriam afetados ao aumentar o valor de dias da janela de disponibilidade.

# Contexto

Atualmente, nossa janela de disponibilidade padrão é de 180 dias. Isso basicamente significa que todas as vezes que puxamos as informações de um imóvel, fazemos isso para hoje + 180 dias. Dessa forma, no nosso site, o período máximo no futuro que nosso usuário pode alugar é 180 dias.

Antes de mais nada, é necessário explicar de qual task estamos falando. A task responsável por esse sync é a **update_availability**. A partir de agora vamos explorar os possíveis triggers dela.

# Triggers

## chain_sync_listing_tasks

Essa chain é composta das seguintes tasks:

* get_listing_detail;
* sync_property;
* link_property_destinations;
* index_property;
* update_grouped_amenities;
* **update_availability:** responsável por atualizar a disponibilidade de datas do imóvel, justamente o processo em que estamos interessados;
* update_fees;
* push_transaction_property_data.

Há duas formas dessa chain ser triggada na aplicação:


1. Durante o sync de propriedades (pull_properties) que acontece a cada 24h (ou ao ser triggado manualmente);
2. Durante o recebimento de alguns webhooks da stays referentes a: eventos de criação ou modificação de propriedades.

## chain_sync_listing_rates_and_availability_tasks

Essa chain é menor que a anterior, sendo composta apenas pelas tasks:

* update_availability;
* update_fees.

Ela só é disparada a partir do método `_handle_listing_rates_and_calendar_update()` , que por sua vez, é triggado no recebimento de alguns webhooks da stays:

* Em eventos de **modificação**, **cancelamento** ou reativação de **reservas**.
* Em enventos de **modificação** de **taxas** e **restrições em calendários**.
* Em eventos de **modificação** de **taxas** em **propriedades**.

## Rotas

O **update_availability** também é chamado a partir de algumas rotas da nossa API, sendo elas:

* `/{reservation_id}/confirm`: Essa rota é responsável por confirmar a reserva. Cada vez que confirmamos uma reserva, rodamos a task **update_availability** para a propriedade que está da reserva que está sendo confirmada;
* `/reservations/create`: Essa rota é responsável por cria uma nova reserva. Cada vez que criamos uma reserva rodamos a task **update_availability** para a propriedade onde estamos criando a nova reserva.
* `/{reservation_id}/cancel`: Essa rota é responsável por cancelar uma reserva. Cada vez que cancelamos uma reserva rodamos a task **update_availability** para a propriedade associada a reserva que está sendo cancelada.