<!-- title: Discovery - Personificação de Hóspedes | url: https://outline.seazone.com.br/doc/discovery-personificacao-de-hospedes-yXrc7hTaaN | area: Tecnologia -->

# Discovery - Personificação de Hóspedes

# Objetivo

O objetivo deste *discovery técnico* é definir e alinhar a abordagem técnica para o **fluxo de personificação de hóspedes** no banco de dados do Sapron, garantindo padronização dos dados de usuários.

# Ações necessárias

## Fluxo de pré-checkin

No contexto do **pré-check-in**, a principal mudança consiste na **necessidade de gerenciar o registro do hóspede principal nas tabelas** `**account_user**` **e** `**account_guest**`, aplicando regras específicas para **evitar a duplicidade de cadastros** e garantir a correta normalização dos dados provenientes de fontes externas à plataforma.

A partir dessa mudança, o **formulário de pré-check-in** passará a aceitar o **e-mail do hóspede principal** (não obrigatório), que será utilizado como **identificador único para a personificação desse ator no sistema**. Esse e-mail servirá como chave para localizar ou criar o vínculo adequado entre o hóspede, o usuário e a reserva associada.

### Regras de Negócio

#### Reservas que possuem e-mail (Booking, Expedia, Website Seazone, entre outros)


1. Se o usuário inserir um e-mail no pré-check-in que existe na `account_user` e esse e-mail for diferente do e-mail que está registrado na `account_user` da reserva, então vamos criar um registro na tabela `user_email_mapping` associando o e-mail antigo com o usuário que possui o e-mail do pré-check-in. Por exemplo, suponha que importamos uma nova reserva para o usuário que possui o e-mail "antigo@guest.booking.com". Ao fazer o pré-check-in, o usuário inseriu o e-mail "novo@gmail.com", que está vinculado ao usuário 123456. Então, durante o pré-check-in, criamos o registro abaixo.

| user_email_mapping |
|----|
| id | stays_email | user_id (PK account_user) |
| 1 | antigo@guest.booking.com | 123456 |

   \
2. Se o usuário inserir um e-mail no pré-check-in que existe na `account_user` e esse e-mail for diferente do e-mail que está registrado na `account_user` da reserva, então atualizamos o `guest_id` da reserva, para apontar para o `account_guest` que possui o usuário com o e-mail registrado no pré-check-in. Além disso, removemos o e-mail anterior do usuário na `account_user`, para evitar que novas reservas voltem a ser atribuídas a esse usuário. Também atualizamos o telefone do usuário, pois consideramos que o telefone enviado pela Stays está atualizado, principalmente porque é através dele que enviamos o pré-check-in. Por exemplo, suponha esse cenário antes do pré-check-in:

| reservation_reservation | account_guest | account_user | user_email_mapping |
|----|----|----|----|
| id | guest_id | code | id | user_id | id | email | phone | id | stays_email | user_id |
| 1 | 1 | ABC123 | 1 | 1 | 1 | fulano@gmail.com | 55 47 99199 9876 |    |    |    |
| 2 | 2 | ABC456 | 2 | 2 | 2 | fulano@guest.booking.com | 55 47 99101 2345 |    |    |    |

   Se durante o pré-check-in fosse inserido o email "fulano@gmail.com", então a nova configuração seria:

| reservation_reservation | account_guest | account_user | user_email_mapping |
|----|----|----|----|
| id | guest_id | code | id | user_id | id | email | phone | id | stays_email | user_id |
| 1 | 1 | ABC123 | 1 | 1 | 1 | fulano@gmail.com | 55 47 99101 2345 | 1 | fulano@guest.booking.com | 1 |
| 2 | 1 | ABC456 | 2 | 2 | 2 |    |    |    |    |    |

   \
3. Se o usuário inserir no pré-check-in um e-mail de um usuário que existe na `account_user`, mas esse usuário possui outras roles, então não podemos atualizar os seus dados de e-mail e telefone desse usuário. Apenas atualizamos o `account_guest` para apontar para o usuário correto na `account_user`. Por exemplo, suponha a seguinte configuração do banco, em que o usuário 1 tem uma role de Host:

| reservation_reservation | account_guest | account_user | user_email_mapping |
|----|----|----|----|
| id | guest_id | code | id | user_id | id | email | phone | id | stays_email | user_id |
| 1 | 1 | ABC123 | 1 | 2 | 1 | fulano@gmail.com | 55 47 99199 9876 |    |    |    |
|    |    |    |    |    | 2 | fulano@guest.booking.com | 55 47 99101 2345 |    |    |    |

   Se no pré-check-in for inserido o e-mail "fulano@gmail.com", então o banco deverá ficar com seguinte configuração após o pré-check-in:

