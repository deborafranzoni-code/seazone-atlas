<!-- title: Nota Fiscal - alterar dados | url: https://outline.seazone.com.br/doc/nota-fiscal-alterar-dados-ApDWl7kFSo | area: Tecnologia -->

# Nota Fiscal - alterar dados

Dados necessários:


1. `property_id` ou `owner_id`
2. Dados que compõem a Nota Fiscal (Nome, CPF ou CNPJ, email, `user_id`, endereço, número do endereço, cidade, complemento, bairro, número de telefone, CEP e estado)

O que fazer:

Todos os dados das notas Fiscais estão na `Financial Invoice Details`


Caso seja a nota fiscal da propriedade:

* Procure por `property_id` na tabela `property_property` e verifique qual o id do campo `invoice_details_id` 
* Com o dado do `invoice_details_id`  procure na `Financial Invoice Details`

  \
  * Se for para ==corrigir dados==, corrija os dados da NF na `Financial Invoice Details`.
  * Se for ==inserir== um novo registro:
    * primeiro Precisa Inserir um novo registro na  depois identificar qual é o novo `novo_ID` gerado. Em seguida atualizar na `Property_property` o campo `invoice_details_id `com esse `novo_ID`  gerado


\
Caso seja a nota fiscal do proprietário:

* Procure por `owner_id` na tabela `account_owner` e altere o dado necessário a partir do campo `default_invoice_details_id`

Se for necessário, crie um novo registro de nota fiscal na tabela `financial_invoice_details`

> 🚨 CUIDADO: Ao alterar dados da nota, tenha ciência de que isso pode afetar um ou mais propriedades/proprietários. Se for preciso manter os dados de um e alterar de outros, crie um novo registro.
>
> ⚠️ As notas fiscais sempre levam em consideração primeiros os dados anexados a propriedade. Os dados que estiverem vazios ou nulos serão buscados nos dados anexados ao proprietário, necessariamente nessa ordem.