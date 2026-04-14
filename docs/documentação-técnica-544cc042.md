<!-- title: Documentação técnica | url: https://outline.seazone.com.br/doc/documentacao-tecnica-pny4tdF5Ps | area: Tecnologia -->

# Documentação técnica

# Arquitetura e Stack Tecnológico

A solução foi desenhada utilizando uma arquitetura moderna e desacoplada, separando claramente as responsabilidades de interface (Frontend), processamento de regras de negócio (Backend) e armazenamento/consulta de grandes volumes de dados (Data Lake).

A escolha do *stack* priorizou performance, escalabilidade e facilidade de manutenção.

### Frontend (Interface e Visualização)

O frontend foi construído com foco em interatividade e na experiência do usuário (UX), garantindo que cálculos complexos sejam refletidos na tela de forma instantânea.

* **Next.js & React:** Framework base da aplicação. Utiliza a abordagem de *Client Components* (`"use client"`) para gerenciar os estados de filtros, formulários de custos e reatividade dos componentes.
* **Tailwind CSS:** Framework utilitário de estilização, responsável por todo o layout responsivo, sistema de grid (ex: cards empilhados) e padronização visual da interface.
* **Recharts:** Biblioteca de Data Visualization (Data Viz) escolhida para a renderização fluida do `ScenarioChart`. Permite a exibição de gráficos de barras agrupadas e customização de *tooltips* com alta performance.
* **jsPDF & html2canvas:** Conjunto de bibliotecas utilizadas para a exportação de relatórios. O `jsPDF-autotable`gerencia a criação de documentos analíticos vetoriais, enquanto o `html2canvas` lida com o *Snapshot Visual* via renderização de Shadow DOM.

### Backend (Processamento e API)

A camada de backend atua como um motor de processamento estatístico, servindo de ponte entre o Data Lake e a interface do usuário.

* **Python:** Linguagem principal do serviço (`RevenueService`), escolhida por sua robustez e amplo ecossistema voltado a dados.
* **Pandas:** Biblioteca de manipulação de dados em memória. Após o backend receber os dados consolidados do banco, o Pandas é utilizado para calcular rapidamente as médias e os percentis estatísticos (P25, P50, P75) de faturamento.
* **AWS Data Wrangler (**`**awswrangler**`**) & Boto3:** O Boto3 gerencia as credenciais e sessões de segurança da AWS, enquanto o AWS Data Wrangler atua de forma otimizada para disparar as *queries* diretamente no Athena e converter os resultados nativamente para *DataFrames* do Pandas.

### Banco de Dados e Data Lake

A base de dados da aplicação não utiliza um banco relacional tradicional, mas sim uma estrutura de Data Lake, ideal para lidar com históricos massivos de mercado e faturamento diário.

* **AWS Athena:** Serviço de consultas interativas *serverless* da Amazon. Permite rodar comandos SQL diretamente nos arquivos armazenados no S3 (ex: bases do Airbnb e tabelas internas da Seazone como `daily_revenue_sapron`). A escolha do Athena elimina a necessidade de gerenciar infraestrutura de banco de dados e cobra apenas pelos dados escaneados em cada simulação.

### Infraestrutura e Deploy

O ecossistema de nuvem utiliza uma abordagem híbrida, extraindo os dados da AWS, mas hospedando o serviço na Google Cloud Platform (GCP) para simplificar o *deploy* e a gestão de containers.

* **Google Cloud Run:** Serviço de computação *serverless* da GCP utilizado para hospedar a API em formato de container Docker. Garante autoescalabilidade (crescendo conforme o número de usuários simulando dados) e cobrança apenas pelo tempo de execução.
* **Artifact Registry (GCR):** Repositório de imagens Docker (`gcr.io`) onde as versões do backend são empacotadas via `gcloud builds`.
* **Google Secret Manager:** Camada de segurança utilizada para injetar as credenciais sensíveis do Athena (`AWS_ACCESS_KEY_ID` e `AWS_SECRET_ACCESS_KEY`) diretamente nas variáveis de ambiente do Cloud Run, sem expor chaves no código-fonte.


# Engenharia de Dados e Backend (API)

A camada de backend foi estruturada em Python para atuar como um motor analítico de alta performance. O grande desafio desta arquitetura é garantir que as consultas (queries) enviadas ao AWS Athena retornem dados perfeitamente comparáveis entre a base do mercado (Airbnb) e a base interna da Seazone, exigindo um rigoroso tratamento de filtros e janelas de tempo.

### Tratamento e Normalização de Filtros

Para evitar erros de *match* causados por digitação ou formatação de dados divergentes entre as tabelas, a API implementa métodos robustos de normalização:

