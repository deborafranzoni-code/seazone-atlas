<!-- title: Product Discovery: BI VivaReal - Portal de Extração de Dados | url: https://outline.seazone.com.br/doc/product-discovery-bi-vivareal-portal-de-extracao-de-dados-d2hH1cIsx7 | area: Tecnologia -->

# Product Discovery: BI VivaReal - Portal de Extração de Dados

**Versão:** 3.0\n**Data:** 12 de Agosto de 2025\n**Autor:** \[Lucas Abel da Silveira PM/Dados\]\n**Stakeholders:** Time de Investimentos / Lançamentos


### **1. Resumo Executivo**

Este documento descreve a proposta de desenvolvimento de um novo **Portal Unificado de Extração de Dados VivaReal**. O objetivo é substituir o ecossistema atual, que consiste em (1) um BI limitado no Power BI e (2) um processo de solicitações manuais via suporte. A nova plataforma de **self-service** permitirá que a equipe de Investimentos aplique filtros, valide e exporte bases de dados limpas e prontas para análise de **todas as regiões de interesse**, eliminando gargalos, aumentando a agilidade e garantindo a confiança nas informações.


### **2. Diagnóstico do Cenário Atual: Um Processo Fragmentado**

Após análise do fluxo de trabalho atual, identificamos um sistema fragmentado com dois principais pontos de dor que geram ineficiência para ambas as equipes (Dados e Investimentos):

**Problema 1: O BI Atual em Power BI é Lento e Limitado.**

* **Escopo Restrito:** A ferramenta atual atende exclusivamente às praças da **Bahia e Florianópolis**. Qualquer análise fora dessas regiões fica impossibilitada via self-service.
* **Performance Comprometida:** O BI sofre com a sobrecarga de dados brutos e não tratados (duplicatas, outliers), resultando em lentidão e uma experiência de uso frustrante.
* **Falta de Confiança:** Os dados crus exigem que o usuário faça validações manuais para garantir que está utilizando informações precisas e atualizadas.

**Problema 2: A Dependência de Suporte Manual é um Gargalo Operacional.**

* **Processo Reativo:** Para qualquer região fora de BA e FL, a equipe de Investimentos precisa abrir um chamado de suporte para a equipe de Dados.
* **Ineficiência Operacional:** Cada pedido exige que um membro da equipe de Dados interrompa suas atividades para executar queries manuais, extrair os dados e enviá-los. Isso cria um **gargalo** que atrasa as análises do time de Investimentos e consome recursos valiosos do time de Dados.
* **Falta de Padronização:** As extrações manuais podem variar, dificultando a criação de um processo de análise padronizado e escalável para a equipe de Investimentos.


### **3. Proposta de Valor e Solução: Um Portal Único e Eficiente**

Propomos a substituição completa do processo atual por uma única ferramenta no Looker Studio, focada no fluxo: **Filtrar → Validar → Exportar**.

**Objetivos Estratégicos:**

* **Unificar o Processo:** Eliminar a fragmentação entre o Power BI e os tickets de suporte, criando uma **fonte única da verdade** para extração de dados do VivaReal.
* **Garantir Autonomia Total:** Empoderar a equipe de Investimentos para que realize extrações de **qualquer região** sem depender da equipe de Dados.
* **Otimizar Recursos:** Liberar a equipe de Dados do trabalho operacional de extrações manuais, permitindo foco em projetos de maior valor estratégico.
* **Aumentar a Confiança e Agilidade:** Entregar dados pré-processados e limpos, permitindo que a análise de viabilidade de terrenos seja feita em minutos, não em dias.


### **4. Requisitos e Funcionalidades Chave**

A solução proposta será construída sobre uma base sólida de regras de negócio automatizadas e uma interface de usuário intuitiva.

#### **4.1. Regras de Negócio e Tratamento de Dados (Lógica Aplicada no Backend)**

Esta é a inteligência central da ferramenta. Antes de qualquer dado ser exibido na tela, as seguintes regras serão aplicadas automaticamente para garantir a qualidade e a relevância da base de dados:


