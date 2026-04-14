<!-- title: Panorama de Aluguel por Temporada - Análise Exploratória e Proposta | url: https://outline.seazone.com.br/doc/panorama-de-aluguel-por-temporada-analise-exploratoria-e-proposta-ZcQvQ0qgNg | area: Tecnologia -->

# Panorama de Aluguel por Temporada - Análise Exploratória e Proposta

**Data:** 09/07/2025\n**Autor:** Lucas Abel da Silveira (PM de Dados)

**Stakeholders:** Leandro Shimanuki (Diretor de Marketing)

#### **1. Contexto**

O relatório **"Panorama do Aluguel por Temporada no Brasil"** é um dos ativos de dados mais estratégicos da Seazone. Lançado anualmente, ele nos posiciona como uma **autoridade de mercado**, gerando brand awareness, confiança e sendo utilizado como fonte de referência por portais de notícia, investidores e proprietários.

O objetivo deste projeto é dar continuidade a essa iniciativa, evoluindo o material para o "Panorama 2026" (com dados de 2025) e estabelecendo um processo robusto e replicável para os anos futuros. Esta primeira fase é de natureza **exploratória, analítica e de proposição**, e servirá como base para a construção do novo modelo do panorama.

#### **2. O Desafio Central: A Mudança na Coleta de Dados de 2024**

O principal obstáculo para a continuidade do panorama é uma mudança fundamental na nossa estratégia de coleta de dados, ocorrida em 2024.

* **Cenário Pré-2024:** Coletávamos dados de preço e ocupação de um universo de aproximadamente **540.000 imóveis** no Brasil. Isso nos permitia calcular o faturamento total de uma região com alta precisão, através de uma soma direta dos dados observados.
* **Cenário Pós-2024:** Otimizamos nossos custos e foco. Hoje, coletamos dados de preço e ocupação de um subconjunto de aproximadamente **60.000-70.000 imóveis**, que classificamos como **"qualificados"** (concorrentes diretos, imóveis com maior potencial de faturamento, etc.). Ainda conhecemos o número total de imóveis (\~540k) e suas características, mas não temos mais o faturamento direto para o universo completo.

Este novo cenário invalida a metodologia antiga. Uma simples soma do faturamento dos imóveis qualificados resultaria em uma queda drástica e irreal nos números, quebrando a série histórica e gerando conclusões equivocadas sobre o mercado.

#### **3. Dores e Dificuldades**

A não resolução deste desafio acarreta em:


1. **Quebra de Continuidade Histórica:** A incapacidade de comparar a evolução do mercado ano a ano, que é o principal valor do panorama.
2. **Risco Reputacional:** Publicar dados que não refletem a realidade do mercado pode minar nossa credibilidade como fonte de autoridade.
3. **Distorção Analítica:** As análises de faturamento regional, municipal e estadual seriam subestimadas, tornando-as inutilizáveis.
4. **Perda de Oportunidade Estratégica:** A falha em produzir o panorama nos faz perder um importante canal de posicionamento de marca e geração de leads.


#### **4. Objetivos da Fase de Discovery**

Esta fase tem como objetivo principal gerar uma proposta fundamentada de como podemos dar continuidade ao Panorama. O Data Scientist responsável deverá focar em quatro pilares:

**Pilar 1: Análise e Mapeamento de Dados**

* **Tarefa:** Familiarizar-se com as tabelas de dados relevantes (listings, details, occupancy, pricing, etc.).
* **Resultado Esperado:** Mapeamento claro de onde encontrar cada informação necessária para replicar as métricas do panorama antigo e das novas solicitadas no arquivo Dados necessários.csv.

**Pilar 2: Desenvolvimento de um Modelo de Estimativa (O Core da Discovery)**

