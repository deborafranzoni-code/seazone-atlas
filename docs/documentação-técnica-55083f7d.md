<!-- title: Documentação Técnica | url: https://outline.seazone.com.br/doc/documentacao-tecnica-cb2HhSbGMS | area: Tecnologia -->

# ⚙️ Documentação Técnica

Esse projeto consiste na criação de um dashboard que ajuda RM a focar em imóveis com maior potencial de impacto no fechamento da meta mensal.

Aqui está o epic criado: <https://seazone.atlassian.net/browse/DS-920>

# Introdução

No primeiro passo, o projeto consiste em adaptar dash MVP que foi feito no Streamlit.

O github responsável pela criação desse dash está aqui (a branch dash-v1_01 é a mais atualizada): <https://github.com/LucasAsilveira/meta-performance-dashboard/tree/dash-v1_01>

Para rodar localmente, basta baixar as bibliotecas e rodar o comando:

```bash
streamlit run app/streamlit_app.py
```

Para atualizar os dados é necessario rodar os scripts de 1_import_data.py e 2_data_prepar.py

Apesar do MVP ter sido feito no StreamLit, foi decidio fazer o projeto no Looker Studio. Essa decisão foi tomada para mantermos o padrão de todos os BIs serem feitos no looker, além disso, parecia que o Looker teria todas as funcionalidades necessárias para o projeto.

# Script

Link Git: <https://github.com/seazone-tech/gcp-data-resources/tree/main/cloud-functions/meta-performance>

O único script utilizado no projeto é o **meta-performance**. Ele foi colocado para rodar no final do workflow da meta, ou seja, toda a vez que a meta é atualizada o script atualiza os dados que vão pro BI.

A lógica dele é a mesma usada no MVP do streamlit, as únicas coisas que mudaram foram algumas colunas:

* **n_dates_special_price:** Antes os dados de preço mínimo vinham da tabela de auditória da Meta 1.0, mas como essa é uma tabela legado que, inclusive, já era pra estar desativada, foi alterado para puxar direto das tabelas de preço + daily_revenue_sapron
* **media_preco_ocupado**: Essa era uma coluna usada para calcular o faturamento perdido por bloqueios, então a lógica era fazer **dias_bloqueados** \* **media_preco_ocupado**, mudei para a coluna ser **daily_revenue_avg**, ou seja, como queremos calcular um tipo de faturamento, faz mais sentido usar o faturamento diário que tivemos no mês.

O script em si faz o seguinte:


1. O script seleciona o start_date e end_date baseado no meses M0, M1, M2, sendo que M0 é o mês de ontem (mesma lógica usado para o calculo da Meta 2.0, ela sempre roda pro mês de ontem, dessa forma ela roda uma vez com o mês totalmente fechado)
2. São pegos os dados da AWS, ou seja, os imóveis, categorias, cidade, dados da daily_revenue_sapron, datas que batem no preço mínimo, etc.
3. São pegos os dados da GCP/BigQuery, que no caso são os da Meta 2.0.
4. É calculado os dados que vão pra tabela performance_dash
5. É calculado os dados que vão pra tabela berlinda_dash
6. As tabelas do BigQuery são atualizadas com um append

# Tabelas

As tabelas possuem várias colunas e são totalmente baseadas no MVP, então dá pra usar a documentação do MVP para entender o que cada coluna representa (no MVP elas eram em português, aqui para manter o padrão é inglês):

