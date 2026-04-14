<!-- title: Precificação Reativa | url: https://outline.seazone.com.br/doc/precificacao-reativa-9sCXMz8OVb | area: Tecnologia -->

# Precificação Reativa

# Documentação: Mecanismo de Precificação Reativa 

## 📌 Visão Geral

Este serviço automatiza o ajuste de preços de listagens com base no atingimento de metas e condições de mercado. Ele consome dados do **BigQuery**, processa regras de negócio em **Python/Pandas** e exporta os resultados de volta para o **BigQuery** e para o **Google Cloud Storage (GCS)** em formato Parquet.


\
<https://console.cloud.google.com/run/detail/us-central1/calculate-reactive-price/observability/metrics?hl=en&inv=1&invt=Abx5nw&project=data-resources-448418>


Planilha destinada à inserção de categorias para a precificação reativa:

<https://docs.google.com/spreadsheets/d/1xqChADuBiBwT2nf2Ou1kiG2ISisZ3s4EbtoqTjQkb0c/edit?gid=0#gid=0>


\

---

## 🛠️ Configurações e Variáveis de Ambiente

O comportamento do algoritmo é controlado por variáveis de ambiente (OS), permitindo ajustes sem alteração de código:

| **Variável** | **Descrição** | **Padrão** |
|----|----|----|
| `FATOR_AGRESSIVIDADE_GAP` | Multiplicador aplicado sobre o gap da meta. | `0.20` |
| `MAX_DESCONTO_CAP` | Limite máximo de desconto permitido (25%). | `0.25` |
| `MAX_MARKUP_CAP` | Limite máximo de aumento permitido (30%). | `0.30` |
| `MIN_DISPONIBILIDADE_PCT` | Percentual mínimo de disponibilidade aceitável. | `0.20` |
| `BUCKET_NAME` | Nome do bucket GCS para histórico. | `system-price` |


---

## 🏗️ Estrutura do Código

### 1. Coleta de Dados (`get_performance_data` & `get_price_data`)

Realiza consultas SQL no BigQuery para obter:

* **Performance:** Status da meta (`group_critic`), faturamento acumulado e dias ocupados.
* **Preços:** Preço atual do sistema, antecedência da reserva, feriados e preços da concorrência (P10 e Mediana).

### 2. Motor de Cálculo (`calcular_ajuste_dinamico`)

Esta é a função core que decide o novo preço. A lógica segue o fluxo:

* **Cálculo de Gap:** `1.0 - (Faturamento / Meta)`.
* **Fator Urgência:** Aumenta a agressividade se a data estiver próxima (menos de 7 ou 15 dias).
* **Fator Mercado:** Ajusta com base no `market_takeup_ratio` e na existência de feriados.
* **Lógica de Status:**
  * **Meta Subestimada:** Aplica **Markup** (Aumento).
  * **Crítico/Atenção:** Aplica **Desconto**, respeitando o "Piso" (P10 de mercado) para não desvalorizar o ativo.

### 3. Persistência (`save_dual_write_gcs`)

Implementa o conceito de **Dual Write**:


1. **BigQuery:** Sobrescreve a tabela `system_price.reactive_price_by_id_seazone` (Snapshot atual).
2. **GCS:** Salva um arquivo Parquet particionado por data e timestamp para auditoria histórica.


---

## 📑 Fluxo de Execução (Endpoint HTTP)

A função é disparada via trigger HTTP (`run_pricing`):


1. **Merge:** Une os dados de preço e performance usando o `id_seazone`.
2. **Processamento:** Aplica a função de ajuste linha a linha (vectorized-like via `.apply`).
3. **Exportação:** Filtra as colunas necessárias e dispara o salvamento.
4. **Resposta:** Retorna um JSON com o status da operação e o caminho do arquivo gerado.


---

## 🔗 Dependências Externas

* **Google Sheets API:** Utilizada (via `gspread`) para ler categorias de uma planilha externa (configurável via `SPREADSHEET_ID`).
* **Service Account:** Requer permissões de `BigQuery Data Editor`, `Storage Object Admin` e `Secret Manager Access`.



---


## 🧮 Simulação do Fluxo de Cálculo

🔴 Cenário A: Unidade em Alerta (Desconto)

Faturamento abaixo da meta com data de reserva próxima.


**Dados de Entrada:**

* **Preço Base (*system_price*):** R$ 500,00
* **Status BI:** Crítico (Multiplicador: 1.4)
* **Atingimento da Meta:** 70% (Gap de 0.3)
* **Antecedência:** 5 dias (Fator Urgência: 1.5)
* **Piso de Mercado (P10):** R$ 380,00

 ![](/api/attachments.redirect?id=539424b2-ae2f-40aa-849f-d7275256fd18 " =722x230")

### 🟢 Cenário B: Meta Subestimada (Aumento/Markup)

*Unidade com meta atingida e demanda alta, permitindo expansão de margem.*

* **Dados de Entrada:**
  * **Preço Base (*system_price*):** R$ 1.000,00
  * **Status BI:** Meta Subestimada (Multiplicador: 1.2)
  * **Atingimento da Meta:** 120% (Surplus de 0.2)
  * **Antecedência:** 30 dias (Fator Urgência: 1.0)

 ![](/api/attachments.redirect?id=33fb4eb4-ee18-4d35-8ed7-c0d3a8f834a1 " =759x228")