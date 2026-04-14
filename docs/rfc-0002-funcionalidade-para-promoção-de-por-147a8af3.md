<!-- title: [RFC-0002] Funcionalidade para Promoção De-Por | url: https://outline.seazone.com.br/doc/rfc-0002-funcionalidade-para-promocao-de-por-OQHAO33nPC | area: Tecnologia -->

# [RFC-0002] Funcionalidade para Promoção De-Por

**REQUISITOS:**

* Deve haver flag para ativar/desativar a promoção De/Por
  * A promoção vai ter um período pre-definido em que estará ativa: Starts_at, Ends_at
* QUALQUER PESSOA deve ser capaz de configurar/ativar essa promoção.
* Deve ser possível especificar quais imóveis vão exibir o De/Por
* (opcional) Deve ser possível buscar por imóveis em promoção de black-friday\nEx.: Mesmos imóveis com a promoção ativa devem receber a badge "Blue Friday 2025"
* Regras para Exibir De/Por:
  * Flag deve estar Ativa e data_atual estar entre o starts_at e ends_at da promoção
  * O preço atual DEVE SER MENOR que o preço histórico.
* (opcional) Poder adicionar várias promoções De-Por com para conseguir mostrar na Home as Promoções Ativas, Finalizadas e que vão iniciar.\nEx.: "Descontaço em Cabanas, inicia em XX horas", Tipo da Promoção: "De_Por", Lista de Imóveis: \[ \] >> Vai exibir o texto/promoção De_Por para aquele imóvel devido a promoção na Cabanas.


**PREMISSAS:**

* Uma promoção possui uma duração pre-definida (tem Início e Fim)
* Cálculo do desconto com base no PREÇO HISTÓRICO (vamos precisar salvá-lo)

\n**ALTERNATIVAS DESCARTADAS**

* Utilização de cupom para oferecer desconto De-Por por baixo dos panos: Vamos ter problemas em combinar o desconto De/Por com desconto de cupom; Ou até mesmo, deixar de oferecer cupom para imóveis que já possuem De/Por
* Oferecer possibilidade de um "Admin" informar quantos % de desconto estará ofertado: Isso poderá causar uma divergência no cálculo de preços pois dependemos diretamente da Stays para calcular o valor final. Atualmente não é possível informar para Stays qual o valor ela deve salvar como valor final da reserva. Logo, na hora de salvar na Stays, vai acabar sendo salvo um valor diferente (calculado pela Stays).

\n**IDEIAS PARA O FUTURO**

* Módulo de promoções: Ser possível criar campanhas promocionais no site & Cupons.


### Anotações

* Retornar `active_promos[{}]` por imóvel. Retornando a promoção que está ativa para exibição de **badge** pelo frontend.