<!-- title: Guia Interno: Funcionamento do Agrupamento de Comodidades | url: https://outline.seazone.com.br/doc/guia-interno-funcionamento-do-agrupamento-de-comodidades-9XN7Cb1XoO | area: Tecnologia -->

# Guia Interno: Funcionamento do Agrupamento de Comodidades

# Objetivo

Este documento tem como objetivo explicar como está estruturado atualmente o agrupamento de comodidades do site de reservas.

# Contexto

O agrupamento de comodidades foi idealizado para simplificar o filtro de comodidades disponível hoje no website. Como as informações de comodidades (amentieies) vem da stays, havia esse problema que, na hora de filtrar, eram exibidas muitas opções de filtros que, às vezes eram redundantes por serem específicas demais, por exemplo, existia "academia" e "academia ao ar livre". Isso poderia dificultar a experiência do usuário, sendo assim foram definidos certos grupos de comodidades, e nosso filtro se tornou menos poluído.

 ![Opções de filtro de comodidade atualmente](/api/attachments.redirect?id=358b0756-ea23-4854-b2ae-24c19a761696)

# Implementação

Os grupos de comodidades foram definidos manualmente e podem ser encontrados no documento [Filtro de Comodidade](/doc/filtro-de-comodidade-PvDy0XZ42L).

Com esses grupos definidos, foi necessário pensar em como associar os imóveis com os determinados grupos, para entender melhor esse processo é necessário falar um pouco sobre o processo de indexação dos imóveis.

## Comodidades

As comodidades dos imóveis são definidas diretamente na Stays. Do nosso lado, apenas armazenamos essas informações e mantemos o vínculo delas com as propriedades no nosso banco de dados. As comodidades chegam da API da Stays como texto (por exemplo, *"Air Condition")*. Para padronizá-las, aplicamos um tratamento que remove espaços e uniformiza o formato, resultando em algo como *"aircondition".*

## Indexação dos imóveis

Atualmente, utilizamos a Stays como nosso oráculo. Novos imóveis são cadastrados lá, e o site consome suas informações via API para registrá-los em nosso banco de dados e no OpenSearch. O processo de indexação dos imóveis ocorre diariamente, no worker, às 00h (UTC), contemplando todos os imóveis da Seazone. Durante essa rotina, atualizamos dados como: nome da propriedade, status, capacidade de hóspedes, comodidades, associação a destinos, informações de disponibilidade, entre outros. Foi nesse fluxo que incluímos a categorização das comodidades agrupadas.

## Categorização de Comodidades Agrupadas

Com os grupos definidos, foi necessário apenas incluir uma nova etapa no processo de indexação dos imóveis: verificar as comodidades de cada propriedade e identificar a quais grupos de comodidades ela deveria estar associada.

No OpenSearch, criamos o campo `grouped_amenities`, que armazena uma lista com os grupos de comodidades presentes em cada imóvel, a partir de suas comodidades originais. Por exemplo, se um imóvel possui a comodidade "Academia área comum" (gymshared) ou "Academia privativa" (gymprivate), o agrupamento resultante será a comodidade agrupada "academia".

A lógica de distribuição e associação foi implementada de forma simples: como já tínhamos a definição de quais comodidades pertencem a quais grupos, criamos um map em Python que relaciona cada comodidade ao seu respectivo grupo.

```python
grouped_amenities_map = {
  "gymshared": "academia",
  "gymprivate": "academia",
  "upperfloorre": "acessibilidade",
  "elevator": "acessibilidade",
  "groundflooru": "acessibilidade",
  "privateentra": "acessibilidade",
  "beachaccess": "acomodacao-com-vista",
  "beachview": "acomodacao-com-vista",
  "seaview": "acomodacao-com-vista",
  "oceanview": "acomodacao-com-vista",
  ...,
  }
```

Assim, a cada indexação de um imóvel, percorremos suas comodidades associadas para identificar, com base nelas, os grupos correspondentes. Esses grupos são então salvos na lista `grouped_amenities` dentro do OpenSearch. Dessa forma, substituimos as `amenities` dos filtros da busca pelo `grouped_amenities`.

Essa abordagem apresenta algumas limitações. A principal é que, quando surge uma nova comodidade que ainda não foi categorizada em nenhum agrupamento, ela se torna 'invisível' nos filtros. Isso acontece porque, ao não pertencer a nenhum grupo, não é possível acessá-la por meio da filtragem baseada em grupos.

A única medida adotada nesse caso foi implementar um alerta no Slack sempre que uma nova comodidade não agrupada fosse encontrada. A ideia era que, ao receber esse alerta, a pessoa de produto pudesse analisar a comodidade e definir a qual grupo ela deveria ser associada.

Apesar de funcional, essa estratégia é pouco prática, já que cada nova comodidade exige uma alteração no código. Ainda assim, essa decisão foi considerada aceitável porque o surgimento de novas comodidades não ocorre com frequência.