<!-- title: Auditoria de Eventos PostHog + Estruturação de Métricas no GrowthBook | url: https://outline.seazone.com.br/doc/auditoria-de-eventos-posthog-estruturacao-de-metricas-no-growthbook-G2HWJlcgoN | area: Tecnologia -->

# Auditoria de Eventos PostHog + Estruturação de Métricas no GrowthBook

Realizei uma auditoria detalhada nos nossos eventos do **PostHog** em 29/01/2026 para limpar o ruído e preparar o terreno para os nossos experimentos no **GrowthBook**. 

**Por que isso foi feito?**

* *Atualmente, temos muitos eventos no histórico que não são mais disparados (eventos "fantasmas"), o que dificulta a criação de métricas precisas. Para organizar os dados, o Growthbook usa uma estrutura de* **[Fact Tables](https://docs.growthbook.io/app/metrics)***, que é muito mais otimizada quando eliminamos esses ruídos.*


**O que foi feito*__:__***

* *Mapeei os eventos que aparecem no PostHog e cruzei com o nosso repositório (Front e Backend) para identificar o que está realmente ativo.*

  \

**os eventos ativos foram cateforizados nestas 8 Fact Tables iniciais*__:__***


1. transactions*__:__* **Pagamento realizado - (Conversão)**

* CHECKOUT - Reserva paga
* BACKEND*__:__* reserva paga

  \


2. search_behavior*__:__* **Funil de descoberta, busca e navegação**

* "BUSCA - busca_na_página_de_resultados",
* "BUSCA - selecionou destino",
* "BUSCA - click_no_imóvel_página_de_busca",
* "BUSCA - nenhum resultado",
* "BUSCA - nenhum resultado - lugares próximos",
* "BUSCA - nenhum resultado - outras datas disponíveis",
* "BUSCA - nenhum resultado - zero resultados",
* "BUSCA - Visualizou Chip de Datas e grid com 3 imóveis",
* "BUSCA - NÃO visualizou Chip de Datas e visualizou um grid com 4 imóveis",
* "Busca - Acessou a página de busca",
* "HOME - Abriu modal de busca mobile",
* "HOME - clique_botão_de_busca_home",
* "HOME - Cicou em um card na home",
* "HOME - Clicou em Buscar no modal de busca mobile",
* "Clique no novo componente de busca",
* "LP - clicou em buscar",
* "LP - clicou em ver preço",

  \


3. property_engagement*__:__* **Engajamento e interações detalhadas com o imóvel**

* "CALENDARIO - Abriu o calendário",
* "IMÓVEL - clicou em reserva whatsapp",
* "IMÓVEL - Clicou em conversar com atendimento",
* "IMÓVEL - Clicou em foto na página do imóvel",
* "IMÓVEL - Clicou em reservar no imóvel",
* "IMÓVEL - Clicou em reservar no rodapé",
* "IMÓVEL - Clicou para ampliar foto na galeria do imóvel",
* "IMÓVEL - Compartilhou os dados da reserva",
* "IMÓVEL - Copiou os dados da reserva",
* "IMÓVEL - Visualizou botão reservar no rodapé",
* "IMÓVEL - visualizou imóvel",
* "Abriu o modal para compartilhar a reserva",
* "Compartilhou os dados da reserva",
* "Copiou os dados da reserva",
* "Entrou na página de detalhes do imóvel",
* "Promocao - Clicou para compartilhar a promoção",
* "Promocao - Clique na Propriedade",
* "Promocao - Clique no link da seção de propriedade",
* "PROMOCAO - Conteudo não encontrado",
* "PROMOCAO - Pagina de erro",
* "Clicou em foto na página do imóvel%",
* "Clicou para ampliar foto na galeria do imóvel%",

  \


4. checkout_conversion*__:__* **Micro-conversões e etapas do fluxo de checkout**

* "CADASTRO - clicou em concluir cadastro",
* "CHECKOUT - Prosseguiu para o pagamento",
* "CHECKOUT - clicou em aplicar - cupom aceito",
* "CONFIRMAR_RESERVA - Clicou em confirmar e pagar",
* "CONFIRMAR_RESERVA - Abriu modal para editar informações",
* "CONFIRMAR_RESERVA - Abriu para leitura os termos e condições",
* "CONFIRMAR_RESERVA - Aceitou os termos e condições",
* "CONFIRMAR_RESERVA - Alterou as informações da reserva",
* "CONFIRMAR_RESERVA - Cupom aplicado",
* "CONFIRMAR_RESERVA - Cupom removido",
* "CONFIRMAR_RESERVA - Escolheu forma de pagamento",
* "CONFIRMAR_RESERVA - Enviou visitorId",
* "CONFIRMAR_RESERVA - Foi redirecionado para o pagamento",
* "Abriu para leitura os termos e condições",
* "Cupom aplicado",

  \


5. system_friction*__:__* **Falhas técnicas, erros de usuário e recusas de pagamento**

* "CHECKOUT - Erro ao confirmar reserva",
* "CHECKOUT - Pagamento falhou",
* "CHECKOUT - Pagamento não autorizado",
* "CHECKOUT - Pagamento rejeitado pelo antifraude",
* "CHECKOUT - Problema com o cartão",
* "CHECKOUT - clicou em aplicar - cupom inválido",
* "CONFIRMAR_RESERVA - Erro ao confirmar a reserva",
* "CONFIRMAR_RESERVA - Erro ao confirmar reserva",
* "CONFIRMAR_RESERVA - Erro de cupom",
* "CONFIRMAR_RESERVA - Cupom inválido",
* "CADASTRO - clicou em concluir cadastro mas tinha erros de input",
* "Cupom inválido",
* "ERROR Erro ao processar a confirmação da reserva",
* "ERROR Erro na validação dos campos da requisição",
* "ERROR Um erro inesperado ocorreu. Por favor, tente novamente mais tarde, ou entre em contato com nossa equipe de atendimento",
* "STARTAR_RESERVA - Erro ao criar reserva pendente",
* "BACKEND - Erro ao criar usuário no Auth0",
* "BACKEND - Fraude bloqueada",
* "BACKEND: pagamento recusado %'"

  \


6. partner_referrals*__:__* **Encaminhamento de tráfego para parceiros**

* "BOOKING - clicou em um destino afiliado na busca",
* "BOOKING - redirecionado para a booking",
* "NÃO OPERADOS - Clique no botão de afiliado dentro do modal",
* "NÃO OPERADOS - Clique no botão de afiliado no banner",
* "NÃO OPERADOS - Redirecionamento direto para afiliado através do experimento",

  \


7. variant_views*__:__* **Exposição e cliques em variantes de experimentos**

* IMÓVEL (CTA RESERVAR WHATSAPP) Visualizou/Clicou na Variante %
* IMÓVEL (CTA RESERVAR) Visualizou/Clicou na Variante %

  \


8. pre_checkin: **Interações operacionais pós-venda**

* PRÉ-CHECKIN - Termos de uso aceitos
* PRÉ-CHECKIN - Clicou em Fale com o atendimento
* PRÉ-CHECKIN - Clicou no link do Guia do Hóspede


\