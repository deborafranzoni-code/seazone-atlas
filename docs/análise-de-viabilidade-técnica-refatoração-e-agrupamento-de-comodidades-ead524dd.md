<!-- title: Análise de Viabilidade Técnica: Refatoração e Agrupamento de Comodidades | url: https://outline.seazone.com.br/doc/analise-de-viabilidade-tecnica-refatoracao-e-agrupamento-de-comodidades-lbFXmMsKcV | area: Tecnologia -->

# Análise de Viabilidade Técnica: Refatoração e Agrupamento de Comodidades

# Contexto

## Glossário

* **Amenity / Comodidade:** representa uma comodidade pertencente a um imóvel, por exemplo, *ar-condicionado*.
* **Imported Amenities / Amenities Importadas:** uma comodidade que vem de uma fonte externa.
* **External Property:** representa um **prédio ou condomínio**, ou seja, uma entidade que agrupa múltiplos imóveis.
* **External Amenity:** representa uma comodidade associada a uma *external property* (prédio ou condomínio), geralmente compartilhada entre os imóveis.\n*Exemplo:* os imóveis do SPJ possuem uma piscina compartilhada, nesse caso, o vínculo é feito entre o SPJ (prédio) e a comodidade, em vez de cada unidade (SPJ001, SPJ002 etc.) ter seu próprio vínculo.
* **Agrupamento de Amenities:** conjunto que reúne várias comodidades relacionadas.

 

## Objetivo

Atualmente as amenities usadas no website são totalmente iguais e dependentes da stays, a ideia é eliminar essa dependência e possibilitar que tenhamos nossas próprias amenties.

Ainda deve ser possível "puxar" amenities de outras fontes (ex: Stays, Sapron), mas queremos ser capazes de ter nossa própria versão de uma amenity e também de agrupá-las. 


## O que não é nosso objetivo

…


## Requisitos

* Devemos ser capazes de renomear uma amenity vinda de outra fonte (ex: "Berço para Bebês" vindo da Stays deve pode chamar apenas "Berço" para nós).
* Deve ser possível adicionar uma amenity a um grupo. (ex: "Berço" e "Trocador" devem poder fazer parte de um grupo "Itens para Bebês").
* Deve ser possível adicionar uma amenity que não esteja em nenhuma das fontes (ex: Adicionar uma amenity "Mesa de Ping Pong").
* Deve ser possível gerenciar as amenities de um imóvel manualmente vira API.
* Deve ser possível gerenciar as amenities de um imóvel automaticamente via task.
* Deve ser possível fazer todas as operações descritas para amenities com external amenities.


## Premissas

* Uma amenity poderá estar em vários grupos.


# Estruturas

Esta seção descreve as novas estruturas definidas neste discovery, incluindo tabelas no banco de dados e índices no OpenSearch.

## Tabelas

O sufixo ==_website== é utilizado em algumas tabelas porque já existe uma versão delas que gerencia as amenities da Stays, ou seja, há uma tabela `amenities` que armazena as comodidades exatamente como elas vêm dessa única fonte atual. Para manter essa separação durante o desenvolvimento do projeto, adotamos o sufixo ==_website==. Ele poderá ser removido posteriormente, quando a antiga estrutura de amenities não for mais necessária.

### imported_amenities

Essa tabela irá guardar as amenities no formato que elas vêm da fonte.

```sql
CREATE TABLE imported_amenities (
    id INT PRIMARY KEY AUTOINCREMENT
    name VARCHAR(64) NOT NULL,
    -- Gerado automaticamente a partir do nome
    name_slug VARCHAR(64) NOT NULL,
    --
    source VARCHAR(64) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT FALSE
);
```


### imported_amenities_properties

Essa tabela irá guardar a relação dos imóveis e prédios com os amenities importados. Olhando pra ela conseguimos dizer quais amenities um imóvel tem de acordo com uma fonte.

```sql
CREATE TABLE imported_amenities_properties (
    property_code VARCHAR(64) NOT NULL,
    imported_amenity_id INT NOT NULL,
    -- property se refere a um imóvel
    -- building se refere a um prédio/condomínio
    property_type ENUM('property', 'building') NOT NULL
);
```


