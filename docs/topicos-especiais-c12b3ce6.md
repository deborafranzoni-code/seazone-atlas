<!-- title: Tópicos Especiais | url: https://outline.seazone.com.br/doc/topicos-especiais-FpAyjcvvr3 | area: Administrativo Financeiro -->

# Tópicos Especiais

![](/api/attachments.redirect?id=18e574e7-27e2-42fd-84ec-b885616a6281)

⭐

# Tópicos Especiais


Categorização de cartões de crédito

A categorização das saídas relacionadas aos cartões de crédito segue a mesma metodologia utilizada para as saídas da conta corrente. A categorização também é feita na planilha AdmSys. No entanto, somente as empresas Seazone Serviços e Seazone Investimentos registram saídas nos cartões de crédito. Na planilha AdmSys Seazone Serviços, a aba relevante para a categorização dos cartões é chamada "Cartão Seazone", enquanto na planilha AdmSys Seazone Investimentos, essa aba é chamada de "Cartão de Crédito".

Na categorização de cartões de crédito, a informação histórica é especialmente relevante. É essencial examinar as categorizações dos meses anteriores para identificar pagamentos parcelados, pois é comum encontrar valores repetidos e com a mesma data, o que geralmente indica parcelas futuras de uma compra passada.

Como mencionado anteriormente, a atualização da seção de cartões ocorre uma vez no mês para cada cartão. Dessa maneira, na data de atualização destas abas, os esforços são concentrados na categorização rápida dos gastos com cartões.

Devido à falta de documentação para muitas compras realizadas com cartão de crédito, é comum surgirem dúvidas durante o processo de categorização. Embora a maioria das compras seja registrada na planilha de [Relatório de Compras](https://docs.google.com/spreadsheets/d/16Yh8Q1adVBdYNyoM8NoGHpnkyVUfRTcVoK14bpg2khw/edit#gid=0), algumas transações de setores específicos podem não estar documentadas ali. Nesses casos, é necessário recorrer ao ControleCPG, Google Drive e Slack para identificar a natureza dessas saídas.


Tags da Atividade

Em alguns casos, a categorização convencional não oferece todas as informações necessárias para uma compreensão completa de uma operação específica. Por exemplo, ajustes manuais na categorização são comuns devido às necessidades dos gestores dos setores. Para suprir a necessidade de sinalizar aquelas categorizações que sofreram ajuste, foi implantado o uso de Tags na Atividade. As Tags são inseridas antes do texto da atividade e seguem o seguinte formato:


 ![](/api/attachments.redirect?id=33ad3979-0a84-448f-b992-668e6e97c7c8)


Elas são sempre apresentadas entre chaves. Ao utilizar essas Tags, é possível localizar rapidamente no AdmSys todas as operações que foram ajustadas por algum motivo.\nAlém disso, também temos Tags para estornos, identificadas como \[ESTORNO PGTO EM DUPLICIDADE\], \[ESTORNO PGTO VARIÁVEL\], \[ESTORNO REPASSE PROP\], \[ESTORNO REPASSE ANFITRIÃO\]. Essas Tags podem variar de acordo com as necessidades do setor, mas em regra, elas sempre estão entre chaves.\n


Categorizações que não afetam o orçamento

Dentro do Plano de Contas, há uma seção intitulada "Outras Movimentações". Esta seção contém uma lista de categorizações que não têm impacto no orçamento. Formalmente, atribuímos uma Empresa, Setor, Centro de Custo e Categoria para essas saídas, por razões de compliance com o restante do Plano de Contas e para fins de análise. No entanto, é importante observar que essas saídas não são consideradas despesas propriamente ditas.

No caso dos repasses, por exemplo, a Seazone recebe esses valores dos hóspedes e transfere para os proprietário e anfitriões. Isso quer dizer que a Seazone funciona como uma espécie de depositário desses valores, ou seja, a saída desses valores não configura despesa assim como a entrada desses valores não configura receita.

Por exemplo, no caso dos repasses, a Seazone atua como intermediária entre os hóspedes e os proprietários/anfitriões. Nesse contexto, os valores transferidos não são considerados despesas, da mesma forma que os valores recebidos não são considerados receita. A Seazone age como um depositário desses valores, facilitando as transações entre as partes envolvidas. Dessa maneira, as saídas de repasses não são levadas em conta ao comparar o orçamento planejado com o realizado.

Os adiantamentos de despesas de clientes seguem a mesma lógica. A Seazone efetua pagamentos de contas de luz, energia elétrica, internet e outras despesas em nome dos clientes. Quando é feito o repasse, esses valores adiantados pela Seazone são deduzidos do montante total do repasse devido, sem afetar o orçamento.

No caso das transferências e aplicações, as saídas de recursos financeiros não são despesas da Seazone. Essas transações representam simplesmente movimentações de valores entre as diferentes contas da própria empresa, e, portanto, não têm impacto direto no orçamento.



| **Empresa** | **Setor** | **CC** | **Categoria** |
|:---|:---|:---|:---|
| **Seazone Serviços** | Admin e Fin | Repasse | Repasse de danos |
| **Seazone Serviços** | Admin e Fin | Repasse | Proprietário |
| **Seazone Serviços** | Admin e Fin | Repasse | Anfitrião |
| **Seazone Serviços** | Admin e Fin | Gestão de contas | Adiantamento de despesas de clientes |
| **Seazone Serviços** | Admin e Fin | Transferência | Transferência |
| **Khanto Reservas** | Admin e Fin | Transferência | Transferência |
| **Seazone Marketplace** | Admin e Fin | Transferência | Transferência |
| **Seazone Investimentos** | Admin e Fin | Transferência | Transferência |
| **Seazone Holding** | Admin e Fin | Transferência | Transferência |
| **Seazone Investimentos** | Admin e Fin | Administrativo | Aplicação |
| **Khanto Reservas** | Admin e Fin | Administrativo | Aplicação |
| **Seazone Holding** | Admin e Fin | Administrativo | Aplicação |
| **Seazone Investimentos** | Admin e Fin | Cartão de crédito | Cartão de crédito |
| **Seazone Serviços** | Admin e Fin | Cartão de crédito | Cartão de crédito |
| **Seazone Serviços** | Admin e Fin | Devolução | Devolução |
| **Seazone Serviços** | Admin e Fin | Repasse | Consumo |

Coluna de saídas inválidas

Uma coluna ainda não mencionada por não fazer parte da categorização propriamente dita, mas que é muito importante como um todo para o processo, é a coluna "Inválido".

O propósito fundamental da coluna "Inválido" no AdmSys é identificar e sinalizar as entradas de dados que não devem ser consideradas. Por exemplo, em casos de estorno de pagamento, onde uma quantia é revertida para a conta, essa transação é refletida como um valor positivo na aba de entradas.

Para um usuário que consulta exclusivamente a aba de saídas, parece que o pagamento foi processado normalmente, ignorando o estorno. Assim, uma etapa muito importante na categorização é detectar esses estornos registrados na aba de entradas, localizar a operação correspondente na aba de saídas e marcá-la como "Inválido".


💡

Observar a coluna "Inválido" é muito importante e não se atentar para invalidar os estornos pode ter muito impacto no processo de conciliação entre os valores realizados e orçados.


\

\