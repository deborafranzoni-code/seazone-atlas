<!-- title: Sincronizar dados manualmente | url: https://outline.seazone.com.br/doc/sincronizar-dados-manualmente-zZ6MHXl7ae | area: Tecnologia -->

# Sincronizar dados manualmente

**Endpoint**

[FastAPI - Swagger UI](https://api.staging.reservas.sapron.com.br/docs#/tasks/sync_data_tasks_sync_data_put)

## Sobre


---

Através do endpoint `PUT /tasks/sync_data/{task_name}` é possível chamar/rodar tasks assíncronas no **Celery**. Ela pode ser usada nos casos em que foi alteradas informações e que **não podem aguardar o tempo da task rodar automaticamente** e então precisa ser acionada manualmente.

**⚠️ ATENÇÃO** ⚠️ Nem tudo é tão urgente que não possa esperar, avalie se de fato há grande urgência em rodar a sincronização. E não deve ser uma prática frequente a chamada manual das tasks.

## Como usar


---

Passar como parametro em `task_name` o nome da tarefa que deseja sincronizar. Opções disponíveis no momento: `sync_properties`, `sync_groups`, `sync_properties_comments`.

Para se autenticar na API, obtenha um **auth_token (Barear Token)** de um usuário que tenha permissão necessária.

> ℹ️ **Observação**: É necessário ter a Role de **"Admin"** atribuída ao usuário que irá realizar a chamada neste endpoint, no [Auth0](/doc/auth0-PsX5OvzmUU) . [Veja aqui como fazer isso](/doc/auth0-PsX5OvzmUU). Se seu usuário não tiver permissão suficiente, irá receber o erro "**401 Unauthorized".**\n**Admins do Auth0 do Reservas são:** @[Bernardo Ribeiro](mention://e14183b4-61c2-4968-b64b-a746e4a5a0f3/user/d68e5193-1b5c-492d-bca8-56f01bad14a7)  e @[Maria Fernanda Vaz Romero](mention://26d1337b-4b58-4b42-9c06-8c86d5584d83/user/20053ef3-06e9-418b-900f-9eee99d3badb) 


1. Acessar o Swagger Docs
2. Realizar autenticação![](/api/attachments.redirect?id=41f75da3-ef5e-4809-a304-8232fbc372bd " =1883x743")
3. Expandir o endpoint `PUT /tasks/sync_properties` ou `PUT /tasks/sync_data/{task_name}` e enviar a requisição.\n

## Tutorial em vídeo

**Video 1: Como executar tasks manualmente pelo Endpoint** `PUT /tasks/sync_data/{task_name}` 

[Como realizar execução manual de Tasks do Worker.mp4 1920x1080](/api/attachments.redirect?id=885cd741-9677-46fe-b2ba-d575c44af0a6)


**Video 2: Como monitorar a execução de uma task**

[Monitorando a execução de uma Task.mp4 1920x1080](/api/attachments.redirect?id=fd67356e-121d-4499-9956-031e5a919b0a)


## Como implementar novas tasks para rodar por esse endpoint


---

Basta adicionar um novo dicionário dentro do dicionário que está na variável tasks. Exemplo:

```python
# Necessário realizar o import da task que deseja adicionar
from reservations_api.algum_modulo.tasks import task_name

 tasks = {
        # nova task
        "task_name": {
            "task": **task_name**.delay(),
            "detail": "manual **task_name** sync recently called, \\
                please wait a few minutes to sync again",
            "cache_key": "manual_**task_name**_requested"
        },
        "...": {...}
}
```


---

*ℹ️ Este endpoint foi implementado inicialmente [neste PR](https://github.com/Khanto-Tecnologia/seazone-reservas-api/pull/111).*