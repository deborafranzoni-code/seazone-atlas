<!-- title: Alternativas para Agente de Investigação de Incidentes em Tempo Real no Kubernetes | url: https://outline.seazone.com.br/doc/alternativas-para-agente-de-investigacao-de-incidentes-em-tempo-real-no-kubernetes-4tIeBKkt1V | area: Tecnologia -->

# Alternativas para Agente de Investigação de Incidentes em Tempo Real no Kubernetes

**Data:** 2026-03-22 **Autor:** Time SRE / Governanca Tech **Status:** Implementado (opção 6 escolhida)


---

## Contexto

Necessidade de um agente que rode em tempo real no cluster Kubernetes, reaja a eventos/problemas automaticamente, investigue a causa raiz e gere relatórios estruturados enviados via Slack para o time.

### Requisitos

* Reação em tempo real a eventos no cluster (CrashLoopBackOff, OOMKill, Node NotReady, etc.)
* Investigação automatizada (coleta de logs, eventos, métricas, status de recursos)
* Geração de relatório estruturado do incidente
* Envio do relatório no Slack em canal do time
* Simplicidade de deploy e manutenção


---

## Alternativas Avaliadas

### 1. Robusta

**O que é:** Plataforma open-source de automação e troubleshooting para Kubernetes.

**Como funciona:** Roda como operator no cluster, assina eventos do Kubernetes e alertas do Prometheus/Alertmanager. Ao detectar um problema, executa "playbooks" de investigação automática (coleta logs, describe pods, top nodes, etc.) e envia um relatório enriquecido no Slack.

| Aspecto | Detalhe |
|----|----|
| Detecção | Event-driven (tempo real) |
| Investigação | Playbooks prontos (CrashLoopBackOff, OOMKill, PendingPods, HighCPU, etc.) |
| Relatório | Rico no Slack (logs, eventos, gráficos) |
| Deploy | 1 Helm chart |
| Backend IA | Opcional (Holmes add-on para RCA com IA) |
| Custo | Open-source (versão SaaS tem features extras pagas) |
| Integração com stack atual | Nativa com Prometheus/Alertmanager |

**Prós:**

* Playbooks prontos para cenários comuns
* Relatórios ricos no Slack com contexto visual
* Comunidade ativa
* Pode criar playbooks customizados em Python

**Contras:**

* Mais um componente no cluster
* Versão open-source mais limitada que a SaaS
* Playbooks são checklist fixos, não "raciocinam"

**Complexidade de deploy:** Baixa (\~1-2h)


---

### 2. k8sgpt-operator

**O que é:** Operator Kubernetes que roda o k8sgpt continuamente no cluster, analisando problemas com LLM.

**Como funciona:** Escaneia o cluster periodicamente via polling, identifica problemas usando analyzers built-in, envia para uma LLM gerar análise em linguagem natural, salva resultados como CRDs `Result` e envia via webhook para Slack.

| Aspecto | Detalhe |
|----|----|
| Detecção | Polling (30s a 5min, configurável) |
| Investigação | Analyzers fixos (Pod, Deployment, Service, Node, Event, Job, etc.) |
| Relatório | Mensagem simples no Slack com análise da IA |
| Deploy | 1 Helm chart + CR K8sGPT |
| Backend IA | OpenAI, Google GenAI (Gemini), Amazon Bedrock (Claude), Azure OpenAI, LocalAI, Cohere, CustomRest |
| Custo | Open-source (CNCF Sandbox project). Custo da API de IA por chamada |
| Integração com stack atual | ServiceMonitor para Prometheus, Grafana dashboard built-in |

**Prós:**

* Projeto CNCF Sandbox (governança comunitária)
* Suporta Gemini como backend (compatível com nossa API key)
* CRD `Result` permite integrar com outros sistemas
* Métricas Prometheus nativas

**Contras:**

* Polling, não event-driven (latência de 30s-5min)
* RBAC muito amplo (praticamente cluster-admin)
* Relatório básico no Slack
* Investigação superficial (describe + heurísticas, sem análise de logs/métricas)
* Sink limitado (só Slack, Mattermost, CloudEvents)

**Complexidade de deploy:** Baixa (\~1-1.5h)


---

### 3. Robusta + Holmes (AI-powered RCA)

**O que é:** Robusta como base de detecção e coleta + Holmes como módulo de Root Cause Analysis com IA.

| Aspecto | Detalhe |
|----|----|
| Detecção | Event-driven (tempo real) |
| Investigação | Coleta automatizada + análise com IA |
| Relatório | Enriquecido com análise de causa raiz |
| Deploy | Robusta Helm chart + Holmes config |
| Backend IA | Requer API key de LLM |
| Custo | Open-source + custo de API IA |

**Complexidade de deploy:** Média (\~2-3h)


---

### 4. Alertmanager Webhook + Script Custom

**O que é:** Usar o Alertmanager existente para disparar webhook para um serviço custom que investiga e posta no Slack.

**Complexidade de deploy:** Média-alta (\~4-6h)


---

### 5. Botkube

**O que é:** Bot de Kubernetes para Slack/Teams com capacidade de monitorar e executar comandos.

**Complexidade de deploy:** Baixa (\~1h)


---

### 6. Script Python Custom com LangChain Agent (ESCOLHIDA)

**O que é:** Deployment no cluster com um agente de IA (LangChain + Gemini) que assiste eventos em tempo real via Watch API e investiga autonomamente usando tools de SRE.

**Stack técnico:** Python 3.12, LangChain (MIT), langchain-google-genai, kubernetes python client, slack-sdk

**Complexidade de deploy:** Média (\~3-4h com Claude Code)

> Ver documento **k8s-incident-agent** para documentação completa da implementação.


---

## Comparativo Geral

| Critério | Robusta | k8sgpt | Robusta+Holmes | Alertmanager Custom | Botkube | LangChain Custom |
|----|----|----|----|----|----|----|
| Detecção tempo real | ★★★ | ★★ | ★★★ | ★★ | ★★★ | ★★★ |
| Qualidade investigação | ★★ | ★★ | ★★★ | ★★ | ★ | ★★★ |
| Qualidade relatório | ★★★ | ★ | ★★★ | ★★ | ★ | ★★★ |
| Simplicidade deploy | ★★★ | ★★★ | ★★ | ★ | ★★★ | ★★ |
| Flexibilidade | ★★ | ★ | ★★ | ★★★ | ★ | ★★★ |
| Custo | Grátis | API IA | API IA | API IA | Pago (cloud) | API IA (Gemini) |
| Manutenção | Comunidade | CNCF | Comunidade | Interna | Comunidade | Interna |
| Compatível com Gemini | Não nativo | Sim | Não nativo | Sim | Não | Sim |
| RBAC mínimo | ★★ | ★ | ★★ | ★★★ | ★★ | ★★★ |