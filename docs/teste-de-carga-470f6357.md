<!-- title: Teste de carga | url: https://outline.seazone.com.br/doc/teste-de-carga-ztbLSyeJzP | area: Tecnologia -->

# Teste de carga

# Testes de Desempenho do n8n

## Dashboards e Monitoramento

* **[Dashboards criados para acompanhar os testes](https://monitoring.seazone.com.br/d/5403cddd-e74b-47a1-8381-8e423e791fa1/n8n-performance?orgId=1&from=now-6h&to=now&timezone=browser)**


---

## Teste com k6

O objetivo desse teste foi simular o comportamento do ambiente com usuários simultâneos batendo em um webhook do n8n.

### Teste Usual

**Objetivo:** Simular um cenário de acesso que se aproxima da carga real esperada para o lançamento da ferramenta.

**Cenário Executado no k6:** Simulação de aumento gradual de usuários, atingindo um pico de **50 usuários simultâneos** por 2 minutos.

```javascript

stages: [
  { duration: "1m", target: 10 }, // 10 VUs por minuto durante 1 minuto
  { duration: "2m", target: 100 }, // 20 VUs por minuto durante 2 minutos
  { duration: "1m", target: 0 }, // Voltar a 0 VUs no final do teste
],
```

### Resumo dos Resultados

* A infraestrutura respondeu bem ao teste com 50 usuários simultâneos.
* Os componentes escalaram conforme esperado, e o consumo de recursos foi dentro dos limites configurados.
* O tempo de resposta foi satisfatório.

### Detalhamento por Componente

#### Escalabilidade

* **Webhook:** Escalou de 2 para 5 réplicas. Limite máximo de 6 réplicas, indicando capacidade para lidar com a carga de 50 usuários.
* **Workers:** Escalou de 2 para 3 réplicas, com limite de 6, indicando sobra de capacidade.

#### Consumo de Recursos

* **Editor:** Memória variando de 220Mi para 310Mi. Ficou 30% abaixo do limite configurado.
* **Workers:** Memória variando de 175Mi para 261Mi. Utilização de 25% do limite.
* **CPU:** Sem variação significativa de CPU nos pods.

#### Banco de Dados

* **CPU:** A CPU do banco passou de 8% para 27%, indicando que há relação com o número de execuções armazenadas.

#### Métricas de Performance

* **Total de Requisições:** 3.621
* **Taxa de Sucesso:** 94% das requisições bem-sucedidas.
* **Tempo de Resposta (P95):** 95% das requisições completadas em até 1.38s.

### Próximos Passos

* Investigar as 6% de falhas nas requisições.
* Avaliar a configuração de armazenamento de execuções.


---

## Teste de Estresse

Este teste validou a capacidade máxima de usuários simultâneos antes de ocorrerem problemas.

### 100 Usuários Simultâneos

* **Taxa de Erros de Requisição:** 4,72%
* **Webhooks e Workers:** Consumo de recursos em torno de 30% dos limites.
* **CPU do Banco:** 41%.
* **Reinício/OOM:** Nenhum pod reiniciado ou OOM killed.

### 200 Usuários Simultâneos

* **Escalabilidade:** Webhooks escalando para o limite de réplicas, Workers escalando de 2 para 5 réplicas.
* **Taxa de Erros de Requisição:** 16,82%
* **Uso de Memória dos Pods:** Aproximadamente 32% do limite.
* **CPU do Banco:** 58%
* **Memória do Banco:** 3,9 GB.

### Conclusão

* O ambiente suportou até 200 usuários simultâneos sem ultrapassar 50% dos limites dos pods.
* O banco de dados apresentou alta carga, especialmente em termos de CPU, com necessidade de investigar a configuração de armazenamento de execuções.


---

## Teste com Code Runners

Este teste avaliou o comportamento da aplicação ao executar nodes de código no n8n.

### Cálculos Intensivos (Uso de CPU)

* O uso de CPU não variou significativamente, com picos de 10 milicores, enquanto o limite é 500m.
* Observou-se que o `N8N_RUNNERS_HEARTBEAT_INTERVAL` limita a execução de tarefas a 30 segundos.

### Operações Assíncronas (Uso de Memória)

* O uso de memória variou de 200Mi para 240Mi.
* O erro encontrado após 30 segundos de operação está relacionado ao `heartbeat`.


---

## Teste com Fluxo de Loop + k6

Simulação de dois fluxos paralelos com o k6, com 200 requisições por segundo e 50 requisições por segundo, executando workflows complexos.

### Comportamentos Observados

* Escalonamento de pods de webhook e workers, mas mantendo recursos abaixo do limite.
* Jobs simultâneos travaram em 60 por uma hora, indicando que 200 requisições por segundo podem afetar outros fluxos.
* CPU do banco atingiu 90%.
* Memória do editor escalou, sem atingir o limite.
* Alguns reinícios nos pods do webhook.

### Alertas Identificados

* **Execuções Paralelas:** Cada worker mantém no máximo 10 execuções em paralelo. Com até 6 workers, o limite é de 60 execuções simultâneas. Criamos um alerta para quando esse número for atingido por mais de 3 minutos.
* **Editor:** O pod do editor não escala horizontalmente. Criamos um alerta quando o uso de memória atingir 80% do limite de 2048Mi.
* **Banco de Dados:** Criamos alertas para monitorar quando a CPU do banco atingir 80% e a memória atingir 80%.


---

## Ações

- [ ] Revisar a necessidade de `N8N_RUNNERS_HEARTBEAT_INTERVAL` para permitir execuções maiores que 30 segundos.
- [ ] Revisar as configurações de [retenção de execuções no n8n](https://docs.n8n.io/hosting/scaling/execution-data/?_gl=1%2A14xwg44%2A_ga%2ANzkxMTI0NTgzLjE2NTc1MzYxNzE.%2A_ga_0SC4FF2FH9%2AMTY5MTYzNTA2OC4zMC4xLjE2OTE2MzkxNzMuMC4wLjA.#reduce-saved-data), verificando se podem ser otimizadas.
- [x] Adicionar alertas de recurso para o banco gerenciado (memória e CPU).
- [x] Criar alertas para componentes do n8n 


---