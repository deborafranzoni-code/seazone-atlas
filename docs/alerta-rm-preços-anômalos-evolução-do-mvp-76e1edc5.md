<!-- title: Alerta RM Preços Anômalos - Evolução do MVP | url: https://outline.seazone.com.br/doc/alerta-rm-precos-anomalos-evolucao-do-mvp-H2XW074eXi | area: Tecnologia -->

# Alerta RM Preços Anômalos - Evolução do MVP

V 3.0

### **1. Contexto e Objetivo**

**Contexto Atual:** O sistema atual de alertas de preços anômalos gera alto volume de ruído e trabalho manual para o time de Revenue Management. Os principais problemas identificados são:

* Duplicação de alertas em dias consecutivos
* Falta de histórico consolidado para análise
* Desalinhamento entre métricas do sistema e as utilizadas pelo RM

**Impacto no Negócio:**

* **Perda de receita:** Preços abaixo do mercado em períodos de alta demanda geram oportunidade perdida
* **Ocupação subutilizada:** Preços acima do mercado em curto prazo resultam em vagas ociosas
* **Desperdício de recursos:** O time de RM gasta tempo em excesso analisando alertas irrelevantes
* **Decisões baseadas em dados incompletos:** Falta de histórico impede análise de tendências e padrões

**Objetivo:** Evoluir o sistema para reduzir drasticamente o ruído, automatizar o fluxo de trabalho e fornecer um histórico estruturado para análise contínua e melhorias futuras.


### **2. Solução Proposta**

Visão geral da solução:

* **Melhoria na qualidade dos alertas:** Implementar filtros para eliminar alertas irrelevantes
* **Google Sheets como central de dados:** Manter histórico e permitir interação do usuário
* **Integração com Slack:** Enviar apenas notificações resumidas, direcionando para o Sheets
* **Armazenamento estruturado:** Utilizar BigQuery para armazenar histórico completo


### **3. Requisitos Funcionais**

#### **3.1. Melhoria na Qualidade dos Alertas**

**Requisitos:**


1. **Utilizar Preço Final:** O sistema deve considerar o preço final (com descontos aplicados) em vez do preço enviado
2. **Threshold de Relevância:**
   * Para alertas de preços altos: apenas gerar alerta se a diferença for > 5% E > R$20
   * Validar implementação existente do threshold de 10% acima do preço competidor
3. **Filtro de Preço Mínimo (Pmin):** Não gerar alerta se o preço já estiver no Pmin do proprietário
4. **Ocupação da Categoria:**
   * Para alertas de preços altos: apenas gerar alerta se a ocupação da categoria for < 40%
   * Dados de ocupação obtidos diretamente da plataforma financeira
5. **Janela de Análise para Preços Baixos:** Alterar de "1 a 6 meses" para "2 a 6 meses" (aproximadamente 2 a 6.5 meses)
6. **Dedupe por ID Único:** Cada alerta deve ter um ID único baseado em hash (Imovel + Categoria + Periodo)

#### **3.2. Estrutura do Google Sheets**

**Abas:**


1. **Preços_Alto_Ativos:** Alertas de preços altos não verificados
2. **Preços_Baixo_Ativos:** Alertas de preços baixos não verificados
3. **Preços_Alto_Arquivado:** Todos alertas de preços altos verificados
4. **Preços_Baixo_Arquivado:** Todos alertas de preços baixos verificados
5. **Dashboard:** Resumo de métricas e estatísticas

**Colunas:**

| **Ordem** | **Coluna** | **Descrição** | **Obrigatório** | **Tipo** |
|----|----|----|----|----|
| 1 | ID | Hash MD5 (Imovel + Categoria + Periodo) | Sim | Texto |
| 2 | Data Coleta | Data da geração do alerta | Sim | Data |
| 3 | Imóvel | ID do imóvel | Sim | Texto |
| 4 | Categoria | Categoria do imóvel | Sim | Texto |
| 5 | Período | Período das datas analisadas | Sim | Texto |
| 6 | Preço | Preço final do imóvel | Sim | Número |
| 7 | Preço Competidor | Preço de referência dos concorrentes | Sim | Número |
| 8 | Motivo | Motivo do alerta (ex: "alta temporada - P75") | Sim | Texto |
| 9 | Número de Competidores | Quantidade de concorrentes considerados | Sim | Número |
| 10 | Feriado/Evento | Indica se há feriado ou evento no período | Sim | Texto |
| 11 | **Status** | Status do alerta (selecionável) | Sim | Lista |
| 12 | **Check** | Checkbox para marcar como verificado | Sim | Booleano |
| 13 | Comentário | Campo livre para observações (não armazenado) | Não | Texto |

**Opções para o campo Status:**

* "Ajustado" (preço foi alterado com base no alerta)
* "Não Aplicável" (alerta não relevante)
* "Em Análise" (em avaliação)
* "Falso Positivo" (alerta incorreto)