| reservation_reservation | account_guest | account_user | user_email_mapping |
|----|----|----|----|
| id | guest_id | code | id | user_id | id | email | phone | id | stays_email | user_id |
| 1 | 1 | ABC123 | 1 | 1 | 1 | fulano@gmail.com | 55 47 99199 9876 | 1 | fulano@guest.booking.com | 1 |
|    |    |    |    |    | 2 |    |    |    |    |    |

   Ou seja, não atualizamos os dados do usuário 1, pois ele possui outros papéis no back-office. Apenas atualizamos o apontamento na `account_guest` e removemos os dados do registro 2 na `account_user`.
4. Se o usuário inserir no pré-check-in um e-mail que não existe na `account_user`, então atualizamos o `account_user` que a reserva está apontando para ficar com esse novo e-mail. Porém, **isso só é feito se o usuário não tiver outras roles no Sapron**. Por exemplo, considere a seguinte configuração do banco:

| reservation_reservation | account_guest | account_user | user_email_mapping |
|----|----|----|----|
| id | guest_id | code | id | user_id | id | email | phone | id | stays_email | user_id |
| 1 | 1 | ABC123 | 1 | 1 | 1 | fulano@guest.booking.com | 55 47 99199 9876 |    |    |    |

   Se o usuário inserir no pré-check-in o e-mail "fulano@gmail.com", como ele não existe na `account_user`, então vamos atualizar o registro 1 por esse novo e-mail (além de inserir o e-mail anterior na `user_email_mapping`):

| reservation_reservation | account_guest | account_user | user_email_mapping |
|----|----|----|----|
| id | guest_id | code | id | user_id | id | email | phone | id | stays_email | user_id |
| 1 | 1 | ABC123 | 1 | 1 | 1 | fulano@gmail.com | 55 47 99199 9876 | 1 | fulanoo@guest.booking.com | 1 |

#### Reservas que não possuem e-mail (Airbnb)


1. Reservas que não possuem e-mail não criam registros na tabela `user_email_mapping`;
2. Se o usuário inserir no pré-check-in um e-mail que existe na `account_user` e ele é um guest, então atualizamos o `guest_id` da reserva, para apontar para o `account_guest` que possui o usuário com o e-mail registrado no pré-check-in. Além disso, atualizamos o telefone desse `account_user` para deixá-lo com o telefone mais atualizado, pois se isso não fosse feito, novas reservas continuariam sendo atribuídas ao outro usuário. Por exemplo, imagina o seguinte cenário:

| reservation_reservation | account_guest | account_user | user_email_mapping |
|----|----|----|----|
| id | guest_id | code | id | user_id | id | email | phone | id | stays_email | user_id |
| 1 | 1 | ABC123 | 1 | 1 | 1 | fulano@gmail.com | 55 47 99199 9876 |    |    |    |
| 2 | 2 | ABC456 | 2 | 2 | 2 |    | 55 47 99101 2345 |    |    |    |

   Se no pré-check-in fosse inserido o e-mail "fulano@gmail.com", então a reserva 2 seria atualizada para apontar para o `account_guest` 1. Além disso, nesse caso, o telefone do usuário 1 seria atualizado:

| reservation_reservation | account_guest | account_user | user_email_mapping |
|----|----|----|----|
| id | guest_id | code | id | user_id | id | email | phone | id | stays_email | user_id |
| 1 | 1 | ABC123 | 1 | 1 | 1 | fulano@gmail.com | 55 47 99101 2345 |    |    |    |
| 2 | 1 | ABC456 | 2 | 2 | 2 |    |    |    |    |    |
3. Se o usuário inserir no pré-check-in um usuário que não existe na `account_user`, então atualizamos o `account_user` vinculado a reserva para ficar com o novo e-mail. Por exemplo, considere a seguinte configuração do banco:

| reservation_reservation | account_guest | account_user | user_email_mapping |
|----|----|----|----|
| id | guest_id | code | id | user_id | id | email | phone | id | stays_email | user_id |
| 1 | 1 | ABC123 | 1 | 1 | 1 | fulano@gmail.com | 55 47 99199 9876 |    |    |    |

   Se o usuário inserir no pré-check-in o e-mail "fulano.silva@gmail.com", como ele não existe na `account_user`, então vamos atualizar o registro 1 por esse novo e-mail:

