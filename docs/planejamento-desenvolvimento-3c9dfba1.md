<!-- title: Planejamento & Desenvolvimento | url: https://outline.seazone.com.br/doc/planejamento-desenvolvimento-5hUOquDBPU | area: Tecnologia -->

# Planejamento & Desenvolvimento

# Documentação Inicial

## 1. Introdução

Este documento apresenta a descrição inicial do projeto **Analise de Faturamento 2.0**, que tem como objetivo desenvolver uma nova versão da planilha utilizada para estimar o faturamento de concorrentes da Seazone nos últimos 12 meses. A versão anterior da planilha alimentava-se de dados coletados do Lake, contendo informações de preço médio, faturamento e taxa de ocupação, e utilizava várias regras e árvores de decisão para flexibilizar os critérios de filtro, visando trazer um maior número de concorrentes para análise.

Nesta nova versão, iremos começar do zero, inicialmente sem flexibilizar os filtros. A ideia é, em ciclos subsequentes e com interação direta com o cliente, flexibilizar os critérios e adicionar melhorias conforme necessário. 

## 2. Objetivos do Projeto

* **Desenvolver a versão 2.0 da planilha**, começando do zero e reformulando a árvore de decisão existente.
* **Retornar informações sobre concorrentes e IDs da Seazone**, obedecendo aos filtros estabelecidos inicialmente.
* **Permitir validação rápida pelo stakeholder**, através de entregas menores e mais frequentes.

## 3. Equipe do Projeto

* **Responsáveis pelo Desenvolvimento**: Patrick de Sousa e Anderson Pimentel
* **Revisor**: Lucas Abel
* **Stakeholder**: Bruno Bill Benetti

## 4. Ciclo 1

### 4.1. Objetivos do Ciclo 1

* **Elaborar uma nova planilha**, começando do zero, com a reformulação da árvore de decisão existente.
* **Incluir os imóveis Seazone** no mesmo template dos concorrentes.
* **Aplicar os critérios de seleção** sem qualquer flexibilização inicial.

### 4.2. Escopo do Ciclo 1

* **Persistir a informação de "strata" no Lake**.
* **Refazer o output da seleção automática de listings**, aplicando todos os critérios sem relaxamento e incluindo os imóveis Seazone.
* **Fornecer o output em planilha ou CSV**, para que o stakeholder possa validar a precisão dos dados em diferentes regiões.
* **Foco na funcionalidade e precisão dos dados**, sem a necessidade de investir tempo em layout da planilha ou desenvolvimento de scripts adicionais além da requisição de API e plotagem dos dados.

### 4.3. Critérios de Seleção Aplicados

Os seguintes critérios serão aplicados na seleção dos listings:


 1. **Faturamento dos últimos 12 meses** diferente de 0 e não nulo.
 2. **Data do último comentário** menor que 180 dias.
 3. **Número de comentários** maior que 10.
 4. **Nota do listing** maior que 4,5.
 5. **Taxa de ocupação anual** entre 10% e 90%.
 6. **Diária média**: manter a lógica atualmente codificada para validação.
 7. **Média de bloqueios por mês** menor que 20.
 8. **Strata**: incluir esta informação no output.
 9. **Tipo de Imóvel (Listing Type)**.
10. **Número de Quartos**.
11. **Bairro**.

### 4.4. Etapas do Ciclo 1


1. **Planejamento do Novo Layout da Planilha**
   * Elaborar o layout básico necessário para acomodar os dados e enviar para aprovação do stakeholder, se necessário.
2. **Definição da Infraestrutura**
   * Configurar as queries e funções Lambda necessárias para coletar e processar os dados do Lake.
   * Persistir a informação de "strata" no Lake, integrando dados de diferentes fontes.
3. **Desenvolvimento da Planilha**
   * Implementar as funcionalidades diretamente na planilha, sem a necessidade de scripts adicionais além da requisição de API e plotagem dos dados.
   * Incluir os imóveis Seazone no mesmo template dos imóveis não-Seazone.
4. **Teste Interno e Ajustes**
   * Realizar testes internos para garantir que os critérios de seleção estão sendo aplicados corretamente.
   * Ajustar quaisquer inconsistências ou erros identificados durante os testes.
5. **Entrega para Revisão do Stakeholder**
   * Fornecer o output em planilha ou CSV para o stakeholder.
   * O stakeholder poderá rodar algumas regiões e validar se o output está correto.

### 4.5. Prazo e Feedback

* **Prazo de Entrega**: A planilha será entregue ao stakeholder ao final das etapas acima.
* **Feedback do Stakeholder**: O stakeholder terá até **2 dias** para retornar com feedback e sugestões.
* **Ajustes Pós-Feedback**: Com base no feedback, serão feitos os ajustes necessários antes de avançar para o próximo ciclo.

### 4.6. Template 

