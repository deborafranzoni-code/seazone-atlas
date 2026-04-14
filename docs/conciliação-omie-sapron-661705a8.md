<!-- title: Conciliação OMIE - Sapron | url: https://outline.seazone.com.br/doc/conciliacao-omie-sapron-7xvNtWgifx | area: Tecnologia -->

# 💵 Conciliação OMIE - Sapron

Código do script atual: <https://script.google.com/u/0/home/projects/1gvoHce7_LJQukmQ2PMVApmcJOENw9H-ZCmhwa4fHlJD0Jgg_vfCISkZX/edit>

Planilha de lançamento de pagamentos OMIE: <https://docs.google.com/spreadsheets/d/1lHr2ROtOtKaLvu6_-0_VSw6zpXzrF6t764g1X_sEwkY/edit?gid=474202860#gid=474202860>

Planilha AdmSys (extrato das reservas): <https://docs.google.com/spreadsheets/d/1YHvus3u692wr75lO_SDJgYuCo6kPqcLh9VxJ5WQ7GhQ/edit?gid=1923745014#gid=1923745014>

URL da API OMIE: <https://app.omie.com.br/api/v1>

# Alterações no BD

Nova tabela `omie_payment_statements`.

Nova coluna `omie_payment_statement_id` na tabela `reservation_payment_statements`.

 ![](/api/attachments.redirect?id=a355248f-16f8-47c1-8f07-ec18c2c99784 " =1153x318")

# Etapas

## Upload de Pagamento de Reservas

O extrato de pagamento utilizado é o mesmo da conciliação do Sapron. Exemplo de extrato:

* **Airbnb**: <https://sa-east-1.console.aws.amazon.com/s3/object/sapron-files-prd?region=sa-east-1&prefix=conciliation/011534c4-airbnb_11_2025-11_2025-14.csv>
* **Booking**: <https://sa-east-1.console.aws.amazon.com/s3/object/sapron-files-prd?region=sa-east-1&prefix=conciliation/1ccbfca5-booking-1-payout_from_2025-09-27_until_2025-11-02-1.csv>
* **Expedia**: <https://sa-east-1.console.aws.amazon.com/s3/object/sapron-files-prd?region=sa-east-1&prefix=conciliation/6065bccd-expedia.csv>
* **Decolar**: <https://sa-east-1.console.aws.amazon.com/s3/object/sapron-files-stg?region=sa-east-1&prefix=conciliation/04089b48-decolarbookingreportsli-bookingreport-1-sli-bookingreport-1-slicsv.csv>

Quando o upload do extrato é enviado para conciliação, inserimos os registros de pagamento na tabela `payment_statements` e atrelamos o registro à reserva correspondente (se encontrada) na tabela `reservation_payment_statements`.

Dessa forma, uma reserva pode possuir N registros de pagamento cuja soma deve totalizar no montante da reserva (conciliada).

O objetivo é construir um fluxo que leia os dados da planilha e os insira nas tabelas `payment_statements` e `reservation_payment_statements`.

## Busca de `Contas a Receber`

Para buscar todos os pagamentos registrados na OMIE, é necessário fazer uma requisição para o endpoint `POST https://app.omie.com.br/api/v1/financas/contareceber/` com o seguinte payload:

```json
{
    "call": "ListarContasReceber",
    "app_key": "4352638314024",
    "app_secret": "2631d15e0214380cb4674da01cad6885",
    "param": {
        "pagina": 1,
        "registros_por_pagina": 999,
        "filtrar_cliente": "id_do_cliente",
        "exibir_obs": "S",
        "ordenar_por": "DATA_EMISSAO",
        "filtrar_por_emissao_de": "1_mes_antes_da_data_atual",
        "ordem_descrescente": "S"
    }
}
```

Onde ID dos clientes é um dos seguintes:

* **Airbnb**: `11054234520`
* **Decolar**: `11125455221`
* **Expedia**: `11082246027`
* **Booking**: `11082245930`

Os pagamentos não conciliados são identificados pelo campo `observação` vindo na resposta do endpoint supracitado: se estiver presente, o pagamento está conciliado; caso contrário, não está.

O objetivo é construir um fluxo que busque todos os registros sem o campo `observação` preenchido. Ao identificá-los, é necessário fazer o registro na nova tabela `omie_payment_statements`, responsável por armazenar os registros de pagamento advindos da OMIE:

 ![](/api/attachments.redirect?id=817d6eac-9a2f-4614-ac6e-25a45d32d884 " =621x522")

## Match entre Contas a Receber <> Pagamento de Reservas

De posse dos registros de pagamento de reservas (`payment_statements`) e dos registros de pagamentos da OMIE (`omie_payment_statements`), pode-se iniciar o processo de conciliação.

Para cada registro de pagamento da OMIE (`omie_payment_statements`), deve-se buscar os pagamentos das reservas (`payment_statements`) que foram feitos num período de tempo anterior ao dia atual (utilizar a coluna `payout_date` da tabela `payment_statements`). Para tal, deve-se agregar pelo identificador de pagamento (`payout_identifier`) todos os pagamentos de reservas feitos nesse período de tempo. 

O período de tempo é específico para cada OTA:

* **Airbnb**: 7 dias anterior ao atual
* **Booking**: 40 dias anterior ao atual
* **Expedia**: 7 dias anterior ao atual
* **Decolar**: 6 dias anterior ao atual

O pagamento é dito como conciliado quando o valor do registro de pagamento da OMIE é encontrado no resultado agregado de pagamento de reservas. A indicação de que um pagamento OMIE está conciliado é identificada pela coluna `is_conciliated` na tabela `omie_payment_statements`.

