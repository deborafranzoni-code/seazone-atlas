<!-- title: Integração com Google Hotels | url: https://outline.seazone.com.br/doc/integracao-com-google-hotels-04oWWhvghu | area: Tecnologia -->

# Integração com Google Hotels

Created by: Bernardo Ribeiro Author: Bernardo Ribeiro Created time: June 19, 2024 11:48 AM Last edited: August 14, 2024 10:41 AM Tags: Disponibilidade, Google, Google Hotels, Preços, Propriedades

# Feed de Propriedades

https://developers.google.com/hotels/vacation-rentals/dev-guide/onboarding?hl=pt-br

Um feed de listagem de aluguel por temporada contém todas as propriedades a serem exibidas no Google. Esse feed contém os atributos físicos da propriedade, incluindo nome, endereço, locais de geocódigos, URLs de imagem, URLs de sites e comodidades.

Uma *lista de hotéis (properties feed)* é um ou mais arquivos XML que contém todos os hotéis para os quais você fornecerá informações de preço. O arquivo de lista de hotéis em si não contém informações de preços.

## Geração do XML

A geração do arquivo `Seazone_local.xml` e `Seazone_local.xml.zip` se derão por meio de uma uma task assíncrona no **Celery** que irá rodar **todo dia às meia noite** para gerar o XML e o arquivo ZIP.

Foi colocado logs em todo o processo, então é possível acompanhar a geração por meio dos logs (veja o código para melhor visualizar quais são os logs)

