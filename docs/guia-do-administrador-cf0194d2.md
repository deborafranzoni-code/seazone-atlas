<!-- title: Guia do Administrador | url: https://outline.seazone.com.br/doc/guia-do-administrador-rAr5gaigRG | area: Tecnologia -->

# Guia do Administrador

> Guia prático para quem administra o Cofre Seazone (Passbolt). Cobre as operações do dia a dia, emergências e boas práticas de segurança.


---

## Suas Responsabilidades como Admin

Como admin do Passbolt, você é responsável por:

* **Convidar e remover usuários** — controlar quem tem acesso ao cofre
* **Gerenciar grupos e pastas** — manter a estrutura organizada (ver doc de Nomenclatura e Governança)
* **Responder incidentes** — ajudar quem perdeu acesso, investigar atividades suspeitas
* **Auditar periodicamente** — garantir que as permissões estão corretas

```mermaidjs
flowchart LR
    subgraph rotina["Dia a dia"]
        A["Convidar\nusuários"]
        B["Gerenciar\ngrupos"]
        C["Responder\ndúvidas"]
    end
    subgraph periodico["Trimestral"]
        D["Auditoria de\npermissões"]
        E["Revisar\nusuários inativos"]
    end
    subgraph emergencia["Emergência"]
        F["Revogar\nacessos"]
        G["Recuperar\ncontas"]
    end

    style rotina fill:#1e40af22,stroke:#3b82f6
    style periodico fill:#16653422,stroke:#22c55e
    style emergencia fill:#7f1d1d22,stroke:#ef4444
```


---

## Operações do Dia a Dia

### **Usuário loga sozinho**

Ver @[Manual de Uso e Onboarding](mention://812cfd0b-ec1f-4741-b590-be23bb3736fb/document/abbdeee5-35c7-4bec-982d-8a5163bc8001)  

Tudo que você administrado precisará fazer é adicionar ele no grupo da equipe.

### Convidar um novo usuário


1. No menu lateral, vá em **Usuários**
2. Clique no botão **"+"**
3. Preencha: nome, sobrenome, email (`@seazone.com.br`)
4. Escolha o role: **User** (padrão) ou **Admin**
5. Clique em **Salvar**
6. O convite é enviado automaticamente por email

>  ![](/api/attachments.redirect?id=89757b1c-3373-4ac5-9357-c9d64cedb0d6 " =1042x644")

**Depois do convite:**

* Adicione o usuário ao **grupo** do time dele
* Avise o usuário para instalar a extensão **antes** de clicar no link
* O link de convite expira em **24h** — se expirar, use "Reenviar convite"

### Reenviar convite

Se o link expirou ou o usuário não recebeu o email:


1. Vá em **Usuários** → selecione o usuário
2. Clique no menu **⋮** → **Reenviar convite**


> ==somente usuários @seazone conseguiram completar o login==

### Criar um grupo


1. Vá em **Usuários → Grupos**
2. Clique em **"+"** para criar
3. Nome em **minúsculo** (ex: `sre`, `reservas-backend`)
4. Adicione os membros
5. Defina pelo menos um **Group Manager** (pode gerenciar membros)

>  ![](/api/attachments.redirect?id=45ea0e5d-c7ad-40bf-b4e1-b4a27ad1c7c9 " =1042x644")

### Compartilhar uma pasta com um grupo


1. Clique com botão direito na pasta → **Compartilhar**
2. Digite o nome do grupo
3. Permissão: **pode editar** (para o time) ou **é dono** (para `admin`)
4. Salvar

> **Lembrete:** O grupo `admin` deve ser **dono** de toda pasta criada. **==Sempre.==**


---

## Gerenciando Acessos

### Quando alguém sai do time

```mermaidjs
flowchart TD
    A(["Membro saiu\ndo time"]) --> B{"Saiu da\nempresa?"}
    B -- Não --> C["Remover do grupo\ndo time antigo"]
    C --> D["Adicionar ao grupo\ndo novo time"]
    B -- Sim --> E["Desabilitar\no usuário"]
    E --> F["Senhas pessoais\nremovidas"]
    E --> G["Senhas compartilhadas\npermanecem para outros"]

    style A fill:#1e293b,color:#e2e8f0,stroke:#475569
    style E fill:#7f1d1d,color:#fff,stroke:none
    style D fill:#166534,color:#fff,stroke:none
```

**Mudou de time:**


1. Remova do grupo antigo
2. Adicione ao grupo novo
3. As senhas compartilhadas do time antigo deixam de aparecer automaticamente

**Saiu da empresa:**


1. Vá em **Usuários** → selecione → **Desabilitar** (ou **Deletar**)
2. Antes de deletar, verifique se o usuário é **dono** de senhas compartilhadas — transfira a ownership primeiro
3. Senhas pessoais (não compartilhadas) são **perdidas permanentemente**

### Quando alguém perde o acesso

O fluxo mais comum: a pessoa trocou de computador ou navegador e não consegue entrar.

**Se ela tem Recovery Kit + passphrase:** → Oriente a acessar `cofre.seazone.com.br` → "Recuperar conta" → upload do kit

**Se ela perdeu tudo (sem kit, sem passphrase):** → Deletar e recriar o usuário. Senhas pessoais serão perdidas. Senhas compartilhadas continuam com os outros membros e podem ser re-compartilhadas.


---

## Monitoramento

### Dashboards no Grafana

Temos auditoria de criações de senhas, ações e deleções via dashboard na pasta **Passbolt** no Grafana:

Acesse com sua conta Google: <https://monitoring.seazone.com.br/d/passbolt-audit/passbolt-e28094-auditoria?orgId=1&from=now-7d&to=now&timezone=browser&var-usuario=Todos&refresh=15m>



| Dashboard | O que mostra | Quando consultar |
|----|----|----|
| **Auditoria** | Quem fez o quê, quando | Investigação de incidentes, auditoria trimestral |

> \