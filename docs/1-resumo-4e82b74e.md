<!-- title: 1. Resumo | url: https://outline.seazone.com.br/doc/1-resumo-FX030vC4Lp | area: Tecnologia -->

# 1. Resumo

## **1.1 Introdução e objetivo**

Este discovery tem como objetivo verificar as principais oportunidades de melhoria na página do proprietário, especialmente no que tange ao seu acompanhamento financeiro, deixando claro os seguintes dados: Saldo total (acumulado), Receita(por imóvel), Despesa(por imóvel), Comissão (por imóvel), Repasse (com o valor real, por conta bancária cadastrada) e Saldo do Período (caso o proprietário selecione o período no campo de busca) Além disso deve ser possível ser permitido ao proprietário selecionar se ele deseja reter sua receita na Seazone ou se ele deseja o repasse.

Para tanto, devemos seguir a seguinte lógica definida pela diretoria:


1. O Repasse é a ted realizada pelo financeiro, que reflete os valores reais que foram repassados para a conta configurada. O Repasse será setado por imóvel (valor + conta bancária). O input desse valor para o Resumo financeiro deve ser feito de forma automática a partir da planilha de repasses manipulada pelo financeiro, a ser integrada no Sapron pelo backend. Esta planilha deve conter um id que identifique o ted a ser realizado e deve ser incluído uma coluna de 'Motivo de ajuste' para que o proprietário tenha visibilidade caso o valor da Receita seja diferente do Repasse. Na lista de TEDs devemos dar visibilidade da Configuração de Repasse do proprietário (se o proprietário deseja ou não o repasse)

SE o proprietário sinalizou que deseja o repasse o valor entrará na seção de 'Repasse' (Valor + Imóvel + conta bancária configurada).

SE o proprietário sinalizou que não deseja o repasse o valor entrará na seção 'Saldo do período' que representa o valor do repasse mensal e no  'Saldo atual' que representa os valores dos repasses acumulados dos meses.

SE o proprietário possuir mais de um imóvel e para eles mais de uma conta bancária configurada para repasse && o saldo de um dos imóveis for negativo e do outro positivo, o imóvel que possui débitos fica com Saldo do período Negativo, e o repasse do outro imóvel deve ocorrer normalmente;

SE o proprietário optar por retenção de repasse,  em meses em que o imóvel não tenha receita suficiente para cobrir todas as despesas, o valor necessário será abatido do seu Saldo acumulado (se disponível) automaticamente;

SE o proprietário não possuir conta bancária cadastrada, automaticamente o repasse ficará retido e esta informação deve ser mostrada em Saldo do período e Saldo acumulado;

A sinalização de retenção  devem ser setados por default como `false` (proprietário deseja que o repasse seja realizado, sua receita não ficará retida) e alterados somente se o proprietário setar que deseja reter o repasse. Os casos de exceção (proprietários que já retém o saldo na Seazone) serão sinalizados pelo financeiro, e somente para estes, a retenção do repasse deve ser sinalizado como `true`. Para estes casos de exceção devemos trazer o Saldo Atual acumulado, para que eles tenham visibilidade deste dado, bem como os valores posteriores, que deverão ser atualizados em 'Saldo do Período'.


2. Receita, Ajuste, Comissão e Despesa são os valores validados pelo financeiro, na tela de fechamento do imóvel. Esses valores devem refletir os valores lançados por imóvel/mês.
3. Não deve ser possível repasses 'parciais' ou sob demanda: uma vez configurado o repasse pelo proprietário, esta configuração deve ser feita até o último dia do mês corrente para ser aplicada no mês seguinte. Caso essa configuração seja realizada fora deste período, as alterações passam a valer para o mês subsequente.

Nice to have: Estender para anfitriões

## **1.2 Para quem é?**

As oportunidades apresentadas são pensadas para o cliente Proprietário.