### amenities==_website==

Essa tabela armazena as amenities no formato e com os nomes que serão exibidos no website, funcionando como uma tradução ou adaptação das amenities importadas para a versão que será utilizada no site.

```sql
CREATE TABLE amenities_website (
    id INT PRIMARY KEY AUTOINCREMENT
    name VARCHAR(128) NOT NULL,
    -- Gerado automaticamente a partir do nome
    name_slug VARCHAR(64) NOT NULL,
    --
    is_active BOOLEAN NOT NULL DEFAULT FALSE,
    details VARCHAR(128) NOT NULL,
);
```


### property_amenities==_website==

Essa tabela irá armazenar a relação entre as amenities do website e os imóveis, definindo quais amenities pertencem a cada imóvel. Essa relação será utilizada pela UI para exibir as amenities associadas a um determinado imóvel.

```sql
CREATE TABLE property_amenities_website (
    amenity_id INT NOT NULL,
    property_id INT NOT NULL,
    created_by VARCHAR(128) NOT NULL DEFAULT 'system',
    FOREIGN KEY (amenity_id) REFERENCES amenities_website(id),
    FOREIGN KEY (property_id) REFERENCES properties(id)
);
```


:::info
**INFO:** O campo `created_by` indica se a relação (link) foi criada automaticamente pelo **sistema** ou manualmente por um **usuário**.\nEsse será utilizado para evitar a remoção automática de vínculos inseridos manualmente, por exemplo, quando uma *amenity* não existe em nenhuma fonte externa e foi criada diretamente por nós.

:::


### external_property_amenities==_website==

Essa tabela irá armazenar a relação entre uma external amenity e uma external property, definindo quais amenities do website estão associadas a um prédio ou condomínio.

```sql
CREATE TABLE external_property_amenities_website (
    amenity_id INT NOT NULL,
    external_property_id INT NOT NULL,
    created_by VARCHAR(128) NOT NULL DEFAULT 'system',
    FOREIGN KEY (amenity_id) REFERENCES amenities_website(id),
    FOREIGN KEY (external_property_id) REFERENCES external_property(id)
);
```


### imported_amenities_mapping

Essa tabela irá armazenar a relação entre as amenities importadas e as amenities do website, atuando como uma **camada de mapeamento e tradução** que permite definir a nossa própria nomenclatura para uma amenity importada, por exemplo.

```sql
CREATE TABLE imported_amenities_mapping (
    amenity_id INT NOT NULL,
    imported_amenity_id INT NOT NULL,
    FOREIGN KEY (amenity_id) REFERENCES amenities_website(id),
    FOREIGN KEY (imported_amenity_id) REFERENCES imported_amenities(id)
);
```


### group_amenities

Essa tabela irá armazenar os grupos de amenities, permitindo a criação e gestão de agrupamentos de amenities relacionadas.

```sql
CREATE TABLE group_amenities (
    id INT PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(128) NOT NULL, -- ou description
    name_slug VARCHAR(128) NOT NULL, -- ou code
    is_active BOOLEAN NOT NULL DEFAULT FALSE, -- ou active
    icon_name VARCHAR(128) NOT NULL,
    group_type VARCHAR(128) NOT NULL,
);
```


### amenities_groups

Essa tabela irá armazenar a relação entre as amenities do website e os grupos, permitindo definir agrupamentos de comodidades e identificar quais amenities pertencem a cada grupo, ou, inversamente, quais amenities compõem um determinado grupo.

```sql
CREATE TABLE amenities_groups (
    amenity_id INT NOT NULL,
    amenity_group_id INT NOT NULL,
    FOREIGN KEY (amenity_id) REFERENCES amenities_website(id),
    FOREIGN KEY (amenity_group_id) REFERENCES group_amenities(id)
);
```


## Índices

Descrever novos índices ou mudanças no índices existentes

# Fluxos

## Importar amenities da fonte

Responsável por importar amenities a partir de uma fonte externa e armazená-los no nosso banco de dados.

**Fluxo:**


