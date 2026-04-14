<!-- title: Setup de serviços que rodam nas EC2 em container Docker | url: https://outline.seazone.com.br/doc/setup-de-servicos-que-rodam-nas-ec2-em-container-docker-li81UTgq7b | area: Tecnologia -->

# Setup de serviços que rodam nas EC2 em container Docker

### Instalando docker

Instala: `sudo yum install docker`

Habilita o docker na máquina: `sudo systemctl enable docker.service`

Inicia o serviço do Docker: `sudo systemctl start docker.service`

Verifica o status do docker service: `sudo systemctl status docker.service`

Verificar se o docker está rodando: `docker ps`

### ???

```bash
sudo usermod -a -G docker ec2-user
```

```bash
id ec2-user
```

```bash
newgrp docker
```

## Setup dos Serviços

### Redis

```bash
docker run -p 6379:6379 --name redis -d redis:alpine redis-server --maxmemory-policy volatile-lru --maxmemory 8Gb
```

```bash
docker restart redis
```

### OpenSearch

```bash
sudo docker run -p 9200:9200 -p 9600:9600 -e "discovery.type=single-node" --name opensearch-node -d opensearchproject/opensearch:latest
```

Testa se o OpenSearch está rodando:

* `curl -XGET 'localhost:9200/_cat/allocation?v'`
* `curl  http://:9200/_nodes/stats/fs?pretty=1`

### RabbitMQ

```bash
docker run -p 5672:5672 -p 15672:15672 --name rabbitmq -e RABBITMQ_DEFAULT_USER=admin -e RABBITMQ_DEFAULT_PASS=<PASSWORD> -d rabbitmq:3.11-management
```