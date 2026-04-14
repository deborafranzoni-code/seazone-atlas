<!-- title: Nova UX System Price | url: https://outline.seazone.com.br/doc/nova-ux-system-price-bT82Hv6134 | area: Tecnologia -->

# 🎓 Nova UX System Price

Esse documento explica a nova UX do System Price

Links:

* Miro: <https://miro.com/app/board/uXjVJdpcRWU=/>
* Github: <https://github.com/seazone-tech/gcp-data-resources/tree/main/cloud-functions/system-price>
* Card do Jira: <https://seazone.atlassian.net/jira/software/c/projects/DS/boards/22?assignee=712020%3Aa5e9a8db-16ea-4e34-b7c4-f3bc4c4e798c&assignee=616436bd07ac3c00686958d9&selectedIssue=DS-863>
* Looker Studio: <https://lookerstudio.google.com/u/1/reporting/7dbdd32d-bdf7-451c-8903-4757135a1011/page/p_6kyy4bu0wd/edit>
* Pasta do Drive: <https://drive.google.com/drive/u/2/folders/1H_Goc7e4ZT5WANXCgbFikaBFucpB8nbm>

# Tabelas/Views

Todas as tabelas/view foram criadas dentro do dataset system-price do BigQuery.

## Agressividade

**Tabela aggressiveness_levels**:

