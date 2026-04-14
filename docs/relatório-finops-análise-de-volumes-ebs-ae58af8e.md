<!-- title: 📊 Relatório FinOps: Análise de Volumes EBS | url: https://outline.seazone.com.br/doc/relatorio-finops-analise-de-volumes-ebs-tkvMgz3TVj | area: Tecnologia -->

# 📊 Relatório FinOps: Análise de Volumes EBS

# 📊 Relatório FinOps: Análise de Volumes EBS

**Data de Geração:** 2026-03-18 13:59:44 **Região AWS:** `sa-east-1`

## 📌 Resumo Executivo

Este relatório mapeia todos os volumes EBS na conta e os cruza com o estado atual do cluster Kubernetes (Persistent Volumes). O principal objetivo é identificar **Desperdício (Volumes Órfãos)** que continuam gerando custos mesmo sem estarem atachados a nenhuma instância ou em uso pelo K8s.

| Categoria | Quantidade de Volumes | Tamanho Total (GB) | Custo Estimado (Mês) |
|:---|:---:|:---:|:---:|
| ⚠️ **Volumes Órfãos (Desperdício)** | 64 | **562 GB** | **$51.14** |
| ✅ Volumes em uso pelo Kubernetes | 87 | 2797 GB | $254.53 |
| 🖥️ Volumes atachados a instâncias EC2 | 31 | 628 GB | $57.15 |
| **Total Geral** | **182** | **3987 GB** | **$362.82** |

> *Nota: A estimativa de custo utiliza um valor base aproximado de $0.091 por GB/mês (tipo gp3 na região sa-east-1). Valores podem variar de acordo com IOPS e Throughput adicionais provisionados.*


---

## ⚠️ Oportunidade de Redução de Custos (Volumes Órfãos)

## Estimativa de Economia — 64 Volumes Órfãos

 ![](/api/attachments.redirect?id=1c0f9ec5-503e-4b0e-90d3-24c13e9aa869 " =835x299")


Estes volumes estão com status `available` (não atachados a nenhuma instância) e não constam na lista de PVs do Kubernetes. **São fortes candidatos a deleção.**

