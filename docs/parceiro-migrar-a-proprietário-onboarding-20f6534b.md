<!-- title: Parceiro migrar a Proprietário (Onboarding) | url: https://outline.seazone.com.br/doc/parceiro-migrar-a-proprietario-onboarding-5ZOFlTNb22 | area: Tecnologia -->

# Parceiro migrar a Proprietário (Onboarding)

No fluxo de Onboarding, existem alguns casos onde:

* Temos parceiros que tem imóveis e vão virar proprietários, porem o `email` e `personid` já estão sendo usados e o parceiro tem registro nas tabelas: 
* `Account Partner`


* `Account User`


O Sapron ainda não lida com esse contexto, assim é necessário "liberar" o `email` e `personid` e seguir os seguintes passos operacionais:



1. Encontrar o userID na `Account User` do parceiro
2. Encontrar o ID na `Account Partner` associado a `Account User` do parceiro
3. Alterar os campos na Tabela `Account User` do parceiro:

   
   1. Email: de `emaildoparceiro@gmail.com`  para >>  `szn_suport_emaildoparceiro@gmail.com`
   2. Personid: de `123456789` para >> `suport123456789`
4. Comunicar a pessoa que abriu suporte que o o `email` e `personid` foi liberado
5. Quando o novo registro do propietario estiver gerado, encontrar o novo `userID` do proprietário 
6. Atualizar o registro do passo 2, na Tabela `Account Partner` a coluna `user_id` com o novo dado (userID) do passo 5 
7. Comunicar que a nova conta do proprietário foi vinculado a sua conta de parceiro e encerrar o suporte

   \