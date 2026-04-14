<!-- title: 6 Protótipo Viabilidade de uso, de construção e | url: https://outline.seazone.com.br/doc/6-prototipo-viabilidade-de-uso-de-construcao-e-HolGf6Wy9a | area: Tecnologia -->

# 6 Protótipo Viabilidade de uso, de construção e

## Jornada do usuário

 ![Frame 1889.png](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%20ad78168ee5154cb39c6af4fa058faec6/Frame_1889.png)

[https://www.figma.com/file/3w5tZcalçahbhpI09p0C2o9OvEu/Danos-de-hospede?type=design&node-id=1002%3A856&mode=design&t=XPsR4UbmaA3Gnuhw-1](https://www.figma.com/file/3w5tZhbhpI09p0C2o9OvEu/Danos-de-hospede?type=design&node-id=1002%3A856&mode=design&t=XPsR4UbmaA3Gnuhw-1)

## Solução Ideal

**[FIGMA](https://www.figma.com/file/3w5tZhbhpI09p0C2o9OvEu/Danos-de-hospede?type=design&node-id=629%3A172&mode=design&t=ZuSJvMiKzKAnlUDt-1)**

## 1 - Rotas

Para todos os usuários (Anfitrião, atendimento e financeiro) deve aparecer a rota: **Danos de hóspede**, no menu lateral desk ou menu inferior no mobile, onde todos poderão acessar as etapas de danos e realizar a busca.

 ![Captura de tela de 2023-04-18 10-51-09.png](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%20ad78168ee5154cb39c6af4fa058faec6/Captura_de_tela_de_2023-04-18_10-51-09.png)

Para o usuário anfitrião, além da rota no menu lateral ele poderá acessar a página de inserir danos através da rota de controle, no card de check-out, botão de "Danos de hóspede". Atualmente o botão redireciona para um formulário que deve ser substituído.

 ![Captura de tela de 2023-04-18 10-56-52.png](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%20ad78168ee5154cb39c6af4fa058faec6/Captura_de_tela_de_2023-04-18_10-56-52.png)

## 2 - Tela Inicial


Esta rota deve conter uma barra inicial de busca com os seguintes campos: **-Busca por Imóvel:** `input string` : Usuário digita as letras iniciais e aparece o select com as propriedades. Para o usuário Anfitrião, deve aparecer apenas os imóveis que estão sob sua competência. Para os demais usuários deve aparecer todos os imóveis. **-Busca por Status:** `select string` : Usuário seleciona o status que deseja buscar São os status: `Tratativa passou para o atendimento || Atendimento verificou pendências na validação de informações || Anfitrião finalizou as pendências || Cobrança solicitada pelo atendimento || Cobrança em disputa com o hóspede || Cobrança pendente, ainda em tratativa || Tratativa finalizada. Aguardando pagamento || Atendimento realizou todas as tratativas porém não obteve sucesso || Pagamento recebido, encaminhado pelo financeiro || Dano cobrado. Repasse realizado ao dono do reembolso.`Os status são provenientes das etapas de preenchimento do processo de danos. **-Busca por Período:** `select | datapicker | Data` : Usuário seleciona pelo período aproximado da *data de checkout* inserida no formulário de danos de hóspede preenchido pelo anfitrião **-Busca por Reembolso Repassado:** `select | boolean` : Usuário filtra se o pagamento foi pago ou não pelo financeiro ao dono do reembolso. `Sim || Não` -**-Busca por Etapa:** `select string` : Usuário seleciona o etapa que está preenchida de e pode verificar as que lhe compete preencher. São as etapas:  `Detalhes do dano || Histórico e tratativa de cobrança || Reembolso do dano` **-Resultado da busca:** Deve aparecer todos os resultados de acordo com filtro utilizado (GET formulário_de_danos), com um botão de Selecionar ao lado do dano listado.

 ![Captura de tela de 2023-04-18 11-03-46.png](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%20ad78168ee5154cb39c6af4fa058faec6/Captura_de_tela_de_2023-04-18_11-03-46.png)

Após clicar em Buscar, deve aparecer a seguinte tabela com o botão de selecionar o processo do dano na linha referente ao dano buscado de acordo com os filtros setados:

 ![Captura de tela de 2023-04-19 09-45-59.png](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%20ad78168ee5154cb39c6af4fa058faec6/Captura_de_tela_de_2023-04-19_09-45-59.png)

Para os usuários Anfitrião e Atendimento, a tela inicial deve conter ainda:

**Inserir novo dano:** `h2` título da seção **+ Adicionar:** `button` Botão que redireciona para o formulário de Danos do hóspede

 ![Captura de tela de 2023-04-19 09-53-01.png](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%20ad78168ee5154cb39c6af4fa058faec6/Captura_de_tela_de_2023-04-19_09-53-01.png)

Após clicar em +Adicionar deverá abrir uma barra lateral com as seguintes etapas:


1. Detalhes do dano: Deve ser preenchido pelo anfitrião e atendimento (com opção de editar) e visualizado pelos demais usuários (sem opção de editar)
2. Histórico e tratativas de cobrança:  Deve ser preenchido pelo Atendimento (com opção de editar) e visualizado pelos demais usuários (sem opção de editar)
3. Reembolso do dano: Deve ser preenchido pelo Financeiro e visualizado pelos demais usuários
4. Status final do histórico: O status final deve ser setado como `default` de acordo com cada ação que os usuários envolvidos preenchem ou selecionam no decorrer do processo. Para cada estado alterado devemos guardar a data de alteração. Para melhor compreensão visualize o fluxograma de jornada do usuário. Os stikys em verde sinalizam quando o status final deve ser alterado.

As mudanças de status final da etapa do Anfitrião é a seguinte:

Assim que o anfitrião finalizar o preenchimento de Detalhes do dano e clicar em 'Adicionar Dados' o status final deve ser alterado para:

**Tratativa passou para o atendimento.**

As mudanças de status final da etapa do Atendimento são as seguintes:

SE o atendimento verifica que há pendências na validação de evidências o status final deve ser alterado para:

**Atendimento verificou pendências na validação de informações.**

SE o anfitrião sinaliza que as pendências foram resolvidas, o status final deve ser alterado para:

**Anfitrião finalizou as pendências**

SE o atendimento seleciona 'Solicitado', o status final deve ser alterado para:

**Cobrança solicitada pelo atendimento.**

SE o atendimento seleciona 'Disputa', o status final deve ser alterado para:

**Cobrança em disputa com o hóspede**

SE o atendimento seleciona 'Pendente', o status final deve ser alterado para:

**Cobrança pendente. Ainda em tratativa.**

SE o atendimento seleciona 'à pagar', o status final deve ser alterado para:

**Tratativa finalizada. Aguardando pagamento**

SE o atendimento seleciona 'Finalizado sem sucesso', o status final deve ser alterado para:

**Atendimento realizou todas as tratativas, porém não obteve sucesso na cobrança.**

SE o atendimento seleciona 'Pago', o status final deve ser alterado para:

**Pagamento recebido, encaminhado para o financeiro**

As cores das etapas devem ser inicialmente em cores neutras (indicando que a etapa ainda não foi incluída/finalizada). Conforme as etapas avançam e são preenchidas elas devem mudar para uma cor que indique que a etapa foi finalizada.

O status final deve ser verde.

 ![Captura de tela de 2023-04-19 10-34-39.png](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%20ad78168ee5154cb39c6af4fa058faec6/Captura_de_tela_de_2023-04-19_10-34-39.png)

## 3 - Fluxo

### **Etapa 1 - Detalhes do dano: Formulário Inserir Danos**

Esta etapa deve ser preenchida pelo Anfitrião ou Atendimento e visualizada pelos demais usuários (financeiro e onboarding).

O formulário que deve ser preenchido contém os seguintes dados:

**As palavras em negrito** correspondem as `labels || título`  do formulário

**Danos do hóspede:** `h1`: Título do formulário da página

**Conciliar Dano:** `h2` : Título da primeira seção do formulário. Nesta seção o anfitrião deverá buscar a reserva a qual se refere o dano, para que alguns dados necessários durante o contato sejam preenchidos pelo banco de dados.

Deverá ser feito um GET no endpoint `reservation` e o resultado deverá ser filtrado de acordo as opções:

**Imóvel:** `input string` : Usuário digita o código do imóvel que deseja buscar. Os anfitriões devem ter acesso somente aos imóveis que estão sob sua competência. **Nome do Hóspede :** `input string` : Usuário digita o nome do hóspede para buscar **Data de check-in:** `select datapicker Data` : Usuário seleciona a data de check-in para buscar **Data de check-out:** `select datapicker Data` : Usuário seleciona a data de check-out para buscar **Plataforma:** `select string` : Usuário seleciona a plataforma de origem da reserva para buscar **Buscar:** `button submit` : Botão no final desta seção que permite realizar a busca.

O resultado deve aparecer em formato de grid com as seguintes colunas:

 ![Captura de tela de 2023-04-19 13-19-32.png](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%20ad78168ee5154cb39c6af4fa058faec6/Captura_de_tela_de_2023-04-19_13-19-32.png)

O resultado deve aparecer em formato de grid com as seguintes colunas:

* Código do imóvel
* Nome do hóspede
* Plataforma
* Check-in
* Check-out

Ao lado de cada linha do resultado deve conter:

**Selecionar:** `button` : Ao clicar neste botão os seguintes dados devem aparecer preenchidos pelo DB

 ![Captura de tela de 2023-04-19 13-23-14.png](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%20ad78168ee5154cb39c6af4fa058faec6/Captura_de_tela_de_2023-04-19_13-23-14.png)

Após selecionar a reserva que se refere ao dano devem aparecer as seguintes informações, seguida de inputs de formulário:

**Imóvel**: `string` : Preenchido pelo DB **Nome do hóspede:** `string` : Preenchido pelo DB **Plataforma:** `string` : Preenchido pelo DB **Data de checkout:** `string` : Preenchido pelo DB SE a plataforma referente a reserva do dano for Airbnb, deverá aparecer um Warning abaixo da informação com a seguinte mensagem: Condicional 1: A data de registro da ocorrência < 14 dias a partir da data de checkout `warning string` : Atenção! O Atendimento tem até o dia DD/MM/YYYY para solicitar o pedido de reembolso com seguro pela plataforma. ONDE DD/MM/YYYY = data de checkout + 14 Condicional 2: A data de registro da ocorrência > 14 dias a partir da data de checkout `warning string` : Atenção! O prazo para realizar o pedido de reembolso com seguro pela plataforma já expirou! O Atendimento prosseguirá com a cobrança sem o respaldo do Aircover, sem garantia de sucesso!

**Descreva o ocorrido:** `input string` : Usuário descreve o dano ou multa ocorrido

 ![Captura de tela de 2023-04-20 15-06-24.png](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%20ad78168ee5154cb39c6af4fa058faec6/Captura_de_tela_de_2023-04-20_15-06-24.png)

 ![Captura de tela de 2023-04-20 15-06-38.png](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%20ad78168ee5154cb39c6af4fa058faec6/Captura_de_tela_de_2023-04-20_15-06-38.png)

**Tipo de problema:** `select string` : Usuário seleciona o tipo de problema ocorrido, com as seguintes opções:

🛌🏻 Enxoval 📺 Danos a itens (ex: móveis, eletrodomésticos, utensílios, banheiro) 💥 Extravio de item 🪟 Danos a Propriedade (ex: janela, porta, parede) 🗳️ Pendências (multa, restaurante)

**ATENÇÃO:** Para cada Tipo de problema o formulário deve conter dados específicos a categoria do problema, conforme descrito abaixo:

🛌🏻 Enxoval: **Qual item do enxoval foi danificado/extraviado?**: `select string` : Usuário deve selecionar a peça do enxoval danificado, com as seguintes opções:

* Toalha
* Rosto
* Piso
* Fronha
* Lençol Solteiro
* Lençol Casal
* Lençol Queen
* Lençol King
* Edredom Solteiro
* Edredom Casal
* Edredom Queen
* Edredom King
* Manta
* Capa Edredom Solteiro
* Capa Edredom Casal
* Capa Edredom Queen
* Capa Edredom King
* Colcha Solteiro
* Colcha Casal
* Colcha Antiga Solteiro
* Colcha Antiga Casal
* Colcha Queen
* Capacho

**Quantidade:** `input number` : Usuário deve inserir a quantidade de itens danificados

**Outro:** `input string` : Usuário tem a opção de inserir outro item que não está contemplado no select

SE o Tipo de problema selecionado for estes abaixo, ambos devem contem os inputs que estão na sequência:

📺 Danos a itens (ex: móveis, eletrodomésticos, utensílios, banheiro) `||` 💥 Extravio de item

**Classifique o dano:** `select string` : Usuário deve selecionar a categoria do dano causado a itens no imóvel, com as seguintes opções:

* Móveis (mesa, sofá, cama, guarda roupa...)
* Eletrodomésticos (TV, ar condicionado, torradeira...)
* Utensílios (chave, copo, talher, panela...)
* Banheiro (chuveiro, vaso, torneira...)

SE a categoria do Danos a itens for Móveis (mesa, sofá, cama, guarda roupa...):

**Qual móvel foi danificado?:** `select string` : Usuário deve selecionar uma das seguintes opções:

* Sofá
* Cama
* Mesa
* Guarda Roupa
* Balcão
* Cadeira

**Outro:** `input string` : Usuário tem a opção de inserir outro móvel que não está incluído nesta lista.

SE a categoria do Danos a itens for Eletrodomésticos (TV, ar condicionado, torradeira...):

**Qual eletrodoméstico foi danificado?**: `select string` : Usuário deve selecionar uma das seguintes opções:

* TV
* Ar condicionado
* Torradeira
* Geladeira
* Fogão
* Chaleira elétrica
* Secador de cabelo

**Outro:** `input string` : Usuário tem a opção de inserir outro eletrodoméstico que não está incluído nesta lista.

SE a categoria do Danos a itens for Utensílios (chave, copo, talher, panela...):

**Qual utensílio foi danificado?** `select string` : Usuário deve selecionar uma das seguintes opções:

* Copo
* Xícara
* Talher
* Taça
* Panela
* Chaves
* Prato

**Outro:** `input string` : Usuário tem a opção de inserir outro utensílio que não está incluído nesta lista. **Quantidade:** `input number` : Usuário digita a quantidade de utensílios danificados

SE a categoria do Danos a itens for Banheiro (chuveiro, vaso, torneira...):

**Qual item do Banheiro foi danificado?:** `select string` : Usuário deve selecionar uma das seguintes opções:

* Chuveiro
* Vaso sanitário
* Torneira
* Pia
* Espelho
* Saboneteira

  **Outro:** `input string` : Usuário tem a opção de inserir outro utensílio que não está incluído nesta lista. **Quantidade:** `input number` : Usuário digita a quantidade de utensílios danificados

🪟 Danos a Propriedade (ex: janela, porta, parede)

**Classifique o dano a propriedade:** `select string` : Usuário deve selecionar a categoria do dano causado a propriedade, com as seguintes opções:

* Janela
* Porta
* Parede
* Chão
* Teto

**Outro:** `input string` : Usuário tem a opção de inserir outro que não está incluído nesta lista.

🗳️ Pendências (multa, restaurante)

**Classifique a pendência:** `select string` : Usuário deve selecionar a categoria da pendência, com as seguintes opções:

* Multa Barulho
* Multa Estacionamento
* Taxa Limpeza
* Multa Desrespeito às regras da casa
* Pendência pagamento de consumos no Resort

**Outro:** `input string` : Usuário tem a opção de inserir outro que não está incluído nesta lista.

**ATENÇÃO:** Todas as categorias de Tipo de problema devem conter os seguintes inputs:

**O que precisa ser feito:** `input select` : Usuário seleciona o que precisa ser feito com o item danificado, com as seguintes opções:

* Repor item
* Conserto
* Limpeza
* Contratar serviço terceirizado
* Cobrar Pendência

**Evidências:** `input Download file` : Usuário poderá clicar ou arrastar um documento ou imagem com as evidências do ocorrido. `placeholder`: Clique ou arraste para fazer o upload **Valor:** `input number` : Usuário deverá colocar o valor do item danificado segundo o orçamento ou compra realizada. SE o tipo de problema for Enxoval, o valor deve vir pré preenchido de acordo com os valores padrão da Seazone.

 ![WhatsApp Image 2023-04-20 at 15.33.36.jpeg](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%20ad78168ee5154cb39c6af4fa058faec6/WhatsApp_Image_2023-04-20_at_15.33.36.jpeg)

Colcha Antiga Solteiro: R$81,29 Colcha Antiga Casal: R$93,05 Colcha Queen: R$98,69 Capacho: R$66,01

**Link do orçamento:** `input string` : Usuário deverá inserir o link do orçamento **Orçamento/Nota fiscal:** `input Download file` : Usuário poderá clicar ou arrastar um documento ou imagem com orçamento realizado ou nota fiscal da compra. `placeholder`: Clique ou arraste para fazer o upload **Observações:** `input string` : Usuário insere observações sobre o item danificado que achar relevante

**Adicionar:** `button submit` : Botão para adicionar o item inserido. Após clicar neste botão, o formulário deve ser limpo e o item inserido deve ser criado logo abaixo, com todas as informações inseridas, possibilitando que seja adicionado mais de um item por Tipo de problema, e podendo visualizar uma listagem de todos os itens incluídos que devem ser cobrados.

Abaixo do formulário de Detalhes do Dano, deve aparecer a seguinte tabela:

SE o anfitrião não cobrou o dano do hóspede aparece a seguinte tabela:

**Resumo de danos lançados :** `h2` : Título da seção

A tabela deve conter as seguintes colunas:

**Tipo de Dano:** `string` : Preenchido pelo DB **Classificação:** `string` : Preenchido pelo DB **Item:** `string` : Preenchido pelo DB **Quantidade:** `string` : Preenchido pelo DB **O que precisa ser feito?:** `string` : Preenchido pelo DB **Nota fiscal ou comprovante:** `Docfile` : Link apara acesso do comprovante upado no preenchimento do dano **Dono do reembolso: A informação de Dono do reembolso só irá aparecer quando o atendimento setar o dono do reembolso na etapa de "Histórico e tratativa de cobrança"**

**Valor:** `string` : Preenchido pelo DB. Valor unitário do item danificado **Valor total:** `string` : Preenchido pelo DB: Valor total da soma de itens danificados

**Adicionar dados**: `button submmit` **Editar dados:** `button submmit` : Caso o anfitrião precise editar os dados inseridos

Colcha Solteiro R$ 81,29

Colcha Casal R$ 93,05

Colcha Solteiro R$ 81,29

Colcha Casal R$ 93,05

**Resumo de danos quando o anfitrião não realizou a cobrança:**

 ![Tabela.png](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%20ad78168ee5154cb39c6af4fa058faec6/Tabela.png)

### **Etapa 2 - Histórico e tratativas de cobrança: Formulário Inserir Dados de tratativas de cobrança**

Esta etapa deve ser preenchida pelo Atendimento e visualizada pelos demais usuários (Financeiro, anfitrião e onboarding).

**ATENÇÃO:** Na tela de visualização do Atendimento, deve conter um botão de 'Editar dados' permitindo que o atendimento possa incluir o histórico de tratativas de cobrança e trazendo os demais dados preenchidos anteriormente.

O formulário que deve ser preenchido contém os seguintes dados:

**As palavras em negrito** correspondem as `labels`  do formulário

**Histórico e tratativas de cobrança :** `h1` : Título do formulário da página

Os seguintes dados devem aparecer preenchidos pelo DB:

**Nome do Hóspede :** `string` : Nome completo do titular da reserva **Anfitrião responsável pelo imóvel :** `string` : Nome completo do anfitrião responsável pelo imóvel **Data de check-in:** `string` : Data de check-in no imóvel **Data de check-out:** `string` : Data de check-out no imóvel **Valor total:** `number` : Valor total do(s) dano(s) inserido pelo anfitrião no formulário Danos do hóspede **Plataforma:** `string` : Plataforma pela qual a reserva foi consolidada **Código de reserva:** `string` : Código da reserva do Sapron **Telefone:** `string` : Telefone para contato de cobrança do hóspede

Abaixo destes dados, deve aparecer a seguinte tabela:

**Resumo de danos lançados :** `h2` : Título da seção

A tabela deve conter as seguintes colunas:

**Tipo de Dano:** `string` : Preenchido pelo DB **Classificação:** `string` : Preenchido pelo DB **Item:** `string` : Preenchido pelo DB **Quantidade:** `string` : Preenchido pelo DB **O que precisa ser feito?:** `string` : Preenchido pelo DB **Nota fiscal ou comprovante:** `Docfile` : Link apara acesso do comprovante upado no preenchimento do dano **Dono do reembolso:** `select string` : o atendimento deve sinalizar o dono do reembolso, dentre as seguintes opções: Proprietário Seazone As linhas da tabela devem ser organizadas de forma que os donos de reembolso 'Proprietário' e 'Seazone' fiquem agrupados;

**Valor:** `string` : Preenchido pelo DB. Valor unitário do item danificado **Valor total:** `string` : Preenchido pelo DB: Valor total da soma de itens danificados DE ACORDO COM O DONO DO REEMBOLSO

Na sequência destes dados para consulta deve conter o seguinte formulário:

**Validação de evidências e orçamento** : `h2` : Título da seção **Evidências e orçamentos validados**: `label` | `boolean radio button` : Sim || Não

**Quais informações estão faltando**: `input string` : o atendimento deve descrever quais evidências precisam de verificação e novos documentos ou fotos.

SE o atendimento verificar existem pendências, o anfitrião deverá receber um popup em sua tela inicial, informando que há pendências na tratativa de danos, conforme imagem abaixo:

 ![Anfitrião - Página Inicial(1).png](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%20ad78168ee5154cb39c6af4fa058faec6/Anfitrio_-_Pgina_Inicial(1).png)

Ao clicar em Visualizar pendências, o anfitrião deve ser redirecionado para a página de Danos de Hóspede, com o Status pré selecionado com a opção: `Atendimento verificou pendências na validação de informações`. Devemos mostrar no resultado somente as pendências referentes ao id daquele anfitrião.

 ![Captura de tela de 2023-04-20 15-32-47.png](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%20ad78168ee5154cb39c6af4fa058faec6/Captura_de_tela_de_2023-04-20_15-32-47.png)

O anfitrião deve sinalizar que as pendências estão resolvidas, na tela de histórico e tratativa de cobrança, no botão 'Pendências resolvidas'. Após clicar no botão o status final do processo será atualizado para **Anfitrião finalizou as pendências**:  e o atendimento poderá filtrar na página inicial por esta opção, verificando que o anfitrião já upou as evidências que faltavam.

**Copiar texto para envio de cobrança:** Opção de copiar para área de transferência um modelo de texto para o atendimento encaminhar para a cobrança do hóspede com os dados da reserva e danos já preenchidos:

[Modelos de Script de Cobrança – Time de Atendimento.pdf](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%20ad78168ee5154cb39c6af4fa058faec6/Modelos_de_Script_de_Cobrana__Time_de_Atendimento.pdf)

**Código Aircover:** `input string` : Usuário deve inserir o código da plataforma quando for o caso **Valor recebido:** `input number` : Usuário deve inserir o valor recebido referente ao pagamento **Upload do comprovante:** `input Download file` : Usuário poderá clicar ou arrastar um documento ou imagem do pagamento realizado. `placeholder`: Clique ou arraste para fazer o upload **Status:** `select string` : Usuário deve atualizar a medida que avança o processo um dos seguintes status:

* Solicitado
* Disputa
* Pago
* Finalizado sem sucesso
* Pendente

**Informar proprietário:** `boolean` : Usuário deve selecionar Sim ou Não para que possamos enviar/informar a informação de danos para tela do proprietário

**Histórico da data de contato:** `input datapicker Data` : Usuário deve inserir as datas referentes as datas de contato com o hóspede para realizar a cobrança. Neste campo deverá ser possível inserir mais de uma data (com um botão de '+' ao lado do input), de forma que as datas fiquem registradas para consulta posterior. Ao lado de cada data deve conter o campo **História** `input string` onde o usuário deve descrever brevemente o que foi realizado naquela data.

**Adicionar dados:** `button submit` : Botão para adicionar os dados inseridos. Após clicar neste botão, os dados devem ser disponibilizados para os demais usuários (anfitrião e financeiro), e um botão de **Editar dados** deve ser criado exclusivamente para o usuário de atendimento, para que este consiga inserir o histórico de tratativas de cobrança conforme o processo avança.

 ![Captura de tela de 2023-04-20 15-40-24.png](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%20ad78168ee5154cb39c6af4fa058faec6/Captura_de_tela_de_2023-04-20_15-40-24.png)

### **Etapa 3 - Reembolso do dano: Formulário de reembolso**

Esta etapa deve ser preenchida pelo Financeiro e visualizada pelos demais usuários (atendimento, anfitrião e onboarding).

O formulário que deve ser preenchido contém os seguintes dados:

**As palavras em negrito** correspondem as `labels`  do formulário

**Reembolso do dano** `h1` **:** Título do formulário da página **Validação do recebimento:** `h2` : Título da seção, que contem as seguintes informações: **Valor total do dano:** `number` : Preenchido pelo DB **Valor recebido:** `number` : Preenchido pelo DB, com um `button` que abre a imagem ou arquivo que foi upada pelo anfitrião ou atendimento **Diferença:** `number` : Valor calculado quando o Valor recebido < Valor total do dano, assim sendo Valor total - Valor recebido = Diferença

**Resumo de danos lançados - Proprietário || Seazone:** `h2` : Título da seção de dados **Dono do reembolso:** `string` : Este valor deve ser preenchido com a informação do formulário de Histórico e tratativas de cobrança **Nome:** `string`: Nome do Proprietário. Deve ser preenchido com os valores do DB. Se o Dono do reembolso for Seazone, o valor deverá ser este.

**Dados bancários:** `h2` : Título da seção de dados. Os dados abaixos devem ser trazidos automaricamente fazendo um GET na API de dados bancários. Os dados bancários que devem ser trazidos são os que estão setados como conta bancária principal no banco de dados. **Banco:** `string` **Número do banco:** `number` **Agência:** `number` **Conta:** `number` **Tipo de conta:** `string` **Nome do correntista:** `string` **CPF/CNPJ:** `number` **Chave PIX:** `number | string`

Abaixo destes dados, deve aparecer a seguinte tabela, com as colunas:

**Tipo de Dano:** `string` : Preenchido pelo DB **Classificação:** `string` : Preenchido pelo DB **Item:** `string` : Preenchido pelo DB **Quantidade:** `string` : Preenchido pelo DB **O que precisa ser feito?:** `string` : Preenchido pelo DB **Valor:** `string` : Preenchido pelo DB. Valor unitário do item danificado

Abaixo da tabela devemos trazer os seguintes dados: **Valor total:** `string` : Preenchido pelo DB: Valor total da soma de itens danificados DE ACORDO COM O DONO DO REEMBOLSO

**Valor recebido:** `string`: Preenchido pelo DB : Se refere ao valor recebido pelo anfitrião ou atendimento **Valor do reembolso:** O valor do reembolso terá duas condicionais: SE o valor total do dano === ao valor recebido, então, o valor do repasse de reembolso === soma do valor total do dano (proprietário ou seazone) SE o valor total do dano < que o valor recebido, então, calcula-se qual a porcentagem recebida baseada no valor total do dano, e com o valor desta porcentagem, calculasse o repasse PROPORCIONAL a cada dono do reembolso: Seazone ou proprietário.

Exemplo: Valor total do dano = 150,00 Valor recebido = 100,00 → equivale a 66% do valor total.

Considerando que:

Valor total de danos ao Proprietário = 100,00

Valor total de danos à Seazone = 50,00

Logo, o repasse deve ser proporcional a esses valores com base nos 66% recebidos. Assim:

Valor do repasse proprietário = 66,00

Valor do repasse Seazone = 34,00

**Upload do comprovante de repasse:** `input Download file` : Usuário poderá clicar ou arrastar um documento ou imagem com pagamento realizado. `placeholder`: Clique ou arraste para fazer o upload **Reembolso realizado:** `boolean`: Usuário deve sinalizar se o reembolso já foi repassado ao dono do reembolso. **Adicionar dados:** `button submit` : Botão para adicionar os dados inseridos. Após clicar neste botão, os dados devem ser disponibilizados para os demais usuários (anfitrião e atendimento). Além disso, a tela deve ficar disponível para o CS, para que o time consiga consultar os valores de transferência.

**ATENÇÃO: Caso haja os danos apontados pertençam a diferentes donos de reembolso, devem haver duas seções referente a cada dono. Por exemplo, se houver reembolsos a serem repassados para a Seazone && Proprietário, devem haver duas seções com os mesmos dados e inputs acima, uma que se refere a Seazone, e a outra que se refere ao Proprietário.**

 ![Finaneiro - Reembolso do dano.png](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%20ad78168ee5154cb39c6af4fa058faec6/Finaneiro_-_Reembolso_do_dano.png)

### Backend:

Arquitetura de dados

<https://www.figma.com/file/3w5tZhbhpI09p0C2o9OvEu/Danos-de-hospede?type=design&node-id=3%3A19&mode=design&t=XPsR4UbmaA3Gnuhw-1> → NÃO ESTÁ EM USO (está sendo salvo para ficar o registro)

Novas tabelas

**household_linen**

Tabela que armazena itens do enxoval.

| Campo | Valor | Descrição |
|----|----|----|
| name | CharField | nome do item do enxoval |
| price | DecimalField | preço do item do enxoval |

**guest_damage**

Tabela que cada dano do hóspede associado a uma reserva.

| Campo | Valor | Descrição |
|----|----|----|
| reservation | FK | Chave estrangeira para a reserva |
| description | TextField | Descrição |
| damage_type | CharField | Tipo de dano (opções: layette, damaged itens, lost itens, damaged property, pendency) |
| item_type | CharField | Tipo do item (opções: furniture, utensils, bathroom, appliance) |
| item_quantity | PositiveInteger | Quantidade de itens |
| item_name | CharField | Nome do item |
| resolution | CharField | O que precisa ser feito (opções: replace item, repair, cleaning, outsourced service, collect pendency) |
| quotation_link | CharField | Link do orçamento |
| quotation_file | FK | Arquivo do orçamento (chave estrangeira para a tabela FileItem) |
| item_price | DecimalField | Preço do orçamento/dano |
| observation | TextField | Observação |
| refund_holder | Charfield | Dono do reembolso (opções: Seazone, proprietário) |
| are_evidences_and_quotation_validated | Boolean | Informa se as evidências e orçamento foram validados |
| missing_information | TextField | Informações faltando |

**guest_damage_evidence**

Tabela que armazena cada evidência associada a um dano do hóspede.

| Campo | Valor | Descrição |
|----|----|----|
| guest_damage | FK | Chave estrangeira para o dano de hóspede |
| evidence | FK | Chave estrangeira para a tabela FIletem (arquivo que mostra evidência do dano) |

**guest_damage_negotiation**

Tabela que armazena a tratativa de pagamento de danos associada a uma reserva.

| Campo | Valor | Descrição |
|----|----|----|
| reservation | FK | Chave estrangeira para a reserva |
| status | CharField | Status |
| last_status_change | Datetime | Última atualização do status |
| stage | CharField | Etapa (opções: Damage details, Damage historic and negotiations, damage refund) |
| aircover_code | CharField | Código do aircode do Airbnb |
| amount_received | DecimalField | Valor Recebido |
| guest_payment_status | CharField | Status do pagamento do hóspede (opções: Requested, Dispute, Paid, Finished with success, Pending) |
| is_to_inform_owner | Boolean | É para informar proprietário? |
| is_receiving_confirmed | Boolean | Recebimento do pagamento do hóspede confirmado? |
| is_refunded | Boolean | Informa se o dano já foi reembolsado |

**damage_negotiation_guest_payment_receipt**

Tabela que armazena pagamentos recebidos do hóspede associado a uma tratativa de danos.

| Campo | Valor | Descrição |
|----|----|----|
| guest_damage_negotiation | FK | Chave estrangeira para a tratativa do dano |
| guest_payment_receipt | FK | Chave estrangeira para a tabela FIletem (comprovante de pagamento do hóspede) |

**damage_negotiation_owner_payment_receipt**

Tabela que armazena pagamentos enviados ao proprietário associado a uma tratativa de danos.

| Campo | Valor | Descrição |
|----|----|----|
| guest_damage_negotiation | FK | Chave estrangeira para a tratativa do dano |
| owner_payment_receipt | FK | Chave estrangeira para a tabela FIletem (comprovante de pagamento do proprietário) |

**guest_damage_negotiation_history**

Tabela que armazena histórico de contato com o hóspede associado a uma tratativa de danos.

| Campo | Valor | Descrição |
|----|----|----|
| guest_damage_negotiation | FK | Chave estrangeira para a tratativa do dano |
| contact_date | Datetime | Data de contato com o hóspede |
| history | TextField | História do contato |

**ENDPOINTS**

*GET /properties/properties_list*

filtros: `search: {property code}`

**precisa criar um search no code para trazer os imóveis e adicionar permissões conforme documentação**

`[`

`{`

`id: number,`

`code: string,`

`status: string`

`}`

`]`

Precisa do id ou code para filtrar as tratativas referentes a esse imóvel. Ou o front pode pegar do input html também.

*GET /reservation*

filtros: `ota_name: string`,  `check_in_date: string`, `check_out_date: string`, `search: {guest name and/or last name}`

→ **precisa ser feito**

`{`

`id: number,`

`code: string,`

`property_code: string,`

`guest_name: string,`

`check_in_date: string,`

`check_out_date: string,`

`ota_name: string,`

`guest_phone_number: string,`

`responsible_host: string`

`}`

*GET /reservation/{id}/*

*→* **precisa ser feito**

`{`

`id: number,`

`code: string,`

`property_code: string,`

`guest_name: string,`

`check_in_date: string,`

`check_out_date: string,`

`ota_name: string,`

`guest_phone_number: string,`

`responsible_host: string`

`}`

*GET /reservation{id}/guest_damages*

filtros: `refund_holder: string`,

→ **precisa ser feito**

`[`

`{`

`id: number,`

`reservation_id: number,`

`description: string,`

`damage_type: string,`

`item_type: string,`

`item_name: string,`

`item_quantity: number,`

`item_price: string,`

`total_price: string,`

`resolution: string,`

`quotation_link: string,`

`quotation_file: string uid of a file,`

`refund_holder: string,`

`observation: string`,

`evidences: [`

`{`

`id: number,`

`evidence: string uid of a file`

`},`

`{`

`id: number,`

`evidence: string uid of a file`

`},`

`…`

`]`

`}`

`]`

*GET reservation/{id}/guest_damage_negotiation*

→ **precisa ser feito**

`{`

`id: number,`

`status: string,`

`stage: string,`

`is_refunded: boolean,`

`reservation: {`

`id: number,`

`code: string,`

`property_code: string,`

`guest_name: string,`

`check_in_date: string,`

`check_out_date: string,`

`ota_name: string,`

`guest_phone_number: string,`

`responsible_host: string`

`}`

`guest_payment_receipts: list of file uids,`

`owner_payment_receipts: list of file uids,`

`histories: [`

`{`

`id: number,`

`contact_date: string,`

`history: string`

`},`

`{`

`id: number,`

`contact_date: string,`

`history: string`

`},`

`…`

`]`

`}`

*GET /household_linen*

→ **precisa ser feito**

`[`

`{`

`id: number,`

`name: string,`

`price: string`

`}`

`]`

*GET /guest_damage*

filtros: `property_code: string`,  `reservation_id: number`, `refund_holder: string`

→ **precisa ser feito**

`[`

`{`

`id: number,`

`reservation_id: number,`

`description: string,`

`damage_type: string,`

`item_type: string,`

`item_name: string,`

`item_quantity: number,`

`item_price: string,`

`total_price: string,`

`resolution: string,`

`quotation_link: string,`

`quotation_file: string uid of a file,`

`refund_holder: string,`

`observation: string`,

`evidences: [`

`{`

`id: number,`

`evidence: string uid of a file`

`},`

`{`

`id: number,`

`evidence: string uid of a file`

`},`

`…`

`]`

`}`

`]`

*GET /guest_damage/{id}/*

→ **precisa ser feito**

`{`

`id: number,`

`reservation_id: number,`

`description: string,`

`damage_type: string,`

`item_type: string,`

`item_name: string,`

`item_quantity: number,`

`item_price: string,`

`total_price: string,`

`resolution: string,`

`quotation_link: string,`

`quotation_file: string uid of a file,`

`refund_holder: string,`

`observation: string`,

`evidences: [`

`{`

`id: number,`

`evidence: string uid of a file`

`},`

`{`

`id: number,`

`evidence: string uid of a file`

`},`

`…`

`]`

`}`

*POST /guest_damage*

→ **precisa ser feito**

`{`

`reservation: number,`

`description: string,`

`damage_type: string,`

`item_type: string,`

`item_name: string,`

`item_quantity: number,`

`resolution: string,`

`quotation_link: string,`

`quotation_file: uid of a file,`

`item_price: string,`

`observation: string,`

`refund_holder: string,`

`evidences: list/array of files uid,`

`are_evidences_and_quotation_validated: boolean,`

`missing_information: string`

`}`

*PATCH /guest_damage/{id}/*

→ **precisa ser feito**

`{`

`description: string,`

`damage_type: string,`

`item_type: string,`

`item_name: string,`

`item_quantity: number,`

`resolution: string,`

`quotation_link: string,`

`quotation_file: uid of a file,`

`item_price: string,`

`observation: string,`

`refund_holder: string,`

`evidences: list/array of files uids,`

`are_evidences_and_quotation_validated: boolean,`

`missing_information: string`

`}`

*POST /guest_damage_evidence*

→ **precisa ser feito**

`{`

`guest_damage: number,`

`evidence: string uid of a file`

`}`

DELETE */guest_damage_evidence/{id}/*

→ **precisa ser feito**

*GET /guest_damage_negotiation*

filtros: `property_code: string`,  `status: string`, `stage: string`, `is_refunded: boolean, start_date: string`, `end_date: string`  → **precisa ser feito**

*OBS: as datas usadas nos filtros 'start_date' e 'end_date' são ambas datas de check out da reserva.*

`[`

`{`

`id: number,`

`status: string,`

`stage: string,`

`amount_to_receive: string,`

`amount_received: string,`

`amount_difference: string,`

`transfer_to_seazone: string,`

`transfer_to_owner: string,`

`is_refunded: boolean,`

`reservation: {`

`id: number,`

`code: string,`

`property_code: string,`

`guest_name: string,`

`check_in_date: string,`

`check_out_date: string,`

`ota_name: string,`

`guest_phone_number: string,`

`responsible_host: string`

`}`

`guest_payment_receipts: list of file uids,`

`owner_payment_receipts: list of file uids,`

`histories: [`

`{`

`id: number,`

`contact_date: string,`

`history: string`

`},`

`{`

`id: number,`

`contact_date: string,`

`history: string`

`},`

`…`

`]`

`}`

`]`

*GET /guest_damage_negotiation/{id}*

→ **precisa ser feito**

`{`

`id: number,`

`status: string,`

`stage: string,`

`amount_to_receive: string,`

`amount_received: string,`

`amount_difference: string,`

`transfer_to_seazone: string,`

`transfer_to_owner: string,`

`is_refunded: boolean,`

`reservation: {`

`id: number,`

`code: string,`

`property_code: string,`

`guest_name: string,`

`check_in_date: string,`

`check_out_date: string,`

`ota_name: string,`

`guest_phone_number: string,`

`responsible_host: string`

`}`

`guest_payment_receipts: list of file uids,`

`owner_payment_receipts: list of file uids,`

`histories: [`

`{`

`id: number,`

`contact_date: string,`

`history: string`

`},`

`{`

`id: number,`

`contact_date: string,`

`history: string`

`},`

`…`

`]`

`}`

*POST  /guest_damage_negotiation*

*→* **precisa ser feito**

`{`

`reservation: number,`

`status: string,`

`last_status_change: string,`

`stage: string,`

`aircover_code: string,`

`amount_received: string,`

`is_to_inform_owner: boolean,`

`guest_payment_status: string,`

`is_receiving_confirmed: boolean,`

`is_refunded: boolean,`

`histories: [`

`{`

`id: number,`

`contact_date: string,`

`history: string`

`},`

`{`

`id: number,`

`contact_date: string,`

`history: string`

`},`

`}`

*PATCH /guest_damage_negotiation/{id}*/

→ **precisa ser feito**

`{`

`status: string,`

`last_status_change: string,`

`stage: string,`

`aircover_code: string,`

`amount_received: string,`

`is_to_inform_owner: boolean,`

`guest_payment_status: string,`

`is_receiving_confirmed: boolean,`

`is_refunded: boolean,`

`}`

*POST /damage_negotiation_guest_payment*

→ **precisa ser feito**

`{`

`guest_damage_negotiation: number,`

`guest_payment_receipt: string uid of a file`

`}`

DELETE */damage_negotiation_guest_payment/{id}/*

→ **precisa ser feito**

*POST /damage_negotiation_owner_payment*

→ **precisa ser feito**

`{`

`guest_damage_negotiation: number,`

`owner_payment_receipt: string uid of a file`

`}`

DELETE */damage_negotiation_owner_payment/{id}/*

→ **precisa ser feito**

*POST /guest_damage_negotiation_history*

→ **precisa ser feito**

`{`

`guest_damage_negotiation: number,`

`contact_date: string,`

`history: string`

`}`

DELETE */guest_damage_negotiation_history/{id}/*

→ **precisa ser feito**

*GET /owner/{id}/bank_details*

→ **já existe**

`[    {         id: number,         bank: {             id: number,             bank_number: string,             long_name: string,             short_name: string         },         is_default: boolean,         entity_name: string,         branch_number: string,         account_number: string,         account_type: string,         cpf: string,         cnpj: string,         pix_key: string,         pix_key_type: string,         user: number     } ]`