#### **3.3. Fluxo de Dados e Integrações**

**Fluxo Diário:**


1. **Geração de Alertas:**
   * Cloud Function executa diariamente às 06:00( Validar horário com Pipeline de dados usados )
   * Aplica os filtros de qualidade (preço final, threshold, Pmin, ocupação, janela)
   * Gera alertas com ID único
2. **Atualização do Google Sheets:**
   * Script compara novos alertas com os existentes (usando ID)
   * Adiciona apenas novos alertas (append) nas respectivas abas
   * Mantém histórico completo (não apaga registros)
3. **Notificação no Slack:**
   * Script filtra alertas não checados (Check = FALSE)
   * Envia mensagem resumo para o canal: "🔍 X novos alertas não verificados. Acesse: \[link\]"
4. **Interação do Usuário:**
   * Usuário acessa planilha pelo link
   * **Passo 1:** Seleciona Status na coluna 11 \[OBRIGATÓRIO\]
   * **Passo 2:** Marca Check na coluna 12 \[BLOQUEADO até Status ser definido\]
   * Sistema move automaticamente para aba de arquivo
   * (Opcional) Adiciona Comentário para notas rápidas
5. **Arquivamento Automático:**
   * Ao marcar Check com Status definido, alerta é movido automaticamente para aba "Arquivado"
   * Abas "Arquivado" são somente leitura para o usuário
   * BigQuery ingere dados de todas as abas diariamente
6. **Limpeza de Histórico:**
   * Execução automática semanal (domingo, 23:00)
   * Remove alertas com mais de 30 dias das abas "Arquivado"
   * Menu manual disponível para limpeza imediata se necessário

#### **3.4. Armazenamento no BigQuery**

**Objetivo:** Armazenar histórico completo para análises futuras e melhorias no sistema

**Tabela: alertas_rm_historico**

| **Coluna** | **Tipo** | **Descrição** |
|----|----|----|
| id | STRING | ID único do alerta (hash) |
| data_coleta | DATE | Data da geração |
| imovel | STRING | ID do imóvel |
| categoria | STRING | Categoria do imóvel |
| periodo | STRING | Período das datas |
| preco | FLOAT | Preço final do imóvel |
| preco_competidor | FLOAT | Preço de referência |
| motivo | STRING | Motivo do alerta |
| num_competidores | INTEGER | Número de competidores |
| feriado_evento | STRING | Feriado ou evento |
| check | BOOLEAN | Se foi verificado |
| status | STRING | Status do alerta |
| data_status | DATE | Data da última atualização do status |
| data_insert_bq | TIMESTAMP | Data de inserção no BQ |


**Integridade dos Dados:**

* Alterações no campo "Status" no Sheets são replicadas diariamente no BigQuery
* Todo alerta arquivado garante status definido (validação preventiva)
* BigQuery serve como histórico imutável para análises


### **4. Requisitos Não Funcionais**


1. **Performance:**
   * O Google Sheets deve suportar até 10.000 linhas por aba sem perda significativa de performance
   * A atualização diária dos dados deve levar menos de 5 minutos
2. **Disponibilidade:**
   * O sistema deve executar diariamente
   * O Google Sheets deve estar disponível para acesso do usuário
3. **Usabilidade:**
   * Interface do Google Sheets deve ser intuitiva, com colunas congeladas para facilitar a navegação
   * Validação visual deve guiar o usuário no fluxo correto
   * Menu de ajuda deve estar disponível
4. **Segurança:**
   * Acesso ao Google Sheets restrito ao time de RM
   * Credenciais da Cloud Function e BigQuery armazenadas de forma segura

### **5. Entregáveis e Aprovações**

#### **Fase 1: Qualidade dos Alertas** 

* **Entregável:** Especificação detalhada dos filtros de qualidade
* **Aprovação:** Product Manager e Gerente de RM/ Analista de RM
* **Responsável:** Desenvolvedor de Dados

#### **Fase 2: Estrutura do Google Sheets**

* **Entregável:** Modelo do Google Sheets com colunas definidas e script de append
* **Aprovação:** Product Manager e Gerente de RM/ Analista de RM
* **Responsável:** Desenvolvedor de Dados

#### **Fase 3: Integração Slack e Limpeza** 

* **Entregável:** Script de envio para Slack e menu de limpeza no Sheets
* **Aprovação:** Product Manager
* **Responsável:** Desenvolvedor de Dados

#### **Fase 4: Armazenamento BigQuery** 

* **Entregável:** Esquema da tabela no BigQuery e script de ingestão
* **Aprovação:** Product Manager e Coordenador de Dados
* **Responsável:** Desenvolvedor de Dados

#### **Fase 5: Validação e Ajustes (contínuo)**

* **Entregável:** Relatório de pós-implementação com métricas
* **Aprovação:** Product Manager e Gerente de RM
* **Responsável:** Product Manager