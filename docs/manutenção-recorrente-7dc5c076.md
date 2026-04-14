<!-- title: Manutenção recorrente | url: https://outline.seazone.com.br/doc/manutencao-recorrente-lNja2qI6Xy | area: Tecnologia -->

# Manutenção recorrente

| **PRODUCT REQUIREMENTS DOCUMENT****Módulo de Gestão de****Manutenções Recorrentes***Garantia de conformidade e rastreabilidade das manutenções realizadas pelas franquias nos imóveis administrados pela Seazone* |
|----|

\n

| **Versão** | 1.0 |
|----|----|
| **Status** | Draft — Aguardando revisão de stakeholders |
| **Área responsável** | Produto & Tecnologia |
| **Stakeholders** | Operações, Franquias, Proprietários de imóveis |
| **Data de criação** | Março 2025 |
| **Última atualização** | Março 2025 |


# **1. Visão Geral**

## **1.1 Contexto e Problema**

A Seazone administra imóveis para aluguel por temporada em nome dos proprietários. Parte das operações — como manutenção, check-in e checkout — é delegada a franquias parceiras, cada uma responsável por uma carteira de imóveis.

\n

O problema central é a ausência de um mecanismo confiável para garantir que as franquias realizem as manutenções recorrentes obrigatórias nos imóveis (limpeza de ar-condicionado, higienização de camas, higienização de sofás etc.). Sem controle sistemático, surgem riscos de:

* Manutenções não realizadas ou realizadas fora do prazo.
* Ausência de evidências documentadas das intervenções.
* Imóveis com padrão de qualidade abaixo do esperado pelo proprietário e pelo hóspede.
* Reembolsos emitidos sem lastro de execução comprovada.
* Falta de visibilidade da Seazone sobre o status real de cada imóvel.

\n

## **1.2 Objetivo da Solução**

Criar um módulo de Gestão de Manutenções Recorrentes que permita à Seazone orquestrar, monitorar e auditar todas as manutenções realizadas pelas franquias, com coleta obrigatória de evidências, fluxo de aprovação do proprietário quando necessário e integração com o processo de reembolso.

\n

## **1.3 Fora de Escopo**

* Fluxo completo de reembolso financeiro (módulo separado, integrado via evento).
* Gestão de check-in e checkout.
* Contratação ou avaliação de desempenho das franquias.
* Agendamento de reservas de hóspedes.


# **2. Atores e Papéis**

| **Ator** | **Responsabilidades no módulo** |
|----|----|
| **Seazone (Operações)** | Cadastrar manutenções recorrentes; atribuir franquia e imóvel; aprovar ou rejeitar evidências; acionar fluxo de reembolso; visualizar dashboard de conformidade. |
| **Franquia** | Receber ordens de manutenção; executar a manutenção; enviar evidências fotográficas/documentais; registrar proativamente manutenções não programadas. |
| **Proprietário do Imóvel** | Receber notificação e aprovar/rejeitar manutenções acima de R$ 300,00; consultar histórico de manutenções do seu imóvel. |
| **Sistema (Automação)** | Disparar lembretes de prazo; escalar manutenções vencidas; acionar evento de reembolso após aprovação; bloquear envio sem evidências. |


# **3. Regras de Negócio**

