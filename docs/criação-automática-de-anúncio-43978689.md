<!-- title: Criação automática de anúncio | url: https://outline.seazone.com.br/doc/criacao-automatica-de-anuncio-yCDAi3lIB9 | area: Tecnologia -->

# Criação automática de anúncio

# PRD – Automação de Criação de Anúncios (PLENO → STAYS)

## 1. Visão Geral

Atualmente, a criação de anúncios de imóveis é um processo majoritariamente manual, envolvendo:

* Consulta à vistoria na PLENO
* Preenchimento de dados na STAYS
* Inclusão de amenities, cômodos, imagens e regras
* Criação de conteúdo multilíngue
* Atualização de status no Pipefy

Este PRD descreve a automação completa desse fluxo por meio de integrações via API, garantindo:

* Redução de esforço operacional
* Padronização de anúncios
* Menos erros manuais
* Escalabilidade


---

## 2. Objetivo

Automatizar a criação e configuração de anúncios na STAYS utilizando dados de vistoria da PLENO, desde o momento em que o card entra no Backlog até o anúncio estar pronto para revisão final.


---

## 3. Escopo

### Dentro do escopo

* Integração com API da PLENO (vistoria)
* Integração com API da STAYS (criação e atualização)
* Preenchimento automático de:
  * Localização
  * Cômodos
  * Amenities
  * Regras
  * Conteúdo multilíngue
* Atualização de status no Pipefy
* Associação de imagens aos cômodos


---

## 4. Gatilho do Processo

O fluxo inicia quando um card é movido para:

**\[IMP\] PIPE 5 – Criação de Anúncios → Coluna: Backlog**


---

## 5. Fluxo Geral


1. Ler o **código do imóvel** no Pipefy
2. Buscar a vistoria na PLENO via API
3. Criar anúncio na STAYS em **status RASCUNHO**
4. Preencher automaticamente:
   * Tipo de imóvel
   * Localização
   * Amenities
   * Cômodos
   * Regras
   * Conteúdo multilíngue
5. Mover card para **REVISÃO INICIAL**
6. Se houver a tag **COLOCAR FOTOS PROFISSIONAIS**:
   * Associar fotos aos cômodos
   * Mover para **REVISÃO FINAL**


---

## 5. Regras de Negócio de Criação do Anúncio na STAYS

### 5.1 Tipo de Propriedade

Campos fixos:

| Campo | Valor |
|----|----|
| Tipo de propriedade | APARTAMENTO |
| Tipo de anúncio | APARTAMENTO |
| Subtipo | IMÓVEL INTEIRO |
| Categoria | ALUGUEL POR TEMPORADA |


---

### 5.2 Localização

* Verificar se o condomínio já existe na Seazone na categoria **Prédio**.
* Caso não exista:
  * Criar novo endereço com base no campo **ENDEREÇO** da PLENO.
* Sempre marcar:
  * Exibição global do número do prédio nos anúncios.


---

### 5.3 Amenities de Endereço

Regras de mapeamento:

| Condição na PLENO | Ação na STAYS |
|----|----|
| Self check-in = SIM | Marcar check-in e checkout expresso |
| Garagem gratuita = SIM | Marcar estacionamento gratuito, garagem no local, sem necessidade de reserva, taxa grátis |
| Sempre | Internet a cabo = NÃO |
| Sempre | Wi-Fi = SIM, em todas as acomodações, cobrança = grátis |

Cozinha e sala de jantar:

* Não oferece café da manhã
* Não possui restaurante

Lavanderia:

* Se a PLENO indicar máquina lava e seca:
  * Marcar **LAVADORA** e **SECADORA** (não existe campo único na STAYS)

Serviços:

* Não oferece babá
* Não oferece concierge
* Não oferece massagem
* Não possui spa
* Funcionários seguem protocolos legais de segurança

Outros amenities:

* Preencher conforme dados da vistoria da PLENO.


---

### 5.4 Cômodos

* Criar cômodos conforme a quantidade de ambientes na vistoria da PLENO.
* Para todos:
  * **O cômodo é compartilhado = NÃO**
* Quantidade de camas:
  * Definida com base na vistoria da PLENO.


---

### 5.5 Amenities do Anúncio

Garagem:

* Preencher conforme PLENO.
* Informar quantidade de carros.

Itens de banheiro (sempre marcar):

