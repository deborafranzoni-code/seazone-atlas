<!-- title: TC04 - Relatório - Corrupção de Secret | url: https://outline.seazone.com.br/doc/tc04-relatorio-corrupcao-de-secret-nqp0sSVDl7 | area: Tecnologia -->

# TC04 - Relatório - Corrupção de Secret

**Data:** 2026-02-24 **Ambiente:** `dev-n8n` — cluster GKE `cluster-tools-prod-gke` Team **Status final:** ✅ Validado (comportamento automático observado)


---

## Objetivo

Validar o comportamento do ambiente quando o Secret `n8n-secrets` é deletado ou corrompido.

O secret `n8n-secrets` é gerenciado pelo **External Secrets Operator** via AWS Parameter Store. Ao deletar o secret no Kubernetes, ele foi recriado automaticamente em \~5 min sem nenhuma intervenção manual.

**Fonte:**

* Store: `aws-parameter-store-global` (ClusterSecretStore)
* Path: `/sre/n8n/dev/*`
* Refresh interval: `1 minuto`
* Deletion policy: `Retain`


---

## O que foi Observado

| Ação | Resultado |
|----|----|
| `kubectl delete secret n8n-secrets -n dev-n8n` | Secret deletado |
| Aguardar | ExternalSecret recriou o secret em \~5 min |
| Pods | Continuaram `Running` sem restart |
| Health check | HTTP 200 mantido |


---

## Implicações para o DR

* Deleção acidental do secret no K8s é **inofensiva**  o operador recupera automaticamente ✅
* O backup local do secret é desnecessário para este cenário
* **A fonte da verdade é o AWS Parameter Store**  corrupção real exigiria alterar os valores lá