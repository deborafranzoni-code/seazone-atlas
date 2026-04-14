<!-- title: Visualizar reservas | url: https://outline.seazone.com.br/doc/visualizar-reservas-LdIUK6Hauc | area: Tecnologia -->

# Visualizar reservas

# PRD — Calendário Global Multi-Imóvel

### Produto: Gestão Operacional da Franquia

### Versão: MVP

### Foco: Mobile First


---

# 1. Problema

Franquias com \~30 imóveis precisam:

* Visualizar todas as reservas em um único lugar
* Identificar rapidamente datas livres
* Criar bloqueios sem risco de conflito
* Entender ocupação geral do portfólio

Hoje a visualização não é consolidada e exige navegação excessiva.


---

# 2. Objetivo

Criar uma **visualização global tipo grade (grid calendar)** onde:

* Linhas = imóveis
* Colunas = dias
* Scroll vertical → imóveis
* Scroll horizontal → datas

Permitindo:

* Visualização rápida de ocupação
* Criação de bloqueios direto na célula
* Visualização rápida de dados essenciais da reserva


---

# 3. Estrutura de Telas (Lovable)


---

## TELA 01 — Calendário Global

### Layout Base (Mobile)

Header fixo:

* Título: "Calendário"
* Seletor de mês
* Botão filtro (ícone)

Sub-header fixo:

* Linha de datas (rolagem horizontal sincronizada)

Corpo:

* Lista vertical de imóveis
* Cada linha contém:
  * Nome do imóvel (fixo à esquerda)
  * Grade de dias (rolável horizontalmente)

Footer fixo:

* Botão flutuante "Novo Bloqueio"


---

# 4. Componentes Reutilizáveis

## 4.1 Célula de Dia (Cell Component)

Estados possíveis:


1. Livre
   * Fundo branco
   * Borda sutil
2. Reservado
   * Fundo verde
   * Tooltip com nome do hóspede
3. Bloqueio Limpeza
   * Fundo azul
4. Bloqueio Manutenção
   * Fundo laranja
5. Estado de conflito (erro)
   * Fundo vermelho
   * Ícone alerta


---

## 4.2 Card Reserva (Bottom Sheet)

Campos obrigatórios:

* Nome do hóspede
* Check-in
* Check-out
* Total de noites
* Valor da reserva
* Valor da taxa de limpeza
* Origem da reserva

CTA:

* Ver detalhes completos


---

## 4.3 Modal Criar Bloqueio

Campos:

* Imóvel (pré-selecionado se iniciado da célula)
* Data início
* Data fim
* Motivo (radio button)
  * Limpeza
  * Manutenção
* Campo descrição (obrigatório)

Botões:

* Cancelar
* Confirmar Bloqueio


---

# 5. Fluxos Principais


---

## FLUXO 01 — Visualizar Reserva


1. Usuário toca em célula verde
2. Abre bottom sheet
3. Exibe dados da reserva
4. Usuário pode fechar ou acessar detalhes

Critério de aceite:

* Informações devem carregar em até 1s
* Datas devem estar consistentes com backend


---

## FLUXO 02 — Criar Bloqueio via Célula


1. Usuário toca em célula branca (livre)
2. Aparece opção: "Criar Bloqueio"
3. Usuário seleciona intervalo arrastando horizontalmente
4. Abre modal de bloqueio
5. Seleciona motivo
6. Insere descrição
7. Confirma

Validações:

* Não permitir selecionar datas com reserva
* Não permitir sobreposição de bloqueio
* Campo descrição obrigatório
* Motivo obrigatório

Após confirmação:

* Atualiza grid imediatamente
* Exibe toast de sucesso


---

## FLUXO 03 — Novo Bloqueio via Botão Flutuante


1. Usuário clica em "Novo Bloqueio"
2. Seleciona imóvel
3. Seleciona datas
4. Motivo
5. Descrição
6. Confirmar


---

# 6. Regras de Negócio

### Reserva deve exibir:

* Check-in
* Check-out
* Total de noites (cálculo automático)
* Dados do hóspede
* Valor total reserva
* Valor taxa limpeza
* Origem da reserva


---

### Bloqueio:

* Só pode ser criado em datas livres
* Não pode sobrepor reservas
* Não pode sobrepor bloqueios existentes
* Motivo obrigatório
* Descrição obrigatória
* Deve registrar:
  * Usuário que criou
  * Data criação
  * Timestamp


---

# 7. Estados do Sistema

### Estado Vazio

* Caso imóvel não tenha reservas no mês
* Exibir grid totalmente livre

### Estado Carregando

* Skeleton loading nas células

### Estado Erro

* Mensagem:\n"Erro ao carregar calendário"
* Botão "Tentar novamente"


---

# 8. Filtros (Versão MVP+)

Filtro por:

* Imóvel
* Status:
  * Reservado
  * Livre
  * Bloqueado
* Origem da reserva


---

