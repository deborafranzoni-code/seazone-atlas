<!-- title: Testes unitários com o Jest | url: https://outline.seazone.com.br/doc/testes-unitarios-com-o-jest-12DoyYewmE | area: Tecnologia -->

# Testes unitários com o Jest

## Testes Unitários

Os testes unitários são uma parte fundamental da prática de desenvolvimento de software e são projetados para testar unidades individuais de código-fonte. Uma unidade pode ser uma função, um método, uma classe ou até mesmo um módulo, dependendo do contexto. O objetivo dos testes unitários é garantir que cada unidade do software funcione conforme o esperado. Para isso utilizamos o Jest.

### **Jest Docs**

[Iniciando · Jest](https://jestjs.io/pt-BR/docs/getting-started)

## **O que testar usando Jest ?**

Nem todos os componentes precisam ser testados através dos testes unitários, devemos testar principalmente componentes que estejam sendo usados por várias partes da aplicação, um bom exemplo para o *front* seria o componente de *FormButton* ele é usado em todos os botões da aplicação e possui uma grande complexidade de código, um ótimo componente para implementarmos os testes unitários, assim garantimos que não vá existir nenhum comportamento inesperado na aplicação quando existir a necessidade de alterar algo dentro do componente do *FormButton*. Os testes que podemos realizar são:


1. **Testes de Componentes:**
   * Teste os componentes React para garantir que eles renderizem corretamente e exibam o comportamento esperado em diferentes estados e propriedades.
2. **Testes de Renderização:**
   * Verifique se os componentes são renderizados corretamente. Use as funções de renderização do Jest (como `render` ou `shallow`) para inspecionar a saída HTML e as props dos componentes.
3. **Testes de Estado e Props:**
   * Teste como os componentes respondem às mudanças de estado e props. Garanta que o estado e as props afetem corretamente o comportamento e a renderização do componente.
4. **Testes de Eventos (se aplicável):**
   * Simule eventos (como cliques, mudanças, etc.) e verifique se os manipuladores de eventos estão sendo chamados e se o componente reage corretamente.
5. **Testes de Hooks (se aplicável):**
   * Se você estiver usando hooks em seus componentes, teste-os para garantir que eles gerenciem o estado corretamente e interajam bem com o ciclo de vida do componente.
6. **Testes de Integração (se aplicável):**
   * Teste a interação entre componentes para garantir que a aplicação funcione corretamente quando diferentes partes estão interagindo.
7. **Testes de Requisições Assíncronas (se aplicável):**
   * Se a sua aplicação faz chamadas assíncronas (por exemplo, requisições API), use recursos do Jest como `async/await` e `mocks` para testar essas interações de forma controlada.
8. **Testes de Rotas (se aplicável):**
   * Se sua aplicação usa roteamento (por exemplo, com React Router), teste se as rotas estão funcionando conforme o esperado.
9. **Testes de Redução de Estado (se aplicável):**
   * Se você estiver usando algum estado global (por exemplo, Redux), teste as ações e os reducers para garantir que o estado seja manipulado corretamente.

   ## Como executar o Jest no SAPRON?
   * **Executando e visualizando os testes no terminal**

     Acione o script do jest para executar os testes . Use o seguinte comando dentro da pasta do front (sapron-frontend/legacy/):

     ```bash
      yarn test
     ```

   ## Padrão de código

   É importante para mantermos o padrão que os testes unitários sejam criados dentro de seus respectivos componentes de teste, seguindo o seguinte padrão de nomenclatura:

   > NomeDoComponente.test.tsx

   ## Testes já implementados no SAPRON

   ### 1. **Expenses - Duplicate Alert Component**
   - [x]  Deve renderizar o componente Alert e exibir as informações dentro dele
   - [x]  Deve existir a classe "unchecked" se a caixa de seleção não estiver marcada
   - [x]  Deve existir a classe "checked" se a caixa de seleção estiver marcada

   ### 2. **User Options - Request Support Button Component**
   - [x]  Deve exibir ícone e texto "Request error support"

   ### 3. **Financial Summary - Owner**
   - [x]  Deve renderizar Tooltip e exibir o texto dentro dele
   - [x]  Deve expandir o grid ao clicar no botão de expansão e exibir detalhes das reservas
   - [x]  Deve recolher o grid ao clicar no botão de recolhimento
   - [x]  Deve abrir o modal de reserva ao clicar no botão "Ver reserva" e exibir detalhes da reserva
   - [x]  Deve fechar o modal de reserva ao clicar no botão de fechar e ocultar os detalhes da reserva
   - [x]  Deve renderizar o ícone de informação de reserva se a reserva cobrir dois meses ou mais
   - [x]  Não deve renderizar o ícone de informação de reserva se a reserva cobrir apenas um mês
   - [x]  Deve validar o formato da data das reservas como "DD/MM/YYYY - DD/MM/YYYY"
   - [x]  Deve validar o formato da data das diárias como "DD/MM/YYYY"

   ### 4. **User Options - Request Support Modal Component**
   - [x]  Deve exibir ícone, título e botões no modal "Request error support"
   - [x]  Fecha o modal quando o botão de fechar é clicado
   - [x]  Fecha o modal quando o fundo é clicado
   - [x]  Redireciona para o relatório de bug quando o botão "Relatar erro" é clicado

   ### 5. **Financial Close - Manual Fit Property**
   - [x]  Deve renderizar a coluna "Ajuste Imóvel Proprietário" com ícone "+" e valor total correto com ícone de edição
   - [x]  Deve renderizar a cor padrão para ajuste manual igual a zero
   - [x]  Deve renderizar a cor verde para ajuste manual positivo
   - [x]  Deve renderizar a cor vermelho para ajuste manual negativo
   - [x]  Deve renderizar as labels corretas no modal de adição de ajuste manual
   - [x]  Deve renderizar as labels corretas no modal de edição de ajuste manual

   ### 6. **Financial Close - Manual Fit Host**
   - [x]  Deve renderizar a coluna "Ajuste Direto Anfitrião" com ícone "+" e valor total correto com ícone de edição
   - [x]  Deve renderizar a cor padrão para ajuste manual igual a zero
   - [x]  Deve renderizar a cor verde para ajuste manual positivo
   - [x]  Deve renderizar a cor vermelho para ajuste manual negativo
   - [x]  Deve renderizar as labels corretas no modal de adição de ajuste manual
   - [x]  Deve renderizar as labels corretas no modal de edição de ajuste manual