* **Detalhes da implementação**
  * **Nome da task:** `google_hotels.generate_properties_feed_xml`
  * **Nome do arquivo:** Foi definito conforme a **[orientação da documentação do Google](https://developers.google.com/hotels/hotel-prices/dev-guide/hlf?hl=pt-br#file-reqs).**
  * Para preenchimento do XML estamos usando um template, conforme o **[modelo](https://developers.google.com/hotels/vacation-rentals/dev-guide/vr-attributes?hl=pt-br#vr-example)** fornecido pelo Google em sua documentação. Usamos o **Jinja2** para preencher o template XML com os dados que queremos.
  * Para preencher o template, durante a Task é criado um dicionário de dados que contém os dados de todos os imóveis.

    > No dicionário os dados já são tratados de acordo com as diretrizes de sintaxe estabelecidas pelo Google, como por exemplo: escapar caracteres especiais, remoção de HTML, etc.
  * Após pegar os dados de todos os dicionários, esse dicionário é passado como contexto para o template XML, onde nele é carregado os dados dos imóveis.
  * O XML é dinâmico, de forma que só são colocados nele, os dados que um determinado imóvel possui. Isso é feito assim pois o Google não recomenda colocar itens vazios no XML, conforme consta na **[diretrizes de sintaxe](https://developers.google.com/hotels/hotel-prices/xml-reference/hotel-list-feed?hl=pt-br#guidelines)**.
  * Após gerar o XML, ele é passado por duas  validações
    * Verifica se está conforme o [Schema XSD do Google Hotel List](https://developers.google.com/hotels/hotel-prices/dev-guide/schemas?hl=pt-br).
    * Verifica se o tamanho dele é maior que 100MB (se for emite um log de erro)
    * Verifica se o tamanho dele está entre
  * Após passar pela validação, enviamos o XML para o S3 bucket que é definido na  variável ambiente: `S3_BUCKET_GOOGLE_HOTELS_PROPERTIES_FEED`, logo após também geramos o arquivo ZIP que também é enviado para o bucket mencionado.
    * Se tiver dado tudo certo, um arquivo com o nome `Seazone_local.xml` e `Seazone_local.xml.zip` estarão no bucket.
    * Em casos de XMLs inválidos serem gerados, será salvo no mesmo bucket, um arquivo com o nome `Seazone_local_INVALID.xml`.

      > Estamos salvando esse arquivo inválido para fins de debugs futuros em casos de erros. Além disso, dessa forma não sobrescrevemos o arquivo válido, garantindo que o Google consiga puxar um XML válido.

  <aside> ℹ️ **- [Diretrizes de sintaxe do XML](https://developers.google.com/hotels/hotel-prices/xml-reference/hotel-list-feed?hl=pt-br#guidelines)**
  * **[Pull Request](https://github.com/Khanto-Tecnologia/seazone-reservas-api/pull/284)** onde foi implementado

  </aside>

### Listings


---

`<listings>`

`<listings>` é o elemento raiz de uma lista de hotéis e contém um elemento `<language>` e pelo menos um `<listing>`.

O elemento `<listings>` aparece no seguinte local na hierarquia XML da lista de hotéis:

```xml
+ **<listings>**
    + <language> <!-- Obrigatório -->
    + <datum>    <!-- Opcional -->
    + <listing>  <!-- Obrigatório, deve ter pelo menos um -->
```

*Todos os listings (imóveis) da Seazone é um* `<listing>` que estarão dentro de `<listings>`

> Veja a sintaxe **[aqui](https://developers.google.com/hotels/hotel-prices/xml-reference/hotel-list-feed?hl=pt-br#listings-syntax)**.

`<listing>`

Uma definição de hotel em um elemento `<listings>` da lista de hotéis.

O elemento `<listing>` aparece no seguinte local na hierarquia XML do feed de lista de hotéis:

```xml
+ <listings>
    + <language>
    + **<listing>**
```

> Veja a sintaxe **[aqui](https://developers.google.com/hotels/hotel-prices/xml-reference/hotel-list-feed?hl=pt-br#listing-syntax)**.

### Content


---

Adiciona informações sobre uma ficha, como notas e avaliações, comodidades e outros detalhes. O elemento `<content>` é opcional. Em `<content>`, todos os elementos filhos são opcionais.

O elemento `<content>` aparece no seguinte local na hierarquia XML do feed de lista de hotéis:

```xml
+ <listings>
    + <language>
    + <listing>
        + **<content>**
```

> Veja a sintaxe [\*\*aqui](https://developers.google.com/hotels/hotel-prices/xml-reference/hotel-list-feed?hl=pt-br#content-syntax).\*\*

### Reviews

> *Atualmente não estamos enviandos as reviews (comentários) dos imóveis*

Contém uma resenha editorial ou de usuário. Não é necessário incluir todas as avaliações de uma ficha no elemento `<listing>`. Esse elemento serve para incluir avaliações selecionadas que indicam os recursos ou a qualidade da página.

O elemento `<review>` aparece no seguinte local na hierarquia XML do feed de lista de hotéis:

```xml
+ <listings>
    + <language>
    + <listing>
        + <content>
            + **<review>**
```

> Veja a sintaxe **[aqui](https://developers.google.com/hotels/hotel-prices/xml-reference/hotel-list-feed?hl=pt-br#review-syntax)**.

### Attributes


---

https://developers.google.com/hotels/vacation-rentals/dev-guide/vr-attributes?hl=pt-br#attribute-name

A tag `<attributes>` pode ser usada para descrever as comodidades da propriedade e classificar notas e avaliações.

```xml
+ <listings>
    + <language>
    + <listing>
        + <content>
            +<review>
            + **<attributes>**
```

> ***Importante:*** *todos os atributos são opcionais.*

Abaixo, contém a tabela (copiada da [documentação do Google](https://developers.google.com/hotels/vacation-rentals/dev-guide/vr-attributes?hl=pt-br#attribute-name)), onde mapeia os atributos que possuímos e estão sendo colocados no XML dos listings, caso a propriedade possua aquele atributos.

[\[tabela\] lista de Atributos](/doc/lista-de-atributos-2z1Mf28itX)

### Images


---

As imagens são usadas para mostrar a propriedade no ID da ficha.

```xml
+ <listings>
    + <language>
    + <listing>
        + <content>
            +<review>
            +<attributes>
            + **<image>**
```

Todas as imagens usadas precisam seguir estas diretrizes:

* A proporção recomendada para imagens é de 4:3.
* O URL da imagem precisa ser acessível pelo rastreador do Googlebot Image.
* Se o site incluir um robots.txt no nível raiz, verifique se ele contém uma das duas opções abaixo:

  
  1. Permite que o rastreador do Googlebot rastreie o conteúdo do seu site, as imagens incluídas.
     * User agent: Googlebot
     * Allow: /
  2. Permite que o rastreador do Googlebot Image rastreie as imagens no seu site.
     * User-agent: Googlebot-Image
     * Allow: /
* Capturas de tela de imagens ou sites não são permitidas. As imagens precisam ser originais e reais.

<aside> ⚠️ **Importante**: somente os parceiros configurados para mostrar imagens aos usuários finais podem ter as imagens listadas nas plataformas do Google. \*\*`Pendente >>**` Entre em contato com seu Gerente técnico de contas (TAM) para atualizar suas configurações de imagem.

</aside>

## Rota para Google obter XML


---

Foi criada uma rota para que o Google consiga nos consultar para obter o arquivo `Seazone_local.xml.zip`. Nesse zip contém o [XML gerado](/doc/integracao-com-google-hotels-64JMEYGIKt) com todas as propriedades da Seazone e seus respectivos dados.

Endpoint: \*\*`GET** /google/hotels/properties_listing_feed`

Ao enviar uma requisição para esse endpoint, será retornado uma **StreamingResponse** contendo o arquivo ZIP. Assim que realizada a requisição, será baixado o arquivo `Seazone_local.xml.zip`.

O arquivo ZIP é obtido a partir da integração com S3, onde buscamos lá o arquivo mencionado acima, e retornamos em chunks para uma melhor perfomance. Dessa forma, conseguimos retornar o arquivo "em tempo real". Deixando o response time da API em menos de 200ms.

Também estamos printando nos logs todo esse processo de obtenção do arquivo (veja no código quais são os logs).

## Atualização parcial do XML


---

*Não implementado…*

# Feed de Preços


---

> 🚧 *Implementação em andamento….*

**Forma de integração:** XML de disponibilidade, taxas e inventário (ARI)(Availability, Rates, and Inventory)

### Tipos de solicitação

O ARI usa as seguintes mensagens de solicitação:

* `Transaction` (Dados da propriedade). Define o tipo de quarto e as informações do pacote (plano de tarifa).
* `OTA_HotelRateAmountNotifRQ`. Define os valores da taxa de ocupação por data ou com base na duração da estadia por produto (combinação de tipo de quarto e plano de tarifas) para períodos específicos.
* `OTA_HotelAvailNotifRQ`. Define a disponibilidade e as restrições com base no tipo de quarto e nos planos de tarifa. O inventário também pode ser atualizado usando esta mensagem, mas é preferível usar `OTA_HotelInvCountNotifRQ`.
* `OTA_HotelInvCountNotifRQ`. Define o inventário físico de quartos ou o número de quartos disponíveis para venda.
* `TaxFeeInfo` (opcional). Define tributos e taxas por propriedade. Essa mensagem não é obrigatória se `AmountAfterTax` for especificado na mensagem `OTA_HotelRateAmountNotifRQ`.
* `Promotions` (opcional). Define taxas promocionais para determinados usuários, estadias e reservas.
* `RateModifications` (opcional). Define regras de modificação de tarifas para determinadas reservas, estadias e usuários.
* `ExtraGuestCharges` (opcional). Define como as tarifas precisam ser configuradas para crianças e outros adultos.

Cada mensagem contém um subconjunto de informações que o Google usa para calcular os preços e a disponibilidade exibidos aos usuários quando eles pesquisam suas propriedades com datas específicas de check-in e check-out e ocupação desejada.

Para mais informações sobre ARI, consulte a [Referência XML](https://developers.google.com/hotels/hotel-prices/xml-reference/ari-overview?hl=pt-br).

<aside> ℹ️ De acordo com a doc do Google, os timestamp devem estar no timezone do Hotel **Link da Doc:** https://developers.google.com/hotels/hotel-prices/xml-reference/datetime?hl=pt-br#DateTime

No futuro, caso venhamos a ter imóveis em outro fuso horário, essa parte deverá ser refatorada.

</aside>

### Desenho da solução Técnica

[https://miro.com/app/board/uXjVN47euTs=/?moveToWidget=3458764606851138571&cot=14](https://miro.com/app/board/uXjVN47euTs=/?moveToWidget=3458764606851138571&cot=14)


### Mensagem de Transação (Dados da Propriedade) ou Transaction (Property Data) 

> <https://developers.google.com/hotels/hotel-prices/dev-guide/ari-transaction-message?hl=pt-br> 
>
> <https://developers.google.com/hotels/hotel-prices/xml-reference/ari-property#restrict-room-capacity>
>
> <https://developers.google.com/hotels/hotel-prices/xml-reference/transaction-messages>

A mensagem de transação de ARI (dados da propriedade) define as informações sobre os tipos de quarto e pacotes (ou planos de tarifa) de cada propriedade. Cada tipo de quarto inclui um identificador exclusivo (RoomID), nome localizado, descrição e URLs para fotos do quarto. Os dados de cada pacote incluem um identificador exclusivo (PackageID), localizado como nome, descrição, ocupação e valores agregados.

É possível usar uma mensagem de transação para:

* Defina dados para uma ou mais propriedades.
* Defina o tipo de quarto e as informações do pacote para cada propriedade.
* Controlar ofertas de produtos.


**Implementação**

O envio dessa mensagem se dará logo após a finalização do sync de um imóvel. 

Para realizar o processamento da geração, validação e envio do XML para a API do Google será criado uma task assíncrona no Celery (`push_transaction_property_data`) que será executada como última task da chain de sincronização do imóvel, atualmente nomeada como `chain_sync_listing_tasks`

```python
def chain_sync_listing_tasks(stays_listing_id: str):
    return chain(
        get_listing_detail.s(stays_listing_id),
        sync_property.s(),
        link_property_destinations.s(),
        index_property.s(),
        update_availability.s(),
        update_fees.s(),
        push_transaction_property_data.s(),  # should be the last task
    )()
```

> **OBS:** A task `push_transaction_property_data` deverá sempre ser a última pois é preciso que o imóvel tenha sido indexado, uma vez que a fonte de dados para a mensagem de Transação é o OpenSearch.


**A task "push_transaction_property_data"**

Sua fila no serviço de mensageria é nomeada como "`google_hotels.push_transaction_property_data`". 

Essa task é responsável pela geração, validação e envio da mensagem Transaction (Property Data). Ela recebe como parâmetro o ID do Imóvel que será enviado a mensagem.

A implementação em si das operações realizadas para isso acontecer, ficam na classe `TransactionPropertyData` onde sua função "main" é a `push(property_id=)` que recebe como parâmetro o ID da propriedade.

Essa função `push()` realiza a chamada à função `self.generate_xml`, e a `GoogleHotelsAPI.push_transaction_property_data`.

* `generate_xml`: Obtém dados do imóvel, gera e valida o XML.

  
  1. `_get_property_data`: Obtém os dados do imóvel (`id`, `listing_title` e `guest_capacity`) a partir do OpenSearch. Caso seja necessário obter mais campos do imóvel, basta incluímos nessa query.
  2. Obtém o template (`transaction_property_data.xml`) e o renderiza passando como contexto os dados obtidos no passo anterior.
  3. Valida o XML gerado com o Schema XSD [Transaction (Property Data)](https://gstatic.com/ads-travel/hotels/api/transaction_property_data.xsd) e também valida o seu tamanho (não pode ser maior que 100MB). \nCaso tenha algum problema no XML é disparado um log de erro e a task é finalizada no mesmo momento, não enviado o XML inválido ao Google.\n**Log  caso inválido**: `ARI Transaction Message: XML generated is invalid.`\n**Log caso válido**: `ARI Transaction Message: XML generated is valid`


* `push_transaction_property_data`: Realiza o envio do XML gerado para a API do Google.\n***Request:*** `POST https://www.google.com/travel/hotels/uploads/property_data`\n*No Body é passado o XML gerado.*

  > *A API do Google retorna uma response no formato XML, porém, aqui no retorno dessa função, realizamos a formatação da resposta para facilitar sua manipulação.*

  Em caso de falha da requisição, será disparada uma exception para que a task seja executada novamente.(São executadas 3 re-tentativas)


Ao final do processo de será retornado o log informando a finalização e também o resultado do push da mensagem. É realizada uma verificação no retorno da função `push_transaction_property_data` (que faz envio do XML para o Google)

```python
seazone_logger.debug(
    loglevel, # INFO se sucesso ERROR se não sucesso
    "ARI Transaction Message: "
    f"Finished push transaction data for property {property_id}: {result_msg}", # result_msg: Success|Failed
)
```


> *No futuro, pode ser interessante dividir a função .push em duas: uma para apenas obter os dados do imóvel e gerar o XML e outra para apenas realizar o envio ao Google. Assim, caso falhe o envio ao Google a task não precisaria ser executada completamente.*\n***Ex: ***`chain(generate_xml.s(property_id), push_message(transaction_xml))`


**Informações enviadas**

Atualmente, enviamos a mínima quantidade de informações. Como nosso modelo é de aluguel por temporada, enviamos apenas a informação de um quarto, pois no nosso modelo de negócio, mesmo que tenhamos um hotel consideramos cada "apartamento" como um único imóvel.

* `Transaction` (elemento root do XML): Nele passamos atributos como o Timestamp, ID e Partner.
  * *Timestamp:* É a data e hora completa (com segundos) no timezone UTC.
  * ID: ID único daquela mensagem. Estamos gerando ela no formato: `seazone_propertyid_YYYYMMDD_HHMMSS`
  * Partner: É a "Chave do parceiro" que fica nas [configurações da conta](https://hotelcenter.google.com/accountsettings/basicsettings).
* `PropertyDataSet`: Enviamos a action como "delta", o que faz atualizar sem sobrescrever a informação de quarto.
* `Property`: ID do imóvel, mesmo que o HotelID enviado no Feed de Propriedades.
* `RoomData`
  * `RoomID`: ID do imóvel, mesmo que o HotelID enviado no Feed de Propriedades.
  * `Name`: Título do imóvel (listing_title)
  * `Capacity`: Capacidade de hóspeds do imóvel.
* `PackageData`: 
  * `PackageID`:  ID do imóvel, mesmo que o HotelID enviado no Feed de Propriedades.
  * `Name`: Título do imóvel (listing_title)
  * `AllowableRoomIDs`: Aqui, passamos a quais "Rooms" esse pacote de preços se aplica. No nosso caso passamos o item `AllowableRoomID` com o RoomID preenchido acima.

Todas essas informações são obtidas a partir do OpenSearch onde especificamos apenas os campos que queremos para evitar um retorno de campos desnecessários (que não serão utilizados).

# Referências


---

https://support.google.com/hotelprices/answer/11947461?hl=en&ref_topic=11957396&sjid=2589947505055144961-SA 


**Properties Feed**

https://developers.google.com/hotels/vacation-rentals/dev-guide/onboarding?hl=pt-br#before_you_begin 

https://developers.google.com/hotels/vacation-rentals/dev-guide/vr-attributes?hl=pt-br#attribute-name

https://developers.google.com/hotels/hotel-prices/xml-reference/hotel-list-feed

https://developers.google.com/hotels/hotel-prices/dev-guide/schemas?hl=pt-br

https://developers.google.com/hotels/hotel-prices/dev-guide/hlf?hl=pt-br#about-hlf

https://support.google.com/hotelprices/answer/10519514


**Prices Feed**

https://developers.google.com/hotels/hotel-prices/dev-guide/ari-overview?hl=pt-br

https://support.google.com/hotelprices/answer/6064419?hl=en

https://developers.google.com/hotels/hotel-prices/dev-guide/delivery-mode?hl=pt-br#pull


**Landing Pages (PoS)**

https://support.google.com/hotelprices/answer/9457428 

https://developers.google.com/hotels/hotel-prices/dev-guide/pos-syntax?hl=pt-br


**Schemas XSD**

<https://developers.google.com/hotels/hotel-prices/dev-guide/schemas?hl=pt-br>