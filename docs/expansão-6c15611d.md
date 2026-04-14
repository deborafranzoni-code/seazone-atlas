<!-- title: Expansão | url: https://outline.seazone.com.br/doc/expansao-DLK0JrxRWS | area: Tecnologia -->

# Expansão

**Data:** Janeiro/2026 **Responsável Técnico:** Patrick de Sousa **Status:** ✅ Concluído / Em Produção **Ambiente:** Google Cloud Platform (GCP)

## 1. Visão Geral e Objetivos

O objetivo primário deste projeto foi expandir o modelo de categorização de imóveis (AI Classification) para novas regiões litorâneas, visando identificar padrões de precificação e qualidade (strata) equivalentes aos observados na região de controle (Florianópolis).

Além da expansão geográfica, houve um esforço concentrado de **Refatoração de Pipeline** e **Otimização de Custos de Nuvem**, migrando cargas de trabalho para Jobs do Cloud Run com paralelismo otimizado.

### KPIs de Sucesso

* **Paridade de Performance:** A assertividade do modelo na nova região deve ser estatisticamente equivalente à de Florianópolis.
* **Automação:** Eliminação de intervenções manuais para upload de resultados.

## 2. Arquitetura da Solução

A infraestrutura foi consolidada utilizando serviços *serverless* da GCP para garantir escalabilidade sob demanda sem custos de ociosidade.

* **Computação:** Google Cloud Run Jobs (Containerized Python Workers).
* **Armazenamento:** Google Cloud Storage (Bucket: `categorizacao_pipeline`).
* **Orquestração de Imagens:** Pub/Sub para filas de processamento de imagens (`images-input`).
* **Monitoramento:** Logs via Cloud Logging e Alertas via Cloud Functions (`receive_alert`).
* **Containers:** Artifact Registry.

## 3. Validação de Resultados (Quality Assurance)

Foi realizada uma análise comparativa rigorosa entre os resultados da nova expansão e o baseline histórico.

| Métrica | Florianópolis (Baseline) | Nova Região (Expansão) | Status |
|----|----|----|----|
| **Acurácia (Accuracy)** | \~71.0% | **\~70.8%** | ✅ Equivalente |
| **Volume Processado** | N/A | 411 Listings | ✅ Completo |


**Conclusão da Análise:** Os outputs gerados demonstraram alta aderência à realidade. A porcentagem de acerto na nova região foi estatisticamente equivalente à de Florianópolis. Devido a essa paridade, **o modelo foi aprovado sem necessidade de retreino específico**, validando a capacidade de generalização da IA para novas geografias costeiras.

## 4. Entregáveis e Repositórios

A atualização envolveu o build e push de novas imagens Docker para o **Artifact Registry** da GCP, garantindo que todas as correções (paths, logs, indentação) estejam versionadas.

### Imagens e Jobs Atualizados

| Componente | Repositório (Artifact Registry) | Cloud Run Job ID | Função |
|----|----|----|----|
| **Scraper** | `airbnb-image-scraper-repo` | `airbnb-image-job-prd` | Coleta massiva de imagens e dados brutos. |
| **Pipeline AI** | `classifier-pipeline-repo` | `image-score-classifier-job` | Processamento de features e classificação (XGBoost). |
| **LLM Proc.** | `gemini-pipeline-repo` | `gemini-image-score-job` | Análise visual avançada via Gemini (se aplicável). |

## 7. Procedimentos de Recuperação (Disaster Recovery)

Para evitar perda de dados em caso de falha no salvamento automático, foi implementado um **mecanismo de backup de emergência** no código:


1. O script verifica se a pasta `results/` foi gerada.
2. Caso negativo, ele verifica se o DataFrame `df_final` está na memória.
3. Se existir, ele força o upload de um arquivo `backup_df_final.csv` para o bucket `categorizacao_pipeline/results/expansion/`.

**Localização dos Arquivos Finais:**

* **Bucket:** `gs://categorizacao_pipeline/`
* **Caminho:** `results/expansion/`
* **Arquivos Chave:** `predictions.csv`, `metrics.json`.


## 8. Novas Regiões

| Penha, SC |
|----|
| Cabo Frio, RJ |
| Ubatuba, SP |
| Guarapari, ES |
| Itajaí, SC |
| Barra Velha, SC |
| João Pessoa, PB |
| Recife, PE |
| Garopaba, SC |
| Passo de Camaragibe, AL |
| Porto de Pedras, AL |
| São Miguel dos Milagres, AL |
| Santa Cruz Cabrália, BA |
| São Pedro da Aldeia, RJ |
| Armação dos Búzios, RJ |
| Cabedelo, PB |


\