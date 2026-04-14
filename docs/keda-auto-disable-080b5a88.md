<!-- title: KEDA Auto-Disable | url: https://outline.seazone.com.br/doc/keda-auto-disable-BeBMli5MEy | area: Tecnologia -->

# KEDA Auto-Disable

Desliga automaticamente ambientes de staging após tempo configurável.

## Como funciona

Quando você liga um ambiente via GitHub Actions, um Job Kubernetes é criado que:


1. Aguarda o tempo configurado (default: 3h)
2. Remove as anotações do KEDA que mantêm o ambiente ligado
3. KEDA volta ao controle e desliga o ambiente (0 réplicas)

## Como usar

### Ligar ambiente (GitHub Actions)

```
Actions > Ligar ambiente de staging > Run workflow
```

**Parâmetros:**

* `app_name`: escolha a aplicação
* `namespace`: `stg-apps`
* `action`: `enable`
* `replicas`: número de réplicas (default: 1)
* `auto_disable_hours`: tempo até desligar (default: 3h, máximo: 24h)

**Exemplos:**

* Ligar wallet-api por 3h: use defaults
* Ligar por 1h: `auto_disable_hours: 0.167`
* Ligar por 8h: `auto_disable_hours: 8`