<!-- title: Roadmap - Franquias | url: https://outline.seazone.com.br/doc/roadmap-franquias-oCRCTgjI4E | area: Tecnologia -->

# Roadmap - Franquias

| Item do Roadmap | Objetivo Estratégico | Resumo da Proposta | Tamanho do Problema | Priorização | IA/Automação Envolvida | Métricas de Sucesso | Insights & Oportunidades | Riscos & Alertas | Discovery |
|----|----|----|----|----|----|----|----|----|----|
| **Refatoração da tela de controle** | Otimização operacional e experiência do usuário | Facilitar organização da limpeza com novos filtros, geolocalização e usabilidade mobile. | 2 sprints | 5 - iara    | Algoritmo de roteirização por geolocalização. | % de tarefas organizadas por geolocalização, redução do tempo médio de organização, NPS mobile | Redução de tempo de organização da limpeza e erro humano. Melhoria na performance mobile. | Complexidade técnica da geolocalização e dependência de dados corretos. | Não iniciado |
| **Verificação de limpeza pré check-in** | Garantia de padrão de qualidade | Geração de link para preenchimento de checklist digital por responsáveis. | 3 sprints |    | Possível integração futura com IA para leitura de fotos e alertas automáticos. | % de checklists preenchidos, índice de conformidade, incidentes por falha de limpeza | Aumenta rastreabilidade e padronização do processo. Pode virar insumo para melhorias futuras. | Baixa adesão se não houver incentivo ou acompanhamento. | Não iniciado |
| **Análise de Comentários e Feedbacks de Melhoria** | Aumento de satisfação do hóspede e melhoria contínua | IA generativa para análise de sentimentos + dashboard de tendências e engajamento por imóvel. |    |    | ✔️ Análise de sentimento e tópicos com IA generativa. | % de comentários categorizados automaticamente, taxa de avaliação por reserva, melhoria de score médio | Permite ações proativas baseadas em dados. Detecta rapidamente melhorias eficazes ou ineficazes. | Risco de interpretações erradas se o volume de dados for baixo ou enviesado. | Em avaliação |
| **Tela de Manutenções Pendentes - organização de demandas no sapron** | Redução de problemas operacionais e aumento da qualidade | Tela de manutenção com alertas periódicos e IA sugerindo pendências com base em feedbacks. |    | 4 - bill  | ✔️ IA para identificar problemas em comentários. | Nº de manutenções resolvidas por mês, % de manutenção preventiva vs corretiva, tempo médio para resolução | Automatiza detecção de problemas ocultos. Reduz fricção entre operações e franquia. | Custo de manter atualização dos dados e IA pode gerar falsos positivos. | Não iniciado |
| **Dashboard de KPIs da Franquia** | Gestão de performance e expansão | Visualização de dados como imóveis ativos, score, receitas e comentários. |    | 2 - iara | IA para geração de insights preditivos futuros (opcional). | Nº de acessos ao dashboard, engajamento das franquias, % de franquias com dados atualizados | Empodera tomada de decisão. Permite benchmarking entre franquias. | Requer governança forte de dados para evitar erros de leitura. | Em definição |
| **~~Agent no Atendimento de Franquias~~****ta com a morada** | Agilidade e personalização do atendimento | Inserção de um "agent" com histórico de conversas e contexto. |    |    | ✔️ LLM (IA de linguagem) como agente inteligente. | Tempo médio de atendimento, satisfação com suporte, % de atendimentos resolvidos no 1º contato | Atendimento mais eficiente, menor tempo de resposta, menos fricção. | Risco de ruído se o histórico não for bem consolidado. | Em validação |
| **Controle de Estoque** | Redução de perdas e controle de custos | Sistema de controle de giro de enxoval por franquia. |    | 4 - bill  | Pode incluir alertas automatizados no futuro. | Acerto de inventário, índice de perda/ruptura, taxa de reposição por imóvel | Melhora reposição, reduz desperdício e perdas não registradas. | Requer adesão e disciplina operacional. | Não iniciado |
| **Vistorias e Onboarding via Sapron** | Escalabilidade e padronização | Digitalizar processo de vistoria e onboarding no sistema. |    |    | IA para validar imagens/fotos e reconhecer padrões. | % de vistorias concluídas sem retrabalho, tempo médio de onboarding, feedback de franquias | Aumenta qualidade e reduz variações no padrão de entrega. | Risco na padronização se houver baixa adoção ou má instrução. | Em análise |
| **~~Aviso de Reserva Instantânea~~** | Agilidade na operação e prevenção de erros | Alertas para reservas instantâneas. |    |    | - | % de reservas instantâneas com erro, tempo médio até resposta da franquia, alertas enviados | Evita conflitos de agenda e desalinhamentos operacionais. | Ruído se o alerta não for bem calibrado (excesso ou ausência). | Em proposta |
| **Melhoria no Cadastro de Imóvel** | Padronização e qualidade dos dados | Novo fluxo de cadastro com mais campos e organização. Entrega em duas etapas (visualização no Metabase + Sapron). |    | 5 - bill  | IA futura para sugerir correções ou detectar inconsistências. | % de cadastros completos, erros por inconsistência, tempo médio de preenchimento | Dados mais completos elevam qualidade dos anúncios e operação. | Risco de abandono no meio do processo se for muito extenso. | Em elaboração |
| **Melhorias no processo de implantação** | Escalabilidade e eficiência operacional | Fluxo mais robusto de onboarding e cadastro. |    |    | - | Tempo médio de implantação, nº de erros no onboarding, satisfação das franquias | Acelera entrada de novos imóveis e reduz erros. | Sobrecarga no time se feito manualmente. | Em desenvolvimento |
| Processo de distribuição de imóveis e stop de crescimento  |    |    |    |    |    |    |    |    |    |
|    |    |    |    |    |    |    |    |    |    |


---

## 🚨 Possíveis Riscos Gerais

* **Baixa adoção pelas franquias** sem um programa de comunicação, treinamento e incentivo.
* **Dependência de dados ruins ou incompletos**, que podem gerar ruído em ferramentas baseadas em IA.
* **Falta de priorização executiva** que pode engavetar propostas com alto potencial de retorno.
* **Infraestrutura técnica subdimensionada** pode atrasar entregas com foco em IA e dashboards.


---