<!-- title: Alerta de validação de categorização Interna - IA | url: https://outline.seazone.com.br/doc/alerta-de-validacao-de-categorizacao-interna-ia-8hqzatMe5F | area: Tecnologia -->

# Alerta de validação de categorização Interna - IA

**Projeto:** (Validação Inteligente de Estratificação

**Versão:** 1.0 

**Status:** Em Descoberta / Rascunho 

**Responsável:** PM Lucas Abel

## 1. Contexto e Visão Geral

A Seazone está em uma transição crítica para uma gestão orientada a **Data Products**. Dentro do pilar de **Pricing (Ação/Receita)**, a correta definição de Stratas (SIM, JR, SUP, TOP, MASTER) é fundamental para a precificação dinâmica.

Atualmente, a definição de strata para novos imóveis é um processo manual e propenso a erros. Revisar todo o portfólio (aprox. 3.000 imóveis e crescendo) manualmente é operacionalmente inviável. Possuímos um modelo de IA (Generativa + ML) treinado em base mista (nossos imóveis + concorrentes) que já realiza essa estratificação para o mercado externo com sucesso.

**A Oportunidade:** Reutilizar esse ativo de IA para auditar nossa base interna, detectando anomalias (imóveis mal classificados) e priorizando a ação dos Revenue Managers (RMs) baseando-se em impacto financeiro.

## 2. O Problema (The Why)


1. **Ineficiência Operacional:** É impossível revisar manualmente 3.000+ imóveis recorrentemente. A equipe hoje foca apenas em casos óbvios de performance extrema.
2. **Perda de Receita (Churn & Pricing):** Imóveis classificados em stratas inferiores à realidade (ex: imóvel TOP classificado como SIM) são precificados abaixo do mercado, gerando receita perdida. O oposto gera insatisfação e churn.
3. **Inconsistência de Dados:** Erros manuais na entrada de dados criam "ilhas" de informações incorretas que afetam a inteligência de precificação.

## 3. Objetivos de Sucesso (Goals)

* **Curto Prazo (MVP):** Reduzir o esforço humano de revisão de 100% da base para <10% (foco apenas em anomalias detectadas).
* **Médio Prazo:** Aumentar a precisão da base de stratas internas em >20% nos primeiros 3 meses de uso.
* **Longo Prazo:** Criar um "loop de feedback" onde as validações humanas alimentam o treinamento de futuros modelos.

## 4. Persona Usuária

**Nome:** Revenue Manager (RM) **Meta:** Garantir que a precificação esteja alinhada com a qualidade real do imóvel para maximizar receita e ocupação. **Dor:** "Perco tempo revisando imóveis que estão corretos e não consigo achar os que estão errados rápido."

## 5. Escopo do MVP (O Que Vamos Fazer)

### 5.1. Funcionalidades Principais


1. **Inferência em Lote (Batch):** Rodar o modelo de IA existente na base completa de fotos dos imóveis Seazone.
2. **Algoritmo de Priorização (Score de Atenção):** Cruzar a Strata Atual vs. Strata Modelo para gerar um ranking de urgência.
   * *Fórmula:* `(Distância entre Stratas) x (Confiança do Modelo)`.
   * *Exemplo:* Erro de 4 níveis com 95% de confiança tem prioridade máxima.
3. **Integração de Performance (Meta):** Trazer dados de performance para embasar a decisão do RM.
   * Fonte: Ferramenta de Meta Performance.
   * Lógica de Temporalidade:
     * Imóveis Novos: Performance Atual.
     * Imóveis Existenes: Último mês fechado ou Média dos últimos 3 meses fechados.
   * Métricas: Status de Performance (Crítico, Atenção, Berlinda, Ok, Meta_subestimada) e % de Cumprimento da Meta (Faturamento Real / Meta).
4. **Interface de Validação (Planilha Conectada):** Google Sheets conectado ao GCP (BigQuery) para ação rápida.
   * Colunas de Ação: Status (Pendente, Ajustado, Ignorado) e Comentário (Justificativa).
   * Log de Alterações: Salvar o histórico das decisões do RM para futuro.

### 5.2. Regras de Negócio

* **Disparo de Anomalia:** O sistema deve alertar sempre que a Strata do Modelo for diferente da Atual.
* **Supressão de Alertas:** Se um RM marcar um imóvel como "Ignorado" (Falso Positivo), esse ID deve sair das próximas execuções automáticas para evitar ruído.
* **Execução Recorrente:**
  * Fase 1: Run único em toda a base (Cleanup).
  * Fase 2: Run apenas para imóveis novos ou não avaliados pelo ML anteriormente.

## 6. Requisitos Funcionais Detalhados

| ID | Requisito | Descrição Detalhada | Prioridade |
|:---|:---|:---|:---|
| **RF-01** | **Extração de Features** | O modelo deve processar as fotos e extrair a Strata sugerida e a Confiança (%). | Must Have |
| **RF-02** | **Cálculo de Score** | Calcular a "distância" entre Stratas (ex: SIM=1, MASTER=5). Multiplicar pela confiança. | Must Have |
| **RF-03** | **Integração Meta Performance** | Buscar na ferramenta de Meta: Status (enum) e % Meta. Lógica: Se novo -> atual; Se velho -> último mês fechado ou média 3 meses. | Must Have |
| **RF-04** | **Tabela de Saída (BigQuery)** | Tabela consolidando: ID Imóvel, Strata Atual, Strata Modelo, Confiança, Score, Status Perf, % Meta, Status Validação (NULL por padrão), Comentário. | Must Have |
| **RF-05** | **Conector Planilha** | Planilha Google Sheets "read/write" conectada à tabela do RF-04. Permite filtragem e edição das colunas "Status Validação" e "Comentário". | Must Have |
| **RF-06** | **Histórico (Log)** | Quando o RM altera o status para "Ajustado" ou "Ignorado", registrar timestamp e user_id em uma tabela de logs auxiliar. | Should Have |

## 7. Requisitos Não-Funcionais (RNF)

**Custo:** Utilizar a infraestrutura GCP já existente; evitar custos de inferência excessivos rodando o modelo repetidamente nos mesmos imóveis.

* **Segurança:** Garantir que as planilhas estejam dentro do domínio da Seazone.

## 8. Arquitetura de Dados (Visão de Alto Nível)


1. **Input:** Base de Imóveis (Fotos + Metadados) + Base de Performance (Meta).
2. **Processamento (GCP):**
   * Job Batch/Python invoca o **Modelo de IA (Existente)**.
   * Script de cruzamento de dados (Modelo vs. Manual vs. Meta).
   * Escrita no **BigQuery** (Tabela `tb_sentinelas_strata`).
3. **Output:**
   * **Google Sheets:** Conectado via API ou conector nativo ao BigQuery.

## 9. O Que Está Fora do Escopo (Backlog Futuro)

* **Alteração Automática:** O modelo não alterará a strata na base de produção automaticamente; isso continua sendo uma ação humana validada.
* **Dashboard Visual:** A visualização será via planilha neste MVP. Dashboards (Looker/Data Studio) virão em iterações futuras se o volume de dados exigir.
* **Retreinamento do Modelo:** O feedback do RM não retreinará o modelo imediatamente; apenas gerará logs para análise posterior.

## 10. Critérios de Êxito (KPIs)


1. **Adoção:** % de alertas gerados que foram revisados/finalizados pelo RM.
2. **Precisão do Alerta:** % de alertas classificados pelo RM como "Ajustado" (erros reais encontrados) vs "Ignorado" (falsos positivos). Se o índice de "Ignorado" for muito alto, ajustamos o *threshold* de confiança.
3. **Impacto de Receita:** Variação de ADR (Average Daily Rate) dos imóveis que tiveram a strata corrigida para "cima" 30 dias após a correção.