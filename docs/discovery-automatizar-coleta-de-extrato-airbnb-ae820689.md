<!-- title: [Discovery] Automatizar coleta de extrato Airbnb | url: https://outline.seazone.com.br/doc/discovery-automatizar-coleta-de-extrato-airbnb-Eziljk0xPP | area: Tecnologia -->

# [Discovery] Automatizar coleta de extrato Airbnb

# TL;DR

É possível automatizar o download do extrato da Airbnb usando a API interna deles, sendo necessário atualizar o cookie de sessão periodicamente.

# Recursos

* <https://github.com/seazone-tech/Pipe-scrapers/blob/Pipe-scrapers/internal/update_seazone_ids.py>
* <https://vault.seazone.com.br/ui/vault/secrets/secret/show/Ferramentas/Airbnb>

# Rotina usando API Airbnb (interno)

O login é realizado através da requisição `POST https://www.airbnb.com.br/api/v2/login_for_web?key=d306zoyjsyarp7ifhu67rjxn52tv0t20&currency=BRL&locale=pt` com o seguinte payload:

```json
{
  "metadata": {
    "sxsMode": "OFF"
  },
  "fromWeb": true,
  "queryParams": "{\"redirect_params\":\"{}\"}",
  "authenticationParams": {
    "email": {
      "email": "<email_contido_no_vault>",
      "password": "<senha_contida_no_vault>"
    }
  }
}
```

A requisição que gera o extrato é `GET https://www.airbnb.com.br/api/v3/FetchCsvReport/2eaa48f6f4024fc820dc3ec3055579c95eb8373509cea71042bd3215333cacd6`, com os seguinte query params:

* operationName
* locale
* currency
* variables
* extensions

Exemplo de URL:

```markup
https://www.airbnb.com.br/api/v3/FetchCsvReport/2eaa48f6f4024fc820dc3ec3055579c95eb8373509cea71042bd3215333cacd6?operationName=FetchCsvReport&locale=pt&currency=BRL&variables={"input":{"csvExportFields":["SENT_DATE","ARRIVE_BY_DATE","TYPE","RESERVATION_CONFIRMATION_CODE","BOOKING_DATE","RESERVATION_START_DATE","RESERVATION_END_DATE","NUMBER_OF_NIGHTS","GUEST_NAMES","LISTING_NAME","DETAILS","REFERENCE","CURRENCY","AMOUNT","TOTAL_PAID","HOST_SERVICE_FEE","FAST_PAY_FEE","WESTERN_UNION_FEE","CLEANING_FEE","RESORT_FEE","LINENS_FEE","MANAGEMENT_FEE","COMMUNITY_FEE","PET_FEE","GROSS_EARNINGS","OCCUPANCY_TAX","EARNINGS_YEAR"],"grossEarningFilters":null,"payoutTransactionAttributes":null,"payoutTransactionFilters":{"userIds":["227777128"],"startTimestamp":"2026-01-19T00:00:00Z","endTimestamp":"2026-01-22T23:59:59Z","airbnbProductTypeFilters":null,"paymentsProductTypeFilters":null,"gibraltarInstrumentTokens":null,"payoutBillTokens":null,"searchText":null,"forUser":null,"incomeTypeFilters":null},"productTransactionAttributes":null,"productTransactionFilters":null,"sendEmail":false}}&extensions={"persistedQuery":{"version":1,"sha256Hash":"2eaa48f6f4024fc820dc3ec3055579c95eb8373509cea71042bd3215333cacd6"}}
```

Exemplo de resposta:

