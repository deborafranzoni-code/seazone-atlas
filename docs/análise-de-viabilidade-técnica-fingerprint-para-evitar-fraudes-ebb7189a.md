<!-- title: Análise de Viabilidade Técnica: Fingerprint para evitar fraudes | url: https://outline.seazone.com.br/doc/analise-de-viabilidade-tecnica-fingerprint-para-evitar-fraudes-d63HVMihFR | area: Tecnologia -->

# Análise de Viabilidade Técnica: Fingerprint para evitar fraudes

# Introdução

O objetivo da integração é aprimorar a detecção e prevenção de fraudes no site de reservas. Atualmente, enfrentamos desafios na identificação de usuários fraudulentos. A proposta é implementar a ferramenta [Fingerprint](https://fingerprint.com/), que nos permite identificar usuários de forma única.

Inicialmente, pretendemos utilizar o Fingerprint para identificar suspeitos de fraude e enviar alertas no grupo **#alert-fraud-website**, utilizaremos os seguintes critérios:

| **Motivo** | **Descrição** |
|----|----|
| CHARGEBACK_USER | Usuário que já realizou uma compra anteriormente e solicitou chargeback |

O alerta deve conter as seguintes informações:

* Data de check-in
* ID da Reserva (Stays)
* Nome do suspeito
* WhatsApp
* Propriedade
* Motivo

Essa integração visa aprimorar nosso controle sobre o processo de reservas, permitindo uma identificação mais precisa de possíveis fraudes e garantindo maior segurança para nossa plataforma e nossos clientes.

# Proposta de Solução

Para viabilizar a identificação consistente dos visitantes, propomos a seguinte solução: O fluxo centraliza a lógica de identificação e persistência na API de Reservas utilizando o `visitor_id` como chave para rastrear a atividade do usuário. Essa abordagem permite diferenciar acessos originados de diferentes dispositivos ou navegadores, mantendo um histórico de interações para análise.

## Fluxo para identificação do usuário


1. **Identificação no Frontend:**
   * Na página de Login e no botão "Confirmar e pagar" (e em outros momentos relevantes), o frontend coleta informações para construir um `visitor_id` (via SDK do Fingerprint) e o envia, juntamente com o email do usuário, para a API de Reservas.
2. **Endpoint da API:**
   * A API de Reservas recebe a requisição **PUT** `users/fingerprint/identify` contendo o `visitor_id` e o `email`.
3. **Verificação e Decisão:**
   * A API verifica se o `visitor_id` atual é diferente do `last_visitor_id` associado ao usuário.
4. **Persistência da Identidade :**
   * **Se o** `visitor_id` **for diferente:**
     * A API atualiza o campo `last_visitor_id` do usuário na tabela `users` no banco de dados.
     * Um novo registro é inserido na tabela `users_visitor_identities`, associando o `user_id`, o `visitor_id` e a data/hora da criação.
   * **Se o visitorId for o mesmo:**
     * Nenhuma ação de persistência é executada.


 ![Diagrama do fluxo de identificação do usuário](/api/attachments.redirect?id=2562c968-4438-4f87-aabe-d206885343c7)

*Disponível em: <https://miro.com/app/board/uXjVN47euTs=/?moveToWidget=3458764621388362108&cot=14>*

## Fluxo do alerta

Além da identificação do usuário (conforme o fluxo anterior), será necessário implementar também o processo de análise e alerta de possíveis chargebacks, o fluxo simplificado será:


1. **Fluxo de Registro da Transação:**
   * A Task `record_payment_transaction` registra os dados da transação de pagamento na tabela `payments_transactions`.
   * Essa task já existe atualmente, sendo necessário apenas ajustá-la para garantir que o evento de chargeback disparado pelo webhook do Tuna seja registrado na tabela, pois, no momento, isso não está sendo contemplado.
2. **Análise da Atividade do Usuário:**
   * Após o registro da transação, a Task `analyze_user_activity(visitor_id)` será executada.
   * O `UserActivityAnalyzer.analyze_by_visitor_id(visitor_id)` analisa a atividade do usuário pelo `visitor_id`.
3. **Validação de Chargeback:**
   * A validação **CHARGEBACK_USER** é realizada para verificar se há algum pagamento com um `visitor_id` associado ao usuário que está tentando comprar e que tenha passado por um chargeback.
4. **Geração de Log e Alerta:**
   * Um log é gerado com o resultado da validação.
   * **Se o resultado da validação CHARGEBACK_USER for TRUE (usuário suspeito de chargeback):**
     * Um alerta será disparado no canal **#website-fraud-alerts** com as informações da reserva, incluindo:
       * Stays ID
       * Check-in
       * Nome do suspeito
       * Whatsapp
       * Propriedade
       * Motivo: CHARGEBACK_USER
   * **Se o resultado da validação CHARGEBACK_USER for FALSE (usuário não suspeito):**
     * Nenhuma ação é tomada.

 ![Diagrama do fluxo de alerta](/api/attachments.redirect?id=a13a6cc6-fba5-431b-9875-9e4f9e931b2f)

*Disponível em: <https://miro.com/app/board/uXjVN47euTs=/?moveToWidget=3458764621489561680&cot=14>*