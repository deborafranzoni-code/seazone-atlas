<!-- title: [Uptime Kuma] | url: https://outline.seazone.com.br/doc/uptime-kuma-Jw68cPcRNa | area: Tecnologia -->

# [Uptime Kuma]

data : 18/06/2025


---

### **Incidente: Erro de Timeout nas Conexões do Uptime Kuma**

**Descrição do Problema**:\nO Uptime Kuma, que utiliza a biblioteca Knex.js para gerenciar as conexões com o banco de dados, apresentou o erro:

**Mensagem do erro**:\n`"Knex: Timeout acquiring a connection. The pool is probably full. Are you missing a .transacting(trx) call?"`

Esse erro indica que o número máximo de conexões simultâneas no pool de conexões foi alcançado. Com isso, novas conexões precisam aguardar a liberação de uma conexão existente. No entanto, as conexões que estavam aguardando atingiram o tempo máximo de espera, resultando no erro de timeout.

**Comportamento Observado**:\nNem todos os monitores falharam, apenas aqueles que estavam tentando se conectar no momento em que o erro ocorreu. Monitores de staging, por exemplo, que estão em manutenção, não apresentaram esse problema.


---

### **Possíveis Causadores**:


1. **Excesso de Monitores**:\nAlguns usuários do Kuma relataram problemas semelhantes ao terem mais de 50 monitores. Embora esse número não tenha sido atingido em nosso caso, é algo a ser monitorado, já que o problema é mais comum em instalações com muitos monitores.
2. **Armazenamento Histórico Exagerado**:\nO banco de dados pode ficar sobrecarregado quando muitos dados históricos são armazenados. Em relatos de outros usuários, quando o banco atinge cerca de 1 GB de dados, o problema se torna mais comum. Nosso banco ainda não atingiu esse tamanho, mas já está próximo de 800 MB, o que pode contribuir para a lentidão nas conexões.
3. **Versão Desatualizada do Uptime Kuma**:\nVersões mais antigas do Kuma não têm mecanismos automáticos para limpar o banco de dados, o que pode causar acúmulo de dados históricos desnecessários. Em versões mais recentes, esse processo é feito automaticamente, mantendo o banco mais leve e rápido.


---

### **Soluções Propostas**:


1. **Reduzir o Histórico de Dados Armazenados**:\nAtualmente, armazenamos cerca de 180 dias de dados históricos. A sugestão é reduzir esse período para 90 dias, visto que para investigar problemas antigos podemos utilizar outras ferramentas de monitoramento, como o Grafana, que são mais adequadas para essa finalidade.
2. **Ativar a Opção de "Shrink Database" no Uptime Kuma**:\nAtivar essa opção permitirá que o Kuma faça a limpeza automática do banco de dados, removendo dados e objetos não utilizados, além de otimizar e melhorar a performance das consultas.
3. **Atualizar a Versão do Uptime Kuma**:\nCriar uma tarefa para atualizar a versão do Uptime Kuma para garantir que a otimização do banco ocorra de forma automática. Isso evitará a necessidade de monitorar periodicamente o tamanho do banco e aplicar a limpeza manualmente.
4. **Implementar Monitoramento e Alertas para o Kuma**:\nO Uptime Kuma já possui o agente do Google Cloud Platform (GCP) ativado. Será necessário investigar como configurar alertas para notificar a equipe sempre que esse tipo de problema ocorrer, permitindo uma resposta rápida antes que o sistema impacte os usuários.


---

### **Correções aplicadas**:


1. Implementar a redução do histórico de dados para 90 dias.
2. Ativar a função de limpeza do banco de dados no Uptime Kuma.

### Próximos passos: 


1. Agendar a atualização da versão do Uptime Kuma.
2. Configurar um sistema de monitoramento e alertas para o Uptime Kuma.