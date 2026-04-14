<!-- title: 6 Protótipo Viabilidade de uso, de construção e | url: https://outline.seazone.com.br/doc/6-prototipo-viabilidade-de-uso-de-construcao-e-wUp2NfHANl | area: Tecnologia -->

# 6 Protótipo Viabilidade de uso, de construção e

**Ideias que poderiam solucionar isso:**

[FIGMA](https://www.figma.com/file/yXtgxPh7MhnKIFq1ZQZJpE/Propriet%C3%A1rio---Carteira?type=design&node-id=3%3A21&mode=design&t=j0FRm7Lq7LaonPQV-1)

**Legenda de ícones:**

👩🏻‍🔧: Feature sendo desenvolvida pelo time de Discovery

✅: Pronto para desenvolver 🔁: Feature entregue para Delivery ❤️‍🔥: Feature em ambiente de Produção

### Feature 1 - Refatoração dos botões header e troca de cor - Refactor- Front ✅

A cor do header deve ser trocada para azul, conforme modelo abaixo e os botões de "Quero investir" e "Quero vender" devem ser incluídos na seção "Oportunidades Seazone". Ao clicar em "Acessar" o comportamento deve permanecer como atualmente.

 ![Captura de tela de 2023-08-09 19-25-44.png](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%201117c076220a4dd7893b364bcdfa72c5/Captura_de_tela_de_2023-08-09_19-25-44.png)

### Feature 2 - Pop-up de apresentação de novas funcionalidades - Feature - Front + Back ✅

Ao abrir a página de proprietário, o usuário deve visualizar os pop-ups abaixo:

 ![Frame 1958(1).png](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%201117c076220a4dd7893b364bcdfa72c5/Frame_1958(1).png)

 ![Frame 1960(1).png](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%201117c076220a4dd7893b364bcdfa72c5/Frame_1960(1).png)

Comportamento: Os modais devem abrir sempre que o proprietário acessa a página a menos que ele clique em 'Não quero mais receber essa mensagem'

No pop-up com o título de 'Nova funcionalidade' o botão 'Quero definir agora', deve levar para a rota de /meus dados, na seção de  Controle de repasse (Feature 3 deste discovery)

 ![Captura de tela de 2023-08-09 19-42-38.png](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%201117c076220a4dd7893b364bcdfa72c5/Captura_de_tela_de_2023-08-09_19-42-38.png)

No pop-up com o título de 'Resumo financeiro', o botão 'Ver resumo financeiro' deve levar para a seção de 'Resumo financeiro' (/proprietario) (Feature 4 deste discovery)

 ![Captura de tela de 2023-08-09 19-47-01.png](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%201117c076220a4dd7893b364bcdfa72c5/Captura_de_tela_de_2023-08-09_19-47-01.png)

### Feature 3 - Configuração de controle de repasse - Feature - Front + Back ✅

Na rota de /meusdados deve ser integrado a seção "Controle de Repasse" conforme modelo abaixo, logo após a seção de "Gerenciamento de contas bancárias"

 ![Group 2032.png](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%201117c076220a4dd7893b364bcdfa72c5/Group_2032.png)

Ao clicar no botão de "Quero configurar agora" deve abrir o seguinte modal, para configuração de repasse dos imóveis do proprietário:

 ![Captura de tela de 2023-08-09 19-57-05.png](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%201117c076220a4dd7893b364bcdfa72c5/Captura_de_tela_de_2023-08-09_19-57-05.png)

Na coluna de "Imóvel" deve constar todos os imóveis cadastrados do proprietário. Na coluna de "Deseja guardar o repasse deste imóvel na Seazone?" deve ser implementado um botão togle para cada um dos imóveis, possibilitando que o proprietário escolha quais os imóveis ele deseja que sua receita seja repassada ou não. O botão de Salvar, guarda os dados configurados.

Uma vez configurado o repasse, a seção deve ser mostrada da seguinte maneira:

 ![Captura de tela de 2023-08-09 20-03-01.png](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%201117c076220a4dd7893b364bcdfa72c5/Captura_de_tela_de_2023-08-09_20-03-01.png)

À esquerda mantém-se a explicação de funcionamento e à direita, um resumo da configuração realizada com o botão de 'Alterar configuração'. Ao clicar neste botão deve abrir o mesmo modal de Configuração de controle de repasse descrito acima.

**Backend** Deve ser possível guardar a informação booleana setada acima: Deseja guardar o repasse deste imóvel na Seazone? Sim/Não

Esta informação será visualizada nas seguintes páginas: Financeiro (administrativo): rota de fechamento de imóvel, rota de fechamento de proprietário, CSV de lista de teds Onboarding (CS proprietário): Lista de proprietários

### Feature 4 - Resumo financeiro - Feature - Front + Back ✅

**ATENÇÂO: Para compreender a renderização correta dos dados desta feature verifique a lógica de negócio a ser aplicada descrita na seção de** ['Fluxograma de validação de dados'](/doc/2-fluxograma-de-validacao-de-dados-84R49wOdDq)

No header da página de proprietário deve ser integrado a informação de "Saldo Atual", acompanhado do botão de "Resumo financeiro", que quando clicado deve levar até a seção com mesmo nome.

 ![Captura de tela de 2023-08-09 20-48-03.png](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%201117c076220a4dd7893b364bcdfa72c5/Captura_de_tela_de_2023-08-09_20-48-03.png)

Ao lado do Saldo atual, onde consta o "i" teremos três tipos de informação:

**Saldo positivo**: `tooltip` : Este valor refere-se ao valor do Repasse acumulado de seus imóveis.

 ![Captura de tela de 2023-08-09 20-59-31.png](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%201117c076220a4dd7893b364bcdfa72c5/Captura_de_tela_de_2023-08-09_20-59-31.png)

**Saldo negativo**:  `tooltip` : Seu saldo está negativo pois o valor de sua receita foi inferior às despesas. Verifique seu Resumo financeiro para verificar mais detalhes.

 ![Captura de tela de 2023-08-09 21-01-37.png](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%201117c076220a4dd7893b364bcdfa72c5/Captura_de_tela_de_2023-08-09_21-01-37.png)

**Saldo zerado:** `tooltip` : Seu Saldo Atual está zerado pois você optou pelo repasse de receita de seus imóveis. Verifique seu Resumo financeiro para detalhes de seus repasses.

 ![Captura de tela de 2023-08-09 21-08-12.png](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%201117c076220a4dd7893b364bcdfa72c5/Captura_de_tela_de_2023-08-09_21-08-12.png)

Logo após a seção de imóveis, deve ser integrada a seção de Resumo financeiro, conforme modelo abaixo:

 ![Captura de tela de 2023-08-09 21-12-27.png](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%201117c076220a4dd7893b364bcdfa72c5/Captura_de_tela_de_2023-08-09_21-12-27.png)

A primeira parte desta seção deve conter o valor do Saldo Atual, acompanhado do "i" que segue a mesma lógica dos tooltips descritas acima. O ícone de "olho" serve para mostrar ou esconder o saldo quando clicado. No botão "Selecione o período" deve ser possível selecionar o mês e o ano de busca. O valor `default` deve ser setado com o mês corrente. No botão "Selecione o imóvel" deve ser possível selecionar um imóvel específico para visualizar o Resumo financeiro. O valor `default` deve ser setado como 'Todos', renderizando assim os dados de todos os imóveis referente ao mês selecionado. O botão "Buscar" permite a busca personalizada de acordo com os valores selecionados nos botões anteriores.

A segunda parte desta seção deve trazer os seguintes dados à esquerda:

**Despesas:** SOMA de todas as despesas de um ou todos os imóveis de acordo com o período selecionado. Este dado vem através da validação de dados do fechamento do imóvel; **Receita:** SOMA de todas as receitas de um ou todos os imóveis de acordo com o período selecionado. Este dado vem através da validação de dados do fechamento do imóvel; **Ajuste:** SOMA de todos os ajustes de um ou todos os imóveis de acordo com o período selecionado. Este dado vem através da validação de dados do fechamento do imóvel && de possíveis ajustes realizados após e emissão da lista de TEDs; **Comissão:** SOMA de todas as comissões de um ou todos os imóveis de acordo com o período selecionado. Este dado vem através da validação de dados do fechamento do imóvel; **Repasse:** SOMA de todos os repasses realizados pelo financeiro de um ou todos os imóveis de acordo com o período selecionado. Este dado vem da planilha integrada de Gerenciamentos de processo do financeiro. Caso o proprietário opte pela retenção de receita daquele  imóvel o valor de Repasse ficará zerado, sendo o valor renderizado no card 'Saldo do período' **Saldo do período:** SOMA de todos os valores de repasse retidos de um ou todos os imóveis de acordo com o período selecionado. Este dado vem da planilha integrada de Gerenciamentos de processo do financeiro. Caso o proprietário opte pelo repasse da receita daquele  imóvel o valor de Saldo do período ficará zerado.

À direita destes valores temos um grid de detalhamento de todas os cards setados acima, com as seguintes colunas:

**Data:** Refere-se a data de lançamento das Despesas, receitas, ajustes, comissões e repasses **Tipo:** Despesas||Receitas||Ajustes||Comissões {Código do imóvel de referência} e Repasses {Código do imóvel de referência} {Conta bancária de destino} **Valor:** Valor discriminado das Despesas, receitas, ajustes, comissões e repasses

Ponto de atenção: Caso o proprietário não possua conta bancária cadastrada deve ser exibido uma tag ao final da seção e o repasse será por default retido:

 ![Captura de tela de 2023-08-09 21-42-48.png](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%201117c076220a4dd7893b364bcdfa72c5/Captura_de_tela_de_2023-08-09_21-42-48.png)

Onde consta 'Clique aqui' deve estar linkado para a rota de /meusdados; Gerenciamento de conta bancária.

**Backend:** ['Fluxograma de validação de dados'](/doc/2-fluxograma-de-validacao-de-dados-84R49wOdDq)

### Feature 5 - Visibilidade configuração de repasse Fechamento Proprietário - Feature - Front + Back ✅

Na rota de Fechamento Proprietário, deve ser integrado na Lista de imóveis, na coluna de repasse os ícones abaixo, indicando se o repasse daquele imóvel deve ser ou não realizado. Os ícones devem estar acompanhados de tooltips que deixem clara a informação indicada pela cor do ícone:

 ![Group 2030(1).png](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%201117c076220a4dd7893b364bcdfa72c5/Group_2030(1).png)

Os ícones da cor vermelha devem estar acompanhados do tooltip:

 ![Group 2028(1).png](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%201117c076220a4dd7893b364bcdfa72c5/Group_2028(1).png)

Os ícones da cor verde devem estar acompanhados do tooltip:

 ![Group 2027.png](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%201117c076220a4dd7893b364bcdfa72c5/Group_2027.png)

### Feature 6 - Visibilidade configuração de repasse Fechamento imóvel - Feature - Front + Back ✅

Na rota de Fechamento Imóvel  (Financeiro/adm), deve ser integrado na coluna de repasse os ícones abaixo, indicando se o repasse daquele imóvel deve ser ou não realizado. Os ícones devem estar acompanhados de tooltips que deixem clara a informação indicada pela cor do ícone:

 ![Group 2029(1).png](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%201117c076220a4dd7893b364bcdfa72c5/Group_2029(1).png)

Os tooltips seguem a mesma lógica descrita na feature acima.

### Feature 7 - Visibilidade configuração de repasse Grid de proprietários - Feature - Front + Back ✅

Na rota de Lista de proprietários (onboarding), deve ser integrado a coluna de repasse com ícones abaixo:

 ![Group 2033.png](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%201117c076220a4dd7893b364bcdfa72c5/Group_2033.png)

Ao clicar no ícone deve abrir o seguinte modal, onde consta as configurações de repasse por imóvel selecionada pelo proprietário:

 ![Group 2031(1).png](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%201117c076220a4dd7893b364bcdfa72c5/Group_2031(1).png)