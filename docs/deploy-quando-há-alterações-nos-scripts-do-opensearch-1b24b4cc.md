<!-- title: Deploy quando há alterações nos Scripts do OpenSearch | url: https://outline.seazone.com.br/doc/deploy-quando-ha-alteracoes-nos-scripts-do-opensearch-xob0MW6Ygv | area: Tecnologia -->

# Deploy quando há alterações nos Scripts do OpenSearch

Deploys que envolvem alterações no OpenSearch sempre dão o frio na barriga 🥶, pois a depender da alteração, é necessário **recriar os indices** (isso apaga todos docs indexados).

Aqui, iremos abordar sobre os deploys quando há alterações no scripts painless do OpenSearch.

Felizmente, ao realizar alterações nos scripts do OpenSearch (localizados atualmente no arquivo `create_search_indexes.py`) eles são atualizados automaticamente quando os containers da API e WORKER, não sendo necessário realizar a recriação dos indices. Essa definição está no seguinte trecho:

`create_search_indexes.py`

```python
**def** **create_indexes**(force: bool = False):
	# ...
	**with** **lock_index_creation_cm**():
		# ...
		**for** script **in** _scripts:
			logger.**info**("creating script [%s]", script["name"])
			search_engine.opensearch.**put_script**(script["name"], body=script["body"])
		# ...
```

Sendo assim, ao realizar alterações nos scripts basta reiniciar os containers. No caso de fazer o deploy, basta apenas que seja realizado o deploy normalmente que o script será atualizado 😀.

* **Mas atenção!** ⚠️ (leia)

  Se na sua **implementação houver a adição/remoção de qualquer novo campo** (**chave) nos indices do OpenSearch**, é preciso ter cuidado, pois pode acabar gerando algum erro caso o campo esteja sendo utilizado em alguma função.

  Portanto, se há novos campos é importante **dividir o deploy em duas etapas** ou **usar feature flags**.

  Onde seria dividido entre: **I.** uma versão que **não usa o campo novo;** e a **II.** outra que **implementa o uso do campo novo**. Dessa forma garantimos que o campo novo só seja usado após a sincronização dessas informações serem indexadas novamente, estando assim, pronto para uso.

  > Para esses casos onde precisa de mais atenção, é **importante criar um planejamento de deploy e um plano de contigência** para garantir que o deploy seja realizado sem problemas. E, para caso haja problema ter um plano B para assegurar o bom funcionamento do site.

### Como realizar o deploy

* **(antes do deploy)** Verificar se no container do **Redis** contém as seguintes keys *(é esperado que **não haja**)*:
  * `deployment:indexes_creation_lock` : Se tiver essa, o update do script não será executado. Uma característica disso é o log "`*Skipping search index creation because another process is already running it*`"
  * `db_migration`: Se houver essa, a aplicação não será iniciada, pois ficará "travada" (com lock). Uma característica disso é o log ficar travado em "`*running alembic upgrade e não prosseguir.`"\*

  ```bash
  # Verificar se uma key existe. É retornado "(nil)" se não existir
  **GET** *key_name*
  
  # Deletar uma key
  **DEL** *key_name*
  ```
* Realize o deploy normalmente e **fique monitorando** os Logs da API e Worker.
* Quando eles subirem, deverá ver os seguintes logs que indicaram sucesso na atualização do script (e criação de novos indexes, caso hajam novos para serem criados)

  Os logs são:

  ```bash
  create_search_indexes: Locking Search Index Creation
  create_search_indexes: Got lock, running
  **create_search_indexes: creating script** [price-and-availability-filter-script] 
  **opensearch: PUT <https://opensearch:9200/_scripts/**price-and-availability-filter-script> [status:200 request:0.069s]
  **create_search_indexes: creating script** [get-calc-values-script]
  **opensearch: PUT <https://opensearch:9200/_scripts/**get-calc-values-script> [status:200 request:0.031s]
  **create_search_indexes: creating script** [get-total-price-script]
  **opensearch: PUT <https://opensearch:9200/_scripts/**get-total-price-script> [status:200 request:0.042s]
  **create_search_indexes: Search index creation succeeded**
  create_search_indexes: Lock released
  ```
