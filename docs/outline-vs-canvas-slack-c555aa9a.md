<!-- title: Outline vs Canvas Slack | url: https://outline.seazone.com.br/doc/outline-vs-canvas-slack-jfajCIecZI | area: Tecnologia -->

# Outline vs Canvas Slack

O objetivo desse documento é levantar características boas e ruins sobre ambas as ferramentas de documentação, o outline e o canvas do slack e com base nisso fazer uma sugestão de qual seria a melhor opção para o nosso caso 


# Canvas Slack 

A funcionalidade de Canvas no Slack permite criar e compartilhar documentos com mais informações e formatação personalizada, seja em uma mensagem direta ou em um canal 

## Pontos Fortes :muscle:

### Facilidade

Por ser o Slack uma ferramenta essencial para a empresa, e já utilizada para comunicação, o fato de a funcionalidade Canvas estar integrada a ele facilita a interação. Como provavelmente já estaremos com o Slack aberto o dia inteiro, fica mais fácil alternar entre as ferramentas rapidamente.

### Utilização de databases 

A funcionalidade Canvas do Slack permite integração com outra ferramenta do Slack, o Lists. Com o Lists, é possível criar uma visualização de quadro para suas tarefas, atribuir características a elas e aplicar filtros interessantes. Isso se assemelha à funcionalidade de databases do Notion. Vale ressaltar que, em comparação ao Notion, essa funcionalidade ainda está incompleta, mas, mesmo assim, facilita a gestão de tarefas.

###  Usabilidade

A interface do Slack é intuitiva e fácil de usar, o que facilita bastante a utilização da ferramenta.

## Pontos fracos :mask:

### Organização de permissões 

Os Canvas do Slack permitem a divisão de permissões, que podem ser feitas individualmente ou por canal. Isso pode tornar a organização das permissões trabalhosa e confusa, por falta de granularidade, algo que também ocorre atualmente no Notion.

### Organização de documentos 

No Canvas do Slack, a organização pode ser feita por meio do aninhamento de documentos, permitindo visualizar documentos dentro de outros. No entanto, a visualização é um pouco mais complexa, pois é necessário abrir os documentos para identificar quais estão referenciados.

### Migração 

Atualmente, estamos migrando do Notion para outra ferramenta de documentação que gere menos custo. No entanto, como o Slack Canvas não permite a importação direta de páginas do Notion, o processo seria muito trabalhoso, exigindo a criação manual de cada página atualmente existente

# Outline

O Outline é uma ferramenta open source para documentação de projetos e processos. Ela é muito semelhante ao Notion e oferece praticamente todas as funcionalidades necessárias para criar um documento

## Pontos Fortes **💪**

### Organização de permissões 

O Outline permite uma organização de permissões eficiente, possibilitando a criação de grupos e a granularização das permissões entre visualização, edição e gerenciamento

### Organização de documentações 

No Outline, é possível adicionar páginas em collections, que funcionam como pastas, e também aninhar páginas dentro de outras. A vantagem dele em relação ao Notion, por exemplo, é que, através da barra lateral, conseguimos visualizar todas as páginas dentro de uma determinada pasta, facilitando a organização e a navegação

### Migração 

O Outline permite a migração de páginas e até workspaces inteiros do Notion. Embora isso possa gerar alguns erros de formatação e exija uma certa revisão, é muito mais rápido do que recriar todas as páginas que temos atualmente no Notion do zero

### Open Source

O Outline é uma ferramenta open source, o que significa que não pagamos nenhum tipo de assinatura para utilizar suas funcionalidades. Precisamos arcar apenas com o custo de mantê-la rodando na nossa infraestrutura, o que acaba sendo mais barato do que pagar pela assinatura de uma plataforma

## Pontos Fracos  **😷**

### Utilização de databases 

Atualmente, não conseguimos utilizar as funções de databases que o Notion oferece no Outline. No momento, a aplicação disponibiliza apenas recursos de formatação e funcionalidades voltadas para a parte de documentação, não cobrindo a parte de gerenciamento de tarefas

### Revisão de arquivos migrados 

Como mencionado anteriormente neste documento, embora o Outline permita a migração de documentos da nossa ferramenta atual de documentação (Notion), os documentos são migrados com alguns problemas de formatação, o que gera a necessidade de uma revisão geral


# Sugestão

Analisando os pontos levantados para cada uma das ferramentas, a melhor escolha para a parte de documentação, ou seja, escrita e leitura de documentos estáticos, ainda parece ser o Outline. No entanto, se quisermos gerar uma economia de custo, existe a possibilidade de migrarmos o gerenciamento de tarefas para a combinação Lists + Canvas do Slack. Dessa forma, desativaríamos por completo o Notion e continuaríamos utilizando o Slack, para o qual já pagamos um plano, e o Outline, no qual pagamos apenas para manter a plataforma funcionando em nossa infraestrutura

\n**Observação**: *no momento usar o canvas do slack não gera nenhum custo adicional ao nosso plano, mas é importante levantar que a ferramenta é privada e nada garante que não terá custos adicionais em algum momento*