<!-- title: Funcão_Register_expenses | url: https://outline.seazone.com.br/doc/funcao_register_expenses-RhCgt8bdgn | area: Tecnologia -->

# Funcão_Register_expenses

Analisando a função `Register_expenses` que impacta na Tabela `Financial_expenses`

### **Logica a considerar**

Pontos de atenção para identificar variáveis e dados a serem considerados


1. **Gatilho (Trigger):** A função é acionada por operações (INSERT, UPDATE, DELETE) na tabela financial_expenses.

   \
2. **Variáveis Principais:** A lógica depende crucialmente dos seguintes campos de financial_expenses:
   * expense_status: Deve ser 'Approved' para a maioria das ações.
   * paid_by: Define quem pagou a despesa ('Owner', 'Host', 'Seazone'). Determina a tabela de débito (closing_property_resume, closing_host_resume, closing_seazone_resume).
   * received_by: Define quem recebeu o valor ('Owner', 'Host', 'Seazone'). Determina a tabela de crédito/reembolso.
   * property_id: Essencial para associar a despesa a uma propriedade.
   * reason: Exclui a criação de registros de reembolso se começar com Account_ ou for Seazone_Charges.
   * register_date e approval_date: Usados para determinar a ac_date (data de competência).
   * value: O valor da despesa. Inserções são ignoradas se o valor for zero.

     \
3. **Lógica de Data (ac_date):**
   * Se register_date for de 2023 ou anterior, usa-se register_date.
   * Se register_date for de 2024 ou posterior, usa-se approval_date. Se approval_date for nulo, usa-se register_date.

     \
4. **Ações Principais:**
   * **Caminho de Limpeza/Deleção:** Se a operação for DELETE ou se expense_status não for 'Approved', ou se paid_by, received_by, ou property_id forem nulos, a função **deleta** quaisquer registros correspondentes das tabelas closing_\*_resume.
   * **Caminho de Processamento:** Se as condições acima não forem atendidas, a função:

     
     1. Cria/Atualiza um registro de **débito** (debited_expense) na tabela closing_\*_resume correspondente a paid_by.
     2. Cria/Atualiza um registro de **crédito/reembolso** (refund_expense) na tabela closing_\*_resume correspondente a received_by, **a menos que** a reason seja uma exceção.


---

### Análise de variáveis para Pairwise

| **ID** | **Parâmetro** | **Valores (e contagem)** |    |
|----|----|----|----|
| C1 | **Operação** | INSERT, UPDATE (2) |    |
| C2 | **Status** | Approved, Not_Approved (2) \*\*OBS validar (Not_Approved= Pending, Canceled) |    |
| C3 | **Pagador** | Owner, Host, Seazone, NULL (4) |    |
| C4 | **Recebedor** | Owner, Host, Seazone, NULL (4) |    |
| C5 | **Propriedade** | Valid, NULL (2) |    |
| C6 | **Motivo** | Standard, Exception (2) |    |
| C7 | **Valor** | > 0, = 0 (2) |    |
| C8 | **Regra da Data** | Legacy (<=23), Modern (+Approval), Modern (-Approval) (3) |    |

**Exceção de Lógica:** A operação DELETE tem um comportamento único que anula a relevância dos outros parâmetros. Ela sempre aciona o caminho de limpeza. Portanto, é mais eficaz testá-la em um cenário separado e focado, em vez de incluí-la na geração pairwise, o que criaria casos de teste redundantes ou ilógicos.


---

### Caso de Teste Específico (Não Pairwise)

Este caso cobre a lógica que tem precedência sobre todas as outras.

| **ID do Teste** | **Operação** | **Pré-condição** | **Resultado Esperado (Efeito)** |
|----|----|----|----|
| **TC-DEL-01** | DELETE | Uma despesa processada (Approved) existe, com registros de débito e crédito nas tabelas closing_\*_resume. | A função é acionada. **Todos os registros** associados a source_id da despesa nas tabelas closing_property_resume, closing_host_resume e closing_seazone_resume são **deletados**. |


---

### Conjunto de Casos de Teste ( Pairwise Testing )