```json
{
    "data": {
        "payout_transaction_history": {
            "__typename": "PayoutTransactionHistoryQuery",
            "fetchCsvReport": {
                "__typename": "PayoutTransactionHistoryFetchCsvReportResponse",
                "fileUrl": "https://airbnb-payments.s3.amazonaws.com/transaction_history/227777128/08f5eb05-5133-425d-abe3-7a1c01f37ccb?X-Amz-Security-Token=IQoJb3JpZ2luX2VjEB8aCXVzLWVhc3QtMSJHMEUCIQCDUl0rRDslacBaJREv%2BHPbJVX9wF6o3BwQZI76%2B%2BT9mAIgZjUUcpiEdtGqY607Fw5KQtyPt8SUmNtMDceJ2XiquasqnQQI6P%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgwxNzI2MzE0NDgwMTkiDKAj9t035Mp4S9wGJirxA68TFq7wnwoLstXcqlnhCQggSgtz3lKtu5dYsyqXjt8oPX8vXBVJv99NcCWLMyVl1ZVXLoxFAb%2F%2Fr4Lr8k9rw10%2FCd2DMpKNCQo1zXarV0KRkBMWs9ufqX96%2BUhh4xHgUbsLmo2K%2BRUX%2B1UXq%2BoTf%2BqwezCnlbCaxQ8UYD6Wnl%2F6dlZe1Y%2FpFhpTI7ajrOPhAIvkBBtWCMYbWb7F%2F7JesQnKmS%2Fj4HheAZapAhZAjG7kk%2FkzsLs42GFOHrVD6ENke5NO15HYEQ7mmGR4v8LByO3rSKafaZceNlBJ6AY%2FFgcEX1iEngXWnimRW2C0R8jkNiltq0cjSfBkhOvj4jmqyX9MgM9bw%2B%2BDXskufPjBnXRCrSA%2BixiChHvTzBfS8FpPeTR35yoqHeKRgEaMsJ1Ncd9tueCVk8at9a5w%2FSmB80NwpwbnNPUFzFoxVRjR6wU1hu3QYCVocl163M%2BbAcfsLCSRgy5q%2BS0s9MJ8YvZUgxmI2FudbH38Orh%2BamQMS%2BJ3UnqzGaI1%2FPspUYD2bCPQRSsVj7ON%2B6bZjYkCGM%2BLVG3MFcN5TtNS3zfBkg0bUTyg%2Fzv8wtUR08qOLhbHbwnpUBUNistiubFhlR%2BpoGLH43vi8nX0xs3527p7qNJY0zox9lomIBqZ5I%2F%2Beet9RSb5wsZNMJH1gswGOpIB2RHMB1k2kyz%2Frgbs54akZryf7Dx6s5VkrzI8Cm1Ychc%2FAIL86I2uCGfkFSg4LyhyAyeeBRW2cyIqONR7LWR%2FZNpQ6tFbGRo8%2FKrePMLZz%2BtOmnn5W6ieIMpT%2FkXE9FiBlj1VVF%2B6lUrsJMd1RPFhHyJlOpKchP2KljD5X%2B2IA7p%2FUnT%2BHhGnoQ%2FwKwRrfcWchdo%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20260202T151803Z&X-Amz-SignedHeaders=host&X-Amz-Expires=5400&X-Amz-Credential=ASIASQMNC3HJX2HRF7EK%2F20260202%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=98b90e6f6c83146f7f9d874962eb098b5a454f4666c386aa14aac7f2335e3760"
            }
        }
    },
    "extensions": {
        "traceId": "O16gxU2_c-qQOnyp8--mPA=="
    }
}
```

Headers obrigatórios**:**

| Header | Valor de Exempo | Nota |
|----|----|----|
| User-Agent | Mozilla/5.0 (X11; Linux x86_64; rv:147.0) Gecko/20100101 Firefox/147.0 | O endpoint pode bloquear **User-Agents de ferramentas HTTP** quando usado muitas vezes seguidas. Prefira usar um **User-Agent de navegador** para evitar bloqueio. |
| X-Airbnb-API-Key | d306zoyjsyarp7ifhu67rjxn52tv0t20 | Mesma regra aplicada à **URL** de login. |
| Cookies  | _aat=0%7CbU%2BFO4kgWR4ih4P1j1rc5yZ3fwV2w0IYB5JFtHmr2PjNCojIfrUhy9Q557uE5S6M | Obrigatório para **autenticação**. Gerado após login. |