| **ID** | **Regra** | **Descrição** |
|----|----|----|
| **RN-01** | **Vínculo obrigatório com imóvel** | Toda manutenção (programada ou proativa) deve estar obrigatoriamente associada a um imóvel cadastrado na plataforma. Não é possível criar uma manutenção sem selecionar o imóvel. |
| **RN-02** | **Evidências obrigatórias** | A franquia só pode concluir uma manutenção após o upload de ao menos uma evidência (foto, vídeo ou documento). O sistema bloqueia a transição de status sem esse requisito. |
| **RN-03** | **Reembolso automático** | Toda manutenção aprovada dispara automaticamente um evento para o módulo de reembolso. O valor e os dados da manutenção são enviados ao fluxo financeiro sem intervenção manual. |
| **RN-04** | **Aprovação do proprietário ≥ R$ 300** | Manutenções com valor estimado acima de R$ 300,00 entram em status 'Aguardando Aprovação do Proprietário' antes de serem executadas. O proprietário tem prazo configurável (padrão: 48 h) para aprovar ou rejeitar. Sem resposta no prazo, a Seazone decide. |
| **RN-05** | **Quem emite a ordem** | Apenas a Seazone pode criar e atribuir manutenções programadas a franquias. A franquia não pode criar ordens para si mesma além das proativas. |
| **RN-06** | **Manutenção proativa da franquia** | A franquia pode registrar manutenções realizadas por iniciativa própria. Essas manutenções seguem o mesmo fluxo de evidências e aprovação, mas ficam marcadas como 'Proativa' para fins de auditoria. Reembolso só é acionado após validação da Seazone. |
| **RN-07** | **Imutabilidade de evidências** | Uma vez enviada, a evidência não pode ser excluída pela franquia. Apenas a Seazone pode remover evidências em casos de erro, com log de auditoria. |
| **RN-08** | **Histórico imutável** | Todas as mudanças de status, aprovações e rejeições são registradas com timestamp e usuário responsável, sem possibilidade de edição retroativa. |


# **4. Fluxos Principais**

## **4.1 Fluxo A — Manutenção Programada (valor ≤ R$ 300)**

| **#** | **Ator** | **Ação** |
|----|----|----|
| **1** | **Seazone** | Cria a ordem de manutenção: seleciona imóvel, tipo de manutenção, valor estimado e prazo. Atribui à franquia responsável. |
| **2** | **Sistema** | Notifica a franquia via plataforma e e-mail/push. Manutenção fica com status Pendente. |
| **3** | **Franquia** | Executa a manutenção no prazo acordado. |
| **4** | **Franquia** | Acessa a plataforma, abre a ordem e realiza o upload das evidências (fotos/vídeos antes e depois). |
| **5** | **Sistema** | Valida que ao menos uma evidência foi anexada. Altera status para Em Revisão. |
| **6** | **Seazone** | Analisa as evidências. Aprova ou solicita reenvio com justificativa. |
| **7** | **Sistema** | Ao aprovar: dispara evento para módulo de Reembolso com os dados da manutenção. Status muda para Concluída. |

\n

## **4.2 Fluxo B — Manutenção Programada (valor > R$ 300)**

Idêntico ao Fluxo A, com o seguinte passo adicional entre os passos 2 e 3:

\n

| **#** | **Ator** | **Ação** |
|----|----|----|
| **2a** | **Sistema** | Detecta valor > R$ 300. Coloca a manutenção em status Aguardando Aprovação do Proprietário e notifica o proprietário do imóvel. |
| **2b** | **Proprietário** | Acessa a notificação (e-mail ou portal), visualiza detalhes e valor, e Aprova ou Rejeita com campo de comentário obrigatório na rejeição. |
| **2c** | **Sistema** | Se aprovado: segue para passo 3 (franquia executa). Se rejeitado: notifica Seazone e a ordem é cancelada ou renegociada. Se sem resposta no prazo (padrão 48 h): escala para a Seazone decidir. |

\n

## **4.3 Fluxo C — Manutenção Proativa da Franquia**

* Franquia acessa a plataforma e registra uma nova manutenção proativa: seleciona imóvel, tipo, valor e data de execução.
* Sistema marca a manutenção como Proativa e coloca em status Em Revisão (Seazone).
* Franquia faz upload das evidências.
* Se valor > R$ 300: segue subfluxo de aprovação do proprietário (2a–2c) antes da validação da Seazone.
* Seazone valida e aprova ou rejeita. Se aprovada, evento de reembolso é disparado.


# **5. Ciclo de Vida — Estados da Manutenção**

