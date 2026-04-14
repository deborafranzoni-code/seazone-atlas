<!-- title: Mapeamento de Features Sirius 2 0 | url: https://outline.seazone.com.br/doc/mapeamento-de-features-sirius-2-0-wU3XJpk32Y | area: Tecnologia -->

# Mapeamento de Features Sirius 2 0

Plano de ação:

[Plano de ação - Sirius 2.0](/doc/plano-de-acao-sirius-20-dl5J2DXUVE)

# Links úteis


 1. **RM day:**
    * **Gravação 1:** [Link](https://drive.google.com/file/d/16u_EMwp0SsoS4_qAyN5pjYHf2tpxdlZ8/view)
    * **Gravação 2:** [Link](https://drive.google.com/file/d/1El_7ExFpGskq-k34kjB3kGCnpJFaBoHT/view)
    * **PPT:** Link
 2. **MVPs Sirius 2.0:**
    * **Precificação:** [Link](https://docs.google.com/spreadsheets/d/1ZB3375qEemCQiriJEIegF2ejp6OEaYVaMqj-hnotBfE/edit#gid=491909812)
    * **Supervisório:** [Link](https://docs.google.com/spreadsheets/d/1bm7ALsMf-Lq_btMZO32jsmx0Xt7P-WkWgeFzYFxOkqg/edit#gid=26144235)
    * **Avaliação de anúncios:** [Link](https://docs.google.com/spreadsheets/d/10on1XkB0AOMBe5BnZb9YxuN3Jyhx7Hg7VM6y8HHZJwo/edit#gid=1471370361)
    * **Avaliação de desempenho:** [Link](https://docs.google.com/spreadsheets/d/11km0fxM5sPE0gweaGh-jgrYCY9Ny784SLmiOKUyA6jg/edit#gid=1879791925)
    * **Onboarding:** pela documentação do Notion ainda não tem ❌
 3. **Documentação dos novos processos de RM:** [Link](https://www.notion.so/Mapeamento-de-processos-antigo-b3ac8c2670964dc189ed1381705196b8?pvs=21)

    
    1. Processos desenhados no Lucid Chart: [Link](https://lucid.app/lucidchart/0186864b-b291-4939-9e2c-0ac21c811ec1/edit?beaconFlowId=8E7E221F58864DD7&invitationId=inv_6d1442ad-b9df-4676-ac86-e73a629779b2&page=0_0#)
 4. **SLAs que RM deve atender:** [Link](https://www.notion.so/Lista-de-SLAs-13302294c926480f9b030ccd89e0ee82?pvs=21)
 5. **KPIs do RM:** [Link](https://docs.google.com/spreadsheets/d/1HkVrLidfr6017F0x0htP_a32nz5pDI6W2y5lt7KtTZ8/edit#gid=0)
 6. **Sirius 1.0:**
    * Planilha de Input do Sirius: [Link](https://docs.google.com/spreadsheets/d/1DsdlDgLhCTL0v3sFEfQ6sPPGeP0ziaS6DYlWbZD6UhA/edit#gid=1016051317)
    * Planilha Geral de Controle: [Link](https://docs.google.com/spreadsheets/d/1aZa9i5nPZEgy_E6_GSxndgycd2YyuERaHWhpPMWAuNY/edit#gid=635301258)
    * Documentação no Notion: [Link](https://www.notion.so/517f1afa61364979b3b7ea28dcdd6ee4?pvs=21)
 7. Livro recomendado: The Theory and Practice of Revenue Management - Talluri
 8. Página da Wheelhouse com artigos sobre RM: [Link](https://www.usewheelhouse.com/research/pricing-engine)
 9. Nova planilha de inputs do Sirius (2.0): [MVP Inputs Sirius 2.0](https://docs.google.com/spreadsheets/d/1EVVswYE0DAlAnmpi-73_kxB9tlUUYd8Al26U63vHUCU/edit#gid=1150791990)
10. Diagrama de warnings: [Link](https://app.diagrams.net/#G1jZU9fqGhtipDfWfPuHhOvI2IcQ2ZG-Wh)
11. Diagrama do fluxo de precificação: [Link](https://app.diagrams.net/#G1xG0wn-335aLkGkoZim8h2Jea5SlqouF6)


---

# Reunião 30/06/2023 - Probst, Campana, Padilha

Gravação da reunião: [Link](https://drive.google.com/file/d/1rjYrw7QrayLL_RqWUKPYi5uzWYGQaOEY/view)

## Anotações Campana

Parte crítica do MVP é Precificação.

### Dados e AWS

→ daily revenue para todas as datas ativas do imóvel

→ bao para todos os concorrentes dos imóveis

→ details para detalhes dos imóveis

→ location para localização dos imóveis

### Inteligência

Processo de Definição de Concorrentes

Como definir os concorrentes, baseado no imóvel?

Processo de Definição de Concorrentes Plus

Como definir os concorrentes plus? (imóvel que vai bem ao longo dos meses) , medida de segurança operacional

Agrupamento de Períodos de Interesse

Como separar períodos quentes e frios e/ou agrupar períodos de interesse?

Previsão de Ocupação

Como prever a ocupação dos concorrentes?

Análise de preços a partir da previsão de ocupação

## Anotações Padilha

O RM terá 5 processos importantes: Precificação, Onboarding, Avaliação de Anúncios, Avaliação de Desempenho e Sistema Supervisório.

### Precificação:


1. Seleção de concorrentes:

   
   1. Usa a daily revenue para as datas ativas/futuras de cada imóvel a ser precificado → **dados**
   2. Usa a block and occupancy de todos os concorrentes, para todos os imóveis (**dados**). Os concorrentes são: mesma cidade, bairro (tabela location, **dados**), quartos, listing type (tabela details, **dados**) que estão dentro de uma faixa de faturamento (percentil entre X e Y) → **inteligência**
2. Seleção de concorrentes plus:

   
   1. Seleciona os concorrentes plus, que são aqueles concorrentes que vão bem com constância, ou seja, faturam bem todos os meses, fotos são profissionais, tem um rating bom, comentários recentes, é super host etc → **inteligência**
   2. Os concorrentes plus são concorrentes que caso a área de RM fique desfalcada, podem ser copiados para manter um bom nível de funcionamento de precificação
3. Separação de períodos:

   
   1. Achar períodos similares que devem podem ser precificados em conjunto (períodos quentes e frios) → **inteligência**
   2. Idealmente cada dia individual deve ser precificado, isso não é feito pois RM não tem braço suficiente
   3. Porém caso o analista precise avaliar manualmente um certo listing, ele pode ver os períodos de interesse para assim fazer
4. Predição de ocupação:

   
   1. Tenta prever a ocupação dos concorrentes nos próximos meses a partir da ocupação medida no dia de hoje e das ocupações medidas nos anos anteriores → **inteligência**
5. Análise de preço:

   
   1. Define um preço de acordo com a predição de ocupação, de acordo com o preço que os concorrentes gerais estão pedindo, de acordo com o preço que os concorrentes plus estão pedindo e/ou de acordo com o preço histórico dos anos anteriores → **inteligência**

**Tabelas que o RM precisa para inputar dados (precisa?):**

seazone_id | percentil_min_concorrentes | percentil_max_concorrentes

Não deu tempo de passar pelos outros processos, agendamos uma outra reunião com o Probst em 12/07/2023.


---

# Reunião 03/07/2023 - Campana, Padilha

* Dificuldades:
  * conseguir definir onde será possível customização/input do usuário;
  * e onde será apenas visualização
    * Gráfico de ocupação atual vs previsão pro d+0;
    * Listas de concorrentes e plus;

Período de desenvolvimento: Julho, Agosto, Setembro, total 90 dias, 6 sprints e meia.

**1 Sprint - 03/07/2023 até 12/07/2023**

* Planejamento (calls, investigação, definições de features, expectativas etc)
* Setup (conta, CI/CD, definição de tags)
* Arquitetura de Dados (tabelas necessárias, cross-account bucket, orquestração e recursos da AWS)

**2 Sprint - 13/07/2023 a 26/07/2023**

* **Verificar com Probst:**
  * Você ficaria satisfeito com o MVP (planilhas) do sirius na AWS?
  * Oque você quer ver e o que você quer dar input?
  * Qual vai ser o requerimento de execução (frequência)?
  * O quanto temos a liberdade de modificar os métodos utilizados?

3 Sprint - ..

4 Sprint

5 Sprint

6 Sprint


---

# Reunião 04/07/2023 - Campana, Padilha, Júlio Monteiro

Gravação da reunião: [Link](https://drive.google.com/file/d/1m4E80TLSb92XaXhSGBzLO3ONwgndJZuX/view)

Planilha de input do Sirius 1.0: [Link](https://docs.google.com/spreadsheets/d/1DsdlDgLhCTL0v3sFEfQ6sPPGeP0ziaS6DYlWbZD6UhA/edit?pli=1#gid=1016051317)

### Sirius 1.0

Júlio passou com a gente pela "Planilha de Input do Sirius".

Preço final = "Preço Base" + "Preço variável"

**Preço Base:** O Sirius 1.0 é baseado em preços para o mês inteiro, que é chamado de "Preços Base". Os "Preços Base" são feitos de acordo com o "mercado", e os dados do mercado são na verdade os dados da BaO. O preço enviado para a Stays é *max(Preço Base, Preço Mínimo)*.

**Setup Grupos:** Todo imóvel que será precificado tem que estar na "Setup Grupos", que é uma tabela que indica quais "grupos" cada imóvel pertence (ex.: SC - Serra).

O Sirius 1.0 funciona com uma infinidade de regras que se sobrepõe, então por exemplo: a estadia mínima de uma região é 1 dia, mas se for um certo condomínio é 2, mas se for num certo feriado, é 4, mas se … etc etc etc. O mesmo é válido para os preços!

Regras de gap:

Comentário meu:

* a parte de preços mínimo a pedido do proprietário são inputs que virão APÓS o novo processo de precificação. O preço mínimo pode ser por MÊS, ou por FERIADO ou GLOBAL ("infinito");
* A operação também pede um preço mínimo de R$100,00;
* também tem a parte de preços máximos, que influencia o "Preço final". Ela foi utilizada por exemplo para definir um preço fixo para os móveis de Vistas de Anitá, já que o preço mínimo e máximo são setados com o mesmo valor;
* também seria necessário uma parte de "preço fixo" que sobrescreve qualquer preço setado pelo analista ou modelo de precificação.


---

# Alinhamento 04/07/2023 - Padilha e Campana

Após uma conversa com o Bill, ficou decidido que todos os componentes do Sirius 2.0 devem ser implementados, e a opção para fazer isso caber no tri é uma implementação mais simples, com escopo menor (principalmente na predição de ocupação, que parece estar muito complicada).

Por isso podemos pensar em várias "caixinhas" com input e output bem definidos para criarmos o Sirius 2.0. A vantagem é que poderemos dividir este desenvolvimento em mais devs, em paralelo.

Abaixo um esboço dessas caixinhas, perceba que há mais caixinhas do que MVPs do Sirius 2.0 feitos por RM, o que é proposital, para ficar mais bem dividido.

## Seleção Concorrentes

## Precificação

**Entrada**:

Imóveis a serem precificados (inicialmente todos), bao, dr, concorrentes

**Saída**:

* Uma tabela onde cada linha representa a combinação de imóvel, uma data (diária), preço sugerido.

## Comunicação com Stays

**Entrada**:

* Lista de precificação dos imóveis.

**Saída**:

* Lista de preços finais dos imóveis para cada data do calendário.

**Processos/Features**:

* Preço mínimo
* Definir preço máximo
* Definir preço fixo
* Gapper v1.0
* Escada de preços para imóveis

## Análise de Anúncios

## Processo Supervisório

## Processo de Onboarding

## Avaliação de Desempenho


---

# Reunião 05/07/2023 - Campana, Padilha, Rodrigo Ribeiro

Gravação da reunião: [Link](https://drive.google.com/file/d/155b8cl00ii0oh5XWjZnUZ6_q8vKPbZMT/view?pli=1)

## Anotações Padilha

Uma das coisas que ele mais faz é onboarding: sempre que entra um imóvel novo, é feito um "estudo" sobre esse imóvel olhando para os preços do mercado.

**Planilha Geral de Controle:** é para ficar avaliando o desempenho dos anúncios (para, por exemplo, pedir para o pessoal refazer algum anúncio), fazer experimentos, análise de cenários, olhar como estão os calendários dos imóveis (aba "Calendário") para dar descontos etc.

**Planilha de Input do Sirius:**

* ele reclamou da mesma coisa que o Júlio:
  * se tiver espaço, quebra o Sirius 1.0
  * se o número for um float, quebra o Sirius 1.0
* hoje eles só fazem precificação (e.g. experimentos e ajustes finos) para os próximos 2 meses, os outros meses são feitos pelo "Preço Base" (que não é alterado)
  * a precificação é feita 4x por semana, 2x pro mês atual e 2x pro mês seguinte
  * o Sirius manda esses

**MVP de Precificação:**

Ele trabalhou no [MVP de Precificação](https://docs.google.com/spreadsheets/d/1ZB3375qEemCQiriJEIegF2ejp6OEaYVaMqj-hnotBfE/edit#gid=491909812), na parte de Predição de Taxa de Ocupação:

* Diferentemente do Probst, que fez de forma manual, ele usou o Prophet para estimar essa taxa de ocupação

**MVP de Avaliação de Desempenho:**

Ele também trabalhou no [MVP Avaliação de Desempenho](https://docs.google.com/spreadsheets/d/11km0fxM5sPE0gweaGh-jgrYCY9Ny784SLmiOKUyA6jg/edit#gid=1879791925):

* é avaliado a média de faturamento de cada imóvel/mês e compara com a média dos mesmos tipos de imóveis da região
* o mais crítico é identificar quando um imóvel está performando ABAIXO do esperado

**Processo de Onboarding:**

* é um processo bem manual pois eles olham as fotos para definir se o imóvel Jr., Sup., Top, Master etc.

**Ideias que ele acha que podem ter no Sirius 2.0:**

* eliminar a quantidade gigantesca de regras que se sobrepõe no Sirius 1.0, i.e., automatizar mais o processo de precificação


---

# Alinhamento 05/07/2023 - Padilha e Victor Guindani

O foco do Victor em RM é aumentar a % de reservas do Booking. Mandei uma mensagem para ele para saber se o Sirius 2.0 tem potencial de ajudar nisso, ele acha que não:

"*A planilha de input do Sirius eu não cheguei a usar.*

*Os dados do BD eu uso toda hora.*

*Não me vem nada em mente de algo específico para ajudar a impulsionar as reservas.*

*Até porque, acredito que a **maiorias dos programas do Booking so são possíveis de "setar" na própria plataforma**. De resto acredito que o Booking replicaria o preço dos anúncios do airbnb (na questão de regras para feriados, preço mínimo, etc)*

***A única coisa que difere é a % de incremento. No Booking incrementados o preço que o Sirius fornece a Stays em 25%.***

*Acho que no airbnb é 10%. **Mas isso é feito na Stays então não sei se vai mudar para o Sirius.**"*


---


---

# Reunião 06/07/2023 - Campana, Padilha, Márcio Fazolin

Gravação da reunião: [Link](https://drive.google.com/file/d/18zrZfYYMYA0YTZfZz033eViVIFLfok0y/view)

## Anotações Padilha

Ordem de aplicação das regras:


1. Regras percentuais
2. Regras de valor mínimo e valor máximo

Coisas que quebram:

* Tabela apartment (?) → **Banco de dados PMS**
* Precisa saber quando tem reserva. Para isso a Stays é lida, e às vezes essa API crasha. A Stays usa um sistema de IDs próprio.

Coisas para melhorar:

* hoje o script de precificação roda para todos os imóveis de uma só vez. Não tem a opção de mudar o preço de apenas 1 imóvel de cada vez.

Minha impressão:

* Há muitas regras específicas para alguns hotéis de Florianópolis (ILC e JBV).


---

# Reunião 07/07/2023 - Campana, Padilha, André Crescenzo

Gravação da reunião: [Link](https://drive.google.com/file/d/1zOkb4laOF4hYRyhxQZrSR79ObPOEGWnb/view)

TCC do André Crescenzo: [Link](https://www.youtube.com/watch?v=RygEVyONwXs)

Livro recomendado: The Theory and Practice of Revenue Management - Talluri

Página da Wheelhouse com artigos sobre RM: [Link](https://www.usewheelhouse.com/research/pricing-engine)

Comecei explicado o funcionamento do Sirius do ponto de vista de usuário e o funcionamento do Sirius do ponto de vista de plataforma para o André, para confirmar se a gente tinha entendido como o Sirius 1.0 funciona.

## Comentários do André Crescenzo:

O grande desafio é precificar de forma otimizada. Conseguimos utilizar a Stays para setar os preços por dia, porém não conseguimos aplicar diversas regras de negócio na Stays, por isso precisamos utilizar uma solução (que é o Sirius) para precificar os dias ANTES de mandar pra Stays.

De maneira geral as regras de negócio são da estrutura:

* Se isso → então aquilo
* Exemplo:
  * Se é fds → então aumente o preço
  * Se a agenda está vazia → então diminua o preço

As regras funcionam de forma cumutativa (tanto faz a ordem que são aplicadas) ou também as regras de máximo e mínimo (que é aplicado no fim).

O André fez o TCC dele em RM e isso gerou o Sirius.

Ele disse que a questão de Oferta e Demanda não funciona muito bem e que apenas seguir essa lógica pode não gerar preços tão bons em alguns imóveis, em cenários mais específicos. Ele nos mandou algumas fontes para ler sobre o assunto.

O sonho dele seria utilizar Aprendizado Não-Supervisionado (Algoritmo Genético): pensar no conjunto de regras como sendo um cromossomo, aplicamos uma mutação, e as mutações (regras) que funcionam bem iriam se espalhar, as que não funcionam bem não iria se espalhar.

Campana explicou que a ideia é usar séries temporais, utilizando o histórico do próprio imóvel e as ocupações dos concorrentes.

Ele recomendou quebrar os processos do Sirius 2.0 em várias contas diferentes da AWS, mas sabendo que quanto mais dividido, mais interfaces isso gera.

Ocupação geralmente segue uma curva exponencial (quanto mais perto do dia em questão fica exponencialmente mais próximo da ocupação final do dia em questão).

O Sirius 1.0 loga 8x por dia todas as regras de negócio aplicadas e os preços definidos.

Linhas tarifárias (descontos por duração de estadia) criam ainda outra complicação.

A Stays talvez não deixe dar um preço diferente para o Airbnb e para o Booking (deixa apenas settar um markup diferente para as duas plataformas).


---


---

# Reunião 12/07/2023 - Campana, Padilha, Probst

Gravação da reunião: [Link](https://drive.google.com/file/d/1vOaC38AoH6z5cAdEpYXcpI2fl9VPz3mk/view)

## Anotações gerais:

### Sistema supervisório:

Olha para os imóveis da Seazone num primeiro momento. Para cada mês ativo do calendário (d0 + 180 dias) e imóvel, tenta identificar onde houve ganho de ocupação expressivo. Não é comum, por exemplo, ver um grande ganho de ocupação daqui 6 meses.

Mas o cerne da questão é ver se estamos vendendo reservas muito barato.

Fechando em:

* identificar média mensal das DIÁRIAS (não necessariamente reservas) que estão muito baratas em relação aos **concorrentes (seleção de concorrentes)**
  * para dizer se está muito barato, ordenamos os preços dos concorrentes e classificamos qual percentil o imóvel da Seazone ocupa
  * se estiver abaixo de um percentil **threshold**, emite o alerta
    * o threshold pode mudar de mês para mês, por exemplo, em janeiro a régua sobe pois esperamos um comportamento melhor dos imóveis
    * podemos experimentar com o preço direto da diária, ao invés da média mensal SE o sistema de precificação estiver funcionando bem e não forem lançados uma infinidade de alertas

Formato imaginado da tabela do supervisório. O analista pode filtrar, por exemplo, apenas os listings que estão com preço médio mensal abaixo do "percentil 5%".

| **listing id** | **mes** | **preço médio mensal** | **percentil 5** | **percentil 10** | **percentil 20** | **percentil 40** | **less than** |
|----|----|----|----|----|----|----|----|
| JBV108 | janeiro | R$250,00 | R$100,00 | R$150,00 | R$220,00 | R$400,00 | percentil 40 |
| JBV120 | janeiro | R$80,00 | R$100,00 | R$150,00 | R$220,00 | R$400,00 | percentil 5 |

### Avaliação de Anúncios:

Quer ver quais anúncios estão bons ou ruins, com tendência de melhora ou piora. "Bom" ou "ruim" é basicamente a nota consolidada do imóvel. *Mas também podemos avaliar os comentários com um dicionário de palavras "proibidas" ou análise de sentimento.*

Vai olhar para a tabela details.

* Busca todos os imóveis da Seazone → seazone_details
* Olha as avaliações de cada imóvel (global) e as últimas avaliações dele. Vai querer focar na tendência de variação das avaliações.
* Análise 1:
  * Imóveis com nota total abaixo de 4 → RM cria um pedido de recriação do anúncio
    * lembrar que o Airbnb ID muda quando o anúncio é recriado
  * O anúncio novo não vai ter nota, até ter 3 comentários (ou avaliações)
    * O "rating" dele será missing value → não dá pra avaliar se não tem nota, então devemos filtrar esses casos
* Análise 2:
  * Ver quais foram as notas dadas nos últimos 21 dias. Se a média dessas notas é menor que 3, RM manda um alerta para CS para investigar
* Output:
  * planilha avisando quais anúncios devem ser recriados

| seazone_id | average_rating |
|----|----|
| OKA106 | 3,8 |
| DME584 | 3,9 |
  * planilha avisando quais anúncios estão com tendência muito grande de queda

| seazone_id | Média das Últ. Avaliações | data do cálculo |
|----|----|----|
| MAV012 | 2,7 | 12/07/2023 |
| CHR101 | 3,0 | 12/07/2023 |
| CNU104 | 3,0 | 12/07/2023 |
| CCL004 | 3,0 | 12/07/2023 |
| RAI010 | 3,0 | 12/07/2023 |
| BOU201 | 3,3 | 12/07/2023 |
| MAV003 | 3,5 | 12/07/2023 |

## Anotações Padilha:

Conversamos sobre as atualizações da última semana e concordamos que seria melhor começarmos pelos processos mais simples (que não são os de precificação).


---

# Reunião 13/07/2023 - Campana, Padilha, Probst

Gravação da reunião: [Link](https://drive.google.com/file/d/1GPh-BDca5Fj2STkQ38tVODYMbL2dMrvE/view)

## Anotações gerais:

### Avaliação de Desempenho:

Objetivo é ver se o faturamento do imóvel está abaixo/acima da concorrência.

* Precisa da **seleção de concorrentes**
* Devemos tomar cuidado com a questão da antecedência
* Também deve fazer uma previsão de faturamento de acordo com a antecedência
* Provavelmente não terá input
* Deve ser feita em todos os imóveis ativos da Seazone
* Frequência: 1x por semana
  * A janela ideal seria para os próximos 180 dias, agregado por mês, caso não seja muito caro
* Tabela de exemplo de output para o RM utilizar nas análises:

| **id seazone** | **data hoje** | **mês analisado** | **antecedência** | **previsão de faturamento no fim do mês analisado** | **faturamento do mês analisado na data de hoje** | **faturamento médio da categoria no mês analisado na data de hoje** | **desv. pad.** | **fator z** | **situação** |
|----|----|----|----|----|----|----|----|----|----|
| JBV108 | 13/07/2023 | 08/2023 | 45 | R$ 10.000,00 | R$ 3.000,00 | R$ 5.000,00 | R$ 1.200,00 | -1,67 | abaixo da média |
| ILC2412 | 13/07/2023 | 08/2023 | 45 | R$ 15.000,00 | R$ 10.000,00 | R$ 7.000,00 | R$ 1.800,00 | 1,67 | acima da média |
| JBV110 | 13/07/2023 | 08/2023 | 45 | R$ 10.000,00 | R$ 4.200,00 | R$ 5.000,00 | R$ 1.200,00 | -0,67 | dentro da média |
| JBV108 | 13/07/2023 | 09/2023 | 75 | R$ 12.000,00 | R$ 5.000,00 | R$ 8.000,00 | R$ 2.000,00 | -1,5 | abaixo da média |
| ILC2412 | 13/07/2023 | 09/2023 | 75 | R$ 20.000,00 | R$ 10.000,00 | R$ 7.000,00 | R$ 1.800,00 | 1,67 | acima da média |
| JBV110 | 13/07/2023 | 09/2023 | 75 | R$ 12.000,00 | R$ 8.500,00 | R$ 8.000,00 | 2000 | 0,25 | dentro da média |

* Uma ideia é 1 dev ficar APENAS com "previsão de faturamento" e outro com o restante, ou então deixar a parte de "previsão de faturamento" para depois


---


---

# Reunião 14/07/2023 - Campana, Probst

Gravação da reunião: [Link](https://drive.google.com/file/d/1_V2IRNdEiHk-92NB5JEoyJP7GwBv_1VQ/view)

## Anotações gerais:

* **Precificação:**

  Objetivo é definir o melhor preço possível para cada data no futuro, para cada imóvel.

  Input:

  **Setup Groups** (criação de clusters por imóvel)

  Planilha: Inputs

| **Lista de Imóveis** | **Lista de Grupos** |
|----|----|
| ABC102 | Fase2 |
| ABC102 | ITA |
| ABC102 | Todas as Regras |
| ABC102 | Todos os imóveis |
| ABC1301 | Fase2 |
| ABC1301 | ITA |
| ABC1301 | Todos os imóveis |
| ABC1303 | Fase2 |
| ABC1303 | ITA |
| ABC1303 | ITAMASTER2Q |

  **Disponibilidade** (abertura de calendário)

  Planilha: Inputs

| **Group** | **Dias disponíveis max** |
|----|----|
| SC-LITORAL | 180 |
| SC-SERRA | 180 |
| SC-RESORTS | 180 |
| SC-CIDADE | 180 |
| RJ-LITORAL | 180 |
| SP-LITORAL | 180 |
| SP-SERRA | 180 |
| SP-CNA | 180 |
| RS-SERRA | 180 |
| RS-CIDADE | 180 |
| SC-VST | 180 |

  **Seleção de Precificação** (seleção da metodologia de cálculo a ser utilizada para gerar os preços finais)

  Planilha: Input

| **Imóveis** | **Metodologia de Precificação** | **Minimo de Faturamento** | **Máximo de Faturamento** |
|----|----|----|----|
| ABC102 | Automático | 0,75 | 0,9 |
| CNA001 | Manual | 0 | 0 |
| ILC001 | Automático | 0,5 | 0,9 |

  **Seleção de Concorrentes**

  Objetivo: seleção de concorrente baseado no faturamento que foi dado de input na "seleção de precificação".

  Planilha: Output

| **Imóvel** | **Concorrente** | **Link** |
|----|----|----|
| CNA001 | listing_id | [airbnb.com.br/](http://airbnb.com.br/doidera) |

  **Seleção dos Concorrentes Plus**

  Objetivo: selecionar concorrentes estrela dentro dos concorrentes selecionados. Seria um imóvel referência.

  **Output**: Deve ter a possibilidade de intervenção manual dos analistas na precificação (válvula de escape). Ou seja, deve haver uma interface (planilha) para o analista, antes de dar o input para Stays. Para os imóveis que a metodologia é "Manual", o preço não deve ser calculado e deve ser disponibilizado como uma célula vazia/com alguma aviso para intervenção do analista.

  Planilha: <https://docs.google.com/spreadsheets/d/1EVVswYE0DAlAnmpi-73_kxB9tlUUYd8Al26U63vHUCU/edit#gid=1949776377>


---

# Reunião 17/07/2023 - Campana, Probst, Padilha

Gravação da reunião: [Link](https://drive.google.com/file/d/1_LQwXoHJwOiCZXiojd7ionKkF2RwJswN/view)

Última reunião falaram sobre a precificação e começaram a esboçar uma [planilha](https://docs.google.com/spreadsheets/d/1EVVswYE0DAlAnmpi-73_kxB9tlUUYd8Al26U63vHUCU/edit#gid=1949776377) para tal.

## Anotações gerais:

Explicação sobre a planilha montada na última reunião pelo Probst e Campana.

Probst mostrou uma ideia da seleção de concorrentes dele: a ideia é, para cada imóvel, dar parâmetros para a seleção dos concorrentes, como:

* Cidades
* Bairros de cada uma dessas cidades
* Listing types
* Quartos
* Faixa mínima de faturamento
* Faixa máxima de faturamento

E os parâmetros para os concorrentes plus:

* Número mínimo de reviews
* Número mínimo de star rating
* Número mínimo de noites vendidas nos últimos 30 dias
* Se é superhost


---

# Reunião 18/07/2023 - Campana, Probst, Padilha

Gravação da reunião: [Link](https://drive.google.com/file/d/1C6M6BSVhDTb3ZiiwlF9QybewtG_L0uj5/view)

## Anotações gerais:

Voltando ao processo de precificação…

Assumindo que temos os concorrentes de um certo imóvel, PARA CADA DIA:

* para o grupo de concorrentes **gerais** iremos calcular os seguintes números:
  * ocupação no momento atual para cada dia futuro
  * faixas de preço (percentil 10%, 25%, 50%, 75% e 90%) no momento atual para cada dia futuro
  * ocupação nos anos anteriores
  * faixas de preço (percentil 10%, 25%, 50%, 75% e 90%) nos anos anteriores
* para o grupo de concorrentes **plus** iremos calcular os seguintes números:
  * ocupação no momento atual para cada dia futuro
  * faixas de preço (percentil 10%, 25%, 50%, 75% e 90%) no momento atual para cada dia futuro
* iremos pegar do **próprio imóvel**:
  * ocupação no momento atual para cada dia futuro
  * preços no momento atual para cada dia futuro
  * ocupação nos anos anteriores
  * preços nos anos anteriores
* apenas depois iremos agrupar por períodos (quer sejam quente/frio, semana, mês ou qualquer outra coisa)

Decidimos que é melhor não falar mais sobre as features do Sirius 2.0 antes de traçar o **plano de ação**. No plano de ação a ideia é colocar:

* quem vai ter disponibilidade de trabalhar no projeto, qual o nível de conhecimento da pessoa e o quanto vai poder se dedicar
* que iremos utilizar IaC para fazer o projeto
* quais partes irão ajudar a medir quais KPIs do RM
* quais partes irão ajudar a atender quais SLAs do RM


---

# Reunião 20/07/2023 - Campana, Probst, Padilha

Gravação da reunião: [Link](https://drive.google.com/file/d/128piLzpPkcQu-Us1uM67Hayj1C1Qz0Nm/view)

Discutimos o [plano de ação do Sirius 2.0](/doc/plano-de-acao-sirius-20-dl5J2DXUVE) (os detalhes foram anotados lá).


---

# Reunião 21/07/2023 - Campana, Probst, Padilha

Gravação da reunião: [Link](https://drive.google.com/file/d/14ZzQKrGosGTIY5LOP1Yphm2Qb_wTT_vh/view)

Detalhamos as tarefas do Gantt.


---

# Reunião 26/07/2023 - Campana, Probst, Padilha, Lucas

Gravação da reunião: [Link](https://drive.google.com/file/d/118V09YJYS13p3bL0Vi_Sls9c6WDPXhkA/view)

Discutimos o *CRUD*, que na verdade será apenas a planilha "setup groups".

* Deve ter uma planilha, **separada**, da "setup groups" que é o "inventário" de imóveis da Seazone e os seus respectivos grupos de pertencimento
* Inserção manual dos imóveis nesta planilha
  * consequência: inserção manual dos mesmos imóveis em todas as outras planilhas
  * Para amenizar este problema, fazer um esquema de **"warnings"**

Fizemos um diagrama para ilustrar o sistema:

[Sirius2.drawio](https://drive.google.com/file/d/1jZU9fqGhtipDfWfPuHhOvI2IcQ2ZG-Wh/view?usp=sharing)


---

# Reunião 27/07/2023 - Campana, Probst, Padilha, Lucas

Gravação da reunião: [Link](https://drive.google.com/file/d/1RxM_Sz6EOBOSvUT6_39CT_8Sjcc7gWrF/view)

Estamos discutindo o uso do Sirius no dia-a-dia e como os testes rápido serão estruturados.

Apenas 1 analista irá usar de cada vez. O fluxo será:


1. analista manda fazer precificação e a tabela com os preços é gerada (e a aba do sheets é preenchida);
2. analista clica em enviar os preços pra Stays, e depois a aba do sheets é limpa;
3. não é possível iniciar uma precificação (incluindo a automática) se a tabela de preços estiver preenchida (do contrário iria sobrescrever os preços).

Serão 3 botões feitos por AppScript:

* Executar Sirius:
  * Para todos os imóveis
    * Puxa todas as tabelas de configurações
  * Para selecionados
    * Puxa todas as tabelas de configurações e usa a aba de selecionados como filtro
* Dar output dos preços na planilha para visualização, não para edição
  * dia x imóvel x tarifa?
* Enviar Preços para Stays
  * Enviar do S3 para Stays (comunicar API)

# Reunião 02/08/2023 - Campana, Probst, Padilha, Lucas, Hideki

Gravação da reunião: Link

Estamos discutindo o uso do Sirius no dia-a-dia e como os testes rápido serão estruturados.

Apenas 1 analista

* Ata da reunião registrada diretamente no Plano de Ação do Sirius


---

# Reunião 02/08/2023 - Campana, Probst, Padilha, Lucas e Hideki

Gravação da reunião: [Link](https://drive.google.com/file/d/1kBL-1ri5jC5UOw-KJ0DNKm3zW8SGkabg/view)

Discutimos detalhes de implementação do fluxo AWS ↔ Sheets e Stays ↔ AWS. Os detalhes foram anotados diretamente no plano de ação.


---

# Reunião 04/08/2023 - Campana, Probst, Padilha, Lucas

Gravação da reunião: [Link](https://drive.google.com/file/d/15Np5t0S-InF6PtV4azo0k8vjj59faYsX/view)

### Definition of Done:

O Sirius 2.0 deve ser capaz de realizar algumas análises diariamente, para todos os imóveis da Seazone e para as datas abertas de calendário. São elas:

* Avaliação de anúncios: verificar quais anúncios estão bons e quais estão ruins (média de avaliações do Airbnb abaixo de um valor definido por RM), para que o time de analistas de RM possa pedir que sejam refeitos quando necessário.
* Seleção de concorrentes: selecionar adequadamente os concorrentes gerais e plus de cada um dos imóveis da Seazone em tempo real, limitando geograficamente pelos bairros da location
* Sistema Supervisório: garantir que não estejamos vendendo reservas abaixo de um percentil definido por RM (quando comparado aos concorrentes) ou, caso estejamos, que os preços potencialmente errados sejam trazidos à tona em tempo hábil
* **Precificação Automática,** utilizando concorrentes: utilizar as informações dos concorrentes para definir os preços dos imóveis, respeitando regras de preço e ocupação definidas por diversos agentes externos (Operação da Seazone, Proprietários, CS etc).
  * Permitir ainda que os preços sejam definidos manualmente caso a precificação baseada em concorrentes não seja considerada adequada (**Precificação Manual**)
* Análise de Desempenho: trazer à tona o faturamento dos imóveis da Seazone por mês ativo de calendário e a sua comparação com faixas de valores de faturamento dos concorrentes. A análise deve retornar, para cada imóvel-mês, uma flag de acima/abaixo/dentro do esperado de acordo com as circunstâncias momentâneas de cada imóvel-mês. Ainda deve destacar quais imóveis-mês possuem preços mínimos e número de dias bloqueados acima de X.
* Permitir que RM meça os [KPIs correspondentes](/doc/plano-de-acao-sirius-20-dl5J2DXUVE)
* Permitir que RM execute os processos desenhados no trimestre passado de maneira escalável, ou seja, para todos os imóveis da Seazone, todos os dias


---

# Reunião 09/08/2023 - Campana, Probst, Padilha, Lucas, Hideki, Márcio

Gravação da reunião: [Link](https://drive.google.com/file/d/12tUIw42Sb9btlTEpbWUaSTT6lXouf4by/view)

* Márcio aproveitou alguns artifícios do Sirius 1.0 no Sirius 2.0 de forma a ganhar tempo. Parte do código já existente foi aproveitado
* Hideki está trabalhando na comunicação com a Stays (AWS-Stays)
* Análise de Anúncios - análise da nota geral está encaminhada. Análise das notas médias em uma janela pode entrar em uma redução de escopo
* Lucas apresentou como está o andamento do MVP Sirius 2.0. O código está quase finalizado.
* Mostramos para o Márcio como que deve funcionar a planilha de seleção de concorrentes e concorrentes plus


---

# Reunião 16/08/2023 - Campana, Probst, Padilha, Lucas

Gravação da reunião: [Link](https://drive.google.com/file/d/15LbHut739fs2vjqK6kP8qRM0zdPTbC4U/view)

* Interface Stays e AWS foi terminada.
* Interface Stays com o Sheets está sendo feita com o envolvimento do Hideki. A task está um pouco travada. Em termos de avanço, estamos em cerca de 30% nessa task. O Burigo será envolvido no projeto para tentarmos adiantar os trabalhos. Ele pode ir trabalhando na parte da planilha enquanto o Hideki foca nos Lambdas.
* A avaliação de anúncios ainda não foi iniciada. Devido à demanda para o Hideki na task anterior, o Márcio pode ser envolvido nessa atividade de Anúncios. Deixamos isso como um plano B caso a interface atrase.
* A seleção de concorrentes foi finalizada pelo Márcio.
* Foi marcada uma call com o Artur para explicação breve da Análise Supervisória na sexta-feira.
* Avaliação de desempenho ficou com o Márcio e com o Rodrigo. Foi marcada uma reunião de Briefing para segunda-feira.


---

# Reunião 18/08/2023 - Campana, Probst, Padilha, Julio, Artur

Gravação da reunião: [Link](https://drive.google.com/file/d/1ecU_Nb3Z2vx4krMpjdO3JVw4LRgdCW0J/view)

* Essa reunião foi feita para apresentar ao Artur como funciona o sistema surpevisório no contexto do Sirius 2.0
* Foi mostrado o diagrama das planilhas e mostrado que o sistema supervisório se comunica com as planilhas Setup Grupos e Seleção dos Concorrentes
* Padilha apresentou o planejamento do sistema supervisório ao Artur no Notion
* Padilha criou uma planilha de exemplo de como seria a planilha do sistema supervisório, para auxiliar o Artur: <https://docs.google.com/spreadsheets/d/1Ly5AZV2drEYwzj1B9WOlnmpVPG3ZB5bW91Tik4T1-xQ/edit#gid=1770300547>
* Os dados dos concorrentes, no qual o Artur vai se basear, ainda não estão no S3. A ingestão dos dados deve ser feita junto ao Hideki, que poderá auxiliar no processo.


---

# Reunião 21/08/2023 - Campana, Probst, Padilha

Gravação da reunião: [Link](https://drive.google.com/file/d/1kXoEMj7cWmjOp_Nji04keN9OG6ib5OVf/view)

* Reunião para atualizar o Gantt e modificar escopo do projeto
* Ficamos preocupados com a conclusão do projeto dentro do tempo
* Decidimos colocar o Márcio e o Hideki juntos para finalizar a parte de integração Sheets ↔ AWS
* Decidimos focar em finalizar os módulos e fazer os deploys em produção para já ter produtos que RM possa utilizar


---

# Reunião 21/08/2023 - Campana, Probst, Padilha, Rodrigo, Lucas, Márcio

Gravação da reunião: [Link](https://drive.google.com/file/d/1kXoEMj7cWmjOp_Nji04keN9OG6ib5OVf/view)

* Essa reunião foi feita para apresentar ao Márcio os conceitos da avaliação de desempenho no contexto do Sirius 2.0.
* Muitas das tasks da seleção de concorrentes já está pronta, feita pelo Márcio, de forma que o início dos trabalhos na avaliação de desempenho deve se dar no dia 30/08/23.
* O objetivo da avaliação foi repassado ao Márcio. Os concorrentes a serem selecionados para a análise devem ser os competidores ALL STRATA, conforme escrito no plano de ação
* Foi repassado que o Lucas já fez um projeto de avaliação de desempenho semelhante ao que deve ser desenvolvido no Sirius 2.0
* Foi desenvolvida uma planilha de exemplo do que deve ser a avaliação de desempenho, que pode ser acessada no link: <https://docs.google.com/spreadsheets/d/1DxuX_GQQzhrOjUfYtoLEJLSjX6bLenvDrkn2QUV0DoY/edit#gid=0>
* Foi definido que a aba de output deverá ter overwrite toda vez que o código for rodado
* Um histórico na AWS deverá ser alimentado com dados de todas as rodagens


---

# Reunião 23/08/2023 - Campana, Probst, Padilha, Hideki

Gravação da reunião: Link

* Reunião para iniciar as atividades do módulo de Avaliação de Anúncios
* Foi desenvolvida uma planilha de exemplo do que deve ser a Avaliação de Anúncios, que pode ser acessada no link: <https://docs.google.com/spreadsheets/d/19KL-xB2-fI7xUcUzzxxDDZNqmWXW7AtT_tiwwTTEGvI/edit#gid=789146069>
* Como previsto, iremos pular a Análise 2 pois é necessário arrumar coisas no scraper do Pipe antes
* Código será executado manualmente 1x por semana


---

# Weekly 23/08/2023 - Campana, Probst, Padilha, Lucas

Gravação da reunião: [Link](https://drive.google.com/file/d/1NCxnRQDofPfGL4ssuL5AafDlu8l0KuVt/view)

* AWS-Sheets destravou, conseguimos ter avanço.
* Hoje já fizemos o kick-off da parte de Anúncios.
* Seleção de Concorrentes também foi finalizado, está em fase de testes pelo Márcio.
* Nesse momento estão sendo feitos testes para o deploy amanhã (24).
* Anúncios vai ter deploy na segunda (28).
* Seleção de concorrentes vai ter deploy no dia 29.
* Temos o Artur trabalhando no Sistema Supervisório, com deploy planejado pro dia 31.
* Avaliação de desempenho deve terminar no dia 5/9
* Depois disso começa a precificação, devendo ela ser a único projeto a partir do dia 6/9 dentro do Sirius 2.0
* Foram feitas algumas alterações no diagrama do Sirius 2.0


---

# Reunião 28/08/2023 - Campana, Probst, Padilha

* A Avaliação de Anúncios deve ter seu deploy hoje.
* Seleção de concorrentes está dentro do esperado também.
* No sistema supervisório, não temos notícia dos andamentos do Artur. Até então ele vinha trabalhando nos alertas. A task está bem atrasada.
* O Márcio terminando o deploy até amanhã, ele já começa a fazer a mexer na análise de desempenho
* As abas da planilha de precificação que sejam para todos os imóveis devem ser movidas para a a planilha setup grupos


---

# Daily 29/08/2023 - Campana, Probst, Padilha

Gravação da reunião: [Link](https://drive.google.com/file/d/1WVZOzWSiFR2HgDHoTARTiRpT_lrfAOVW/view)

* Alinhamento sobre as tabelas de outputs, que já estão no Trello Sirius 2.0
* Foi apresentado o MVP de Precificação, versões 1 e 2
* Foi apresentado o dashboard do Sirius 2.0 - Precificação Automática
* Probst deve trocar uma ideia com os analistas para levantar feedbacks do dashboard e do processo de precificação
* Probst deve pensar em uma forma de resumir a precificação manual de forma que ela possa ser considerada dentro do Sirius 2.0


---

# Weekly 30/08/2023 - Campana, Probst, Padilha, Lucas

Gravação da reunião: [Link](https://drive.google.com/file/d/1c3UHUuhJwBrZ9Py0up1G0GX48jVQxpyp/view)

* Evoluções no MVP de precificação
* Revisão do Gantt - Seleção dos concorrentes foi testada já. Campana trouxe a ideia de desenvolver um ambiente de testes para usá-lo antes de deploys. A ideia é também ter um ambiente de teste dentro da Stays. Avaliação de Anúncios também está pronto. Sistema Supervisório deve ser terminado hoje pelo Artur. A planilha ainda não foi realizada (com Apps Script). A ideia é que o Hideki assuma essa parte de criar a planilha do processo supervisório. A parte de Desempenho foi iniciada pelo Márcio hoje e deve ocorrer mais rápido do que o previsto.
* Campana trouxe uma ideia de futuramente trazer informações da Stays em tempo real ao invés de usar APIs no futuro.
* No módulo de precificação, além das ideias que tínhamos discutido, Probst disse que seria interessante mostrar o ganho de ocupação do listing nos últimos 5 dias ou 10 dias.
* Um novo dashboard foi apresentado, que é praticamente a última versão do MVP Precisificação antes do módulo de precificação no Sirius 2.0. Boa parte do módulo será baseado nesse MVP. Ele utiliza a AWS para queries e processamento dos dados, permite que o analista faça modificações em alguns fatores para ajustar o processo e que ele selecione qual imóvel/período está sendo precificado. Então clica em um botão para enviar os preços para uma planilha pré-Stays e depois confirma para enviar para a planilha da Stays.
* Probst deve pintar de laranja todas as células que vêm da AWS no MVP Precificação 2, o qual vai ser usado como a planilha "oficial" pra definir a planilha de precificação automática.


---

# Daily 31/08/2023 - Campana, Probst, Padilha, Lucas, Márcio

Gravação da reunião: [Link](https://drive.google.com/file/d/125L39OGK6z-doxs5C7E0mHORtf27xW2b/view)

* Probst deve puxar cerca de 50 grupos para a aba de concorrentes OK
* Probst deve validar a planilha de análise de anúncios OK
* O sistema supervisório terá um atraso no seu deploy, que deverá ser completado na segunda-feira
* Probst deve validar a planilha de setups, considerando regras genéricas que hoje estão na planilha de precificação manual OK
* Probst deve separar cada planilha do Sirius 2.0 em dev, prod e test. Ao terminar essas duplicações, colocar no Drive e compartilhar no Trello
* Probst deve colocar alerta de alteração percentual de preços no dashboard de RM


---

# Daily 01/09/2023 - Campana, Probst, Padilha, Lucas, Márcio

Gravação da reunião: [Link](https://drive.google.com/file/d/14lxX5xCcjrbq3s3xeFbA6I2pvaTHUYIh/view)

* Avaliação de anúncios foi validado.
* Probst deve mover todas as planilhas para o Drive de RM
* Sobre o sistema supervisório, Artur deve validar o job com o Probst
* Sobre a avaliação de desempenho, já foi feita uma step function, que agora vai se comunicar com a planilha. Os dados já estão salvos num bucket. Falta a parte da ingestão. Ainda será definido se essa última etapa vai ser feita pelo Márcio ou pelo Hideki
* Probst deve atualizar a planilha de setup com todos os dados necessários
* \


---

# Daily 04/09/2023 - Campana, Probst, Padilha, Lucas, Márcio

Gravação da reunião: [Link](https://drive.google.com/file/d/1bvOk2yP-Bvnx-lwcIImiLM_5pUROVlRe/view)

* Revisão do Gantt → No sistema supervisório, falta o Artur alinhar as ideias com o Probst, o que deve ser feito ainda hoje. O deploy não deve ser feito até dia 05, como planejado. O deploy do sistema supervisório deve ser feito até quarta-feira
* Na parte de desempenho, ainda é necessário fazer a ingestão da planilha pra AWS. Márcio já foca nas tarefas restantes a partir de hoje. Falta também fazer o pull request antes da ingestão. O deploy da avaliação de desempenho deve ser feito até amanhã.
* Processo de precificação → No fluxo de precificação, adicionamos o fato de cada planilha ser nominal. O nome do usuário ficará sempre hard-coded no código .gs da planilha, para que dois ou mais analistas possam trabalhar ao mesmo tempo em planilhas diferentes, apenas com os imóveis associados ao analista "correto" de acordo com a planilha de setup de imóveis.
* O que vai precisar mudar em relação ao MVP de Precificação → inclusão da coluna "mudar" nos fatores, exclusão do fator percentil e inclusão do botão "enviar" dentro do dashboard. Após o envio dos preços novos definidos dentro da precificação automática, a AWS faz os cálculos de condições de calendário com base nos dados de setup.
* Ficou definido que a "planilha Pré-Stays" será uma aba na planilha de precificação automática de cada analista.
* Ficou definido o formato da tabela pré-Stays, que terá colunas de: imóvel, data, tarifa e preço
* **Probst deve trazer para a próxima reunião a precificação manual**


---

# Daily 05/09/2023 - Campana, Probst, Padilha, Lucas, Márcio

Gravação da reunião: [Link](https://drive.google.com/file/d/1Ok-VD0pmDPlfNbg9ElqgoRXg1YmPJahx/view)

* Revisão do Gantt → Probst deve revisar com o Hideki a parte de warnings entre as planilhas. Sobre o sistema supervisório, o Artur pracisa ajustar algumas questões de infraestrutura e alinhar o job com o Probst. A ingestão deve ser passada pro Hideki. Deploy do supervisório está previsto para quarta-feira. Avaliação de desempenho tem seu deploy planejado para agora à tarde e tudo a princípio vai dar certo. Sobre a precificação geral, o início deve ocorrer no dia 11.


---

# Daily 06/09/2023 - Campana, Probst, Padilha, Lucas, Márcio

Gravação da reunião: [Link](https://drive.google.com/file/d/1ScBm9HUBQQ8lslwgVcm3F7WB70ArAbC2/view)

* Na parte dos warnings do Sirius, o Probst ainda precisa validar com o Hideki se ele faz sentido
* No sistema supervisório, tivemos um problema com o payload (volume de dados de output). Para solucionar esse problema, definimos os limites inferior e superior como 10 e 90. Para conectar o lambda ao API Gateway, também houve um problema de timeout. A solução, que está sendo feita agora, vai fazer com que o deploy seja atrasado para segunda-feira.
* Resultados do supervisório foram gerados no sheets e os resultados estão sendo salvos no S3 (como um histórico).
* Sobre a avaliação de desempenho, foi feito o deploy hoje e testes estão sendo realizados nesse processo. A seleção de concorrentes para a análise funcionou.
* Na precificação, num primeiro momento devem ficar o Campana e o Márcio. O resto do pessoal pode ser envolvido com o tempo conforme a disponibilidade e a urgência das tasks.
* Fizemos a abertura do processo de precificação manual no fluxograma de precificação.


---

# Daily 11/09/2023 - Campana, Probst, Padilha

Gravação da reunião: [Link](https://drive.google.com/file/d/1f-Tk0q5iYOdZdChE3TxMIJTzzVWxPIR0/view)

* Supervisórrio foi implementado e agora deve ser revisado pelo Probst para aprovação
* Deploy da avaliação de desempenho deve ocorrer na quarta-feira
* A análise de desemepenho já está retornando resultados. Probst deve analisar se os valores estão faznedo sentido
* Precificação - o deploy inicial fica planejado para ocorrer no dia 19


---

# Daily 12/09/2023 - Campana, Probst, Padilha

Gravação da reunião:

* Warnings - Probst deve validar até hoje, via card do Trello
* Supervisório - Probst deve validar até hoje à noite, mas a planilha já vem sendo usada
* Desempenho - As colunas que faltavam foram inseridas pelo Márcio e devem ser validadas pelo Probst
* Precificação Heurística - Campana começou a fazer ingestões. Devem ser criadas as planilhas e deve ser feito seu preenchimento (a ser feito pelo Probst). Depois disso, deve ocorrer o processamento das regras, em cima dos preços de base, por meio de um job específico. Os preços de base devem ser salvos no S3, juntamente com as regras de preço
* Precificação por concorrentes - A planilha sheets com dashboard já está criada. Os próximos passos serão a consideração dos períodos quentes e frios
* Validações da Precificação ocorrerão na semana que vem. A ideia é fazer um primeiro teste na quarta-feira, no horário da Weekly

# Daily 13/09/2023 - Campana, Probst, Padilha, Lucas, Márcio

Gravação da reunião:

* A planilha supervisória em Prod deve ser usada daqui em diante
* Na avaliação de desempenho, foi feito o deploy hoje também. Usar em Prod daqui pra frente

# Daily 14/09/2023 - Campana, Probst, Padilha, Lucas, Márcio

* Probst ainda deve revisar pontos anteriores sobre Warnings, Desempenho e Supervisório
* As pastas relacionadas a cada projeto também devem ser organizadasno Drive
* Precificação já está andando bem. Márcio já conseguiu encaixar a análise de concorrentes para seleção de ocupações.
* Ainda falta a geração do calendário na planilha de precificação por concorrente

# Daily 15/09/2023 - Campana, Probst, Padilha, Lucas, Márcio

* Probst deve terminar de preencher a planilha de Setup em Dev
* Campana já começou a parte de preços especiais
* Márcio já terminou a análise de concorrentes
* Márcio está trabalhando na parte de importação de preços, ocupações e bloqueios da precificação por concorrentes
* Probst deve desenvolver os gráficos, calendários e fórmulas da planilha de precificação por concorrentes em Dev

# Daily 25/09/2023 - Campana, Probst, Padilha

* Sobre a precificação, o que foi feito foi consolidar os parâmetros em feature. Hoje deve dar pra consolidar em DEV para RM poder testar
* Pré-Stays saiu do escopo de precificação por concorrentes
* A integração com o módulo da Stays ainda precisa ser validada, mas a princípio está fazendo sentido
* Da parte da precificação huerística, já temos os jobs que calculam os preços finais prontos
* A Stays de teste infelizmente ainda não possui todos os imóveis da Seazone, tornando difícil os testes e validações por meio da própria Stays

# Dump de anotações

## Anotações do Bill

Features Sirius 2.0

Gapper (remoção de gaps)

Gapper de feriados

Regras dinâmicas para mínimo de noites

Bloqueio de last minute

Regras de preço mínimo, máximo e fixo

Comunicação com a Stays com frequência mínima de a cada 3 horas

Precificar manualmente

Abertura de calendário dinâmico por imóvel

Agrupamento de imóveis em grupos

Bloqueio de checkin/checkout

Descontos por duração de estadia

Estadias mínimas e máximas

Teste Rápido\*

Processo de implantação de novos imóveis

Macro processo de precificação do cluster principal

* Notion RM

## Anotações Campana - RM Day

Vídeo 1:

Parte I: Precificação

* Introdução e a área de RM: 02:30m
* Maior dor do Probst 18m e 35s
* O que significa RM? 21m e 00s
* Se não vender, é sempre culpa do RM? 25:40
* Parte I - Geral do Novo Processo de Precificação 36:35
* Módulo 1: 1h 02m 15s
* Módulo 2: 1h 06m 25s
* Módulo 3: 1h 10m 30s
* Módulo 4: 1h 20m 40s
* Módulo 5: 1h 34m 40s

**Anotações**: -> Monitoração das aplicações -> Atualmente a revisão de preços é feita para o mês atual e o mês seguinte, mas no futuro, revisar 6 meses. -> Interessante olharmos os módulos que o Probst apresenta (possível separação) -> Maior dor -> não conseguir ter visibilidade de todas as datas de calendário aberto que temos, e que tenha um sistema de avisar os problemas, antes de que algo ruim aconteça -> Como descobrir o motivo de pq o imóvel vai mal? A única estratégia hoje é diminuir o preço. -> Cluster principal de imóveis da seazone: tenho infos suficientes para utilizar o processo descrito

**Parte 1:** O objetivo da parte 1 é conseguir olhar para a concorrência que faz sentido e ajustar os nossos preços. Isso resolve problema de 80% dos imóveis. gerar o preço x imóvel por dia em um horizonte de 180 dias (são 130k no total) Hoje feito 2x por semana Feito com janela de tempo, cada dia

**Módulo 1:** seleção de um imóvel e de seu calendário aberto

Daily revenue, com 700 imóveis + 180 dias

Escolha da faixa de faturamento.

**Módulo 2:** identificar concorrentes gerais (imóveis compatíveis com o meu) na data de hoje, para a data de análise (180 dias)

Todos concorrentes do mesmo bairro, com o mesmo n de quartos

Filtro para os que estão na mesma faixa de faturamento da categoria do imóvel (strata) (com janela de +-15 dias)

Saída: seleção dos concorrentes gerais que possuam faturamento de acordo com o potencial do imóvel

**Módulo 3**: identificar concorrentes plus (imóveis dentre os gerais que tem algo a mais), dentro os gerais

Aplicado vários filtros (quais?) para selecionar apenas os que tem um anúncio diferenciado

Identificar anúncios com maior potencial de faturamento contínuo

Saída:

seleção de concorrentes "plus", que tendem a possuir uma seleção de preços que parece indicar um bom faturamento ao longo do tempo

**Módulo 4:** separação  dos períodos de análise com base nos concorrentes gerais.

Dados dos concorrentes gerais são levantados para cada dia no futuro, períodos que tenham ocupação semelhante são destacados

Atualmente é feito pelo período de mês, mas é interessante fazer uma análise mais granular, por exemplo. Inclusive é aqui que geralmente são vistos valorização de eventos que desconhecemos na cidade, pois os concorrentes aumentam os valores

O método atual trabalha com uma separação de períodos, tentando evidenciar períodos de alta demanda (ou preço).

O objetivo é mostrar os períodos onde o analista vai ficar mais atento e montar uma estratégia por período

Requerimento de atualização diária ou real time.

Saída: imóvel, dia, se é um período quente ou frio (e uma divisória, transição dos períodos)

**Módulo 5:** Análise de predição de ocupação dos concorrentes gerais.

Estimar o quanto os concorrentes gerais vão faturar, baseado na ocupação

Método: 1- histórico normal, 2 histórico outlier, 3 ganho recente por dia da semana

Saída: ocupação final esperada para cada dia no futuro na categoria do imóvel

**Módulo 6:** Análise de desempenho do imóvel por período Por período e por imóvel, avalia o desempenho (baseado na previsão de ocupação dos imóveis), ou seja, usando o faturamento.

São determinados limites max e min de faturamento esperado para a data de análise em cada período

Comparação em relação aos concorrentes (Faturamento) em um determinado período (parece que são 15 dias)

Saída: Score do imóvel para cada período

**Módulo 7**: Ajuste de preços por período com base na concorrência

Em cada período, preços são sugeridos por dia com base nos valores usados pelos concorrentes plus e concorrentes gerais.

O ajuste é feito via faixas, junto com uma análise de período e desempenho do imóvel. Fatores de alteração: fator plus, fator mercado, fator geral

Saída: preços revisados para todos os dias disponíveis do imóvel

**Módulo 8:** Registro das alterações de preço

sirius devidamente atualizado com os novos preços

Output: um preço para cada dia para cada imóvel e o registro de alteração dos preços.

**Vídeo 2**

**Parte II (Processo de onboarding de um novo imóvel)**

* Introdução 1m
* Módulo 1: 8m 20s
* Módulo 2: 8m 42s
* Módulo 3: 9m 05
* Módulo 4: 10m 25s
* Módulo 5: 11m 35m

**Anotações**:

**Módulo 1: Verificação de entrada de novos imóveis**

identificar características do imóvel e definir a sua categoria

Granularidade: imóvel-dia

Frequência: 1 ciclo por dia com 1-5 imóveis normalmente

**Módulo 2:** Avaliação da categoria do imóvel e possíveis condições especiais

Valor mínimo, estadia mínima, confirmação da categoria

**Módulo 3:** Identificação dos concorrentes gerais

É passível de comparação com a concorrência? Seleção de concorrentes gerais que possuam faturamento de acordo com o potencial do imóvel

**Se sim:**

Processo de precificação normal: Análise de predição de ocupação (Módulo 5) e Geração de preços dos concorrentes (Módulo 6)

Saída: Geração de preços para tarifário inicial do imóvel

**Se não** (mais raro de acontecer, 10% das vezes)

Análise de similares no Airbnb

Análise de similares da Seazone

**Módulo 4:** definição do tarifário inicial e atualizações do Sirius

Os preços iniciais são automaticamente gerados como na precificação, porém, como o imóvel novo não possui histórico, não possui score também.

Saída: sirius devidamente atualizado com os valores, condições especiais e seleção de clusters do imóvel na aba Setup Grupos.

**Módulo 5:** Geração de um relatório para o setor de CS (de proprietários)

A ideia é mostrar e justificar a precificação para os proprietários

**Parte III (Processo de  avaliação de anúncios)**

* Introdução: 17m 30s
* Módulo 1:  22m 50s
* Módulo 2: 32m 0s
* Módulo 3: 36m 40s
* Módulo 4: 40m 50s
* Módulo 5: 41m
* Comentários: 41m 50s

**Objetivo**:

Identificar anúncios com desempenho ruim por meio de seus KPIs

Se não está desempenhando bem, geralmente o problema não é preço. como descobrir qual o problema? Como dizer se um anúncio é bom ou ruim ?

Solicitar ao setor de anúncios a atualização do anúncio com desempenho ruim

Granularidade: imóvel

Frequência: 1x por semana

**Módulo 1**: Levantar KPI de Ranqueamento

Entrada: enriched_ranking_airbnb_location_weekend

Dados de ranqueamento referentes aos últimos 3 finais de semana do imóvel devem ser elevados

O KPI é formado pelo número de página médio dos três valores para  o imóvel e serve como um indicador de potencial de venda no airbnb

Saída: KPI de Ranqueamento

**Módulo 2:** Levantar KPI de Taxa de conversão

Entrada: raw.airbnb_conversion_rate

Dados sobre conversão:

Quantas vezes o imóvel apareceu na busca e alguém clicou

Quantas vezes, quem clicou e viu o anúnciou, reservou

Saída:

KPI de taxa de conversão

**Módulo 3**: Levanta KPI de avaliações airbnb

Entrada: clean.details

Dados das últimas 10 semanas do imóvel, extraindo as últimos 3 dados

Saída:

KPI de avaliações airbnb

**Módulo 4:** identificar imóveis com avaliações ≤ 4.0

Seleção dos anúncios com baixa avaliação

**Módulo 5:** solicitar anúncios selecionados sejam refeitos

Repasses ao setor de anúncios via Slack quando  anúncios com review ≤ 4.0, após três últimos notas

**módulo 6:** registrar KPIs por imóveis por data em um relatório

Relatório KPI por data de análise e imóvel

**Parte IV (Processo de  avaliação de desempenho)**

* Introdução: 46m 45s
* Módulo 1: 59m 10s
* Módulo 2: 1h 01m 22s

Objetivo:

Como saber se o desempenho foi bom ou ruim?

> "Se eu faturar 4000 reais, em julho, no centro de Floripa, é bom ou ruim?"

Trazer visibilidade sobre o atingimento das metas mensais de cada imóvel em tempo real.

Permitir que se identifiquem casos muito acima ou muito abaixo da média de forma que o analista consiga dar atenção maior a essas situações

Granularidade: imóvel-mês,

Frequência: 2 ciclos por semana

**Módulo 1:** Levantar metas mensais de cada imóvel Seazone

Entrada: faturamento-cidade-bairro-strata

Inicialmente as metas mensais são calculadas como a média de faturamento de dois meses dos dois anos passados, fechados na planilha de faturamento

Cada imóvel → conjunto cidade-bairro

Saída: levantamento das metas por imóvel/mes

Módulo 2: Levantar curvas de ganho de faturamento típicas de cada mês

Módulo 3: Selecionar limites sup e inf de faturamento por mes

Módulo 4: identificar imóveis fora dos limites em cada mÊs

Módulo 5: calcular scores dos imóveis de acordo com a sua meta do mês

Módulo 6: Alertar o setor de CS sobre ocorrencias anormais em imóveis com preços mínimos

Módulo 7: Registrar scores de cada imóvel-mês na análise

Módulo 8: Registrar scores de cada imóvel-mes da análise

## Anotações Padilha

**Features que anotei na reunião com Bill, Probst, Campana e eu**

* Gapper -> alteração do min_night de acordo com período disponível
* Definição manual de preços (preço mínimo + dinâmico)
* Definição manual de estadias mínimas (por imóvel e data)
* Teste rápido -> validação + rápida de definição dos preços de um imóvel/datas
* Bloqueio de last_minute no ILC e JBV (depois das 19:00 ninguém pode entrar no mesmo dia)
* Preço mínimo (para não quebrar contrato com proprietário)
* Comunicação com Stays no mínimo de 3hrs em 3hrs
* Avisar quando o preço foi inputado e quando houve erros (na hora)
* Log dos preços inputados e dos erros
* Bloqueio automático de datas de acordo com antecedência (por imóvel)
* Cluster de imóveis (regras que são aplicadas sobre um grupo de imóveis, 1 imóvel pode estar em mais de um cluster)
* Bloqueio de checkin/checkout (proibir checkin ou checkout em certas datas)
* Descontos por duração de estadia
* Regras de preço (por dia e por imóvel)
* Cluster de precificação altruísta de imóveis bons (precificação escada)
* Macroprocesso de precificação do cluster principal (frequência 2x semana)