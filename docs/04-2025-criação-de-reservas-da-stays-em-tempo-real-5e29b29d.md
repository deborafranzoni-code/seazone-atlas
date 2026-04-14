<!-- title: [04-2025] Criação de Reservas da Stays em Tempo Real | url: https://outline.seazone.com.br/doc/04-2025-criacao-de-reservas-da-stays-em-tempo-real-Z7WJiukH82 | area: Tecnologia -->

# [04-2025] Criação de Reservas da Stays em Tempo Real

As reservas são criadas no nosso sistema de duas formas:

* **Webhook da Stays**: a Stays envia um evento de criação/modificação de reservas quando esse evento ocorre;
* **Task de importação de dados**: a cada 15 minutos, executamos uma rotina que busca todos os eventos de criação de reservas que ocorreram no dia atual e no dia anterior.


Portanto, por meio do webhook, a criação de reservas já deveria estar ocorrendo em tempo real. Porém, os usuários do Sapron não estão com essa percepção. Por isso, foi feita uma investigação para tentar entender o que está ocorrendo. O objetivo foi tentar responder duas perguntas:

* Estamos recebendo com delay as mensagens da Stays?
* Estamos realmente demorando para salvar os eventos da Stays no nosso banco de dados?


Para responder a essas perguntas, registramos todos os eventos de criação de reservas enviados pela Stays ao longo de 3 dias (entre 01/04 e 04/04), totalizando 1000 registros. Toda vez que chegava um evento da Stays, salvamos em log o tipo do evento, o código da reserva na Stays, a data-hora em que a Stays reportou o evento (campo "_dt" no evento recebido pelo webhook) e a data-hora atual do sistema. Infelizmente, a Stays não envia um campo indicando a data exata de criação. Portanto, assumimos que o campo "_dt" está relacionado com o tempo de criação do evento, embora ele possa simplesmente representar o tempo que o evento foi emitido.

\nCom isso, calculamos a diferença entre a data-hora do sistema pela data-hora do evento. Para praticamente todos os eventos, a diferença entre esses tempos foi de menos de 1 segundo. Nenhum evento levou mais que 2 segundos de diferença. Ou seja, o tempo que a Stays diz que enviou o evento é praticamente o mesmo tempo que o nosso sistema diz que recebeu o evento. Portanto, podemos concluir que **o webhook da Stays não está enviando as mensagens com delay**. Isso responde à primeira pergunta.

\nPara responder a segunda pergunta, pegamos cada evento de criação que a Stays reportou e buscamos no banco de dados a data-hora que o registro foi criado, que está na coluna \`created_at\` da tabela *reservation_reservation* (o registro na *reservation_reservation* foi encontrado usando o código da reserva na Stays). Em seguida, calculamos a diferença de tempo entre a criação do registro e a chegada do evento. O gráfico a seguir mostra a distribuição da diferença de tempo. Em seguida, mostramos alguns decis da distribuição.


---

 ![](/api/attachments.redirect?id=d97fc255-372b-4c24-b15b-0ef439716c46)


50º Percentil: 7,46 segundos (mediana) 60º Percentil: 8,57 segundos

70º Percentil: 11,77 segundos

80º Percentil: 93,15 segundos

90º Percentil: 1948,65 segundos (32 minutos) Diferença máxima: 171597,58 (47,66 horas)


---

Ou seja, podemos ver que 70% dos registros foram criados no banco em menos de 12 segundos. No entanto, tem vários outliers, no qual a diferença de tempo entre a criação e a chegada do evento foram significativos. Em um primeiro momento achei que o motivo desse delay seria por causa dos picos do Banco de Dados que ocorreram ao longo das últimas semanas, mas não encontrei uma correlação forte entre eles. Por outro lado, achei uma correlação maior em relação a data de criação e se a reserva é uma extensão (ver Gráfico 2), ou seja, quando a reserva é uma extensão, a data de criação dela geralmente é mais discrepante em relação ao tempo de chegada do evento (mas isso não ocorreu para todas as extensões também). A minha suspeita é que tem algum ajuste em código alterando a data de criação das reservas quando é uma extensão.


---

 ![](/api/attachments.redirect?id=068a3dc3-dc81-4c55-9b10-202f1ba8187b)

50º Percentil (mediana): 1426.84 segundos

60º Percentil: 1820.18 segundos

70º Percentil: 2748.40 segundos

80º Percentil: 4798.60 segundos

90º Percentil: 7014.78 segundos

Diferença máxima: 20183,62 (5,6 horas)


---

Portanto, respondendo à segunda pergunta, podemos ver que a criação de reservas via webhook funciona em grande parte dos casos, com delay de criação de até 12 segundos após a chegada do evento em 70% dos casos. Porém, em 30% dos casos, a diferença entre a chegada do evento e a criação dele em banco é expressiva, e isso pode ser a causa para o time de operações achar que a importação em tempo real não está funcionando. Porém, não consegui encontrar um motivo claro para esse delay tão alto. As reservas que são extensões tem alguma relação com isso, mas também não explica totalmente o problema.