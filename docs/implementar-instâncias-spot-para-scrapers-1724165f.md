<!-- title: Implementar Instâncias Spot para Scrapers | url: https://outline.seazone.com.br/doc/implementar-instancias-spot-para-scrapers-4bBMtA3OEe | area: Tecnologia -->

# Implementar Instâncias Spot para Scrapers

#### **1. Contexto Estratégico**

* **Objetivo de Negócio Principal:** Otimização de Custos e Performance Operacional.
* **Problema/Oportunidade:** Nossos custos com instâncias EC2 On-Demand são uma despesa operacional significativa. Existe uma oportunidade comprovada de reduzir drasticamente esses custos (potencial de 70-90%) através do uso de Instâncias Spot da AWS.
* **Visão de Sucesso:** Teremos uma arquitetura de scraping resiliente, operando majoritariamente em Instâncias Spot. A operação será significativamente mais barata (redução de custos de computação > 40%), e o sistema será tolerante a falhas, garantindo que a interrupção de uma instância não resulte em perda de dados.

#### **2. Diretrizes Técnicas Essenciais**

A equipe técnica tem a autonomia para desenhar a melhor solução. No entanto, qualquer implementação deve aderir aos seguintes princípios e atender a estes requisitos, que são baseados nas melhores práticas da indústria para este tipo de arquitetura:

* **Resiliência a Interrupções:** A solução **deve** ser capaz de sobreviver ao término inesperado de instâncias. Isso implica na necessidade de um mecanismo para detectar o aviso de interrupção (o sinal de 2 minutos da AWS) e executar uma rotina de finalização segura (*graceful shutdown*).
* **Tolerância a Falhas e Idempotência:** O processo **deve** garantir que a interrupção de um scraper não cause perda de dados. As tarefas devem ser reiniciáveis e idempotentes, ou seja, se um trabalho for executado mais de uma vez, não deve gerar duplicidade ou corromper o resultado final. Um mecanismo de **checkpointing** (salvar o progresso periodicamente) é fundamental para isso.
* **Desacoplamento e Escalabilidade:** A arquitetura **deve** ser desacoplada, utilizando um sistema de filas para gerenciar as tarefas de scraping. Isso permite que os "workers" (scrapers) sejam stateless e possam ser adicionados ou removidos dinamicamente sem impactar o sistema como um todo.
* **Alta Disponibilidade de Recursos:** Para mitigar o risco de não haver capacidade Spot, a solução **deve** ser flexível, permitindo o uso de múltiplos tipos de instância (*Mixed Instances*). A estratégia de alocação deve priorizar os "pools" de instâncias com maior disponibilidade e menor risco de interrupção (*Capacity-Optimized*), em vez de focar apenas no menor preço.

#### **3. Plano de Ação Proposto (Implementação em Fases)**

A adoção será gradual para mitigar riscos e permitir o aprendizado.

**Fase 1: Prova de Conceito (PoC)**

* **Objetivo:** Validar tecnicamente em um ambiente controlado se conseguimos construir um scraper que atenda a todos os requisitos listados acima.
* **Escopo:** Selecionar um scraper de baixa criticidade. Desenvolver e testar uma primeira versão da arquitetura resiliente.
* **Entregável:** Uma **demonstração funcional**, um **Desenho da Arquitetura de Referência** proposto e um **relatório de aprendizados** da PoC.

**Fase 2: Rollout Controlado**

* **Objetivo:** Expandir a solução validada para um grupo maior de scrapers secundários.
* **Escopo:** Refinar a implementação, otimizar a infraestrutura (IaC), os alertas e o monitoramento com base nos aprendizados da PoC.

**Fase 3: Adoção Completa**

* **Objetivo:** Migrar os scrapers mais críticos e de maior custo (como o PriceAV) para a nova arquitetura.
* **Escopo:** Aplicar a solução agora estável e monitorada para os principais processos de scraping.

#### **4. Critérios de Sucesso e Métricas de Acompanhamento**

* **Métrica de Custo (Sucesso):** A projeção de custos mensais no AWS/Billing para a computação dos scrapers migrados deve apresentar uma **redução > 40%** em comparação com a linha de base On-Demand.
* **Métrica Operacional (Estabilidade):** O sistema deve manter sua capacidade de processamento mesmo sob eventos de interrupção, validado pela **taxa de conclusão de tarefas** e pela **estabilidade do número de workers em serviço**.
* **Métrica de Qualidade (Segurança):** Os KPIs de qualidade de dados existentes (% de Diárias Não Scrappadas e MAPE Mudança de Preço) **não devem apresentar degradação** após a migração, provando que a integridade dos dados foi mantida.