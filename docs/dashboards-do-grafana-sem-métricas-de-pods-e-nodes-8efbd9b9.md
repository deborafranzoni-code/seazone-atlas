<!-- title: Dashboards do grafana sem métricas de pods e nodes | url: https://outline.seazone.com.br/doc/dashboards-do-grafana-sem-metricas-de-pods-e-nodes-xRdzhJ2Gke | area: Tecnologia -->

# Dashboards do grafana sem métricas de pods e nodes

---

### **1. Identificação do Incidente**

* **Data de Ocorrência:** Segunda-feira, 14 de Julho, 2025
* **Descrição Resumida do Incidente:** Problema nos dashboards de monitoramento, onde não eram exibidos dados nem componentes do cluster (namespaces, pods e nodes) devido à indisponibilidade das métricas essenciais no Prometheus.
* **Status do Incidente:** Resolvido

### **2. Detalhes do Impacto**

* **Serviços Afetados:** Dashboards de monitoramento
* **Impacto no Negócio:** Impossibilidade de monitorar e identificar componentes essenciais do cluster, como namespaces, pods e nodes, afetando a visibilidade e a capacidade de monitoramento dos sistemas.
* **Escala do Incidente:** Aconteceu no ambiente de monitoramento do cluster, afetando a coleta e visualização de métricas no Prometheus.
* **Usuários Afetados:** Equipe de monitoramento e operações do cluster.

### **3. Causa Raiz**

* **Descrição da Causa:** As métricas essenciais (`kube_pod_info` e `kube_node_info`) não estavam disponíveis no Prometheus, o que resultou na falha da atualização dos dashboards.
* **Fatores Contribuintes:** A indisponibilidade das métricas foi causada por um problema na atualização do addon `kubeProxy`, que não conseguia atualizar devido à presença de nodes com status "NotReady". Isso impediu a criação de novos pods necessários para a atualização.

### **4. Cronologia do Incidente**

* **Início do Incidente:** Segunda-feira, 14 de Julho, 2025, quando o Thiago Faria identificou o problema.
* **Ações Iniciais:** O problema foi reportado via suporte e começou a investigação.
* **Resolução:** Após investigar, descobriu-se que os nodes "NotReady" estavam bloqueando a atualização do `kubeProxy`. Os nodes e pods que ocupavam espaço de maneira não otimizada foram removidos. Após isso, o addon `kubeProxy` foi atualizado manualmente, restaurando a disponibilidade das métricas no Prometheus.
* **Data da Resolução:** Terça-feira, 15 de julho, 2025

**5. Comunicação durante o Incidente**

* **Notificação para Stakeholders:** O incidente foi reportado para a equipe de suporte e monitoramento no momento da identificação do problema.
* **Canal de Comunicação:** Suporte interno via canal de suporte.

**6. Ações Corretivas e Preventivas**

* **Correções Imediatas:** Remoção dos nodes e pods com status "NotReady" que estavam ocupando espaço de maneira não otimizada.
* **Prevenção de Reincidência:** nenhuma ação aplicada

**7. Lições Aprendidas**

* **Lição 1:** É importante monitorar proativamente o status dos nodes "NotReady" para evitar bloqueios nas atualizações de addons essenciais.

**8. Conclusão**

* **Status Final:** O incidente foi resolvido com sucesso. As métricas voltaram a ser coletadas corretamente, e os dashboards de monitoramento estão operacionais novamente.
* **Responsáveis pela Resolução:** Time de Governança


---