<!-- title: Dia  2 - GUIA | url: https://outline.seazone.com.br/doc/dia-2-guia-5li7kz5KSX | area: Tecnologia -->

# Dia  2 - GUIA

* **Tecnologias utilizadas**
  * ReactJS
  * Yarn
  * Typescript
  * Styled components
  * Material UI / Material UI icons
  * Axios
  * Cypress
  * Eslint
  * Circle CI
* **Estrutura do projeto**
  * ***src***
    * ***assets →*** local destinado para os ícones e animações da aplicação
    * ***components →*** local destinado para os componentes customizados da aplicação
    * ***context →*** local destinado para os contextos que permitem gerenciar os estados compartilhados entre um ou mais componentes da aplicação
    * ***hooks →*** local destinado para os hooks da aplicação \*\*
    * ***mocks →*** local destinado para os dados mocados
    * ***pages →*** *local destinado para as páginas*
    * ***services →*** *local destinado para os adicionar as requisições às apis*
    * ***styles →*** local destinado para os estilos globais e paleta de temas da aplicação
    * ***utils →*** local destinado para a criação de funcionalidades úteis da aplicação (exemplo: *Formatação de máscara de CPF, telefone, números, datas, entre outros.*)
    * ***Routes.tsx →*** local destinado para a definição das rotas e permissões de acesso às páginas da aplicação
* **Padronizações e boas práticas de implementação**

  > ***[Khanto Talks sobre Clean Code](https://drive.google.com/drive/u/2/folders/1viVxA6BElOk2j9fY9GRgaR4whLWet266)***
  * Todo o código deve ser implementado no idioma Inglês sempre que possível
  * Nome de variáveis e estados devem seguir o padrão *camelCase*: **Exemplo:** **dailyPrice**
  * Ao criar um novo componente ou uma nova página deve-se seguir o seguinte padrão:
    * *ComponentName*\*\*.tsx\*\*
    * *index*\*\*.ts\*\*
    * *styles*\*\*.tsx\*\*
  * As telas devem ser responsivas para mobile, exceto quando estiver especificado que a tela não deve ser responsiva no card do trello
  * Implementar, sempre que possível, componentes reutilizáveis
  * Reutilizar, sempre que possível, componentes que já tenham sido implementados para evitar ter componentes redundantes no projeto
  * Buscar, sempre que possível, melhorar a escrita do próprio código ou o código que foi desenvolvido por algum outro colaborador
* **Git e Github**

  > ***[Khanto Talks sobre Git](https://drive.google.com/drive/u/0/folders/1DGihLI4bXZco1we3T7xK0uxhaJM_Axuf)***
  * Adicionar Dev ao repositório do projeto
  * **[Nomenclatura de branchs](/doc/instrucoes-de-contribuicao-no-projeto-Xn1o0ObOBQ)**
  * **[Padrão de commits](/doc/instrucoes-de-contribuicao-no-projeto-Xn1o0ObOBQ)**
  * [Template de pull requests](https://github.com/billbenettiSeazone/sapron-pms-web/blob/main/.github/PULL_REQUEST_TEMPLATE.md)
  * Revisão de Pull Requests
    * Adicionar revisores
    * Adicionar tags
    * Aprovar, changes request
* **Trello**

  > ***[Khanto Talks sobre SCRUM](https://drive.google.com/drive/u/2/folders/15BmLtOV-fKowCAxOVobMl1qGYNtWxVPX)***
  * Adicionar Dev ao board do trello do projeto
  * Acessar o Trello e explicar como as tasks estão organizadas
    * **Listas**
      * **Resources:** Onde fica alguns links e/ou documentos importantes para o projeto.
      * **Supports To-Do:** Lista que contém as tasks vindas dos pedidos de suporte.
      * **To-do:** Tarefas à fazer na Sprint.
      * **In Progress:** Tarefas que estão em andamento.
      * **Testing:** Tarefas que ficaram prontas mas estão em revisão (PR em aberto).
      * **Increment (Sprint Review):** Tarefas que foram mergeadas com a **main.**
    * **Cards**
      * Todas as tarefas são atribuídas à quem deverá fazê-la. **PS:** Para facilitar a visualização das suas tarefas ou de seu time, use os filtros.
      * Usamos tags nos cards que facilitam saber do que se trata aquela tarefa e sua prioridade.
      * Deve sempre ser realizada a tarefa que possui maior prioridade.
      * Não iniciar uma nova tarefa até que finalize a atual; Se ficar travado, peça ajuda à um colega.
  * Utilizamos a metodologia ágil SCRUM:

    **Artefatos do Scrum utilizados:**
    * **Sprint:** Atualmente a Sprint do projeto tem duração de duas semanas.
    * **Daily Meeting:** Reuniões diárias onde todos do time de desenvolvimento se junta para responderem basicamente 3 perguntas:
      * O que fez ontem?
      * O que planeja fazer hoje?
      * Está com algum impedimento/travamento?
    * **Weakly:** Reunião semanal onde os times de todos os projetos se reúne para falarem/mostrarem seus feitos durante a semana anterior e falar do seu planejamento para a semana atual.
    * **Sprint Planning/Review:** Sprint Planning e Review são realizadas no mesmo dia.

      **Sprint Review:** o time de desenvolvimento se reúne para falar como foi a Sprint passada, as dificuldades, os aprendizados, etc. **Sprint Planning:** O Gerente de Projeto apresenta as tasks de cada integrante para a próxima Sprint . O Time de Dev dá seu feedback em cima das tarefas se são suficientes, insuficientes ou se são muitas tarefas para a Sprint.

    > **OBS:** Caso perceba que não vai ser possível concluir todas as suas atividades durante a Sprint, avise o Gestor do Projeto.
* **Lição de casa**
  * Assistir ***[Khanto Talks sobre Git](https://drive.google.com/drive/u/0/folders/1DGihLI4bXZco1we3T7xK0uxhaJM_Axuf)***
  * Assistir ***[Khanto Talks sobre Clean Code](https://drive.google.com/drive/u/2/folders/1viVxA6BElOk2j9fY9GRgaR4whLWet266)***
  * Revisar como o projeto está estruturado (*Organização de arquivos e pastas*)