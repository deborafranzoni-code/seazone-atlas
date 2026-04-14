<!-- title: Gestão de contas | url: https://outline.seazone.com.br/doc/gestao-de-contas-Aqy8gCAxVU | area: Tecnologia -->

# Gestão de contas

## Estrutura do banco

### bill_management

| **Nome** | **Tipo** | **Nullable** | **Descrição** |
|----|----|----|----|
| id | PK | False | Identificação única |
| property_id | FK | False | Identificação da propriedade |
| created_at | timestamp | False | Data de criação do registro |
| updated_at | timestamp | False | Data de edição do registro |
| type | enum(bill_type) | False | Tipo da conta |
| supplier | varchar | False | Fornecedor da conta |
| due_day | int | False | Dia de vencimento |
| recurrence | enum(bill_recurrance) | False | Recorrência da conta |
| is_active | bool | False | Se a conta está ativa |
| inactivated_at | timestamp | True | Data em que a conta foi inativada |
| access_data | JSON | True | Dados necessário para obtenção da conta na plataforma externa |


### Enum bill_type

| **Enum Name** | **Tipo da Despesa** |
|----|----|
| CONDOMINIUM | Condomínio |
| ELECTRICITY | Eletricidade |
| INTERNET | Internet |
| PROPERTY_TAX | IPTU |
| COLLECTION_FEE | Taxa de coleta |
| WATER | Água |
| GAS | Gás |
| TAXES | Impostos |
| TV | TV |
| GARAGE_SPACE | Vaga de garagem |
| GARAGE_PROPERTY_TAX | IPTU da garagem |
| GARBAGE_COLLECTION | Coleta de lixo |
| EASYCOVER | Easycover |
| EXTRA | Extra |


### Enum bill_recurrence

| **Enum Name** | **Recorrência** |
|----|----|
| MONTHLY | Mensal |
| ANNUAL | Anual |