<!-- title: Diagnóstico de problemas TUNA | url: https://outline.seazone.com.br/doc/diagnostico-de-problemas-tuna-UNJIx98dOb | area: Tecnologia -->

# Diagnóstico de problemas TUNA

TL;DR

A proposta desse documento é abordar todos tópicos e demandas que desaceleraram a velocidade de entrega e diminuíram a qualidade do software desenvolvido dentro da Seazone.

# Dificuldades durante o desevolvimento do Checkout Próprio

O principal desafio durante o desenvolvimento deste produto foi, sem dúvida, a integração com a Tuna. A ausência de uma documentação clara, detalhada e com exemplos práticos (especialmente em relação ao 3DS) nos forçava a recorrer constantemente ao suporte para obter esclarecimentos básicos sobre o uso da API. Isso gerava atrasos significativos, já que dependíamos da disponibilidade de outras pessoas para entender nosso problema e fornecer uma resposta. Esse processo envolvia explicar o contexto, aguardar que alguém compreendesse a situação e só então encontrar e sugerir uma solução. Todo esse ciclo de espera e comunicação poderia ter sido evitado, ou ao menos reduzido, se houvesse uma documentação de qualidade disponível desde o início.

Maiores dores:

* Não fomos informados previamente de que seria necessário implementar um novo fluxo específico para o 3DS, descobrindo só durante a implementação.
* Não recebemos orientações prévias claras sobre o que deveria ser enviado em cada campo ao iniciar um pagamento com 3DS (por exemplo, não sabíamos o que era o *code* do authenticationInformation), só coseguimos compreender após explicação.
* Enfrentamos diversos transtornos ao seguir as instruções fornecidas e não obter o resultado esperado.
* O SDK de frontend apresentou bugs e não funcionava corretamente.
  * Não havia documentação suficiente sobre a geração do session_id. Os campos necessários para que o session_id fosse gerado corretamente só foram informados via chat.
  * Em relação ao modal do 3DS, não havia informações sobre os métodos que ele utilizava nem sobre como o fluxo deveria ser seguido. Por exemplo, não estava claro que a responsabilidade de fechar o modal era nossa, por meio de um método disponibilizado pelo próprio modal.

A principal dificuldade foi descobrir os requisitos de implementação apenas durante o processo. Cada dúvida levava a uma nova descoberta, que por sua vez gerava mais dúvidas, criando um ciclo contínuo de desenvolvimento às cegas.

| Problema | Tempo até resolver | Link |    |
|----|----|----|----|
| Dúvidas iniciais relacionadas do 3DS | 15d | <https://seazone-fund.slack.com/archives/C07N307SJBF/p1741808590831759> |    |
| Dúvidas sobre campos não documentados da API  | 12d | <https://seazone-fund.slack.com/archives/C07N307SJBF/p1743618365283859> |    |
| Pagamento via cartão de crédito com 3DS | 3d | <https://seazone-fund.slack.com/archives/C07N307SJBF/p1744635699044929> |    |
| Expiração de Pagamentos Pendentes | 1d | <https://seazone-fund.slack.com/archives/C07N307SJBF/p1745328224762899> |    |
| Adição de novo fluxo | 14d | <https://seazone-fund.slack.com/archives/C07N307SJBF/p1745349727222129> |    |
| Dúvida fechar modal do 3ds da tuna | 7d | <https://seazone-fund.slack.com/archives/C07N307SJBF/p1748357569415739> |    |
| Transações pendentes no cartão | 1d | <https://seazone-fund.slack.com/archives/C07N307SJBF/p1745435384689969> |    |
| Exibição da Modal de desafio 3DS | 1d | <https://seazone-fund.slack.com/archives/C07N307SJBF/p1745586438535829> |    |
| Contexto de mensagem de erro | 6d (e contando) | <https://seazone-fund.slack.com/archives/C07N307SJBF/p1751311041456139> |    |