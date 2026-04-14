<!-- title: Banco tools - GCP | url: https://outline.seazone.com.br/doc/banco-tools-gcp-vBFFqukdAf | area: Tecnologia -->

# Banco tools - GCP

# 📄 Relatório Técnico: Atualização de Versão de Banco de Dados (PostgreSQL)

**Data:** 18 de Fevereiro de 2026 **Ambiente:** Google Cloud Platform (Cloud SQL) **Banco de Dados Atual:** PostgreSQL 15 **Versão Alvo Analisada:** PostgreSQL 17 (Recomendada) vs PostgreSQL 18 **Aplicações Impactadas:**


1. **Outline** (Versão 0.87.1)
2. **Baserow** (Versão 2.0.6)


---

## 1. Resumo Executivo

O objetivo deste documento é validar a viabilidade técnica e os riscos associados à atualização do motor de banco de dados PostgreSQL da versão 15 para uma versão superior (17 ou 18).

**Recomendação Oficial:** Atualização para o **PostgreSQL 17**.

**Justificativa:**

* **Estabilidade:** A versão 17 (lançada em Set/2024) já possui mais de 1 ano de maturação e patches de correção, sendo considerada "LTS" de fato para produção.
* **Compatibilidade:** As aplicações Outline e Baserow, nas versões citadas, possuem bibliotecas (drivers) totalmente compatíveis com a versão 17.
* **Risco da Versão 18:** Embora o PostgreSQL 18 (lançado em Set/2025) ofereça melhorias de I/O, ele introduz mudanças restritivas de autenticação que podem exigir refatoração nas strings de conexão e configuração dos containers das aplicações, o que aumenta o tempo de *downtime* e risco de falha de conexão.


---

## 2. Análise de Compatibilidade das Aplicações

### 2.1. Outline (v0.87.1)

* **Stack Tecnológico:** Node.js, Sequelize ORM, driver `pg`.
* **Análise de Impacto:**
  * O Outline utiliza o ORM *Sequelize*, que abstrai a maioria das mudanças de sintaxe SQL entre versões.
  * **Ponto de Atenção:** O Outline faz uso intensivo de índices de busca textual. O PostgreSQL 17 otimizou a estrutura de índices B-Tree e BRIN. Isso deve resultar em *melhoria* de performance na busca de documentos.
  * **Veredito:** Compatível com PG 17 e 18.

### 2.2. Baserow (v2.0.6)

* **Stack Tecnológico:** Python, Django ORM.
* **Análise de Impacto:**
  * O Baserow opera criando tabelas dinamicamente para cada "database" criado pelo usuário.
  * **Dependência Crítica:** O Baserow depende fortemente de tipos de dados `JSONB`. O PostgreSQL 17 introduziu melhorias significativas na performance de consulta e atualização de `JSONB`, o que beneficiará diretamente a aplicação.
  * **Extensões:** O Baserow pode utilizar extensões como `pg_trgm` (trigramas). É necessário garantir que as extensões sejam atualizadas no GCP durante o processo.
  * **Veredito:** Altamente beneficiado pelo PG 17. Compatível com PG 18 (salvo configurações de Auth).


---

## 3. Matriz de Mudanças e Riscos (Breaking Changes)

### 3.1. Mudanças Críticas (PG 15 ➔ PG 17) - *Baixo Risco*

Ao migrar para a versão 17, as seguintes alterações devem ser observadas:


1. **Permissões do Schema** `**public**`**:**
   * *Mudança:* Desde o PG 15 (reforçado no 16/17), usuários sem privilégios explícitos não podem mais criar tabelas no schema `public` por padrão.
   * *Mitigação:* Se as aplicações conectam com um usuário que não é o dono do banco (`postgres`), será necessário rodar: `GRANT CREATE ON SCHEMA public TO [usuario_app];` (Geralmente o GCP mantém as permissões na migração, mas é vital validar).
2. **Parâmetros de Configuração Removidos:**
   * Parâmetros legados como `promote_trigger_file` foram removidos. Se houver configurações manuais (flags) customizadas no painel do GCP, verifique a compatibilidade.
3. **Formato de Expressões Regulares (Regex):**
4. O PG 17 atualizou a biblioteca de Regex. Em casos raros, filtros de busca muito complexos no Baserow podem se comportar de forma ligeiramente diferente se usarem sintaxe inválida que antes era tolerada.

### 3.2. Mudanças Críticas (PG 17 ➔ PG 18) - *Médio/Alto Risco*

Ao considerar a versão 18, os riscos operacionais aumentam:


1. **Depreciação/Remoção do Suporte MD5:**
   * *Impacto:* O PostgreSQL 18 força o uso de autenticação `SCRAM-SHA-256`.
   * *Problema:* Se as aplicações (Outline/Baserow) estiverem configuradas ou usando drivers antigos que tentam "handshake" via MD5, **a conexão será recusada**.
   * *Ação Necessária:* É obrigatório recriar as senhas dos usuários no banco antes ou imediatamente após o upgrade para garantir que o hash armazenado seja SCRAM.
2. **Caminho de Busca (Search Path):**
   * Mudanças na segurança de como funções (`SECURITY INVOKER`) resolvem nomes de tabelas podem quebrar *views* customizadas se houver SQL manual injetado no banco.


---

## 4. Plano de Ação (Checklist de Migração GCP)

Para garantir zero perda de dados e retorno rápido em caso de falha:


1. **Plano de atualizção**

   \
   * Fazer snapshot da instância atual
   * Checar extenções pre update
   * atualizar instância do GCP
   * Checar extenções pós update
   * Testar e validar funcionamento do baserow
   * Testar e validar funcionamento do oultine
   * Testar e validar funcionamento do n8n
2. **Plano de Rollback:**
   * O Cloud SQL não permite "downgrade" in-place. O rollback consiste em:
   * Excluir a instância atual (ou renomear).
   * Restaurar o Backup realizado no passo 3 em uma nova instância PG 15.
   * Reapontar os DNS/IPs das aplicações.


---

## 5. Conclusão

A atualização para o **PostgreSQL 17** é segura e trará benefícios de performance, especialmente para o Baserow (JSONB). A atualização para a versão 18 é desaconselhada neste momento sem uma validação prévia exaustiva dos drivers de conexão das aplicações devido às mudanças no protocolo de autenticação.