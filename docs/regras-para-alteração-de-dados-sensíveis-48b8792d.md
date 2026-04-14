<!-- title: Regras para Alteração de Dados Sensíveis | url: https://outline.seazone.com.br/doc/regras-para-alteracao-de-dados-sensiveis-KuO1ecqcDM | area: Tecnologia -->

# Regras para Alteração de Dados Sensíveis

Devido a falha de segurança dos dados ocorrida em 28/02, torna-se necessária a implementação de um plano de ação para mitigar os riscos e evitar novas vulnerabilidades na alteração de dados sensíveis. Abaixo, seguem as etapas com a respectiva classificação de risco e urgência para execução.

## Desabilitar a edição de dados bancários 

:rotating_light: Risco: Grave | ⚠️ Urgência: Imediata 

✅ Status: ==Implementado em 10/03==

* **Ação:** Remover todas as funcionalidades que permitam a alteração, adição ou vinculação de imóveis a contas bancárias. 

## Implementar autenticação por e-mail para edição de dados bancários 

:rotating_light: Risco: Alto | ⚠️ Urgência: Importante 

:white_check_mark: Status: ==Não iniciado==

* **Ação:** Exigir verificação por código enviado ao e-mail cadastrado para: Edição de conta bancária com imóveis vinculados. Vinculação de um imóvel a uma nova conta bancária. Requisito: Criar modal de confirmação de código antes de permitir a alteração. 

## Coluna de client na financial bank details audit 

**🚨** Risco: Alto | ⚠️ Urgência: Importante \n**✅** Status: ==Não iniciado==

* **Ação:** Incluir coluna de cliente na tabela responsável por armazenamento de alterações financeiras no qual deve ser possível identificar por onde a mudança foi realizada, podendo ser sapron, wallet ou API 

## Canal de Registo de Mudança de Dados Sensíveis 

:rotating_light: Risco: Alto | ⚠️ Urgência: Importante 

**✅** Status: ==Não iniciado==

* Ação: Criar canal de alerta de mudança de dados sensíveis, dessa forma registrando todas as alterações realizadas **(avaliar a necessidade de canal, pode ser substituído por dashboard no posthog).**

## Implementar autenticação para primeiro acesso e alteração de e-mail 

:rotating_light: Risco: Medio | ⚠️ Urgência: Importante 

:white_check_mark: Status: ==Não iniciado==

* **Ação:** No primeiro login ou após alteração de e-mail, exigir validação via código enviado por SMS antes de permitir o acesso. 

## Restringir a troca de senha 

:rotating_light: Risco: Baixo | ⚠️ Urgência: Moderada 

:white_check_mark: Status: ==Não iniciado==

* **Ação:** Implementar regra para que a recuperação de senha possa ser realizada apenas uma vez a cada 24 horas.