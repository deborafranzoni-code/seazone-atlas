<!-- title: Documentação do Usuário | url: https://outline.seazone.com.br/doc/documentacao-do-usuario-ROF0HWdaJu | area: Tecnologia -->

# Documentação do Usuário

# Visão Geral do Dashboard

O dashboard é dividido em três seções principais:


1. **Filtros de Análise:** Permite refinar os dados exibidos na tabela de "Min Stay Aplicadas" e "Todas Min Stay".
2. **Min Stay Aplicadas:** Apresenta uma tabela detalhada com as configurações de Min Stay ativas para os imóveis selecionados.
3. **Todas Min Stay (página separada):** Exibe todas as configurações de Min Stay, independentemente de estarem ativas no dashboard principal.

# 1. Filtros de Análise

Esta seção permite personalizar a visualização dos dados na tabela "Min Stay Aplicadas".

* **Selecionar período:**
  * Clique no campo "Selecionar período" para abrir um seletor de datas.
  * Utilize o seletor para definir um **intervalo de datas** específico. A tabela de "Min Stay Aplicadas" e "Todas Min Stay" exibirá apenas as configurações de Min Stay que se sobrepõem a esse período.
* **Imóveis:**
  * Este filtro permite selecionar os imóveis específicos cujas configurações de Min Stay você deseja analisar.
  * **Campo "Digite para pesquisar":** Digite o código de um imóvel (ex: AAF1974) para encontrá-lo rapidamente na lista.
  * **Caixas de seleção:** Marque as caixas ao lado dos códigos dos imóveis para incluí-los na análise. Desmarque para excluí-los.
* **Origem:**
  * Este filtro permite selecionar a origem da configuração do Min Stay.
  * **Campo "Digite para pesquisar":** Digite um termo de pesquisa (ex: Calendário) para filtrar as opções.
  * **Caixas de seleção:** Marque as caixas para incluir ou excluir as opções de origem. As opções disponíveis são: Calendário, Mês, Período, Dias da semana, Gapper, Gapper - Calendário e Gapper - Período.

# 2. Min Stay Aplicadas

Esta tabela exibe as configurações de Min Stay que estão ativas e se enquadram nos filtros selecionados.

| Coluna | Descrição |
|:---|:---|
| **Imóvel** | Código de identificação do imóvel. |
| **Min Stay** | O número mínimo de noites de estadia exigidas para o imóvel. |
| **Primeiro Dia** | A data de início da validade da configuração de Min Stay. |
| **Último Dia** | A data de término da validade da configuração de Min Stay. |
| **Origem** | A origem do Min Stay (ex: Calendário, Período). |
| **Clima** | Indica o clima da região à qual o imóvel pertence (ex: Região quente). |
| **Ocorrência** | Detalha a ocorrência no período observado (ex: Carnaval, Dia normal, Reveillon). |
| **Sazonalidade** | Aponta a sazonalidade da região à qual o imóvel pertence dado o período observado (ex: Baixa temporada, Alta temporada). |
| **Gapper** | Número de dias disponíveis entre datas com reservas. |
| **Observação** | Observações relacionadas ao gapper (ex: Condomínio não aceita estadia menor que 7). |

* **Ordenação:** Clique nos cabeçalhos das colunas (por exemplo, "Imóvel" ou "Min Stay") para ordenar os dados em ordem crescente ou decrescente.

# 3. Todas Min Stay 

Esta tabela oferece uma visão abrangente de todas as configurações de Min Stay cadastradas, incluindo aquelas que podem não estar visíveis no dashboard principal devido aos filtros aplicados ou à sua data de validade.

| Coluna | Descrição |
|:---|:---|
| **Imóvel** | Código de identificação do imóvel. |
| **Min Stay** | O número mínimo de noites de estadia exigidas para o imóvel. |
| **Primeiro Dia** | A data de início da validade da configuração de Min Stay. |
| **Último Dia** | A data de término da validade da configuração de Min Stay. |
| **Origem** | A origem do Min Stay (ex: Calendário, Período). |
| **Aplicada** | Indica se a configuração de Min Stay está atualmente ativa ("Sim") ou não ("Não"). |
| **Clima** | Indica o clima da região à qual o imóvel pertence (ex: Região quente). |
| **Ocorrência** | Detalha a ocorrência no período observado (ex: Carnaval, Dia normal, Reveillon). |
| **Sazonalidade** | Aponta a sazonalidade da região à qual o imóvel pertence dado o período observado (ex: Baixa temporada, Alta temporada). |
| **Gapper** | Número de dias disponíveis entre datas com reservas. |
| **Observação** | Observações relacionadas ao gapper (ex: Condomínio não aceita estadia menor que 7). |

* **Paginação:** Utilize os controles de paginação localizados na parte inferior da tabela (indicando "1 - 100 / 163313") para navegar entre as páginas de resultados, caso haja um grande volume de dados.

# **Observações Importantes**

* **Atualização dos Dados:** O dashboard principal é atualizado na data indicada no canto superior direito ("Atualizado: 31 de jul. de 2025").