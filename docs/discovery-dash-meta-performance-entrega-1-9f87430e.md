<!-- title: Discovery: Dash Meta Performance (Entrega 1) | url: https://outline.seazone.com.br/doc/discovery-dash-meta-performance-entrega-1-CjuLMEcpp1 | area: Tecnologia -->

# Discovery: Dash Meta Performance (Entrega 1)

**Versão:** 1.0\n**Data:** 09/12/2025\n**Objetivo:** Migração da POC local para ambiente Cloud (GCP), automação diária e estruturação de histórico.


## 1. Visão Geral e Arquitetura - Sugerida( Exemplo )

O objetivo desta entrega é **produtizar** a ferramenta atual. Não serão criadas novas regras de negócio ou novos gráficos, o foco é estabilidade, automação e disponibilidade.

### 1.1. Arquitetura Proposta (MVP Low-Cost)

Para atender ao requisito de baixo custo e simplicidade na GCP:

* **Compute:** Google Compute Engine (VM) - Menor custo benefício possível (Suficiente para script Python e Streamlit com poucos usuários).
  * *OS:* Linux (Debian/Ubuntu).
  * *Motivo:* Permite manter a estrutura de arquivos locais (data/raw, data/processed) sem precisar refatorar o código para usar Cloud Storage (buckets) neste primeiro momento.
* **Agendamento:** Crontab (Linux) interno na VM.
  * *Frequência:* Diária (ex: 06:00 AM) → Em sincronia com a atualização da Meta 2.0.
* **Armazenamento:** Disco Persistente da VM.
  * Retenção de arquivos CSV para histórico.
* **Acesso:** IP Estático ou DNS simples. Controle de acesso via autenticação nativa do Streamlit ou firewall de rede.


## 2. Requisitos de Engenharia de Dados (Backend)

### 2.1. Refatoração do 1_import_data.py

O script atual é interativo (input()), o que impede a automação. Ele precisa ser ajustado para rodar em *batch*.

* **Remover Interatividade:** Eliminar o while True e os inputs.
* **Loop de Execução (M0, M1, M2):** O script deve iterar automaticamente para extrair dados de 3 meses distintos a cada execução diária:

  
  1. **Mês Atual (M0):** Ex: Dezembro (Foco em acompanhamento diário).
  2. **Mês Seguinte (M1):** Ex: Janeiro (Foco em planejamento).
  3. **Mês +2 (M2):** Ex: Fevereiro (Visão futura).
* **Nomeamento de Arquivos:** Ajustar a saída para evitar sobreposição.
  * *Atual:* nome_arquivo.csv (sobrescreve ou usa data fixa).
  * *Novo Padrão:* raw/{nome_query}_REF_{anomes}_RUN_{data_execucao}.csv
  * *Exemplo:* meta_analysis_price_REF_2025-12_RUN_2025-12-09.csv

### 2.2. Refatoração do 2_data_prepar.py

* **Processamento em Lote:** O script deve ler os arquivos gerados no passo anterior.
* **Output Enriquecido:** Gerar arquivos processados mantendo a referência do mês analisado.
  * *Novo Padrão:* processed/final_enriched_REF_{anomes}_RUN_{data_execucao}.csv
* **Limpeza:** Garantir que colunas de data (timestamp) estejam padronizadas para leitura no Pandas.

### 2.3. Gestão de Histórico

* **Conceito:** O "Histórico" é a capacidade de ver como estava o M0 (Dezembro) no dia 05/12, no dia 06/12, etc.
* **Armazenamento:**
  * Manter arquivos CSV no disco.
  * **Política de Retenção (MVP):** Script de limpeza (cron) para arquivar ou deletar arquivos raw antigos (ex: > 30 dias) para economizar espaço, mantendo apenas os processed por 1 ano.


## 3. Requisitos de Aplicação (Frontend Streamlit)

### 3.1. Seletor de Mês de Análise (Novo Recurso)

Na Sidebar, substituir a lógica atual por dois seletores hierárquicos:


1. **Seletor de Mês de Referência (O que queremos ver?):**
   * Opções: Mês Atual (M0), Próximo Mês (M1), Mês Futuro (M2).
   * *Comportamento:* Ao selecionar "Próximo Mês", o dashboard carrega os dados de Janeiro (estando em Dezembro).
