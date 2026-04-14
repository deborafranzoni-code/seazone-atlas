<!-- title: Documentação Técnica | url: https://outline.seazone.com.br/doc/documentacao-tecnica-9IwWDHk4Ut | area: Tecnologia -->

# Documentação Técnica

# Visão Geral 

**Problema:** O monitoramento da saúde do Lake estava distribuído, com dependência de alertas pontuais e um painel no Power BI, dificultando a visualização integrada do estado dos pipelines.

**Objetivo:** Criar um BI centralizado de observabilidade no Looker, com dados consolidados no BigQuery, permitindo monitorar: execução dos scrapers, volumetria dos dados, qualidade dos dados, anomalias de métricas. 

**Solução:** Migração do BI para a GCP, centralizando as métricas no dataset `lake_observability`, com visualizações no Looker Studio organizadas por criticidade e profundidade analítica.

# Fontes de Dados

O dashboard foi construído utilizando o dataset **lake_observability** no BigQuery. 

As principais tabelas integradas são:

| Tabela |
|----|
| scrapers_health |
| revenue_mape_report_last_days |
| revenue_mape_monthly_last_years |
| revenue_mape_monthly_big_errors |
| priceav_mape_report |
| anomaly_mape_report |
| anomaly_price_metrics |

# View de Suporte no BigQuery

Para padronizar regras de cálculo, reduzir lógica duplicada no Looker e garantir consistência visual entre os gráficos e KPIs, foi criada uma view auxiliar **no BigQuery**, utilizada como base para tabela de *"Variação Percentual de Linhas Inseridas (Ontem vs Última Ingestão de Sucesso)"* do dashboard.

A view concentra regras de negócio relacionadas a **volumetria**, **variação entre dias** e **detecção de quedas/aumentos relevantes**, evitando que essas regras fiquem espalhadas em múltiplos campos calculados no Looker. 

## View de Volumetria (Ontem vs Última Ingestão de Sucesso)

### **Objetivo da View**

Essa view tem como objetivo:

* Consolidar, por tabela, o número de linhas inseridas ontem e na última ingestão de sucesso;
* Calcular a variação percentual e a variação absoluta entre ontem e a última ingestão de sucesso;
* Servir como base para:
  * KPIs de volumetria;
  * Tabela de variações críticas;
  * Regras de alerta visual no Looker (ex.: quedas/aumentos relevantes).

### **Fonte de Dados**

* **Tabela base:** `lake_observability.scrapers_health`
* **Granularidade:** diária
* **Fuso horário:** America/Sao_Paulo

### **Lógica Aplicada**

A view `vw_scrapers_health_data` consolida informações de ingestão de dados por **base de dados** e **tabela**, comparando o volume inserido no dia de referência ("ontem", na prática) com o volume da **última ingestão de sucesso** registrada anteriormente.

A lógica é composta pelas seguintes etapas:

####  **1. Definição do dia de referência ("Ontem")**

* O dia de referência é tratado como `CURRENT_DATE('America/Sao_Paulo')`.
* Apesar de utilizar `CURRENT_DATE`, esse valor representa **os dados do dia anterior na prática**, pois o processo `insert_report` executa no dia atual com dados referentes ao dia anterior.
* Para cada `(database, table)`, são somadas as linhas inseridas (`rows_inserted`) apenas para registros com `date = CURRENT_DATE`. 


---

#### 2. **Identificação de erro no dia de referência**

* Para o mesmo dia de referência (`CURRENT_DATE`), é avaliada a coluna booleana `error`.
* Caso exista qualquer registro com `error = TRUE` naquele dia para uma determinada tabela, a coluna `error` da view será marcada como `TRUE`.
* Caso contrário (ou na ausência de registros no dia), o valor será `FALSE`.


---

#### 3. **Última ingestão de sucesso**

* A "última ingestão de sucesso" é definida como a execução mais recente com `error = FALSE` **anterior ao dia de referência** (`date < CURRENT_DATE`).
* Para cada `(database, table)`, é selecionada:
  * a data da última ingestão de sucesso (`last_success_date`);
  * a quantidade de linhas inseridas nessa execução (`rows_inserted_last_success`).
