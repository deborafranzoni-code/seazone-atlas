<!-- title: Novo fluxo de Tarefas de Check-out | url: https://outline.seazone.com.br/doc/novo-fluxo-de-tarefas-de-check-out-azdHadOFRh | area: Tecnologia -->

# Novo fluxo de Tarefas de Check-out

# PRD – Fluxo de Tarefas de Checkout

## 1. Visão Geral

Este PRD descreve a criação de um fluxo de tarefas de checkout com o objetivo de transformar o processo de saída do hóspede em etapas operacionais claras, sequenciais e facilmente concluíveis.

Cada checkout gera um conjunto de cards (tarefas) que aparecem de forma progressiva conforme a conclusão da etapa anterior, garantindo padronização, rastreabilidade e controle operacional.


---

## 2. Objetivo

Transformar o checkout em um fluxo estruturado de tarefas, facilitando:

* Execução operacional
* Acompanhamento do status do imóvel
* Comunicação com hóspedes e equipe de limpeza
* Avaliação padronizada do estado do imóvel


---

## 3. Escopo

### Incluído

* Criação de tarefas automáticas por checkout
* Lógica de exibição sequencial dos cards
* Envio de mensagens via WhatsApp
* Formulário de limpeza por reserva
* Avaliação do imóvel com classificação de problemas
* Solicitação de avaliação do hóspede

### Não incluído

* Integrações financeiras
* Gestão de manutenção corretiva detalhada
* Acesso da equipe de limpeza ao sistema Sapron


---

## 4. Estrutura do Fluxo de Tarefas

Cada checkout gera os seguintes cards, em ordem:


1. Perguntar horário de saída do hóspede
2. Planejar limpeza
3. Avaliar estado do imóvel (3 possíveis estados)
4. Solicitar avaliação do hóspede

**Regra principal:**\nUm card só aparece após a conclusão do card anterior.


---

## 5. Detalhamento das Tarefas e Regras de Negócio

### 5.1 Perguntar horário de saída do hóspede

**Quando aparece:**

* 1 dia antes da data de checkout

**Funcionalidade:**

* A franquia pode enviar mensagem diretamente para o número do hóspede.
* Após o envio, é possível registrar o horário de saída.

**Regra de conclusão:**

* Após clicar em "Finalizar", o card desaparece.
* Uma nova tarefa de *Planejar limpeza* é gerada para o dia seguinte.


---

### 5.2 Planejar limpeza

**Funcionalidades:**

* Cadastro simples do responsável pela limpeza (nome e telefone).
* Este cadastro **não** concede acesso ao Sapron.
* Possibilidade de enviar diretamente o link do formulário de limpeza via WhatsApp.

**Mensagem padrão de WhatsApp:**

> Nome, você está responsável por realizar a limpeza no imóvel ABC123.\nO imóvel estará disponível para limpeza a partir de 10h.\n*\[link da localização do imóvel\]*

**Regra importante:**

* O horário de disponibilidade da limpeza deve ser o mesmo informado na tarefa anterior (horário de saída do hóspede).


---

### 5.3 Formulário de Limpeza

**Regras gerais:**

* Cada reserva possui um link único de formulário.
* O formulário contém as seguintes perguntas:


1. Wi-Fi funcionando? (com nome da rede e senha)
2. Ar-condicionado funcionando corretamente?
3. Chuveiro com água quente funcionando?
4. Controle remoto da TV funcionando?
5. Iluminação funcionando em todos os ambientes?
6. Portas e fechaduras funcionando?
7. Enxoval completo e sem problemas?
   * Quantidade de itens deve respeitar o número de hóspedes da reserva.

**Regras de evidência:**

* Sempre que houver resposta indicando problema, o envio de evidência (foto ou vídeo) é obrigatório.
* Ao final, deve ser enviado um vídeo curto do estado geral do imóvel.


---

### 5.4 Planejar limpeza – imóvel limpo (fluxo alternativo)

**Cenário alternativo:**

* A franquia pode indicar que o imóvel já está limpo.
* Nesse caso, o formulário é preenchido diretamente dentro do Sapron, sem envio para a equipe externa.


---

### 5.5 Avaliar estado do imóvel

**Quando aparece:**

* Após a finalização da limpeza.

**Funcionalidade:**

* A franquia visualiza:
  * Respostas do formulário
  * Evidências enviadas
  * Possíveis problemas identificados

**Classificação obrigatória dos problemas:**

* Falso positivo
* Dano causado por hóspede
* Necessidade de manutenção

**Regra de negócio:**

* O veredito deve ser salvo com uma **tag** associada à reserva/imóvel.

**Estados possíveis da tarefa:**


1. Aguardando limpeza
2. Problemas encontrados
3. Tudo certo com a limpeza


---

### 5.6 Solicitar avaliação do hóspede

**Quando aparece:**

* Após a avaliação do imóvel ser concluída.

**Funcionalidade:**

* Exibe o número do hóspede.
* Permite enviar mensagem solicitando avaliação.
* Após o envio, o botão de "Encerrar card" fica disponível.

**Conclusão:**

* Ao encerrar o card, todas as ações do checkout são finalizadas.


---

## 6. Status Final do Checkout

Após a conclusão de todas as tarefas:

* O checkout passa para o status **FEITO** na tela de controle.


---

## 7. Regras de Negócio Gerais


1. Cada checkout gera um conjunto único de cards.
2. Os cards seguem uma ordem fixa.
3. Um card só aparece após a conclusão do anterior.
4. A avaliação do imóvel possui três estados possíveis.
5. Evidências são obrigatórias quando há problemas.
6. O formulário de limpeza é único por reserva.
7. O horário da limpeza depende do horário de saída do hóspede.
8. O checkout só é considerado concluído após a solicitação de avaliação do hóspede.


---

## 8. Fluxo Resumido

`Perguntar horário de saída (D-1)         `\n`↓ Planejar limpeza (D0)         `\n`↓ Formulário de limpeza         `\n`↓ Avaliar estado do imóvel         `\n`↓ Solicitar avaliação do hóspede        `\n`↓ Checkout = FEITO`