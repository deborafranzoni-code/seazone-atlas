<!-- title: Erros de Onboarding | url: https://outline.seazone.com.br/doc/erros-de-onboarding-bfCL05c6vH | area: Tecnologia -->

# ⚠️ Erros de Onboarding

# Validação Front-End ([WAL-1480](https://seazone.atlassian.net/browse/WAL-1480))

## 1️⃣ Erros de Formulário (Formik / Validação)

### 1.1 Campo: Email

**Condição:** Email inválido ou já cadastrado\n**Onde aparece:** Input + Toast\n**Mensagem:** "O e-mail inserido já está cadastrado!"\n**Tratamento:** `formik.setFieldError('email', ...)` + `formik.setFieldTouched('email', true, false)`


---

### 1.2 Campo: Data de Nascimento (born)

**Condição:** Idade fora do intervalo 12-123 anos\n**Onde aparece:** Input + Toast\n**Mensagem:** "A idade inserida deve ser entre 12 e 123 anos. Reveja o campo 'Data de nascimento'"\n**Tratamento:** `formik.setFieldError('born', ...)` + `formik.setFieldTouched('born', true, false)`


---

### 1.3 Campo: Pipedrive Person ID

**Condição:** Person ID já existe no sistema\n**Onde aparece:** Input + Toast\n**Mensagem:** "Person ID já cadastrado"\n**Tratamento:** `formik.setFieldError('pipedrive_person_id', ...)` + `formik.setFieldTouched('pipedrive_person_id', true, false)`


---

### 1.4 Campo: Código do Imóvel (propertyCode)

**Condição:** Código já existe e está ativo\n**Onde aparece:** Input + Toast\n**Bloqueio:** Submit abortado\n**Mensagem:** "Esse código de imóvel já existe e está ativo!"\n**Tratamento:** `formik.setFieldError('propertyCode', ...)` + `formik.setFieldTouched('propertyCode', true, false)` + `toast.error(...)`


---

### 1.5 Validação: Schema Condicional

**Condição:** Schema muda baseado em `ownerAlreadyExists`\n**Onde aparece:** Validação de todos os campos do schema\n**Tratamento:** `getValidationSchema(ownerAlreadyExists)` retorna schema diferente\n**Impacto:** Campos obrigatórios mudam dinamicamente


---

### 1.6 Validação: País do Proprietário

**Condição:** Validações diferentes para Brasil vs Internacional\n**Onde aparece:** Campos de endereço (CEP, Estado, etc.)\n**Dependência:** `ownerCountryIsBrazil` (derivado de `formik.values.isForeignUser`)\n**Impacto:** Máscaras, obrigatoriedade e validações de campos mudam


---

### 1.7 Validação: Comissão de Parceiro

**Condição:** `isPartnerIndication === true` mas valores de comissão inválidos\n**Onde aparece:** Botão de submit desabilitado\n**Função:** `validateCommission()`\n**Regra:** Se indicação de parceiro, `commission_value_type` não pode ser "Não se aplica", e dependendo do valor, `commission_period` pode ser obrigatório ou não\n**Impacto:** `disabledSaveButton` = true


---

### 1.8 Validação: Total de Erros

**Condição:** `getTotalErrors()` retorna contagem > 0\n**Onde aparece:** Botão de submit desabilitado\n**Dependência:** Debounced validation a cada 1s\n**Tratamento:** `setTotalErrors(errors)` → `disabledSaveButton` calculado via `useMemo`\n**Impacto:** Submit bloqueado até todos os erros serem corrigidos


---


## :two: Erros Vindos da API

### 2.1 `createOwnerAddress` (via `postAddress`)

#### Erro Genérico

**Payload:** Endereço inválido\n**Formato:** `Error` ou objeto com `detail`\n**Tratamento:** Capturado no `catch` de `handleCreateAccountOwner`\n**Mensagem:** Depende do backend — se não mapeado, exibe "Ocorreu um erro inesperado..."\n**Cleanup:** Se `mainAddress` foi criado mas `userId` não, deleta endereço


---

### 2.2 `createUser` (via `postUser`)

#### Email Duplicado

**Payload:** Email já cadastrado\n**Formato:** `e.detail.email = ["This email already exists"]` (array)\n**Tratamento:**

* `formik.setFieldError('email', 'O e-mail inserido já está cadastrado!')`
* `formik.setFieldTouched('email', true, false)`
* Toast com mensagem\n**Cleanup:** Deleta `mainAddress` se criado


---

#### Birth Date Inválido

**Payload:** Data de nascimento fora do intervalo permitido\n**Formato:** `e.detail.birth_date = ["Age must be between 12 and 123"]`\n**Tratamento:**

* `formik.setFieldError('born', 'A idade inserida deve ser entre 12 e 123 anos...')`
* `formik.setFieldTouched('born', true, false)`
* Toast\n**Cleanup:** Deleta `mainAddress`


---

#### Pipedrive Person ID Duplicado

**Payload:** Person ID já existe\n**Formato:** `e.detail.pipedrive_person_id = ["Already exists"]`\n**Tratamento:**

* `formik.setFieldError('pipedrive_person_id', 'Person ID já cadastrado')`
* Toast\n**Cleanup:** Deleta `mainAddress`


---

#### Erro Não Mapeado em `createUser`

**Payload:** Qualquer campo não listado em `fieldMapping`\n**Formato:** `e.detail[campo] = ["mensagem"]`\n**Tratamento:** Toast com `"${campo}: ${mensagem}"`\n**Cleanup:** Deleta recursos criados (address, user se aplicável)


---

### 2.3 `createOwner` (via `postOwner`)

#### Erro Genérico