* Finalizado o deploy, é possível usar um endpoint do OpenSearch para obter um script, assim conseguimos validar se ele foi de fato atualizado: \*\*`GET** {{opensearch_url}}/_scripts/**<script_name>**`
  * Exemplo de retorno

    ```json
    {
        "**_id**": "price-and-availability-filter-script",
        "**found**": **true**,
        "**script**": {
            "**lang**": "painless",
            "**source**": "*<aqui aparecerá o conteúdo do script buscado>*"
        }
    }
    ```

  <aside> ℹ️ Usar ***Basic auth*** para se conectar ao OpenSearch e add seu IP no Security Group.

  É possível pegar a URL e credenciais do OpenSearch nas ENVs da API (na AWS)

  </aside>

## Exemplo prático

**Tarefa**: **[refact: consider check-in and check-ou blocks in search #365](https://github.com/seazone-tech/seazone-reservas-api/pull/365)**

O Deploy foi seguindo o que está descrito no tópico *[Como realizar o deploy](/doc/deploy-quando-ha-alteracoes-nos-scripts-do-opensearch-b9MTOvfoPM)*

### Plano de Contigência para Evitar Downtime

**Solução encontrada como plano:**  Uso de Feature Flag

Foi criada a Feature Flag no Posthog nomeada como **[ff_consider_check_in_out_blocks](https://us.posthog.com/project/47303/feature_flags/65445)** para conseguirmos habilitar/desabilitar essa implementação.

* **O Problema**

  Foi visto que ocorreria um problema se a alteração na busca fosse liberada **antes dos imóveis serem sincronizados** **novamente** no indice de "*properties*". **Pelo motivo de que**: foi adicionado dois novos tipos de chaves para os imóveis dentro do objeto `_availability` durante a task **index_property**.

  **Descrição do problema**

  As novas chaves (keys) criadas que ficarão no objeto **_availability** são: `YYYY-MM-DD_checkin_closed` e `YYYY-MM-DD_checkout_closed` que dizem se o dia está disponivel para checkin e para checkout, respectivamente.

  E enquanto essas chaves não forem indexadas, os imóveis **deixariam de ser retornados na busca** **devido a uma validação** que é feita no script do opensearch **que** **depende dessas novas chaves** criadas para verificar se o dia pra In e Out estão disponíveis para isso.
* **A Solução**

  Tendo em visto esse potencial problema, foi então **utilizada uma feature flag** que irá desabilitar o envio do parâmetro `check_in_out_dates` para o OpenSearch, dessa forma, o script irá **retornar** **por padrão que o dia de checkin está disponível pra checkin, e o dia de checkout vai estar disponível para checkout.**

  > *Esse parametro "*`check_in_out_dates`"  foi introduzido apenas nessa/para essa implementação, e não irá impactar no funcionamento na busca caso não seja enviado.)

  Isso possibilitará com que a busca por imóveis não seja interrompida enquanto os imóveis são sincronizados novamente.

  Após todos serem sincronizados, podemos ativar a feature flag `ff_consider_check_in_out_blocks`

  Caso haja algum problema na busca por causa dessa implementação, basta desativar a feature flag.

***Plano de Deploy E Contigência***

| **Ação** | **DoD** | **Solução de problemas** |
|----|----|----|
| Lançar release | Conclusão da Action | Investigar Logs |
| Monitoramento da Release | Obter os mencionados no comentário (Como realizar o deploy) |    |
| Busca com e sem datas funcionando normalmente. | Investigar logs + verificar item 1 (verificação de keys do redis) do comentário (Como realizar o deploy) |    |
| Realizar rollback para revisão anterior. |    |    |
| Executar o **pull_properties** | Sem tasks de sync de propriedades pendentes no RabbitMQ. |    |
| Propriedes no OpenSearch contendo a nova chave. | Sync Demorado? Falar com Bernar + verificar existência de erros nos logs |    |

Sem chave? Verificar logs + rodar o sync novamente | | Ativar a feature flag **ff_consider_check_in_out_blocks** | Busca com e sem datas funcionando normalmente. Blocks de In e Out sendo levados em consideração. | Desativar  a feature flag |