# 9. Performance (Importante para Lovable)

* Virtualização de lista (30 imóveis)
* Carregar apenas mês atual
* Scroll horizontal fluido
* Atualização otimista após bloqueio


\
# Prompt Lovable

Crie um protótipo mobile-first de um sistema de gestão de reservas e bloqueios para franquias que administram em média 30 imóveis.

O objetivo é permitir visualização global de reservas e criação de bloqueios diretamente no calendário.


---

## CONTEXTO DO PRODUTO

Usuário: Franqueado operacional\nUso principal: Mobile\nQuantidade média: 30 imóveis\nNecessidade principal: Visualizar reservas + criar bloqueios sem conflito


---

## TELA PRINCIPAL — CALENDÁRIO GLOBAL MULTI-IMÓVEL

## Estrutura Geral

Layout mobile-first.

Header fixo contendo:

* Título: "Calendário"
* Seletor de mês
* Ícone de filtro

Sub-header fixo:

* Linha horizontal com dias do mês (scroll horizontal)

Corpo da tela:

* Lista vertical de imóveis
* Cada linha representa um imóvel
* Cada linha possui:
  * Nome do imóvel fixo à esquerda
  * Grade de dias rolável horizontalmente

Scroll vertical → imóveis\nScroll horizontal → dias

Rodapé:

* Botão flutuante fixo: "Novo Bloqueio"


---

# COMPORTAMENTO DAS CÉLULAS DO CALENDÁRIO

Cada célula representa 1 dia de 1 imóvel.

Estados possíveis:


1. Livre

* Fundo branco
* Toque abre opção "Criar Bloqueio"


2. Reservado

* Fundo verde
* Toque abre bottom sheet com dados da reserva


3. Bloqueio - Limpeza

* Fundo azul


4. Bloqueio - Manutenção

* Fundo laranja


5. Conflito (não pode selecionar)

* Fundo vermelho
* Ícone de alerta


---

# FLUXO 1 — VISUALIZAR RESERVA

Ao tocar em uma célula verde:

Abrir bottom sheet contendo:

* Nome do hóspede
* Check-in
* Check-out
* Total de noites (cálculo automático)
* Valor total da reserva
* Valor da taxa de limpeza
* Origem da reserva

Botão:

* "Ver detalhes completos"

Fechar ao arrastar para baixo.


---

# FLUXO 2 — CRIAR BLOQUEIO DIRETO NA CÉLULA

Ao tocar em uma célula livre:


1. Exibir opção "Criar Bloqueio"
2. Permitir selecionar intervalo de datas arrastando horizontalmente
3. Após seleção, abrir modal com:

Campos:

* Imóvel (preenchido automaticamente)
* Data início
* Data fim
* Motivo (radio button obrigatório):
  * Limpeza
  * Manutenção
* Campo descrição (obrigatório)

Botões:

* Cancelar
* Confirmar Bloqueio

Validações obrigatórias:

* Não permitir sobreposição com reservas
* Não permitir sobreposição com bloqueios
* Motivo obrigatório
* Descrição obrigatória

Após confirmação:

* Atualizar grid imediatamente
* Mostrar toast: "Bloqueio criado com sucesso"


---

# FLUXO 3 — NOVO BLOQUEIO VIA BOTÃO FLUTUANTE

Ao clicar em "Novo Bloqueio":


1. Selecionar imóvel (dropdown)
2. Selecionar datas no calendário
3. Selecionar motivo
4. Inserir descrição
5. Confirmar

Aplicar mesmas validações do fluxo anterior.


---

# FILTROS (ÍCONE NO HEADER)

Abrir modal lateral com filtros:

* Imóvel
* Status:
  * Reservado
  * Livre
  * Bloqueado
* Origem da reserva

Botão:

* Aplicar filtros


---

# ESTADOS DO SISTEMA

Estado carregando:

* Exibir skeleton nas linhas e células

Estado erro:

* Mensagem: "Erro ao carregar calendário"
* Botão "Tentar novamente"

Estado vazio:

* Caso imóvel não tenha reservas no mês, exibir todas células como livres


---

# REGRAS DE NEGÓCIO

Reservas devem exibir:

* Check-in
* Check-out
* Total de noites
* Dados do hóspede
* Valor da reserva
* Valor da taxa de limpeza
* Origem da reserva

Bloqueios:

* Só podem ser criados em datas livres
* Não podem sobrepor reservas
* Não podem sobrepor bloqueios
* Motivo obrigatório
* Descrição obrigatória
* Registrar usuário criador e timestamp


---

# REQUISITOS DE PERFORMANCE

* Suportar 30 imóveis sem travamento
* Scroll vertical e horizontal fluido
* Virtualização da lista
* Atualização otimista após criação de bloqueio


---

# DIFERENCIAL VISUAL

* Uso claro de cores para status
* Interface minimalista
* Interações rápidas com bottom sheets
* Experiência focada em tomada de decisão operacional rápida