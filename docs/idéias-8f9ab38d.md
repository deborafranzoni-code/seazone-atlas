<!-- title: Idéias | url: https://outline.seazone.com.br/doc/ideias-Lj89RZ2LBa | area: Tecnologia -->

# Idéias

---

# Resumo da Ideia: Dashboard "Monitor de Pressão de Demanda"

 **Objetivo Principal:** Criar uma ferramenta visual no BI para que o time de RM possa, de forma proativa, identificar e analisar períodos futuros com alta pressão de demanda (ocupação elevada com antecedência), substituindo a necessidade de um "Alerta de Ocupação (Tipo 3)".


1. **O Coração do Dashboard: A Tabela "Monitor de Períodos de Alta Pressão"** 

   A ideia central é uma tabela dinâmica que não mostra médias em faixas amplas, mas sim "eventos de ocupação" específicos.

   
   1.  O que é um "Evento de Ocupação"? 
      * Um período de dias consecutivos para um polígono específico, onde a ocupação atinge um limiar mínimo de relevância. 
   2. Regras para Gerar as Linhas da Tabela:
      *  Polígonos Considerados: A análise se concentrará em polígonos com 10 ou mais unidades para garantir que a métrica de ocupação seja significativa e menos volátil. 
      * Limiar de Criticidade: Um período só aparecerá na tabela se a ocupação atingir pelo menos 30% em algum dia desse período. Este é o nosso gatilho para considerar um período como "relevante". 
   3. Estrutura da Tabela: 
      * Cada linha representa um único evento de ocupação.
      *  A tabela será ordenada por padrão pela "Ocupação Máx. (%)", trazendo os casos mais críticos para o topo. 
      * Colunas Principais:
      * Polígono: Onde o evento está ocorrendo. 
      * Período Alvo: O intervalo de datas do evento (ex: "2025-09-07" ou "2025-10-12 a 2025-10-14"). 
      * Antecedência (dias): Quantos dias faltam para o início do evento.
      *  Ocupação Máx. (%): O pico de ocupação atingido dentro daquele período. (Métrica principal para ordenação). 
      * Capacidade Total: O número de unidades no polígono, para dar contexto.

 ![](/api/attachments.redirect?id=ff90a88d-894a-4f67-be33-274e686a2236 " =1076x218")


2. **Funcionalidades de Análise e Exploração (Componentes de Suporte no Dashboard)**

    A tabela principal direciona a atenção. Os seguintes componentes permitem a investigação detalhada:

   
   1. Filtros Interativos: 
      * Polígono(s): Para focar em áreas específicas. 
      * Faixa de Antecedência: Para analisar eventos que ocorrerão em um futuro próximo (ex: 30-60 dias) ou mais distante (ex: 91-120 dias). 
      * Período Alvo (Calendário): Para investigar datas específicas, como feriados ou eventos conhecidos. 
   2. Gráfico de Ocupação Diária: 
      * Um gráfico de colunas ou linhas que mostra a curva de ocupação diária. 


      * **Interatividade**: Ao clicar em uma linha (um "evento") na tabela principal, este gráfico se atualiza para dar um "zoom" naquele polígono e período, mostrando visualmente a evolução da ocupação dia a dia. 

        \
        **Por que esta abordagem é poderosa:** 
        * **Precisa**: Identifica picos de ocupação em períodos curtos (como fins de semana), que seriam perdidos em médias de faixas longas. 
        * **Acionável**: Direciona o time de RM exatamente para os polígonos e datas que mais precisam de atenção. 
        * **Capacitadora**: Transforma o RM de um receptor passivo de alertas para um analista proativo, permitindo que eles explorem os dados e validem suas próprias hipóteses. 
        * **Contextual**: Apresenta a ocupação junto com a antecedência e a capacidade total, fornecendo o contexto necessário para uma tomada de decisão informada. 

          \

Em resumo, a proposta é criar um dashboard inteligente e interativo que serve como um supervisor, destacando automaticamente os períodos de maior oportunidade ou risco, e fornecendo as ferramentas para uma análise mais profunda.