2. **Seletor de Data de Snapshot (Histórico):**
   * *Default:* Data de hoje (última execução).
   * *Opções:* Lista de datas passadas disponíveis para aquele Mês de Referência.
   * *Exemplo:* Estou vendo o **Mês de Dezembro (M0)**, mas quero ver como ele estava no dia **01/12**.

### 3.2. Ajustes Visuais

* **Rodapé:** Exibir claramente: *"Dados referentes a \[Mês/Ano\] | Atualizado em \[Data Execução\]"*.
* **Performance:** Implementar st.cache_data robusto, pois carregar CSVs pode ficar lento conforme o histórico cresce.

# **4. Definition of Done (DoD) & Critérios de Aceite**

Para considerarmos a **Entrega 1 (MVP)** concluída com sucesso, o produto deve atender aos seguintes critérios funcionais e de usabilidade:

#### **4.1. Acessibilidade e Estabilidade**

* **Acesso Web:** O dashboard deve estar acessível através de uma URL web estável (não rodando na máquina local de ninguém).
* **Disponibilidade:** A aplicação deve estar disponível 24/7.
* **Custo:** A infraestrutura escolhida deve respeitar a premissa de *low-cost* (baixo custo), adequada para poucos usuários e baixo volume de dados.

#### **4.2. Automação e Atualização de Dados**

* **Atualização Diária:** O pipeline de dados deve rodar automaticamente uma vez por dia (idealmente disponível para o usuário final até as **08:00 AM**), sem necessidade de intervenção humana (ex: apertar play, rodar script manual).
* **Confiabilidade:** Caso a atualização falhe, o dashboard deve exibir os dados do último dia disponível com sucesso, deixando claro no rodapé a data da última atualização (para não induzir o usuário ao erro).

#### **4.3. Funcionalidade: Navegação Temporal (M0, M1, M2)**

* **Visão de Futuro:** O usuário deve ter um seletor claro para alternar a visão entre:
  * **Mês Atual (M0):** Para gestão da meta corrente.
  * **Mês Seguinte (M1):** Para planejamento tático.
  * **Mês +2 (M2):** Para visão estratégica de antecipação.
* **Comportamento:** Ao mudar o seletor, todos os gráficos e KPIs devem ser recarregados para refletir o mês escolhido.

#### **4.4. Funcionalidade: Histórico (Snapshots)**

* **Consulta Retroativa:** Deve haver um seletor de "Data de Referência" (Snapshot).
  * *Padrão:* Deve vir pré-selecionado com a data de **hoje** (dados mais recentes).
  * *Histórico:* O usuário deve conseguir selecionar uma data passada (ex: 5 dias atrás) e ver exatamente como estava o painel naquele dia.
* **Retenção:** O sistema deve garantir o armazenamento dos dados históricos conforme os meses viram (ex: ao virar para Janeiro, os dados de Dezembro devem permanecer consultáveis via histórico).


---

### **5. Jornada do Usuário Esperada (User Flow)**

Para validar se a implementação técnica atingiu o objetivo de negócio, o fluxo de uso deve seguir esta lógica:

**Cenário: Hoje é dia 09/12 (Segunda-feira). O Gerente de Receita acessa o Dash.**


1. **Abertura:** O usuário acessa o link. O dashboard carrega exibindo, por padrão, o **Mês Atual (Dezembro)** com os dados extraídos na manhã de **09/12**.
2. **Verificação de Atualização:** O usuário confere no rodapé a mensagem: *"Dados atualizados em: 09/12/2025"*.
3. **Análise de Tendência (Histórico):**
   * O usuário nota que a métrica de "Imóveis na Berlinda" está alta.
   * Ele vai no seletor de Data e muda para **02/12** (uma semana atrás).
   * O painel recarrega. Ele percebe que o número era menor, concluindo que a performance piorou na última semana.
4. **Planejamento (Futuro):**
   * O usuário muda o seletor de Mês para **Janeiro (M+1)**.
   * O seletor de data mantém-se em **09/12** (ou a última disponível).
   * O painel exibe as metas e prévias de ocupação para Janeiro.