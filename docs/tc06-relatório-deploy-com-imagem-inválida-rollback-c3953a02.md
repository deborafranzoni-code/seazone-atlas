<!-- title: TC06 - Relatório - Deploy com Imagem Inválida (Rollback) | url: https://outline.seazone.com.br/doc/tc06-relatorio-deploy-com-imagem-invalida-rollback-ohi5bDPxJl | area: Tecnologia -->

# TC06 - Relatório - Deploy com Imagem Inválida (Rollback)

**Data:** 2026-02-24 **Ambiente:** `dev-n8n` — cluster GKE `cluster-tools-prod-gke` Team **Status final:** ✅ Sucesso


---

## Execução

 ![Check-up pŕe teste](/api/attachments.redirect?id=ec61b176-f9b6-402c-9ef6-237cb12c58a3 " =691x531")

Execução da imagem errada e logs de crash:

 ![](/api/attachments.redirect?id=3a33e854-7fb7-4024-9306-dff206977a40 " =691x531")

 ![n8n caiu](/api/attachments.redirect?id=cd177e75-2888-4da6-9294-4c983e89c3e2 " =1911x809")

|   Hora | Evento |
|----|----|
| 10:27:06 | Início do teste |
| 10:27:10 | Imagem inválida aplicada: `n8nio/n8n:99.99.99` |
| 10:27:17 | Novo pod `n8n-editor-6d4665b9d9-vpwd5` — `ImagePullBackOff` |
| 10:27:06 | Pod anterior `n8n-editor-7698dc6f96-dmvms` mantido `Running` (RollingUpdate) |
| 10:28:37 | Pod com imagem inválida terminado pelo K8s |
| 10:28:40 | `kubectl rollout undo` executado |
| 10:28:43 | Rollback concluído |
| 10:29:10 | Conclusão |


---

## Resultados

| Verificação | Resultado |
|----|----|
| Imagem inválida gerou `ImagePullBackOff` | ✅ Comportamento esperado |
| Pod anterior mantido durante o deploy ruim | ✅ RollingUpdate protegeu o serviço |
| Health check durante o incidente | HTTP 200 ✅ — sem downtime // front off rapidamente |
| `kubectl rollout undo` funcionou | ✅ |
| Rollback concluído | ✅ |
| Health check pós-rollback | HTTP 200 ✅ |


---

## Observações

### RollingUpdate protegeu o serviço

O Kubernetes não removeu o pod anterior até o novo estar healthy. Como o novo pod nunca ficou `Ready` (falhou no pull), o pod original continuou servindo tráfego durante todo o incidente — **zero downtime**.

### OOMKilled em webhook (não relacionado)

Durante o teste, o pod `n8n-webhooks-79d8c5fb8d-9scjb` sofreu `OOMKilled` e entrou em `CrashLoopBackOff`. Recuperou automaticamente. Não está relacionado ao TC-07, indica pressão de memória no pod.