<!-- title: Padrão de canais em Dados | url: https://outline.seazone.com.br/doc/padrao-de-canais-em-dados-p27aafeGIY | area: Tecnologia -->

# Padrão de canais em Dados

## **Padrão de Nomenclatura para entrega de dados para squads, times e areas da Seazone (externo ao time de data):**\n

```javascript
data-alerts-<nome_cliente_se_houver>-<contexto_alerta>
data-reports-<nome_cliente_se_houver>-<contexto_alerta>
```

\nOnde:

* data-alerts: Indica que são alertas relacionados a dados.
* data-reports: Quando entregamos relatorios, csv's e listas que não sejam alertas.
* <nome_cliente_se_houver>: O nome do cliente (ex: rm, terrenos). Use um identificador curto e padronizado para o cliente, sempre em minúsculas e sem espaços (use hífen se necessário, ex: banco-xyz). Se o objetivo são varias areas, não é necessário colocar um cliente.
* <contexto_alerta>: Esta é a parte mais flexível e precisa ser bem definida. Pode ser:
  * **Projeto específico:**

    ```javascript
    projeto-migracao-crm
    dashboard-vendas
    ```
  * **Tipo de dado/sistema:**

    ```javascript
    qualidade-dados-sap
    pipeline-etl-comercial
    ```
  * **Relatório específico:**

    ```javascript
    relatorio-churn-mensal
    performance-campanha-x
    ```
  * **Severidade/Tipo de alerta (se for genérico para o cliente):**

    ```javascript
    erros-criticos
    avisos-performance
    ```

    (menos comum se você já tem o contexto).

**Exemplos Práticos:**

* data-alerts-rm-qualidade-pedidos
* data-reports-rm-pipeline-vendas-diarias
* data-reports-terrenos-relatorio-engajamento-semanal
* data-alerts-terrenos-erros-integracao-api
* data-alerts-erros-integracao-gcp


### **Regras Adicionais para Nomenclatura:**


1. **Sempre minúsculas:** Facilita a digitação e a busca.
2. **Use hífen (** Evite underscores (_) ou espaços.
3. **Seja conciso, mas descritivo:** O nome deve dar uma ideia clara do conteúdo do canal.
4. **Evite caracteres especiais:** Além do hífen.
5. **Padronize abreviações (se usar):** Se for abreviar "relatório" para "rel", use sempre "rel".


### **Recomendações para Canais (Não Deixar Privado e Outras):**


**Visibilidade: Público por Padrão (Dentro do Workspace)**


**Por quê?**

* **Transparência:** Qualquer pessoa do time de dados (ou times relacionados como Sucesso do Cliente, Engenharia) pode encontrar e, se necessário, participar ou acompanhar as discussões e resoluções.
* **Conhecimento Compartilhado:** Soluções para um problema de um cliente podem ser úteis para outros. Um canal público permite que outros aprendam.
* **Facilidade de Acesso:** Evita o "quem eu preciso adicionar?" quando alguém novo precisa de acesso ou quando alguém precisa cobrir férias.


* **Redução de Silos:** Informação não fica presa a poucas pessoas.


* **Exceção para Privado:**


* Se o canal for discutir informações *extremamente* sensíveis do cliente que não deveriam ser vistas por *todo* o workspace, mesmo que internamente. Nesse caso, o canal privado deve ter uma justificativa clara e um grupo restrito.
* Canais temporários para investigações muito específicas e sensíveis podem ser privados e depois arquivados/deletados.


**Descrição do Canal (Purpose):**

* Sempre preencha a descrição do canal!
* Exemplo: "Alertas de qualidade de dados para o pipeline de vendas diárias do cliente Acme. Responsável: @fulano. Contato do cliente: [ciclano@cliente.com](mailto:ciclano@cliente.com)".
* Inclua o objetivo principal, quem são os principais stakeholders e talvez um link para documentação relevante.


**Tópico do Canal (Topic):**

* Use o tópico para informações dinâmicas ou links importantes, como o status atual de um problema, link para um dashboard de monitoramento, ou o último incidente reportado.


**Mensagens Fixadas (Pinned Messages):**

* Fixe mensagens importantes: Procedimentos padrão de resposta a alertas, contatos chave, links para runbooks ou documentação de resolução.


**Use Threads:**

* Fundamental! Para cada novo alerta ou discussão, inicie uma thread. Isso mantém o canal principal limpo e organizado, facilitando o acompanhamento de conversas específicas.


**Notificações:**

* Instrua os membros a configurarem suas notificações. Para canais de alerta, geralmente é desejável que as notificações sejam mais imediatas para os responsáveis diretos.
* Use @menções com moderação, mas de forma eficaz para direcionar a atenção de pessoas específicas ou grupos (@data-team-oncall).


**Emojis para Status:**

* Considere usar um sistema de emojis para indicar o status de um alerta:

  \


* ![:rotating_light:](https://a.slack-edge.com/production-standard-emoji-assets/14.0/google-medium/1f6a8.png "left-50 =42x42") ou ![:fire:](https://a.slack-edge.com/production-standard-emoji-assets/14.0/google-medium/1f525.png "left-50 =42x42") para um novo alerta crítico.


\
* ![:eyes:](https://a.slack-edge.com/production-standard-emoji-assets/14.0/google-medium/1f440.png "left-50 =42x42") para "investigando".

  \
  \


* ![:hammer_and_wrench:](https://a.slack-edge.com/production-standard-emoji-assets/14.0/google-medium/1f6e0-fe0f.png "left-50 =42x42") para "trabalhando na correção".


\
* ![:white_check_mark:](https://a.slack-edge.com/production-standard-emoji-assets/14.0/google-medium/2705.png "left-50 =42x42") para "resolvido".


\
* ![:information_source:](https://a.slack-edge.com/production-standard-emoji-assets/14.0/google-medium/2139-fe0f.png "left-50 =42x42") para "informação/atualização".


\
**Arquivamento:**

* Canais de clientes ou projetos que não estão mais ativos devem ser arquivados (não deletados, para manter o histórico). Isso mantém a lista de canais ativa mais limpa.


**Documente o Padrão:**

* Crie uma página na sua wiki interna ou um documento compartilhado com o padrão de nomenclatura e as boas práticas de uso dos canais. Isso ajuda na adoção e consistência.


\
# Padrão de alerta interno / infraestrutura


[#alerts-critics-lake](https://seazone-fund.slack.com/archives/C08AS1CS63W) 

o **critics** é para quando algo quebra e precisa ser resolvido imediatamente, indicando uma falha crítica. 


[#alerts-warning-lake](https://seazone-fund.slack.com/archives/C08A8V6J7TR)

o **warning** é para problemas ou bugs comuns, algo que não necessariamente representa uma quebra e não requer ação imediata. Esse canal será mantido por mais algum tempo até termos certeza de que não há nenhum script "perdido" enviando mensagens para ele.