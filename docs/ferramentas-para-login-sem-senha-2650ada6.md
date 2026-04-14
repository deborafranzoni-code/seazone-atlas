<!-- title: Ferramentas para login sem senha | url: https://outline.seazone.com.br/doc/ferramentas-para-login-sem-senha-nq7j1bp3Tk | area: Tecnologia -->

# 🔒 Ferramentas para login sem senha

> **Relacionado a tarefa**: <https://seazone.atlassian.net/browse/SZRDEV-1072>

# :dart: Objetivo

Investigar alternativas e ferramentas para a implementação do login sem senha no website de reservas,  avaliando métodos de envio de códigos únicos via e-mail ou SMS.

# 🔀 Alternativas

Possíveis ferramentas ou serviços para implementar:

## Gerar o código por conta própria

### ✅ Vantagens


1. **Flexibilidade**

   
   1. Possibilidade de personalizar o código, mudando o número de digítos e até mesmo o formato.
2. **Mais controle**

   
   1. Total liberdade da lógica de geração, armazenamento e validação do código;
   2. Independência de bibliotecas externas.
3. **Simplicidade**

   
   1. Fácil de implementar de acordo com o escopo que já temos.

### ❌ Desvantagens


1. **Segurança**

   
   1. Pode ser menos seguro gerar um código aleatório por conta própria.
   2. Não possui garantias de resistência contra ataques.
2. **Dependência de armazenamento**

   
   1. É necessário armazenar o código gerado para validá-lo posteriormente (por exemplo, no Redis).
3. **Implementação de login completo**

   
   1. Seria necessário implementar nosso próprio esquema de login, diferente do que é feito hoje, onde apenas integramos com o Auth0.

### 💻 Exemplo de código

```python

def generate_otp_code(length=6):
    digits = string.digits
    return ''.join(random.choices(digits, k=length))

@router.post("/send_otp_code")
async def send_otp_code(
    body: OTPCreate
):
    otp = generate_otp_code()
    await cache.async_redis_cli.set(f"otp:{body.email}", otp, ex=60 * 5)
    
    email_body = f"""
        <html>
        <body>
            <p>Olá,</p>
            <p>Seu código de autenticação é: <strong>{otp}</strong></p>
            <p>Este código é válido por 5 minutos.</p>
        </body>
        </html>
        """

    send_email.delay(
        'email@email.com',
        'OTP RANDOM',
        email_body,
    )

    return {"message": "Código enviado para seu e-mail. Válido por 5 minutos."}

@router.post("/login/v2")
async def validate_otp(
    body: LoginOTP
):
    stored_otp = await cache.async_redis_cli.get(f"otp:{body.email}")

    if not stored_otp or body.otp != str(stored_otp, 'utf-8'):
        raise HTTPException(status_code=400, detail="Código OTP inválido ou expirado.")

    await cache.async_redis_cli.delete(f"otp:{body.email}")

    return {"message": "Autenticação bem-sucedida."}
```

## Usar a biblioteca pyotp

### ✅ Vantagens


1. **Segurança**

   
   1. PyOTP implementa o padrão TOTP (Time-based One-Time Password) e HOTP (HMAC-based One-Time Password), que seguem especificações seguras e amplamente utilizadas.
2. **Simplicidade na validação**

   
   1. Não é necessário armazenar o código OTP no redis, pois ele pode ser regenerado dinamicamente com a mesma chave secreta e comparado com o código fornecido.
3. **Resistência contra ataques**

   
   1. Menos suscetível a ataques de brute force, pois os códigos expiram rapidamente e são baseados em uma combinação única de tempo e chave secreta.

### ❌ Desvantagens


1. **Dependência de biblioteca externa**

   
   1. Requer PyOTP, o que adiciona uma dependência ao projeto.
2. **Implementação de login completo**

   
   1. Seria necessário implementar nosso próprio esquema de login, diferente do que é feito hoje, onde apenas integramos com o Auth0.

### 💻 Exemplo de código

### Counter-Based OTP (HOTP)

Baseado em um contador compartilhado entre cliente e servidor.

* **Como funciona:**
* Cada vez que um código é gerado, o contador é incrementado.
* O servidor verifica o valor do contador para validar o código.

**Exemplo de uso:** Sistemas em que o OTP é gerado por eventos, como pressionar um botão.

```python

import pyotp

hotp = pyotp.HOTP('base32secret3232')
hotp.at(0) # => '260182'
hotp.at(1) # => '055283'
hotp.at(1401) # => '316439'

# OTP verified with a counter

hotp.verify('316439', 1401) # => True

hotp.verify('316439', 1402) # => False
```

### Time-Based OTP (TOTP)

Baseado no tempo atual.

**Como funciona:**

