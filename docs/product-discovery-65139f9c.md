<!-- title: Product Discovery | url: https://outline.seazone.com.br/doc/product-discovery-lXa78utcqa | area: Tecnologia -->

# 🕵️‍♀️ Product Discovery

# Product Discovery: Melhorias no System Price - [Detalhamento](https://outline.seazone.com.br/doc/sytem-price-CQ4bJnkUB0)

**Status:** Em Andamento\n**Data Início:** 09/05/2024 (Data da primeira call formal de DoD/DoP com RM)\n**Última Atualização:** 28-0-2025\n**Responsável PM:** Lucas Abel


---

## 🎯 Objetivo do Discovery

* **Qual problema de negócio estamos tentando resolver?**
  * A baixa confiança e adoção da ferramenta "System Price" pelo time de Revenue Management (RM), o que leva a ajustes manuais frequentes, inconsistência na estratégia de precificação.
* **Qual oportunidade estamos buscando explorar?**
  * Melhorar a precisão das sugestões do "System Price" para que se torne uma ferramenta estratégica confiável para o time de RM, permitindo uma precificação mais ágil, consistente e otimizada.
* **Qual o impacto esperado no negócio e/ou para o usuário final?**
  * **Para o Negócio:** Potencial aumento de receita através de precificação mais dinâmica e competitiva, maior consistência na estratégia de preços, e otimização do uso dos dados de mercado e internos.
  * **Para o Usuário Final (Time RM):** Aumento da eficiência operacional (menos ajustes manuais), maior confiança nas sugestões da ferramenta, melhor embasamento para tomada de decisão, e redução da frustração com o sistema atual.


---

## 🧑‍🤝‍👩 Stakeholders Envolvidos

* **Quem são os principais stakeholders de negócio e usuários impactados por este problema/oportunidade?**
  * **Time de Revenue Management (RM):**  Fábio - Gerente RM, Precificadores de RM).
  * **Time de Dados:** Responsáveis pelo desenvolvimento, manutenção e processamento dos dados que alimentam o System Price.
  * **Liderança de Produto/Negócios:** Interessados nos resultados de receita, eficiência operacional e satisfação do time de RM.
* **Quais são as suas necessidades e dores relacionadas a este tema?**
  * **Time RM:**
    * Não compreendem completamente as regras de negócio do System Price.
    * Percebem que o System Price não é preciso para certas categorias (ex: Categorias Master) ou em determinadas situações de mercado.
    * Necessitam de maior transparência sobre como o preço é calculado.
    * Desejam uma ferramenta que efetivamente auxilie na definição de preços ótimos, reduzindo a necessidade de intervenção manual extensiva.


---

## 🧐 Entendimento do Problema/Oportunidade

* **Qual a descrição detalhada do problema ou oportunidade?**
  * O "System Price", um componente da ferramenta de precificação do Sirius que é o sistema de precificação usado pela Seazone para analisar precificar e enviar os preços para Stays a qual conecta com as OTAs, apesar de ser alimentado por um robusto sistema de Big Data e regras lógicas, não é plenamente utilizado pelo time de RM devido à falta de confiança em suas sugestões. Isso se manifesta na necessidade de ajustes manuais, não utilização para categorias específicas (como "Master"), e uma percepção de que as sugestões podem não refletir adequadamente a dinâmica do mercado ou a melhor estratégia de preço. A oportunidade reside em revisar e aprimorar as entradas de parâmetros, lógicas e a transparência do sistema para torná-lo um ativo valioso e confiável para o RM.
* **Quais evidências (dados, feedback de usuários, observações) temos que confirmam a existência e relevância deste problema/oportunidade?**
  * **Feedback direto do Time RM (Call de 09/05/2024):**
    * Fábio (RM) indicou não dominar as regras de negócio e solicitou mapeamento.
    * Indicação de que Categorias Master não usam o System Price por falta de dados/precisão.
    * Percepção de que o sistema funciona melhor em regiões não sazonais.
    * Crença de que a quantidade e qualidade dos concorrentes são cruciais, mas com parâmetros ainda não definidos ("número mágico", "como medir qualidade", "qual % de precisão aceitável?").
  * **Observação (implícita):** Necessidade de revisão e melhoria reconhecida pelo time de Dados, que está disposto a desenvolver melhorias.
  * **Documentação do Sistema (Análise em Andamento):** Será gerada uma documentação mais robusto indicando todas as regas de negócio do sytem price.
