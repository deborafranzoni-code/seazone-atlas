<!-- title: Processo de On-Call | url: https://outline.seazone.com.br/doc/processo-de-on-call-KUCRnjKf0B | area: Tecnologia -->

# Processo de On-Call

# 📘 **O que é?** 

O On-Call é um processo de plantão técnico rotativo que garante que sempre exista alguém responsável por atender incidentes, dúvidas, tarefas operacionais e demandas urgentes fora do fluxo normal de desenvolvimento (sprint semanal).

O termo "On-Call" significa literalmente "de prontidão" — ou seja, um desenvolvedor é designado para estar disponível e preparado para responder rapidamente a chamadas de suporte, alertas de sistema ou incidentes em produção durante um período pré-determinado.

# 🎯 **Objetivos do On-Call**

* Garantir **resposta rápida a incidentes** e falhas críticas.
* Evitar que **todo o time seja interrompido** por questões urgentes.
* Centralizar a comunicação e a triagem de problemas.
* Melhorar a **confiabilidade e estabilidade** dos sistemas.
* Criar **rastreabilidade** sobre o histórico de incidentes e suas soluções.

# 👥 **Papel do Dev On-Call (*DOD – Dev On Duty*)**

O Dev On-Call (ou Dev On Duty) é o responsável durante o período do plantão por:


1. Monitorar alertas, tickets no pipefy de cada time
2. Responder rapidamente a solicitações e incidentes nos canais de suporte (#suporte-hosting, #suporte-backoffice, #suporte-website).
3. Priorizar e categorizar  cada ocorrência, conforme as regras:

   
   1. P0 - Highest - 1 a 4 horas
   2. P1 - High - 1 dia
   3. P2 - Medium - 3 a 5 dias
   4. P3 - Low - 5 a 15 dias
   5. P4 - Lowest - mais de 15 dias

      As categorias já estão definidas no pipefy de cada BU
4. Registrar ações tomadas nos comentários do Pipefy e garantir que a comunicação com o solicitante seja clara.
5. Se o escopo não for da BU do On-Call, pode **"Escalar-Time" no pipefy** para enviar ao time correspondente.
6. Se o suporte precisa algum fix no código, deve aplicar a opção "Enviar ao Jira", e  confirmar com a/o PM qual a prioridade para entrar na Sprint da semana.

   \


:::info
Links de Kanban Pipefy de cada time:


SUPORTE HOSTING      -  Kanban Pipefy - <https://app.pipefy.com/pipes/305658493>


SUPORTE BACKOFFICE - Kanban Pipefy - **<https://app.pipefy.com/pipes/304437472>**


SUPORTE WEBSITE       -  Kanban Pipefy - <https://app.pipefy.com/pipes/305862008>

:::

# 🔁 **Rotação e Escala**

O processo é baseado em uma **escala semanal rotativa** entre os membros do time.\nCada dev cumpre **1 semana de plantão**, garantindo que sempre haja **cobertura contínua**.\nA rotação evita sobrecarga e distribui responsabilidades de forma equilibrada.

# 💡 **Boas Práticas**

* Mantenha **comunicação ativa** durante o plantão (status **"On-Call" no Slack**).
* Paras as tarefas operacionais use as informações nesta [documentação](https://outline.seazone.com.br/doc/suportes-operacionais-YXgySMB0dS) sobre Suportes Operacionais, se não tiver o tema, procure entender a regra e crie uma documentação sobre o novo tema.
* **Não assuma tudo sozinho** — escale quando necessário.
* Faça **handover claro** ao próximo dev ao fim do turno.


# 🧭 **Encerramento e Aprendizado Contínuo**

Ao final de cada semana de On-Call:

* O dev responsável faz uma **breve call ou resumo** dos incidentes que ficaram pendentes para o próximo dev.
* O dev realiza uma **mini-retrospectiva de plantão**, para identificar melhorias (ex: automatizações, alertas ruidosos, lacunas de monitoramento). Pode ser uma thread no canal do time com assunto `**\[ Semana NN -  On-call \]**` Para que seja avaliado pela/o PM e possa ser considerado na proxima sprint

  \