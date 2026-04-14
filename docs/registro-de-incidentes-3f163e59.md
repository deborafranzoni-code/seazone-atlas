<!-- title: Registro de Incidentes | url: https://outline.seazone.com.br/doc/registro-de-incidentes-EhP13BfEp0 | area: Tecnologia -->

# Registro de Incidentes

Este é o espaço de documentação de incidentes que afetaram os dados do data lake em algum momento. O intuíto dessa página é criar uma espécie de diário de incidentes com as informações necessárias para documentar possíveis marcas permanentes no lake (buracos de dados, interpolações, mudanças de schema, etc.) e servir de histórico para auxíliar na resolução de problemas repetidos.

Abaixo está o template padrão de registros:


---

**Data de início:** <data de início do incidente> ex.: 2025-01-01

**Data de término:** <data de resolução do incidente> ex.: 2025-01-03

**Dados diretamente afetados:**

* *<database>.<tabela>:* <como esses dados foram afetados durante o incidente e descrição de marcas permanentes que continuarão ali pós-incidente (caso tenha alguma), como interpolações, preenchimento de dados, mudanças de schema, mudanças de comportamento de coluna, etc.> ex.:
* *database_1.tabela_1:* Tabela ficou sem dados durante os dias 2025-01-01 e 2025-01-03 e foi realizado uma interpolação linear nos preços destes mesmos dias.
* *database_2.tabela_2:* Dados vieram com valores nulos na coluna X entre os dias 2025-01-01 e 2025-01-05, porém é uma tabela do tipo overwrite então não ficou nenhum problema permanente

**Dados indiretamente afetados:**

* *<database>.<tabela> ou <conjunto de tabelas/dados afetados>:* <como esses dados foram afetados durante o incidente e descrição de marcas permanentes que continuarão ali pós-incidente (caso tenha alguma), como interpolações, preenchimento de dados, mudanças de schema, mudanças de comportamento de coluna, etc.> ex.:
* *tabelas de faturamento:* Tabelas de faturmaneto não foram atualizadas pela duração do incidente e terão os dados de faturamento que incluirem os dias 2025-01-01 a 2025-01-03 afetados pela interpolação da tabela_1

**Tasks e/ou PRs associados:**

* <link para o card/link para PR de resolução do problema> ex.:
* [PR](https://www.google.com/search?q=link+ilustrativo&oq=link+ilustrativo&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIICAEQABgWGB4yCggCEAAYChgWGB4yCAgDEAAYFhgeMgoIBBAAGAoYFhgeMggIBRAAGBYYHjIICAYQABgWGB4yCAgHEAAYFhgeMggICBAAGBYYHjIKCAkQABgKGBYYHtIBCDI3NzZqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8)
* [Card no Jira](https://www.google.com/search?q=link+ilustrativo&oq=link+ilustrativo&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIICAEQABgWGB4yCggCEAAYChgWGB4yCAgDEAAYFhgeMgoIBBAAGAoYFhgeMggIBRAAGBYYHjIICAYQABgWGB4yCAgHEAAYFhgeMggICBAAGBYYHjIKCAkQABgKGBYYHtIBCDI3NzZqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8)

**Descrição do incidente:** <descrição do ocorrido e suas causas raízes> ex.: Scraper X começou a sofrer bloqueios do site Y e ficou sem inserir dados na tabela Z durante o príodo do incidente.

**Descrição da solução:** <descrição do que foi feito para corrigir o problema e de quaisquer processos que tenham sido executados para consertar dados corrompidos/faltantes> ex.: Foi implementado uma nova estratégia de requisições no scraper X que fez ele voltar a coletar dados do site Y. Também foi aplicado uma interpolação linear feita em Glue para as datas que ficaram sem dados.

**Observações adicionais:** <informações extras pertinentes para o caso que não se enquadram nos outros campos> ex.: O script de interpolação foi salvo neste job [aqui](https://www.google.com/search?q=link+ilustrativo&oq=link+ilustrativo&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIICAEQABgWGB4yCggCEAAYChgWGB4yCAgDEAAYFhgeMgoIBBAAGAoYFhgeMggIBRAAGBYYHjIICAYQABgWGB4yCAgHEAAYFhgeMggICBAAGBYYHjIKCAkQABgKGBYYHtIBCDI3NzZqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8) e pode ser usado como template para interpolações futuras.


---

Favor adicionar novas entradas de logs em ordem cronológica baseado na data de início do incidente, sempre adicionando novas entradas acima das antigas (quanto mais novo, mais pra cima no documento) e separados pela linha separadora do outline.

# Incidentes


---

**Data de início:** 2025-08-06

**Data de término:** 2025-08-07

**Dados diretamente afetados:**

* *seazone_real_data.raw_reservations:* Tabela do tipo overwrite, portanto apenas não foi atualizada no dia do incidente, mas voltou ao normal assim que a solução foi implementada

**Dados indiretamente afetados:**

* *tabelas seguintes do fluxo de real data:* Dados ficaram desatualizados apenas até a implementação da solução, nada permanente

**Tasks e/ou PRs associados:**

* [PR 1](https://github.com/seazone-tech/pipe-lake/pull/422)

**Descrição do incidente:** Lambda de reservations do schema real_data deu timeout e acabou não atualizando a tabela neste dia.

**Descrição da solução:** Lambda de reservations foi separado em 2, dividindo a carga melhor e aumentando o tempo que cada lambda tem para executar sua tarefa.

**Observações adicionais:**


---

**Data de início:** 2025-09-15

**Data de término:** 2025-09-23

**Dados diretamente afetados:**

* *Modelo de predição de blockDetection no Sagemaker*

**Dados indiretamente afetados:**

* \

**Tasks e/ou PRs associados:**

* Não há

**Descrição do incidente:** No dia 15/09/2025 o pipeline do Sagemaker BlockDetectionNNSPipelineProd teve falha de execução. Inicialmente foi feito uma análise comparativa dos logs da execução bem sucedida e da que falhou e foi descoberto que teve uma mudança do ambiente de execução com um downgrade da versão do Python (3.9 para 3.8) para as bibliotecas scikit-learn e pandas. Na investigação, encontrei que isso já é um bug conhecido <https://github.com/aws/sagemaker-scikit-learn-container/issues/249> e que a AWS necessita fazer um novo release da imagem para corrigir esse bug.


**Descrição da solução:** Como medida paliativa, foi realizado a implementação de uma imagem customizada para rodar os jobs no container ao invés da imagem da AWS. A imagem foi registrada no ECR e depois incorporada ao código-fonte  do notebook de create_pipeline.ipynb no Sagemaker AI Studio. Além disso, ao realizar a nova execução, a instância que rodava a parte do pipeline com os dados do Lake estourou a memória, então tive que aumentar o tamanho da instância no código do notebook para fazer funcionar.

**Observações adicionais:**