* **Qual o impacto quantitativo (se possível) deste problema/oportunidade?**
  * Atualmente não quantificado de forma precisa.
  * **Potencial:** Redução do tempo gasto em ajustes manuais pelo time de RM (ganho de eficiência), aumento da taxa de ocupação e/ou diária média por precificação otimizada.


---

## 🤔 Hipóteses e Suposições

* Quais são as nossas principais hipóteses sobre a causa raiz do problema ou sobre a melhor forma de aproveitar a oportunidade?
  * **Hipótese 1:** A falta de clareza e documentação acessível sobre as regras de negócio do "System Price" é um dos principais fatores para a baixa confiança do time de RM.
  * **Hipótese 2:** As regras atuais e os parâmetros utilizados no "System Price" (ex: definição de concorrentes, pesos de sazonalidade, regras de antecedência) podem não ser os mais adequados para todos os cenários de mercado ou categorias de imóveis, levando a sugestões de preço percebidas como imprecisas.
  * **Hipótese 3:** A falta de explicabilidade sobre *como* uma sugestão de preço específica foi gerada impede que o time de RM valide e confie na ferramenta.
  * **Hipótese 4:** Melhorar a precisão do System Price em regiões específicas (ex: não sazonais) e expandir gradualmente pode ser uma forma eficaz de (re)construir a confiança.
* Quais são as suposições críticas que estamos fazendo sobre o problema, usuários, tecnologia ou mercado?
  * **Suposição 1:** O time de RM possui conhecimento de mercado valioso que, se incorporado corretamente nas regras ou como feedback, pode melhorar significativamente a precisão do sistema.
  * **Suposição 2:** Os dados de concorrentes disponíveis (preços, ocupação) são suficientes e de qualidade razoável para embasar decisões de precificação, desde que bem filtrados e ponderados.
  * **Suposição 3:** É tecnicamente viável ajustar os parâmetros e lógicas existentes no backend (Lambda, queries BigQuery) sem necessidade de uma reconstrução completa da arquitetura de dados ou da interface em Sheets (que foi validada para outros fins).
  * **Suposição 4:** O time de RM está aberto a testar e adotar uma versão melhorada do System Price se as melhorias endereçarem suas principais dores e demonstrarem valor.


---

## 💡 Ideias de Solução (Brainstorming)

* Quais são as diferentes ideias que surgiram para resolver o problema/oportunidade?
  * Mapeamento completo das regras de negócio atuais.
  * Acompanhamento do processo de precificação manual do RM (Não Sazonais).
  * Definição de critérios para reparametrização do System Price (foco inicial em Não Sazonais).
  * Levantamento de uma lista de potenciais novas features/parâmetros.
  * Desenho de um plano de teste A/B (automático vs. manual) e comparação com PriceLabs para regiões Não Sazonais.
  * Definição de KPIs para monitorar a performance.


---

## 🧪 Plano de Validação

* **Métodos:** Mapeamento, Entrevistas/Observação com RM, Definição de Cenários de Teste e KPIs.
* **Atividades do PM (Discovery):**

  
  1. **Mapeamento de Regras e Comportamento:**
     * *Ação:* Concluir o mapeamento das regras de negócio do System Price. Acompanhar e mapear o comportamento de precificação de Nicole e Elisangela em regiões Não Sazonais.
     * *Valida:* H1, H2, S1.
     * *Saída (Input para Time de Dados/RM):* Documento de regras atuais; Relatório de práticas manuais do RM.
  2. **Definição de Novas Features/Parâmetros:**
     * *Ação:* Com base no mapeamento, feedback do RM e análise, definir uma lista priorizada de novas features ou parâmetros que poderiam melhorar a precisão.
     * *Valida:* H5.
     * *Saída (Input para Time de Dados):* Especificação funcional de novas features/parâmetros.
  3. **Desenho do Teste A/B e KPIs:**
     * *Ação:* Em parceria com o RM, definir a estrutura do teste A/B para regiões Não Sazonais (critérios para grupo de teste/controle). Definir os KPIs chave para medir a performance (ex: ocupação, diária média, receita, tempo de ajuste manual, satisfação do RM). Definir como a comparação com PriceLabs será feita.
     * *Valida:* H4, S5.
     * *Saída (Input para Time de Dados/RM):* Plano de teste A/B; Lista de KPIs e metas/critérios de sucesso.
  4. **Especificação para Time de Dados (Epic/DoD):**
     * *Ação:* Com base em todos os achados, criar o Epic para o time de Dados, detalhando o escopo da primeira fase de implementação/ajuste (foco em Não Sazonais), os critérios de aceite (DoD), e os inputs gerados (regras a ajustar, features a incluir, plano de teste a suportar).
     * *Saída:* Epic detalhado no Jira (ou ferramenta similar) com DoD claro.


