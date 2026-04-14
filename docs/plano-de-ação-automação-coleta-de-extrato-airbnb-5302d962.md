<!-- title: [Plano de Ação] - Automação coleta de extrato Airbnb | url: https://outline.seazone.com.br/doc/plano-de-acao-automacao-coleta-de-extrato-airbnb-Hrl41QK2pc | area: Tecnologia -->

# [Plano de Ação] - Automação coleta de extrato Airbnb

## 1. Visão Geral

Este documento detalha a estratégia técnica para automatizar o download de relatórios financeiros do Airbnb e sua integração com o fluxo de conciliação da Sapron API.

**Objetivo:** Substituir o processo manual de download de CSVs pela execução programática via API interna do Airbnb, utilizando scripts Python parametrizados e orquestrados pelo n8n.

## 2. Arquitetura do Fluxo

O fluxo seguirá a seguinte sequência:


1. **Orquestrador (n8n):** Gatilho agendado (Cron).
2. **Extrator (Python):** Execução do script
   * Uso de `AAT_COOKIE` (via ENV) para bypass de autenticação.
   * Cálculo dinâmico de datas (padrão: últimos 5 dias).
3. **Tratamento de Erros:**
   * Se **Sucesso (JSON):** Segue para integração.
   * Se **Erro de Auth:** Notificação via Slack para renovação manual do cookie.
4. **Ingestão (Sapron API):**
   * `POST /files` -> Obtém URL assinada do S3 Seazone.
   * `PUT` (Upload) -> Envio do arquivo para o S3.
   * `PUT /reservations/conciliate_reservations` -> Inicia conciliação síncrona.


---

## 3. Roadmap de Implementação (Tasks)

### **Task 1: Infraestrutura e Segurança**

- [ ] **1.1 Configuração de ENVs:** Definir `AIRBNB_API_KEY`, `AIRBNB_USER_ID`, `USER_AGENT`, `AAT_COOKIE`, etc.
- [ ] **1.2 Secret Management:** Armazenar chaves sensíveis (n8n Credentials).
- [ ] **1.3 Environment Setup:** Garantir ambiente Python com biblioteca `requests` disponível no runner do n8n.

### **Task 2: Desenvolvimento do Webhook/Pipeline (n8n)**

- [ ] **2.1 Nó de Execução:** Integrar script Python ao n8n via nó *Execute Command*.
- [ ] **2.2 Parser de Saída:** Configurar n8n para ler o `stdout` JSON do script.
- [ ] **2.3 Sistema de Alertas:** Criar rota de fallback para erros de autenticação (Cookie expirado).

### **Task 3: Integração com Backend (Sapron API)**

- [ ] **3.1 Fluxo de Upload:** Implementar a sequência necessária para o sistema de arquivos da Seazone (POST /files + S3 + PUT /conciliate).
- [ ] **3.2 Validação de Dados:** Testar a integridade do CSV baixado em relação ao esperado pela API de conciliação.


---

## 4. Definições Técnicas (Estratégia de autenticação)

* **Decisão:** Semi-automática com sessão persistente de cookie:
  * **Fluxo:**

    → Acessar página de login 

    → Entrar com e-mail e senha (Vault) 

    → Validação 2F (Obter o código com a Nathalia Beltramello) 

    → Obter cookie da sessão (Devtools > Applications > Cookies > airbnb.com.br > Filtrar por "_aat")

    → Atualizar env COOKIE_AAT com o valor do cookie obtido no passo anterior

    → \*NOTA: Após expiração do cookie esse fluxo de autenticação deve ser repetido

    \
* **Justificativa:** O Airbnb não suporta TOTP universal (2FA via SMS, Ligação ou e-mail é a regra para a conta). Automatizar a leitura de e-mail aumentaria a complexidade e a fragilidade do sistema. A manutenção periódica de cookies (que podem durar dias/semanas) é o melhor custo-benefício atual. Inclusive há outros scrapers no repositório [Pipe-Scrapers](https://github.com/seazone-tech/Pipe-scrapers/blob/Pipe-scrapers/internal/update_seazone_ids.py) que funcionam dessa forma.