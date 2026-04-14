<!-- title: Stays | url: https://outline.seazone.com.br/doc/stays-CuKYa566M5 | area: Tecnologia -->

# Stays

![Untitled](/api/attachments.redirect?id=c95d8c51-3582-4f88-9c8b-6455c84dce04)

**[Link para acessar a plataforma](https://ssl.stays.com.br/i/home)**

## O que é a Stays


---

Stays é um sistema web que a gente chama de PMS (Property Management System) voltado para gestão de aluguel de imóveis de curta temporadora.

Na Stays está centralizado todas as informações de imóveis, hóspedes e reservas da Seazone, além de fazer também a sincronização dos imóveis e reservas com outras plataformas como Airbnb, Booking, Site, etc, evitando assim que a gente precisasse fazer isso manualmente em cada uma das pltaformas.

Resumidamente, a Stays é onde está centralizada as informações referente a imóveis, hóspedes e reservas. E a partir dela é importado para o Sapron essas informações para que a parte operacional que lida diretamente com imóveis, hóspedes e reservas, consigam realizar o seu trabalho.

O Site de Reservas hoje funciona como se fosse uma outra OTA, como o Airbnb, onde nós comunicamos via API com a Stays essas informações mencionadas para que ela chegue até o Sapron, e assim, as demais partes interessadas.

## Para que usamos a Stays no Site de Reservas?


---

Atualmente, utilizamos a Stays para:

**Sincronização dos imóveis**

De tempos em tempos, o backend, consulta determinadas API(s) da Stays para obter os imóveis inserindo os novos e atualizando os que já existem. Assim, garantindo que os imóveis e as informações deles sempre estejam atualizadas.

### **Sincronização dos Preços e Disponibilidade dos imóveis**

De tempos em tempos, o backend, consulta determinadas API(s) Stays para sincronizar (atualizar) a disponibilidade e preços dos imóveis. **Obs:** Atualmente, essas informações de preços e disponibilidade são salvas no *OpenSearch*. Não são salvas no nosso Banco de Dados.

No caso da atualização de disponibilidade, além de haver essa atualização de tempos e tempos, há também a atualização via Webhook, onde quando é realizado uma nova reserva (ou alteração de reserva), e ela é registrada na Stays, a disponibilidade daquele imóvel é atualizada no site naquele mesmo momento.

### **Sincronização de Reservas**

Durante o fluxo de reservar, quando o hóspede clica em "Confirmar e pagar" e em seguida é levado para o Checkout, nesse momento o Site de Reservas **cria uma Pré-Reservas na Stays**  (via API) para aquele imóvel e no período selecionados, evitando assim um *overbooking* (reserva em cima de um período que já foi reservado para um mesmo imóvel).

Quando a reserva é paga, nesse momento o Site de Reservas, atualiza na Stays (via API), mudando o status de "Pre-reserva" para "Reserva".

Outra comunicação que é realizada é a de alterações na reserva:

* Quando uma reserva for cancelada, ou atualizar seu status (pre-reserva > reserva; reserva > pre-reserva) ou alterada as datas na Stays, essa alteração também será refletida no Site de Reservas, assim, atualizando a disponibilidade do imóvel também.
* O contrário também ocorre. Exceto para a alteração de datas que hoje não é possível editar as datas de uma reserva no Site.

## Como acessar a Stays?


---

**Link:** <https://ssl.stays.com.br/i/home>

Necessário solicitar ao seu Gestor para criar um acesso para você.

## Rotacionamento de Chave de API


---

### Geração da nova chave

* Acessar a Stays > Menu Lateral > App Center > **API Externo** → Aqui terá todas as credenciais criadas. ***OBS: O seu usuário precisa ter permissão para acessar essa parte da Stays.***
* Criar novas chaves (sem remover as que já existem)
* Testar se as novas chaves geradas existem (pelo postman é mais fácil)
* Caso esteja funcionando, copie o Basic token que está no header da requisição

### Atualizando a chave de API na aplicação

* Acesse a AWS
* Acesse o serviço **ECS** (Elastic Container Service).
* Acesse o container que deseja atualizar e siga os passos abaixo, na sequência *(recomendo fazer no de staging primeiro)*

  ### Atualizando a variável ambiente + criando nova revision

  Para cada task definition no cluster (seja de prod ou staging), altere a variável ambiente: `STAYS_AUTH_TOKEN`. Para isso:
  * Clique na task definition do serviço (coluna task definition)

    ![Untitled](/api/attachments.redirect?id=db8dd22a-94e2-449e-981a-737efb130b30)
  * Clique em "Create new revision"

    ![Untitled](/api/attachments.redirect?id=1df945dd-a631-4ea5-8dcd-f024fcd11ae2)
  * Na seção **"Container"** procure pela variavel ambiente "`STAYS_AUTH_TOKEN`", copie o Basic Token que copiou anteriormente, e cole no campo de **"valor"** da variável de ambiente.

    ![Untitled](/api/attachments.redirect?id=a957ca95-97e6-4c46-aa21-3df649e80abe)
  * Por fim, clique em "Create" no final da página. Não é necessário alterar mais nada além disso.

    ![Untitled](/api/attachments.redirect?id=c6840379-4d94-4178-93d5-f2916944643e)

  <aside> ℹ️ **Repita esse processo para cada um dos Clusters**

  </aside>

  ### Atualizando a revision da task definition para a mais recente

  Agora, precisamos atualizar o cluster, mudando na task definition para a **revision** mais recente (a que gerou no passo anterior), para que assim, a alteração da chave seja efetivada.

  
  1. Volte para a página do Cluster, onde é exibido os serviços que estão rodando. E então, selecione 1 dos serviços (apenas um), e vá em "Update".

     ![Untitled](/api/attachments.redirect?id=8ec1ae06-5431-4670-86b1-932496d440ad)
  2. No dropdown "Revision", clique nele e selecione a "Mais recente" (ou Latest)

     ![Untitled](/api/attachments.redirect?id=bb749ad7-b421-4eb4-beee-31727e14e082)

     ![Untitled](/api/attachments.redirect?id=ba4e4d7e-dbf9-4f51-b4be-785bd6789706)
  3. Vá até o fim da página e então clique em "Update" para atualizar.

     ![Untitled](/api/attachments.redirect?id=666b2290-727b-4e9e-94ae-5a5bbda21670)

  <aside> ℹ️ **Repita esse processo para cada um dos Clusters**

  </aside>

### Teste & Validação

* Na página do cluster, onde exibe os serviço, **confira se todos os Clusters estão na última revisão da task definition**, e se está com o **deployment concluído** (não pode estar vemelho, vermelho indica falha; e nem na revision anterior, se estiver, pode ser uma falha)

  ![Untitled](/api/attachments.redirect?id=702fd925-e689-4694-bf98-a3070c51953b)

  > Atualização em andamento de todos os serviços (após atualizar cada um para a última revision
  >
  > ![Untitled](/api/attachments.redirect?id=fe2e2cef-8705-4423-86f9-2e31e4822747)

  > Deployment completado com sucesso para todos os serviços (observe que a versão da task definition se manteve na última). Sem erros.
  >
  > ![Untitled](/api/attachments.redirect?id=5ff5cdce-ad88-4ec6-b209-40a8d5fd4d73)
* Agora, volte na Stays e apague a chave que era usada anteriormente.

  ![Untitled](/api/attachments.redirect?id=8ead48bf-5a41-4b2e-ba36-e138f7955f46)
* Teste se a comunicação com a Stays está funcionando normalmente (exemplo, criando uma pre-reservas através do imóvel TST001)
* Conferir também os logs, pra verificar se estamos recebendo os webhooks normalmente.
* Se tudo estiver Ok e funcionando, o rotacionamento de chave está **concluído.**

<aside> ⚠️ Faça essas alterações **primeiramente no ambiente de staging** e só então, replique para o ambiente de produção.

</aside>