* Água quente
* Ducha
* Itens básicos de banheiro
* Papel higiênico
* Sabonete de corpo
* Secador de cabelo
* Toalhas
* Xampu

Internet e escritório:

* Internet
* Wi-Fi

Limpeza:

* Lixeiras

Demais itens:

* Conforme vistoria da PLENO.


---

## 6. Conteúdo Descritivo

Todos os campos devem ser preenchidos em:

* Inglês
* Português (BR)
* Espanhol

### 6.1 Campos

| Campo | Regra |
|----|----|
| Nome interno | Código do imóvel na Seazone |
| Título do anúncio | Gerado via prompt |
| Descrição resumida | Gerada via prompt |
| Notas gerais | Regras da aba "Descrição Fase 2" |
| Sobre o espaço | Texto padrão da Planilha 02 |
| Acesso ao espaço | Texto padrão da Planilha 02 |
| Interação com anfitrião | Texto padrão da Planilha 02 |
| Descrição do bairro | Planilha 02 ou prompt |
| Locomoção | Planilha 02 ou prompt |

As regras de "Notas gerais" devem considerar:

* Aceita pet
* Self check-in


---

## 7. Regras da Acomodação

| Regra | Valor |
|----|----|
| Máx. adultos | Definido pela vistoria + camas |
| Idade mínima | 18 anos |
| Crianças e bebês | Total de pessoas – 1 |
| Fumar | Não permitido |
| Pets | Verificar vistoria, pode haver cobrança |
| Eventos | Não permitido |
| Silêncio | 22h às 07h |
| Regras adicionais | Repetir "Notas gerais" |


\

---

## 6. Integração com a PLENO

### 6.1 Autenticação

`POST /api/vistoria/usuario/login `

Payload:

`{   "usu_email": "...",   "usu_senha": "...",   "sis_codigo": "3",   "host": "seazone.sistemaspleno.com" } `

Resposta:

`{   "success": true,   "data": {     "auth_token": "..."   } } `

Header:

`Authorization: Basic {auth_token} `


---

### 6.2 Busca da vistoria


1. Buscar pelo código do imóvel:

`GET /api/vistoria/vistoria?term={codigoImovel} `


2. Buscar detalhes completos:

`GET /api/vistoria/vistoria/{vis_codigo}/show `


---

### 6.3 Estrutura de dados utilizada

Campos confirmados na PLENO:

| Categoria | Campo |
|----|----|
| Endereço | `imovel.imo_endereco_completo_formatado` |
| Bairro | `imovel.bairro.bai_nome` |
| Cidade | `imovel.cidade.cid_nome` |
| Estado | `imovel.uf.uf_nome` |
| Geo | `imovel.imo_geolocalizacao` |
| Ambientes | `ambientes` |
| Tipo ambiente | `tipo_ambiente.tip_amb_descricao` |
| Referência | `amb_referencia` |
| Itens | `ambientes_itens` |
| Tipo item | `tipo_ambiente_item.tip_amb_ite_descricao` |
| Quantidade | `amb_ite_quantidade` |

Esses campos alimentam:

* Localização
* Cômodos
* Camas
* Amenities
* Descrições


---

## 7. Estrutura do Anúncio na STAYS

### 7.1 Identificação

| Campo STAYS | Uso |
|----|----|
| `_id` | Identificador |
| `_idproperty` | Imóvel |
| `_idpropertyType` | Tipo |
| `_idtype` | Tipo de anúncio |
| `subtype` | Subtipo |
| `status` | DRAFT |
| `internalName` | Código do imóvel |


---

### 7.2 Tipos fixos

| Campo | Valor |
|----|----|
| Tipo de propriedade | APARTAMENTO |
| Tipo de anúncio | APARTAMENTO |
| Subtipo | IMÓVEL INTEIRO |
| Categoria | ALUGUEL POR TEMPORADA |


---

### 7.3 Localização

Campos:

* `address`
* `latLng`
* `listingCategories`

Regras:

* Verificar se o condomínio já existe como **Prédio**
* Caso não exista, criar novo endereço
* Sempre exibir número do prédio globalmente

Mapeamento:

| PLENO | STAYS |
|----|----|
| Endereço formatado | address |
| Bairro | address.neighborhood |
| Cidade | address.city |
| UF | address.state |
| Geo | latLng |


