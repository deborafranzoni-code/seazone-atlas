<!-- title: Reservas e Extensões | url: https://outline.seazone.com.br/doc/reservas-e-extensoes-CRkm1Z5bEU | area: Tecnologia -->

# Reservas e Extensões

==Essa documentação se aplica a todas as reservas que não são provenientes do AirBNB.==


---

# Entendendo o Fluxo

Reservas e Extensões são tratadas todas no mesmo modelo, que no banco de dados atende por `reservation_reservation`. Nela, existem alguns campos que são essenciais para podermos entender o que cada dado significa e como navegar entre as reservas. 

## Campos relevantes pra essa documentação

* `id`: **Identificar único** de uma instância do modelo `reservation_reservation`
* `check_in_date`: **Data de check-in** para uma reserva;
* `check_out_date`: **Data de check-out** para uma reserva;
* `is_early_extension`: Se a instância **antecipa o check-in** da reserva original;
* `is_late_extension`: Se a instância **prorroga o check-out** da reserva original;
* `has_early_extension`: **Se** a instância aponta pra uma **outra instância** que **antecipa** o **check-in;**
* `has_late_extension`: **Se** a instância aponta pra uma **outra instância** que **prorroga** o **check-out;**
* `early_extension_reservation_id`: **Aponta** pra qual **instância** **antecipa** o **check-in**;
* `late_extension_reservation_id`: **Aponta** pra qual **instância** **prorroga** o **check-out**;
* `original_reservation_id`: **Aponta em direção** a reserva original;
  * Se a instância tem `is_late_extension`, a `original_reservation_id` deve apontar para uma instância que acontece **antes** da instância em questão. O contrário acontece quando `is_early_extension`.
* `status`: Indica o status de uma instância. Os mais comuns são "*Concluded*" e "*Canceled*".

Exemplo de um cenário real:

 ![](/api/attachments.redirect?id=04e3e4c2-08fe-4884-bc50-2fc2c1fb9221)

Para identificar corretamente qual instância é o que, o padrão a ser seguido é:

### Características da Reserva Original

* A reserva original **DEVE** ter:
  * `original_reservation_id`= *NULL*;
  * `is_early_extension` = *false*;
  * `is_late_extension` = *false*;
* A reserva original **PODE** ter:
  * `has_early_extension` e `early_extension_reservation_id` = *true* e *ID da reserva que antecipa o check-in* (necessariamente preenchidos juntos, respectivamente);
  * `has_early_extension` e `early_extension_reservation_id` = *true* e *ID da reserva que prorroga o check-out* (necessariamente preenchidos juntos, respectivamente);

### Características da Early Extension

* A reserva que antecipa o check-in **DEVE** ter:
  * `is_early_extension` = *true*;
  * `is_late_extension` = *false*;
  * `original_reservation_id` = *ID da reserva que aponta pra ela* no `early_extension_reservation_id`;
  * `has_late_extension` e `late_extension_reservation_id` = false e NULL (necessariamente preenchidos juntos, respectivamente);
* A reserva que antecipa o check-in **PODE** ter:
  * `has_early_extension` e `early_extension_reservation_id` = *true* e *ID da reserva que antecipa o check-in mais ainda* (necessariamente preenchidos juntos);

### Características da Late Extension

* A reserva que prorroga o check-out **DEVE** ter:
  * `is_late_extension` = *true*;
  * `is_early_extension` = *false*;
  * `original_reservation_id` = *ID da reserva que aponta pra ela* no `late_extension_reservation_id`;
  * `has_early_extension` e `early_extension_reservation_id` = *false* e *NULL* (necessariamente preenchidos juntos, respectivamente);
* A reserva que prorroga o check-out **PODE** ter:
  * `has_late_extension` e `late_extension_reservation_id` = *true* e *ID da reserva que prorroga o check-out mais ainda* (necessariamente preenchidos juntos);

### Limites das extensões

Reservas podem ser estendidas ou adiantadas indefinidamente, seguindo o exemplo:

 ![](/api/attachments.redirect?id=c9c509e4-d158-441b-bdbe-1bb782a295f0)

### Cancelamento de Extensões