| Volume ID | Nome (Tag) | Tamanho | Tipo | Status | PVC Original (se houver) | Custo Mensal |
|:---|:---|:---:|:---:|:---:|:---|:---:|
| vol-0de23689e03e43957 | general-cluster-dynamic-pvc-1f979b02-e76e-4b72-bc6a-3c5b5411b541 | 32 GB | gp3 | available | kubecost/kubecost-local-store | $2.91 |
| vol-033bee90b614a27d1 | general-cluster-dynamic-pvc-a9a25e6f-9a74-4d4f-8dae-717d6dc598de | 32 GB | gp3 | available | kubecost/kubecost-local-store | $2.91 |
| vol-0f80c7bc3ca311d2c | general-cluster-dynamic-pvc-484caec9-a718-41c6-8783-2792a8190f1c | 32 GB | gp3 | available | kubecost/kubecost-local-store | $2.91 |
| vol-03962df7fad6f68ae | general-cluster-dynamic-pvc-030cb739-5772-465f-a691-e4e55d4cf625 | 32 GB | gp3 | available | tools/kubecost-local-store | $2.91 |
| vol-0714aea6ab98952a2 | general-cluster-dynamic-pvc-1d00d508-292f-490d-8045-edf28daf9cef | 32 GB | gp3 | available | kubecost/kubecost-local-store | $2.91 |
| vol-0060e61b58daef283 | general-cluster-dynamic-pvc-71758270-f1ed-4c06-af25-b44fb256f0b2 | 20 GB | gp3 | available | kubecost/aggregator-db-storage-kubecost-aggregator-0 | $1.82 |
| vol-0981b6f74a1ef9033 | general-cluster-dynamic-pvc-4a5e0be0-e625-42e4-8716-16e7ddd1bdb9 | 20 GB | gp3 | available | kubecost/aggregator-db-storage-kubecost-aggregator-0 | $1.82 |
| vol-0ec650794e2279e5c | general-cluster-dynamic-pvc-9fa0e86d-4c3d-4fd6-8434-5eaeef92d5fe | 20 GB | gp3 | available | kubecost/aggregator-db-storage-kubecost-aggregator-0 | $1.82 |
| vol-0f1f432012ae9b136 | general-cluster-dynamic-pvc-27cd04c6-f4d7-4470-a100-1e2348a78f65 | 20 GB | gp3 | available | tools/aggregator-db-storage-kubecost-aggregator-0 | $1.82 |
| vol-00c1524ea819dc342 | general-cluster-dynamic-pvc-25283402-a9ad-4c27-8064-2d7a23cfe69b | 20 GB | gp3 | available | kubecost/aggregator-db-storage-kubecost-aggregator-0 | $1.82 |
| vol-006c72847a622b4e7 | general-cluster-dynamic-pvc-26610ef4-bd03-4bae-b435-bce901b05aa4 | 15 GB | gp3 | available | monitoring/storage-mimir-compactor-0 | $1.36 |
| vol-0c9c0ce217fb082a9 | general-cluster-dynamic-pvc-da35549c-0b9a-4de7-8475-6caa9c0b56af | 15 GB | gp3 | available | monitoring/storage-grafana-mimir-compactor-0 | $1.36 |
| vol-059c81d9d2ceeaf89 | general-cluster-dynamic-pvc-8c5c0775-4f42-4026-beab-622c5d993601 | 10 GB | gp3 | available | kubecost/persistent-configs-kubecost-aggregator-0 | $0.91 |
| vol-041cdb7df28300a1e | general-cluster-dynamic-pvc-391de9f7-f7b9-40bf-bf63-a2275e0ebe5a | 10 GB | gp3 | available | tools/persistent-configs-kubecost-aggregator-0 | $0.91 |
| vol-07bcbb329994ec670 | general-cluster-dynamic-pvc-e3d937f0-afb1-4674-8709-4f66535bd8ac | 10 GB | gp3 | available | monitoring/data-loki-backend-0 | $0.91 |
| vol-0955cce22bf4b5974 | general-cluster-dynamic-pvc-fe3f1a4c-4039-4e6d-aa1a-9c3de8af4c22 | 10 GB | gp3 | available | monitoring/grafana | $0.91 |
| vol-05122808d69f15a62 | general-cluster-dynamic-pvc-d4cd0d58-ac2a-4391-8066-d0b46e26ddab | 10 GB | gp3 | available | monitoring/grafana | $0.91 |
| vol-049a1d48e1105b7fd | general-cluster-dynamic-pvc-0a3e5202-4e97-4d69-b33b-0dba20d20cee | 10 GB | gp3 | available | kubecost/persistent-configs-kubecost-aggregator-0 | $0.91 |
| vol-0866f64570dc85f43 | general-cluster-dynamic-pvc-643c4d52-2fd0-4a7b-a695-cb5c0fe2181c | 10 GB | gp3 | available | monitoring/data-loki-backend-1 | $0.91 |
| vol-09489dea50755cc7d | general-cluster-dynamic-pvc-07302919-6c34-43c8-893a-5c2a4bdb413b | 10 GB | gp3 | available | kubecost/persistent-configs-kubecost-aggregator-0 | $0.91 |
| vol-0a31baf3dda5a0a30 | general-cluster-dynamic-pvc-88fa1ed5-f564-4dd8-8d3f-4110c33c088f | 10 GB | gp3 | available | monitoring/grafana | $0.91 |
| vol-0de4576fdc9b3780b | general-cluster-dynamic-pvc-c1920a64-eaf6-4243-a4bf-844aa0fc3527 | 10 GB | gp3 | available | monitoring/data-loki-backend-2 | $0.91 |
| vol-0cef870ece1ea2175 | general-cluster-dynamic-pvc-0130a412-9cc3-4070-b4da-adc2d290b81d | 10 GB | gp3 | available | monitoring/grafana | $0.91 |
| vol-061250f7ac8ec4cf3 | general-cluster-dynamic-pvc-d0ae3ae9-80a7-499f-b1cd-b2d4e309598d | 10 GB | gp3 | available | kubecost/persistent-configs-kubecost-aggregator-0 | $0.91 |
| vol-0aecb3027f64e730f | general-cluster-dynamic-pvc-eb091a91-a948-4f7f-ba5c-c5fc37d78403 | 8 GB | gp3 | available | kubecost/kubecost-finopsagent | $0.73 |
| vol-0e36539bc8bb1fca2 | general-cluster-dynamic-pvc-6defca50-c566-4769-a406-7adf3a250f51 | 8 GB | gp3 | available | kubecost/kubecost-finopsagent | $0.73 |
| vol-05761425ba030eada | general-cluster-dynamic-pvc-539e0bfc-239f-4842-80b1-2a214383304b | 8 GB | gp3 | available | tools/kubecost-finopsagent | $0.73 |
| vol-0b67d7e8851a0a922 | general-cluster-dynamic-pvc-cd4e1e94-382d-464c-bdfc-84eb6b808f3b | 8 GB | gp3 | available | kubecost/kubecost-finopsagent | $0.73 |
| vol-091d0fd87b9890d5a | general-cluster-dynamic-pvc-9e7b7fb9-ff59-4980-b458-033975919708 | 8 GB | gp3 | available | kubecost/kubecost-finopsagent | $0.73 |
| vol-0c0670f2547920721 | general-cluster-dynamic-pvc-4358fd53-5b28-415a-9f56-edbc8dada4c0 | 8 GB | gp3 | available | tools/kubecost-finopsagent | $0.73 |
| vol-0b92ddebedf2a6438 | general-cluster-dynamic-pvc-6ec332c8-4238-4126-bc61-0ee9f7b7a5f1 | 8 GB | gp3 | available | tools/kubecost-finopsagent | $0.73 |
| vol-0da1196858adb0c33 | general-cluster-dynamic-pvc-855e9c73-ac16-4e83-9a33-ed2d7641aaac | 8 GB | gp3 | available | tools/redis-data-my-passbolt-redis-node-1 | $0.73 |
| vol-05be5cdba1adefff9 | general-cluster-dynamic-pvc-d979437b-eeb0-4efb-a4af-5403564baca8 | 8 GB | gp3 | available | tools/data-my-passbolt-mariadb-primary-0 | $0.73 |
| vol-0c811764d947de8e4 | general-cluster-dynamic-pvc-42cc5c52-b914-4bec-a6a4-6ab63c0d6f5a | 8 GB | gp3 | available | tools/redis-data-my-passbolt-redis-node-0 | $0.73 |
| vol-04d4a73b2509782c3 | general-cluster-dynamic-pvc-dd7bcbba-32c0-4be7-8468-3215d928909e | 8 GB | gp3 | available | tools/redis-data-my-passbolt-redis-master-0 | $0.73 |
| vol-0cff83cc019ff898c | general-cluster-dynamic-pvc-949d553d-3622-4fcc-b0c0-427270d622fe | 8 GB | gp3 | available | tools/redis-data-my-passbolt-redis-node-2 | $0.73 |
| vol-0ca46c7ed625c5431 | general-cluster-dynamic-pvc-12f12dd9-1149-435f-b919-acf4ce867ed8 | 8 GB | gp3 | available | tools/redis-data-my-passbolt-redis-replicas-0 | $0.73 |
| vol-075dc4c51c9679ef3 | general-cluster-dynamic-pvc-4ffe0151-d081-4ce9-bd1a-d9398cbc0635 | 8 GB | gp3 | available | tools/data-my-passbolt-mariadb-secondary-0 | $0.73 |
| vol-0f81ba69ad7d0e59b | general-cluster-dynamic-pvc-7022412a-f2b4-4165-a366-01df38106c7f | 2 GB | gp3 | available | monitoring/storage-grafana-mimir-store-gateway-0 | $0.18 |
| vol-0a50c31239a49fe06 | general-cluster-dynamic-pvc-4d7c50b7-bcdd-409c-ba49-cec51ea5de30 | 2 GB | gp3 | available | monitoring/storage-mimir-store-gateway-0 | $0.18 |
| vol-0317b91fce77e25ac | general-cluster-dynamic-pvc-2125be60-72ca-4061-9ca2-0386c2faa95c | 2 GB | gp3 | available | monitoring/storage-grafana-mimir-ingester-0 | $0.18 |
| vol-0f806cbfb8d39baf3 | general-cluster-dynamic-pvc-3db7e5b7-1335-44a1-987e-bb7c6d80ee04 | 2 GB | gp3 | available | monitoring/storage-mimir-store-gateway-2 | $0.18 |
| vol-048244fa52cb9c65d | general-cluster-dynamic-pvc-479cdb96-47af-4b45-bcfd-e57f7b819a29 | 2 GB | gp3 | available | monitoring/storage-mimir-ingester-2 | $0.18 |
| vol-070bd38b7dc6c7671 | general-cluster-dynamic-pvc-d7a7513e-5711-443f-b513-e1538831d460 | 2 GB | gp3 | available | monitoring/storage-mimir-store-gateway-1 | $0.18 |
| vol-051c47615c22e68e6 | general-cluster-dynamic-pvc-6e1b7dce-9fd3-4cd7-a048-11e04f1c0add | 2 GB | gp3 | available | monitoring/storage-grafana-mimir-ingester-2 | $0.18 |
| vol-0222fad960edfb7ff | general-cluster-dynamic-pvc-889cdce7-a0c3-4d14-8f8c-e09c3a4bed7d | 2 GB | gp3 | available | monitoring/storage-mimir-ingester-1 | $0.18 |
| vol-07d4fbb6b6785d34e | general-cluster-dynamic-pvc-21f03287-a7fa-434b-b32e-2c6d6e9ea285 | 2 GB | gp3 | available | monitoring/storage-grafana-mimir-store-gateway-1 | $0.18 |
| vol-017262e7abf163f5f | general-cluster-dynamic-pvc-65d1bd82-383a-4001-b258-d009a19744bd | 2 GB | gp3 | available | monitoring/storage-mimir-ingester-0 | $0.18 |
| vol-024c65235aed0bf90 | general-cluster-dynamic-pvc-bebd0d85-894d-4817-8f98-84d8628a8b4c | 2 GB | gp3 | available | monitoring/storage-grafana-mimir-store-gateway-3 | $0.18 |
| vol-07a1e6064acd59159 | general-cluster-dynamic-pvc-94521779-a5b8-4bf1-af05-fbeac6b7eb8f | 2 GB | gp3 | available | monitoring/storage-mimir-store-gateway-3 | $0.18 |
| vol-0ed1e36eafbe80c6b | general-cluster-dynamic-pvc-561b0d94-2d8d-4623-bb22-0a18ff95ca6d | 2 GB | gp3 | available | monitoring/storage-grafana-mimir-store-gateway-2 | $0.18 |
| vol-04fd47c08ed675721 | general-cluster-dynamic-pvc-cd2957d4-d23e-4aed-bd5f-d110cf9b7e13 | 2 GB | gp3 | available | monitoring/storage-grafana-mimir-ingester-1 | $0.18 |
| vol-0f7b0a472fa1ad645 | general-cluster-dynamic-pvc-2d351317-2991-4678-89fe-547fa0af6c2f | 1 GB | gp3 | available | netbird/netbird-management | $0.09 |
| vol-066b1d9d73f0bc803 | general-cluster-dynamic-pvc-a6c07e7c-66b2-40f2-9cf9-ac5624f6bbc8 | 1 GB | gp3 | available | netbird/netbird-management | $0.09 |
| vol-0e4d83d2be50767f7 | general-cluster-dynamic-pvc-0c1d8a0f-1334-4629-a7ac-93b2f1ab9427 | 1 GB | gp3 | available | postgres/postgres-pvc | $0.09 |
| vol-09554845ec83451e6 | general-cluster-dynamic-pvc-0c3dccf3-6920-4865-b4c7-519b5bc4ef6c | 1 GB | gp3 | available | netbird/netbird-management | $0.09 |
| vol-0be7826606fe7337c | general-cluster-dynamic-pvc-be4983d5-159f-4160-9060-385911ffd6eb | 1 GB | gp3 | available | monitoring/storage-mimir-alertmanager-0 | $0.09 |
| vol-0a732f62fb710e502 | general-cluster-dynamic-pvc-4e4a354f-b7df-465e-a402-0f64f3b0eda5 | 1 GB | gp3 | available | netbird/netbird-management | $0.09 |
| vol-0e44d723456e55337 | general-cluster-dynamic-pvc-ce81bc9a-0fe8-420d-9f5d-f79ebe24416b | 1 GB | gp3 | available | monitoring/storage-grafana-mimir-alertmanager-0 | $0.09 |
| vol-0e113fb7d3838b8b2 | general-cluster-dynamic-pvc-3f6fe388-eead-48fe-b0e0-d96e0a07a26c | 1 GB | gp3 | available | netbird/netbird-management | $0.09 |
| vol-096bf3e177d7ab343 | general-cluster-dynamic-pvc-1eff6a02-62dc-4096-9db1-5a20fc101376 | 1 GB | gp3 | available | netbird/netbird-management | $0.09 |
| vol-09fde6b4614fa8928 | general-cluster-dynamic-pvc-7ef2e1f5-0833-4fee-80f3-96de62bb7e2d | 1 GB | gp3 | available | netbird/netbird-management | $0.09 |
| vol-0a9f5c319618ee63b | general-cluster-dynamic-pvc-ed2dedd1-10ac-47cc-a10c-2d802f2421ee | 1 GB | gp3 | available | netbird/netbird-management | $0.09 |
| vol-0f5b48ec17ea50f97 | general-cluster-dynamic-pvc-bc35528b-bfab-4eca-83ac-0411ed33be25 | 1 GB | gp3 | available | netbird/netbird-management | $0.09 |


