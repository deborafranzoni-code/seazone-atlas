<!-- title: Orçamento de Diárias | url: https://outline.seazone.com.br/doc/orcamento-de-diarias-3OQWoKAbgz | area: Tecnologia -->

# Orçamento de Diárias

### API

> **Fonte dos preços das diárias dos imóveis:** ~~Tabela no BD~~ → API que [puxa da stays](https://github.com/Khanto-Tecnologia/sapron-pms-web/pull/1265) o preço das diárias.

API com o método GET que traz as informações do orçamento de diárias.

**Input:** check_in, check_out, property\[lista de imoveis\], Filtro (codigo do imóvel)

**Output:** para cada propriedade:

```json
{
 property 1: {
    Info do imóvel: [
       code
       Address [ ]
       guest_capacity
       cleaning_fee
       cover_image
    ]
    Nº noites
    Valor por noite
    Valor total
 }
 property 2: {...}
}
```

* No **Input**:
  * Receberá um range de data (check_in e check_out) e poderá ser fornecido uma ou mas propriedades para o cálculo do orçamento.
  * Haverá também um filtro para pesquisa pelo código do imóvel. **OBS:** Deverá aceitar matchs parciais.
* No **Output:**
  * **Nº noites**: `check_out - check_out`
  * **Valor por noite (média)**: (soma das diárias do **check_in** ao **checkout-1**)/nº noites
  * **Cleaning_fee**: Puxar da tabela **property_property**
  * **Valor total**: (soma das diárias do **check_in** ao **(check_out-1)**) + cleaning_fee

### Interface

**Protótipo:**

[Novas telas](https://www.figma.com/proto/GHkVrNqbgLadmeRQ6SgwAw/Novas-telas?node-id=157%3A6692&scaling=scale-down-width&page-id=0%3A1&starting-point-node-id=157%3A5111&show-proto-sidebar=1)

* Modal de orçamento é aberto ao selecionar o período em um imóvel no Multicalendar
* *Texto para "Copiar Informações do Orçamento":*

  > Olá {primeiro nome do hóspede} tudo bem? Sou o/a {nome atendente} e serei responsável pelo seu atendimento. Como solicitado, este é o orçamento e as possibilidades de locação para o período de {data_inicio} até {data_fim}:
  >
  > > {categoria}{listagem de imóveis selecionados da mesma categoria}Valor total: R$ {valor da reserva para o período selecionado, para esta categoria}
  >
  > Estou à disposição para qualquer esclarecimento que se fizer necessário. Esperamos concretizar a sua reserva em breve 😁

### **Integração com API**

* O front deverá enviar o GET na API informando o imóvel e o período selecionado no Multicalendar para obter as informações do imóvel e do orçamento.
* Ao clicar em **"Aplicar desconto"**, o botão deverá ficar indisponível e aplicar 5% de desconto no valor Total do orçamento.
* Ao clicar em **"Adicionar imóvel",** o campo de busca deverá ser integrado com a API, e ao dar Enter:
  * Realizar a requisição na API
  * Carregar um novo Card com as informações de orçamento daquela propriedade adicionada.
* Ao adicionar novas propriedades, o campo **"Total do orçamento"** deve ser incrementado somando o **"Valor total"** do orçamento de cada propriedade.

  
---
* Ao clicar em **"Concluir"**, deverá ser aberto o modal de **"Criar reserva"**, já carregando as informações preenchidas no orçamento:**Deverá vir já selecionado os campos:**
  * Imóvel(s)
  * Datas selecionadas (De ... Até ...)
  * Valor total = Valor total do orçamento
  * Adultos = Valor selecionado onde há "Até X hóspedes ..."