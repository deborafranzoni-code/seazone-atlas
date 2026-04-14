<!-- title: [RFC-0001] Parametrização da Homepage | url: https://outline.seazone.com.br/doc/rfc-0001-parametrizacao-da-homepage-1SARlybOtf | area: Tecnologia -->

# [RFC-0001] Parametrização da Homepage

| **Summary** | Standardize communication rules and establish common norms of usage |
|----|----|
| **Created** | October 16, 2025 |
| **Status** | **WIP** \| In-Review \| Approved \| Obsolete |
| **Owner** | Fulano |
| **Contributors** | *Ciclano, Beltrano* |

> Delete notes in *italics*. Remove sections that are not applicable.

# :page_facing_up: **Summary**

> *A brief explanation of the feature. A single-paragraph context-problem-solution summary. The goal is to make the purpose click for the reader. (It's usually best to write this as a final step of writing the RFC.)*


# :toolbox: **Problem**

> *A description of the problem that this RFC is trying to address, the constraints, and why this problem is worth solving now.*

Atualmente todas as páginas são construídas diretamente na código, não sendo possível customizar de forma fácil por alguém que não seja do time de desenvolvimento.

Uma atenção especial à Homepage (que é o foco desse RFC) que é a porta de entrada do site, e a qual para inserir novas seções e personalizar o conteúdo de cada uma depende diretamente de uma atuação do time de desenvolvimento. Dessa forma o time de produto (ou de pessoas externas) não conseguem customizar facilmente a Homepage sem a necessidade de novos deploys ou desenvolvimento de novo código.

# :dizzy: **Motivation**

> *Why are we doing this? What use cases does it support? What is the expected outcome? Which metrics will this improve? What capabilities will it add?*
>
> *Please focus on explaining the motivation so that if this RFC is not accepted, the motivation could be used to develop alternative solutions. In other words, enumerate the constraints you are trying to solve without coupling them too closely to the solution you have in mind.*

Temos uma Homepage que é rígida, no sentido de que para adicionar novas coisas ou modificar algo, sempre depende de novos desenvolvimentos. Queremos tornar possível que outros times consigam atuar em cima da Homepage inserindo novas seções e informando o que deverá aparecer em cada uma delas. E que para essas alterações, não dependam diretamente de atuação do time de desenvolvimento.

Além disso, queremos melhorar a perfomance da página: Tempo de resposta/carregamento e Métricas do Core Web Vitals.

**Casos de uso que queremos dar suporte:**

* Personalização das **abas** exibidas na Homepage
* Personalização das **seções** exibidas em cada aba
* Personalização dos **conteúdos** que serão exibidos em cada seção.
  * A seção poderá ser **Estática**: Conteúdo pre-definido (ex.: conteúdo patrocinado)
  * Ou **Dinâmica**: Conteúdo carregado de alguma outra fonte de forma dinâmica (precisa informar de qual fonte)
* Ações promocionais: Banners, Preços promocionais "De"<>"Por", Conteúdo Patrocinado

# :x: Non-Goals

> *What we will not cover in this RFC? What won't be done? What is not expected after this RFC is implemented?*

Neste RFC não será coberto a parametrização do site como um todo, inicialmente, apenas da Homepage.

Não será o foco também, a otimização das APIs já existente.

Não é o foco trazer seções que ainda não existem na Homepage. Partiremos do conteúdo que temos atualmente e o que seria necessário para implementar.

# :sparkles: **Proposal**

> *Explain the proposal as if it was already included in Monty and you were teaching it to another Monty user. That generally means:*
>
> * *Introducing new named concepts.*
> * *Explaining the feature largely in terms of examples.*
> * *If applicable, provide sample error messages, deprecation warnings, or migration guidance.*
> * *If applicable, describe the differences between teaching this to existing Monty users and new Monty users.*
> * *If applicable, include pictures or other media if possible to visualize the idea.*
> * *If applicable, provide pseudo plots (even if hand-drawn) showing the intended impact on performance (e.g., the model converges quicker, accuracy is better, etc.).*
> * *Discuss how this impacts the ability to read, understand, and maintain the code. Code is read and modified far more often than written; will the proposed feature make code easier to maintain?*
>
> *For implementation-oriented RFCs, this section should focus on how developer contributors should think about the change and give examples of its concrete impact.*

## :male_technologist: Tasks

- [ ] História 1
  - [ ] Task 1
- [ ] Task 2


# :books: References

> *Should link to external references (links, articles, videos, etc) that was used to embase this RFC.*

* <https://github.com/thousandbrainsproject/tbp.monty/blob/main/rfcs/0000_comprehensive_template.md>


# :rocket: **Definition of success**

> *How do we know if this proposal was successful?*


# :interrobang: **Unresolved questions**

> ***Optional***\*, but suggested for first drafts.\*
>
> *What parts of the design are still TBD?*


# :crystal_ball: **Future possibilities**

> ***Optional.***
>
> *Think about what the natural extension and evolution of your proposal would be and how it would affect Monty and the Thousand Brains Project as a whole in a holistic way. Try to use this section as a tool to more fully consider all possible interactions with the Thousand Brains Project and Monty in your proposal. Also consider how this all fits into the future of Monty.*
>
> *This is also a good place to "dump ideas" if they are out of the scope of the RFC you are writing but otherwise related.*
>
> *If you have tried and cannot think of any future possibilities, you may simply state that you cannot think of anything.*
>
> *Note that having something written down in the future-possibilities section is not a reason to accept the current or a future RFC; such notes should be in the section on motivation or rationale in this or subsequent RFCs. The section merely provides additional information.*