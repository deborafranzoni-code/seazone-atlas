<!-- title: MVP Gestão de Preços Especiais (Sirius) | url: https://outline.seazone.com.br/doc/mvp-gestao-de-precos-especiais-sirius-KSD3DtIh8H | area: Tecnologia -->

# MVP Gestão de Preços Especiais (Sirius)

## **1. Visão Geral**

**Objetivo:** Substituir a aba "Preços Especiais" da planilha por uma UI web funcional e integrada ao backend existente (Sirius/Lake). **Escopo do MVP:** Interface completa para Consulta, Inserção, Edição e Exclusão de regras, conectada em tempo real à base de dados atual.

## **2. Requisitos de Implementação Técnica (Obrigatório)**

### **2.1. Conexão com Dados Reais (Sem Mocks)**

* **Frontend:** A aplicação deve ser construída conectando-se diretamente aos endpoints existentes do sistema Sirius.
* **Sem Dados Falsos:** O desenvolvedor **não deve** utilizar dados simulados (mocks) para popular as tabelas. A UI deve exibir os dados reais da tabela do Lake desde o primeiro deploy.
* **Fonte de Dados:** Consumir a mesma fonte que a planilha/aba atual utiliza.

### **2.2. Persistência e Integração com Lake**

* **Ação de Escrita:** Ao clicar em "Salvar" (em uma nova regra ou edição), o sistema deve realizar um `**POST/PUT**` para a API do Sirius, atualizando a tabela do Lake imediatamente.
* **Sincronização:** A lista de regras na UI deve refletir instantaneamente a alteração feita (refresh automático ou atualização do estado local).
* **Feedback ao Usuário:** Enquanto a requisição estiver em andamento, exibir estado de "Loading". Se falhar, exibir mensagem de erro clara.

### **2.3. Segurança e Auditoria (Logs)**

* **Autenticação:** Acesso restrito a e-mails `**@seazone.com.br**`.
* **Rastreamento (Audit Log):** Toda operação de escrita (CREATE, UPDATE, DELETE) deve enviar automaticamente o ID do usuário logado e o timestamp para o Lake, garantindo a rastreabilidade de quem fez a alteração.

## **3. Requisitos Funcionais da UI**

### **3.1. Tela de Gestão (Listagem e CRUD)**

* **Listagem:** Exibir as regras existentes na tabela do Lake.
* **Filtros Obrigatórios:** Imóvel, Categoria, Intervalo de Datas, Região, Polígono (para facilitar a carga de dados pesada).
* **Ações:**
  * **Nova Regra:** Botão que abre formulário para inserção.
  * **Editar:** Altera dados de uma linha existente.
  * **Excluir:** Remove a regra do Lake.

### **3.2. Tela "Raio-X" (Visualização de Conflitos)**

* **Lógica:** O sistema deve calcular localmente (client-side) ou via endpoint a precedência de regras para o Imóvel/Data selecionado.
* **Visualização:** Mostrar qual regra está valendo (vencedora) e quais foram sobrepostas (ignoradas), seguindo a lógica de hierarquia (Nível > Tipo) e a flag "Ignorar Hierarquia".


---

## **4. Guia de "Vibe Coding" para o Dev (Ajustado para Integração Real)**

O objetivo aqui é usar a IA para acelerar a criação dos componentes visuais e a lógica de consumo da API.

### **Passo 1: Gerar a UI com dados dinâmicos (Lovable)**

O foco é pedir para o Lovable criar a **estrutura** que aceita os dados reais.

> **Prompt Lovable:** "Crie uma aplicação React para 'Gestão de Preços Especiais' com foco em integração imediata com API.
>
> **Funcionalidades:**
>
> 
> 1. **Header:** Título e botão 'Nova Regra'.
> 2. **Painel Raio-X:** Seção para simular regras (Input Imóvel + Date Picker). Deve mostrar visualmente qual regra vence (ex: Card Verde) e quais foram ignoradas (Card Cinza).
> 3. **Tabela de Dados:** Uma tabela robusta com colunas para Grupo, Data, Valor, Tipo, Nível e Ações (Editar/Excluir).
> 4. **Formulário (Modal):** Campos para criar/editar regra.
>
> **Requisito Técnico:** Use variáveis de estado (useState) para carregar dados de uma função `**fetchRules()**` (simule a chamada mas deixe pronto para trocar pela URL real da API). A estrutura deve estar pronta para receber dados reais via props ou contexto."

### **Passo 2: Lógica de Hierarquia e Cálculo (Claude)**

Pedir para o Claude gerar a função pura que o Front vai usar para decidir quem vence no "Raio-X".

> **Prompt Claude:** "Escreva uma função em TypeScript `**resolveHierarchy(rules: Rule\[\]): Rule**` que determine a regra vencedora.
>
> **Regras:**
>
> 
> 1. Prioridade de Nível: Imóvel (0) > Categoria (1) > Região.
> 2. Prioridade de Tipo: Fixo > Mínimo/Máximo.
> 3. Exceção: Se flag `**ignoreHierarchy**` for true, o nível inferior pode vencer.
>
> A função deve retornar a regra vencedora e indicar as perdedoras."

### **Passo 3: Conexão com o Backend (Dev + IA)**

O Dev deve usar a IA para gerar o código de integração ("boilerplate") das funções geradas no Passo 1 com os endpoints reais do Sirius.

> **Prompt Claude:** "Tenho um endpoint GET `**https://api.sirius.com.br/prices**` e preciso conectar no meu componente React Table. Gere o hook `**useFetchPrices**` usando React Query ou useEffect. O retorno precisa tipar os dados conforme o JSON que a API entrega."