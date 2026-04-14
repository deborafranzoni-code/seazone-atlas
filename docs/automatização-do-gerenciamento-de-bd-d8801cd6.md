<!-- title: Automatização do gerenciamento de BD | url: https://outline.seazone.com.br/doc/automatizacao-do-gerenciamento-de-bd-t5SDhY0bIu | area: Tecnologia -->

# Automatização do gerenciamento de BD

# Automação de Gerenciamento do Banco de Dados

## Visão Geral

Este documento descreve o fluxo de automação para gerenciamento de usuários e permissões no banco de dados. O sistema automatiza a criação, remoção e concessão de permissões para usuários em ambientes de *staging* e *production*.

## Arquitetura do Sistema

O sistema é composto por três camadas principais:


1. **Workflow**: Ponto de entrada para acionar a automação.
2. **Action**: Orquestrador que gerencia autenticação e execução.
3. **Scripts**: Implementações específicas para cada operação.

## Fluxo de Execução

```mermaidjs

graph TD
    A[Webhook/N8N] --> B[db-automation.yaml]
    B --> C[mgmt-database Action]
    C --> D{Qual ação?}
    D -->|create| E[user_create.sh]
    D -->|grant| F[user_grant.sh]
    D -->|remove| G[user_remove.sh]
    E --> H[Banco de Dados]
    F --> H
    G --> H
    H --> I[Coleta Resultado]
    I --> J[Aciona N8N]
    J --> K[Slack Notification]
    J --> L[Atualiza Jira]
    J --> M[Registra Histórico]
```

## Componentes do Sistema

### 1. **Workflow (db-automation.yaml)**

* **Responsabilidade**: Ponto de entrada do sistema de automação.
* **Funcionalidades**:
  * Recebe solicitações via webhook ou N8N.
  * Chama a *action* de gerenciamento de banco de dados.
  * Passa parâmetros necessários (ex: ação, usuário, ambiente, banco).

  **Exemplos de Parâmetros**:

  ```yaml
  # Criar usuário
  action: "create"
  username: "usuario_teste"
  environment: "staging"
  database: "reservas_db"
  
  # Conceder permissões
  action: "grant"
  username: "usuario_existente"
  environment: "production"
  database: "sapron_db"
  
  # Remover usuário
  action: "remove"
  username: "usuario_antigo"
  environment: "staging"
  database: "governanca_db"
  ```

### 2. **Action (mgmt-database/action.yaml)**

* **Responsabilidade**: Orquestrador central do sistema.
* **Funcionalidades**:
  * Recebe parâmetros do workflow.
  * Realiza autenticação na AWS e EKS.
  * Determina e executa o script correspondente à ação solicitada.
  * Aciona o fluxo N8N com o resultado da operação.

  **Motivação para Uso de GitHub Actions e EKS**: O RDS está em uma rede privada na AWS, acessível apenas pelas instâncias do cluster EKS. Por isso, o uso do GitHub Actions com conexão ao EKS é necessário para garantir acesso seguro.

  **Processo**:

  
  1. Valida parâmetros.
  2. Configura credenciais AWS.
  3. Conecta ao cluster EKS.
  4. Identifica script a ser executado.
  5. Executa script com parâmetros apropriados.
  6. Coleta resultado da operação.
  7. Aciona fluxo N8N para continuidade do processo.

### 3. **Scripts de Execução**

#### user_create.sh

* **Responsabilidade**: Criação de usuários no banco de dados.
* **Funcionalidades**:
  * Cria novo usuário no ambiente especificado.
  * Configura credenciais iniciais.
  * Aplica políticas de segurança padrão.

#### user_grant.sh

* **Responsabilidade**: Concessão de permissões.
* **Funcionalidades**:
  * Concede permissões específicas a usuários existentes.
  * Gerencia níveis de acesso (read, write, admin).
  * Aplica permissões por banco de dados.

#### user_remove.sh

* **Responsabilidade**: Remoção de usuários.
* **Funcionalidades**:
  * Remove usuário do banco de dados.
  * Revoga permissões associadas.
  * Limpa credenciais e acessos.

## Ambientes Suportados

* **Staging**: Ambiente de desenvolvimento e testes.
* **Production**: Ambiente de produção.

## Configuração da Infraestrutura

### Cluster EKS

* **Nome do Cluster**: `general-cluster`
* **Região**: `sa-east-1`
* **ARN**: `arn:aws:eks:sa-east-1:711387131913:cluster/general-cluster`

### Namespaces