O conjunto a seguir foi gerado para cobrir todas as interações de pares dos parâmetros C1 a C8. O total de combinações possíveis seria 2 \* 2 \* 4 \* 4 \* 2 \* 2 \* 2 \* 3 = **1.536 testes**. A técnica de pairwise reduz isso para apenas **13 testes**, mantendo uma excelente cobertura das interações.

| **ID do Teste** | **Operação (C1)** | **Status (C2)** | **Pagador (C3)** | **Recebedor (C4)** | **Propriedade (C5)** | **Motivo (C6)** | **Valor (C7)** | **Regra da Data (C8)** | **Resultado Esperado (Efeito)** |
|----|----|----|----|----|----|----|----|----|----|
| **TC-PW-01** | INSERT | Approved | Owner | Owner | Valid | Standard | > 0 | Legacy (<=23) | **Sucesso:** Débito criado em closing_property_resume e Crédito criado em closing_property_resume. accrual_date = register_date. |
| **TC-PW-02** | UPDATE | Approved | Owner | Host | NULL | Exception | = 0 | Modern (+Approval) | **Limpeza:** A função entra no caminho de limpeza porque property_id é NULL. Registros existentes são deletados. |
| **TC-PW-03** | INSERT | Approved | Host | Seazone | Valid | Exception | > 0 | Modern (-Approval) | **Débito Parcial:** Débito criado em closing_host_resume. Bloco de crédito é ignorado devido ao Motivo (Exception). accrual_date = register_date (fallback). |
| **TC-PW-04** | UPDATE | Approved | Host | NULL | Valid | Standard | > 0 | Legacy (<=23) | **Limpeza:** A função entra no caminho de limpeza porque received_by é NULL. Registros existentes são deletados. |
| **TC-PW-05** | INSERT | Not_Approved | Seazone | Owner | Valid | Standard | > 0 | Modern (+Approval) | **Limpeza:** A função entra no caminho de limpeza porque o Status é Not_Approved. Nenhum registro é criado. |
| **TC-PW-06** | UPDATE | Not_Approved | Seazone | Host | Valid | Exception | = 0 | Modern (-Approval) | **Limpeza:** A função entra no caminho de limpeza porque o Status é Not_Approved. Registros existentes são deletados. |
| **TC-PW-07** | INSERT | Not_Approved | NULL | Seazone | NULL | Standard | > 0 | Legacy (<=23) | **Limpeza:** A função entra no caminho de limpeza (múltiplas razões: Not_Approved, Pagador é NULL, Propriedade é NULL). |
| **TC-PW-08** | UPDATE | Not_Approved | NULL | NULL | Valid | Exception | > 0 | Modern (+Approval) | **Limpeza:** A função entra no caminho de limpeza (múltiplas razões). Registros existentes são deletados. |
| **TC-PW-09** | INSERT | Approved | Seazone | Seazone | NULL | Standard | > 0 | Legacy (<=23) | **Limpeza:** A função entra no caminho de limpeza porque property_id é NULL. Nenhum registro é criado. |
| **TC-PW-10** | UPDATE | Approved | NULL | Owner | Valid | Standard | > 0 | Modern (-Approval) | **Limpeza:** A função entra no caminho de limpeza porque paid_by é NULL. Registros existentes são deletados. |
| **TC-PW-11** | INSERT | Approved | Host | Host | Valid | Standard | = 0 | Modern (+Approval) | **Sem Ação (Valor 0):** A função processa, mas o INSERT nas tabelas closing é pulado pela condição if valor_despesa > 0. |
| **TC-PW-12** | UPDATE | Approved | Owner | Seazone | Valid | Standard | > 0 | Modern (-Approval) | **Sucesso (Update):** Débito em closing_property_resume e Crédito em closing_seazone_resume são **atualizados**. accrual_date = register_date (fallback). |
| **TC-PW-13** | INSERT | Approved | Seazone | Host | Valid | Standard | > 0 | Modern (+Approval) | **Sucesso:** Débito criado em closing_seazone_resume e Crédito em closing_host_resume. accrual_date = approval_date. |