[\[TEMPLATE\]-Análise de Faturemanto 2.0](https://docs.google.com/spreadsheets/d/1xns3JcpidMG2S4Gt-_G4IV4KH0kOHIyA3xFEN-kokt0/edit?gid=971245834#gid=971245834)


 ![](/api/attachments.redirect?id=c9ffe5a2-5502-4640-a63a-e4fb62b8f94e " =1281x899")


Teremos apenas 3 abas, com as colunas indicadas no template. Segue as abas: 

* imóvel: Com as entradas iniciais definidas para o filtro

  ![](/api/attachments.redirect?id=22201c9f-a71a-4e98-92fa-65f005c5f2b7 " =567x180")

  \
* **Listings Selecionados: Com as colunas a baixo:** 

  ![](/api/attachments.redirect?id=9efbce9e-a56d-4035-9856-cf87a99c4bba " =1247x73")

  \


* **FAT_SELECIONADOS: Com retorno dos faturamentos dois últmos 12 meses.**

  ![](/api/attachments.redirect?id=81feeb7d-15a2-4afd-91a3-20b071219ee7 " =1515x207")

  \

## 5. Próximos Passos

Após a validação inicial pelo stakeholder:

* **Analisar o Feedback**: Entender se os critérios aplicados atendem às necessidades ou se é necessário alterar alguma regra de negócio inicial.
* **Flexibilizar os Critérios**: Iniciar o trabalho nas regras de negócio para relaxar os critérios, conforme a necessidade identificada.
* **Adicionar Melhorias**: Incluir mensagens de erro e outras funcionalidades adicionais, evitando retrabalho desnecessário antes da validação inicial.

## 6. Considerações Finais

* **Comunicação Contínua**: Manteremos contato direto com o stakeholder em cada fase do processo, visando minimizar erros e alinhar expectativas.
* **Entrega de Valor**: Priorizar entregas menores e funcionais para validação rápida, garantindo que o desenvolvimento esteja alinhado com as necessidades do negócio.
* **Foco na Funcionalidade**: Inicialmente, o foco será na precisão dos dados e na aplicação correta dos critérios de seleção, adiando preocupações com layout e funcionalidades adicionais para ciclos posteriores.


---


# Documentação de Desenvolvimento – Ciclo 1

## 1. Visão Geral do Ciclo 1

O Ciclo 1 do projeto **Análise de Faturamento 2.0** tem como principal objetivo a criação de uma nova planilha para estimar o faturamento de concorrentes da Seazone, integrando os imóveis Seazone com os concorrentes, sem a flexibilização dos critérios de seleção. O foco na coleta e processamento de dados, com o objetivo de entregar um modelo funcional para validação inicial.

### **Objetivos do Ciclo 1**

* Criar a planilha com a seleção automática de listings.
* Incluir os imóveis Seazone no mesmo template dos concorrentes.
* Validar a precisão dos dados com a aplicação dos critérios de seleção.
* Entregar a planilha para feedback do stakeholder.

## 2. Planejamento e Layout da Planilha

O layout da planilha foi desenvolvido e aprovado, contendo as três abas essenciais:


1. **Imóvel**: Filtros iniciais para os listings.

   \
   ![](/api/attachments.redirect?id=e8573583-dbeb-4b0d-9a34-a2208e3c2490 " =552x165")

   \
2. **Listings Selecionados**: Resultados da seleção, com as informações dos imóveis.
   * **ID Listing: Id airbnb**
   * **Bairro: Bairro especificado na nossa tabela location**
   * **Cidade: Cidade espcificado na nossa tabela location**
   * **Estado: Estadp especificado na nossa tabela location**
   * **TO anual: Taxa de ocupação anual útil, calculada pelo total de ocupação sobre os dias disponíveis( não bloqueados )**
   * **Diária média: Preço médio da diária no ano.**
   * **Quartos: número de quartos do listing**
   * **Link: emdereço URL do anúncio**
   * **Dias úteis: Tptal de doas disponíveis no ano**
   * **Tipo: Apartamento, Hotel ou Casa**
   * **Padrão: Qualidade do imóvel definido por strata SIM, JR, SUP, TOP ou MASTER**
   * **ID_SEAZONE: Indica se o listing é ou não um imóvel da Seazone**
3. **FAT_SELECIONADOS**: Dados de faturamento dos últimos 12 meses dos imóveis selecionados.
   * As colunas indicam o faturamento de cada mês do listing e no final o faturamento total anual. 

     ![](/api/attachments.redirect?id=318e961a-926c-4554-a997-789e438023f8 " =1517x178")

     \

## 3. **Desafios e Problemas Encontrados**

Durante o desenvolvimento, surgiram algumas dificuldades técnicas relacionadas à performance e ao volume de dados, que impactaram diretamente a velocidade de processamento e a viabilidade da integração com a planilha.

#### **Problemas Identificados:**


1. **Complexidade e tamanho da tabela** fato_block_occupancy
2. A tabela contém mais de 500k registros de imóveis, particionados por mês e ano, e é vinculada a múltiplas views. O processamento dessas informações tornou-se lento devido ao grande volume de dados.
3. **Criação de Features**:
   * Métricas como meses sem comentários ou faturamento dos últimos 12 meses exigem consultas complexas com agrupamentos pesados, o que aumentou o tempo de execução das queries.
4. **Mudança no comportamento do Lambda**:
   * Inicialmente, o Lambda processava apenas 10 imóveis, o que permitia uma execução rápida. Com a inclusão de todos os imóveis (sem limite), o tempo de processamento aumentou consideravelmente, tornando o processo muito mais lento.

### Soluções Propostas

### **Solução Provisória**:

* **Quebra das Queries**: A solução imediata foi dividir as queries em partes menores e transferir a lógica de processamento para o **Python**, visando reduzir a complexidade e o tempo de execução das consultas diretamente no banco de dados.
* **Execução em Blocos**: Processar os dados em blocos menores (por exemplo, por estado ou cidade) para reduzir o impacto no tempo de execução.

### **Solução Permanente**:

* **Criação de Tabela Otimizada e Enriquecida**: Desenvolver uma tabela otimizada que:
  * Inclua os merges necessários entre as diferentes fontes de dados.
  * Tenha partições por estado, cidade e strata.
  * Aplique filtros de qualidade (views, ratings, faturamento > 0).
  * Gere features pré-processadas para facilitar a consulta e o processamento subsequente, sem sobrecarregar o sistema.

Esta tabela otimizada estará em desenvolvimento durante o pelo time de DataOps e será incluída nos próximos passos.


 ![](/api/attachments.redirect?id=4aaeaf44-8767-4de4-8208-d87c70acaff3 " =1151x847")


### **Documentação Técnica da Tabela Otimizada**

Uma documentação detalhada sobre a tabela otimizada será criada, incluindo:

* **Estrutura da Tabela**: Definição das colunas e partições.
* **Merges e Enriquecimento dos Dados**: Como as fontes de dados serão integradas e enriquecidas.
* **Queries e Filtros**: Descrição das queries de pré-processamento e filtros de qualidade.

Link para a documentação da tabela otimizada. [analise_faturamento](https://outline.seazone.com.br/doc/catalogo-externo-de-dados-do-pipe-AKrS7tPmSv) pode ser encontrada na seção Camada ENRICHED

## 4. Execução final 

A solução para resolver o problema de timeout no API Gateway foi baseada na API existente *"diagnostico-faturamento-lista-ids"*, que possuía um tempo médio de execução de 17 segundos. A principal diferença estava na quantidade de filtros aplicados, que não eram necessários para este ciclo específico, e no fato de que essa API não realizava a junção de dados dos competidores com os da Seazone.

O passo inicial foi eliminar filtros desnecessários, como o ajuste na *strata* para compensar a falta de competidores ideais. Assim, os filtros mantidos na nova API foram definidos com base no escopo do primeiro ciclo:

* Possuir *strata*.
* Data do último comentário menor que 180 dias.
* e 4,5.Número de comentários maior que 10.
* Nota do *listing* maior qu
* Taxa de ocupação anual entre 10% e 90%.
* Possuir 12 meses de faturamento.

Para realizar a verificação dos imóveis da Seazone em relação aos filtros, foi aplicada a mesma query utilizada para os competidores, já que esta abrange tanto os dados de faturamento quanto os de ocupação. Após essa validação, realizamos uma simples concatenação dos dois conjuntos de dados (competidores e Seazone). Antes disso, o campo *id_seazone* foi removido do *dataframe* e posteriormente reinserido, indicando se os imóveis pertencem ou não à Seazone\nTrecho do código, onde 

```javascript
selected_listings
```

 faz referência aos competidores e 

```javascript
selected_seazone
```

 aos imóveis da seazone:

```javascript
selected_listings["id_seazone"] = "Não"
    
seazone_data = seazone_data.merge(total_fat, left_on=['airbnb_listing_id'], right_index=True, how='left')

if seazone_data.empty:
    result = {
    'listing_ids': selected_listings.to_json(orient='split', index=False),
}
else:
    seazone_data['faturamento'].fillna(0, inplace=True)

    selected_seazone = seazone_data[['airbnb_listing_id', 'state', 'city', 'suburb', 'number_of_bedrooms', 'number_of_guests', 'listing_type', 'strata']]
    selected_seazone['strata'].fillna('Sem Padrão', inplace=True)
    selected_seazone["id_seazone"] = "Sim"
    
    finalresult = pd.concat([selected_listings,selected_seazone], ignore_index=True)

    result = {
        'listing_ids': finalresult.to_json(orient='split', index=False),
    }
```

Por fim, para obter os dados de faturamento utilizados no *template* , essa tarefa à API já existente *"* ***diagnostico-faturamento*** *"* , cuja função é complementar os dados que não estão presentes na API criada. Essa abordagem resultou em uma otimização significativa no processo.

## 5. Testes e Resultados Obtidos

## 6. Definições de Requesitos para o Próximo ciclo