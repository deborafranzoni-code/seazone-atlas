<!-- title: Casos de Uso do OpenSearch no Site de Reservas | url: https://outline.seazone.com.br/doc/casos-de-uso-do-opensearch-no-site-de-reservas-k1Y7LiGICF | area: Tecnologia -->

# Casos de Uso do OpenSearch no Site de Reservas

<aside> ℹ️ Utilizamos o OpenSearch para prover um mecanismo de busca mais poderoso. Os dados do OpenSearch são efêmeros, ou seja, podemos excluir todos os dados e ainda assim é possível re-gerar tudo de novo. Toda sincronização com a Stays atualiza os dados do OpenSearch.

</aside>

## Por que usamos o OpenSearch?

Para ter alta disponibilidade e velocidade no tempo de retorno de informações na busca por imóveis. Isso inclui as informações básicas sobre eles, bem como seus preços e disponibilidade, e também, a busca pelos destinos.

## Onde usamos o OpenSearch?

### Destinos e Imóveis

Apesar de ter os imóveis e os destinos (bairros, cidades, estados, destinos personalizados) salvos em nosso Banco de Dados, também indexamos todos imóveis e seus detalhes no OpenSearch para que os resultados de uma busca pelo usuário sejam retornado rapidamente.

Possuímos uma base com cerca de 1K de imóveis, e cada imóveis com várias informações. Seria pouco performático realizar essas buscas e filtragens por meio do ORM/BD.

Então, pensando na escalabilidade, optamos por já começar o projeto usando o OpenSearch, começando com pé direito.

### Preços e Disponibilidade

Diferente dos Destinos e Imóveis, os preços e disponibilidade dos imóveis não são salvos em base de dados, mas sim exclusivamente no OpenSearch.

Assim, quando o usuário realiza uma busca, os preços e disponibilidade são obtidos através de um script do OpenSearch.

Assim como os Destinos e Imóveis, guardar preços e disponibilidade em uma base de dados seria pouco performático e escalável. Além de ser um dado que pode mudar a todo momento, assim, sendo melhor deixá-lo apenas no OpenSearch.

<aside> ℹ️ A indexação dos imóveis, destinos, preços e disponibilidade no OpenSearch são realizados por meio de tarefa assíncrona do Celery, que rodam a cada 30min (em produção) para atualizar as informações. Os preços e Disponibilidade também são atualizados quando recebemos webhooks da Stays informando que preços e disponibilidade de um determinado imóvel foram alterados.

</aside>

<aside> ℹ️ As informações de imóveis, preços e disponibilidade são importadas da Stays. Os destinos são criados com base nos endereços dos imóveis ativos.

</aside>

## Desenvolvimento uma feature que utiliza o OpenSearch

**Como é Indexação das informações no OpenSearch (Create e Update)**

Descrever…

**Obtenção das informações que estão em um index do OpenSearch (Read)**

Descrever…