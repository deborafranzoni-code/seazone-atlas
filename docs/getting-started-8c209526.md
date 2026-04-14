<!-- title: Getting Started | url: https://outline.seazone.com.br/doc/getting-started-kwqPNO0UBn | area: Tecnologia -->

# Getting Started

This wiki is built in Notion. Here are all the tips you need to contribute.

# Sapron || Front-end

O front-end do Sapron PMS foi desenvolvido com as seguintes tecnologias:

* ReactJS
* Yarn
* TypeScript
* Styled components
* Material UI
* Material UI icons
* Axios
* Eslint
* Cypress
* Circleci


---

## Padrão de projeto

* Criação de variáveis e funções usando camelCase. Exemplo: `const dailyPrice`.
* As telas devem ser responsivas.
* Todo Pull Request (PR) passa pelo Code Review (CR) da equipe de front
* Clean code

## Setup

Clone o repositório do sapron:

```bash
git clone <https://github.com/billbenettiSeazone/sapron-pms-web.git>
```

Inicie o container do Front:

```bash
make docker-front
```

Para rodar os comandos de yarn dentro do container usar `./cli/yarn <comando>`

Instale as depêndencias do projeto:

```bash
./cli/yarn install
```

Configure o .env do front:

```tsx
#Adicionar a url do backend
REACT_APP_URL=http://localhost:8000
```

## Como usar

Acesse a url `http://localhost:3000/` e faça o login usando o super usuário criado no backend.

## **Documentação**