* Um código é gerado com base em uma combinação do segredo compartilhado e o tempo atual dividido em intervalos (geralmente de 30 segundos).
* O servidor valida o código com base no intervalo de tempo atual.

**Exemplo de uso:** Autenticação de dois fatores (2FA) amplamente usado em aplicativos como Google Authenticator, Authy, etc.

```python

import pyotp

import time

totp = pyotp.TOTP('base32secret3232')
totp.now() # => '492039'

# OTP verified for current time

totp.verify('492039') # => True

time.sleep(30)
totp.verify('492039') # => False
```


\
## Auth0

É possível também manter o auth0 e configurar o login com OTP via e-mail ou SMS.

### ✅ **Vantagens**


1. **Facilidade de implementação**

   
   1. Fluxos passwordless já prontos para uso, sendo necessário apenas configurar via dashboard;
2. **Segurança**

   
   1. Autenticação baseada em protocolos seguros (como OAuth 2.0 e OpenID Connect);
   2. Armazenamento e envio de códigos de acesso gerenciados diretamente pelo Auth0, reduzindo a necessidade de infraestrutura adicional;
3. **Já Usado Atualmente**

   
   1. Já fazemos uso do Auth0 na solução atual, o que reduz a curva de aprendizado para configuração e manutenção;

### ❌ **Desvantagens**


1. **Dependência de Serviço Externo**

   
   1. Requer dependência da infraestrutura e disponibilidade do Auth0;
2. **Mudança no tipo de login usado atualmente**

   
   1. Para o passwordless do auth0 funciona, é necessário desativar o que eles chamam de [universal login](https://auth0.com/features/universal-login), o que desabilitaria os logins com email e senha e também o login com a conta google. Também impactaria na maneira que customizamos o widget deles, de modo que seria necessário fazer via HTML.

## Firebase Authentication

### ✅ Vantagens


1. **Facilidade de Implementação**

   
   1. SDKs e bibliotecas prontas: O Firebase oferece bibliotecas e SDKs que facilitam a integração, no caso do python, temos a biblioteca `firebase-admin` ;
2. **Segurança**

   
   1. Criptografia e protocolos de segurança: O Firebase Authentication utiliza padrões de segurança reconhecidos, como OAuth 2.0 e OpenID Connect. Além disso, os links de autenticação (Magic Links) são gerados e enviados de forma segura, e os dados são protegidos por criptografia, oferecendo uma camada robusta de segurança;

### ❌ **Desvantagens**


1. **Dependência de Serviço Externo**

   
   1. Nossa infraestrutura está na AWS, enquanto o Firebase é uma solução fora desse ecossistema. Isso pode criar desafios de integração, além de aumentar a dependência de uma plataforma externa (Google) para o gerenciamento de autenticaçã;
2. **Custos Crescentes**

   
   1. O Firebase utiliza um modelo de precificação baseado no número de autenticações, especialmente para SMS e e-mails. Isso pode gerar custos inesperados à medida que o número de usuários ou as tentativas de login aumentem;
   2. Embora o Firebase haja uma camada gratuita ([detalhes aqui](https://firebase.google.com/pricing)), ela possui limites e, conforme o uso aumenta, tornando necessárop migrar para um plano pago. Isso pode se tornar um custo crescente se a base de usuários for grande.

## **Supabase**

### ✅ Vantagens


1. **Facilidade de Implementação**

   
   1. Fluxos de autenticação sem senha prontos para uso, com configuração simples (<https://supabase.com/docs/reference/python/auth-signinwithotp>).
2. **Plano bom**

   
   1. O plano gratuito engloba 50k de usuários ativos mensalmente.

### ❌ Desvantagens


1. **Dependência do PostgreSQL**

   
   1. A solução é centrada no PostgreSQL, o que pode ser um limitador caso um dia a gente precise trocar de banco;
2. **Imaturidade**

   
   1. O projeto ainda está em desenvolvimento e pode ter menos recursos e suporte comparado a soluções mais maduras.
3. **Complexidade Desnecessária**

   
   1. O Supabase oferece um ecossistema completo, incluindo banco de dados, autenticação, armazenamento e etc, mas, para um propósito simples como login sem senha, parece uma solução excessiva.

## magic.link

<https://magic.link/docs/authentication/overview>

### ✅ Vantagens


1. Implementação fácil

   
   1. SDKs e APIs bem documentadas, facilitando a implementação.
2. Redução de Complexidade

   
   1. Gerenciamento de tokens, autenticação e validação é tratado diretamente pela plataforma.

### ❌ Desvantagens


1. Custo elevado

   
   1. Preço muito alto (detalhes em <https://magic.link/pricing>)

## :warning: **Keycloak**

Não oferece suporte a OTP via email ou SMS, sendo possível usar somente via app de autenticação (Google authenticator, Authy e etc).