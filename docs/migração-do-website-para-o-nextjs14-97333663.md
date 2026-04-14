<!-- title: Migração do website para o nextjs.14 | url: https://outline.seazone.com.br/doc/migracao-do-website-para-o-nextjs14-fqZEMEHXWW | area: Tecnologia -->

# Migração do website para o nextjs.14

:::tip
## **TL;DR**

O website foi desenvolvido com Next.js 13, antes do lançamento da versão 14. A versão 13 tem limitações na renderização no servidor, que impactam o desempenho, especialmente em páginas com múltiplas requisições API.

*==Temos uma== [==tech talks==](https://drive.google.com/file/d/1F4KB_Ip6YQVBkwbvJdVqauGDFLYEwhd0/view?usp=drive_link) ==que explica melhor sobre nextjs caso deseje saber mais.==*

### **Impacto no Website**

* **Next.js 13**: Toda a página depende de múltiplas requisições no servidor, aumentando o tempo de carregamento.
* **Next.js 14**: Componentes server-side independentes permitem renderização mais eficiente e rápida, reduzindo o tempo de espera e entregando uma experiência superior ao usuário.

### **Exemplo Prático**

Com Next.js 14, a home do website poderia usar estratégias de renderização assíncrona, exibindo seções não dependentes de APIs de imediato, enquanto outras usam shimmer loaders para mostrar progresso. Isso resulta em páginas mais rápidas e dinâmicas.

### **Conclusão**

A atualização para Next.js 14 traria melhorias significativas em desempenho, modularidade e experiência do usuário.

:::

# O que é Next ?

O **Next.js** é um framework de desenvolvimento baseado em **React**, utilizado para construir aplicações web modernas. Ele é conhecido por oferecer funcionalidades avançadas como **renderização no servidor (SSR)**, **geração de páginas estáticas (SSG)** e um excelente suporte a **SEO**. Essas características ajudam a melhorar a experiência do usuário final, aumentar o desempenho das aplicações e otimizar a visibilidade nos mecanismos de busca.


:::info
Caso você queira saber mais temos um talks que explica com mais detalhes oq é essa técnologia - [Tech Talks - Nextjs](https://drive.google.com/file/d/1F4KB_Ip6YQVBkwbvJdVqauGDFLYEwhd0/view?usp=drive_link)

:::

# O problema 

O website de reservas foi desenvolvido utilizando a tecnologia Next.js, que oferece benefícios importantes, como suporte para renderização no servidor, geração de páginas estáticas para melhorar o desempenho do usuário final e um bom suporte a SEO, essencial para aumentar a visibilidade de nossas páginas nos mecanismos de busca, como o Google.


No entanto, na época da construção do website, o Next.js estava passando por uma grande refatoração em sua estrutura interna e planejando uma atualização significativa, a versão 14, que traria várias melhorias e mudanças estruturais importantes. Como essa versão ainda estava em beta naquele momento, o website foi desenvolvido utilizando a versão 13, mais antiga. Isso implica que nosso sistema atualmente não aproveita os novos recursos e a arquitetura aprimorada introduzidos na versão 14.


# Entendendo as vantagens do Next.js 14

Alguns pontos de vantagens do next 14 segundo a **[documentação oficial](https://nextjs.org/blog/next-14?utm_source=chatgpt.com)**

* **Melhorias no desempenho** 
  * A introdução de recursos avançados, como **React Server Components** aprimorados, torna as páginas mais rápidas e leves. O Next.js 14 prioriza o carregamento eficiente dos componentes, permitindo uma experiência de usuário fluida.

    \
* **Layouts Aninhados e Novo Roteamento**
  * Os layouts aninhados são um grande avanço para a organização de projetos complexos. Agora, é possível definir layouts reutilizáveis de forma hierárquica, facilitando a consistência visual e a modularidade do código.
  * O Router foi refinado para simplificar o roteamento baseado em arquivos. Este recurso aproveita melhor as funcionalidades do React Server Components, o que resulta em um fluxo de navegação mais limpo e integrado com o server-side.

    \
* **Melhoria na renderização híbrida**
  * O Next.js 14 reforça seu suporte a diferentes estratégias de renderização (SSR, SSG e ISR), possibilitando a combinação mais eficiente conforme as necessidades do projeto. A renderização incremental agora está mais rápida e flexível.

    \
* **Server Actions**
  * Permite que ações específicas sejam processadas diretamente no servidor, reduzindo a necessidade de APIs separadas e melhorando a segurança e a performance.

# Como o website poderia se aproveitar desses recursos

A principal vantagem do Next.js 14 em relação à versão 13, atualmente em uso, é a possibilidade de transformar qualquer componente em um componente renderizado no servidor. Isso potencializa a performance, reduz o tempo de carregamento e melhora a experiência do usuário ao entregar páginas mais rápidas e eficientes.

Na versão 13 apenas componentes de páginas podem ser renderizados pelo servidor, o que implica que se uma página faz varias requisições para varias apis, nessa versão o next espera todas as requests finalizarem para que ai sim a página seja renderizada.

## Vamos usar como exemplo a home do website para exemplificar melhor essa ideia


Podemos notar que a nossa home pode ser dividida de forma simples em três etapas que realizam requisições para diferentes apis


 ![](/api/attachments.redirect?id=5c3d54d9-bd79-45d9-be99-204b69d53f50 " =6804x267")


> Vamos imaginar que desejamos realizar todas as operações no lado do servidor para garantir um carregamento mais rápido da página.


### **1° Cenário - Next 13**

Com o Next.js 13, apenas o componente principal da página pode ser renderizado no lado do servidor. Isso significa que todas as requisições para a API precisariam ser feitas em um único local. Como consequência, mesmo que existam seções da página que não dependam de requisições à API, o carregamento completo da página ficaria condicionado à resposta de todas as APIs, aumentando o tempo de renderização.


### **2º Cenário - Next.js 14**

No Next.js 14, é possível aproveitar o suporte aprimorado à renderização assíncrona e componentes server-side isolados. Isso permite que diferentes partes da página realizem requisições de forma independente no lado do servidor. Dessa forma, componentes que não dependem de respostas da API podem ser renderizados imediatamente, enquanto outros aguardam apenas as requisições necessárias para cada seção específica. Esse modelo reduz o impacto no tempo de carregamento geral da página e melhora a experiência do usuário.

Utilizando algum shimmer de loading poderiamos renderizar a home dessa forma

onde os lugares que estão fazendo requisições usando o servidor teriam um shimmer loading e os lugares que não precisam seriam renderizados de imediato


 ![](/api/attachments.redirect?id=82dc1bbe-e13a-495a-b914-5675058e1e98)


Esse exemplo é mais para ilustrar a forma como ambas as versões trabalham com o SSR, atualmente no website nós não deixamos tudo a cargo do servidor justamente para não limitar o carregamento da página em si