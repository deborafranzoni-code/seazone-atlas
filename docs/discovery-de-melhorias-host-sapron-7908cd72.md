<!-- title: Discovery de Melhorias HOST - Sapron | url: https://outline.seazone.com.br/doc/discovery-de-melhorias-host-sapron-W2a6HJrYt4 | area: Tecnologia -->

# Discovery de Melhorias HOST - Sapron

# Contexto

Este discovery foi realizado a partir da análise dos principais tickets abertos por hosts, além de entrevistas com 11 franqueados que compartilharam suas principais dores e insatisfações com a plataforma Sapron para hosts.

O objetivo principal é identificar pontos de melhoria que:

* Aprimorem a experiência do franqueado.
* Maximizem o resultado da operação.
* Impactem positivamente os principais KPIs da empresa.

## Refatoração da Tela de Controle

### **Problemática 1: Visualização ineficiente das tarefas por imóvel**

**Cenário atual:** 

A tela de controle lista todos os check-ins e check-outs do dia, permitindo filtros apenas por check-ins, check-outs e cards completos. O principal problema apontado é a dificuldade de visualizar todas as tarefas de um único imóvel, especialmente para hosts responsáveis por SPOTs ou prédios com grandes operações da Seazone.

**Proposta de solução:** 

Incluir filtros que permitam filtrar por **imóvel** e **cama quente**, facilitando a organização das limpezas e destacando as mais urgentes. 

 ![](/api/attachments.redirect?id=5e948831-55c7-4846-8c46-65c5c1f9338e " =349x761")

### **Problemática 2: Tempo excessivo para preencher requisitos de check-out**

**Cenário atual:** 

Franqueados relatam que o preenchimento dos requisitos para fechar um card de check-out é demorado e burocrático.

**Proposta de solução:**

Simplificar os formulários e campos obrigatórios para realizar o check-out. 

Sugestão de simplificação: 

* ==Formulário de check-out== 
* ==Dados sobre a limpeza== 
* ==Danos de hóspede== - incluir evento para verificar se esta sendo clicado 
* Unificar código de reserva e detalhe da reserva - verificar a necessidade alterar codigo de reserva para ==código da stays== 

 ![](/api/attachments.redirect?id=c49293c1-3038-49dd-956a-4f0d0b9b3e4a " =348x665")

## Refatoração do Multicalendar

### Problemática 1: Dificuldade no desbloqueio de manutenção/limpeza

**Cenário atual:** 

Hosts precisam abrir chamados com o atendimento para desbloquear imóveis após manutenção ou limpeza, pois não percebem que essa funcionalidade já existe na plataforma.

**Proposta de solução:**

Tornar o desbloqueio mais intuitivo e visível na interface do usuário. 

 ![](/api/attachments.redirect?id=9619ab2c-756f-489e-961a-110773cdedb9 " =352x765")

### Problemática 2: Falta de filtro por nome de hóspede

**Cenário atual:** 

Reservas feitas via Booking (que representam 40% das reservas da Seazone) não especificam qual imóvel dentro do SPOT/região foi reservado, dificultando a busca pela reserva apenas pelo filtro de imóvel.

**Proposta de solução:**

Adicionar filtro por nome do hóspede para facilitar a localização da reserva. 

 ![](/api/attachments.redirect?id=760c713c-639e-45bb-8846-d529ef466053 " =347x757")

### Problemática 3: Acesso irrestrito do cohost a dados financeiros sensíveis

**Cenário atual:** 

O cohost tem acesso ao Multicalendar com a mesma visualização do host principal, incluindo informações sensíveis como o valor pago na taxa de limpeza.

**Proposta de solução:**

* tirar só taxa de limpeza de cohost 

Criar um nível diferenciado de visualização para cohosts, ocultando dados financeiros sensíveis. 

 ![](/api/attachments.redirect?id=a648e850-39d0-41a6-bb3a-fb6f99a7e409 " =349x760")

## Alerta de Novas Reservas

### Problemática: Dificuldade de organização para reservas instantâneas 

**Cenário atual:** 

Hosts relatam dificuldades para preparar o imóvel quando uma reserva instantânea é recebida para o mesmo dia.

**Proposta de solução:**

Envio de mensagens automáticas via WhatsApp com detalhes da reserva e dados do hóspede para reservas de entrada no mesmo dia. Incluir na home uma listagem das últimas reservas recebidas, facilitando a visualização rápida das novas entradas. (Em discovery para validação).