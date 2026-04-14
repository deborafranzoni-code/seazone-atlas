<!-- title: BI CS RM | url: https://outline.seazone.com.br/doc/bi-cs-rm-sX8zU3xe86 | area: Tecnologia -->

# BI CS RM

# Documentação Usuário:

* Aba Imóvel/Categoria

  ![Untitled](/api/attachments.redirect?id=ea30579f-0647-45d6-8720-579c175a0623)

  Esta aba é útil para comparar preço e ocupação de um imóvel Seazone com outros imóveis Seazone dentro da categoria. Do lado esquerdo temos as métricas do imóvel Seazone filtrado por mês e do lado direito uma média do desempenho dos listings seazone da mesma categoria por mês. É possível também visualizar um ranking de preço e ocupação dos listings seazone da mesma categoria selecionando "Ranking", no lugar de "Desempenho Médio Categoria".

  Importante ressaltar que tantos os cards do meio de Preço Médio e Ocupação do imóvel e da categoria quanto a tabela de ranking são relativos às datas filtradas pelo filtro de Data.
* Aba Imóvel/Concorrentes

  ![Untitled](/api/attachments.redirect?id=c27bd9c9-17d2-4035-b5f0-50bc06e8a243)

  Esta aba é útil para comparar preço e ocupação de um imóvel seazone com seus respectivos concorrentes. Do lado esquerdo temos as métricas do imóvel seazone filtrado por mês e do lado direito uma média do desempenho dos listings concorrentes por mês. É possível também visualizar um ranking de preço e ocupação dos listings concorrentes selecionando "Ranking", no lugar de "Desempenho Médio Concorrentes". Neste tabela de ranqueamento é possível clicar no código do listing Airbnb para abrir a página do anúncio.

  Importante ressaltar que tantos os cards do meio de Preço Médio e Ocupação do imóvel e dos concorrentes quanto a tabela de ranking são relativos às datas filtradas pelo filtro de data.
* Aba Reservas

  ![Untitled](/api/attachments.redirect?id=01ec3fec-4c60-43fb-aba1-ce6999cd3377)

  Aqui é possível ver as reservas de um imóvel e a comparação de algumas métricas com a média de sua categoria. Os cards de antecedência média e valor médio de diária são relativos às datas filtradas pelo filtro de data, sendo que a data filtrada para cálculo de antecedência é a data de Check-In.

  Exemplo da imagem: A antecedência média do imóvel para os últimos 7 dias é 8 pois existem 3 reservas com checkin entre 02/12 e 8/12 e a média de antecedência delas é

  $(10 + 5 + 8)/3 = 7.7$  , que arredondando dá 8.
* Aba Calendário

  ![Untitled](/api/attachments.redirect?id=97965246-7b3a-4a01-bc78-7350fd01e321)

  Esta aba é útil para ter uma visibilidade diária do calendário de um imóvel e/ou categoria. Dias em azul são dias alugados, em marrom são dias bloqueados e brancos/cinzas são dias disponíveis. Os dias em cinza são as sextas e sábados disponíveis. É possível filtrar por Categoria e Imóvel. No futuro queremos trazer valores de Faturamento bruto e líquido quando ligarmos esse dashboard aos dados do Sapron.

o antes da reserva acontecer. O Preço Médio Ofertado só leva em conta datas **não bloqueadas**(dias disponíveis). Se houver algum Preço Médio Ofertado nulo, significa que naquele contexto não há datas disponíveis para o determinado listing/categoria/concorrente.

* Dias Disponíveis: Dias não bloqueados.
  * Ou seja, (dias disponíveis) = (todos os dias) - (dias bloqueados)
* Concorrentes General e Plus:
  * Concorrentes General são imóveis dentro de uma mesma localização, tipo de anúncio(hotel, apartamento ou casa), número de quartos e strata.
  * Concorrentes Plus são os concorrentes general com alguns filtros de qualidade do anúncio, como número de reviews, nota do anúncio, superhost e número de noites vendidas nos últimos 30 dias.

  <aside> 💡 Atualmente a maioria dos concorrentes General vai ser igual aos concorrentes Plus pois estamos passando por uma modificação no processo de seleção de concorrentes, mas no futuro funcionará como mencionado acima.

  </aside>

### FAQ:

# Documentação Técnica: