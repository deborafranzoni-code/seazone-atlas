<!-- title: Função_register_cleaning_fee_manual_fit | url: https://outline.seazone.com.br/doc/funcao_register_cleaning_fee_manual_fit-tPLvGQRHvs | area: Tecnologia -->

# Função_register_cleaning_fee_manual_fit

## **Análise da Lógica da Função**


1. **Evento do Gatilho:** A função é acionada por operações de INSERT, UPDATE ou DELETE (implícito pelo uso de TG_OP e OLD/NEW) na tabela financial_cleaning_fee_manual_fit.

   \
2. **Limpeza (Idempotência):** A primeira ação da função é sempre **excluir** registros existentes nas tabelas closing_host_resume e closing_seazone_resume que correspondam à reserva (reservation_id) em questão. Isso garante que, não importa quantas vezes o gatilho seja disparado para a mesma reserva, não haverá dados duplicados.

   \
3. **Coleta de Dados (Cursor):** A função usa um cursor (clean_cursor) para buscar **todos** os registros de ajuste manual para a reserva (res_id). O cursor tem filtros importantes:
   * A reserva deve ter o status  (Validos)  'Concluded' ou 'No-Show' e (Invalidos) 
   * A reserva **não** pode ser de bloqueio (is_blocking is false).

   \
4. **Cálculo da Data de Caixa (cash_date):** A data de pagamento (cash_date) é calculada com base na configuração da OTA (reservation_ota_setup):
   * Se payment_delay for 0, cash_date é a mesma que date_ref.
   * Se payment_delay for diferente de 0, cash_date é date_ref mais um mês.

     \
5. **Lógica de Inserção:** Para cada registro encontrado pelo cursor, a função faz o seguinte:
   * Verifica o campo is_adding:
     * Se true: É um ajuste a favor do anfitrião.
       * **Host:** input (entrada de dinheiro).
       * **Seazone:** output (saída de dinheiro).
     * Se false: É um ajuste a favor da Seazone (ou uma cobrança do anfitrião).
       * **Host:** output (saída de dinheiro).
       * **Seazone:** input (entrada de dinheiro).
   * Insere um novo registro em closing_host_resume.
   * Insere um novo registro em closing_seazone_resume.

## **Pré-requisitos para os Testes (Setup)**


* reservation_reservation (rr)
* reservation_ota_setup (ros)
* financial_cleaning_fee_manual_fit (fcfmf) - *Esta é a tabela onde o gatilho está aplicado.*
* closing_host_resume - *Para verificar os resultados.*
* closing_seazone_resume - *Para verificar os resultados.*


\
## Identificar os Parâmetros e Seus Valores

Primeiro, extraímos os parâmetros (fatores) da análise da função e listamos seus possíveis valores (níveis). Parâmetro (Fator)	Valores (Níveis)	Descrição


1. Operação do Gatilho (TG_OP)	INSERT, UPDATE, DELETE	O tipo de comando DML que aciona a função.
2. Tipo de Ajuste (is_adding)	true, false, N/A	Se o valor é adicionado ou subtraído. N/A se aplica ao DELETE.
3. Status da Reserva	Válido (Concluded/No-Show), Inválido (Outro)	Condição para o cursor processar o registro.
4. Reserva de Bloqueio (is_blocking)	false (Não é bloqueio), true (É bloqueio)	Outra condição do cursor.
5. Atraso no Pagamento (payment_delay)	0 (Sem atraso), > 0 (Com atraso)	Condição que afeta o cálculo da cash_date. Análise Combinatória: O teste exaustivo (testar todas as combinações) exigiria: 3 (Operação) \* 2 (Tipo Ajuste) \* 2 (Status) \* 2 (Bloqueio) \* 2 (Atraso) = 48 casos de teste (sem contar as restrições). Com o Pairwise Testing, podemos reduzir esse número para algo em torno de 8 a 10 casos de teste, garantindo que cada par de valores (ex: UPDATE com Status Inválido, is_adding=true com is_blocking=true, etc.) seja coberto. Passo 2: Gerar os Casos de Teste Pairwise


## Cenários de teste identificados

### **Cenário 1: "Caminho Feliz" - Inserção de um Ajuste Positivo (Adição)**

* **Objetivo:** Validar o fluxo padrão para um novo ajuste que adiciona valor ao anfitrião.
* **Pré-condições (Setup):**

  
  1. Crie uma reserva na reservation_reservation com id = 100, status = 'Concluded', is_blocking = false, e ota_id = 1.
  2. Crie uma configuração na reservation_ota_setup com ota_id = 1 e payment_delay = 0.