[Planilha](https://docs.google.com/spreadsheets/d/1NbAOpYfpJYpcltqSYXZmAHSHc_YlsuQ-1wvNsiZ8N3k/edit?usp=sharing) para Acompanhar a Execução dos testes - 

[https://docs.google.com/spreadsheets/d/1NbAOpYfpJYpcltqSYXZmAHSHc%5FYlsuQ-1wvNsiZ8N3k/edit?usp=sharing](https://docs.google.com/spreadsheets/d/1NbAOpYfpJYpcltqSYXZmAHSHc%5FYlsuQ-1wvNsiZ8N3k/edit?usp=sharing)


\


| **ID do Teste** | **Operação (C1)** | **Status (C2)** | **Pagador (C3)** | **Recebedor (C4)** | **Propriedade (C5)** | **Motivo (C6)** | **Valor (C7)** | **Regra da Data (C8)** | **Resultado Esperado (Efeito)** |
|----|----|----|----|----|----|----|----|----|----|
| **TC-PW-F-01** | INSERT | Approved | Owner | Host | Valid | Standard | > 0 | Legacy (<=23) | **Sucesso:** Débito criado em closing_property_resume e Crédito criado em closing_host_resume. accrual_date = register_date. |
| **TC-PW-F-02** | UPDATE | Approved | Host | Seazone | Valid | Exception | = 0 | Modern (+Approval) | **Débito Parcial (Update):** Débito em closing_host_resume é atualizado (para valor 0). Bloco de crédito é ignorado/deletado devido ao Motivo Exception. |
| **TC-PW-F-03** | INSERT | Approved | Seazone | Owner | NULL | Standard | > 0 | Modern (-Approval) | **Limpeza:** A função entra no caminho de limpeza porque Propriedade é NULL. Nenhum registro é criado. |
| **TC-PW-F-04** | UPDATE | Approved | NULL | Host | Valid | Standard | > 0 | Legacy (<=23) | **Limpeza:** A função entra no caminho de limpeza porque Pagador é NULL. Registros existentes são deletados. |
| **TC-PW-F-05** | INSERT | Pending | Owner | Seazone | Valid | Standard | > 0 | Modern (+Approval) | **Limpeza:** A função entra no caminho de limpeza porque o Status é Pending. Nenhum registro é criado. |
| **TC-PW-F-06** | UPDATE | Pending | Host | Owner | NULL | Exception | > 0 | Modern (-Approval) | **Limpeza:** A função entra no caminho de limpeza por múltiplas razões (Status Pending, Propriedade NULL). Registros existentes são deletados. |
| **TC-PW-F-07** | INSERT | Canceled | Seazone | Host | Valid | Exception | > 0 | Legacy (<=23) | **Limpeza:** A função entra no caminho de limpeza porque o Status é Canceled. Nenhum registro é criado. |
| **TC-PW-F-08** | UPDATE | Canceled | Owner | Host | Valid | Standard | = 0 | Modern (+Approval) | **Limpeza:** A função entra no caminho de limpeza porque o Status é Canceled. Registros existentes são deletados. |
| **TC-PW-F-09** | INSERT | Approved | Host | Owner | Valid | Standard | = 0 | Modern (-Approval) | **Sem Ação (Valor 0):** A função processa, mas a criação de registros é pulada pela condição if valor_despesa > 0. |
| **TC-PW-F-10** | UPDATE | Approved | Seazone | NULL | Valid | Standard | > 0 | Modern (-Approval) | **Limpeza:** A função entra no caminho de limpeza porque Recebedor é NULL. Registros existentes são deletados. |
| **TC-PW-F-11** | INSERT | Approved | Owner | NULL | NULL | Exception | > 0 | Modern (+Approval) | **Limpeza:** A função entra no caminho de limpeza por múltiplas razões (Recebedor e Propriedade são NULL). |
| **TC-PW-F-12** | UPDATE | Approved | Seazone | Owner | Valid | Standard | > 0 | Legacy (<=23) | **Sucesso (Update):** Débito em closing_seazone_resume e Crédito em closing_property_resume são atualizados. accrual_date = register_date. |
| **TC-PW-F-13** | INSERT | Approved | Owner | Seazone | Valid | Standard | > 0 | Modern (+Approval) | **Sucesso:** Débito criado em closing_property_resume e Crédito em closing_seazone_resume. accrual_date = approval_date. |