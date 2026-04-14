<!-- title: Elementos da Categorização | url: https://outline.seazone.com.br/doc/elementos-da-categorizacao-N75ectuyOq | area: Administrativo Financeiro -->

# Elementos da Categorização

![](/api/attachments.redirect?id=7461ded8-acf9-4a4a-8294-2edda78781fe)

 ![](https://www.notion.so/icons/kind_red.svg)

# Elementos da Categorização


\
No processo de categorização da Seazone, traduzimos os dados dos extratos bancários e dos cartões de crédito de várias instituições financeiras em termos compatíveis com nosso Plano de Contas e, por consequência, com nosso orçamento. Os extratos fornecidos contêm informações como data, valor e descrição. No entanto, muitas vezes, as descrições são pouco explicativas. Por exemplo, uma transação pode ser rotulada como "PAGAMENTO DE TITULO", o que não oferece muitos detalhes sobre a natureza da despesa. É importante ressaltar que, embora haja um processo de solicitação e aprovação dos gastos antes que os pagamentos sejam efetuados, esse processo não inclui a categorização das despesas.

As informações essenciais relacionadas às saídas incluem Atividade, Empresa, Setor, Centro de Custo, Categoria e Subcategoria. Data, o valor e a descrição do extrato não informações muito importantes, mas passam por nenhum processo de categorização, já que essas informações vêm do extrato.

Cada empresa dentro da Seazone mantém suas próprias contas bancárias independentes. Isso significa que um pagamento pode ser realizado, por exemplo, através da conta do Banco BTG pertencente à Seazone Serviços ou da conta do Banco BTG pertencente à Seazone Investimentos, e essas duas contas não possuem nenhuma interligação.

A etapa inicial da categorização ocorre quando, diariamente, o extrato é baixado do sistema dos bancos. Através de um script, as informações de Data, Valor e Descrição do Extrato são transferidas para as linhas da planilhas AdmSys, onde ocorre o cadastro da Atividade, Empresa, Setor, Centro de Custo, Categoria e Subcategoria.


### Atividade

Na categorização, a atividade descreve as saídas de maneira compreensível. Seu objetivo principal é que qualquer pessoa que veja a informação possa entender do que se trata aquela despesa. Por exemplo, as descrições podem ser "Primeira parcela de pagamento de Camisetas para Colaboradores", "Limpeza de escritório" ou "Pagamento de fotos profissionais para o Imóvel ETA0152".

Algumas despesas são mais rotineiras e previsíveis, como, por exemplo, o pagamento de salários e os repasses aos proprietários. Nestes casos, não é necessário uma descrição muito detalhada, pois a natureza do negócio e o restante da categorização já explicam claramente o propósito da saída de caixa. Para pagamentos de salários, podemos usar apenas o código do colaborador na atividade. Para repasses aos proprietários, podemos usar apenas o código do proprietário.

Mas como garantir que entendemos exatamente o motivo do gasto? A maioria das despesas está registrada na planilha [Controle CPG](https://docs.google.com/spreadsheets/d/12jFzCTYAISO2xVBFcC6YkDehBmR2m5ymYGcwQnU3fhA/edit#gid=1561465343). Normalmente, as descrições que encontramos lá são as mesmas que usamos para cadastrar na planilha AdmSys. No entanto, é importante ressaltar que às vezes, essas informações não estão completas, então é necessário buscar em outras fontes ou esclarecer diretamente aos responsáveis pela despesa. Além disso, as vezes as descrições no [Controle CPG](https://docs.google.com/spreadsheets/d/12jFzCTYAISO2xVBFcC6YkDehBmR2m5ymYGcwQnU3fhA/edit#gid=1561465343) são detalhadas e prolixas, então é necessário resumir o conteúdo.


### Empresa

A Seazone é composta elas empresas Seazone Serviços (SZS), Seazone Investimentos (SZI), Khanto Reservas e Seazone Holding. Cada uma dessas empresas possui sua própria planilha AdmSys, onde ocorre o processo de categorização das despesas. É importante entender que quando uma despesa é registrada na AdmSys de uma empresa, isso indica que o pagamento foi feito a partir de uma conta bancária dessa empresa, mas não necessariamente que a despesa é atribuída a essa empresa em termos gerenciais. Isso significa que às vezes a SZI pode pagar despesas que, na verdade, pertencem à SZS e vice-versa.

Para lidar com essa situação, todas as planilhas AdmSys das empresas têm uma coluna chamada "Empresa". Na maioria dos casos, a empresa listada nessa coluna é a mesma à qual pertence a AdmSys em questão. No entanto, quando uma despesa é realizada por uma empresa, mas pertence a outra, o nome dessa outra empresa é registrado nessa coluna.


### Setor

Normalmente, as empresas são divididas em setores. Um setor é uma divisão funcional que agrupa atividades relacionadas. Cada Setor possui seus proprios objetivos, metas e estratégias específicas de funcionamento e todos eles convergem em direção ao funcionamento da empresa como um todo. Então, o que ocorre normalmente é que os setores são subdivisões das empresas, porém a Seazone opera por meio de 4 empresas, então como ficam distribuidos os setores? Existem setores específicos que só aparecem em uma empresa, mas existem também setores "multiempresa", ou seja, um setor que aparece em mais de uma empresa da Seazone. Por exemplo, o Comercial é um Setor cujos gastos estão alocados tanto na Seazone Serviços quanto na Seazone Investimentos.

Para visualizar a organização completa dos setores e colaboradores, é recomendado consultar o Organograma de Pessoas da Seazone. Lá, é possível encontrar informações sobre os responsáveis por cada setor.

A tabela abaixo apresenta a distribuição dos setores em relação às empresas. É importante ressaltar que essa esta é a configuração de setores e empresas, em 03/2024. A estrutura do Plano de Contas muda conforme a necessidade da empresa e conforme o orçamento e esta tabela é apenas um exemplo de como os setores e empresas podem estar organizados.



| Setor | SZS | SZI | Khanto | Holding |
|:---|:---|:---|:---|:---|
| Administrativo e Financeiro | X | X | X | X |
| Análise de Negócios |    | X |    |    |
| B2B | X |    |    |    |
| Business Operations | X |    |    |    |
| Comercial | X | X |    |    |
| Compliance |    | X |    |    |
| Diretoria | X |    |    |    |
| Estruturação |    | X |    |    |
| Expansão | X |    |    |    |
| Holding (Setor) | X |    |    |    |
| Jovens Talentos | X |    |    |    |
| Jurídico | X | X |    |    |
| Marketing | X | X |    |    |
| Marketplace | X |    |    |    |
| Negócios | X | X |    |    |
| Novos Projetos |    | X |    |    |
| Operação | X |    |    |    |
| People | X |    |    |    |
| Planejamento | X |    |    |    |
| Seazone Investimentos (Setor) |    | X |    |    |
| Tecnologia | X |    |    |    |


### Centro de Custo

Na Seazone, o termo "Centro de Custo" é usado para designar um agrupamento lógico de gastos semelhantes dentro de um determinado setor. Por exemplo, é razoável agrupar despesas relacionadas a impostos sob um Centro de Custo chamado "Impostos". Da mesma forma, os Sistemas Integrados de Gestão que utilizamos são agrupados sob um Centro de Custo chamado "S.I.G.". Além disso, é lógico ter um agrupamento lógico específico para os valores que repassamos para proprietários e anfitriões, e esse agrupamento, ou Centro de Custo, é denominado "Repasse" nesse caso específico.

Embora não seja prático listar todos os centros de custo da Seazone, eles estão devidamente organizados em nosso Plano de Contas. Essa estrutura ajuda a entender e controlar de forma mais eficaz como os recursos financeiros são utilizados em cada parte da empresa.

Como exemplificado na tabela abaixo, temos um setor chamado People, que é o equivalente ao Departamento de Recursos Humanos (RH). Além disso, também temos um Centro de Custo chamado "RH". É importante entender que esses são conceitos diferentes. O Centro de Custo "RH" está presente em todos os setores que possuem colaboradores. Nele, agrupamos os gastos relacionados a salários, pagamento de variáveis, rescisões, e assim por diante. Por exemplo, no setor Comercial, Administrativo e Financeiro, entre outros, é nesse Centro de Custo que registramos as saídas relacionadas à colaboradores, como salários, benefícios, e demais despesas relacionadas.

A tabela destaca exemplos em que o nome do Setor e do Centro de Custo são semelhantes, o que pode causar confusão. É essencial manter-se atento ao Plano de Contas para evitar equívocos entre esses conceitos.

| Empresa | Setor | Centro de Custo |
|:---|:---|:---|
| Seazone Serviços | Administrativo e Financeiro | Administrativo |
| Seazone Serviços | People | RH |
| Seazone Serviços | Administrativo e Financeiro | Serviços |


### Categorias

As Categorias são subdivisões mais detalhadas dos Centros de Custo. Por exemplo, o Centro de Custo chamado "S.I.G." agrupa cada sistema contratados e utilizado pela Seazone.

Na empresa Seazone Serviços, Setor Comercial, Centro de Custo S.I.G., temos as seguintes Categorias:

| Empresa | Setor | Centro de Custo | Categoria |
|:---|:---|:---|:---|
| Seazone Serviços | Comercial | S.I.G. | API4COM |
| ——————— | ——————— | ——————— | Meetime |
| ——————— | ——————— | ——————— | Pipedrive |
| ——————— | ——————— | ——————— | Pluga |
| ——————— | ——————— | ——————— | Timelines |
| ——————— | ——————— | ——————— | Umbler |

A tabela acima apresenta apenas um exemplo de padrão de categoria. Pela quantidade de Categorias, não seria prático listar aqui todas as Categorias possíveis, mas o rol completo de Empresas, Setores, Centros de Custo e Categorias estão elencados no Plano de Contas.


### Subcategorias

As Subcategorias seguem a mesma lógica das Categorias. É uma especificação ainda maior da Categoria. Atualmente, utilizamos a Subcategoria para especificar a SubSubÁrea do Colaborador no caso dos pagamentos de Salário, Variáveis e Viagens. Outros usos podem vir a ocorrer conforme a necessidade dos gestores.


💡

Cada Colaborador possui uma Matrícula, Setor, Área, SubÁrea e SubSubÁrea. Normalmente, em saídas relacionadas ao RH, a matrícula fica registrada na Atividade e a SubSubÁrea fica registrada na Subcategoria.