<!-- title: Tabelas Athena | url: https://outline.seazone.com.br/doc/tabelas-athena-s3viMJp3Nf | area: Tecnologia -->

# Tabelas Athena

# pricingdata

As tabelas dessa database são referentes aos preços e ao módulo de precificação.

Muitas delas possuem a coluna "origin", que representa de onde o preço veio. Hoje, "origin" pode ser: "rds" (preço do Sirius 1.0), "heuristic", "g.probst" (nome do operador em caso de precificação por concorrente), "direct" e "direct_category".

## historical_last_offered_price

**Descrição:** Essa tabela contem o **último preço** para cada dia que o Sirius **tenta** enviar para a Stays (se o script que envia para stays crashar ou similar esta tabela irá possuir preços que nunca entraram na Stays, mas esse evento é raro) .

Esses dados são referentes aos preços **DEPOIS** da aplicação das regras de setup.

**Essa tabela se atualiza toda manhã**, então para visualizar preços enviados no dia de hoje, deve-se esperar o próximo dia. Caso queira os preços mais atualizado, utilize a view "last_offered_price".

**Colunas:**

* **id_seazone:** ID da Seazone.
* **date:** Data do calendário.
* **price:** Preço do imóvel na data do calendário referente a estadia mínima.
* **min_stay:** Estadia mínima para a data.
* **block_checkin:** Verdadeiro caso o checkin esteja bloqueado e Falso caso esteja livre.
* **block_checkout:** Verdadeiro caso o checkout esteja bloqueado e Falso caso esteja livre.
* **timestamp:** Data, hora, minuto e segundo que o preço foi enviado para a Stays.
* **origin:** Origem do preço.
* **discount:** Se esta linha é referente a um desconto de estadia mínima ou não.

## historical_raw_last_offered_price

**Descrição:** Essa tabela contem o **último preço** para cada dia que o Sirius **tenta** aplicar as regras da Planilha de Setup (se o script que aplica as regras crashar ou similar esta tabela irá possuir preços que nunca foram aplicados as regras e, portanto, nunca entraram na Stays, mas esse evento é raro) .

Esses dados são referentes aos preços **ANTES** da aplicação das regras de setup, então não terão preço mínimo, máximo, estadia mínima, etc.

**Essa tabela se atualiza toda manhã**, então para visualizar preços enviados no dia de hoje, deve-se esperar o próximo dia. Caso queira os preços mais atualizado, utilize a view "last_offered_raw_price".

**Colunas:**

* **id_seazone:** ID da Seazone.
* **date:** Data do calendário.
* **price:** Preço do imóvel na data do calendário referente a estadia mínima.
* **timestamp:** Data, hora, minuto e segundo que o preço foi enviado para a aplicação das regras de setup.
* **origin:** Origem do preço.

## historical_prices

**Descrição:** Essa tabela contem **todos os preços** que o Sirius **tenta** enviar para a Stays (se o script que envia para stays crashar ou similar esta tabela irá possuir preços que nunca entraram na Stays, mas esse evento é raro) .

Esses dados são referentes aos preços **DEPOIS** da aplicação das regras de setup.

**Essa tabela se atualiza toda manhã**, então para visualizar preços enviados no dia de hoje, nesta tabela, deve-se esperar o próximo dia. Também há a opção de usar a tabela "price_before_stays_temp" que possuí os preços apenas de HOJE.

**Colunas:**

* **id_seazone:** ID da Seazone.
* **date:** Data do calendário.
* **price:** Preço do imóvel na data do calendário referente a estadia mínima.
* **min_stay:** Estadia mínima para a data.
* **block_checkin:** Verdadeiro caso o checkin esteja bloqueado e Falso caso esteja livre.
* **block_checkout:** Verdadeiro caso o checkout esteja bloqueado e Falso caso esteja livre.
* **timestamp:** Data, hora, minuto e segundo que o preço foi enviado para a Stays.
* **origin:** Origem do preço.
* **discount:** Se esta linha é referente a um desconto de estadia mínima ou não.
* **acquisition_date:** Mesma coisa do "timestamp", mas apenas a data (não possuí hora, minuto e segundo). Essa coluna é a partição, então sempre que possível é melhor usa-la.

## historical_raw_prices

**Descrição:** Essa tabela contem **todos os preço**s que o Sirius **tenta** aplicar as regras da Planilha de Setup (se o script que aplica as regras crashar ou similar esta tabela irá possuir preços que nunca foram aplicados as regras e, portanto, nunca entraram na Stays, mas esse evento é raro) .

Esses dados são referentes aos preços **ANTES** da aplicação das regras de setup, então não terão preço mínimo, máximo, estadia mínima, etc.

**Essa tabela se atualiza toda manhã,** então para visualizar preços enviados no dia de hoje, deve-se esperar o próximo dia.

