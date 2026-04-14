<!-- title: Unificação de categorização Automática | url: https://outline.seazone.com.br/doc/unificacao-de-categorizacao-automatica-fOj9YuVmdk | area: Tecnologia -->

# Unificação de categorização Automática

**Autor:** Lucas Abel - PM de Dados 

**Data:** 09-03-2026

## 1. Contexto e Motivação

Atualmente, a classificação (stratificação) dos concorrentes ocorre por duas vias:


1. **Automática:** Modelo de ML que analisa imagens e features.
2. **Manual:** Equipe de RM (Revenue Management) através de análise humana.

Ambas as fontes alimentam um banco relacional (DBaver), que é consumido pelo sistema operacional **Sirius**. No entanto, nosso **Data Lake** não possui essa informação centralizada. Hoje, quando produtos de dados (como a análise de faturamento) necessitam dessa informação, precisam buscá-la no Sirius, gerando dependência de sistemas transacionais e falta de padronização analítica.

## 2. Objetivo

Criar uma tabela centralizada na camada **Enriched** do Data Lake que consolide as stratas de todos os concorrentes (automáticas e manuais), tornando-se a "Fonte da Verdade" (Single Source of Truth) para consumo analítico e eliminando a dependência de consultas ao sistema Sirius para fins de reporte.

## 3. Escopo e Requisitos Técnicos

### 3.1. Fonte de Dados

* **Sistema Origem:** Banco de Dados Relacional (DBaver).
* **Dados de Entrada:** Tabelas contendo as stratas automáticas (modelo) e stratas manuais (RM).

### 3.2. Camada de Destino

* **Camada:** Enriched.
* **Tabela:** `enriched.competitor_strata` (nome sugerido).

### 3.3. Lógica de Negócio (Requisito Funcional)

A tabela final deve conter a visão consolidada. A regra de precedência sugerida é:


1. Manter o histórico de ambas as classificações (Automática vs Manual) em colunas separadas.
2. Criar uma coluna de **"Strata Final"**.
   * *Regra:* Se existir strata Manual, ela prevalece sobre a Automática. Se não houver Manual, utiliza-se a Automática.

### 3.4. Especificação da Tabela (Schema Sugerido)

| Coluna | Tipo | Descrição |
|:---|:---|:---|
| `competitor_id` | String/Int | Identificador único do concorrente. |
| `strata_automatica` | String | Classificação gerada pelo modelo. |
| `strata_manual` | String | Classificação inserida pelo time de RM. |
| `strata_final` | String | **Campo principal.** Prioriza Manual > Automática. |
| `data_atualizacao` | Timestamp | Data e hora da última atualização do registro. |
| `fonte_registro` | String | Indicador de qual fonte originou a atualização. |

## 4. Critérios de Aceite (Acceptance Criteria)


1. **Ingestão:** O pipeline deve ler os dados do DBaver com sucesso, garantindo a conexão segura.
2. **Histórico:** A tabela deve permitir a análise histórica (Slowly Changing Dimension - Type 2 é um plus, ou ao menos manter o snapshot diário).
3. **Validação de Dados:**
   * A soma de stratas na nova tabela do Lake deve ser igual à soma de stratas existentes no DBaver/Sirius no momento da carga inicial.
   * Não deve haver duplicidade de `competitor_id` na visão mais recente.
4. **Disponibilidade:** A tabela deve ser atualizada com frequência diária (ou conforme a atualização do modelo manual/automático).
5. **Consumo:** Após a criação, validar se a tabela pode ser lida pela ferramenta de análise de faturamento sem necessidade de joins complexos com o Sirius.

## 5. Fora do Escopo

* Alteração no modelo de classificação automática.
* Alteração na interface do sistema Sirius.
* Limpeza de dados históricos incorretos no banco relacional de origem.

## 6. Stakeholders

* **Requisitante:** PM de Dados.
* **Consumidores:** Time de Analytics (Faturamento), Time de RM.
* **Executor:** Time de Engenharia de Dados.

## 7. Riscos e Dependências

* **Conectividade:** Necessidade de garantir acesso do Lake ao banco DBaver (túnel/VPN ou credenciais).
* **Latência:** Definir se a atualização é batch (diária) ou se necessita de near real-time.


***

###