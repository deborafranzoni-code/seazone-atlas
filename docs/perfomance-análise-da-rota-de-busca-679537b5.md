<!-- title: Perfomance - Análise da Rota de Busca | url: https://outline.seazone.com.br/doc/perfomance-analise-da-rota-de-busca-dNHVi73g3I | area: Tecnologia -->

# 🔎 Perfomance | Análise da Rota de Busca

# **Análise da Implementação atual**

A busca é feita atualmente via OpenSearch, não tendo conexão com nenhuma API externa ou algo do tipo.

## Passo a passo do fluxo atual


1. **Recebimento dos parâmetros de busca**

   A rota recebe diversos parâmetros via query string, como destination_ids, datas, quantidade de hóspedes, filtros de amenities (comodidades), tipos de imóvel, localização, faixa de preço, ordenação, paginação, entre outros.
2. **Pré-processamento dos parâmetros**
   * Parâmetros que chegam como string separada por vírgula (destination_ids, amenities, grouped_amenities, property_types) são convertidos para listas.
   * O parâmetro location, se informado, é convertido para um objeto de localização (latitude, longitude, raio).
   * O número de adultos é ajustado para ser o maior valor entre o informado em adults e guests.
3. **Instanciação do mecanismo de busca**

   É criada uma instância de `AsyncPropertiesSearcher`, responsável por montar a query e consultar o mecanismo de busca (OpenSearch).
4. **Execução da busca**

   O método `.search()` é chamado, recebendo todos os parâmetros já processados.

   Internamente, ele:
   * Monta a query de busca considerando todos os filtros.
   * Executa a consulta no OpenSearch.
   * Formata e retorna os resultados paginados, podendo incluir sugestões de datas ou propriedades próximas, conforme parâmetros.
5. **Retorno dos resultados**

   A resposta traz a lista de propriedades encontradas, total de resultados e outras informações relevantes para a busca.

## Análise de Latência

