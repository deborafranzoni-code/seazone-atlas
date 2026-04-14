<!-- title: Uso de IA no Time | url: https://outline.seazone.com.br/doc/uso-de-ia-no-time-qnKZjv7X99 | area: Tecnologia -->

# ✨ Uso de IA no Time

### 1. Estrutura de Agentes e Contextos (IA)

* **Foco Inicial:** O projeto de estruturação dos "agentes" e arquivos de contexto começará pelo repositório de **Reservas**, onde o time tem mais domínio e contexto. 

  \
* **Arquitetura de Contexto:**
  * Foi decidido criar uma **versão genérica** (que possa ser exportada para outros times, como o SAPRON) e uma **específica para Reservas**.
  * A organização dos arquivos de contexto será baseada na **estrutura do código e endpoints**, e não necessariamente por BU, para evitar problemas caso a estrutura organizacional da empresa mude.
  * O time de Back-end vai ajustar a estrutura dos "agentes" para considerar as praticas que o time de Front-end sugeriu.

    \
* **SAPRON:** Será o próximo passo, mas exigirá alinhamento com outros times, já que é um repositório compartilhado (monolítico/com muitos colaboradores).


### 2. Padronização de Processos e PRs

* **Template de Pull Request (PR):** O time decidiu unificar o padrão de PR. O modelo do Front-end será atualizado para seguir o padrão do Back-end, que é mais detalhado e inclui checklists e instruções de "como testar".
* **Instruções para a IA:** O template de PR e a documentação servirão como base para as instruções (prompts) que a IA utilizará para gerar código e contextos.


### 3. Qualidade de Código e Testes

* **Cultura de Testes:** Ficou acordado que a cobertura de testes é agora **mais crucial do que nunca**. O uso de IA exige que o processo de testes impeça que novas funcionalidades quebrem o que já existe (o "efeito Frankenstein").
* **Documentação como Guia:** A documentação interna passa a ser vista como a "fonte de verdade" para a IA. Se um novo desenvolvedor (ou a IA) entrar no projeto, ele deve ser capaz de entender tudo apenas lendo os arquivos de contexto (.agents ou similares).
* **Testes**: Karina, revisará a documentação de testes e garantir que os diferentes tipos de testes (regressão, etc.) estejam cobertos.

  \

### 4. Design System

* O "Season Design" será a fonte oficial de verdade para tudo o que for relacionado a design no contexto da IA. link: <https://seazone-guidelines.netlify.app/>



5. ### DoD:

- [ ] Contexto dos agentes nos repositórios de Back-end e Fron-end 
- [ ] Template de PR Back-end e Fron-end
- [ ] Karina, revisará a documentação de testes e garantir que os diferentes tipos de testes (regressão, etc.) estejam cobertos.



6. Links uteis:

* <https://antigravity.google/docs/skills>  
* [https://platform.claude.com/docs/en/agents-and-tools/agent-s](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)