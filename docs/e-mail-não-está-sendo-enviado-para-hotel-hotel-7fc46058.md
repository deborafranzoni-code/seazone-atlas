<!-- title: E-mail não está sendo enviado para hotel [hotel  | url: https://outline.seazone.com.br/doc/e-mail-nao-esta-sendo-enviado-para-hotel-hotel-vp6saARN5Q | area: Tecnologia -->

# E-mail não está sendo enviado para hotel [hotel 

**Observações**

**Contexto**


1. \

**Possível Solução**

<https://drive.google.com/file/d/1GgtCrpPM_baavIYW4p22yJn5FW94LI0H/view?usp=sharing>


1. Encontrar o ID do imóvel e category_location_id na tabela `property_property` (Pode ser

   utilizado como parâmetro de busca, o codigo do imóvel).

   ![Untitled](E-mail%20na%CC%83o%20esta%CC%81%20sendo%20enviado%20para%20hotel%20%5Bhotel%20%2006464cf3f7da4dd6b72e71efb0a34215/Untitled.png)

   Encontrar o `category_location_id` e verificar se está com a relação correta

   ![Untitled](E-mail%20na%CC%83o%20esta%CC%81%20sendo%20enviado%20para%20hotel%20%5Bhotel%20%2006464cf3f7da4dd6b72e71efb0a34215/Untitled%201.png)

   Clicar na setinha azul(Para buscar a localização do dado na tabela em que ele está referenciado)

   PS: Nesse caso, o JBV343 está com a localização em JURERÊ (Abreviação JUR), quando na verdade, deveria estar com a localização JBV.
2. Para modificar para a localização correta, é necessário ir nesse mesmo campo `category_location_id` e verificar qual é o código de categoria da relação categoria/localização pelo campo `category_id` (Guarde essa informação).
3. Ir na tabela `property_categorylocation` e pesquisar por um registro que tenha o category_id =

**Entenda mais  esse contexto lendo a conversa  do suporte:**

**Algumas informações importantes para conseguir realizar o suporte:**