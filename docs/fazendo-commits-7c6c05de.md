<!-- title: Fazendo commits | url: https://outline.seazone.com.br/doc/fazendo-commits-7ZHcm70mX2 | area: Tecnologia -->

# Fazendo commits

Os commits realizados devem ser `atomicos`, ou seja, devem ser unidades objetivas que implementam uma única funcionalidade, ou tratam a correção de um único erro. ***#NÃO_FAÇA_COMMIT_BOMBA***

## Nosso padrão de commits

Use estrutura de `commits semânticos` para isso siga a orientação:

* Seja descritivo na mensagem e utilize um dos prefixos abaixo no início da mensagem do commit para indicar qual o tipo do commit.
  * **feat:** para novas features
  * **fix:** quando a task for para corrigir algo
  * **hotfix** quando for um correção urgente
  * **docs:** para algo relacionado a documentações, README e afins
  * **style:** quando for alteração no estilo
  * **refactor:** quando for apenas refatoração de código
  * **perf:** quando você mexer em algo relacionado a performance
  * **test:** para tarefas de testes
* Assim o commit ficará parecido com esse exemplo:

```
git commit -m **"feat: change in route settings for the login"**
```