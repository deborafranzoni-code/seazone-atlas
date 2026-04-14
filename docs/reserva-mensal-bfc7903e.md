<!-- title: Reserva mensal | url: https://outline.seazone.com.br/doc/reserva-mensal-jhZYnaHaYr | area: Tecnologia -->

# Reserva mensal

### Orçamento mensal

### Geração do contrato e inserção da reserva

Gera o contrato de reserva mensal e a insere no Multicalendar a reserva mensal.

**Regras:**

* A reserva mensal deve ter uma limpeza a cada mês (a cada 30d) Essa limpeza deverá aparecer na página de Controle do Anfitrião daquela propriedade.
* A cleaning_fee cobrada, é multiplicada pela quantidade de meses que a reserva abrange. Ex.: Se abrange 2 meses, são duas cleaning_fee; Se abrange 2 meses e meio, são três cleaning_fee.
* Não deve passar de 90d

**OBS:**

> *A OTA de uma reserva mensal, sempre será a Contrato. Ao inserir na tabela a reserva, deve ser feito uma busca na tabela reservation_listing, informando o property_id e a ota_id = 7 (contrato), e pegar o ID desse listing para linkar a reserva no campo listing_id.*

### **Contrato de reserva mensal**

* Os dados vindos do Input, deverão ser preenchidos no [template HTML](https://sapron-templates.s3.us-west-2.amazonaws.com/monthly_reservation/contract/ContratodeAluguelMensal.html), preenchendo os respectivos campos que estão com `{ }`
* Quando preenchido todos os campos, deve ser gerado um arquivo em PDF com todos os campos devidamente preenchidos.
* Após inserida a reserva mensal, o contrato também poderá ser baixada pelo modal de dados da reserva no Multicalendar.

### **Inserção da reserva mensal**

Ao inserir a reserva mensal, é gerado e baixado para a máquina do usuário o contrato de reserva mensal, e a reserva é inserida no BD e deverá aparecer no Multicalendar também.

A reserva mensal deverá ser divida (quebrada) em **N** reservas menores de até 30d cada, onde há um principal e as partes seguintes são **extensões** da anterior.

A cada 30d há uma limpeza que aparecerá como um card na página de Controle do Anfitrião.

* **Funcionamento da página de Geração de Contrato e Inserção de Reserva Mensal**
  * A inserção da reserva mensal acontecerá quando o usuário clicar em "Confirmar/finalizar" no modal lateral onde há informações do orçamento.
  * Ao clicar neste botão é aberto o modal para criação da reserva mensal no imóvel desejado. Veja **[aqui](https://miro.com/app/board/uXjVOzxl-hA=/?share_link_id=260509461664)** o rascunho do modal.

    > OBS: Para conseguir prosseguir para a inserção da reserva, no modal de orçamento mensal deverá ter apenas um imóvel selecionado, e este imóvel será o escolhido para inserção da reserva. Caso tenha mais de um, deve ser exibido um toast.
  * O front já deverá trazer alguns dados do modal anterior para essa nova etapa/modal, como: Imóvel, Data Check-in e Check-out, Valores (seção de resumo do modal).
  * Os demais campos serão preenchidos no modal.
  * Todas essas informações deverão ser enviadas para a API.
  * O contrato da reserva mensal retornado deverá ser baixado para o dispositivo do usuário.
  * O contrato da reserva mensal também deverá ser exibido no modal de "Dados da reserva" no Multicalendar, para quando a reserva for uma reserva mensal. Ele deverá ficar como um item mas que será apenas um link clicável que ao clicar é baixado o contrato. O contrato é retornado no GET dessa mesma API. Haverá um campo retornado pela API informando se ela é mensal, ou não (`is_monthly`)
  * **Testes Cypress Implementados**
    * Ao avançar para o modal de inserir reserva mensal, as informações preenchidas anteriormente deve ser puxada para este modal: imóvel, check-in/out e valores.
    * Ao inserir uma reserva mensal deve ser baixado para a máquina o contrato da reserva mensal retornado pela API
    * Ao inserir uma reserva mensal ela deve aparecer no multicalendar.
    * No modal de dados da reserva, para quando for uma reserva mensal deverá ser exibido o contrato dela neste modal em formato de link que ao clicar nele é baixado o contrato para a máquina do usuário..