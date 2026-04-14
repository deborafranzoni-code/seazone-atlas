<!-- title: [ Sugestão ] Monitoramento dos Workers | url: https://outline.seazone.com.br/doc/sugestao-monitoramento-dos-workers-fUVFICaeoH | area: Tecnologia -->

# [ Sugestão ] Monitoramento dos Workers

Created by: Bernardo Ribeiro Created time: August 7, 2024 3:26 PM Last edited: September 24, 2024 11:05 AM Tags: Observabilidade, System

## Soluções Sugeridas

**Branch com as implementações:** [feature/workers-monitoring](https://github.com/seazone-tech/seazone-reservas-api/tree/feature/workers-monitoring) **Alterações:** [feature/workers-monitoring](https://github.com/seazone-tech/seazone-reservas-api/compare/develop...feature/workers-monitoring)

**Refs:**

https://docs.celeryq.dev/en/stable/reference/index.html

https://docs.celeryq.dev/en/v5.2.7/userguide/monitoring.html#monitoring-and-management-guide

https://docs.celeryq.dev/en/stable/reference/celery.app.control.html#celery-app-control

### Endpoint de monitoramento


---

Endpoint criado em nossa aplicação para consultarmos periodicamente para sabermos o status dos workers.

Exemplos de retornos (testados em ambiente local) da API implementada para monitoramento dos workers:

* Retorno quando o Celery **Worker** e **Worker-User** estão **down**

  ```json
  {
    "status": "Unhealthy",
    "broker_health": {
      "hostname": "rabbitmq",
      "userid": "seazone-reservas",
      "password": "seazone-reservas",
      "virtual_host": "/",
      "port": 5672,
      "insist": false,
      "ssl": false,
      "transport": "amqp",
      "connect_timeout": 4,
      "transport_options": {},
      "login_method": "PLAIN",
      "uri_prefix": null,
      "heartbeat": null,
      "failover_strategy": "round-robin",
      "alternates": []
    },
    "worker_health": {
  		"error": "Celery worker is not running."
    },
    "worker_info": null,
    "worker_heartbeat": [],
    "worker_memsample": null
  }
  ```
* Retorno quando o Celery **Worker** e **Worker-User** estão **UP**

  ```json
  {
    "status": "Healthy",
    "broker_health": {
      "hostname": "rabbitmq",
      "userid": "seazone-reservas",
      "password": "seazone-reservas",
      "virtual_host": "/",
      "port": 5672,
      "insist": false,
      "ssl": false,
      "transport": "amqp",
      "connect_timeout": 4,
      "transport_options": {},
      "login_method": "PLAIN",
      "uri_prefix": null,
      "heartbeat": null,
      "failover_strategy": "round-robin",
      "alternates": []
    },
    "worker_health": [
      {
        "celery@worker": {
          "ok": "pong"
        }
      },
      {
        "celery@worker_user": {
          "ok": "pong"
        }
      }
    ],
    "worker_info": {
      "celery@worker": {
        "total": {},
        "pid": 9,
        "clock": "62",
        "uptime": 42,
        "pool": {
          "max-concurrency": 20,
          "free-threads": 20,
          "running-threads": 0
        },
        "broker": {
          "hostname": "rabbitmq",
          "userid": "seazone-reservas",
          "virtual_host": "/",
          "port": 5672,
          "insist": false,
          "ssl": false,
          "transport": "amqp",
          "connect_timeout": 4,
          "transport_options": {},
          "login_method": "PLAIN",
          "uri_prefix": null,
          "heartbeat": 120,
          "failover_strategy": "round-robin",
          "alternates": []
        },
        "prefetch_count": 80,
        "rusage": {
          "utime": 1.582605,
          "stime": 0.09421399999999999,
          "maxrss": 120944,
          "ixrss": 0,
          "idrss": 0,
          "isrss": 0,
          "minflt": 29310,
          "majflt": 4,
          "nswap": 0,
          "inblock": 6176,
          "oublock": 0,
          "msgsnd": 0,
          "msgrcv": 0,
          "nsignals": 0,
          "nvcsw": 557,
          "nivcsw": 25
        }
      },
      "celery@worker_user": {
        "total": {},
        "pid": 9,
        "clock": "62",
        "uptime": 16,
        "pool": {
          "max-concurrency": 20,
          "free-threads": 20,
          "running-threads": 0
        },
        "broker": {
          "hostname": "rabbitmq",
          "userid": "seazone-reservas",
          "virtual_host": "/",
          "port": 5672,
          "insist": false,
          "ssl": false,
          "transport": "amqp",
          "connect_timeout": 4,
          "transport_options": {},
          "login_method": "PLAIN",
          "uri_prefix": null,
          "heartbeat": 120,
          "failover_strategy": "round-robin",
          "alternates": []
        },
        "prefetch_count": 80,
        "rusage": {
          "utime": 1.538757,
          "stime": 0.111416,
          "maxrss": 121192,
          "ixrss": 0,
          "idrss": 0,
          "isrss": 0,
          "minflt": 29142,
          "majflt": 0,
          "nswap": 0,
          "inblock": 0,
          "oublock": 0,
          "msgsnd": 0,
          "msgrcv": 0,
          "nsignals": 0,
          "nvcsw": 150,
          "nivcsw": 73
        }
      }
    },
    "worker_heartbeat": [
      {
        "celery@worker": null
      },
      {
        "celery@worker_user": null
      }
    ],
    "worker_memsample": {
      "celery@worker": "118.11MB",
      "celery@worker_user": "118.35MB"
    }
  }
  ```
* Retorno quando o **Redis** está Down

  No retorno não traz informações úteis sobre o Redis, não diz se está ok.

  O retorno fica igual ao retorno quando os workers estão UP, porém, sempre que houver a chamada de uma task pela aplicação.

  Porém, foi visto/testado que quando o redis está DOWN ou sem conexão, vai gerar uma exception no worker/API (depende de quem chamar) quando uma task do celery foi chamada para executar.Essa é a exception gerada:

  ```bash
  redis.exceptions.**ConnectionError**: Error -3 connecting to redis:6379. Temporary failure in name resolution.
  
  ```
* Retorno quando o **RabbitMQ** está **Down** (perda de conexão) O retorno é o mesmo quando **RabbitMQ** **E** **Workers** estão **Down**
  * Logs dos Workers

    ```bash
    [2024-08-07 17:47:34,455: **ERROR**/MainProcess] consumer: Cannot connect toamqp://seazone-reservas:**@rabbitmq:5672//: [Errno 111] ECONNREFUSED.
    seazone-reservas-api-worker_user-1  | Trying again in 6.00 seconds... (3/100)
    
    ```

    ```
    [2024-08-07 17:55:19,688: **ERROR**/MainProcess] consumer: Cannot connect toamqp://seazone-reservas:**@rabbitmq:5672//: [Errno -2] Name or service not known.
    
    ```
  * Retorno: é gerado exception devido a falha na conexão com o rabbit

    ```json
    {
      "status": "ok",
      "broker_health": {
        "error": "[Errno -3] Temporary failure in name resolution"
      },
      "worker_health": {
        "error": "[Errno -3] Temporary failure in name resolution"
      },
      "worker_info": {
        "error": "[Errno -3] Temporary failure in name resolution"
      },
      "worker_heartbeat": {
        "error": "[Errno -3] Temporary failure in name resolution"
      },
      "worker_memsample": {
        "error": "[Errno -3] Temporary failure in name resolution"
      }
    }
    
    ```

Podemos usar o **status** retornado como base para montar um relatório de Uptime.

Além disso, no retorno quando os workers estão "healthy" é retornado o Uptime também.

E também, em caso de falha em algum ponto, será possível monitorar através dos logs ou mesmo do retorno dessa API, já que quando o worker ou rabbitmq estão down, é retornado error e exibido qual o erro. O status fica como "Unhealthy" caso detecte erro no retorno.

<aside> ⚠️ **Limitação:** Será preciso implementar alguma Lambda function para conseguir consultar essa API de tempos em tempos para saber a saúde dos workers.

</aside>

### Celery Flower (solução do Celery para monitoramento)


---

Aplicação Celery que possui interface gráfica e APIs para monitoramento do status dos workers e observar as tasks/filas que estão sendo executadas.

Sendo possível ver até os argumentos e retorno de cada tarefa, bem como a duração da task e se houve falha ou retry.

 ![Untitled](%5B%20Sugesta%CC%83o%20%5D%20Monitoramento%20dos%20Workers%206b38d0fd89394560af7a4ebda1bcf6f5/Untitled.png)

É possível ver as tasks que estão rodando, os arumentos delas, status e resultados. Alem de informações sobre o tempo de exceução de cada uma

 ![Podemos ver até o trace da task que houve retry/falha](%5B%20Sugesta%CC%83o%20%5D%20Monitoramento%20dos%20Workers%206b38d0fd89394560af7a4ebda1bcf6f5/Untitled%201.png)

Podemos ver até o trace da task que houve retry/falha

 ![Untitled](%5B%20Sugesta%CC%83o%20%5D%20Monitoramento%20dos%20Workers%206b38d0fd89394560af7a4ebda1bcf6f5/Untitled%202.png)

Flower possui uma API que podemos usar para obter informações do worker

<https://flower.readthedocs.io/en/latest/api.html>

<https://flower.readthedocs.io/en/latest/api.html#get--api-tasks>

E possui também integração com Grafana e Prometheus:

* <https://flower.readthedocs.io/en/latest/prometheus-integration.html#grafana-integration-guide>
* <https://flower.readthedocs.io/en/latest/prometheus-integration.html#>