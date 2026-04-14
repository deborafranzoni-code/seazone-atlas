<!-- title: TC05 - Relatório Falha do Redis | url: https://outline.seazone.com.br/doc/tc05-relatorio-falha-do-redis-dkgwBw0Qp1 | area: Tecnologia -->

# TC05 - Relatório Falha do Redis

**Data:** 2026-02-24 **Ambiente:** `dev-n8n` — cluster GKE `cluster-tools-prod-gke`  **Status final:** ✅ Sucesso


---

## Execução

 ![Deleção de pod e recriação automática](/api/attachments.redirect?id=7e6eb746-5b2e-48ba-bb9e-11e146454335 " =755x453")

 ![Dados integros](/api/attachments.redirect?id=426692b0-03cd-43ba-a1ca-3fadb2e9ae82 " =952x438")

Resultados

| Verificação | Resultado |
|----|----|
| Redis recriado automaticamente | ✅ |
| Health check HTTP | 200 ✅ |
| Workers sem referência a erros de Redis nos logs | ✅ |
| Dados no banco (workflows / credentials) | 13 / 48 ✅ |


---

## Observações

* O Deployment do Redis recriou o pod automaticamente sem intervenção
* Nenhuma perda de dados críticos,  Redis é cache/fila, não estado persistente
* Workers restartaram automaticamente ao detectar a reconexão com o Redis
* Nenhuma entrada de erro relacionada ao Redis nos logs dos workers no período do teste

**Conclusão:** a falha do Redis é transparente para os dados da aplicação. O impacto é limitado a execuções em andamento no momento da falha, que podem ser reprocessadas.