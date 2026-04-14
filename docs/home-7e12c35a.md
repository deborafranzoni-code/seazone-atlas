<!-- title: Home | url: https://outline.seazone.com.br/doc/home-m04PN8lYLc | area: Tecnologia -->

# Home

# PRD — Home "Command Center" Dashboard para Franquias

## 1. Visão Geral

Construir a **Home do sistema das franquias** como um **Command Center orientado a informação**, funcionando como:

* Visualizador primário da operação
* Consolidador de indicadores críticos
* Hub de navegação para todas as features
* Painel de acompanhamento diário, semanal e mensal

A proposta não é listar pendências isoladas, mas oferecer **leitura rápida da saúde operacional e financeira da franquia**, com navegação contextual para aprofundamento.


---

## 2. Objetivo do Produto

Criar uma home que permita, em até 10 segundos:

* Entender o volume operacional do dia
* Avaliar riscos e impactos financeiros
* Acompanhar churn e saúde da carteira
* Navegar para qualquer feature com contexto aplicado


---

## 3. Estrutura do Dashboard (Command Center)

A Home será estruturada em **5 módulos principais**.


---

# Módulo 1 — Snapshot do Dia

Indicadores rápidos e clicáveis:

* Check-ins hoje
* Check-outs hoje
* Vistorias agendadas
* Danos abertos
* Reembolsos pendentes (com valor total)
* Receita prevista hoje

### Comportamento

* Cada card é clicável
* Redireciona para a feature correspondente já filtrada por "Hoje"
* Exibe indicador visual de variação vs. média dos últimos 7 dias


---

# Módulo 2 — Pipeline Operacional

Visualização por etapa da operação:

| Etapa | Quantidade |
|----|----|
| Check-in pendente | X |
| Em hospedagem | X |
| Check-out pendente | X |
| Em vistoria | X |
| Em manutenção | X |

Permite entender onde está concentrado o volume operacional.

### Interação

Clique na etapa → Lista filtrada por status.


---

# Módulo 3 — Indicadores Financeiros Consolidados

Bloco com foco financeiro:

* Receita confirmada no mês
* Receita prevista
* Valor total em reembolsos
* Danos com cobrança pendente
* Resultado operacional estimado

Permite visão clara de impacto econômico da operação.


---

# Módulo 4 — Saúde da Carteira

Indicadores estratégicos:

* Total de imóveis ativos
* Imóveis em implantação
* Churn do mês
* Taxa de ocupação
* Média de diária

Cada métrica pode levar para:

* Página de imóveis
* Página de reservas
* Página de cancelamentos


---

# Módulo 5 — Navegação Estruturada

Menu lateral fixo com acesso direto:

### Reservas

* Lista geral
* Filtros por status

### Operacional

* Check-in
* Check-out
* Danos
* Vistoria
* Pesquisar e editar imóveis

### Manutenção

### Financeiro

* Reembolsos
* Extrato


---

## 4. Fluxos a Prototipar no Lovable

### 1. Drill-down por métrica

Card → Lista filtrada → Detalhe → Ação

### 2. Filtro global

Filtro superior com:

* Período (Hoje / Semana / Mês / Personalizado)
* Imóvel
* Status

Os filtros aplicam-se a todo o dashboard.

### 3. Estados de visualização

* Estado normal
* Estado sem dados
* Estado com volume elevado
* Estado de queda de performance

### 4. Persistência de contexto

Se usuário entrar em:\nHome → Check-ins Hoje → Voltar\nO sistema mantém filtro aplicado.


---

## 5. Arquitetura de Informação

Home\n├── Snapshot do Dia\n├── Pipeline Operacional\n├── Financeiro\n├── Saúde da Carteira\n└── Navegação

Cada bloco funciona como ponto de entrada contextual.


---

## 6. Requisitos Funcionais

* Todos os cards devem ser clicáveis
* Todos os dados devem suportar filtro por período
* Atualização automática (refresh periódico)
* Performance inferior a 2s de carregamento
* Permitir exportação de dados financeiros


---

## 7. Requisitos Não Funcionais

* Layout responsivo
* Hierarquia visual clara
* Uso consistente de cores por categoria:
  * Operacional
  * Financeiro
  * Estratégico
* Indicadores com comparação histórica


---

## 8. Métricas de Sucesso

* Aumento do uso da home como página inicial
* Redução do tempo médio até iniciar uma ação
* Aumento da navegação via cards vs menu lateral
* Aumento da visibilidade de indicadores financeiros


---

## 9. Diferencial Estratégico

Esse Command Center:

* Não é apenas um agregador de contadores
* Não é apenas um menu
* É um painel de leitura de negócio
* Une operação + financeiro + carteira

Ele transforma a franquia de executora reativa para gestora orientada por dados.


\