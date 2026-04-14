<!-- title: Subindo os containers docker das EC2 | url: https://outline.seazone.com.br/doc/subindo-os-containers-docker-das-ec2-SenQnbw2zF | area: Tecnologia -->

# Subindo os containers docker das EC2

Tags: AWS

<aside> ℹ️ **OBS:** Para subir os serviços, é necessário acessar as máquinas via SSH para executar os comandos abaixo. Além disso, é preciso adicionar seu IP no mesmo Security Group e ter em posso o arquivo da chave **toni.pem** para conseguir acessar.

*Para ter esse arquivo, solicite ao @Bernardo Ribeiro*

</aside>

## Como acessar via SSH uma máquina EC2

* Adicione seu IP no mesmo security group que a da instância
* Clique na instância e depois em "Conectar".
  * Basta copiar o comando de exemplo e colar em seu terminal

    ![Untitled](../Gesta%CC%83o%20de%20Conhecimento%20Soluc%CC%A7o%CC%83es%20de%20Suportes%207334c51b7f76445d9f146684a13e687d/Subindo%20os%20containers%20docker%20das%20EC2%20d72f09b8972e4b89a82b0bd0efd2fe54/Untitled.png)

## Subindo os serviços

### Instância **001**

Serviços:

* Redis: `docker start redis`
* OpenSearch: `docker start opensearch-node`

### Instância **002**

Serviços:

* RabbitMQ: `docker start rabbitmq`