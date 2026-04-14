<!-- title: Definição de processos e templates para entrega | url: https://outline.seazone.com.br/doc/definicao-de-processos-e-templates-para-entrega-SkmUkdCpNb | area: Tecnologia -->

# Definição de processos e templates para entrega

# Fase A: Tudo começa com o Discovery

## 1. O que é o Discovery? (Conceito Geral)

O **Product Discovery** é a fase de investigação que ocorre antes de qualquer linha de código ser escrita ou qualquer automação ser configurada.

Seu objetivo principal é reduzir incertezas, em vez de construirmos o que o solicitante *pede*, nós investigamos o que ele realmente *precisa*. É o momento de validar se o problema é real, se a solução proposta é viável tecnicamente e se ela trará valor para a empresa (ROI).

**Os 4 Pilares do Discovery:**


1. **Valor:** O cliente vai querer usar/comprar isso?
2. **Usabilidade:** O usuário conseguirá entender como usar?
3. **Viabilidade:** Temos tecnologia e dados para construir isso?
4. **Viabilidade de Negócio:** Essa solução respeita as regras e o orçamento da empresa?

## 2. O Discovery no Contexto de Automação

Diferente de produtos de software tradicionais, onde o foco é a interface com o usuário, o Discovery para Automação foca na eficiência operacional e na integridade do fluxo de dados.

Na nossa área, o Discovery serve para garantir que não estamos "automatizando o caos". Se um processo manual é confuso e cheio de erros, automatizá-lo apenas fará com que os erros aconteçam mais rápido. Nosso papel como PM é organizar o processo antes de entregá-lo ao time de desenvolvimento.

## 3. Fluxo de Discovery para Automação (Passo a Passo)

Para que uma demanda saia do backlog e vá para o desenvolvimento, ela deve passar pelas seguintes etapas de Discovery:

### **Etapa 1: Imersão no Processo Atual** 

* **Entrevista com o Especialista:** Sentar com quem faz a tarefa hoje.
* **Mapeamento de Cliques:** Entender exatamente onde o dado nasce, por onde passa e onde ele morre.
* **Identificação de Gargalos:** Onde o humano mais erra? Onde o processo trava?

### **Etapa 2: Análise de Dados e Inputs**

* **Origem do Gatilho:** O que inicia a automação? (Um formulário, um e-mail, um horário fixo?)
* **Qualidade do Dado:** O dado que recebemos é estruturado (planilha) ou não estruturado (texto solto no corpo do e-mail)? 

### **Etapa 3: Desenho da Solução Proposta (To-Be)**

* **Desenho do Fluxo:** Criar um fluxograma simples mostrando: "O robô lê aqui -> decide ali -> escreve lá".
* **Definição de Exceções:** O que o robô deve fazer se o sistema estiver fora do ar ou se o dado vier errado? (Isso evita que o dev tenha que parar o trabalho para te perguntar depois).

## 4. Template de Documentação de Discovery (Modelo para preencher):

## \[Template\] Documento de Product Discovery: Automação

**Nota:** Utilize este modelo para documentar cada nova demanda priorizada. Lembre-se que esta documentação é **viva**; este template serve como um guia flexível. Preencha o que fizer sentido e adicione novos campos sempre que o processo exigir detalhes específicos para garantir o sucesso da entrega.

**Autor:** \[Seu Nome\] **Stakeholders:** \[Área Solicitante - Ex: Financeiro / Comercial\] **Data:** \[00/00/0000\]


---

### 1. Resumo

*Breve descrição (2 a 3 linhas) sobre o que se trata o projeto para situar qualquer pessoa que abra o documento.*

### 2. O Problema

* **Contexto:** Descrição do cenário atual.
* **Dores do Time:** O que acontece de errado hoje? (Ex: "O time perde 10h semanais em digitação manual").
* **Impacto no Negócio:** Qual o risco de não automatizar? (Ex: "Risco de multas por erro no preenchimento de impostos").

### 3. Objetivos e Informações Técnicas

