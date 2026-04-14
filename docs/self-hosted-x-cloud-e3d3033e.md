<!-- title: Self Hosted X Cloud | url: https://outline.seazone.com.br/doc/self-hosted-x-cloud-9VPwq7E4AR | area: Tecnologia -->

# Self Hosted X Cloud

# n8n Cloud vs Self-Hosted — Análise comparativa

> Preços extraídos da página oficial [n8n.io/pricing](http://n8n.io/pricing) (já em BRL)


---

## Cenário atual

| Métrica | Valor |
|----|----|
| Execuções/mês | \~93,000 |
| Workflows ativos | \~75 (crescendo) |
| Execuções simultâneas (pico) | até 80 |
| **Custo self-hosted no cluster** | **R$ 655,99/mês** |


---

## Planos (valores em R$, billing mensal)

|    | **Starter** | **Pro** | **Pro (\~100k)** | **Enterprise** | **Self-Hosted Community** |
|----|----|----|----|----|----|
| **Preço/mês** | R$ 150 | R$ 900 | \~R$ 1.800 | Sob consulta | R$ 655,99 |
| Execuções incluídas | 2,500 | 50,000 | \~100,000 | Custom | Ilimitadas |
| Execuções simultâneas | 5 | 20 | 20 | 200+ | Sem limite |
| Hospedagem | Cloud | Cloud | Cloud | Custom | Self-hosted |
| Workflow history | 1 dia | 5 dias | 5 dias | 365+ dias | Configurável |
| Max saved executions | 2,500 | 25,000 | 25,000 | 50,000 | Sem limite |
| Execution log retention | 7 dias | 30 dias | 30 dias | Ilimitado | Configurável |
| Shared projects | 1 | 3 | 3 | Ilimitado | — |
| AI Builder credits | 50 | 150 | 150 | 1,000 | — |
| Global Variables | Não | Sim | Sim | Sim | Sim |
| Search executions by data | Não | Sim | Sim | Sim | Sim |
| Project editors/admins | Só admins | Sim | Sim | Sim | Sim |
| Project viewers | Não | Não | Não | Sim | — |
| Environments (dev/staging/prod) | Não | Não | Não | Sim | — |
| Version control (Git) | Não | Não | Não | Sim | — |
| Workflow Diff | Não | Não | Não | Sim | — |
| Queue mode (multi-instance) | Não | Não | Não | Sim | — |
| Worker view | Não | Não | Não | Sim | — |
| External storage (S3) | Não | Não | Não | Sim | — |
| Multi-main | Não | Não | Não | Sim | — |
| SSO SAML/LDAP | Não | Não | Não | Sim | — |
| Enforce 2FA | Não | Não | Não | Sim | — |
| External secret store | Não | Não | Não | Sim | — |
| Audit logging | Não | Não | Não | Sim | — |
| Stream logs (Datadog) | Não | Não | Não | Sim | — |
| Run bash scripts | Não | Não | Não | Só self-hosted | Sim |
| Control via CLI | Não | Não | Não | Só self-hosted | Sim |
| Custom nodes | Não | Não | Não | Só self-hosted | Sim |


---

## Starter — R$ 150/mês

**Prós:**

* Zero manutenção de infra
* Menor custo entre todos os planos

**Contras:**

* 2,500 execuções — cobre \~2.7% do uso atual
* 5 execuções simultâneas (uso atual: até 80)
* Workflow history de apenas 1 dia
* Sem Global Variables
* Sem busca por dados nas execuções
* Sem project editors


---

## Pro (50k) — R$ 900/mês

**Prós:**

* Global Variables
* Search executions by data
* 3 shared projects com editors e admins
* 30 dias de log retention
* 25k saved executions

**Contras:**

* 50,000 execuções — cobre \~54% do uso atual
* 20 execuções simultâneas (uso atual: até 80)
* Sem environments, Git, queue mode, worker view, multi-main
* Sem bash scripts, CLI, custom nodes


---

## Pro (\~100k) — \~R$ 1.800/mês (estimado)

obs : esse custo não aparece no pricing do n8n ele mostra somente até 50k e depois um botão de `custom executions`, isso aqui foi um inferência feita pelo claude com base no valor de 50k de execuções

**Prós:**

* Mesmas features do Pro
* \~100k execuções — atende o volume atual

**Contras:**

* 20 execuções simultâneas (uso atual: até 80)
* O volume de execuções está crescendo — o custo escala proporcionalmente
* Sem bash scripts, CLI, custom nodes
* Sem environments, Git, queue mode


---

## Enterprise — Sob consulta

**Prós:**

* Execuções e simultâneas customizáveis (200+)
* Environments, Git, Workflow Diff, Queue mode, Multi-main
* SSO/SAML, Audit logging, External storage S3
* 365+ dias de history, 50k saved executions

**Contras:**

* Preço sob consulta
* No Cloud: sem bash scripts, CLI, custom nodes
* Dependência do vendor para escalar


---

## Self-Hosted Community (atual) — R$ 655,99/mês

**Prós:**

* Execuções ilimitadas
* Execuções simultâneas sem limite
* Custom nodes, bash scripts, CLI
* Controle total da infra
* Custo fixo independente do crescimento de uso

**Contras:**

* Manutenção de infra (updates, backups, monitoramento)
* Sem SLA formal do vendor
* Sem Git integration nativa
* Sem audit logging nativo


---

## Resumo comparativo

|    | Starter | Pro (50k) | Pro (\~100k) | Enterprise | Self-Hosted |
|----|----|----|----|----|----|
| **Custo/mês** | R$ 150 | R$ 900 | \~R$ 1.800 | Sob consulta | R$ 656 |
| Hospedagem | Cloud | Cloud | Cloud | Custom | Self-hosted |
| Atende execuções? | Não (2.7%) | Não (54%) | Sim | Sim | Sim (ilimitado) |
| Atende simultâneas? | Não (5) | Não (20) | Não (20) | Sim (200+) | Sim (80+) |
| Custom nodes/bash/CLI | Não | Não | Não | Só self-hosted | Sim |
| **Custo anual** | R$ 1.800 | R$ 10.800 | \~R$ 21.600 | — | R$ 7.872 |

> **Ponto de atenção:** Existe também o plano **Business** (R$ 10.787/mês) que não foi incluído nesta comparação por ser **self-hosted** — ou seja, na mesma modalidade de hospedagem atual. Ele adiciona features de governança e scaling (queue mode, multi-main, worker view, SSO, audit logging) sobre a instância self-hosted, mas o custo de infra seria adicional ao valor da licença.