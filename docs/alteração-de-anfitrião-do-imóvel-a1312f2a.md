<!-- title: Alteração de Anfitrião do Imóvel | url: https://outline.seazone.com.br/doc/alteracao-de-anfitriao-do-imovel-utnLxfuD7N | area: Tecnologia -->

# Alteração de Anfitrião do Imóvel

**Contexto**

Nesse caso, o requerente reclamou que o imóvel não estava aparecendo na conta do anfitrião que ele havia(teoricamente) sido alocado. Feita a investigação, ficou constatado que o imóvel estava com o anfitrião errado, nesse caso, com a própria Seazone, quando deveria estar com o anfitrião Guilherme Nuremberg.

**Possível Solução**


1. Achar o imóvel na tabela **property_property**. Ex: VST023 - Imagem ilustrativa abaixo:

   ![Untitled](Alterac%CC%A7a%CC%83o%20de%20Anfitria%CC%83o%20do%20Imo%CC%81vel%20a03bf52e3f004fff936074d9107a90ad/Untitled.png)

   Observação: Sempre pegar o registro com status = 'Active':

   ![Untitled](Alterac%CC%A7a%CC%83o%20de%20Anfitria%CC%83o%20do%20Imo%CC%81vel%20a03bf52e3f004fff936074d9107a90ad/Untitled%201.png)
2. Verificar o campo **host_id**, clicando na setinha azul:

   ![Untitled](Alterac%CC%A7a%CC%83o%20de%20Anfitria%CC%83o%20do%20Imo%CC%81vel%20a03bf52e3f004fff936074d9107a90ad/Untitled%202.png)

   Verificar se o Anfitrião está correto. Nesse caso, o imóvel deveria estar com o anfitrião Pool Vistas, mas está com a Seazone Serviços LTDA:

   ![Untitled](Alterac%CC%A7a%CC%83o%20de%20Anfitria%CC%83o%20do%20Imo%CC%81vel%20a03bf52e3f004fff936074d9107a90ad/Untitled%203.png)
3. Tendo em mãos um identificador único(ID, Email, CPF, CNPJ), pesquise pelo novo anfitrião na tabela account_user:

   ![Untitled](Alterac%CC%A7a%CC%83o%20de%20Anfitria%CC%83o%20do%20Imo%CC%81vel%20a03bf52e3f004fff936074d9107a90ad/Untitled%204.png)

   Nesse caso, utilizamos o email.

   Colete o id do usuário e guarde a informação:

   ![Untitled](Alterac%CC%A7a%CC%83o%20de%20Anfitria%CC%83o%20do%20Imo%CC%81vel%20a03bf52e3f004fff936074d9107a90ad/Untitled%205.png)
4. Procure na tabela **account_host**, buscando pelo campo **user_id**(Dado que obtemos no passo anterior).

   ![Untitled](Alterac%CC%A7a%CC%83o%20de%20Anfitria%CC%83o%20do%20Imo%CC%81vel%20a03bf52e3f004fff936074d9107a90ad/Untitled%206.png)

   Copie o ID do registro na tabela **account_host**

   ![Untitled](Alterac%CC%A7a%CC%83o%20de%20Anfitria%CC%83o%20do%20Imo%CC%81vel%20a03bf52e3f004fff936074d9107a90ad/Untitled%207.png)
5. Volte ao registro da propriedade na tabela **property_property** e no campo **host_id**, cole o dado adquirido na etapa anterior(Da tabela **account_host**).

   ![Untitled](Alterac%CC%A7a%CC%83o%20de%20Anfitria%CC%83o%20do%20Imo%CC%81vel%20a03bf52e3f004fff936074d9107a90ad/Untitled%208.png)

Feito! Ao seguir todos esses passos, o problema deve se resolver.

**Entenda mais  esse contexto lendo a conversa  do suporte:**

**Algumas informações importantes para conseguir realizar o suporte:**

* Ter acesso ao banco de dados de produção (**sapron_production**)
* Ter posse de um dado que identifique o host que irá ser inserido.(Email, CPF, CNPJ, id)
* Ter o código do imóvel.