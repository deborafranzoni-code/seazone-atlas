<!-- title: Faturamento | url: https://outline.seazone.com.br/doc/faturamento-osfBCCgigH | area: Tecnologia -->

# Faturamento

# Visualização de Faturamento Financeiro da Franquia

## 1. Contexto

Atualmente a franquia não possui uma visão consolidada, clara e confiável do seu faturamento financeiro por período. A ausência dessa visão gera:

* Dificuldade de conciliação financeira
* Baixa previsibilidade de caixa
* Dúvidas recorrentes sobre valores repassados
* Falta de transparência sobre impacto de ajustes e despesas

É necessário criar uma **visão consolidada de faturamento**, com regras financeiras explícitas e separação correta entre competência e pagamento.


---

## 2. Objetivo

Permitir que a franquia visualize, de forma clara e consolidada:

* Seu faturamento por período (mês)
* Separação entre valores executados e valores pagos
* Impacto de reservas Booking com pagamento no mês subsequente
* Resultado financeiro final
* Saldo após repasses


---

## 3. Escopo

### 3.1 Filtros obrigatórios

O usuário deve conseguir:

* Visualizar dados de **todos os imóveis**
* Visualizar dados de **um imóvel específico**
* Filtrar por **mês/ano**


---

## 4. Regras de Negócio Críticas

### 4.1 Regra Booking (Regra Principal)

Reservas originadas do Booking possuem a seguinte lógica:

* A reserva é **executada no mês X**
* O pagamento ocorre **no mês X+1**

Logo:

O sistema deve separar claramente:

* Reservas executadas e pagas no mesmo mês
* Reservas executadas no mês anterior e pagas no mês atual

Essa separação deve impactar diretamente o cálculo de:

* Reservas pagas
* Resultado
* Saldo


---

## 5. Estrutura da Visualização

A visualização será mensal e organizada em blocos financeiros.


---

# BLOCO 1 — Entradas

### 5.1 Reservas Pagas

Exibir:

* Total pago no mês atual
* Total pago referente a reservas executadas no mês anterior
* Total pago referente a reservas executadas no próprio mês

Visualização sugerida:

Reservas Pagas

* Mês atual (competência atual)
* Mês anterior (Booking e similares)


---

### 5.2 Limpezas Pagas

Exibir:

* Total pago no mês atual
* Total pago no mês anterior


---

### 5.3 Reembolsos Pagos

Valor total de reembolsos efetivamente pagos no período.


---

### 5.4 Ajustes Positivos Pagos

Qualquer ajuste financeiro que aumente receita.


---

# BLOCO 2 — Saídas

### 5.5 Saídas

Inclui:

* Ajustes negativos de reserva
* Despesas operacionais
* Estornos
* Qualquer débito lançado contra a franquia


---

### 5.6 Taxa de Franquia

* Valor total cobrado como taxa
* Deve estar claramente destacado como saída


---

# BLOCO 3 — Repasses

### 5.7 Repasses Efetuados

* Total efetivamente transferido para conta da franquia no mês
* Pode haver múltiplos repasses no período
* Deve ser exibido valor consolidado


---

# BLOCO 4 — Indicadores Finais

### 5.8 Resultado

Fórmula:

Resultado =\n(Reservas Pagas\n+ Limpezas Pagas\n+ Reembolsos Pagos\n+ Ajustes Positivos)\n-\n(Saídas\n+ Taxa de Franquia)


---

### 5.9 Saldo

Fórmula:

Saldo = Resultado - Repasses Efetuados

Pode ser:

* Positivo → Valor a receber
* Negativo → Valor a compensar nos próximos ciclos


---

## 6. Comportamentos do Sistema

* Valores devem refletir apenas lançamentos com status "pago"
* Alterações retroativas devem atualizar automaticamente os meses impactados
* Deve existir drill-down por categoria (ex: clicar em Reservas Pagas abre detalhamento)
* Valores devem ser consolidados respeitando a data de pagamento, não apenas data de execução


---

## 7. Critérios de Aceite


1. Usuário consegue alternar entre visão consolidada e por imóvel.
2. Booking aparece corretamente no mês subsequente.
3. Resultado e Saldo fecham matematicamente.
4. Total de repasses corresponde à soma real das transferências.
5. Não há divergência entre relatório e extrato financeiro.


---

## 8. Métricas de Sucesso

* Redução de chamados financeiros da franquia
* Redução de dúvidas sobre repasse
* Diminuição de divergência entre sistema e extrato bancário
* Aumento da confiança na visão financeira