<!-- title: Apontar domínio Seazone para Vercel, removendo a necessidade do NGINX | url: https://outline.seazone.com.br/doc/apontar-dominio-seazone-para-vercel-removendo-a-necessidade-do-nginx-Abs2wdU8aV | area: Tecnologia -->

# Apontar domínio Seazone para Vercel, removendo a necessidade do NGINX

Tags: DNS, NGINX, Vercel

<aside> ℹ️ Atualmente, o DNS do domínio [\*\*seazone.com.br](http://seazone.com.br)\*\* está configurado no CloudFlare, portanto, para realizar os passos a seguir é preciso ter acesso à ele.

Atualmente, a implementação padrão é enviar o tráfego de seazone.com.br para o Nginx, e o Nginx realizará o proxy reverso. *(Vide [NGINX | Proxy para roteamento de páginas](/doc/nginx-proxy-para-roteamento-de-paginas-IUy93eKLGM))*

</aside>

## Apontando domínio Seazone para Vercel

Será necessário alterar o registro "Root" do domínio e o subdomínio `www.`.

Primeiramente, vamos alterar o registro `root` do domínio. Alterando **De:**

```
**CNAME**
seazone.com.br
website-seazone-elb-2008935346.us-west-2.elb.amazonaws.com 
*(DNS Only, non proxied)*
```

**Para:**

```
**A**
seazone.com.br
76.76.21.21 
*(DNS Only, non proxied)*
```

<aside> ℹ️ Recomendo conferir nas configurações de Domínio da Vercel para verificar se o endereço IP e cname foram alterados. <https://vercel.com/seazone-reservas-team/seazone-reservas/settings/domains>

</aside>

Agora, alteramos o registros do subdomínio **www.** Alterando **De:**

```
**A**
www
192.0.2.1 
*(Proxied)*
```

**Para:**

```
**CNAME**
www
cname.vercel-dns.com 
*(DNS Only; Non-proxied)*
```

<aside> ℹ️ Após aplicar essas alterações, é preciso conferir na vercel a geração do certificado SSL. Isso pode levar alguns minutos até as alterações serem propagadas.

</aside>

## Apontando domínio Seazone para NGINX

Primeiramente, vamos alterar o registro `root` do domínio. Alterando **De:**

```
**A**
seazone.com.br
76.76.21.21 
*(DNS Only, non proxied)*
```

**Para:**

```
**CNAME**
seazone.com.br
website-seazone-elb-2008935346.us-west-2.elb.amazonaws.com 
*(DNS Only, non proxied)*
```

Agora, alteramos o registros do subdomínio **www.** Alterando **De:**

```
**CNAME**
www
cname.vercel-dns.com 
*(DNS Only; Non-proxied)*
```

**Para:**

```
**A**
www
192.0.2.1 
*(Proxied)*
```

<aside> ℹ️ Após aplicar essas alterações, é preciso conferir na vercel a geração do certificado SSL. Isso pode levar alguns minutos até as alterações serem propagadas.

</aside>