<!-- title: [Post-Mortem] Relatório de Incidente | url: https://outline.seazone.com.br/doc/post-mortem-relatorio-de-incidente-TIHrgqcT57 | area: Tecnologia -->

# [Post-Mortem] Relatório de Incidente

Created by: Bernardo Ribeiro Created time: December 15, 2023 10:22 PM

## Resumo do Incidente

*Write a summary of the incident in a few sentences. Include what happened, why, the severity of the incident and how long the impact lasted.*

### TEMPLATE\*\*:\*\*

Entre a hora {intervalo de tempo do incidente, por ex. 15h45 e 16h35} de {DATE}, {NUMBER} usuários encontraram {EVENT SYMPTOMS}.

O evento foi acionado por uma {CHANGE} às {TIME OF CHANGE that CAUSED THE EVENT}.

A {CHANGE} continha {DESCRIPTION OF OR REASON FOR THE CHANGE, such as a change in code to update a system}.

Um bug neste código causou {DESCRIPTION OF THE PROBLEM}.

O evento foi detectado por {MONITORING SYSTEM}. A equipe começou a trabalhar no evento em {RESOLUTION ACTIONS TAKEN}.

Este incidente de {SEVERITY LEVEL} afetou {X%} dos usuários.

Houve impacto adicional, conforme observado por {ex. NÚMERO DE INGRESSOS DE SUPORTE ENVIADOS, MENÇÕES NAS MÍDIAS SOCIAIS, CHAMADAS PARA GERENTES DE CONTA} foram levantados em relação a este incidente.

## O que levou ao incidente

*Describe the sequence of events that led to the incident, for example, previous changes that introduced bugs that had not yet been detected.*

### TEMPLATE\*\*:\*\*

At {16:00} on {MM/DD/YY}, ({AMOUNT OF TIME BEFORE CUSTOMER IMPACT, e.g. 10 days before the incident in question}), a change was introduced to {PRODUCT OR SERVICE}  in order to {THE CHANGES THAT LED TO THE INCIDENT}.

This change resulted in  {DESCRIPTION OF THE IMPACT OF THE CHANGE}.

## O que não funcionou como esperado

*Describe how the change that was implemented didn't work as expected. If available, attach screenshots of relevant data visualizations that illustrate the fault.*

### **EXAMPLE:**

{NUMBER} responses were sent in error to {XX%} of requests. This went on for {TIME PERIOD}.

## **Impacto**

Describe how the incident impacted internal and external users during the incident. Include how many support cases were raised.

### **EXAMPLE:**

For {XXhrs XX minutes} between {XX:XX UTC and XX:XX UTC} on {MM/DD/YY}, {SUMMARY OF INCIDENT} our users experienced this incident.

This incident affected {XX} customers (X% OF {SYSTEM OR SERVICE} USERS), who experienced {DESCRIPTION OF SYMPTOMS}.

{XX NUMBER OF SUPPORT TICKETS AND XX NUMBER OF SOCIAL MEDIA POSTS} were submitted.

## **Detecção do incidente**

When did the team detect the incident? How did they know it was happening? How could we improve time-to-detection? Consider: How would we have cut that time by half?

### **EXAMPLE:**

This incident was detected when the {ALERT TYPE} was triggered and {TEAM/PERSON} were paged.

Next, {SECONDARY PERSON} was paged, because {FIRST PERSON} didn't own the service writing to the disk, delaying the response by {XX MINUTES/HOURS}.

{DESCRIBE THE IMPROVEMENT} will be set up by {TEAM OWNER OF THE IMPROVEMENT} so that {EXPECTED IMPROVEMENT}.

## **Root cause**

Note the final root cause of the incident, the thing identified that needs to change in order to prevent this class of incident from happening again.

### **EXAMPLE:**

A bug in connection pool handling led to leaked connections under failure conditions, combined with lack of visibility into connection state.

## **Resposta ao incidente**

Who responded to the incident? When did they respond, and what did they do? Note any delays or obstacles to responding.

### **EXAMPLE:**

After receiving a page at {XX:XX UTC}, {ON-CALL ENGINEER} came online at {XX:XX UTC} in {SYSTEM WHERE INCIDENT INFO IS CAPTURED}.

This engineer did not have a background in the {AFFECTED SYSTEM} so a second alert was sent at {XX:XX UTC} to {ESCALATIONS ON-CALL ENGINEER} into the who came into the room at {XX:XX UTC}.

## Como o incidente foi resolvido

*Describe how the service was restored and the incident was deemed over. Detail how the service was successfully restored and you knew how what steps you needed to take to recovery.*

*Depending on the scenario, consider these questions: How could you improve time to mitigation? How could you have cut that time by half?*

### **EXAMPLE:**

We used a three-pronged approach to the recovery of the system:

{DESCRIBE THE ACTION THAT MITIGATED THE ISSUE, WHY IT WAS TAKEN, AND THE OUTCOME}

Example: By Increasing the size of the BuildEng EC3 ASG to increase the number of nodes available to support the workload and reduce the likelihood of scheduling on oversubscribed nodes

* Disabled the Escalator autoscaler to prevent the cluster from aggressively scaling-down
* Reverting the Build Engineering scheduler to the previous version.

## **Timeline**

Detail the incident timeline. We recommend using UTC to standardize for timezones.

Include any notable lead-up events, any starts of activity, the first known impact, and escalations. Note any decisions or changed made, and when the incident ended, along with any post-impact events of note.

**TEMPLATE:**

XX:XX UTC - INCIDENT ACTIVITY; ACTION TAKEN

XX:XX UTC - INCIDENT ACTIVITY; ACTION TAKEN

XX:XX UTC - INCIDENT ACTIVITY; ACTION TAKEN

## **Backlog check**

Review your engineering backlog to find out if there was any unplanned work there that could have prevented this incident, or at least reduced its impact?

A clear-eyed assessment of the backlog can shed light on past decisions around priority and risk.

### **EXAMPLE:**

No specific items in the backlog that could have improved this service. There is a note about improvements to flow typing, and these were ongoing tasks with workflows in place.

There have been tickets submitted for improving integration tests but so far they haven't been successful.

## **Recorrência (incidentes semelhantes)**

Now that you know the root cause, can you look back and see any other incidents that could have the same root cause? If yes, note what mitigation was attempted in those incidents and ask why this incident occurred again.

### **EXAMPLE:**

This same root cause resulted in incidents HOT-13432, HOT-14932 and HOT-19452.

## **Lições aprendidas**

Discuss what went well in the incident response, what could have been improved, and where there are opportunities for improvement.

### **EXAMPLE:**

* Need a unit test to verify the rate-limiter for work has been properly maintained
* Bulk operation workloads which are atypical of normal operation should be reviewed
* Bulk ops should start slowly and monitored, increasing when service metrics appear nominal

## Ações para mitigar esse tipo de incidente

*Describe the corrective action ordered to prevent this class of incident in the future. Note who is responsible and when they have to complete the work and where that work is being tracked.*

**EXAMPLE:**


1. Manual auto-scaling rate limit put in place temporarily to limit failures
2. Unit test and re-introduction of job rate limiting
3. Introduction of a secondary mechanism to collect distributed rate information across cluster to guide scaling effects