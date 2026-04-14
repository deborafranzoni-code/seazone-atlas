<!-- title: Incident-agent | url: https://outline.seazone.com.br/doc/incident-agent-IB0qXcXdak | area: Tecnologia -->

# Incident-agent

Agente autônomo de detecção e investigação de incidentes em Kubernetes. Monitora o cluster em tempo real via Watch API, identifica quando um serviço está **realmente fora do ar** (0 réplicas disponíveis), investiga a causa raiz usando IA (Gemini via LangChain), e envia um relatório estruturado ao Slack com um prompt pronto para o Claude Code corrigir o problema.

**Repositório:** `gitops-governanca/k8s-incident-agent/` (branch `feat/k8s-incident-agent`) **Imagem:** `us-central1-docker.pkg.dev/tools-440117/docker-production/k8s-incident-agent:0.6.1` **Cluster:** `cluster-tools-prod-gke` (GKE) **Namespace:** `k8s-incident-agent`

## Filosofia

O agente foi projetado para alertar **somente incidentes reais** — situações onde o Uptime Kuma também apitaria. Eventos transientes, probe failures esporádicos e intermitências conhecidas de spot nodes são ignorados. Quando uma mensagem chega no Slack, significa que uma aplicação está quebrada e precisa de atenção.

## Pipeline de decisão — Quando o agente alerta?

Um alerta no Slack só é enviado quando **todos** estes critérios são verdadeiros:


1. Evento Warning recebido via Watch API
2. Namespace não está na lista de ignorados
3. Reason não está na lista de ignorados (22 reasons filtrados no GKE)
4. Threshold de contagem atingido (ex: BackOff 3x em 5min, Unhealthy 5x em 5min)
5. Não está em cooldown (30min entre alertas do mesmo owner+reason)
6. Dispatch lock — nenhum outro worker está processando o mesmo owner+reason
7. **O SERVIÇO ESTÁ REALMENTE FORA DO AR:**
   * Deployment: 0 available replicas
   * StatefulSet: 0 ready replicas
   * DaemonSet: 0 ready pods
   * Bare Pod: em estado de falha por >= 5 minutos
8. IA investiga a causa raiz e gera relatório
9. Relatório enviado ao Slack com severidade CRITICAL + prompt para Claude Code

## Módulos

| Módulo | Responsabilidade |
|----|----|
| `src/main.py` | Entrypoint: validação de env, preflight check da IA, health server (:8080/healthz) |
| `src/watcher.py` | Watch API, filtragem, service health check, dispatch para ThreadPoolExecutor (3 workers) |
| `src/owner_resolver.py` | Resolve Pod → ReplicaSet → Deployment. Cache 5min. Thread-safe |
| `src/event_counter.py` | Contagem com thresholds, pending cooldown (60s), full cooldown (30min) |
| `src/agent.py` | LangChain agent com Gemini 2.5 Flash, 8 tools, histórico de 20 investigações |
| `src/reporter.py` | Formata report, extrai causa raiz, gera prompt Claude Code, piso de severidade |
| `src/slack_notifier.py` | Envia via webhook com Block Kit (header + body + prompt + metadata) |
| `src/tools/k8s_tools.py` | 6 tools: describe_pod, get_pod_logs, get_events, list_pods, describe_deployment, describe_node |
| `src/tools/prometheus_tools.py` | 2 tools: prometheus_query, prometheus_query_range |

## Configuração (env vars)

| Variável | Default | Descrição |
|----|----|----|
| `GOOGLE_API_KEY` | (obrigatória) | API key do Google Gemini |
| `SLACK_WEBHOOK_URL` | (obrigatória) | Webhook URL do canal Slack |
| `GEMINI_MODEL` | `gemini-2.5-flash` | Modelo Gemini |
| `CLUSTER_NAME` | `unknown` | Nome do cluster |
| `EVENT_THRESHOLDS` | — | Thresholds: `Reason:count:window_seconds` (CSV) |
| `EVENT_THRESHOLD_DEFAULT` | `3:300` | Threshold padrão |
| `COOLDOWN_SECONDS` | `1800` | Cooldown entre alertas (30min) |
| `MIN_FAILURE_DURATION_SECONDS` | `300` | Tempo mínimo de falha para bare pods (5min) |
| `MIN_SEVERITY_SLACK` | `CRITICAL` | Severidade mínima para Slack |
| `IGNORED_NAMESPACES` | `kube-system,kube-public,kube-node-lease` | Namespaces ignorados |
| `IGNORED_REASONS` | `FailedScheduling` | Reasons ignorados |

## Formato da mensagem no Slack

Cada alerta inclui:

* Header com emoji de severidade e nome do recurso
* Investigação completa da IA (resumo, causa raiz, impacto, remediação)
* **Prompt para Claude Code** — pronto para copiar e colar para investigar e corrigir o problema
* Metadata (cluster, reason, timestamp)

## Deploy

```bash
# Build e push
docker build -t k8s-incident-agent:TAG .
docker tag k8s-incident-agent:TAG us-central1-docker.pkg.dev/tools-440117/docker-production/k8s-incident-agent:TAG
docker push us-central1-docker.pkg.dev/tools-440117/docker-production/k8s-incident-agent:TAG

# Deploy GKE
helm upgrade k8s-incident-agent ./chart --namespace k8s-incident-agent -f ./values-gke.yaml
```

Secrets via ExternalSecret → AWS SSM Parameter Store:

* `/sre/incident_agent/GOOGLE_API_KEY`
* `/sre/incident_agent/SLACK_WEBHOOK_URL`

## Melhorias futuras

* **Rollout Suppression** — Suprimir eventos de pods antigos durante rolling updates (design documentado)
* **Persistência do histórico** — Salvar investigações em ConfigMap/PVC (atualmente in-memory)
* **Expansão para EKS** — Chart já tem values default para EKS com Karpenter
* **Métricas Prometheus** — Expor counters/histograms do agente