| **Status** | **Responsável** | **Condição de saída** |
|----|----|----|
| **Pendente** | Franquia | Franquia inicia a execução ou prazo vence. |
| **Aguardando Aprovação do Proprietário** | Proprietário | Proprietário aprova, rejeita ou prazo expira. |
| **Em Execução** | Franquia | Franquia faz upload das evidências. |
| **Em Revisão** | Seazone | Seazone aprova ou solicita reenvio. |
| **Reenvio Solicitado** | Franquia | Franquia envia novas evidências. |
| **Concluída** | Sistema | Estado final — reembolso disparado. |
| **Cancelada** | Seazone | Estado final — proprietário rejeitou ou Seazone cancelou. |
| **Vencida** | Sistema | Prazo expirou sem execução — escalonamento acionado. |


# **6. Requisitos Funcionais**

## **6.1 Portal Seazone (Backoffice)**

* RF-01  Criar, editar e cancelar ordens de manutenção com seleção de imóvel, tipo, valor estimado, franquia responsável e prazo.
* RF-02  Visualizar todas as manutenções em dashboard com filtros por imóvel, franquia, status, tipo e período.
* RF-03  Revisar evidências enviadas pela franquia e aprovar ou solicitar reenvio com justificativa.
* RF-04  Consultar histórico completo e imutável de cada manutenção (log de auditoria).
* RF-05  Receber alertas de manutenções vencidas ou com prazo próximo.
* RF-06  Remover evidências com justificativa, gerando registro no log.
* RF-07  Configurar o prazo de resposta do proprietário (padrão 48 h).
* RF-08  Exportar relatório de conformidade por franquia e por período.

\n

## **6.2 Portal / App da Franquia**

* RF-09  Visualizar fila de manutenções atribuídas, ordenadas por prazo.
* RF-10  Atualizar status de execução (iniciar, concluir) com data e horário.
* RF-11  Realizar upload de evidências (fotos, vídeos, documentos) com limite configurável de arquivos e tamanho.
* RF-12  Registrar manutenções proativas: imóvel, tipo, valor, data e evidências.
* RF-13  Consultar histórico de manutenções realizadas e status de reembolsos vinculados.
* RF-14  Receber notificações de novas ordens, prazos e solicitações de reenvio.

\n

## **6.3 Portal do Proprietário**

* RF-15  Receber notificação (e-mail e portal) para aprovação de manutenções > R$ 300.
* RF-16  Visualizar detalhes da manutenção: tipo, valor, imóvel e justificativa da Seazone.
* RF-17  Aprovar ou rejeitar com campo de comentário obrigatório na rejeição.
* RF-18  Consultar histórico de todas as manutenções do seu imóvel com evidências e valores.

\n

## **6.4 Automações e Integrações**

* RF-19  Disparar evento para o módulo de Reembolso ao concluir uma manutenção aprovada (payload: id_manutenção, imóvel, franquia, valor, data, evidências).
* RF-20  Enviar lembretes automáticos de prazo (D-2, D-1, dia do vencimento) para a franquia.
* RF-21  Escalar manutenções vencidas automaticamente com alerta para a equipe de Operações da Seazone.
* RF-22  Escalar aprovações de proprietário sem resposta no prazo configurado.


# **7. Requisitos Não Funcionais**

* RNF-01  Auditabilidade: todas as ações devem ser registradas em log imutável com timestamp e usuário.
* RNF-02  Disponibilidade: uptime mínimo de 99,5% para os portais de franquia e Seazone.
* RNF-03  Armazenamento de evidências: suporte a arquivos de até 50 MB por upload; armazenamento seguro com acesso por URL assinada com expiração.
* RNF-04  Notificações: entrega de e-mail em até 2 minutos após o evento; push (se app) em tempo real.
* RNF-05  Rastreabilidade: cada manutenção deve ter um ID único e todos os eventos vinculados a ela devem referenciar esse ID.
* RNF-06  Segurança: a franquia só pode visualizar imóveis da sua carteira; o proprietário só visualiza seus imóveis; logs de acesso são mantidos por 12 meses.
* RNF-07  Performance: listagem de manutenções com até 1.000 registros deve responder em menos de 2 segundos.


# **8. Modelo de Dados (Resumido)**

## **8.1 Entidade: Manutenção**