* **Ação (Action):**
  * Execute um INSERT na tabela financial_cleaning_fee_manual_fit:

    **Generated sql**

    ```javascript
    INSERT INTO financial_cleaning_fee_manual_fit (reservation_id, date_ref, value, description, is_adding) 
    VALUES (100, '2023-10-26', 50.00, 'Ajuste positivo manual', true);
    ```

    Use code **[with caution](https://support.google.com/legal/answer/13505487)**.SQL
* **Resultados Esperados (Expected Outcome):**

  
  1. Um novo registro deve ser criado em closing_host_resume com:
     * reservation_id = 100
     * value = 50.00
     * transfer_type = 'input'
     * transfer_category = 'cleaning_manual_fit'
     * cash_date = '2023-10-26' (pois payment_delay é 0).
  2. Um novo registro deve ser criado em closing_seazone_resume com:
     * reservation_id = 100
     * value = 50.00
     * transfer_type = 'output'
     * transfer_category = 'cleaning_manual_fit'
     * cash_date = '2023-10-26'.


---

#### **Cenário 2: Inserção de um Ajuste Negativo (Subtração)**

* **Objetivo:** Validar o fluxo para um ajuste que remove valor do anfitrião (is_adding = false).
* **Pré-condições (Setup):**
  * Mesmas do Cenário 1.
* **Ação (Action):**
  * Execute um INSERT na tabela financial_cleaning_fee_manual_fit:

    **Generated sql**

    ```javascript
    INSERT INTO financial_cleaning_fee_manual_fit (reservation_id, date_ref, value, description, is_adding) 
    VALUES (100, '2023-10-26', 25.00, 'Cobrança extra de limpeza', false);
    ```

    Use code **[with caution](https://support.google.com/legal/answer/13505487)**.SQL
* **Resultados Esperados (Expected Outcome):**

  
  1. Um novo registro deve ser criado em closing_host_resume com:
     * transfer_type = 'output'
     * value = 25.00
  2. Um novo registro deve ser criado em closing_seazone_resume com:
     * transfer_type = 'input'
     * value = 25.00


---

#### **Cenário 3: Validação do payment_delay (Data de Caixa Futura)**

* **Objetivo:** Testar o cálculo da cash_date quando há um atraso no pagamento.
* **Pré-condições (Setup):**

  
  1. Crie uma reserva na reservation_reservation com id = 101, status = 'Concluded', is_blocking = false, e ota_id = 2.
  2. Crie uma configuração na reservation_ota_setup com ota_id = 2 e payment_delay = 30 (ou qualquer valor != 0).
* **Ação (Action):**
  * Execute um INSERT na tabela financial_cleaning_fee_manual_fit:

    **Generated sql**

    ```javascript
    INSERT INTO financial_cleaning_fee_manual_fit (reservation_id, date_ref, value, description, is_adding) 
    VALUES (101, '2023-10-26', 70.00, 'Ajuste com delay', true);
    ```

    Use code **[with caution](https://support.google.com/legal/answer/13505487)**.SQL
* **Resultados Esperados (Expected Outcome):**

  
  1. Um novo registro deve ser criado em closing_host_resume e closing_seazone_resume com:
     * accrual_date = '2023-10-26'
     * cash_date = '2023-11-26' (date_ref + 1 mês).


---

#### **Cenário 4: Operação de UPDATE (Garantia de Idempotência)**

* **Objetivo:** Garantir que uma atualização no registro original limpa os dados antigos e insere os novos corretamente.
* **Pré-condições (Setup):**

  
  1. Execute o Cenário 1 para que existam registros nas tabelas closing_\*_resume.
  2. O registro com reservation_id = 100 existe em financial_cleaning_fee_manual_fit.
* **Ação (Action):**
  * Execute um UPDATE no registro criado:

    **Generated sql**

    ```javascript
    UPDATE financial_cleaning_fee_manual_fit 
    SET value = 55.00 
    WHERE reservation_id = 100;
    ```

    Use code **[with caution](https://support.google.com/legal/answer/13505487)**.SQL
* **Resultados Esperados (Expected Outcome):**

  
  1. Os registros antigos (value = 50.00) para reservation_id = 100 devem ser **excluídos** de closing_host_resume e closing_seazone_resume.
  2. Novos registros com value = 55.00 devem ser **inseridos** em ambas as tabelas.
  3. A contagem final de registros para reservation_id = 100 e transfer_category = 'cleaning_manual_fit' deve ser 1 em cada tabela de resumo.


---

#### **Cenário 5: Status da Reserva Inválido**

* **Objetivo:** Validar que o gatilho não insere dados se a reserva não estiver com status Concluded ou No-Show.
* **Pré-condições (Setup):**

  
  1. Crie uma reserva na reservation_reservation com id = 102, status = 'Confirmed', is_blocking = false.
* **Ação (Action):**
  * Execute um INSERT na financial_cleaning_fee_manual_fit para essa reserva:

    **Generated sql**

    ```javascript
    INSERT INTO financial_cleaning_fee_manual_fit (reservation_id, date_ref, value, description, is_adding) 
    VALUES (102, '2023-10-26', 50.00, 'Ajuste em reserva confirmada', true);
    ```

    Use code **[with caution](https://support.google.com/legal/answer/13505487)**.SQL
* **Resultados Esperados (Expected Outcome):**

  
  1. O gatilho será acionado. A parte de DELETE será executada (sem efeito se não houver dados prévios).
  2. O cursor clean_cursor não retornará nenhuma linha, pois o filtro rr.status in ('Concluded', 'No-Show') falhará.
  3. **Nenhum** novo registro será inserido em closing_host_resume ou closing_seazone_resume.


---

#### **Cenário 6: Reserva do Tipo Bloqueio (is_blocking = true)**

* **Objetivo:** Validar que o gatilho não insere dados se a reserva for um bloqueio.
* **Pré-condições (Setup):**

  
  1. Crie uma reserva na reservation_reservation com id = 103, status = 'Concluded', is_blocking = true.
* **Ação (Action):**
  * Execute um INSERT na financial_cleaning_fee_manual_fit para essa reserva.
* **Resultados Esperados (Expected Outcome):**

  
  1. O cursor clean_cursor não retornará nenhuma linha, pois o filtro rr.is_blocking is false falhará.
  2. **Nenhum** novo registro será inserido em closing_host_resume ou closing_seazone_resume.


---

#### **Cenário 7: Múltiplos Ajustes para a Mesma Reserva**

* **Objetivo:** Testar se a função lida corretamente com vários registros de ajuste para a mesma reserva.
* **Pré-condições (Setup):**

  
  1. Use a mesma reserva do Cenário 1 (id = 100).
  2. Insira dois registros na financial_cleaning_fee_manual_fit:

     **Generated sql**

     ```javascript
     -- Primeiro ajuste
     INSERT INTO financial_cleaning_fee_manual_fit (reservation_id, date_ref, value, description, is_adding) 
     VALUES (100, '2023-10-26', 50.00, 'Ajuste positivo', true);
     -- Segundo ajuste (dispara o gatilho de novo)
     INSERT INTO financial_cleaning_fee_manual_fit (reservation_id, date_ref, value, description, is_adding) 
     VALUES (100, '2023-10-27', 15.00, 'Ajuste negativo', false);
     ```

     Use code **[with caution](https://support.google.com/legal/answer/13505487)**.SQL
* **Ação (Action):**
  * A segunda inserção acima já serve como ação. O gatilho irá limpar o resultado da primeira inserção e reprocessar tudo.
* **Resultados Esperados (Expected Outcome):**

  
  1. Após a segunda inserção, a tabela closing_host_resume deve conter **dois** registros para reservation_id = 100:
     * Um com value = 50.00 e transfer_type = 'input'.
     * Um com value = 15.00 e transfer_type = 'output'.
  2. O mesmo acontecerá para closing_seazone_resume, com os transfer_type invertidos.


---

#### **Cenário 8: Caso de Borda - Operação de DELETE (Potencial Falha)**

* **Objetivo:** Analisar o comportamento da função ao deletar um registro de ajuste.
* **Análise:** A função possui um bug em potencial. Na linha res_id := NEW.reservation_id;, a variável NEW é NULL durante uma operação de DELETE. Isso causará um erro de "cannot read property of null" e a transação inteira falhará.
* **Pré-condições (Setup):**

  
  1. Execute o Cenário 1 para criar um registro em financial_cleaning_fee_manual_fit e os registros correspondentes em closing_\*_resume.
* **Ação (Action):**
  * Execute um DELETE no registro:

    **Generated sql**

    ```javascript
    DELETE FROM financial_cleaning_fee_manual_fit WHERE reservation_id = 100;
    ```

    Use code **[with caution](https://support.google.com/legal/answer/13505487)**.SQL
* **Resultados Esperados (Com o código atual):**

  
  1. A função será acionada.
  2. old_res_id será definido como 100 a partir de OLD.reservation_id.
  3. A etapa de DELETE nas tabelas de resumo será executada com sucesso.
  4. A execução **falhará** na linha res_id := NEW.reservation_id;, e a transação sofrerá um ROLLBACK.
  5. **Conclusão:** Nenhum dado será efetivamente deletado, nem o registro original nem os registros de resumo. Isso é um bug a ser corrigido.
* **Correção Sugerida:** A lógica deveria parar após a limpeza se a operação for DELETE.