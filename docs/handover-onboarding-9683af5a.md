<!-- title: Handover > Onboarding | url: https://outline.seazone.com.br/doc/handover-onboarding-OE00R6uWNN | area: Tecnologia -->

# Handover > Onboarding

> ***OBS: Atualmente, o Onboarding e Comercial estão compartilhando do mesmo Login***

> **Permissões:** `Admin, SeazoneOnboarding`
>
> * **Endpoints:**
>   * `/property/handover_details/`
>   * `/property/manager/`
>   * `/owners/`
>   * `/hosts/`
>   * `/address/`

> OBS: Ao preencher o CEP deverá ser feito um request na API ViaCEP para preencher as informações de endereço para facilitar o preenchimento.

* Inicialmente será realizada uma requisição na API `/endpoint/` para obter dados do Pipedrive e economizar tempo de preenchimento do usuário. Ao obter esses dados, seles deverão ser colocados em seus respectivos campos nos formulários de handover.
* Ao buscar por um proprietário, deverá ser exibida uma lista com os proprietários que dão match com o termo pesquisado.
  * Na lista exibida de proprietários, ao clicar sobre um deles, ele será o proprietário selecionado para aquela propriedade
  * Caso o proprietário ainda não exista, ao clicar para inserir um novo e inserí-lo, ele deverá ser atribuído como proprietário da propriedade que está sendo inserida.
  * Inserção de proprietário:
    * POST /address/
    * POST /users/
    * POST /owners/
* Gerar código do imóvel (botão ficará desabilitado no momento até que o gerador fique pronto.
* Anfitrião responsável será um campo de busca onde será possível buscar por um anfitrião já existente para linkar ele com aquela propriedade. Funcionamento semelhante ao seletor de owner. Quando selecionar um anfitirão ele quem será atribuído como anfitrião daquela propriedade.
* Nome do indicador no momento será apenas um campo de texto, não de busca (remover lupa e botão 'Buscar').


---

Há certos campos que vão para a API `/property/handover_details/` e outras que vão ser enviadas para `/property/manager/`.

Porém, ao final do fluxo, quando for realizar o POST para salvar as informações inseridas, primeiro será necessário salvar os dados presentes na API `/property/manager/` pois o ID da propriedade inserida será necessário para a inserção dos dados de Handover>Onboarding na API `/property/handover_details/`

* Inserir propriedade:
  * POST /address/
  * POST /property/manager/
* Inserir Handover Details:
  * POST /property/handover_details/ -> Deve ser informado o property_id inserido anteriormente.

**OBS:** Caso alguma inserção falhe, as seguintes não deverão ser realizadas e as que foram feitas já, deverão ser desfeitas usando os métodos DELETE das respectivas APIs.