**Payload:** Erro ao criar owner\n**Formato:** `Error` ou `e.detail`\n**Tratamento:** Capturado no `catch` de `handleCreateAccountOwner`\n**Mensagem:** Mensagem do backend ou genérica\n**Cleanup:** Deleta `mainAddress` e `userId` se criados


---

### 2.4 `postOwnerInvoice`

#### Telefone Inválido

**Payload:** Número de telefone com formato incorreto\n**Formato:** Não explicitamente tratado no `handleCreateInvoice`, mas pode ocorrer\n**Tratamento:** Erro genérico (cai no `catch` de `handleCreatePropertyAddress` ou `onSubmit`)\n**Mensagem:** Mensagem do backend


---

#### Erro ao Criar Invoice

**Payload:** Dados de faturamento inválidos\n**Formato:** `Error`\n**Tratamento:** Capturado no `catch` de `onSubmit`\n**Mensagem:** `e.message` ou genérica\n**Cleanup:** Deleta `propertyAddress` e `ownerResponse` se criados


---

### 2.5 `handleCreatePropertyAddress` (via `postAddress`)

#### Erro ao Criar Endereço da Propriedade

**Payload:** Endereço inválido\n**Formato:** `Error`\n**Tratamento:** Capturado no `catch` de `onSubmit`\n**Mensagem:** `e.message`\n**Cleanup:**

* Deleta `propertyAddress` se `id !== -1`
* Deleta `ownerResponse` se criado


---

### 2.6 `postUnifiedPropertyManager`

#### Deal ID Inválido

**Payload:** `pipedrive_deal_id` não é inteiro válido\n**Formato:** `e.detail.pipedrive_deal_id = ["A valid integer is required."]`\n**Tratamento:** Handler específico\n**Mensagem Toast:** "O campo 'DEAL ID' precisa ser um número com no mínimo 5 caracteres"\n**Cleanup:** Deleta `propertyAddress` e `ownerResponse`


---

#### Categoria Não Preenchida

**Payload:** `category_location` é `null`\n**Formato:** `e.detail.category_location = ["This field may not be null."]`\n**Tratamento:** Handler específico\n**Mensagem Toast:** "O campo 'Categoria' não foi preenchido"\n**Cleanup:** Deleta recursos criados


---

#### Código de Imóvel Duplicado (Backend)

**Payload:** Código já existe no backend\n**Formato:** `e.detail.non_field_errors = ["This property code already exists and is active"]`\n**Tratamento:** Handler específico\n**Mensagem Toast:** "Esse código de imóvel já existe e está ativo"\n**Cleanup:** Deleta recursos criados


---

#### Telefone de Contato Inválido

**Payload:** `onboarding_contact_phonenumber` com formato inválido\n**Formato:** `e.detail.onboarding_contact_phonenumber = ["The entered phone number is not valid."]`\n**Tratamento:** Handler específico\n**Mensagem Toast:** "O número de telefone não é válido"\n**Cleanup:** Deleta recursos criados


---

#### Erro Array no Root

**Payload:** API retorna array diretamente\n**Formato:** `Array.isArray(e) === true` ou `Array.isArray(e.detail) === true`\n**Tratamento:** Pega primeiro elemento: `e[0]` ou `e.detail[0]`\n**Mensagem Toast:** Primeira mensagem do array ou "Ocorreu um erro inesperado..."\n**Cleanup:** Deleta recursos criados


---

#### Erro com Múltiplos Campos

**Payload:** `e.detail` é objeto com múltiplos campos\n**Formato:** `{ campo1: ["erro1"], campo2: ["erro2"] }`\n**Tratamento:**

* Itera sobre todos os campos
* Aplica handlers específicos quando disponíveis
* Concatena todas as mensagens em um único toast\n**Mensagem Toast:** "campo1: erro1. campo2: erro2"\n**Cleanup:** Deleta recursos criados


---

#### Erro Não Mapeado em `postUnifiedPropertyManager`

**Payload:** Campo sem handler específico\n**Formato:** `e.detail[campo] = ["mensagem"]`\n**Tratamento:** Toast com `"${campo}: ${mensagem}"`\n**Cleanup:** Deleta recursos criados


---

### 2.7 `sendEmailWithUserCredentials`

#### Erro ao Enviar Email

**Payload:** Falha no envio de credenciais\n**Formato:** Não há `try/catch` explícito — erro pode propagar\n**Tratamento:** **RISCO** — Não há tratamento explícito, mas ocorre após `postUnifiedPropertyManager` ser bem-sucedido\n**Impacto:** Usuário vê tela final de sucesso, mas pode não receber email\n**Mensagem:** Nenhuma (erro silencioso)


---

### 2.8 Cleanup APIs (`deleteAddress`, `deleteUser`, `deleteOwner`)

#### Erro ao Deletar Recursos

**Payload:** Falha em operações de cleanup\n**Formato:** `Error`\n**Tratamento:** Wrapped em `Promise.allSettled` — erros são ignorados\n**Impacto:** **RISCO** — Recursos podem ficar órfãos no banco\n**Mensagem:** Nenhuma (erro silencioso)

## 📊 Tabela Resumo de Erros

