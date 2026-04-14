<!-- title: Acessos - Sistemas Retool | url: https://outline.seazone.com.br/doc/acessos-sistemas-retool-Aydofb1ODO | area: Tecnologia -->

# Acessos - Sistemas Retool

## SpotSys

Sistema criado no Retool para gerenciar os dados da **SZI** (Unidade, Empreendimento, Contrato e outros). Para conceder acesso a este sistema, o Seazoner deve ter conta Sapron criada e ativa, pois o acesso é o mesmo.

Importante verificar duas coisas nos registros do Seazoner: a primeira coisa, `main_role = Seazone` na tabela `account_user`; a segunda coisa é verificar na tabela `account_seazone`, o campo `department = Administrative`.

Com isso, o acesso já deve funcionar, o Seazone acessa a ferramenta com seu email e senha (a mesma do Sapron Backoffice).

Se não houver conta criada, uma nova conta deve ser criada no Djando Produção, com as mesmas configurações acima.