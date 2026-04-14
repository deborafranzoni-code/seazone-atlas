<!-- title: Q2 2025 - Delivery + Discovery | url: https://outline.seazone.com.br/doc/q2-2025-delivery-discovery-ouJE09m12f | area: Tecnologia -->

# Q2 2025 - Delivery + Discovery

# \nDelivery

## Checkout - Está em andamento

* Resolver o problema de não conseguir trocar o meio de pagamento 
* Resolver o problema de baixa conversão no checkout

  \

## Teste com recuperação de Carrinho

**Hoje:** Atendimento entra em contato 1 por 1 com hóspedes que abandonaram a reserva. 

**Primeira iteração:** Queremos automatizar esse processo, todo abandono de carrinho é contatado imediatamente assim que a reserva é expirada. Manteremos exatamente a mesma mensagem que o atendimento envia atualmente. A idéia inicial é somente automatizar a recuperação de carrinho.

**Queremos medir:** Quantas pessoas receberam a recuperação de carrinho automática e compraram. 

**Segunda Iteração (Junho):** Queremos entender se as pessoas:

* não estão conseguindo comprar (será ofertado um cupom de 10% pelas atendentes)
* ou querem um cupom de 5% para terminarem suas compras (só será oferecido caso a pessoa esteja comprando sem cupom aplicado)

Precisamos entender se conseguimos estatística dessas conversas sobre os cliques nos botões do bot.

Precisamos ainda alinhar com atendimento essa linha de automação.


## Refatoração da Página do Imóvel

Dores dos usuários: Muito texto, muitas amenities, regras de cancelamento antes dos depoimentos, sem avaliação (estrelinha), muito texto para ler nas avaliações, fotos não realistas 

Dores do Bruno: biblioteca de ícones, sempre tem amenities novas 

Dores do atendimento: Usuário não lê as regras de cancelamento e nem as cobranças extras, usuário reserva com pet e não sabe que tem cobranças extras 

 Nossos usuários querem:

→ Entender mais rápido os diferenciais daquele imóvel sem ler textão

→ Avaliações com destaque por limpeza, localização e conforto

→ Nota da propriedade com mais destaque

→ Entender rápido se o imóvel atende às suas necessidades

→ Entender o quão bem aquele imóvel é localizado sem precisar de muito esforço 

[https://www.figma.com/design/SxkaCB56BXCDHHZq1oaWOG/Seazone-Site?t=mzlD01i2JJnMQbNy-0](https://www.figma.com/design/SxkaCB56BXCDHHZq1oaWOG/Seazone-Site?t=mzlD01i2JJnMQbNy-0)

A idéia é quebrar o design em pequenos experimentos para serem diluídos nas sprints.


1. Incluir preço da booking e airbnb
2. A forma de mostrar as fotos
3. Destaque para o rating
4. Amenities de forma escalável
5. Maior destaque das localidades no mapa
6. Notas de avaliações 
7. Selos nos imóveis → "Instagramável",  Ideal para casais", "Ideal para home office"
8. Colocar as regras de forma positiva
9. Reels na página do imóvel

# Refatorar exibição de comentários de imóveis

**Dores do hóspede:** Querem conseguir saber como é a limpeza, a localização, o conforto, etc

Pretotipo:

* Vou gerar um json com os comentários classificados por uma LLM para testarmos, a interface está no figma


# Testes AB de conteúdo na nova home (imóveis, cidades)

* Testar mostrar a imagem da propriedade mais bem rankeada
* Testar mostrar cabanas primeiro agora para a temporada de outono e inverno 
* Mover o banner com cupom mais pra baixo na página
* Testar a barra no topo com desconto (a mesma do wallet pro webinar)


# Apresentar preços de outras OTAs

**Dores do hóspede:** Precisar fazer pesquisa de mercado

**Exemplo de teste:** Apresentar o preço de outras OTAs na página de busca com o link do airbnb e da booking (não precisamos de API, o valor é um incremento percentual)

 ![](/api/attachments.redirect?id=49a1dd54-6fbd-4451-9d7d-3d950248874d " =862x340")

Inclui somente mudanças no card da busca - mudanças exclusivas no Front.


## Discovery Q2 2025

### 1. Diferenciação em relação aos nosso competidores


1. **Pesquisar Motivação do Cliente (Alta Prioridade)** 
   * Começar a coletar reviews dos usuários diretamente (não necessariamente exibir no site ainda, mas para ter feedback diario sobre a experiência do hóspede e entender nossa vantagem competitiva)


   * O que exatamente leva os hóspedes a reservar pelo Airbnb/Booking.com em vez da Seazone?
   * Que valor único poderia fazer com que eles trocassem de canal?
     * Explorar meios de pagamento facilitado por exemplo parcelado sem juros
     * Pix com desconto
     * Determinar experimentos para validar as hipóteses
     * Cashback
   * Determinar um segmento tem maior probabilidade de reservar direto
     * :white_check_mark: Salvador está definido como nossa prioridade
     * Acredito que casais seria o segundo
     * Cabanas é outro segmento
     * A idéia é junto com o time de marketing escolher esses segmentos e focar em converter neles em específico
   * Definição de seções que teremos para inserir conteúdo para cada segmento de cliente em nossas landing pages que temos com seleção de propriedades para converter com o segmento (ex: cabanas para casais sem filhos)

   \
2. **Estratégias de aumento de usuários (Alta prioridade)**

   
   1. Estudar programa de referral
   2. Estudar programa de cashback
   3. Estudar parcerias com companhias aéreas para gerar tráfego qualificado
   4. Tráfego orgânico (quick wins)
   5. Tráfego via IA
   6. Divulgações em grupos de facebook para o ano novo



3. **Aumento de ticket (Média prioridade)**

   
   1. Min stays
   2. Diminuição de valores de cupom 
   3. Melhorar implementação Rent Cars
   4. Extensão de reserva (atendimento está oferecendo diretamente quando há oportunidade e está dando certo mas tem dificuldade operacional) - Área do hóspede
   5. Inclusão de taxa pet diretamente pelo site
   6. Oferecer early checkin e late checkout
   7. Estudo de desconto sem cancelamento vs Ticket mais alto com cancelamento grátis
   8. Repetir a booking para cidades selecionadas



4. **Campanhas offline** 
   * QR Code na propriedade com guia turístico + promovendo o site
   * Estudar promover a seazone em aeroportos (spoiler: é muito caro!)



5. Campanhas de retenção (Baixa prioridade)

   
   1. Desconto progressivo conforme estadias repetidas 


**Campanhas de Marketing Importantes que precisamos acertar tráfego + landing page**

* Dia dos namorados
* São João
* Inverno
* Férias escolares


Bonus: Lentidão no site


\

\

\

\