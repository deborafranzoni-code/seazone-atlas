<!-- title: [Estruturação] Módulo de Parceiros | url: https://outline.seazone.com.br/doc/estruturacao-modulo-de-parceiros-jmfmbWMniX | area: Tecnologia -->

# [Estruturação] Módulo de Parceiros

# Anotações

* Ver com o Ody sobre a comissão dos parceiros (2% do que o imóvel fatura, durante o primeiro ano de contrato, por imóvel. Após isso ele para de receber)
* Pode ter Anfitrião que também é parceiros
* Daniel que cadastra os novos parceiros
  * Tela de cadastro de novos parceiros para o daniel
* Botão solicitar visita:
  * Parceiros ve a disponibilidade do imóvel para pedir visita à ele (talvez um calendar como o do proprietário)

# Planilhas e Forms:

* Formulário de cadastro do parceiro: <https://docs.google.com/forms/d/e/1FAIpQLSeGUznf3evM0kREJCzD2O0sHnsWorU8PK1xx72kIUagIZ4KqQ/viewform>
* Formulário de indicação de imóvel: <https://docs.google.com/forms/d/e/1FAIpQLScYfMT9D1mxREJouGmJrtteP9MBs3HZ-uHrn58b-NSgrfXdHg/viewform?entry.696660100=Cristina+Batistella>
* Planilha de Acompanhamento (Leads/Comissões): <https://docs.google.com/spreadsheets/d/1xePNTJIckWJebb1KgnhLwwWZGjgkuLmFq_NOFebBNZo/edit#gid=1341045361>
* Formulário de Solicitação de Pagamento: <https://docs.google.com/forms/d/e/1FAIpQLScvwEBoA5uRJnmLZ5W68Tbz7WIlTRMhVuoLeIIXucDK8-o4MQ/viewform>

# Processos

### Parceiros faz Indicação imóvel

* \

# Telas:

