<!-- title: Como realizar um deploy do Backend que possui alteração de tabela no Banco de Dados | url: https://outline.seazone.com.br/doc/como-realizar-um-deploy-do-backend-que-possui-alteracao-de-tabela-no-banco-de-dados-nciGOPXBvD | area: Tecnologia -->

# Como realizar um deploy do Backend que possui alteração de tabela no Banco de Dados

Nos casos onde há alterações em tabelas e/ou criação/deleção delas, é preciso ter um pouco mais de atenção para deployar essas alterações.

Enfrentamos 2 incidentes até a data de hoje (December 19, 2023) devido a isso.

> *Recomendo ler todo o tutorial e ir acompanhando mas sem realizar alterações. Caso haja dúvidas pergunte ao time do website no canal* `#website` ou para o **@Bernardo Ribeiro** no Slack.

A maneira atual de como conseguir evitar que esses incidentes aconteçam e até como resolvê-los caso ocorram, consiste em seguir os seguintes passos **(não pule etapas)**:


1. Acessar a AWS > ECS > Cluster de Produção
2. [Parar todos os serviços](/doc/como-realizar-um-deploy-do-backend-que-possui-alteracao-de-tabela-no-banco-de-dados-5DD5E36PX9), deixando o serviço API rodando no Clusters no ECS.
3. Nesse passo temos duas situações, siga a que encaixa no seu caso:
   * **Situação 1:** Caso ainda **não tenha** realizado o deploy uma vez.

     Nesse caso, está mais tranquilo. Se você já realizou o [\*\*passo 2](/doc/como-realizar-um-deploy-do-backend-que-possui-alteracao-de-tabela-no-banco-de-dados-5DD5E36PX9),\*\* basta seguir para o **[passo 4](/doc/como-realizar-um-deploy-do-backend-que-possui-alteracao-de-tabela-no-banco-de-dados-5DD5E36PX9).**
   * **Situação 2:** Caso ainda **já tenha** rodado pelo menos uma vez .

     Nesse caso, é possível que se depare com o problema em que a migration não será aplicada, podendo (ou não) gerar log no CloudWatch informando sobre o DeadLock.

     Se esse for o caso caso de a migration não ter sido aplicada por causa de um Lock, será necessário realizar essas ações descritas aqui: **[Visualizar operações com LOCK no BD e matar a operação.](/doc/como-realizar-um-deploy-do-backend-que-possui-alteracao-de-tabela-no-banco-de-dados-5DD5E36PX9)** Além disso, precisamos verificar se no **redis** há a chave `*db_migration`,\* pois se houver, a aplicação das migrações ficaram bloqueadas. Portanto, será necessário removê-la.

     <aside> ⚠️ Quando uma migração vai ser aplicada, é criada uma chave no redis para realizar um lock no BD para a realização da migração.

     Caso tenha seguido os passos até aqui, e mesmo assim a migration não foi aplicada, será necessário [apagar do redis a chave](/doc/como-realizar-um-deploy-do-backend-que-possui-alteracao-de-tabela-no-banco-de-dados-5DD5E36PX9) `*db_migration` e então, tentar realizar o deploy novamente **(passo 4-b)**, forçando a implantação\*

     </aside>

     Após ver que não há mais operações que bloqueiam sua migration e não há mais a chave `*db_migration`\* no **redis**, vá para o [\*\*passo 4](/doc/como-realizar-um-deploy-do-backend-que-possui-alteracao-de-tabela-no-banco-de-dados-5DD5E36PX9).\*\*
4. Realizando o deploy

   
   1. **Item 3, situação 1:** Realize o deploy. Verifique se a alteração foi aplicada, caso não, confira os logs e faça o que está descrito na [\*\*situação 2](/doc/como-realizar-um-deploy-do-backend-que-possui-alteracao-de-tabela-no-banco-de-dados-5DD5E36PX9).\*\*
   2. **Item 3, situação 2:** Basta atualizar para a task definition (definição da tarefa) do serviço **API (apenas),** para a mais recente
5. **Após finalizar, subimos novamente** os outros serviços, atualizando-os também para a versão mais recente da Task Definition (Desfazendo a alteração realizada no **[passo 2](/doc/como-realizar-um-deploy-do-backend-que-possui-alteracao-de-tabela-no-banco-de-dados-5DD5E36PX9)**).

> Observação\*\*: Entendemos que essa não é a forma mais ideal de se fazer, porém até o momento é a solução que temos. No futuro deve ser repensado uma estratégia melhor para evitar que tenhamos que fazer todas essas ações de forma manual.\*

> Documento baseado na resolução do incidente [SZRICDT-6 | Site de Reservas Fora do Ar](/doc/szricdt-6-site-de-reservas-fora-do-ar-7NpG4rYovd)

### **FAQ**


---

* **Como parar um serviço de um Cluster ECS na AWS**
  * Marque o cluster e clique em "Atualizar".
  * Em seguida, e "Desired tasks" ou "Tarefas desejadas" altere o valor para zero (**IMPORTANTE: Guarde o valor que estava anteriormente**, vai ser preciso voltar ele ao valor original após finalizar o processo que está fazendo\*\*)\*\*
  * Após isso, basta salvar e verificar se o serviço está parado: O número de tarefas em execução deve ser **zero**)
* **Visualizar operações com LOCK no BD e matar a operação.**
  * Comando SQL: Veja as queries que estão com Lock

    ```jsx
    SELECT pid
    , query_start
    , datname
    , client_addr
    , coalesce(wait_event_type||'/'||wait_event,'') as wait
    , query
    , state
    FROM pg_stat_activity a
    WHERE pid <> pg_backend_pid()
    AND state <> 'idle'
    ORDER BY query_start desc nulls LAST
    ;
    ```
  * Comando SQL: Terminar (matar) operação do banco de dados com Lock

    **⚠️ USE ESSE COMANDO COM MUITA CAUTELA E ATENÇÃO, NÃO DEVE SER NORMAL RODÁ-LO COM FREQUÊNCIA. APENAS USE SE SOUBER O QUE ESTÁ FAZENDO ⚠️**

    ```sql
    -- Encerra uma operação que está rodando com base no pid (process id)
    SELECT pg_terminate_backend(492);
    ```
* **Como apagar chave** `db_migration` do redis para aplicar a migração
  * Acesse a instância EC2 em que o redis está rodando **(prod-reservas-001, stg-reservas-001)**

    > *Irá precisar da chave SSH* `toni.pem` para acessar a máquina, além de precisar adicionar seu IP no security group da EC2, permitindo o acesso via SSH
  * Execute o comando: `docker ps` e copie o CONTAINER ID
  * Acesse o redis-cli do container:  `docker exec -it CONTAINER_ID redis-cli`
  * Veja se a KEY de migração está no Redis: `get db_migration`
    * Se o retorno for `"1"` a key está lá, e possivelmente bloqueando as novas migrações
    * Se o retorno for `(nil)` então quer dizer que a key não está no redis, e está apto a aplicar novas migrações, podendo prosseguir com o deploy.
  * Se o retorno for `"1"` , então vamos precisar deletar essa Key para conseguirmos aplicar a migration.
    * Execute: `DEL db_migration`
    * Execute novamente: `get db_migration`
    * É esperado, que o retorno desse get seja `(nil)`