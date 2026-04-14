<!-- title: Prioridades - Conceitos | url: https://outline.seazone.com.br/doc/prioridades-conceitos-EEQortDGAe | area: Tecnologia -->

# Prioridades - Conceitos

No fluxo de Suporte atual, temos uma fase que é a priorização para a resolução. As prioridades e tempos de resolução definidos atualmente para os times é o seguinte:

* P0 (**Crítico**) - Highest - 1 a 4 horas
* P1 (**Alto**) - High           - 1 dia
* P2 (**Médio**) - Medium - 1 a 3 dias
* P3 (**Baixo**) - Low         - 5 a 7 dias
* P4 (**Mínimo**) - Lowest - mais de 15 dias


As características que devemos considerar para classificar as prioridades dos suportes são:

# **P0 - Crítico**

**Tempo de Resolução :** 1 a 4 horas

**Descrição:**\nUm P0 significa que o  sistema/plataforma ou serviço crítico está totalmente inoperacional, causando uma paragem completa das operações para **==todos==** ou para um grande número de usuários.

Estes incidentes têm um impacto financeiro, de segurança ou de reputação  e exigem uma resposta imediata e a mobilização de todos os recursos necessários até que o serviço seja restaurado.


## **Exemplos:**

* **Indisponibilidade Total da Plataforma:** O site da Seazone, Wallet, Sapron estão offline, impedindo a realização de novas acessos, reservas, check-ins ou a gestão operacional.

  \
* **Falha Sistêmica de Sincronização:** A ligação da Stays com todos os OTAs(Airbnb, Booking.com, etc.) cai, resultando num risco massivo de overbooking em todo o portfólio.
  * sincronização/atualização de reservas
  * bloqueio de reservas

  \
* **Dados financeiros errados:** dados inconsistentes podem causar desconfiança nos serviços da Seazone 
  * Dados de pagamentos de reservas errados, 
  * Saldos de proprietários e franqueados 
  * Dados do Fechamento de proprietários / franqueados

  \

# **P1 - Crítico**

**Tempo de Resolução:** 1 dia útil

**Descrição:**

Indica uma falha grave, mas parcial. A plataforma está online, mas uma funcionalidade crítica ou um módulo específico não funciona, afetando um grupo significativo de utilizadores. Embora o impacto seja alto, existem **soluções de contorno (workarounds)**, geralmente manuais ou operacionais, que permitem que a operação continue de forma degradada enquanto a equipa técnica trabalha na solução definitiva.


## **Exemplos:**

* **O sistema de checkout (mobile/desktop) de pagamentos falha.** *Contorno***:** O time de atendimento contacta os hóspedes para ajudar/processar os pagamentos manualmente.

  \
* **O dashboard financeiro dos proprietários não carrega.** *Contorno***:** A equipe de atendimento ao Proprietário ou o #supote-wallet / #suporte-sapron  extrai e envia os relatórios manualmente.

  \
* **A sincronização de calendários com o Stays falha**, gerando risco de overbooking. *Contorno***:** A equipe de atendimento bloqueia manualmente os calendários ou gera as reservas enquanto o problema é resolvido.

  \
* **Painel do Proprietário com Dados Incorretos:** O dashboard do proprietário exibe informações financeiras ou de ocupação  erradas, em algumas telas, quebrando a confiança. *Contorno***:** O proprietário consegue acessar as informações certas em outras funcionalidades como o extrato, enquanto é resolvido o erro.

  \
* Dados de login/senha: Alguns casos podem não ser bug, porem o login e senha dos usuários (proprietários, franqueados, parceiros) é o acesso principal a seazone, então eles são sempre considerados como P1 para o usuario que solicitou o suporte


# **P2 - Médio**

**Tempo de Resolução:** 1 a 3 dias úteis

**Descrição:**\nEste tipo de suporte refere-se a problemas que, embora pareçam uma falha para o utilizador final, podem ser resolvidos operacionalmente alguns casos **sem a necessidade de intervenção dos devs**. 

Geralmente envolvem erros de configuração, ajustes de dados, processos manuais ou orientação ao utilizador. 

## **Exemplos:**

* Atualização de links externos (website)
* Atualização de dados pessoais, bancários, endereços,
* Atualização de dados sobre taxas (obs. Nestes casos considerar se afeta o Fechamento do mês atual eles se tornam P1)


# **P3 - Baixo**

**Tempo de Resolução Alvo:** 5 a 7 dias úteis

**Descrição:**\nQuestões de baixo impacto, como erros cosméticos, dúvidas gerais ou problemas em funcionalidades raramente utilizadas. Não afetam a experiência do usuário.

## **Exemplos:**

* Pequenos ajustes ou melhorias não muito complexas.

  \

# **P4 - Mínimo**

**Tempo de Resolução Alvo:** Mais de 15 dias úteis

**Descrição:**\nReservado para pedidos que não são problemas, mas sim sugestões de melhoria, pedidos de novas funcionalidades ou tarefas de manutenção não urgentes. Estes itens são adicionados ao backlog para análise e planeamento futuro.

## **Exemplos:**

* Nova tela de edição de dados bancários  (ainda não existente)