<!-- title: Bastion | url: https://outline.seazone.com.br/doc/bastion-zzbHSciPOq | area: Tecnologia -->

# Bastion

Durante a migração da região de Oregon `(us-west-2)` para a região de São Paulo `(sa-east-1)`, o time de governança aproveitou a oportunidade para transferir todos os bancos de dados, que antes eram acessíveis via rede pública, para uma rede privada na nova VPC. Essa mudança gerou a necessidade de criar novos métodos de acesso a esses bancos.


## Acesso via Bastion :globe_with_meridians:

Este é o acesso criado para pessoas que não fazem parte do time de desenvolvimento (gerentes, diretores, time de produto etc.). O acesso é realizado por meio de uma máquina que roteia o tráfego com base nas portas para cada RDS que temos internamente.

:rotating_light: **Para acessar dessa forma é obrigatório estar com a VPN ativada !**

O `HOST` para acessar os bancos será o mesmo para todos, mas utilizamos as portas para diferenciar o acesso a cada banco.

### Sapron

| Chave | valor |
|----|----|
| Host | 18.228.39.169 |
| Port | 5432 |
| Database | sapron-api |
| Username | `<seu_usuario>` |
| Password | `<sua_senha>` |

### Reservas

| Chave | valor |
|----|----|
| Host | 18.228.39.169 |
| Port | 7432 |
| Database | reservas-api |
| Username | `<seu_usuario>` |
| Password | `<sua_senha>` |


### Staging

A dinâmica para staging é um pouco diferente. Como temos um único banco de staging para reservas e Sapron, eles utilizarão a mesma porta e o mesmo host. A diferença estará nas credenciais de acesso, como `database`, `username` e `password`.

| Chave | valor |
|----|----|
| Host | 18.228.39.169 |
| Port | 6432 |
| Database | sapron-api \|\| reservas-api |
| Username | <seu_usuario> |
| Password | <sua_senha> |


## Acesso via Script :dart:

Criamos essa forma para que membros da equipe de desenvolvimento utilizem. Por ser uma conexão interna, não gera custo de transfer out e não representa grande dificuldade para membros com o ambiente de desenvolvimento já configurado.

O script se autentica no cluster Kubernetes, cria um pod temporário com acesso à rede interna e ao banco selecionado, e realiza um `port-forward` para a porta `5432` da sua máquina, permitindo o acesso ao banco via `localhost`.


## 🚀 Execução

```bash

curl -sSfL https://github.com/seazone-tech/bastion-rds/releases/latest/download/bastion-linux-amd64 -o bastion && chmod +x bastion && ./bastion
```

## 🎯 Como Usar


1. **Execute o comando:**

   ```bash
   curl -sSfL https://github.com/seazone-tech/bastion-rds/releases/latest/download/bastion-linux-amd64 -o bastion && chmod +x bastion && ./bastion
   ```
2. **Selecione o ambiente:**

   ```
   [1] STAGING (namespace: stg-apps)
   [2] PRODUCTION (namespace: prd-apps)
   [0] Sair
   
   Digite sua escolha [0-2]: 1
   ```
3. **Confirme a conexão:**

   ```
   Confirma a criação da conexão? [Y/n]: Y
   ```
4. **Aguarde o estabelecimento da conexão:**

   ```
   [CHECK] Verificando pré-requisitos...
   [SERVICE] Verificando serviço bastion...
   [FORWARD] Iniciando port-forward para os serviços...
   ```
5. **Conexão estabelecida com sucesso:**

   ```
   Conexão para PostgreSQL e Redis/Valkey estabelecida com sucesso!
   
   Como conectar:
   
   --- PostgreSQL (RDS) ---
     Host:     localhost
     Porta:    5432
     Exemplo:  psql -h localhost -p 5432 -U postgres
   
   --- Redis/Valkey (ElastiCache) ---
     Host:     localhost
     Porta:    6379
     Exemplo:  redis-cli -h localhost -p 6379
   ```
6. **Para encerrar a conexão:**

   ```
   Pressione Ctrl+C nesta janela para encerrar a conexão.
   ```

## 🔧 Pré-requisitos

* `kubectl` configurado e conectado ao cluster
* Acesso aos namespaces `stg-apps` e `prd-apps`
* Pods bastion rodando nos ambientes

## 🏗️ Desenvolvimento

### Build Local

```bash
# Usar o script de build
./build.sh

# Ou build manual

go build -o bastion .
```

### Deploy no Kubernetes

```bash
# Aplicar os manifests

kubectl apply -f bastion-pod.yaml

# Verificar status

kubectl get pods -n stg-apps -l app=bastion

kubectl get pods -n prd-apps -l app=bastion
```


## 🔍 Verificação de Integridade

Após o download, verifique a integridade do arquivo:

```bash

sha256sum -c bastion-linux-amd64.sha256
```

## 🆘 Troubleshooting

### Erro: "kubectl não encontrado"

```bash
# Instale o kubectl

curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```

### Erro: "Namespace não encontrado"

Verifique se você tem acesso aos namespaces:

```bash

kubectl get namespaces | grep -E "(stg-apps|prd-apps)"
```

### Erro: "Serviço bastion não encontrado"

Verifique se os pods estão rodando:

```bash

kubectl get pods -n stg-apps -l app=bastion

kubectl get pods -n prd-apps -l app=bastion
```