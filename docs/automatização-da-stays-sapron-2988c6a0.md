<!-- title: Automatização da Stays Sapron | url: https://outline.seazone.com.br/doc/automatizacao-da-stays-sapron-e5CJqyBHR1 | area: Tecnologia -->

# Automatização da Stays Sapron

# Documentações

API Stays: <https://stays.net/external-api/#introduction>

API Pleno: <https://documenter.getpostman.com/view/7403048/UVXdPeYB>

[Fluxo de dados Website>Stays>Sapron](/doc/fluxo-de-dados-websitestayssapron-vaovzogXkq)

Organização Migração por fases(Produto): 

[https://miro.com/app/board/uXjVIR6fDkk=/](https://miro.com/app/board/uXjVIR6fDkk=/)


# Stays

Na documentação da API da Stays.net, a criação de anúncios (listings) é realizada através do endpoint 

```javascript
POST /content/listings
```

Por padrão, os anúncios criados por meio desse endpoint são definidos com o status "draft" (rascunho). Isso significa que, ao criar um anúncio utilizando esse endpoint, ele será inicialmente salvo como rascunho. Posteriormente, podemos modificar o status do anúncio para "active" (ativo) ou outro status conforme necessário, utilizando o endpoint 

```javascript
PUT /content/listings/{id}
```


**\[validar\]** se existeuma tabela que registre os anúncios criados por meio da API da Stays.net,  podemos incluir as seguintes colunas essenciais:

* **ID Interno (_id)**: Identificador único do anúncio.​
* **Nome Interno (internalName)**: Nome interno atribuído ao anúncio.​
* **Título (_mstitle)**: Título comercial do anúncio.​
* **Status (status)**: Estado atual do anúncio (por exemplo, "draft", "active").​
* **Endereço (address)**: Localização do imóvel, incluindo rua, número, cidade e estado.​
* **Coordenadas Geográficas (latLng)**: Latitude e longitude do imóvel.​
* **Data de Criação**: Data em que o anúncio foi criado.​

Estruturada:

| ID Interno | Nome Interno | Título | Status | Endereço | Coordenadas Geográficas | Data de Criação |
|----|----|----|----|----|----|----|
| 5f896e2165394ecf5ddcfb97 | API Listing 001 | Apartamento Maravilhoso | Draft | Alameda Rio Negro, 584, Barueri, SP | Lat: -23.5007271, Lng: -46.8479001 | 08/04/2025 17:15:19 |

Essa estrutura permitirá um acompanhamento eficaz dos anúncios criados, facilitando a gestão e monitoramento de cada um.​


Para sincronizar as comodidades (amenities) de um imóvel entre o sistema Pleno e o Stays.net,  podemos utilizar os seguintes endpoints da API do Stays.net:​


1. **Obter a lista de comodidades disponíveis no Stays.net**: Utilize o endpoint GET /external/v1/translation/property-amenities para recuperar todas as comodidades disponíveis no Stays.net. Cada comodidade possui um identificador único (_id) que será necessário para a sincronização. ​[Stays](https://stays.net/external-api/?utm_source=chatgpt.com)
2. **Atualizar as comodidades do imóvel no Stays.net**: Após mapear as comodidades do Pleno com as do Stays.net, utilize o endpoint PATCH /external/v1/content/properties/{propertyId} para atualizar as comodidades do imóvel específico no Stays.net. No corpo da requisição, incluir a lista de comodidades correspondentes utilizando os _id obtidos anteriormente. ​[Stays](https://stays.net/external-api/?utm_source=chatgpt.com)

**\[Atenção\]** Precisamos ter certeza de que as comodidades no Pleno estejam devidamente mapeadas para as correspondentes no Stays.net, garantindo uma sincronização precisa entre os sistemas.​


# **Pleno**

Para sincronizar as comodidades (amenities) de um imóvel utilizando a API da Pleno Vistorias:​

**Endpoint:**

* **PUT /api/v1/imoveis/{id}/comodidades**: Este endpoint permite atualizar as comodidades de um imóvel específico, identificado pelo {id}.​

**Procedimento:**


1. **Recuperar as Comodidades Disponíveis**: Primeiro, obtenha a lista de comodidades disponíveis no sistema da Pleno para assegurar que os IDs correspondam corretamente.​
2. **Mapear as Comodidades**: Compare as comodidades entre os sistemas da Pleno e do Stays.net para garantir que cada comodidade no Stays.net tenha uma correspondente na Pleno.​
3. **Atualizar as Comodidades do Imóvel**: Utilize o endpoint PUT /api/v1/imoveis/{id}/comodidades para atualizar as comodidades do imóvel na Pleno. No corpo da requisição, inclua a lista de IDs das comodidades que deseja associar ao imóvel.​

**Exemplo de Requisição:**

```javascript
PUT /api/v1/imoveis/{id}/comodidades
Content-Type: application/json
Authorization: Bearer {seu_token_de_acesso}

{
  "comodidades": [
    "id_comodidade_1",
    "id_comodidade_2",
    "id_comodidade_3"
  ]
}
```


**Observações:**

* **Autenticação**: Certifique-se de incluir um token de acesso válido no cabeçalho Authorization para autenticar a requisição.​
* **Consistência de Dados**: Garanta que os IDs das comodidades enviados na requisição correspondam aos IDs existentes no sistema da Pleno para evitar erros.​
* **Documentação**: Para mais detalhes e possíveis atualizações, consulte a [documentação oficial da API da Pleno Vistorias](https://documenter.getpostman.com/view/7403048/UVXdPeYB#intro).​