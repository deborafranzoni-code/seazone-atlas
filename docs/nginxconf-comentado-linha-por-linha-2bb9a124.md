<!-- title: nginx.conf comentado linha por linha | url: https://outline.seazone.com.br/doc/nginxconf-comentado-linha-por-linha-MRHh2uAujz | area: Tecnologia -->

# nginx.conf comentado linha por linha

```elixir
# Definições globais de eventos
**events {**
  **worker_connections**  1024;  ## Número máximo de conexões simultâneas por trabalhador
**}**

# Configurações globais HTTP
**http {**
  # Configuração do cache proxy
  **proxy_cache_path** /var/cache/nginx levels=1:2 keys_zone=default_cache:10m max_size=4g inactive=120m use_temp_path=off;
  
	# Chave única para identificação do cache
  **proxy_cache_key** "$scheme$request_method$host$request_uri";

  # Define o tempo de validade do cache para 10 minutos
  **proxy_cache_valid** 10m;

  # Bloco de configuração do servidor HTTP
  **server {**
    **listen**  80;  ## Porta em que o servidor nginx irá escutar

    # Location para o caminho /health. 
		# Essa location em específcio serve para o Load Balancer saber que o nginx está UP
    **location =** /health **{**
        **access_log** off;  ## Desativa a gravação de logs de acesso para esta location
        **add_header** 'Content-Type' 'application/json';  ## Define o cabeçalho Content-Type como JSON
        **return** 200 '{"status":"UP"}';  ## Retorna uma resposta JSON com o status "UP"
    **}**

    # Location para as URLs nos padrões especificados. 
    **location ~** /wp-.*|/blog/?|/blog/.* **{**
      # Configuração aplicada a estes padrões de caminhos
    **}**

    # Location padrão para outras URLs
    **location** / **{**
        **proxy_cache** default_cache;  ## Ativa o cache chamado "default_cache"
        **proxy_buffering** on;  ## Ativa o buffering de respostas do servidor de backend
        **proxy_ignore_headers** Expires;  ## Ignora o cabeçalho Expires nas solicitações para o backend
        **proxy_ignore_headers** X-Accel-Expires;  ## Ignora o cabeçalho X-Accel-Expires nas solicitações para o backend
        **proxy_ignore_headers** Cache-Control;  ## Ignora o cabeçalho Cache-Control nas solicitações para o backend
        **proxy_ignore_headers** Set-Cookie;  ## Ignora o cabeçalho Set-Cookie nas solicitações para o backend

        **proxy_hide_header** X-Accel-Expires;  ## Esconde o cabeçalho X-Accel-Expires na resposta para o cliente
        **proxy_hide_header** Expires;  ## Esconde o cabeçalho Expires na resposta para o cliente
        **proxy_hide_header** Cache-Control;  ## Esconde o cabeçalho Cache-Control na resposta para o cliente
        **proxy_hide_header** Pragma;  ## Esconde o cabeçalho Pragma na resposta para o cliente

        **proxy_pass** https://seazone-reservas.vercel.app;  ## Encaminha as solicitações para o servidor em https://seazone-reservas.vercel.app, também pode ser um endereço IP
        **proxy_redirect** off;  ## Desativa a alteração automática de URLs de redirecionamento
        **proxy_set_header** Host seazone-reservas.vercel.app;  ## Define o cabeçalho Host como https://seazone-reservas.vercel.app
        **proxy_set_header** X-Real-IP $remote_addr;  ## Define o cabeçalho X-Real-IP com o endereço IP do cliente
        **proxy_set_header** X-Forwarded-For $proxy_add_x_forwarded_for;  ## Define o cabeçalho X-Forwarded-For para rastrear os endereços IP intermediários
        **add_header** X-GG-Cache-Status $upstream_cache_status;  ## Adiciona um cabeçalho personalizado com o status do cache da resposta
    **}
  }
}**
```