**Colunas:**

* **id_seazone:** ID da Seazone.
* **date:** Data do calendário.
* **price:** Preço do imóvel na data do calendário referente a estadia mínima.
* **timestamp:** Data, hora, minuto e segundo que o preço foi enviado para a aplicação das regras de setup.
* **origin:** Origem do preço.
* **acquisition_date:** Mesma coisa do "timestamp", mas apenas a data (não possuí hora, minuto e segundo). Essa coluna é a partição, então sempre que possível é melhor usa-la.

## price_before_stays_temp

**Descrição:** Essa tabela contem **todos os preços** que o Sirius **tentou** enviar **HOJE** para a Stays (se o script que envia para stays crashar ou similar esta tabela irá possuir preços que nunca entraram na Stays, mas esse evento é raro) .

Esses dados são referentes aos preços **DEPOIS** da aplicação das regras de setup.

**Essa tabela possui dados apenas de hoje e toda manhã ela é esvaziada.** Caso queira os preços ofertados para outras datas e aquisições, utilize a tabela historical_prices.

**Colunas:**

* **id_seazone:** ID da Seazone.
* **date:** Data do calendário.
* **price:** Preço do imóvel na data do calendário referente a estadia mínima.
* **min_stay:** Estadia mínima para a data.
* **block_checkin:** Verdadeiro caso o checkin esteja bloqueado e Falso caso esteja livre.
* **block_checkout:** Verdadeiro caso o checkout esteja bloqueado e Falso caso esteja livre.
* **timestamp:** Data, hora, minuto e segundo que o preço foi enviado para a Stays.
* **origin:** Origem do preço.
* **discount:** Se esta linha é referente a um desconto de estadia mínima ou não.

## raw_price_temp

**Descrição:** Essa tabela contem **todos os preços** que o Sirius **tentou** aplicar **HOJE** das regras da Planilha de Setup (se o script que aplica as regras crashar ou similar esta tabela irá possuir preços que nunca foram aplicados as regras e, portanto, nunca entraram na Stays, mas esse evento é raro) .

Esses dados são referentes aos preços **ANTES** da aplicação das regras de setup.

**Essa tabela possui dados apenas de hoje e toda manhã ela é esvaziada.** Caso queira os preços antes de aplicar as regras de setup para outras datas e aquisições, utilize a tabela historical_raw_prices.

**Colunas:**

* **id_seazone:** ID da Seazone.
* **date:** Data do calendário.
* **price:** Preço do imóvel na data do calendário referente a estadia mínima.
* **timestamp:** Data, hora, minuto e segundo que o preço foi enviado para a Stays.
* **origin:** Origem do preço.

## last_offered_price

**Descrição:** Essa view contem o **último preço** para cada dia que o Sirius **tenta** enviar para a Stays (se o script que envia para stays crashar ou similar esta tabela irá possuir preços que nunca entraram na Stays, mas esse evento é raro) .

Esses dados são referentes aos preços **DEPOIS** da aplicação das regras de setup.

**Essa view sempre está atualizada com os últimos preços para cada data**, ela é uma mistura da historical_last_offered_price com os preços mais recentes enviados hoje.

**Colunas:**

* **id_seazone:** ID da Seazone.
* **date:** Data do calendário.
* **price:** Preço do imóvel na data do calendário referente a estadia mínima.
* **min_stay:** Estadia mínima para a data.
* **block_checkin:** Verdadeiro caso o checkin esteja bloqueado e Falso caso esteja livre.
* **block_checkout:** Verdadeiro caso o checkout esteja bloqueado e Falso caso esteja livre.
* **timestamp:** Data, hora, minuto e segundo que o preço foi enviado para a Stays.
* **origin:** Origem do preço.
* **discount:** Se esta linha é referente a um desconto de estadia mínima ou não.

## last_raw_offered_price

**Descrição:** Essa tabela contem o **último preço** para cada dia que o Sirius **tenta** aplicar as regras da Planilha de Setup (se o script que aplica as regras crashar ou similar esta tabela irá possuir preços que nunca foram aplicados as regras e, portanto, nunca entraram na Stays, mas esse evento é raro) .

Esses dados são referentes aos preços **ANTES** da aplicação das regras de setup, então não terão preço mínimo, máximo, estadia mínima, etc.

**Essa view sempre está atualizada com os últimos preços para cada data**, ela é uma mistura da historical_raw_last_offered_price com os preços mais recentes enviados hoje.

**Colunas:**

* **id_seazone:** ID da Seazone.
* **date:** Data do calendário.
* **price:** Preço do imóvel na data do calendário referente a estadia mínima.
* **timestamp:** Data, hora, minuto e segundo que o preço foi enviado para a aplicação das regras de setup.
* **origin:** Origem do preço.

# revenuedata

## reservations

## daily_revenue