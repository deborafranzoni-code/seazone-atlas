<!-- title: O que preencher em cada campo? | url: https://outline.seazone.com.br/doc/o-que-preencher-em-cada-campo-6d5plVoeSc | area: Tecnologia -->

# O que preencher em cada campo?

# Documentação de Preenchimento - Formulários de Governança Tech


---

## Solicitações para o Vault

| Campo | Obrigatório | Descrição |
|----|----|----|
| **Código OIDC** | Sim | Acesse <https://vault.seazone.com.br/ui/>, faça login com OIDC usando sua conta Google, e copie o código que aparece ao clicar no ícone do seu perfil (canto superior direito). |
| **Vaults solicitados** | Sim | Selecione a quais grupos de senhas você deseja acesso. A solicitação deve condizer com sua função. |


---

## Solicitações para o Github

| Campo | Obrigatório | Descrição |
|----|----|----|
| **Usuário Github** | Sim | Informe seu username do Github (não o email). Exemplo: `joaosilva`. |


---

## Solicitações para o Sapron

| Campo | Obrigatório | Descrição |
|----|----|----|
| **Tipo de usuário** | Sim | Escolha o nível de permissão necessário para suas atividades. Opções: **Visualizador** (apenas leitura), **Editor** (leitura e edição), **Administrador** (acesso completo). |


---

## Solicitações para o Banco de Dados

| Campo | Obrigatório | Descrição |
|----|----|----|
| **Qual banco?** | Sim | Selecione o banco de dados ao qual a solicitação é direcionada. Opções: Sapron, Reservas. Esse tipo de solicitação será analisada com cuidado pela equipe. |
| **Ambiente** | Sim | Escolha o ambiente em que o banco de dados previamente selecionado está localizado. Opções: **Staging** (testes/homologação), **Production** (produção). |
| **Selecione a role** | Sim | Escolha a role do seu cargo. Para ajustes pontuais de privilégios, mantenha a atual. Opções: DBA, Quality Assurance, Tech Lead (supervisor), Frontend, Backend, Infra (SRE, Devops). |
| **Usuário do banco** | Sim | Informe o nome de usuário a ser criado, utilizando o formato adequado. Exemplos de entradas válidas: `nomesobrenome`, `nome_sobrenome`. |
| **Privilégios desejados** | Não | Descreva privilégios específicos caso precise de algo além do padrão da role selecionada. |


---

## Solicitações de tipo Outros

Utilizado quando o sistema/ferramenta selecionado não possui formulário específico (AWS, ASAAS, Baserow, Google, Metabase, N8N, Pipefy, Stays, Tuna, VPN, Outros).

| Campo | Obrigatório | Descrição |
|----|----|----|
| **Sistema/Ferramenta** | Sim | Selecione o sistema ao qual a solicitação se refere. |
| **O que precisa fazer?** | Sim | Tipo de ação solicitada. Opções: Criar conta, Remover conta, Alterar permissões, Recuperar senha, Recuperar 2FA, Outros. |
| **Para quem é a solicitação?** | Sim | Indique se a solicitação é para você mesmo ou para outra pessoa. |
| **Email/Username do usuário afetado** | Condicional | Obrigatório se a solicitação for para outra pessoa. Informe o email ou username do usuário que será afetado. |
| **Justificativa** | Sim | Explique o motivo da solicitação (mínimo 20 caracteres). |


---

## Campos Comuns (Formulário Inicial)

Estes campos são preenchidos antes de qualquer formulário específico:

| Campo | Obrigatório | Descrição |
|----|----|----|
| **Email do solicitante** | Sim | Seu email corporativo @seazone.com.br. |
| **Time** | Sim | Selecione o time ao qual você pertence. |
| **Tipo de Solicitação** | Sim | Escolha entre: Solicitar Acesso, Reportar Problema, Tirar Dúvida. |