---

## ✅ Volumes Mapeados no Kubernetes (PVs Ativos)

Volumes que estão corretamente provisionados e atrelados a um Persistent Volume (PV) no cluster EKS.

| Volume ID | Nome (Tag) | Tamanho | Tipo | Status | PVC Atual | Custo Mensal |
|:---|:---|:---:|:---:|:---:|:---|:---:|
| vol-0904dc6af97b66d5b | general-cluster-dynamic-pvc-b515730f-c764-44d3-9a58-65c4dc4d0aad | 100 GB | gp3 | available | monitoring/storage-grafana-mimir-ingester-2 | $9.10 |
| vol-0b996e08c90c739a4 | general-cluster-dynamic-pvc-6edc51e7-3de7-4012-91d0-22ee204b73e3 | 100 GB | gp3 | available | monitoring/storage-grafana-mimir-ingester-0 | $9.10 |
| vol-0deff396f0fdb251e | general-cluster-dynamic-pvc-66afe209-1800-48e2-b407-8321faa29416 | 100 GB | gp3 | in-use | prd-apps/data-opensearch-reservas-api-prd-data-2 | $9.10 |
| vol-0f686f8a53237f669 | general-cluster-dynamic-pvc-aa9b8a16-e67a-4315-a3f1-a5c432d36d53 | 100 GB | gp3 | available | monitoring/storage-grafana-mimir-ingester-1 | $9.10 |
| vol-0ac638adc72a9cc51 | general-cluster-dynamic-pvc-182b3dd8-68eb-4803-bc3c-c059c616e7ff | 100 GB | gp3 | available | prd-apps/data-reservas-prd-data-1 | $9.10 |
| vol-0dbdf8b0234db94a9 | general-cluster-dynamic-pvc-ca9dd201-5b32-4059-98be-73da757d7b54 | 100 GB | gp3 | available | prd-apps/data-reservas-prd-data-0 | $9.10 |
| vol-0ae84427aba94ae14 | general-cluster-dynamic-pvc-918591ee-6ad6-415d-8b97-7a191bf3fa34 | 100 GB | gp3 | available | prd-apps/data-reservas-api-opensearch-data-1 | $9.10 |
| vol-055a3ae634d39b135 | general-cluster-dynamic-pvc-8c6b4a2d-f4ba-4e4d-8c87-aea59af94c91 | 100 GB | gp3 | in-use | monitoring/prometheus-kps-prometheus-db-prometheus-kps-prometheus-0 | $9.10 |
| vol-08c47e61b4e536b3a | general-cluster-dynamic-pvc-d876e5b6-19af-42ed-8ef7-b3a63f3ffc98 | 100 GB | gp3 | available | prd-apps/data-reservas-api-opensearch-data-2 | $9.10 |
| vol-064d63a0f45f795e1 | general-cluster-dynamic-pvc-56a5fa5c-3065-4f27-9e1c-9c7a62d0b174 | 100 GB | gp3 | in-use | prd-apps/data-opensearch-reservas-api-prd-data-0 | $9.10 |
| vol-05b2f3aa84d0e4027 | general-cluster-dynamic-pvc-ea8c4ad3-8e6e-4d17-a9d2-5958eeeb8b3a | 100 GB | gp3 | available | posthog-poc/clickhouse-data-clickhouse-0 | $9.10 |
| vol-02fcdd89319bfbe09 | general-cluster-dynamic-pvc-5d139255-b2ae-445d-8282-edd7b19a9702 | 100 GB | gp3 | in-use | prd-apps/data-opensearch-reservas-api-prd-data-1 | $9.10 |
| vol-0ec9028f0643a1493 | general-cluster-dynamic-pvc-937ac425-99a9-4533-9530-e82aa9e30608 | 100 GB | gp3 | available | prd-apps/data-reservas-api-opensearch-data-0 | $9.10 |
| vol-090ca80d6864bb533 | general-cluster-dynamic-pvc-c5ca4a5a-da2f-410b-b295-438a0cf99150 | 50 GB | gp3 | in-use | clickhouse/data-volume-chi-clickhouse-cluster-production-0-0-0 | $4.55 |
| vol-0bc2ac8cf93385dc9 | general-cluster-dynamic-pvc-f8de169c-c969-4c1c-838a-a1bfc573f002 | 50 GB | gp3 | available | stg-apps/data-reservas-stg-data-0 | $4.55 |
| vol-0bf2a27021ca5e220 | general-cluster-dynamic-pvc-d5b9a6e7-cd9d-4dbb-9cf0-77a36e609abb | 50 GB | gp3 | in-use | monitoring/prometheus-kps-prometheus-db-prometheus-kps-prometheus-2 | $4.55 |
| vol-027c7681063014b64 | general-cluster-dynamic-pvc-b295f172-f55b-46f2-838d-b682cdcf0c88 | 50 GB | gp3 | in-use | clickhouse/data-volume-chi-clickhouse-cluster-production-0-1-0 | $4.55 |
| vol-078228c5e74397210 | general-cluster-dynamic-pvc-fb524890-3ac3-4247-9feb-e92206acd013 | 50 GB | gp3 | in-use | stg-apps/data-opensearch-reservas-api-stg-data-0 | $4.55 |
| vol-0ac8a325b9a9b375b | general-cluster-dynamic-pvc-8641c4a5-b840-41fd-96ed-d6751a6bb84f | 50 GB | gp3 | available | monitoring/prometheus-kube-prometheus-stack-prometheus-db-prometheus-kube-prometheus-stack-prometheus-0 | $4.55 |
| vol-0d8a399f518081374 | general-cluster-dynamic-pvc-04c64382-0447-47a0-8bf9-ffcbf45383be | 50 GB | gp3 | available | stg-apps/data-reservas-stg-data-1 | $4.55 |
| vol-04506b6681a14c37a | general-cluster-dynamic-pvc-a1e1e00c-faaf-48f7-8c9e-dcd6c447d30e | 50 GB | gp3 | available | monitoring/prometheus-kps-prometheus-db-prometheus-kps-prometheus-3 | $4.55 |
| vol-05f158c3e7da2fd30 | general-cluster-dynamic-pvc-53e7b7e6-e79c-41d0-9be5-ab43bd3c0f9a | 50 GB | gp3 | in-use | clickhouse/data-volume-chi-clickhouse-cluster-production-0-2-0 | $4.55 |
| vol-00b10dea4584f04f9 | general-cluster-dynamic-pvc-241bddac-07ba-4686-81ad-81c81885402c | 50 GB | gp3 | available | posthog-poc/kafka-data-kafka-0 | $4.55 |
| vol-07d6c329858fe949d | general-cluster-dynamic-pvc-13b5f02f-757c-42d4-aa06-e7bc2eff0d17 | 50 GB | gp3 | in-use | monitoring/prometheus-kps-prometheus-db-prometheus-kps-prometheus-1 | $4.55 |
| vol-02d82ca05eb869997 | general-cluster-dynamic-pvc-cbc44751-9f90-4b30-bf5f-02886f3c13ec | 50 GB | gp3 | in-use | kubecost/kubecost-local-store | $4.55 |
| vol-0c75af0850d450fe2 | general-cluster-dynamic-pvc-72661fbf-5555-49c8-b5e7-6499e5edb754 | 50 GB | gp3 | in-use | stg-apps/data-opensearch-reservas-api-stg-data-1 | $4.55 |
| vol-0c5a90849682bf2ab | general-cluster-dynamic-pvc-4c6ebd87-0f9b-4918-8ecd-e0043fffc5aa | 30 GB | gp3 | available | prd-apps/data-reservas-api-opensearch-masters-2 | $2.73 |
| vol-060f283909ca23bce | general-cluster-dynamic-pvc-74fc2fc1-93d3-4a8f-b8bc-8aec30c59df7 | 30 GB | gp3 | available | monitoring/storage-grafana-mimir-compactor-0 | $2.73 |
| vol-0146eeddf407d827e | general-cluster-dynamic-pvc-ab4cef56-38d2-4418-a5a9-4f7749330213 | 30 GB | gp3 | in-use | prd-apps/data-opensearch-reservas-api-prd-masters-1 | $2.73 |
| vol-02d0ca9030b378a3b | general-cluster-dynamic-pvc-acc0caec-dfe6-4e77-b160-9d1df664f24e | 30 GB | gp3 | available | prd-apps/data-reservas-prd-masters-2 | $2.73 |
| vol-05ce0985327107845 | general-cluster-dynamic-pvc-ffc76120-db91-4635-98a5-4def2e94e5d7 | 30 GB | gp3 | in-use | stg-apps/data-opensearch-reservas-api-stg-masters-0 | $2.73 |
| vol-022ceef473c1929f3 | general-cluster-dynamic-pvc-199fc044-142e-4896-ad53-47ca994726c0 | 30 GB | gp3 | available | prd-apps/data-reservas-prd-masters-1 | $2.73 |
| vol-0e6c5377e0b33253f | general-cluster-dynamic-pvc-6dd8b392-26dd-47ed-9f27-879598d7b37c | 30 GB | gp3 | in-use | prd-apps/data-opensearch-reservas-api-prd-masters-0 | $2.73 |
| vol-0b337c3ce949fb226 | general-cluster-dynamic-pvc-9a138793-7d8e-432e-9c97-c3a6845adf5d | 30 GB | gp3 | available | prd-apps/data-reservas-api-opensearch-masters-1 | $2.73 |
| vol-00cd4974445075f7a | general-cluster-dynamic-pvc-1726e2f7-f6a9-4610-8926-681e5bf094f4 | 30 GB | gp3 | in-use | prd-apps/data-opensearch-reservas-api-prd-masters-2 | $2.73 |
| vol-0239e24bda50a045f | general-cluster-dynamic-pvc-ff844c6b-71e2-468c-83f1-cb4a4ad2b367 | 30 GB | gp3 | in-use | kubecost/aggregator-db-storage-kubecost-aggregator-0 | $2.73 |
| vol-08fa17c52b860bdf5 | general-cluster-dynamic-pvc-f8765830-7c6b-45f3-96eb-01aa4efd45b5 | 30 GB | gp3 | available | prd-apps/data-reservas-api-opensearch-masters-0 | $2.73 |
| vol-0611f4a7ecb18e97a | general-cluster-dynamic-pvc-c34220fa-443a-4d0e-92d7-963add6ff24f | 30 GB | gp3 | available | prd-apps/data-reservas-prd-masters-0 | $2.73 |
| vol-0960dd79dcef0a028 | general-cluster-dynamic-pvc-569f766d-d936-4b25-a0a1-c7dc8d9bbaa7 | 30 GB | gp3 | in-use | stg-apps/data-opensearch-reservas-api-stg-masters-1 | $2.73 |
| vol-08bffc235cad4327b | general-cluster-dynamic-pvc-d7907d41-2878-4dc3-ac9d-dce23878725b | 20 GB | gp3 | available | stg-apps/data-reservas-stg-masters-0 | $1.82 |
| vol-092cd616b132066d3 | general-cluster-dynamic-pvc-357d9c19-a693-489a-a0bb-47d14c6ba441 | 20 GB | gp3 | available | stg-apps/data-reservas-stg-masters-1 | $1.82 |
| vol-0459ba43f5cf5eede | general-cluster-dynamic-pvc-ce5cb1cd-e13b-49bf-8794-d9f358051a80 | 20 GB | gp3 | in-use | kubecost/persistent-configs-kubecost-aggregator-0 | $1.82 |
| vol-08aa9406970be0ca1 | general-cluster-dynamic-pvc-ece070e4-c0a6-4e79-ab62-8258b92ae4c4 | 20 GB | gp3 | available | stg-apps/data-reservas-stg-masters-2 | $1.82 |
| vol-0da03a4b83a58de6b | general-cluster-dynamic-pvc-47620f28-aec2-4f70-b569-9d2967359a27 | 10 GB | gp3 | in-use | monitoring/data-loki-backend-3 | $0.91 |
| vol-0cd8d1b0cc7af206b | general-cluster-dynamic-pvc-113b4218-95be-441e-9045-2a63869d12b8 | 10 GB | gp3 | in-use | clickhouse/data-clickhouse-keeper-1 | $0.91 |
| vol-0ae80b8ff2c3166dd | general-cluster-dynamic-pvc-c2f8e697-9f97-4f92-8024-de76c22e8298 | 10 GB | gp3 | available | monitoring/data-tempo-ingester-6 | $0.91 |
| vol-0c13075e990031d13 | general-cluster-dynamic-pvc-99de5c94-94ea-45bc-a9e4-125a76e2d5b2 | 10 GB | gp3 | in-use | monitoring/alertmanager-kps-alertmanager-db-alertmanager-kps-alertmanager-0 | $0.91 |
| vol-0077b1589c3b98717 | general-cluster-dynamic-pvc-f24fcfa0-15bc-4911-852b-5fd47ebaf4df | 10 GB | gp3 | in-use | monitoring/data-tempo-ingester-5 | $0.91 |
| vol-02b5424e7b09f55f8 | general-cluster-dynamic-pvc-b86c3343-3134-4fa6-a5dc-4f687c7af91b | 10 GB | gp3 | in-use | monitoring/data-loki-write-3 | $0.91 |
| vol-0e92ad7ff9c3c4d3b | general-cluster-dynamic-pvc-1e7e2318-da95-4c48-871e-2dbd21eae653 | 10 GB | gp3 | in-use | monitoring/data-loki-write-6 | $0.91 |
| vol-0fa9d55818bc5611d | general-cluster-dynamic-pvc-cb0b6d0c-cd28-4e89-9745-4cf4b5ad2387 | 10 GB | gp3 | available | monitoring/data-tempo-ingester-7 | $0.91 |
| vol-0253c1cf0f3f5e08c | general-cluster-dynamic-pvc-11eed228-6fe4-4f9b-8a7b-469ff916605a | 10 GB | gp3 | in-use | monitoring/data-loki-write-8 | $0.91 |
| vol-0ac478d0796b56a05 | general-cluster-dynamic-pvc-77025aa2-7612-4fef-be50-330ace91f33e | 10 GB | gp3 | in-use | monitoring/data-loki-write-2 | $0.91 |
| vol-07b5e19389f251427 | general-cluster-dynamic-pvc-49e26b17-d017-4edc-b71b-408aad99a766 | 10 GB | gp3 | available | monitoring/data-tempo-ingester-9 | $0.91 |
| vol-00c932cece3603b41 | general-cluster-dynamic-pvc-3ded20ca-3536-4477-96bd-90071610ad99 | 10 GB | gp3 | in-use | clickhouse/data-clickhouse-keeper-0 | $0.91 |
| vol-07587b8061043be0f | general-cluster-dynamic-pvc-3424a732-44ea-46c4-a7de-21e82251dc1d | 10 GB | gp3 | in-use | monitoring/data-tempo-ingester-1 | $0.91 |
| vol-073b32675215d95ff | general-cluster-dynamic-pvc-0cd08804-93d0-44fb-8381-b511ebb63f4f | 10 GB | gp3 | in-use | monitoring/data-tempo-ingester-4 | $0.91 |
| vol-08b1738ba8520c75f | general-cluster-dynamic-pvc-2ff98056-6dab-4b9a-8193-d72ca480a709 | 10 GB | gp3 | available | monitoring/data-tempo-ingester-8 | $0.91 |
| vol-05b3fbca06e5b7014 | general-cluster-dynamic-pvc-cac79db0-b67e-4f14-8671-fe718be75c38 | 10 GB | gp3 | in-use | monitoring/data-loki-write-9 | $0.91 |
| vol-04c45d82d83eb5528 | general-cluster-dynamic-pvc-2f6dac76-1de7-4b58-9174-5bd666ef6cad | 10 GB | gp3 | in-use | clickhouse/data-clickhouse-keeper-2 | $0.91 |
| vol-0fa96dddcf4a23a18 | general-cluster-dynamic-pvc-ed122735-a2d3-4046-8fbf-7cbb0cef4691 | 10 GB | gp3 | in-use | monitoring/data-loki-backend-4 | $0.91 |
| vol-0a94443aec5e020b9 | general-cluster-dynamic-pvc-5fc74c60-a87d-4a90-80ea-29383781550d | 10 GB | gp3 | in-use | monitoring/data-loki-write-4 | $0.91 |
| vol-0f699cdda379c17b2 | general-cluster-dynamic-pvc-d5b30c37-f4de-4f04-a4eb-ee36305f48ab | 10 GB | gp3 | in-use | monitoring/data-tempo-ingester-2 | $0.91 |
| vol-064e0e1c11971acc3 | general-cluster-dynamic-pvc-090b9dc4-8be3-4f4f-8ed1-fc4b5c545eb3 | 10 GB | gp3 | in-use | monitoring/data-loki-backend-1 | $0.91 |
| vol-0e145c4b330567495 | general-cluster-dynamic-pvc-c4389301-87dd-4d22-a7d5-504d1d898b08 | 10 GB | gp3 | in-use | monitoring/data-loki-backend-2 | $0.91 |
| vol-09de3b00281684a96 | general-cluster-dynamic-pvc-1b6319e6-42fa-44e2-abc0-20603b312eab | 10 GB | gp3 | in-use | monitoring/data-tempo-ingester-3 | $0.91 |
| vol-012f13ac17eca68aa | general-cluster-dynamic-pvc-496a7558-df48-4851-b84e-74d6346bf4b1 | 10 GB | gp3 | available | monitoring/alertmanager-kube-prometheus-stack-alertmanager-db-alertmanager-kube-prometheus-stack-alertmanager-0 | $0.91 |
| vol-0b70aa380a29d8503 | general-cluster-dynamic-pvc-a4ae68f4-9843-4183-8bcf-de2495966b18 | 10 GB | gp3 | in-use | monitoring/data-loki-write-1 | $0.91 |
| vol-075c685fad8bb5108 | general-cluster-dynamic-pvc-8344a598-7d38-4128-bdfa-40b647698071 | 10 GB | gp3 | in-use | monitoring/data-loki-write-5 | $0.91 |
| vol-0cde7ceb4599950e4 | general-cluster-dynamic-pvc-ca87b096-1ed9-4308-a980-8464c0390c0e | 10 GB | gp3 | in-use | tools/data-mongodb-tools-0 | $0.91 |
| vol-0d32c3931aae767c1 | general-cluster-dynamic-pvc-ded377d2-a094-4bf8-af2e-627f1050517e | 10 GB | gp3 | in-use | monitoring/data-loki-write-7 | $0.91 |
| vol-0a4821c81360cf9f5 | general-cluster-dynamic-pvc-03d3be90-28fb-47b1-a4e3-54f90631ab85 | 10 GB | gp3 | in-use | monitoring/data-tempo-ingester-0 | $0.91 |
| vol-03a67c0293fa82c15 | general-cluster-dynamic-pvc-636ba80a-a0fb-4a8a-933a-fe569c960fc7 | 10 GB | gp3 | in-use | monitoring/data-loki-write-0 | $0.91 |
| vol-0c2393b2dde863461 | general-cluster-dynamic-pvc-a65195a4-93a0-4765-ba1c-b6d616ee45e5 | 10 GB | gp3 | in-use | monitoring/data-loki-backend-0 | $0.91 |
| vol-07cb77cceceb44951 | general-cluster-dynamic-pvc-836398cf-512d-4269-9c72-a0f3b4f6b8e2 | 10 GB | gp3 | in-use | monitoring/grafana | $0.91 |
| vol-0219b0006cd19a543 | general-cluster-dynamic-pvc-9ce475da-6aa0-446d-b2bb-abf770a87987 | 8 GB | gp3 | available | growthbook/data-growthbook-mongo-mongodb-0 | $0.73 |
| vol-0195a0ee3c56777f7 | general-cluster-dynamic-pvc-9413a3e1-e343-404c-ab58-8153e824a384 | 8 GB | gp3 | in-use | kubecost/kubecost-finopsagent | $0.73 |
| vol-0c274bfbcd08b00de | general-cluster-dynamic-pvc-7914c76b-6ab5-4594-bc8f-37db60f17572 | 5 GB | gp3 | available | tools/clickhouse-data-op-ch-0 | $0.45 |
| vol-04a0c6351f1f220d1 | general-cluster-dynamic-pvc-785ac836-2b35-4e8b-895a-838c117f5b0d | 5 GB | gp3 | available | tools/postgres-data-op-db-0 | $0.45 |
| vol-068de3f7c4259a7ee | general-cluster-dynamic-pvc-bc9d0174-f3df-4cd5-aaf3-cd202ca76848 | 5 GB | gp3 | available | tools/clickhouse-logs-op-ch-0 | $0.45 |
| vol-07d9e5d428be5a280 | general-cluster-dynamic-pvc-6fbae13a-a5f7-470e-a27a-3860bc4957a3 | 5 GB | gp3 | available | tools/redis-data-op-kv-0 | $0.45 |
| vol-0b164bc485b828002 | general-cluster-dynamic-pvc-09ea121b-941b-439a-a4e6-c9d94c63e7fa | 4 GB | gp3 | available | monitoring/storage-grafana-mimir-store-gateway-1 | $0.36 |
| vol-0047a17aa675b8035 | general-cluster-dynamic-pvc-9fb3aa4a-a792-4746-a035-40e7084e5c93 | 4 GB | gp3 | available | monitoring/storage-grafana-mimir-store-gateway-0 | $0.36 |
| vol-0d1651a4681587304 | general-cluster-dynamic-pvc-618c68ab-9f35-4311-9e81-7aa8e8b84d35 | 4 GB | gp3 | in-use | monitoring/storage-uptime-kuma-0 | $0.36 |
| vol-03f43a925c1e240b7 | general-cluster-dynamic-pvc-146e5951-c6fb-46b1-a6ea-b56c33f7b397 | 4 GB | gp3 | available | monitoring/storage-grafana-mimir-store-gateway-3 | $0.36 |
| vol-01171b8045850901c | general-cluster-dynamic-pvc-b5083393-872c-4a1e-bcc4-a67793eb7aec | 4 GB | gp3 | available | monitoring/storage-grafana-mimir-store-gateway-2 | $0.36 |
| vol-0fe54ed7648c4da66 | general-cluster-dynamic-pvc-648f2ccc-84b1-42c2-83f8-e5af4c3262f8 | 1 GB | gp3 | available | monitoring/storage-grafana-mimir-alertmanager-0 | $0.09 |


