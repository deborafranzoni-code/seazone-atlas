<!-- title: Sprint 2 | url: https://outline.seazone.com.br/doc/sprint-2-fnt6x6Dx61 | area: Tecnologia -->

# Sprint 2

## Integração N8N com Sapron

### Objetivo

Mapear e documentar os principais campos utilizados nas integrações da **Sia** com os sistemas **Sapron** e **Wallet**, acessados por meio do **MCP (Model Context Protocol)**.

O objetivo dessa documentação é:

* Identificar a origem de cada dado
* Explicar o significado dos campos utilizados
* Mostrar como esses dados são utilizados pela Sia
* Facilitar entendimento e manutenção da integração pelo time técnico

  \

### Arquitetura da Integração

A Sia acessa dados externos por meio do **MCP (Model Context Protocol)**, que atua como uma camada intermediária entre a Sia e os sistemas externos.

Neste cenário, o MCP disponibiliza ferramentas que permitem consultar informações de **proprietários e unidades** no sistema **Sapron**.

Fluxo simplificado da arquitetura:

Sia → MCP (Model Context Protocol) → Integração Sapron → Dados de proprietários e unidades

Nesse modelo, a Sia não realiza chamadas diretas à API do Sapron, utilizando apenas as ferramentas disponibilizadas pelo MCP.

### Mapeamento de Campos: Proprietários

Origem dos dados: **Sapron (via MCP)**

| **Campo MCP (Original)** | **Tipo** | **Descrição** | **Importância para a Sia** |
|----|----|----|----|
| `**id**` | String/ID | Identificador único do registro | **Crítica**: Chave para o Update (SIA-70). |
| `**first_name**` | String | Primeiro nome | Saudação e exibição simples. |
| `**last_name**` | String | Sobrenome completo | Identificação formal. |
| `**email**` | String | E-mail do usuário | Comunicação oficial. |
| `**phone_number1**` | String | Telefone principal | Contato via WhatsApp. |
| `**phone_number2**` | String | Telefone secundário | Backup de contato. |
| `**gender**` | String | Gênero (ex: "Female") | Personalização de tratamento. |
| `**birth_date**` | Datetime | Data de nascimento | Ações de CRM (aniversários). |
| `**cpf**` | String | CPF | Validação de identidade. |
| `**cnpj**` | String | CNPJ | Identificação de PJ. |
| `**is_individual**` | Boolean | Se é pessoa física | Define se a Sia olha para CPF ou CNPJ. |
| `**corporate_name**` | String | Razão Social | Registro de empresas. |
| `**trading_name**` | String | Nome Fantasia | Nome comercial. |
| `**main_role**` | String | Papel principal (ex: "Owner") | Garante que o usuário é de fato um dono. |
| `**is_superuser**` | Boolean | Nível de permissão | Segurança (identifica admins). |
| `**is_active**` | Boolean | Status da conta | Verifica se o cadastro está liberado. |
| `**last_login**` | Datetime | Último acesso | Auditoria de engajamento. |
| `**created_at**` | Datetime | Data de criação | Histórico de entrada no sistema. |
| `**updated_at**` | Datetime | Última alteração | Controle de sincronização. |

#### **Query SQL de Extração:**

Esta query foi utilizada para mapear a estrutura completa e validar os campos disponíveis:

```javascript
SELECT 
    u.*, 
    o.*
FROM account_user u
INNER JOIN account_owner o ON u.id = o.user_id;
```

### Mapeamento de Campos: Unidades

Origem dos dados: **Sapron (via MCP)**

