<!-- title: Cypress - Testes E2E | url: https://outline.seazone.com.br/doc/cypress-testes-e2e-Lac1vv8gYL | area: Tecnologia -->

# Cypress - Testes E2E

## 1. Introdução

<aside> ℹ️ Essa documentação descreve a utilização do Cypress no Sapron. Nela, serão apresentados os passos que irão te orientar sobre como configurar, implementar e executar os testes E2E (end-to-end) com o Cypress.

Aqui você também poderá consultar todos os testes automatizados que já foram implementados no Sapron, e terá um norte para que você possa escrever os seus próprios testes.

Mas antes de entrar nos detalhes específicos sobre as configurações dessa ferramenta e a sua utilização no projeto, é importante destacar que o Cypress é um framework javascript voltado para a implementação de testes automatizados e2e.

Para o seu conhecimento, os testes E2E são aqueles testes que avaliam todo o fluxo de integração do sistema e que simulam a interação do usuário com a aplicação.

Em resumo, nos testes E2E é possível prever erros/bugs em um software de forma automatizada e tornar o software cada vez mais robusto na medida em que ele cresce.

</aside>

## 2. Instalação, configurações e organização de arquivos

* **2.1. Instalação**

  O Cypress está instalado no Sapron como dependência de desenvolvimento. Para o seu conhecimento, o comando utilizado para instalar essa dependência é o seguinte:

  ```bash
  yarn add cypress -D
  ```
* **2.2. Configurações do cypress.json**

  Com o Cypress instalado, é possível consultar algumas configurações existentes no arquivo ***cypress.json***:

  ```json
  {
      "integrationFolder": "./cypress/e2e/tests/",
      "baseUrl": "http://localhost:3000",
      "apiUrl": "http://localhost:8000",
      "video": false,
      "testFiles": [
          "Auth/*.ts",
          "Multicalendar/*.ts",
          "Properties/*.ts",
          "Host/*.ts",
          "Owner/*.ts"
      ],
      "*defaultCommandTimeout*": 10000,
      "retries": 1
  }
  ```
  * **IntegrationFolder:** parâmetro que define o caminho para a pasta onde estão implementados todos os testes e2e
  * **baseUrl:** parâmetro que define a url do servidor do front-end
  * **apiUrl:** parâmetro que define a url do servidor do back-end
  * **video:** parâmetro que define se você deseja ou não gravar a execução dos testes
  * **testFiles:** parâmetro que define a ordem em que os testes serão executados. Na ilustração acima, os primeiros testes a serem executados serão sempre os estão na pasta **Auth**, enquanto os últimos serão os que estão na pasta **Owner**
  * **defaultCommandTimeout:**  parâmetro que define um tempo limite para que os comandos reservados do Cypress terminem o que estão fazendo. Por exemplo, o comando **cy.get('input')** é um comando reservado do cypress que tenta buscar na DOM a tag input. Dito isso, defaultCommandTimeout é o limite de tempo máximo para que a tag input seja encontrada.
  * **retries:** parâmetro que define o número de tentativas para que o teste em execução no momento seja aprovado. Esse parâmetro é bem interessante de ser configurado pois ele tenta amenizar algumas aleatoriedades durante a execução dos testes que não estão sob o nosso controle, como por exemplo, a perda de conexão com a internet. No Sapron, esse parâmetro está definido com o valor 1 para que todo teste que falhar, seja repetido mais uma vez. Em caso de falha na segunda tentativa, o teste é de fato considerado uma falha. Em resumo, para um teste falhar no Sapron ele deve falhar no mínimo duas vezes.
* **2.3. Organização dos arquivos dos testes**

  No Sapron, os principais arquivos específicos para os testes estão localizados dentro da pasta *legacy*/cypress/\*\*, conforme o print a seguir:

  ![Untitled](/api/attachments.redirect?id=2d00b72d-893c-4808-8426-945f6a1bcb2a)

  Os arquivos estão organizados da seguinte maneira:
  * **e2e:** pasta que contém as implementações dos testes e2e
  * **fixtures:** pasta que contém os arquivos com dados mocados para uso nos testes. É nessa pasta que você deve inserir seus jsons fakes, ou mesmo, imagens quando estiver testando páginas que usam a funcionalidade de upload de arquivos
  * **plugins:** pasta que contém plugins do Cypress
  * **support:** pasta que contém os comandos customizados que são usados na implementação dos testes e2e

## 3. Executando testes e2e no Sapron

* **3.1. Executando e visualizando os testes no browser**
  * Acione o script do cypress para executar os testes em ambiente de staging. Use o seguinte comando dentro da pasta do front:

    ```bash
     yarn cypress:open
    ```
  * Após acionar o comando **yarn cypress** aguarde alguns segundos até que seja aberto o Dashboard do cypress. Em seguida, clique em "**Run integration specs**" para que a execução dos testes seja inicializada
* **3.2. Executando e visualizando os testes no terminal**
  * Acione o script do cypress para executá-lo em seu navegador. Use o seguinte comando:

    ```bash
     yarn cypess:run
    ```

## 4. Implementando testes e2e no Sapron - Passo a passo

* **4.1. Mapeando elementos HTML do Document Object Model** **(*DOM*)**

  A primeira etapa para que você consiga implementar os seus testes com o Cypress é mapear os elementos HTML do [DOM](https://tableless.github.io/iniciantes/manual/obasico/oquedom.html) das páginas que você vai testar. Na documentação do Cypress há uma [\*\*lista de seletores](https://docs.cypress.io/api/cypress-api/selector-playground-api)\*\* que podem ser usados para mapear os elementos HTML. Nesta documentação será apresentado apenas o seletor **data-cy** que é o mais recomendado de se usar pela própria documentação do Cypress, pois ele funciona como um atributo voltado exclusivamente para testes. Segue um exemplo de como usá-lo em seus testes:

  O código a seguir se refere a tela de Login do Sapron. Nela, há 3 elementos HTML (***input*** *email, **input** senha, **button** logar*) que foram mapeados com o seletor **data-cy**.

  ```jsx
  <TextField
      id="email"
      dataCy="email" // Mapeamento do input do email
      type="email"
      formik={formik}
      placeholder="Seu e-mail"
      startAdornment={(
        <InputAdornment position="start">
          <Mail strokeWidth={'1'} size={20} />
        </InputAdornment>
        )}
  />
  --------------------------------------------------------------------------
  
  <TextField
    id="password"
    dataCy="password" // Mapeamento do input da senha 
    type={type}
    
    formik={formik}
    startAdornment={(
      <InputAdornment position="start">
        <Lock strokeWidth={'1'} size={20} />
      </InputAdornment>
      )}
    endAdornment={(
      <InputAdornment position="start">
        {type === 'password'
          ? <EyeOff onClick={() => setType('text')} strokeWidth={'1'} cursor="pointer" size={20} />
          : <Eye onClick={() => setType('password')} strokeWidth={'1'} cursor="pointer" size={20} />}
      </InputAdornment>
      )}
  />
  --------------------------------------------------------------------------  
  
  <LoginButton type="submit" data-cy="btn-login"> // Mapeamento do button de login 
    Entrar
  </LoginButton>
   
  ```
* **4.2.** **Encapsulando os testes dentro de um contexto**

  Uma vez que os elementos HTML da página que você quer testar já estão mapeados de acordo com as recomendações descritas no passo 4.1, para iniciar a implementação do teste é necessário que você organize-o dentro de um contexto. Para exemplificar, no Sapron, o contexto do teste de autenticação se encontra no arquivo ***front/cypress/e2e/tests/Auth/Auth.ts****.* Esse contexto é definido da seguinte maneira:

  ```jsx
  describe('Auth', () => {});
  ```

  onde, **describe** é uma função que está recebendo como parâmetros uma string que descreve o contexto do teste, e uma função de callback onde os testes são implementados. Além de definir a função **describe**, é recomendado que você encapsule os seus testes dentro de funções nomeadas **it**, que devem descrever exatamente o que está sendo testado, como no exemplo a seguir:

  ```jsx
  describe('Auth', () => {
  	it('Should not allow the invalid user access', () => {});
  });
  ```
* **4.3.** **Visitando a página a ser testada**

  O Cypress disponibiliza o comando **cy.visit()** para acessar a url da página a ser testada. Para exemplificar o uso desse comando vamos ao exemplo de login do Sapron em que ele é usado para acessar a rota de login do sistema.

  ```jsx
  describe('Auth', () => {
  	it('Should not allow the invalid user access', () => {
  		cy.visit('/login');
  	});
  });
  ```
* **4.4.** **Buscando pelos elementos HTML mapeados**

  O Cypress disponibiliza o comando **cy.get()** para buscar pelos elementos HTML que você mapeou no passo 4.1. Para exemplificar o uso desse comando vamos ao exemplo de login do Sapron em que ele é usado para encontrar os elementos **input** mapeado como ***data-cy****="email"*, **input** mapeado como ***data-cy=****"password"* e **button** mapeado como ***data-cy=****"btn-login"*.

  ```jsx
  describe('Auth', () => {
  	it('Should not allow the invalid user access', () => {
  		cy.visit('/login');
  		cy.get('[data-cy]=email');
  		cy.get('[data-cy]=password');
  		cy.get('[data-cy]=btn-click');
  	});
  });
  ```
* **4.5.** **Preenchendo formulários e acionando evento de click**

  O Cypress disponibiliza o comando **cy.clear()** para limpar um campo de texto, bem como, os comandos **cy.type()** para inserir algum texto, e **cy.click()** para acionar um evento de clique. Para exemplificar o uso desse comando seguimos com o exemplo de login do Sapron em que **cy.clear()** e **cy.type()** são usados para limpar e preencher os inputs de email e senha, respectivamente; enquanto o comando **cy.click()** realiza a ação de clique no botão de logar no sistema.

  ```jsx
  describe('Auth', () => {
  	it('Should not allow the invalid user access', () => {
  		cy.visit('/login');
  		cy.get('[data-cy]=email').clear().type('sapron@seazone.com.br');
  		cy.get('[data-cy]=password').clear().type('teste123!');
  		cy.get('[data-cy]=btn-click').click();
  	});
  });
  ```
* **4.6.** **Usando assertions para validar os testes**

  O Cypress disponibiliza diversos comandos para que seja possível validar os testes. Um exemplo é o comando **should('contain.text', "Bem vindo ao sistema")** que valida se o campo retornado por **cy.get()** contém o texto "**Bem vindo ao sitema**". Outros comandos que poderia ser utilizados para as assetions vão depender do contexto do teste e podem ser verificados na documentação oficial.

  ```jsx
  describe('Auth', () => {
  	it('Should not allow the invalid user access', () => {
  		cy.visit('/login');
  		cy.get('[data-cy]=email').clear().type('sapron@seazone.com.br');
  		cy.get('[data-cy]=password').clear().type('teste123!');
  		cy.get('[data-cy]=btn-click').click();
  
  		cy.get('[data-cy]=tooltip-message').should('contain.text', 'Bem vindo ao sistema!');  
  	});
  });
  ```

## 5. Padronizações e dicas de boas práticas

* Os testes e2e do Sapron devem ser escritos no idioma inglês
* Mantenha a organização da estrutura de pastas dos testes
* Priorize sempre que possível o seletor data-cy para mapear os elementos HTML da página que estiver testando
* Tente ser objetivo ao descrever o que está sendo testado
* Peça ajuda se estiver com dificuldades em pensar nos casos de teste ou mesmo de implementá-los
* Consulte a documentação do Cypress para conhecer melhor outros recursos que não foram detalhados neste documento
* Busque sempre estar melhorando a escrita do código do seu teste ou mesmo o teste escrito por alguém da equipe

## 6. Banco de dados de testes do Sapron

Para que os testes e2e funcionem corretamente no Sapron usamos o banco de dados de staging com alguns dados já conhecidos pelo time de desenvolvimento, por exemplo, credenciais de autenticação de usuários de teste. Também mocamos o retorno das apis sempre que precisamos de dados previamente conhecidos antes de realizar algum teste.

## 7. Testes e2e já implementados no Sapron

* **7.1.** **Resumo financeiro do proprietário**
  - [x]  Deve validar o cálculo do valor total da receita de diárias e exibir o valor correto no grid de receitas
  - [x]  Deve validar se as informações de Receita, Despesa, Ajuste Manual, Comissão e Saldo do Período estão sendo exibidas no grid com os valores corretos
  - [x]  Deve validar se as informações da reserva estão corretas no modal da reserva
* **7.2.** **Ajuste direto imóvel**
  - [x]  Deve exibir um tooltip com a mensagem de erro se nenhuma propriedade for selecionada no grid ao clicar no "+" para realizar o ajuste
  - [x]  Deve ser possível adicionar um novo ajuste
  - [x]  Deve ser possível editar um ajuste existente
  - [x]  Deve ser possível excluir um ajuste
* **7.3.** **Ajuste direto anfitrião**
  - [x]  Deve exibir um tooltip com a mensagem de erro se nenhuma propriedade for selecionada no grid ao clicar no "+" para realizar o ajuste
  - [x]  Deve ser possível adicionar um novo ajuste
  - [x]  Deve ser possível editar um ajuste existente
  - [x]  Deve ser possível excluir um ajuste
* **7.4.** **Reporte de bugs para suporte (Host - Owner)**
  - [x]  Deve ser possível dos usuários Host e Owner acessarem a página de report de bug clicando no botão do pop-up de reportar erro.
* **7.5.** **Alerta de despesas duplicadas**
  - [x]  Deve validar se o sistema exibe uma mensagem de alerta de risco de inserção de despesas duplicadas

## 8. Lista de features do Sapron

[Google Sheets - create and edit spreadsheets online, for free.](https://docs.google.com/spreadsheets/d/1GiL6igGnAh1keKIXHJO6Vn20BOt-fpxuVBqTR0pQjX4/edit?usp=sharing)

## 9. Khanto Talks - Cypress

[Meet Google Drive - One place for all your files](https://drive.google.com/file/d/1TFc314gJc3luPHtx_KpFWORXl8U_kZcl/view?usp=sharing)

## 10. Documentação do Cypress

[Why Cypress? | Cypress Documentation](https://docs.cypress.io/guides/overview/why-cypress)