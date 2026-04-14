<!-- title: Escopo da reunião | url: https://outline.seazone.com.br/doc/escopo-da-reuniao-ZHR8pgcc0x | area: Tecnologia -->

# Escopo da reunião

# 1. Checklist para a Reunião: Alinhamento de Stack e Ferramentas

#### **A. Nivelamento de Conhecimento (Knowledge Share)**

- [ ] **Conceitos Básicos:** Todos entendem o que são alucinações, limites de tokens e a diferença entre modelos (ex: GPT-4o vs Claude 3.5 Sonnet)?
  - [ ] Multiplos agentes: 
  - [ ] Ideias: <https://github.com/snarktank/ralph>
  - [ ] FrontEnd: <https://github.com/seazone-tech/reservas-frontend/pull/2988/changes>
  - [ ] Seazone Design: <https://seazone-guidelines.netlify.app/>
  - [ ] \
- [ ] **Prompt Engineering do Time:** Vamos adotar um padrão de escrita de prompts? (Ex: Framework Persona-Contexto-Tarefa-Saída).

  \
- [ ] **Compartilhamento:** Como vamos trocar "prompts que funcionam"? (Canal no Slack, repositório de prompts, etc).
- [ ] \

#### **B. Definição da Stack de Ferramentas (The Tooling)**

- [ ] **IDE:** Vamos padronizar o uso do **Cursor** (que tem IA nativa) ou continuaremos no **VS Code + Copilot**?
- [ ] **Modelos de Chat:** Qual o modelo oficial para discussões de arquitetura? (Ex: Claude 3.5 Sonnet é hoje o favorito de muitos devs por lógica e código, enquanto GPT-4o é ótimo para automação).
- [ ] **CLI e Terminais:** Uso de ferramentas como Warp ou GitHub Copilot CLI.
- [ ] **QA Específico:** Uso de IA para geração de seletores, massa de dados ou escrita de Gherkin/BDD.
- [ ] **Ferramentas de Design:**

#### **C. Contexto do Projeto (Onde a IA "bebe água")**

* **Indexação de Código:** Como garantir que a IA do colega A tenha o mesmo contexto (conhecimento das libs internas) que a do colega B?
* **Arquivos de Regras (.cursorrules / .clinerules):** Vamos criar arquivos na raiz do projeto que ensinam a IA como nosso time escreve código (ex: "Sempre use Styled Components", "Sempre use Clean Architecture")?

#### **D. Workflow de Equipe**

* **Commits e Docs:** Usaremos IA para gerar mensagens de commit e documentação JSDoc/Swagger? Se sim, qual o padrão?
* **Pair Programming com IA:** Em tarefas complexas, como faremos o review de algo que foi 90% gerado por IA?


---

# 2. Documento de Saída: "IA Team Playbook"

Este documento serve para que um novo integrante do time saiba exatamente como o time usa IA para trabalhar.


---

#### **Guia de Operação com IA - \[Nome do Time\]**

#### **1. Nossa Stack de IA Homologada**

* **IDE Principal:** \[Ex: Cursor IDE\] - *Configurada com indexação de repositório ativada.*
* **Extensões Padrão:** \[Ex: GitHub Copilot, SonarLint\]
* **Modelos de Referência:**
  * **Lógica e Refatoração:** Claude 3.5 Sonnet.
  * **Explicação de Conceitos e Docs:** GPT-4o.
  * **QA/Testes:** \[Ferramenta específica ou modelo\].

#### **2. Padronização de Contexto (Project Rules)**

Para que a IA não sugira padrões diferentes do que o time usa, adotamos:

* **Arquivo de Regras:** Todo repositório deve ter um arquivo .cursorrules ou similar contendo:
  * Padrões de nomenclatura (camelCase, PascalCase).
  * Stack de testes (Jest, Cypress, Playwright).
  * Proibições (ex: "Não use a biblioteca Axios, use Fetch API").

#### **3. Guia de Uso por Papel**

* **Desenvolvedores (Back/Front):**
  * **Boilerplate:** Permitido para gerar estruturas repetitivas.
  * **Refatoração:** Sempre pedir para a IA explicar o "porquê" da mudança para garantir aprendizado do dev.
  * **Documentação:** Obrigatório revisar os comentários gerados (IA tende a ser prolixa).
* **QA (Quality Assurance):**
  * **Cenários de Teste:** Usar IA para ler o Requirement Document e sugerir cenários de borda.
  * **Automação:** Usar IA para converter comandos manuais em scripts (Cypress/Playwright).
  * **Massa de Dados:** Gerar JSONs de teste complexos.

#### **4. Ritos de Colaboração**

* **Review de Código IA:** No Pull Request, se um trecho grande foi gerado por IA, use a tag #AI-Generated. O revisor deve focar em: *Segurança, Performance e Manutenibilidade.*
* **Sessões de "Prompt Share":** Uma vez por mês (ou na sprint review), compartilhamos um "hack" ou prompt que economizou tempo.

#### **5. O que NÃO fazer (The "No-Go's")**


1. **Confiança Cega:** Nunca fazer commit de código que você não entendeu 100%.
2. **Vazamento de Dados:** Proibido colar segredos (.env), dados reais de usuários ou chaves de criptografia em chats de IA.
3. **Ignorar Testes:** Código gerado por IA **exige** a criação de testes unitários automatizados.


---

### Dica para o sucesso da implementação:

Crie um pequeno repositório chamado tech-ia-standards e coloque lá o seu arquivo de regras (.cursorrules ou um PROMPTS.md). Quando todos do time baixarem esse arquivo e usarem na IDE, a sensação de "trabalhar em equipe" será imediata, pois a IA de todos passará a sugerir o mesmo estilo de código.


# Pontos definidos:

* Definição de contexto do repositório (Back e frontend)
  * Fazer o link das skills para funcionar corretamente na claude e gemini
  * \
* Seazone Design: <https://seazone-guidelines.netlify.app/>
* Nova Template para PR


# Links uteis:

Link das documentações oficiais sobre skills:  

* <https://antigravity.google/docs/skills>  
* <https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview>