<!-- title: Jira Software x Github | url: https://outline.seazone.com.br/doc/jira-software-x-github-RUimj7RZqo | area: Tecnologia -->

# Jira Software x Github

Esta seção tem como finalidade ser uma explicação detalhada de como é funcionamento da integração do Jira Software com o Github. As informações disponibilizadas abaixo e o treinamento realizado foram desenvolvidos pelo @Paulo Lenz.

Link para o treinamento: <https://drive.google.com/file/d/1Whz_O8wY0KiiApdDkE6fgU8_clD60UHs/view?usp=drive_web>

# Integração JIRA com GIT

Este documento explica como utilizar a integração JIRA com GIT de maneira eficiente. Este fluxo de trabalho permite que você automatize muitas das ações do JIRA através dos comandos do GIT.

## Padrões para Branches e Commits

### Branches

Todos os branches e commits devem seguir o padrão de nomenclatura do Git Flow, com prefixos para indicar o tipo de tarefa que está sendo feita (confira na tabela abaixo). O nome do branch também deve incluir o número da tarefa do JIRA para facilitar a rastreabilidade.

### Padrão de nomenclatura para branches

| Padrão | Descrição |
|----|----|
| feature | Nova funcionalidade |
| release | Preparação para nova versão do produto |
| hotfix | Correções de bugs críticos em produção |
| support | Manutenção de versões antigas do produto que ainda estão em uso |

Para maiores informações consulte [Git Flow](https://www.atlassian.com/br/git/tutorials/comparing-workflows/gitflow-workflow).

### Commits

As mensagens de commit devem ser claras e explicativas, e também seguir um padrão que permita ao JIRA entender e processar automaticamente. Para isso, você deve incluir o código da tarefa no início da mensagem, seguido por um resumo do que foi feito. Também é possível adicionar mais informações, como o tempo gasto, um comentário adicional e a coluna para a qual o card deve ir seguindo o fluxo grama apresentado.

### Padrão de nomenclatura para commits

| Padrão | Descrição |
|----|----|
| feat | Uma nova funcionalidade |
| fix | Correção de bug |
| docs | Alterações na documentação |
| style | Alterações que não afetam o significado do código (white-space, formatação..) |
| refactor | Alteração no código que não corrige um bug nem adiciona uma funcionalidade |
| perf | Alteração no código que melhora a performance |
| test | Adiciona testes faltantes ou corrige testes existentes |
| build | Alterações que afetam o sistema de build ou dependências externas |
| ci | Alterações nos arquivos e scripts de configuração CI |
| chore | Outras alterações que não modificam os arquivos src ou test |

Para maiores informações sobre padrões de mensagem em commits consulte [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).

## Fluxo de Trabalho

Visualização do fluxo de trabalho no Jira.

### Criando um Branch

Para criar um novo branch a partir da `main` e iniciar uma nova funcionalidade, execute o seguinte comando, substituindo `feature-name` pelo nome apropriado. Por exemplo, se a tarefa do Jira for a SAP-146 e você está adicionando uma nova api para o APP account, a branch deve ser nomeada como `feature/SAP-146-add-account-new-api`.

Exemplo:

`git checkout -b feature/SAP-146-add-account-new-api`

Ou há um bug em produção que precisa ser corrigido em uma funcionalidade especifica:

`git checkout -b hotfix/SAP-147-fix-delete-button`

Ao criar a branch, o card da tarefa automaticamente será movido para a coluna "Em Progresso" no quadro do JIRA.

### Commitando suas modificações

Após adicionar e/ou modificar uma funcionalidade, você pode criar um commit para dividir seus PRs em fluxos de modificação. Isso contribui para uma melhor rastreabilidade e facilita possíveis `rollbacks`.

Exemplo:

`git commit -m "feature: updated users retrieve serializer" \            -m "SAP-146 #time 1h 30m #comment adicionada nova funcionalidade à conta APP #review"`

Ou para a correção de um bug:

`git commit -m "fix: fixed delete action" \            -m "SAP-146 #time 1h 30m #comment resolvido problema com o botão de delete na página XYZ #review"`

O Jira interpreta comandos padrões nas mensagens como: `#comment`, `#time` e `#<TRANSITION-NAME>`. Para linkar o commit com a task, basta adicionar o nome da task (neste caso `SAP-148`) à mensagem do commit (**Obrigatório** para efetuar o link). O comando `#comment` adiciona um comentário ao card (**Opcional**). O comando `#time` adiciona o tempo gasto na tarefa (**Opcional**). O comando `#<TRANSITION-NAME>` move o card para a possivel coluna de acordo com o [Fluxo de Trabalho](https://github.com/Khanto-Tecnologia/sapron-pms-web/wiki/Integracao-Jira#fluxo-de-trabalho) (**Opcional**).

Possiveis Transitions de acordo com o fluxo atual:

* start-working
* review
* rejected
* approved
* deploy-staging
* deploy-prod

> NOTA: No fluxo atual não é necessário adicionar nome da transiton ao corpo do commit

### Enviando para Revisão

Quando terminar o trabalho em sua funcionalidade, você pode enviá-la para revisão criando um Pull Request. Isso moverá a tarefa para a coluna "REVIEW PR" no quadro do JIRA.

### Após a Revisão

Se o PR for rejeitado, a tarefa voltará para a coluna "Em Progresso". Se for aprovado, ele será movido para a coluna "PR APPROVED".

### Depois da Aprovação

Após o processo de aprovação do PR, ele deverá ser movido para a coluna "STAGING".

### Depois do Staging

Depois de testar e verificar que tudo está funcionando como esperado no ambiente de staging, um novo deploy será feito para produção. Só então o card do Jira deverá ser movido para "DONE"

## Exemplo completo


1. Task/Card [SAP-148](https://seazone.atlassian.net/jira/software/projects/SAP/boards/3/backlog?text=sap-148) criado no Jira para a sprint atual. Nesse passo, Card permanece na coluna `TO DO`
2. Criar branch local a partir da main:

`git checkout -b feature/SAP-148-update-readme`

> Como a branch foi criada localmente e ainda não foi publicada no repositório, o card não será movido para a coluna IN PROGRESS, permanecendo na coluna TO DO até que o primeiro push seja enviado!


1. Após realizar suas alterações, envie-as para o repositório:

`git add README.md git commit -m "docs: added react badge to readme" \            -m "SAP-148 #comment Adicionado badges ao readme" git push origin feature/SAP-148-update-readme`


1. Card é movido automaticamente para a coluna `IN PROGRESS`
2. Criar Pull Request da nova `feature`
3. Card é movido automaticamente para a coluna `REVIEW PR`
4. PR aprovado no GIT
5. Card é movido automaticamente para a coluna `PR APPROVED`
6. Após o merge, voltar para a `main` e rodar os comandos:

`git checkout main  # volta para a main git fetch # atualiza o git local com o remote git pull origin main  # atualiza a branch local com a remote git fetch --prune  # deleta as branches que foram mergeadas`