<!-- title: Auditoria de Variação de Concorrentes | url: https://outline.seazone.com.br/doc/auditoria-de-variacao-de-concorrentes-3EKJT6iuhK | area: Tecnologia -->

# Auditoria de Variação de Concorrentes

* **Iniciativa:** Auditoria de Variação de Concorrentes
* **Produto Associado:** Plataforma de Inteligência de Concorrentes (PIC)
* **Status:** Em Discovery
* **Versão:** 1.0


### 1. Resumo Executivo

A "Plataforma de Inteligência de Concorrentes" (PIC) nos permite avaliar a saúde estática dos nossos clusters. No entanto, uma dor operacional crítica persiste: o alto custo de investigação para entender **por que** o número total de concorrentes ativos flutua diariamente. Atualmente, quando o KPI de "Nº de Concorrentes" cai, o time de RM inicia um processo de análise manual, reativo e demorado para identificar as causas.

Este documento propõe a criação de uma nova funcionalidade, a **"Auditoria de Variação de Concorrentes"**, uma ferramenta de diagnóstico que adicionará uma dimensão temporal à PIC. O objetivo é transformar a análise de variação de um processo investigativo e custoso para um diagnóstico rápido e automatizado, permitindo que o time entenda as causas de qualquer mudança no universo de concorrentes em minutos, não em horas.

### 2. Contexto (Onde Estamos Hoje)

Nossos dashboards atuais, incluindo o "Painel de Saúde dos Clusters", fornecem uma "fotografia" diária da nossa base de concorrentes. Sabemos *quantos* concorrentes temos e qual a *qualidade* deles em um determinado dia.

Quando ocorre uma queda de 100 concorrentes de um dia para o outro, a equipe sabe que algo aconteceu, mas não sabe o quê. As causas podem ser diversas:

* Concorrentes deixaram de cumprir filtros mínimos (ex: nº de reviews, nota).
* Concorrentes não registraram faturamento nos últimos 90 dias.
* Problemas na coleta de dados (erros de scraping, bloqueios).
* Um concorrente foi "pausado" ou removido da plataforma de origem.

O processo para encontrar quais dos milhares de concorrentes foram afetados e por qual motivo é inteiramente manual, gerando um gargalo operacional significativo.


### 3. O Problema Central (A Dor que Enfrentamos)

**A Dor da Investigação Cega:** A falta de rastreabilidade sobre as mudanças na base de concorrentes torna a análise de variações um processo ineficiente e frustrante. O time de RM gasta um tempo valioso em tarefas de baixo valor (cruzamento de dados, investigação manual) em vez de focar em ações estratégicas. Isso gera três problemas secundários:


1. **Custo Operacional Elevado:** Horas de analistas são consumidas para diagnosticar problemas que poderiam ser identificados automaticamente.
2. **Lentidão na Resposta:** A demora para identificar a causa raiz (ex: um problema no scraper) atrasa a correção e pode impactar a precisão da precificação por dias.
3. **Perda de Confiança nos Dados:** Variações inexplicadas minam a confiança do time de RM nos dados que sustentam suas decisões diárias.


### 4. Solução Proposta: A Ferramenta de Auditoria de Variação

Propomos a criação de um novo dashboard ou aba dentro da PIC, chamado **"Auditoria de Variação de Concorrentes"**.

**Visão Geral da Ferramenta:**

Uma interface de diagnóstico projetada para comparar o status dos concorrentes entre duas datas e expor as razões exatas para qualquer mudança.

**Fluxo de Trabalho do Usuário:**


1. **Seleção do Período:** O usuário define o intervalo de análise . Filtros adicionais por Categoria, Polígono, etc., permitem focar a investigação.
2. **Resumo do Impacto:** KPIs de alto nível mostram a variação líquida e o detalhe bruto (quantos foram perdidos, quantos foram ganhos).
   * *Ex: Variação Líquida: -139 (150 perdidos, 11 ganhos).*
3. **Diagnóstico Detalhado (A Tabela de Auditoria):** O núcleo da ferramenta é uma tabela que lista **apenas os concorrentes que mudaram de status** (entraram ou saíram da lista de ativos). As colunas-chave incluem:
   * **Identificação:** ID do Concorrente, Categoria.
   * **Mudança de Status:** Status (Data Inicial) e Status (Data Final).
   * **Causa Raiz:** Uma coluna "Motivo da Mudança" que indica qual regra de negócio falhou (ex: "Filtro de Reviews", "Sem Faturamento Recente", "Erro de Coleta").
   * **Evidências:** Colunas adjacentes que mostram o valor que falhou na validação (ex: Nº de Reviews, comprovando o motivo.

**Benefícios Esperados:**

* **Redução do Tempo de Investigação:** De horas para minutos.
* **Aumento da Eficiência Operacional:** Libera o time de RM para focar em tarefas estratégicas.
* **Melhora na Qualidade dos Dados:** A identificação rápida de problemas (ex: falhas no scraper) acelera a correção na origem.
* **Restauração da Confiança:** Fornece transparência e explicabilidade sobre a dinâmica dos dados.

### 5. Análise de Viabilidade Técnica (Próximos Passos)

Para garantir o sucesso desta iniciativa, a equipe de engenharia de dados deverá realizar uma análise prévia para:


1. **Mapear Fontes de Dados:** Identificar e documentar todas as tabelas, queries e lógicas de negócio que definem o status "ativo" de um concorrente.
2. **Definir a Lista de "Motivos":** Com base no mapeamento, criar uma lista exaustiva de todos os motivos possíveis para um concorrente mudar de status.
3. **Desenhar a Lógica de Comparação:** Projetar o processo de "snapshot" e comparação que alimentará a tabela de auditoria de forma eficiente.


\