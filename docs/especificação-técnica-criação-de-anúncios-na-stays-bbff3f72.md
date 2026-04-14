<!-- title: Especificação Técnica - Criação de Anúncios na Stays | url: https://outline.seazone.com.br/doc/especificacao-tecnica-criacao-de-anuncios-na-stays-MvDeTSxBPO | area: Tecnologia -->

# Especificação Técnica - Criação de Anúncios na Stays

# Mudanças Propostas

## 1. Criação de uma tabela para registrar os eventos de criação de anúncios

Criar uma nova tabela chamada `property_listing` para registrar os eventos de criação de anúncios na Stays. As principais colunas dessa tabela são:

* **property_id**: ID da propriedade;
* **status**: status do anúncio na Stays. Os possíveis valores são:
  * *Not_Created*: anúncio não criado na Stays;
  * *Draft*: anúncio criado como draft;
  * *Active*: anúncio ativo na Stays;
  * *Hidden*: anúncio ativo na Stays, mas marcado como oculto;
  * *Inactive*: anúncio marcado como inativo na Stays;
  * *Cancelled*: esse anúncio não precisa mais ser criado na Stays.

A partir do ID da propriedade, conseguimos recuperar as informações da propriedade para enviá-las à Stays. Se outras informações forem necessárias, elas serão adicionadas futuramente nessa tabela.

## 2. Endpoint para registrar que um novo anúncio deve ser criado

Criar um novo endpoint `POST /property/listings/` para registrar o evento de onboarding, que vai salvar na tabela `property_listing` que um novo imóvel foi adicionado no Sapron.

Esse endpoint também inicia a task de criação do anúncio na Stays (ou seja, a inserção na Stays será feita de forma assíncrona).

## 3. Task para criação de anúncio na Stays

Caso a chamada para a Stays falhe durante o onboarding da propriedade, vamos criar um cronjob para executar a cada 5 minutos para reenviar os dados a Stays.

Para todos os registros na `property_listing` com status "Not_Created", vamos tentar fazer o cadastro do anúncio na Stays. Se a operação for bem sucedida, marcamos o status do anúncio como "Draft".


Abaixo temos um diagrama de sequência mostrando onde a nova rota vai se encaixar no fluxo de onboarding atual.

 ![](/api/attachments.redirect?id=5a021a71-68fc-412d-8a8b-d0e1dc43cd77)

[Editar](https://www.planttext.com/?text=bPEnRW8n38RtF4MKRYUXss-ea53dLgBxoIG68e9pSdoqF4-7laDNNgmve1HE366quo__B-VFD0cmzDkWr29-gYuNtleEIBHPSYIP83bpsr-0tTnfvvlsgRMC8DXs73jasRV19_6qQWNIngXC3J8tu7pWz5FmgxKiGezANIdhoVELOAFVNkVlkWPhOqzIWtECgIu7-eJym7Zye8VcJtvA32qz0LaFuQpXQHUznTQXW0ybD_njkDu2mQh8vWNXFXIjxGAiWLpS8HVvgweHVSv0ggjA_G-EiHauIC9H4sWppe_HOx8WReqsBpiaYTgXjkpXy7tuEXP0Xv-y_cWUZ4xZNPtoQIkuxI83xmS7BclafqmvkGMkZZB7q0y6P_Ti3IiuJIWrpNB3__m5)

# Vantagens e Desvantagens

## Vantagens

* Se a Stays estiver fora do ar durante o onboarding, as outras etapas do fluxo de onboarding não são impactadas;
* Possuimos um mecanismo de retry, para garantir que em algum momento ocorrerá a criação do anúncio na Stays;
* Facilidade para incluir as outras etapas do projeto nesse fluxo, sem impactar o fluxo de onboarding atual. Por exemplo, se for necessário, podemos inserir novas colunas na tabela `property_listing_creation` para realizar outras etapas do projeto, ou podemos também incluir na task a integração com a Pleno, para importar os amenities e enviar para a Stays.

  \

## Desvantagens

* A criação de listing na Stays não ocorrerá em tempo real (embora se a Stays estiver disponível, essa inserção deve ocorrer bem próximo do tempo real);


# Atualização dos anúncios na PropertyListing

Após criar o anúncio na Stays, precisamos acompanhar o status dele para saber se ele foi ativado ou inativado, por exemplo. Isso é especialmente importante, pois precisamos mostrar essa informação na página de status do anúncio. Por isso, a tabela `property_listing` precisa estar com as informações atualizadas na Stays.

A atualização do status do anúncio ocorrerá por dois fluxos: webhook e cronjob.