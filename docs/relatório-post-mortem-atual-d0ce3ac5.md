<!-- title: Relatório Post-Mortem (Atual) | url: https://outline.seazone.com.br/doc/relatorio-post-mortem-atual-7S2NPNmc46 | area: Tecnologia -->

# Relatório Post-Mortem (Atual)

Created by: Bernardo Ribeiro Created time: December 18, 2023 8:38 PM

## Resumo do Incidente

*Escreva um resumo do incidente em algumas frases. Inclua o que aconteceu, por que, a gravidade do incidente e quanto tempo o impacto durou.*

### **MODELO:**

Entre **{hora inicial e final do incidente, por exemplo, 15h45 e 16h35}** do dia **{DATA}**, **{NÚMERO}** usuários encontraram **{SINTOMAS DO EVENTO}**.

O evento foi desencadeado por uma {ALTERAÇÃO} às {HORÁRIO DA ALTERAÇÃO que CAUSOU O EVENTO}.

A {ALTERAÇÃO} continha {DESCRIÇÃO OU MOTIVO PARA A ALTERAÇÃO, como uma mudança de código para atualizar um sistema}.

Um bug neste código causou {DESCRIÇÃO DO PROBLEMA}.

O evento foi detectado pelo {SISTEMA DE MONITORAMENTO}. A equipe começou a trabalhar no evento às {AÇÕES DE RESOLUÇÃO TOMADAS}.

Este incidente de {NÍVEL DE GRAVIDADE} afetou {X%} dos usuários.

Houve impacto adicional, conforme observado por {por exemplo, NÚMERO DE CHAMADOS DE SUPORTE ENVIADOS, MENÇÕES NAS MÍDIAS SOCIAIS, CHAMADAS PARA GERENTES DE CONTA} relacionados a este incidente.

## O que levou ao incidente

*Descreva a sequência de eventos que levou ao incidente, por exemplo, mudanças anteriores que introduziram bugs que ainda não haviam sido detectados.*

### **MODELO:**

Às {16:00} do dia {MM/DD/AA}, ({QUANTIDADE DE TEMPO ANTES DO IMPACTO NO CLIENTE, por exemplo, 10 dias antes do incidente em questão}), uma alteração foi introduzida no {PRODUTO OU SERVIÇO} para {AS ALTERAÇÕES QUE LEVARAM AO INCIDENTE}.

Essa mudança resultou em {DESCRIÇÃO DO IMPACTO DA ALTERAÇÃO}.

## O que não funcionou como esperado

*Descreva como a alteração implementada não funcionou como esperado. Se disponível, inclua capturas de tela de visualizações de dados relevantes que ilustrem a falha.*

### **EXEMPLO:**

{NÚMERO} respostas foram enviadas incorretamente para {XX%} das solicitações. Isso durou {PERÍODO DE TEMPO}.

## Impacto

Descreva como o incidente afetou os usuários internos e externos durante o incidente. Inclua quantos casos de suporte foram abertos.

### **EXEMPLO:**

Por {XX horas XX minutos} entre {XX:XX UTC e XX:XX UTC} do dia {MM/DD/AA}, {RESUMO DO INCIDENTE} nossos usuários enfrentaram este incidente.

Este incidente afetou {XX} clientes (X% DOS USUÁRIOS DO {SISTEMA OU SERVIÇO}), que experimentaram {DESCRIÇÃO DOS SINTOMAS}.

Foram enviados {XX NÚMERO DE CHAMADOS DE SUPORTE E XX NÚMERO DE POSTS EM MÍDIAS SOCIAIS}.

## Detecção do incidente

Quando a equipe detectou o incidente? Como eles souberam que estava acontecendo? Como podemos melhorar o tempo de detecção? Considere: Como poderíamos ter reduzido esse tempo pela metade?

### **EXEMPLO:**

Este incidente foi detectado quando o {TIPO DE ALERTA} foi acionado e {EQUIPE/PESSOA} foi acionado.

Em seguida, {PESSOA SECUNDÁRIA} foi acionada, porque {PESSOA PRIMÁRIA} não era responsável pelo serviço gravando no disco, atrasando a resposta em {XX MINUTOS/HORAS}.

{DESCREVA A MELHORIA} será implementada por {RESPONSÁVEL DA EQUIPE DA MELHORIA} para que {MELHORIA ESPERADA}.

## Causa raiz

Registre a causa raiz final do incidente, a coisa identificada que precisa mudar para evitar que esse tipo de incidente aconteça novamente.

### **EXEMPLO:**

