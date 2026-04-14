<!-- title: Detecção de Anomalias de Ocupação | url: https://outline.seazone.com.br/doc/deteccao-de-anomalias-de-ocupacao-Qpttkpuwlz | area: Tecnologia -->

# Detecção de Anomalias de Ocupação

### **1. Contexto do Produto**

**Problema:**\nNossos modelos de detecção de bloqueios (heurística + XGBoost + redes neurais) **falham em distinguir bloqueios intencionais de locações reais**, gerando distorções críticas na estimativa de faturamento de imóveis. Isso compromete:

* **Precificação estratégica:** Decisões baseadas em dados irreais de concorrentes.
* **Análise de sazonalidade:** Projeções de demanda distorcidas.
* **Confiança interna:** Times de BI e operação questionam a qualidade dos dados.

### **2. Dor Principal**

**Estimativas de faturamento que não refletem a realidade operacional dos imóveis**, gerando:

* Precificação incorreta em nossas próprias unidades;
* Análises de mercado distorcidas;
* Projeções financeiras imprecisas para novos investimentos.

O problema **não está nos preços coletados** (já validamos que erros de preço são raros), mas sim na **classificação incorreta de datas como "alugadas" quando, na verdade, estavam bloqueadas** — ou vice-versa.

Isso ocorre especialmente em cenários onde:

* O anfitrião **define preços artificialmente altos** (para evitar locações sem remover o anúncio);
* O anfitrião **bloqueia com preços baixos** (por exemplo, para "reservar" datas para uso próprio, mas mantendo o calendário com valores simbólicos);
* Há **padrões sazonais atípicos** que contradizem o comportamento esperado da região.

### **3. Onde o Problema Acontece**

O erro se manifesta **após a etapa de detecção de bloqueios**, ou seja:

* Os modelos atuais **não conseguem capturar todos os padrões de comportamento anômalo** dos anfitriões;
* A heurística existente **não é suficiente para cobrir a diversidade de estratégias de gestão de calendário** usadas na prática.

O problema **não é localizado**: afeta imóveis em:

* Regiões **sazonais de verão** (ex: Campeche/SC, Rio, Nordeste);
* Regiões **sazonais de inverno** (ex: Gramado/RS, Campos do Jordão/SP);
* Regiões **não sazonais** (ex: Goiânia, Brasília, cidades do interior).

Portanto, **não podemos assumir que a anomalia segue um único padrão** — ela varia conforme o comportamento do anfitrião e o contexto regional.

### **4. Evidências Reais (Casos Observados) \[[planilha com cases](https://docs.google.com/spreadsheets/d/14ik3vgwn0K4-cF7J4SNDQJvtLSzURqzv2_HHrY1bBgk/edit?gid=1883901746#gid=1883901746)\]**

**Caso 1: Faturamento alto em baixa temporada com preços irreais**

* **Imóvel**: `15120841` (Campeche – sazonalidade de verão)
* **Problema**:
  * Agosto/2025: faturamento de R$68.815 com **31 dias ocupados** e **preço médio de R$2.220/dia**.
  * Setembro/2025: R$40.854 com **25 dias ocupados** e **preço médio de R$1.634/dia**.
* **Contexto**: Em Campeche, os meses de pico são **dezembro, janeiro e fevereiro**. Agosto/setembro são de baixa demanda.
* **Indício**: Preços absurdamente acima da média de alta temporada → **altíssima probabilidade de bloqueio com preço inflado**, mas classificado como "alugado".

**Caso 2: Padrão invertido de sazonalidade + preços suspeitos**

* **Imóvel**: `1134994259772620896` (Campeche)
* **Problema**:
  * Janeiro/fevereiro: preço médio de **R$100**, ocupação alta → valor **muito abaixo do esperado** para alta temporada.
  * Abril–junho: preços saltam para **R$378–R$840**, com picos diários acima de **R$1.600** em junho.
* **Indício**:
  * Janeiro/fevereiro: possível **bloqueio com preço simbólico** (classificado como alugado).
  * Junho: preços elevados em baixa temporada → **possível bloqueio com preço alto**, também classificado como alugado.

> **Observação**: ambos os casos passaram por todos os tratamentos atuais (heurística + 2 modelos de ML) e **não foram corrigidos**.

### **5.** Lições de Iniciativas Anteriores

Um projeto anterior tentou usar **Autoencoders e cluster para detecção de anomalias**, mas **falhou** por:

* Falta de alinhamento entre Data Science e regras de negócio;
* Modelo treinado sem considerar **sazonalidade regional**, **tipologia de imóvel** e **comportamento real de anfitriões**;
* Ausência de **validação com casos reais antes da implementação**.

**Aprendizado**: qualquer nova abordagem **precisa partir do entendimento profundo do domínio**, não apenas de técnicas estatísticas.

### **6. Plano de Investigação: Da Raiz à Solução**

\nPara evitar repetir erros passados, propomos uma abordagem **focada em diagnóstico antes da solução**:

\n**Fase 1: Mapeamento do Sistema Atual**

**Objetivo:** Entender como os modelos de detecção funcionam e onde falham.\n**Atividades:**