---

## 8. Cômodos

* Criar cômodos conforme `ambientes` da PLENO
* Todos os cômodos:
  * Compartilhado = NÃO
* Quantidade de camas:
  * Derivada dos itens "Cama"

Campos usados:

* `_i_rooms`
* `_i_beds`
* `images`


---

## 9. Amenities

A STAYS possui dois tipos:

| Tipo | Campo |
|----|----|
| Estrutura | `propertyAmenities` |
| Unidade | `amenities` |

### 9.1 Atualização via API

`PATCH /external/v1/content/listings/{listingId} `

Exemplo:

`{   "amenities": [{ "_id": "123" }] } `

`{   "propertyAmenities": [{ "_id": "456" }] } `


---

### 9.2 Regras de negócio

**Internet**

* Wi-Fi = SIM (amenities)
* Internet a cabo = NÃO

**Check-in**

* Se PLENO indicar self check-in:
  * propertyAmenities: Check-in expresso

**Garagem**

* Se gratuita:
  * propertyAmenities: estacionamento gratuito
  * Sem reserva
  * Taxa grátis

**Cozinha**

* Não oferece café da manhã
* Não possui restaurante

**Lavanderia**

* Lava e seca = marcar:
  * Lavadora
  * Secadora

**Serviços**

* Sem babá
* Sem concierge
* Sem massagem
* Sem spa
* Protocolos de segurança ativos

**Banheiro (sempre marcar)**

* Água quente
* Ducha
* Itens básicos
* Papel higiênico
* Sabonete
* Secador
* Toalhas
* Xampu

**Limpeza**

* Lixeiras

Outros itens:

* Conforme vistoria PLENO


---

## 10. Conteúdo Multilíngue

### 10.1 Campos suportados

| Campo STAYS | Finalidade |
|----|----|
| `_mstitle` | Título |
| `_mssummary` | Resumo |
| `_msnotes` | Notas |
| `_msspace` | Espaço |
| `_msaccess` | Acesso |
| `_msinteraction` | Interação |
| `_msneighborhood_overview` | Bairro |
| `_mstransit` | Locomoção |
| `_mshouserules` | Regras |

Formato:

`{   "pt_BR": "...",   "en_US": "...",   "es_ES": "..." } `

### 10.2 Regras de preenchimento

| Campo | Regra |
|----|----|
| Nome interno | Código do imóvel |
| Título | Gerado por prompt |
| Resumo | Gerado por prompt |
| Notas | Regras Fase 2 |
| Espaço | Texto padrão |
| Acesso | Texto padrão |
| Interação | Texto padrão |
| Bairro | Planilha 02 ou prompt |
| Locomoção | Planilha 02 ou prompt |

HTML permitido:

* `<b>`
* `<br>`


---

## 11. Regras da Acomodação

| Regra | Valor |
|----|----|
| Máx. adultos | Vistoria + camas |
| Idade mínima | 18 |
| Crianças/bebês | Total - 1 |
| Fumar | Proibido |
| Pets | Verificar PLENO (com cobrança) |
| Eventos | Proibidos |
| Silêncio | 22h às 07h |
| Regras adicionais | Repetir notas |


---

## 12. Integração com a STAYS

### 12.1 Autenticação

`Authorization: Basic base64(username:password) `

### 12.2 Atualização de conteúdo

`PATCH /external/v1/content/listings/{listingId} `

Usado para:

* Conteúdo multilíngue
* Amenities
* PropertyAmenities


\
[LISTA DE TODAS AS AMENITIES DA STAYS](https://docs.google.com/spreadsheets/d/1fhmp43v6gby7NuIjXRdgqc6Z-nQIz-i7GVqFEFe6zlU/edit?gid=1762280093#gid=1762280093)


### Ordem das fotos na Stays no padrão de casa/apto:


 1. Principais
 2. Sala/Área Comum
 3. sacada
 4. cozinha
 5. varanda
 6. Suíte
 7. Quartos (Individual, Duplo, Triplo, Quádruplo e Com 2 camas de solteiro)
 8. Banheiro
 9. 1/2 Banheiro
10. área de serviço

Ordem das fotos na Stays no padrão de estúdio:


1. Principais
2. Estúdio
3. Sacada
4. cozinha
5. varanda
6. Banheiro
7. 1/2 Banheiro