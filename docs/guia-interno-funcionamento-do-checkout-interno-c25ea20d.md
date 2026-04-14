<!-- title: Guia Interno: Funcionamento do Checkout Interno | url: https://outline.seazone.com.br/doc/guia-interno-funcionamento-do-checkout-interno-QB1Uez0qi4 | area: Tecnologia -->

# Guia Interno: Funcionamento do Checkout Interno

Este documento tem como objetivo explicar o funcionamento do nosso **checkout interno**, com foco em como ele se comporta e se conecta aos serviços internos e externos. Ao contrário de uma documentação voltada à API, aqui queremos centralizar o **conhecimento contextual e técnico** sobre o processo, para facilitar a vida de qualquer dev que precise entender, dar manutenção ou evoluir essa funcionalidade.

> ⚠️ Este guia **não aborda detalhes de requisição ou resposta** da API. Para isso, consulte a documentação pública da API gerada com o [ReDoc](https://api.seazone.com.br/redoc#tag/reservations/operation/process_payment_capture_reservations_payment_pay_post).

# Contexto e Motivação

O checkout interno foi implementado para substituir o uso direto do link de pagamento que leva para checkout externo do Tuna, dando à Seazone mais controle sobre o fluxo, UX e integrações e etc.

Uma das principais motivações para implementarmos o checkout interno foi a possibilidade de permitir a troca entre meios de pagamento, algo que antes não era possível .Quando o cliente queria mudar a forma de pagamento, o atendimento precisava cancelar a reserva e gerar um novo link de pagamento.

# Visão Geral do Fluxo

`/payment/pay`

**Objetivo**: Iniciar o processo de pagamento para uma reserva.\n**Passos**:


1. **Validação da Sessão**:
   * Verifica ou cria uma nova sessão no Tuna usando **get_or_create_new_session**.
   * Se **X-Gateway-Session-Id** for inválido, gera um novo token.
2. **Busca da Reserva**:
   * Valida existência da reserva via **reservation_code** e **reservation_pin**.
3. **Tratamento de Conflitos**:
   * Cancela pagamentos PIX pendentes se o novo método for cartão (**verify_pix_conflict_and_cancel_if_needed**).
4. **Captura do Pagamento**:
   * Processa o pagamento via Tuna (**capture_payment**).

**Exceções**:

* **ReservationDoesNotExistsException**: Reserva não encontrada.
* **UserDoesNotExistsException**: Usuário não existe no banco de dados.

# Núcleo do Processamento: Classe `InternalCheckout`

**Responsabilidade**: Orquestrar toda a lógica de pagamento.

## **Métodos críticos**

* **capture_payment**:
  * Valida pré-condições (reserva, método de pagamento, CPF, etc.).
  * Prepara detalhes do pagamento (juros, descrição).
  * Comunica com a Tuna (**_process_tuna_payment**).
  * Salva o pagamento no banco (**_save_payment_with_status**).
* **_process_tuna_payment**:
  * Converte os dados para o formato esperado pela Tuna (**_init_payment_request**).
  * Trata erros da API (ex.: **TunaErrorInitingPaymentRequest**).
* **_save_reservation_payment_data**:
  * Atualiza a reserva (valor pago, método, parcelas).
  * Registra transações assíncronas via **record_payment_transaction.delay**.

## **Regras de Negócio**

* **Juros em Parcelas**:
  * Calculados via **_apply_interests_on_value** (usa **get_interests_of_installments**).
* **Antifraude**:
  * Verifica usuários bloqueados por e-mail/CPF (**_get_user_block_status**).

# Comunicação com a Tuna

## **Estrutura das Requisições**

### **_init_payment_request**:

* Estrutura dados do cliente, itens, métodos de pagamento (cartão/cartão com 3DS/PIX). Um dos pontos mais importantes dessa estruturação é a estruturação dos meios de pagamento realizada dentro desse método com a chamada de **_format_payment_methods**.

#### Meios de pagamento disponíveis

* **PIX**: método mais simples e direto.
* **Cartão de crédito**: possui duas variações com regras mais complexas:
  * Cartão com 3DS
  * Cartão sem 3DS (fluxo padrão)

#### Fluxos de pagamento com cartão no Tuna


1. **Fluxo Padrão (credit_card)**
   * Passa por checagem de antifraude.
   * Não exige autenticação por padrão.
   * Pode acionar o 3DS automaticamente se o comportamento do usuário for considerado suspeito.
2. **Fluxo 3DS (credit_card_with_3ds)**
   * Utiliza o **3D Secure (3DS)**: um protocolo de segurança que adiciona uma camada extra de autenticação.
   * Durante o pagamento, o cliente deve verificar sua identidade com o banco emissor.
   * Reduz significativamente o risco de fraude.

#### Como o fluxo é definido no código

* Se o campo `payment_method` da requisição para `/payment/pay` for:
  * "credit_card_with_3ds" → usa o **Fluxo 3DS**
  * "credit_card" → segue o **Fluxo Padrão**

#### Importância do authenticationInformation

* Campo essencial para pagamentos com cartão.
* Obtido na resposta da tokenização do cartão.
* Deve ser incluído na requisição enviada ao Tuna, sem ele o 3DS não funciona.
* É obrigatório em **ambos os fluxos**, pois o 3DS pode ser acionado em qualquer um deles.

## **Tratamento de Respostas**

* **Sucesso**:
  * Status **PAYMENT_ANALYSIS** para pagamentos em processamento.
  * Retorna dados específicos por método (ex.: QR Code para PIX, URL de 3DS).
* **Erros**:
  * Mapeia códigos de erro da Tuna para slugs internos (ex.: **GwNotAuthorized** → **CARD_NOT_AUTHORIZED**).

## Webhooks

A Tuna envia notificações assíncronas para informar eventos relacionados aos pagamentos. Esses eventos são tratados por métodos específicos na classe TunaWebhookHandler. Abaixo estão os principais tipos de webhook tratados e o comportamento esperado para cada um deles:

### payment_captured

* **Descrição**: Indica que o pagamento foi aprovado com sucesso.
* **Ação**:
  * Confirma o pagamento da reserva, alterrando seu status para paga.
  * Notifica o usuário.
  * Registra o evento na trilha de pagamento.

### payment_denied

* **Descrição**: Indica que o pagamento foi negado.
* **Ação**:
  * Marca o pagamento como falho.
  * Notifica o usuário.
  * Analisa o motivo da negação (incluindo possível fraude).
  * Se detectada fraude e o *feature flag* estiver habilitado, o acesso do usuário é bloqueado.

### payment_pending

* **Descrição**: Pagamento está pendente (ex: aguardando confirmação no PIX ou análise de risco).
* **Ação**:
  * Atualiza o status da reserva e do pagamento.
  * Registra o evento correspondente (ex: PAYMENT_PENDING ou PAYMENT_RISK_ANALYSIS).

### payment_chargeback

* **Descrição**: Indica que o pagamento foi estornado via chargeback.
* **Ação**:
  * Executa um processo assíncrono de chargeback.
  * Registra o evento na trilha de pagamento.

### payment_refunded

* **Descrição**: Pagamento foi reembolsado totalmente.
* **Ação**:
  * Atualiza o status do pagamento como REFUNDED.
  * Registra o evento de reembolso.

### payment_partial_refunded

* **Descrição**: Parte do valor pago foi reembolsado.
* **Ação**:
  * Atualiza o status do pagamento como PARTIAL_REFUNDED.
  * Registra o evento de reembolso.

### payment_canceled

* **Descrição**: Pagamento foi cancelado.
* **Ação**:
  * Apenas loga o evento.
  * Ainda não há um processo automatizado definido para lidar com cancelamentos.

# Segurança e Observabilidade

* **Dados Sensíveis**:
  * Cartões são tokenizados pelo Tuna (números não são armazenados).
* **Logs**:
  * Detalhes de transações são registrados (ex.: **payment_request** sem token do cartão).