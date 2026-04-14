<!-- title: Carga do BD Terrenos para o BD Sapron | url: https://outline.seazone.com.br/doc/carga-do-bd-terrenos-para-o-bd-sapron-DZI5svCIMq | area: Tecnologia -->

# Carga do BD Terrenos para o BD Sapron

# Componentes atuais

* [Pipefy de Terrenos](https://app.pipefy.com/pipes/304543320): Workflow de análise de indicação de terrenos.
* [Pipefy de Indicações de Terrenos](https://app.pipefy.com/pipes/306376151): Workflow de análise de dados prévia de terrenos indicados por parceiros. Após validação, o terreno é transferido para o Pipefy de Terrenos.
* [Formulário de Indicação de Terrenos](https://app.pipefy.com/organizations/330500/interfaces/741579fb-df99-4642-9b5a-d8e290b6f6ce/pages/00e630fb-4c13-45b0-b114-98271b58d36f?form=5c073a3d-67ec-4cc6-abe3-999f42568b62&origin=public%20form): Utilizado no Sapron para que o Parceiro faça a indicação de um terreno. Após submissão, um card é criado no Pipefy de Indicações de Terrenos.
* [BD Terrenos](https://docs.google.com/spreadsheets/d/1U7E3wCKaGpMOaMlfKdnR-0L1hyBIjOTlb93f_kg6GIM/edit?gid=220134111#gid=220134111): Dados normalizados do Pipefy de Terrenos em forma de planilha.
* [BD Sapron — partners_indications_allotment](https://metabase.seazone.com.br/dashboard/130-terrenos): Tabela em que atualmente armazenamos as indicações de terrenos realizadas por parceiros.

# Decisões arquiteturais

## Fonte de dados

### Pipes de Terrenos + Pipe de Indicação de Terrenos + BD Sapron de Indicações

 ![](/api/attachments.redirect?id=80d9e069-7b2d-44b8-8f1f-bdddb4b4cdde " =1153x424")

Nesse fluxo, o parceiro realiza a indicação do terreno via Sapron, criando um registro na tabela de indicações e posteriormente criando o card no Pipefy de Indicações de Terrenos. O parceiro Sapron enxerga apenas o BD Sapron.

O card criado no Pipe de Indicações de Terrenos pode ou não ser movido para o Pipe de Terrenos.

Dessa forma, há de se ter uma sincronização entre as três fontes de dados, de tal forma que o BD Sapron tenha as informações corretas a respeito da indicação. Toda e qualquer alteração nos Pipes deve refletir no registro atrelado no BD Sapron, inclusive quando há a movimentação entre Pipes.

Problemas:

* Precisamos manter a sincronia entre as fontes de dados;
* Precisamos adequar o formulário de criação de terrenos no Sapron;
* Pouco escalável;

Benefícios:

* Não há necessidade de mudanças de fluxo por parte do time de Terrenos;
* Toda indicação realizada pelo Sapron será mostrada na listagem imediatamente;

### Pipe de Terrenos + BD Sapron de Indicações

 ![](/api/attachments.redirect?id=8c294f96-09e0-4a3d-94a5-5f16ad8b3a6d " =1153x279")

Nesse fluxo, o parceiro realiza a indicação do terreno via Sapron, criando um registro na tabela de indicações e posteriormente criando o card no Pipefy de Terrenos. O parceiro Sapron enxerga apenas o BD Sapron.

Dessa forma, toda e qualquer alteração no Pipe de Terrenos deve refletir no BD do Sapron.

Problemas:

* Precisamos manter a sincronia entre o Pipe de Terrenos e o BD Sapron;
* Precisamos adequar o formulário de criação de terrenos no Sapron;
* O time de Terrenos precisará ajustar o fluxo para considerar que não utilizaremos o Pipe de Indicações de Terrenos;

Benefícios:

* Solução escalável;


* Toda indicação realizada pelo Sapron será mostrada na listagem imediatamente;

## Períodos de sincronização

### Sincronização periódica (cronjob)

* [Sincronização utilizada no site de Terrenos](https://app.nekt.ai/catalog?selectedTable=service.pipefy_mapa_terrenos_transformada&tab=lineage)
* [Sincronização com BigQuery](https://app.nekt.ai/destinations/bigquery-l7eB)

A ideia é fazer a sincronia dos Pipes de forma periódica (por exemplo, às 8h e 18h) com o BD do Sapron.

Problemas:

* Nossa base pode ficar desatualizada, dependendo do período de sincronização;
* Dependendo da carga de dados, pode ocorrer sobrecarga no BD do Sapron;
* Deve-se escolher uma forma de atualização: upsert ou overwrite;
* Pouco escalável;

Benefícios:

* Solução simples;

### Sincronização reativa (webhook)

* [Documentação — Pipefy Webhooks](https://developers.pipefy.com/reference/pipe-table-webhooks#card-and-record-management-webhooks)

A ideia é fazer a carga inicial dos dados contidos na [BD terrenos](https://docs.google.com/spreadsheets/d/1U7E3wCKaGpMOaMlfKdnR-0L1hyBIjOTlb93f_kg6GIM/edit?gid=220134111#gid=220134111), e a partir de mudanças no Pipe utilizado como fonte de dados, atualizar os dados do BD.

Problemas:

* Solução complexa;
* Erros no processamento do webhook ocasionam em dados desatualizados;

Benefícios:

* Bastante escalável;
* Baixa chance/período de dados desatualizados;
* Baixa chance de sobrecarga no BD do Sapron;

## Relacão entre o terreno e o parceiro que o indicou

### Utilizando pipedrive_person_id

A tabela no BD do Sapron terá a coluna `pipedrive_person_id`.

Os cards do Pipe de Terrenos armazenam a informação do ID do Parceiro no Pipedrive (coluna id_do_parceiro no [catálogo de colunas extendidas](https://app.nekt.ai/catalog?selectedTable=service.pipefy_szi_all_cards_304543320_colunas_expandidas)).

Ao fazer a sincronização, armazenaremos o pipedrive_person_id para relacionar o parceiro que indicou o terreno.

Problemas:

* Para identificar os terrenos indicados de um parceiro Sapron (account_partner), teremos que fazer o mapeamento entre **pipedrive_person_id <> partner_id** via JOIN;
* Tabela no BD do Sapron não terá nenhuma referência direta aos parceiros;

Benefícios:

* Ao fazer a sincronização, não é necessário fazer o mapeamento entre **Pipedrive Person <> Sapron Partner**, uma vez que isso é feito na própria busca;

### Utilizando partner_id

A tabela no BD do Sapron terá a coluna `partner_id` que referenciará a tabela `account_partner`.

Os cards do Pipe de Terrenos não armazenam a informação do ID do Parceiro no Sapron.

Na sincronização, deveremos fazer o mapeamento entre **pipedrive_person_id <> partner_id.**

Problemas:

* Dependendo do tipo de sincronização, o mapeamento entre os IDs pode impactar no tempo;

Benefícios:

* Para identificar os terrenos indicados de um parceiro Sapron (account_partner), basta filtrar pela coluna `partner_id`;
* Tabela no BD do Sapron possui referência direta aos parceiros.


\