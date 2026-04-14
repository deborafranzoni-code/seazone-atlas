<!-- title: Testes de software | url: https://outline.seazone.com.br/doc/testes-de-software-RzYA9e7IWF | area: Tecnologia -->

# Testes de software

Testamos uma aplicação para encontrar erros no produto desenvolvido e também verificar se se os resultados finais correspondem estão dentro do esperado.

Os testes são de extrema importância e devem caminhar lado a lado com o desenvolvimento do seu software, pois eles visam assegurar que a aplicação está funcionando corretamente e se atendem aos requisitos da regra de negócio.

Testes bem implementados garantem mais qualidade e segurança ao seu software.


---

## Algumas vantagens dos testes automatizados

* A automação dos testes vai reduzir consideravelmente a chance de termos erros no teste, ao contrário do teste manual que por sua vez é realizado por humanos;
* Reduz a quantidade de esforço realizada em testes manuais;
* Poupa recurso humano, isso é, não precisamos de pessoas para realizar os testes;
* Nos ajuda a encontrar e corrigir bugs existentes no sistema.


---

## Tipos de testes

* **Teste de unidade/unitário**

  É a fase de testes onde testamos cada unidade do sistema isoladamente. Nele testamos os métodos e funções da aplicação.

  Se seu código acessar qualquer coisa fora de seu processo, ele passa a ser um teste de integração.
* **Teste de integração**

  É o teste entre diferentes módulos em um sistema, como requisições http. Nele você verifica o resultado de uma requisição completa, analisando o formato de resposta, código de status, formato de dados e validação.
* **Teste de regressão**

  O objetivo do teste de regressão é assegurar que nenhum problema surgiu após sua evolução, ou seja, depois de termos implementado alguma feature nova.

  Ele tem esse nome, porque temos que testar novamente funcionalidades que já foram testadas antes para assegurar que tudo está ocorrendo como deveria.
* **Teste funcional**

  Visa testar o requisito de negócio e vai se concentrar em verificar a saída de uma ação.

  Nele verificamos se conseguimos por exemplo conseguir obter um valor específico de dentro do banco de dados.
* Importante → Esses não são todos os tipos de testes que existem, são apenas alguns exemplos para que possamos compreender um pouco mais sobre o assunto.


---

## TDD - Test-Driven Development

Podemos dizer que o TDD é o desenvolvimento orientado por testes, ou seja, desenvolvemos os testes antes do código de produção.

O TDD é baseado em pequenos ciclos de repetições, onde criamos um teste para cada funcionalidade do sistema.

 ![Untitled](/api/attachments.redirect?id=43ec6419-a87f-4c25-92c4-43d86150fc3b)

No exemplo que temos abaixo o teste inicialmente irá falhar, pois não temos a implementação da funcionalidade.

Em seguida escrevemos a funcionalidade que desejemos para fazê-lo passar e após isso podemos refatorá-lo seguindo boas práticas de desenvolvimento, garantindo assim uma maior coesão, facilidade de leitura e de manutenção, além de claro, um código mais limpo. Simples assim!

Neste tipo de estratégia nós temos também uma maior segurança na hora de refatorarmos nosso código, tendo em vista que se o teste falhar após uma refatoração, algo deu errado, podemos dizer o mesmo para a adição de novas funcionalidades.

```python
# 1 - escrevemos um teste que irá falhar já que não temos a função "sum_numbers"
# implementada ainda
def test_sum_numbers():
	a = 9
	b = 1
	assert sum_numbers(a, b) == 10

# 2 - implementamos a funcionalidade "sum_numbers"
def sum_numbers(a: int, b: int) -> int:
	return a + b

# 3 - Agora refatoramos nosso teste
def test_sum_numbers():
	assert sum_numbers(9, 1) == 10

# 4 - o teste irá passar e podemos seguir para o próximo
```


---

## Kiss (keep it simple and stupid)

Devemos escrever nosso código da forma mais simples possível!

Limpo, simples e funcional. Nosso objetivo é fazer o teste passar, e não perder tempo com código que não faz sentido dentro da funcionalidade.

## Alguns benefícios do TDD

* Código mais limpo;
* Segurança na refatoração;
* Segurança na correção de bugs;
* Possibilidade de integração contínua;
* Segurança de que nosso sistema está funcionando de acordo com o esperado.

## Boas práticas

* **Nossos testes devem possuir nomes autoexplicativos**

  Dê preferência a nomes que deixem o mais claro possível o que o código está se propondo a testar, mesmo que o nome escolhido seja grande.
* **Rode os testes diversas vezes**

  Por menor que seja a alteração realizada em seu código assegure-se de sempre rodar os testes. Recomendo rodá-los antes, durante e após finalizar uma alteração em seu código.

  Por via das dúvidas e apenas para ter certeza de não irá ter nenhuma surpresa desagradável, rode mais uma última vez antes de subir suas alterações finais.
* **Teste apenas uma coisa por vez**

  Apesar de podermos utilizar vários `assert` dentro de um bloco de instrução, podemos afirmar que isso é uma má prática, pois prejudica a clareza do que o teste está se propondo a fazer, aumenta a chance de bugs, torna o debug muito mais difícil de se realizar e também de identificar o motivo de uma possível falha durante o teste.
* **Não insira lógica nos seus testes**

  Nosso teste não deve possuir estruturas de decisões como `if`, `else` e/ou `switch`

  Se nos depararmos com um cenário onde o que foi citado acima aparece, provavelmente estamos olhando para um teste que está tratando mais de uma coisa, o que reitero que não deveria estar acontecendo.
* **Testes existentes devem passar antes de criar novos testes**

  Como podemos ver nesta **[imagem](https://www.notion.so/aec217b095ad4f249a09139ae643653e?pvs=21)** é importante que passemos para o próximo teste, apenas quando o que estivermos trabalhando esteja aprovado, ou seja, tenha passado como esperado.
* **Faça com que seu teste rode da forma mais simples possível**

  Quanto mais simples for o código de teste implementado, mais fácil será de implementar novos testes, realizar manutenções, visualizar possíveis problemas, identificar causas de bugs e escalar.

  Se nosso teste tem a necessidade de ser muito complexo, provavelmente nosso código de produção não está escrito da melhor maneira logo podemos dizer que um código que não é testável não é um bom código.
* **Não use dependências entre testes**

  Testes devem ser independentes e individuais.
* **Não remova nem altere testes antigos**

  Testes são implementados para assegurar que nosso software funcione da maneira que estamos esperando e que caso haja alguma mudança que interfira nesse resultado, tenhamos uma visualização e consciência de que algo está errado.

  Remover testes deve ser sempre evitado a não ser que aquela funcionalidade do sistema deixe de existir por alguma razão.

  Já no caso de alteração de testes, devem ser realizadas apenas caso haja alteração no propósito do código de produção.