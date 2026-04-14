<!-- title: Performance - Componente da Busca Mobile | url: https://outline.seazone.com.br/doc/performance-componente-da-busca-mobile-xq2NBuC95B | area: Tecnologia -->

# Performance | Componente da Busca Mobile

## Visão Geral

Este relatório analisa o tempo médio de abertura do modal de busca em dispositivos móveis, simulando pelo DevTools do Chrome diferentes cenários de CPU (real vs. 4x mais lenta), tipo de rede (3G, Slow 4G, Fast 4G) e tipo de carregamento (First Load vs. Next Load cacheado), com e sem as otimizações aplicadas.

Inicialmente, o modal levava cerca de 3 ou mais segundos para abrir, especialmente em dispositivos mais lentos (ex: Moto G). A principal causa identificada foi o uso de SVGs complexos nos mapas das regiões, além da renderização de um intervalo muito grande de meses no calendário. A partir dessa investigação, foram implementadas as seguintes melhorias de performance:

* **1.** Substituição dos mapas em SVG por imagens PNG otimizadas com TinyPNG; 
* **2.** Carregamento dinâmico das datas no calendário conforme o scroll (2 meses por vez); 
* **3.** Renderização preguiçosa (lazy render) dos modais de destino e calendário, evitando que fossem montados na DOM antes da interação do usuário.

  \

Com essas mudanças, o tempo de abertura do modal caiu drasticamente, oferecendo uma experiência significativamente mais fluida em ambientes com recursos limitados.


## Análise comparativa

As Tabelas 1 e 2 detalham os resultados obtidos. Os tempos medidos em milessegundos correspondem a média de 5 execuções realizadas em cada cenário. Como podemos observar, as otimizações implementadas resultaram em reduções drásticas nos tempos de carregamento em todos os cenários. Os principais impactos foram:

* **Impacto da CPU:** A lentidão da CPU (simulada em 4x) tem um efeito drástico no tempo de carregamento, aumentando-o significativamente em todos os cenários de rede. Por exemplo, em 3G, o First Load salta de \~839 ms (CPU real) para \~5125 ms (CPU 4x lenta).
* **Impacto da Rede:** Redes mais rápidas (Fast 4G) melhoram os tempos de carregamento em comparação com 3G, mas o ganho é menos pronunciado do que o impacto da CPU. A rede 3G é a mais lenta, enquanto a Fast 4G oferece os melhores tempos.
* **First Load vs. Next Load:** O Next Load, que utiliza recursos em cache, é sempre mais rápido que o First Load. Isso demonstra a eficácia do cache na redução dos tempos de carregamento, mesmo em cenários de CPU lenta.


**Tabela 1. Primeiro Carregamento**

| Rede | CPU | First Load atual (ms) | First Load otimizado (ms) | Redução (ms) | Redução (%) |
|----|----|----|----|----|----|
| 3G | real | 839.1 | 498.5 | 340.6 | 40.6% |
| 3G | 4× lento | 5125.4 | 1097.1 | 4028.3 | 78.6% |
| Slow 4G | real | 752.4 | 292.3 | 460.1 | 61.2% |
| Slow 4G | 4× lento | 4742.9 | 1039.3 | 3703.6 | 78.1% |
| Fast 4G | real | 630.9 | 221.5 | 409.4 | 64.9% |
| Fast 4G | 4× lento | 3508.1 | 465.6 | 3042.5 | 86.7% |


**Tabela 2. Carregamentos Subsequentes (Cacheado)**

| Rede | CPU | Next Load atual (ms) | Next Load otimizado (ms) | Redução (ms) | Redução (%) |
|----|----|----|----|----|----|
| 3G | real | 768.6 | 191.3 | 577.3 | 75.1% |
| 3G | 4× lento | 4988.7 | 487.6 | 4501.1 | 90.2% |
| Slow 4G | real | 664.9 | 121.5 | 543.4 | 81.7% |
| Slow 4G | 4× lento | 3958.7 | 462.3 | 3496.4 | 88.4% |
| Fast 4G | real | 493.6 | 99.0 | 394.6 | 79.9% |
| Fast 4G | 4× lento | 3340.3 | 441.5 | 2898.8 | 86.8% |

As melhorias foram particularmente eficazes nos cenários mais lentos (CPU 4x lenta), com reduções percentuais significativas. No Tabela 2, as reduções foram ainda maiores devido ao cache de recursos pelo browser após o primeiro carregamento, variando de 75% a 90% em muitos casos.

## Conclusões

Em condições realistas (smartphone mediano e rede móvel decente), a experiência de carregamento do modal deve ser fluida (abaixo de 500 ms após otimizações). Dispositivos normais em redes Fast 4G devem abrir o modal em centenas de milissegundos. Com as melhorias aplicadas, todos os cenários de 4G ficam confortavelmente abaixo de 1 segundo, mesmo com CPU lenta. A análise conclui que a CPU lenta é o principal gargalo, degradando drasticamente os tempos, enquanto a rede lenta tem um impacto menor. As melhorias de performance e o uso de cache são essenciais para uma boa experiência mobile, especialmente em redes menos robustas.

## Referências

* [Recommended Web Performance Timings: How long is too long? - Performance | MDN](https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/How_long_is_too_long)
* [Speed Comparison: 5G, 4G, LTE, and 3G](bandwidthplace.com)
* [How To Debug React Apps Like A Senior Developer](https://www.youtube.com/watch?v=l8knG0BPr-o&t=1046s)
* [Como usar o Profiler no React DevTools para otimizar seus componentes](https://www.youtube.com/watch?v=x4b7jAh6N1c)
* [ReactJS: Quando e Como Usar Memoization para Evitar Re-Renders](https://www.youtube.com/watch?v=nJOca650HKs&t=494s)