* **Descrição:** Essa tabela é usada para armazenar todo o histórico dos leveis de agressividade. Esse esquema garante uma linha por categoria, então fica mais fácil de registrar e auditar no histórico toda a vez que uma alteração for feita.
* **Esquema:**
  * **category**: Categoria
  * **timestamp**: Data da inserção da linha
  * **updated_by**: Email da pessoa responsável 
  * **aggressiveness_levels**: É uma lista com todos os níveis de agressividade
    * **advance_min**: Antecedência mínima da regra
    * **advance_max**: Antecedência máxima da regra
    * **level**: Nível de agressividade (tem que ser um de 'very_moderate', 'moderate', 'standard', 'aggressive', 'very_aggressive'.

**View** **aggressiveness_levels_active:**

* **Descrição:** pega a última timestamp para cada Categoria da tablea **aggressiveness_levels.** A lógica é: A tabela será usada para ter o histórico de todas as inserções de usuários, enquanto que a view sempre terá a última para usarmos no resto do fluxo.

**View** **aggressiveness_levels_unnested_active:**

* **Descrição:** Transforma os dados que estão na coluna/lista **aggressiveness_levels** em linhas, facilitando o uso dos dados.
* **Esquema:**
  * **category**: Categoria
  * **timestamp**: Data da inserção da linha
  * **updated_by**: Email da pessoa responsável 
  * **advance_min**: Antecedência mínima da regra
  * **advance_max**: Antecedência máxima da regra
  * **aggressiveness_level**: Nível de agressividade (tem que ser um de 'very_moderate', 'moderate', 'standard', 'aggressive', 'very_aggressive')

## Matrizes

**Tabela cluster_matrix:**

* **Descrição:** Essa tabela é usada para armazenar todo o histórico de matrizes do System Price. Esse esquema garante uma linha por cluster, então fica mais fácil de registrar e auditar no histórico toda a vez que uma alteração for feita.
* **Esquema:**
  * **cluster**: Nome do Cluster
  * **timestamp**: Data da inserção da linha
  * **origin**: Email da pessoa responsável por inserir a linha
  * **climate_type**: Clima da região (Não sazonal ou Região quente)
  * **matrix**: É uma lista de dicionários onde cada elemento da lista representa uma linha da respectiva temporada.
    * **season:** É a temporada. A temporada pode ser os seguintes valores:
      * **Não sazonal:** Apenas Média Temporada
      * **Região quente:** Baixa/Média/Alta Temporada
    * **season_matrix:** É uma lista de dicionários onde cada elemento da lista é uma linha da matriz.
      * **rule_type**: É o tipo de regra, pode ser "Fim de semana", "Dia de semana", "feriado", "evento"
      * **acronym**: É a sigla, ela será usada como abreviação no Looker Studio facilitando o entendimento da regra. exemplo: NS_DDS, NS_EV, etc
      * **occupancy_type**: É o tipo de ocupação, pode ser Low, Medium ou High
      * **advance_interval:** É uma lista de intervalos/percentils.
        * **advance_min**: Antecedência mínima da regra
        * **advance_max**: Antecedência máxima da regra
        * **p_type**: Tipo do percentil que será usado, pode ser (mix, occ, avb, min, max)
        * **p_value:** Valor do percentil que será usado

**View cluster_matrix_active:**

* **Descrição:** pega a última timestamp para cada cluster da tablea **cluster_matrix.** A lógica é: A tabela será usada para ter o histórico de todas as matrizes, enquanto que a view sempre terá a última para usarmos no resto do fluxo.

**Tabela cluster_category:**

* **Descrição:** Possuí a relação de categoria e clustar.
* **Esquema:**
  * **cluster**: Nome do Cluster
  * **category**: Categoria

## Informações dos imóveis

**Tabela allowed_periods_current_unnested:**

* **Descrição:** Essa tabela puxa os dados da tabela allowed_periods do Athena (referente à aba **System Price - Periodos** da planilha) e os transforma em dados diários já aplicando qualquer regra de hierarquia existente.
* **Esquema:**
  * **id_seazone:** Nome do imóvel.
  * **date:** Data, se um imóvel existe numa data dessa tabela, isso quer dizer que ele está senod precificado pelo System Price.

**View system_price_listings:**

* **Descrição:** Lista de imóveis que usam o system_price. Caso o imóvel esteja com pelo menos 15 dias na allowed_periods_current_unnested, então ele entra na lista.

**Tabela listings_system_price:**

* **Descrição:** Essa tabela fornece dados para usar de filtro no BI para os KPIs. Ela puxa as colunas de Categoria, Cidade e Polígono de todos os imóveis da SETUP + informação de se o imóvel está ou não configurado para o system price (view system_price_listings**)**
* **Esquema:**
  * **id_seazone:** Nome do imóvel.
  * **Categoria, Poligono, Cidade:** Grupo da Setup
  * **Clima:** É o clima configurado para o imóvel na aba Clima. Detalhe: Para os filtros funcionarem é necessário o clima estar como "Não sazonal" ou "Clima-CO"
  * **is_system_price:** Booleano, caso o imóvel tenha pelo menos 90 dias na aba System Price - Periodos ele é considerado que está no system_price.

**View listings_system_price_and_matrix:**

* **Descrição:**
  * Pode ser que o imóvel esteja configurado na aba Periodos, mas ele não tenha cluster ou o cluster dele não tem matrix, essa view corrige o campo is_sytem_price para só ser true se ele possuír matriz/cluster.
  * Essa view também adiciona a coluna is_florianopolis. Essa coluna é para diferenciar quais imóveis estão inclusos na primeira etapa da precificação Sazonal.

**View listings_system_price_by_category:**

* **Descrição:** Essa view é utilizada para fazer o filtro de ativo/inativo do BI, ela basicamente agrupa **listings_system_price** para termos quais categorias possuem pelo menos um imóvel usando o system price.

## System Price

**Tabela** **aggressiveness_prices:**

* **Descrição**: Essa tabela tem praticamente TODOS os dados do system_price. Ela já tem tudo pré-calculado, o que facilita pro BI e pro script que precifica.
* **Esquema:**
  * **category, date, cluster, acronym, to_competitors, to_category, p_type_target, consecutive_event, etc**: Essa tabela possuí várias colunas, mas a maioria tem o nome auto-explicativo e estão ali para trazer algum dado chave (como to_category) ou estão ali para debuggar alguma informação do system_price (dados da matrix, como o acronym, que mostra a sigla daquele dia, feriado, DDS, etc, ou o consecutive_event, que diz se uma data é seguida da outra e possuí o mesmo evento).
  * **p_occ_010, p_occ_025, p_mix_010, etc:** São os percentils ocupados, disponiveis e mix dos concorrentes.
  * **price_on_reservation**, **lower_limit_occ e upper_limit_occ:** Limites inferiores e superiores pro system_price. A price_on_reservation é o valor base usado pra encontrar os limites.
  * **very_aggressive, agressive, standart, moderate, very_moderate:** É o valor do system_price para cada modalidade de agressividade.
  * **p_value_coef_aggressive e p_value_coef_moderate:** Valor do coeficiente usado para cada modalidade de agressividade (a lógica em si tá na seção que explica o fluxo da precificação)
  * **p_value_very_aggressive, p_value_aggressive, etc:** Essas colunas são o valor do percentil utilizado para cada modalidade de agressividade. Se o p_value_target for 50, então p_value_aggressive seria 42, por exemplo. Não existe p_value_standart, visto que esse é igual o p_value_target.
  * **p_value_target_original:** Valor do p_value_target da Matriz ANTES de aplicar as regras de holiday_level e strata_weight. Ou seja, é realmente o valor original da Matriz**.**
  * **to_diff_price_percentage:** Porcentagem usada no parametro do TO Diff (Motor de Precificação Inteligente)

**Tabela fill_category_price:**

* **Descrição**:
  * Essa tabela é usada para adicionar um preenchimento automático em datas sem system price. Isso pode acontecer em datas futuras, caso não exista concorrentes disponíveis.
  * **Como atualizar ela?** Existe uma query salva no bigquery. Caso seja necessário, só adicionar as respectivas novas linhas, salvar a consulta e executá-la.![](/api/attachments.redirect?id=fcf0e183-7cfd-4bf4-8586-e769ebf28277 " =1930x330")
* **Esquema:**
  * **category_normalized_prefix:** Essa coluna precisa ser o prefixo da categoria, estar minúscula e não ter acentos ou caracteres especiais.
  * **fill_system_price:** Valor para o preenchimento.

**View aggressiveness_prices_and_levels**

* **Descrição**:
  * Essa é a view que faz a "mágica". Ela junta a tabela **aggressiveness_prices** com **aggressiveness_levels_unnested_active,** ou seja, agora podemos, em tempo real, toda a vez que a agressividade for alterada, saber o valor do system_price.
  * Ela também faz um join com a view **listings_system_price_by_category**, apenas para o filtro de "Ativos no System Price" do BI funcionar.
* **Esquema:**
  * **system_price:** Dependendo do aggressiveness_level, o system_price é o respectivo valor que já está pré-calculado nas colunas very_aggressive, aggressive, standart, etc.
    * Ele pode ser nulo, caso não exista preço dos concorrentes ou caso não exista uma agressividade definida para a categoria naquela data
    * Ele pode ser o valor FILL da tabela fill_category_price
  * **system_price_p_value:** É o percentil final utilizado no cálculo do sytem_price, também dependendo do aggressiveness_level
  * **reason:** Faz o concat de algumas colunas chaves para melhorar a explicabilidade da regra no BI, normalmente ele será: `CONCAT(p.acronym, '_', p.occupation_type, '_', p.advance_min, '_', p.advance_max)`. Exceções:
    * **Sem Agressividade**: Caso não exista na tabela de agressividade.
    * **Preenchimento Automático**: Caso não haja preço dos concorrentes e antecedencia >= 295.
    * **Sem Preço Competidores:** Caso não tenho preço dos concorrentes e não tenha preenchimento automático.
    * **Sem Sazonalidade**: Caso RM não tenha definido a sazonalidade daquele clima.

**View aggressiveness_prices_and_levels_by_id_seazone**

* **Descrição:** Ela faz um join com a tabela **pricing.sirius_stays_explainer**, essa é uma tabela atualizada de 3 em 3 horas que resume todas as regras de preço aplicadas a cada imóvel. Essa tabela é a nível imóvel e é usada para puxar os preços da Stays de cada imóvel e gerar essas métricas de Preço Stays no BI.

**Tabela Externa prices_sent_sirius**

* **Descrição**:
  * Essa é uma tabela externa que possuí todos os parquets já enviados para a precificação.
* **Esquema:** Por questões de compatibilidade, ela também possúi todas as colunas necessárias pra geração dos warnings (reason, upper_limit, lower_limit, etc).
  * **Partição:** Coluna acquisition_date.
  * **acquisition_timestamp:** Diferenciar as multiplicas precificações que acontecem no mesmo dia.

## Warnings

Todas as tabelas de warnings seguem um mesmo padrão. Existe uma tabela base chamada warning_{tipo}, ela tem os dados do warning gerado na última vez que o script rodou, sendo que o {tipo} é o tipo do warning.

### Abaixo do Intervalo

**Tabela** **warning_prices_lower_range:**

* **Descrição**: Essa tabela representa o warning "**Abaixo do Intervalo**"
* **Esquema:** Mesmas colunas usadas no warning.

**Tabelas warning_prices_lower_range_status:**

* **Descrição**: Essa tabela representa as linhas verificadas na planilha do Sistemas de Alertas 2.0 sobre o warning "**Abaixo do Intervalo**".
* **Esquema:** Mesmas colunas usadas no warning, mas com a adição das colunas **Status**, **Comentário e acquisition_date.**

**View warning_prices_lower_range_pending**

* **Descrição**: Essa tabela representa todos os warnings encontrados na tabela **warning_prices_lower_range,** mas que ainda não foram verificados na tabela **warning_prices_lower_range_status.**
* **Lógica:** Caso a categoria/data nunca tenham sido verificadas ou se a proporção price/lower_limit ficar menor que 10% de quando o warning foi aprovado, então o warning volta a aparecer nessa view. Isso é para pegar os cases em que o warning havia sido aprovado, mas que o preço continuou caindo abaixo do limite inferior, sendo necessário uma outra verificação.
* **Esquema:** Mesmas colunas usadas no warning.

### Acima do Intervalo

**Tabela** **warning_prices_over_range:**

* **Descrição**: Essa tabela representa o warning "**Acima do Intervalo**"
* **Esquema:** Mesmas colunas usadas no warning.

**Tabelas warning_prices_over_range_status:**

* **Descrição**: Essa tabela representa as linhas verificadas na planilha do Sistemas de Alertas 2.0 sobre o warning "**Acima do Intervalo**".
* **Esquema:** Mesmas colunas usadas no warning, mas com a adição das colunas **Status**, **Comentário e acquisition_date.**

**View warning_prices_over_range_pending**

* **Descrição**: Essa tabela representa todos os warnings encontrados na tabela **warning_prices_over_range,** mas que ainda não foram verificados na tabela **warning_prices_over_range_status.**
* **Lógica:** Caso a categoria/data nunca tenham sido verificadas ou se a proporção price/upper_limit ficar maior que 10% de quando o warning foi aprovado, então o warning volta a aparecer nessa view. Isso é para pegar os cases em que o warning havia sido aprovado, mas que o preço continuou subindo acima do limite superior, sendo necessário uma outra verificação.
* **Esquema:** Mesmas colunas usadas no warning.

### Acima Strata Superior

**Tabela** **warning_prices_outside_strata:**

* **Descrição**: Essa tabela representa o warning "**Acima Strata Superior**"
* **Esquema:** Mesmas colunas usadas no warning.

**Tabelas warning_prices_outside_strata_status:**

* **Descrição**: Essa tabela representa as linhas verificadas na planilha do Sistemas de Alertas 2.0 sobre o warning "**Acima Strata Superior**".
* **Esquema:** Mesmas colunas usadas no warning, mas com a adição das colunas **Status**, **Comentário e acquisition_date.**

**View warning_prices_outside_strata_pending**

* **Descrição**: Essa tabela representa todos os warnings encontrados na tabela **warning_prices_outside_strata,** mas que ainda não foram verificados na tabela **warning_prices_outside_strata_status.**
* **Lógica:** Caso a categoria/data nunca tenham sido verificadas OU se a proporção price/strata_upper_limit ficar maior que 10% de quando o warning foi aprovado OU a categoria superior mudou, então o warning volta a aparecer nessa view. Isso é para pegar os cases em que o warning havia sido aprovado, mas que o preço continuou subindo acima do limite superior, sendo necessário uma outra verificação, ou que a categoria do limite superior simplesmente mudou.
* **Esquema:** Mesmas colunas usadas no warning.

### Categorias não Elegíveis

**Tabela** **warning_not_eligible_categories:**

* **Descrição**: Essa tabela representa o warning "**Categorias não Elegíveis**"
* **Esquema:** Mesmas colunas usadas no warning.

**Tabelas warning_not_eligible_categories_status:**

* **Descrição**: Essa tabela representa as linhas verificadas na planilha do Sistemas de Alertas 2.0 sobre o warning "**Categorias não Elegíveis**".
* **Esquema:** Mesmas colunas usadas no warning, mas com a adição das colunas **Status**, **Comentário e acquisition_date.**

**View warning_not_eligible_categories_pending**

* **Descrição**: Essa tabela representa todos os warnings encontrados na tabela **warning_not_eligible_categories,** mas que ainda não foram verificados na tabela **warning_not_eligible_categories_status.**
* **Lógica:** Caso a categoria nunca tenha sido verificada ou se a rasão da categoria ter virado Ilegível tenha mudado, então o warning volta a aparecer nessa view.
* **Esquema:** Mesmas colunas usadas no warning.

# Scripts

## update-listings-system-price

Esse é o script mais simples do processo, ele apenas roda duas queries, uma que cria a tabela `allowed_periods_current_unnested` e outra pro `listings_system_price.`

Ele é triggado por um apigateway toda vez que o RM atualiza a aba System Price - Periodos da Setup.

## app-aggressiveness-level

O app é usado pelo RM para inserir novas linhas na tabela **aggressiveness_levels.** 

Cloud Run: __[system-price-app](https://console.cloud.google.com/run/detail/southamerica-east1/system-price-app/observability/metrics?project=data-resources-448418)__

### LoadBalancer

Para garantir que quem está usando o APP é da Seazone, foi criado um load_balancer __[lb-system-price](https://console.cloud.google.com/net-services/loadbalancing/details/httpAdvanced/lb-system-price?project=data-resources-448418&authuser=1)__.

#### Frontend

Foi configurado um IP estático para o frontend.

Esse ip foi atrelado ao certificado SSL system-price, cujo domínio é __<https://systemprice.seazone.com.br>__. Esse subdomínio foi passado para a governança adicionar no DNS pelo cloudflare.

Depois de tudo isso, quando alguém acessar o link ele será direcionado ao backend do LoadBalancer.

#### Backend

O Backend foi configurado para ser CloudRun/Function e o link do app foi fornecido, além disso, o Cloud CDN foi desativado (o default é ser ativo, mas não precisa de cache a aplicação) e **IAP foi ativado**, esse IAP é importante porque é justamente ele que faz a validação se o usuário é da Seazone ou não.

O resto das configurações ficam default.

Depois de criado o Backend, é necessário ir na seção do IAP e configurá-lo. Para isso, é necessário adicionar o principal: __[seazone.com.br](http://seazone.com.br)__ para a role: "IAP-secured Web App User" e garantir que a regra está ativada.\n

 ![](/api/attachments.redirect?id=4739077e-08bb-41e3-8deb-9fa27dbf9bb5 " =342x295")

### Script

Para rodar localmente o script, basta executar a função main, exemplo: `python3 main.py`

O script consiste num app em flask, por default, o app será aberto no link: __<http://127.0.0.1:8080/>__

**Detalhes:**

* É necessário ter configurado CLI do gcloud, sem ele não é possível rodar as APIs localmente, visto que elas fazem requests no bigquery. __[Como instalar CLI gcloud](https://cloud.google.com/sdk/docs/install?hl=pt-br)__
* **❗❗❗Para testes locais, cuidado ao testar o botão de atualizar agressividade, visto que mesmo rodando de forma local, o script atualiza a tabela de PROD❗❗❗**

#### Lógica do Backend

A API foi feita em Flask e existem 3 endpoints.

* GET /categories → retorna a lista de categorias disponíveis. Exemplo de resposta:

  ```json
    {
      "data": {
        "categories": ["Eletrônicos", "Roupas", "Móveis"]
      }
    }
  ```
* GET /intervals?category=<categoria> → retorna os intervalos e os níveis atuais da categoria selecionada. Exemplo de resposta:

  ```json
  {
    "data": {
      "intervals": ["000-005", "006-010", "011-015"],
      "current_level": ["standard", "moderate", "very_aggressive"]
    }
  }
  ```
* POST /intervals → recebe os novos níveis para atualização no banco de dados. Exemplo de payload:

  ```json
  {
    "category": "Categoria 1",
    "intervals": ["000-005", "006-010", "011-015"],
    "levels": ["standard", "moderate", "very_aggressive"]
  }
  ```

#### Lógica do Front


1. É aberto o HTML com os campos bloqueados.
2. O javascript executa a função **loadCategories()** que, por sua vez, executa o endpoint **/categories** para puxar a lista de todas as categorias possíveis. Terminando, o campo de selecionar Categoria é desbloqueado.
3. Existe um eventListener no campo categorySearch, então quando o usuário selecionar uma categoria essa função async será executada.

   
   1. Ela executa um GET no endpoint /intervals. O endpoint retorna "intervals" (lista de antecedências) e "current_level" (lista de agressividades para cada período de antecedência). 
   2. Ela executa a função **displayIntervalsAndLevels()** que cria os dropdown pro usuário selecionar a agressividade de cada período. Detalhes:

      
      1. Os 5 levels possíveis estão hardcoded na constante **possibleLevels**
      2. A função utiliza o current_level para adicionar a string " (Atual)" na respectiva agressividade.
4. Existe um EventListener no formúlario, então quando o botão for pressionado a função é executada.

   
   1. O evento executa **setFormState(false)**, o que faz o forms bloquear simbolizando pro usuário que o request está sendo feito (também garante que o usuário não clique em nada evitando erros).
   2. A função **postNewIntervalLevels()** pega a categoria, intervalos e leveis e faz um POST no /intervals.
   3. Se não der erro, o script executa novamente **displayIntervalsAndLevels()**, mas dessa vez usando os novos leveis que o usuário selecionou (ou seja, os novos leveis que terão a string " (Atual)")
   4. **setFormState(true**) para liberar o forms pro usuário.

Durante cada etapa do processo é chamada a função **setStatus()** que fornece uma mensagem na caixa de status. As mensagens podem ser coisas como "Selecione as Novas Agressividades" ou **erros, sendo que em caso de erros ela também fica vermelha.**

## calculate-aggressiveness-prices

Esse é o principal script da nova UX. Ele calcula TODOS os dados que irão para a tabela aggressiveness-prices.

Ele é trigado toda vez que o RM atualiza a lista de concorrentes (pelo botão da planilha) ou quando der meia noite UTC (o script roda meia-noite para garantir que as regras de antecedencia estão olhando para o dia certo, a data falando ser antecedencia 0 precisa ser HJ assim que o dia vira).

 ![](/api/attachments.redirect?id=fa1b5ae4-02f4-4de6-88e2-7df7e6562186 " =380x218")

### Lógica do Script:


1. São feitos requests de forma assincrona para as tabelas holidays, old_holidays, cluster_category e cluster_matrix_active.
2. É criado o dataframe "rules" com todas as regras formatadas
3. É criado o dataframe "dates_info", ele retorna as informações dentre 1 ano para trás e 1 ano no futuro para cada categoria elegivel do system_price.

   
   1. Esse dataframe, para feriados, também tem linhas duplicadas. A tabela old_holidays é usada para sabermos em qual aquisição o feriado foi criado ou deletado, então se o feriado foi criado no dia '2025-10-01" e a reserva foi criada no dia "2025-09-10", como o feriado ainda não existia essa data (terça-feira) é considerada um dia semana nas regras do system_price.
   2. Ele também usa os dados de Sazonalidade definidos por RM, então, é importante que a planilha esteja atualizada com os dados dentre 1 ano trás e para frente.
4. É criado o dataframe "system_price", ele tem todos os dados diários de dates_info a partir de hoje + informações de preços dos concorrentes.
5. É calculado o respectivo percentil para cada nível de agressividade e o valor das diárias de cada nível de agressividade também é calculado

   
   1. Nesse percentil também está incluso os níveis do feriado, ou seja, nos níveis 2 e 3 é somado 10 e 20 ao parâmetro base da matriz. 
6. É calculado o incremento TO diff (to_diff_price_percentage), ele é usado no **Motor de Precificação inteligente.**
7. O script puxa os percentils 10, 25, 50, 75 e 90 dos concorrentes occ, avb e mix para depois fornecer o dado no BI.
8. É usado as datas do "dates_info" antes de hoje para encontrar os respectivos valores de percentil.
9. O resultado é salvo na tabela aggressiveness_prices

### Lógica da Agressividade

O card com os testes realizados se encontra aqui: [Jira](https://seazone.atlassian.net/jira/software/c/projects/DS/boards/22?assignee=712020%3Aa5e9a8db-16ea-4e34-b7c4-f3bc4c4e798c&assignee=616436bd07ac3c00686958d9&selectedIssue=DS-897)

A fórmula da agressividade é:

* Se o P target estiver dentre 35 e 65, então retorna 16 pros coeficientes de agressividade.
* Se for > 65, então o nível moderado precisa ser amortecido e é retornado essa formulá:

  ```python
  d = abs(x - 65)
  return 16 * np.exp(-d/16)
  ```
* Se for < 35, então o nível agressivo precisa ser amortecido e a formúla é:

  ```python
  d = abs(x - 35)
  return 16 * np.exp(-d/16)
  ```
* É adicionado um peso chamado "Agressividade a nível strada". A ideia é que imóveis TOPs e MASTERs precisam de um percentil maior que imóveis SIMs e JRs. A lógica é simplesmente somar esse peso ao percentil da categoria, então se a matriz fala pros SUP serem o P20, os respectivos percentils serão 16, 18, 20, 22 e 24.
  * SIM: -4
  * JR: -2
  * SUP: 0
  * TOP: 2
  * MASTER: 4

Esses coeficientes são salvos nos campos p_value_coef_aggressive e p_value_coef_moderate. Os percentils em si são:

* p_value_very_aggressive: `p_value_target - p_value_coef_aggressive + strata_weights`
* p_value_aggressive: `p_value_target - (p_value_coef_aggressive/2) + strata_weights`
* p_value_target: `p_value_target + strata_weights`
* p_value_moderate: `p_value_target + (p_value_coef_moderate/2) + strata_weights`
* p_value_very_moderate: `p_value_target + p_value_coef_moderate + strata_weights`

### Motor de Precificação Inteligente

A ideia do motor de precificação seria aplicar outras regras e pesos ao System Price, como a meta, diferença da TO dos competidores, escadinha, etc.

No fim, a única lógica implementada foi a do TO Diff. A lógica consiste em:

* Pegar periodos consecutivos, então datas seguidas de DDS, FDS, evento ou feriado são agrupadas em periodos.
* São calculadas a TO Cat e TO Comp nesses períodos. Somasse todos os dias ocupados e divide-se por todos os dias não bloqueados nos periodos.
* É feita a diferença da TO Cat e TO Comp.
  * Se -1 <= diff < -0.8, então -20%
  * Se -0.8 <= diff < -0.6, então -15%
  * Se -0.6 <= diff < -0.4, então -10%
  * Se -0.4 <= diff < -0.2, então -5%
  * Se -0.2 <= diff <= 0.2, então 0
  * Se 0.2 < diff <= 0.4, então 5%
  * Se 0.4 < diff <= 06, então 10%
  * Se 0.6 < diff <= 08, então 15%
  * Se 0.8 < diff <= 1, então 20%
* Essa porcentagem é multiplicada em cada uma das agressividades, então se o preço do standard e moderado antes era 100 e 90 e a porcentagem ficou em 5%, agora o que aparece pro standart será 105 e 94.5. Mesma coisa para as outras agressividades.

Atualmente, essa lógica só está sendo usada na categoria Goiania-Leste-apartamento-SUP-1Q, mas existem planos para adiciona-la nas outras.

### Lógica dos Limites

A ideia dos limites é pegar o valor de aluguél dos últimos dias para cada tipo de Temporada e tipo de regra (DDS, FDS, Evento e Feriado) e usar isso como o valor base do limite.

Datas utilizadas:

* **Não sazonais**: Últimos 180 dias
* **Região quente:** Último ano.

Aqui é levado em conta se, na data de criação da reservas, elas eram consideradas como feriado/evento pelo RM.

O valor considerada para a diária é a coluna `price` da daily_revenue_sapron, ou seja, é o preço que estava na Stays no momento da reserva (não necessariamente é o preço da diária na OTA). É pego a mediana desse price ocupado para cada rule_type.

Foi criado a função `get_occ_limits()` para calcular os limites. Os limtes são:

* 00-01:
  * DDS/FDS: 0.85 até 1.5
  * Feriado/Evento: 0.65 até 1.3
* 02-05:
  * DDS/FDS: 0.95 até 1.5
  * Feriado/Evento: 0.75 até 1.3
* 06-60:
  * DDS/FDS: 1 até 1.5
  * Feriado/Evento: 0.8 até 1.3
* 61-75:
  * DDS/FDS: 1 até 1.55
  * Feriado/Evento: 0.8 até 1.35
* 76-90:
  * DDS/FDS: 1 até 1.6
  * Feriado/Evento: 0.8 até 1.4
* 91-365:
  * DDS/FDS: 1 até 1.55
  * Feriado/Evento: 0.8 até 1.45

#### **Lógicas Exclusivas dos Sazonais.**

Os imóveis Sazonais (Região quente) possuem algumas lógicas adicionais.

**Níveis de Feriado**

Os níveis de feriado também são utilizados para diferenciar os limites, ou seja, não são misturados os dados de reservas feitas em feriados de nível 1 com 3, por exemplo.

Isso foi feito após observar que reservas no Revillon ficam muito mais caras que reservas de outros feriados. Em teoria, Revillon tem um nível de feriado maior, então separar fez mais sentido.

**Predição**

Como os dados desses imóveis ficam muito dividos, é difícil termos exemplos em cada temporada de DDS/FDS/Feriado/Evento, mesmo pegando 1 ano no passado.

Para isso é feita uma predição para os parametros que não temos dados, ou seja:

* Em cada poligono é encontrado um base_price_limit. Esse é o preço base daquel poligono.,
* É encontrado coeficientes para a strata e rooms (imóveis mais caros vão ter coeficientes maiores)
* É feita a multiplicação dos campos para termos uma predição do preço que queremos usar pros limites para quando não temos dados daquela categoria.
* Imóveis com menos de 300 dias de dados sempre vão usar os dados da predição, visto que eles precisam ter praticamente o ano completo para conseguir ter dado pros limites.

## insert-new-matrix

Esse script/api está ligado a planilha [Edição Parâmetros - System Price](https://docs.google.com/spreadsheets/d/10Pp06i7XBL_j2hcTJDYs4J5Kr9qfsP7OPFxxwqalwGY/edit?gid=0#gid=0).

A lógica do script é:

* Receber o conjunto de parâmetros colocados na planilha.
* Formatar os dados (ajeitar os tipos, renomear colunas).
* Adicionar os dados na tabela cluster_matrix.

Na planilha existe uma validação para garantir que o nome do cluster seja "cluster_sazonal-centro-SC-JRSUP-3Q" e do clima "Região quente", mas nada impede de no futuro usarmos essa API para editar parâmetros das matrizes.

## upsert-cluster

Esse script/api está ligado a planilha [Alteração de Clusters - System Price](https://docs.google.com/spreadsheets/d/1NtcZQbiPQGljvVsiOQWIP29BwhjjP-RlaKvefG0CtSs/edit?gid=1310462300#gid=1310462300).

As pessoas colocam na planilha todas as categorias e seus respectivos clusters. Depois, basta rodar o script.

A lógica do script é:

* Fazer um overwrite da tabela cluster_category com todas as categorias/clusters fornecidas pela planilha.
* Fazer um append no cloud storage para termos todo o histórico de execuções salvas. Por enquanto essa tabela não está conectada ao bigquery, mas existe no cloud storage.
* Realiza uma consulta para identificar se todas as categorias existem na aggressiveness_levels. Caso uma categoria não exista, então o script atualiza a tabela com uma linha nova para as respectivas categorias faltantes.

## Sistemas de Alertas 2.0

Aqui se encontram os scripts usados pro novo sistema de alertas que envolve a planilha [Sistema de Alertas - System Price](https://docs.google.com/spreadsheets/d/10d2oSGdxaKPCaqu715_SaMc_26C7j3DtkMCGUDZYGtc/edit?gid=746153009#gid=746153009).

### send-prices-to-aws

Esse é o cloud function que começa o processo de precificação em si. Existe um trigger na planilha que de 3 em 3 horas (ou cada vez que o RM roda o botão) uma API é executada que dispara esse cloud function.

Esse script começa fazendo um JOIN dentre a view aggressiveness_prices_and_levels e allowed_periods_current_unnested para pegar todos os system_price que existem e todas as datas necessárias para precificar.

Esse script também gera e envia os warnings para o Slack.

* **Abaixo do Intervalo:** Datas onde alguma categoria ficou abaixo do intervalo.
* **Acima doIntervalo:** Datas onde alguma categoria ficou acima do intervalo.
* **sem intervalo:** Datas onde não existe intervalos superior ou inferior.
* **Sem System Price:** Datas que estão configuradas para serem precificadas no SystemPrice, ma que não estão possuem dados de SystemPrice.
* **Acima Strata Superior:** Datas onde o system price de uma categoria ficou acima do de uma categoria com strata superior.
* **Categorias Não Elegíveis**: Lista de categorias que não são elegíveis, mas que estão cadastradas para precificação no system price.

Ele gera todos os warnings e, nos avisos que se encontram na planilha, ele também salva no cloud storage + bigquery. Depois, ele realiza a consulta na view com sufixo _pending que, como já explicado na seção de Tabelas/Views, realiza a lógica de remover os warnings já validados por RM. Após essas lógicas, o script envia a mensagem pro Slack.

No final, o script remove datas que não possuem System Price e as envia para a AWS:

* O script atualiza o cloud storage com o parquet
* Envia um request para a API do LambdaPricingSystemPrice dizendo o nome do arquivo necessário para precificar.

### new-warnings-api e AppScript

Esse é o script que realiza a validação dos warnings junto a planilha.

* Toda a vez que a função do AppScript é executada, o script lê todas as linhas dos 4 warnings que possuem alguma coisa na coluna "**Status**". Essas linhas são enviadas para o script new-warnings-api.
* O new-warnings-api atualiza as tabelas com o sufixo "_status" numa lógica de overwrite (ler a última execução, adicionar os novos dados e sobrescrever a tabela)
* O script lê os warnings que ainda precisam de validação, ou seja, os das views com sufixo "_pending" e retorna para o appscript esses warnings.
* O appscript atualiza todas as abas da planilha com os warnings que ainda não foram validados.

O AppScript roda uma vez por dia para garantir que a planilha está atualizada com todos os warnings sendo gerados de 3 em 3 horas.

Idealmente, ela rodaria toda a vez que o send-prices-to-aws rodasse, mas isso não é possível, visto que pode ser que alguém esteja usando a planilha no momento da execução e o appscript atualizasse a tabela com um dado ainda incompleto, por isso, que o appscript roda uma vez por dia de madrugada.

## LambdaPricingSystemPrice

 ![](/api/attachments.redirect?id=5e5d9d16-a2b9-4c4a-a23a-7edd67b814d4 " =266x315")

Esse é o lambda que faz a precificação em si. Ele é triggadon pelo send-prices-to-aws.

Esse lambda faz uma consulta na tabela do bigquery prices_sent_sirius e lê o arquivo recebido no request. O motivo dela ler através do bigquery é que, dessa forma, não seria necessário alterar as permissões do lambda ou criar um novo layer capaz de ler o cloud storage.

Depois de ler a labela e formatar algumas colunas, o script utiliza os limites inferiores de chão para o system_price, ou seja, preços abaixo do limite inferior virão o limite inferior. Os limites superiores são usados apenas para o warning (eles não viram o teto do system_price).

Datas sem intervalo NÃO são precificadas.

No final, o script salva o parquet na tabela system_price_full e passa a tag `system_price - v1` para o script de precificação.

As datas sem limites tambéms são salvas nessa tabela, mas elas NÃO são precificadas.

# FAQ

* Como mudar os campos de agressividade? Exemplo: Quero adicionar o tipo "slightly_agressive".
  * É necessário no javascript do app adicionar esse campo na constante possibleLevels.
  * Ir no script calculate-aggressiveness-prices e adicionar esse tipo de agressividade na função get_aggressiveness_prices.
  * Ir na view aggressiveness_prices_and_levels e adicionar esse CASE WHEN.
* Como adicionar ou editar matrizes?
  * Utilizando o endpoint insert-new-matrix +  a Planilha. Nele podemos facilmente editar uma matriz.
* Como alterar os intervalos de agressividade?
  * Basta adicionar uma nova linha para cada categoria na tabela aggressiveness_levels, essa nova linha tem que ter os respectivos intervalos de agressividade
* Como alterar clusters?
  * **Alterações granualares (como adicionar nova categoria ou renomear uma categoria):** Dá pra usar o endpoint upsert-cluster e sua respectiva planilha.
  * **Inserir cluster novo:** O processo envolve multiplias etapas:
    * Usar o endpoint insert-new-matrix para adicionar o novo cluster + seus respectivos parametros.
    * Usar o endpoint upsert-cluster para cadastrar as categorias a esse novo cluster.
    * Rodar o updateSystemPrice (Pode ser na SETUP ou nas planilhas dessas duas APIs, todas elas tem uma cópia dessa função). Também dá pra esperar o trigger roda-la automaticamente.
* **Alteração do algorítimo de clusterização:** Quando os novos clusters forem gerados, é necessário ver se alguma categoria mudou de cluster.
  * caso alguma categoria tenha mudado, é necessário entender o motivo.
  * caso na nova clusterização exista um novo cluster, é enquanto não for adicionado esse novo cluster na tabela cluster_matrix essas categorias não terão system_price.
* Como foram gerados a lista de categorias pro teste em imóveis Sazonais? Foi feira uma query no BigQuery que retornava as categorias + o número de imóveis e concorrentes. A consulta está salva no card: <https://seazone.atlassian.net/browse/DS-1203>