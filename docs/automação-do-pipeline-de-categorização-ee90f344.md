<!-- title: Automação do Pipeline de Categorização | url: https://outline.seazone.com.br/doc/automacao-do-pipeline-de-categorizacao-gyejTp8bOJ | area: Tecnologia -->

# Automação do Pipeline de Categorização

### **Discovery da Call: Automação do Pipeline de Categorização**

**Data:** 06 de Agosto\n**Participantes:**

* Lucas Abel da Silveira (PM)
* Lucas Machado Azevedo (Stakeholder/Manager)
* Márcio Fazolin (Desenvolvedor Original - DS)
* Lander Souza Crispim (Desenvolvedor de Produção - Engenheiro de ML/Dados)

**Objetivo Principal da Call:** Realizar a passagem de conhecimento do projeto MVP de categorização, desenvolvido por Márcio, para Lander, que será responsável por automatizá-lo e colocá-lo em produção.

### **Resumo do Status Atual e Visão do Produto**

O projeto atual é um pipeline de classificação de imóveis do Airbnb em "stratas" de qualidade, composto por três etapas principais:


1. **Scraping:** Baixa imagens e metadados de anúncios do Airbnb.
2. **Feature Extraction (IA Generativa):** Usa o Gemini (via Vertex AI) para analisar as imagens e gerar scores de qualidade (mobília, acabamentos, etc.).
3. **Classificação (Machine Learning):** Um modelo de Regressão Logística usa os scores do Gemini e outros dados (faturamento, nº de quartos) para prever a "strata" final do imóvel.

**Dor Principal:** O processo é **totalmente manual e fragmentado**. Cada etapa precisa ser executada separadamente, com scripts e notebooks que não estão preparados para produção, envolvendo muitas "gambiarras" e soluções temporárias.


**Visão do Produto (PM):**

* **Automatização de Ponta a Ponta:** Criar um pipeline automatizado que possa ser executado com um *trigger* (ex: mensalmente).
* **Fluxo Contínuo:** O pipeline deve automaticamente:

  
  1. Identificar e scrapar novos listings.
  2. Extrair features visuais com Gemini para os novos listings.
  3. Aplicar o modelo de ML para gerar a strata.
  4. Salvar o resultado final em um banco de dados.
* **Escalabilidade:** A solução deve ser projetada para ser facilmente expandida para novas regiões (além de Florianópolis) e para permitir futuras modificações no modelo.


### **Pontos Chave e Dores Identificadas por Etapa do Pipeline**

#### **1. Scraping de Imagens e Metadados**

* **Ferramentas:** Util-dados (repositório GitHub), Cloud Run, Pub/Sub.
* **Processo Atual:**
  * Um script inicial gera a lista de IDs para scrapar.
  * Um segundo script baixa um arquivo metadata.json para cada ID de imóvel e o salva em uma pasta específica no Cloud Storage.
  * Um terceiro script lê esse metadata.json e baixa as imagens correspondentes.
  * A comunicação entre as etapas é feita via Pub/Sub.
* **Dores e Problemas Identificados:**
  * **Fragilidade:** O processo é manual e não possui um bom sistema de tratamento de erros. Se uma imagem falha ao baixar, não há um log claro do que foi perdido.
  * **Estrutura de Dados Ineficiente:** O metadata.json é salvo individualmente dentro da pasta de cada imóvel no Cloud Storage. Para processar todos, é preciso listar *todos* os arquivos do bucket e filtrar, o que é lento e ineficiente.
  * **Manutenção:** As filas do Pub/Sub foram deletadas após o uso, exigindo recriação manual para rodar novamente.


#### **2. Extração de Features com Gemini (Vertex AI)**

* **Ferramentas:** Vertex AI, Jupyter Notebooks.
* **Processo Atual:**
  * Um notebook lê os arquivos metadata.json espalhados pelo bucket
  * Utiliza a API do Vertex AI (e não o Gemini padrão) para poder passar os links das imagens diretamente do Cloud Storage, evitando o download local.
  * O prompt solicita notas de 0 a 100 para 6 características e a identificação de imagens irrelevantes ("BadImage").
