<!-- title: Instruções de contribuição no projeto | url: https://outline.seazone.com.br/doc/instrucoes-de-contribuicao-no-projeto-eHEzTHG2in | area: Tecnologia -->

# Instruções de contribuição no projeto

# Como contribuir

## Fluxo de desenvolvimento

* O fluxo de desenvolvimento está descrito no **README.md**
* Toda nova tarefa deve ser submetida por uma Pull Request e deve ter no mínimo uma aprovação antes de ir para a main.
* Faça diversos commits dependendo do tamanho da task.
* Os commits devem ser descritivos. Eles devem contar uma história do seu desenvolvimento.


---

## Branches

* Todas as branches devem ser escritas em inglês
* As branches são categorizadas da seguinte forma:
  * `feature/` ⮕ Para implementação de nova feature
  * `task/` ⮕ Para implementação de uma tarefa que não seja nem uma feature nem um bug
  * `fix/` ⮕ Para correção de um bug
  * `hotfix/` ⮕ para correção de um bug urgente, que irá paralisar o andamento do projeto em alguma parte ou para alguém
    * ex:

      `feature/new-component`

      `task/neither-feature-nor-bug`

      `fix/not-urgent-bug`

      `hotfix/urgent-bug`


---

## Commit Message

* Os commits devem ser feitos em inglês e devem ser feitos de forma que "contem uma história"
* Deve ser evitado ao máximo commits "bomba", que são aqueles que tem todas ou muitas alterações em um commit só.

### **Padrão de commits**

```bash
git commit -m 'feat: message' # <new feature>
git commit -m 'fix: message' # <documentation a bug fix>
git commit -m 'docs: message' # <documentation only>
git commit -m 'style: message' # <changes that do not affect the meaning of the code>
git commit -m 'refactor: message' # <neither fixes a bug nor adds feature>
git commit -m 'perf: message' # <a code change that improves performance>
git commit -m 'test: message' # <adding missing tests or correcting existing tests>
git commit -m 'build: message' # <changes that affect the build or dependecies>
git commit -m 'ci: message' # <changes to our CI conf files>
git commit -m 'chore: message' # <changes that do not modify src or test files>
```


---

## Pull Request

* As discussões dentro das Pull Requests devem ser feitas em português para maior compreensão de todos
* O template de Pull Request deve ser preenchido!
* O PR deve ser descritivo


---

## Guia de estilo Frontend

* Todo o código e documentação `(storybook)` quando possível devem ser escritos em inglês
* O projeto usa o style guide do Airbnb


---

## Guia de estilo Backend

* Todo o código quando possível deve ser escrito em inglês
* As APIs são desenvolvidas na arquitetura REST
* Utilizamos o formato de data: `yyyy-mm-dd`

[Documentação de Software- Sapron](/doc/documentacao-de-software-sapron-QV0Hm45oTn)