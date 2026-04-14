<!-- title: Melhoria de Perfomance - Páginas e APIs | url: https://outline.seazone.com.br/doc/melhoria-de-perfomance-paginas-e-apis-h5k9ZfgUte | area: Tecnologia -->

# Melhoria de Perfomance | Páginas e APIs

# Pré-Reserva

## Home


## Busca


## Imóvel


## Checkout

### **Página "Confirmar e Pagar"**


1. Ao entrar em qualquer página, é como se aplicação inteira fosse carregada novamente. Vemos aqui que os arquivos JavaScript (.js) e de fontes (.otf) estão muito pesados, especialmente em conexões mais lentas (caso do print).

 ![Simulado carregamento em conexão 3G](/api/attachments.redirect?id=49ce46f5-be7d-4ff7-a67c-d8b72946c53f)


2. A transição da página de confirmar e pagar para a página do imóvel (ao clicar em voltar para o imóvel) também está lenta e brusca. Seria interessante adicionar uma transição mais suave nas trocas de telas.\nEsse comportamento dá a sensação de que o sistema está lento ou que travou, já que não há um feedback imediato da ação que o usuário realizou.\n
3. A página também está com um alto consumo de memória RAM, requerendo bastante do dispositivo que está acessando o site.

   ![](/api/attachments.redirect?id=2a3c963a-4c78-47c2-b52d-fc725d1bc510)



4. Ao acessar a página, é visto que as chamadas ao prismic para carregar os itens do menu, ocorrem 3 vezes como mostra o print a seguir:![3 chamadas seguidas ao menu_prismic](/api/attachments.redirect?id=eb2bca3d-22c2-41ba-b76e-720e895257ce " =506x292")
5. No ambiente local, a API de Login que há na página está levando cerca de 570ms para redirecionar o usuário, já no ambiente de produção esse valor dobra, levando cerca de 1.2s. Mas, esse aumento considerável (dobro do tempo) se deve ao tempo inicial de conexão, que pode estar relacionado com o servidor estar no Oregon, já que o tempo para resposta foi praticamente o mesmo.

   > ***[Conexão inicial](https://developer.chrome.com/docs/devtools/network/reference?utm_source=devtools&utm_campaign=stable&hl=pt-br#timing-explanation)****. O navegador está estabelecendo uma conexão, incluindo handshakes ou novas tentativas TCP e negociando um SSL.*

   \n![Teste API de Login (ambiente de dev)](/api/attachments.redirect?id=51de438f-d76b-425b-8c1f-956dca17b856 " =844x250")![Teste, API de Login (ambiente de produção)](/api/attachments.redirect?id=ffc94804-3fc7-49dd-9604-3c963fe839b9 "left-50 =966x434")

   \
   \


\
### **API properties/{id}/booking-price-v2**

Precisa consultar a Stays. O tempo de retorno depende basicamente da velocidade da conexão do usuário. Quanto mais rápida a conexão, mais rápido retorna. Porém, há um fato de que o servidor do backend está no Oregon, isso impacta no tempo de resposta final, levando a resposta pra 200ms.

Por meio de testes realizados (em ambiente de dev), as APIs da Stays leva em média 200ms para retornar um dado.


### **API reservations/create**

Estava analisando no ambiente local parte por parte do código e como esperado, as partes que mais tomam tempo são as que precisam se comunicar com a Stays para obter alguma informação.

Ao que parece, os requests à Stays podem levar cerca de 200 a 300ms, e se acontecem duas chamadas o tempo praticamente dobra (`~300ms * qtd_req`).

Esses são testes do pior cenário, onde a pessoa usa um cupom que é inválido e aciona o fallback.

 ![](/api/attachments.redirect?id=5e791577-5743-490d-b85a-df7886edcf86)

A parte que lida com cupons e faz o fallback deles é a parte que mais impacta ali para a demora (praticamente 1s: \~700ms da handle_promo_code + \~300ms da create_reservation), pq ela precisa fazer vários requests à Stays para validar os cupons.

Dessa forma, **1s de intervalo entre uma verificação e outra faz sentido,** já que o tempo de concluir a task vai ser próximo disso.

 ![1s de delay](/api/attachments.redirect?id=d686d4d4-927e-4df0-826a-b7eecda6886e)

 ![](/api/attachments.redirect?id=61b2d496-ae70-4790-9663-73171e39f3c7)

**Em resumo**, a lentidão da API se deve especialmente pela necessidade de comunicar com APIs externas durante o processo de criação de reserva.


#### Possível solução utilizando **Cache na APIs da Stays**:

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


### **API reservations/checkout**


## Login


# Pós-reserva

## Detalhes da Reserva

## Minhas Reservas

## Meu Perfil