* **Dores e Problemas Identificados:**
  * **Gestão de Cotas e Erros:** O código atual não trata bem os erros de cota da API (requests por minuto) nem outros possíveis erros (ex: imagem corrompida). A solução temporária foi rodar o processo em lotes manuais e sequenciais (100 linhas, depois 200, etc.), o que é inviável para produção.
  * **Redundância e Custo:** Não há um mecanismo automático para verificar se um imóvel já foi processado. A regra de negócio para evitar reprocessamento era controlada manualmente pelo desenvolvedor.
  * **Organização do Código:** O código de extração está espalhado em notebooks que serviram para testes, tutoriais e o projeto final, sem uma clara separação. O notebook final (modelo_florianopolis_production_final.ipynb) contém todo o fluxo, desde a leitura de dados até a modelagem, de forma desorganizada.


#### **3. Modelo de Machine Learning e Classificação**

* **Ferramentas:** Jupyter Notebook, Scikit-learn.
* **Processo Atual:**
  * O mesmo notebook modelo_florianopolis_production_final.ipynb contém a lógica.
  * Ele importa múltiplos arquivos (features do Gemini, dados de polígonos, dados internos de faturamento/reviews).
  * Realiza uma extensa criação e filtragem de features.
  * O modelo final é um LogisticRegression simples, precedido por um StandardScaler, usando um conjunto específico de 10 features.
* **Dores e Problemas Identificados:**
  * **Código "Exploratório":** O notebook é um artefato de exploração e não um script de produção. Contém muito código comentado, testes, visualizações e funções legadas que não são usadas no modelo final. Não está "enxuto".
  * **Complexidade Oculta:** O processo para chegar ao modelo final envolveu muitos testes e pipelines customizadas que, embora não estejam no modelo final, estão no código, tornando-o difícil de entender e manter.


### **Requisitos e Decisões Técnicas para a Produção**

* **Plataforma:** O pipeline deve ser implementado no **GCP** (Google Cloud Platform) para aproveitar os créditos existentes.
* **Colaboração:** Lander  deve colaborar com Hideki (Scrapers) para quaisquer modificações necessárias no scraper, sem precisar mergulhar a fundo no código dele.
* **Otimização de Dados:** O metadata.json deve ser transformado de arquivos individuais para uma **tabela centralizada**, preferencialmente no **BigQuery**, com uma coluna para o ID do imóvel, facilitando consultas e processamento.
* **Tratamento de Erros:** O pipeline precisa ser robusto, com tratamento de erros em todas as etapas, especialmente na comunicação com APIs externas (Scraper, Vertex AI). Implementar *retries* com *exponential backoff* (ou um simples *sleep*) para lidar com erros de cota é crucial.
* **Idempotência:** O sistema deve ser capaz de identificar listings já processados para não reprocessá-los desnecessariamente, economizando custos de API e tempo de processamento. A regra inicial será: "se o ID do imóvel já existe, não reprocessar". A verificação de mudança de imagens é um complicador a ser deixado para o futuro.
* **Refatoração de Código:** O código dos notebooks precisa ser massivamente refatorado e organizado em scripts Python modulares e testáveis. A lógica de exploração de dados deve ser separada da lógica de treinamento e predição.
* **Gerenciamento de Ferramentas:** A escolha das ferramentas de orquestração no GCP (ex: Cloud Composer/Airflow, Vertex AI Pipelines, Cloud Functions + Pub/Sub) fica a cargo do time técnico, sempre balanceando otimização de custo e velocidade de desenvolvimento.

Links importantes: 

```markup
https://github.com/seazone-tech/Util-dados/tree/main/gcp/airbnb-image-scraper
https://console.cloud.google.com/storage/browser/image-scraper?pageState=(%22StorageObjectListTable%22:(%22f%22:%22%255B%255D%22))&authuser=1&hl=en&inv=1&invt=Ab4wfg&project=sandbox-439302
https://console.cloud.google.com/run/jobs/details/us-central1/image-scraper/executions?project=sandbox-439302&authuser=1&hl=en&inv=1&invt=Ab4wfg
https://console.cloud.google.com/cloudpubsub/topic/detail/image-metadata-input?authuser=1&hl=en&inv=1&invt=Ab4wfg&project=sandbox-439302
https://github.com/seazone-tech/Util-dados/tree/main/data-solutions/image_score_model
https://console.cloud.google.com/storage/browser/categorizacao;tab=objects?forceOnBucketsSortingFiltering=true&authuser=1&hl=en&inv=1&invt=Ab4wfg&project=services-440319&prefix=dataset_tables&forceOnObjectsSortingFiltering=false
https://docs.google.com/presentation/d/19jNiQIIZw11ygJd0qFEKuTA3f7LYngiyyWFgUkuyDNs/edit?slide=id.g3522903c1b1_0_0#slide=id.g3522903c1b1_0_0
```


\