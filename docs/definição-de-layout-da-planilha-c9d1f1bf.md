<!-- title: Definição de Layout da Planilha | url: https://outline.seazone.com.br/doc/definicao-de-layout-da-planilha-Ug4c1pzyZD | area: Tecnologia -->

# Definição de Layout da Planilha

[Layout Planilha](https://docs.google.com/spreadsheets/d/1dhVYbeHSlL9k9a6vPY8lczutQ5Jbl-WnJFFyXCcnous/edit?gid=1787875739#gid=1787875739): sta planilha é um template para visualização e demonstração. Os dados apresentados são ilustrativos e não representam dados reais.

## **1.Atualização de Dados:**


* **Automática:** A planilha Meta 2.0 é projetada para atualização automática de dados. As informações são extraídas diretamente do Data Lake, eliminando a necessidade de input manual de dados.
* **Sem Aba de Input:** Não há uma aba de "Input" tradicional. Os dados base para o cálculo são acessíveis e auditáveis através da planilha de auditoria (camada audit no Data Lake).
* **Re-execução em Caso de Bugs:** Em situações de erros ou necessidade de reprocessamento, a re-execução da planilha requer um pedido de suporte ao time de dados. Este time será responsável por iniciar uma nova rodada de atualização dos dados na planilha.

  \

## 2. **Abas de Output:**


* **Output M+0 (Mensal - Mês Vigente):**
  * Conteúdo: Apresenta os dados de cálculo de metas para o mês vigente (Mês atual - "M+0").
  * Atualização: Diária, garantindo que os dados sejam atualizados regularmente ao longo do mês. A atualização ocorre até o fechamento do mês + 1 dia.
  * Congelamento: Após o fechamento do mês + 1 dia, os dados desta aba são "congelados" e tornam-se não modificáveis. Para consultas históricas, os dados congelados devem ser acessados diretamente no Banco de Dados (Data Lake).
* **Output M+1 (Mensal - Próximo Mês):**
  * Conteúdo: Apresenta os dados de cálculo de metas para o próximo mês (Mês seguinte ao vigente - "M+1").
  * Atualização e Congelamento: Segue o mesmo processo de atualização diária e congelamento que a aba "Output M+0".
* **Output M+2 (Mensal - Dois Meses à Frente):**
  * Conteúdo: Apresenta os dados de cálculo de metas para o mês posterior ao próximo (Dois meses à frente do vigente - "M+2").
  * Atualização e Congelamento: Segue o mesmo processo de atualização diária e congelamento que as abas "Output M+0" e "Output M+1".
* **Output Trimestral (Trimestre Vigente):**
  * Conteúdo: Apresenta os dados de cálculo de metas para o trimestre vigente.
  * Atualização: A atualização ocorre ao longo do trimestre até o seu fechamento + 1 dia.
  * Congelamento: Após o fechamento do trimestre + 1 dia, os dados desta aba são "congelados" e tornam-se não modificáveis. Para consultas históricas, os dados congelados devem ser acessados diretamente no Banco de Dados (Data Lake).
* **Output Trimestral Confirmada (Trimestre Vigente - Dados Confirmados):**
  * Conteúdo: Apresenta os dados de cálculo de metas trimestrais, com faturamento considerado **apenas até o dia anterior à data de execução da planilha (D-1)**.
  * Objetivo: Fornecer uma visão "confirmada" do trimestre, excluindo o dia corrente.
  * Atualização: A aba é atualizada a cada rodada da planilha, refletindo o faturamento acumulado até D-1.
  * Equivalência: No último dia do trimestre, o conteúdo desta aba deve ser idêntico ao da aba "Output Trimestral", pois ambas considerarão o mesmo período de faturamento.

## 3. **Aba "Board" (Painel de Controle):**


* **Função:** A aba "Board" serve como um painel de controle centralizado, agregando e visualizando os resultados dos cálculos de metas para cada mês e trimestre.
* **Cálculos Via AppScript:** Os cálculos e a organização dos dados nesta aba são realizados através de scripts Apps Script, que referenciam as abas de "Output Mensal" e "Output Trimestral".
* **Status Congelado:** Após o fechamento de cada mês ou trimestre, o "Board" exibe o resultado final "congelado" para aquele período, permitindo o acompanhamento histórico das metas.
* **Visualização Trimestral:** A aba também oferece uma visualização consolidada do resultado final do trimestre.

## 4. **Aba "Farol" (Indicador Visual):**


* **Indicador Visual de Meta:** A aba "Farol" fornece um indicador visual do status da meta, facilitando a rápida identificação de imóveis que atingiram ou não suas metas.
* **Visão Mensal:** Apresenta um histórico diário da meta mensal, permitindo acompanhar a evolução do status da meta ao longo do mês até o momento do congelamento. O cálculo do "Farol Mensal" é feito via AppScript.
* **Visão Trimestral:** Exibe as metas calculadas em relação ao faturamento trimestral, permitindo acompanhar a performance ao longo do trimestre. O cálculo do "Farol Trimestral" também é feito via AppScript.\n