| reservation_reservation | account_guest | account_user | user_email_mapping |
|----|----|----|----|
| id | guest_id | code | id | user_id | id | email | phone | id | stays_email | user_id |
| 1 | 1 | ABC123 | 1 | 1 | 1 | fulano.silva@gmail.com | 55 47 99199 9876 |    |    |    |
4. Se o usuário inserir no pré-check-in um e-mail que existe na base, mas esse usuário possui outras roles, então vamos atualizar o `user_id` da `account_guest` associado a reserva, para apontar para o usuário que possui o e-mail inserido no pré-check-in. Por exemplo, na configuração a seguir:

| reservation_reservation | account_guest | account_user | user_email_mapping |
|----|----|----|----|
| id | guest_id | code | id | user_id | id | email | phone | id | stays_email | user_id |
| 1 | 1 | ABC123 | 1 | 2 | 1 | fulano@gmail.com | 55 47 99199 9876 |    |    |    |
|    |    |    |    |    | 2 |    | 55 47 99101 2345 |    |    |    |

   Se o pré-check-in fosse feito para o e-mail "fulano@gmail.com", como esse usuário não possui um `account_guest`, então vamos atualizar o `user_id` da `account_guest` 1 para associá-la a esse usuário.

| reservation_reservation | account_guest | account_user | user_email_mapping |
|----|----|----|----|
| id | guest_id | code | id | user_id | id | email | phone | id | stays_email | user_id |
| 1 | 2 | ABC123 | 1 | 1 | 1 | fulano@gmail.com | 55 47 99199 9876 |    |    |    |
|    |    |    |    |    | 2 |    | 55 47 99101 2345 |    |    |    |

   Essa decisão foi escolhida pois assim todas as demais reservas que apontam para esse `account_guest` 1 não precisam ser atualizadas. Se a gente atualizasse o `guest_id` da reserva, teríamos que fazer isso também para outras reservas desse `guest_id`.

   Como esse usuário tem uma role diferente, então não mudamos o telefone. Isso significa que o `account_user` 2 continua com o telefone do usuário e, por isso, futuras reservas podem ser atribuídas a ele.

               

Esse fluxo garante que:

* Usuários já existentes sejam reutilizados sempre que possível;
* O vínculo entre `account_user`, `account_guest` e `reservation_reservation` seja mantido de forma consistente;
* A criação de registros duplicados seja evitada, preservando a integridade dos dados e a rastreabilidade das ações realizadas em nome do hóspede principal.

### **❗** Pontos de atenção