* Não é exigido que `rows_inserted > 0` como critério adicional de sucesso.


---

#### 4. **Universo de tabelas**

* A view constrói um universo completo de `(database, table)` a partir da tabela de origem.
* Isso garante que todas as tabelas apareçam no resultado final, mesmo quando não há registros no dia de referência ou não existe ingestão de sucesso anterior.


---

#### 5. **Cálculo das métricas**

Para cada tabela, são calculadas:

* **Quantidade de linhas ontem**\nVolume total de linhas inseridas no dia de referência (`CURRENT_DATE`).
  * O volume de linhas "ontem" é calculado por soma (`SUM(rows_inserted)`) para o dia de referência. Embora atualmente exista no máximo uma execução por dia por tabela, essa abordagem garante compatibilidade caso a granularidade de execução mude no futuro.
* **Quantidade de linhas da última ingestão de sucesso**\nVolume de linhas inseridas na última execução bem-sucedida anterior ao dia de referência.
  * Caso uma tabela **atualize mais de uma vez no dia**, o campo **"Ontem"** representa a **soma das execuções do dia**, enquanto **"Última ingestão de sucesso"** representa apenas a **última execução bem-sucedida**. Dependendo da granularidade do log (se ele registra múltiplas execuções no mesmo dia), pode haver diferença entre o "total do dia" e a "última execução". Se a expectativa for comparar **"Ontem" vs "Último dia com sucesso"** (ambos agregados por dia), terá que adaptar a view para essa granularidade.
* **Variação absoluta**\nDiferença direta entre o volume de ontem e o volume da última ingestão de sucesso.
* **Variação percentual**\nCalculada conforme as regras abaixo:
  * Se `última ingestão = 0` e `ontem = 0` → variação = `0%`;
  * Se `última ingestão = 0` e `ontem > 0` → variação = `NULL` (percentual indefinido);
  * Caso contrário, a variação percentual é calculada como a diferença entre o volume de ontem e o volume da última ingestão de sucesso, dividida pelo volume da última ingestão de sucesso, multiplicada por 100. → é feito o cálculo: ((ontem − última ingestão de sucesso) / última ingestão de sucesso) × 100

### **Exibição no dashboard**

* A view **não aplica filtros de relevância**: todas as tabelas são retornadas, independentemente de terem ou não variação.
* Qualquer filtragem (por exemplo, ocultar variações iguais a zero) é feita diretamente no BI.
* A coluna **Variação % já está em percentual** (ex.: `0,36` representa `0,36%`) e deve ser tratada como número no Looker. Não deve ser formatada como percentual no Looker para evitar duplicação de escala.
* A lógica atual assume, por padrão, uma execução diária por tabela, mas foi construída de forma defensiva para suportar mudanças futuras de granularidade.
* A coluna `error` tem como objetivo sinalizar falhas de ingestão no dia de referência e é utilizada principalmente para regras de alerta visual no dashboard.

### Definição da View (SQL)