1. Conecta-se à fonte externa e obtém todos os amenities disponíveis dessa fonte.
2. Armazena os amenities obtidos na tabela **imported_amenities**, mantendo um registro de quais amenities foram importados de cada fonte.


## Gerenciamento de amenities de um imóvel (manual)

Fluxo responsável por controlar manualmente as amenities associadas a um imóvel.

**Principais operações:**


1. Gerenciar amenities: adicionar, consultar, atualizar e remover amenities.
2. Vinculação com imóveis: associar ou desassociar uma amenity a um imóvel específico, garantindo que cada propriedade tenha a lista correta de amenities exibida.


## Gerenciamento de external amenities de uma external property (manual)

Fluxo responsável pelo gerenciamento manual das **external amenities** associadas a uma **external property**.

**Principais operações:**


1. Gerenciar external amenities: adicionar e remover external amenities.
2. Vinculação com external properties: associar ou desassociar uma external amenity a uma external property específica.


## Gerenciamento de grupos de amenities de um imóvel (manual)

Fluxo responsável pelo gerenciamento manual dos **grupos de amenities** associados a um **imóvel**.

**Principais operações:**


1. Gerenciar grupos de amenities: adicionar e remover grupos de amenities.
2. Vinculação com imóveis: associar ou desassociar um grupo de amenities a um imóvel específico.


## Gerenciamento da camada de tradução das amenities (manual)

Fluxo responsável pelo gerenciamento manual das **relações de tradução (DE-PARA)** entre amenities importados e amenities do website.

**Principais operações:**


1. Adicionar relação DE-PARA: associar um amenity importado a um amenity existente no website.
2. Remover relação DE-PARA: desvincular um amenity importado de um amenity do website.


## Sincronização de amenities de um imóvel (preenchimento automático)

Fluxo responsável pela **sincronização automática** das amenities de um **imóvel**, vinculando amenities importados às propriedades correspondentes no website.

**Principais operações:**


1. Buscar o **imported_amenity_id** na tabela **imported_amenities_properties** a partir do **code**.
2. Consultar a tabela de mapeamento **imported_amenities_mapping** para obter o **amenity_id** correspondente.
3. Inserir na tabela **properties_amenities** o vínculo entre a **Amenity** (`amenity_id`) e a **Property** (`prop.id`).


## Sincronização de external amenities de uma external property (preenchimento automático)

Fluxo responsável pela **sincronização automática** das **external amenities** de uma **external property**, vinculando amenities importados às external properties correspondentes no website.

**Principais operações:**


1. Buscar o **imported_amenity_id** na tabela **imported_amenities_properties** a partir do **code**.
2. Consultar a tabela de mapeamento **imported_amenities_mapping** para obter o **amenity_id** correspondente.
3. Inserir na tabela **external_property_amenities** o vínculo entre a **External Amenity** (`amenity_id`) e a **External Property** (`prop.id`).


# Rotas

Seção que **detalha** tanto as **novas rotas** quanto as **alterações em rotas existentes**, incluindo a descrição e o propósito de cada endpoint.

## **POST** /management/amenity

Cria uma nova comodidade na `amenities_website`. Insere na NOSSA estrutura os amenities da forma como NÓS queremos, do NOSSO jeito. Podendo variar a forma como escrevemos. Não necessariamente precisa seguir a escrita da Fonte. E não necessariamente precisa ser um amenity que está em alguma fonte.


## **PATCH** /management/amenity/{id}

Edita as informações de uma comodidade na `amenities_website`.


## **DELETE** /management/amenity/{id}

Apaga uma comodidade da `amenities_website`. Não deletar se estiver sendo usada por algum imóvel. Realiza um Soft-DELETE (is_active=False)


## **POST** /management/properties/amenities

Insere o link (relação) de uma amenity com um imóvel na `property_amenities_website`

Body: { prop_id, amenity_ids\[\] }


## **DELETE** /management/properties/amenities

Remove o link (relação) de uma amenity com um imóvel na `property_amenities_website`.

Body: { prop_id, amenity_ids\[\] }


## **POST** /management/amenities/groups

Cria um novo grupo de comodidade na `group_amenities`


## **PATCH** /management/amenities/groups/{id}

