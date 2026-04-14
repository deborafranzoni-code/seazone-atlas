<!-- title: [2025] Proposta de solução | url: https://outline.seazone.com.br/doc/2025-proposta-de-solucao-3qVTGbuXF9 | area: Tecnologia -->

# [2025] Proposta de solução

# Requisitos

* Sincronização com os dados da Pleno
* Armazenar os dados no nosso banco para não depender do status do serviço de terceiros
* Criar um modelo escalável e que facilite a comunicação futura com a Stays (próxima etapa)

# Proposta

## Modelos

### property_inspection

* `id` (int)
* `created_at` (datetime)
* `updated_at` (datetime)
* `property_id` (FK property_property) (associada por `property.code` + `status == Active` na hora do cadastro)
* `pleno_id` (int) (as informações que precisamos está numa API que só responde se usamos o ID deles, então armazenar esse dado para atualizar vistorias já registradas elimina uma requisição) 

### property_items

* `id` (int)
* `created_at` (datetime)
* `updated_at` (datetime)
* `pleno_item_id` (int)
* `pleno_item_name` (str)
* `stays_item_id` (str) (é um hash)
* `stays_item_name` (str)

### property_inspection_items

* `id` (int)
* `created_at` (datetime)
* `updated_at` (datetime)
* `inspection_id` (FK property_inspection)
* `item_id` (FK property_items)
* `included` (bool)

  \

## Endpoints


1. Atualizar uma única vistoria no banco de dados a partir do property_code ou property_id: `property/sync_inspection`
2. Atualizar todas as vistorias: `property/sync_all_inspections`
3. Atualizar todas as vistorias criadas desde ontem: `property/sync_recent_inspections`
4. Retornar os dados da property_inspections_items formatados para o Frontend: GET `property/inspection`


## Worker

* Executa diariamente a mesma tarefa que o endpoint 3 faria (até as últimas 48h)


## Dúvidas

* Esse modelo de dados é escalável o suficiente? Escolhi ele por que fazer queries com JSONField não parece ser muito bacana, então algo mais tradicional soou melhor
* Como criar um artefato que permita fazer o mapeamento de nomes das amenities na stays, no sapron e na pleno sem deixar hard-coded? Essa seria a parte responsável por preencher o campo `stays_item_id` da `property_items`, visto que o `stays_item_name` teria que vir de algum usuário
  * Pensei numa planilha onde os responsáveis pelo processo podem eles mesmos fazer a manutenção, sem criar suporte para nós. Já existe código que faz a integração com Google Sheets. Se esse for o caso, eu colocaria mais um endpoint para atualizar a `property_items` manualmente, e também colocaria uma task diária.