* **Sistemas Envolvidos:** \[Lista de softwares, APIs, Planilhas, Bancos de Dados\].
* **Volume/Frequência:** \[Ex: 100 execuções/dia ou 1x por mês\].
* **Objetivo Principal:** O que é o sucesso absoluto? (Ex: "Eliminar 100% da digitação manual no sistema X").
* **Objetivos Secundários:** (Ex: "Gerar um log de erros que não existe hoje").

### 4. Escopo (Como conceituar)

*O escopo serve para proteger o seu tempo e o do desenvolvedor. Ele define os limites.*

* **Dentro do Escopo:** É tudo o que o robô **DEVE** fazer.
  * *Exemplo:* Ler o e-mail, baixar o PDF, extrair o valor total e salvar no Google Sheets.
* **Fora do Escopo:** É o que o robô **NÃO** vai fazer (geralmente coisas que o solicitante pediu, mas que não serão feitas agora para não atrasar a entrega).
  * *Exemplo:* O robô não vai enviar e-mail de confirmação para o cliente final nesta fase; o robô não vai tratar arquivos que cheguem em formato de imagem (JPG).

### 5. Proposta de Solução (Visão Geral)

* **Gatilho (Trigger):** O que faz a automação começar?
* **Fluxo Lógico:** Descrição simples do "Caminho Feliz" (o caminho sem erros).

### 6. Detalhamento de Regras e Fases

*Sobre o que você perguntou de "Bloqueio e Quarentena": em automação, isso é fundamental e chamamos de **Tratamento de Exceções**.*

* **Fase 1 (MVP - Mínimo Viável):** Focar no fluxo principal que atende 80% dos casos.
* **Regras de Bloqueio/Exceção:**
  * **O que bloqueia?** (Ex: Se o CNPJ no arquivo for inválido, a automação para e avisa o humano).
  * **Quarentena:** (Ex: Se o sistema de destino estiver fora do ar, a automação aguarda 30 min e tenta de novo)

# Processo: Do Discovery ao Jira

* **Finalização do Discovery:** Assim que o documento de Discovery for validado pelo stakeholder, ele vira a "fonte da verdade". Nenhuma alteração de escopo deve ser aceita sem atualizar este documento.
* **Criação do Card:** No Jira, dentro do **Épico** correspondente à automação, organize as informações utilizando o template de descrição abaixo.
* **Anexo de Contexto:** É obrigatório anexar o link do documento completo de Discovery e, se possível, o fluxograma do processo.
* **Kick-off (Refinamento):** Apresente o card ao desenvolvedor/líder técnico. O card só deve ser movido para "To Do" ou "In Progress" após o time técnico confirmar que entendeu os requisitos e que a solução é viável.

## Template de Card no Jira (História de Usuário)

### **Título do Ticket**

`[Automação] <Nome da Área> - <Ação do Robô>`

### **Descrição**

### **2. Contexto (O Problema)**

* **O que acontece hoje:** \[Descreva o processo manual ou a falha do fluxo atual\]
* **Dor Principal:** \[Qual o maior prejuízo atual? Ex: Perda de leads, erro de digitação, processo não escalável\]
* **Resultado Negativo:** \[O que acontece se não resolvermos? Ex: Reuniões não confirmadas a tempo\]


---

### **3. Objetivo e Solução (O que deve ser feito)**

* **Objetivo Geral:** \[Frase resumida do que a automação deve entregar\]
* **Detalhamento da Solução:** \[Passo a passo do que foi pedido pelo stakeholder\]
* **Resultado Esperado:** \[Como o processo deve estar funcionando ao final da entrega\]


---

### **4. Regras de Negócio e Parâmetros Técnicos**

* **Gatilho (Trigger):** \[O que inicia o robô? Ex: Webhook, Cron 2h antes, Evento no Pipedrive\]
* **Variáveis/Endpoints:** \[Ex: Endpoint `send-notification`, ID do Deal, Tipos de Atividade\]
* **Condicionais (Templates/Segmentos):** \[Regras de "Se X então Y". Ex: Se Segmento A usar Template 1; Se Segmento B usar Template 2\]


---

### **6. Documentação e Apoio**

