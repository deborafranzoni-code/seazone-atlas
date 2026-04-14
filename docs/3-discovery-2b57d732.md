<!-- title: 3 Discovery | url: https://outline.seazone.com.br/doc/3-discovery-GBFt11olzS | area: Tecnologia -->

# 3 Discovery

## Levantamento de dados

Inclua aqui, dados relevantes que justifiquem o desenvolvimento do produto. Você pode inserir gráficos, relatos de retorno de entrevistas, prints de imagens de pesquisa de formulário de NPS e o que mais achar relevante dos dados levantados durante o desenvolvimento da pesquisa.

 ![Contagem de Status(1).png](3%20Discovery%2083488a1f3e43474f9ed5c56f1798bfc5/Contagem_de_Status(1).png)

**Qual a média de danos reportados por mês?** *A média mensal de danos reportados por mês é de 41, podendo variar de 22 a 161 nos meses de maior procura.*

**Qual o tempo médio de resolução do dano (inclui o dia da entrada do dano e a data final de resolução)** *20 a 30 dias*

**Quantos dias o atendimento tem para reportar o dano de acordo com a plataforma?** *Airbnb: 14 dias após o checkout Booking: 7 dias após o checkout*

**Quantos dias o atendimento tem para tentar solucionar o caso antes de dar como 'Perdido'?** *Não há padrão definido para a finalização e desistência de cobrança*

**De quantos em quantos dias o atendimento deve entrar em contato com o hóspede para fazer a cobrança?** *Tentativas de contato são diárias. Cobrança Airbnb de 2 a 3 dias até acionamento do seguro.*

**Qual o tempo que o financeiro leva para realizar o repasse para o dono do reembolso? -**

**Em que momento é reportado ao proprietário que houve um dano no seu imóvel?** *Depende do proprietário e depende do dano, danos miúdos (copos, taças, talheres) não são reportados. Danos maiores (estruturais, móveis) são reportados para evitar surpresas para o proprietário. Entretanto, tem proprietário que gosta de saber de tudo e  fiscaliza todos os danos.*

**Em quais casos de não sucesso o jurídico deve ser notificado?** *Seria em todos os casos perdidos.*

## Qual o problema queremos resolver?

Eliminar o processo de danos de hóspedes que atualmente é feito por planilhas em todo o seu processo, desde o registro do dano realizado pelo anfitrião, passando pela mediação de cobrança realizada pelo tome do atendimento, até a o repasse ao dono do reembolso que é realizado pelo time do financeiro.

Nos casos em que a cobrança é realizada diretamente pelo anfitrião a etapa de mediação pelo time do atendimento não ocorre.

Além da melhora no fluxo de trabalho o processo atual não dispõe de visibilidade para outros times envolvidos como os proprietários e os anfitriões (após o lançamento do dano), setor jurídico (que precisa ser notificado para quaisquer danos ou multa no imóvel).

## Porque este problema é importante?

A resolução desta oportunidade torna o processo de danos com maior controle através da visibilidade de todos os clientes envolvidos, eliminando as planilhas e centralizando suas ações unicamente no Sapron. Esta unificação faz com que a comunicação entre os envolvidos fique mais clara e organizada, de forma que não será mais necessário manipular várias planilhas de controle de danos entre os usuários que são responsáveis por cada etapa de controle do processo.

## Como resolveremos este problema?

Para que esta oportunidade seja solucionada de forma mais ágil o time de discovery pensou em uma solução que envolve reaproveitamento de componentes que já estão desenvolvidos dentro do Sapron (utilizando como modelo a tela de acompanhamento do onboarding) e criação de novos componentes para que todos os clientes possam ter acesso e acompanhar o processo de danos, preenchendo os dados que compete a cada time.

Centralizando o processo em uma única página que pode ser filtrada por imóvel, data de check-out, status ou reembolso recebido, o usuário poderá navegar entre as etapas de acompanhamento do dano, de forma que cada usuário será responsável por atualizar as etapas que compete a cada setor. As etapas que não compete ao setor de atendimento (por exemplo) ficariam apenas para visualização deste time.

Para os proprietários que desejam acompanhar os danos no imóvel (o atendimento deve sinalizar se a comunicação deve ser feita ou não no preenchimento do formulário) pensamos em disponibilizar a rota de danos para o proprietário, em que este consiga visualizar os danos referente ao seu imóvel, podendo este acompanhar em qual etapa se encontra o processo.

Para os danos que não tiveram sucesso de cobrança, pensamos em realizar a sinalização ao setor jurídico por email ou slack para que este se encarregue do encaminhamento quando for relevante dar continuidade a cobrança.

## Dentro do escopo deste MVP

\-Criar rota Danos de hóspede para os usuários Anfitrião, Atendimento e Financeiro; -Dentro da roda de Danos de hóspede deverá ser possível Inserir Danos (Anfitrião) na etapa de Detalhes do Dano; inserir dados de tratativas de cobrança (Atendimento) na etapa de Histórico e tratativas de cobrança; inserir dados de repasse (Financeiro) na etapa de Reembolso do Dano e atualizar o status do processo (Atendimento) na etapa de Status. As etapas mencionadas devem ser inseridas pelos usuários e visualizada pelos demais; -Criar formulário de inserir danos e eliminar formulário do Google; -Criar formulário de histórico e tratativa de cobrança, bem como formulário de reembolso, eliminando a planilha sheets e melhorando a visibilidade do processo de danos para todos os usuários envolvidos

## Fora do escopo deste MVP

\-Criar rota de visualização de danos nas propriedades para o Proprietário

\-Fazer a comunicação com o setor jurídico quando o dado é 'Perdido', via Slack ou Email.

## Oportunidades

\-Eliminar a planilha do atendimento de 'Problemas a resolver', onde se encontra várias abas de controle e centralizar todas a as ações no Sapron.