A relação entre pagamentos OMIE e as reservas atreladas é feita através da coluna `omie_payment_statement_id` na tabela `reservation_payment_statements`, que também deve ser indicada após conciliação.

## Envio para OMIE de pagamentos conciliados

Devemos sinalizar na OMIE que o pagamento foi conciliado, informando o ID do pagamento da OTA em questão.

Para cada pagamento conciliado, deve-se fazer uma requisição `POST /financas/contareceber/` com o payload:

```json
{
    "call": "AlterarContaReceber",
    "app_key": "4352638314024",
    "app_secret": "2631d15e0214380cb4674da01cad6885",
    "param": {
        "codigo_lancamento_omie": "{codigo_do_pagamento_omie}",
        "observacao": "_Invoice: {id_pagamento_ota}"
    }
}
```

Onde `codigo_do_pagamento_omie` é o `omie_payment_statements.payout_identifier` e `id_pagamento_ota` é o `payment_statements.payout_identifier`.

# Atividades a serem feitas


1. Criar migration para criar a tabela `omie_payment_statements` e a coluna `omie_payment_statement_id` na `reservation_payment_statements`;

   
   1. Além de criar as colunas especificadas para a tabela `omie_payment_statements`, considero que temos que inserir também uma coluna `is_sync_with_omie` para sabermos quando temos que chamar a rota da Omie para enviar os pagamentos conciliados. Se essa coluna estiver com o valor False e o campo `is_conciliated` for True, então sabemos que precisamos chamar a rota `POST /financas/contareceber/` da Omie para fazer a conciliação. Caso o valor seja True, então sabemos que não precisamos enviar novamente essa conciliação a Omie, pois ela já foi enviada antes.
2. Criar endpoint para ler um extrato de uma OTA e inserir os registros nas tabelas `payment_statements` e  `reservation_payment_statements`;

   
   1. Atualmente existe o endpoint `PUT /reservations/conciliate_reservations?file_uid=<file_uid>&ota_name=<nome da ota. Ex: "airbnb">`, que é a rota chamada para fazer a conciliação de reservas. Vamos precisar reaproveitar a lógica que essa rota utiliza para salvar os dados nas tabelas `payment_statements` e  `reservation_payment_statements`;

      
      1. O `file_uid` é obtido através da `POST /files/`, que gera uma URL pre-signed para fazer a inserção do arquivo no S3 e retorna o `file_uid` do arquivo.
3. Criar endpoint para acessar a API da Omie e inserir os registros na tabela `omie_payment_statements`;

   
   1. Para não precisar baixar todos os registros da API da Omie, podemos usar os campos `ordenar_por="DATA_VENCIMENTO"`e `ordem_descrescente="S"`  para recuperar somente os registros mais recentes. Por exemplo, se o último registro inserido possui um `due_date` de "2026-01-25", qualquer registro anterior a essa data pode ser ignorado.
4. Criar endpoint para fazer a conciliação de pagamento para o extrato do Airbnb;

   
   1. Esse endpoint vai implementar a lógica descrita na seção "[Match entre contas a Receber <> Pagamento de reservas](https://outline.seazone.com.br/doc/conciliacao-omie-7xvNtWgifx#h-match-entre-contas-a-receber-lessgreater-pagamento-de-reservas)" apenas para registros do Airbnb;
   2. Em seguida, buscamos todos os registros na `omie_payment_statements` que não estão conciliados e realizamos a lógica descrita na seção "[Envio para OMIE de pagamentos conciliados](https://outline.seazone.com.br/doc/conciliacao-omie-7xvNtWgifx#h-envio-para-omie-de-pagamentos-conciliados)".

      
      1. Se a API da Omie estiver fora do ar, vamos retornar um erro para o usuário indicando que a conciliação não pode ser concluída, pois a API da Omie está fora do ar. Aí o usuário teria que repetir o procedimento de reimportação em outro momento. Os pagamentos que foram conciliados mas não foram enviados para a Omie ficarão com o campo `is_sync_with_omie` igual a False.
5. Utilizar rotas criadas na página de conciliação de pagamentos, criadas no Retool;
6. Atualizar endpoint para fazer a conciliação de pagamento para o extrato do Booking;

   
   1. Atualizar a rota feita anteriormente para o Airbnb para também suportar os pagamentos da Booking;
7. Atualizar endpoint para fazer a conciliação de pagamento para o extrato do Expedia;
8. Atualizar endpoint para fazer a conciliação de pagamento para o extrato do Decolar;


Abaixo temos um diagrama de sequência para facilitar o entendimento da troca de mensagens entre o Retool e o Sapron

 ![](/api/attachments.redirect?id=ea92b044-8749-41e7-8c00-479e6402afa5 "left-50 =568x638")


\

\

\

\

\

\

\

\

\

[Editar diagrama](https://www.planttext.com?text=jP9FIyD04CNl-oc6FRkqwYreR6jxKeWaBUAfBCcq7SZknCr44F6xkw6DVq2A2BqzPj-y-GsparPiaCxLIkKep3MO50hR1FO9w8UiMC9eGpMsMkshOA9XRqsWVrbtL7rlrjF70efB7TkRWAQbhSSALlazbEo0mORdZbvOgy7u8r5VZCUGtUaZE2NxacgoGkn7ZNrrwCN4DGHx5K4z2qAWxKw0DuTaDSlcJubwK_09dS3L8DEpM6UnQsyTnleWK_Mkq5VG9_wsVwGzXzjyCLqkvdz6PaTe_i5z6hxLCRpsPfXq_JNpHA27iq-YBNx73m00)