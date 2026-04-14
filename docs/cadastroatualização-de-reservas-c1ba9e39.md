<!-- title: Cadastro/Atualização de Reservas | url: https://outline.seazone.com.br/doc/cadastroatualizacao-de-reservas-n4Ntk0aS1s | area: Tecnologia -->

# Cadastro/Atualização de Reservas

# Fluxo Atual de Cadastro de Reservas

Na imagem abaixo temos os workers envolvidos no fluxo de criação de reservas. O fluxo começa na task `stays_import_new_reservations_task`, que é um cron job que executa a cada 15 minutos. Esse job publica um evento, que é consumido pelo `stays_dispatch_reservations_by_date_taks`, dizendo para este buscar reservas criadas desde o dia anterior até o dia atual. Nesse momento, é feita uma requisição para a Stays para obter essas reservas. Para isso, é chamado o endpoint [POST reservations-export.](/doc/refatoracao-da-integracao-com-a-stays-AUEEgUqY9k) Em seguida, cada reserva é enviada como um evento que é consumido pela `stays_handle_reservation_task`.


 ![](/api/attachments.redirect?id=3bddc95f-5362-4528-a1da-bc966a4b526f)[Editar diagrama](https://www.planttext.com/?text=bP8nJiGm44NxESLegH6Ye4c1jg6WejW3H1DxGaOuTcIFOPSxSGekXfs0s1K8igtr__F_CxDDIb7pw02wiCVDZgOO_0QcyYf69lAAHN98hOnJYDfwVcaZ9uxFf19yQfNI4_YWZ8vxnT2lqT_jsMGb6v3Ga2Myli5HVDQGWBsjk5yYM4aJgHbEWTsXjQIyW7-Q1lBMyR5bKPPlIcCuSUog0o-SF0xQkSm0_tV1ozlLyHgydqaKyLEJq4Gf0qZ88-OHhH1ocjYyl_LY0gmbrnHp-WOVEkKZlkMPMsTTuB1KF2kpawAjd2_cMQd-t48pruzNf9cSl7xF1M1R5bJlyWC0)

# Fluxo Atual de Atualização de Reservas

O fluxo de autalização de reservas é muito semelhante ao [fluxo de criação de reservas](https://outline.seazone.com.br/doc/cadastroatualizacao-de-reservas-AcV4eGKKq4#h-fluxo-atual-de-cadastro-de-reservas). As principais diferenças são o tempo de disparo do job, que é a cada 6 horas. Além disso, busca-se um intervalo maior de reservas (reservas com check-out entre 30 dias atrás e a data de hoje). A lógica de criação e atualização de reservas são o mesmo para os dois casos, que é feito pela task `stays_handle_reservation_task`.


 ![](/api/attachments.redirect?id=84980876-b1f2-451d-a20f-2f18ae6a6b35 " =1036x")[Editar diagrama](https://www.planttext.com/?text=bL8xJWCn4Etd5AEa3Y0XKMo1Wb0AAeeSO3LhJrWh_iaUHmb7e-LYU3S8j092qbdMc_URMMQX9CLPW2xiSRQcc8AVGQo_Hfb8Nh123hajKPDmcpXpsf6Ou7ChbBVWWp1QtWY6pN_OrPvL4T812HLfmZliGw8CxFN0yukkDZcIg7xArXtQKM9a_JdKazTsOk28h38r9amcriC4pgrvwQMpXG5EXy35_TdM6dnoCQJQCNvYCghWKFMijejG17t8-FvcnRZwkBr1RIXVmRdyWvVHVuFFdV2VAkomEDHS8SxueV-g0yVa5yMnfc8hqPVGHLPFBgV1nsGeNJz88MjUloi3MDQz3JVw0G00)

# Fluxo Atual de Cadastro/Atualização de Reservas via Webhook

Além dos jobs de criação e atualização de reservas descritos anteriormente, há também uma integração com a Stays via webhook, cujo objetivo é fazer a criação ou atualização de reserva em tempo real.

Esse fluxo inicia-se com a Stays enviando um evento pela rota `POST /stays/event/`. Após confirmar que o evento está relacionado a reservas ou a listing, ele é enviado para a task `stays_handler_webhook_task`. Ao receber esse evento, esse consumidor vai direcionar o evento para a task apropriada. Por exemplo, se for uma criação, reativação ou modificação de reserva, o evento é direcionado para a task `stays_dispatch_create_update_reserv_event_task`, e assim sucessivamente, como pode ser visto na imagem. 


 ![](/api/attachments.redirect?id=34ec94ba-4461-4197-bf5e-9b27cb7575a9)[Editar diagrama](https://www.planttext.com/?text=fL8xJiGm4ErzYf5fGUbJe6seGGhIbjR47ZOMZYUodG3deU0WUp6SZs2Z9O8LbJsUzvcFTp5XI7thXEZonMhReKzG9NoB05VE7ffKkvw4gFaLP8LTO2_FiNkg6-RdLIAE2TMWDuw2UfaHAc7y2MPix33fHkb0c4ZrdHcFG972e6WWdtwb6d9qASVPcAm_dAB9czoi47BgJCBDxQh74kJ3VVK8nQHKJCH2YbF8IDdkleI9ms1m5XRRs6-blmweXBj5dK07YyUFupjVmqYomnm1zz2oiKzMBmyPEmlXPRLiJNnL17fD3jifpiw1MlwVw_dElln2TjAMFHe6X0Ken2xlTFpadm00)


A imagem abaixo mostra a lógica da task `stays_dispatch_create_update_reserv_event_task`. Basicamente, ela extrai do evento emitido pela Stays o ID da reserva, busca os detalhes dessa reserva através do endpoint [POST reservations-export](/doc/refatoracao-da-integracao-com-a-stays-AUEEgUqY9k) e envia esses dados da reserva para a task `stays_handle_reservation_task`.


 ![](/api/attachments.redirect?id=40f891db-d138-45b4-b0e3-3a970e1e1610 " =844x339")[Editar imagem](https://www.planttext.com/?text=lLBBJWCn3BpdAwps31_GGrK9E20XSUW7HDx4i1QB4pdU2lw-NlhW8JXq3vmi9JEUyMWspL1jV1r2wCeRBBPOjSWYL7_bn1N5m27lBMPk5ItrCIcXKHnhdePI8zr5sf5OD6mllr1xb3oSe6XSv80aoIuQlZ6s4mDWEV1pRzqmKWYNwSFL-aB7AtZiZ1JkRo4Z75tEKFsmVbfsNDCWAMFsAGKounS5dxMe-MSu73t3-0Cx0pATvVuXh3j9HKnHGH26dmRWypufna-S_C3hsRR-gCuARZpMSyeXRBnBKult)


Quando a Stays envia um evento de cancelamento ou remoção de reserva, esse evento é redirecionado para o consumidor `stays_dispatch_delete_reserv_event_task`. A imagem abaixo mostra a lógica dessa task.


 ![](/api/attachments.redirect?id=bc26a8aa-fdf4-4e9f-bcc3-0ea63b6d0eee)[Editar imagem](https://www.planttext.com/?text=bP4n3i8m34NtdCBgpWKw85IniC818XDR8gB4KUmYk3qfhH02Xh96VjyltnirB3PSUkUESeFcWBb8Qbokhp74ZCcWZjpLKzIC5awUk6TZNrYvN3rVEPatrFCFPiY4TNGYQ4RGeYJzHfeEKn0WXYsIQECuKNLopYqKWDNwAwI5Rj201H3cxP2vbzdlJSX7Sf_m6BXmTmlxAUiVsMKbjS2NQB704nR8g8g910HsMw3NnsfHcrhPUCi7)


Basicamente, essa task busca no BD as informações da reserva notificada e, em seguida, envia o ID dela para a task `stays_update_deleted_reservations_task`. Basicamente, essa task faz o cancelamento da reserva se o status dela na Stays também for cancelada.

# Propostas de Melhoria no Fluxo de Cadastro/Atualização de Reservas

Para resolver os problemas de sincronização em tempo real, em um primeiro momento consideramos que o cadastro/atualização de reservas via webhook seria a solução. Porém, como foi mostrado na seção anterior, esse fluxo já está implementado e, pelo menos do ponto de vista arquitetural, não vejo como seria possível melhorar a solução que foi implementada atualmente.

Porém, como esse problema está ocorrendo e está gerando problemas operacionais, o próximo passo será analisar alguns casos em que esse problema ocorre e, a partir disso, buscar identificar a causa raiz desses problemas. Com isso, esperamos detectar algum fluxo não coberto pela solução atual e atuar na correção dele.