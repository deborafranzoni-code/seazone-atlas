<!-- title: [SAP-2281] Especificação Técnica - aviso de importação de reservas | url: https://outline.seazone.com.br/doc/sap-2281-especificacao-tecnica-aviso-de-importacao-de-reservas-fU1BMcctSt | area: Tecnologia -->

# [SAP-2281] Especificação Técnica - aviso de importação de reservas

Para ter um melhor acompanhamento da saúde do sistema em relação a importação de reservas da Stays, precisamos melhorar o nosso processo de importação e processamento das reservas.

Atualmente, temos duas fontes principais de divulgação de problemas envolvendo reservas:


1. Canal `sapron-backend-logs`: reporta erros relacionados com a importação de reservas específicas;
2. Canal `sapron-x-stays`: reporta quando faz mais de 6 horas que uma reserva não foi criada no nosso banco de dados.

Essas duas formas são insuficientes para o time de produto identificar rapidamente problemas de integração com a Stays. A atividade [SAP-2281](/doc/httpsseazoneatlassiannetbrowsesap-2281-9nTtAUfyFj) descreve os problemas existentes na solução atual.


## Mudanças Propostas

### 1. Criação de tabela para registrar o processamento das reservas

Criar uma tabela chamada `reservation_processing_report` para guardar informações sobre todas as reservas importadas na Stays e processadas no Sapron. A partir dessa tabela, vamos conseguir gerar as métricas que o time de produto precisa para acompanhar a integração com a Stays.

Essa tabela teria os seguintes campos:

* `id`, `created_at`, `updated_at`;
* `stays_code`: código da reserva na Stays. Esse campo possui um índice `unique`;
* `status`: situação do processamento da reserva, se teve algum tipo de erro ou se a importação foi sucedida (possíveis status: 'pending', 'success');
* `pending_reason`: possíveis mensagens de erro que surgiram durante a importação indicando o motivo para a reserva continuar pendente.
* ` succeeded_at`: data em que o registro foi importado com sucesso.

Isso atende ao requisito: mostrar a causa provável da falha que levou as reservas a ficarem pendentes.


### 2. Criação de task de comparação de reservas

Para conseguirmos identificar possíveis reservas que deixaram de ser importadas, vamos precisar de um novo worker que busque na Stays as reservas criadas em um determinado período e compará-las com o que existe hoje na nossa base. Se tiver alguma divergência, isso seria notificado no canal `sapron-x-stays`.

Isso atende ao requisito: reportar número de reservas pendentes de importação.


### 3. Inserir mais logs no fluxo de importação de reservas

Inserir mais logs no código da `StaysHandler`, para que o time consiga acompanhar todo o processamento da reserva, identificar se teve algum erro ou se ela foi processada com sucesso. A mensagem de log deve possuir também um trace_id, para conseguirmos filtrar com facilidade no Grafana as mensagens referentes a uma reserva.

Isso atende a um dos requisitos: o sistema ter dados suficientes para investigação e correção rápida.