| **Campo** | **Tipo** | **Descrição** |
|----|----|----|
| **id** | UUID | Identificador único da manutenção. |
| **imovel_id** | FK | Referência ao imóvel cadastrado (obrigatório). |
| **franquia_id** | FK | Franquia responsável pela execução. |
| **tipo_manutencao** | Enum | limpeza_ar, higienizacao_cama, higienizacao_sofa, outro. |
| **origem** | Enum | programada \| proativa |
| **valor_estimado** | Decimal | Valor em R$. Determina necessidade de aprovação do proprietário. |
| **status** | Enum | Pendente, Aguardando Aprovação, Em Execução, Em Revisão, Reenvio Solicitado, Concluída, Cancelada, Vencida. |
| **prazo_execucao** | DateTime | Data limite para a franquia concluir. |
| **data_execucao** | DateTime | Data/hora real de conclusão pela franquia. |
| **aprovado_proprietario** | Boolean / Null | Null = não aplicável; True/False após decisão. |
| **comentario_proprietario** | Text | Preenchido obrigatoriamente na rejeição. |
| **reembolso_disparado** | Boolean | Indica se o evento de reembolso já foi enviado. |
| **criado_em** | DateTime | Timestamp de criação. |
| **atualizado_em** | DateTime | Timestamp da última atualização. |

\n

## **8.2 Entidade: Evidência**

* id (UUID), manutencao_id (FK), url_arquivo, tipo (foto | video | documento), hash_integridade, enviado_em (DateTime), enviado_por (FK usuário franquia).

\n

## **8.3 Entidade: Log de Auditoria**

* id, manutencao_id (FK), acao (ex: status_change, evidencia_enviada, aprovacao_proprietario), usuario_id, timestamp, payload_anterior, payload_novo.


# **9. Métricas de Sucesso**

| **Métrica** | **Baseline esperado** | **Meta (6 meses)** |
|----|----|----|
| Taxa de conformidade (manutenções concluídas no prazo) | — | **≥ 90%** |
| Taxa de manutenções com evidências na primeira submissão | — | **≥ 85%** |
| Tempo médio de revisão pela Seazone | — | **< 24 h** |
| Taxa de resposta do proprietário dentro do prazo | — | **≥ 80%** |
| Manutenções vencidas sem execução | — | **< 5% do total** |


# **10. Questões em Aberto**

* OQ-01  Quais são os tipos de manutenção recorrente iniciais a serem cadastrados? Quem é o owner do catálogo de tipos?
* OQ-02  O prazo de resposta do proprietário (padrão 48 h) é configurável por imóvel ou global?
* OQ-03  O valor de R$ 300 para aprovação do proprietário é fixo ou configurável por imóvel/proprietário?
* OQ-04  Como será o contrato de interface (payload) com o módulo de Reembolso? Quando será definido?
* OQ-05  As franquias usarão app mobile ou apenas web? Isso impacta o design das notificações.
* OQ-06  Qual o limite de arquivos e tamanho máximo por evidência? (Sugestão inicial: 10 arquivos, 50 MB cada.)
* OQ-07  Há necessidade de integração com sistemas legados ou ERPs externos?
* OQ-08  O proprietário terá acesso contínuo ao portal ou apenas via link de notificação?

\n

# **11. Próximos Passos**

| **#** | **Ação** | **Responsável** |
|----|----|----|
| **1** | Revisão e alinhamento do PRD com stakeholders de Operações e Franquias. | **Product Manager** |
| **2** | Resolução das questões em aberto (seção 10). | **PM + Operações** |
| **3** | Definição do contrato de integração com módulo de Reembolso. | **PM + Engenharia** |
| **4** | Design de protótipos de baixa fidelidade dos portais (Seazone, Franquia, Proprietário). | **UX Design** |
| **5** | Refinement técnico e quebra em épicos/histórias para o backlog. | **PM + Engenharia** |
| **6** | Definição de MVP: quais funcionalidades entram na primeira entrega. | **PM + Liderança** |

\n


\n