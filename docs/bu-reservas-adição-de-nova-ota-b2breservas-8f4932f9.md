<!-- title: [BU Reservas] Adição de nova OTA (B2B.Reservas) | url: https://outline.seazone.com.br/doc/bu-reservas-adicao-de-nova-ota-b2breservas-Pz89yIcnyp | area: Tecnologia -->

# [BU Reservas] Adição de nova OTA (B2B.Reservas)

## Discovery

### Para sincronizar as reservas.

**1.** Entendido que a classe `**StaysHandler**` é a classe Core ("Mãe") de toda a sincronização da reserva com a Stays. Todos os processos de sincronização de reserva chamam ela, independente se a sincronização é manual (via API), via Webhook, via Task Assíncrona, todas chamam a `**StaysHandler**`.


**2.** Na Resposta da API usada para obter a reserva, o campo `response["partner"]["name"]` é "API B2B" (API `/external/v1/booking/reservations/{stays_id}`), logo, esse seria o *Partner Name*. Também vem dessa forma no response do reservation-export (API `/external/v1/booking/reservations-export`) 

```json
// GET /external/v1/booking/reservations/HC101J
{
    "partner": {
        "_id": "65f06a48aa7c454c822f99e4",
        "name": "API B2B",
        "commission": {"type": "fixed"}
    }
}

// POST /external/v1/booking/reservations-export
[{
    "_id": "694995502ef0ea0ee257a60d",
    "id": "HC101J",
    "type": "canceled",        
    "reserveTotal": 1010,
    "partnerName": "API B2B",
    "ownerFee": [],
    "fee": [],
},]
```

Esse campo `partnerName` é utilizado para a validação presente no `**StaysUpdater**``._get_data` (`stays_updater.py`; Linha 119) e `**StaysHandler**``._get_ota_name` (stays_handler.py; linha 421)

O campo `ota_name` precisa ser igual ao campo `ota_name` na tabela **reservation_ota**. (sugestão: **"B2B.Reservas"**)


:::info
~~No response (stays_reservation) não foi retornado o campo com nome~~ `~~partnerName~~`~~. Apenas foi encontrado dentro do objeto partner.name~~

No fluxo que lida com a reserva, são usadas 2 APIs diferentes para se obter informação da reserva. 

* Uma é a `/external/v1/booking/reservations/{stays_id}` que traz o objeto `partner.commission`
* Outra é a `/external/v1/booking/reservations-export` que traz uma listagem de reserva, e em cada reserva há o `partnerName` e `reserveTotal`.

:::


**3. (ponto de atenção)** Não foi visto no response o item `reserveTotal` o que poderá ocasionar o warning e report com status **Pending** e reason **"total_price_mismatch"** devido a validação na **linha 184** (`stays_handler.py`). Foi entendido que isso fará com que a sincronização não seja concluída automaticamente por esse fluxo.


:::info
~~No response (stays_reservation) não foi retornado o campo com nome~~ `~~reserveTotal~~`

No fluxo que lida com a reserva, são usadas 2 APIs diferentes para se obter informação da reserva. 

* Uma é a `/external/v1/booking/reservations/{stays_id}` que traz o objeto `partner.commission`
* Outra é a `/external/v1/booking/reservations-export` que traz uma listagem de reserva, e em cada reserva há o `partnerName` e `reserveTotal`.

:::


**4. (ponto de atenção)** O valor da comissão da OTA é obtida da reserva da Stays no fluxo atual. Porém, foi observado no response que o campo `partner.commission._mcval.BRL` não veio no response (ver exemplo no item 2). (linha **123**; `stays_handler.py`)


:::warning
No response (stays_reservation_details) não foi retornado o campo com nome com o valor da comissão `partner.commission._mcval.BRL`. 

:::

Esse campo precisa ser retornado pela API `GET /external/v1/booking/reservations/{stays_id}` ou então devemos inserir de forma mockada a `ota_fee` na função `**StaysCalculator._calculate_ota_fee**`. 

Para esse segundo caso, precisamos saber o percentual do ota_fee para o B2B.Reservas, e então adicionar um `elif` para caso `ota_name=="B2B.Reservas"`, use o ota_fee fixado para os cálculos.

```python
B2B_RESERVAS_OTA_FEE = 0.10 # valor a definir
class StaysCalculator:
    # ...
    def _calculate_ota_fee(
        # ...
        if ota_name in ("Seazone", "Madego", "Stays"):
            ota_fee = STAYS_FEE_OLD
            if stays_creation_date >= datetime(2023, 8, 1, 0, 0, 0):
                ota_fee = STAYS_FEE_NEW
        elif ota_name == "B2B.Reservas":       # adicionar essa condição
            ota_fee = B2B_RESERVAS_OTA_FEE
        else:
            # ...
        # ...
```


