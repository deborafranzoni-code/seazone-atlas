<!-- title: BI VivaReal - Análise de Valorização Imobiliária (ROI) | url: https://outline.seazone.com.br/doc/bi-vivareal-analise-de-valorizacao-imobiliaria-roi-mLrYm4gLmb | area: Tecnologia -->

# BI VivaReal - Análise de Valorização Imobiliária (ROI)

### **1. Visão Geral**

* **Objetivo:** Automatizar o cálculo da valorização do metro quadrado (m²) de imóveis por região, substituindo o processo manual atual em planilhas.
* **Problema:** O processo manual é demorado, não escalável e propenso a erros. A consulta a dados brutos na nuvem é custosa.
* **Solução:** Criar uma nova aba no BI que permita ao usuário aplicar filtros dinâmicos e obter, de forma instantânea, a média de valor do m² por ano, além de métricas de qualidade para validar a análise.

### **2. Dados de Entrada (Fonte de Dados)**

 A coluna `**Data da última aquisição**` é a referência temporal principal.

| **Nome da Coluna** | **Tipo de Dado** | **Descrição / Uso na Análise** |
|----|----|----|
| `**Id do anúncio**` | Texto / Número | **Identificador único.** Usado para deduplicação. |
| `**Valor da unidade**` | Numérico | Valor total do imóvel. |
| `**Tamanho**` | Numérico | Área útil em m². |
| `**Número de quartos**` | Número Inteiro | Quantidade de quartos do imóvel. |
| `**Cidade**` | Texto | Usado para filtro de localização. |
| `**Bairro**` | Texto | Usado para filtro de localização (nível mais granular). |
| `**Data da última aquisição**` | Data | **Data chave.** Define o ano do imóvel para a análise e a deduplicação. |
| `**Valor do m²**` | Numérico | **Valor principal para o cálculo.** (Valor da unidade / Tamanho). |


### **3. Lógica de Processamento e Cálculo (Backend)**

Esta é a sequência de passos que o sistema deve executar sempre que os filtros forem aplicados ou alterados.


1. **Aplicar Filtros do Usuário:**
   * Filtrar a tabela base por `**Cidade**` e/ou `**Bairro**`.
   * Filtrar por `**Tamanho**` (ex: `**Tamanho <= 35**`).
   * Filtrar por `**Número de quartos**` (ex: `**Número de quartos == 1**`).
2. **Deduplicação:**
   * Após os filtros iniciais, agrupar os dados por `**Id do anúncio**`.
   * Para cada anúncio, **manter apenas a linha com a** `**Data da última aquisição**` **mais recente**. Isso garante que estamos trabalhando com o último valor conhecido de cada imóvel.
3. **Identificação e Remoção de Outliers:**
   * Com o conjunto de dados deduplicado, calcular os percentis do `**Valor do m²**`:
     * **1º Quartil (Q1):** Valor que separa os 25% mais baixos.
     * **3º Quartil (Q3):** Valor que separa os 25% mais altos.
   * **Definir o intervalo válido:** Considerar apenas os imóveis cujo `**Valor do m²**` seja **maior que Q1 e menor ou igual a Q3**.
   * **Isolar Outliers:** Os imóveis fora desse intervalo são considerados outliers. Eles devem ser contabilizados, mas **não** entrar no cálculo da média final.
4. **Cálculo Final por Ano:**
   * Com os dados já filtrados e sem outliers, agrupar os registros pelo **ano** extraído da coluna `**Data da última aquisição**`.
   * Para cada ano, calcular a **média aritmética** do `**Valor do m²**`.
   * O resultado é a tabela de valorização.

### **4. Saída Esperada (Frontend / Interface)**

A interface deve ser dividida em duas áreas principais: Controles e Resultados.

**1. Painel de Controle (Filtros)**

* **Seleção de Localidade:** Dropdown para `**Cidade**` e `**Bairro**`.
* **Filtros Numéricos (Inputs):**
  * `**Tamanho máximo (m²):**` Campo para o usuário digitar um valor.
  * `**Número de quartos:**` Campo para selecionar um número.
* **Ação:** Um botão "Aplicar Filtros" ou a atualização automática ao alterar um filtro.

**4.2. Área de Resultados**

* **Tabela Principal: Valorização do Mercado**
  * Deve seguir exatamente este formato, sendo atualizada dinamicamente com os filtros.

| **Item/Ano** | **2021** | **2022** | **2023** | **2024** |
|----|----|----|----|----|
| **Valor do m²** | R$ X.XXX,XX | R$ X.XXX,XX | R$ X.XXX,XX | R$ X.XXX,XX |

* **Painel de Qualidade dos Dados (Essencial para Validação)**
  * **Quantidade de Listings Utilizados:** Mostrar o total de imóveis que entraram no cálculo (após remoção de outliers).
  * **Quantidade de Outliers Removidos:** Mostrar quantos imóveis foram descartados no passo 3.
  * **Desvio Padrão (por ano):** Exibir o desvio padrão do `**Valor do m²**` para cada ano, dando uma noção da variabilidade dos dados.
  * **Tabela Detalhada (Opcional, mas recomendado):** Um botão "Ver Detalhes" que abre uma tabela com os listings que foram **efetivamente utilizados** no cálculo, mostrando colunas como: `**Id do anúncio**`, `**Bairro**`, `**Valor da unidade**`, `**Tamanho**`, `**Valor do m²**` e `**Data da última aquisição**`.

**5. Definição de "Pronto" (Definition of Done)**

A funcionalidade estará pronta quando:


1. O BI consumir a tabela de dados de entrada.
2. O usuário conseguir selecionar uma região (ex: Ingleses do Rio Vermelho) e aplicar filtros (ex: Tamanho até 45m², 1 quarto).
3. A **Tabela Principal** exibir os valores médios do m² por ano calculados corretamente.
4. O **Painel de Qualidade** mostrar a quantidade de listings, outliers e o desvio padrão correspondentes à seleção.
5. Os resultados forem validados contra uma análise manual feita em planilha para garantir a precisão da lógica