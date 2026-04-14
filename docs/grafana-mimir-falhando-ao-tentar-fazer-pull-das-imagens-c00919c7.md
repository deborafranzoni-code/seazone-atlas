<!-- title: Grafana Mimir  falhando ao tentar fazer pull das imagens | url: https://outline.seazone.com.br/doc/grafana-mimir-falhando-ao-tentar-fazer-pull-das-imagens-tjm3PcvgEL | area: Tecnologia -->

# Grafana Mimir  falhando ao tentar fazer pull das imagens

## 🕒 Data

23/06/2025

## 🌍 Ambiente

Produção

## ☁️ Cluster / Conta AWS

seazone-prod / EKS Production

## 🚨 Descrição do Incidente

O deployment do Grafana Mimir estava falhando ao tentar fazer pull das imagens do memcached e memcached-exporter do Docker Hub. O erro apresentado foi:

```
Failed to pull image "prom/memcached-exporter:v0.14.4": failed to pull and unpack image "docker.io/prom/memcached-exporter:v0.14.4": failed to copy: httpReadSeeker: failed open: unexpected status code https://registry-1.docker.io/v2/prom/memcached-exporter/manifests/sha256:...: 429 Too Many Requests - Server message: toomanyrequests: You have reached your unauthenticated pull rate limit.
```

Este erro impedia que os pods do memcached fossem criados corretamente, afetando o funcionamento do sistema de cache do Grafana Mimir.

## 🧠 Causa Raiz

**Docker Hub Rate Limiting**: O Docker Hub implementou limites de taxa para downloads não autenticados:

* **Usuários anônimos**: 100 pulls por 6 horas por endereço IP
* **Usuários autenticados gratuitos**: 200 pulls por 6 horas
* **Usuários pagos**: Sem limites

O erro ocorre quando o cluster Kubernetes excede esses limites ao fazer pull de imagens do registry `docker.io`. Isso é comum em ambientes de produção com muitos pods ou deployments frequentes.

**Documentação oficial sobre rate limits**: <https://docs.docker.com/docker-hub/download-rate-limit/>

## 🔧 Ações Corretivas Aplicadas

Atualizadas as imagens no arquivo `values.yaml` do Helm chart do Grafana Mimir para usar registries alternativos:

```yaml
# Alteração 1: Memcached

memcached:
  image:
    repository: public.ecr.aws/docker/library/memcached  # Era: memcached
    tag: 1.6.31-alpine
    pullPolicy: IfNotPresent

# Alteração 2: Memcached Exporter  
memcachedExporter:
  enabled: true
  image:
    repository: quay.io/prometheus/memcached-exporter    # Era: prom/memcached-exporter
    tag: v0.14.4
    pullPolicy: IfNotPresent
```

## ✅ Resultados

* ✅ Eliminação do erro de rate limit do Docker Hub
* ✅ Deploy do Grafana Mimir executado com sucesso
* ✅ Pods do memcached funcionando corretamente
* ✅ Sistema de cache do Mimir operacional

## 🔎 Verificações

Para verificar a resolução:

```bash
# Verificar status dos pods

kubectl get pods -n monitoring | grep memcached

# Verificar logs para confirmar ausência de erros de pull

kubectl logs -n monitoring <memcached-pod-name>

# Verificar se as imagens estão sendo baixadas dos novos registries

kubectl describe pod -n monitoring <memcached-pod-name> | grep "Successfully pulled"
```

## 📝 Recomendações Futuras


1. **Auditoria de Imagens**: Fazer um levantamento de todas as imagens que usam Docker Hub nos charts Helm
2. **Migração Preventiva**: Migrar imagens críticas para registries alternativos como:
   * Amazon ECR Public Gallery (`public.ecr.aws`)
   * [Quay.io](http://Quay.io) (`quay.io`)
   * GitHub Container Registry (`ghcr.io`)
3. **Autenticação Docker Hub**: Configurar credenciais do Docker Hub no cluster para aumentar os limites
4. **Image Pull Policy**: Revisar políticas de pull para evitar downloads desnecessários
5. **Monitoramento**: Implementar alertas para detectar falhas de image pull
6. **Documentação**: Criar guideline interno sobre escolha de registries de imagem

## 🏷️ Tags

\#docker #ratelimit #memcached #grafana-mimir #kubernetes #registry #production

## 👥 Responsáveis

johnpaulo