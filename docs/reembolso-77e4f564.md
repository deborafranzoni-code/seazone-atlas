<!-- title: Reembolso | url: https://outline.seazone.com.br/doc/reembolso-PWVGaIPsQ7 | area: Tecnologia -->

# Reembolso

# Fluxo de Lançamento de Reembolso 

## 1. Objetivo

Estruturar o fluxo completo de **lançamento, análise e acompanhamento de reembolsos** realizados pela franquia, garantindo:

* Rastreabilidade financeira por imóvel
* Padronização de documentação obrigatória
* Controle de aprovação (incluindo proprietário quando aplicável)
* Visibilidade clara de status (em análise, pendente, aprovado, pago, etc.)
* Integração com o fluxo de formulário de limpeza


---

## 2. Contexto

O sistema é utilizado por **franquias da Seazone** para gestão operacional e financeira de imóveis de aluguel por temporada.

O reembolso representa um valor que a franquia solicita restituição referente a despesas operacionais como:

* Manutenções
* Substituição de itens
* Pequenos reparos
* Compras emergenciais

Todo reembolso impacta diretamente a gestão financeira do imóvel.


---

## 3. Regras de Negócio

### 3.1 Regras Gerais


1. **Todo reembolso deve estar obrigatoriamente vinculado a um imóvel.**
2. Todo reembolso deve possuir:
   * Data de execução
   * Valor
   * Categoria
   * Subcategoria (quando aplicável)
   * Descrição obrigatória
   * Evidências obrigatórias
3. O status inicial de todo reembolso é: **Em análise**.
4. Caso o valor seja **maior que R$300**, é obrigatório anexar:
   * Comprovante de aprovação do proprietário.


---

## 4. Estrutura do Fluxo — Lançamento Manual

### 4.1 Etapa 1 — Identificação do Imóvel

Campos obrigatórios:

* Selecionar imóvel (autocomplete ou busca)
* Data de execução do gasto
* Valor do reembolso (R$)

Validações:

* Valor deve ser numérico e maior que zero.
* Data não pode ser futura.


---

### 4.2 Etapa 2 — Classificação

Campos obrigatórios:

* Categoria (dropdown)
* Subcategoria (condicional)
* Descrição detalhada (campo aberto — obrigatório)

A descrição deve conter contexto suficiente para análise financeira.


---

### 4.3 Etapa 3 — Evidências Obrigatórias

### Documentos obrigatórios para todos os reembolsos:

* Evidência de compra\n(Nota Fiscal ou recibo)
* Evidência da manutenção realizada ou item substituído\n(foto, vídeo ou documento)

### Documento adicional obrigatório (condicional):

* Se valor > R$300\n→ Upload do comprovante de aprovação do proprietário

Regras técnicas:

* Upload múltiplo permitido.
* Arquivos permitidos: PDF, JPG, PNG.
* Sistema deve bloquear envio sem documentação obrigatória.


---

## 5. Fluxo de Status

### Status possíveis:


1. Em análise
2. Pendente
3. Pré-aprovado
4. Aprovado
5. Pago
6. Reprovado


---

## 6. Gestão de Reembolsos

### 6.1 Tela de Listagem Geral

A franquia deve conseguir visualizar:

* Todos os reembolsos
* Filtros por:
  * Imóvel
  * Período
  * Status
  * Categoria


---

### 6.2 Em Análise

* Status inicial após envio.
* Aguardando avaliação do financeiro.


---

### 6.3 Pendente

O financeiro pode alterar para **Pendente**, quando:

* Falta documentação
* Informação incompleta
* Dúvida sobre valor

Regras:

* Deve ser obrigatório informar o motivo da pendência.
* O motivo deve ser visível na tela da franquia.
* Reembolsos pendentes devem ficar agrupados em aba específica.

A franquia deve conseguir:

* Editar o lançamento
* Ajustar documentação
* Reenviar para análise

Ao reenviar:

* Status retorna para **Em análise**


---

### 6.4 Pré-aprovado

Indica que:

* Documentação validada
* Aguardando processamento financeiro


---

### 6.5 Aprovado

* Valor confirmado para pagamento.
* Não pode mais ser editado.


---

### 6.6 Pago

* Pagamento efetivado.
* Deve conter:
  * Data de pagamento
  * Referência de pagamento


---

### 6.7 Reprovado

* Reembolso negado.
* Motivo obrigatório.
* Não pode ser editado.
* Histórico deve permanecer visível.


---

## 7. Integração com Fluxo de Formulário de Limpeza

### 7.1 Lista de Possíveis Lançamentos

Origem: fluxo de preenchimento do formulário de limpeza.

Quando no formulário de limpeza for identificado:

* Item danificado
* Necessidade de substituição
* Compra emergencial

O sistema deve gerar um registro na lista de:

> "Possíveis Reembolsos"


---

### 7.2 Tela de Possíveis Reembolsos

A lista deve exibir:

* Imóvel
* Reserva associada
* Data
* Evidência anexada no formulário
* Tipo de ocorrência

A franquia deve ter opção:

> Botão: "Lançar Reembolso"


---

### 7.3 Auto Preenchimento

Ao clicar em "Lançar Reembolso":

Campos automaticamente preenchidos:

* Imóvel
* Reserva (se houver)
* Evidências já anexadas
* Data da ocorrência

Usuário apenas complementa:

* Valor
* Categoria / Subcategoria
* Descrição
* Documento de compra (NF/recibo)
* Aprovação do proprietário (se aplicável)


---

## 8. Auditoria e Histórico

Cada reembolso deve possuir:

* Linha do tempo de alterações
* Usuário responsável por cada ação
* Data e hora
* Histórico de status


---

## 9. Regras de Permissão

Franquia pode:

* Criar
* Editar (somente se Pendente)
* Reenviar para análise
* Visualizar todos os status

Financeiro pode:

* Alterar status
* Definir pendência
* Aprovar
* Reprovar
* Marcar como pago


---

## 10. Critérios de Aceite

O fluxo será considerado completo quando:

* Não for possível enviar reembolso sem documentação obrigatória.
* Reembolso > R$300 exigir obrigatoriamente aprovação do proprietário.
* Pendências exibirem motivo claramente.
* Reenvio alterar corretamente status.
* Integração com formulário de limpeza permitir auto preenchimento.
* Todos os status estiverem corretamente segregados na interface.