<!-- title: [ Blip ] Recuperação de Carrinho | url: https://outline.seazone.com.br/doc/blip-recuperacao-de-carrinho-NYqbwl62EF | area: Tecnologia -->

# [ Blip ] Recuperação de Carrinho

# Objetivo

Este documento tem como objetivo explicar o funcionamento do envio automático de mensagens de recuperação de carrinho no site de reservas. Para um contexto mais abrangente, confira o documento [Recuperação de Carrinho](/doc/recuperacao-de-carrinho-DS64nm4haF).

# Como funciona?

Quando um hóspede faz uma reserva conosco, entramos no processo de pré-reserva. Basicamente, a propriedade escolhida fica reservada e aguardando pagamento por até 30min. Se a reserva não for paga em até 30min, ela será expirada.

A recuperação de carrinho entra nesse processo. A ideia é que, ao expirar uma reserva, automaticamente seja enviada uma mensagem no WhatsApp do hóspede com o objetivo de recuperar aquela venda. Sobre essas mensagens, há duas possibilidades:

* **Com cupom:** Caso a pré-reserva tenha sido feita **com** cupom, a mensagem usará o template *pre_reserva_cancelada*
* **Sem cupom:** Caso a pré-reserva tenha sido sido feita **sem** cupom, a mensagem usará o template *carrinhoabandonado1*

A principal diferença entre os templates citados é que no caso da pré-reserva sem cupom, a mensagem informa ao usuário que ele pode falar com o atendimento para obter um cupom e reservar novamente, dessa vez, com um desconto especial.

Basicamente, a ideia é converter um hóspede que tenha desistido da compra.

# Detalhes técnicos

Em resumo, a nível técnico, isso funciona da seguinte forma. Nosso worker tem uma task para checar e expirar as reservas que não foram pagas em 30min após sua confirmação (`check_reservation_expiration`), cada vez que essa task roda, avaliamos se há feature flag `ff_abandoned_cart_notification` está ativada, caso esteja, triggamos o processo de envio de mensagem.

## Pré requisitos sobre o envio da mensagem

Detalhes técnicos relacionados ao formato de requisições da BLIP podem ser encotrados no documento [Recuperação de Carrinho](/doc/recuperacao-de-carrinho-DS64nm4haF). Porém, existem alguns detalhes extras relacionados a regras de negócio que serão esclarecidos aqui.

Ao ativarmos pela primeira vez essa automatção, tivemos um problema relacionado a mensagens sendo enviadas enquanto o usuário já estava em uma conversa com o atendimento, gerando confusão e incômodo. Perante a esse cenário, surgiu a ideia de que a mensagem só deve ser enviada caso o hóspede não esteja com uma conversa ativa com o atendimento. 

A partir disto, iniciou-se a busca por um meio de saber se o usuário já está conversando com o atendimento antes de triggar a automação. Nesse processo, foi necessário conversar com o suporte da plataforma Blip. Nesse conversa, foi apresentada a solução detalhada na próxima seção.

## Processo de checagem do estado do usuário

Esse processo é pautado nas orientações dadas pela própria BLIP. A ideia aqui é explicá-lo para que futuramente dúvidas sejam sanadas facilmente acessando esse documento.

Atualmente, a BLIP não possui uma requisição específica para verificar diretamente se um usuário está em atendimento humano. No entanto, existe uma alternativa eficaz apresentada por eles: a requisição **Get user state**. Com essa chamada, é possível identificar em que ponto do fluxo o usuário está, utilizando o \`user-identity\` do contato e o \`flow-identifier\` do bot.

### Passo a passo


1. **Obtenção do user-identity:** O user-identity pode ser encontrado no roteador, na aba "Contatos", pela URL do contato ou adicionando \`@wa.gw.msging.net\` após o número do telefone. (Exemplo: \`5543991631304@wa.gw.msging.net\`).
2. **Obtenção do flow-identifier:** O flow-identifier do bot pode ser encontrado nas configurações do bot no Builder. (Exemplo: d887d0fe-a27a-446b-ac35-81886527461f)

   ![](/api/attachments.redirect?id=d4d472b2-489d-4445-b401-e2081fac2d96)

   \
3. **Requisição:** Uso da requisição \`Get user state\` para verificar o estado do usuário. A documentação da BLIP para essa requisição pode ser encontrada aqui: [https://docs.blip.ai/#get-user-state](https://www.google.com/url?q=https://docs.blip.ai/#get-user-state&source=gmail&sa=D&sa=E).
4. **Análise da resposta:** A resposta da requisição indicará em qual bloco do fluxo o usuário se encontra. Caso ele esteja em um bloco de atendimento humano, isso poderá ser identificado pelo campo 

   `resource` da resposta. Segundo orientações da equipe da BLIP e discussões em fóruns da comunidade (consulte a seção de [fontes](https://outline.seazone.com.br/doc/blip-recuperacao-de-carrinho-N7DG2doAtU#h-fontes), se necessário), quando o valor d'e `resource` começa com "desk...", significa que o usuário está em processo de atendimento humano. Exemplo de resposta:

   ```json
   {
       "type": "text/plain",
       "resource": "desk:fa45f794-dd91-4e17-977a-708379a4c...",
       "method": "get",
       "status": "success",
       "id": "e6bfcf67-2cee-4beb-9081-44135de3e51b",
       "from": "postmaster@builder.msging.net/#msging-application-builder-597689fbc-nr7d6",
       "to": "hospedesseazone1@msging.net/!msging-server-847c8846d9-c92b6-6otm57gi",
       "metadata": {
           "traceparent": "00-ab53162a7993431e9c7c655a42f39f10-9cb83ed68b4ba174-01",
           "#command.uri": "lime://hospedesseazone1@msging.net/contexts/5512996050047@wa.gw.msging.net/stateid@d887d0fe-a27a-446b-ac35-81886527461f"
       }
   }
   ```

### Sobre o código

O passo a passo detalhado na seção anterior foi convertido para código e está disponível no arquivo **reservations_api/integration/blip/blip_api.py** dentro do método `has_active_human_support_session`. A ideia é que, a cada checagem de necessidade de envio da mensagem, esse método seja chamado antes, de modo que a mensagem só seja enviada caso o usuário não esteja em uma conversa com o atendimento.

# Fontes


---

<https://community.blip.ai/outros-assuntos-4/como-atraves-da-api-checar-o-fluxo-de-chatbot-que-um-numero-esta-4405>

[https://drive.google.com/file/d/1%5FFkiS-iPHqEINJkVommD7vr%5F4RqN1YhA/view?usp=sharing](https://drive.google.com/file/d/1%5FFkiS-iPHqEINJkVommD7vr%5F4RqN1YhA/view?usp=sharing)