Edita as informações de um grupo de comodidades na `group_amenities`


## **DELETE** /management/amenities/groups/{id}

Apaga um grupo de comodidades da `group_amenities`. Realizar CASCADE dos links. Realiza um Soft-DELETE (is_active=False)


## **POST** /management/amenities/group/link

Insere o link (relação) de um amenity com um grupo na `amenities_groups`

Body: { group_id, amenity_ids\[\] }


## **POST** /management/amenities/groups/unlink 

Remove o link (relação) de uma amenity com um grupo da `amenities_groups`

Body: { group_id, amenity_ids\[\] }


## **POST** /management/properties/external-amenities

Insere o link (relação) de uma external amenity com uma external property na `external_properties_amenities_website`

Body: { external_prop_id, amenity_ids\[\] }


## **DELETE** /management/properties/external-amenities

Remove o link (relação) de uma external_amenity com uma external_property da `external_properties_amenities_website`.

Body: { external_prop_id, amenity_ids\[\] }

## POST /management/amenity/imported-amenities-mapping

Insere na tabela `imported_amenities_mapping` o de-para da NOSSA amenity com a amenity da fonte.


## DELETE /management/amenity/imported-amenities-mapping

Remove na tabela imported_amenities_mapping o de-para da NOSSA amenity com a amenity da fonte.


## 

# Worker Chains & Tasks

Tasks a novas e alterações em tasks existentes

## sync_imported_amenities ==(new)==

Responsável por importar **todos os amenities de uma fonte externa específica**.\nEssa task é executada **uma vez por semana** e implementa a lógica de pull das amenities de cada fonte.

Cada fonte possui sua própria lógica de importação, definida conforme suas particularidades e formato de dados.

De forma resumida, o processo consiste em:


1. **Buscar** na fonte externa **todos os amenities disponíveis**;
2. **Armazenar** os amenities obtidos na tabela `imported_amenities`.


## associate_imported_amenities_properties ==(new)==

Responsável por **associar as amenities importadas aos imóveis de uma fonte externa específica**.

O processo consiste em:


1. **Buscar** todos os imóveis da fonte externa;
2. Para cada imóvel, **obter todas as amenities associadas**;
3. **Registrar** a relação entre o imóvel e suas amenities na base local, utilizando as amenities previamente salvas em `imported_amenities`.


## sync_property_amenities ==(new)==

Responsável por sincronizar as amenities associadas a uma propriedade.


1. Busca, na tabela `imported_amenities_properties`, o campo `imported_amenity_id` correspondente ao `property_code`.
2. Com o `imported_amenity_id` em mãos, consulta a tabela de mapeamento `imported_amenities_mapping` para obter o `amenity_id`.
3. Insere, na tabela `properties_amenities_website`, o vínculo entre a **Amenity** (`amenity_id`) e a **Property** (`prop.id`).


## sync_external_property_amenities ==(new)==

Responsável por sincronizar as **external amenities** associadas a uma propriedade.


1. Busca, na tabela `imported_amenities_properties`, o campo `imported_amenity_id` correspondente ao `property_code`.
2. Com o `imported_amenity_id` em mãos, consulta a tabela de mapeamento `imported_amenities_mapping` para obter o `amenity_id`.
3. Insere, na tabela `external_properties_amenities_website`, o vínculo entre a **External Amenity** (`external_amenity_id`) e a **Property** (`prop.id`).


## updated_grouped_amenities

A ideia é ajustar a task **updated_grouped_amenities** para incluir uma **index_v2** que realize a indexação, no OpenSearch, dos grupos de amenities, incluindo os amenities que fazem parte de cada grupo.

Com isso, será possível:


1. Listar, via OpenSearch, os grupos de um imóvel e os amenities associados a cada grupo para aquele imóvel específico.
2. Permitir a busca por um amenity dentro de um imóvel específico.


# Diagrama

[https://miro.com/app/board/uXjVN47euTs=/?moveToWidget=3458764645446946360&cot=14](https://miro.com/app/board/uXjVN47euTs=/?moveToWidget=3458764645446946360&cot=14)

# Tarefas & Prazos

…

# Implementações Futuras

…