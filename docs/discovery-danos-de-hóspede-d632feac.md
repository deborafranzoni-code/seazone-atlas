<!-- title: Discovery - Danos de Hóspede | url: https://outline.seazone.com.br/doc/discovery-danos-de-hospede-cMGbyey8ba | area: Tecnologia -->

# Discovery - Danos de Hóspede

### 1. Visão Geral e Contexto

#### 1.1. O Problema

Atualmente, a gestão de danos causados por hóspedes é um processo ineficiente e propenso a erros. A equipe operacional utiliza duas ferramentas distintas: o Sapron para registro de status financeiros e histórico, e o Pipefy para acompanhamento visual do processo (Kanban). Essa separação resulta em:

* **Trabalho Duplicado:** A equipe precisa atualizar informações em dois sistemas diferentes.
* **Inconsistência de Dados:** Risco de os status no Sapron e no Pipefy não estarem sincronizados.
* **Troca de Contexto Constante:** O usuário precisa alternar entre telas, o que diminui a produtividade e aumenta a carga cognitiva.
* **Falta de Visibilidade Completa:** É impossível ter uma visão 360º de um caso sem consultar ambas as ferramentas.

#### 1.2. A Solução Proposta

Este projeto visa descontinuar o uso do Pipefy para este fluxo, internalizando e aprimorando a funcionalidade de um painel Kanban diretamente no Sapron. Criaremos um módulo de gestão de danos unificado que servirá como uma fonte única de verdade, combinando a clareza visual de um Kanban com a riqueza de detalhes e o registro histórico do nosso sistema.

#### 1.3. Objetivos e Métricas de Sucesso

* **Objetivo Primário:** Aumentar a eficiência operacional na resolução de casos de danos.
  * **Métrica de Sucesso:** Reduzir em 25% o tempo médio para resolução de um caso (do `Solicitado` ao `Pago`/`Cancelado`).
* **Objetivo Secundário:** Melhorar a precisão dos dados e a satisfação da equipe.
  * **Métrica de Sucesso:** Zerar as discrepâncias de status entre sistemas (pois haverá apenas um).
  * **Métrica de Sucesso:** Aumentar a pontuação de satisfação da equipe operacional (pesquisa qualitativa).

### 2. Personas e Casos de Uso

* **Persona Principal:** Maria, Analista Operacional de Danos.
* **Suas Tarefas:** Maria é responsável por receber novos casos de danos, analisar as evidências, decidir o canal de cobrança, negociar com as partes (hóspedes, seguros) e acompanhar o caso até o seu pagamento ou cancelamento.
* **Suas Frustrações Atuais:** "Perco muito tempo atualizando o card no Pipefy e depois o histórico no Sapron. Às vezes, esqueço de atualizar um deles e a informação fica errada. Gostaria de ver tudo em um só lugar."
* **Caso de Uso Principal:** "Como Maria, eu quero gerenciar todo o ciclo de vida de um dano de hóspede, desde a solicitação até a finalização, em uma única interface visual e interativa, para que eu possa trabalhar de forma mais rápida, com menos erros e ter uma visão clara do status de todos os meus casos."

### 3. Requisitos Funcionais (RF)

#### RF-01: Painel Kanban de Danos

O sistema deve apresentar um painel no estilo Kanban como a visão principal do módulo.

* **3.1. Colunas do Kanban:** O painel deve ter as seguintes colunas fixas, representando as etapas do processo:

  
  1. `Solicitado` (Novo dano)
  2. `Em Validação` (Análise de evidências)
  3. `Em Cobrança: Via Airbnb`
  4. `Em Cobrança: Hóspede`
  5. `Em Cobrança: EasyCover`
  6. `Em Cobrança: Jurídico`
  7. `Finalizados`
