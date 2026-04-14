<!-- title: Perfomance - Análise API de Criação de Reserva | url: https://outline.seazone.com.br/doc/perfomance-analise-api-de-criacao-de-reserva-d6hdF4vqKz | area: Tecnologia -->

# Perfomance | Análise API de Criação de Reserva

# Análise Implementação atual \[API\]

Atualmente o fluxo de criação de reserva (checkout) envolvem 3 etapas e 6 APIs principais:

* **Orçamento:**
  * `GET /properties/{property_id}/booking-price-v2`: Obtém preço da reserva consultando a Stays.
* **Pré-reserva ==(foco atual)==:**
  * `POST /reservations/create`: Cria pre-reserva (BD e Stays). Cria/atualiza o user (BD e Auth0).
* **Pagamento/Checkout:**
  * `POST /reservations/checkout` (checkout externo): Gera link para o checkout
  * `POST /reservations/payment/pay` (checkout interno): Realiza processamento do pagamento (pix, cartão)
  * `POST /paypal/create-order` e `POST /paypal/capture-order`


Nesta análise irei focar na `POST /reservations/create` que atualmente é a mais lenta dentre as demais.

> *As análises das demais podem ser inseridas aqui no futuro.*


## POST /reservations/create

### Dependências

* Conexão com o **Banco de Dados** da Aplicação: para obter, atualizar e criar reserva/usuário no BD
* Integração com a **Stays**: Para Validar Disponibilidade, Validar cupons, Calcular preço da reserva, Criar pre-reserva e Cancelar pre-reserva.
* Integração com **Auth0**: Para criar usuário e possibilitar que ele faça login na aplicação.
* Integração com o **Celery**: para envio de tarefas para fila e verificar seu andamento


### Etapas que compõe a API

Essa API ela unifica 3 APIs em uma só. Ela foi criada com o objetivo de evitar que o front precisasse realizar 2 chamadas de API + 1 polling para verificar a confirmação da reserva, enviando e recebendo tudo que precisa em uma só chamada.

O que a API faz:


1. **Pré-validações básicas**

   
   1. Valida se o cupom SOUSEAZONE25  está sendo usado por um Email `@seazone.com.br`.
   2. Verifica se as datas são válidas (datas no futuro, checkin maior que checkout, etc; não verifica disponibilidade)
2. **Criação de reserva**

   
   1. **Validações básicas**

      
      1. Valida se o imóvel selecionado existe. **==\[Query ao BD\]==**
      2. Valida o documento informado
   2. **Cria ou Atualiza usuário**

      
      1. Se usuário existe só atualiza no BD **==\[Query ao BD\]==**
      2. Se usuário não existe, cria no BD e Atualiza no Auth0 **==\[Query ao BD\] \[Request HTTP ao Auth0\]==**
   3. **Geração de reserva no BD**

      
      1. Verifica se já existe um registro de reserva (status PENDING) no BD **==\[Query ao BD\]==**
      2. Caso não exista, verifica se há uma pre-reserva (status CONFIRMED) no BD **==\[Query ao BD\]==**

         
         1. Se já existir, Cancela pre-reserva **==\[Query ao BD\] \[Request HTTP à Stays\]==**
         2. Se não, Cria nova reserva no BD (mas não cria na Stays) **==\[Query ao BD\]==**
   4. **Valida quantidade de hóspedes**
   5. Persiste reserva no BD **==\[Query ao BD\]==**
3. **Prepara chain de tasks para ser enviada ao worker-user** (não executa, envia as tasks para a fila)

   
   1. `stays_check_client`: Cria ou atualiza usuário na Stays ++ Salva user.stays_id no BD
   2. `confirm_reservation_task`: Processa criação da pre-reserva na Stays (confirma pre-reserva) (depende da task anterior por causa do user.stays_id)
   3. `notify_reservation_confirmed`: Notifica o hóspede caso tenha sido confirmada a pre-reserva.
   4. `update_availability`: Atualiza disponibilidade do imóvel no OpenSearch, devido pre-reserva criada.
4. **Aguardar conclusão das tasks** `stays_check_client` e `confirm_reservation_task` (polling; max 25s)
5. **Obtém registro atualizado da Reserva**
6. **Retorna reserva**.


#### **Tempos de resposta**

