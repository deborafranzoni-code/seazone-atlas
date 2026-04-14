<!-- title: Análise de Viabilidade Técnica: De-por | url: https://outline.seazone.com.br/doc/analise-de-viabilidade-tecnica-de-por-WfjDU3mUFH | area: Tecnologia -->

# Análise de Viabilidade Técnica: De-por

# Contexto

## Objetivo

Queremos possibilitar a criação e aplicação de promoções no site. Essas promoções poderão ser associadas a um imóvel específico, a um grupo de imóveis ou a um destino (sendo o imóvel a unidade básica).

Qualquer pessoa do time, com as permissões adequadas, deve conseguir criar uma promoção de forma simples e intuitiva.

O objetivo é exibir o desconto no site no formato **de R$ X por R$ Y**.

[https://www.figma.com/design/SxkaCB56BXCDHHZq1oaWOG/Seazone-Site?node-id=6147-7968&t=ST2hTtQkJDktfZig-4](https://www.figma.com/design/SxkaCB56BXCDHHZq1oaWOG/Seazone-Site?node-id=6147-7968&t=ST2hTtQkJDktfZig-4)

## O que não é nosso objetivo

* Criação da estrutura de promoções na Homepage ou da Home personalizável.
* Criar um módulo que permite gerenciar coupons.
* Oferecer desconto DE-POR usando cupons por baixo dos panos (fallback).
* Aplicar **desconto automático** após a criação de uma promoção, interferindo diretamente nos preços em RM (preço "Por") (quem deve definir os preços das hospedagens é RM).
* Construir estrutura para armazenar preço histórico.
* ~~Limitação de uso de cupom em conjunto com promoção (combo preço promocional + cupom)~~


## **Requisitos**

* Deve haver **toggle para ativar/desativar** uma promoção De/Por 
  * A promoção vai ter um **toggle** **true/false** servindo como status para dizer se está ativa ou inativa.
  * *A promoção vai ter um **período predefinido** em que estará ativa: Starts_at, Ends_at*
* QUALQUER PESSOA deve ser **capaz de configurar/ativar** uma promoção.
* Deve ser possível **especificar quais imóveis** vão exibir o De/Por

  *Um imóvel não poderá estar em duas promoções com De/Por ativo, ao mesmo tempo devido conflito de preço "De", já que promoções podem ter % diferente.*
* Regras para **Exibir** preço De/Por em um imóvel:
  * Imóvel precisa possuir promoção com De/Por ativo.
  * A promoção deve estar ativa.
  * Não pode ser uma promoção expirada: O dia atual deve estar entre a data de início e fim da promoção. starts_at >= HOJE <= ends_at da promoção
  * ~~O preço atual DEVE SER MENOR que o preço histórico.~~
* Não impactar precisão de preço do Google Hotéis.
* *==(???) Adicionar configuração que permita proibir/permitir uso de cupons junto com a promoção?==*
* *==(???) Cada imóvel na promoção pode ter um % diferente? ou o % da promoção é para todos imóveis dela?==*\n

## **Premissas**

* Uma promoção possui uma duração pré-definida (tem Início e Fim), e pode estar ativa ou inativa.
* Os imóveis incluídos na promoção realmente estão com preços reduzidos em `x`%
* **==LÓGICA DE CÁLCULO:: Cálculo inverso do preço "De":==** O preço atual deverá ser reduzido por RM em `x`%, onde esse `x` será usado no cálculo do PREÇO "DE" para encontrar o desconto.

# Estruturas

Esta seção descreve as novas estruturas definidas neste discovery, incluindo tabelas no banco de dados e índices no OpenSearch.

## Tabelas

### promotions ==(new)==

```sql
CREATE TABLE promotions (
    id INT PRIMARY KEY AUTOINCREMENT
    name_slug VARCHAR(64) NOT NULL,
    name VARCHAR(64) NOT NULL,
    description VARCHAR(64),
    starts_at TIMESTAMP NOT NULL,
    ends_at TIMESTAMP NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT FALSE,
    
    -- Lista de códigos de propriedades, como 'VST001', 'VST123' etc.
    properties TEXT[] NOT NULL,           

    -- Configuração do preço anterior (DE-POR)
    show_previous_price NOT NULL DEFAULT FALSE,
    previous_price_config JSONB NOT NULL DEFAULT '{}'::jsonb,

    promo_type TEXT CHECK (promo_type IN ('blue_friday', 'sazonal', 'patrocinado'))
    internal_notes VARCHAR(128) NULL
);


-- Cria index para otimização de queries utilizando esse campo
CREATE INDEX idx_promotions_properties_gin ON promotions USING gin (properties);
```

 ![Model tabela Promotions](/api/attachments.redirect?id=0fe38af1-ac74-431d-bdc3-ce9950b9065b " =428x358")

## Indícies (OpenSearch)

### promotions ==(new)==

O schema será criado com base no mesmo formato do model de **promotions (acima)**, guardando no index os mesmos dados. Portanto, o mapping será baseado no Model.

```python
# exemplo do mapping
_indexes = [
    # conteudo existente...
    {
        "name": "promotions", 
        "mappings": {
            "properties": {
                "id": {...},
                "name": {...},
                # demais campos...
            }
        }
    },
]
```


### properties ==(modified)==

No schema de imóveis (properties) será adicionado um novo item do tipo lista para que guarde os IDs das promoções a qual aquele imóvel faz parte. Será equivalente a informação no index `promotions` do campo `id`. 

```python
# create_search_indexes.py

# exemplo do mapping
_indexes = [
    # conteudo existente...
    {
        "name": "properties", 
        "mappings": {
            "properties": {
                  # campos existentes...
                  promotions: {...} # lista de IDs referente ao indice 'promotions'
            },        
        },
    },
]
```


# Fluxos

## Gerenciar promoções ==(Novo Módulo)==


1. Alguém ~~da squad~~ cria a promoção no nosso DB;

   
   1. *Obs.: Validar que* *não há outra promoções ativa que contenha **show_previous_price** como true.* \n*Se já existe promoção_ativa && exibir_de_por, então retorna conflito.*
2. Task acionada para criar a promoção também no índice promotions do opensearch;
3. Task acionada para inserir o id da promoção nos imóveis necessários;
4. RM diminui os preços em X% para imóveis escolhidos para a promoção (tem que ser feito antes de iniciar a promoção);


> :bulb: **Ideia:** Podemos utilizar uma ferramenta como **[Retool](https://retool.com/apps)** para fornecer uma UI que qualquer pessoa consiga criar promoções. O App criado pelo Retool seria integrado com as APIs criadas para edição/inserção de promoções.
>
> **Exemplo de UI [(link)](https://sapron.retool.com/apps/8d69ed42-adfc-11f0-9f90-cb20e42e3dde/(1986739)%20Bernardo%20Ribeiro's%20Drafts/POC%20-%20Promo%C3%A7%C3%B5es%20Reservas/promotionManagementPage)** ![Protótipo inicial construído no Retool](/api/attachments.redirect?id=58fcb09e-ce9a-4114-ba08-bd2cc6886abe " =1916x1014")
>
> \

## Remover promoções inativas de imóveis

Para evitar ficar guardando informações obsoletas/inativas no indice de imóveis (OpenSearch),vamos precisar de algum processo que remova essas promoções do campo `promotions` no indice de `properties`. 

Será necessário:


1. Remover promoção de imóvel caso o status dela seja alterado para **inativo (is_active==false)**
2. Task async que verifica **x vezes** ao dia se há promoções que já expiraram.
   * Altera essas promoções para inativa **(is_active=false)**
   * Para cada imóvel vinculado, remove esses IDs de promoções do indice de `properties`.


## Exibir valor promocional

**Na** `**/properties/search**` **e na** `**/booking-price-v2**`**,** quando houver promoções com **preço de-por associado** (`show_previous_price = true` e `price_diff > X%`), será incluído um novo objeto `promotional_price` na resposta.


1. Adiciona novo objeto `promotional_price` na resposta;

   
   1. promotional_price

   ```sql
   promotional_price: {
       previous_total_price: 1000 // DE (calcula com base no aumento_equivalente)
       previous_night_price: 200  // DE (calcula com base no aumento_equivalente)
       promo_total_price: 900     // POR
       promo_night_price: 180     // POR
       discount_percent: 10% // (obtém do índice promotions)
       discount_value: 100 // (previous_total_price - promo_total_price)
   }
   ```

   
   1. Calcula o preço do "de" com base no desconto que foi aplicado

      
      1. `**aumento_equivalente**`` = desconto / (1-desconto)`

         
         1. para obter o desconto é necessário consultar o índice promotions no opensearch e obter as promoções associadas ao imóvel
      2. `aumento_equivalente * 100`
      3. valor do **"por"** é estipulado por RM, e já será o valor atual do imóvel. A redução realizada por RM é para ser equivalente ao **valor anterior - desconto**
   2. A partir dos valores "de" e "por", conseguimos saber o desconto em R$\n

   > ***OBS:*** *A diferença é que na busca esse processo é feito para cada imóvel, enquanto na booking-price é feito só para o imóvel que está sendo cotado.*

   \
2. Adiciona novo objeto `active_promotions` na resposta. **(opcional)**\nA ideia é que esse campo retorne as promoções ativas para aquele imóvel, possibilitando a exibição de badges  nos imóveis conforme as promoções ativas para ele.

   
   1. active_promotions


## Rotas

Seção que **detalha** tanto as **novas rotas** quanto as **alterações em rotas existentes**, incluindo a descrição e o propósito de cada endpoint.

### POST /promotions ==(new)==

Endpoint responsável pela criação de uma nova promoção. É necessário estar autenticado e possuir permissão de admin.

```json
{
    name_slug*: "bf-2025-vistas-de-anita" // (gera baseado no 'name' se não for informado)
    name*: "Blue Friday 2025"
    description: "Imóveis estão com 10% de desconto!"
    starts_at*: "2025-11-20 18:00:00"
    ends_at*: "2025-11-25 18:00:00"
    is_active*: true, (default: false)
    properties: {"VST001", "VST123", <list_property_ids>}
    show_previus_price: true,
    previous_price_config: { // DE-POR
        _type: percent, // (fixed)
        value: 10,
        target: "night_price" // total_price,
        apply_to_field: "de"  // por (default: "de")
    }
    promo_type: "blue_friday" // (blue_friday, sazonal, patrocinado)
}
```

> **OBS:** A criação da promoção aqui não garante que RM vá reduzir os preços. Será necessário um alinhamento prévio para que eles apliquem os descontos no tempo programado aqui.


### PATCH /promotions/{id} ==(new)==

Endpoint responsável por atualizar uma promoção existente pelo seu ID. É necessário estar autenticado e possuir permissão de admin.

```json
{
    # o campo de id e name_slug não será editável via API/UI
    name*: "Blue Friday 2025"
    description: "Imóveis estão com 10% de desconto!"
    starts_at*: "2025-11-20 18:00:00"
    ends_at*: "2025-11-25 18:00:00"
    is_active*: true, (default: false)
    properties: {"VST001", "VST123", <list_property_ids>}
    show_previus_price: true,
    previous_price_config: { // DE-POR
        _type: percent, // (fixed)
        value: 10,
        target: "night_price" // total_price,
        apply_to_field: "de"  // por (default: "de")
    }
    promo_type: "blue_friday" // (blue_friday, sazonal, patrocinado)
}
```


### GET /promotions ==(new)==

Endpoint responsável por retornar promoções do sistema, permitindo filtragem por status (`is_active`) e nome (`promo_name`). Os resultados podem ser paginados utilizando os parâmetros `page` e `page_size`.

> Promoção é considerada **ATIVA** se: `is_active=true` && `starts_at >= hoje < ends_at`.

```json
// GET /promotions?page=1&page_size=10
[
  {
    "id": 1,
    "name_slug": "flash-weekend-44",
    "name": "Flash Weekend",
    "description": "Imóveis estão com 10% de desconto!",
    "starts_at": "2025-10-31 00:00:00", 
    "ends_at": "2025-10-03 00:00:00",
    "is_active": true,
    "properties": ["VST001", "VST123"],
    "internal_notes": "Os preços de-por dessa promoção estão mockados"
    "show_previous_price": true,
    "previous_price_config": {
      "_type": "percent",
      "value": 10,
      "target": "night_price",
      "apply_to_field": "de"
    },
    "promo_type": "blue_friday"
  },
  {
    "id": 2,
    "name_slug": "blue-friday-2025",
    "name": "Blue Friday 2025",
    "description": "Imóveis estão com 10% de desconto!",
    "starts_at": "2025-11-28 00:00:00",
    "ends_at": "2025-12-06 23:59:59",
    "is_active": false,
    "properties": ["all"], // "all" indica que vale para todos os imóveis ativos do site
    "internal_notes": null
    "show_previous_price": false,
    "previous_price_config": {
      "_type": "percent",
      "value": 10,
      "target": "night_price",
      "apply_to_field": "de"
    },
    "promo_type": "blue_friday"
  },
  ...
]
```


### GET /promotions/{id} ==(new)==

Endpoint responsável por retornar os detalhes de uma promoção específica, identificada pelo seu ID.

```json
{
    "id": 2,
    "name_slug": "blue-friday-2025",
    "name": "Blue Friday 2025",
    "description": "Imóveis estão com 10% de desconto!",
    "starts_at": "2025-11-28 00:00:00",
    "ends_at": "2025-12-06 23:59:59",
    "is_active": false,
    "properties": ["all"], // "all" indica que vale para todos os imóveis ativos do site
    "internal_notes": null
    
    "previous_price_config": {
      "show": true,
      "_type": "percent",
      "value": 10,
      "target": "night_price",
      "apply_to_field": "de"
    },
    "promo_type": "blue_friday"
}
```

### GET /properties/search

Ajustar endpoint para adicionar o campo `promotional_price` na resposta sempre que houver promoções válidas com preço de-pôr, permitindo exibir os valores "de" e "por" e o desconto aplicado em R$.

```json
{
  "page": 1,
  "page_size": 1,
  "total_pages": 12,
  "total_results": 36,
  "results": [
    {
      "id": 773,
      "code": "VST033",
      "listing_title": "Cabana romântica com vista na serra VST033",
      "type": "Chalet",
      "guest_capacity": 3,
      "price": {
        "total_nights": 5.0,
        "total_price": 900.0,
        "night_price": 180.0,
        "cleaning_fee": 280.0,
        "date_from": "2025-11-02",
        "date_to": "2025-11-07"
      },
      "promotions": [1], // lista IDs de Promoções ativas para o imóvel
      "promotional_price": {
        "previous_total_price": 1058,
        "previous_night_price": 211.6,
        "promo_total_price": 900,
        "promo_night_price": 180,
        "discount_percent": 15,
        "discount_value": 158
      }
    }
  ],
  "date_suggest_results": null
}
```

> OBS: Regra de cálculo descrita na seção "Exibir valor promocional"


#### Exemplo de query ("JOIN") para obter promoções ativas de um imóvel

OpenSearch Application-side join


1. Consulta o índice de propriedades:

```python
GET properties/_search { "query": { "term": { "code": "VST001" } } } 
```

1\.1 Retorna a propriedade:

```json
{ "code": "VST001", "name": "Apartamento Vista Mar", "owner": "João" }
```



2. Consulta o índice de promoções filtrando por properties:

```json
GET promotions/_search { "query": { "terms": { "properties": ["VST001"] } } } 
```

2\.1 Retorna todas as promoções associadas a essa propriedade:

```json
[
  {
    "id": 100,
    "name_slug": "desconto-de-verao",
    "name": "Desconto de Verão",
    "description": "Aproveite 10% de desconto nos imóveis selecionados",
    "starts_at": "2025-12-01T00:00:00",
    "ends_at": "2025-12-31T23:59:59",
    "is_active": true,
    "properties": ["CNA001", "CNA002", ...],
    "previous_price_config": {
      "show": true,
      "_type": "percent",
      "value": 10,
      "target": "night_price",
      "apply_to_field": "de"
    },
    "promo_type": "sazonal"
  },
  {
    "id": "bf-2025-vistas-de-anita",
    "name": "Blue Friday 2025 - Vistas de Anitá",
    "description": "Desconto especial de 15% para imóveis selecionados",
    "starts_at": "2025-12-20T00:00:00",
    "ends_at": "2026-01-05T23:59:59",
    "is_active": true,
    "properties": ["VST001", "VST002", ...],
    "previous_price_config": {
      "show": true,
      "_type": "percent",
      "value": 15,
      "target": "night_price",
      "apply_to_field": "de"
    },
    "promo_type": "blue_friday"
  }
]
```



3. Resultado combinando:

```json
{
    "page": 1,
    "page_size": 3,
    "total_pages": 12,
    "total_results": 36,
    "results": [
        {
            "id": 773,
            "code": "VST033",
            "listing_title": "Cabana romântica com vista na serra VST033",
            ...,
            "promotions": ["bf-2025-vistas-de-anita"]
            "promotional_price": {...}
        },
        {
            "id": 1864,
            "code": "VST036",
            "listing_title": "Cabana com jacuzzi e vista na serra | VST036",
            ...,
            "promotions": ["bf-2025-vistas-de-anita"]
            "promotional_price": {...}
        },
        {
            "id": 305,
            "code": "VST022",
            "listing_title": "Cabana com vista panorâmica e jacuzzi VST022",
            ...,
            "promotions": ["bf-2025-vistas-de-anita"],
            "promotional_price": {...}
        }
    ],
    "date_suggest_results": null
}
```


\

\
### **GET** /properties/search/early-checkout

Ajustar endpoint para adicionar o campo promotional_price na resposta sempre que houver promoções válidas com preço de-pôr, permitindo exibir os valores "de" e "por" e o desconto aplicado em R$.

### **GET** /properties/search/vst

Ajustar endpoint para adicionar o campo `promotional_price` na resposta sempre que houver promoções válidas com preço de-pôr, permitindo exibir os valores "de" e "por" e o desconto aplicado em R$.

### **GET** /recommendation/suggest-sections

Ajustar endpoint para adicionar o campo promotional_price na resposta sempre que houver promoções válidas com preço de-pôr, permitindo exibir os valores "de" e "por" e o desconto aplicado em R$.

### GET /properties/{property_id}/booking-price (v1 e v2)

Ajustar endpoint para adicionar o campo `promotional_price` na resposta sempre que houver promoções válidas com preço de-pôr, permitindo exibir os valores "de" e "por" e o desconto aplicado em R$.

```json
{
    "property_id": 773,
    "date_from": "2025-11-02",
    "date_to": "2025-11-07",
    "total_price": null,
    "subtotal_price": 819.0,
    "nights_quantity": 5,
    "effective_price": 1099.0,
    "nights_price": 163.8,
    "fees": [],
    "cleaning_fee": 280.0,
    "promo": null,
    "promotional_price": {
      "previous_total_price": 1294,      // DE
      "previous_night_price": 258.8,     // DE
      "promo_total_price": 1099,         // POR (valor atual do imóvel)
      "promo_night_price": 219.8,        // POR
      "discount_percent": 15,            // do índice promotions
      "discount_value": 195              // previous_total_price - promo_total_price
    },
    "installments": [
        {
            "quantity": 1.0,
            "value": 1099.0,
            "total_value": 1099.0
        },
        {
            "quantity": 2.0,
            "value": 559.88,
            "total_value": 1119.77
        },
        ...
    ],
    "pix": {
        "total_value": 1058.05,
        "discount": 40.95,
        "promo_info": {
            "name": "fallback5",
            "type": "percent",
            "value": 5
        },
        "message": "discount_applied"
    }
}
```


### **PUT** tasks/sync/promotions?promo_id={name_slug} ==(new)==

Endpoint responsável pelo sync manual de uma promoção, a ideia é usá-lo em casos de falha. Ele acionará a task `index_promotion` descrita na seção abaixo. O endpoint em si já existe, só será preciso ajustar para que seja possóvel acionar a `index_promotion` a partir dele,


## Worker Chains & Tasks

Seção responsável por detalhar as novas chains e tasks que serão adicionadas ao worker.

### index_promotion(promo_id)

Indexa a criação e/ou atualização de uma promoção que foi persistida no BD.

Ao final da execução dessa task, deve ser disparada a task `index_property_promotions` **caso tenha tido alteração nos imóveis participantes da promoção ou no status da promoção**

### **index_properties_promotions(prop_id, promo_id)**

Cria/atualiza o índice de propriedades no OpenSearch adicionando ou sincronizando o campo `promotions`, que armazena a lista de IDs das promoções associadas a cada imóvel. Esse campo reflete as promoções do índice `promotions`, garantindo que cada propriedade saiba a quais promoções está vinculada.

> **Ideia** :bulb:: Executar essa task apenas se tiver tido alteração de imóvel ou de status da promoção. Caso contrário, não é necessário executar essa task.

### remove_inactive_property_promotions

Executa diariamente às 00h UTC-3 para procurar e desativar promoções cujo período expirou, garantindo que não sejam mais consideradas ativas nem exibidas no site.

Essa task irá executar a `index_promotions` ao final dela, para persistir no opensearch a atualização daquela promoção.


# Diagrama

[https://miro.com/app/board/uXjVN47euTs=/?moveToWidget=3458764645039301004&cot=14](https://miro.com/app/board/uXjVN47euTs=/?moveToWidget=3458764645039301004&cot=14)

# Tarefas & Prazos (TBD)

- [ ] História 1:
  - [ ] Task 1:
  - [ ] Task 2:
- [ ] História 2:


# **Implementações Futuras**

* Módulo de promoções: I. Ser possível criar campanhas promocionais no site & II. Cupons.
* Limitação de uso de cupom em conjunto com promoção (combo preço promocional + cupom)\n*Possibilitar o "não uso" de cupons caso o imóvel já tenha uma promoção ativa. ex.: "Não foi possível aplicar o cupom. Uma promoção melhor está ativa"*