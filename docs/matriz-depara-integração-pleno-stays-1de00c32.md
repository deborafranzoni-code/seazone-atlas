<!-- title: Matriz De/Para – Integração PLENO → STAYS | url: https://outline.seazone.com.br/doc/matriz-depara-integracao-pleno-stays-xm2fSfMfxq | area: Tecnologia -->

# Matriz De/Para – Integração PLENO → STAYS

## 1. Identificação do Imóvel

| PLENO | STAYS | Tipo | Regra |
|----|----|----|----|
| Código do imóvel (Pipefy / planilha) | `internalName` | string | Usar como nome interno do anúncio |


---

## 2. Tipo de Propriedade / Categoria

| STAYS | Valor Fixo |
|----|----|
| `_idpropertyType` | APARTAMENTO |
| `_idtype` | APARTAMENTO |
| `subtype` | IMÓVEL INTEIRO |
| `listingCategories` | ALUGUEL POR TEMPORADA |

> Não depende da PLENO – regra de negócio fixa.


---

## 3. Localização

| PLENO | STAYS | Tipo | Observação |
|----|----|----|----|
| `imovel.imo_endereco_completo_formatado` | `address` | string | Endereço completo |
| `imovel.bairro.bai_nome` | `address.neighborhood` | string | Bairro |
| `imovel.cidade.cid_nome` | `address.city` | string | Cidade |
| `imovel.uf.uf_nome` | `address.state` | string | Estado |
| `imovel.imo_geolocalizacao[0]` | `latLng.lat` | number | Latitude |
| `imovel.imo_geolocalizacao[1]` | `latLng.lng` | number | Longitude |


---

## 4. Cômodos (Ambientes)

| PLENO | STAYS | Tipo | Regra |
|----|----|----|----|
| `ambientes` | `_i_rooms` | number | Quantidade de ambientes |
| `tipo_ambiente.tip_amb_descricao` | Nome do cômodo | string | Ex: Quarto, Sala |
| `amb_referencia` | Identificador | string | Diferencia cômodos iguais |
| Todos os ambientes | Compartilhado = NÃO | boolean | Regra fixa |


---

## 5. Camas

| PLENO | STAYS | Tipo | Regra |
|----|----|----|----|
| Item: `Cama` + `amb_ite_quantidade` | `_i_beds` | number | Soma total de camas |
| Tipo da cama | Room details | string | Ex: Queen, Solteiro |


---

## 6. Capacidade

| PLENO | STAYS | Tipo | Regra |
|----|----|----|----|
| Quantidade de camas | `_i_maxGuests` | number | Definido por regra de negócio |


---

## 7. Amenities do Endereço (propertyAmenities)

Atualizados via:

`{ "propertyAmenities": [{ "_id": "ID" }] } `

| PLENO / Regra | STAYS | Observação |
|----|----|----|
| Self check-in = SIM | propertyAmenities | Check-in expresso |
| Garagem gratuita = SIM | propertyAmenities | Estacionamento gratuito |
| Garagem no local | propertyAmenities | Sem reserva |
| Taxa de estacionamento | propertyAmenities | Grátis |
| Funcionários seguem protocolos | propertyAmenities | Segurança |
| Não oferece concierge | propertyAmenities | Serviço indisponível |
| Não oferece babá | propertyAmenities | Serviço indisponível |
| Não oferece massagem | propertyAmenities | Serviço indisponível |
| Não possui spa | propertyAmenities | Serviço indisponível |

> IDs vêm da tabela oficial da STAYS.


---

## 8. Amenities do Anúncio (amenities)

Atualizados via:

`{ "amenities": [{ "_id": "ID" }] } `

### Banheiro (sempre marcar)

| Item | STAYS |
|----|----|
| Água quente | amenities |
| Ducha | amenities |
| Itens básicos | amenities |
| Papel higiênico | amenities |
| Sabonete | amenities |
| Secador | amenities |
| Toalhas | amenities |
| Xampu | amenities |

### Internet

| Regra | STAYS |
|----|----|
| Wi-Fi = SIM | amenities |
| Internet a cabo = NÃO | Não incluir |

### Limpeza

| Item | STAYS |
|----|----|
| Lixeiras | amenities |

### Lavanderia

| PLENO | STAYS |
|----|----|
| Lava e seca | Lavadora + Secadora |

### Cozinha / Sala

| Regra | STAYS |
|----|----|
| Não oferece café da manhã | amenities |
| Não possui restaurante | amenities |

### Itens por ambiente

| PLENO | STAYS |
|----|----|
| Televisão | amenities |
| Fogão / Cooktop | amenities |
| Sofá | amenities |


---

## 9. Imagens

| PLENO | STAYS | Regra |
|----|----|----|
| Ambientes | `images` | Associar por cômodo |
| Fotos profissionais | `_idmainImage` | Definir principal |


---

## 10. Regras da Acomodação

| Regra | STAYS |
|----|----|
| Idade mínima = 18 | `_mshouserules` |
| Crianças/bebês = total - 1 | `_mshouserules` |
| Não fumar | `_mshouserules` |
| Pets (com cobrança) | `_mshouserules` |
| Eventos proibidos | `_mshouserules` |
| Silêncio 22h–07h | `_mshouserules` |
| Regras adicionais | `_msnotes` |


---

## 11. Autenticação e Endpoints

### PLENO

| Ação | Endpoint |
|----|----|
| Login | `POST /api/vistoria/usuario/login` |
| Buscar vistoria | `GET /api/vistoria/vistoria?term=` |
| Detalhe | `GET /api/vistoria/vistoria/{id}/show` |

### STAYS

| Ação | Endpoint |
|----|----|
| Atualizar conteúdo | `PATCH /external/v1/content/listings/{id}` |
| Atualizar amenities | Mesmo endpoint |
| Atualizar propertyAmenities | Mesmo endpoint |