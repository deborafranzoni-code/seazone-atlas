<!-- title: Manual de Uso e Onboarding | url: https://outline.seazone.com.br/doc/manual-de-uso-e-onboarding-I0jKoWQVVi | area: Tecnologia -->

# Manual de Uso e Onboarding

> Guia completo para quem vai usar o **Cofre Seazone** (Passbolt) pela primeira vez. Leitura de \~10 minutos. Ao final, você vai saber instalar, acessar, criar e compartilhar senhas com segurança.


---

## O que é o Passbolt?

O Passbolt é o **cofre de senhas da Seazone**. Ele guarda todas as credenciais do time de forma segura, com **criptografia ponta-a-ponta**, isso significa que nem o servidor consegue ler suas senhas. Só você e as pessoas com quem você compartilha.

Pense nele como um cofre físico, mas digital: cada pessoa tem sua própria chave (GPG), e só com ela consegue abrir os compartimentos que lhe pertencem.

```mermaidjs
flowchart LR
    A["🔑 Sua chave\nprivada (local)"] --> B["🔒 Encripta\nno seu browser"]
    B --> C["☁️ Servidor\narmazena ciphertext"]
    C --> D["🔓 Decripta\nno browser do colega"]
    D --> E["🔑 Chave privada\ndo colega (local)"]

    style A fill:#3b82f6,color:#fff,stroke:none
    style B fill:#1e293b,color:#e2e8f0,stroke:#475569
    style C fill:#475569,color:#e2e8f0,stroke:#64748b
    style D fill:#1e293b,color:#e2e8f0,stroke:#475569
    style E fill:#22c55e,color:#fff,stroke:none
```

> **O servidor nunca vê suas senhas.** Toda a criptografia acontece dentro do seu navegador.

