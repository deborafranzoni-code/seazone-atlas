<!-- title: Padronização de Código - Equipe de Dados | url: https://outline.seazone.com.br/doc/padronizacao-de-codigo-equipe-de-dados-SKK21O79xE | area: Tecnologia -->

# Padronização de Código - Equipe de Dados

## 1. **Introdução**


Este documento tem como objetivo definir um guia de estilo para a equipe de dados da \[Nome da Startup\], visando promover a simplicidade, clareza e consistência em nosso código Python, SQL e Spark. Um código bem estruturado não apenas facilita a colaboração e manutenção, mas também contribui diretamente para a qualidade dos insights gerados e a eficiência das soluções implementadas.

Adotar estas práticas trará diversos benefícios, como:

* **Melhor legibilidade e compreensão do código:** Facilitando a colaboração entre membros da equipe, a revisão de código e a manutenção a longo prazo.
* **Redução de erros:** Código consistente e claro é menos propenso a erros e mais fácil de depurar.
* **Onboarding mais rápido para novos membros:** Um guia de estilo claro facilita a integração de novos membros à equipe, permitindo que eles rapidamente entendam e contribuam com o código existente.
* **Base para automação e ferramentas:** Um estilo consistente facilita a implementação de ferramentas de análise estática e formatação automática de código.

Este guia é um documento vivo e será atualizado periodicamente com base no feedback da equipe e na evolução das tecnologias que utilizamos.


## 2.  **Princípios Gerais**