```javascript
CREATE OR REPLACE VIEW `data-resources-448418.lake_observability.vw_scrapers_health_data` AS
WITH 
-- 1) "Ontem" (na prática: dados que entram em CURRENT_DATE por causa do insert_report,
-- que possui a lógica de no dia atual pegar dados do dia anterior)
yesterday AS (
  SELECT
    database,
    `table` AS table_name,
    SUM(
      CASE
        WHEN date = CURRENT_DATE('America/Sao_Paulo') THEN rows_inserted
        ELSE 0
      END
    ) AS rows_inserted_yesterday,
    -- coluna erro no dia de referência (current_date)
    -- (se existir mais de um registro no dia por algum motivo, marca como true se qualquer um tiver erro)
    LOGICAL_OR(
      CASE
        WHEN date = CURRENT_DATE('America/Sao_Paulo') THEN error
        ELSE FALSE
      END
    ) AS error
  FROM `data-resources-448418.lake_observability.scrapers_health`
  GROUP BY database, table_name
),

-- 2) Última ingestão de sucesso mais recente ANTERIOR a current_date
last_success AS (
  SELECT
    database,
    `table` AS table_name,
    date AS last_success_date,
    rows_inserted AS rows_inserted_last_success
  FROM (
    SELECT
      database,
      `table`,
      date,
      rows_inserted,
      ROW_NUMBER() OVER (
        PARTITION BY database, `table`
        ORDER BY date DESC
      ) AS rn
    FROM `data-resources-448418.lake_observability.scrapers_health`
    WHERE error = false
      AND date < CURRENT_DATE('America/Sao_Paulo')
  )
  WHERE rn = 1
),

-- 3) Universo de chaves (garante aparecer mesmo que um lado seja nulo)
keys AS (
  SELECT DISTINCT database, `table` AS table_name
  FROM `data-resources-448418.lake_observability.scrapers_health`
)

SELECT
  k.database AS database,
  k.table_name AS table_name,

  -- coluna error (de "ontem" na prática / current_date na tabela)
  COALESCE(y.error, FALSE) AS error,

  -- Quantidades 
  COALESCE(y.rows_inserted_yesterday, 0) AS qtd_linhas_ontem,
  COALESCE(s.rows_inserted_last_success, 0) AS qtd_linhas_ultima_ingestao_sucesso,
  s.last_success_date AS data_ultima_ingestao_sucesso,

  -- Variação absoluta
  COALESCE(y.rows_inserted_yesterday, 0) - COALESCE(s.rows_inserted_last_success, 0) AS variacao_absoluta,

  -- Variação percentual
  -- Regra:
  -- - se last_success = 0 e ontem = 0 => 0%
  -- - se last_success = 0 e ontem > 0 => NULL 
  -- - caso contrário => delta / last_success * 100
  CASE
    WHEN COALESCE(s.rows_inserted_last_success, 0) = 0
         AND COALESCE(y.rows_inserted_yesterday, 0) = 0
      THEN 0.0
    WHEN COALESCE(s.rows_inserted_last_success, 0) = 0
         AND COALESCE(y.rows_inserted_yesterday, 0) <> 0
      THEN NULL
    ELSE
      SAFE_DIVIDE(
        CAST(COALESCE(y.rows_inserted_yesterday, 0) - COALESCE(s.rows_inserted_last_success, 0) AS FLOAT64),
        CAST(COALESCE(s.rows_inserted_last_success, 0) AS FLOAT64)
      ) * 100
  END AS variacao_pct

FROM keys k
LEFT JOIN yesterday y
  ON y.database = k.database
 AND y.table_name = k.table_name
LEFT JOIN last_success s
  ON s.database = k.database
 AND s.table_name = k.table_name
;
```

### **Por que essa lógica foi implementada no BigQuery (e não no Looker)**

* Evita duplicação de lógica em múltiplos gráficos;
* Garante que todos os KPIs e tabelas usem exatamente a mesma regra;
* Melhora performance do Looker, reduzindo cálculos em tempo de visualização;
* Facilita manutenção e auditoria das regras de volumetria.

### **Uso no Dashboard**

Essa view é utilizada principalmente em:

* **Tabela de Volumetria Crítica (Ontem vs Última Ingestão de Sucesso)**
* **KPIs de variação de linhas inseridas**
* **Regras de formatação condicional** (ex.: quedas percentuais acima de um limiar configurado no Looker)

# Estrutura do Dashboard

O dashboard foi organizado em três páginas principais, seguindo um fluxo de aprofundamento progressivo:


1. Visão Geral (Torre de Controle): Monitoramento diário de execução e volumetria.
2. Receita (MAPE): Avaliação da qualidade das métricas de receita ao longo do tempo.
3. Diagnóstico e Logs: Visualização de dados de modo detalhado.

Essa organização permite:

* rápida identificação de problemas,
* análise progressiva da causa raiz,
* priorização de ações corretivas.

  \

Link do Dashboard: <https://lookerstudio.google.com/u/0/reporting/9af9c18c-0790-4068-84d9-b93b52db580b/page/p_rh740aejzd>