**5.** No arquivo `stays_calculator.py` é preciso adicionar o **partnerName** no mapping `OTA_NAMES` assim como foi feito no **item 2.**

```python
OTA_NAMES = {
    # ...
    # "partnerName": "ota_name"
    "API B2B": "B2B.Reservas"
}
```


**6.** Os listings (reservation_listings) são criados automaticamente durante o sync de reservas. Caso não exista ainda o listing (entidade usada no campo reservation.listing_id) um novo será criado.

As demais informações como id_in_ota, title_in_ota e ota_fee nesta tabela, são de resposanbilidade de um usuário do backoffice inseri-las por meio de uma tela própria para isso no sapron: Novo Listing, Editar Listing. ![Tela para edição de Listing no Sapron. Há uma semelhante para criar novos listings.](/api/attachments.redirect?id=86e71d09-eda0-401d-8867-809fb7d0f32d " =470x279")

### Para listar os links do anúncio


:::info
Caso haja uma **limitação** com relação **não possuir um link público** para os imóveis no B2B Reservas. Esse passo pode ser desconsiderado.

:::

**7.** No model **Listing** (reservation_listing) precisamos configurar o campo `ota_link` no arquivo `reservation > models.py > Listing` … **Linha 120** ![](/api/attachments.redirect?id=3d6b8c2a-c711-4742-ae57-71c615ec711d " =640x355")

Para isso também vamos precisar adicionar uma nova variável de ambiente `B2B_RESERVAS_LISTING_LINK_URL` contendo a URL base para a página do anúncio do imóvel.


:::warning
*Necessário entender qual é o ID do Listing na OTA para construção do Link*

:::

 ![](/api/attachments.redirect?id=d381f409-dd3b-46ae-b948-bc561d4b594c " =640x150")

E criar a constante `B2B_RESERVAS_INITIALS` no arquivo `reservation > constants.py` (sugestão: "BBR" para não confundir com o termo B2B - business to business) ![](/api/attachments.redirect?id=19fe9eb4-615e-4d6d-a9c6-a5a5dd788542 " =494x215")


**8.** A API usada para retornar os links dos imóveis é a `GET /properties/details` no campo **ota_links**.

A **ViewSet** é a `**PropertiesDetailsViewSet**` e o **Serializer** é o `**PropertiesDetailsSerializer**`, o campo `ota_links` é preenchido pela função `get_ota_links()` que utiliza o serializer `**ListingPropertySerializer**` que por sua vez busca pelo atributo `ota_link` retornado pela função mencionada no **item 5.**


## **Tasks**

- [x] Investigar ausência dos campos: `partnerName`, `partner.commission._mcval.BRL` e `reserveTotal`.
  * Descoberto que é usado duas APIs diferentes para obter as informações da reserva. 
    * Uma é a `/external/v1/booking/reservations/{stays_id}` que traz o objeto `partner.commission`
    * Outra é a `/external/v1/booking/reservations-export` que traz uma listagem de reserva, e em cada reserva há o `partnerName` e `reserveTotal`.
  * Sobre a ausência do campo `partner.commission._mcval.BRL`, de fato não vai vir e a comissão será um percentual fixo que está sendo decidido ainda.


- [ ] Cadastrar OTA
  - [x] Definir nome para OTA: **"B2B.Reservas"** (esse nome afeta o código do `StaysHandler`, no código há uma parte que obtém o `ota_name`)
  - [ ] Inserir nova OTA na tabela **Reservation OTA** (coluna `**initials**` deve ser igual a sigla no `**constants.py**`)

    ```sql
    INSERT INTO public.reservation_ota
    (created_at, updated_at, "name", initials, phone_number, account_manager, account_manager_email, img_url)
    VALUES(now(), now(), 'B2B.Reservas', 'B2B', NULL, 'Bill', 'b2breservas@seazone.com.br', ' ');
    ```
  - [ ] Inserir config da OTA na tabela **Reservation OTA Setup:** `delay=0` *(confirmar valor exato)*

    ```sql
    INSERT INTO public.reservation_ota_setup
    (created_at, updated_at, payment_delay, ota_id)
    VALUES(now(), now(), 0, 12);
    ```
  - [ ] Inserir Nome da OTA no mapping `OTA_NAMES` no arquivo `**stays_calculator.py**`

    ```python
    # src > channel_manager > action > stays > stays_calculator.py
    OTA_NAMES = {
        # ...
        "API B2B": "B2B.Reservas"
    }
    ```
- [ ] Adicionar Sigla da OTA no `**constants.py**`
  - [x] Definir sigla para OTA: **"B2B"** ou **"BBR"** *(sugestão de BBR para evitar confusão de termos) >> BBR*
  - [ ] Add linha: 

    ```python
    # src > reservation > constants.py
    # ...
    B2B_RESERVAS_INITIALS = _('BBR')
    ```
