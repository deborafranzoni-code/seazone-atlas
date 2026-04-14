<!-- title: Integrar o MAPE de Erros de Preços no Processo de Melhorias | url: https://outline.seazone.com.br/doc/integrar-o-mape-de-erros-de-precos-no-processo-de-melhorias-5zx0iQcYnc | area: Tecnologia -->

# Integrar o MAPE de Erros de Preços no Processo de Melhorias

**Objetivo:** Este documento estabelece um framework para interpretar, diagnosticar e agir sobre os alertas de anomalia de preços. O objetivo é transformar dados brutos em inteligência acionável, criando um processo padronizado para a melhoria contínua da qualidade dos dados de scraping.


---

### **Parte 1: O Framework de Análise de Alertas**

Para cada alerta de dados, será implementado um processo de análise padronizado, baseado nos quatro pilares a seguir. O desenvolvimento técnico deverá contemplar a criação de ferramentas e documentação para suportar cada um destes pilares.


1. **Interpretação das Métricas:** Para cada alerta, serão definidas as métricas-chave que melhor descrevem a saúde do sistema. A documentação explicará o que cada métrica representa em termos de negócio e impacto técnico.
2. **Definição de Criticidade:** Durante o desenvolvimento, uma matriz de criticidade deve ser estabelecida. Esta matriz definirá os limites (thresholds) que classificam um alerta em níveis de severidade (ex: "Normal", "Atenção", "Crítico"). Regras claras serão criadas para determinar quando um alerta deve gerar uma ação automática, como a criação de um ticket no Jira.
3. **Playbook de Diagnóstico:** Para cada alerta, um guia de investigação passo a passo (playbook) será criado. Este guia orientará o analista sobre como investigar a causa raiz do problema, formulando hipóteses com base nos dados do alerta.
4. **Plano de Ação e Mitigação:** O playbook de diagnóstico levará a um conjunto de ações sugeridas. Estas ações serão divididas em **corretivas** (para resolver o problema imediato) e **preventivas/de mitigação** (para reduzir a probabilidade de recorrência).\n\n

### Parte 2: Aplicação do Framework aos Alertas de Preço 

A seguir, detalha-se como o framework será aplicado aos alertas de preço existentes. 

Este alerta monitora a cobertura de preços que deveríamos ter, mas que não foram capturados.


1. **Métricas Chave e sua Interpretação:** 
   * **% de Diárias Não Scrappadas:** Indica a magnitude total do problema, representando o percentual de cobertura de preço que estamos perdendo. 
   * **% de IDs Afetados:** Mede a amplitude do problema, mostrando se a falha está concentrada em poucos imóveis ou espalhada por todo o universo de scraping. 
   * **Percentis de Distribuição (P50, P90):** Revelam a profundidade do problema por imóvel. O P50 mostra o impacto no imóvel mediano, enquanto o P90 indica a gravidade nos casos mais extremos, ajudando a identificar anúncios "mortos" ou com falhas críticas.
2. **Definição de Criticidade:** 
   * A equipe de desenvolvimento deverá analisar dados históricos para definir os thresholds para cada uma das métricas acima. A regra para acionamento (criação de ticket) será baseada na combinação da severidade dessas métricas (ex: uma métrica em nível "Crítico" ou múltiplas em "Atenção").
3. **Playbook de Diagnóstico:** 
   * A investigação deverá começar diferenciando se o problema é amplo (% de IDs alto, P90 baixo) ou profundo (% de IDs baixo, P90 alto), pois cada cenário sugere causas diferentes (ex: mudança geral na API vs. bug em um tipo de anúncio). 
   * O playbook incluirá passos como: Análise de uma amostra de IDs dos casos mais graves (P90) para identificar padrões. 
   * Verificação da documentação e regras de negócio do próprio alerta para garantir que não haja divergências com a implementação do scraper (ex: janelas de tempo diferentes). 
   * Análise de logs dos scrapers em busca de erros recorrentes associados aos IDs problemáticos.
4. **Plano de Ação (Ações Corretivas e de Mitigação):** 
   * Com base na causa raiz, um plano de ação será executado. A tabela abaixo serve como um guia de possíveis soluções a serem implementadas.

| **Causa Raiz Identificada** | **Ação Corretiva Imediata** | **Ação de Mitigação (Prevenção)** |
|----|----|----|
| **Imóveis "mortos" na lista** | Remover manualmente os IDs inválidos. | Criar um job periódico que valida e limpa a lista de IDs. |
| **Nova regra de bloqueio do site** | Ajustar a lógica do scraper. | Melhorar a telemetria para detectar novos padrões de bloqueio. |
| **Divergência regra do alerta vs. scraper** | Ajustar o código do alerta ou do scraper. | Criar testes de integração para garantir a consistência das premissas. |
| **Bug específico no scraper** | Corrigir o código e fazer o deploy. | Aumentar a cobertura de testes unitários e de integração. |


### **Parte 3: Gestão do Conhecimento e Melhoria Contínua**

\nPara garantir que o aprendizado de cada incidente seja retido e que a resolução de problemas futuros seja acelerada, será mantido um **Log de Incidentes de Dados**. Este repositório de conhecimento criará a memória institucional necessária para a melhoria contínua. É possível usarmos a planilha já usada de [Falhas/erros](https://docs.google.com/spreadsheets/d/1O6nIL0xMQHgti6jdIj06M-nH_NUr_9caCHV3al09Lcs/edit?gid=0#gid=0)