---

## ✅ Achados e Validações

* Confirmação da necessidade de clareza nas regras (H1).
* Indicação de potencial de otimização (H2), especialmente em regiões Não Sazonais.
* Definição da estratégia de ataque inicial focada em Não Sazonais e teste A/B.
* Reconhecimento da necessidade de um backlog de novas features/parâmetros para o futuro.
* *\[Esta seção será a consolidação final de todos os aprendizados do PM ao final da sua fase de discovery, antes do handover para o time de Dados iniciar o trabalho especificado no Epic.\]*


---

## 🏗️ Definição do Escopo Inicial e Entregáveis

* **Solução Proposta (a ser implementada pelo Time de Dados com base no Discovery do PM):**
  * "System Price" com parâmetros ajustados (e/ou novas features/parâmetros iniciais implementados) para **regiões Não Sazonais**.
  * Infraestrutura para rodar teste A/B: um grupo de imóveis em Não Sazonais com precificação automática via System Price ajustado, e um grupo de controle com precificação manual.
  * Dashboard/Relatórios para monitoramento dos KPIs definidos pelo PM.
* **Escopo da Implementação da Fase 1 (Trabalho do Time de Dados):**
  * Análise e ajuste técnico dos parâmetros existentes para Não Sazonais.
  * Implementação das novas features/parâmetros priorizadas pelo PM para Não Sazonais (se houver).
  * Criação da segmentação de listings para grupo de teste/controle.
  * Garantir que os dados para KPIs estejam disponíveis.
* **Principais Entregáveis Técnicos (do Time de Dados):**

  
  1. Código do "System Price" com ajustes/novas features implementado em ambiente de produção/teste.
  2. Sistema de segmentação de listings para teste A/B funcional.
  3. Fontes de dados para KPIs prontas para consumo.
* **DoD para o Epic da Fase 1 (Implementação):**
  * \[A ser detalhado no Epic pelo PM, mas incluiria: Funcionalidades implementadas conforme especificações, testes unitários/integração passando, infraestrutura de A/B pronta, dados de KPI acessíveis, RM e PM validam que o sistema está pronto para iniciar o período de teste A/B.\]


---

## ▶️ Próximos Passos


1. **PM finaliza e entrega os artefatos do Discovery** (Mapeamentos, Especificações de Features/Parâmetros, Plano de Teste A/B, KPIs, Epic com DoD) para o Time de Dados. (Responsável: Lucas Abel)
2. **Kick-off com Time de Dados** para alinhar o Epic e o plano de trabalho da Fase 1 de implementação. (Responsáveis: PM, Tech Lead/Representante do Time de Dados)
3. **Time de Dados inicia o desenvolvimento/ajustes** conforme o Epic. (Responsável: Time de Dados)
4. **PM e RM preparam a logística para o teste A/B** (comunicação, seleção final de imóveis com apoio de dados, etc.).
5. **Após implementação pelo Time de Dados:** Iniciar o período formal de Teste A/B nas regiões Não Sazonais, monitorando KPIs e comparando com PriceLabs. (Responsáveis: PM/RM monitoram, Dados suportam).
6. **Coleta de feedback contínuo do RM** durante o teste.
7. **Ao final do período de teste:** Análise dos resultados e decisão sobre próximos passos (expandir, iterar, etc.).


---