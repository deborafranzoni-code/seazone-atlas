<!-- title: Decolar | url: https://outline.seazone.com.br/doc/decolar-hZpO9Bd8qM | area: Tecnologia -->

# Decolar

* Adicionar a Decolar no chanel manager do SAPRON

  Hoje temos o channel manager que é o serviço que sincroniza reservas da stays com o sapron. Temos algumas condicionais dentro do código que aplica taxas diferentes dependendo da OTA e faz algumas ações. Precisamos incluir a Decolar dentro dessas condicionais.
* Cadastro na tabela de OTAs

  Cadastrar OTA no BD.

  
  1. Como configurar extensões na Decolar?

     A Seazone não consegue editar/alterar nada na Reserva. A Decolar não faz modificações na reserva, em casos assim, o cliente necessita emitir uma nova reserva no site.

     Não conseguimos alterar reservas, então o ideal é que o cliente cancele e emita uma nova, ou a alteração pode ser feita com a gente diretamente e mantemos a reserva como original na OTA ja que a Seazone não pode cancelar essa reserva.

     As políticas de cancelamento do hóspede são definidas por nós, existem 4 opções. Explicadas na seção de RM.
  2. Pedido de Alterações por parte dos hóspedes.

  Após o pagamento o hóspede ainda pode solicitar as seguintes alterações:
  * Data de entrada e saída
  * Quarto
  * Tipo de refeição
  * Hóspedes que irão se hospedar

  Se o hóspede solicitar essas alterações uma equipe de pós-venda da Decolar entrará em contato conosco para tentar conciliar essas alterações. Podemos pedir uma taxa adicional a depender da alteração. Caso a Seazone permita as alterações a reserva em questão é cancelada e é emitida uma nova reserva com as alterações pedidas.

  Portanto, apesar da Seazone não conseguir alterar nada na plataforma da Decolar o hóspede pode solicitar alteração dos itens descritos. Contudo, se confirmado a alteração a reserva será cancelada e outra emitida.
* Adicionar da Decolar os listings na tabela listing

  A princípio o listing é criado automaticamente ao importar a reserva. Podemos fazer um teste, caso o listing não seja criado, fazemos a inserção manual.
* Adicionar a Decolar nos códigos de fechamento Card criado para delivery

  
  1. Como é feito o cálculo do valor liquido da reserva?

  Valor Total (quadrado vermelho) - 15% (quadrado azul | taxa OTA) = Valor Liquido (esse é o valor descontado no cartão virtual da OTA).

  Valor Liquido - taxa de limpeza = Valor Liquido Sem Limpeza

  Valor Liquido Sem Limpeza - Comissão Seazone = Repasse para o proprietário.

  ![Untitled](/api/attachments.redirect?id=214fcf52-b79c-42e9-ac0d-a7cb35773e1a)
* Descobrir como criar o Link do anúncio na Decolar

  Existe um método na tabela Listing que cria os links de acordo com o formato na OTA. O padrão da URL da Decolar é `https://decolar.com/hoteis/h-{id-do-imóvel-na-decolar}`
* Adicionar anúncio da Decolar na página do proprietário && Renderização correta no calendário de reservas da propriedade

  Criar ícones no Front com os ids da Decolar.
* Verificar a renderização correta nas rotas de multicalendar das reservas da decolar
* Adicionar Decolar na rota de Danos de hóspede

  Possibilitar ao time de atendimento e franquias que selecione a plataforma Decolar ao ocorrer um dano durante a reserva do cliente