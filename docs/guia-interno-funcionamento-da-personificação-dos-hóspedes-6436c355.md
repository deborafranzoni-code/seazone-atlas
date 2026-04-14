<!-- title: Guia Interno: Funcionamento da Personificação dos Hóspedes | url: https://outline.seazone.com.br/doc/guia-interno-funcionamento-da-personificacao-dos-hospedes-FoMd8mtaAp | area: Tecnologia -->

# Guia Interno: Funcionamento da Personificação dos Hóspedes

O objetivo desta documentação é explicar a abordagem técnica para o Fluxo de Personificação de Hóspedes no banco de dados do Sapron, garantindo padronização dos dados de usuários. Apesar de se tratar do banco do Sapron, essa feature faz parte da BU de Reservas, por isso será documentada aqui.

Para mais detalhes, acesse a planilha (a forma mais simples de entender é simulando os casos descritos nela): <https://docs.google.com/spreadsheets/d/1VFQpHkqB3Gbs65VovzSY1xl6J9Y1l5PLVZeWUjmW9Yo/edit?usp=sharing>

# Fluxo de pré-checkin

No contexto do pré-check-in, a principal mudança consiste na necessidade de gerenciar o registro do hóspede principal nas tabelas `account_user` e `account_guest`, aplicando regras específicas para evitar a duplicidade de cadastros e garantir a correta normalização dos dados provenientes de fontes externas à plataforma.

A partir dessa mudança, o formulário de pré-check-in passa a aceitar o e-mail do hóspede principal que será utilizado como identificador para a personificação desse ator no sistema. Esse e-mail servirá como chave para localizar ou criar o vínculo adequado entre o hóspede, o usuário e a reserva associada.

## Nova tabela \`user_identifier_mapping\`

Utilizamos a tabela `user_identifier_mapping` para registrar identificadores vindos das OTAs associados ao `account_user` correto.

Campos:

* `id`
* `identifier`: identificador vindo da reserva (ex.: e-mail Booking fulano@guest.booking.com)
* `account_user_id`: usuário final (normalmente o usuário identificado pelo e-mail do pré-check-in)

Na prática, quando o hóspede informa um e-mail no pré-check-in, o e-mail original que veio na reserva (ex.: fulano@guest.booking.com) passa a ser mapeado para o usuário do pré-check-in (ex.: fulano@gmail.com).

# Regras de negócio

## Modelo de dados (visão operacional)


1. `Reservation` (RR) referencia um `Guest ID` (AG) e tem `Stays Code`.​
2. `Account Guest` (AG) referencia um `User ID` (AU).​
3. `Account User` (AU) contém `MainRole`, `Email`, `Telefone`, `Nome`.​
4. `User Identifier Mapping` (UIM) contém `Identifier` e `Account User ID` para "lembrar" que um identificador externo pertence a um AU.

   \

## Caso 1 - Pré Checkin preenchido e account_user do pré checkin é Guest, e-mail diferente do e-mail da reserva

Condição:

* O pré checkin foi preenchido, este e-mail já existe em `Account User` como `MainRole=guest`, e é diferente do e-mail que veio na reserva.

O que deve acontecer:

* O `Account User` que ficará associado ao fluxo passa a usar o que possui o email informado no pré checkin, como e-mail do usuário "final" (o e-mail do hóspede).
* Deve existir um registro na `User Identifier Mapping` relacionando o e-mail original da reserva (ex: fulano@guest.booking.com) ao `Account User ID` do hóspede.
* O telefone do hóspede permanece o mesmo que já estava associado a account_user.

## Caso 2 - Pré Checkin preenchido, mas "já está correto" (e-mail igual)

Condição:

* O pré checkin foi preenchido e o email informado nele é igual ao e-mail atual associado ao usuário.

O que deve acontecer:

* Nenhuma alteração estrutural em `Reservation`→`Account Guest`→`Account User`.​
* Caso exista registro relacionado na `User Identifier Mapping`, permanece igual.

## Caso 3 - Pré Checkin preenchido e o email pertence a usuário Guest, mas o usuário atual da reserva tem outra role: atualizar vínculo sem alterar telefone

Condição:

* O pré checkin foi preenchido, e o cenário indica atualização de vínculo, mas preservação de telefone.

O que deve acontecer:

* O apontamento (vínculo) é corrigido para refletir o usuário encontrado pelo e-mail informado no pré checkin, sem atualizar dados.​
* Deve ser inserido um registro na `User Identifier Mapping` para o identificador externo apontar para o `Account User ID` correto.


## Caso 4 - PreCheckIn preenchido e o email informado nele é novo no sistema e o usuário atual da reserva não tem outras roles: atualizar e-mail do usuário atual

