<!-- title: Guia Interno: POC Referral | url: https://outline.seazone.com.br/doc/guia-interno-poc-referral-JAj9dBAhcc | area: Tecnologia -->

# Guia Interno: POC Referral

# Objetivo & Motivação

Validar a viabilidade de um programa de indicação (referral) que apoie o crescimento orgânico da Seazone a partir da base de clientes existente. 

# Detalhes da Implementação

A POC implementa a divulgação de cupons personalizados no email de confirmação de pagamento da reserva, permitindo que cada usuário compartilhe seu cupom com amigos. Cada novo usuário que realizar uma reserva recebe o próprio cupom, garantindo a continuidade do ciclo de compartilhamento.

Na prática, cada usuário "possui" um cupom referral que é revelado apenas no momento em que recebe o email de confirmação de pagamento, ou seja, somente após efetuar uma reserva. Para suportar o monitoramento dessas métricas de envio de forma isolada, criamos um novo sender exclusivo para os emails de confirmação de pagamento: `noreply-payments@seazone.com.br`.

Como a infraestrutura de cupons já é fornecida pela plataforma parceira Stays, o que temos é um padrão de nome de cupom `[PrimeiroNome]15REF[UserID]` (MARIA15REF222), que, ao ser inserido, aponta para um cupom "pai" único na Stays, o `referral15`.

O foco da POC está em validar a experiência do usuário, os fluxos técnicos envolvidos e o potencial de adoção da funcionalidade. É possível desligar a divulgação do cupom de referral através da feature flag [ff_enable_referral_banner](https://us.posthog.com/project/47303/feature_flags/201463).

# Monitoramento & Métricas

A ideia principal é validar se as pessoas estão reservando mais e se os cupons referral estão sendo efetivamente compartilhados e utilizados pelos novos usuários. Para isso, contamos com diferentes métodos e fontes de dados para acompanhar esses indicadores:

## Quantidade de Reservas via Referral

É possível acompanhar o uso de cupons referral e identificar quais são os mais utilizados através do Metabase, [neste link](https://metabase.seazone.com.br/dashboard/62-kpis-site?city=Salvador&filtro_de_data=past7days&tab=30-referral).

 ![](/api/attachments.redirect?id=3ff48585-8e01-4d9f-984f-42d3f5eadf26 " =1920x1080")

## Dados do Funil de Checkout com Cupons Referral

É possível acompanhar o fluxo de uso de cupons referral no checkout (incluindo número de acessos ao checkout, inserções de cupom, reservas pagas e reservas pagas com cupom referral) através do PostHog, neste [link](https://us.posthog.com/project/47303/notebooks/ZM9uI8Ak) .

 ![](/api/attachments.redirect?id=4030332e-4029-4956-bad3-12135bc08a2a " =1920x1080")

## Estatísticas do Email de Confirmação de Pagamento

Para acompanhar a performance do envio de cupons referral, habilitamos o "Gerenciador Virtual de Capacidade de Entrega" do AWS SES, que já era utilizado pelo sistema. 

Além disso, como mencionado anteriormente, criamos um sender exclusivo para os emails de confirmação de pagamento, permitindo separar as métricas desses disparos no console e monitorar aberturas, cliques e entregas de forma isolada. As estatísticas podem ser acessadas diretamente no console do SES, neste [link](https://sa-east-1.console.aws.amazon.com/ses/home?region=sa-east-1#/vdm/dashboard?tabId=identities).

Para facilitar o entendimento do acesso ao SES e das métricas disponíveis, anexamos um vídeo demonstrativo que explica passo a passo o funcionamento desde o início.

[https://drive.google.com/file/d/1AVXeQmQjAqvdHlFHpd1%5FbpIZO3dRYBEc/view?usp=sharing](https://drive.google.com/file/d/1AVXeQmQjAqvdHlFHpd1%5FbpIZO3dRYBEc/view?usp=sharing)

### Glossário de métricas

* **Volume de envio**: número total de mensagens para as quais houve solicitação de envio bem-sucedida pelo SES (cada tentativa de envio conta como um envio).
  * *Exemplo:* se você enviar 100 e-mails, o volume de envio será 100.
* **Entregas**: número de e-mails efetivamente entregues com sucesso ao servidor de e-mail do destinatário.
  * *Exemplo:* de 100 mensagens enviadas, se 90 chegam ao servidor de destino, há 90 entregas.
* **Reclamações**: número de e-mails entregues que foram marcados como spam ou reclamados pelo destinatário
  * *Exemplo:* se 5 pessoas que receberam o e-mail marcaram-no como spam, há 5 reclamações.
* **Devoluções**: número de e-mails que foram permanentemente rejeitados pelo servidor de destino. Existem dois tipos:
  * **Devolução Transitória (Soft Bounce):** falha temporária. Ocorre quando o e-mail não pôde ser entregue no momento, mas há chance de sucesso em tentativas futuras.
    * *Exemplo:* a caixa de entrada do destinatário está cheia.
  * **Devolução Permanente (Hard Bounce):** falha definitiva. Ocorre quando o endereço de e-mail é inválido ou inexistente. O SES não tenta reenviar e coloca o endereço na **Suppression List**.
    * *Exemplo:* o endereço usuario@dominioinvalido.com não existe.
  * *Exemplo:* se 10 mensagens retornarem com erro permanente, há 10 devoluções.
* **Taxa de abertura**: porcentagem de e-mails recebidos que foram abertos pelo destinatário em seu cliente de e-mail
  * *Exemplo:* se 60 dos 100 destinatários abrirem o e-mail, são registradas 60% de taxa de aberturas.
* **Taxa de Clique:** porcentagem de emails entregues em que os destinatários clicaram em um ou mais links contidos no e-mail.
  * *Exemplo*: se 30 de 100 e-mails entregues tiveram cliques em links, a taxa de clique é 30%.

  \

### Links

Acesso a AWS: <https://seazone.awsapps.com/start/#/?tab=accounts>

Estatísticas do Email de Confirmação de Pagamento: <https://sa-east-1.console.aws.amazon.com/ses/home?region=sa-east-1#/vdm/dashboard/identity/noreply-payments%40seazone.com.br>