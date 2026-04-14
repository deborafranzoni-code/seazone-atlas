<!-- title: Criação da reservas e comunicação com a Stays | url: https://outline.seazone.com.br/doc/criacao-da-reservas-e-comunicacao-com-a-stays-QwPQxHB8Ci | area: Tecnologia -->

# Criação da reservas e comunicação com a Stays

## Criação da reserva | Site de Reservas


---

Para criar uma reserva pelo website, é necessário clicar no botão de "Reservar" na página do imóvel desejado.

* Necessário selecionar uma data; Essas datas possuem regras que podem ser encontrada aqui  *[Detalhes do imóvel](/doc/detalhes-do-imovel-BaMhIIjVEk)*
* Necessário que o usuário esteja **logado** para conseguir realizar a reserva.
  * Caso não esteja, ele será levado para a tela de Login
  * Em seguida ele voltará para a página do imóvel onde deverá clicar novamente em "Reservar".
    * **Por que voltar pra página do imóvel e não levar direto para a página de confirmação?**

      A ideia do `/start-reservation` (requisição/ação que fica no botão "Quero reservar") é para a gente saber que o user iniciou a reserva, mas não necessariamente vai pagar. Quando o **usuário da o start na reserva**, a mesma é criada no nosso banco de dados com o status **Pending**. Isso, ao nosso ver, tem valor em uma questão de análise de dados apenas, pois assim sabemos que determinado usuário teve "interesse" em um imóvel, em certas datas, etc.. Com essas informações, podemos futuramente disparar emails para esses usuário "finalizarem sua reserva", ou "sugerindo outras datas" enfim, só um exemplo do valor que isso tem.

Com essas duas condições satisfeitas, o usuário é levado para a página de Confirmação, onde é possível informar um **cupom de desconto**.

O usuário deverá clicar em "Confirmar e pagar" confirmar a criação da reserva. Após isso será levado para a tela de [Pagamento da reserva](/doc/pagamento-da-reserva-Uq54E7aePF) (checkout externo).

> *Caso o usuário tente voltar do checkout para o site (usando a ação de voltar), ele será levado para a página de detalhes da reserva onde ele terá duas opções: **Cancelar** reserva ou **Pagá-la**.*

Concluído a etapa de pagamento o usuário será redirecionado para o site na tela de conclusão, contendo os detalhes da reserva que ele realizou.

**Regras**

* Caso não seja identificado o pagamento da reserva em até 30min após a sua criação, a reserva irá expirar.
* **Diagrama de estados da reserva \[TO-DO\]**

## Criação da reserva | Stays


---

Quando a criação de uma reserva é concretizada no website, ela é refletida na Stays, gerando lá um registro da reserva para o imóvel e o hóspede autor.

Esse processo é realizado de forma assíncrona em uma task do **Celery:** `nome da task aqui`

Atualmente, as reservas são criadas com o status **booked (pre-reserva)**

## Observações


---

* Em **staging** caso crie uma reserva em um imóvel que não seja o TST001, ela só será criada no BD do website, não será criada na Stays.
* Em **staging** só é possível criar a reserva na Stays se for no imóvel `TST001`. Ele é um imóvel de teste configurado para realizar testes.
* Em **produção**, toda reserva criada em qualquer imóvel, será criada também na Stays.