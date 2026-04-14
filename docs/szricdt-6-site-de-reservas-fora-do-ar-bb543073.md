<!-- title: SZRICDT-6 Site de Reservas Fora do Ar | url: https://outline.seazone.com.br/doc/szricdt-6-site-de-reservas-fora-do-ar-wBTKeuggdu | area: Tecnologia -->

# SZRICDT-6 Site de Reservas Fora do Ar

ID: SZRICDT-6 Data do Incidente: December 13, 2023 Created by: Bernardo Ribeiro Created time: December 15, 2023 10:22 PM Tags: AWS, Backend, Banco de Dados, Busca por Imóveis, Deadlock, Indisponibilidade da API

## Resumo do Incidente

* Ocorreu entre **December 12, 2023 9:00 AM (GMT-3) → December 13, 2023 7:28 PM (GMT-3)** ,
* Usuários não conseguiam acessar o site devido, se deparando com erro **HTTP 500.**
* O evento foi detectado pela [\*\*Status Page](https://seazone-reservas.betteruptime.com/) e\*\* pelos usuários que acessavam o site no momento. A equipe começou a trabalhar no evento às December 13, 2023 9:14 AM (GMT-3) assim que foi reportado no Canal de Suporte no Slack.
* Houve impacto adicional? Não.

## O que levou ao incidente

* O evento foi desencadeado **pelo Deploy** às **December 12, 2023 6:49 PM (GMT-3).**
* O Deploy continha uma migration (alteração nos modelos do BD) que realizava um **DROP TABLE na tabela de "Cards".**
* Devido ao fluxo de acesso que há no ambiente de produção (várias consultas e inserções sendo realizadas) durante o deploy, acabou **gerando um Lock no Banco de Dados**, **impedimento que a migração fosse executada**, esses Locks geraram um **grande acúmulo de sessões abertas** no BD, até que chegou um ponto onde não era mais possível realizar nem um select nele.

## O que não funcionou como esperado

A migração que continha DROP TABLE implementado não aplicou como era esperado ao realizar o deploy. O que gerou locks no BD, fazendo com que todas consultas que necessitavam de algum dado do BD, ocorressem erro. Isso durou Até ás 12h00 (meio-dia) quando conseguimos reiniciar o Banco de Dados e resetar as sessões abertas.

## Impacto

*Descreva como o incidente afetou os usuários internos e externos durante o incidente. Inclua quantos casos de suporte foram abertos.*

* Entre **December 12, 2023 7:20 AM (GMT-3)**  e **December 13, 2023 12:15 AM (GMT-3), todos usuários** que tentaram acessar enfrentaram este incidente.
* Foram enviados **4 Chamados** de Suporte (3 pelo Slack, 1 pelo Jira)
* Estima-se perda de R$**13,379.41** em Faturamento, ou seja, em média 5 reservas
* Houve uma queda de **500** usuários únicos com relação ao dia anterior.

## Detecção do incidente

* Este incidente foi detectado quando **chegou o chamado no canal do Slack** `#website-support`  e o time de desenvolvimento do site foi acionado.
* Também foi relato por usuários ao time de atendimento.
* E também foi visto na [\*\*página de status](https://seazone-reservas.betteruptime.com/).\*\*

> *A implementação de uma ferramenta de observabilidade de em nossa Infra deverá implementada para que sejamos mais pró-ativos quando ocorrer problemas em nosso site e/ou até previni-los, para que não fiquemos sabendo que algo estourou quando atingir o usuário final.*

* Conseguimos detectar o aumento de sessões ao acessar o **Amazon RDS** e verificar as sessões ativas do BD

## Causa raiz

* Migration não aplicada devido a selects na tabela que a tabela a ser deletada tinha relação.
  * Notamos que ela não foi aplicada pelo fato de ainda existir a tabela no BD e após o deploy, a Task Definition do serviço `seazone-reservas-api` não foi atualizada para a "mais recente".
* O que levou elevou o número de conexões abertas no BD até atingir sua capacidade máxima.

  ![](/api/attachments.redirect?id=ba164568-2f61-4d5c-8dd8-383975e369cf)

  **Sessões ativas do BD**

  ![](/api/attachments.redirect?id=c4c0bdc2-7d84-4298-b785-2684965aa4bc)

  **Consultas SQL com Lock no BD**
* Isso impediu que qualquer outro SELECT ou operação no BD fosse concluída, gerando erros de timeout na API.

## Resposta ao incidente

Após receber um alerta às December 13, 2023 9:00 AM (GMT-3) , todo o time se reuniu para investigar e solucionar o problema.

## Como o incidente foi resolvido

* Para resetar a sessões abertas e nunca fechadas: Reiniciamos o BD.
* Para conseguir rodar a migration e evitar que o problema persistisse:
  * Pausamos os Workers e Scheduler, deixando apenas o serviço API rodando no Clusters no ECS.
  * Além de pausar, também visualizamos as consultas que estavam com lock no BD (expanda para ver o comando).

    **Comando SQL:**

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
  * **Matamos cada uma** das operações **DROP TABLE** que estavam rodando infinitamente e também **matamos** as operações que estavam **fazendo SELECT na tabela Users**

    **Comando SQL:** `SELECT pg_terminate_backend(492);`
  * **Atualizamos a task definition** **para mais recente** e aguardamos o deployment finalizar.
  * **Após finalizar, subimos novamente** os outros serviços, atualizando-os também para a versão mais recente da Task Definition.

## Backlog Check

Não há itens no backlog que poderiam ter melhorado este serviço.

Há uma observação sobre a implementação de ferramentas de observabilidade para que possamos chegar no problema raiz e mitigar falhas com mais rapidez.

## Recorrência (incidentes semelhantes)

No deploy do dia 24/11 ([Release v0.2.10](https://github.com/Khanto-Tecnologia/seazone-reservas-api/releases/tag/v0.2.10)) ocorreu problema semelhante (Deadlock) ao tentar subir features que alteravam uma tabela e criava uma nova. Conseguimos solucionar após algumas re-tentativas de deploy.

## Lições aprendidas + Ações para mitigar esse tipo de incidente

* Necessidade de ferramentas de observabilidade melhores
* Mais atenção em deploys que envolvem alteração em tabelas do Banco de Dados.
  * Devemos sempre deixar apenas o serviço da API rodando e então rodar o deploy.
  * Devemos ficar online até finalizar afim e monitorar após o deploy se as alterações que foram feitas, foram aplicadas corretamente.
* Alteração de BD dar certo no local e em staging, não significa que vai dar certo em produção devido o fluxo de acessos que o ambiente de produção possui.


---

**Artigo Gerado:** [Como realizar um deploy do Backend que possui alteração de tabela no Banco de Dados](/doc/como-realizar-um-deploy-do-backend-que-possui-alteracao-de-tabela-no-banco-de-dados-5DD5E36PX9)