1. O email deve ser validado, inicialmente por regex, para garantir que é um email real. Inicialmente, a validação poderá ser via regex, mas a utilização de bibliotecas como [email-validator](https://pypi.org/project/email-validator/) podem ser levadas em consideração
2. O email não será obrigatório, então, toda ação deve ser ignorada caso o usuário não preencha o email

## Fluxo de sincronização com Stays

Para garantir que as reservas serão associadas aos usuários corretos e que não haverá atualizações de usuários nas reservas, precisamos fazer algumas alterações na task de importação de reservas (*stays_handler_reservation_task*), mais especificamente na parte que determina qual guest será atribuído a reserva.

### Regras de Negócio


1. A atribuição de um guest a uma reserva só será feita durante a criação da reserva. Portanto, uma vez que a reserva foi criada, não alteramos mais o o `guest_id` da reserva, ou o `user_id` vinculado a esse `account_guest`.
2. Para determinar qual usuário será atribuído a uma reserva durante a criação dela, vamos efetuar a lógica a seguir:

   
   1. Se a nova reserva tem um e-mail, verificamos se o e-mail está inserido na `user_email_mapping`. Se estiver, então inserimos na reserva o guest vinculado ao usuário definido na `user_email_mapping`.
   2. Se a nova reserva tem um e-mail e ele não está inserido na `user_email_mapping`, então buscamos um `account_user` que possua esse e-mail. Se for encontrado um, então o associamos a reserva.
   3. Se não for encontrado o usuário por e-mail, então buscamos com o telefone e nome que veio na reserva. Se encontrarmos um `account_user` com esses dados, então o associamos a reserva.
   4. Se não for encontrado um usuário com o telefone fornecido, então criamos um novo usuário.
3. Se a reserva tiver uma atualização de telefone ou de CPF, o importador de reserva faz essa atualização somente se o `account_user` vinculado a reserva não possuir uma role de Host ou Owner.
4. O importador de reservas não realiza atualizações de e-mails de usuários vinculado a reserva;

### Nova tabela `user_email_mapping`

A tabela `user_email_mapping` possui os seguintes campos:

* Colunas básicas (id, created_at, updated_at);
* *stays_email*: e-mail do usuário fornecido pela Stays e que difere do e-mail enviado no pré-check-in;
* *user_id*: ID do guest na tabela `account_user`;
  * Chave estrangeira para a tabela `account_user`;

Esse registro será inserido durante a etapa de pré-check-in, se o usuário inserir um e-mail válido.

## Cenários de Teste

Essa nova feature precisa considerar os seguintes casos, que estão descritos no diagrama abaixo:


1. O usuário cadastra um e-mail no pré-check-in que não existe em nossa base;
2. O usuário cadastra um e-mail no pré-check-in que existe em nossa base e ele está vinculado a um usuário que possui role de guest (ou seja, possui um registro na `account_guest` apontando para esse `user_id`);
3. O usuário cadastra um e-mail no pré-check-in que existe em nossa base, mas o usuário desse e-mail não possui role de guest. Por exemplo, ele é um Host, Owner, ou Admin;

```mermaidjs
flowchart TD
    A[Start] --> B
    B[E-mail de pré-check-in é inserido] --> C{Existe email na account_user?}
    C --> | Yes | D{Possui account_guest?}
    D --> | Yes | E[Atualiza reservation_reservation com o guest_id relacionado ao usuário com e-mail do pré-check-in.]
    D --> | No | F[Atualiza user_id da account_guest da reserva com o usuário que possui o e-mail do pré-check-in.]
    C --> | No | G[Atualiza email do hóspede principal na account_user com o e-mail do pré-check-in.]
```

As regras de uso descritas anteriormente lidam com cada um desses cenários.

Além disso, vale a pena prestar atenção em dois pontos:


1. A maioria das reservas enviam o e-mail do hóspede principal. Porém, reservas do Airbnb não enviam essa informação. Por isso, o pré-check-in deve lidar com esses cenários, em que um usuário pode não ter e-mail cadastrado na `account_user`;
2. O importador de reservas pode atualizar os dados do usuário na `account_user`, como telefone e cpf, se a role do hóspede for guest. Se a role do usuário for  Host ou Owner, esses dados não podem ser atualizados.

Sendo assim, fizemos diversas simulações envolvendo esses cenários e eles estão descritos [nesta planilha](https://docs.google.com/spreadsheets/d/1UWGJhWyLF1D0TOxVnkD7Wzt888FKNK1rqCbKMlL_6zA/edit?usp=sharing).

### Reservas de OTAs diferentes

Quando um hóspede faz uma reserva em OTAs diferentes, a Stays não envia as mesmas informações sobre os hóspedes. Abaixo segue algumas diferenças entre cada OTA:

* 
  1. Airbnb: envia telefone e nome;
* 
  2. Booking: envia e-mail, telefone e nome;
* 
  3. Expedia: envia e-mail, telefone e nome;
* 
  4. (Antigo) HomeAway\*\*:\*\* envia e-mail, telefone, documento (cpf ou passaporte) e nome;
* 
  5. Stays: envia e-mail, telefone e nome;
* 
  6. ~~Temporada Livre: sem informações;~~
* 
  7. (Antigo) Contrato: envia e-mail, telefone, documento e nome;
* 
  8. Website Seazone: envia e-mail, telefone, documento e nome;
* 
  10. Decolar: envia e-mail, telefone e nome;
* 
  11. Madego: envia e-mail, telefone, documento e nome;

Portanto, a solução proposta neste documento vai conseguir identificar os usuários para quase todas as OTAs que temos integração. A exceção será o Airbnb, porque a Stays não envia o e-mail na requisição. Porém, apenas para o Airbnb, poderíamos usar o telefone para identificar o usuário.

## Atividades



1. **~~\[Wallet\]~~** ~~Criar nova tabela~~ `~~user_email_mapping~~` ~~no BD do Sapron;~~
2. **\[Wallet\]** Registrar e-mail Stays na `user_email_mapping` durante o pré-check-in;

   
   1. Criar uma env var para controlar o release da solução;
3. **\[Reservas\]** Ajustar importador de reservas para obter o `account_user` pela `user_email_mapping`;

   
   1. Criar uma env var para controlarmos o release da solução;
4. **\[Wallet | Reservas\]** Validação do fluxo em staging
5. **\[Reservas\]** Remover env var após validação da solução;
6. **\[Wallet\]** Remover env var após validação da solução;

\n**Para o deploy:**



1. Fazer primeiro deploy no importador de reservas;
2. Fazer deploy no Wallet;