Consultando os Traces e Logs, o tempo para retornar a conclusão da reserva está em 3 segundos em média, onde o máximo é **\~5 segundos** e o mínimo **\~2 segundos.** 

> As métricas de duração podem não ser tão precisas devido a forma como foi obtida. A métrica latency_bucket do Prometheus, o valor exibido parece bem inconsistente, não sendo possível determinar a escala em que ele está ou se está correto.\n`avg by(http_route) (rate(traces_spanmetrics_latency_bucket{service="seazone-reservas-api-cluster", http_route=~"/reservations/create|/reservations/checkout|/reservations/details"}[1m])) * 1000`


**Query Traces**

```none
{span.http.route="/reservations/create" && resource.service.name="seazone-reservas-api-cluster" && name="POST /reservations/create" && kind=server && span.http.user_agent!="Uptime-Kuma/1.23.15"}
```

 ![](/api/attachments.redirect?id=b42b6f03-d1f1-4e4a-92dd-868caf949537)

**Query logs**

```javascript
{app="api-seazone-reservas"} != `Uptime-Kuma` |~ `POST.*reservations/create` | json
```

 ![](/api/attachments.redirect?id=cdb78018-8f25-46ca-a385-168b25b46951)


#### Cenários possíveis


1. ==(pior)==       Reserva com cupom inválido (cai no fluxo de fallback)
2. ==(médio)==   Reserva com cupom válido (não cai no fluxo de fallback)
3. ==(melhor)==  Reserva sem cupom


### Gargalos identificados

Ao realizar testes na API e Inserir logs para calcular o tempo de cada etapa, vemos que o principal gargalo dessa API são as requests realizadas à serviços externos (auth0 e stays). \nPrincipalmente a quantidade de requisições realizadas à Stays, pois ela é nossa fonte da verdade para validações e precisamos estar sincronizados com ela.

Observe os Traces abaixo:

 ![Trace ID: 528d5c61819008e9233a65859b6fafa3](/api/attachments.redirect?id=d4150d31-f1aa-4450-9cac-e466d5cfeddf)


 ![Trace ID: 2b1cbc6a0e3f50c19e41025cd9958f6e](/api/attachments.redirect?id=9bca66ab-8a63-46eb-a5a9-4d1643b99c01 " =1919x1017")


 ![](/api/attachments.redirect?id=f3334d77-5b4a-4548-ab02-666238fc0e19)


#### **Gargalo 1: Requisições à terceiros**

Dessa forma, observamos que quanto mais requests fazemos, mais demorada o processamento da pre-reserva fica. Aumentando cerca de 200ms/request, sendo o de **atualização/criação de usuário no Auth0** e **criação de reserva** **na Stays** **os mais demorados.**

No entanto, são requests necessárias para validar e garantir que as dê tudo certo com a criação da pre-reserva, logo (a princípio), não daria para simplesmente remove-las ou postergá-las.


**Requests Stays**

Realizamos essas requisições pois hoje a **Stays é nosso oráculo** para dados de reservas. \nEmbora, tenhamos indexado no OpenSearch a disponibilidade e preço, no momento da reserva buscamos na Stays essa informação para **garantir o preço mais atualizado**.

E **além disso, não temos um módulo de cupom no site**, por isso precisamos usar a Stays para realizar o cálculo do valor com e sem cupom para nós.

> *No passado **já tentamos nós mesmos calcular o valor do desconto** aplicado pelo cupom com base na informação do cupom, porém, esse **cálculo era incerto** pois sempre dava uma diferença no valor calculado pela Stays e no valor calculado por nós.*\n*Por isso, optamos por delegar para a Stays calcular.*


**Requests Auth0**

Com relação ao request ao Auth0, realizamos e esperamos que ele tenha dado sucesso pois caso tenha falhado, o usuário não conseguirá realizar redefinir sua senha e realizar login. 


#### **Gargalo 2: Aguardar finalização da Task assíncrona**

Atualmente estamos forçando um processo assíncrono ser síncrono para poupar trabalho do frontend. 

Como dito inicialmente, essa API **agrupam 3 outras APIs**, sendo **uma dessas**, **um polling**. \nEsse polling era realizado no frontend para verificar se o processamento da pre-reserva havia finalizado.


### Quick wins