* **Staging**: `stg-apps`
* **Production**: `prd-apps`

### Instâncias RDS

#### Staging

* **RDS Principal**: `stg-postgres.cbwcm8my4qns.sa-east-1.rds.amazonaws.com`
* **Estrutura**: Instância com múltiplos bancos (wallet, reservas, sapron).

#### Production

* **RDS Reservas**: `reservas-prd-postgres.cbwcm8my4qns.sa-east-1.rds.amazonaws.com`
* **Outros RDS**: Sapron e Wallet (instâncias separadas).

### Usuário de Automação

* **Usuário**: `automacao`
* **Responsabilidade**: Executar queries e operações nos bancos.
* **Nota**: Este usuário deve ser criado em todos os bancos com permissões necessárias.

### Exemplo de Comando de Conexão

```bash

kubectl -n stg-apps run temp-psql-$RANDOM --rm -i --restart=Never \
  --image=postgres:16-alpine \
  --env="PGPASSWORD=SUA_SENHA_AQUI" \
  -- psql -h bastion-staging.stg-apps.svc.cluster.local \
     -p 5432 -U automacao -d postgres -c "SELECT 1;"
```

## Fluxo Detalhado

### 1. **Iniciação**

* Sistema externo (webhook ou N8N) envia solicitação.
* Workflow `db-automation.yaml` é acionado e valida parâmetros, passando-os para a *action*.

### 2. **Processamento**

* A *action* `mgmt-database` recebe parâmetros e realiza autenticação AWS/EKS.
* O script apropriado é identificado e executado.

### 3. **Execução**

* O script executa a operação no banco de dados.
* O resultado é retornado para o sistema solicitante.

### 4. **Finalização**

* Logs são gerados para auditoria.
* Status da operação é reportado.
* Fluxo N8N é acionado para continuar o processo.
* Sistema se prepara para próxima solicitação.

### 5. **Integração com N8N**

Após a execução do script, o fluxo N8N é acionado com o resultado da operação (sucesso, falha, erro). O N8N é responsável por:

* Enviar notificações no Slack.
* Atualizar status no Jira.
* Gerenciar continuidade do fluxo de suporte.
* Registrar histórico completo da operação.

## Vantagens do Sistema

* **Automação Completa**: Elimina intervenção manual.
* **Segurança**: Autenticação centralizada e controlada.
* **Auditoria**: Logs detalhados de todas as operações.
* **Flexibilidade**: Suporte a múltiplos ambientes.
* **Confiabilidade**: Processo padronizado e testado.

## Configuração de Secrets

### Secrets Obrigatórias

* `**GH_TOKEN**`: Token do GitHub para autenticação.
* `**AWS_ACCOUNT_ID**`: ID da conta AWS.
* `**AWS_ACCOUNT_REGION**`: Região AWS.
* `**AWS_ACCOUNT_ROLE**`: Role IAM para acesso ao EKS.
* `**DB_USER_AUTOMATION**`: Usuário de automação do banco.
* `**DB_PASSWORD_AUTOMATION**`: Senha do usuário de automação.

### Secrets Opcionais

* `**N8N_TOKEN**`: Token para acionar fluxos no N8N (recomendado).

## Considerações de Segurança

* Todas as operações são autenticadas via AWS.
* Acesso controlado por roles IAM.
* Logs detalhados de auditoria.
* Validação de parâmetros antes da execução.
* Isolamento por ambiente (staging/production).
* Credenciais de banco armazenadas como secrets do GitHub.

## Extensibilidade do Sistema

O sistema é extensível, permitindo adicionar novas *actions* e scripts conforme a necessidade da Central de Serviços de Suporte de TI. Exemplos de novas funcionalidades:

### Possíveis Novas Funcionalidades


1. **Backup e Restore de Dados**
   * Backup automático de tabelas específicas.
   * Restauração e validação de integridade dos backups.
2. **Monitoramento de Performance**
   * Análise de queries lentas.
   * Alertas de performance.
3. **Gerenciamento de Schemas**
   * Criação e modificação de tabelas.
   * Migrações de schema.
4. **Auditoria e Compliance**
   * Relatórios de acesso e permissões.
   * Verificação de conformidade com políticas.
5. **Manutenção Preventiva**
   * Limpeza de logs antigos.
   * Otimização de índices.
6. **Gestão de Conectividade**
   * Teste de conectividade com bancos.
   * Monitoramento de latência.

Essas funcionalidades podem ser adicionadas com o mesmo padrão arquitetural: workflow → action → script.