<!-- title: Expansão da Categorização (Regiões Similares) | url: https://outline.seazone.com.br/doc/expansao-da-categorizacao-regioes-similares-Ve5PfNocPE | area: Tecnologia -->

# Expansão da Categorização (Regiões Similares)

## **1. Resumo Executivo**

 O objetivo é estender a capacidade do modelo, atualmente funcional em um conjunto limitado de regiões, para **"regiões similares"**. A principal definição de "similaridade" adotada é a sazonalidade, focando em **regiões litorâneas** onde a Seazone já atua e possui dados de precificação. O projeto envolve validar a eficácia do modelo atual nessas novas regiões, adaptá-lo se necessário, e integrar a solução na pipeline de dados existente, considerando as restrições de custo e a necessidade de uma validação robusta.

## **2. Contexto e Objetivo do Projeto**

O projeto de categorização automática utiliza a API do Gemini para analisar imagens de imóveis e extrair features, alimentando o modelo de precificação (System Price). Inicialmente desenvolvido para Florianópolis, o modelo foi expandido para 12 regiões adicionais.

**O objetivo principal desta nova fase é:**

* Expandir o modelo para todas as **regiões litorâneas** onde a Seazone atua e coleta dados de preço.
* Validar se o modelo treinado existente é eficaz nessas novas regiões ou se necessita de adaptações/re-treinamento.
* Garantir que a expansão seja economicamente viável, controlando os custos da API do Gemini.
* Documentar o processo de expansão, criando um pipeline de validação que possa ser reutilizado no futuro.

## **3. Escopo do Projeto**

**3.1. Definição de "Regiões Similares"** Foram definidas como "regiões similares" aquelas que compartilham características de sazonalidade com as regiões já modeladas. O critério prático adotado é:

* **Regiões litorâneas** onde a Seazone possui operação.
* **Regiões onde  atua**, e a coleta de preços de concorrentes é realizada.

**3.2. Critérios de Inclusão de Imóveis** O escopo da expansão abrangerá todos os imóveis que:


1. Pertencem às novas regiões litorâneas definidas.
2. Fazem parte da lista de concorrentes dos quais a Seazone extrai preços.

## **4. Estado Atual e Desafios**

**4.1. Estado Atual**

* **Modelo:** Funcional para Florianópolis + 12 regiões.
* **Tecnologia:** Utiliza um Scrapper para baixar imagens e a API do Gemini (atualmente a versão 2.0) para criar features.
* **Custo:** A execução completa no escopo atual custa aproximadamente US$ 10-20 (ou R$ 200), dividido entre o custo do Scrapper e da API do Gemini.
* **Documentação:** A documentação da expansão anterior esta incompleta, contendo a fase até  Florianópolis, sem constar a expansão para as 12 regiões.

**4.2. Desafios e Considerações Chave**

* **Custo da API:** Rodar o modelo repetidamente em toda a base expandida para testes pode gerar custos elevados. É crucial desenvolver uma estratégia de testes com uma amostra menor para evitar gastos excessivos.
* **Validação do Modelo:** É necessário definir métricas claras para avaliar se o modelo mantém a performance (precisão, assertividade) nas novas regiões. A comparação deverá ser feita contra as métricas do modelo atual. 
* **Adaptação do Modelo:** Existe a incerteza se o modelo atual funcionará "out-of-the-box". Pode ser necessário:
  * Fazer pequenos ajustes.
  * Retreinar o modelo com um dataset que inclua as novas regiões.
  * Criar um modelo/configuração paralela especificamente para as novas regiões.
* **Integração:** Após a validação, o novo processo precisará ser integrado à pipeline de dados existente (AWS Lambda), modificando o código para incluir as novas regiões na execução mensal.


---

## **5. Plano de Ação - Próximos Passos**

**Fase 1: Entendimento e Preparação**


1. **Estudo do Projeto Atual:** Imersão na lógica do modelo existente, código, documentação disponível e conversas alinhadas com Márcio para entender os pormenores da expansão anterior.
2. **Definição da Base de Dados:** Mapear e preparar a lista completa de imóveis dentro do novo escopo (regiões litorâneas onde o System Price atua).

**Fase 2: Teste e Validação Controlada** 

3\.  **Estratégia de Teste de Baixo Custo:** Definir uma amostra representativa (ex: uma única cidade ou um subconjunto de imóveis) para os testes iniciais, evitando rodar o modelo na base completa.

4\.  **Execução dos Testes:** Rodar o modelo na amostra definida e coletar as métricas de performance.

5\.  **Análise Comparativa:** Comparar os resultados do modelo expandido com as métricas do System Price atual para a mesma amostra, identificando desvios de performance.

**Fase 3: Adaptação e Validação Final** 

6\.  **Iteração e Adaptação:** Com base na análise, decidir o caminho:

* Se a performance for satisfatória, prosseguir. 
* Se não, investigar a necessidade de novas features, re-treinamento ou ajustes no prompt do Gemini. 

7\.  **Execução em Escala Completa:** Após a validação, executar o processo em toda a base de dados das novas regiões para popular a tabela inicialmente.

**Fase 4: Integração e Documentação** 

8\.  **Integração na Pipeline:** Modificar o código do Lambda na pipeline de DAW para que a nova expansão seja incluída nas execuções mensais automatizadas. 

9\.  **Documentação Final:** Documentar todo o processo de descoberta, teste, validação e integração, criando um guia para futuras expansões.

#### **6. Oportunidades e Melhorias Adicionais**

* **Avaliação da API Gemini 2.5:** Testar a versão mais recente da API do Gemini para verificar se oferece uma melhoria significativa na qualidade da categorização, avaliando se o ganho de performance justifica um possível aumento de custo.
* **Criação de um Pipeline de Validação:** Desenvolver um pipeline de validação automatizado e reutilizável. Isso permitiria testar futuras alterações no modelo (novas features, mudanças de API, etc.) de forma estruturada e segura.

#### **7. Anexos e Referências**

* **Gravação da Reunião de Discovery:** [Link para o Fathom](https://fathom.video/share/MKC5s4AB5zJM2nzVfs5Mg9iNiHDJxdPF)
* **Documentação de Referência:** **[Categorização automática de Strata](https://outline.seazone.com.br/doc/categorizacao-automatica-de-strata-4zxO7W9qzi)**
* **Apresentação de Escopo:** [MVP - Categorização Automática](https://docs.google.com/presentation/d/19jNiQIIZw11ygJd0qFEKuTA3f7LYngiyyWFgUkuyDNs/edit?slide=id.g22420e645c0_0_72#slide=id.g22420e645c0_0_72)
* **Planilha de Regiões:** [Expansão Categorização Preço](https://docs.google.com/spreadsheets/d/1I2X1HycNBlyZHP9aV1a4nmcUXYnisAcgRHEB2MpG3Go/edit?gid=1707241059#gid=1707241059)