#### -1. Disparar survey para nossos usuários 

Acredito que pode ser útil pedir a opinião de quem compra conosco, e verificar se a demora é realmente um problema hoje, ou se estamos focando em um problema que a princípio, não é grave (embora lentidão no geral seja ruim).

Isso é interessante pois vai nos ajudar a focar no que é realmente prioritário. Pode ser que, por exemplo, a lentidão em na página de busca ou imóvel incomode gere mais abandono que na página de checkout.

Olhando pelo Posthog, 97% dos que clicam no botão de Confirmar e Pagar foram redirecionados. A lentidão sendo um problema, acredito que o número de não redirecionados seria maior. ![](/api/attachments.redirect?id=45025ff2-836c-40dc-a86e-37756d30adf9)


#### 0. Animação para distrair os usuários

Podemos utilizar uma animação com texto dinâmico para dar um feedback do usuário e distraí-lo quanto a demora. Essa animação seria executada enquanto a requisição não é finalizada.

O processo de criar a pre-reserva é naturalmente assíncrono para que haja uma resiliência, por exemplo, caso a mesma falhasse (exceptions) o próprio celery iria retentar automaticamente.

Para disfarçar a demora desse processo (que se deve principalmente a requests à APIs de terceiros), podemos por uma animação.


\
#### **1. Uso de Cache em determinadas APIs da Stays**

Na página do imóvel, na Task confirm_reservation (criação da pre-reserva), a API da Stays usada para Calcular o Preço (`POST /external/v1/booking/calculate-price`)  da reserva, é a mesma utilizada na API de Preço (`GET /properties/property_id/booking-price-v2`) usada na página do imóvel e checkout.

Isso vale para a verificação de disponibilidade para o período selecionado, o qual é consultado a API da Stays para verificar se o período está disponível e se obedece ao min stay (`GET /external/v1/calendar/listing/{listingId}/from=&to=`) 

Se cachearmos por 10 minutos, por exemplo, quando a task realizar a request novamente, irá obter do cache a resposta, não precisando refazer a requisição.

**Ganhos:**

* Isso deve economizar 4 requests, ou \~800-1200ms \n*(considerando que cada requests leva em média 200-300ms)*

  \n**Resultados obtidos:**\n***Obs.:*** *Os resultados variam pois* o tempo de resposta da Stays variam bastante de request para request.
  * **Sem cache**: \~5392.08 ms![](/api/attachments.redirect?id=5207d835-0ba7-44bb-82e5-14795b9d8c16)

    \
  * **Com Cache**:  \~4179.06 ms (Redução de \~1200ms, aprox. **==22.49%==**)\n*Em um dos testes chegou a ficar abaixo de 3 segundos (que é o mínimo hoje)*\n![](/api/attachments.redirect?id=6dfbb97e-05d1-467c-804b-e9dbcc6e6837)![](/api/attachments.redirect?id=25c9ae3a-f636-44dd-aa05-839e2aa32d6e)\n


**Consequência:** 

* Já houve casos em que o atendimento cancelou uma pre-reserva para que ela fosse refeita pelo hóspede.\nNesse caso, caso isso ocorra, pode levar até 10min para o cache ser revalidado. 
  * Exemplo: `GET /properties/88/booking-price?adults=1&promo_code=hospede10&date_from=2025-06-18&date_to=2025-06-21`
  * Se a API retornar que o período está indisponível, isso ficará em cache.
  * Caso o período seja liberado antes dos 10min, vai continuar sendo retornado como indisponível pois o cache ainda não expirou. Expirará após os 10min.

  \n**Como resolver:** Podemos resolver esse problema revalidando o cache (deletando a key do redis) no momento em que recebermos algum webhook ou na própria Task. \nPara revalidar, poderíamos deletar todas as keys com pattern do listing. Exemplo: `redis-cli --scan --pattern 'get_listing_calendar_req:listing_id=604e42...*' | xargs redis-cli unlink`.\n*Ref.:* <https://redis.io/docs/latest/commands/unlink/>

  ```python
  # Obs: Não testado ainda no projeto...
  pattern="get_listing_calendar_req:listing_id=<stays_listing_id>:*",
  batch_size=100
  while True:
      cursor, keys = r.scan(cursor=cursor, match=pattern, count=batch_size)
      if keys:
          # UNLINK is better than DEL. UNLINK is async (non-blocking)
          deleted = r.unlink(*keys)
          total_deleted += deleted
          logger.info(f"Deleted {deleted} keys (batch).")
      if cursor == 0:
          break
  ```

  \