* **Link do Discovery (Fonte da Verdade)**
* **Massa de Dados/Exemplos**

# Fase B: Passagem para Execução e Gestão

## 1. Consolidação e Passagem para o Time (Ready for Dev)

Após o Discovery estar documentado e o Card no Jira devidamente preenchido, o processo entra na fase de **Consolidação**. O objetivo é garantir que o time técnico receba a demanda sem dúvidas e com todos os acessos necessários.

#### **Etapa 1.1: Sinalização de Prontidão**

* **Ação:** O PM altera o status do card para **"Ready for Dev"**.
* **Comunicação:** Informe no canal de comunicação da equipe (Slack/Teams) ou na reunião de Daily/Planning que a demanda já passou pelo Discovery e está pronta para ser executada.

#### **Etapa 1.2: O Momento do "Handover" (Kick-off)**

Antes do desenvolvedor iniciar o código, ocorre uma breve conversa de alinhamento:

* **Apresentação do PM:** Você apresenta o contexto (o problema atual e a dor principal do cliente).
* **Validação Técnica:** O desenvolvedor ou Líder Técnico confirma se os acessos aos sistemas (APIs, Tokens, Bancos de Dados) e os Endpoints já estão disponíveis ou se precisam ser solicitados.
* **Atribuição:** O card é oficialmente atribuído ao desenvolvedor responsável.

#### **Etapa 1.3: Quebra em Atividades Técnicas (Sub-tasks)**

Uma vez que o desenvolvedor entendeu o desafio, o card (ou o Épico) deve ser populado com as atividades específicas. Isso permite que o PM acompanhe o progresso sem precisar interromper o desenvolvedor constantemente.

* **Quem faz:** O desenvolvedor ou o líder técnico, com o apoio do PM para garantir que nenhuma regra de negócio foi esquecida.
* **Exemplos de atividades no Jira:**
  * \[ \] Desenvolvimento do Fluxo Principal (ex: workflow no n8n).
  * \[ \] Implementação de Regras de Filtro e Condicionais.
  * \[ \] Configuração de Logs e Tratamento de Erros.
  * \[ \] Testes em Ambiente de Homologação.


---

### 2. Gestão e Acompanhamento (O papel do PM na Execução)

Com as atividades listadas e o status em **"In Progress"**, a demanda sai das mãos do PM como "idealizador" e ele passa a atuar como **Facilitador**.

#### **Etapa 2.1: O papel do PM nesta fase:**


1. **Remoção de Impedimentos:** Se o desenvolvedor sinalizar que uma API está bloqueada ou falta um dado, o PM atua junto às outras áreas para liberar o caminho.
2. **Gestão de Expectativas:** Caso o desenvolvedor perceba que a complexidade é maior que o previsto, o PM comunica o solicitante (stakeholder) sobre possíveis ajustes de prazo.
3. **Acompanhamento Visual:** O PM monitora a conclusão das Sub-tasks no Jira. Se o prazo está próximo e as atividades técnicas não avançam, é o momento de realizar um check-in com o desenvolvedor para entender o motivo.

# Fase C: Validação e Entrega (Homologação)

Nesta fase, o foco sai do "desenvolver" e entra no "garantir qualidade e entregar valor".

## 1. O "Kit de Entrega"**(Documentação como Atividade)**

*Antes de abrir a Pré-Homologação, o desenvolvedor deve concluir a documentação como parte integrante da solução. O card*  do Jira *só avança se estes itens estiverem anexados:*


1. **Link da Documentação Técnica**.
2. **Link da** Documentação do Usuário (entregue ao cliente).
3. **Vídeo Demonstrativo** (mostrando o fluxo operando).

## **1.1. Documentação Técnica** 

### Template de Documentação Técnica (Foco: Equipe de Automação)

*Este documento deve ser técnico e direto. O objetivo é permitir que um desenvolvedor que nunca viu o projeto consiga dar manutenção ou corrigir um bug.*

Foco: Manutenção, Arquitetura e Continuidade.

### 1. Visão Geral e Contexto Técnico