- [ ] ~~Inserir nova Variável de Ambiente:~~ `~~B2B_RESERVAS_LISTING_LINK_URL~~`

  
:::info
  Não será necessário pois a OTA não possui link público do anúncio. Os passos abaixo não serão necessários.

  :::

  Devemos inserir nela a URL base para construir o link do anúncio na OTA.
  - [ ] Descobrir formato do link de um imóvel na OTA **B2B.Reservas**
  - [ ] Adicionar ENV no **settings.py**  do projeto:

    ```python
    # src > config > settings.py
    # ...
    B2B_RESERVAS_LISTING_LINK_URL = config('B2B_RESERVAS_LISTING_LINK_URL')
    ```
- [ ] ~~Adicionar na Wallet API o retorno do link do anúncio~~
  - [ ] Adicionar sigla/iniciais da OTA no enum **[OtaNames ](https://github.com/seazone-tech/wallet-api/blob/main/app/enums/otas.py#L4)**(assim como definido no passo de definir sigla da OTA)

  
:::info
  *Não será necessário pois a OTA não possui link público do anúncio. Os passos abaixo não serão necessários.*

  :::
  - [ ] Adicionar sigla/iniciais no construtor do `PropertiesDetailsResponse`: [PropertyDetailsBuilder._build_otas](https://github.com/seazone-tech/wallet-api/blob/035d6d493d694fd3bfea6dfe95f682f794929699/app/builders/property_details_builder.py#L17-L27)
  - [ ] Adicionar sigla/iniciais no construtor [PropertyDetailsBuilder.get_ota_base_url](https://github.com/seazone-tech/wallet-api/blob/035d6d493d694fd3bfea6dfe95f682f794929699/app/builders/property_details_builder.py#L17C9-L17C25)

    ![](/api/attachments.redirect?id=51e9fb04-1a3a-47dc-a353-80124efd1e64 " =1895x745")
- [ ] No Frontend do Sapron e Wallet:
  - [ ] **Sapron |** Adicionar logo da nova OTA na reserva: Multicalendar,  
  - [ ] **~~Sapron |~~** ~~Adicionar logo da nova OTA na lista de links de OTAs na Pág. Detalhes do Imóvel~~
  - [ ] **Wallet |** Adicionar logo da nova OTA na reserva: Calendário do Imóvel
  - [ ] **~~Wallet |~~** ~~Adicionar logo da nova OTA na lista de links de OTAs na Pág. Detalhes do Imóvel~~
- [ ] Validações
  - [ ] Importar reserva vinda do B2B Reservas\nPela API, Webhook ou Task Async
  - [ ] Validar que a reserva foi importada e o `listing_id` atribuído foi ao listing do imóvel referente a OTA B2B Reservas
  - [ ] Validar que ao enviar a requisição `**GET/properties/details/{id}/ **`foi retornado o link para o B2B Reservas
  - [ ] Validar que o link do listing no B2B Reservas está correto
  - [ ] Validar valores financeiros da reserva (staging)

  *Se todas essas validações forem sucesso, a integração estará finalizada.*


## **Outras Informações**

* Documentação Sapron sobre [Cadastro/Atualização de Reservas](https://outline.seazone.com.br/doc/cadastroatualizacao-de-reservas-n4Ntk0aS1s) 
* API para Importar Reserva Manualmente da Stays `PUT /channel_manager/import_stays_reservation/`

  ```json
  PUT /channel_manager/import_stays_reservation/
  {
    "stays_id": "HC101J"
  }
  ```


## **Dúvidas**

* **Q: Em qual etapa ou como é criado o registro na tabela** `**reservation_listing**` **com os campos** `id_in_ota`**,** `ota_fee`**,** `title_in_ota`**?**\n**A:** Na tela Editar Listing e Novo Listing presentes no Sapron
* **Q: Não está claro o caso de uso das tabelas**  reservation_ota_listing_id **e** reservation_ota_listing_title**.**\n**A:** …
* **Q:** **O B2B Reservas parece não possuir um link público para o anúncio do imóvel. Procede?** \n*Nesse caso, mesmo que saibamos o formato da URL, o proprietário pode não conseguiria vê-lo.* \n*Poderia começar surgir suportes relacionados à "não consigo ver meu anúncio na OTA".*\n**A:** Não possui.\n\n**Q: Sendo o link do anúncio um link não-público, vamos exibí-lo no frontend?**\n**A:** Não.
* **Q:** **Qual o valor da** `**ota_fee**` **para o B2B.Reservas?**\n**A:** ??\n\n
* **Q: Verificar motivo da Cleaning Fee não estar sendo retornada.**\n**A**
* \


\