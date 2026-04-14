<!-- title: Validações  campos Pipedrive - Onboarding | url: https://outline.seazone.com.br/doc/validacoes-campos-pipedrive-onboarding-axpS9a5OE2 | area: Tecnologia -->

# Validações  campos Pipedrive - Onboarding

# Regras de validação de campos Pipedrive

## 1. Dados do Proprietário

### 1.1. Endereço do Proprietário

Estes campos são utilizados para criar o registro de endereço vinculado ao proprietário.

**Campos no Pipedrive:**

* **País** (Máx 70 caracteres)
* **Bairro** (Máx 255 caracteres)
* **CEP** (Máx 10 caracteres)
* **Logradouro** (Máx 255 caracteres)
* **Número** (Máx 255 caracteres)
* **Complemento** (Máx 255 caracteres)
* **Cidade** (Máx 255 caracteres)
* **Estado** (Máx 255 caracteres)

#### **Validações possíveis mapeadas:**



1. **Bairro**

* O campo não aceita caracteres especiais (exceto hífens) e não aceita *underscores* (`_`).

2\. **País**

* O campo não aceita números ou *underscores*.


### 1.2. Dados do Usuário (Proprietário)

**Campos no Pipedrive**

* **Nome** (Máx 255 caracteres)
* **Sobrenome**: (Máx 255 caracteres)
* **Email**
* **Telefone** (Máx 255 caracteres)
* **CPF**
* **CNPJ**
* **Data de Nascimento**

#### **Validações possíveis mapeadas:**



1. **Data de Nascimento**

* O usuário deve ter idade entre 12 e 123 anos.


2. **Documentos (CPF)**

* Exatamente 11 dígitos numéricos.


3. **Documentos (CNPJ)**

* Exatamente 14 dígitos numéricos.

\n4. Telefone

* Deve conter ao menos 10 dígitos numéricos


---

### 1.3. Dados do Owner (Proprietário)

**Campos no Pipedrive**

* **Profissão** (Máx 255 caracteres)
* **Nacionalidade** (Máx 255 caracteres)


#### **Validações possíveis mapeadas:**


1. **Profissão**

* Não permite números. Apenas letras, hífens ou espaços.


---

## 2. Taxas e Comissões

Estes campos afetam diretamente o contrato financeiro e comissões da propriedade.

**Campos no Pipedrive**

* **Taxa de Adesão**: Deal -> Taxa de Adesão -> Taxa de Adesão
* **Forma de Pagamento Parcelas**: Deal -> Taxa de Adesão -> Forma de pagamento das parcelas
* **Qtd. Parcelas**: Deal -> Taxa de Adesão -> Quantidade de parcelas do valor restante
* **Taxa de Desconto**: Deal -> Taxa de Adesão -> Taxa de abatimento nas reservas
* **Valor da entrada**: Deal -> Taxa de Adesão -> Valor da entrada
* **Forma de pagamento da entrada**: Deal -> Taxa de Adesão ->  Forma de pagamento da entrada
* **Comissão de Parceiro**: Deal -> Vendas SZS -> Valor da comissão (parceiros)
* **Período comissão Parceiro**: Deal -> Vendas SZS -> Comissão Vitalícia?


#### **Validações possíveis mapeadas:**



1. **Consistência de Pagamento (Entrada vs Parcelas)**

* **Regra de Negócio**: É necessário informar valor de entrada OU número de parcelas.
* Se `Valor da entrada` == `Taxa de Adesão`, parcelas não são permitidas.
* `Valor da entrada` não deve ser maior que `Taxa de Adesão`
* Caso `Valor da entrada` seja menor que `Taxa de Adesão` é OBRIGATÓRIA a inclusão de `Quantidade de parcelas do valor restante` e `Forma de pagamento das parcelas`

\n2. **Consistência de método de pagamento (Entrada e Parcelas)**

* Se houver `Quantidade de parcelas do valor restante`, `Forma de pagamento das parcelas` é obrigatória.
* Se NÃO houver `Quantidade de parcelas do valor restante`, `Forma de pagamento das parcelas` NÃO deve ser informada.
* Se houver `Valor da entrada`, `Forma de pagamento da entrada` é obrigatória.
* Se NÃO houver `Valor da entrada`, `Forma de pagamento da entrada` NÃO deve ser informado.

\n3. **Taxa de Desconto (**`Taxa de abatimento nas reservas`**)**

* Só permitida se `Forma de pagamento das parcelas` === "Abatimento - retirar".
* Se `Forma de pagamento das parcelas` === "Abatimento - retirar" é obrigatório informar `Taxa de abatimento nas reservas`.
* Deve estar entre 0 e 100%.

  \


4. **Comissão de Parceiro**

* Se for `Indicação de Parceiro`, deve-se informar Recorrência e Valor da comissão.
* Caso valor seja um pagamento à vista (e.g., `R$ 500,00 à vista`), período deve ser nulo, ou `Não se aplica`.
* Caso valor seja um pagamento recorrente (e.g., `2% recorrente`), período deve ser informado, e diferente de `Não se aplica`.

## 3. Dados da Propriedade

### 3.1. Endereço da Propriedade

**Campos no Pipedrive**

* **Bairro** (Máx 255 caracteres)
* **CEP** (Máx 10 caracteres)
* **Logradouro** (Máx 255 caracteres)
* **Número** (Máx 255 caracteres)
* **Complemento** (Máx 255 caracteres)
* **Cidade** (Máx 255 caracteres)
* **Estado** (Máx 255 caracteres)
* **Nome do Condomínio** (Máx 255 caracteres)

#### **Validações possíveis mapeadas:**


1. **Bairro**

* O campo não aceita caracteres especiais (exceto hífens) e não aceita *underscores* (`_`).

2\. **País**

* O campo não aceita números ou *underscores*.