| Trigger (Causa) | Output (Efeito no sistema / UX) |
|----|----|
| Email já cadastrado (API `createUser`) | Campo `email` com erro + Toast: "O e-mail inserido já está cadastrado!" + Cleanup de `mainAddress` |
| Data de nascimento inválida (API `createUser`) | Campo `born` com erro + Toast: "A idade inserida deve ser entre 12 e 123 anos..." + Cleanup |
| Pipedrive Person ID duplicado (API `createUser`) | Campo `pipedrive_person_id` com erro + Toast: "Person ID já cadastrado" + Cleanup |
| Código de imóvel duplicado (validação local) | Campo `propertyCode` com erro + Toast + Submit abortado |
| Código de imóvel duplicado (API backend) | Toast: "Esse código de imóvel já existe e está ativo" + Cleanup de recursos |
| Deal ID inválido (API `postUnifiedPropertyManager`) | Toast: "O campo 'DEAL ID' precisa ser um número com no mínimo 5 caracteres" + Cleanup |
| Categoria não preenchida (API) | Toast: "O campo 'Categoria' não foi preenchido" + Cleanup |
| Telefone inválido (API) | Toast: "O número de telefone não é válido" + Cleanup |
| Erro genérico em `createUser` (campo não mapeado) | Toast: "campo: mensagem" + Cleanup |
| Erro genérico em `postUnifiedPropertyManager` (campo não mapeado) | Toast: "campo: mensagem" + Cleanup |
| Erro array da API | Toast: primeira mensagem do array ou "Ocorreu um erro inesperado..." + Cleanup |
| Múltiplos erros da API | Toast concatenado: "erro1. erro2. erro3" + Cleanup |
| `handleCreateAccountOwner` retorna `null` | Submit abortado com `return` + Toast de erro da função |
| `ownerAlreadyExists` mas `owner` é `null` | Submit abortado silenciosamente (sem feedback) |
| `validateCommission()` retorna `false` | Botão "Salvar" desabilitado (sem mensagem explícita) |
| `totalErrors` > 0 | Botão "Salvar" desabilitado (sem mensagem explícita) |
| `formik.isSubmitting === true` | Botão "Salvar" desabilitado temporariamente |
| Enter pressionado no formulário | `preventDefault()` — submit não dispara |
| `resetFormik === true` | Formulário resetado + campos limpos + contexto resetado |
| `isForeignUser` muda e país incompatível | Campo `owner_address_country` resetado automaticamente |
| `owner_address_country` muda | `isForeignUser` atualizado automaticamente |
| `infosPipeDrive` vazio + `!owner?.owner_id` | `useEffect` retorna early — formulário não inicializa |
| `sendEmailWithUserCredentials` falha | Erro silencioso — propriedade criada mas email não enviado |
| Cleanup de recursos falha | Erro silencioso — recursos órfãos no banco (via `Promise.allSettled`) |
| Feature flag `ff_enable_onboarding_payment_methods` off | Campos de pagamento ignorados no payload |
| `dealID` vazio | `pipedrive_deal_id: undefined` no payload — pode causar erro backend |
| `stateMappings` incorreto | Estado normalizado errado — endereço salvo com UF incorreta |
| `categoriesLocations` vazio | `categoryId` inválido ou `undefined` — erro no backend |
| `listHost` ou `listPartner` vazios | IDs inválidos enviados no payload |
| Invoice reutilizada com dados incorretos | Nova propriedade herda dados errados da invoice existente |
| Erro em `createOwnerAddress` | Toast com mensagem do backend + Cleanup (se aplicável) |
| Erro em `createOwner` | Toast com mensagem do backend + Cleanup de `mainAddress` e `userId` |
| Erro em `postOwnerInvoice` | Toast com mensagem do backend ou genérica + Cleanup |
| Erro em `handleCreatePropertyAddress` | Toast: `e.message` + Cleanup de `propertyAddress` e `ownerResponse` |
| Debounce de validação em andamento | Botão pode estar habilitado/desabilitado incorretamente por até 1s |
| Listener de Enter em `window` | Afeta toda a janela — pode interferir com outros componentes |
| Payload com campos condicionais `undefined` | Backend pode rejeitar ou aceitar — comportamento inconsistente |
| Owner estrangeiro sem invoice existente | 2 invoices criadas (owner address + property address) |
| Owner brasileiro | 1 invoice criada (owner address) |
| Campo obrigatório não preenchido (Formik/Yup) | Campo com erro + validação via `getValidationSchema` + `disabledSaveButton === true` |
| Erro não tratado em qualquer API | Toast: "Ocorreu um erro inesperado, tente novamente mais tarde!" + possível cleanup parcial |


# Validação Back-End  ([WAL-1478](https://seazone.atlassian.net/browse/WAL-1478))

## Resumo dos Fluxos

**1. Novo Proprietário:**

* Criação de Endereço (Owner) -> Usuário -> Owner -> Endereço (Imóvel) -> Invoice -> Imóvel Unificado -> Envio de Credenciais.

**2. Proprietário Existente:**

* Criação de Endereço (Imóvel) -> Invoice -> Imóvel Unificado -> (Vínculo de Usuário).


---

## POST `/account/address/`

Utilizado para criação de endereços, tanto para o Owner quanto para a Propriedade.

### Payloads

```json
{
    "street": "string (max 255, opcional)",
    "number": "string (max 255, opcional)",
    "complement": "string (max 255, opcional)",
    "neighborhood": "string (max 255, opcional)",
    "city": "string (max 255, opcional)",
    "state": "string (max 255, opcional)",
    "postal_code": "string (max 10, opcional)",
    "country": "string (max 70, opcional)",
    "condominium": "string (max 255, opcional)"
}
```

### Payload field rules

#### `neighborhood`

* **Formato**: Apenas letras, hífens, espaços ou números.
* **Proibido**: Underscores (`_`) não são permitidos.
* **Regex**: `^(\w|\-)+((\w|\-|\ )+)$` e `^[^_]*$`

#### `country`

* **Formato**: Apenas letras, hífens, parênteses, vírgulas ou espaços.
* **Proibido**: Números e underscores (`_`) não são permitidos.
* **Regex**: `^([\w\-\(\),\ ]+)$` e `^[^0-9_]*$`

