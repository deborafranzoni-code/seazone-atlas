<!-- title: Infraestrutura VPN GCP | url: https://outline.seazone.com.br/doc/infraestrutura-vpn-gcp-1y1whoZT3A | area: Tecnologia -->

# Infraestrutura VPN GCP

# vpn-seazone

## Como o projeto foi construído

1 - Criar uma instância com os arquivos necessários para rodar o pritunl

* o script de instalação pode ser encontrado em `./commands/oldvm.sh`
* exemplo criando uma instancia com cli 👇 `gcloud compute instances create instancia-teste \   --zone=us-central1-a \   --machine-type=e2-micro \   --image-family=debian-11 \   --image-project=debian-cloud \   --boot-disk-size=10GB `

2 - Criar uma imagem a partir da instância configurada.

* Comando para criar uma imagem 👇 `gcloud compute images create minha-imagem \   --source-disk=nome-da-instancia \   --source-disk-zone=us-central1-a \   --family=nome-da-familia \`

3 - Criar um disco de armazenamento externo que será integrado na instância

* Comando para criar um disco `gcloud compute disks create nome-do-disco \   --size=tamanho-do-disco \   --zone=zona-da-instancia \   --type=tipo-do-disco `

4 - Criar um template de instância baseado na imagem criada anteriormente, vinculando o disco de armazenamento externo ao template.

* o código terraform de criação do template pode ser encontrado em `./main.tf`

5 - Configurar no template um script para montar o disco de armazenamento na pasta que o mongoDB guarda seus dados.

* O script mencionado acima pode ser encontrado em `./commands/vm.sh`

6 - Criar um grupo de instâncias a partir do template de imagem criado para que a aplicação seja reestabelecida caso algum problema ocorra na instância

* o código terraform de criação do grupo pode ser encontrado em `./main.tf`

## Como o projeto foi construído

## Recursos usados no projeto

* [ Compute address](https://cloud.google.com/config-connector/docs/reference/resource-docs/compute/computeaddress) - Pra gerar o IP do pritunl
* [Instance template](https://cloud.google.com/compute/docs/instance-templates/create-instance-templates) - Pra gerar o modelo que seria utilizado pelo grupo de instâncias
* [ Compute instance group manager](https://cloud.google.com/compute/docs/reference/rest/v1/instanceGroupManagers) - Pra configurar a persistência da aplicação
* [Mongodb](https://hub.docker.com/_/mongo) Para persistir os dados do pritunl

## Como o projeto está estruturado

 ![](/api/attachments.redirect?id=5d334555-10be-4701-8059-1176ec6ddee9)