A partir do [SAP-1951](https://seazone.atlassian.net/browse/SAP-1951), serão inseridas duas regras para o **cancelamento de extensões**:

* Caso a atualização de uma extensão mude seus status pra "*Canceled*", a conexão entre a extensão e a reserva original será cortada, ou seja, os campos `has_XXXX_extension` e `XXXX_extension_reservation_id` na reserva original ficarão com os valores `False` e `NULL`, respectivamente. A extensão que está cancelada também será marcada como **conciliada,** para evitar que ela seja atualizada novamente.
  * Caso essa extensão esteja cancelada, na hora de atualizar também é feita uma verificação para garantir que não haja nenhuma outra extensão no seu lugar (caso o hóspede tenha errado a data no primeiro pedido de extensão). Caso haja, verifica se o status dela é "*Concluded*", se for, ignora.
  * Exemplo:

    ![](/api/attachments.redirect?id=e895f9bd-8d06-4b95-959c-8e7ed917e98f)
  * Quando o Sapron for atualizar a reserva 391834 no nosso banco de dados, ele vai ver que a reserva original (348316) aponta pra 391560 que está com status "*Canceled*". Por causa desse status, a extensão cancelada vai ser sobreescrita, resultando em:

    ![](/api/attachments.redirect?id=917f7319-4f5a-4c93-94f5-d9f732ae51fe)
  * No estado da última print, caso a extensão 391560 fosse atualizada novamente, ela não iria sobreescrever o campo `late_extension_reservation_id` da reserva original, porque a 391834 está com status "Concluded"
* Caso essa mesma atualização tenha uma extensão depois da cancelada (é o caso da 442087 caso ela estivesse cancelada na print a baixo), os campos que conectam a próxima extensão (443269) serão zerados e nulificados também, e ela passará a se tornar uma reserva independente.

  ![](/api/attachments.redirect?id=c9c509e4-d158-441b-bdbe-1bb782a295f0)

### Anomalias no Banco

A **maioria** das ocorrências são antigas (de 2021 a 2023), mas ainda existem ocorrências muito recentes, como:

 ![](/api/attachments.redirect?id=f4d1aee2-5840-4054-b6a0-691e7bfaa2fc)

Observando as datas de check-in e check-out, podemos concluir que o problema nesse caso em específico é:


1. Reserva original não aponta para a Early Extension;

   
   1. Deveria ter marcado `has_early_extension` e com `early_extension_reservation_id` preenchido com 405118.
2. Early Extension aponta pra Late Extension;

   
   1. Deveria estar com `original_reservation_id` preenchido com 398735. 
3. Late Extension aponta pra Early Extension.

   
   1. Deveria estar com  `has_early_extension` como *falso* e com `early_extension_reservation_id` *nulo.*

 ![](/api/attachments.redirect?id=4d891e7e-bdeb-4ff3-914b-e5b05d51d58c)


---

As permutações que não deveriam ser possíveis são:


1. `has_late` & `is_early` (43 ocorrências concluídas) 
2. `has_early` & `is_late` (17 ocorrências concluídas)
3. `is_early` & `is_late` (5 ocorrências, todas muito antigas)
4. `has_late` & `has_early` & `is_early` (2 ocorrências, todas antigas)
5. `has_late` & `has_early` & `is_late` (2 ocorrências, uma recente)
6. `has_late` & `has_early` & `is_late` & `is_early` (1 ocorrência, antiga)

As reservas a baixo não tem conexão entre si, mas ficam como exemplos dos casos a cima:

 ![](/api/attachments.redirect?id=e09052ca-2c73-40e2-8391-d4e0638efcdb)

Durante investigação, não consegui determinar exatamente a causa dessas anomalias. Mas elas só podem ter duas origens: ou é erro de inferência no código (pros casos antigos provavelmente já foram corrigidos) ou alguém mexeu diretamente no banco. Infelizmente a `property_audit` nem sempre é confiável pra validação disso, pois o gatilho só acontece via código. 


## Conclusão

Atualmente o fluxo funciona bem e ele, apesar de um pouco complexo, é claro o suficiente. Acredito que uma mudança no modelo de dados teria pouco ganho, principalmente por que hoje já fazemos o fechamento em cima dela, mas seria uma possibilidade plausível simplificar ele a fim de facilitar qualquer manutenção posterior no mesmo.

**Mais importante**: Seria ideal dedicar uma tarefa exclusiva pra garantir que essas anomalias não ocorram mais, seja por validação no backend, mudança no modelo `reservation_reservation` ou outras possibilidades.