* **Analise e investigação junto com o time:** Documentar regras de heurística, features do XGBoost e arquitetura da rede neural.

  \

**Fase 2: Caça a Casos Reais**

**Objetivo:** Identificar e documentar **o máximo de perfis de erro** no Brasil.

**Metodologia:**

* **Amostragem Estratificada:** Selecionar imóveis de:
  * 5 regiões com sazonalidades distintas (litoral, serra, urbano, interior, Nordeste).
  * 3 perfis de sazonalidade (verão, inverno, não sazonal).
  * Diferentes níveis de preço (baixo, médio, alto).
* **Análise Qualitativa:**
  * Revisão manual de X imóveis (N por região) para classificar erros.
  * Estudo e analise das características das regiões (ex: "Este preço faz sentido para Gramado no inverno?").

**Entregável:** Catálogo de casos de erro com:

* Descrição do padrão (ex: "bloqueio com preço alto em baixa temporada").
* Causa raiz suspeita (ex: "modelo ignora sazonalidade regional").
* Impacto no faturamento (ex: "superestimativa de 200%").


**Fase 3: Prototipação da Solução**

**Objetivo:** Testar uma abordagem **hierárquica** (mensal → diário) **apenas se** as fases anteriores validarem sua necessidade.\n**Premissas:**

* **Passo 1:** Detector de anomalias mensais para flagrar meses suspeitos.
* **Passo 2:** Revisão diária desses meses para corrigir bloqueios.\n**Critérios de Sucesso:**
* Cobertura de 100% dos casos identificados na Fase 2.
* Taxa de falso positivo < 5%.


### **7. Plano de Implementação da solução validada**

**Fase 1: Implementação do Pipeline Manual**

**Objetivo:** Validar a solução em escala controlada, com intervenção humana, para ajustar regras e garantir eficácia antes da automação.

**Atividades:**


1. **Escopo Controlado:**
   * Selecionar **3 regiões críticas**  e **100 imóveis** por região.
   * Executar manualmente o fluxo de detecção de anomalias mensais → correção diária.
2. **Ferramentas de Apoio:**
   * Scripts em **Python/SQL** para:
     * Identificar meses anômalos (usando limiares definidos na prototipação).
     * Gerar relatórios diários para correção (ex: lista de dias com preços suspeitos).
   * Planilhas controladas para validação humana (ex: classificar "bloqueio confirmado" vs. "locação real").

**Entregáveis:**

* Relatório de eficácia (ex: "85% dos erros corrigidos manualmente").
* Lista de ajustes necessários para automação (ex: "incluir feriados locais como variável").

**Critérios de Sucesso:**

* Redução de >80% nos erros de faturamento para os imóveis testados.

**Fase 2: Análise e Definição de Arquitetura**

**Objetivo:** Definir **onde e como** a solução será integrada ao pipeline existente, garantindo escalabilidade e alinhamento técnico.


**Atividades:**


1. **Mapeamento do Pipeline Atual:**
   * Documentar o fluxo de dados:
   * \[Coleta de Dados\] --> \[Tratamento/Limpeza\]  -->C\[Modelos de Detecção de Bloqueios\]  --> \[Enriquecimento\]  --> \[Tabelas de Faturamento\]

     \
   * Identificar **ponto de inserção ideal** para a nova etapa:
     * **Opção A:** Após os modelos de bloqueio (pré-enriquecimento).
     * **Opção B:** Como camada de correção pós-enriquecimento.

**Requisitos Técnicos:**

| **Requisito** | **Descrição** |
|----|----|
| **Escalabilidade** | Processar todos os imóveis do Brasil com frequência conforme workflow inserido. |
| **Monitoramento** | Métricas de performance (ex: % de anomalias detectadas). |


**Entregáveis:**

* Diagrama de arquitetura aprovado por Engenharia de Dados.
* Documentação de integração com o pipeline existente.
* Especificação de APIs/interfaces entre componentes.


#### **Fase 3: Implementação do Pipeline Automático**

**Objetivo:** Desenvolver e implantar a solução em produção, integrada ao ecossistema de dados.

\n**Atividades:**


1. **Desenvolvimento:**
   * Construir jobs de:
     * **Detecção de anomalias mensais** (nível agregado).
     * **Correção diária** para meses anômalos (regras + ML(caso utilizado)).
   * Orquestração via **Airflow** ou **Step Functions**.\n
2. **Testes:**
   * **Testes de Carga:** Simular processamento de todos os imóveis do Brasil.
   * **Testes de Regressão:** Garantir que não introduza novos erros.
   * **Testes de Aceitação:** Validar em ambiente de staging.

**Deploy em Produção:**

* Implementação automática do fluxo.
* Monitoramento pós-lançamento

**Entregáveis:**

* Pipeline automatizado em produção.
* Monitoramento (ex: taxa de falsos positivos por região).
* Documentação operacional.

**Critérios de Sucesso:**

* Processamento de 100% dos imóveis dentro da janela de atualização.
* Redução nos erros de faturamento por bloqueios mal classificados.