1. **Legibilidade é Prioridade:** O código deve ser fácil de ler e entender por qualquer membro da equipe. Priorize a clareza sobre otimizações obscuras ou "esperteza".
2. **Princípio do Menor Surpresa:** O código deve se comportar de forma intuitiva e esperada. Evite construções complexas ou comportamentos inesperados.
3. **Seja Explícito e Evite Ambiguidade:** Deixe o código autoexplicativo. Evite abreviações excessivas ou jargões que possam não ser compreendidos por todos.
4. **Priorize a Clareza sobre a Concisão Extrema:** Embora a concisão seja desejável, a clareza e a legibilidade são mais importantes.
5. **DRY (Don't Repeat Yourself):** Evite duplicação de código. Reutilize funções e módulos sempre que possível.
6. **KISS (Keep It Simple, Stupid):** Mantenha o código simples e direto, evitando complexidade desnecessária.


## 3. **Nomenclatura e Convenções**


### **Linguagem**

* **Variáveis/Funções/Código em Geral:** Utilizar inglês para nomes de variáveis, funções, classes, módulos e código em geral.
* **Documentação Interna:** Utilizar português para comentários internos e documentação destinada à equipe, facilitando o entendimento.


### **Python**

* **Convenções:**
  * Usar `snake_case`  para variáveis, funções e nomes de módulos.
  * Usar `PascalCase`  para nomes de classes.
  * Seguir o padrão PEP 8 para formatação (espaçamento, quebra de linha, etc.).
  * Evitar nomes genéricos. Usar nomes descritivos e específicos.
  * Evite iniciar nomes de variáveis, funções ou colunas com palavras genéricas como `total`, `max`, `min`, `sum`, etc. Em vez disso, posicione essas palavras no final do nome para tornar o contexto mais claro e evitar duplicidade.

  **Exemplos de Nomenclatura Python:**

  \
  * **Variáveis:**
    * Ruim: `data` ,  `temp`, `total_sales`

      Bom: `user_data`,  `temporary_results` , `sales_total`

      \
  * **Funções:**
    * Ruim: `process()`, `calculate()`
    * Bom: `process_user_data()`, `calculate_total_sales()`
  * **Classes:**
    * Ruim: `Handler`, `Manager`
    * Bom: `ReportHandler`,  `OrderManager`
    * \
* **Dicas Importantes:**
  * Evite usar palavras reservadas ( `list`, `dict`,  etc.) como nomes de variáveis.
  * Prefira nomes descritivos que reflitam o propósito do objeto.


### **SQL**

* **Convenções:**
  * Keywords SQL em MAIÚSCULO (e.g., `SELECT`, `FROM`, `WHERE`, `JOIN`).
  * Nomes de tabelas e colunas em `snake_case`  e minúsculas.
  * Organizar colunas em linhas separadas na cláusula `SELECT`  para melhor legibilidade, especialmente quando há muitas colunas.
  * Incluir aliases curtos e significativos para tabelas e colunas, especialmente em queries complexas.
  * Usar referências explícitas a tabelas, incluindo o nome do banco de dados (e.g., `database_name.table_name.column_name`).

    \

  **Exemplo de Formatação SQL:**

  \

```sql
SELECT
    ua.user_id,
    ua.full_name,
    COUNT(DISTINCT od.order_id) AS total_orders
FROM
    real_estate_temp.active_users AS ua
JOIN
    real_estate_temp.order_details AS od
        ON ua.user_id = od.user_id
WHERE
    od.order_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
GROUP BY
    ua.user_id,
    ua.full_name
ORDER BY
    total_orders DESC;
```


## **4 . Ferramentas e Automação**

* **Black:** Formata automaticamente o código Python para garantir consistência visual.
* **Flake8:** Analisa o código para identificar problemas de estilo e conformidade com PEP 8.
* **isort:** Organiza as importações de forma automática e padronizada.
* **Pre-commit Hooks:** Automatizam a execução de Black, Flake8 e isort antes de cada commit, garantindo que o código esteja sempre formatado corretamente.

  \

## 5. **Estrutura e Organização do Código**


**Funções e Métodos**

* **Mantenha funções curtas e focadas em uma única responsabilidade.**
  * **Exemplo Ruim:** Uma função que processa dados, gera relatórios e salva arquivos

  \
  ```python
  def process_and_save_data(data):
  
      # Processa dados
      processed_data = [x * 2 for x in data]
  
      # Gera relatório
      report = f"Total: {sum(processed_data)}"
  
      # Salva arquivo
      with open("output.txt", "w") as f:
  
          f.write(report) 
  ```

  \
  * **Exemplo Bom:** Funções separadas para cada responsabilidade.

    \

```python
def process_data(data):
    return [x * 2 for x in data]

def generate_report(data):
    return f"Total: {sum(data)}"

def save_report(report, filename):
    with open(filename, "w") as f:
        f.write(report)
```


* **Use comentários breves (em português) para explicar a finalidade, argumentos e retorno**
  * **Exemplo:**

    \
    ```python
    def calculate_conversion_rate(total_users, active_users):
    
        """
        Calcula a taxa de conversão de usuários ativos.
        Args:
            users_total (int): Número total de usuários.
            users_actives (int): Número de usuários ativos.
        Returns:
            float: Taxa de conversão em porcentagem.
        """
    
        return (active_users / total_users) * 100
    ```
* **Funções longas e complexas devem ser refatoradas em funções menores e mais gerenciáveis.**


\
## 6. **Processos de Revisão de Código (Code Review)**

* Não refatorar código se esta fazendo uma feature
* Fazer um PR para cada topico
* Pensar em padronizar Commit. 

 

## 7.  **Considerações Finais**


Este guia de estilo é um documento vivo e será atualizado periodicamente com base no feedback da equipe e na evolução das tecnologias utilizadas. Sua colaboração é essencial para mantê-lo relevante e eficaz. Caso tenha sugestões ou dúvidas, compartilhe-as com a equipe de liderança técnica.


\
## Próximos Passos

* Criar bibliotecas de funções reutilizáveis; 
* Padronizar e utilizar ferramentas de automação; ( Pre-commit hooks, Balck, Flake8 )
* Pensar em padronização de PR 

Não refatorar código se esta fazendo uma feature

Fazer um PR para cada topico

Pensar em padronizar Commit.