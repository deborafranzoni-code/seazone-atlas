<!-- title: Gerenciamento de Ambientes KEDA | url: https://outline.seazone.com.br/doc/gerenciamento-de-ambientes-keda-BWwUlFo51i | area: Tecnologia -->

# Gerenciamento de Ambientes KEDA

Sistema para ligar/desligar ambientes de staging sob demanda com desligamento automático.

## Por que existe

Ambientes de staging ficam desligados (0 réplicas) quando não estão em uso, economizando recursos. Quando você precisa testar algo, liga o ambiente por GitHub Actions e ele desliga sozinho depois.

**Problema resolvido:** antes, ambientes ficavam ligados 24/7 desperdiçando recursos, ou alguém esquecia ligado.

## Como ligar um ambiente

### Via [GitHub Actions](https://github.com/seazone-tech/gitops-governanca/actions/workflows/manage-keda-environment.yaml)

==GitHub > Actions > "Ligar ambiente de staging" > Run workflow==

**Campos:**

* `app_name`: escolha o componente (ex: wallet-api)
* `namespace`: selecione `stg-apps`
* `action`: sempre `enable`
* `replicas`: quantos pods subir (default: 1)
* `auto_disable_hours`: tempo até desligar automaticamente (default: 3h)

## Auto-Disable (desligamento automático)

### Como funciona

Um Job Kubernetes fica rodando que:


1. Aguarda o tempo configurado (ex: 3h)
2. KEDA retoma controle e volta a 0 réplicas (desliga)

## Como funciona o KEDA

**KEDA ScaledObject** = configuração de autoscaling baseada em eventos (ex: mensagens em fila, horário).

* **Normal:** KEDA controla réplicas baseado em métricas (ex: 0 réplicas se não tem trabalho)
* **Pausado (nossa action):** annotation força N réplicas, KEDA não interfere
* **Despausado:** KEDA volta ao controle e aplica regras (geralmente 0 réplicas)

**Annotation usada:**

```yaml
autoscaling.keda.sh/paused-replicas: "1"  # Liga com 1 réplica
```

Remover a annotation = KEDA retoma = desliga (0 réplicas na maioria dos casos).