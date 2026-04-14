<!-- title: Análise de Latência: AWS Brasil vs Oregon | url: https://outline.seazone.com.br/doc/analise-de-latencia-aws-brasil-vs-oregon-EOqTLOIhL7 | area: Tecnologia -->

# 🌐 Análise de Latência: AWS Brasil vs Oregon

# Detalhamento dos Testes

Esta seção tem como objetivo detalhar a metodologia adotada para a realização dos testes.

Inicialmente, a proposta era subir toda a aplicação do backend em um servidor localizado na região sa-east-1 (São Paulo). No entanto, durante esse processo, surgiram algumas dificuldades técnicas, o que nos levou a adotar uma abordagem alternativa.

Optamos, então, por focar especificamente na rota `/reservations/create`, que, conforme apontado no documento [Perfomance | Análise API de Criação de Reserva](/doc/perfomance-analise-api-de-criacao-de-reserva-A0i47iz5Uh) é uma das mais críticas em termos de desempenho. Ainda segundo esse documento, foi evidenciado que essa rota realiza chamadas para diversos serviços externos, como a Stays e o Auth0.

A partir dessa análise, foi definido o seguinte procedimento: identificamos os endpoints da Stays e do Auth0 acionados pela rota `/reservations/create` e desenvolvemos um script específico para realizar chamadas diretamente a esses endpoints.

Essa abordagem permitiu simplificar a comparação de latência, eliminando a necessidade de subir toda a aplicação backend, bastando apenas executar o script nas duas máquinas distintas: uma localizada na região de Oregon (us-west-2) e outra em São Paulo (sa-east-1).

# Detalhamento das etapas analisadas

Conforme detalhado no documento [Perfomance | Análise API de Criação de Reserva](/doc/perfomance-analise-api-de-criacao-de-reserva-A0i47iz5Uh), a rota `/reservations/create` percorre diversas etapas. Neste teste, iremos contemplar todas elas:

* Atualizar/Criar usuário no Auth0;


* Atualizar/Criar cliente;
* Obter disponibilidade do imóvel;
* Obter informações do cupom;
* Calcular preço com cupom (verifica se ele é válido);
* Calcular preço final com cupom;
* Calcular preço final sem cupom;
* Criar a pré reserva.

# Resultados Obtidos

Como mencionado anteriormente, os testes foram realizados por meio da execução de um script em cada uma das máquinas. Esse script foi executado 10 vezes em cada ambiente, com o objetivo de obter uma média representativa e fornecer uma visão geral do desempenho. Abaixo, apresentamos os resultados obtidos, organizados por etapa do processo.

| Etapa | Média Oregon (ms) | Média SP (ms) | Diferença (ms) | % |
|----|----|----|----|----|
| Atualizar/Criar usuário no Auth0 | 281.15 | 500.34 | **==-219.19==** | **==−77,96==** |
| Atualizar/Criar cliente | 578.73 | 486.55 | **==92.19==** | **==+15,93==** |
| Obter disponibilidade do imóvel | 335.43 | 217.37 | **==118.07==** | **==+35,20==** |
| Obter informações do cupom | 286.10 | 196.96 | **==89.14==** | **==+31,15==** |
| Calcular preço com cupom (verifica se ele é válido) | 330.03 | 170.65 | **==159.38==** | **==+48,29==** |
| Calcular preço final com cupom | 291.47 | 206.60 | **==84.87==** | **==+29,12==** |
| Calcular preço final sem cupom | 285.93 | 437.18 | **==151.25==** | **==+52,90==** |
| Criar a pré reserva | 670.32 | 473.48 | **==196.63==** | **==+29,33==** |


Observa-se que todas as etapas apresentaram ganhos de desempenho positivos, com exceção da etapa relacionada à criação do usuário no Auth0. No entanto, como já há planos para mover essa operação para uma task assíncrona, esse ponto não representa um impeditivo. Além disso, os ganhos expressivos observados nas demais etapas reforçam a efetividade da solução adotada.

# Fontes de dados

Como mencionado várias vezes nesse documento, os testes foram realizados via scripts. Para encontrar esses scripts e outros arquivos relevantes, clique [aqui](https://drive.google.com/drive/folders/1ddEGDMDMluWKi9GHYceWLyMSvDE4aLbS?usp=sharing).