@[Lógica de Cálculo e Escolha de Métricas](mention://41140ed0-b18e-4ef0-950a-dedde85e3cf1/document/3b6842f7-1a8b-4055-ab10-308b400f7ddf)

**Tabela** **performance_dash:**

* **Descrição**: Essa tabela tem todos os dados usados na aba de Visão Geral do dash + os dados usados pro calculo de algumas colunas.

**Tabela berlinda_dash:**

* **Descrição:** Essa tabela tem todos os dados usados na aba de Berlinda Detalhada do dash + os dados usados pro calculo de algumas colunas.

As duas tabelas são clusterizadas em year_month + timestamp, como todas as consultas usam essas colunas isso acelera o tempo de query.

Também foram criadas views com sufixo last_timestamp nas duas tabelas para ter numa view de fácil acesso a última timestmap de cada dia, visto que, se por algum motivo o script rodar duas vezes no mesmo dia, vamos sempre querer a última versão.

Essas views também possuem a coluna "date" que é a coluna timestamp truncada.

# Looker Studio

Link: <https://lookerstudio.google.com/u/2/reporting/95aa49c3-e88d-40cc-946d-e4749a32f10d/page/aiNjF>

## Explicação Geral

Essa seção é dedicada a explicar como foram feitas algumas medidas chave do Looker Studio.

### Selecionar Data + Evolução da Quantidade de Imóveis

Se fosse colocado um controle simples em cima da coluna timestamp pro usuário selecionar uma timestamp especifica, esse controle iria interferir com o gráfico de evolução da quantidade de imóveis, ou seja, se fosse selecionado "2026-01-01" o gráfico de evolução só mostraria essa data.

Esse problema acontece até se forem duas fontes de dados diferentes, visto que, como elas teriam o mesmo nome de colunas, o looker automaticamente aplicaria o filtro nas duas.

Para evitar isso, o controle usado é um de data onde o usuário pode selecionar o start e end dates.

Os dados do performance_dash e da berlinda_dash são puxados através de uma consulta personalizada onde é pego a maior timestamp de cada year_month.

```sql
SELECT *
FROM `meta.performance_dash_last_timestamp`
WHERE FORMAT_DATE('%Y%m%d', date) <= @DS_END_DATE
QUALIFY
    MAX(timestamp) OVER (PARTITION BY year_month) = timestamp
```

Para o gráfico de evolução temporal foi criada uma segunda fonte de dados que puxa a tabela toda. Inclusive, o número de datas que aparece aqui vai depender do periodo que o usuário selecionar no controle. Por default foi colocado para ser os últimos 30 dias.

### Mês Atual

É impossível num controle do Looker Studio pro valor default ser o mês de agora, visto que o mês de agora é algo que muda dinamicamente.

Para consertar isso, foi criado um campo nas duas tabelas onde é feito um CASE, caso for mês de agora então substitui pela string "Mês Atual", dessa forma, é possível no próprio controle colocar pro valor default ser "Mês Atual".

 ![](https://outline.seazone.com.br/api/attachments.redirect?id=829ad2d7-f0ee-420c-87bb-7ae95583ee38 "left-50 =214x230")


\

\

\

**Detalhe:** Esse campo foi criado nas DUAS tabelas com o MESMO id, dessa forma o looker automaticamente sabe que se filtrarmos o campo current_year_month de uma tabela estamos querendo filtrar esse campo na outra tabela.

## Scatter Plot

A maioria das funções dos Scatter Plor que existiam na versão do Streamlit também funcionariam no looker. Inclusive, elas foram feitas e estão na página oculta "Copy of Visão Geral", mas haviam alguns problemas:

* Não daria pra colocar um botão que automaticamente altera a escala do gráfico para logaritima.
* Não daria para automaticamente mudar o tipo da coluna de número para porcentagem ou mudar o eixo X.
* Não daria para dinamicamente mudar as linhas de referencia para irem do eixo X pro Y ao inverter o eixo.
* Não daria para mostrar todas as informações desejadas ao passar o mouse em cima do pontos.

Para resolver esse problema, foi criado um gráfico personalizado usando as "visualizações da comunidade" do looker studio. Essa é uma funcionalidade que permite usar javascript para fazer qualquer tipo de gráfico.

**Links úteis:**

* Serie no Youtube onde ele explica tudo: <https://www.youtube.com/watch?v=qgrVPLncK4A>
* Documentação da Google sobre o assunto: <https://developers.google.com/looker-studio/visualization>
* Documentação dos arquivos necessários: <https://developers.google.com/looker-studio/visualization/config-reference>
* Link do Git com os scripts criados para esse projeto: <https://github.com/seazone-tech/gcp-data-resources/tree/main/looker-studio/meta-performance>

### Como funciona o gráfico em si?

Aqui em baixo estão os campos cirado pro gráfico:

 ![](https://outline.seazone.com.br/api/attachments.redirect?id=5d4fd7fd-4e19-4a93-adc0-f3762c9b456d "left-50 =207x405")

* **Tooltip Details**: Ao passar o mouse em cima dos pontos, automaticamente foi configurado para os campos de Dimension, Color By, Eixo X e Y para aparecer. Se for necessário mais algum então dá pra inserir aqui.
* **Bubble Size:** Esse é um dos únicos campos que pode ser ignorado. É possível selecionar uma coluna pro script usar como base pro tamanho dos pontos.
* **Format X to %** : Aqui é esperado uma coluna true or false que indica se será ou não necessário format o eixo X para porcentagem. Infelizmente o looker não traz uma opção de passarmos apenas um parametro, para mudar dinamicamente é realmente necessário passar uma coluna inteira de true or false.
* **Inver X/Y e Escala log**: Mesma coisa do de cima, mas para dizer se será necessario invertar os eixos ou passar o eixo Y para log.


\

 ![](https://outline.seazone.com.br/api/attachments.redirect?id=f8b23e05-354e-48c5-a755-04ef965c889d "left-50 =86x264")

* **Char Colors For Groups:** Esse é o campo onde se define a cor dos grupos de prioridade. Infelizmente não foi descoberto uma forma de automaticamente usar os campos de dimensão que o looker studio automaticamente gera.
* **Char Colors For Priority:** É usado para definir as cores do Status Operactional


\

\

 ![](https://outline.seazone.com.br/api/attachments.redirect?id=3f86b1af-f7c5-4fe9-b6d4-fc455b2b4989 "left-50 =86x178")

Esses campos são usados para definir o valor e o label de cada linha de refêrencia. No scripts as cores foram definidas para automaticamente usar as definidas no campo "**Char Colors For Groups"**

No gráfico da berlinda, todas as linhas de referencia foram definidas para serem 2, visto que dessa forma elas ficam pra fora do gráfico (o looker não estava permitindo deixar nulo)


### Como criar/editar os scripts do gráfico?

A visualização da comunidade consiste em criarmos alguns scripts e colocarmos no Cloud Storage. O Cloud Storage PRECISA estar configurado para acesso público. Em teoria não tem problema, visto que os scripts que colocarmos nele não possuem nada sensível.

[Link do Cloud Storage](https://console.cloud.google.com/storage/browser/looker-studio-data-resources-448418?pageState=(%22StorageObjectListTable%22:(%22f%22:%22%255B%255D%22))&authuser=2&hl=pt-BR&organizationId=465702385920&project=data-resources-448418)

Para editar qualquer coisa o processo é: Alterar os scripts e fazer o upload daquilo que foi alterado no cloud storage. Um ponto de atenção é tomar cuidado pois não tem ambiente de DEV, então simplesmente fazer o upload pode quebrar os gráficos de PROD.

Também é recomendado SEMPRE alterar o script do manifest.json para devMode=True. Caso contrário, o looker studio automaticamente usa um cache dos arquivos, então as alterações demoram umas 12 horas para atualizar no looker. **Caso use o devMode elas sobem instantaneamente.**

#### Arquivo config.json

Esse é o arquivo onde se define quais campos vão aparecer no front das configurações do gráfico.

Em data é possível colocar campos de dimensão e métricas que serão usados no script.

Em style dá pra definir campos como cor, fonte, tamanho, formatação, etc.

Na documentação do google está bem explicado como que cada tipo de campo que é possível adicionar.

#### Arquivo style.css

Arquivo css padrão. Dá pra definir o estilo dos gráficos que serão gerados nos scripts.js

#### Arquivo manifest.json

Esse é tipo o "main", é aqui que se define o logo/descrição do gráfico criado. Aqui também se define o caminho dos scripts no cloud storage, então caso algum for renomeado é necessário alterar aqui.

Também é importante o campo devMode que, como já foi explicado anteriormente, é necessário ser True para fazer alterações nos scripts.

#### Arquivo src/index.js + dist/viz.js

O arquivo src/index.json vai possuir o script do gráfico de dispersão. Infelizmente, não é uma boa ideia colocar ele direto no cloud storage.

Isso é porque ele depende das bibliotecas @google/dscc (pro looker) e d3 (pro gráfico). Idealmente, a gente quer subir o mínimo possível de dados pro cloud storage, isso é pra deixar os requests mais rápidos.

Para isso foi usado o webpack, ele automaticamente faz o bundle das libs e salva tudo no script dist/viz.js, então **é por isso que no cloud storage é apenas feito o upload do arquivo viz.js**

Após fazer as edições locais em cima do index.js, é necessário rodar os seguintes comandos para atualizar o viz.js.

O comando abaixo é necessário rodar apenas uma vez, isso é pra baixar localmente as bibliotecas usadas, obviamente, é necessário ter npm instalado para funcionar no terminal.

```bash
npm install --save d3@7.9.0 @google/dscc@0.3.22
npm install --save-dev webpack@5.91.0 webpack-cli@5.1.4
```

Depois, basta fazer:

```bash
npx webpack
```

Esse comando vai atualizar o arquivo **dist/viz.js.**

Agora basta fazer o upload do arquivo no cloud storage e recarregar a página do looker studio para ver as mudanças.

### Lógica do Script

Caso seja necessário editar o script e é a primeira vez mexendo, é recomendado começar colocando um console.log(data), isso é só pra entender o formato de como os dados chegam no script.

Lembrando que pra atualizar no looker basta:

* Rodar npx webpack
* Fazer o uplaod do viz.js
* Alterar o manifest.json para ser devMode=True
* Fazer o upload do manifest.json

Abaixo está a documentação do script disponibilizada pelo ChatGPT:

#### 📊 Visão Geral da Visualização

Este script implementa uma **visualização customizada de gráfico de dispersão com bolhas (Bubble Chart)** para o **Looker Studio**, utilizando **D3.js** para renderização gráfica e **@google/dscc** para integração com os dados, estilos e controles da plataforma.

A visualização permite:

* Comparação entre duas métricas (Eixo X e Eixo Y)
* Tamanho variável das bolhas
* Agrupamento por status ou criticidade
* Escala linear ou logarítmica
* Inversão dos eixos
* Linhas de referência configuráveis
* Tooltip detalhado
* Legenda automática


---

#### 📦 Dependências

O script utiliza as seguintes bibliotecas externas:

* **@google/dscc@0.3.22** Responsável pela comunicação com o Looker Studio, acesso a dados, dimensões, métricas e estilos.
* **d3@7.9.0** Biblioteca para criação e manipulação de visualizações SVG interativas.


---

#### 🧩 Estrutura Geral do Código

O código está dividido em três partes principais:


1. Importação das dependências
2. Funções auxiliares (linhas de referência)
3. Função principal de renderização (`drawViz`)
4. Inscrição da visualização no Looker Studio


---

#### 🔧 Função `drawReferenceLine`

Esta função é responsável por desenhar **linhas de referência horizontais ou verticais** no gráfico, com rótulo opcional.

**Responsabilidades:**

* Calcular a posição da linha com base nas escalas
* Desenhar uma linha tracejada
* Exibir um texto identificador (label), se configurado

**Parâmetros:**

* `svg`: container SVG principal
* `width`: largura útil do gráfico
* `refValue`: valor numérico da linha de referência
* `refLabel`: texto exibido junto à linha
* `invertXY`: define se a linha é vertical ou horizontal
* `xScale`: escala do eixo X
* `yScale`: escala do eixo Y
* `color`: cor da linha e do texto

A linha só é desenhada caso `refValue` esteja definido.


---

#### 🎨 Função Principal `drawViz(data)`

Esta é a função principal da visualização, chamada automaticamente pelo Looker Studio sempre que os dados ou estilos são alterados.

Ela é responsável por **limpar o canvas, preparar os dados e renderizar todos os elementos gráficos**.


---

#### 🧹 Limpeza Inicial do Canvas

Antes de qualquer renderização, o script remove elementos existentes:

* SVGs antigos
* Tooltips antigos

Isso evita duplicações durante atualizações da visualização.


---

#### 📐 Configuração do Canvas e Margens

Define o espaço disponível para o gráfico utilizando:

* Margens internas (`top`, `right`, `bottom`, `left`)
* Largura e altura dinâmicas baseadas no tamanho do container do Looker Studio


---

#### 🗂️ Preparação e Tratamento dos Dados

Os dados utilizados vêm de `data.tables.DEFAULT`.

Principais tratamentos:

* Limitação da quantidade de pontos com `maxBubbles`
* Leitura de configurações por linha:
  * Inversão de eixos (`invert_x_y`)
  * Formatação percentual (`format_x_to_percentage`)
  * Escala logarítmica (`log_scale`)
* Filtro automático de valores inválidos para escala logarítmica


---

#### 📏 Definição das Escalas

O gráfico utiliza três escalas principais:

* **Escala X**: linear, baseada na métrica do eixo X
* **Escala Y**: linear ou logarítmica, conforme configuração
* **Escala de Raio**: escala raiz quadrada (`scaleSqrt`) baseada na métrica de tamanho da bolha

Os limites das escalas são calculados dinamicamente a partir dos dados.


---

#### 🎯 Definição de Cores e Grupos

As cores das bolhas são determinadas pelo campo `color_by`.

A estratégia de cores segue a ordem:


1. Mapas customizados de **Criticidade**
2. Mapas customizados de **Status Operacional**
3. Fallback automático com `d3.schemeCategory10`

Somente os **10 grupos mais frequentes** são destacados individualmente. Os demais são agrupados como `"Others"`.


---

#### 🧭 Criação dos Eixos

Os eixos X e Y são renderizados com:

* Formatação automática (percentual ou numérica)
* Quantidade dinâmica de ticks
* Compatibilidade com inversão de eixos


---

#### 🧱 Grid de Fundo

O gráfico possui um grid de fundo com **densidade dupla**, composto por:

* Linhas principais (ticks do eixo)
* Linhas intermediárias (valores médios entre ticks)

Esse grid melhora a leitura visual sem poluir o gráfico.


---

#### 🫧 Renderização das Bolhas

Cada linha de dados é representada por uma bolha SVG.

Características:

* Posição baseada nas escalas X e Y
* Raio proporcional à métrica de tamanho
* Cor definida pelo grupo
* Opacidade configurável via estilo


---

#### 🧠 Interações e Tooltip

A visualização possui interações completas de mouse:

* **Mouseover**: exibe tooltip
* **Mousemove**: reposiciona tooltip automaticamente
* **Mouseout**: oculta tooltip

O tooltip exibe:

* Dimensão principal
* Grupo ou status
* Valores dos eixos X e Y
* Campos adicionais configurados no Looker Studio


---

#### 🏷️ Legenda

A legenda é gerada automaticamente:

* Mostra até 10 grupos mais frequentes
* Organizada em múltiplas linhas
* Inclui item `"Others"` quando necessário
* Cores consistentes com as bolhas


---

#### 📌 Linhas de Referência

O gráfico suporta múltiplas linhas de referência configuráveis:

* Crítico
* Atenção
* Berlinda
* OK

Cada linha:

* Possui valor e rótulo configuráveis
* Usa a cor correspondente ao grupo
* Pode ser horizontal ou vertical (dependendo da inversão dos eixos)


---

#### 🔌 Integração com o Looker Studio

A visualização é registrada no Looker Studio através de:

`dscc.subscribeToData(drawViz, { transform: dscc.objectTransform }); `

Isso garante:

* Atualização automática ao alterar filtros ou estilos
* Estrutura de dados compatível com o script


---

#### ✅ Resumo Funcional

* Visualização customizada e interativa
* Alta flexibilidade de configuração
* Compatível com grandes volumes de dados
* Visual consistente com padrões do Looker Studio
* Código modular e extensível