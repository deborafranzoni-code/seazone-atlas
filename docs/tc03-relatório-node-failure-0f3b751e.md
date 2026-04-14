<!-- title: TC03 - Relatório - Node Failure | url: https://outline.seazone.com.br/doc/tc03-relatorio-node-failure-NHYacC9mhu | area: Tecnologia -->

# TC03 - Relatório - Node Failure

**Data:** 2026-02-24 **Ambiente:** `dev-n8n` — cluster GKE `cluster-tools-prod-gke` Team **Status final:** ⚠️ Bloqueado,risco de impacto em outros namespaces


---

## Objetivo

Validar que o pod `n8n-postgres-0` é reagendado automaticamente em outro nó quando o nó atual falha ou é drenado, e que o PVC é remontado corretamente sem perda de dados.


---

## Estado Inicial

 ![](/api/attachments.redirect?id=3f348ce3-884f-4e01-9eb6-8f6ef576c1fa " =1723x301")


---

## Execução

### Passo 1 - Identificação do nó e outros workloads

Antes de executar o drain, foi feito um levantamento de todos os pods rodando no nó alvo:

| Namespace | Pod | Impacto |
|----|----|----|
| `dev-n8n` | `n8n-postgres-0` | Alvo do teste |
| `dev-n8n` | `n8n-editor-7698dc6f96-dmvms` | Seria evacuado |
| `tools` | `n8n-worker-6b49fbc485-8wgqr` | ⚠️ Outro namespace — seria evacuado |
| `gmp-system` | `gmp-operator-79f9d984bd-bglsx` | ⚠️ Monitoramento — seria evacuado |
| `kube-system` | daemonsets diversos | Ignorados pelo `--ignore-daemonsets` |

**Conclusão:** o nó é compartilhado com workloads de outros namespaces (`tools`, `gmp-system`). Um drain afeta todos indiscriminadamente.

## Estado Final

```
Nó:      Ready ✅
Pods:    todos Running, nenhum movido ✅
Dados:   íntegros, nenhuma operação destrutiva executada ✅
```


---

## Por que o Teste Foi Bloqueado

O drain de um nó no GKE é uma operação que afeta **todos os pods do nó**, independente do namespace. No cluster `cluster-tools-prod-gke`, os nós são compartilhados entre múltiplos ambientes e times. Executar o drain do nó onde o `n8n-postgres-0` está rodando causaria a evacuação de pods de outros namespaces em produção, risco inaceitável para um teste de DR em ambiente dev.

Diferente de um ambiente com nós dedicados por namespace ou por ambiente, aqui não é possível isolar o impacto do drain ao `dev-n8n`.


---

## Comportamento Esperado 

Com base na arquitetura do cluster e no comportamente padrão


1. O cordon impede novos pods de serem agendados no nó
2. O drain evacua todos os pods não-daemonset
3. O StatefulSet `n8n-postgres` detecta o pod terminado e cria um novo
4. O scheduler tenta agendar o novo pod em outro nó da mesma zona (`us-central1-a`)
5. O PVC `data-n8n-postgres-0` é remontado no novo nó 
6. O Postgres inicializa e os dados são acessíveis normalmente


---