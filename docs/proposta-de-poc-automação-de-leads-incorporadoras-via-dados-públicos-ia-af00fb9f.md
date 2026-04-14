<!-- title: Proposta de POC: Automação de Leads (Incorporadoras) via Dados Públicos + IA | url: https://outline.seazone.com.br/doc/proposta-de-poc-automacao-de-leads-incorporadoras-via-dados-publicos-ia-b6PG0lqWyk | area: Tecnologia -->

# Proposta de POC: Automação de Leads (Incorporadoras) via Dados Públicos + IA

**Objetivo Principal:** Validar a viabilidade técnica e financeira de automatizar a geração de leads qualificados (Incorporadoras/Construtoras) utilizando dados da Receita Federal enriquecidos via Web e IA, sem infraestrutura complexa nesta etapa.

**Escopo da POC (Micro-Teste):**

* **Região:** Florianópolis - SC (Matriz/Filial).
* **Segmento:** Incorporadoras e Construtoras (CNAEs específicos definidos no projeto original).
* **Resultado Esperado:** Gerar uma lista final curada de leads. **O volume de leads qualificados para uma cidade será um dos principais aprendizados da POC.**

### \n1. Metodologia de Execução (Local & Low-Code)

A execução será manual (scripts rodados localmente), dividida em 3 etapas de funil para garantir custo zero/mínimo:


1. **ETL & Higienização (Python/Pandas):**
   * Reaproveitamento do código do Stakeholder (José) para leitura dos arquivos .ESTABELE da Receita.
   * **Filtro Rígido:** Apenas MUNICIPIO = 'FLORIANOPOLIS' + CNAE Primário de construção + Exclusão de termos negativos na Razão Social (ex: "Condomínio", "Associação").
2. **Enriquecimento (Busca Web):**
   * Script simples para buscar "\[Razão Social\] site" no Google/Bing (usando camadas gratuitas de API ou Scraping leve).
   * Objetivo: Encontrar a URL oficial e validar se a empresa tem "pegada digital".
3. **Classificação Inteligente (IA):**
   * Uso de LLM (Gemini Flash ou similar em tier gratuito) apenas para os casos onde um site foi encontrado.
   * *Input:* Texto da Homepage. *Output:* "Esta empresa vende imóveis? Sim/Não".

### 2. Definição de Papéis

* **Lucas Machado (Tech Lead):** Definição da lógica dos scripts, revisão de código e garantia de que não haverá custos de infraestrutura (Cloud).
* **Equipe de Dados (Execução):** Refinamento do script Python, execução da busca web e integração com a IA.
* **José Monteiro (Stakeholder/Sales Ops):**
  * **Input:** Fornecer lista de "Palavras Negativas" (o que não queremos).
  * **Validação:** Auditar a lista final de leads de Floripa para confirmar se são aderentes ao ICP (Perfil de Cliente Ideal).
  * **Definição de Sucesso:** Definir os KPIs quantitativos para a aprovação da POC (ver seção abaixo).

### 3. Métricas de Sucesso (KPIs da POC)

A POC será considerada um sucesso se atingirmos os indicadores de negócio e técnicos abaixo. Os valores-alvo de negócio serão definidos em conjunto com a área de Sales Ops.


1. **Taxa de Enriquecimento:** Qual a taxa mínima de sucesso na busca por sites válidos para que o processo seja considerado viável? **\[A ser definido pelo José Monteiro\]**
2. **Precisão da Ferramenta:** Qual o percentual mínimo de acerto na classificação final (leads realmente aderentes) para que a ferramenta seja confiável? **\[A ser definido pelo José Monteiro\]**
3. **Ganho de Produtividade:** O processo deve ser drasticamente mais rápido que a prospecção manual. Qual o ganho de tempo esperado (vs. 2-3h/dia) para justificar o investimento futuro no projeto? **\[A ser definido pelo José Monteiro\]**
4. **Custo x Benefício (Técnico):** O custo computacional/API deve ser próximo de zero. 

### 4. Stack Tecnológica (Padrão Atual)

* **Linguagem:** Python 3.10+ (Pandas, PyArrow, Requests, BeautifulSoup).
* **Ambiente:** Local (VS Code / Jupyter Notebooks). t
* **Formatos:** Leitura em Parquet, entrega final em Excel (para validação do time de Vendas).

### 5. Fontes Alternativas (Para Roadmap Futuro)

Além da Receita Federal, mapeamos fontes para investigar numa fase 2:

* **Prefeituras:** Diários Oficiais (Alvarás de Construção) – *Alta complexidade de extração.*
* **Redes Sociais:** Instagram/LinkedIn (Busca por bio "Incorporadora" + Geo-localização).
* **Marketplaces:** Portais imobiliários (Raspagem de quem está anunciando lançamentos).