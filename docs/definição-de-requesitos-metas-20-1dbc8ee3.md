<!-- title: Definição de Requesitos Metas 2.0 | url: https://outline.seazone.com.br/doc/definicao-de-requesitos-metas-20-KkkZWbjhZS | area: Tecnologia -->

# Definição de Requesitos Metas 2.0

# Mapeamento de Problemas das Metas 1.0

## 1. **Complexidade dos Cálculos**

* Cálculo do Percentil 25 dos concorrentes: 
  * **Descrição do Problema:** O cálculo do faturamento dos concorrentes envolve a multiplicação do percentil 25 dos preços pela taxa de ocupação diária, agregando dia a dia até o fim do mês. Essa abordagem resulta em cálculos complexos e difíceis de entender e validar.
  * **Justificativa:**

     percentil 25 dos preços diários e então multiplicar pela taxa de ocupação diária (calculada por dia) deA complexidade do cálculo diário do faturamento dos concorrentes dificulta a identificação de erros e a validação dos resultados.
  * A lógica do cálculo não é intuitiva e requer um entendimento aprofundado de cada etapa para validar a sua corretude.
* **Exemplo:** A necessidade de calcular o todos os dias de um determinado mês torna o processo lento e dificulta a rastreabilidade das operações. Uma abordagem mais simples seria calcular o percentil do faturamento total do mês, ou pelo menos agregar os valores dos concorrentes e só entao aplicar o percentil.
  * **Sugestão de Melhoria:** Simplificar o cálculo do faturamento dos concorrentes utilizando um percentil representativo do faturamento mensal.


* A taxa de OTA
  * **Descrição do Problema:** A taxa de OTA é descontada diretamente nos dados dos concorrentes e poderia ser aplicada apenas nos dados da Seazone.
  * **Justificativa:**
    * Descontar a taxa de OTA nos concorrentes, a qual é adicionada em processamento no Lake, adiciona complexidade desnecessária ao processo, teriamos a analise de dados mais 'brutos' considerando OTA do Airbnb para todos.
  * **Sugestão de Melhoria:** Padronizar a aplicação da taxa de OTA, aplicando-a apenas aos dados dos imóveis da Seazone.

## 

## 

## 

##