| Campo MCP (Original) | Tipo | Descrição |
|----|----|----|
| `**id**` | ID | Identificador único (Chave para a **SIA-70**) |
| `**created_at**` | Datetime | Data de criação do registro |
| `**updated_at**` | Datetime | Data da última modificação |
| `**code**` | String | Código da unidade (ex: CGN0306) |
| `**comission_fee**` | Decimal | Taxa de comissão |
| `**single_bed_quantity**` | Integer | Quantidade de camas de solteiro |
| `**double_bed_quantity**` | Integer | Quantidade de camas de casal |
| `**queen_bed_quantity**` | Integer | Quantidade de camas Queen |
| `**king_bed_quantity**` | Integer | Quantidade de camas King |
| `**single_sofa_bed_quantity**` | Integer | Quantidade de sofás-cama solteiro |
| `**double_sofa_bed_quantity**` | Integer | Quantidade de sofás-cama casal |
| `**pillow_quantity**` | Integer | Quantidade de travesseiros |
| `**bedroom_quantity**` | Integer | Quantidade de quartos |
| `**bathroom_quantity**` | Integer | Quantidade de banheiros |
| `**lavatory_quantity**` | Integer | Quantidade de lavabos |
| `**cleaning_fee**` | Decimal | Valor da taxa de limpeza |
| `**bond_amount**` | Decimal | Valor do caução |
| `**guest_capacity**` | Integer | Capacidade total de hóspedes |
| `**property_type**` | String | Tipo de propriedade (ex: Apartment) |
| `**status**` | String | Status da unidade (ex: Active) |
| `**activation_date**` | Datetime | Data de ativação no sistema |
| `**inactivation_date**` | Datetime | Data de inativação (se houver) |
| `**contract_start_date**` | Datetime | Data de início do contrato |
| `**contract_end_date**` | Datetime | Data de término do contrato |
| `**address_id**` | ID | ID do endereço vinculado |
| `**category_location_id**` | ID | ID da categoria de localização |
| `**host_id**` | ID | ID do anfitrião/gestor |
| `**partner_id**` | ID | ID do parceiro vinculado |
| `**cover_image_uid**` | String | Identificador da imagem de capa |
| `**balance_discount_rate**` | Decimal | Taxa de desconto de saldo |
| `**bank_details_id**` | ID | ID dos dados bancários vinculados |
| `**invoice_details_id**` | ID | ID dos dados de faturamento |
| `**category_id**` | ID | ID da categoria da unidade |
| `**region**` | String | Localização (Cidade, UF, Bairro) |
| `**is_to_keep_funds...**` | Boolean | Se deve manter fundos na Seazone |
| `**host_cleaning_comission_fee**` | Integer | Taxa de comissão de limpeza do host |
| `**host_reservation_comission_fee**` | Decimal | Taxa de comissão de reserva do host |
| `**churn**` | Boolean | Indicador se a unidade saiu da base |
| `**churn_date**` | Datetime | Data em que ocorreu o churn |
| `**stays_code**` | String | Código no sistema Stays (ex: EM16J) |
| `**stays_listing_id**` | String | ID do anúncio no Stays |

#### **Query SQL de Extração:**

Esta query foi utilizada para mapear a estrutura completa e validar os campos disponíveis:

```javascript
SELECT 
    *
FROM property_property;
```

### Fluxo de Uso dos Dados

O fluxo de utilização dos dados pela Sia ocorre da seguinte forma:


1. A Sia recebe uma solicitação relacionada a proprietário ou unidade.
2. A Sia utiliza uma ferramenta MCP para consultar os dados necessários.
3. O MCP acessa o sistema Sapron.
4. Os dados são retornados para a Sia de forma estruturada.
5. A Sia utiliza essas informações para gerar respostas ou executar regras de negócio.

### Fluxo de Operação e Lógica de Negócio

O workflow baseia-se em um roteamento dinâmico via nó **Switch**, que processa as requisições de acordo com o parâmetro `acao`:


1. **Consulta de Proprietários:** Realiza o cruzamento (*JOIN*) entre as tabelas de usuários e proprietários.
2. **Consulta de Unidades:** Extrai dados técnicos e operacionais de imóveis.
3. **Fluxo de Teste:** Ambiente isolado para validação de novas queries sem impacto nos caminhos de produção.

### Instruções de Uso

As requisições devem ser enviadas ao Webhook do n8n com o seguinte formato JSON:

```javascript
{
  "acao": "proprietarios" | "unidades" | "prop-unid" | "teste"
}
```

### Testes e Manutenção

* **Validação de Alterações:** Toda nova query deve ser validada primeiramente através do caminho de "teste" no n8n.
* **Monitoramento de Erros:** O sistema conta com um **Error Workflow** (Dedo-duro) que monitora falhas de execução. Em caso de erro persistente, um alerta é enviado aos canais de suporte técnico.
* **Auditabilidade:** O histórico de execuções no n8n deve ser consultado para depuração de inconsistências nos dados retornados.