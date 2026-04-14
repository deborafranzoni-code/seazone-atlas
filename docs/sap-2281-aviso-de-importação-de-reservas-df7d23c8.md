<!-- title: [SAP-2281] Aviso de importação de reservas | url: https://outline.seazone.com.br/doc/sap-2281-aviso-de-importacao-de-reservas-c9d40FPaSg | area: Tecnologia -->

# [SAP-2281] Aviso de importação de reservas

O objetivo deste documento é explicar as melhorias feitas no processo de importação de reservas e como funciona os alertas criados.

## Tabela "reservation_processing_report"

Essa tabela foi criada com o objetivo de acompanhar o status de processamento de todas as reservas que recebemos da Stays. Cada registro dessa tabela armazena as seguintes informações:

* `stays_code`: o código da reserva na Stays, ou reservation_stays_code, (por exemplo, "XI64I"). Esse código é único;
* `status`: o status de processamento, que pode ser "Pending" ou "Success". Se ocorrer algum problema no processamento da reserva, esse registro deverá ficar com status "Pending". Uma vez que uma reserva foi importada com sucesso, o registro é marcado como "Success" e ele nunca mais deverá ficar como "Pending" novamente.
* `pending_reason`: motivo pelo qual uma reserva ficou com status "Pending". Essa coluna é útil para identificar possíveis problemas durante a importação.
* `succeeded_at`: data-hora que a reserva foi inserida no sistema com sucesso. Uma vez que uma reserva foi importada com sucesso, essa data-hora será salva e ela nunca mais será alterada.
* `attempts`: número de tentativas que o sistema fez para importar uma reserva.

Toda vez que recebemos uma nova reserva da Stays, seja por webhook ou pelos workers de importações diários, pegamos o stays code dela e criamos um registro nessa nova tabela. Se o registro relativo a esse code já existia antes, apenas recuperamos ele (ou seja, não tem duplicação de registros para um mesmo stays code). Ao final do processamento da reserva, se a importação foi bem sucedida, trocamos o status de "Pending" para "Success". Futuras importações da mesma reserva apenas vão ler esse registro que já está com status "Success" e fará nada com ele.

Portanto, observe que o objetivo dessa tabela é **detectar problemas na importação de novas reservas**. Se ocorrer erros na atualização de uma reserva que já tinha sido importada antes, essa tabela não vai ajudar.

## Tasks para notificação de problemas

Para essa demanda, foram criadas duas tasks: `reservation_processing_report_task` e `stays_reservations_import_check_task`.

A task `reservation_processing_report_task` executa a cada 1 hora e ela verifica todos os registros na tabela `reservation_processing_report` com status "Pending", ou seja, ela busca reservas que tiveram algum problema durante a importação. Se existir tabelas com esse status, será enviada uma mensagem semelhante a essa no canal `sapron-x-stays`:

 ![](/api/attachments.redirect?id=bf933ee2-c316-4aa0-b497-f4988e7110b1)

Assim, a pessoa pode acessar o Metabase, procurar na tabela `reservation_processing_report` os registros que estão pendentes e ver na coluna `pending_reason` o erro que ocorreu. Alguns exemplos de mensagens que pode aparecer na `pending_reason` são: "no_original_reservation_found", "property_not_found", entre outros.

Já a segunda task, `stays_reservations_import_check_task`, executa a cada 30 minutos. Ele busca todas as reservas criadas na Stays no dia atual e anterior (assim como o worker de importação de reservas que roda a cada 15 minutos) e verifica o status dela na tabela `reservation_processing_report`. Se essa reserva estiver com status "Pending", a coluna `attemps` é incrementada em 1. Quando a task voltar a executar e essa coluna `attempts` for maior que 2, então a task considera que teve algum problema na importação e ela envia a seguinte notificação no Slack, no canal `sapron-x-stays`:

 ![](/api/attachments.redirect?id=aa35df7f-30e6-4f08-a838-1fb3b9692d52)

Por exemplo, suponha que a task `stays_reservations_import_check_task` busque na Stays a reserva "ABC123". Ela ainda não tinha sido processada pelo Sapron, então ela não tem um registro na `reservation_processing_report`. Sendo assim, essa task cria esse registro e finaliza o fluxo. A coluna `attempts` fica com valor igual a 0.

Trinta minutos depois, a task volta a executar e obtém novamente essa reserva "ABC123". Dessa vez, esse registro existe na `reservation_processing_report`. Como o valor de `attempts` é 0 e ele é menor que 2, então a task apenas atualiza a coluna `attempts` para 1 e finaliza o fluxo.

Após trinta minutos, a task volta a executar. Como `attempts` é 1 e ele é menor que 2, então apenas incrementamos o valor dele para 2 e finalizamos o worker. Ou seja, agora a coluna `attempts` é igual a 2.

Por fim, após mais 30 minutos, a task volta a executar, recupera o registro relacionado ao código "ABC123" e verifica que o `attempts` não é menor que 2. Com isso, o worker emite um alerta dizendo que essa reserva não foi importada, junto com outras na mesma situação. Enquanto a reserva não for importada pelo sistema, esse aviso será notificado no Slack.