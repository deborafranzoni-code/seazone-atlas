<!-- title: Discovery System Price - Apresentação Interna ( 02-06-2025 ) | url: https://outline.seazone.com.br/doc/discovery-system-price-apresentacao-interna-02-06-2025-2ytOTaqtcN | area: Tecnologia -->

# Discovery System Price - Apresentação Interna ( 02-06-2025 )

**Principais Insights da Reunião Interna:**


1. **A Necessidade de Contextualizar o System Price (Feedback Inicial):**
   * Ficou claro que, mesmo para a equipe técnica, uma breve explicação sobre "o que é e qual o objetivo do System Price" é um ponto de partida necessário para alinhar a todos. Isso validou a necessidade de incluir essa explicação nas apresentações.
2. **Confirmação do Problema Central:**
   * **Desuso e Desatualização:** Confirmaram sua percepção: os parâmetros da RegrasAGC estão fixos há muito tempo, sem uma rotina de revisão, e a falta de documentação/clareza dificulta a adoção pelo RM.
   * **Uso como Referência Distante:** O RM usa a AGC como um todo, mas o System Price é apenas uma coluna de referência distante, não um guia principal. A percepção é que "se tirasse a coluna hoje, não mudaria muito a vida deles".
3. **Redirecionamento Estratégico da "Fase 1" (Insight mais importante do Arilo):**
   * **O Problema não é (ainda) a falta de features:** A audiência técnica (especialmente Arilo) argumentou fortemente que adicionar novas features (FH, FP, etc.) agora seria prematuro. O passo fundamental que falta é uma **análise de dados profunda para provar o valor (ou o potencial) do sistema *atual*, mesmo que precise de reparametrização.**
   * **O "Pulo do Gato" é a Automatização da Parametrização:** A verdadeira dificuldade e onde se pode agregar valor é em como encontrar os parâmetros ótimos, não apenas em adicionar mais variáveis.
   * **O System Price como "Fofoqueiro das Metas não Batidas":** Uma ideia poderosa que surgiu. Em vez de apenas sugerir um preço, o System Price (e as ferramentas ao redor dele) deveria ajudar o RM a diagnosticar *por que* certos imóveis ou categorias não estão performando. A análise deveria cruzar as categorias do System Price com as metas de faturamento do RM.
4. **A Confiança Virá dos Resultados e da Análise, não do Arsenal de Features:**
   * A confiança do RM não será conquistada pela adição de muitas features, mas sim por:
     * **Provas concretas de que o sistema pode performar bem**, mesmo que em um escopo limitado (análise retroativa, teste A/B em um piloto).
     * **Ferramentas que os ajudem a *entender* a performance e a *parametrizar melhor*,** em vez de apenas mais parâmetros para gerenciar.
5. **A Questão da Interface (Planilhas):**
   * Anderson levantou a preocupação sobre a complexidade de gerenciar tudo em planilhas, comparando com o antigo sistema de concorrentes.
   * A conclusão foi que, embora uma interface dedicada pudesse simplificar, o problema fundamental não é a interface em si, mas a falta de confiança e clareza na lógica e nos resultados.
6. **O Papel do Discovery foi Validado:**
   * Arilo validou que o papel do discovery é exatamente o que você fez: **entender por que a galera não usa o System Price**. Suas conclusões (falta de conhecimento, complexidade, falta de confiança, resultados imprecisos) foram confirmadas. O que a discussão trouxe foi um refinamento do *próximo passo* (a Fase 1).

**Próximos Passos (Redefinidos com Base no Feedback):**


1. **Segurar as Novas Features:** A ideia de implementar um grande conjunto de novas features (FH, FP, etc.) na Fase 1 deve ser pausada. Elas continuam válidas no backlog de "oportunidades", mas não são a prioridade imediata.
2. **Focar na Análise de Dados Profunda (Pré-Fase 1 ou Início da Fase 1):**
   * **Ação:** Realizar uma análise de dados (em conjunto com o time de Dados) para responder a perguntas chave:
     * Se o System Price, com as regras atuais, estivesse minimamente bem configurado/parametrizado, ele conseguiria se aproximar dos preços locados em um extrato do passado?
     * Quais categorias do System Price (Sazonalidade, Ocorrência, etc.) estão mais presentes nos imóveis que **não bateram a meta de RM**? Há uma predominância?
     * Para os imóveis que não bateram a meta, o que o System Price (se bem parametrizado) teria sugerido de diferente?
   * **Objetivo:** Gerar um diagnóstico baseado em dados que mostre onde o System Price tem potencial e onde ele falha. Isso é a "análise pronta" que o Arilo mencionou, necessária antes de se construir qualquer ferramenta.
3. **Refinar a Proposta da Fase 1:**
   * **A "Fase 1" se torna:** **"Análise, Melhorias na Parametrização e Ferramentas de Suporte para Regiões Não Sazonais".**
   * O foco muda de "implementar novas features" para:

     
     1. **Análise de Dados:** Realizar a análise descrita no ponto 2.
     2. **Primeiras Ferramentas de Suporte:** Construir as primeiras ferramentas que ajudem o RM a entender e parametrizar melhor, mesmo o sistema *atual*. Isso se alinha com as features de "Gerenciabilidade" (FG) que você listou, como o "Dashboard de Análise de Sensibilidade de Parâmetros" ou o "Simulador de Impacto" (em uma versão muito simples).
     3. **Teste A/B com Reparametrização:** Com base na análise, propor uma reparametrização para as regiões Não Sazonais e colocá-la em um teste A/B para provar seu valor.
4. **Ajustar a Apresentação para o RM/COO:**
   * Manter a estrutura de problema, dores, gaps, etc.
   * Na parte da "Proposta de Evolução", ajustar o foco da Fase 1 para refletir essa nova abordagem: "Nossa primeira fase não será sobre adicionar muitas coisas novas, mas sim sobre **analisar profundamente o que temos, provar seu potencial com uma reparametrização cuidadosa, e construir as primeiras ferramentas para que vocês (RM) tenham mais visibilidade e controle**."