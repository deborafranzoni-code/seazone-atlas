<!-- title: Otimização de Recursos dos Scrapers | url: https://outline.seazone.com.br/doc/otimizacao-de-recursos-dos-scrapers-ebupK3c23v | area: Tecnologia -->

# Otimização de Recursos dos Scrapers

#### **1. Visão Geral e Contexto**

Nossa operação de coleta de dados,  é vital para o negócio. Atualmente, enfrentamos o desafio de custos com infraestrutura acima do orçado e ineficiências operacionais que consomem recursos desnecessariamente. Esta iniciativa foca em otimizações de alto impacto e baixo esforço para reverter este quadro.

#### **2. Problema / Dor Principal**

A equipe técnica identificou duas dores centrais que geram custos e desperdício:


1. **Superdimensionamento de Recursos:** *Scrapers* estão configurados com mais CPU e Memória (RAM) do que o necessário para suas tarefas, resultando em um custo direto e elevado na AWS sem um benefício de performance correspondente.
2. **Ineficiência Lógica:** Sistemas de *retry* estão configurados de forma genérica, tentando reprocessar erros que são permanentes (ex: um anúncio não existe mais, acesso negado). Isso gera ciclos de processamento inúteis, consumindo CPU e aumentando o tempo de execução e o custo.

#### **3. Objetivos e Resultados-Chave (OKRs)**

**Objetivo:** Reduzir significativamente os custos operacionais e aumentar a eficiência dos nossos *scrapers* de dados.

* **KR1:** Reduzir em **20%** o custo mensal com AWS Fargate relacionado ao workload de scraping até o final do Q3.
* **KR2:** Diminuir em **50%** o volume de mensagens na Failure Queue (ou DLQ) causadas por erros permanentes conhecidos.
* **KR3:** Garantir que **90%** dos serviços de *scraping* em Fargate operem com uma utilização média de CPU/Memória dentro de uma faixa saudável (ex: 50-70%), eliminando o superdimensionamento.

#### **4. Escopo da Iniciativa**

O foco é em otimizações que possam ser aplicadas de forma ampla e com esforço contido.

**In-Scope (Foco Principal):**

* **Análise e ajuste de CPU/Memória** (*Right-Sizing*) dos serviços existentes no AWS Fargate.
* **Refinamento da lógica de *retries*** para diferenciar erros transitórios de erros permanentes.
* **Análise e tratamento das causas raiz** dos erros mais comuns na Failure Queue.

**Out-of-Scope (Fora do Escopo):**

* Reescrita completa ou refatoração arquitetônica majoritária dos *scrapers*.
* Migração para outros serviços de computação da AWS (o foco é otimizar o uso do **Fargate** atual).
* Introdução de novas tecnologias complexas (ex: orquestradores como Step Functions) nesta fase inicial.

#### **5. Requisitos e Diretrizes para a Equipe Técnica**

Como PM, a expectativa é que a equipe técnica investigue e implemente as melhores soluções para os seguintes requisitos:

**Ação 1: Revisão de Dimensionamento (*Right-Sizing*)**

* **O que deve ser feito:** Analisar o perfil de consumo de recursos de cada *scraper* para ajustar sua alocação.
* **Requisitos/Diretrizes:**
  * Utilizar as métricas do **Amazon CloudWatch** (ex: CPUUtilization, MemoryUtilization) para estabelecer uma linha de base do consumo real.
  * **Validar o uso do AWS Compute Optimizer** como ferramenta de apoio para gerar recomendações de dimensionamento para os serviços em Fargate.
  * Criar um plano de reconfiguração para aplicar os novos tamanhos, priorizando os *scrapers* de maior custo. O resultado esperado é uma redução de custo por *scraper*, como no exemplo de 500MB para 256MB.

**Ação 2: Otimização da Lógica de *Retry***

* **O que deve ser feito:** Impedir que o sistema desperdice recursos tentando reprocessar erros sem solução.
* **Requisitos/Diretrizes:**
  * Mapear e classificar os tipos de erros mais comuns (ex: HTTP 404, 403, 401 vs. timeouts de rede, HTTP 5xx).
  * Implementar uma política de **"fail-fast"**: erros permanentes devem falhar imediatamente e ser direcionados para uma Dead-Letter Queue (DLQ) para análise, sem passar por novos *retries*.
  * A lógica de *retry* com *backoff* exponencial deve ser mantida apenas para erros transitórios (que podem ser resolvidos com uma nova tentativa).

**Ação 3: Análise e Saneamento da Fila de Falhas**

* **O que deve ser feito:** Investigar a fila de falhas para encontrar e corrigir problemas recorrentes e de fácil resolução.
* **Requisitos/Diretrizes:**
  * Analisar e categorizar os erros presentes na Failure Queue (ou DLQ) para identificar os 2-3 principais ofensores.
  * Priorizar a investigação e correção desses erros de alto volume, que podem ser causados por bugs simples ou mudanças na API de origem.

#### **6. Monitoramento e Métricas de Sucesso**

O sucesso da iniciativa será medido através de:

* **Painel de Custos:** Acompanhamento dos custos de Fargate no AWS Cost Explorer, utilizando *tags* de recursos para filtrar apenas os serviços de scraping.
* **Métricas de Fila:** Monitoramento do número de mensagens visíveis na Failure Queue/DLQ via CloudWatch.
* **Métricas de Utilização:** Gráficos de utilização de CPU e Memória no CloudWatch para validar a eficiência após o *right-sizing*.