|    |    |
|----|----|
| **Acesso** | [cofre.seazone.com.br](https://cofre.seazone.com.br) |
| **Funciona em** | Chrome, Brave, Edge, Firefox |
| **Obrigatório** | Extensão do Passbolt instalada |


---

## 1. Instalando a Extensão

A extensão é o coração do Passbolt, sem ela, nada funciona. Ela gerencia sua chave de criptografia e faz o login automático.

**Escolha seu navegador:**

| Navegador | Link |
|----|----|
| Chrome / Brave / Edge | [Chrome Web Store](https://chromewebstore.google.com/detail/passbolt/didegimhafipceonhjepacocaffmoppf) |
| Firefox | [Add-ons Firefox](https://addons.mozilla.org/pt-BR/firefox/addon/passbolt/) |

Depois de instalar, o ícone de uma **chave vermelha** aparece na barra do navegador.

>  ![](/api/attachments.redirect?id=a326733e-5936-499b-b697-6a1e80190d91 " =499x230")

> **Dica:** Instale a extensão **antes** de clicar no link de convite. Se fizer ao contrário, vai ver uma tela de erro.


---

## 2. Primeiro Acesso — Setup da Conta

Você vai receber um **email de convite** vindo de `cofre-no-reply@seazone.com.br`. O setup é feito uma única vez e leva cerca de 2 minutos.

>  ![](/api/attachments.redirect?id=07e00ea6-37a2-4284-b6d2-30704ed74795 " =1095x705")

```mermaidjs
flowchart TD
    A(["📧 Recebeu o email\nde convite"]) --> B["Clique no link\ndo email"]
    B --> C["A extensão abre\no wizard de setup"]
    C --> D["Defina sua\npassphrase"]
    D --> E["Baixe o\nRecovery Kit"]
    E --> F["Escolha cor + frase\nde segurança"]
    F --> G(["✅ Pronto!"])

    style A fill:#1e40af,color:#fff,stroke:none
    style G fill:#166534,color:#fff,stroke:none
```

### Passo a passo


1. **Abra o email** de convite e clique no botão de setup
2. A extensão detecta o link e abre um **wizard** (assistente)
3. **Defina sua passphrase** — essa é sua senha mestra. Escolha algo longo e memorável (veja dicas abaixo)
4. **Baixe o Recovery Kit** — é um arquivo `.asc` que salva sua chave privada. **==Guarde em local seguro!==**
5. **Escolha uma cor e frase** de segurança — isso aparece toda vez que você faz login, pra garantir que o site é o verdadeiro Passbolt e não um phishing

> 
> [Screencast from 2026-03-18 13-53-30.webm 1909x1006](/api/attachments.redirect?id=a3c3220c-e6e6-480f-a783-ea60a81a9850)

> \

### Como escolher uma boa passphrase

| Ruim | Bom |
|----|----|
| `Senha123!` | `meu gato preto dorme no teclado` |
| `P@ssw0rd` | `cafe expresso com 3 acucares sempre` |
| `qwerty2026` | `a janela do escritorio tem 4 plantas` |

Frases longas e pessoais são mais seguras **e** mais fáceis de lembrar que senhas curtas com caracteres especiais.

### Sobre o Recovery Kit

O Recovery Kit é como a **chave reserva do seu cofre**. Sem ele + passphrase, não existe recuperação.

| Cenário | Resultado |
|----|----|
| Tem Recovery Kit + lembra passphrase | Recupera acesso em qualquer navegador |
| Tem Recovery Kit + esqueceu passphrase | Conta precisa ser recriada (senhas pessoais perdidas) |
| Não tem Recovery Kit + lembra passphrase | Pode exportar um novo pela extensão atual |
| Não tem nenhum dos dois | Conta precisa ser recriada do zero |

> **Onde guardar:** pen drive pessoal, pasta segura no computador, contas drive pessoal. Nunca compartilhe com ninguém.


---

## 3. Login no Dia a Dia

Depois do setup, fazer login é rápido:


1. Acesse [cofre.seazone.com.br](https://cofre.seazone.com.br)
2. A extensão mostra o campo de **passphrase**
3. Confira se a **cor e frase de segurança** são as que você definiu
4. Digite sua passphrase e clique em **Login**

>  ![Definição de Passphrase](/api/attachments.redirect?id=0a4485c9-41c3-4e13-a048-775fc17ea529 " =1548x727")

>  ![Download do arquivo de recuperação](/api/attachments.redirect?id=6239ca73-ced7-4257-8258-0562b5704c6f " =1548x727") ![Definição de cor e caracteres](/api/attachments.redirect?id=c88249e2-1c79-4320-b884-1da8abd449b3 " =1548x727")**Por que verificar a cor e frase?** Se alguém criar um site falso imitando o Passbolt, ele não vai saber qual cor e frase você escolheu. Isso te protege contra phishing.


---

## 4. Criando uma Senha

```mermaidjs
flowchart LR
    A["Clique no\nbotão +"] --> B["Preencha\nos campos"]
    B --> C["Clique em\nSalvar"]
    C --> D["A extensão encripta\ne envia pro servidor"]

    style A fill:#3b82f6,color:#fff,stroke:none
    style D fill:#166534,color:#fff,stroke:none
```


1. No painel, clique no botão **"+"** (canto superior direito)
2. Preencha:
   * **Nome** — algo descritivo (ex: "AWS Console — Produção")
   * **URL** — endereço do site
   * **Usuário** — seu login naquele serviço
   * **Senha** — clique no **ícone de dado** para gerar uma senha forte automaticamente
   * **Descrição** — opcional, para anotações
3. Clique em **Salvar**

>  ![](/api/attachments.redirect?id=787bb871-6107-4a32-895c-d1b1cace139c " =1665x930")

### Ações rápidas

| Ação | Como |
|----|----|
| **Copiar senha** | Clique no ícone de copiar ao lado da senha |
| **Copiar usuário** | Clique no ícone de copiar ao lado do username |
| **Editar** | Clique na senha → botão Editar |
| **Deletar** | Clique na senha → menu ⋮ → Deletar |

> **Dica:** A extensão também sugere salvar senhas automaticamente quando você faz login em sites. Um popup aparece perguntando se quer salvar no cofre.


---

## 5. Compartilhando com Colegas

Compartilhar é simples e seguro — o Passbolt re-encripta a senha com a chave do colega antes de enviar.

```mermaidjs
sequenceDiagram
    actor V as Você
    participant P as Passbolt
    actor C as Colega

    V->>P: Compartilhar "AWS Console"
    P-->>V: Chave pública do colega
    Note over V: Re-encripta com a chave do colega
    V->>P: Envia ciphertext
    P-->>C: Notificação por email
    C->>P: Abre o cofre
    Note over C: Decripta com sua chave privada
```

### Passo a passo


1. Clique na senha que quer compartilhar
2. Clique no botão **"Compartilhar"**
3. Digite o nome ou email do colega
4. Escolha a **permissão**:

| Permissão | O que pode fazer |
|----|----|
| **Pode ler** | Ver e copiar a senha |
| **Pode editar** | Tudo acima + alterar a senha |
| **É dono** | Tudo acima + compartilhar e deletar |


5. Clique em **Salvar**

O colega recebe uma notificação por email e a senha aparece no cofre dele na próxima vez que acessar.

>  ![](/api/attachments.redirect?id=7ea7eeb3-9886-4ac8-b2aa-b099ad893014 " =1203x717")


---

## 6. Organizando com Pastas

Pastas ajudam a manter o cofre organizado, especialmente quando o número de senhas cresce.


1. No menu lateral, clique com botão direito → **"Nova Pasta"**
2. Dê um nome descritivo (ex: "Infra AWS", "Ferramentas Time")
3. Arraste senhas para dentro da pasta

> 
> [Screencast from 2026-03-18 13-49-02.webm 1897x878](/api/attachments.redirect?id=4fff3713-5236-43b3-b0f8-9c29cdbcad11)

> \

> **Pastas compartilhadas:** você pode compartilhar uma pasta inteira com um colega ou grupo. Todas as senhas dentro dela herdam a permissão.


---

## 7. Usando em Outro Computador ou Navegador

Se você trocou de máquina, formatou o computador, ou quer acessar de outro navegador, vai precisar **reconfigurar a extensão**. Isso é normal — sua chave GPG fica salva **apenas** no navegador onde você fez o setup.

```mermaidjs
flowchart TD
    A(["Preciso acessar\nde outro lugar"]) --> B["Instale a extensão\nno novo navegador"]
    B --> C["Acesse cofre.seazone.com.br"]
    C --> D["Clique em\nRecuperar Conta"]
    D --> E["Digite seu email"]
    E --> F["Abra o email\ncom o link"]
    F --> G["Faça upload do\nRecovery Kit + passphrase"]
    G --> H(["✅ Acesso\nrestaurado"])

    style A fill:#1e293b,color:#e2e8f0,stroke:#475569
    style H fill:#166534,color:#fff,stroke:none
```

> 🎬 **\[Inserir vídeo\]** Gravação mostrando o processo de recuperação em um navegador novo (\~1 min).

### Dica: Contas compartilhadas (ex: governancatech)

Se você precisa acessar mais de uma conta Passbolt no mesmo computador (ex: sua conta pessoal + conta admin), use **perfis separados no navegador**:


1. No Chrome/Brave: clique no ícone de perfil → **"Adicionar"**
2. Configure a extensão Passbolt em cada perfil com a respectiva conta
3. Alterne entre os perfis sem precisar refazer recovery

```mermaidjs
flowchart LR
    subgraph perfil1["Perfil: Pessoal"]
        A["Extensão com\nsua conta"]
    end
    subgraph perfil2["Perfil: Admin"]
        B["Extensão com\nconta admin"]
    end
    
    perfil1 -.->|"Trocar perfil\nno navegador"| perfil2

    style perfil1 fill:#1e40af22,stroke:#3b82f6
    style perfil2 fill:#16653422,stroke:#22c55e
```

> 
> [Perfis em navegadores permitem Passbolt com contas diferentes logadas 1919x969](/api/attachments.redirect?id=a7b35e1f-1c0e-4d56-8d91-f7eb878072db)

> \


---

## 8. Dicas de Segurança

| Faça | Não faça |
|----|----|
| Use uma passphrase longa e memorável | Reutilizar a mesma senha de outros serviços |
| Guarde o Recovery Kit em local seguro | Enviar o Recovery Kit por email ou chat |
| Verifique a cor/frase anti-phishing no login | Ignorar o indicador visual de segurança |
| Use o gerador de senhas do Passbolt | Inventar senhas "de cabeça" |
| Compartilhe senhas pelo Passbolt | Mandar senhas por Slack, email ou WhatsApp |


---

## 9. Perguntas Frequentes

**"Cliquei no link de convite mas aparece erro"** → A extensão precisa estar instalada **antes** de clicar no link. Instale primeiro, depois clique novamente.

**"Esqueci minha passphrase"** → Não existe recuperação de passphrase. Contate o admin para recriar sua conta. Senhas pessoais (não compartilhadas) serão perdidas.

**"Troquei de computador e não consigo entrar"** → Instale a extensão no novo navegador, acesse [cofre.seazone.com.br](https://cofre.seazone.com.br), clique em "Recuperar conta" e use seu Recovery Kit + passphrase.

**"O site pede pra verificar email toda vez que entro"** → Você está sem a extensão configurada nesse navegador. Veja a seção 7 (Usando em Outro Computador).

**"Posso acessar pelo celular?"** → Não no momento. O Passbolt CE funciona apenas via extensão de navegador desktop.

**"Uma senha compartilhada comigo sumiu"** → O dono pode ter removido o compartilhamento ou deletado a senha. Entre em contato com quem compartilhou.

**"Preciso de ajuda urgente"** → Procure o time de SRE no Slack ou abra um chamado em [seazone.atlassian.net](https://seazone.atlassian.net).


---

## Resumo Visual — Sua Jornada no Passbolt

```mermaidjs
flowchart TD
    A(["📧 Recebe convite\npor email"]) --> B["Instala a extensão\nno navegador"]
    B --> C["Completa o setup\n(passphrase + Recovery Kit)"]
    C --> D(["✅ Acesso ao cofre"])
    D --> E["Cria e organiza\nsuas senhas"]
    D --> F["Compartilha\ncom colegas"]
    D --> G["Acessa senhas\ncompartilhadas"]

    style A fill:#1e40af,color:#fff,stroke:none
    style D fill:#166534,color:#fff,stroke:none
    style E fill:#1e293b,color:#e2e8f0,stroke:#475569
    style F fill:#1e293b,color:#e2e8f0,stroke:#475569
    style G fill:#1e293b,color:#e2e8f0,stroke:#475569
```