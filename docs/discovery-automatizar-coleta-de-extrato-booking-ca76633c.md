<!-- title: [Discovery] Automatizar coleta de extrato Booking | url: https://outline.seazone.com.br/doc/discovery-automatizar-coleta-de-extrato-booking-ehBa3bO5H8 | area: Tecnologia -->

# [Discovery] Automatizar coleta de extrato Booking

# TL;DR

**Não é possível ter o download de extrato 100% automático** por conta da obrigatoriedade do 2FA usando SMS. Contudo, é **possível automatizar parte da rotina**, sendo necessária intervenção humana para informar o código OTP enviado via SMS.

**É possível automatizar a conciliação das reservas** usando a Booking Payments API, mas impossibilita o desenvolvimento da conciliação OMIE.

# Rotina usando Admin API (interno)

* O endpoint usado é interno do painel, não é uma API pública.
* Depende de sessão autenticada, cookies e tokens dinâmicos.
* Possui proteções anti-bot, gerando bloqueios (403).

## Como foi testado

O endpoint que gera o arquivo de download é montado via GraphQL:

```javascript
 https://admin.booking.com/dml/graphql.json?lang=xb&ses=dfba174aedd0b2598078a50571fa836a
```

A autenticação é feita pelos seguintes **cookies**:

* bkng_sso_session
* bkng_sso_auth
* esadm
* aws-waf-token

Mesmo autenticado, a API bloqueia qualquer acesso externo retornando  `HTTP 403 Access Forbidden`:

```markup
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <title>403 Access Forbidden</title>
  </head>
  <body>
    <center><h1>403 Access Forbidden</h1></center>
    <hr>
    <p>
      You have been detected as a robot accessing the site in violation
      of our <a href="https://www.booking.com/content/terms.html">terms of
        service</a>.
    </p>
    <p>
      We will block you unless:
    </p>
    <ol>
      <li>
        You identify yourself in your user agent string, and include the word
        'robot' and an
        email address where we may contact you (for example
        'company X robot &lt;your.email@domain.com&gt;').
      </li>
      <li>
        You fetch from us in an even and consistent manner that does not produce
        load
        spikes in our systems and impair our service to our customers.
      </li>
    </ol>
    <p><b>Warning:</b> continued violation of TOS is a criminal offense in many
      jurisdictions.
      <p>
        Please contact us at <a id="email"
          href="mailto:robotcontact@booking.com">robotcontact@booking.com</a> in
        case you think this is an
        error or if you have any questions.
      </p>
      <img src="https://reports.booking.com/block?type=img"
        style="display: none" />
      <script>
    (function() {
        function getRandomInt(max) {
            return Math.floor(Math.random() * max);
        }

        let blockId = getRandomInt(256 * 256).toString(16);
        let emailElem = document.getElementById('email');
        let emailAddress = "mailto:robotcontact+" + blockId + '@booking.com';
        emailElem.innerText = emailElem.href = emailAddress;
        fetch("https://reports.booking.com/block?type=fetch&blockId=" + blockId);
    })();
</script>
    </body>
  </html>
```

Fazendo a mesma requisição com o header *User-Agent* no formato `company X robot <your.email@domain.com>`, essa abordagem não funciona para o endpoint em questão. O acesso a esse endpoint exige uma **conta específica autenticada**, portanto apenas ajustar o *User-Agent* não é suficiente para obter um retorno válido.

Dessa forma, torna-se **inviável automatizar a geração desse documento utilizando a API**, uma vez que o endpoint impõe restrições que impedem o acesso automatizado de forma estável e confiável.

# Rotina usando Payments API

* <https://developers.booking.com/connectivity/docs/payments-api/understanding-the-payments-api>

Essa API expõe endpoints que retornam dados de pagamento de uma reserva em específico, além de disparar webhooks quando acontecem mudanças no pagamento da reserva.

Contudo, os endpoints não informam nenhum tipo de "identificador de pagamento", ou seja, um código que representa uma transação bancária feita pela Booking à Seazone e presente no extrato emitido pela plataforma administrativa. 

Isso impossibilita a Conciliação da OMIE, uma vez que esse código de transação é utilizado para fazer o match entre **pagamento OMIE** <> **pagamento Booking**.

# Web Crawler

* Não bloqueia um web crawler desde que usado com baixa frequência.
* Evita erros e bloqueio de sessão, porque o navegador gerencia automaticamente
* Geração pode levar minutos, precisa esperar um tempo **não fixo** antes do download.

## Passo a passo

* Fazer login na [página administrativa da Booking](https://account.booking.com/sign-in) com as [credenciais armazenadas no Vault](https://vault.seazone.com.br/ui/vault/secrets/secret/kv/Ferramentas%2Fbooking/details?version=22).
* Realizar autenticação 2FA. 
  * Selecionar a opção de SMS e escolher o número com final **8610** que pertence a @[Francisco Oliveira da Silva Filho](mention://a584ac44-61e1-4e33-8d83-92ef3de636ee/user/ed358268-7f1e-4490-9fff-b0aa608d820b) (solicitar código a ele).
    * Em produção, o código deve ser enviado ao colaborador que assumirá a responsabilidade de manter essa rotina.

 ![](/api/attachments.redirect?id=d0c1f830-f249-4497-81ad-07db99206de7 " =1153x649")

* Acessar seção **Financeiro → Relatórios Financeiros**

  \n![](https://outline.seazone.com.br/api/attachments.redirect?id=fd1b3a5a-f272-4e66-b554-dc5ab7ad1819 " =1242x699")


* Nos filtros "**a partir de"** e **"até"**, informar o período desejado.

\n ![](https://outline.seazone.com.br/api/attachments.redirect?id=4252d3c0-904e-4ca8-b599-bfd9b8148a6c " =1153x649")

* Clicar em **Gerar Relatório**

 ![](https://outline.seazone.com.br/api/attachments.redirect?id=cb01555a-fdea-450e-9cb3-b02938e537dc " =1142x643")

* Clicar em **Criar Relatório**

 ![](https://outline.seazone.com.br/api/attachments.redirect?id=db6591bc-0c17-4918-9cf6-387706e6537c " =1142x643")

* Clicar em **Baixar Relatório**

  ![](https://outline.seazone.com.br/api/attachments.redirect?id=9b59b293-c25b-4fc9-9b9b-8dadc02fa9e2 " =1142x643")


# Solução

Deve-se criar uma rotina com execução periódica que baixa o extrato utilizando o fluxo descrito em [\[Discovery\] Automatizar coleta de extrato Booking](/doc/discovery-automatizar-coleta-de-extrato-booking-ehBa3bO5H8#h-web-crawler). Contudo, é necessária intervenção humana para informar o código OTP enviado via SMS.

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
* Fazer a requisição `PUT /reservations/conciliate_reservations?file_uid=<uid_do_arquivo>&ota_name=booking`. 
  * A conciliação é feita de forma síncrona, então qualquer eventual erro é informado no retorno do endpoint.