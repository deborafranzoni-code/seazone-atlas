<!-- title: Integração Advertiser Awin | url: https://outline.seazone.com.br/doc/integracao-advertiser-awin-jOz52xFHi3 | area: Tecnologia -->

# Integração Advertiser Awin

# A Awin

A Awin é uma plataforma de afiliados marketing que possibilita anunciantes (Advertisers; lojas) ficarem a disposição de "vitrines", os publishers (afiliado do anunciante) para que sejam anunciados em suas plataformas por eles.

Publishers podem se afiliar à Adivertisers para anunciar o site/produtos do Advertiser e com isso, ganhar uma comissão em cima das vendas realizadas que originaram do Publisher, além de quem compra poder ganhar cashback ou ter promoções especiais. 

Dando um exemplo prático: através da Awin nós Seazone (Advertiser) poderemos colocar nosso site de reservas a disposição para ser promovido (anunciado) na vitrine de plataformas como a Méliuz (Publisher), Cuponomia (Publisher), etc. Isso aumentaria nossos acessos, e consequentemente, as vendas; além de fidelizar nossos clientes oferecendo um programa de cashback (por exemplo).


**Objetivo da integração:** Obter mais acessos e eventualmente o aumento do faturamento do site de reservas.

**Será um sucesso se:** …


> Plano contratado da Awin: **Access**

# INTEGRAÇÃO TRACKING


Fluxo de integração e comunicação com a Awin usando a integração via Tag Manager


\
## Tracking: Client-Side

