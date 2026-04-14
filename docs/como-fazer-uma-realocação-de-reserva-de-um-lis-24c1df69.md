<!-- title: Como fazer uma realocação de reserva - De um lis | url: https://outline.seazone.com.br/doc/como-fazer-uma-realocacao-de-reserva-de-um-lis-VAyp5pxCse | area: Tecnologia -->

# Como fazer uma realocação de reserva - De um lis

**Observações**

* Necessário ter acesso ao banco de dados de produção do Sapron(**sapron_production**)

**Contexto**

O que aconteceu no caso desse suporte, foi que o cliente(Seazone Serviços) pediu uma realocação de uma reserva do imóvel ILC1413 para o ILC4202 pelo Sapron, porém, mesmo depois do tempo de atualização das reservas, a realocação não aconteceu.

**Algumas informações importantes para conseguir realizar o suporte:**

* Ter o código da reserva.
* Ter o código do imóvel para onde a alocação será feita.

**Possível Solução**

Um possível solução para este problema, seria a realocação manual pelo banco de dados, que pode ser executada seguindo os passos abaixo:


1. Procurar pelo imóvel para o qual a reserva será realocada(tabela `property_property`) e copie o **id** do registro. Ex: ILC4202

   ![Untitled](Como%20fazer%20uma%20realocac%CC%A7a%CC%83o%20de%20reserva%20-%20De%20um%20lis%20299559345ecc478c825eb042ad5ff2af/Untitled.png)
2. Fazer uma pesquisa na tabela `reservation_reservation`(Banco de dados **sapron_production**), utilizando o parâmetro "`code`"(Código da reserva). Imagem de exemplo abaixo:

   ![Untitled](Como%20fazer%20uma%20realocac%CC%A7a%CC%83o%20de%20reserva%20-%20De%20um%20lis%20299559345ecc478c825eb042ad5ff2af/Untitled%201.png)
3. Logo após, vá até o campo `listing_id` e clique no botão azul (foreign_key) para ir até o registro dele na tabela `reservation_listing` .

   ![Untitled](Como%20fazer%20uma%20realocac%CC%A7a%CC%83o%20de%20reserva%20-%20De%20um%20lis%20299559345ecc478c825eb042ad5ff2af/Untitled%202.png)
   * Em seguida, procure pelo campo `ota_id` e anote/memorize a informação dele em algum lugar.

     ![Untitled](Como%20fazer%20uma%20realocac%CC%A7a%CC%83o%20de%20reserva%20-%20De%20um%20lis%20299559345ecc478c825eb042ad5ff2af/Untitled%203.png)
4. Vá até a tabela `reservation_listing` e faça uma query pelo campo `property_id` (Id do imóvel que pesquisamos no primeiro passo, na tabela `property_property`) + campo `ota_id` com o valor do campo `ota_id` que guardamos no 3 passo.

   ![Untitled](Como%20fazer%20uma%20realocac%CC%A7a%CC%83o%20de%20reserva%20-%20De%20um%20lis%20299559345ecc478c825eb042ad5ff2af/Untitled%204.png)

   Copie o id do registro.
5. Vá até a tabela `reservation_reservation`, no registro da reserva, e cole o id copiado no passo 4 na coluna `listing_id`.

   ![Untitled](Como%20fazer%20uma%20realocac%CC%A7a%CC%83o%20de%20reserva%20-%20De%20um%20lis%20299559345ecc478c825eb042ad5ff2af/Untitled%205.png)

**Entenda mais  esse contexto lendo a conversa  do suporte:**