### Erros mapeados

#### **Validação de Bairro**

* **Descrição**: O campo bairro contém caracteres especiais não permitidos ou underscores.
* **Texto de erro**: "Insira um nome de bairro válido (Apenas letras, hífens, espaços ou números)"
* **Fields**: `neighborhood`

#### **Validação de País**

* **Descrição**: O campo país contém números ou underscores.
* **Texto de erro**: "Insira um nome de país válido (Apenas letras, hífens ou espaços)"
* **Fields**: `country`

#### **Erro de Formato**

* **Descrição**: Campo de texto com formato incorreto ou ultrapassando o limite de caracteres.
* **Tipo de erro**: `ValidationError`
* **Fields**: `neighborhood`, `country`, etc.


---

## POST `/account/user/`

Criação do usuário de acesso ao sistema.

### Payloads

```json
{
    "first_name": "string (max 255 chars, obrigatório)",
    "last_name": "string (max 255 chars, obrigatório)",
    "email": "email (único, case-insensitive, obrigatório)",
    "phone_number1": "string (max 255 chars, opcional)",
    "phone_number2": "string (max 255 chars, opcional)",
    "main_role": "string (max 50 chars, choices: Admin, Seazone, Attendant, Host, Owner, Partner, Guest, opcional)",
    "gender": "string (max 50 chars, choices: Female, Male, Not_informed, opcional)",
    "birth_date": "date (formato YYYY-MM-DD, opcional, idade entre 12-123 anos)",
    "is_individual": "boolean (opcional)",
    "cpf": "string (11 dígitos numéricos, opcional, validador CPF_validator)",
    "cnpj": "string (14 dígitos numéricos, opcional, validador CNPJ_validator)",
    "corporate_name": "string (max 100 chars, opcional)",
    "trading_name": "string (max 100 chars, opcional)",
    "is_staff": "boolean (opcional, default 'false')",
    "is_active": "boolean (opcional, default 'true')",
    "main_address": "integer (FK para Address, opcional)",
    "postal_address": "integer (FK para Address, opcional)",
    "user_permissions": "",
    "pipedrive_person_id": "string (único, opcional, default '')",
    "password": "string (obrigatório, validação Django password)",
    "password_confirmation": "string (obrigatório, deve coincidir com password)"
}
```

### Payload field rules

#### `email`

* **Unicidade**: Deve ser único no sistema.
* **Lookup**: A verificação é *case-insensitive* (`iexact`).

#### `cpf`

* **Formato**: Exatamente 11 dígitos numéricos.
* **Sanitização**: Não deve conter pontos ou hífens.
* **Validação**: Algoritmo de validação de CPF (`CPF_validator`).

#### `cnpj`

* **Formato**: Exatamente 14 dígitos numéricos.
* **Sanitização**: Não deve conter pontos, barras ou hífens.
* **Validação**: Algoritmo de validação de CNPJ (`CNPJ_validator`).

#### `pipedrive_person_id`

* **Unicidade**: Se fornecido, deve ser único no banco.

#### `birth_date`

* **Idade**: O usuário deve ter entre 12 e 123 anos na data do cadastro.

#### `password`

* **Confirmação**: `password` deve ser idêntico a `password_confirmation`.
* **Segurança**: Validação padrão do Django.

### Erros mapeados

#### **Email Duplicado**

* **Texto de erro**: "Email já cadastrado"
* **Fields**: `email`

#### **CPF Inválido/Formatado**

* **Texto de erro**: "Insira um CPF válido, sem caracteres separadores (pontos ou hífens)"
* **Fields**: `cpf`

#### **CNPJ Inválido/Formatado**

* **Texto de erro**: "Insira um CNPJ válido, sem caracteres separadores (pontos, contra-barras ou hífens)"
* **Fields**: `cnpj`

#### **Conflito de Pipedrive ID**

* **Texto de erro**: "Person ID já cadastrado"
* **Fields**: `pipedrive_person_id`

#### **Idade Inválida**

* **Texto de erro**: "User age must be over 12 and under 123 years."
* **Fields**: `birth_date`

#### **Erro de Formato**

* **Descrição**: Campo de texto com formato incorreto ou ultrapassando o limite de caracteres.
* **Fields**: `email`, `cpf`, etc.


---

## POST `/account/owner/`

Cria a entidade "Proprietário" vinculada ao Usuário.

### Payloads

```json
{
    "user": "integer (obrigatório, FK para User)",
    "invoice_address": "integer (obrigatório, FK para Address)",
    "profession": "string (max 255 chars, opcional, validação: sem números)",
    "nationality": "string (max 255 chars, opcional)",
    "marital_status": "string (max 50 chars, opcional, choices: 'Single', 'Married', 'Divorced', 'Widowed', 'Civil Union')",
    "is_partner_indication": "boolean (opcional, default false)",
    "referrer_partner": "integer (opcional, nullable, FK para Partner)"
}
```

### Payload field rules

#### `user`

* **Unicidade**: Um usuário só pode ter UM owner (relação OneToOne). Tentar criar um segundo owner para o mesmo user gera erro.
* **Tipo**: Deve ser um ID (integer), não string.

#### `profession`

* **Formato**: Apenas letras, hífens ou espaços. Números não são permitidos.

#### `invoice_address`

* **Obrigatoriedade**: Campo não pode ser nulo (Constraint DB `NOT NULL`).

#### `marital_status`

* **Validação de Escolha**: O valor deve estar estritamente dentro da lista de `Choices` permitidas.

### Erros mapeados

#### **Erro de Caracteres na Profissão**

* **Texto de erro**: "Insira um nome válido (Apenas letras, hífens ou espaços)"
* **Fields**: `profession`