O gráfico abaixo exibe, ao longo de 24 horas do dia 16/06/2025 (data em que registramos 1400 acessos), a média do tempo de resposta da rota `/properties/search`. Apesar de alguns picos isolados, o desempenho da rota se manteve dentro de um intervalo considerado aceitável, com tempos médios variando entre 222ms e 593ms.

 ![Fonte: https://grafana.seazone.com.br/d/fe9dmehxwu39cc/monitoramento-de-rotas-cluster?orgId=1&from=1750042800000&to=1750129199000&viewPanel=21](/api/attachments.redirect?id=936d5475-1368-4df7-b3bf-223df6686bab)


 ![](/api/attachments.redirect?id=a1491844-8488-4e83-b6ac-d0ed71e56f69 " =1905x856")

### Pior caso

O pior caso ocorre quando:

* **Nenhuma propriedade é encontrada** para os filtros informados, os parâmetros `date_from` e `date_to` estão presentes e o parâmetro `nearby_results=True` é utilizado.

**Por quê?**


1. **Primeira busca:**

   O sistema executa a busca principal no OpenSearch com todos os filtros (datas, localização, amenities, etc).
2. **Nenhum resultado:**

   Se não houver resultados e as datas foram informadas, o código tenta **ampliar o intervalo de datas** para pelo menos 7 dias e faz uma nova busca.
3. **Ainda sem resultados e** `nearby_results=True`:

   O sistema executa a função `_suggest_alternate_dates_for_location`, que:
   * Remove as datas do filtro e faz uma nova busca para tentar encontrar qualquer propriedade.
   * Se encontrar, faz uma nova busca por propriedades próximas usando a localização da primeira propriedade encontrada.
4. **Cada etapa faz uma nova consulta ao OpenSearch.**

**Exemplo**

 ![Trace: 4122a15a1a0ff4503fad05d2116b801](/api/attachments.redirect?id=bf107b66-47e0-4dd1-86d2-a5947530a656 " =1903x882")

### Melhor caso

O melhor cenário de performance para a rota ocorre quando:

* Os filtros são pouco restritivos (ex: apenas cidade ou destino, sem muitas amenities, tipos ou faixas de preço).
* Não há agregações solicitadas (`is_to_filter=False`).
* Não há busca por propriedades próximas (`nearby_results=False`).
* As datas não são informadas, ou, se informadas, retornam resultados logo na primeira consulta.

**Por quê?**

* Apenas **uma consulta simples** é feita ao OpenSearch, sem necessidade de buscas adicionais, sugestões de datas ou propriedades próximas.
* O volume de dados retornado é pequeno (pouca paginação, poucos resultados).
* Não há cálculos extras de agregação ou ordenação complexa.
* O processamento no Python é mínimo, apenas formatando os resultados.

**Exemplo**

 ![Trace: 45373e58a07a54aaee866ca52a56643b](/api/attachments.redirect?id=2b33fd22-5eac-483a-aa7e-4b0d15ba4c85 " =1903x882")

## Gargalos encontrados

### OpenSearch

Apesar da existência de alguns pré-processamentos de dados, o gargalo de lentidão parece ser o OpenSearch em si. Exemplo:

O trace abaixo se refere a seguinte consulta:

**GET** `/properties/search?destination_ids=27&is_to_filter=false&order=airbnb_conversion_v2&date_to=2025-07-06&date_from=2025-07-04&page=1&kids=0&adults=2&babies=0&page_size=18&nearby_results=true`

 ![Trace: ab4d1e794c9bd53e86a6299a786b9e34](/api/attachments.redirect?id=788fe332-47ed-43b5-a09d-7d5386313c7c " =1331x797")

Podemos observar que dos 500.29ms totais, 454.79ms são relacionados a consulta no OpenSearch. Dessa forma, podemos concluir que a consulta do OpenSearch representaria então **90%** do tempo gasto.

Para fins de teste, a mesma requisição realizada em ambiente local apresentou desempenho significativamente superior. O campo `extra_info` detalha o tempo (em ms) gasto em cada etapa, sendo `_search` referente à consulta no OpenSearch.

```json
{
  "timestamp": "2025-06-26 17:13:12,653",
  "level": "INFO",
  "message": "Performance Report [/properties/search]",
  "service": null,
  "extra_info": {
    "_search": 141.2875909882132,
    "_properties_response": 56.81676999665797
  },
  "method_name": "search",
  "file_name": "search.py",
  "logger_name": "api",
  "span_id": 0,
  "trace_id": 0
}
```

A disparidade de desempenho é significativa, possivelmente devido ao fato de que, no ambiente local, todos os serviços estão na mesma rede, enquanto em produção a infraestrutura está hospedada na AWS (oregon), o que pode introduzir maior latência na comunicação com o OpenSearch. Além disso, é possível que os recursos da máquina local sejam maiores do que os definidos na AWS, o que também influencia.

## Detalhes da Infraestrutura atual do OpenSearch

Atualmente, o OpenSearch não está alocado em uma máquina dedicada. Ele roda dentro de um **pod Kubernetes**, com recursos definidos via **limits** e **requests** configurados no próprio pod.

Esses limites determinam a quantidade máxima de **CPU** e **memória RAM** que o serviço pode utilizar. Caso o uso atinja 100% desses limites, o OpenSearch pode sofrer degradação de performance, o que pode explicar parte da lentidão observada na rota de busca de imóveis.

Os pods do OpenSearch estão divididos em dois tipos: masters (por exemplo, reservas-masters-0) e nodes (como reservas-nodes-0). Segundo o time de Governança, os masters são responsáveis pelas operações de escrita, enquanto os nodes se encarregam das leituras (sendo estes últimos os mais relevantes para a rota de busca de imóveis). Atualmente, tanto os masters quanto os nodes possuem os seguintes recursos alocados:

* **Memória**: 4 GiB
* **CPU**: 2000 millicores (equivalente a 2 CPUs)

# Conclusão

Embora a performance geral da rota esteja dentro do aceitável, a análise mostra que o **OpenSearch é o principal gargalo** atualmente. A partir disso, podemos pensar em algumas alternativas de melhorias:

## Cache

Infelizmente, o uso de cache não é viável. Experiências anteriores mostraram que isso pode causar inconsistências, como divergência de preços em relação à Stays e exibição de imóveis indisponíveis nos resultados de busca.

## Infraestrutura do OpenSearch

Atualmente, nossa infraestrutura na AWS está localizada na região **us-west-2 (Oregon)**. Considerando a latência geográfica, uma alternativa que poderia reduzir significativamente o tempo de resposta seria migrar para a região **sa-east-1 (São Paulo)**, mais próxima dos nossos usuários.

Em uma pesquisa rápida, é possível ver que essa região ofereceria menos latência, em duas ferramentas diferentes ela foi apontada como a melhor alternativa, oferencendo uma latência média de **30ms** contra **160-200ms** de Oregon. Apresentando então um ganho de **130 - 160ms**.

 ![Fonte: https://clients.amazonworkspaces.com/Health.html](/api/attachments.redirect?id=e6d88cb7-ead3-4156-a5e8-e5c1ef25d789)\n ![Fonte: https://aws-latency-test.com/](/api/attachments.redirect?id=467e88c0-f664-4ae0-ac40-0eeca114c964)

Devido a esses números, talvez fosse interessante fazer um teste mudando a região do pod do OpenSearch para São Paulo para verificar se haveria alguma melhoria significativa.

## Otimização da query

Na query do OpenSearch, o maior gargalo são com certeza os scripts, já que eles adicionam complexidade e custo ao processamento de cada documento. Atualmente, utilizamos três scripts distintos ao longo da query, todos escritos em Painless (linguagem de scripts nativa do OpenSearch) e definidos no arquivo `create_search_indexes.py`. Dentre eles, os dois principais são o `price-and-availability-filter-script` e o `get-calc-values-script`.


**price-and-availability-filter-script**

Responsável por **filtrar propriedades** com base em disponibilidade e preço. Avalia, para cada documento:

* Se **todas as datas solicitadas** estão disponíveis
* Se **check-in e check-out não estão bloqueados**
* Se o **preço médio por diária** está dentro do intervalo definido na busca
* Se a **estadia mínima (min_stay)** é respeitada
* Se comporta **hóspedes extras** (ex: bebês)
* Verifica **restrições de entrada e saída**
* Custo alto: envolve múltiplas verificações por documento, tornando a execução **pesada para o OpenSearch**

  \

**get-calc-values-script**

Utilizado para **calcular valores exibidos na interface** do usuário. Para cada documento retornado, ele:

* Calcula o **valor total da estadia**
* Calcula o **preço médio por diária**
* Retorna a **lista de datas consideradas**
* Essencial para fornecer **informações precisas** ao usuário
* Custo: executa **cálculos personalizados por documento**, contribuindo para o tempo de resposta da query

Remover esses scripts implicaria em uma refatoração consideravelmente grande de toda a lógica de busca, uma vez que boa parte das regras de negócio hoje está embutida nos scripts. Para eliminar essa dependência, seria talvez seja necessário reestruturar os dados e talvez antecipar diversos cálculos no momento da indexação. Além disso, a query nativa do OpenSearch teria que incorporar essas regras manualmente, o que aumentaria significativamente sua complexidade.

Como experimento, foi realizado um teste comentando temporariamente o `price-and-availability-filter-script` para observar o impacto direto na performance. O ganho obtido foi de aproximadamente 30ms.