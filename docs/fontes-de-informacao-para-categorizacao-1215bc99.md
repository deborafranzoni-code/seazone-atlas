<!-- title: Fontes de Informação para Categorização | url: https://outline.seazone.com.br/doc/fontes-de-informacao-para-categorizacao-ypI5GS7wG7 | area: Administrativo Financeiro -->

# Fontes de Informação para Categorização

![](/api/attachments.redirect?id=d55ecee0-eee4-495d-8723-84fd727cad8a)

📁

# Fontes de Informação para Categorização


\
O processo de categorização frequentemente envolve uma busca detalhada pelas informações relacionadas às saídas. Dependendo do tipo de pagamento, essas informações podem estar dispersas em diferentes fontes. Nesta seção, vamos detalhar todos os locais onde podemos encontrar os dados necessários sobre as saídas e sua categorização.

Controle CPG

A planilha [Controle CPG](https://docs.google.com/spreadsheets/d/12jFzCTYAISO2xVBFcC6YkDehBmR2m5ymYGcwQnU3fhA/edit#gid=1561465343) é a planilha que compila todas contas a pagar, bem como as contas pagas, com informações de data, valor, solicitante, empresas envolvidas e todas outras informações necessárias para saber tudo sobre uma determinada saída. As abas de interesse para categorizações são:

* PGTO_REQ:
  * Nem todas as transações são previsíveis ou regulares. Muitas delas são reembolsos relacionados a viagens ou outros tipos de pagamentos que variam de acordo com as circunstâncias. Esta aba consolida as contas pagas e as contas a pagar que foram solicitadas através do formulário pelos colaboradores.\nNesta aba, são listados os valores, data da requisição, data do pagamento, link da nota fiscal ou documento comprobatório, documento de cobrança, nome do solicitante, diretor responsável, empresa e banco. Além dessas informações, na aba PGTP_REQ temos colunas para Setor, CC, Categoria e Subcategoria. Essa "categorização", que não pode ser considerada categorização propriamente dita, uma vez que ainda não foi integrada à planilha AdmSys, vem de duas fontes principais:\n
    * Quando o solicitante requisita um pagamento, ele indica um Setor e um CC. No entanto, essa categorização nem sempre é precisa, já que os colaboradores podem não estar familiarizados com o plano de contas.
    * Durante o processo de aprovação do pagamento, o CFO recategoriza a saída de acordo com a visão correta do setor financeiro e do setor responsável pela saída. Por ser uma entrada manual, é importante verificar se esta categorização é adequada, faz sentido e está alinhada com o Plano de Contas.
* PGTO_PARCELAS:
  * Nessa aba, são listados os pagamentos de parcelas no caso das compras parceladas.
* PGTO_RECORRENTE:
  * Nesta aba, são listados os pagamentos que ocorrem com mais frequência e regularidade. Como exemplo, temos o pagamento da contabilidade terceirizada, agências de marketing, aluguéis de escritório, impostos, entre outros.
* PGTO_COMERCIAL:
  * Nesta aba, são listados os pagamentos variáveis para colaboradores. Devido à sua natureza variável, o controle desses valores é mantido em uma aba específica, separada dos salários. Normalmente, os colaboradores envolvidos são do setor Comercial.
* PGTO_PARCEIROS:
  * Os parceiros atuam como corretores para a Seazone, buscando compradores para os Spots. Quando uma venda é concluída, uma parte da comissão é destinada a eles e outra parte para a Seazone. Nesta aba, são listados os pagamentos para parceiros.
* PGTO_GESTAO_CONTAS:
  * A Seazone efetua pagamentos de contas de luz, energia elétrica, internet e outras despesas em nome dos clientes. Quando é feito o repasse, esses valores adiantados pela Seazone são deduzidos do montante total do repasse devido. O registro desses pagamentos adiantados é feito na aba PGTO_GESTAO_CONTAS.
* PGTO_PEOPLE:
  * Esta aba lista os pagamentos de rescisão, gratificação e bônus por indicação de colaboradores. Em casos de rescisão onde haja valores de metas trimestrais ou variáveis comerciais a receber, os valores também serão listados aqui.
* PGTO_DANOS:
  * Durante as hospedagens, é possível que os hóspedes danifiquem objetos nos imóveis. Nestes casos, os hóspedes são cobrados pelo valor do dano. A Seazone recebe esse valor e repassa para os proprietários. Nesta aba, são organizados todos os repasses de danos para proprietários.
* PGTO_REC_STO:
  * Cada imóvel possui um código composto por letras e números. STO são as letras iniciais dos códigos de imóveis do Resort Santo Agostinho. Lá os hóspedes consome e pagam posteriormente para a Seazone. Quando esses hóspedes pagam o valor, repassamos ao proprietário desse imóvel. Por ser uma operação especial e diferente das demais, utilizamos um controle separado. Na aba "PGTO_REC_STO", registramos os valores repassados aos proprietários desse imóvel.
* DADOS_COLABORADORES:
  * Nesta aba, são consolidados os dados de todos os colaboradores, passados e presentes, da Seazone. As informações-chave para categorização estão nas colunas "Matrícula", "Ativo", "Setor" e "SubsubÁrea". A coluna "Ativo" indica o status atual do colaborador; quando inativo, o colaborador deixou a empresa ou teve alterações em cargo, setor, nível ou step. Assim, pode haver múltiplas entradas para o mesmo colaborador, com apenas uma ativa. As entradas inativas registram todo o histórico do colaborador na empresa, incluindo promoções, mudanças de setor e progressão na carreira. Nessa aba não há informações específicas de pagamentos, mas funciona como um banco de dados dentro do [Controle CPG](https://docs.google.com/spreadsheets/d/12jFzCTYAISO2xVBFcC6YkDehBmR2m5ymYGcwQnU3fhA/edit#gid=1561465343) que alimenta outras abas com informações sobre colaboradores.
* DADOS_PROP:
  * Nesta aba, encontram-se as informações sobre imóveis e proprietários. Para a categorização dos repasses, as colunas fundamentais são "Nome Correntista", "Imóvel" e "Proprietário".

💡

O procedimento padrão estabelece que todos os pagamentos devem ser registrados no [Controle CPG](https://docs.google.com/spreadsheets/d/12jFzCTYAISO2xVBFcC6YkDehBmR2m5ymYGcwQnU3fhA/edit#gid=1561465343) . Caso isso não tenha ocorrido, pode indicar que o processo não foi seguido corretamente ou que o pagamento foi considerado uma urgência.

Google [Drive](https://drive.google.com/drive/folders/19PIBFcOD4k6EsTirQVU6SQpRHnSQxBT6) Adm/Fin Seazone

Em alguns casos, a categorização pode ser mais complexa. Podemos notar discrepâncias de valor ou data entre um pagamento registrado no extrato e seu correspondente no [Controle CPG](https://docs.google.com/spreadsheets/d/12jFzCTYAISO2xVBFcC6YkDehBmR2m5ymYGcwQnU3fhA/edit#gid=1561465343) , ou podemos não encontrar o registro de um pagamento específico no [Controle CPG](https://docs.google.com/spreadsheets/d/12jFzCTYAISO2xVBFcC6YkDehBmR2m5ymYGcwQnU3fhA/edit#gid=1561465343) . Algumas vezes, as solicitações de pagamento são feitas por meio de slack ou e-mail, não sendo registradas no [Controle CPG](https://docs.google.com/spreadsheets/d/12jFzCTYAISO2xVBFcC6YkDehBmR2m5ymYGcwQnU3fhA/edit#gid=1561465343) . Nessas situações, o [Drive](https://drive.google.com/drive/folders/19PIBFcOD4k6EsTirQVU6SQpRHnSQxBT6) do setor Administrativo e Financeiro se mostra muito útil, já que os comprovantes de pagamento devem estar registrados lá, independentemente da forma como foram solicitados.

Ao realizar uma busca por valor ou data no [Drive](https://drive.google.com/drive/folders/19PIBFcOD4k6EsTirQVU6SQpRHnSQxBT6), é possível encontrar um PDF do comprovante correspondente ao pagamento no extrato. Ao acessar a pasta onde esse PDF está armazenado, é possível obter mais detalhes sobre o pagamento em questão.


Na prática, buscamos informações no [Drive](https://drive.google.com/drive/folders/19PIBFcOD4k6EsTirQVU6SQpRHnSQxBT6) conforme os passos a seguir:

 ![](/api/attachments.redirect?id=8b65410c-9588-4091-8f6c-11e7b19ea2f5)


1. No campo de busca, normalmente o valor que consta no extrato é o bastante para encontrar os comprovantes. Quando isso não é possível por conta da formatação do número ou por outro motivo, a data no extrato pode ser usada na busca. A combinação das duas informações pode ser usada na busca também.
2. O comprovante possui nome padronizado, com informações de data e favorecido. Uma vez localizado, é muito importante verificar o arquivo para ter certeza que as informações ali presentes são compatíveis com o as informações de extrato que estão no AdmSys.
3. Uma vez que se tem certeza de que aquele comprovante realmente se trata daquele pagamento específico no extrato, verificamos a pasta onde esse arquivo está armazenado.


 ![](/api/attachments.redirect?id=70aef8d2-4d46-4bc8-a0fe-dd276b6bd527)



4. O nome da pasta onde o comprovante está armazenado pode indicar onde encontrar mais informações sobre o pagamento. Se estiver na pasta de Requisições, geralmente corresponde a uma entrada no [Controle CPG](https://docs.google.com/spreadsheets/d/12jFzCTYAISO2xVBFcC6YkDehBmR2m5ymYGcwQnU3fhA/edit#gid=1561465343) . Porém, em alguns casos, o comprovante pode estar em uma pasta sem uma correspondência no [Controle CPG](https://docs.google.com/spreadsheets/d/12jFzCTYAISO2xVBFcC6YkDehBmR2m5ymYGcwQnU3fhA/edit#gid=1561465343) . Nessas situações, é recomendável perguntar sobre a origem do pagamento no Slack para o responsável pelo pagamento. No entanto, mesmo sem uma entrada correspondente, o nome da pasta já oferece uma pista sobre a natureza do pagamento. Este processo auxilia na categorização e no entendimento das transações.

Pedido de Pagamento / Respostas ao formulário

Todos os pedidos de pagamentos feitos através do formulário são registrados na planilha [Pedido de pagamento (Atualizado)](https://docs.google.com/spreadsheets/d/1arWMv0rL3giOxsJRj0TtVomoUHqN3-YzWmLfi6obbjc/edit?resourcekey#gid=1876907782). Essa planilha serve como fonte de informações acessória à aba "PGTO_REQ" do [Controle CPG](https://docs.google.com/spreadsheets/d/12jFzCTYAISO2xVBFcC6YkDehBmR2m5ymYGcwQnU3fhA/edit#gid=1561465343) . Nessa aba, todas as solicitações de pagamento são detalhadas, mesmo quando recusadas. Esse recurso é particularmente útil em casos de solicitações inicialmente negadas, seguidas por uma nova solicitação via e-mail ou Slack. Na planilha de pedidos de pagamento, é possível visualizar as informações iniciais fornecidas pelo solicitante, que podem servir como uma referência adicional para esclarecer a natureza de um pagamento específico.

SAPRON

O [SAPRON](https://sapron.com.br/login) é o sistema que organiza e consolida todos os dados relevantes sobre imóveis, repasses, proprietários, anfitriões e outros elementos relacionados ao processo de hospedagem. Ele permite verificar os valores de repasse devidos aos proprietários e anfitriões. É muito importante acessá-lo com cautela, limitando-se à visualização de informações para garantir a integridade dos dados.

Lotes de Pagamentos

Os repasses para proprietários são geralmente realizados no início do mês, totalizando mais de 1000 transferências de repasse para proprietários por mês. Cada transferência é feita por imóvel, o que significa que se diferentes propriedades do mesmo proprietário geraram repasses, serão feitas transferências separadas para cada uma delas.

Transferências feitas por lote envolvem pagamentos a vários favorecidos de uma vez só. Para gerenciar esses pagamentos, é criado um arquivo contendo todas as informações de pagamento. Normalmente, os repasses para proprietários e anfitriões são realizados por lote. O arquivo organizacional está disponível no Drive, na pasta " [01 - Baskets Enviadas](https://drive.google.com/drive/folders/1Zb2-iXvVWqdH9epvT498qr5yWgPgXL1C)". Ao verificar esse arquivo, é possível relacionar os valores e os nomes nos extratos com os respectivos imóveis listados no arquivo de lote de transferência.

Slack

Quando a busca por informações sobre as saídas de recursos nos locais padrão ([Controle CPG](https://docs.google.com/spreadsheets/d/12jFzCTYAISO2xVBFcC6YkDehBmR2m5ymYGcwQnU3fhA/edit#gid=1561465343) e [Drive](https://drive.google.com/drive/folders/19PIBFcOD4k6EsTirQVU6SQpRHnSQxBT6)) não é bem-sucedida, é possível utilizar a função de busca do Slack, inserindo valores, datas e descrições do extrato. Caso a discussão sobre o pagamento tenha ocorrido em um canal aberto no Slack, a busca revelará essa discussão. Além disso, também é possível questionar os solicitantes ou pessoas chave dos setores através do Slack sobre pagamentos específicos para obter um entendimento mais completo do contexto dos pagamentos.

Categorizações Anteriores

É possível consultar o histórico de categorizações anteriores, especialmente aquelas mais recentes, para obter orientação sobre a categorização adequada ou compreender a natureza de um pagamento específico. No entanto, não é adequado depender exclusivamente desse recurso, pois a percepção da categorização pode evoluir com o tempo. Desde janeiro de 2024, houve uma alteração no padrão de categorização, portanto, é recomendável consultar apenas o histórico a partir desse período.