#### **Erro de Integridade (User Duplicado)**

* **Descrição**: Violação de chave única. O User já possui Owner.
* **Tipo de erro**: `IntegrityError` (500)
* **Fields**: `user`

#### **Erro de Integridade (Endereço Nulo)**

* **Descrição**: Tentativa de salvar sem `invoice_address`.
* **Tipo de erro**: `IntegrityError` (500)
* **Fields**: `invoice_address`

#### **Objeto Não Encontrado**

* **Descrição**: `user_id` ou `invoice_address` fornecidos não existem.
* **Tipo de erro**: `DoesNotExist` (400)

#### **Valor Inválido (Enum)**

* **Descrição**: Valor fora das opções permitidas.
* **Tipo de erro**: `ValidationError` (400)
* **Fields**: `marital_status`, `meet_seazone`

#### **Erro de Formato**

* **Descrição**: Campo de texto com formato incorreto ou ultrapassando o limite de caracteres.
* **Fields**: `profession`, `marital_status`, etc.


---

## POST `/financial/owner/invoice_details`

Responsável por criar os dados de faturamento do proprietário.

### Payloads

```json
{
    "is_default": "boolean (default=False)",
    "invoice_entity_name": "string (max 255 chars, opcional)",
    "cpf": "string (max 11 chars, opcional)",
    "cnpj": "string (max 14 chars, opcional)",
    "email": "string (email, max 254, opcional)",
    "phone_number": "string (max 32 chars, opcional)",
    "postal_code": "string (max 32 chars, opcional)",
    "address": "string (max 256 chars, opcional)",
    "address_number": "string (max 32 chars, opcional)",
    "complement": "string (max 256 chars, opcional)",
    "district": "string (max 64 chars, opcional)",
    "city": "string (max 64 chars, opcional)",
    "state": "string (max 32 chars, opcional)",
    "user": "integer (FK para User - obrigatório)"
}
```

### Payload field rules

#### `user`

* **Validação de Existência**: Deve corresponder a um ID de `User` válido no banco de dados.
* **Vínculo com Owner**: O usuário fornecido **deve** possuir um registro de `Owner` associado.
* **Integridade de Conta**: O usuário deve possuir uma conta de Owner válida (validado via `get_is_default`).

#### `email`

* **Formato**: Deve ser um endereço de e-mail válido.

#### `is_default`

* **Regra de Negócio (Primeiro Registro)**: Se este for o primeiro `invoice_details` criado para o Owner, ele é automaticamente definido como `True` (padrão), independentemente do payload.
* **Regra de Negócio (Atualização)**: Se `is_default` for `True`, atualiza o Owner para usar este invoice como `default_invoice_details`.
* **Regra de Negócio (Fallback)**: Se `is_default` for `False` mas não existirem outros registros, torna-se `True` automaticamente.

#### `cpf` / `cnpj` / Demais campos de texto

* **Tamanho**: Devem respeitar rigorosamente o `Max Length` definido no Model (ex: CPF máx 11 chars).

### Erros mapeados

#### **Erro de ForeignKey**

* **Descrição**: O ID do usuário informado não existe ou é inválido.
* **Tipo de erro**: `ValidationError`
* **Fields**: `user`

#### **Erro de Vínculo com Owner**

* **Descrição**: O usuário existe, mas não é um proprietário (não tem registro na tabela Owner).
* **Tipo de erro**: `ValidationError`
* **Texto de erro**: (Variação de "User não possui registro de Owner")
* **Fields**: `user`

#### **Erro de Formato**

* **Descrição**: E-mail inválido ou campos de texto ultrapassando o limite de caracteres.
* **Tipo de erro**: `ValidationError`
* **Fields**: `email`, `cpf`, `cnpj`, etc.


---


## POST `/property/manager/`

Rota que cria `Property`, `Property_rules` e `PropertyHandoverDetails` em uma única transação.

### Payloads

O payload é composto por três objetos principais:


1. `property`: Dados cadastrais do imóvel.
2. `rules`: Regras de convivência (check-in, pets, etc).
3. `handover_details`: Dados financeiros da implantação.

#### Payload geral

```json
{
    "property": { },
    "rules": { },
    "handover_details": { }
}
```

#### Payload Property

```json
{
    "address": "integer (FK Address, obrigatório)",
    "host": "integer (FK Host, obrigatório)",
    "code": "string (3-4 letras maiúsculas + 3-4 números, obrigatório)",
    "comission_fee": "decimal (max_digits=50, decimal_places=2, opcional)",
    "property_type": "string (choices: House|Apartment|Hotel|Inn|Entire Building|Spot|Launch|Views|Studio, opcional)",
    "bedroom_quantity": "integer positivo (opcional)",
    "category_location": "integer (FK CategoryLocation, obrigatório)",
    "contract_start_date": "date (formato YYYY-MM-DD, opcional)",
    "balance_discount_rate": "decimal (max_digits=50, decimal_places=2, opcional)",
    "status": "string (choices: Active|Inactive|Onboarding|Closed|Signed Contract, opcional)",
    "owners": "array de integers (FK Owner, obrigatório - ManyToMany)",
    "owner": "integer (FK Owner, obrigatório)",
    "host_reservation_comission_fee": "float (opcional)",
    "host_cleaning_comission_fee": "float (opcional)",
    "has_insurance": "boolean (default=False, opcional)",
    "has_bill_management": "boolean (default=False, opcional)",
    "invoice_details": "integer (FK Invoice_details, opcional)",
}
```

#### Payload Rules

