<!-- title: ATA DE REUNIÃO – DISCOVERY ENRIQUECIMENTO DE CONCORRENTES | url: https://outline.seazone.com.br/doc/ata-de-reuniao-discovery-enriquecimento-de-concorrentes-9ZZyCWSuZx | area: Tecnologia -->

# ATA DE REUNIÃO – DISCOVERY ENRIQUECIMENTO DE CONCORRENTES

**Data:** 09 de Outubro de 2023 **Duração:** 21 minutos **Participantes:**

* Lucas Abel da Silveira 
* Viviane Naomi Kohatsu
* Victor Guindani

**Assunto:** Apresentação e discussão sobre a nova Plataforma de Inteligência de Concorrentes e definição de próximos passos para seu enriquecimento.


## **1. Abertura e Objetivo**

A reunião foi iniciada por Lucas, que apresentou a nova "Plataforma de Inteligência de Concorrentes". O objetivo principal foi centralizar as informações sobre concorrentes, que antes estavam dispersas em múltiplas planilhas e painéis de BI, e discutir as evoluções necessárias para aprimorar a ferramenta com base no uso da equipe de operações.


## **2. Apresentação da Plataforma e Ferramentas Atuais**

* **Centralização:** Foi apresentado o novo BI que unificará as informações de concorrentes, incluindo o CRM, painel de auditoria e dados com e sem "extrata". O objetivo é otimizar o acesso e a análise, evitando a dispersão de informações.
* **Painel de Saúde:** Lucas demonstrou o painel que classifica a "saúde" das categorias em verde, amarelo e vermelho. A classificação se baseia na quantidade de concorrentes e em métricas de qualidade, como a identificação de *outliers* de precificação.

## **3. Discussão e Sugestões de Melhoria**

Durante a demonstração, os participantes levantaram pontos e sugestões para aprimorar a plataforma:

* **Identificação de Outliers (Hotliers):**
  * **Ponto levantado por Viviane:** Atualmente, a identificação de *outliers* é baseada na precificação. Viviane sugeriu que seria extremamente útil também identificar *outliers* com base no faturamento, alinhando a ferramenta com o processo manual que ela já realiza.
  * **Ação:** Lucas anotou a sugestão e verificou a documentação para entender como os scores de frequência e certificação (baseados em IQR) são calculados. A ideia é tornar a análise mais explicável.
* **Expansão da Lógica de Candidatos a Concorrente:**
  * **Ponto levantado por Viviane:** A lógica atual para sugerir "candidatos a concorrente" é limitada (apenas por polígono, tipo e quartos). Ela sugeriu a inclusão de outros critérios:

    
    1. **Polígono expandido:** Buscar imóveis em uma área maior.
    2. **Compensação:** Incluir imóveis com números de quartos próximos (ex: 1 quarto pode compensar com 2 ou 3).
    3. **Equivalência:** Puxar candidatos de categorias marcadas como "equivalentes", mesmo que em outras regiões.
  * **Ação:** Lucas anotou todas as sugestões para incorporá-las à lógica da plataforma, visando expandir o número de concorrentes disponíveis para análise.

## **4. Proposta de Evolução: Modelo de Concorrentes "Lookalike"**

* **Apresentação:** Lucas introduziu a principal iniciativa de evolução: a criação de um modelo "Lookalike" (semelhantes). O objetivo é encontrar concorrentes que, mesmo não estando na mesma região, possuam comportamento de preço, sazonalidade e características semelhantes.
* **Discussão:**
  * Viviane comparou a proposta com o processo manual de definir "equivalências" entre regiões distantes, que é feito por tentativa e erro ("olhômetro").
  * Victor reforçou a necessidade de parametrizar essa lógica para que o sistema possa gerar automaticamente uma lista de concorrentes semelhantes.
  * Foi definido que esses concorrentes "Lookalike" chegariam à plataforma para uma validação manual, e, se aprovados, seriam adicionados às categorias através do campo de "equivalência" ou "compensação".

## **5. Próximos Passos e Definição de Prioridades**

* **Feedback Contínuo:** Lucas solicitou que Viviane e Victor utilizem a plataforma no dia a dia para que possam identificar dores e oportunidades de melhoria, fornecendo feedbacks constantes para refinar a ferramenta.
* **Definição de Prioridades:** Victor questionou sobre o andamento do projeto de "Quarentena de Imóveis Novos". Lucas explicou que ele está com prioridade baixa e apresentou um dilema para a equipe de operações:
  * **Opção A:** Acelerar o desenvolvimento do "Enriquecimento de Concorrentes" (com a funcionalidade Lookalike), que é mais complexo e demorado.
  * **Opção B:** Priorizar o projeto de "Quarentena de Imóveis Novos", que tem um esforço de desenvolvimento menor.
* **Ação Definida:** A equipe de operações (Viviane e Victor) deve deliberar internamente qual das duas iniciativas trará maior valor no curto prazo para definir qual será a próxima tarefa da equipe de desenvolvimento.