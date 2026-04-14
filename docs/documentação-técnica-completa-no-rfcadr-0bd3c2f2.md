<!-- title: Documentação técnica completa no RFC/ADR | url: https://outline.seazone.com.br/doc/documentacao-tecnica-completa-no-rfcadr-fQNzxO61n6 | area: Tecnologia -->

# Documentação técnica completa no RFC/ADR

Implementar controle seguro de edição de dados sensíveis por área de atuação


## **Objetivo**

\nResolver os erros de permissão enfrentados por usuários de diferentes áreas (Suporte Operacional, CS Proprietários, OTA etc.) ao editar dados em formulários, eliminando a dependência da allow list manual (por e-mail no código).


**Proposta de solução**\nImplementar um **mecanismo de autorização baseado em papéis/perfis (RBAC)** ou **grupos de atuação** (ex: operador_franchise, cs_owner, ota_agent), validado no backend, e que respeite as permissões específicas de cada área sobre os campos sensíveis.

**Escopos que devem ter controle de permissão sensível:**

* Apps
* Rotas do fechamento
* Anfitrião
* Imóvel
* Descrição


**Critérios de Aceite**


1. O sistema deve permitir edição de dados conforme a **área de atuação** do usuário.
2. Nenhum dado sensível poderá ser alterado sem validação da autorização no backend.
3. O mecanismo de autorização **não deve depender de e-mails hardcoded**.
4. A solução deve **integrar com o sistema de autenticação existente**.
5. Logs de tentativa de edição devem ser registrados para auditoria.


## Implementação Técnica



1. Modelagem de Permissões (RBAC ou ABAC) Defina roles como franchise_operator, cs_owner, ota_editor, etc. Associe essas roles com escopos/formulários e permissões específicas (ex: editar descricao de imovel). // Exemplo de definição de permissões { "role": "cs_owner", "permissions": { "imovel": \["view", "edit"\], "descricao": \["view", "edit"\] } }

   \
2. Integração com Login

No login, recupere e armazene o role do usuário (JWT ou session). Inclua os escopos de permissão no token (ex: roles, areas_atuacao). 


3\. Middleware de Autorização

Crie um middleware backend que, antes de qualquer edição, valide se o role tem permissão para editar aquele campo. def authorize_edit(user, area, field): if user.role in allowed_roles\[area\]\[field\]: return True raise PermissionDenied



4. Fallback Seguro + Logs

Toda tentativa de edição deve passar pela validação. Logue as tentativas negadas com usuário, área, campo e payload. 5. Admin UI (opcional) Criar uma tela para administradores mapearem roles × permissões de forma dinâmica, evitando hardcoded.


## Benefícios da abordagem


* Escalável e segura
* Menor dependência do time técnico para adicionar permissões
* Integra com autenticação existente
* Mais transparência e rastreabilidade (com logs)


## **Documento Técnico (RFC/ADR)**


**Título:** RFC - Controle seguro e escalável de edição de dados sensíveis por área de atuação\n**Data:** 22/05/2025\n**Status:** Em andamento\n**Autores:** Ederson Melo\n**Revisores:** Time Engenharia Backoffice


### Contexto

Desde 29/04, múltiplos usuários de áreas distintas (Suporte Operacional, CS Proprietários, OTA) perderam a capacidade de editar campos de formulários nas interfaces da plataforma. O motivo: a remoção das **feature flags de autorização baseadas em e-mails individuais**. Isso tornou o sistema dependente de uma lógica não escalável, gerando gargalos operacionais e alto risco de falha.


---

### Problema

* Sistema de edição atualmente depende de uma allow list estática por e-mail.
* Isso não escala e exige deploy para mudanças de permissão.
* Usuários de áreas legítimas estão impedidos de realizar alterações básicas.
* Dados sensíveis precisam de controle rigoroso, sem abrir mão da autonomia das áreas.


---

### Solução Proposta

**Implementar controle de acesso baseado em papéis (RBAC)** e validação centralizada no backend.


---

#### Etapas da Solução:


1. **Mapeamento de áreas × permissões**
   * Exemplo de papéis: franchise_operator, cs_owner, ota_editor
   * Exemplo de permissões:
     * imovel.descricao: editável por cs_owner
     * apps.config: editável por ota_editor
2. **Integração com autenticação**
   * Os tokens de login (JWT ou sessão) passam a incluir os papéis/áreas atribuídos ao usuário.
   * Exemplo:

     ```javascript
     json
     ```

     CopiarEditar

     ```javascript
     {
       "user": "ana.souza@empresa.com",
       "roles": ["cs_owner"],
       "areas_atuacao": ["imovel", "descricao"]
     }
     
     ```
3. **Middleware de autorização**
   * Backend intercepta qualquer tentativa de edição e valida se o papel do usuário tem permissão sobre o campo.
   * Exemplo:

     ```javascript
     python
     ```

     CopiarEditar

     ```javascript
     def authorize_edit(user, entidade, campo):
         if user.role in ACL[entidade][campo]:
             return True
         raise PermissionDenied
     
     ```
4. **Fallback seguro + Logs**
   * Toda tentativa de edição negada será registrada com: user, endpoint, payload e razão da negação.
   * Isso viabiliza auditoria e ajustes finos.
5. **Painel de administração (futuro)**
   * Permitir que líderes ou administradores atualizem os mapeamentos papel × permissão via interface segura, sem depender de deploys.


---

### Benefícios

* Elimina o hardcoding de permissões por e-mail.
* Permite delegar responsabilidade às áreas com segurança.
* Solução escalável, audível e de fácil manutenção.
* Alinha-se às boas práticas de segurança (principle of least privilege).


---

### Critérios de Aceite Técnicos

*  Middleware funcional validando permissões por papel.
*  Inclusão de papéis no token de autenticação.
*  Tentativas de edição indevidas devidamente bloqueadas e logadas.
*  Permissões organizadas por área e escopo.
*  Cobertura de testes para cenários de permissão e negação.