<aside> ℹ️ A documentação do frontend é feita usando a ferramenta mdbook e fica hospedada no Github Pages. [Link da Documentação Sapron](https://billbenettiseazone.github.io/sapron-pms-web/frontend/book/)

</aside>

### **Instalando o mdBook**

Para instalar o projeto, basta utilizar os seguintes comandos no terminal Linux.

`$ curl https://sh.rustup.rs -sSf | sh  $ cargo install mdbook`

Após a instalação configure o PATH `mdbook` para o caminho da instalação `/home/[your_user]/.cargo/bin/mdbook`.

Com o mdbook instalado agora é só baixar a branch gh-pages do repositório do sapron e entrar nessa branch. A documentação do front está localizada em `sapron-pms-web/docs/frontend/`.

Os arquivos markdown são criados e editados em `sapron-pms-web/docs/frontend/src/`.

Para adicionar a documentação criada no menu lateral você precisa colocar o link para a página desejada no arquivo `SUMMARY.md`.

Para visualizar o que está fazendo pelo navegador você deve startar o servidor mdbook:

`mdbook server`

Por padrão ela roda na porta 3000 mas você pode rodar ela em outra porta com o seguinte comando:

`mdbook server -p 3001`

Após terminar de escrever a documentação você precisa fazer o build, para isso rode o seguinte comando:

`mdbook build`

Mais detalhes sobre como usar o mdbook veja a [Documentação](https://rust-lang.github.io/mdBook/index.html)

### **Padronização da documentação**

* A documentação está estruturada por usuários, ou seja nós temos uma pasta Anfitrião com todas as features dele, uma pasta Proprietário com todas as features dele e assim por diante. Somente o Multicalendar não segue esse padrão, por ter muitas features e ser acessado por mais de um usuário.
* O nome dos arquivos é criado com padrão snake_case, exemplo `create_reservation.md`.
* [Template para usar na Documentação de uma feature](/doc/template-de-documentacao-QLDYgVTSB4)

## Testes Cypress

Pra executar os testes e visualizá-los em seu navegador siga os passos a seguir:

* Suba todos os containeres do projeto com o comando sudo docker-compose up;
* Certifique que os containeres estão todos upados antes de executar os passos seguintes;
* Na pasta raíz do projeto rode o comando:

```bash
cd front && yarn cypress
```

* Na janela que será aberta clique em "Run integration specs".

Pra executar os testes e visualizá-los em seu terminal siga os passos a seguir:

* Suba todos os containeres do projeto com o comando sudo docker-compose up;
* Certifique que os containeres estão todos upados antes de executar o passo seguinte;
* Na pasta raíz do projeto rode o comando:

```bash
cd front && yarn cypress:run
```

## Testes unitários com JEST

* links úteis
  * [Documentação global do jest](https://jestjs.io/pt-BR/docs/getting-started)
  * [Jest para React](https://jestjs.io/pt-BR/docs/tutorial-react)
  * [Receitas de teste](https://pt-br.reactjs.org/docs/testing-recipes.html)
* Como rodar os testes unitários ?

  Para rodar os testes com o jest, existem várias formas, a mais simples é utilizando o comando pronto

  ```bash
  make run-jest
  ```

  básicamente o que ele faz é dar permissão de execução para o Shell Script `run-jest` dentro da pasta `./cli` e rodar os testes unitários.
  * Caso não tenha o make file instalado

  Se não tiver o make instalado, você ainda pode rodar os testes diretamente da pasta `./cli` para isso rode o seguinte comando na raiz do projeto:

  ```bash
  ./cli/run-jest
  ```
  * Error permission denied

  Por padrão algumas distribuições bloqueiam a execução de arquivios **bash** ou S**hellScript**, para resolver isso você precisa dar permissão de execução para o `run-jest` dentro da pasta `./cli`, através do seguinte comando:

  ```bash
  chmod +x ./cli/run-jest
  ```

  **Obs: vale lembrar que este comando só precisa ser dado uma vez, ja que depois disso o arquivo já estara pronto para ser executado sempre**

## Patterns de testes unitários

Nem todos os componentes precisam ser testados através dos testes unitŕaios, devemos testar principalmente componentes que estejam sendo usados por várias partes da aplicação, um bom exemplo para o `front` seria o componente de `FormButton` ele é usado em todos os botões da aplicação e possúi uma grande complexidade de código, um ótimo componente para implementarmos os testes unitários, assim garantimos que não vá existir nenhum comportamento inesperado na aplicação quando existir a necessidade de alterar algo dentro do componente do `FormButton`.

* Padrão de código

  É importante para mantermos o padrão que os testes unitários sejam criados dentro de seus respectivos componentes de teste, seguindo o seguinte padrão de nomenclatura:

  ```tsx
    NomeDoCompoente.test(.ts | .tsx)
  ```

  Como no exemplo dos componentes do FormButton

  ![/api/attachments.redirect?id=60056510-7387-4169-9015-5fed3aec000d](/api/attachments.redirect?id=dbcd11c8-ad57-4a62-8051-2e6bb33db420)
* Boas praticas para os testes

  Existem algumas boas praticas para implementar os testes unitários, para nos ajudar na organização do código com o jest:
  * **Arquivos Separados** Testes unitários devem ser escritos em arquivos separados, por exemplo: `./front/components/FormButton/FormButton.test.ts`
  * **Describe:** Use os describe do jest para organizar os testes unitários, por exemplo: `describe('FormButton', () => {`
    * **Obs:** Vale lembrar que é possível criar um describe dentro de outro, então crie um describe principal com o componente a ser testado e organize os testes em grupos menores de describe dentro dele, por exemplo: `describe('FormButton', () => { describe('Button', () => {`
* O que testar com o jest ?

  Nem todos os componentes do projeto precisam de testes unitários, é recomendado usar em certos casos específicos como por exemplo:
  * **Componentes muito utilizados:** Componentes que sejam reutilizados por várias partes do projeto, como no caso dos FormButtons
  * **Muitas requisições em API'S:** Componentes que sejam muito grandes e possuam muitas requisições em api e etc, como no caso do Calendário, é possível testar com o jest se o retorno daquela api específica esta de acordo com o esperado assim evitando uma série de problemas que podem ser desencadeados
  * **Componentes principais de páginas que sejam muito grandes:** Componentes que sejam muito grandes tendem a ficar mais complexos cada vez mais e a manutenção fica cada vez mais dificil, como é o caso do componente principal da página de controle, que esta cada dia maior e com mais funcionalidades, testar algumas funções dele de foram isolada é ideal para termos certeza de que nada esta quebrando ou sendo mudado enquanto implementamos novas funcionalidades, este é um dos exemplos, temos outros componentes que também estão bem complexmos no Sapron

## Codando os testes unitários com o Jest

Os testes unitários com o Jest possúem uma sintaxe muito intuitiva, basta criar um arquivo `.test.js` e dentro dele criar uma função `test` ou `it` que recebe um parâmetro `t` que é o teste unitário.

```tsx
// FormButton.test.jsx
import { render, screen } from '@testing-library/react';
import FormButton from './FormButton';
describe('Testes no componente FormButton', () => {
  it('Testando o botão sem passar nenhum parâmetro e verificando se na tela ele vai ser exibido com a role de button', () => {
    // o render do testing-library/react retorna um debug que funciona como um console.log daquele elemento
    // além disso ele cria uma renderização virtual na dom
    // simulando uma renderização pelo react-dom convencional
    render(<FormButton />);
    const typeButton = screen.getByRole('button');
    expect(typeButton).toBeInTheDocument();
  });
});
```

```tsx
// rodando o debug do testing-library/react
import { render } from '@testing-library/react';
import FormButton from './FormButton';
describe('Testes no componente FormButton', () => {
  it('Testando o botão sem passar nenhum parâmetro e verificando se ele vai sair do tipo button', () => {
    const { debug } = render(<FormButton />);
    debug();
  });
});
```

```tsx
<!-- saída do console.log -->

    <body>
      <div>
        <button
          class="MuiButton-root MuiButton-text MuiButton-textPrimary MuiButton-sizeMedium MuiButton-textSizeMedium MuiButtonBase-root sc-bdfBwQ gUPQBC grey  css-d0ukip-MuiButtonBase-root-MuiButton-root"
          customcolorbg="blue"
          data-cy=""
          linkto="0"
          tabindex="0"
          type="submit"
        >
          <span
            class="MuiButton-label css-8xplcm-MuiButton-label"
          />
          <span
            class="MuiTouchRipple-root css-8je8zh-MuiTouchRipple-root"
          />
        </button>
      </div>
    </body>
```

## Instalação de nova biblioteca

```bash
./cli/yarn nome-da-biblioteca
```

## Produtividade

Configurando seu VS Code para ao salvar o arquivo corrigir automaticamente problemas de Eslint.

Vá em configurações do VS Code, clique em settings, clique em `Edit in settings.json` e adicione o seguinte trecho de código:

```json
{
...,
"editor.formatOnSave": false,
    "editor.codeActionsOnSave": {
        "source.fixAll.eslint": true
    },
    "eslint.validate": [
        "javascript",
        "javascriptreact"
    ],
}
```

Extensões recomendadas para instalar no seu VS Code:

* Eslint
* Editor config
* Material icons
* Styled components
* Color highlight
* Bracket Pair Colorizer 2