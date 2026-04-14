<!-- title: Documentação do Usuário | url: https://outline.seazone.com.br/doc/documentacao-do-usuario-DaVluflQNu | area: Tecnologia -->

# Documentação do Usuário

# Acesso

* Abra o seu navegador e digite o endereço: <https://mapa-de-calor-poligonos-352882589845.us-central1.run.app>
* Será solicitado que você faça login no site. Para isso, utilize sua conta Seazone, caso contrário, o site não permitirá o seu acesso.

# Componentes da aplicação

## Menu Lateral

Na esquerda do site, há um menu lateral que contém possibilidade de filtros e parâmetros.

 ![](/api/attachments.redirect?id=e669d8cb-b1dd-4d57-bd4e-5194d29dea53 " =211.5x433.5")

* É possível filtrar geograficamente (por estado, cidade e polígono)

  \
* É possível escolher uma frente de análise
  * As frentes de análise atualmente disponíveis são:
    * Preço ofertado: compara o preço anunciado por grupo (Strata+Quartos) com a referência do polígono.
    * Reservas: compara o valor médio reservado por grupo com a referência do polígono.
    * Demanda: compara o volume de registros de reserva por grupo com a referência do polígono. 

  \
* É possível escolher um valor de discrepância mínima. 
  * Nesse filtro são filtrados polígonos que possuem pelo menos um grupo com DISCREPÂNCIA maior ou igual ao valor que for selecionado no filtro. 
  * A discrepância é calculada por grupo (Strata + Quartos) comparando o valor do grupo com a referência do polígono. 
  * Não importa se o grupo está acima ou abaixo da referência, o que importa é o TAMANHO da discrepância. 
  * Exemplo: • Discrepância mínima = 0.20 (20%). • Grupos a +20% ou -20% aparecem no mapa. • Grupos a +19% ou -19% não aparecem. 
  * Regra do mapa: Se nenhum grupo dentro do polígono atingir essa discrepância mínima, esse polígono não aparece no mapa.

  \
* É possível escolher um score mínimo:
  * Nesse filtro são filtrados os polígonos com score >= ao valor selecionado. 
  * Score = média ponderada (pela quantidade de imóveis em cada grupo) da discrepância absoluta dos grupos.

    \
* É possível escolher o número mínimo de imóveis por grupo:
  * Remove grupos (Strata + Quartos) com poucos imóveis antes de calcular referência, discrepância e score.

    \
* É possível ativar o modo de análise por imóvel:
  * Selecione um polígono para habilitar a análise por imóvel.
  * Ative para ver os imóveis (pins) apenas dentro do polígono selecionado.


* É possível visualizar informações sobre a qualidade dos dados:
  * Algumas métricas por imóvel podem ficar instáveis quando há poucos registros.
  * Para evitar instabilidade, são marcados como cinza (sem valor) imóveis com pouca amostra. 
  * O número mínimo de registros para as frentes de análise variam com base na distribuição dos dados. Por isso, o código sempre verifica qual é o melhor limiar com base nos dados atuais.

## Parte superior ao mapa de calor de polígonos

Essa parte do site possui informações gerais e norteadoras para a interpretação dos dados da aplicação. Há um espaço para detalhamento de informações e a legenda de cores usadas no mapa.

 ![](/api/attachments.redirect?id=7922df63-aaee-441e-aee2-edefbf93c303 " =378x216.5")

## Mapa de calor de polígonos: visão macro

Oferece uma visualização dos polígonos (por frente de análise), e permite que o usuário visualize informações sobre cada polígono ao passar o mouse em cima do polígono.

 ![](/api/attachments.redirect?id=5d188e3b-6556-4cba-a72b-ff40dedd9fa0 " =670.5x335.5")

 ![](/api/attachments.redirect?id=99b093bb-6ed6-4478-b732-769a0952a763 " =380.5x145")

*OBS: Também é possível expandir o mapa na tela clicando na seta dupla que se encontra no canto superior direito do mapa:*

 ![](/api/attachments.redirect?id=9db901e6-0fa7-4da2-80e7-1f3af00fcb26 " =695x341")

## Mapa de calor de polígonos: análise por imóvel

Para uma visão mais detalhada, é possível ativar a análise por imóvel. Nela se pode:

* Filtrar por um ou mais grupos
* Visualizar dados de cada imóvel pertencente ao polígono previamente selecionado.

  OBS: No mapa também é informado o que cada cor do pin do imóvel significa.

 ![](/api/attachments.redirect?id=68a6bc39-e981-4e7c-a6ae-9d4822853979 " =689x374")

 ![](/api/attachments.redirect?id=7f220a4e-9fa8-40b6-ac4f-c256545d7b79 " =261x160")

## Tabela de KPI**s por polígono na frente de análise selecionada**

Nessa tabela é possível filtrar por estado, cidade, polígono (um ou mais) e visualizar informações a nível polígono. Além da visualização do mapa, é possível ver de modo tabular também.

 ![](/api/attachments.redirect?id=e5af4143-6504-48eb-a729-57573167459c " =658.5x320.5")

*OBS: É possível fazer download das informações que estão na tabela, pesquisar na tabela e expandir a tabela*

 ![](/api/attachments.redirect?id=2090205d-a575-4493-adbe-6d649b60e841 " =659x199")

## Tabela de d**etalhamento por grupos (Strata + Quartos)**

Nessa tabela é possível ver os dados de modo mais granular, a nível grupos. Nesse caso, apenas aparecerão na tabela os polígonos contidos no estado e cidade selecionados no menu lateral. 

 ![](/api/attachments.redirect?id=514ce74c-84e8-40f2-92cb-a5f32de1a43f " =654x375.5")

# Atualização dos dados

* Um Cloud Scheduler chamado: `**atualiza_tabelas_mapa_de_calor**`
* Executa **1x por dia às 09h** (diariamente)