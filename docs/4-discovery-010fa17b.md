<!-- title: 4 Discovery | url: https://outline.seazone.com.br/doc/4-discovery-cfhwfbkSna | area: Tecnologia -->

# 4 Discovery

[Entrevista](/doc/entrevista-0WyuCPTbAO)

## Levantamento de dados

* **Qual o tempo médio de onboarding dos 3 últimos meses?** 20 dias
* **Quantidade de Imóveis em onboarding no último mês?** 100 imóveis
* **Quanto tempo leva cada etapa de onboarding?** 2 a 3 dias para todas as etapas, exceto adequação (que varia de acordo com o imóvel)
* **Quais indicadores gerenciais o comercial/onboarding utilizam hoje?** *por exemplo a quantidade de chamados no CS (telefone, email e whatsapp) relacionados a isso.* O onboarding não gera demanda de atendimento para o CS, apenas após o anúncio estar ativado. Quanto ao Comercial, esta demanda é gerada somente se o processo de Onboarding estiver demorando muito
* **Quantos formulários são preenchidos no processo de onboarding?** 5 google forms e 2 planilhas excel

## Qual o problema queremos resolver?

Após pesquisa inicial, verificamos a duplicidade de informação no fluxo atual do processo de onboarding de proprietários. Isso gera um trabalho de inclusão de dados pelo time do comercial e onboarding, o que torna o processo moroso e gera um retrabalho ao time do onboarding.

Atrelado a isto verificamos a falta de visibilidade dos proprietários e anfitriões neste fluxo através da aplicação, de forma que a comunicação do processo atual de onboarding é realizada manualmente através de mensagens via WhatsApp.

Ao dar visibilidade ao fluxo do Onboarding ao proprietário, além de deixar o processo mais transparente para o cliente a intenção é diminuir ou até eliminar a necessidade de entrar em contato com CS e questionar como está o andamento do onboarding e o motivo da demora em disponibilizar imóvel para a locação de temporada.

Ao dar visibilidade ao fluxo do Onboarding ao anfitrião, a intenção é fazer com que o franqueado possa se planejar melhor quanto a atuação do mesmo no imóvel para realizar a vistoria. Atualmente esta informação não está disponível no Sapron.

Para os times envolvidos, eliminar a demora na passagem de bastão entre áreas e processos, que também pode gerar mais atrasos no tempo total de onboarding. Há também problemas frequentes de duplicidade de criação de imóveis, proprietários e listings o que atrapalha a visibilidade no Sapron e gera insatisfações em todos os elos (proprietários, onboarding, tech)

## Porque este problema é importante?

* Hoje, temos aproximadamente 100 imóveis em onboarding, o acompanhamento é feito apenas por planilhas e poucas pessoas. Quem tem acesso e sabe onde estão os dados é que podem dizer a situação de cada uma dos imóveis e repassar aos gestores e aos proprietários e anfitriões. A forma que trabalhamos não é escalável e impossibilita uma visão geral do onboarding.
* A resolução das oportunidades mencionadas tornam o processo de onboarding mais fluido e produtivo, uma vez que os dados não precisam ser preenchidos em duplicidade, eliminando o preenchimento de formulários e centralizando suas ações no Sapron, fazendo com que o time do onboarding priorize as etapas que ainda não foram tratadas pelo time do comercial. Além disso, a disponibilização do fluxo de onboarding ao anfitrião e ao proprietário, deixam o processo mais transparente e atrativo para o cliente. A automatização desta comunicação através do Sapron facilita o processo para o time de onboarding centralizando seu fluxo de trabalho no Sapron.

## Como resolveremos este problema?

* Centralizando as informações no Sapron do processo de Onboarding. Ao disponibilizar a lista de Proprietários integrando dados relevantes do pipedrive e vinculando os listings criados, lista de Propriedades atualizada, a intenção é simplificar o processo de onboarding para o time, que terá acesso a dados previamente preenchidos pelo time do comercial e ota, eliminando o preenchimento de dados em duplicidade ou triplicidade, dando mais visibilidade ao processo.
* Além disso, através da atualização de status de onboarding à medida que suas etapas avançam, tornaremos melhor os indicadores de gerenciamento. Estas atualizações serão enviadas para o proprietário e anfitrião, tornando o processo mais transparente para ambos usuários e assim, diminuindo chamados de CS relacionados a onboarding

## Dentro do escopo deste MVP


1. Lista de proprietários
2. Lista de propriedades (Além das informações do comercial, dependem das informações validadas de comodidades realizado pelo anfitrião), com funcionalidade de atualização do status do onboarding e detalhamento da etapa (data de entrega das chaves, período de adequação, data da vistoria terceirizada etc). Na lista de propriedades devemos inserir os listings ativos com seus dados e a opção de redirecionamento para criar os listings que ainda não foram criados
3. Botão de Gerar login proprietário (onde o login seria reenderizado na Lista de proprietários)
4. Fluxo de andamento do onboarding (Para anfitrião e proprietário), somente visualização

## Fora do escopo deste MVP


1. Opção de inserir proprietário com residência no exterior (Pesquisar API que fornece esses dados ou colocar um check-box 'Proprietário reside no exterior', habilitando os inputs para preenchimento manual;
2. Criação de Login e senha para acesso ao proprietário no Sapron (refatoração de Novo Proprietário em que seja apenas necessário criar o Login e os demais viriam preenchidos de acordo com os dados provenientes do pipedrive)
3. Mensagem de erro quando o imóvel já está cadastrado (assim como ocorre quando o proprietário já está cadastrado);
4. Disponibilizar a rota multicalendar para o onboarding;
5. Retirar a parte de 'Dados para nota fiscal' e considerar que os dados para nota no financeiro serão em nome do proprietário (Em caso de proprietários com residência no exterior, a emissão de nota é realizada com o endereço do imóvel do proprietário);
6. Página de acompanhamento permita visualizar o fluxo de onboarding sem ser necessário exportar csv e tratar dados em planilhas;
7. Permitir edição de dados do proprietário ou do imóvel que já podem ser feitos pela tela de Editar Dados;
8. Comunicação por email/mensagem de forma bonita (cheia de fru…fru)

## Oportunidades futuras:

* Preenchimento das comodidades específicas pelo anfitrião diretamente pelo SAPRON durante a etapa de vistoria para que o time do Atendimento tenha maior visibilidade das comodidades do imóvel e possa melhorar o tempo de seu atendimento. Além disso, o preenchimento direto no forms facilitaria para o time da OTA a etapa de criação de anúncios, centralizando as informações no SAPRON.