#### **2. Solicitar cacheamento de requisições por parte da Stays**

Assim como podemos cachear, podemos aproveitar o caso de que somos o maior cliente da Stays e solicitar à eles que fosse implementado algum tipo de cache na requisição. Isso diminuiria o tempo de resposta e seria delegado para eles a implementação e gestão do cache.

Essa implementação teria praticamente o mesmo efeito do **item 1.**

**Ganhos:** 

* Isso deve economizar 4 requests, ou \~800-1200ms \n*(considerando que cada requests leva em média 200-300ms)*
* (Talvez) Não precisamos gastar tempo de dev implementando cache.\n*Se não precisar de ação do nosso lado para habilitar o cache na request.*
* (Talvez) Deixe os tempos de resposta mais consistentes\n*Os requests à Stays acabam variando o tempo de resposta, não há um tempo de resposta consistente, mesmo sendo o mesmo request.*


#### 3. Mover criação de usuário no Auth0 para uma task separada

Atualmente, criamos o usuário durante a chamada da API de criação da reserva. Como a maioria dos nossos usuários são usuários novos, então essa etapa é acionada com frequência. Logo, aumenta o tempo de resposta em cerca de 1 segundo (pelos testes realizados).

Podemos realizar essa ação em um Task no Worker, já que não necessariamente é obrigatório o usuário ter sido criado no auth0 para criar a pre-reserva.

**Ganhos:** 

* Poderíamos economizar 1 segundo do tempo de processamento da API.


**Consequência:** 

* Se por algum motivo ocorrer falha na criação do usuário no Auth0, ele não conseguirá fazer redefinir sua senha ou fazer login pois: O Email existirá no BD mas não no auth0, ao tentar se registrar, irá ocorrer o erro de email duplicado.
  * Apesar disso, ser um trade-off, ele é um caso de borda (pouco comum de ocorrer), e que não vimos acontecer nos últimos 30d. Ocorrências: 1x em Março; 3x em Abril *(Loki crashou, pode haver mais)*
  * Esse problema de login poderá ser contornado se criarmos manualmente o usuário no Auth0 e atribuirmos o auth0_id gerado, ao usuário no BD manualmente. 
  * Logo, se para **Produto** não for um problema postergar a criação do usuário no Auth0, podemos aplicar essa alteração.![](/api/attachments.redirect?id=61f53fee-f38b-4fce-84e8-48d12dd689b4 " =549x288")


\

### **Future**

#### **1. OpenSearch como fonte de dados de preço/disponibilidade**

Já atualizamos com grande frequencia os dados do OpenSearch, os dados de disponibilidade e preço do OpenSearch são praticamente real-time, então faz sentido o considerar fonte da verdade para essas informações.

* Com isso, a request de obtenção da disponibilidade (`GET /external/v1/calendar/listing/{listingId}/from=&to=`) não precisa ser realizada na Stays, mas sim, no OpenSearch.
* Porém, isso não resolve o problema do cálculo de preço pois caso haja cupom, não conseguimos garantir que o cálculo do desconto esteja correto.
  * Isso poderia ser sanado se a Stays tivesse uma forma de nós mesmos informar qual valor da reserva e quanto foi o desconto.

**Ganho:**

* Isso geraria uma economia de \~300ms.

**Ponto de atenção:**

* Garantir que os dados indexados sejam sempre os mais atualizados possíveis. **(já é assim)**


#### **2. Deixar a Stays ser a última a saber da reserva**

Aqui o objetivo seria ser 100% autonomos na criação de reservas, a Stays iria ser comunicada apenas quando o pagamento fosse realizado e a reserva paga de fato.

O que seria feito:

* Realizar o que foi comentado no **Item 1**
* Realizar a implementação do módulo de cupom no site

Dessa forma, todo a verificação de disponibilidade e calculo do preço de reserva (com e sem cupom) ficaria 100% do nosso lado, não havendo comunicação com serviços externos, reduzindo a latência dessas etapas.

