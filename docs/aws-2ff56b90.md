<!-- title: AWS | url: https://outline.seazone.com.br/doc/aws-sc8segpUV0 | area: Tecnologia -->

# AWS

## Serviços utizados

### **RDS**


---

\*\*Versão: `PostgreSQL 13.13** on x86_64-pc-linux-gnu, compiled by gcc (GCC) 7.3.1 20180712 (Red Hat 7.3.1-12), 64-bit`

**Instâncias**

* `seazone-reservas-prod`: BD do ambiente de Produção
  * seazone-reservas-prod-ro: Réplica de produção para uso em ferramentas de BI
* `seazone-staging`: BD do ambiente de Staging

### **EC2**


---

* RabbitMQ
  * Production: Location → `EC2 (prod-reservas-002)`
  * Staging: Location → `EC2 (stg-reservas-002)`
* OpenSearch
  * Production: Location → `EC2 (prod-reservas-001)`
  * Staging: Location → `EC2 (stg-reservas-001)`
* Redis
  * Production: Location → `EC2 (prod-reservas-001)`
  * Staging: Location → `EC2 (stg-reservas-001)`
* NGINX
  * Production: Location → `EC2 (nginx-website)`

### **ECS**


---

* prod-seazone-reservas
  * seazone-reservas-worker-user (fargate)
  * seazone-reservas-scheduler (fargate)
  * seazone-reservas-api (fargate)
  * seazone-reservas-worker (fargate) → *Possui auto scaling*
* staging-seazone-reservas
  * seazone-reservas-worker-user (fargate)
  * seazone-reservas-scheduler (fargate)
  * seazone-reservas-api (fargate)
  * seazone-reservas-worker (fargate)