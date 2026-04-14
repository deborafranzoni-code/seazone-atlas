<!-- title: Infraestrutura Da Vpn AWS | url: https://outline.seazone.com.br/doc/infraestrutura-da-vpn-aws-YT4b6uCBMN | area: Tecnologia -->

# Infraestrutura Da Vpn AWS

# Pritunl

O Pritunl foi configurado com terraform neste [repositório](https://github.com/Khanto-Tecnologia/terraform) e esta em uma instância EC2 na região de São Paulo (sa-east-1). A instância foi criada a partir de uma imagem, que foi configurada manualmente conforme a documentação do [Pritunl](https://docs.pritunl.com/docs/configuration-5). A configuração do pritunl pode ser visualizada com o comando `pritunl get app`. Esta imagem também possui um mongodb com o seu volume no diretório `/data/mongod`.

# Disponibilidade e Confiabilidade

 ![pritunl.drawio.png](/api/attachments.redirect?id=0b58b247-55a0-45e3-81b5-c21d1c693863)

O terraform que foi utilizado para configurar o Pritunl conta com um `Auto-Scale` configurado para manter uma instância ativa, que utiliza como base um `Lauch Template` com a imagem previamente configurada.

Como o MongoDb precisa que os dados sejam mantidos com confiabilidade, no `userdata`um `EFS` é montado no diretório `/data/mongodb`.

A Cloudflare é utilizada para fazer o roteamento do ip para o dns \[`seazone.com.b](http://seazone.com.br)r` e foi utilizada para gerar o certificado de origin do Pritunl.