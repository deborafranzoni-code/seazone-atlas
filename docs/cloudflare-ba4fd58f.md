<!-- title: Cloudflare | url: https://outline.seazone.com.br/doc/cloudflare-ywpLaRYOFe | area: Tecnologia -->

# Cloudflare

## O QUE É?

É uma rede global de servidores e os utilizamos como um proxy reverso.

Podemos afirmar que o Cloudflare é um intermediário entre os visitantes do site (Client) e o servidor de origem (Server).

 ![Untitled](/api/attachments.redirect?id=e668db90-0495-44e8-9e9e-29db6da737e3)

Alguns dos benefícios de se utilizar esse produto são o que ele pode nos oferecer, como camada adicional de segurança, melhora de desempenho, funcionalidades de otimização para melhorar a experiência do usuário e proteção contra ameaças.

* **Mais benefícios**
  * Gerenciamento de DNS;
  * Proteção do site contra usuários indesejados;
  * Redução dos tempos de carregamento de páginas web, com serviço de caching, a minificação de javascript e css, carregamento assíncrono de javascript e otimização de imagens;
  * Distribuição de conteúdos através do sistema CDN;
  * Acelera a resolução do DNS;
  * Redução do consumo do servidor e banda;
  * Suporte para certificados SSL.


---

## API TOKEN

É requerido o uso de **autenticação** para que a **[API da Cloudflare](https://developers.cloudflare.com/fundamentals/api/)** saiba qual cliente está realizando as requisições e quais permissões ele possui.

Para isso podemos **[criar um token](https://developers.cloudflare.com/fundamentals/api/get-started/create-token/)** e também vamos precisar dos id's de zona e conta.

Os id's poderão ser criados e visualizados no canto inferior direito na seção **API** após selecionarmos um site que podemos encontrar no [\*\*dashboard](https://dash.cloudflare.com/login).\*\*

Logo encontraremos algo como:

 ![Untitled](/api/attachments.redirect?id=7806da57-9223-47b0-a270-a3e8759f6a50)

No canto superior direito devemos clicar em [\*\*meu perfil](https://dash.cloudflare.com/profile/api-tokens)\*\* e teremos uma resposta como esta:

 ![Untitled](/api/attachments.redirect?id=7b5c8f1a-407c-414c-a93e-8353468a6598)

Clique em **criar token,** selecione o modelo que melhor se adequa ao seu cenário e configure-o da maneira que lhe convir.

A maioria dos grupos oferece `Edit`ou `Read`opções. `Edit`é o acesso CRUDL completo (criar, ler, atualizar, excluir, listar), enquanto `Read`é a permissão de leitura e listar.


---

### REALIZANDO CHAMADAS DE API

Depois de termos nosso **token de API** criado, todas as solicitações que formos fazer precisarão ser autorizadas da mesma maneira e para ter esta autorização precisaremos passar no header da requisição `Authorization: Bearer <API_TOKEN>` já que o Cloudflare utiliza o **[padrão RFC.](https://tools.ietf.org/html/rfc6750#section-2.1)**

Os endpoints do Cloudflare são fixados em um número de versão e o mais recente é o 4.

**O URL base estável para todos os endpoints da versão 4 é:**

`https://api.cloudflare.com/client/v4/`


---

### CLOUDFLARE IMAGE OPTIMIZATION

Este é um serviço que oferece um conjunto de produtos que possibilita com que realizemos o processamento de imagens.

### Cloudflare Polish

[Cloudflare Polish · Cloudflare Image Optimization docs](https://developers.cloudflare.com/images/polish/)

É um produto que otimiza automaticamente as imagens do nosso site removendo metadados, reduzindo tamanho através de compactação com ou sem perdas para acelerar a velocidade dos downloads e entregas de imagens.

Quando o cliente acessar pela primeira vez uma página que tenha uma imagem otimizada pelo serviço, o Cloudflare irá buscar na origem (servidor) e a imagem ainda não estará armazenada em cache.

No fim da primeira solicitação o Cloudflare realiza o armazenamento desta imagem em cache, logo nas solicitações seguintes ele entregará a versão que está armazenada no sistema de caching que será mais rápida de carregar e estará otimizada da maneira que definimos.

* **Motivos de utilizar o Polish:**
  * **Remover metadados da imagem:**
    * Polish é projetado especificamente para remover metadados de imagens e otimizá-las para acelerar o carregamento do site. Ele faz isso automaticamente quando as imagens são buscadas na origem.
  * **Conversão para diferentes tipos de formatos:**
    * **WebP**
    * **JPEG**
    * **PNG**
  * **Redução da qualidade da imagem:**
    * Polish inclui opções de compactação de imagem que permitem reduzir a qualidade da imagem para otimizá-la. Você pode configurá-lo para alcançar a qualidade desejada ao ajustar as configurações de compactação.

### Compressão com ou sem perdas

**Sem perdas:**

* Remove metadados como dados EXIF sem alterar os detalhes da imagem. Uma imagem descompactada e sem perdas é exatamente igual à original e com um tamanho 21% menor em média.

**Com perdas:**

* Remove metadados e compacta imagens em cerca de 15% e algumas informações redundantes da imagem são perdidas e com um tamanho 48% menor em média.