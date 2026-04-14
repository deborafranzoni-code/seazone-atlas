<!-- title: Diagnóstico de Instabilidade nos Scrapers | url: https://outline.seazone.com.br/doc/diagnostico-de-instabilidade-nos-scrapers-GZ1xtGpWEA | area: Tecnologia -->

# Diagnóstico de Instabilidade nos Scrapers

#### **Fase 1: Imersão e Contextualização** 

*Meta:* Entender o ecossistema e o problema sem mexer em código.\n**Tarefas:**


1. **Estudo do Contexto de Negócio:**
   * Ler a documentação interna sobre:
     * Fluxo de dados (aquisição → tratamento → disponibilização).
     * Impacto dos scrapers para o time Solutions (ex: "O que acontece quando o Mesh falha?").
   * Entender os termos-chave: *Data Lake, SQS, Firehose, timeout, scraping*.
   * **Output:**
     * Resumo de 1 página: "Por que os scrapers Mesh/Details são críticos?".
     * **Glossário Compartilhado:** Documento no outline com definições simples (ex: "SQS: Fila de mensagens da AWS para organizar tarefas") + exemplos de uso no contexto.
2. **Mapeamento dos Componentes:**
   * Desenhar um diagrama simples mostrando:
     * Fontes de dados (Airbnb).
     * Fluxo: Scrapers → SQS → Firehose → Data Lake.
     * Pontos de falha conhecidos (ex: "Onde ocorrem timeouts?").
     * **Dependências Críticas:** Mapear efeitos em cascata (ex: "Falha no Mesh → Falha no Details" devido à dependência de IDs).
   * **Output:** Diagrama visual com anotações de gargalos e setas de impacto entre componentes.

#### **Fase 2: Análise de Dados e Logs**

*Meta:* Identificar padrões de falha usando dados existentes (sem criar novos processos).\n**Tarefas:**


1. **Coleta de Logs e Métricas:**
   * Acessar ferramentas de monitoramento (ex: AWS CloudWatch):
     * Extrair logs de execução dos scrapers (últimos 30 dias).
     * Filtrar por: erros de timeout, códigos HTTP 429/503, mensagens de falha.
   * **Output:** Planilha com:\n| Data/Hora | Scraper | Tipo de Erro | Duração da Execução | Bbox Afetado |
2. **Análise de Padrões:**
   * Responder perguntas-chave com base nos dados:
     * "Qual scraper tem mais falhas? (Mesh vs. Details)"
     * "Falhas ocorrem em horários específicos?"
     * "Existe correlação entre tamanho do bbox e timeouts?"
     * "Quantas requisições são feitas por minuto em média?"
     * **Nova Dimensão:** "Falhas concentram-se em imóveis com algum padrão recorrente?"
   * **Output:** 
     * Gráficos simples (ex: barras de falhas por hora, dispersão de bbox vs. duração).
     * Análise segmentada de característica padrão
3. **Análise de Custos:**
   * Verificar no AWS Cost Explorer:
     * Custo associado a reprocessamentos (ex: execuções repetidas por falha).
     * Uso de recursos (ex: Firehose, Lambda) durante picos de falha.
   * **Output:** Estimativa de impacto financeiro das instabilidades.

#### **Fase 3: Investigação de Causas** 

*Meta:* Formular hipóteses sobre causas raiz com base nas descobertas.\n**Tarefas:**


1. **Entrevistas com o Time:**
   * Conversar Hideki:
     * Perguntas-chave:
       * "O que vocês suspeitam ser a causa principal dos timeouts?"
       * "Já houve mudanças recentes no código ou na infra?"
       * "Quais são as workarounds atuais (além de aumentar timeouts)?"
   * **Output:** Resumo das hipóteses levantadas pelo time.
2. **Análise de Comportamento do Airbnb:**
   * Usar ferramentas como **Postman** ou **curl** para testar manualmente:
     * Simular requisições à API do Airbnb (com mesmos parâmetros do scraper).
     * Verificar: tempo de resposta, limites de taxa, mudanças na estrutura da resposta.
   * **Cuidado:** Não sobrecarregar a API (fazer testes pontuais).
   * **Output:** Relatório de testes manuais com:
     * Tempo médio de resposta por requisição.
     * Exemplos de erros recebidos (ex: 429 Too Many Requests).
3. **Revisão de Configurações Atuais:**
   * Verificar no console da AWS:
     * Configurações das filas SQS (timeout de visibilidade, retry policies).
     * Limites de concorrência atuais (ex: variável

       ```javascript
       CONCURENCY
       ```

        no ambiente).
     * Configurações do Firehose (buffer size, intervalo de envio).
     * **Histórico de Mudanças:** Evolução de timeout/memória em Lambda/ECS Tasks (últimos 6 meses).
   * **Output:** 
     * Lista de configurações que podem estar contribuindo para falhas.
     * Tabela com histórico de alterações (ex: "Timeout aumentado de 5s → 30s em Jan/2024").

#### **Fase 4: Síntese e Recomendações** 

*Meta:* Consolidar descobertas em um relatório claro para o time.\n**Tarefas:**


1. **Estruturação do Relatório Final:**
   * Criar um documento  com:
     * **Resumo Executivo:** Principais descobertas em 3 frases.
     * **Padrões Identificados:** Gráficos e tabelas da Fase 2.
     * **Hipóteses de Causa Raiz:** Lista priorizada (ex: "1. Timeout fixo muito baixo", "2. Limite de concorrência inadequado").
     * **Recomendações (Categorizadas):**
       * **Quick Wins (Baixo Esforço):** Ações imediatas (ex: "Ajustar timeout SQS de 30s → 60s").
       * **Correções de Médio Prazo:** Ações com desenvolvimento (ex: "Refatorar lógica de retry").
       * **Investigações Futuras:** Hipóteses não confirmadas (ex: "Verificar memory leak na biblioteca X").
2. **Apresentação para o Time:**
   * Preparar uma apresentação de 10 minutos para:
     * Mostrar os principais achados.
     * Sugerir 2-3 iniciativas prioritárias para a próxima fase.
   * **Output:** Registro da reunião com feedback do time.