* **Tarefa:** ais modelos estatístiPropor e validar um ou mcos para estimar o faturamento total de uma localidade (cidade, estado) com base na nossa amostra de imóveis "qualificados".
  * Analisar o perfil e a distribuição da nossa amostra de "qualificados" em comparação com o universo total de imóveis. A nossa amostra é enviesada? Como podemos corrigir esse viés?
  * Estudar a correlação entre as características dos imóveis (quartos, amenities, localização) e o faturamento observado na nossa amostra.
  * Propor um modelo para "escalar" o faturamento da amostra para o universo total. Exemplo: *Se os imóveis qualificados representam X% do total de listings de uma cidade e geram um faturamento Y, como podemos estimar o faturamento dos (100-X)% restantes?*
* **Resultado Esperado:** Uma análise detalhada com a proposta de uma metodologia de estimativa, incluindo a quantificação do **intervalo de confiança** e da **margem de erro** associada.

**Pilar 3: Validação de Métricas e Análise de Viabilidade**

* **Tarefa:** Analisar cada métrica solicitada no arquivo Dados necessários.csv e no relatório de 2024.
* **Resultado Esperado:** Um parecer técnico para cada métrica, respondendo:
  * É possível gerar este dado com a nossa configuração atual?
  * Qual o nível de confiança/precisão que teremos (direto, estimado com baixo erro, estimado com alto erro)?
  * Quais são as premissas e limitações?

**Pilar 4: Proposta de Novas Análises (Estudos de Valor Agregado)**

* **Tarefa:** Ir além do solicitado e, com base na exploração dos dados (especialmente amenities e características dos imóveis), propor novos estudos e insights de alto valor para o Marketing.
  * **Exemplos a serem explorados:**
    * Qual o impacto no faturamento e na ocupação de um imóvel ter Ar-condicionado em capitais do Nordeste vs. cidades na Serra Gaúcha?
    * Imóveis pet-friendly faturam, em média, mais que os não-pet friendly? Essa diferença varia por região?
    * Qual a correlação entre a nota do anfitrião (gestão individual) e a taxa de ocupação?
* **Resultado Esperado:** Uma lista de 3 a 5 novas análises/narrativas, com uma breve descrição do seu potencial de mercado e a viabilidade técnica de execução.

\n**5. Entregável Esperado ao Final da Fase**

O resultado final desta fase de Discovery será um **documento de proposta técnica e analítica** a ser apresentado para o time de Marketing. Este documento deve conter:


1. **Resumo do Desafio e da Solução Proposta:** Uma síntese clara do problema e da metodologia de estimativa recomendada.
2. **Metodologia de Estimativa Detalhada:** Explicação do modelo estatístico, premissas, e a margem de erro e intervalo de confiança esperados para as principais métricas (faturamento, ocupação, diária média).
3. **Matriz de Viabilidade de Métricas:** Uma tabela indicando o status de cada métrica solicitada (Viável, Viável com ressalvas, Inviável) e as observações pertinentes.
4. **Catálogo de Novas Análises:** Detalhamento das novas propostas de estudos, com exemplos de como poderiam ser apresentados no panorama.
5. **Riscos e Próximos Passos:** Identificação de possíveis riscos e um esboço do plano de ação para a fase de construção do novo panorama.


#### **6. Recursos e Ferramentas**

* **Documento de Referência:** <https://drive.google.com/file/d/1_MwIe9SRd4OB-GU1FQn3HxMrNlKM8XBG/view?usp=sharing>
* **Lista de Métricas Desejadas:** [Dados necessários - Panorama](https://docs.google.com/spreadsheets/d/1_9qHRj1PV7QVpSV5QIC2HmXucTVdrxv6a3cOzH79e3I/edit?gid=0#gid=0) 
* **Contexto da Reunião:** [Gravação e resumo da reunião "Dados marketing - Panorama do Aluguel por Temporada - July 08"](https://fathom.video/share/6jxPqLGXdFT-nk1s6bm7yD2PLJ7xKp1-?tab=summary&utm_campaign=postmeetingsummary&utm_content=view_recording_link&utm_medium=email).
* **Acesso ao Banco de Dados: <https://us-west-2.console.aws.amazon.com/athena/home?region=us-west-2#/query-editor>**
* \