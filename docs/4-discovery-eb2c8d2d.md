<!-- title: 4 Discovery | url: https://outline.seazone.com.br/doc/4-discovery-JkzIDZ38lY | area: Tecnologia -->

# 4 Discovery

## Levantamento de dados

Para este discovery realizamos pesquisa NPS (via hotjar), pesquisa via formulário (google forms) e entrevista com proprietários (google meet).

Resultados de pesquisa:

**Hotjar**

Tivemos 36 respostas em pesquisa enviada, e dentre as perguntas abaixo, tivemos os seguintes resultados:

**Com base na sua experiência com o acompanhamento financeiro, como você está se sentindo?**

 ![Captura de tela de 2023-08-10 09-43-43.png](/api/attachments.redirect?id=f19debbf-1397-449a-8f8d-3616676b4f0d)

Dentre os 8 usuários que responderam que 'Odeiam' e 'Não gostam', 5 usuários são estrangeiros. Dentre estes, 2 são brasileiros e relatam insatisfação com os valores das diárias de seus imóveis.

Este índice de estrangeiros insatisfeitos também é validado com a pergunta "Em uma escala de 1 a 5, qual o grau de dificuldade em realizar o acompanhamento financeiro pela plataforma?": de 40 respostas, 17 responderam "Muito difícil" ou "Difícil", e destes, 11 usuários são estrangeiros.

**Google Forms**

Esta pesquisa tinha como objetivo validar a usabilidade do novo layout de resumo financeiro, bem como a configuração de repasse por imóvel. Tivemos baixo retorno para aplicação desta pesquisa. Dos 6 usuários que responderam, todos concordam que a configuração de repasse é intuitiva e fácil de seguir; 5 responderam que se sentem confortáveis em utilizar o resumo financeiro para fazer os seuc acompanhamentos, e 1 usuário respondeu que deveria ter as despesas discriminadas.

**Entrevista com proprietário**

Realizamos entrevista com 2 proprietários, apresentando o novo modelo de configuração de repasse e o novo layout de acompanhamento financeiro: ambos concordam que do ponto de vista de clareza de dados e usabilidade a página está mais transparente e fácil de usar. A respeito da configuração de repasse, ambos relataram que preferem que o repasse continue sendo realizado, a menos que seja oferecido alguma vantagem de reter o repasse de um de seus imóveis com a Seazone.

## Qual o problema queremos resolver?

A principal oportunidade encontrada neste discovery é aumentar a confiança e transparência na visibilidade de dados financeiros para o proprietário, especialmente para proprietários estrangeiros que atualmente retém a receita de seus imóveis na Seazone e não tem visibilidade do seu saldo disponível, demonstrando assim insatisfação quanto ao seu acompanhamento via Sapron, como confimado na pesquisa de NPS.

## Porque este problema é importante?

* **Confiabilidade e Credibilidade:** Fornecer transparência demonstra responsabilidade e honestidade por parte da Seazone. Isso ajuda a construir uma relação de confiança e credibilidade tanto entre os proprietários que utilizam a plataforma quanto entre os potenciais clientes.
* **Satisfação do Cliente:** Proporcionar transparência aos proprietários aumenta a satisfação do cliente e estreita as relações entre Seazone e Proprietário
* **Atração de Proprietários:** A transparência financeira pode ser um fator diferencial para atrair novos proprietários para a plataforma Seazone. Proprietários em potencial podem ser mais propensos a escolher a plataforma que oferece clareza e visibilidade em relação às suas finanças.

## Como resolveremos este problema?


1. Elaborar um resumo financeiro claro e intuitivo, com soma total de Receitas, despesas, ajustes, comissões, repasses e saldo; bem como um extrato detalhado destes valores
2. Possibilidade de configurar o repasse das receitas por imóvel

## Dentro do escopo deste MVP


1. O Repasse é a ted realizada pelo financeiro, que reflete os valores reais que foram repassados para a conta configurada. O Repasse será setado por imóvel (valor + conta bancária). O input desse valor para o Resumo financeiro deve ser feito de forma automática a partir da planilha de repasses manipulada pelo financeiro, a ser integrada no Sapron pelo backend. Esta planilha deve conter um id que identifique o ted a ser realizado e deve ser incluído uma coluna de 'Motivo de ajuste' para que o proprietário tenha visibilidade caso o valor da Receita seja diferente do Repasse. Na lista de TEDs devemos dar visibilidade da Configuração de Repasse do proprietário (se o proprietário deseja ou não o repasse)

SE o proprietário sinalizou que deseja o repasse o valor entrará na seção de 'Repasse' (Valor + Imóvel + conta bancária configurada).

SE o proprietário sinalizou que não deseja o repasse o valor entrará na seção 'Saldo do período' que representa o valor do repasse mensal e no  'Saldo atual' que representa os valores dos repasses acumulados dos meses.

SE o proprietário possuir mais de um imóvel e para eles mais de uma conta bancária configurada para repasse && o saldo de um dos imóveis for negativo e do outro positivo, o imóvel que possui débitos fica com Saldo do período Negativo, e o repasse do outro imóvel deve ocorrer normalmente;

SE o proprietário optar por retenção de repasse,  em meses em que o imóvel não tenha receita suficiente para cobrir todas as despesas, o valor necessário será abatido do seu Saldo acumulado (se disponível) automaticamente;

SE o proprietário não possuir conta bancária cadastrada, automaticamente o repasse ficará retido e esta informação deve ser mostrada em Saldo do período e Saldo acumulado;

A sinalização de retenção  devem ser setados por default como `false` (proprietário deseja que o repasse seja realizado, sua receita não ficará retida) e alterados somente se o proprietário setar que deseja reter o repasse. Os casos de exceção (proprietários que já retém o saldo na Seazone) serão sinalizados pelo financeiro, e somente para estes, a retenção do repasse deve ser sinalizado como `true`. Para estes casos de exceção devemos trazer o Saldo Atual acumulado, para que eles tenham visibilidade deste dado, bem como os valores posteriores, que deverão ser atualizados em 'Saldo do Período'.


2. Receita, Ajuste, Comissão e Despesa são os valores validados pelo financeiro, na tela de fechamento do imóvel. Esses valores devem refletir os valores lançados por imóvel/mês.
3. Não deve ser possível repasses 'parciais' ou sob demanda: uma vez configurado o repasse pelo proprietário, esta configuração deve ser feita até o último dia do mês corrente para ser aplicada no mês seguinte. Caso essa configuração seja realizada fora deste período, as alterações passam a valer para o mês subsequente.

## Oportunidades futuras:

As principais oportunidades futuras que não estão elencadas neste discovery estão detalhadas no [Braimstorming](/doc/3-brainstorming-RoUnZsMWUn)