* **Resumo Executivo:** O que este fluxo resolve? *(Descreva de forma simples para que um gestor entenda o valor do projeto).*
* **Regra de Ouro (Premissa):** Qual o comportamento que **não** pode mudar? *(Ex: "Nunca enviar mensagem após as 20h" ou "Obrigatório ter ID do Pipedrive para prosseguir").*
* ### **Stack Técnica (Arquitetura)**

  > **💡 *Instrução****: Liste as ferramentas essenciais. Isso define quais acessos/chaves um novo dev precisará para dar manutenção.*
  * **Orquestrador:** (Ex: n8n, Google Apps Script) — *Onde a lógica "mora" e é executada.*
  * **Serviços de Mensageria:** (Ex: MIA Gateway, SendGrid, Twilio) — *Canais de saída para o cliente.*
  * **Sistemas de Destino/Origem:** (Ex: Pipedrive API, Decolar Extranet, RD Station) — *Sistemas que fornecem ou recebem os dados brutos.*

### 2. Arquitetura e Fluxo de Dados

#### 2.1. Diagrama Macro (Fluxograma)**Diagrama Macro (Fluxograma)**

> **💡 Instrução:** Insira a imagem ou link do desenho visual. Use caixas para sistemas (Pipedrive, MIA) e setas para o sentido dos dados. *Ferramentas Sugeridas: Miro, Mermaid ou Lucidchart.* 

#### **2.2. Gatilho Real (Trigger)**

> **💡 Instrução:** Detalhe o evento exato que "acorda" a automação. Não diga apenas "Pipedrive", diga "Webhook disparado quando o Deal entra na Etapa X".

* **Sistema de Origem:** (Ex: Pipedrive, Meta Ads, Google Forms)
* **Tipo de Gatilho:** (Ex: Webhook, etc…)

### 3. Lógica de Processamento (Passo a Passo)

**Orquestração (Decisões):**

* *Descreva os critérios de 'continua' ou 'para'.*
* **Ex:** "Valida se o negócio está na etapa X e se o campo 'Responsável' está preenchido."

**Gestão de Lock / Concorrência:**

* *Como evitamos disparos duplicados para o mesmo registro?*
* **Ex:** "Uso de tabela no Supabase para registrar o ID do Deal por 24h."

**Detalhamento das Ações:**

Aqui detalhamos as etapas de execução. Se o fluxo for muito grande,  não deve descrever cada nó, mas sim os "blocos de ação"

### 4. Tratamento de Exceções e Erros (Crítico)

**O que é:** É aqui para explicar o "Plano B". Automação boa é aquela que sabe o que fazer quando a internet cai ou o sistema de destino está fora do ar.

#### **4.1. Cenários de Falha e Consequências**

> **💡 Instrução:** Crie uma relação de "Se \[isso\] acontecer, o sistema deve \[fazer aquilo\]".

* **Exemplo:** "Se a API da MIA retornar erro 429 (Rate Limit), o n8n deve aguardar 1 minuto e tentar novamente 3 vezes."
* **Exemplo:** "Se o telefone estiver inválido, o fluxo deve criar uma nota no Pipedrive marcando como 'Erro de Envio' e alertar o comercial."

#### **4.2. Fluxo de Recuperação (Manual ou Automático)**

> **💡 Instrução:** Se o fluxo travar, como um humano ou o próprio sistema resolve?

### 5. Referências Técnicas e Ativos

* **Links Diretos:**
  * Workflow no n8n
  * Card no Jira
  * **Exemplo de Payload (JSON):** 
  * > **💡 Instrução:** *Cole aqui um exemplo do JSON que o gatilho recebe para facilitar testes futuros.*

## 1.2.  Documentação do Usuário

### Template de Documentação do Usuário (Foco: cliente/solicitante)

*Para automações "invisíveis", o manual deve focar em como o cliente interage com os sistemas que ele já conhece.*

*Foco: Operação, Regras de Negócio e Suporte. (Sem termos técnicos complexos).*

### 1. Objetivo da Automação