```json
{
    "allow_pet": "boolean (obrigatório)",
    "check_in_time": "string (max_length=50, obrigatório)",
    "check_out_time": "string (max_length=50, obrigatório)",
    "events_permitted": "boolean (obrigatório)"
    "smoking_permitted": "boolean (obrigatório)",
    "suitable_for_babies": "boolean (obrigatório)",
    "suitable_for_children": "boolean (obrigatório)",
}
```

#### Payload Handover Details

```json
{
    "plan": "string (choices: Full|Mid|Light|Digital Management|Essencial|Plus|Pool|Safe|Premium, opcional)",
    "comment": "string (text, opcional)",
    "implantation_items_description": "string (text, opcional)",
    "onboarding_contact_name": "string (text, opcional)",
    "onboarding_contact_phonenumber": "string (phone number format, opcional)",
    "property_area_size_m2": "float (opcional)",
    "payment_method": "string (choices: On Budget|Installments|Discount_Rate|Bank Slip|Credit Card|Pix|Madego, opcional)",
    "bed_linen_photo": "string UUID (FK FileItem, opcional)",
    "implantation_fee_total_value": "float (opcional)",
    "payment_installments": "integer (opcional)",
    "pipedrive_deal_id": "biginteger (opcional)"
    "property": "integer (FK Property, gerado automaticamente após criação)",
    "rules": "integer (FK Property_rules, gerado automaticamente após criação)",
}
```

#### Pipedrive (Handover Details):

Valores só existentes no Pipedrive - não enviados pelo front-end

```json
{
    "implantation_fee_entrance_value": "float (opcional)",
    "entrance_payment_method": "string (choices: On Budget|Installments|Discount_Rate|Bank Slip|Credit Card|Pix|Madego, opcional)"
}
```

### Payload field rules

#### `property.code`

* **Unicidade**: O código (3-4 letras + 3-4 números) deve ser único.
* **Exceção**: É permitido duplicar apenas se o status da propriedade existente for 'Inactive'.

#### `property` (FKs)

* **Validação de Relacionamentos**: `host`, `owners`, `address`, `category_location`, `invoice_details` devem apontar para objetos existentes. Falha resulta em `object does not exist`.

#### `handover_details`


1. **Entrada vs Parcelas**:

* Deve-se informar valor de entrada (`implantation_fee_entrance_value`) **OU** número de parcelas (`payment_installments`). Ambos não podem ser nulos/zero simultaneamente.
* Se `entrance_value` == `total_value`, parcelas não são permitidas.
* `entrance_value` não pode ser maior que `total_value`.
* Se `entrance_value` for < `total_value`, deve ser informado `payment_installments`.


2. **Métodos de Pagamento**:

* Se houver **parcelas**, `payment_method` (parcelamento) é obrigatório.
* Se houver **entrada**, `entrance_payment_method` é obrigatório.
* Se **não** houver entrada, `entrance_payment_method` não deve ser enviado.
* Se **não** houver parcelas, `payment_method` não deve ser enviado.


3. **Descontos (**`**Discount_Rate**`**)**:

* Se `payment_method` for `Discount_Rate`, uma taxa de desconto válida (>0) é obrigatória.
* A taxa deve ser um float entre 0 e 100.
* Taxa de desconto só é permitida se o método de pagamento for compatível.

#### `pipedrive_deal_id`

* **Validação Externa**: O Deal ID informado deve existir no Pipedrive.
* **Consistência**: A Pessoa (Person) associada ao Deal deve ser encontrada.

### Erros mapeados

#### **Erros de Pipedrive**

* **Texto de erro**: "Deal ID not found" ou "Person ID not found".
* **Fields**: `handover_details.pipedrive_deal_id`

#### **Duplicidade de Código**

* **Texto de erro**: "This property code already exists and is active".
* **Fields**: `property.code`

#### **Erros de Referência (FK)**

* **Texto de erro**: "Invalid pk "X" - object does not exist."
* **Fields**: `address`, `host`, `owners`, `category_location`, `invoice_details`.

#### **Erros Financeiros (Handover)**

##### **Métodos de Pagamento Obrigatórios**:

* **Texto de erro**: "O método de pagamento de parcelamento é obrigatório quando há número de parcelamentos informado"
* **Fields**: `payment_method`, `payment_installments`

  \
* **Texto de erro**: "O método de pagamento da entrada é obrigatório quando há valor de entrada informado"
* **Fields**: `entrance_payment_method`, `implantation_fee_entrance_value`

#### **Métodos de Pagamento inconsistentes**:

* **Texto de erro**: "O método de pagamento de parcelamento não deve ser informado quando não há número de parcelamentos válido"
* **Fields**: `payment_method`, `payment_installments`

  \
* **Texto de erro**:"O método de pagamento da entrada não deve ser informado quando não há valor de entrada válido"
* **Fields**: `entrance_payment_method`, `implantation_fee_entrance_value`

#### **Consistência de Valores**:

* **Texto de erro**:"É necessário informar valor de entrada ou número de parcelas"
* **Fields**: `implantation_fee_entrance_value`, `payment_installments`

  \
* **Texto de erro**:"O valor de entrada não deve ser maior que o valor total informado"
* **Fields**: `implantation_fee_entrance_value`, `implantation_fee_total_value`

  \
* **Texto de erro**:"Quando o valor de entrada é igual ao valor total, não são permitidas parcelas"
* **Fields**: `implantation_fee_entrance_value`, `implantation_fee_total_value`, `payment_installments`

  \
* **Texto de erro**:"É necessário informar o número de parcelas quando há saldo restante"
* **Fields**: `implantation_fee_entrance_value`, `implantation_fee_total_value`, `payment_installments`

#### **Logica de Desconto**:

