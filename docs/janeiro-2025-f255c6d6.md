<!-- title: Janeiro 2025 | url: https://outline.seazone.com.br/doc/janeiro-2025-EGTKUjMXcl | area: Tecnologia -->

# Janeiro 2025

`<palestrinha>`

Fala pessoal como vão ? Passando pra trazer mais uma edição da nossa querida, amada, honrada, idolatrada e adorada TechZone :heart_on_fire: o lugar onde você encontra as maiores novidades da área de tecnologia da seazone :rocket:

`<palestrinha>`\n

## Desafio do mês 

Esse aqui é pra saber se vocês andam lendo a techzone :eyes: , a ideia é que vocês respondam uma pergunta simples através dos comentários da página  :rotating_light:SEM USAR O CHATGPT :rotating_light: (somente a última techzone pode ser usada para pesquisa) , aqui vai a pergunta : 

> O que é e pra que serve um MVP ? 

 *respondam através dos comentários **💬***

# Números do mês :1234:

### Taxas AWS - Governança 

Até o mês de novembro, apenas as contas Seazone-Technology e Seazone-Manager estavam configuradas com CNPJ ativo, o que gerava a cobrança de impostos sobre os serviços associados a essas contas específicas. No entanto, a partir de dezembro, foi necessário adicionar o CNPJ em todas as contas vinculadas à AWS, em conformidade com os requisitos legais aplicáveis (mais informações disponíveis https://aws.amazon.com/pt/legal/aws-sbl/).

Essa mudança resultou na aplicação de impostos sobre todas as contas da organização na AWS, aumentando significativamente os custos tributários para o mês de dezembro. A alteração impactou nosso planejamento financeiro, gerando um custo adicional no mês de R$ 4.548 apenas em impostos.

### Aumento do MAPE

Observamos um aumento acentuado no erro MAPE de 15 dias (principal KPI) no período de final de ano, conforme demonstrado no gráfico abaixo.\n ![](/api/attachments.redirect?id=8538a648-58d3-4eed-95b0-26b3664b512b " =1005x341")

**Causas Identificadas:**

* **Bloqueios de Imóveis:** Grande número de imóveis com bloqueios de final de ano, comportamento similar a reservas, o que dificultou a detecção pelos modelos.
* **Sensibilidade a Outliers:** O MAPE é sensível a valores discrepantes, e os altos valores de reserva no final de ano elevaram o percentual de erro, gerando desvios significativos nos cálculos.


**Decisão tomada:** Ao compartilhar o cenário com a diretoria, chegamos à conclusão de que não precisaríamos fazer nada sobre isso, pois para análises de faturamento da região é importante ter uma estimativa de ganhos no período de réveillon.

**Exemplo de Impacto:** No dia 06/01/2025 (pico do MAPE de 15 dias), os imóveis apresentaram erros superiores a 1800%, com bloqueios de ano novo não detectados. Como pode ser visto na próxima imagem: \n ![](/api/attachments.redirect?id=25eaf458-78b6-4d2b-b828-364a4b2a19bc " =678x281")

**Status atual:** Como pode ser observado no gráfico, após o período do réveillon, o erro MAPE vou ao seu patamar normal, próximo a 30%.

# O que ta rolando **👀**

o que teve de bom no último mês ? e de ruim ? 

## Lançamento da Wallet :tada:**🎉**

Pra quem ainda não sabe, a **Wallet** é a nova plataforma da Seazone! 🚀 Ela foi criada para funcionar como uma carteira digital, voltada para proprietários, franqueados e parceiros da Seazone. Recentemente, finalizamos a primeira versão dessa plataforma, destinada apenas a **proprietários**, e já liberamos para que os proprietários Seazoners comecem a fazer os primeiros testes. 🎉 

 ![](/api/attachments.redirect?id=974b27a8-0f1e-47a2-bfef-fbe26028cd97 " =261x438")


## Novo Menu do Sapron :round_pushpin:

O novo menu do Sapron foi pensando para melhorar a usabilidade do produto: ao deixar as funcionalidades agrupadas pelos universos Operacional, Financeiro, Proprietário, Anfitrião e Parceiros, as áreas internas da Seazone agora acessam com mais facilidade suas tarefas diárias. Além disso é possível favoritar as funcionalidades mais utilizadas no dia-a-dia na página principal, otimizando a produtividade das equipes!


 ![](/api/attachments.redirect?id=ae4f5ed8-b684-45b3-b1f7-fc0f16c4ce0e)

## Google Hotéis

O Google Hotels é uma iniciativa desenvolvida pelo time de reservas com o objetivo de promover nossos imóveis diretamente na plataforma do Google. Esses anúncios direcionam os clientes ao site da Seazone, facilitando o processo de reserva e, como resultado, aumentando o número de acessos, reservas e o faturamento da empresa.

Atualmente, o Google Hotels já está em operação e contribuindo para o crescimento do tráfego em nosso site

[Clicando aqui](https://www.google.com/travel/hotels/entity/CgsQpeHwk773oM2KARAC/overview?g2lb=43807868&utm_campaign=sharing&utm_medium=link&utm_source=htls&ved=0CAAQ5JsGahcKEwjgk4fmp4yLAxUAAAAAHQAAAAAQBA&ts=CAEaIAoCGgASGhIUCgcI6Q8QAxgMEgcI6Q8QAxgSGAYyAhAAKgkKBToDQlJMGgA) :point_left: você consegue ver um dos nossos anúncios no google 

e pra quem quer saber como andam nossos números na plataforma até o momento :point_down:

 ![](/api/attachments.redirect?id=abd9549f-2e8d-4b05-a846-ebb1e8472859 " =448x227")


## Metabase em novo endereço :world_map:

Pra quem ainda não ficou sabendo, estamos migrando o nosso Metabase para dentro do `cluster Kubernetes`! 🚀 Essa migração traz algumas mudanças, incluindo a própria URL do Metabase, que vai deixar de ser `metabase.sapron.com.br` e passar a ser `metabase.seazone.com.br`.

Mas por que estamos fazendo essa migração? 🤔 Bom, o `Kubernetes` oferece um ambiente mais seguro, resiliente (ou seja, resistente a quedas) e escalável. Isso significa que a Seazone pode crescer sem que o Metabase fique sobrecarregado ou sofra com isso. 🙌


# O que vem por ai **🔍**

### Migrar aplicações restantes para o cluster

Assim como fizemos com o Metabase, estamos trabalhando para migrar nossas aplicações de tecnologia para um ambiente mais resiliente e escalável. 🚀 Atualmente, já temos algumas aplicações rodando no cluster, e nossa meta para o início deste tri é migrar as restantes. 🙌

### Novo fechamento 

Em fase final de desenvolvimento, o novo fechamento prevê mudanças significativas no processo financeiro, tendo como principais objetivos:

* **Escalabilidade**: o processo de fechamento torna-se mais fácil de ser processado, pois ele apenas processa o que é dado novo a cada dia, diferentemente do fluxo anterior, que regerava todo o fechamento da Seazone desde 2019 até hoje todos os dias, tornando a sua escalabilidade algo crítico. 
* **Eficiência**: dados serão mostrados em tempo real. Atualmente para contabilizar quaisquer dados financeiros relacionados ao fechamento (reservas, ajustes, despesas) é necessário aguardar o processamento de dados, que ocorre na madrugada de um dia para o outro. Desta forma clientes finais e o time do fechamento precisa aguardar o dia seguinte para ver seus ganhos e saldo final somente no dia posterior. Com o novo fechamento os dados passam a ser refletidos no momento em que entram no banco, não sendo mais necessário aguardar o dia seguinte.
* **Redução de custos**: atualmente o processamento de dados do fechamento tem um custo médio de 8 dólares por dia. Isso equivale a uma média de $240 por mês e $2880 por ano. Com o novo fechamento não teremos mais este custo, uma vez que o processamento não mais será realizado pela AWS (serviço da Amazon de armazenamento e processamento de dados).
* **Manutenção de código**: atualmente o fechamento realiza lógicas complexas de processamento de dados e fica armazenado AWS, o que dificulta muito a manutenção do código, impactando na escalabilidade e desenvolvimento de soluções que tornam o processo mais ágil. O novo fechamento estabelece lógicas mais simples e torna mais acessível ao time de desenvolvimento a manutenção do código, facilitando a resolução de problemas e escalabilidade do processo.\n\nPara acessar a documentação completa clique [aqui.](https://outline.seazone.com.br/doc/fechamento-sapron-JefcFvVmTK)

### Refatoração Stays

Nova implementação da engenharia em relação a como funciona nossa comunicação tech com a plataforma Stays, melhorando a resiliencia dos nossos sistemas e aumentando a escala com que ocorre a comunicação.

#  Olá mundo **🌍**

Essa é a seção onde apresentamos um dos nossos times da tech, quais são as responsabilidades desse time e claro a parte mais importante, mostramos quem são os membros desse time e um pouco da função de cada um 

> *O nosso time da vez será o Reservas***👇**

## O que ele faz **⁉️**

O time tech de Reservas da Seazone foca na experiência do hóspede, atuando no Website Seazone e em iniciativas como Google Hotels e programas de afiliados, sempre buscando reduzir fricções e melhorar a experiência do usuário final.

## Quem faz ele **⁉️**

| Quem é ?  | Qual é o papel ?  |    |
|----|----|----|
| Alysson Alcântara | **Desenvolvedor frontend** |    ![](/api/attachments.redirect?id=7a34f756-ee0c-4280-becd-09350a2fe34e " =75x75")   |
| Marcos Paulo  | **Desenvolvedor frontend** |    ![](/api/attachments.redirect?id=2a22008b-c741-4e2c-a13c-3669baa5c6bf " =75x75")   |
| Maria Fernanda | Desenvolvedora Backend |    ![](/api/attachments.redirect?id=b6e9cbe5-7fa4-4323-88f4-99d20c099bd0 " =75x75")   |
| Bernardo Antônio  | Desenvolvedor Backend |  ![](/api/attachments.redirect?id=e851fdd5-be97-48cd-b119-405f548808c6 " =75x75") |
| Roberto Campos | Gerente de desenvolvimento web |  ![](/api/attachments.redirect?id=9430a3ad-9cda-4ad8-bec1-bd01263b5174 " =75x75") |
| Marina Coimbra  | Coordenadora de Produto |  ![](/api/attachments.redirect?id=cdbb7a6e-aab8-4eb5-8b43-f2213715417a " =75x75") |
| Bruno Rodrigues | Analista de Design  |  ![](/api/attachments.redirect?id=12f6a9b5-800a-43ad-9819-092f880c1207 " =75x75") |

## Tecniquês for Dummies

Não entendeu algum termo que citamos aqui ? conteúdo abaixo pode te ajudar 

`Cluster Kubernetes`

*Um **cluster Kubernetes** é um conjunto de computadores que trabalham juntos para rodar aplicativos de forma organizada e eficiente. O Kubernetes gerencia esses computadores, distribuindo as tarefas de maneira inteligente para garantir que tudo funcione corretamente.*

`Kubernetes`

***Kubernetes*** *é uma ferramenta que ajuda a gerenciar e organizar aplicações em vários computadores de forma automática. Ele cuida de distribuir, ajustar e manter essas aplicativos funcionando de maneira resiliente e escalável.*

`Mape`

*O **MAPE** (Mean Absolute Percentage Error, ou Erro Percentual Absoluto Médio) é uma métrica usada para medir a precisão de modelos de previsão ou análise de dados. Ele indica, em média, o quão distante as previsões estão dos valores reais, em termos percentuais. No contexto Seazone, o MAPE expressa o erro entre o valor real de faturamento de um imóvel Seazone (obtido a partir do Sapron) e o valor inferido pelos nossos algoritmos de predição de faturamento a partir de dados scrapados dos nossos imóveis. Quanto mais próximo de 0%, menor é o erro, logo, melhor é o resultado.*