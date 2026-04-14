<!-- title: 2 Fluxograma de validação de dados | url: https://outline.seazone.com.br/doc/2-fluxograma-de-validacao-de-dados-SBrX2NvhIN | area: Tecnologia -->

# 2 Fluxograma de validação de dados

![Fluxograma Resumo Financeiro(2).png](2%20Fluxograma%20de%20validac%CC%A7a%CC%83o%20de%20dados%20d48cb3e1e741420c8ca8a0189f40a5fe/Fluxograma_Resumo_Financeiro(2).png)

[Fluxo Lucid](https://lucid.app/lucidchart/af71470a-eb86-4a2c-bdf7-b620f939208d/edit?viewport_loc=-5006%2C-2894%2C6937%2C3237%2C0_0&invitationId=inv_6998267e-2ff0-43cc-a9ee-2d93b2c001d3)

Lógica de negócio fluxo de dados:


1. Na tela proprietário, rota de /meusdados o proprietário irá realizar as configurações de repasse:

 ![Captura de tela de 2023-07-31 15-39-28.png](2%20Fluxograma%20de%20validac%CC%A7a%CC%83o%20de%20dados%20d48cb3e1e741420c8ca8a0189f40a5fe/Captura_de_tela_de_2023-07-31_15-39-28.png)

Deseja guardar o repasse deste imóvel na Seazone? : `boolean` A configuração ocorrerá por imóvel.

A sinalização de retenção  deve ser setado por default como `false` (proprietário deseja que o repasse seja realizado, sua receita não ficará retida) e alterados somente se o proprietário setar que deseja reter o repasse. Os casos de exceção (proprietários que já retém o saldo na Seazone) serão sinalizados pelo financeiro, e somente para estes, a retenção do repasse deve ser sinalizado como `true`. Para estes casos de exceção devemos trazer o Saldo Atual acumulado, para que eles tenham visibilidade deste dado, bem como os valores posteriores, que deverão ser atualizados em 'Saldo do Período'.


2. Após configurações de repasse configuradas, daremos visibilidade para este dado de três formas:

a) Tela financeiro (administrativo): Grid do fechamento de imóvel e fechamento do proprietário: coluna de repasse será sinalizado com ícone vermelho (Proprietário deseja reter o repasse); ícone verde (Proprietário deseja que o repasse seja realizado)

 ![Group 2030.png](2%20Fluxograma%20de%20validac%CC%A7a%CC%83o%20de%20dados%20d48cb3e1e741420c8ca8a0189f40a5fe/Group_2030.png)

 ![Group 2029.png](2%20Fluxograma%20de%20validac%CC%A7a%CC%83o%20de%20dados%20d48cb3e1e741420c8ca8a0189f40a5fe/Group_2029.png)

b) Tela onboarding, rota proprietário: integração da coluna de repasse que contém o ícone, ao clicar no ícone abre as informações de repasse configuradas pelo proprietário:

 ![Frame 1995.png](2%20Fluxograma%20de%20validac%CC%A7a%CC%83o%20de%20dados%20d48cb3e1e741420c8ca8a0189f40a5fe/Frame_1995.png)

 ![Group 2031.png](2%20Fluxograma%20de%20validac%CC%A7a%CC%83o%20de%20dados%20d48cb3e1e741420c8ca8a0189f40a5fe/Group_2031.png)

c) Tela financeiro (administrativo), rota de Lista de TEDs para proprietário: ao exportar o csv gerado nesta tela, o financeiro deve ter visibilidade de ambos os casos de configuração: aqueles que querem e não querem o repasse, a partir das configurações realizadas pelo proprietário. Deve ser incluída uma coluna: O proprietário deseja guardar o repasse deste imóvel na Seazone?

Deve ser incluído um id de rastreamento de TED para posteriormente sinalizarmos os pagamentos e retenções efetuadas, bem como os valores reais de repasse e a conta bancária de destino.


3. Após a exportação do arquivo CSV o financeiro irá realizar os ajustes finais na planilha de Gerenciamento de processos, **onde deve ser integrada a coluna de Motivo do ajuste** (para os casos em que o valor do repasse sofra alterações, o financeiro sinaliza os repasses efetivados de acordo com a configuração de repasse realizada pelos proprietários e  sinaliza os corretos valores repassados, bem como os corretos valores para aqueles que optaram por reter o repasse na Seazone). Desta forma, garantimos que tanto os valores de "Repasse" como os valores de "Saldo Atual" sejam confiáveis.

Os valores de repasse devem ser reenderizados na tela de Resumo financeiro do proprietário (dia 05 e dia 10 do mês), seguindo a seguinte lógica:

**Caso 1**: Proprietário deseja reter o repasse de seus imóveis na Seazone: Os valores referentes ao Repasse devem ser mostrados nos campos de 'Saldo do período' (valor referente ao mês) e Saldo Atual (Somado ao saldo anterior, sempre que houver). Neste caso não haverá valor de repasse pois assim o proprietário optou.

**Caso 2:** Proprietário deseja que o repasse seja realizado para a conta bancária configurada: Os valores referentes ao Repasse devem ser mostrados por imóvel na seção de repasse (valor total quando houver mais de um repasse) e na parte do extrato, com o valor, código do imóvel e os dados bancários da conta de repasse de destino.

**PONTOS DE ATENÇÃO:**


1. Um dos principais motivos de desenvolvimento desta feature é dar visibilidade para os proprietários que já retém sua receita na Seazone, desta forma, precisamos assegurar que para estes, os valores de "Saldo do período" e "Saldo Atual" sejam reenderizados de maneira correta.
2. Para os proprietários que não possuem conta bancária cadastrada, o repasse será retido na Seazone, e os valores devem aparecer tanto em "Saldo do período" como em "Saldo Atual"
3. Para os proprietários que optarem por retenção de receita, nos meses em que as despesas forem maior que sua receita, as despesas devem ser abatidas do Saldo disponível (quando houver). Se o saldo disponível não for suficiente para cobrie as despesas o imóvel ficará com saldo negativo (respeitando a regra de repasse por imóvel)
4. Quando houver Ajuste no valor da Receita, após a emissão da lista de TEDs, nós devemos trazer o valor do ajuste bem como o motivo, dando visiblidade deste dado para o proprietário.