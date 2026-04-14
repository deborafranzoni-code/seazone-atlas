<!-- title: Suspeita de Fraude | url: https://outline.seazone.com.br/doc/suspeita-de-fraude-2cUAe7dm3k | area: Tecnologia -->

# Suspeita de Fraude

# Classificação de Fraude

Um usuário pode ser considerado suspeito de fraude ao apresentar um ou mais comportamentos suspeitos.

As classificações de fraude são as seguintes:

* **not_fraud**: Cliente com características que o identificam como não fraudulento, permitindo seguir o fluxo de cobrança sem necessidade de verificação anti-fraude.
* **suspect**: Usuário com comportamentos suspeitos, classificado como potencial fraude, devendo passar pelo processo de verificação anti-fraude.
* **fraud**: Usuários confirmados como fraudulentos pelo sistema de verificação, cuja conta Seazone deve ser bloqueada.

## Not Fraud

O cliente deve ser classificado como não fraudulento se apresentar o seguinte padrão de comportamento:

* A última reserva paga foi realizada há mais de 3 meses.

## Suspect

Todos os usuários que não atenderam ao menos uma das regras definidas em `not_fraud` devem passar pela verificação de fraude.

## Fraud

O cliente deve ser classificado como fraude caso o pagamento seja negado por suspeita de fraude. Neste caso, a conta Seazone deve ser bloqueada imediatamente, impedindo novas reservas.

## Requisitos Importantes

A verificação de possíveis fraudes deve ser realizada no momento da reserva para todos os clientes que estão marcados como *fraud = false* no banco de dados. Usuários só serão marcados como fraudulentos após a confirmação de possível fraude pelo gateway de pagamento. Uma vez identificados como fraudulentos, esses usuários não devem ter acesso ao site.