* **Texto de erro**:"A taxa de desconto deve estar entre 0 e 100 porcento"
* **Fields**: `balance_discount_rate`

  \
* **Texto de erro**:"O valor da taxa de desconto é obrigatório para este método de pagamento"
* **Fields**: `payment_method`, `balance_discount_rate`

  \
* **Texto de erro**:"A presença da taxa de desconto requer método de pagamento válido associado"
* **Fields**: `payment_method`, `balance_discount_rate`

#### **Valores com tipo ou formato inválido**:

* **Texto de erro**:"O valor da taxa de desconto é inválido"
* **Fields**: `balance_discount_rate`

  \
* **Texto de erro**:"O número de parcelas informado é inválido"
* **Fields**: `payment_installments`

  \
* **Texto de erro**:"O valor de entrada informado é inválido"
* **Fields**: `implantation_fee_entrance_value`

  \
* **Texto de erro**:"O valor total informado é inválido"
* **Fields**: `implantation_fee_total_value`

## POST `/account/user/{user_id}/send_temporary_credentials`

# Models

### User

* `id`: AutoField (implícito) — Nullable: não
* `password`: CharField(128, implícito do AbstractBaseUser) — Nullable: não
* `last_login`: DateTimeField (implícito) — Nullable: sim (null=True)
* `first_name`: CharField(max_length=255) — Nullable: não
* `last_name`: CharField(max_length=255) — Nullable: não
* `email`: EmailField — Nullable: sim (null=True, blank=True)
* `phone_number1`: CharField(max_length=255) — Nullable: sim (null=True, blank=True)
* `phone_number2`: CharField(max_length=255) — Nullable: sim (null=True, blank=True)
* `main_role`: CharField(max_length=50) — Nullable: não
* `gender`: CharField(max_length=50) — Nullable: sim (null=True, blank=True)
* `birth_date`: DateField — Nullable: sim (null=True, blank=True)
* `main_address` (FK account.Address): ForeignKey — Nullable: sim (null=True, blank=True)
* `postal_address` (OneToOne account.Address): OneToOneField — Nullable: sim (null=True, blank=True)
* `is_individual`: BooleanField — Nullable: sim (null=True, blank=True)
* `id_number`: CharField(max_length=50) — Nullable: não (blank=True apenas)
* `cpf`: CharField(max_length=11) — Nullable: não (blank=True, default='')
* `cnpj`: CharField(max_length=14) — Nullable: não (blank=True, default='')
* `corporate_name`: CharField(max_length=100) — Nullable: não (blank=True)
* `trading_name`: CharField(max_length=100) — Nullable: não (blank=True)
* `is_staff`: BooleanField — Nullable: não
* `is_active`: BooleanField — Nullable: não
* `nickname`: CharField(max_length=255) — Nullable: não (blank=True)
* `pipedrive_person_id`: CharField(max_length=256) — Nullable: não (blank=True, default='')
* `required_actions`: JSONField — Nullable: sim (null=True, blank=True)
* `source`: CharField(max_length=50) — Nullable: não (blank=True, default='')
* `created_from_workflow_name`: CharField(max_length=50) — Nullable: não (blank=True, default='')

### Owner

* `id`: AutoField (implícito) — Nullable: não
* `user`: OneToOneField(account.User) — Nullable: não
* `nationality`: CharField(max_length=255) — Nullable: não (blank=True)
* `marital_status`: CharField(max_length=50) — Nullable: não (blank=True)
* `profession`: CharField(max_length=255) — Nullable: não (blank=True)
* `email_for_operation`: EmailField — Nullable: não (blank=True)
* `invoice_address`: ForeignKey(account.Address) — Nullable: não
* `default_bank_details`: ForeignKey(financial.Bank_details) — Nullable: sim (null=True)
* `default_invoice_details`: ForeignKey(financial.Invoice_details) — Nullable: sim (null=True)
* `hometown`: CharField(max_length=128) — Nullable: não (blank=True, default='')
* `properties_owned`: IntegerField — Nullable: sim (null=True, blank=True)
* `properties_to_rent`: IntegerField — Nullable: sim (null=True, blank=True)
* `instagram_profile`: CharField(max_length=64) — Nullable: não (blank=True, default='')
* `income`: DecimalField(max_digits=50, decimal_places=2) — Nullable: não (blank=True, default=0)
* `lives_same_town_as_property`: BooleanField — Nullable: sim (null=True, blank=True)
* `meet_seazone`: CharField(max_length=50) — Nullable: não (blank=True)
* `birth_city`: CharField(max_length=255) — Nullable: não (blank=True, default='')
* `transfer_day`: IntegerField — Nullable: sim (null=True, blank=True)
* `is_partner_indication`: BooleanField — Nullable: não (blank=True, default=False)
* `referrer_partner`: ForeignKey(Partner) — Nullable: sim (null=True, default=None)
* `source`: CharField(max_length=50) — Nullable: não (blank=True, default='')
* `created_from_workflow_name`: CharField(max_length=50) — Nullable: não (blank=True, default='')

### Address

* `id`: AutoField (implícito) — Nullable: não
* `street`: CharField(max_length=255) — Nullable: sim (null=True, blank=True)
* `number`: CharField(max_length=255) — Nullable: sim (null=True, blank=True)
* `complement`: CharField(max_length=255) — Nullable: sim (null=True, blank=True)
* `neighborhood`: CharField(max_length=255) — Nullable: sim (null=True, blank=True)
* `city`: CharField(max_length=255) — Nullable: sim (null=True, blank=True)
* `state`: CharField(max_length=255) — Nullable: sim (null=True, blank=True)
* `postal_code`: CharField(max_length=10) — Nullable: sim (null=True, blank=True)
* `country`: CharField(max_length=70) — Nullable: sim (null=True, blank=True)
* `condominium`: CharField(max_length=255) — Nullable: sim (null=True, blank=True)

