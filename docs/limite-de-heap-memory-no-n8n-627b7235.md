<!-- title: Limite de Heap Memory no N8N | url: https://outline.seazone.com.br/doc/limite-de-heap-memory-no-n8n-QZpi9Iun5s | area: Tecnologia -->

# Limite de Heap Memory no N8N

## **Relatório de Diagnóstico - Problema de Memória interna dos processos no N8N (28/02/2026)**

### **Contexto Inicial**

Foi identificado que o pod do componente de editor do N8N havia experimentado 66 reinicializações, e o último reinício coincidiu com os alertas registrados no dia 28.\n

### **Investigação e Análise**

Ao examinar os logs por meio do [Cloud Logging](https://console.cloud.google.com/logs/query;query=resource.type%3D%22k8s_container%22%0Aresource.labels.cluster_name%3D%22cluster-tools-prod-gke%22%0Aresource.labels.container_name%3D%22n8n%22%0Aresource.labels.namespace_name%3D%22tools%22%0Aseverity%3D%22ERROR%22;cursorTimestamp=2026-02-28T11:19:01.947524465Z;startTime=2026-02-28T11:18:04.371Z;endTime=2026-02-28T11:24:04.371Z?referrer=search&hl=en&project=tools-440117), foram encontrados dois registros de erro relevantes:\n

`1- 46035 ms: Mark-Compact 511.3 (523.9) -> 507.5 (526.7) MB, pooled: 0 MB, 1068.18 / 0.00 ms (average mu = 0.368, current mu = 0.021) allocation failure; scavenge might not succeed`

`2- FATAL ERROR: Reached heap limit Allocation failed - JavaScript heap out of memory`

 ![](/api/attachments.redirect?id=6cb738e4-c1c1-49ee-935e-6387e1d3e904 " =1030x110")

 ![](/api/attachments.redirect?id=a7fe50e0-5b0c-4912-af02-b21166f145ed " =945x73")

* O **primeiro log** indica que o Garbage Collector do JavaScript falhou ao tentar liberar memória no processo do Node.js.
* O **segundo log** evidencia que o processo que estava sendo executado no Node.js ultrapassou o limite máximo de memória alocada, gerando uma falha fatal. Esse processo pode ter sido um workflow ou um único nó, sendo que, com base em pesquisas, a ocorrência desse tipo de problema está mais associada a nós de código.

### **Solução Implementada**

Foi identificado que existe uma variável de configuração que permite ajustar o limite de memória alocada para os task_runners que são os que mais causam esse tipo de problema. A variável `N8N_RUNNERS_MAX_OLD_SPACE_SIZE` foi configurada para 2 GiB, um valor consideravelmente elevado, para evitar que o erro se repita.

Além disso, para garantir o monitoramento contínuo desse problema,  começamos a monitorar a métrica `n8n_nodejs_heap_space_size_used_bytes`, que permite acompanhar o uso da memória do processo em tempo real.

### **Ações de Monitoramento e Prevenção**

* [Criado um dashboard](https://N8N_RUNNERS_MAX_OLD_SPACE_SIZE) para monitoramento do uso de memória.


* [Implementado um alerta](https://monitoring.seazone.com.br/alerting/grafana/dfetapaaacw74d/view) para notificar a equipe caso o uso de memória se aproxime do limite configurado.\n