Nessa abordagem, a Stays só seria informada da reserva após ela ter sido de fato confirmada e reduzindo a dependencia dela para criação dessas reservas.

**Ganhos:**

* Redução de dependencia da Stays
* Autonomia para gerenciar nossos próprios cupons e calcular descontos como quisermos.

**Trade-off:**

* Aumento de complexidade: Vamos precisar criar e gerenciar um novo módulo (cupons) que não existe hoje.
* Risco de overbooking por não travar o período com uma pre-reserva, caso a gente deixe para informar a Stays apenas após a confirmação do pagamento.


\

\


---


---


# 

# 

# Anotações

Para análise, considere os textos acima.

## **POST reservations/create**

Estava analisando no ambiente local parte por parte do código e como esperado, as partes que mais tomam tempo são as que precisam se comunicar com a Stays para obter alguma informação.

Ao que parece, os requests à Stays podem levar cerca de 200 a 300ms, e se acontecem duas chamadas o tempo praticamente dobra (`~300ms * qtd_req`).

Esses são testes do pior cenário, onde a pessoa usa um cupom que é inválido e aciona o fallback.


\
 ![](/api/attachments.redirect?id=5e791577-5743-490d-b85a-df7886edcf86)


\
A parte que lida com cupons e faz o fallback deles é a parte que mais impacta ali para a demora (praticamente 1s: \~700ms da handle_promo_code + \~300ms da create_reservation), pq ela precisa fazer vários requests à Stays para validar os cupons.

Dessa forma, **1s de intervalo entre uma verificação e outra faz sentido (polling para verificar se uma reserva foi concluída),** já que o tempo de concluir a task vai ser próximo disso.


\
 ![1s de delay](/api/attachments.redirect?id=d686d4d4-927e-4df0-826a-b7eecda6886e)


\

 ![](/api/attachments.redirect?id=61b2d496-ae70-4790-9663-73171e39f3c7)


\
**Em resumo**, a lentidão da API se deve especialmente pela necessidade de comunicar com APIs externas durante o processo de criação de reserva.


### Detalhando o tempo de execução de cada etapa

Realizando um novo teste, desta vez datalhando mais o tempo de execução de cada etapa, podemos verificar o que exatamente aumenta o tempo de execução.

E como esperado, vemos que o tempo é aumentado drasticamente quando precisamos realizar um request à uma API externa (Stays e Auth0)


 ![](/api/attachments.redirect?id=f4f1b959-aefa-4f2a-9885-6ba0d0e5f871)


\
## Possível solução utilizando **Cache na APIs da Stays**:

* Para conseguirmos cachear, a API e a Task, precisam usar a mesma função para obter o preço/disponibilidade do imóvel.
* Ao utilizar cache nas APIs da Stays, conseguimos reduzir aprox pela metade o tempo que leva para processar a task. De **4s** para **2s**.
  * Esses 2 segundos ainda restaram pois é preciso esperar a task `stays_check_client` ser concluída, e nela possui comunicação com a Stays para atualizar o user. Essa task é necessária, não dá para deixar para depois pois precisamos garantir que o user tenha um stays_id para que criação da reserva.
  * O tempo da task de confirmar reserva agora é cerca de \~500ms. Redução de \~80%

Problema para implementar Cache nessas APIs:

* O Celery roda código python **síncrono (não possui suporte ao async)**. A request realizada na página do imóvel e checkout para obter o preço, é assíncrono.
* Sendo assim, ao cachear a resposta da API, a chave do cache criada no Redis fica diferente da queria utilizada no Worker, pois são classes diferentes.
* O decorator de cache cria um padrão de key no formato: ClassName.FunctionName.args_kwargs
* Uma possível solução para isso, poderia:
  * Utilizar a lib asyncio, no entanto, de acordo com a pesquisa o asyncio não funciona caso já tenha um outro loop em execução, e no caso do Celery, ele utiliza o eventlet.\nIsso foi visto durante os testes também, onde ao tentar usar o asyncio.run() houve o erro: `"RuntimeError: await wasn't used with future"`
  * Ou, Criar um versão síncrona da API de Preço execute a request de forma síncrona. \nO **trade-off** seria perder os benefícios do *async* neste endpoint. No caso, os requests à API de preço passariam as ser bloqueantes, reduzindo a performance e potencial de requests simultâneos à essa API.


\