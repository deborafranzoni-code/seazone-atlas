<!-- title: SLA Gestão de Contas Financeiro | url: https://outline.seazone.com.br/doc/sla-gestao-de-contas-financeiro-0mbbStQIS7 | area: Administrativo Financeiro -->

# SLA Gestão de Contas Financeiro

A gestão de contas necessita da interface com o time do financeiro para realizar o pagamento das despesas do proprietário, registra-las no Sapron e anexar os comprovantes de pagamento no Drive. Tal interface vai colaborar com o processo de transparência para o proprietário, para que ele tenha a certeza que o serviço está sendo executado conforme contratou.



|    |    |    |    |    |
|:---|:---|:---|:---|:---|
| **Tarefa** | **Tempo** | **Realização** | **Responsável** | **Interface** |
| Verificar contas a pagar | Diariamente | [Planilha](https://docs.google.com/spreadsheets/d/12jFzCTYAISO2xVBFcC6YkDehBmR2m5ymYGcwQnU3fhA/edit#gid=131740303) | Drieli | GC e Financeiro |
| Efetuar pagamento e baixar comprovantes. | Conforme vencimento | Banco | Drieli | Apenas financeiro |
| Anexar comprovante na pasta | Após pagamento da conta | [Drive](https://drive.google.com/drive/folders/1q5WZVou7FhvpvZZ2WOU3QMa3vrQFgbuW) | Drieli | Apenas financeiro |
| Acessar infos para emissão de NF | Dia 10 de cada mês | [Lista de NFs](https://docs.google.com/spreadsheets/d/1UBBagU3HUYD00v8xVFEE6c5e_iR3PT453lbwluclBlk/edit#gid=1962662412) | Gabriel Almeida | GC e Financeiro |
| Emissão de NFs | Dia 10 de cada mês | Site da Prefeitura | Gabriel Almeida | Apenas financeiro |
| Registro de NF | Após a emissão | Sapron | Gabriel Almeida | Apenas financeiro |
| Anexar NFs nas pastas | Após registro da NF no Sapron | Pasta de cada prop no [Drive](https://drive.google.com/drive/folders/1q5WZVou7FhvpvZZ2WOU3QMa3vrQFgbuW?usp=drive_link) | Gabriel Almeida | Apenas financeiro |
| Categorizar Admsys conforme padrão Gestão de Contas. | Após importação do extrato | Admsys Seazone Serviços | Roberto Ianes | Apenas financeiro |
| Reuniões de acompanhamento. | Quinzenal | Meet | GC e Financeiro | GC e Financeiro |
| Registrar despesas | Após pagamento da conta | Sapron | Lander | Apenas financeiro |


# Processo Financeiro

[Link do processo no Lucid](https://lucid.app/lucidchart/be92371a-7e7c-4cb2-85d3-b9dc86d7269f/edit?invitationId=inv_2d8823f9-b931-42f8-9e08-00a1f014a82f&referringApp=slack&page=n484MyZE4Z_l#)


## Passo a passo para execução do processo:

* Passo 1 - Pagamento de Contas\n\n
  * Acessar a planilha de [Contas a Pagar](https://docs.google.com/spreadsheets/d/12jFzCTYAISO2xVBFcC6YkDehBmR2m5ymYGcwQnU3fhA/edit#gid=131740303), acessar o boleto correspondente ao vencimento e efetuar o pagamento.\n\n
* Passo 2 - Registro no Sapron\n\n
  * Após efetuar o pagamento, logar no Sapron com as credenciais do **Administrativo** ([Vault](https://vault.sapron.com.br/ui/vault/secrets))
  * Clicar no menu **Despesas** para iniciar o registro do pagamento efetuado:

  ![](/api/attachments.redirect?id=68d3c991-8877-45c9-8e5e-277b1f301264)

  \
  * Clicar em **Nova despesa** para realizar o registro das informações necessárias:

  ![](/api/attachments.redirect?id=9f0e832d-61ed-44e2-9443-85f093b32869)

  \
  * Preencher todos os campos obrigatórios:

  ![](/api/attachments.redirect?id=244cab99-8f12-461f-a20b-94f3034f4eee)
  * No campo **Motivo**, selecionar o tipo de conta que foi paga dentre as opções com a nomenclatura **Gestão de Contas:**

  ![](/api/attachments.redirect?id=66bbd3d1-728e-4707-bae6-dd7bee8c7b7d)

  \
  * Caso não identifique o motivo correspondente, marque a opção **Despesas Recorrentes,** utilize o campo **Descrição da despesa** para detalhar qual conta foi paga e não estava nos Motivos, e solicite ao responsável pela Gestão de Contas que realize a inclusão para o próximo lançamento:

  ![](/api/attachments.redirect?id=a6a8a894-bf75-42f2-9a8c-bdb0d1779fa1)

  \
  * Anexar o pdf do boleto no campo **Upload dos arquivos do recibo** e o comprovante de pagamento em **Upload dos arquivos da manutenção**.

  ![](/api/attachments.redirect?id=3cb9728d-9278-446f-9ff7-656fea2f47de)

  \
  * Finalizar o registro da despesa do imóvel inserindo a data de vencimento da despesa, selecione **"Proprietário"** no campo **Quem paga** e clique em **Salvar**:\n\n

  ![](/api/attachments.redirect?id=589617b6-18c2-4e0d-9ede-cd6091fc15fd)
* Passo 3 - Salvar arquivos no Drive\n\n
  * Acessar a pasta de proprietários no [Drive](https://drive.google.com/drive/u/0/folders/1-7DPC9EVnuoZRZjrFZ2N3NyauHpSmEVK);
  * Clicar na pasta do [proprietário](https://drive.google.com/drive/folders/1q5WZVou7FhvpvZZ2WOU3QMa3vrQFgbuW) correspondente (estará identificado na planilha de [contas a pagar](https://docs.google.com/spreadsheets/d/12jFzCTYAISO2xVBFcC6YkDehBmR2m5ymYGcwQnU3fhA/edit#gid=131740303), coluna C);
  * Acessar a pasta de **Comprovantes de Pagamento;**
  * Criar nova pasta com o mês de pagamento se não existir, e anexar o arquivo.\n\n

  ![](/api/attachments.redirect?id=d5c111b0-2db5-48f0-bb19-7d288772d1a1)
* Passo 4 - Emissão de NFs\n\n

  No dia 25 de cada mês, será enviado no canal **gestão-de-contas** do Slack uma notificação via fluxo de trabalho para a emissão das notas fiscais, correspondentes ao serviço da Gestão de Contas, seguindo os passos:
  * Acessar a [planilha](https://docs.google.com/spreadsheets/d/1Q1dV4hkJqfKABiPMsYXY5sLYVVq8l1NyBBediuWqApE/edit#gid=505531135) com os dados para emissão no mês;
  * Realizar a emissão da NF no site da prefeitura de SC;
  * Lançar as NFs emitidas no Sapron, seguindo o Passo 2;
  * Acessar a pasta de notas fiscais no [Drive](https://drive.google.com/drive/u/0/folders/1tceVOG_VJvUns46FlznsUC6hadHChT7k) da Seazone Serviços;
  * Acessar ou criar pasta com o mês da emissão;
  * Acessar ou criar pasta de Gestão de Contas;
  * Anexar as NFs emitidas separadas por proprietário;
  * Dar os checks na [planilha](https://docs.google.com/spreadsheets/d/1Q1dV4hkJqfKABiPMsYXY5sLYVVq8l1NyBBediuWqApE/edit#gid=505531135), colunas J / L / M.
* Passo 5 - Categorização do Admsys

  Após realizar a importação do extrato bancário no Admsys da Seazone Serviços, é necessário seguir o padrão de categorização abaixo para que o [Admsys da Gestão de Contas](https://docs.google.com/spreadsheets/d/1mbs7eTz95e1LV5qCavYlxjfJqjgPPhnj84BseDNLpzY/edit#gid=1506782190) seja atualizado:
  * Centro de Custo - **Gestão de Contas**
  * Categoria - **Adiantamento de despesas de clientes**
  * Apto - **inserir o código do imóvel**