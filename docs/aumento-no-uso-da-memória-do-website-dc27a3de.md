<!-- title: Aumento no uso da memória do website | url: https://outline.seazone.com.br/doc/aumento-no-uso-da-memoria-do-website-UGk8kjwuAr | area: Tecnologia -->

# Aumento no uso da memória do website

Task [SZRDEV-1039](https://seazone.atlassian.net/browse/SZRDEV-1039)


# O Problema

> No dia 06/01/2025 o website ficou fora do ar

Detectamos recentemente um aumento significativo no uso de memória do website. Analisando os gráficos da AWS, foi possível observar que a memória vem sendo consumida de forma gradual, até que em determinado momento ela é resetada, voltando a crescer novamente.

 ![](/api/attachments.redirect?id=68580c01-84e8-4685-81ba-83bb89be36eb)

Analisando o uso de memória nas últimas seis semanas, percebemos que no dia em que o website saiu do ar o consumo atingiu 99,9%.

# **Hipóteses sobre o problema**

A causa exata do elevado consumo de memória ainda é desconhecida, mas levantamos algumas hipóteses que podem ter contribuído para o problema. Entre elas, destacam-se:


* **Uso incorreto e excessivo do BFF para repasse de requisições do backend**
  * Atualmente, temos APIs BFF praticamente duplicadas para cada API do backend necessária para o front-end. A maioria dessas APIs não faz nada além de repassar requisições. Esse comportamento gera problemas, pois o uso excessivo dessas APIs aumenta não só o consumo de processamento, mas também o uso de memória na máquina.

    \
* **Aumento no número de acessos ao website**
  * Outra hipótese é que, no período em que o website saiu do ar, ele recebeu uma média de **2.000 usuários a mais** do que o normal. Isso pode indicar que o site não está dimensionado para suportar uma carga superior a essa. Para resolver o problema, é possível:

    \
    * Aumentar a memória e a CPU do website;
    * Implementar soluções de escalabilidade automática, evitando quedas em momentos de maior tráfego.


# Possíveis soluções

Para mitigar o problema e melhorar a eficiência do website, propomos as seguintes soluções:


* **Análise do uso de SSR e viabilidade de substituição por ISR**
  * O uso de SSR (Server-Side Rendering) faz com que o Next.js entenda que uma página possui dados altamente dinâmicos, que mudam constantemente. Uma alternativa é adotar o ISR (Incremental Static Regeneration), que revalida a página em intervalos definidos.\n
  * Por exemplo, na tela de busca de imóveis, podemos configurá-la para ser revalidada a cada **2 horas**, reduzindo a carga do servidor.


* **Refatoração dos BFFs desnecessários**
  * Para reduzir o uso excessivo de processamento e memória, sugerimos a refatoração das APIs BFF que atualmente funcionam apenas como intermediários. Para isso, será necessário:

    \
    * **Implementar uma camada de segurança no backend**, incluindo autenticação e autorização robustas, garantindo que ele possa ser acessado diretamente sem comprometer a segurança dos dados.
    * Eliminar intermediários redundantes, simplificando a comunicação entre o front-end e o backend.


* **Migração para o App Directory (Next.js 14)**
  * A nova arquitetura do Next.js melhora significativamente a renderização no servidor, introduzindo:

    \
    * **Server Components**: Permitem que apenas partes específicas da página busquem dados no servidor;

      \
    * **Streaming**: Enquanto os dados são buscados, é possível exibir um fallback de loading ou outra informação;

      \
    * **Renderização estática otimizada**: O uso de multithreading é habilitado, algo que a arquitetura atual (Pages Layout) não suporta, pois toda a página é renderizada no servidor de forma monolítica. Com a nova abordagem, apenas os componentes necessários são renderizados no servidor.

      \
  * Essas melhorias podem reduzir o tempo de resposta, o uso de recursos do servidor e proporcionar uma experiência de navegação mais fluida para os usuários.

  \