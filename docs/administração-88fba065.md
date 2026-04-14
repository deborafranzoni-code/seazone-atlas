<!-- title: Administração | url: https://outline.seazone.com.br/doc/administracao-2dbwbAjMsm | area: Tecnologia -->

# Administração

## Ciclo de Vida de um Usuário

```mermaidjs
flowchart TD
    A(["Admin convida\npelo painel"]) --> B["Email enviado via SES\ncofre-no-reply@seazone.com.br"]
    B --> C["Usuário instala extensão\ne completa setup"]
    C --> D(["✅ Ativo"])
    D --> E{"Saiu da empresa?"}
    E -- Sim --> F["Admin desabilita\nou deleta"]
    F --> G["Senhas pessoais removidas\nSenhas compartilhadas\npermanecem para outros"]
    G --> H(["🔒 Acesso revogado"])
    E -- Não --> D

    style A fill:#1e293b,color:#e2e8f0,stroke:#475569
    style D fill:#166534,color:#fff,stroke:#22c55e
    style H fill:#7f1d1d,color:#fff,stroke:#ef4444
    style E fill:#1e293b,color:#e2e8f0,stroke:#475569
```


---

## Convidar Novo Usuário

Somente admins podem convidar novos usuários.


1. No menu lateral, vá em **"Usuários"**
2. Clique em **"+"** para criar novo usuário
3. Preencha: primeiro nome, sobrenome, email (`@seazone.com.br`)
4. Selecione o role: **User** (padrão) ou **Admin**
5. Clique em **"Salvar"**
6. O convite é enviado automaticamente por email


---

## Configurar Self Registration (Restrição de Domínio)

Para garantir que apenas emails `@seazone.com.br` possam se registrar:


1. Vá em **Administração > Self Registration**
2. Ative a funcionalidade
3. Adicione `seazone.com.br` como domínio permitido
4. Salve


---

## Revogar Acesso de um Usuário


1. Em **"Usuários"**, selecione o usuário
2. Clique em **"Desabilitar"** ou **"Deletar"**
3. Senhas compartilhadas com esse usuário serão automaticamente re-criptografadas sem a chave dele


---

## Criar Admin via CLI

Em caso de emergência (sem acesso ao painel):

```bash
kubectl exec -n passbolt deploy/passbolt -- \
  su -s /bin/bash -c "bin/cake passbolt register_user \
    -u email@seazone.com.br \
    -f Nome -l Sobrenome -r admin" www-data
```