<!-- title: Email de primeiro Acesso - Log Grafana | url: https://outline.seazone.com.br/doc/email-de-primeiro-acesso-log-grafana-fXPqyF4ZRq | area: Tecnologia -->

# Email de primeiro Acesso - Log Grafana

Para procurar se um email foi enviado ao cliente no Grafana podemos procurar



1. Acessar o Grafana de prod: <https://grafana.seazone.com.br/>. Autenticar usando a sua conta Seazone;
2. Clicar na aba `Explore`
3. No campo `Outline`, selecionar "loki";
4. No `label filters`, selecionar "job" "=" "firelens";
5. No campo `Line contains`, inserir o que você quiser buscar.
6. No canto superior direito, você pode também ajustar o tempo de busca. Se inserir um período muito longo, você não vai conseguir buscar. De preferência, busque no máximo em um intervalo de 24h.

 ![](/api/attachments.redirect?id=c0d82b24-9418-4e0c-a9e1-9179f91b8783 " =1249x728")