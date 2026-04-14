<!-- title: Post-Mortem - Alteração de dados indevidos | url: https://outline.seazone.com.br/doc/post-mortem-alteracao-de-dados-indevidos-eOcx56dGIV | area: Tecnologia -->

# Post-Mortem - Alteração de dados indevidos

Projeto/Sistema: Sapron\nData do Evento: 06/03/2025\nAutor(es): Natália Bessa, Isabel Karina, Roberto Campos, Ederson de Maria, Lucas Malagoli, Renata Domingues\nData do Relatório: 19/03/2025\n


1. **Visão Geral Descrição do Incidente:**\n\nNo dia 06 de março foi solicitado [um suporte](https://app.pipefy.com/open-cards/1089875722) relatando que havia uma conta bancária não identificada pelo proprietário Flávio Antônio Vendramin (fvendram6@yahoo.com.br).\n\nA partir disso, iniciamos uma investigação e identificamos 43 registros de dados bancários de proprietário, bem como suas notas ficais, dados pessoais (email, endereço, cpf, cnpj - 21 linhas de alteração na account_user_audit) foram alterados indevidamente. Estes registros foram alterados pelo usuário [administrativo@seazone.com.br](mailto:administrativo@seazone.com.br), via front backoffice (Sapron).\n\nAlém disso, o time de CS de proprietários relatou que recebeu uma solicitação da secretária do proprietário Ciro Gabolla pedindo a alteração de email de acesso ao Sapron, pois ela não estava conseguindo acessar a conta do proprietário. Após a alteração de login e senha,  [foi identificado](https://seazone-fund.slack.com/archives/C02H5GM0VB5/p1741268223022349) que houve alterações não reconhecidas nos dados bancários do proprietário. Estas alterações foram feitas via front de proprietário (Sapron).

### **Impacto:**

* 43 registros alterados na financial_bank_details_audit, via backoffice; 
* 21 registros alterados na account_user_audit, via backoffice;
* 1 alteração de dado bancário de proprietário, via front de proprietário.

### **Gravidade:** 

**Altíssima**\nPor estar relacionado a dados sensíveis que impactam no pagamento e repasse de proprietários este incidente é categorizado como gravíssimo.


---


2. **Linha do Tempo do Incidente**

| Data  | Evento |
|----|----|
| 28/02/2025 - 23:00 BRT | Alterações nas tabelas financial_bank_details, Account_adress, Account_user, Financial_invoice_details |
| 06/03/2025 - 10:37 BRT | Abertura de suporte reportando alteração indevida nos dados bancários |
| 06/03/2025 - 11:30 BRT | Abertura de War Room para encaminhar as primeiras medidas e inativação do usuário administrativo@seazone.com.br |
| 06/03/2025 | Criação de co-host, através da conta da Madego (host_id 95) com email  administrativoo@seazone.com.br |
| 06/03/2025 - 11:30 BRT | Comunicação ao times envolvidos - Financeiro, CS do Proprietário |
| 07/03/2025 -  10:30 BRT | Abertura de War Room para dar continuidade as correções das alterações indevidas |
| 10/03/2025   | Remoção das permissões de edições de dados bancários no front de proprietário na wallet e sapron |
| 12/03/2025 | Vinculação do email de acesso do usuário com a indentity do posthog |
| 13/03/2025 | Remoção das permissões de edições de dados pessoais, bancários e nota fiscal no backoffice |
| 13/03/2025 | Remoção das permissões de edições de dados bancários anfitrião |
| 14/03/2025 | Inativação dos usuários que possuíam domínio genérico de email e usuários inativos no slack |

   
---
3. **Causa Raiz** 

### **Análise da causa raiz:**

* Fragilidade de permissão concedida a uma conta genérica em editar os dados sensíveis;
* Falha de segurança do produto ao permitir a edição de dados sensíveis sem dupla confirmação do usuário; 
* Falha de processo no atendimento ao proprietário, sem a confirmação da autenticidade do solicitante da alteração;

### **Ferramentas e métodos utilizados na investigação:**

* Consultas nas tabelas financial_bank_details_audit, Account_adress_audit, Account_user_audit, Financial_invoice_details_audit, verificando qual o usuário havia realizado as alterações;
* Visualização do histórico de acessos no Posthog;
* Constatação das alterações feitas pelo front no Grafana;
* Confirmação dos dados de proprietários pelo time de atendimento CS de proprietários.


---


4. **Resolução e Medidas Tomadas** 

### Ações durante o incidente:

Para solução imediata durante o incidente foi realizado a inativação das contas `adminitrativo@seazone.com.br` e `administrativoo@seazone.com.br`, bem como a inativação das permissões de edição de dados pessoais e bancários de proprietário, anfitrião e backoffice.

### Solução implementada:

* Inativar por meio de feature flag a edição de dados bancários de proprietário na Wallet e Sapron; 
* Inativar por meio de feature flag a edição de dados bancários de anfitrião no Sapron;
* Inativar por meio de feature flag e edição de dados bancários por seazoners pelo backoffice no Sapron.


---


5. **Ações Preventivas** 

### Mudanças necessárias, prazos e responsáveis:

* WALLET - Implementar a autenticação por e-mail para edição de dados bancário na Wallet - 31/03/2025 - @[Natália Bessa Ribeiro](mention://b7cf8b04-7ae9-46ad-9090-0a072f14a4b3/user/81cf90ab-0590-4de7-9558-8678a963bde2) 
* BANCO - Criar coluna de client na financial_bank_details_audit para identificar por onde a mudança foi realizada, podendo ser Sapron, Wallet ou API - 31/03/2015 - @[Roberto Campos](mention://9441aa8a-2df0-41eb-b100-347254dd2303/user/7a820dce-f3c4-4cd0-9054-82f4b4d27bf7) 
* POSTHOG - Criar alerta de mudança de dado sensível em dashboard no posthog - 31/03/2025 - @[Natália Bessa Ribeiro](mention://b6cd5104-37f5-465d-90c6-8eed9911a6c3/user/81cf90ab-0590-4de7-9558-8678a963bde2) 
* SAPRON  - Implementar autenticação por e-mail para edição de dados bancários, dados de notas fiscais e notas fiscais no backoffice  - prazo a definir - @[Ederson de Maria Melo](mention://2cf7a006-e583-47c1-a866-9d75c71f6f70/user/71fcd337-b0bd-4973-83dc-4e9793ff55f5) @[Renata Domingues](mention://f752db36-cdb1-4c53-99b3-6ac5d6469e7f/user/83caf9a1-d063-4e25-9f03-c26abd05694e) @[Renata Domingues](mention://3765fa44-b4b8-42d6-bcf3-cc324671716b/user/83caf9a1-d063-4e25-9f03-c26abd05694e)  
* SAPRON - Implementar autenticação por e-mail para edição de dados bancários no Sapron do Anfitrião - prazo a definir - @[Natália Bessa Ribeiro](mention://14f8c98a-23d7-40cc-96ae-7d0faa9bdbb1/user/81cf90ab-0590-4de7-9558-8678a963bde2) 

### **Lições Aprendidas** 

* Nenhum usuário Seazoner deve conseguir acessar o Sapron ou solicitar um login utilizando usuário genérico. Todos devem ter contas pessoais com seus emails corporativo.
* Reforçar a segurança de dados e inputs.\nNecessário verificar a autenticidade do solicitante de alteração de dados tanto no produto como no atendimento.
* Devemos conseguir monitorar as tarefas com logs mais detalhados que nos forneçam dados da origem dos problemas.

### O que funcionou bem:

* Proatividade de investigação de PM responsável pelo backoffice e Coordenadora de QA 
* Comunicação rápida com stakeholders afetados 

### O que pode ser melhorado:

* Aumentar níveis de segurança para alteração de dados sensíveis.
* Registrar de forma clara qual o client resposável por realizar a mudança.
* Melhorar o processo de identificação de solicitação de alteração de dados sensíveis no suporte ao proprietário.



7. **Revisores**


\