* > **💡 Instrução: **Descreva o propósito da automação sem termos técnicos.
* **O que ela faz por você:** \[Descreva  o benefício principal. Ex: "Elimina a necessidade de envio manual de lembretes, reduzindo o esquecimento de reuniões"\]

### 2. Como Operar (O que o usuário faz)

> ⚠️ **Nota:** Esta seção é **opcional**. Preencha apenas se a automação exigir uma ação manual (ex: clicar em um botão ou mover um card) para começar ou parar.

#### **2.1. Como Ativar (Gatilho)** — *Se aplicável*

* **Ação do Usuário:** (Ex: "Mover o card para a etapa 'No-Show'").
* *Se for 100% automática, escrever: "Nenhuma ação necessária; o sistema identifica o evento sozinho".*

#### **2.2. Como Interromper (Condições de Parada)** — *Se aplicável*

* **Ação para Parar:** (Ex: "Mover o card para a etapa 'Perdido' para o robô parar de enviar mensagens").

#### **2.3. Regras de Segurança (O que NÃO fazer)**

> 💡 **Instrução:** Mesmo em automações automáticas, liste o que o usuário faz que pode "quebrar" o robô.

* **Proibido:** (Ex: "Não alterar o ID do imóvel no campo X", "Não deletar a etiqueta 'MIA_SENT'").

### 3. Entregas e Visibilidade (Como saber se funcionou)

#### **3.1. Onde acompanhar (Rastro do Robô)**

> 💡 **Instrução:** Indique o local exato onde o robô registra a atividade.

* **Local do Registro:** (Ex: "Aba X do Pipedrive").
* **O que é registrado:** (Ex: "O robô escreve o horário do envio e anexa o link da conversa no MIA").

#### **3.2. Indicadores Visuais (Status)**

> 💡 **Instrução:** Descreva mudanças de cores, etiquetas ou campos que sinalizam que o processo está em andamento ou foi concluído.

* **Etiquetas/Labels:** (Ex: "A etiqueta mudará de 'Aguardando' para 'Recuperação Enviada'").
* **Atividades:** (Ex: "Uma tarefa do tipo 'Mensagem' será criada e marcada como feita automaticamente").

#### **3.3. 📸 Evidências no Sistema (Prints)**

> 💡 **Instrução:** Insira prints de tela reais. Isso ajuda o usuário a "bater o olho" e identificar o padrão.

### Resolução de Problemas (Autoajuda)

#### **4.1. Check-list de Diagnóstico ("Por que o robô não rodou?")**

> 💡 **Instrução:** Liste os 3 ou 4 erros humanos mais comuns que impedem a automação de funcionar.

* **Telefone Inválido:** Verifique se o número possui DDD e se não há letras no campo.
* **Etapa Incorreta:** O robô só lê negócios que estão na etapa \[X\]. Se moveu para a etapa \[Y\], ele ignorará.
* **Proprietário do Negócio:** Verifique se o card está atribuído a um usuário ativo (usuários desativados bloqueiam o fluxo).
* **Campos Obrigatórios:** Garanta que o campo \[Nome do Campo\] esteja preenchido.

#### **4.2. O que fazer em caso de erro crítico?**

> 💡 **Instrução:** Diga ao usuário como ele deve reportar um erro que ele não conseguiu resolver sozinho.

* **Procedimento:** (Ex: "Tire um print do erro e envie no canal #suporte-ti com o ID do negócio").

#### **4.3. Vídeo Demonstrativo (O "Caminho Feliz")**

> 💡 **Instrução:** Insira o link de um vídeo curto (Loom/Tear) mostrando a automação funcionando perfeitamente do início ao fim.

## 1.3.  Vídeo Demonstrativo (O Guia Visual)

> **Objetivo:** Provar o funcionamento (Caminho Feliz) e servir de treinamento rápido para novos usuários/devs.

#### Diretrizes para Gravação

* **Duração:** 2 a 5 minutos (seja direto).
* **Ferramenta Sugerida:** **Google Meet** (Grave uma reunião sozinho), Loom, Clip (ClickUp) ou OBS.
* **Áudio:** Obrigatório (explique o que está acontecendo).

#### Roteiro Obrigatório (O "Passo a Passo" da Gravação)


