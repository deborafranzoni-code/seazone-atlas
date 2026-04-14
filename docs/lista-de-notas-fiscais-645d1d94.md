<!-- title: Lista de Notas Fiscais | url: https://outline.seazone.com.br/doc/lista-de-notas-fiscais-KX3OhIcxAw | area: Tecnologia -->

# Lista de Notas Fiscais

## Funcionamento da Funcionalidade


---

* \[…\]
* \

**Rascunho:** <https://miro.com/app/board/uXjVO5oQZhU=/?moveToWidget=3458764524670131311&cot=14>

**Qual o objetivo da tarefa?**

Criar API com filtros para carregar a lista de Notas Fiscais, e criar tabela no BD para armazenar o status daquela Nota Fiscal.

Criar task de consolidação da lista de Notas Fiscais que que atualiza a lista de Notas Fiscais, com base nas **comissões** na tabela **financial_revenues** se o status='Closed'.Criar endpoint para rodar essa consolidação.

**Permissões:** IsAdmin, IsSeazoneAdministrative\*\*Endpoint: \*\* /financial_closing/owner/invoice_details_list/\*\*App: \*\* Financial


---

## **Detalhes da tarefa:**

### **1. Criar tabela *financial_invoice_details*, com os campos:**

```
- created_at (datetime)
- updated_at (datetime)
- owner_id (fk para owner)
- owner_id (fk para host)
- invoice_detail_id (fk para invoice detail do imovel)
- ref_date (date: "yyyy-mm")
- comission (decimal)
- done_timestamp (datetime, pode ser null)
- status (string): Concluded, Not concluded, Pending
```

### **2. Criar API que gera a lista de Notas Fiscais:**

* A API irá receber o **mês/ano** de referência e retornar agrupado por invoice detail das propriedades, os valores de comissão. Se há imóveis de um proprietário que estão no mesmo invoice detail, eles serão agrupados, somando a comissão.
* O valor da comissão pode ser obtido através da tabela **financial_revenues**, no campo **comission**.

**Cálculo para quebra do valor da comissão:**

* Por invoice_details das propriedade.
  * Se o anfitrião = Seazone: Gera **uma nota** (uma linha no grid/tabela) Seazone com o valor total da comissão.
  * Se não for a Seazone: São **duas notas** (duas linhas no grid/tabela): *Obs: A soma das partes das comissões é igual ao valor total comissão:* `host_comission + seazone_comission == reservations_comission`
    * Comissão Seazone (campo anfitrião fica como Seazone): \*\*`seazone_comission** = reservations_comission - host_comission`
    * Comissão Anfitrião (campo anfitrião fica com o anfitrião do imóvel): \*\*`host_comission** = reservations_incomes * 0.08`
    * Supondo Receita de Reservas do imóvel de R$10.000, considerando que o imóvel tenha uma comissão de **20%:**
    * Comissão Anfitrião = R$800 (`10.000 * 0.08`)
    * Comissão Seazone = R$1200 (`2000 - 800`)
    * Comissão do imóvel = R$2000 (`10.000 * 0.20`)

**Anotações**

* No mês da troca vai ter uma NF para cada host, com o comissão proporcional para cada um de acordo com o dia da troca
* \


---

* **Input:** date_ref (yyyy-mm), Filtros \[search(nome proprietário, anfitrião), ordering\] **OBS:** O Search deverá aceitar matchs parciais.
* **Output:** Lista de Notas Fiscais, contendo as informações: status, owner\[\], host\[\], invoice_details\[\] por proprietário, por conta e que na tabela **financial_revenues** possui `status = 'Closed'`.

**Exemplo de retorno:**

* Owner 1 é o caso onde todos os imóveis possuem a mesma invoice detail, então a Seazone recebe 100% da comissão
* Owner 2 é o caso onde há imóveis com com invoice detail diferentes, então a Seazone recebe 92% e Anfitrião 8% da comissão.
* *Supondo uma comissão de R$1000,00:*

  ```
  {
      owner 1: {
          1: {
                  status:
                  owner[ id, user[ ] ]
                  host: [
                          id,
                          user: [
                                  id
                                  trading_name: "Seazone Serviços"
                                  ...
                          ]
                  ]
                  invoice_details:[
                          invoice_entity_name
                          cpf
                          cnpj
                          email
                          phone_number
                          postal_code
                          address
                          address_number
                          complement
                          district
                          city
                          state
                          comission: 1000.00
                  ]
          }
      }
  
     owner 2: {
          1: {
                  status:
                  owner[ id, user[ ] ]
                  host: [
                          id,
                          user: [
                                  id
                                  trading_name: "Seazone Serviços"
                                  ...
                          ]
                  ]
                  invoice_details:[
                          invoice_entity_name
                          cpf
                          cnpj
                          email
                          phone_number
                          postal_code
                          address
                          address_number
                          complement
                          district
                          city
                          state
                          comission: 920.00
                  ]
          }
          2: {
                  status:
                  owner[ id, user[ ] ]
                  host: [
                          id,
                          user: [
                                  id
                                  trading_name: "Gabriela Nunes"
                                  ...
                          ]
                  ]
                  invoice_details:[
                          invoice_entity_name
                          cpf
                          cnpj
                          email
                          phone_number
                          postal_code
                          address
                          address_number
                          complement
                          district
                          city
                          state
                          comission: 80.00
                  ]
          }
      }
  }
  ```


---

### **3. Criar task de consolidação no Celery**

Criar task no celery que consolida essa lista de Notas Fiscais, verificando se sofreu alguma alteração no valor da comissão da lista atual e se há novos comissões que estão como status='Closed' na **financial_revenues**.

* Se na lista de NF `is_done=True` e houve alteração nos valores daquele repasse de comissão, o status da NF deve passar a ser 'Pending'. Isso servirá como flag caso haja alteração no valor de uma repasse de comissão que já foi realizado.
* Se o valor mudou mas o `is_done=False`, não faz nada; não aponta flag.
* **OBS:** Deve ser criado um endpoint (`/financial_closing/owner/invoice_detail_list_update/`) para que seja possível rodar essa task. E deve ter um parametro (não obrigatório) de mes/ano para atualizar apenas para o mes/ano informado.

**OBS:** Ao enviar um GET no endpoint para carregar a lista de teds, as que já estão na tabela não podem ser sobreescritas ou duplicadas. Quando enviado para carregar a lista, deve atualizar os valores das comissões se houver mudança e carregar as novas Notas Fiscais (comissões com status=Closed na **financial_revenues**.


---

### **4. Criar endpoint para atualizar o status**

Criar API para atualizar o status (se foi feito ou não a ted) dos registros na tabela. (GET, POST, PATCH)- Se marcado como status='Concluded', também grava o done_timestamp  na tabela.- Se marcado como status='Not Concluded', o campo done_timestamp fica como null


---

### **5. Criar endpoint para exportar CSV**

Criar API para exportar para CSV a lista de Notas Fiscais com todos os campos:Nome, Nome p/ Nota Fiscal, Comissão, CPF, CNPJ, Endereço completo (concatenado), E-mail