Um bug no manuseio do pool de conexões levou a conexões vazadas em condições de falha, combinado com a falta de visibilidade no estado da conexão.

## Resposta ao incidente

Quem respondeu ao incidente? Quando eles responderam e o que fizeram? Note qualquer atraso ou obstáculo na resposta.

### **EXEMPLO:**

Após receber um alerta às {XX:XX UTC}, {ENGENHEIRO DE PLANTÃO} entrou online às {XX:XX UTC} no {SISTEMA ONDE AS INFORMAÇÕES DO INCIDENTE SÃO CAPTURADAS}.

Esse engenheiro não tinha experiência no {SISTEMA AFETADO}, então um segundo alerta foi enviado às {XX:XX UTC} para {ENGENHEIRO DE PLANTÃO DE ESCALAÇÃO} que entrou na sala às {XX:XX UTC}.

## Como o incidente foi resolvido

*Descreva como o serviço foi restaurado e o incidente foi considerado encerrado. Detalhe como o serviço foi restaurado com sucesso e como você soube quais passos tomar para a recuperação.*

*Dependendo do cenário, considere estas perguntas: Como você poderia melhorar o tempo para mitigação? Como você poderia ter reduzido esse tempo pela metade?*

### **EXEMPLO:**

Utilizamos uma abordagem de três etapas para a recuperação do sistema:

{DESCRIÇÃO DA AÇÃO QUE MITIGOU O PROBLEMA, POR QUE FOI TOMADA E O RESULTADO}

Exemplo: Aumentando o tamanho do grupo de instâncias EC3 da BuildEng para aumentar o número de nós disponíveis para suportar a carga de trabalho e reduzir a probabilidade de agendamento em nós superalocados.

* Desabilitado o escalonador automático do Escalator para evitar que o cluster dimensionasse agressivamente para baixo
* Revertendo o escalonador de engenharia de compilação para a versão anterior.

## Cronograma

Detalhe o cronograma do incidente. Recomendamos o uso de UTC para padronizar os fusos horários.

Inclua quaisquer eventos relevantes anteriores, início de atividades, o primeiro impacto conhecido e escalonamentos. Registre quaisquer decisões ou alterações feitas e quando o incidente terminou, j

**MODELO:**

XX:XX UTC - ATIVIDADE DO INCIDENTE; AÇÃO TOMADA

XX:XX UTC - ATIVIDADE DO INCIDENTE; AÇÃO TOMADA

XX:XX UTC - ATIVIDADE DO INCIDENTE; AÇÃO TOMADA

## Backlog Check

Revise seu backlog de engenharia para descobrir se havia algum trabalho não planejado que poderia ter evitado este incidente, ou pelo menos reduzido seu impacto?

Uma avaliação objetiva do backlog pode esclarecer decisões passadas sobre prioridade e risco.

### **EXEMPLO:**

Não há itens específicos no backlog que poderiam ter melhorado este serviço. Há uma observação sobre melhorias no tipo de fluxo, e essas eram tarefas contínuas com fluxos de trabalho estabelecidos.

Foram abertos chamados para melhorar os testes de integração, mas até agora não foram bem-sucedidos.

## Recorrência (incidentes semelhantes)

Agora que você conhece a causa raiz, é possível revisar e identificar outros incidentes que poderiam ter a mesma causa raiz? Se sim, note qual mitigação foi tentada nesses incidentes e pergunte por que esse incidente ocorreu novamente.

### **EXEMPLO:**

A mesma causa raiz resultou nos incidentes HOT-13432, HOT-14932 e HOT-19452.

## Lições aprendidas

Discuta o que correu bem na resposta ao incidente, o que poderia ter sido melhorado e onde existem oportunidades de melhoria.

### **EXEMPLO:**

* Necessidade de um teste de unidade para verificar se o limitador de taxa para o trabalho foi mantido corretamente
* Cargas de trabalho de operações em massa, atípicas da operação normal, devem ser revisadas
* As operações em massa devem começar lentamente e ser monitoradas, aumentando quando as métricas do serviço parecerem nominais

## Ações para mitigar esse tipo de incidente

*Descreva a ação corretiva ordenada para evitar esse tipo de incidente no futuro. Note quem é responsável e quando eles devem concluir o trabalho e onde esse trabalho está sendo rastreado.*

**EXEMPLO:**


1. Limite de taxa de dimensionamento automático manual temporário implementado para limitar falhas
2. Teste de unidade e reintrodução do limite de taxa de trabalho
3. Introdução de um mecanismo secundário para coletar informações de taxa distribuída em todo o cluster para orientar os efeitos de dimensionamento


---

**Artigo Gerado:**