1. **O Filtro Principal: Unicidade e Validade do Anúncio**
   * **Regra:** A consulta à base de dados incluirá a condição data da última aquisição = data de aquisicao.
   * **Justificativa:** Este é o requisito mais crítico. Ele garante que apenas o registro mais recente e válido de cada anúncio seja utilizado, eliminando duplicatas históricas e assegurando que as análises de valor sejam feitas sobre o preço mais atual do imóvel.
2. **Redução de Outliers e Dados Irrelevantes (Limpeza Automática)**
   * **Regra:** A consulta excluirá registros que não atendam à condição tamanho >= 12.
   * **Justificativa:** Com base no feedback da equipe, imóveis com tamanho inferior a 12 (especialmente o valor "10") são considerados outliers ou erros de cadastro. Sua remoção automática aumenta a confiabilidade do dataset.
3. **Priorização de Campos de Data**
   * **Regra:** O campo data de aquisição será o principal pilar para filtros de tempo e análises de valorização.
   * **Justificativa:** O campo data de criação será mantido como um dado informativo na extração final, mas não será utilizado como chave para as análises, alinhando a ferramenta ao processo de negócio da equipe de Investimentos.

#### **4.2. Interface do Usuário e Filtros de Self-Service (Controles do Frontend)**

O usuário terá controle total sobre a segmentação dos dados com os seguintes componentes:

* **Filtro de Período de Aquisição:** Um seletor de período com **campos de data de início e fim** para permitir a seleção de intervalos específicos (ex: 01/01/2024 a 31/07/2024).
* **Filtro de Tipo de Imóvel:** Um filtro de **seleção múltipla** (checkboxes) que permite ao usuário escolher uma ou mais opções, incluindo **Apartamento, Casa, Comercial e Terreno**.
* **Filtro de Bairro e Nome do Anunciante:** Filtros de busca que permitem a **seleção múltipla** de um ou mais itens.
* **Filtro de Número de Quartos:** Um filtro de **seleção múltipla** (checkboxes) com as opções "0", "1", "2", "3", "4", "5+", permitindo a escolha de categorias específicas (ex: apenas "1" e "3" quartos).

#### **4.3. Funcionalidades de Validação e Extração**

* **KPIs de Validação:** Cards simples para o usuário confirmar o resultado de seus filtros:
  * **Imóveis Únicos Encontrados**: Informa o número exato de linhas que o arquivo .CSV exportado conterá.
* **Botão de Ação Principal:** Um botão de destaque para **"Exportar para .CSV"**, permitindo o download imediato dos dados da tabela.
* **Tabela de Dados Detalhada:**
  * **Visualização:** A interface exibirá uma tabela com as colunas mais relevantes para uma validação visual rápida antes da extração.
  * **Manutenção de Features:** O arquivo .CSV exportado conterá **todas as colunas já existentes** no processo de extração atual, garantindo que não haverá perda de informações. A estrutura de dados completa será mantida, incluindo:
    * bairro, cep, cidade, data da última aquisição, data de aquisicao, data de criação, id do anunciante, id do anúncio, link, link do anunciante, nome do anunciante, número de quartos, número do anunciante, tamanho, tipo, valor da unidade.

#### **4.4. Decisões de Escopo (Versão 1) e Considerações Futuras**

Para garantir uma entrega de valor rápida e focada, as seguintes decisões de escopo foram tomadas para a primeira versão da ferramenta:

* **Escopo da Versão 1 (Foco na Limpeza):** A ferramenta será focada em entregar uma base de dados **limpa, atual e desduplicada**, resolvendo o principal gargalo do processo atual. Por isso, a regra de unicidade do anúncio (data da última aquisição = data de aquisicao) será o pilar desta versão.
* **Consideração para Versão 2 (Histórico de Anúncios):** O feedback sobre a necessidade de visualizar o histórico de um mesmo anúncio foi registrado como uma demanda estratégica. Esta funcionalidade será avaliada para uma futura versão, pois requer uma investigação técnica sobre a viabilidade de recuperar dados de anúncios cujos links já não existem e um redesenho da lógica de consulta para não conflitar com o objetivo de limpeza da V1.