Condição:

* O email do pré checkin não existe na `Account User`.​

O que deve acontecer:

* A `Account User` da reserva tem seu e-mail atualizado para o e-mail informado no pré checkin.​
* Deve ser criado um registro na  `User Identifier Mapping` ligando o e-mail original da reserva ao `Account User ID` desse usuário.

## Caso 5 - PreCheckIn preenchido e o email informado nele é novo no sistema, mas o usuário atual da reserva tem outras roles

Condição:

* O cenário envolve `MainRole=host` (ou outra Secure Role).

O que deve acontecer:

* Não atualizar dados do usuário na account_user.​
* O sistema mantém o usuário sem sofrer alterações e utiliza a `User Identifier Mapping` para permitir associação ao usuário correto.


## Regras de negócio da Importação de reserva (criação) e Reimportação

## Caso 6 - Criação de reserva com e-mail (Booking/Website/Stays): usuário encontrado por telefone

Condição:

* Reserva chega com e-mail da OTA (ex: fulano@guest.booking.com) e telefone; o usuário é localizado pela busca por telefone.

O que deve acontecer:

* Reserva é criada apontando para `Account User` existente (ou criado) que referencia o usuário encontrado.
* O e-mail que veio na reserva (@guest.booking.com) pode ficar registrado no `Account User` enquanto o hóspede ainda não tiver preenchido o pré checkin. Após o Pré Checkin a `Account User` passa a ter o e-mail que o hóspede informou, mantendo o e-mail externo na `User Identifier Mapping`.

## Caso 7 - Após preenchimento do pré checkin existe um registro na  User Identifier Mapping para o e-mail da reserva: novas reservas com mesmo e-mail externo devem apontar para o usuário mapeado

Condição:

* Existe `User Identifier Mapping` com `Identifier = email da reserva` e `Account User ID = usuário do hóspede`.​

O que deve acontecer:

* Na importação de uma nova reserva com esse mesmo e-mail externo, o usuário deve ser encontrado pelo mapping e o vínculo Reservation→Account Guest→ Account User deve apontar para esse `Account User ID`.

## Caso 8 - Reimportação: não atualizar apontamentos Reservation→Account Guest→ Account User

Condição:

* Reserva já existe e é reimportada (mesmo `Stays Code`).​

O que deve acontecer:

* Nada acontece no sentido de não alterar os apontamentos de `Reservation.guest_id` e nem o vínculo Account Guest→ Account User.​
* Mesmo que o e-mail/telefone venha diferente na reimportação, o vínculo permanece como estava após o preenchimento do pré checkin daquela reserva.

## Caso 9 - Reimportação encontrada por mapping: dados não são atualizados quando a reserva é anterior ao último pré checkin preenchido

Condição:

* Reimportação encontra o usuário pela `User Identifier Mapping`, e o cenário define que a reserva é anterior ao último pré checkin preenchido.​

O que deve acontecer:

* Não atualizar `Account User`.

## Caso 10 - Atualização de dados em importação posterior ao último pré checkin preenchido (encontrado por mapping)

Condição:

* Importação de reserva encontra usuário pelo mapping, e o cenário define que a reserva é posterior ao último pré checkin preenchido.​

O que deve acontecer:

* Atualizar dados do usuário na `Account User` conforme o valor da nova reserva.

## Caso 11 - Reimportação com duas opções registradas

Condição:

* Reimportação de reserva com e-mail externo encontra usuário pelo mapping e chega com telefone diferente; o cenário lista duas possibilidades.​

O que deve acontecer:

* Não atualiza os dados do usuário porque a atualização é "congelada" após o pré checkin ser preenchido e a reserva ser anterior a ele.

## Regras para reservas sem e-mail (Airbnb)

### Caso 12 -  Criar registro na mapping por "Nome | Telefone" ao responder pré checkin e reutilizar nas próximas reservas

Condição:

* Reserva Airbnb chega sem e-mail, no pré checkin, o email informado já existe na `Account User`, há necessidade de estabilizar identificação por telefone/nome.​

O que deve acontecer:

* Inserir em `User Identifier Mapping` um `Identifier` no formato "Nome | Telefone" apontando para o `Account User ID` do hóspede.​
* Novas reservas com o mesmo telefone deve ser inserida apontando para esse mesmo usuário por causa do mapping.

### Caso 13 - Reimportações não alteram vínculo e não alteram dados existentes

Condição:

* Reimportação de reserva Airbnb já importada (mesmo código), ou cancelamento e recriação sem alteração de dados do hóspede.​

O que deve acontecer:

* Não atualizar registros.


\

\

\