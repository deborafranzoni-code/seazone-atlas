<!-- title: Não aparece organização de cama para o imóvel | url: https://outline.seazone.com.br/doc/nao-aparece-organizacao-de-cama-para-o-imovel-kym2gqoqza | area: Tecnologia -->

# Não aparece organização de cama para o imóvel

**Contexto**

Neste suporte os emails de organização de cama não estavam sendo enviados. (Pelo fato de o suporte ser antigo, não consegui achar mais informações sobre ele)

**Possível Solução**


1. Achar o imóvel:

   **🟢** Ter em mãos o código do imóvel. Ex: JBV343

   **🟢** Logo após, acessar a tabela **property_property** e fazer uma busca através do código do imóvel(code) e pelo status, que deve ser 'Active'.

   ![Untitled](Na%CC%83o%20aparece%20organizac%CC%A7a%CC%83o%20de%20cama%20para%20o%20imo%CC%81vel%20b2a6a7e67eb44dafae8ada098d6fb3af/Untitled.png)

   **🟢**Localizar o campo **category_location_id**, clicar na seta azul e localizar o campo **location_id**. Como nos exemplos abaixo **⬇️**

**Entenda mais  esse contexto lendo a conversa  do suporte:**

Vídeo explicativo :<https://drive.google.com/file/d/1GgtCrpPM_baavIYW4p22yJn5FW94LI0H/view>

**Algumas informações importantes para conseguir realizar o suporte:**

* Ter acesso ao banco de dados de **produção.**
* Ter o código do imóvel