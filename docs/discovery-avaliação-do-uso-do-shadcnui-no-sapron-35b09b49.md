<!-- title: [Discovery] Avaliação do uso do shadcn/ui no SAPRON | url: https://outline.seazone.com.br/doc/discovery-avaliacao-do-uso-do-shadcnui-no-sapron-Ra4cyFwa3p | area: Tecnologia -->

# [Discovery] Avaliação do uso do shadcn/ui no SAPRON

Shadcn/ui é uma coleção de componentes de interface de usuário (UI) reutilizáveis, projetada para React e construída com Tailwind CSS e Radix UI. Diferente de bibliotecas tradicionais, você não instala o shadcn como dependência; em vez disso, você copia e cola o código dos componentes diretamente no seu projeto, garantindo controle total, personalização e leveza.


Atualmente a empresa possui **três produtos front-end** ativos:

* **Wallet** — React + Tailwind CSS
* **Website** — Next.js + Tailwind CSS
* **SAPRON** — React + styled-components (uso pontual de MUI)

Wallet e Website já estão tecnicamente alinhados com Tailwind, enquanto o SAPRON possui um contexto legado, com maior custo de refatoração.

O SAPRON, por possuir stack diferente (styled-components), foi tratado como **exceção estratégica**, com plano de migração gradual, iniciando com a migração dos componentes do shadcn e depois partindo pra refatoração para uso do Tailwind


## Decisão Técnica Tomada

Foi decidido:

* utilizar o **shadcn/ui como base técnica**
* criar uma **biblioteca corporativa de UI**
* tratar a biblioteca como fonte única de componentes
* permitir adoção progressiva nos produtos
* postergar refatoração global do SAPRON


## Impacto em Design UI/UX

Foi identificado que:

* o design atual dos componentes precisará de revisão
* o time de Design UI/UX será envolvido


## Próximos Passos Definidos

### Curto prazo

* Criar repositório da biblioteca
* Configurar Tailwind + shadcn
* Criar componentes base
* Alinhar design com o time de UI

### Médio prazo

* Expansão do catálogo de componentes
* Definição formal de Design System
* Planejamento de refatoração gradual do SAPRON


## Conclusão

O discovery confirmou que é possível padronizar a UI entre os produtos da empresa sem comprometer a estabilidade do SAPRON.