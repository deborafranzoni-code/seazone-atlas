<!-- title: 01 - Overview | url: https://outline.seazone.com.br/doc/01-overview-0yyaH67wP9 | area: Tecnologia -->

# 01 - Overview

# Introdução

Para tal solução foi utilizada a plataforma de dados Nekt, visando consolidar os dados dos contatos dos mais diferentes sabores e uma [planilha](https://docs.google.com/spreadsheets/d/1G3IkbBwYFlPh2abttFQS4JzhCr9PG3iO_QfTHqymE2Y/edit?gid=0#gid=0) (também encontrada na Nekt) para armazenamento dos disparos e suas respectivas datas. 


1. Tabelas : As tabelas utilizadas foram construídas na Nekt e salvas no lakehouse
2. Consulta : Consultas as tabelas construídas anteriormente criadas para cada sabor, utilizando os parâmetros especificos como consta na tabela da seção "[Sabores](https://outline.seazone.com.br/doc/disparos-de-notificacao-para-contatos-GYETDZfjDo)", visando facilitar a geração da base dentro da Nekt


# Tabelas

| Sabor | Nome | Descrição | Fonte |
|----|----|----|----|
| [Clientes SZS](https://app.nekt.ai/notebooks/notebook-2rOG) | [szs_owners_contacts](https://app.nekt.ai/catalog?selectedTable=silver.szs_owners_contacts) | Traz informações dos contatos dos proprietários de Imóveis : nome, email, telefone, data da ativação do proprietário | Sapron |
| [Clientes SZS](https://app.nekt.ai/notebooks/notebook-2rOG) | [szs_dim_property](https://app.nekt.ai/catalog?selectedTable=silver.szs_dim_property) | Informações dos imóveis dos proprietários da SZS : código do imóvel, bairro, cidade, estado, data de ativação do imóvel | Sapron |
| [Hóspedes](https://app.nekt.ai/notebooks/notebook-Ko6l) | [sapron_guests_szs_contacts](https://app.nekt.ai/catalog?selectedTable=silver.sapron_guests_szs_contacts) | Traz informações dos contatos dos hóspedes : nome, email, telefone | Sapron |
| [Hóspedes](https://app.nekt.ai/notebooks/notebook-Ko6l) | [sapron_dim_guests_szs_reservations](https://app.nekt.ai/catalog?selectedTable=silver.sapron_dim_guests_szs_reservations) | Informações de cada estadia do hóspede em imóveis da SZN : data de check-in, check-out, código do imóvel, cidade, estado | Sapron |
| Clientes SZI/MKTP | [pipedrive_persons_investors_contacts](https://app.nekt.ai/catalog?selectedTable=silver.pipedrive_persons_investors_contacts) | Traz informações dos contatos dos investidores : nome, email, telefone | Pipedrive |
| Clientes SZI/MKTP | [dim_spot_pipedrive_investors](https://app.nekt.ai/catalog?selectedTable=silver.dim_spot_pipedrive_investors) | Informações sobre o empreendimento, data de ganho e código da unidade | Pipedrive |
| Clientes Decor | [pipedrive_customers_decor_contacts](https://app.nekt.ai/catalog?selectedTable=silver.pipedrive_customers_decor_contacts) | Traz informações dos contatos dos clientes de decor : nome, email, telefone | Pipedrive |
| Clientes Decor | [pipedrive_dim_customers_decor_property](https://app.nekt.ai/catalog?selectedTable=silver.pipedrive_dim_customers_decor_property) | Informações dos imóveis dos clientes decor : data de ganho, condomínio, código do imóvel | Pipedrive |
| Lost - Pipedrive | [pipedrive_persons_contacts](https://app.nekt.ai/catalog?selectedTable=silver.pipedrive_persons_contacts) | Traz informações dos deals perdidos no Pipedrive : nome, email, telefone | PIpedrive |
| Lost - Pipedrive | [dim_pipedrive_deals](https://app.nekt.ai/catalog?selectedTable=silver.dim_pipedrive_deals) | Funil, data de lost e motivo de perda | Pipedrive |
| Leads | [rd_leads_contacts](https://app.nekt.ai/catalog?selectedTable=silver.rd_leads_contacts) | Traz informações dos leads : nome, email, telefone | RD Station |
| Leads | [rd_leads_conversions](https://app.nekt.ai/catalog?selectedTable=silver.rd_leads_conversions) | Informações sobre a vertical da SZN, data da ultima conversão, data de criação | RD Station |
| Parceiros | **[sapron_partners_contacts](https://app.nekt.ai/catalog?selectedTable=silver.sapron_partners_contacts)** | Informações de contato dos parceiros : nome, email, telefone e a data de criação | Sapron |

***\*\*Observação : As tabelas de cada sabor foram separadas dessa forma pois apresentam uma relação de um para muitos (1 —> \*).*** 

***Exemplo : Um proprietário SZS (szs_owners_contacts) pode possuir mais de um imóvel (szs_dim_property)***


\
# Relacionamento entre tabelas :

 

As tabelas de contatos e seus atributos ligam-se de acordo com a tabela abaixo : 

| Fonte de Dados | Sabor | Chave JOIN |
|----|----|----|
| Pipedrive | Todos | `table_1.id = table_1.person_id` |
| Sapron | Clientes SZS | `table_1.id = table_2.user_id` |
| Sapron | Hóspedes | `table_1.id = table_2.guest_id` |
| RD Station | Todos | `table_1.id = table_2.uuid` |

*\*Caso haja alguma dúvida, consulte a coluna* `*Fonte de Dados*` *na seção* `*"Tabelas"*` *acima*


Para  cruzar os dados de tais tabelas com a tabela de disparos, visando verificar os contatos elegíveis para disparo de acordo com os tipos de campanhas pré-estabelecidos (whatsapp e email) são utilizadas as seguintes chaves listadas a seguir : 


                                        *Relacionamento entre tabelas - Tabela de Sabores e Disparos*

| Fonte de Dados | Sabor | Coluna JOIN com disparos |
|----|:---:|:---:|
| Pipedrive | Todos |            `pipedrive_person_id` |
| Sapron | Hóspedes | `phone` |
| Sapron | Clientes SZS | `email` |
| RD Station | Leads | `email` |


\
# Consultas

As querys já estão prontas e modeladas de acordo com os parâmetros de cada sabor, podendo ser filtradas a partir de alguns parâmetros : 

| Sabor | Filtros |
|----|----|
| Clientes SZS | cidade e estado |
| Hóspedes | data último check-out, cidade |
| Clientes SZI/MKTP | data de ganho, empreendimento |
| Clientes Decor | data de ganho, condominio |
| Lost - Pipedrive | data de lost, funil |
| Leads | vertical, data de conversão |
| Parceiros | data de criação |