### Property

* `id`: AutoField (implícito) — Nullable: não
* `code`: CharField(max_length=255) — Nullable: não
* `category_location`: ForeignKey(CategoryLocation) — Nullable: não
* `category`: ForeignKey(Category) — Nullable: sim (null=True)
* `region`: CharField(max_length=256) — Nullable: não (blank=True, default="")
* `address`: OneToOneField(account.Address) — Nullable: não (blank=True apenas)
* `comission_fee`: DecimalField(max_digits=50, decimal_places=2) — Nullable: sim (null=True, blank=True)
* `single_bed_quantity`: PositiveSmallIntegerField — Nullable: sim (null=True, blank=True)
* `double_bed_quantity`: PositiveSmallIntegerField — Nullable: sim (null=True, blank=True)
* `queen_bed_quantity`: PositiveSmallIntegerField — Nullable: sim (null=True, blank=True)
* `king_bed_quantity`: PositiveSmallIntegerField — Nullable: sim (null=True, blank=True)
* `single_sofa_bed_quantity`: PositiveSmallIntegerField — Nullable: sim (null=True, blank=True)
* `double_sofa_bed_quantity`: PositiveSmallIntegerField — Nullable: sim (null=True, blank=True)
* `pillow_quantity`: PositiveSmallIntegerField — Nullable: sim (null=True, blank=True)
* `bedroom_quantity`: PositiveSmallIntegerField — Nullable: sim (null=True, blank=True)
* `bathroom_quantity`: PositiveSmallIntegerField — Nullable: sim (null=True, blank=True)
* `lavatory_quantity`: PositiveSmallIntegerField — Nullable: sim (null=True, blank=True)
* `cleaning_fee`: DecimalField(max_digits=50, decimal_places=2) — Nullable: sim (null=True, blank=True)
* `bond_amount`: DecimalField(max_digits=50, decimal_places=2) — Nullable: sim (null=True, blank=True)
* `guest_capacity`: PositiveSmallIntegerField — Nullable: sim (null=True, blank=True)
* `property_type`: CharField(max_length=50) — Nullable: não (blank=True apenas)
* `status`: CharField(max_length=50) — Nullable: não (blank=True apenas)
* `activation_date`: DateField — Nullable: sim (null=True, blank=True)
* `inactivation_date`: DateField — Nullable: sim (null=True, blank=True)
* `contract_start_date`: DateField — Nullable: sim (null=True, blank=True)
* `contract_end_date`: DateField — Nullable: sim (null=True, blank=True)
* `host`: ForeignKey(account.Host) — Nullable: não (blank=True apenas)
* `owners`: ManyToManyField(account.Owner) — Nullable: n/a (M2M, pode estar vazia, blank=True)
* `owner`: ForeignKey(account.Owner) — Nullable: não (blank=True apenas)
* `partner`: ForeignKey(account.Partner) — Nullable: sim (null=True, blank=True)
* `cover_image`: ForeignKey(FileItem) — Nullable: sim (null=True)
* `balance_discount_rate`: DecimalField(max_digits=50, decimal_places=2) — Nullable: sim (null=True, blank=True)
* `bank_details`: ForeignKey(financial.Bank_details) — Nullable: sim (null=True)
* `invoice_details`: ForeignKey(financial.Invoice_details) — Nullable: sim (null=True)
* `extra_day_preparation`: SmallIntegerField — Nullable: não (default=0)
* `is_to_keep_funds_in_seazone`: BooleanField — Nullable: não (default=False)
* `host_reservation_comission_fee`: FloatField — Nullable: sim (null=True)
* `host_cleaning_comission_fee`: FloatField — Nullable: sim (null=True)
* `churn`: BooleanField — Nullable: não (default=False)
* `churn_date`: DateField — Nullable: sim (null=True, blank=True)
* `stays_code`: CharField(max_length=255) — Nullable: sim (null=True, blank=True)
* `stays_listing_id`: CharField(max_length=255) — Nullable: sim (null=True, blank=True)
* `has_ownership_change_in_progress`: BooleanField — Nullable: Não (default=False)
* `is_cleaning_fee_embedded`: BooleanField  — Nullable: Não  (default=False)
* `has_insurance`: BooleanField — Nullable: Não  (default=False)
* `has_bill_management`: BooleanField —  Nullable: Não  (default=False)

### Invoice_details

* `id`: AutoField (implícito) — Nullable: não
* `invoice_entity_name`: CharField(max_length=255) — Nullable: não (blank=True apenas)
* `cpf`: CharField(max_length=11) — Nullable: não (blank=True apenas)
* `cnpj`: CharField(max_length=14) — Nullable: não (blank=True apenas)
* `email`: EmailField — Nullable: não (blank=True apenas)
* `phone_number`: CharField(max_length=32) — Nullable: no (blank=True apenas)
* `postal_code`: CharField(max_length=32) — Nullable: não (blank=True apenas)
* `address`: CharField(max_length=256) — Nullable: não (blank=True apenas)
* `address_number`: CharField(max_length=32) — Nullable: não (blank=True apenas)
* `complement`: CharField(max_length=256) — Nullable: não (blank=True apenas)
* `district`: CharField(max_length=64) — Nullable: não (blank=True apenas)
* `city`: CharField(max_length=64) — Nullable: não (blank=True apenas)
* `state`: CharField(max_length=32) — Nullable: não (blank=True apenas)
* `user`: ForeignKey('account.user') — Nullable: não (blank=True apenas; observe: null=True não está definido, logo BD não permite NULL a menos que haja default)