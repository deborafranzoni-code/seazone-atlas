<!-- title: Template | url: https://outline.seazone.com.br/doc/template-BduQZLLtZz | area: Tecnologia -->

# Template

1. **Resumo do Artefato (O que foi construído? Coloque prints ou links do protótipo/sistema rodando)**

   Foi desenvolvida uma aplicação web que consolida dados de reservas e hóspedes em um resumo simples, claro e confiável para proprietários de imóveis por temporada.

   \
   A solução permite visualizar, de forma objetiva, quais hóspedes se hospedaram em cada imóvel e em quais períodos, organizando as informações necessárias para a emissão de notas fiscais e adequação às novas normas de hospedagem.

   \
   O sistema centraliza os dados de reservas e apresenta um panorama acessível, reduzindo retrabalho manual, aumentando a confiabilidade das informações e proporcionando maior autonomia ao proprietário no cumprimento das exigências legais.

   ![](/api/attachments.redirect?id=c12485ab-a841-4103-8c93-9e643bda56d1 " =1912x891")

   \
   Após o login, o usuário consegue ter uma visualização macro sobre as reservas, seu rendimento, os hóspedes e datas de check-in e check-out. É possível também filtrar por ranges de datas específicas e exportar como XLS, para visualização em planilhas.\n

   ![](/api/attachments.redirect?id=aeff60c2-4700-473e-9c6b-5de2a34496f8 "right-50 =1899x894")



1. **Resultados Conseguidos (O que funciona de ponta a ponta? O que ficou apenas no mock?)**

   
   1. Login via API Sapron
   2. Pesquisa de propriedades do usuário (para filtragem de reservas)
   3. Pesquisa de reservas/receita via rota de calendário (Sapron)
   4. Download do XLS

      \
2. **Ferramentas Utilizadas** 

   
   1. Google AI Studio
   2. Lovable
   3. Google Antigravity

      \
3. **Dores e Limitações (O Aprendizado) (Onde a IA falhou? Onde o Low-code travou? Qual foi a maior dificuldade ao não usar o fluxo tradicional?)**

   \
   
   1.  **Acesso à dados do sistema**

      O desenvolvimento da aplicação foi iniciado pelo mapeamento das rotas de API e dos recursos disponíveis para a construção da solução. Como a arquitetura do projeto não permitia a execução de consultas (*queries*) diretas no banco de dados, a estratégia adotada baseou-se inteiramente no consumo de *endpoints* preexistentes.

      \
      A principal limitação encontrada nesse modelo foi a incompatibilidade entre os dados retornados (ou o comportamento das rotas) e os requisitos da solução planejada. Frequentemente, os *endpoints* não forneciam a totalidade das informações necessárias ou operavam de maneira divergente da regra de negócio esperada.

      \
      De forma específica, a rota utilizada para a busca de reservas por data apresentou dois gargalos centrais: o *payload* de resposta omitia o valor "total" da reserva; e o filtro de período aplicava-se exclusivamente à data de *check-in*, ignorando a data de *check-out* para a composição da janela temporal.

      \
      Outro obstáculo significativo foi a obtenção do CPF dos hóspedes (*guests*). Por questões de controle de acesso, essa informação não fica facilmente exposta para credenciais com perfil de *owner*. Além dessa limitação de permissão, o sistema possui duas fontes distintas para esse dado: `account_user` e `precheckin`. Como o preenchimento do documento não é obrigatório em nenhuma das duas entidades, a falta de uma única fonte de verdade centralizada abre margem para inconsistências no banco de dados.\n
   2. **Dependência de plataforma**

      \
      O projeto foi inicialmente conduzido no Google AI Studio. Contudo, a ferramenta apresentou instabilidades durante o período de uso, além de não oferecer o suporte necessário para uma colaboração ativa e simultânea na construção do software.

      \
      Diante desse cenário, a operação foi migrada para a plataforma Lovable, que se destacou por fornecer recursos nativos de colaboração em tempo real — como edição compartilhada de prompts e ambiente de preview integrado. Apesar desses benefícios, a franquia de créditos da Lovable revelou-se estrita, criando um gargalo que inviabilizou a continuidade do desenvolvimento na ferramenta após um curto período.

      \
      Como solução de contorno, o projeto foi transferido para um ambiente local (Antigravity, do Google). Nessa arquitetura, as restrições de infraestrutura foram superadas: não houve limitação de cotas de requisição, latência elevada ou degradação no comportamento dos modelos. 

      \
      O único trade-off dessa abordagem foi a necessidade de um conhecimento técnico mais abrangente para a configuração do setup inicial e para o deploy da aplicação. Em contrapartida, operar localmente eliminou a dependência de plataformas SaaS (Software as a Service), mitigando os riscos de instabilidade e interrupções.

      \
      Apesar das vantagens do ambiente local, optou-se por retornar ao Google AI Studio assim que os problemas de estabilidade foram resolvidos. Essa decisão teve como objetivo homologar o processo em um ambiente com menor complexidade técnica de infraestrutura e altamente direcionado à prática de vibe coding — onde o ecossistema incentiva o desenvolvimento e a iteração de código guiados estritamente por prompts em linguagem natural.

      \
   3. **Publicação de aplicação**

      \
      Outra dificuldade encontrada foi a publicação do app via ia studio. A funcionalidade retorna um erro "Failed to create Cloud Run service. Please try again" que não conseguimos contornar até o momento.

   \
   
   1. ![](/api/attachments.redirect?id=a87a0eed-c3b5-4c27-b0cd-84f9f3ae90eb " =1194x854")
4. **Próximos Passos Sugeridos (Vale a pena levar para produção? O que falta?)**

   No momento, a solução não está adequada para implantação em ambiente de produção.

   \
   Atualmente, a aplicação utiliza uma combinação de chamadas de API que não supre a totalidade dos dados necessários (como o CPF do convidado) nem garante precisão financeira. Hoje, os valores refletem o período da reserva, quando deveriam basear-se nas datas de receita. Para resolver isso, propõe-se a alteração da rota utilizada para buscar os dados apresentados - de forma a priorizar a busca de dados de revenues (`/owners/{owner_id}/movements/revenues/`) - que busca os dados necessários com maior eficiência e confiabilidade; e oferece os filtros necessários para apresentar os dados de acordo com a seleção do usuário dentro da aplicação.

   \
   A rota `/owners/{owner_id}/movements/revenues/` necessita apenas da adição do dado de CPF do Guest - dado atualmente inexistente.

   \
   Por fim, é necessário adicionar filtro na aplicação (client-side), de forma a permitir o acesso apenas de usuários que possuam a role de Owner.