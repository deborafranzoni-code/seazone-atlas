<!-- title: NGINX Proxy para roteamento de páginas | url: https://outline.seazone.com.br/doc/nginx-proxy-para-roteamento-de-paginas-BmWJqDtufT | area: Tecnologia -->

# NGINX Proxy para roteamento de páginas

## Por que/para que implementar um proxy?


---

Para explicar precisamos voltar um pouco no tempo. Anteriormente:

* Sob do domínio `seazone.com.br` havia o site em WordPress (WP) que contém toda as páginas institucionais, blog e algumas landing pages.
* Sob o domínio `reservas.seazone.com.br` havia todo o site de reservas (Stays), onde os hóspedes podiam pesquisar destinos e realizar reservas.

Agora, com o desenvolvimento do novo site de reservas, o site institucional hospedado em `seazone.com.br`  (mais especificamente a página Home) e o site de reservas (reservas.seazone.com.br) iriam se tornar apenas um.

Assim, o site de reservas da Seazone ficaria no `seazone.com.br` e a responsabilidade de desenvolver e manter a **Home** seria o time de dev do site (construindo-a em Next.js (outra stack)).

Porém, as outras páginas institucionais, blog e landing pages continuariam sendo mantidas no WordPress, pois não seriam replicadas (por enquanto).

Sendo assim, precisaríamos de uma solução para fazer esse proxy, tratando quais caminhos seriam redirecionados para o WP e quais seriam redirecionados para a [Vercel](/doc/vercel-xJBkgdNzg5) (onde está hospedado o site de reservas). E é nesse ponto que entra o ✨ **NGINX** ✨.


---

## O que é esse tal de NGINX?


---

O NGINX atua como um **Servidor Web**, entregando páginas da web, imagens, arquivos e outros conteúdos para os navegadores dos usuários.

E também funciona como um **Proxy Reverso**, encaminhando solicitações para servidores de aplicativos, equilibrando a carga e melhorando o desempenho.

A configuração do NGINX é feita por meio de arquivos de configuração. Esses arquivos contêm instruções sobre como o NGINX deve responder a diferentes tipos de solicitações.

A versão utilizada no website é a **Open Source**.

> \*\* No nosso caso, estamos usando ele como Proxy Reservo\*


---

## Como foi configurado?


---

| **Serviço** | Plataforma | **Nome** |
|----|----|----|
| EC2 Instância (máquina) | AWS | nginx-website |
| Load Balancer | AWS | website-seazone-elb |
| Target Group | AWS | website-nginx-tg |
| DNS | CloudFlare | seazone.com.br |
| WordPress | Hostinger | seazone.com.br |

 ![Diagrama da arquitetura da implementação do NGINX. Disponível em: ](NGINX%20Proxy%20para%20roteamento%20de%20pa%CC%81ginas%205731a8506d424950bedc6f5a18e2e114/Untitled.png)

