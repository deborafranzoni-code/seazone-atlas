<!-- title: Análise Comparativa: POC de Performance das Imagens da Busca | url: https://outline.seazone.com.br/doc/analise-comparativa-poc-de-performance-das-imagens-da-busca-XOwT3BM0HU | area: Tecnologia -->

# 🖼️ Análise Comparativa: POC de Performance das Imagens da Busca

# Objetivo

O objetivo deste documento é apresentar uma análise comparativa simples sobre o desempenho no tempo de carregamento das imagens, considerando dois cenários: quando as imagens são carregadas da Stays e quando estão hospedadas em nosso bucket no S3.

# Cenário do Teste


1. **Seleção das imagens**
   * Foram escolhidas as primeiras imagens da página de resultados da busca para a cidade de Florianópolis, sem datas selecionadas.
2. **Hospedagem no S3**
   * As imagens selecionadas foram carregadas em um bucket do S3.
3. **Uso de CDN para ambos os cenários**
   * Como atualmente utilizamos uma CDN para servir as imagens da Stays, as imagens hospedadas no S3 também foram configuradas para serem entregues via CDN.
4. **"Disable Cache" Ativado no DevTools**
   * O cache do navegador foi desabilitado para que os testes considerem exclusivamente a performance da CDN, sem interferência do cache local.

Diante desse cenário, definiu-se que a comparação seria realizada por meio da execução de 5 carregamentos da página em cada um dos dois cenários (utilizando imagens da Stays e do S3). Em cada execução, o tempo de carregamento seria observado na aba "Network" do navegador, permitindo calcular uma média e, assim, comparar o desempenho entre as duas abordagens.

# Resultados

Os resultados obtidos com base nos testes estão apresentados na tabela a seguir:

| ImageID | Stays (ms) | S3 (ms) | Size (Kb) |
|----|----|----|----|
| **68557122fe5b75c850fc1eb3** | ==135.16== | ==161.34== | 18.0 |
| **680aa0cf40b694f84a476836** | ==161.76== | ==241.82== | 15.8 |
| **6696ce9e413f5fc40f8662fe** | ==172.14== | ==266.24== | 15.3 |
| **67d86c2617630fe193561bac** | ==208.28== | ==317.12== | 23.9 |
| **67fe75d20a6913f0d3fee009** | ==332.7== | ==381.78== | 17.2 |
| **66a8070f4f1a7e2358241ac1** | ==262.58== | ==435.9== | 21.5 |
| **66b2264493e5b63a93596ef3** | ==268.1== | ==434.1== | 18.9 |
| **6633eca577c3100b417ce95a** | ==383.18== | ==628.32== | 14.6 |
| **6842e939e332df97174c31c7** | ==416.78== | ==496.2== | 18.7 |
| **6801511f752fcfd2d2b15371** | ==396.36== | ==524.68== | 14.7 |
| **678fbb93d3217d74baa34cbe** | ==359.26== | ==557.32== | 15.6 |
| **677813532b699b6f26fa070b** | ==431.22== | ==571.44== | 16.5 |
| **622a2f92b928a77ad1fa6c8e** | ==480.02== | ==678.04== | 21.0 |
| **6759d8a1c9d98b96624a4003** | ==545.54== | ==737.08== | 17.2 |
| **67780073d5783bf83a089f83** | ==612.1== | ==759.7== | 9.9 |
| **6842f7915f94293d7d136fe0** | ==568.58== | ==769.12== | 19.4 |
| **6842f2d6a8bff84ebdb65e24** | ==585.52== | ==751.34== | 19.4 |
| **684c2f69032c536fbd724e3b** | ==515.96== | ==820.92== | 17.3 |

# Conclusões & Descobertas

Após a conversa com o time de Governança, foi esclarecido que a motivação inicial para hospedar as imagens no S3 foi a dificuldade de cacheamento via CDN, o que resultava em lentidão no carregamento. Na tabela abaixo, a coluna "Stays" mostra os números registrados antes da implementação do cache.


 ![Números antes da CDN](/api/attachments.redirect?id=2a647173-fe2c-4f85-a1e9-febf97688bb3)

Descobriu-se, então, que o problema estava na ausência de um Behavior específico para as imagens da Stays na distribuição do CloudFront do ambiente de produção. Esse Behavior já existia na distribuição de staging, mas não havia sido replicado na de produção.

Com o objetivo de viabilizar um teste justo entre as duas alternativas (carregar as imagens diretamente da Stays ou do S3), foi identificado que o Behavior necessário não estava configurado na distribuição de produção. Após sua adição, o cache passou a funcionar corretamente, refletindo nos números apresentados na primeira tabela da seção de resultados.

Nesse momento, ficou claro que o problema central que motivou toda a investigação (a impossibilidade de cachear as imagens vindas da Stays) foi efetivamente resolvido com a adição do Behavior na distribuição do CloudFront.

Com as imagens sendo corretamente cacheadas pela nossa distribuição no CloudFront, sua performance passou a ser significativamente melhor. Isso ocorre porque, quanto mais acessado, mais eficiente o cache se torna. Como todas as imagens dos imóveis vêm da Stays, o cache se beneficia desse volume de acessos, tornando-se otimizado. Isso explica os melhores números associados à Stays, que são, na verdade, reflexo da eficiência da nossa CDN (e não da infraestrutura deles). Essa conclusão é reforçada pelos dados coletados antes da configuração do cache, que mostram tempos de carregamento consideravelmente maiores.

Outros indicativos da melhoria de performance após a inclusão do Behavior na CDN são as imagens abaixo. A primeira mostra um aumento significativo no número de hits a partir do dia 11/07, data em que a configuração foi aplicada. A segunda exibe a pontuação de performance da busca segundo o Lighthouse, refletindo os ganhos obtidos.

 ![Número de hits](/api/attachments.redirect?id=7b443415-85d6-46c2-8e1c-ec5858b97524)

 ![Performance do site de acordo com o Lighthouse](/api/attachments.redirect?id=7f310fb5-c621-4eb1-905a-303aef89a5a2)

Nesse contexto, temos o seguinte cenário: o principal problema que motivou a ideia de hospedar as imagens no S3 (a impossibilidade de cachear as imagens da Stays) foi resolvido. Como vimos, essa correção já resultou em uma melhora significativa no tempo de carregamento das imagens. Agora, após a conversa com o time de Governança, entendemos que o caminho para continuar melhorando a performance não passa mais pela utilização do S3, mas sim por uma maior otimização da nossa CDN.

## Alterar política de cache

Atualmente, o cache das imagens está configurado para durar um dia. Isso significa que, após 24 horas, o conteúdo armazenado em cache expira, e uma nova requisição é feita à origem para atualizar a imagem. Um próximo passo importante seria avaliar com que frequência as imagens realmente mudam, pois, caso aumentássemos esse tempo para uma semana, por exemplo, a performance poderia ser ainda mais otimizada.

## Otimização da Qualidade das Imagens no Setup dos Anúncios

Outra ação importante que pode contribuir para a otimização é reduzir o tamanho das imagens antes de enviá-las para a Stays. O time responsável pelo setup dos anúncios poderia enviar as imagens com qualidade ajustada para um nível inferior, o que provavelmente ajudaria a melhorar o desempenho do nosso lado.