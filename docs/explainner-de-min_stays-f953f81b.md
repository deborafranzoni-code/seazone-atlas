<!-- title: Explainner de Min_Stays | url: https://outline.seazone.com.br/doc/explainner-de-min_stays-JC6Oe2X79O | area: Tecnologia -->

# Explainner de Min_Stays

* **Iniciativa:** Explainner Min_Stays
* **Status:** Discovery Concluído
* **PM Responsável:** Lucas Abel
* **Stakeholders Principais:** Fábio de Biasi (RM), Victor Guindani (RM)


#### **1. Resumo Executivo** 

A equipe de RM enfrenta ineficiência e incerteza ao tentar identificar qual regra de min_stay está ativa para seus imóveis. Para resolver essa dor, propomos a criação do produto **"Explainner de Min_Stays"**, um dashboard no Looker Studio a ser entregue em duas fases planejadas.

* **Fase 1 (Entrega Rápida):** Um "Mapa da Regra", mostrando qual regra final está vigente para cada imóvel e **onde encontrá-la na Setup**, resolvendo a dor imediata de rastreabilidade.
* **Fase 2 (Entrega Completa):** Um "Log de Decisões", que exibirá todas as regras consideradas (aplicadas e ignoradas), oferecendo transparência total.

Esta abordagem entrega valor imediato ao RM enquanto gerenciamos a complexidade técnica da implementação do logging completo.


#### **2. O Problema: A "Caixa-Preta" da Estadia Mínima**

* **Falta de Rastreabilidade:** É impossível saber com clareza qual, entre as múltiplas regras de min_stay, está prevalecendo para um imóvel.
* **Ineficiência Operacional:** O processo de verificação é manual, custoso em tempo e descrito como um trabalho de "Sherlock Holmes".
* **Soluções Paliativas ("Gambiarra"):** A causa raiz raramente é encontrada, levando à criação de novas regras que aumentam a complexidade do sistema.


#### **3. A Solução: Entrega Faseada do "Explainner Min_Stays"**

A entrega será feita em duas fases distintas, dentro do mesmo produto/dashboard.

**Fase 1: Mapa da Regra Vigente (Entrega Rápida de Valor)**

O objetivo é responder à pergunta mais crítica do RM: **"De onde está vindo esta regra?"**

* **Entregável:** Um dashboard no Looker Studio com uma visualização em formato de tabela/lista.
* **Funcionalidade Principal:** O usuário poderá filtrar por imóvel, data, etc. A tabela mostrará:
  * **Imóvel:** O código do imóvel.
  * **Minstay Aplicada:** O valor final da estadia mínima.
  * **Período da Regra:** A data de início e fim em que a regra é válida.
  * **Localização da Regra:** Um "ponteiro" claro para a origem da regra. Ex: Setup - Aba: Minstay_Calendario, Setup - Aba: Minstay_Proprietario.
* **Benefício Imediato:** Resolve a dor mais urgente, permitindo que a equipe de RM encontre e corrija problemas rapidamente, sem a necessidade de investigações complexas.

**Fase 2: Rastreabilidade Completa (O Log de Decisões)**

O objetivo é responder à pergunta mais profunda: **"Por que esta regra venceu as outras?"**

* **Pré-requisito Técnico:** Esta fase depende da implementação de um mecanismo de logging no backend para capturar e armazenar todas as regras avaliadas.
* **Funcionalidade Principal:** Aprimoramento do dashboard. Ao clicar em um imóvel/data, o usuário verá:
  * Uma lista de **todas as regras de min_stay consideradas** para aquele contexto.
  * A indicação clara de quais foram **ignoradas** e qual foi a **vencedora**, incluindo a ordem hierárquica.
* **Benefício Final:** Oferece uma transparência total sobre o sistema, permitindo diagnósticos mais profundos e uma compreensão completa da lógica de sobreposição de regras.

#### **4. Considerações Técnicas**

* **Fase 1:** Viabilidade alta. Utiliza dados que já temos ou que são mais fáceis de expor (a regra final aplicada).
* **Fase 2:** Requer um esforço significativo de engenharia para criar o mecanismo de logging, justificando a separação em uma fase posterior.


\

---

\n