1. **O Gatilho (O Início):** Mostre o estado inicial do sistema (ex: Deal sem etiquetas no Pipedrive) e execute a ação que "acorda" o robô (ex: mover o card).
2. **A Espera (O que acontece):** "Nesse momento, o robô já identificou a mudança e está processando os dados." (Você pode usar um corte no vídeo se a automação demorar alguns segundos).
3. **O Resultado (Entrega):** "Pronto! Veja que a nota já apareceu aqui com o link e o cliente já recebeu a mensagem no WhatsApp."


---

## 2. Pré-Homologação (Filtro Interno)

*O objetivo aqui é verificar se a solução foi desenvolvida corretamente seguindo as regras definidas e testar a solução evitando falhas básicas no momento da entrega com o cliente.*

* **Participantes:** PM, Líder Técnico e Desenvolvedor.
* **Dinâmica:** O desenvolvedor faz uma demonstração ao vivo (Live Demo) do fluxo ponta a ponta.
* **Checklist de Critérios de Aceite (DoD):**
  * \[ \] O robô executa o "Caminho Feliz" sem erros?
  * \[ \] O tratamento de exceções funciona? (Ex: Se faltar um dado, o robô avisa ou trava?)
  * \[ \] Os logs estão a ser gerados corretamente?
* **Aprovação Técnica:** O Líder Técnico dá o "OK" de que o código segue os padrões da empresa e está pronto para ser mostrado ao cliente.


---

## 3. Homologação com o Cliente (Validação de Valor)

*Este é o momento de mostrar a solução. O foco não é o código, mas sim como o problema do cliente foi resolvido.*

* **Participantes:** PM, Desenvolvedor, Líder Técnico e Stakeholder (Cliente).
* **Roteiro da Reunião:**

  
  1. **Relembrar o Problema:** "Antes vocês perdiam 4h nisto, hoje vamos mostrar como será automático."
  2. **Demonstração Prática:** Mostrar a automação a funcionar em tempo real (ou um vídeo da execução).
  3. **Validação de Dados:** O cliente confirma se os dados de saída (e-mail, planilha, etc..) estão corretos.
  4. **Assinatura de Entrega:** O cliente dá o aceite formal na call.

     \

# Processo de Entrega (Slack Delivery)

O objetivo é que cada entrega no canal `#platform-automation-delivery` siga um padrão visual que facilite a leitura do cliente e garanta que ele tenha todos os recursos necessários à mão.

## 📝 Estrutura da Mensagem de Entrega

## **\[📦 ENTREGA DE PROJETO\] - Nome da Automação**

> **Status:** ✅ Concluído e Homologado **Impacto:** \[Breve frase sobre o benefício, ex: "Redução de 30% no tempo de resposta"\]
>
> 
---
>
> 💬 **Mensagem de Boas-vindas:** "Olá \[Nome do Cliente/Área\], sua automação já está ativa! A partir de agora, o processo \[Nome do Processo\] será realizado automaticamente pela nossa automação"
>
> 🎥 **Guia Rápido (Vídeo):** \[Link do Vídeo Demonstrativo\] *Assista para ver o robô funcionando na prática.*
>
> 📖 **Manual do Usuário:** \[Link do Documento do Usuário\] 
>
> 🛠️ **Suporte:** "Em caso de dúvidas ou comportamentos inesperados, responda a esta thread."

### 1. Uso de Threads para cada Automação

* **A Regra:** Toda e qualquer conversa sobre aquela entrega **deve** acontecer dentro da thread da mensagem original.
* **Por que?** Isso evita que o canal principal vire uma bagunça de mensagens picadas e permite que o histórico de suporte daquela automação específica fique centralizado.

### 2. Padronização de Emojis para Status

Utilize emojis no início do título para indicar o tipo de entrega:

* 📦 **\[ENTREGA\]:** Novo projeto finalizado.
* 🆙 **\[UPDATE\]:** Melhoria em uma automação que já existia.
* 🛠️ **\[MANUTENÇÃO\]:** Aviso de correção de bug concluída.


\

\