> Rascunhos das telas:
>
> [rascunho telas de parceiros](https://miro.com/app/board/uXjVOCAni08=/?invite_link_id=726372376913)

### 1. **Tela de comissões || [Planilha - Comissões](https://docs.google.com/spreadsheets/d/1xePNTJIckWJebb1KgnhLwwWZGjgkuLmFq_NOFebBNZo/edit#gid=1341045361)**

* Data Fechamento (mes/ano): Data de fechamento da comissão. É o mês de referência da comissão.
* Comissão total: Tudo que recebeu desde o primeiro imóvel (o que já recebeu+o que tem a receber)
* Data de Ganho: Data de quando o imóvel entrou para seazone (usar campo start_contract_date)
* Data vencimento: Até quando ele vai receber comissão por aquele imóvel
* Corretagem = Comissão

  > 2% do que o imóvel fatura, durante o primeiro ano de contrato, por imóvel. Após isso (data vencimento) ele para de receber daquele imóvel
* Precisa ver quanto que o imóvel está faturando.
* **Protótipo que foi combinado**

  ![Untitled](%5BEstruturac%CC%A7a%CC%83o%5D%20Mo%CC%81dulo%20de%20Parceiros%208f21199f9dd7414ebb0d42e7400721f7/Untitled.png)

  ![Untitled](%5BEstruturac%CC%A7a%CC%83o%5D%20Mo%CC%81dulo%20de%20Parceiros%208f21199f9dd7414ebb0d42e7400721f7/Untitled%201.png)


---

Com botão de solicitar pagamento

* Página solicitar pagamento
  * Ao solicitar o pagamento, a linha no Grid ficaria verde, indicando que ele já recebeu a comissão referentes aquele(s) mês(es)
  * Form: Solicitar de pagamento
    * Possibilitar assinatura pelo Sapron || Por enquanto anexar o PDF

### 2. Tela de Solicitar pagamento || [Form - Solicitar Pagamento](https://docs.google.com/forms/d/e/1FAIpQLScvwEBoA5uRJnmLZ5W68Tbz7WIlTRMhVuoLeIIXucDK8-o4MQ/formResponse)

> **Descrição da página:** Preencha para solicitar o pagamento das suas comissões da Seazone conforme a sua planilha de acompanhamento.

Pedidos realizados até o dia 10 serão pagos no dia 15 do mesmo mês. Pedidos realizados após o dia 10 serão pagos até o dia 15 do mês subsequente.

Enviando previamente o recibo ou NF para [administrativo@seazone.com.br](mailto:administrativo@seazone.com.br), o pagamento ocorrerá mais rapidamente.

> \

**Campos do formulário de solicitar pagamento:**

> Front já irá trazer as informações do parceiro preenchidas (Email, Nome, CPF/CNPJ

* Email
* Nome do Parceiro
* CPF/CNPJ

  Se for CNPJ mostra essas opções também: `is_email_set`
  - [ ]  Enviei a NF por e-mail para [administrativo@seazone.com.br](mailto:administrativo@seazone.com.br)
  - [ ]  Ainda não enviei, mas estou ciente de que o pagamento só será realizado após o envio
* Valor do resgate
* Possui Chave PIX?
  * Sim.
    * Nome do Favorecido
    * Tipo de chave PIX: CPF/CNPJ, Número de celular, Email, Aleatória
    * Chave PIX
  * Não, preciso receber por transferência bancária normal.
    * Caso não tenha PIX, abre campos para informar os dados bancários:
      * Nome do Favorecido
      * CPF/CNPJ do Favorecido
      * nº banco - banco (ex.: 260 - NU Pagamento IP) → Puxar da tabela `financial_banks`
      * Agência
      * Número da conta (com dígito)
      * Tipo de conta (corrente, poupança)
      * \
* **\[ Botão Solicitar pagamento \]**
  * O que ocorre agora? Para quem/onde é enviado essas informações?

### 3. **Tela Leads || [Planilha - Leads](https://docs.google.com/spreadsheets/d/1xePNTJIckWJebb1KgnhLwwWZGjgkuLmFq_NOFebBNZo/edit#gid=1753693502)**

* **Info. visualizada pelos parceiros:**
  * **O que são leads?**

    > Indicações que o parceiros faz. Cada **proprietário** indicado é um **lead. Lead = Proprietário**
  * **Quais dessas colunas são de fato importante para o Partner (principais colunas que ele olha, mais relevantes)?**

    > Imóvel, Proprietário (nome do lead), Endereço, Data indicação,
    >
    > > Info. que precisa ter, mas não precisa ficar visível: Ultimo update, Data de ganho, Motivo de perdido
  * **Tem alguma Coluna que podemos tirar? Qual?**
  * **Quais são os Status?**

    > **Ganho, Perdido, Em andamento**
  * **Quais são as Etapas?**

    > É o estágio de negociação que este lead (proprietário) está. (vai haver mudanças nos proceços da operação. Essa info vem do pipedrive.
  * **O que é "Nome do Lead"?**

    > Nome do proprietário
  * **De que é o endereço?**

    > Endereço do imóvel
  * **O que é a Data de Indicação?**

    > Data que o parceiro indicou aquele proprietário
  * **O que é Último update? Update de que?**

    > Data do último contato que o pessoal do comercial fez com o Proprietário pra saber sobre a negociação.
  * **O que é data de perdido? É a data em que o Status do imóvel mudou para perdido?**

    > Data da última negociação e que por algum motivo a negociação falhou, por algum dos motivos abaixo.
  * **Quais são os motivos de perda?**

    > Não é qualificado Não tem interesse Sem urgência/tempo Concorrência Sem resposta O imóvel não está disponível para locação Contato inválido Sem conexão Taxa de implantação Prefere administrar sozinho Região não atendida Somente de divulgação/geração de reserva Não quer adequar o imóvel Não cocorda com nosso modelo de trabalho Prefere aluguel anual Duplicado/Erro Outros
  * O que é comissão a vista? Quais as opções? **→** **Não é mais usado, não incluir**

  **Processos:**
  * **Como o parceiro usa essa tela? Pra que ela serve?**

    > Essa tela é para os parceiros **acompanhar as indicações** que ele fez, **acompanhar o status da negociação**.
  * **Como essas informações são atualizas? De onde vem? Quem/o que as atualiza?**

    > Essas planilhas são atualizadas pelo **Pipedrive**. Operação preenche o form de **Indicação de Imóvel**, essa indicação chega ao Pipedrive que manda para a [planilha](https://docs.google.com/spreadsheets/d/1xePNTJIckWJebb1KgnhLwwWZGjgkuLmFq_NOFebBNZo/edit#gid=1753693502). Ai pelas atualizações no Pipedrive ela é passada para esta planilha.
    * Pipedrive
      * Pipedrive tem sua API propria: <https://developers.pipedrive.com/docs/api/v1>
      * Pipedrive é um software PMS utilizado pelo comercial/vendas

      
      1. Ao criar um novo lead ele entra no filtro de PRE-VENDA || Etapa = Pre-venda
      2. Ao saber que o imovel está disponivel para passar para VENDA || Etapa = Venda
  * **Os parceiros usam mais o celular ou computador? Por onde preferem visualizar essas informações? Celular ou PC?**

    > Aguardar pesquisa que o Daniel irá fazer....

OBS: Pode acontecer de o parceiro ficar alguns meses sem indicar

* **Protótipo combinado:**

  ![Untitled](%5BEstruturac%CC%A7a%CC%83o%5D%20Mo%CC%81dulo%20de%20Parceiros%208f21199f9dd7414ebb0d42e7400721f7/Untitled%202.png)

### 4. **Página de Indicação || [Form - Indicação parceiro com contrato](https://docs.google.com/forms/d/e/1FAIpQLScYfMT9D1mxREJouGmJrtteP9MBs3HZ-uHrn58b-NSgrfXdHg/viewform)**

### 5. Tela de cadastro do Parceiro || [Form - Incluir Parceiro](https://docs.google.com/forms/d/e/1FAIpQLSeGUznf3evM0kREJCzD2O0sHnsWorU8PK1xx72kIUagIZ4KqQ/viewform)

* **Cadastro do Parceiro (quem faz é a operação, partner não se auto-cadastra)**