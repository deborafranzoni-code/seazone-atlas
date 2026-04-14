<!-- title: 3. Brainstorming | url: https://outline.seazone.com.br/doc/3-brainstorming-4OWSTWZp2e | area: Tecnologia -->

# 3. Brainstorming

Problemas & Oportunidades

| Tipo de correção | **Oportunidade** | **Justificativa** | **Solução sugerida** |
|----|----|----|----|
| Feature | Na sessão Financeiro, o grid principal apresenta os dados referentes a todos os imóveis, ele mostra o somatório referente a cada mês, tanto de repasses quanto de saldo devedor (taxa implantação, despesa), não ficando claro ao que estes valores se refere. Isto também se aplica ao extrato financeiro. |    | Detalhar tanto na sessão do financeiro quanto no extrato a somatória do valor, como por exemplo: |

Receita: Imóvel: Data de lançamento 03/05 |LC2022 | Check-in 23/05 Check-out 03/06 | Valor: 842,00 Data de lançamento 03/05 ILC1012 | Check-in 12/5 Check-out 30/05  | Valor: 953,00

Total de receitas do mês: R$1795,00 Despesas:

Data de lançamento 03/05 | Manutenção (material, mão de obra, etc) - Manutenção da Janela | Valor: 100,00 Data de lançamento 04/05 | Taxa de implantação onboarding (1/4) | 250,00

Total de débitos do mês : 350,00 | | Feature | O Valor do Repasse, deve ser exatamente o valor da TED realizada naquele mês, não mostrando o valor do Saldo disponível em carteira |  | Incluir na sessão 'carteira' uma linha que represente o Saldo disponível (que representa o valor saldo total do mês, menos o saldo devedor, menos o repasse)

Sugestão de legenda: Saldo a ser repassado Saldo em carteira Saldo disponível em carteira | | Feature + Fix | A importação de relatório de Hóspedes para declaração da receita federal se dá através de CSV, o que dificulta a visualização dos dados.

Além disso nesta relação não aparecem as reservas canceladas.

O relatório de Lista de hóspedes é exclusivo para realizar o imposto de renda, pois em seu detalhamento aparecem hóspedes referentes ao mês anterior e subsequente. Desta forma os valores somados de reserva será um valor superior ao mês de repasse, podendo gerar dúvidas ao proprietário |  | Dar a opção de baixar o relatório em CSV e também em PDF para que a visualização de dados seja otimizada.

Incluir a coluna de status: Reservas aprovadas ou Reservas com NoShow

Alterar a label de Lista de Hóspedes para Lista de hóspede - Imposto de renda

| | Refactor | Na sessão de Despesas o grid alternando cor cinza e verde gera um pouco de confusão pois o verde remete a despesa validada. |  | Reestruturar a sessão melhorando a usabilidade (espaçamento de colunas no desk), cores das linhas | | Refactor | Visualização Mobile: Praticamente todas as sessões estão muito ruins de ver no mobile, o que dificulta a visualização de dados.

|  | Acompanhamento financeiro: Mostrar na tela apenas o mês de referência e não os meses subsequentes a partir de janeiro. Exemplo: Julho: (valores). Ao passar para o lado mostra somente o mês de Agosto na tela. | | Feature | Foi verificado que os proprietários tendem a acessar a página com mais frequência no mês do fechamento |  | Pensar em ações que tendem a estimular o proprietário a acessar a página com maior frequência. Por exemplo: push notification quando o imóvel recebe uma reserva, uma despesa ou outras informações que ocorrem anteriormente à semana do fechamento. | | Refactor | Mobile: A rota de detalhes do imóvel está péssima a visualização em relação ao layout e espaçamento das sessões da página.

Desk: o calendário de visualização de reservas quanto a "linha" que demarca o período da reserva o bloqueio é confuso. Exemplo: A faixa verde não deixa claro em qual mês está iniciando e finalizando a reserva, isso tende a piorar de acordo com o aumento da tela de visualização. |

| Mobile:

Diminuir o espaçamento das seções de acordo com o Design System; Otimizar a visualização do calendário, ícone da plataforma, label da reserva, valor da reserva e faixa colorida referente ao período da reserva ou bloqueio do imóvel. Além disso quando tempos reservas com out in no mesmo dia, o período demarcado fica aparecendo em apenas uma linha, o que torna ainda mais difícil a visualização.

Desk: Verificar no analytics e no hotjar quais os tamanhos de tela utilizados e assegurar que naqueles formatos de tela a visualização do calendário esteja clara e coerente. | | Feature | Ao solicitar o bloqueio para terceiros, não é repassado a informação do telefone de contato do hóspede 'convidado', o que torna o processo de check-in um pouco dificultoso. | Facilitar a comunicação do pré check-in e check-in do hóspede 'Convidado' | Ao solicitar o bloqueio, o proprietário deve selecionar 'Uso próprio' ou 'Uso para terceiros', quando for selecionado o Uso para terceiros, o proprietário deve incluir o nome do hóspede principal e pelo menos um telefone para contato. | | Fix | Na rota de 'Meus dados' na sessão de dados bancários, os dados incluídos no input de Agência aparecem com muitos zeros na frente, fazendo com que o time do financeiro tenha que exportar e manipular os dados para retirar os zeros.

No input de Nome dos destinatários é necessário realizar mensalmente também um regex para que seja retirado os acentos e caracteres especiais, pois o banco não aceita os caracteres especiais |  | Ao salvar no DB os dados bancários, assegurar que está sendo passado somente os dígitos válidos (agencia e conta corrente), sem os zeros na frente do do value.


Ao salvar no DB o nome do destinatário deve ser salvo sem os acentos e caracteres especiais (criar talvez mais uma key, que guarde este dado que será exportado para o banco e manter a key que guarda o nome correto) | | Feature | Ao setar a conta bancária para a qual deve ser passada a receita de determinado imóvel, se houver duas ou mais contas no Banco do Brasil (por exemplo) fica difícil para o proprietário identificar na lista do select qual conta se refere a determinada pessoa (pois no select aparece somente o nome do banco. |  | No formulário de dados bancários, incluir a opção de 'Apelido' para conta, onde o usuário possa inputar um nome que melhore na hora setar os repasses de cada imóvel e incluir os últimos dígitos da conta para melhorar a identificação. Por exemplo: 'Principal - 104 Caixa econômica - CC8954''Renata - 104 - Caixa econômica - CC5578' | | Refactor | A sessão de gerenciamento de imóveis fica distante da sessão de dados bancários | Melhorar a usabilidade | A sessão de gerenciamento deve vir logo após a sessão de dados bancários. | | Fix | Na sessão de telefones para contato aparece um 'Teste' no select.

Além disso, verificar nas ferramentas de métricas se esta sessão está sendo utilizada |  | Retirar o 'Teste' do select.

Se for verificado que a sessão não é utilizada repensar se é importante ou não manter.  | | fix |  |  |

| |  |  |  |  | |  |  |  |  | |  |  |  |  |