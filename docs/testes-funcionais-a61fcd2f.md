<!-- title: Testes Funcionais | url: https://outline.seazone.com.br/doc/testes-funcionais-TeyI9s7qEJ | area: Tecnologia -->

# 🧪 Testes Funcionais

# Guia de Teste: Fluxo de Token Expirado

Este documento descreve o passo a passo para simular um ambiente onde o token de autenticação do pré-checkin (`pre_checkin_token`) está expirado.

O objetivo é testar o tratamento de erro da aplicação, como a exibição do toast de "Sessão Expirada" e o redirecionamento para o login.

## 📋 Pré-requisitos


1. Acesso à aplicação do reservas rodando localmente (ex: `http://localhost:3000`) ou em staging.
2. Credenciais de teste válidas (código de reserva, data inicial e final).
3. Acesso ao arquivo `.env` do projeto `sapron_backend` para obter o `SECRET_KEY`.

## ⚙️ Passo a Passo

Siga estas etapas para gerar um token expirado e substituí-lo no seu navegador.

### Parte 1: Obter o Token de Autenticação


1. Acesse a página de pré-checkin da aplicação (ex: `/v2/pre-checkin`).
2. Faça o login usando um código de reserva, data inicial e data final válidas.
3. Após o login, abra as **Ferramentas de Desenvolvedor** (DevTools) no seu navegador (clique direito > Inspecionar ou `F12`).
4. Vá para a aba **Application** (no Chrome/Edge) ou **Armazenamento** (no Firefox).
5. No menu à esquerda, navegue até **Cookies** e selecione o domínio da sua aplicação (ex: `http://localhost:3000`).
6. Encontre o cookie chamado `pre_checkin_token`.
7. **Copie o valor completo** deste cookie. Ele será um token JWT longo, parecido com isto:

   ```
   eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwi...
   ```

### Parte 2: Modificar o Token para Expirar

Para facilitar o processo de invalidar o token, criei uma aplicação que permite alterar o payload e re-assinar o JWT de maneira simples.


1. Acesse o editor de JWT: **<https://jwt-modifier.vercel.app/>**
2. No campo **Token JWT Atual**, cole o `pre_checkin_token` que você copiou na etapa anterior.
3. No campo **Segredo de Assinatura (Secret)**, insira o valor da variável `SECRET_KEY` que está no arquivo `.env` do `sapron_backend`.

   > **⚠️ Aviso:** Nunca insira segredos de produção em ferramentas online. Use esta aplicação apenas com segredos de desenvolvimento/teste.
4. No campo **Nova Expiração**, defina o valor como `0` (zero). Isso fará com que o token seja considerado expirado imediatamente.
5. Clique em **"Gerar Novo Token"** e copie o novo token JWT gerado na área de resultado.

### Parte 3: Substituir o Token no Navegador


1. Volte para o DevTools no seu navegador (na mesma aba **Application** > **Cookies**).
2. Encontre o `pre_checkin_token` novamente.
3. Dê um clique duplo no **valor** do cookie.
4. **Apague o valor antigo e cole o novo token (expirado)** que você acabou de gerar.
5. Pressione `Enter` para salvar a alteração.

## ✅ Resultado Esperado

Pronto! O cookie de autenticação no seu navegador agora está oficialmente expirado.

Para testar, tente realizar qualquer ação que exija autenticação (como navegar para a página `/v2/pre-checkin/formulario` ou tentar enviar o formulário). A aplicação deve:


1. Identificar o token como inválido/expirado.
2. Exibir o toast de erro (ex: "Sessão expirada...").
3. Redirecionar o usuário de volta para a tela de login (`/v2/pre-checkin`).


\