* **3.2. Card Resumido:** Cada caso de dano deve ser representado por um card no painel. O card deve exibir as seguintes informações mínimas:
  * ID do Dano (ex: #1023)
  * Nome da Propriedade
  * Valor Reivindicado (R$)
  * Data da Ocorrência
  * Ícone de cor indicando o "Status Detalhado" (ver RF-03).
* **3.3. Funcionalidade de Arrastar e Soltar (Drag-and-Drop):** O usuário deve ser capaz de mover os cards entre as colunas para atualizar a etapa do processo.
* **3.4. Filtros e Busca:** O painel deve incluir:
  * Uma barra de busca para encontrar casos por ID, nome do hóspede ou propriedade.
  * Filtros para refinar a visão por: `Propriedade`, `Anfitrião`, `Período da Ocorrência` e `Status Detalhado`.

#### RF-02: Visão Detalhada do Dano

Ao clicar em um card no Kanban, uma visão detalhada do caso deve ser exibida (preferencialmente em uma janela modal sobre o painel).

* **3.1. Layout:** A tela deve ser organizada de forma clara, preferencialmente em duas colunas.
* **3.2. Conteúdo da Tela:** Deve conter as seguintes seções:
  * **Informações Gerais:** Dados do hóspede, anfitrião, reserva e propriedade.
  * **Valores:** Campos para `Valor Reivindicado`, `Valor Acordado` e `Taxas`.
  * **Evidências:** Área para upload e visualização de arquivos (fotos, vídeos, orçamentos, notas fiscais).
  * **Histórico de Atividades:** Um feed de todas as ações e comentários (ver RF-04).
* **3.3. Campos de Status (Crucial):** A tela deve apresentar dois campos de status distintos:
  * `Status do Processo`: Um campo de texto **somente leitura** que exibe o nome da coluna do Kanban onde o card se encontra (ex: "Em Cobrança: Hóspede"). Este campo é atualizado automaticamente quando o card é movido.
  * `Status Detalhado`: Um campo de seleção **interativo (dropdown)** onde o usuário define a condição atual do caso. As opções são:
    * `Pendente` (Aguardando resposta externa)
    * `Em Disputa` (Caso haja contestação)
    * `A Pagar` (Aprovado, aguardando pagamento)
    * `Pago` (Finalizado com sucesso)
    * `Cancelado` (Finalizado sem sucesso)

#### RF-03: Histórico de Atividades Inteligente

A visão detalhada deve possuir um histórico que registra todas as interações do caso.

* **3.1. Registros Manuais:** O usuário deve poder adicionar comentários de texto a qualquer momento.
* **3.2. Registros Automáticos:** O sistema deve registrar automaticamente os seguintes eventos, com data, hora e nome do usuário:
  * Movimentação de card entre colunas.
  * Alteração do `Status Detalhado`.
  * Upload de um novo arquivo de evidência.
  * Alteração nos campos de `Valores`.

### 4. Fluxo de Usuário Principal


1. **Entrada:** Um dano é reportado. Um card é criado automaticamente na coluna `Solicitado`.
2. **Triagem:** A analista Maria move o card para `Em Validação`. Ela clica no card para abrir a visão detalhada.
3. **Análise:** Maria analisa as evidências e conclui que a cobrança será via Airbnb. Ela move o card para `Em Cobrança: Via Airbnb`.
4. **Acompanhamento:** O Airbnb solicita mais informações. Maria abre o card e altera o `Status Detalhado` para `Pendente`.
5. **Disputa:** O hóspede contesta o valor via Airbnb. A plataforma informa Maria. Ela atualiza o `Status Detalhado` para `Em Disputa` e adiciona um comentário manual: "Airbnb iniciou mediação."
6. **Resolução:** O Airbnb define um valor a ser pago. Maria atualiza o `Valor Acordado` e altera o `Status Detalhado` para `A Pagar`.
7. **Conclusão:** O pagamento é confirmado. Maria altera o `Status Detalhado` para `Pago` e move o card para a coluna `Finalizados`. O caso sai da sua visão de trabalho ativo.


**Oportunidades de melhoria:**


1. **Refatoração da tela de lançamento de despesas** para torná-la mais intuitiva, com campos obrigatórios e estrutura mais clara.
2. **Obrigatoriedade da inclusão de nota fiscal (NF) ou link de cotação** no momento do lançamento, garantindo comprovação da despesa.
3. **Geração automática de um código identificador para cada dano**, permitindo rastreamento e associação entre diferentes registros do sistema.
4. **Inclusão de um botão de associação de dano à despesa**, logo após o registro do dano, facilitando o vínculo direto entre o evento e o custo relacionado.