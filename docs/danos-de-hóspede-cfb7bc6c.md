<!-- title: Danos de Hóspede | url: https://outline.seazone.com.br/doc/danos-de-hospede-0UYEZZcYkv | area: Tecnologia -->

# Danos de Hóspede

## 1. Visão Geral

Este documento descreve a criação do **módulo de Danos de Hóspede** no sistema da franquia, permitindo:

* Registrar danos vinculados a uma **reserva específica**
* Operacionalizar tratativa (cobrança, conserto, limpeza ou contratação de serviço)
* Gerenciar evidências e orçamentos
* Acompanhar status até a resolução financeira ou encerramento
* Converter automaticamente **possíveis danos identificados na limpeza** em lançamentos formais

O fluxo deve garantir rastreabilidade, padronização operacional e controle financeiro.


---

## 2. Objetivos do Produto

* Garantir que **todo dano esteja vinculado a uma reserva**
* Reduzir perda de prazo para abertura de disputa (Airbnb/OTA)
* Padronizar categorização e registro de evidências
* Permitir acompanhamento claro por status
* Conectar operação (limpeza/manutenção) com financeiro


---

## 3. Perfis de Usuário

* **Franquia Seazone** (usuário principal)
* Time de apoio (financeiro/jurídico — visualização futura)


---

# 4. Estrutura da Tela Principal — "Danos de Hóspede"

A tela principal deve conter:

### 4.1 Abas


1. **Possíveis Danos (vindos da limpeza)**
2. **Danos Lançados**
3. **Todos**


---

## 4.2 Lista de Possíveis Danos

Origem: formulário de limpeza/vistoria pós-checkout.

### Estrutura da Lista

Cada item deve exibir:

* Imóvel
* Reserva vinculada
* Nome do hóspede
* Data de checkout
* Evidência (thumbnail da imagem)
* Data do registro
* Status: "Possível dano"

### Ação principal:

Botão: **"Lançar Dano"**

Ao clicar:

* Abre tela de lançamento
* Campos pré-preenchidos:
  * Imóvel
  * Reserva
  * Evidências já anexadas
  * Observação do time de limpeza


---

# 5. Fluxo de Lançamento de Dano

## 5.1 Regra Estrutural Obrigatória

> Todo dano deve estar obrigatoriamente vinculado a uma reserva.

Não é permitido criar dano sem:

* Selecionar imóvel
* Selecionar reserva


---

## 5.2 Etapas do Fluxo

### Etapa 1 — Identificação do Imóvel

Campo: Select com busca

Após selecionar imóvel:

* Sistema carrega automaticamente:
  * Últimas reservas (ordenadas por checkout mais recente)

Regra:

* Exibir no mínimo últimas 10 reservas
* Destacar reservas encerradas nos últimos 7 dias


---

### Etapa 2 — Seleção da Reserva

Exibir:

* Nome do hóspede
* Canal (Airbnb, Booking, Direto)
* Datas check-in/check-out
* Status da reserva
* Valor total

Bloqueio:

* Se reserva estiver fora do prazo de disputa (configurável por canal), exibir alerta.


---

### Etapa 3 — Categoria do Problema

Campo obrigatório.

Exemplo de categorias:

* Mobília
* Eletrodomésticos
* Enxoval
* Estrutura
* Utensílios
* Limpeza extraordinária
* Outros


---

### Etapa 4 — Item Danificado

Campo dependente da categoria.

Pode ser:

* Dropdown pré-configurado
* Ou campo aberto se categoria = "Outros"


---

### Etapa 5 — Detalhamento Financeiro

Campos obrigatórios:

* Quantidade
* Valor unitário
* Valor total (calculado automaticamente)
* Evidências (upload múltiplo)
* Observação detalhada do ocorrido

Regras:

* Pelo menos 1 evidência obrigatória
* Permitir anexar fotos, vídeos ou PDF
* Valor total sempre recalculado automaticamente


---

### Etapa 6 — Ação Necessária

Campo obrigatório (radio button):

* Cobrar pendência do hóspede
* Conserto
* Limpeza extraordinária
* Contratar serviço terceirizado


---

### Etapa 7 — Orçamento

Obrigatório quando:

* Ação = Conserto
* Ação = Contratar serviço terceirizado

Permitir:

* Upload de orçamento (PDF ou imagem)
* Ou inserção de link externo


---

### Etapa 8 — Confirmação

Botão: **"Registrar Dano"**

Ao confirmar:

* Status inicial: **Solicitação**
* Gera ID único do dano
* Registra log de criação (data + usuário)


---

# 6. Estrutura da Tela de Danos Lançados

Lista com filtros:

* Imóvel
* Período
* Status
* Canal
* Hóspede

Cada card deve exibir:

* ID do dano
* Imóvel
* Hóspede
* Canal
* Valor total
* Status
* Data de abertura

Ação ao clicar: abrir detalhes completos.


---

# 7. Fluxo de Status do Dano

Os danos podem assumir os seguintes status:


 1. **Solicitação**
 2. **Validação**
 3. **Cobrança com Airbnb**
 4. **Cobrança com OTA**
 5. **Cobrança com Hóspede**
 6. **Cobrança Easy Cover**
 7. **Cobrança Judicial**
 8. **Pago**
 9. **Finalizado sem sucesso**
10. **Cancelado**


---

## 7.1 Regras de Transição

### Solicitação → Validação

* Quando franquia finaliza documentação

### Validação → Cobrança

* Quando definido canal de cobrança

### Cobrança → Pago

* Quando valor recebido

### Cobrança → Finalizado sem sucesso

* Quando disputa é encerrada negativamente

### Qualquer status → Cancelado

* Apenas se ainda não estiver "Pago"


---

# 8. Tela de Detalhe do Dano

Deve conter:

* Dados da reserva
* Dados do hóspede
* Histórico completo de status (timeline)
* Evidências
* Orçamentos
* Logs de movimentação
* Campo para adicionar novas evidências
* Botão para alterar status


---

# 9. Regras de Negócio Críticas


1. Não permitir dano sem reserva.
2. Não permitir exclusão de dano com status "Pago".
3. Manter histórico imutável de movimentações.
4. Se origem for "Possível dano da limpeza":
   * Marcar flag de origem automática.
5. Permitir múltiplos danos na mesma reserva.
6. Permitir múltiplos itens dentro do mesmo dano.


---

# 10. Indicadores (Métricas Futuras)

* Total de danos por imóvel
* Taxa de sucesso de cobrança
* Tempo médio até resolução
* Valor recuperado por canal
* Percentual de danos vindos da limpeza


---

# 11. Estrutura Técnica Recomendada

### Entidades Principais:

* Damage
* DamageItem
* DamageEvidence
* DamageBudget
* DamageStatusHistory

Relacionamentos:

* 1 Reserva → N Danos
* 1 Dano → N Itens
* 1 Dano → N Evidências
* 1 Dano → N Mudanças de Status


---

# 12. Resultado Esperado

Ao final da implementação, a franquia deve:

* Identificar rapidamente possíveis danos
* Formalizar o lançamento de forma estruturada
* Garantir documentação adequada
* Acompanhar cobrança até o desfecho
* Ter visibilidade clara do impacto financeiro


---

Se quiser, posso transformar isso em:

* PRD técnico para desenvolvimento
* System prompt para prototipação no Lovable
* Fluxo de jornada detalhado
* Modelo de banco de dados
* Ou estrutura de API

Qual próximo passo você quer aprofundar?