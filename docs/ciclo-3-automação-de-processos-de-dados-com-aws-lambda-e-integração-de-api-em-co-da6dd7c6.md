<!-- title: Ciclo 3: Automação de Processos de Dados com AWS Lambda e Integração de API( EM CONTRUÇÃO) | url: https://outline.seazone.com.br/doc/ciclo-3-automacao-de-processos-de-dados-com-aws-lambda-e-integracao-de-api-em-contrucao-dfMaEyJKtg | area: Tecnologia -->

# Ciclo 3: Automação de Processos de Dados com AWS Lambda e Integração de API( EM CONTRUÇÃO)

# **Aula Introdutória (1 hora):**

* **Introdução ao AWS Lambda:**
  * Conceitos de computação serverless.
  * Criação e implantação de funções Lambda
* **Introdução ao IAM roles:**
  * Criação da role do Lambda
* **Configuração do API Gateway:**
  * Criação de endpoints RESTful.
  * Integração com Lambda.
  * Limites e quotas
* **Integração com Google Sheets:**
  * Conectando APIs ao Google Sheets.
  * Atualização automática de dados.
* **Automatizando Consultas e Processamentos:**
  * Uso de scripts Python para automatizar tarefas.
* **CI/CD com GitHub:**
  * Conceitos de integração contínua e entrega contínua.
  * Configuração de pipelines de deployment.
* **Uso do Git e GitHub:**
  * Controle de versão.
  * Boas práticas de commits e branches.

**Ferramentas:**

* AWS Athena
* VS Code
* ChatGPT
* Python
* Jupyter Notebook
* AWS Lambda
* API Gateway
* CI/CD - GitHub

**Objetivos de Aprendizado:**

* Conectar-se à AWS via VS Code.
* Manipular dados da Camada Enriched.
* Praticar SQL no Athena.
* Automatizar consultas e manipulação de dados com Lambda.
* Criar um endpoint acessível com o API Gateway.
* Integrar dados da AWS ao Google Sheets.
* Utilizar Git e GitHub para controle de versão e CI/CD.

# DESAFIO:

**Desafio:**

**Contexto:**

A empresa busca otimizar o fluxo de informações e necessita de um sistema automatizado que forneça dados atualizados em tempo real para auxiliar na tomada de decisões estratégicas.

**Contexto:**

O RM gostaria de ter uma aba explicando quais regras foram usadas para alterar o preço de um imóvel ou grupo de imóveis.

É necessário criar uma API que recebe de parametros um imóvel (JBV108) ou grupo de imóvels (Especial-JBV), um periodo de datas (pode ser um start_date e end_date) e retorne algo no seguinte formato, preço enviado, preço final e todas as regras usadas em cada dia.

| id_seazone | date | min_stay | preço enviado | preço final | preço mínimo | increment_agc | … |
|----|----|----|----|----|----|----|----|
| JBV108 | 2024-01-01 | 2 | 100 | 120 | 120 | 0 | … |
| JBV108 | 2024-01-02 | 2 | 150 | 150 | 120 | 0 | … |

No final, é necessário criar uma planilha que rode um AppScript, ele lê os parametros, envia para a API, lê o resultado e atualizada a aba da Planilha.

**Tarefa:**


1. Explorar os dados (no Athena mesmo)

   
   1. Explorar a view last_offered_raw_price (database pricingdata). Ela tem as informações das tabelas de preço ANTES de aplicar as mudanças de preço da setup.
   2. Explorar a view last_offered_price (database pricingdata). Ela tem as informações das tabelas de preço DEPOIS de aplicar as mudanças de preço da setup.
   3. Explorar a tabela setup_groups (database inputdata). Ela relaciona quais imóveis estão em quais grupos.
2. Criar recursos sem o CI/CD (Opcional)

   
   1. Se achar mais fácil criar os recusos primeiro pela AWS e só depois passar pelo CI/CD, fique a vontate.
   2. **Desenvolver uma Função Lambda.**

      
      1. Ela recebe de parametros um imóvel ou grupo de imóveis e um intervalo de datas
      2. Faz as respectivas quereis no Athena/manipulações em panadas para alcançar o formato da tabela final.

         
         1. Como as tabelas de preço estão em outro repositório, tu precisa descobrir qual o nome exato do database. Exemplo de script do repositorio [api-stays](https://github.com/seazone-tech/api-stays) que faz isso: [daily_revenue](https://github.com/seazone-tech/api-stays/tree/dev/sapron_communication/process/daily_revenue).
      3. Retorna um json da tabela final.
   3. **Configurar o API Gateway:**

      
      1. Criar um endpoint POST que trigga o lambda
      2. Esse endpoint deve precisar duma API key
3. **Implementar CI/CD com GitHub:**
   * Criar uma branch de feature nova no repositório [api-stays](https://github.com/seazone-tech/api-stays).
   * Criar a role do lambda no iam-roles.
   * Adicionar os recursos do passo 2 e 3 nessa branch.
   * Subir para AWS e testar.
4. **Integrar com o Google Sheets:**

   
   1. Criar uma cópia da [\[S2.0\] \[DEV\] Planilha de Setup](https://docs.google.com/spreadsheets/d/1Px1rW8jTy7UqcUmHUNE7uGMUUAWzYQvt3zPErk4glJI/edit?gid=2135658376#gid=2135658376), mas dar o nome de \[S2.0\] \[TEST\] Planilha de Setup.
   2. Criar uma aba nova onde o usuário pode fornecer os parametros e clicar num botão "Executar"
   3. Executar o AppScript e faze-lo triggar a API e retornar na mesma aba ou uma aba nova as informações.
5. **Entrega:**

**Entrega Esperada:**

* PR para dev no respositório do api-stays
* Planilha de TEST da setup funcionando e integrada com o API gateway criada na branch