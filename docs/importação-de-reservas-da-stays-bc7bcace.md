<!-- title: Importação de reservas da Stays | url: https://outline.seazone.com.br/doc/importacao-de-reservas-da-stays-tBFscWmhuB | area: Tecnologia -->

# Importação de reservas da Stays

### **Importação de reservas da Stays no dia de Hoje**

Task assíncrona, roda a cada **15min.**

Busca por todas as reservas **criadas**  **ontem** e **hoje** comparando as reservas que estão no **Sapron** com reservas que estão na **Stays**, adicionando-as caso não existam e/ou atualizando as que já existam no BD do Sapron.

### **Atualização de reservas futuras de Hoje até 2035**

Task assíncrona, roda a cada **24** **horas.**

Busca **todas** as reservas de com **check-out** de **hoje** até **2035,** adicionando-as caso não existam e/ou atualizando-as caso já existam no BD do Sapron.

### **Rodar importação manualmente**

> Ao chamar este endpoint, ele irá rodar a task que importa as reservas criadas da data informada até o dia atual.

Chamar o endpoint: `PUT /channel_manager/import_stays_reservations/`

**Body:**

```json
{
    "start_date": "2022-03-24"
}
```

O progresso dela pode ser verificado enviando o `task_id`  retornado para a API `GET /tasks/<task_id>`

### Importação dos valores da reservas

Devido a uma taxa (por danos,ou extensão de diária) inserida pelo Aribnb em algumas reservas, o campo base para o preço total da reserva vinha com divergência do valor final. Por isso foi trocado o campo `baseAmountForwarding` para `reserveTotal`.

Não ouve explicação de porque o campo antigo estava sendo usado ou se haveria algum impacto, por isso foi trocado.


---

### **Observações**

* As **Pré-reservas** da Stays **não** estão mais entrando no Sapron. (Deverá ser mudado no futuro quando o Atendimento vier para o Sapron para que pre-reservas venham como pre-reservas de fato)
* **Extensões de reservas do Airbnb vindas da Stays**

  Devido a forma diferente do Airbnb enviar as extensões de reservas (enviando a mesma reserva atualizada) foi criado uma classe para lidar com essas extensões. Não será atualizada a reserva original, e sim, criada uma nova extensão. As extensões de uma mesma reserva serão encadeadas pelo id, onde o pai indica o filho na mesma tabela, e na tabela `channel_manager_reservation_state` as extensões terão o id da Stays da seguinte forma `{id stays}-EX{Nº da extensão}`

  > Implementado no **[Pull Request #1293](https://github.com/Khanto-Tecnologia/sapron-pms-web/pull/1293)**


---

### **Sobre o código**

> **Onde está o código:** `/backend/channel_manager/tasks.py /`

* A importação das reservas vindas da Stays acontece via script que rodam de forma assíncrona por meio do **Celery.** A relação de código da reserva da stays e código da reserva Sapron fica na tabela: `channel_manager_reservation_state`
* Cada reserva individual retornada pela Stays será executada como uma task Celery separada. Assim podemos controlar os retries apenas para a reserva específica que deu problema, de outro modo teríamos que fazer o retry em todo o processo de importação da Stays.