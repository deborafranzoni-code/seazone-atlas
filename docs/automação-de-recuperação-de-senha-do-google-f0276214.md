<!-- title: Automação de Recuperação de Senha do Google | url: https://outline.seazone.com.br/doc/automacao-de-recuperacao-de-senha-do-google-bmgYFoRUbn | area: Tecnologia -->

# Automação de Recuperação de Senha do Google

# 📄 **Documentação Técnica da Automação: Recuperar Senha do Google**

## ✅ **Visão Geral**

Esta automação tem como objetivo realizar o **reset automático de senhas de usuários no Google Workspace**, acionada indiretamente por um fluxo no **Slack**.


---

## ✅ **1. Funcionamento Geral**

* O verdadeiro **gatilho** ocorre no **Slack**, onde o usuário realiza uma solicitação via comando ou formulário.
* Esse fluxo no Slack insere uma nova **linha em uma Google Sheet** específica.
* O **n8n** monitora essa planilha a cada **1 minuto** utilizando o **Google Sheets Trigger**.
* Quando uma nova linha é detectada, a automação executa as seguintes etapas automaticamente.


---

## ✅ **2. Fluxo Detalhado**

### 🔹 **1. Google Sheets Trigger**

Monitora a planilha `RESET_SENHA_GOOGLE` (Google Sheets).

* **Evento:** `rowAdded`
* **Intervalo:** a cada **1 minuto**
* Quando detecta uma nova linha, dispara o fluxo.


---

### 🔹 **2. Definir Variáveis**

* Extrai e organiza variáveis importantes vindas da planilha, como:
  * `mail_target`: email que será resetado.
  * `solicitante_slack_user`, `solicitante_slack_mail`, `solicitante_slack_id`: informações do solicitante via Slack.
  * `row_id`: identificador da linha.


---

### 🔹 **3. Criar Card no Jira**

* Cria automaticamente um **ticket** no **Jira** com as informações da solicitação.
* Define:
  * Projeto: Governança.
  * Tipo de Issue: Reset de Senha.
  * Labels: Automação, Google.


---

### 🔹 **4. Verifica se o E-mail Existe**

* Consulta via **Google Workspace Admin** se o e-mail de destino (`mail_target`) existe.
* Garante que o reset de senha só será feito em contas válidas.


---

### 🔹 **5. Gera uma Nova Senha**

* Gera uma senha **aleatória segura** de **16 caracteres**.
* Usa um **Code Node** configurado com execução `runOnceForEachItem`.


---

### 🔹 **6. Altera a Senha no Google**

* Atualiza a senha do usuário no **Google Workspace Admin**.
* Define que o usuário **deve alterar a senha no próximo login**.


---

### 🔹 **7. Gera Bloco de Mensagem para Slack**

* Monta dinamicamente o **bloco de mensagem** (`blocksUi`) em formato Slack.
* Inclui:
  * Saudação personalizada.
  * Email resetado.
  * Número do ticket.
  * Nova senha provisória.
  * Instruções de próximos passos.
  * Botões de ação (Finalizar suporte / Preciso de ajuda).


---

### 🔹 **8. Envia Mensagem ao Solicitante no Slack**

* Usa **Slack Node** com `messageType: block`.
* Envia a mensagem gerada para o **solicitante** usando o `solicitante_slack_id`.
* Inclui o `blocksUi` montado.


---

### 🔹 **9. Atualiza Status no Jira**

* Atualiza o **status do ticket** no Jira para "EM_VALIDAÇÃO".
* Adiciona labels e responsável.


---

### 🔹 **10. Adiciona Comentário no Card do Jira**

* Adiciona um **comentário automático** no ticket, informando:
  * Reset realizado via automação.
  * Aguardando confirmação do usuário no Slack.
  * Informações do solicitante, email resetado, ticket e data.


---

### 🔹 **11. Atualiza Planilha com o ID do Card**

* Atualiza a **Google Sheet** com o ID do ticket Jira criado (`jira_card_id`).
* Garante rastreabilidade total entre Planilha, Jira e Slack.


---

### 🔹 **12. Atualiza Status na Planilha**

* Atualiza o status da linha na planilha para **"EM_VALIDAÇÃO"**.
* Indica que o processo de reset foi realizado e aguarda validação do usuário.


---

## ✅ **3. Tecnologias e Serviços Utilizados**

| Tecnologia | Finalidade |
|----|----|
| **Slack** | Envio de mensagens ao solicitante com informações e botões interativos. |
| **Google Sheets** | Armazenamento e monitoramento das solicitações. |
| **Google Workspace Admin** | Reset e atualização de senhas de contas corporativas. |
| **Jira** | Criação, atualização e rastreabilidade de tickets. |
| **n8n** | Orquestração completa do fluxo, automação e integração entre sistemas. |


---

## ✅ **4. Características Especiais da Automação**

✅ Modular, totalmente sem intervenção humana após inserção na planilha. ✅ Segura: gera senha aleatória e obriga troca no próximo login. ✅ Auditável: registra todas as etapas no Jira e Google Sheets. ✅ Notifica automaticamente o solicitante no Slack. ✅ Totalmente escalável: pode processar múltiplas solicitações sequenciais.


---

## ✅ **5. Fluxo Visual (Resumo)**

```plaintext

Slack -> Insere linha na Google Sheet
   ↓
Google Sheets Trigger (n8n)
   ↓
[Define Variáveis]
   ↓
[Criar Card no Jira]
   ↓
[Verifica E-mail] -> [Gera Senha] -> [Altera Senha]
   ↓
[Gerar blocksUi]
   ↓
[Enviar Slack]
   ↓
↙         ↘
[Jira Atualiza]  [Atualiza Planilha]
```


---

## ✅ **6. Pontos de Atenção**

* A automação depende da estrutura da planilha estar **intacta**.
* Campos como `row_id` e `solicitante_slack_id` são essenciais.
* O Slack deve ter permissão para enviar mensagens ao usuário solicitante.
* A autenticação correta deve estar configurada para:
  * Google Sheets
  * Google Workspace Admin
  * Jira
  * Slack


---

## ✅ **7. Benefícios**

✅ Redução de tempo para reset de senhas. ✅ Menor carga para equipe de suporte. ✅ Transparência total para o usuário solicitante. ✅ Rastreabilidade em múltiplos sistemas.


---

## ✅ **8. Última atualização**

* Data: **21/05/2025**
* Versão do n8n: **1.90.2 (Self Hosted)**