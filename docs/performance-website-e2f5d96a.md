<!-- title: Performance Website | url: https://outline.seazone.com.br/doc/performance-website-RL9cKLXJvE | area: Tecnologia -->

# Performance Website

# KPIs

## Meta: \n*70% da performance do Airbnb para Mobile e Desktop*

KPI186; KPI187; KPI188 da planilha [KPI TECH](https://docs.google.com/spreadsheets/d/1kKbv_75rRcwUBrTwaDLZiTOtuiLQulsx4-1mNJi76jI/edit?gid=0#gid=0&fvid=663758499)


Pontos de controle para o Q3:

| Tela | Device | Pontos Lighthouse |
|----|----|----|
| Home | Desktop |    |
| Home | Mobile |    |
| Busca | Desktop |    |
| Busca | Mobile |    |
| Página do Imóvel | Desktop |    |
| Página do Imóvel | Mobile |    |

## Home

| Métrica | Website ANTES da CDN | Website ATUAL | Website Meta | Booking.com | Airbnb | Wander |
|----|----|----|----|----|----|----|
| FCP | 4.9s | 3.2s | 1.5s | 1.5s | 0.7s | 0.4s |
| LCP | 7.3s | 7.3s | 2.8s | 2.2s | 2.8s | 1.1s |
| TBT |    | 130ms | 170ms | 140ms | 380ms | 240ms |
| SI |    | 6.2s | 3s | 3.7s | 3.1s | 2.8s |
| CLS | 0.38 | 0.55 | 0.15 | 0.05 | 0.0006 | 0.05 |

## Resultados da Busca

| Métrica | Website ANTES da CDN | Website ATUAL | Website Meta | Booking.com | Airbnb | Wander |
|----|----|----|----|----|----|----|
| FCP | 4.5s | 3.4s | 2.3s | 2.3s | 0.6s | 0.5s |
| LCP | 7.3s | 7.7s | 5.9s | 5.2s | 3.0s | 5.9s |
| TBT |    | 160ms | 170ms | 270ms | 600ms | 140ms |
| SI |    | 7.1s | 5s | 6s | 4.3s | 2.4s |
| CLS | 0.35 | 0.17 | 0.15 | 0 | 0.02 | 0.4 |

## Imóvel

| Métrica | Website ANTES da CDN | Website ATUAL | Website Meta | Booking.com | Airbnb | Wander |
|----|----|----|----|----|----|----|
| FCP | 4.5s | 3.0s | 3.1s | 1.4s | 3.1s | 0.5s |
| LCP | 7.3s | 8.5s | 4.7s | 3s | 4.7s | 3.4s |
| TBT |    | 30ms | 100ms | 130ms | 20ms | 210ms |
| SI |    | 6.9s | 4s | 3.8s | 4.6s | 2.5s |
| CLS | 0.35 | 0.664 | 0.15 | 0.05 | 0.016 | 0 |

## Checkout

| Métrica | Website ANTES da CDN | Website ATUAL | Website Meta | Booking.com | Airbnb | Wander |
|----|----|----|----|----|----|----|
| FCP |    |    | 1.5s |    |    |    |
| LCP |    |    | 2.2s |    |    |    |
| TBT |    |    | 150ms |    |    |    |
| SI |    |    | 2s |    |    |    |
| CLS |    |    | 0.1 |    |    |    |


## Considerações Extras MUITO IMPORTANTES


1. O componente da busca mobile e o componente de mudança de datas desktop não deve demorar mais do que 200ms para serem renderizados ao usuário
2. O endpoint de pagamento não deve demorar mais do que 2 segundos para finalizar  a compra COMPLETAMENTE (inclui: recebermos no nosso sistema o webhook da Tuna, até darmos o ok ao usuário)

# Plano de Ação

## O que será feito?

### KPIs de Performance que iremos olhar

Iremos olhar para o cálculo geral da performance e para a latência de alguns endpoints.

| KPI | Meta | Atual |
|----|----|----|
| Home | 63 no lighthouse | 32 |
| Busca | 48 no lighthouse | 44 |
| Imóvel | 52 no lighthouse | 33 |
| Componente de busca | 200ms para abrir o componente e o usuário utilizar |    |
| Pagamento | 2 segundos desde que o usuário clicou em pagar até ser confirmada a compra |    |


Em sequência serão feitas as tasks abaixo com o objetivo de atingir os KPIs acima. O plano será considerado entregue quando os KPIs forem atingidos, não precisando ser executado totalmente.

## Itens a serem implementados

### Ajustes da CDN - Já foi feito @[Roberto Campos](mention://0336ba33-7b2e-4477-aac0-13440dfb7db5/user/7a820dce-f3c4-4cd0-9054-82f4b4d27bf7) 

* Motivo:
* O que será feito:
* DoD:
* Esforço:
* Tempo para conclusão: 

### POC BACK LATAM  [🌐 Análise de Latência: AWS Brasil vs Oregon](/doc/analise-de-latencia-aws-brasil-vs-oregon-HV9dxF9BuY)**[🌐 Análise de Latência: AWS Brasil vs Oregon](/doc/analise-de-latencia-aws-brasil-vs-oregon-HV9dxF9BuY)**

* Motivo: O servidor da stays e da tuna estão localizados no brasil enquanto o nosso servidor está localizado nos EUA. Com isso, a latência de cada *request* ganha um adicional de mais de 100ms, o que piora quando temos *requests* empilhadas. Queremos testar o impacto de migrar o servidor para deixá-lo mais perto 
* O que será feito: Teste com o *endpoint* de busca e com o *endpoint* de reservas no servidor LATAM para avaliar o impacto em ms da troca.
* DoD: Relatório que compara a latência nos *endpoints* de busca e reserva para entender quais os possíveis ganhos em uma migração e os possíveis custos de infra. Será definido junto com o time de infra o plano de ação para a migração definitiva (ou não) do servidor.
* Esforço: 1 semana
* Tempo para conclusão: 4/07

### POC de performance com imagens no site

* Motivo: As imagens hoje são armazenadas na stays, o que faz o que não tenhamos o controle sobre a rapidez e cache dos recursos mais pesados e mais importantes para o nosso usuário. 
* O que será feito: A POC visa testar para florianópolis a migração das imagens da primeira página de busca para o S3 e avaliar o impacto disso no carregamento da página de busca.
* DoD: Relatório mostrando tempo de carregamento antes e depois e o impacto para o usuário final no carregamento da página. Esse relatório irá ser utilizado para definir se iremos prosseguir com a migração total das imagens para infra própria ou não.
* Esforço: 1 semana
* Tempo para conclusão: 11/07

### Migração do Back para o Servidor LATAM

* Motivo: De acordo com o relatório feito, o endpoint de /create das reservas poderia ficar até 800ms mais rápido
* O que será feito: Migração da AWS para servidor em são paulo
* DoD: AWS em servidor em são paulo
* Esforço: Médio
* Tempo para conclusão: 11/07

### Migração do Front para o Servidor LATAM @[Roberto Campos](mention://de842400-f0b9-4f58-8aaf-1ae746493c74/user/7a820dce-f3c4-4cd0-9054-82f4b4d27bf7) 

* Motivo: 
* O que será feito:
* DoD:
* Esforço: Médio
* Tempo para conclusão: 18/07

### Melhorar o Loading do Calendário no Mobile

* Motivo: Hoje o usuário mobile leva mais de 3s para conseguir abrir o modal para escolher a localidade. Isso ocorre porque o calendário é pesado e demora para carregar, impactando a experiência do usuário.
* O que será feito: Melhorar a performance de carregamento do calendário da busca
* DoD: Abrir a modal do componente de busca em até 200ms
* Esforço: Médio
* Tempo para conclusão: 01/08

### Retirada do *Auth0* da */create*

* Motivo: O endpoint de */create* da reserva demora em média 4.5s para executar. O *Auth0* demora 1s para criar a conta do usuário durante a compra. A conta só será de fato necessária depois que a compra estiver paga.
* O que será feito: Mover a criação de conta para ser feita de maneira assíncrona.
* DoD: Abaixar o tempo que o usuário aguarda para ver a reserva feita para até 3.5s em média.
* Esforço: Médio
* Tempo para conclusão: 25/07

### Retirada da criação de conta na stays da */create*

* Motivo: O endpoint de */create* da reserva demora em média 4.5s para executar. A criação de conta na stays leva em média 800ms e não é necessária nesse momento.
* O que será feito: Realizar a criação de conta de maneira assíncrona. 
* DoD: Abaixar o tempo que o usuário aguarda para ver a reserva feita para 2.8s
* Esforço: Médio
* Tempo para conclusão: 15/08

### Categorizar requests pro prioridade (fetch-priority) @[Roberto Campos](mention://9dd17218-9fdb-4b92-a627-f90df70dafa6/user/7a820dce-f3c4-4cd0-9054-82f4b4d27bf7) 

* Motivo: Atualmente no website várias chamadas são feitas dentro do site, e todas elas levam um tempo de X segundos para serem finalizadas, por padrão, os navegadores esperam que todas sejam concluídas para mostrar o conteúdo na tela. Dentro das nossas regras de negócio, podemos priorizar e paralelizar algumas chamadas para que sejam feitas conforme a página seja renderizada, e assim, melhorar a performance
* O que será feito: Categorizar as chamadas feitas no site em low e high, e aplicar isso dentro de cada página do site (home, checkout, pg do imóvel)
* DoD: Ter todas chamadas de páginas do site categorizadas com fetch-priority low ou high
* Esforço: Baixo
* Tempo para conclusão:  25/07

### Refatorar feature-flags do client-side para SSR @[Roberto Campos](mention://f1e3d6e0-29f9-4ef4-bab5-243534ffbba3/user/7a820dce-f3c4-4cd0-9054-82f4b4d27bf7) 

* Motivo: Utilizar as feature-flags no client-side pioram nossa performance devido principalmente a experimentos, testes A/B e entrega contínua, visto que antes da página ser renderizada é preciso saber o que alterar em tempo de tela.
* O que será feito: Refatorar o código para saber em tempo de servidor qual variante e o que deve ser renderizado na tela.
* DoD: Ter busca, home e página do imóvel com features flag no server-side.
* Esforço: Alto
* Tempo para conclusão: 01/08

### Remover carregamento inicial (3 pontinhos) @[Roberto Campos](mention://24c05a74-248b-412c-b8be-d87f469a0c24/user/7a820dce-f3c4-4cd0-9054-82f4b4d27bf7) 

* Motivo: O site força um carregamento inicial que nem sempre é necessário, e afeta nossas métricas de KPI e a experiência do usuário.
* O que será feito: Seja removido o carregamento forçado e alterado a UI/UX para carregar em partes o site
* DoD: Não ter mais carregamento forçado (desnecessário)
* Esforço: Médio
* Tempo para conclusão: 08/08

### Infra de imagens própria (depende do resultado da POC de imagens) @[Roberto Campos](mention://725ed1f4-7cf7-4b1d-95ef-328ec2009a1d/user/7a820dce-f3c4-4cd0-9054-82f4b4d27bf7) 

* Motivo:
* O que será feito:
* DoD:
* Esforço: Médio
* Tempo para conclusão: 08/06

### Melhorar o loading dos destinos seazone

* Motivo: Toda vez que o usuário clica para ver os destinos seazone no componente de busca ele leva quase 1s carregando - e são os memos destinos e não são muitos.
* O que será feito: @[Roberto Campos](mention://5a384c0c-b256-452d-ae93-ced567124cd3/user/7a820dce-f3c4-4cd0-9054-82f4b4d27bf7) 
* DoD: Não precisar de carregamento a cada request quando o usuário clica nos destinos.
* Esforço: Baixo
* Tempo para conclusão: 15/08

## Prazos e Gantt

→ Seguiremos com as iniciativas na ordem apresentada no gantt abaixo e podemos parar antes caso atingirmos os KPIs da meta acima e despriorizar o restante.

[https://docs.google.com/spreadsheets/d/1ADjm4NPH%5FooKxmoyHUFXy5QiP7Yv-Jtc-5hOIT1iBbk/edit?gid=0#gid=0](https://docs.google.com/spreadsheets/d/1ADjm4NPH%5FooKxmoyHUFXy5QiP7Yv-Jtc-5hOIT1iBbk/edit?gid=0#gid=0)

## Impacto x Esforço

| Ação | KPI Impactado | Impacto | Esforço | Custo de Infra | Prazo | Priorização | Status |
|----|----|----|----|----|----|----|----|
| POC Back para servidor LATAM | Latência da Busca e do Back, TBT | 0 | Baixo | Baixo | 7/7 | Must | 
:::info
Estudo Iniciado

::: |
| Migração do Back para servidor LATAM | Latência da Busca e do Back, TBT | Alto | Medio | Alto (1.3x) | Será definido após a POC estar concluída | Must | 
:::tip
Não iniciada

::: |
| Migração do Front para servidor LATAM | FCP, LCP | Alto | Médio | Alto (1.3x) | Será definido após a POC estar concluída | Must | 
:::tip
Não iniciada

:::   |
| Melhorar o Loading do Calendário no mobile  | Lentidão do componente de busca | Medio | Medio | Zero |    | Must<br> | 
:::tip
Não iniciada

:::   |
| Melhorar o loading dos destinos seazone | Lentidão do componente de busca | Baixo | Baixo | Zero |    | Could | 
:::tip
Não iniciada

:::   |
| Retirada do auth0 da /create | Latência da /create | Alto | Medio | Zero |    | Must | 
:::tip
Não iniciada

:::   |
| Retirada da criação de conta na stays da /create | Latência da /create | Alto | Medio | Zero |    | Must | 
:::tip
Não iniciada

:::   |
| Ajustes da CDN | LCP, FCP | Alto | Médio | A definir |    | Must | 
:::success
Completa

::: |
| Categorizar requests por prioridade (fetch-priority) | LCP, FCP | Médio | Baixo | Zero |    | Must | 
:::tip
Não iniciada

:::   |
| Refatorar feature-flags do client-side para SSR | LCP, FCP | Alto | Alto | Zero |    | Must | 
:::tip
Não iniciada

:::   |
| Remover Carregamento inicial (3 pontinhos) | LCP, FCP | Alto | Medio | Zero |    | Must | 
:::tip
Não iniciada

:::   |
| POC de performance com imagem no Site | LCP, FCP | Baixo | Baixo | Baixo |    | Must | 
:::tip
Não iniciada

:::   |
| Infra de imagens própria | LCP, FCP | Alto | Medio | Baixo | Definiremos após a POC | ??? | 
:::tip
Não iniciada

:::   |
| Migrar para v2 do next |    | Baixo | Alto | Zero | **❌** | Won't (Mas conforme novas páginas forem refatoradas, elas serão refatoradas já na v2 do next) | 
:::warning
Não faremos

::: |
| Depreciar pacotes que não são mais usados |    | Baixo | Baixo | Zero | **❌** | Could | 
:::warning
Não faremos

::: |
| Criar script para "esquentar cache" |    |    |    | Altíssimo | :x: | Won't | 
:::warning
Não faremos

::: |