<!-- title: Franquia - Troca/Migração de cohost | url: https://outline.seazone.com.br/doc/franquia-trocamigracao-de-cohost-bezH00tUOy | area: Tecnologia -->

# Franquia - Troca/Migração de cohost

Caso - um cohost migra de HostID


O CoHost tem registros na **Account User** e na `Account Host Profile`

Identificar o `Account_user>ID` do cohost 

Identificar o `HostID` *antigo* ao que esta relacionado o Cohost na `Account Host Profile`


Exemplo O CoHost de UserID `Account User ID 151722` pertence ao `HostID 145` e vai migrar para o novo `HostID 78`


O que fazer:

Na tabela `Account Host Profile`  localizar o  `Account_user>ID` do cohost e atualizar o `HostID` 

 (No exemplo acima seria mudar de 145 para 78)