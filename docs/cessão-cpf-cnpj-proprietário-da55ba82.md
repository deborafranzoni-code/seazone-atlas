<!-- title: Cessão CPF -> CNPJ (Proprietário) | url: https://outline.seazone.com.br/doc/cessao-cpf-cnpj-proprietario-zGMIAy2Tqe | area: Tecnologia -->

# Cessão CPF -> CNPJ (Proprietário)

# O que é?

Atualmente, alguns proprietários estão optando por migrar as suas contas de pessoa física para pessoa jurídica. E esse ajuste gera suportes para o CS Proprietário, que consequentemente cai para nós ajustarmos as informações no banco de dados (e Wallet, consequentemente).\n

# Como resolver?

No banco de dados, busque pelo proprietário indicado no suporte e edite as seguintes informações na tabela `account_user`:

* Setar o campo `is_individual` como `false` 
* Adicionar os novos valores de `CNPJ`, `corporate_name` e `trading_name` para corresponder aos dados "jurídicos"