---

## 🖥️ Volumes Atachados a Instâncias (Não Kubernetes)

Normalmente são os discos de sistema operacional (Root Volumes) dos EC2 Nodes do cluster (Karpenter/NodeGroups) ou outras instâncias EC2 rodando fora do escopo de PVs do K8s.

| Volume ID | Nome (Tag) | Tamanho | Tipo | Status | Instância Atachada | Custo Mensal |
|:---|:---|:---:|:---:|:---:|:---|:---:|
| vol-08e88dadd0ddff64e | cluster-services | 30 GB | gp3 | in-use | i-0471e9841017342eb | $2.73 |
| vol-03ab393e75ee045da | cluster-services | 30 GB | gp3 | in-use | i-093275a7e8a6d3bad | $2.73 |
| vol-002c5edc6b1cf0ec5 | - | 20 GB | gp3 | in-use | i-02ad9d28d8481f460 | $1.82 |
| vol-06e2a742b657854f7 | - | 20 GB | gp3 | in-use | i-03df62c23395d2b4f | $1.82 |
| vol-054593b44d265597c | - | 20 GB | gp3 | in-use | i-07c09bd942b6f4cf2 | $1.82 |
| vol-075c3ab05922f7a8a | - | 20 GB | gp3 | in-use | i-0268d5695789d3a9e | $1.82 |
| vol-0b3eecc412a4818dd | - | 20 GB | gp3 | in-use | i-00f27ecd38e45fdff | $1.82 |
| vol-0aeab50be475a1bbc | - | 20 GB | gp3 | in-use | i-03d117dbc29614e40 | $1.82 |
| vol-0cd8b9fb544f9fe44 | - | 20 GB | gp3 | in-use | i-0c3c13318a67f3c21 | $1.82 |
| vol-0e1645d4c285d502c | - | 20 GB | gp3 | in-use | i-0a0dc794142652a70 | $1.82 |
| vol-078168ea5276e925e | - | 20 GB | gp3 | in-use | i-03e204e40dc1284a3 | $1.82 |
| vol-06613a393b8ae2557 | - | 20 GB | gp3 | in-use | i-05c10028343c77e98 | $1.82 |
| vol-0ec05987e20ba2f34 | - | 20 GB | gp3 | in-use | i-0249c9adba4bcee91 | $1.82 |
| vol-063908e2191bfee81 | - | 20 GB | gp3 | in-use | i-0ae4b0e5af6350927 | $1.82 |
| vol-044b942a3cfbefa2b | - | 20 GB | gp3 | in-use | i-07cd0c5df521f5c6c | $1.82 |
| vol-080ab4c1f319c5be9 | - | 20 GB | gp3 | in-use | i-0698f11c77f260d4a | $1.82 |
| vol-0804838d3c50cf6ae | - | 20 GB | gp3 | in-use | i-0a1a64c078ea7db28 | $1.82 |
| vol-0e573b196716fd744 | - | 20 GB | gp3 | in-use | i-01a8f8ab1e60ae202 | $1.82 |
| vol-01d36779684f139cb | - | 20 GB | gp3 | in-use | i-062584a7312eae973 | $1.82 |
| vol-09422ca1e6b4e50a7 | - | 20 GB | gp3 | in-use | i-04e8ec262c040269a | $1.82 |
| vol-09e5248f9be3aa9de | - | 20 GB | gp3 | in-use | i-06196a29c7b0e6672 | $1.82 |
| vol-03e175db300dcad6f | - | 20 GB | gp3 | in-use | i-0adc7ba8d13876e2e | $1.82 |
| vol-09992bfb21355ad2d | - | 20 GB | gp3 | in-use | i-0c18cad4731dccaaf | $1.82 |
| vol-0f00f3d42507a919f | - | 20 GB | gp3 | in-use | i-0f95de4a9a90144be | $1.82 |
| vol-02018d6eb0d6e06dd | - | 20 GB | gp3 | in-use | i-04283484b85ba08c5 | $1.82 |
| vol-081667cc5406e977f | - | 20 GB | gp3 | in-use | i-0f4e3b62df9893933 | $1.82 |
| vol-03a249ae7c99b9d98 | - | 20 GB | gp3 | in-use | i-037d4901dd0bc3ba8 | $1.82 |
| vol-07a86a5964d0e6215 | - | 20 GB | gp3 | in-use | i-0ab58cc561a699921 | $1.82 |
| vol-0c3e1f9c16846496c | - | 20 GB | gp3 | in-use | i-0c732638086b6c7b5 | $1.82 |
| vol-00e4de065fe28effe | - | 20 GB | gp3 | in-use | i-058eb3fc0ca89e4f9 | $1.82 |
| vol-084533a4726eaf180 | - | 8 GB | gp3 | in-use | i-08cf3d9c12b8c3eeb | $0.73 |