[https://youtu.be/GEtI82ZJIrk](https://youtu.be/GEtI82ZJIrk)

> ***Doc: <https://developer.awin.com/docs/gtm-client-side>***
>
> ***Doc: ****<https://developer.awin.com/docs/client-side-tracking-1>*

Para integrar o tracking client-side da Awin via Google Tag Manager (GTM), é necessário preparar os elementos principais:

### MasterTag

*==…. Detalhar aqui a config do MasterTag …==*


### **Last Click Identifier Tag**

> Esta tag cria e mantém um cookie que guarda a referência do último clique pago (afiliado) que trouxe o usuário ao site. Essencial para assegurar que o afiliado responsável será creditado pela venda.


### ConversionTag

*==…. Detalhar aqui a config do ConversionTag …==*


### Variáveis

> Variáveis são usadas para capturar dados importantes como o valor da compra, o ID do pedido, e o valor do cookie que identifica o canal afiliado. Esses dados são a base para enviar informações corretas de conversão.


### Trigger de Confirmação de Pagamento

> Um gatilho configurado para disparar a tag de conversão somente no momento em que o usuário finaliza a compra, a ideia é enviar o evento após recebermos o webhook de pagamento bem sucedido e redirecionar o usuário para a página de reserva paga.


### Fallback Conversion Pixel

> ***Doc: <https://developer.awin.com/docs/fall-back-conversion-pixel>***

*==TODO: Verificar se é necessário, caso não for, informar aqui o motivo==*


### Consent Framework (consentimento de uso de cookies)

Como anunciante é nossa responsabilidade obter o consentimento do usuário para uso de cookies. Caso não usemos este framework a Awin vai assumir já pedimos e o usuário consentiu.

> *Referência: <https://developer.awin.com/v1/docs/consent-framework>*


\
## Tracking: Server-Side

> ***Doc: ****<https://developer.awin.com/docs/server-side-tracking>*

De acordo com a **[documentação](https://developer.awin.com/docs/gtm-client-side#:\~:text=Server%2Dto%2DServer%20Tracking)** de tracking usando o Google Tag Manager, podemos escolher uma opção - que for mais conveniente para nós - dentre essas 3 opções para realizar a integração no server-side para informar o evento de compra à Awin:

#### **[Server-side GTM](https://developer.awin.com/docs/s2s-via-gtm) ou [Stape](https://stape.io/solutions/awin-tag)**

Opção low code para implementar o tracking no Server-Side.

**Prós:**

* Solução No-Code
* Captura automática do evento, sem intervenção do lado do backend/api
* Possibilidade de implementar independente do plano contratado

**Cons:** ![](/api/attachments.redirect?id=1fc74ba4-0d39-47eb-87b6-6350cb0de57d "right-50 =169x211")

* Vários passos de setup necessários para ser realizados no GTM (mais tags a ser configurada) e GCP
* Requer uso do Google Cloud (GCP), do serviço Cloud Run (possível geração de custo com Cloud Run; tem free tier, ver img ao lado)
* Necessidade de um novo subdomínio específico para capturar o evento de compra
* *Solução de Integração é desenvolvida e mantida por um parceiro da Awin ([Stape](https://stape.io/)).*


\
#### **[Server-side tracking via Conversion API](https://developer.awin.com/apidocs/conversion-api)**

Opção que podemos implementar do nosso lado para informar em batches à Awin as reservas/pedidos realizados. Essa é uma forma mais segura e autenticada de comunicar com a Awin.

**Limites**

* 1000 pedidos/reservas por request
* Máx. 20 requests por minuto por user

**Prós:**

* Implementação mais simples, diretamente do nosso lado
* Segurança: Comunicação autenticada com a Awin usando uma api-key
* exportação em batch (limite 1000/request)
* webhook com retorno de erro/sucesso na captura de um evento, podemos criar alertas para esses erros.
* Método **recomendado** pela Awin (sendo uma alternativa, o server-side do GTM)\n*==Podemos perguntar diretamente à eles qual seria o método preferível entre ConversionAPI e GTM Server-Side==*

**Cons:**

* Delay de 3 minutos para o evento aparecer na plataforma da Awin após o envio da request.
* *Advertiser APIs are only available for the **Awin Accelerate** and **Advanced plans**.*

  ***==TODO==****==: Verificar qual plano contratamos. Verificar se podemos usar a Conversion API==*\n*==Realizei um teste pelo Postman e consegui enviar a requisição para Awin pra capturar o evento no server-side e ele apareceu lá na Awin, mesmo estando no plano Access. Mas é importante confirmar com eles se podemos usar esse meio. Caso não seja possível, devemos usar o **GTM Server-Side**==*


#### **[Server-side tracking via Direct Implementation](https://developer.awin.com/docs/direct-s2s)**

Podemos usar esse método para enviar o evento diretamente para a Awin, porém a Awin **altamente recomenda** a opção tracking via Conversion API.

**Prós:**

* :thinking_face:
* Possibilidade de implementar independente do plano contratado

**Cons:**

* Não recomendado pela Awin, é preferível usar a ConversionAPI
* Setup maior, requer mais controle do nosso lado sobre os cookies


\

\
### GTM Server-Side com Stape

> **Docs:**
>
> * Doc principal: <https://stape.io/blog/awin-server-to-server-tracking-using-server-google-tag-manager#how-to-set-up-awin-server-to-server-tracking-using-server-to-server-tracking-gtm>
> * <https://developer.awin.com/docs/gtm-s2s>
> * <https://stape.io/solutions/awin-tag>


**Step 1: Fazer setup de um novo container do tipo Server**

O container atual do GTM que possuímos é do tipo Web (roda em páginas web), precisamos criar um do tipo Server (para instrumentação do tracking do lado do servidor).

Vamos seguir essa doc até o step 4: [https://stape.io/blog/how-to-set-up-google-tag-manager-server-side-container](https://stape.io/blog/how-to-set-up-google-tag-manager-server-side-container#step-4-create-a-google-tag-inside-the-web-gtm-container)

> **Step 1.1: Criar Server container no GTM**
>
> Siga este guia para __[criar e configurar um container de servidor do Google Tag Manager](https://stape.io/blog/how-to-set-up-google-tag-manager-server-side-container)__.
>
> \
> **[Step 1.2: Criar container sGTM na plataforma Stape](https://stape.io/blog/how-to-set-up-google-tag-manager-server-side-container#step-2-create-a-stape-account-to-host-your-server-gtm-container)**
>
> O **Stape** é a plataforma que usaremos para fazer a conexão entre o GTM Server e a Awin. Precisamos criar uma conta lá e então criar um container. 
>
> \
> **[Step 1.3: Configurar um domínio customizado para o container ](https://stape.io/blog/how-to-set-up-google-tag-manager-server-side-container#step-3-configure-a-custom-tagging-server-url)**
>
> Isso é altamente recomendado para que seja possível utilizar 1st-party cookies. Dessa forma, nós "mascaramos" o domínio do gtm ou stape para que possamos usar os first-party cookies.
>
> Para realizar isso podemos fazer de 3 formas: **same origin**, **subdomain** e **default domain** (o que já é fornecido pela Stape ao criar o container).
>
>  ![https://stape.io/blog/how-to-set-up-google-tag-manager-server-side-container#step-3-configure-a-custom-tagging-server-url](/api/attachments.redirect?id=eea6bb7b-108b-482d-be61-5ae44bb33708 " =802x450")
>
> Em nosso setup vamos utilizar um subdomain:
>
> * **Staging:**      `sst-stg.seazone.com.br`
> * **Produção:**  `sst.seazone.com.br`
>
> > `sst` *é a sigla para **S**erver-**S**ide-**T**racking*
>
> \
> **Step 1.4 Configurar DNS**
>
> Configurar o novo subdominio para fazer um proxy para a url da stape. ![Sub-domínios criados para serem usados com o Stape.io](/api/attachments.redirect?id=4c6aab33-e5ca-447d-84b2-d5de1e7c0e17)
>
> Após criar os DNS no CloudFlare, é preciso validá-lo no Stape  ![Após validar o domínio, ele ficará dessa forma com status "Ready" ao lado do domínio.](/api/attachments.redirect?id=8484caa7-f29f-4caf-9801-d072d4421514)
>
> \
> **Step 1.5: Colocar subdomínio de tracking no container no GTM**
>
> Usaremos uma variável única com o valor da URL para fique simples a alteração futura, caso necessário. Padronizaremos a variável com o nome: `{{GTM Server URL}}`


**[Step 2: Configurar envio dos dados do Client (DataLayer) para o container do Server](https://stape.io/blog/sending-data-from-google-tag-manager-web-container-to-the-server-container#how-to-send-data-from-the-google-tag-manager-web-to-the-server-container)**

Pelo fato de o container Web (Client) e Servidor (server) serem containers distintos, precisaremos fazer o envio das informações do client para o server. Para realizar isso há dois caminhos: [setting up server-side Google Analytics 4 tracking](https://stape.io/blog/set-up-ga4-server-side-tracking)  ou  [Data Tag/Data Client](https://stape.io/blog/sending-data-from-google-tag-manager-web-container-to-the-server-container).

Precisamos fazer isso para que o evento disparado do lado do server consiga ter acesso aos dados dos eventos que estão no Data Layer, pois é lá que estão as informações que serão enviadas para a Awin.

Foi testado as duas maneiras, e escolhemos usar o **DataTag/Data Client** pelo fato dela ter sido a que funcionou sem dificuldades. Além disso, economizaria chamadas à Stape, visto que a DataTag só será chamada caso ocorra um evento de conversão.

* No Container Web (client) **criamos uma** **DataTag** com nome `DataTag - Conversion Event` que enviará para o Server tendo como **trigger** o mesmo evento de conversão usado pela **ConversionTag** eventos de conversão. Na DataTag, podemos configurar para enviar os dados que desejamos. Esses dados são relacionados ao evento capturado, que nesse caso, foi o evento de `purchaseSuccess` que é o trigger dessa Tag.\n**\[Seguir steps 1 a 4 da [doc](https://stape.io/blog/sending-data-from-google-tag-manager-web-container-to-the-server-container#how-to-send-data-from-the-google-tag-manager-web-to-the-server-container)\]**


* No Container Server (server) criaremos uma nova tag **DataClient** para irá obter os dados da DataTag. Essa Tag será criada com base no **[template (modelo)](https://github.com/gtm-server/data-client)** fornecido na doc da Stape \n**\[Seguir steps 5 a 8 da [doc](https://stape.io/blog/sending-data-from-google-tag-manager-web-container-to-the-server-container#how-to-send-data-from-the-google-tag-manager-web-to-the-server-container))**


\
## Product Level Tracking

> ***Doc: <https://developer.awin.com/docs/product-level-tracking-2>***

Optional, offers detailed product-specific reporting.


\
## Teste de Integração

> ***Doc: <https://developer.awin.com/docs/testing-your-integration>***
>
> 
> 1. Acessar a Awin e acessar o menu **"[Support > Tracking Diagnosis](https://ui.awin.com/advertiser-integration-tool/trackingwizard/us/awin/merchant/107484)"**
> 2. Clicar em "Create a test transaction" e acessar o link gerado
> 3. Copie a URL. *Ps.: Altere o domínio para* `stg.seazone.com.br` *para testar usando o ambiente de staging*
> 4. Iniciar modo debug/preview do GTM (fazer isso para o GTM Server e GTM Web (client).\nPara habilitar, clique nesse botão de "Visualizar" (ou Preview).
>    * No container Web, você precisará colocar a URL que copiou no **passo 3** do ambiente que deseja
>    * No container Servidor, irá abrir uma aba que irá mostrar os eventos que ocorrerem do lado do servidor conforme ele for ocorrendo.
>
>    ![](/api/attachments.redirect?id=2f3dd5b5-bafe-4c8b-b4cb-62dd24d16ff2 " =1604x175")
> 5. Realizar uma reserva para haver a captura do evento de conversão.\nAqui haverá 2 alternativas para o pagamento
>
>    
>    1. Simular webhook de pagamento capturado: Nesse caso será necessário selecionar o PIX como meio de pagamento
>    2. Pagar de verdade.
> 6. Validar nas abas de Debug do GTM se houve a captura do evento `purchaseSuccess` 
> 7. Validar que na Awin > Tracking Diagnosis apareceu a transação que acabou de realizar
> 8. Aguardar \~3min e Validar que na tela de comissões apareceu a comissão referente a reserva que acaboud e pagar.
> 9. (caso tenha testado em produção) lembrar de cancelar a reserva e estornar o pagamento (se necessário)


# INTEGRAÇÃO PRODUCT FEEDS

> ***Doc: ****<https://developer.awin.com/docs/product-feed-intro>*

*==TODO: Verificar se é necessário essa integração==*


# MONITORAMENTO

**Métricas**

* KPI Acessos por dia
* KPI Reservas com origem do programa de Afiliados: Count e Percent
* KPIs Core Web Vitals
* Requests por minuto por API: Search, Detalhes do Imóvel, Verificação de Preço & Disponibilidade, Checkout
* Latência por minuto por API: : Search, Detalhes do Imóvel, Verificação de Preço & Disponibilidade, Checkout


# Links úteis

* **[Why hybrid tracking is essential for your affiliate programme - here's what you need to know](https://advertiser-success.awin.com/s/article/Why-hybrid-tracking-is-essential-for-your-affiliate-programme-here-s-what-you-need-to-know?language=en_GB):** *Esse artigo explica o por que do tracking hibrido que mesclar **client-side** e **server-side** tracking e contém links para os respectivos Guias.*
* [Tracking Overview](https://developer.awin.com/docs/tracking) (mais detalhada que o guia fornecido pela UI da Awin): *Este link leva para documentação de tracking com guias de como implementar e testar o tracking, que no nosso caso é a integração é via **[Google Tag Manager ](https://developer.awin.com/docs/gtm-client-side)**no client e usado uma das opções de server-side apresentadas na doc**.***
* **[Awin API Docs](https://developer.awin.com/apidocs/introduction-1):** *Documentação de API da Awin.*
* [GTM Client Side tracking](https://developer.awin.com/docs/gtm-client-side): Guia de como implementar o tracking no client-side usando o Google Tag Manager.
* **[Conversion API](https://developer.awin.com/apidocs/conversion-api):** API usada do lado do servidor para informar as compras realizadas originadas dos afiliados à Awin.
* **[How can I integrate server-to-server tracking?](https://advertiser-success.awin.com/s/article/How-can-I-integrate-server-to-server-tracking?language=en_US)**
* **[Technical Guides](https://advertiser-success.awin.com/s/topic/0TO2p000000Qol0GAC/technical-guides?language=en_US)**


# Glossário

* **Awin:** Empresa que usaremos para o programa de afiliados.
* **Advertisers & Publishers**
  * **Advertiser**: É quem está anunciando, os marketplaces. Exemplo: Seazone (nós), Magalu, etc.
  * **Publisher**: É quem publica os anúncios, são as "vitrines" que vão promover os marketplaces. Exemplo: Méliuz, Cuponomia, etc.
* **Affiliate (afiliados):** Afiliados e Publishers são a mesma "pessoa". Os 'Publishers' (afiliados) se afiliam à anunciantes (Advertisers) para anunciar seus produtos e/ou plataforma.
* **Commission Groups:** É a configuração do quanto de comissão pagaremos ao parceiros (publishers)**. Na página** Commission Manager (**Commission > Commission Manager**) é onde podemos configurar as comissões dos parceiros.
* **Google Tag Manager (GTM)**: Ferramenta de Tracking & Analytics da Google.


**Siglas na nomenclaturas utilizadas no GTM**

* **DC**: Data Client
* **DT**: Data Tag
* **ED**: Event Data
* **S2S**: Server-To-Server