* **Sanitização de Strings (**`**_normalize_string**` **/** `**_normalize_sql**`**):** Os inputs do usuário (cidade, bairro, tipo) têm acentos removidos e são convertidos para letras minúsculas (lowercase) usando expressões regulares (Regex), tanto no código Python quanto via funções SQL nativas no Athena.
* **Conversão de Estados (De/Para):** Implementação de um dicionário dinâmico que converte nomes completos de estados recebidos do frontend (ex: "Santa Catarina") para a sigla geográfica exata esperada pela tabela interna da Seazone (ex: "SC"), garantindo o cruzamento de dados.
* **Mapeamento de Tipologia:** Injeção inteligente de sufixos na formatação de quartos (ex: o usuário seleciona "1", e o backend formata como "1q" para dar *match* perfeito com a coluna `group_name` do banco da Seazone).

### Consulta de Dados de Mercado (Airbnb)

A extração de dados da concorrência foca em garantir uma amostra estatisticamente relevante e limpa.

* **CTE de Cálculo de Ocupação (**`**tx_occup_calculation**`**):** Uma *Common Table Expression* (CTE) é utilizada para pré-agregar o faturamento anual, dias ocupados e dias disponíveis por imóvel (`airbnb_listing_id`), filtrando apenas anúncios ativos há pelo menos 6 meses.
* **Regra de Amostragem (Threshold):** Implementação de uma trava de segurança (`MIN_SAMPLE_SIZE = 10`). Se o filtro do usuário retornar menos de 10 propriedades na região, a API bloqueia a simulação e devolve um aviso de `INSUFFICIENT_DATA`, protegendo o cliente de análises baseadas em amostras irreais.

### Consulta de Dados Seazone

Executada em paralelo aos dados de mercado, essa consulta consolida o faturamento diário interno.

* **Cruzamento Estrutural:** A query faz um `INNER JOIN` entre a tabela transacional `daily_revenue_sapron` (receitas diárias) e tabelas de configuração `setup_groups` / `listing_status`.
* **Extração Dinâmica de Entidades:** Utilização de `split_part` e `MAX(CASE WHEN...)` para extrair, "on-the-fly", os atributos de localização (Estado, Cidade, Bairro) e tipologia (Tipo e Quartos) que estão contidos em strings compostas dentro da tabela de grupos.

### Alinhamento Temporal (Ano Móvel Fechado)

Um dos requisitos de negócio cruciais foi garantir a precisão da janela de comparação.

* **Lógica do Ano Móvel:** Em vez de usar filtros de dias quebrados (`interval '12' month`), a arquitetura aplica uma matemática de meses fechados. Extraímos o ano e o mês das datas (`EXTRACT(year FROM date)*100 + EXTRACT(month FROM date)`) para garantir que tanto o Airbnb quanto a Seazone considerem os mesmos últimos 12 meses inteiros, descartando o mês atual incompleto.

### Matemática Estatística e Percentis

Em vez de depender do banco de dados para os cálculos de quartis (o que exigiria processamento excessivo em SQL), a API transfere a carga matemática para o servidor local:

* **Pandas no Motor Financeiro:** O backend utiliza `pandas.DataFrame.quantile()` para processar rapidamente a matriz de faturamento dos imóveis e extrair a distribuição real do mercado em três fatias:
  * **P25 (25º Percentil):** Cenário Conservador.
  * **P50 (Mediana):** Cenário Médio.
  * **P75 (75º Percentil):** Cenário Otimista.
* **Cálculo de Eficiência da Carteira:** Para as métricas Seazone (ADR e Taxa de Ocupação Globais), o sistema soma todos os faturamentos e divide pelo total real de noites ocupadas e disponíveis, evitando as distorções que ocorreriam caso tirássemos uma média simples de médias diferentes.


# Lógica de Negócios e Métricas (KPIs)

O painel não atua apenas como um visualizador de dados estáticos, mas como um simulador financeiro interativo. Para garantir uma experiência ágil (sem telas de carregamento a cada alteração), grande parte da inteligência de precificação e dedução de custos foi isolada no *Client-side* (frontend).

### Faturamento Bruto vs. Líquido (Processamento Client-side)

A API (backend) sempre devolve a **Visão Bruta** (faturamento integral gerado pelo imóvel). A conversão para a **Visão Líquida** (dinheiro real no bolso do proprietário) ocorre instantaneamente no navegador do usuário utilizando o *hook*`useMemo` do React.

* **Composição de Custos:** O usuário pode preencher um formulário interativo (`ExpensesForm`) com:
  * **Custos Fixos Mensais:** Condomínio, IPTU, Energia, Internet, Água, Jardineiro, Piscineiro e Manutenção. O sistema multiplica esse bloco por 12 para encontrar o Custo Fixo Anual.
  * **Custos Variáveis (Taxas):** Porcentagem cobrada pelas plataformas (Taxa OTA, ex: Airbnb/Booking) e a taxa de gestão da propriedade (Taxa Seazone).
* **Fórmula de Dedução:** `Lucro Anual = Faturamento Bruto - (Faturamento Bruto * (Taxa OTA + Taxa Seazone)) - (Custo Fixo Mensal * 12)`.
* **Performance:** Como essa lógica roda no frontend, o usuário pode ligar/desligar a chave "Visão Líquida" ou alterar o valor do condomínio e ver todos os gráficos, cards e tabelas se reajustarem em milissegundos, sem precisar disparar novas requisições (consultas) caras ao AWS Athena.

### Fórmulas de Eficiência (KPIs)

Para garantir que a comparação entre um imóvel de R$ 50.000 e outro de R$ 150.000 seja justa, o dashboard utiliza métricas de eficiência padronizadas na hotelaria:

* **ADR (Average Daily Rate / Diária Média):** \* *Fórmula:* `Faturamento Total / Noites Ocupadas`.
  * *Objetivo:* Mostra o poder de precificação daquele imóvel ou da carteira Seazone na região. O cálculo ignora os dias em que o imóvel ficou vazio ou bloqueado, refletindo apenas o valor real pago pelos hóspedes.
* **Taxa de Ocupação:** \* *Fórmula:* `Noites Ocupadas / (Noites Ocupadas + Noites Disponíveis)`.
  * *Tratamento Visual:* Para evitar números quebrados de máquina (ex: `0.6345`), o frontend recebe o fator decimal da API e utiliza o formatador nativo do Javascript (`Intl.NumberFormat` com estilo `percent`) para exibir o dado cravado em duas casas decimais (ex: `63,45%`), transmitindo maior precisão na análise comercial.


# Frontend e Interface de Usuário

O frontend foi desenhado não apenas como um painel analítico, mas como uma ferramenta comercial persuasiva. A interface guia o olhar do usuário para a comparação de performance e simplifica a leitura de grandes volumes de dados.

### Estrutura do Dashboard

A tela principal segue uma hierarquia de informações focada na conversão e na interatividade:

* **Header Sticky e Ações Rápidas:** O cabeçalho permanece fixo no topo da tela (`sticky`), abrigando o título, o botão de exportação e a chave principal de "Visão Bruta / Líquida". Um *badge* com uma legenda explicativa (*tooltip*dinâmico) foi adicionado para deixar claro se os valores apresentados já descontam as taxas das plataformas OTA ou não.
* **Barra de Filtros (**`**FilterBar**`**):** Componente de seleção em cascata (Estado > Cidade > Bairro > Tipo > Quartos) alimentado dinamicamente pela API para evitar que o usuário pesquise combinações inexistentes.
* **Painel de Custos Colapsável (**`**ExpensesForm**`**):** Um painel deslizante que só aparece quando a "Visão Líquida" é ativada. Ele permite a personalização detalhada de todas as despesas fixas e variáveis da propriedade.

### Cards de Performance (Layout Empilhado)

Os KPIs principais (Faturamento Anual, ADR e Ocupação) foram estruturados para maximizar a legibilidade e o contraste entre as duas fontes de dados:

* **Layout 100% (Full-width):** A interface utiliza um layout empilhado (`flex-col`), onde o card do Mercado ocupa uma linha inteira e o card da Seazone ocupa a linha de baixo. Isso evita o "esmagamento" dos números em telas menores.
* **Separação Visual Clara:** \* **Mercado (Airbnb):** Utiliza tons de cinza e fundo neutro para estabelecer a "linha de base" (baseline).
  * **Seazone:** Utiliza gradientes suaves em azul e fontes destacadas para guiar a atenção do usuário para a nossa performance.
* **Fallback Inteligente:** Caso a Seazone não tenha propriedades na região filtrada, o painel exibe graciosamente um selo vermelho ("Sem dados na região") no cabeçalho do card e zera os indicadores, em vez de quebrar a interface.

### Gráfico de Cenários Comparativo (`ScenarioChart`)

A visualização de dados (Data Viz) foi projetada para impacto imediato durante uma argumentação de vendas.

* **Barras Agrupadas (Lado a Lado):** Utilizando a biblioteca Recharts, o gráfico de barras horizontais foi configurado com `barGap` para colocar a média da Seazone (Barra Azul) exatamente ao lado dos três cenários de mercado (Barras Cinzas: Conservador, Média, Otimista). Isso permite que o investidor veja se a média da Seazone supera até mesmo o cenário otimista da concorrência.
* **Legendas e Tooltips Educativos:** Ícones de informação (`Info`) com *tooltips* flutuantes foram adicionados ao cabeçalho do gráfico para educar o usuário sobre o que significam os percentis (25º, Mediana, 75º) na prática de mercado.

### Listagem e Detalhamento de Concorrentes (`PropertyTable`)

Para os usuários que desejam auditar os dados linha a linha (drill-down), o dashboard renderiza tabelas detalhadas de propriedades.

* **Ordenação Automática:** Os dados injetados na tabela sofrem um `.sort()` prévio no frontend, ordenando os imóveis sempre do maior faturamento para o menor, destacando os "Top Performers" no topo.
* **Renderização Dupla e Dinâmica:** O mesmo componente `<PropertyTable>` foi construído para aceitar parâmetros dinâmicos (props como `isSeazone`). Isso permite renderizar:

  
  1. **Tabela de Mercado (Airbnb):** Exibe o ID do imóvel como um hiperlink clicável (`ExternalLink`) que redireciona o usuário para a página real do anúncio no Airbnb.
  2. **Tabela Interna (Seazone):** Renderizada logo abaixo (condicionalmente, apenas se houver dados), listando os imóveis da carteira em tons de azul e utilizando os Códigos Internos da Seazone em formato de *badge*, sem links externos.


# Sistema de Exportação e Relatórios (PDF)

Para transformar o dashboard em uma ferramenta de vendas e relacionamento com investidores, foi implementado um robusto sistema de exportação *Client-side* (processado inteiramente no navegador do usuário). O sistema oferece duas abordagens de exportação para atender a diferentes necessidades de apresentação.

### Relatório Analítico (`jspdf` + `jspdf-autotable`)

Gera um documento vetorial de múltiplas páginas, ideal para leitura aprofundada, auditoria de dados e envio formal de propostas comerciais.

* **Cabeçalho e Metadados:** O PDF inicia registrando a data/hora da extração e os filtros exatos aplicados (Cidade, Bairro, Tipologia e Tamanho da Amostra), garantindo a rastreabilidade da análise.
* **Tabelas Comparativas:** O resumo financeiro e os cenários projetados utilizam o `autotable` para renderizar uma terceira coluna comparativa. Isso permite ao investidor ver o faturamento e a ocupação do Mercado (Airbnb) alinhados perfeitamente ao lado da Performance Seazone na mesma linha da tabela.
* **Listagem de Imóveis (Exportação de Dados):** O relatório anexa páginas finais contendo o detalhamento individual de todos os imóveis da região. Caso existam dados internos na mesma área, uma tabela separada e estilizada com a paleta da Seazone é gerada em uma nova página, listando nossos imóveis para comprovação do *benchmarking*.

### Snapshot Visual (`html2canvas`)

Gera uma "fotografia" exata dos gráficos, mapas e KPIs do dashboard, ideal para apresentações de impacto e visualização rápida.

* **Técnica de *Shadow DOM Rendering*:** Em vez de "printar" a tela que o usuário está vendo (o que causaria quebras de layout dependendo do tamanho do monitor ou celular), o sistema renderiza um container oculto (`#print-shadow-container`) em *background*.
* **Adaptação para Impressão:** Este container oculto possui regras CSS engessadas (largura fixa de 1280px) e substitui o layout responsivo padrão por um layout otimizado para papel:
  * Remoção do comportamento `sticky` do cabeçalho.
  * Força o alinhamento em linha (`flex-row`) da barra de filtros.
  * Fixa o grid do Gráfico e do Mapa em exatamente duas colunas simétricas.
  * Mantém os cards de Mercado e Seazone empilhados para melhor legibilidade dos números grandes.
* **Ajuste Automático para Folha A4:** O script captura esse DOM oculto em alta resolução (`scale: 2`), calcula a proporção geométrica da imagem (Ratio) e a centraliza vertical e horizontalmente em um documento PDF formato A4 Paisagem (Landscape), garantindo que nada fique cortado ou distorcido, independentemente do volume de dados da tela.


# Deploy, Segurança e Infraestrutura

A aplicação foi desenhada para operar em uma arquitetura *Serverless* (sem servidor dedicado), aproveitando o melhor de duas nuvens (Multi-Cloud): os dados residem na AWS (Athena/S3), enquanto a computação e a hospedagem da API rodam na Google Cloud Platform (GCP). Essa abordagem garante alta disponibilidade, escalabilidade automática e custos baseados apenas no uso real.

### Segurança e Gerenciamento de Secrets

Para garantir que chaves sensíveis não fiquem expostas no código-fonte (repositório) ou no *frontend*, adotamos práticas rigorosas de injeção de credenciais:

* **Integração Multi-Cloud Segura:** Como o backend Python (hospedado no Google Cloud) precisa consultar o AWS Athena, utilizamos o Boto3 configurado via variáveis de ambiente para a autenticação cruzada.
* **Google Secret Manager:** As chaves de acesso da AWS (`AWS_ACCESS_KEY_ID` e `AWS_SECRET_ACCESS_KEY`) foram cadastradas como "Secrets" nativos na GCP.
* **Injeção em Tempo de Execução:** Durante o deploy no Cloud Run, utilizamos a *flag* `--set-secrets` para injetar essas credenciais de forma criptografada diretamente no container. Isso garante que o serviço tenha acesso ao Data Lake da AWS de forma invisível e totalmente segura.

### Processo de CI/CD e Deploy (Cloud Run)

O empacotamento e a distribuição da API backend são feitos via containers Docker, garantindo que o código rode de forma idêntica tanto no ambiente de desenvolvimento quanto em produção.

* **Build da Imagem (Artifact/Container Registry):** Sempre que há uma atualização na lógica de negócios ou nas *queries* SQL, o código é empacotado em uma nova imagem Docker utilizando o comando `gcloud builds submit --tag ...`. Essa imagem fica armazenada com segurança no repositório privado da GCP (`gcr.io`).
* **Deploy Serverless (Google Cloud Run):** A atualização do serviço no ar é feita via linha de comando (`gcloud run deploy`), onde definimos:
  * `--platform managed`: Delega à infraestrutura do Google a responsabilidade de escalar a aplicação (de zero a múltiplas instâncias) conforme o volume de usuários utilizando o dashboard.
  * `--allow-unauthenticated`: Libera os *endpoints* da API para serem consumidos livremente pelo nosso frontend (Next.js).
  * `--set-env-vars`: Configurações padrão de ambiente, como a região de execução da AWS (`AWS_DEFAULT_REGION=us-west-2`), mantendo o código flexível e parametrizado.


# Guia de Deploy na Google Cloud Platform (GCP)

A aplicação utiliza o **Google Cloud Build** para empacotar o código em imagens Docker e o **Google Cloud Run** para hospedar e escalar os serviços de forma *serverless*. Todo o processo é feito via linha de comando (`gcloud CLI`).

**Pré-requisito:** Certifique-se de executar os comandos abaixo estando na pasta raiz de cada respectivo projeto (onde está localizado o arquivo `Dockerfile`).

### Deploy do Backend (API Python)

O backend exige injeção de credenciais de segurança e definição de região padrão para que o Boto3 consiga se autenticar e consultar o AWS Athena.

**Passo 1: Build da Imagem** Gera a imagem do container e a envia para o Google Container Registry (GCR).

```javascript
gcloud builds submit --tag gcr.io/data-resources-448418/backend-analise-faturamento-api .
```

**Passo 2: Deploy no Cloud Run** Publica a nova imagem em produção. Aqui, passamos a flag `--set-secrets` para injetar as chaves da AWS armazenadas no Secret Manager diretamente como variáveis de ambiente, garantindo total segurança.

```javascript
gcloud run deploy backend-analise-faturamento-api \
  --image gcr.io/data-resources-448418/backend-analise-faturamento-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-secrets=AWS_ACCESS_KEY_ID=AWS-ATHENA-ACCESS_KEY:latest,AWS_SECRET_ACCESS_KEY=AWS-ATHENA-SECRET-KEY:latest \
  --set-env-vars AWS_DEFAULT_REGION=us-west-2
```


---

### Deploy do Frontend (React / Next.js UI)

O frontend é uma aplicação estática/React que consome a API do backend. Como ele roda no navegador do cliente, não há injeção de *secrets* no momento do deploy.

**Passo 1: Build da Imagem** Gera a versão otimizada para produção do painel e envia para o Registry.

```javascript
gcloud builds submit --tag gcr.io/data-resources-448418/frontend-analise-fat-ui-service .
```

**Passo 2: Deploy no Cloud Run** Publica a interface do usuário e a torna acessível publicamente na internet (`--allow-unauthenticated`).

```javascript
gcloud run deploy frontend-analise-fat-ui-service \
  --image gcr.io/data-resources-448418/frontend-analise-fat-ui-service \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```


\