Diagrama da arquitetura da implementação do NGINX. Disponível em: **[Miro: Tech/Website > System Design](https://miro.com/app/board/uXjVMqc8v6A=/?moveToWidget=3458764562674470949&cot=14)**

### **Instruções de como foi configurado**

* Levantado um **Load Balancer** na AWS.
* Ele está encaminhando a carga para um **Target Group**
* Esse **Target Group** está apontado para o IP do **Nginx** que está rodando em uma instância (máquina) **EC2**.
* O **Nginx** foi instalado e está rodando em um container Docker.
* No **DNS** foi alterado o apontamento do domínio [seazone.com.br](http://seazone.com.br/) para o **Load Balancer** que criado.

  > *Redireciona para a URL "Nome do DNS" do Load Balancer.*
* Foi criado uma regra simples nesse **Nginx** pra só redirecionar tudo para o IP do site [seazone.com.br](http://seazone.com.br/) .
* Todo tráfego recebido está passando pelo **Nginx** primeiro, ele quem decide para onde será redirecionado.
* Agora com esse **Nginx** em mãos, é possível criar regras pra redirecionar: ou pro site **novo** ou pro **velho**. Ou outra plataforma que esteja usando o domínio [seazone.com.br](http://seazone.com.br)

  > *Consulte o **[arquivo de configuração](https://github.com/Khanto-Tecnologia/seazone-website-nginx/blob/develop/nginx.conf)** do **Nginx** para verificar as páginas configuradas.*

> *Foi realizado um **git clone** do projeto na máquina que está rodando o nginx*

<aside> ⚠️ Qualquer outro endereço fora [dessa lista](/doc/nginx-proxy-para-roteamento-de-paginas-IUy93eKLGM), o usuário será levado para o site novo, e caso a página não exista lá, será retornado um erro **404**.

</aside>


---

## Alteração de configurações do Nginx


---

**Arquivos de configuração**

* **Nginx:** [\*\*nginx.conf](/doc/nginxconf-comentado-linha-por-linha-9e261Eq6cu)\*\*
* **Docker: [docker-compose.yml](https://github.com/Khanto-Tecnologia/seazone-website-nginx/blob/main/docker-compose.yml) e [Dockerfile](https://github.com/Khanto-Tecnologia/seazone-website-nginx/blob/main/Dockerfile)**

### Como adicionar/editar uma `location`?


---

* **Desejo criar uma location nova, como faço?**

  Considerando que já temos o arquivo de configuração pronto, para criar uma nova `location` basta copiar e colar o exemplo de uma que já exista, e alterar os padrões de URLs presentes nela.

  Após isso, modifique os padrões de URL presente na `location`. Para especificar esses padrões de URL, é necessário utilizar Regex.
* **Desejo inserir uma nova URL para fazer proxy para outra maquina (domínio), como faço?**

  Vá na `location` configurada (ou crie uma nova), e acrescente ao final dela o padrão que deseja, por exemplo:

  Desejo add o redirecionamento para o **/blog/**, ficaria:

  ```
  **location ~** /category/?|/category/.***|/blog/?|/blog/.*** **{**
        *# Aqui fica a configuração para essas locations*
  **}**
  ```
  * `/blog/?` → é o caminho da página, a `?` no final é para aceitar tanto com quanto sem a barra "`/`" no final.
  * `/blog/.*` → `.*` indica que tudo que começar com `/blog/alguma-coisa` sera aplicada a configuração.
  * `|` → Significa **"ou".** Lê-se no exemplo: `/blog/? ou /blog/.* ou /category …` será aplicada a configuração.

[nginx.conf comentado linha por linha](/doc/nginxconf-comentado-linha-por-linha-9e261Eq6cu)


---

* **O que são** `Locations`

  As "**locations**" no NGINX são diretivas usadas para definir regras de processamento de URLs específicas. Elas permitem direcionar solicitações HTTP para diferentes blocos de configuração, permitindo controle detalhado sobre como os pedidos são tratados. Cada localização corresponde a um **padrão de URL** ou a uma **expressão regular (regex)**.
  * **Especificação com Regex**

    Expressões regulares (regex) podem ser usadas para criar padrões de matching mais flexíveis nas locations. Isso é útil quando você precisa combinar URLs que seguem um padrão variável.
* **Formas de definir uma** `Location`
  * `location /path`: Especifica uma **location exata** que corresponde a um **caminho específico** na URL.
  * `location ~ pattern`: Usa uma expressão regular para realizar o **matching da URL**. O padrão começa com `~` e é seguido pela regex.
  * `location ~* pattern`: Similar ao anterior, mas faz o **matching sem diferenciar maiúsculas e minúsculas.**
  * `location ^~ /prefix`: Define um **matching exato** e interrompe a busca por outras locations que também poderiam corresponder.
  * `location = /exact`: Define um **matching exato** e interrompe a busca por outras locations.
  * `location /`: Corresponde a **qualquer URL** **que não tenha sido correspondida** por outras locations.

  ```
  **location ~** /path {
      ...
  }
  ```
* **Definindo Múltiplas URLs em uma mesma** `Location`
  * Usando Regex

    Neste exemplo, a expressão regular `^/(path1|path2|path3)` irá corresponder a qualquer URL que comece com `/path1`, `/path2` ou `/path3`.

    ```
    **location ~ ^/**(path1|path2|path3) **{**
        *# Configurações para as URLs path1, path2 e path3*
    **}**
    ```
  * Especificando cada caminho diretamente

    ```
    **location /**path1 **{**
        *# Configurações para a URL /path1*
    **}**
    
    **location /**path2 **{**
        *# Configurações para a URL /path2*
    **}**
    
    **location /**path3 **{**
        *# Configurações para a URL /path3*
    **}**
    ```
* **Configurar cache**

  Para configurar o cache para uma `location` específica, você pode usar a diretiva `proxy_cache` ou `fastcgi_cache`, dependendo do tipo de aplicação sendo atendida. Aqui está um exemplo de configuração básica de cache para uma `location` usando **proxy_cache:**

  ```
  **location /**cached **{**
      **proxy_pass** http://backend_server;
      **proxy_cache** my_cache;
      **proxy_cache_valid** 200 5m;
      **proxy_cache_use_stale** error timeout updating http_500 http_502 http_503 http_504;
  		
  		*# Outras configurações para essa location...*
  **}**
  ```

  Neste exemplo:
  * `proxy_pass` direciona as solicitações para o servidor de backend.
  * `proxy_cache` define o nome do cache a ser usado.
  * `proxy_cache_valid` especifica quanto tempo os itens em cache são considerados válidos.
  * `proxy_cache_use_stale` define como o NGINX lida com solicitações enquanto o cache está sendo atualizado.
* **Boa prática sobre a quantidade de URLs em uma mesma** `Location`

  O NGINX não tem um limite rígido para o número de URLs que você pode definir em uma mesma `location`.

  No entanto, é importante manter a organização e a clareza em sua configuração. À medida que o número de URLs aumenta, a complexidade também aumenta, o que pode dificultar a manutenção e a depuração.

  Se tiver muitas URLs a serem configuradas, considere dividir as configurações em `locations` separadas para facilitar a administração.

  <aside> ℹ️ A eficiência da configuração também é importante. Se você está usando expressões regulares complexas para corresponder a muitas URLs diferentes, pode haver impacto no desempenho do servidor. Sempre teste e avalie o desempenho da sua configuração.

  </aside>

### Como testar se as alterações que fiz irá funcionar?


---

* **Pré-Requisitos**
  * Ter o **docker** e **docker-composer** instalados na máquina
  * Clonar o projeto **[seazone-website-nginx](https://github.com/Khanto-Tecnologia/seazone-website-nginx/tree/main)** na sua máquina
* **1.** **Como rodar | [README](https://github.com/Khanto-Tecnologia/seazone-website-nginx/tree/main#readme)**

  Entre na pasta do projeto e rode o comando:

  ```bash
  docker-compose stop && sudo rm -rf /tmp/nginx-cache && docker-compose up --build --force-recreate -d
  ```

  Em seguida verá uma mensagem que o container foi iniciado: "`✔ **Container seazone-website-nginx-nginx-1 Started**`"

  ![Coloque ](NGINX%20Proxy%20para%20roteamento%20de%20pa%CC%81ginas%205731a8506d424950bedc6f5a18e2e114/Untitled%201.png)

  Coloque `sudo` antes do `docker-compose` caso tenha problemas de permissão.
* **2. Como testar**
  * Acesse `http://localhost/path/`
  * Fazendo isso, é esperado que você veja no browser a página para a qual configurou o redirecionamento.
  * **Por exemplo:**
    * No **[nginx.conf](https://github.com/Khanto-Tecnologia/seazone-website-nginx/blob/main/nginx.conf)** está configurado para que faça proxy para o `/blog/` quando acessarmos esse caminho.
    * Ao informar `http://localhost/blog/` é espero que eu veja na minha tela a página do blog da Seazone.

  <aside> ℹ️ A vercel não aceita muito bem os redirecionamentos com proxy quando vindos do localhost.

  Como alternativa, você pode alterar uma configuração no arquivo `/etc/hosts` na sua máquina, adicionando a seguinte linha:

  ```bash
  127.0.0.1		tonisantes.com.br
  ```

  *Obs: Dê esse espaço entre o IP e o domínio com a tecla tab.*

  Ficará assim:

  ![Untitled](NGINX%20Proxy%20para%20roteamento%20de%20pa%CC%81ginas%205731a8506d424950bedc6f5a18e2e114/Untitled%202.png)

  Após isso, salve as modificações Isso fará com que você consiga acessar o *localhost* informando `tonisantes.com.br`, assim não deverá ter problemas com proxy para Vercel.

  **Por que** `tonisantes.com.br`? Na Vercel na variável ambiente NEXT_PUBLIC_CORS_ALLOWED_ORIGINS\*\*,\*\* foi adicionado o domínio `tonisantes.com.br`. Mas isso pode ser alterado no futuro.

  </aside>

### Como realizar o Deploy das alterações?


---

* **Pré-Requisitos**
  * ⚠️**Leia completamente essas instruções para entender antes de realizar de fato**⚠️
  * *Antes de tudo, caso não tenha testado, [teste sua implementação](/doc/nginx-proxy-para-roteamento-de-paginas-IUy93eKLGM)*
  * Ter enviado as alterações para a branch `develop` no repositório.
  * Ter um login na AWS com permissão para acessar a conta **PRD- Sapron**
* \
  
  1. Conectar com a instância EC2 que está rodando o **nginx**

  > *Considerando que você já logou na sua conta AWS e está na página inicial do console.*
  * No campo de *Search*, procure por "**EC2"** Será a opção que contém: (Virtual Servers in the Cloud)
  * Vá em **Instâncias (em execução)**
  * Clique o **"ID de instância"** da instância **nginx-website**
  * Clique em "**Conectar"** no cano superior direito
  * Clique em **"Conectar"** novamente (botão amarelo)
  * Será aberta uma nova guia e pronto! Nessa aba terá o console para você interagir com a instância via terminal.
* \
  
  2. Acessar pasta do projeto

  Estando no diretório raiz da máquina, rode o comando:

  ```bash
  cd seazone-website-nginx/
  ```
* \
  
  3. Atualizar projeto na instância EC2
  * Rode o comando: `git pull` para obter as últimas alterações

  <aside> ℹ️ Pode ser que o token do github configurado tenha sido expirado. Se for esse o caso você não conseguirá realizar o `pull` das alterações. Sendo assim, siga essas instruções para gerar um novo token: **[Gerar um token de acesso para sua conta do Github](/doc/gerar-um-token-de-acesso-para-sua-conta-do-github-NNcSKGdF3c)**

  Agora use o seguinte comando substituindo **seu_token_aqui** pelo token gerado no passo anterior, para setar o novo token:

  ```bash
  git remote set-url origin https://**seu_token_aqui**@github.com/Khanto-Tecnologia/seazone-website-nginx.git
  ```

  **Pronto!** Só será necessário trocar o token novamente após ele expirar. Agora será capaz de efetuar o `git pull`.

  </aside>
* \
  
  4. Deployar alterações

  4\.1 Acesse a branch **develop**: `git checkout develop`

  4\.2 Rode o comande abaixo:

  ```bash
  docker-compose stop && sudo rm -rf /tmp/nginx-cache && docker-compose up --build --force-recreate -d
  ```

  Esse comando irá **parar o container** em execução, **apagar o cache** e em seguida **irá re-criar a imagem e o container**.

  O deploy é bem rápido, assim que rodar o comando acima verá uma mensagem que o container foi iniciado.

  4\.3 Acesse `seazone.com.br/nova-rota-criada` e veja se suas alterações deram certo. É esperado que ao acessar essa nova rota, você caia na página que esperava cair.

  4\.4 Uma vez que **deu certo** a alteração que realizou, basta você:

  4\.4.1 Enviar suas alterações para a branch `main` no Github

  4\.4.2 (considerando que você está conectado na máquina ainda) atualize o projeto na máquina com o comando: `git pull`

  4\.4.3 Vá para a branch main: `git checkout main`

  4\.4.4 Rode [este comando](/doc/nginx-proxy-para-roteamento-de-paginas-IUy93eKLGM) novamente.

  4\.5 Caso sua alteração **não deu certo**, siga os passos:

  4\.5.1 Volte para a branch `main`.

  4\.5.2 Rode [este comando](/doc/nginx-proxy-para-roteamento-de-paginas-IUy93eKLGM) novamente.

  4\.5.3 Investigue o que causou o insucesso. E e*m caso de dúvida chame o Toni Santes ou Bernardo Ribeiro*


---

<aside> ℹ️ **Tip:** Usar branch `develop` como intermediária para que, caso algo não funcione como esperado, seja feito o rollback a trocando para a branch `main`.

</aside>


---


---

<aside> ℹ️ Caso seja necessário a adição (redirecionamento/proxy) de uma nova página sob o domínio `seazone.com.br/.*` , deverá ser comunicado ao ***Bernardo Ribeiro*** ou ***Toni Santes*** com antecedência (antes de divulgar a página).

</aside>

Para mais informações sobre **nginx** veja a [documentação oficial](https://nginx.org/en/docs/)