:::tip
A geração do arquivo CSV é realizada por um endpoint de **execução demorada**, devido ao **alto volume de dados**. Em função disso, o serviço está sujeito a **políticas de rate limiting**, podendo retornar o status **HTTP 429 – Too Many Requests** caso o limite de requisições seja excedido. Nessa situação, novas requisições podem ser **temporariamente bloqueadas**, sendo necessário aguardar um intervalo antes de tentar novamente.

:::

# Web Crawler

* Fazer login na [página administrativa da Booking](https://account.booking.com/sign-in) com as [credenciais armazenadas no Vault](https://vault.seazone.com.br/ui/vault/secrets/secret/kv/Ferramentas%2Fbooking/details?version=22).
* Realizar autenticação 2FA. 
  * Selecionar a opção de **Email de Contato**, quem tem acesso a esse email e a Seazoner **Nathalia Mizevski** (solicitar código a ela).

    \
* Acessar **Todas as datas:**

  \


 ![](/api/attachments.redirect?id=761f7840-84ed-4889-9041-6de02f65e7bd " =837x471")


* Colocar o filtro em **Datas personalizadas** e selecionar para os **últimos Cinco dias:**


\

 ![](/api/attachments.redirect?id=ebaa981e-0d31-4429-80e2-aedb87ba0743 " =837x470")


* Clicar em **Baixar relatório em CSV:**


 ![](/api/attachments.redirect?id=492a0388-6959-4112-8bbb-28a480499b96 " =837x471")


# Solução

Deve-se criar uma rotina com execução periódica que baixa o extrato utilizando o fluxo descrito em [\[Discovery\] Automatizar Coleta de Extrato Airbnb](/doc/discovery-automatizar-coleta-de-extrato-airbnb-Eziljk0xPP#h-rotina-usando-api-airbnb-interno).

Após download do CSV, inicia-se o processo de conciliação conforme realizado atualmente (utilizando a Sapron API):

* Criação de registro de arquivo no BD:
* Fazer a requisição `POST /files` com o seguinte payload:
  * ```json
    {
      "category": "conciliation",
      "name": "<nome_do_arquivo>",
      "content_type": "text/csv"
    }
    ```
* O retorno do endpoint segue o padrão abaixo, contendo o `uid` do arquivo no BD e a URL assinada para a qual se deve fazer o upload do arquivo:
  * ```json
    {
      "uid": "<uid_do_arquivo>",
      "name": "011534c4-airbnb_11_2025-11_2025-14.csv",
      "category": "conciliation",
      "content_type": "text/csv",
      "storage": {
        "url": "https://sapron-files-stg.s3.amazonaws.com/",
        "fields": {
          "acl": "private",
          "Content-Type": "text/csv",
          "key": "conciliation/0d6bb261-011534c4-airbnb_11_2025-11_2025-14.csv",
          "AWSAccessKeyId": "AKIA2LIP2GAEYJRKMF5H",
          "policy": "eyJleHBpcmF0aW9uIjogIjIwMjYtMDEtMjlUMjE6MDU6MzRaIiwgImNvbmRpdGlvbnMiOiBbeyJhY2wiOiAicHJpdmF0ZSJ9LCB7IkNvbnRlbnQtVHlwZSI6ICJ0ZXh0L2NzdiJ9LCB7ImJ1Y2tldCI6ICJzYXByb24tZmlsZXMtc3RnIn0sIHsia2V5IjogImNvbmNpbGlhdGlvbi8wZDZiYjI2MS0wMTE1MzRjNC1haXJibmJfMTFfMjAyNS0xMV8yMDI1LTE0LmNzdiJ9XX0=",
          "signature": "++PVe7IJDNESr7zbbbmoz6m+Hxs="
        }
      }
    }
    ```
* Upload do arquivo CSV para o S3 utilizando a URL assinada;
* Fazer a requisição `PUT /reservations/conciliate_reservations?file_uid=<uid_do_arquivo>&ota_name=airbnb`. 
  * A conciliação é feita de forma síncrona, então qualquer eventual erro é informado no retorno do endpoint.