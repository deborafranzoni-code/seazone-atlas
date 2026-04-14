<!-- title: Extensões não carregam no Sapron [Nomes divergentes no BD] | url: https://outline.seazone.com.br/doc/extensoes-nao-carregam-no-sapron-nomes-divergentes-no-bd-X6tzMl5yhr | area: Tecnologia -->

# Extensões não carregam no Sapron [Nomes divergentes no BD]

**Observações**

Para conseguir resolver esse suporte é preciso ter acesso ao Banco de Dados  de Produção o login da Stays.

**Contexto**


1. O primeiro contexto  o suporte pode ser resumido à impaciência da pessoa que pediu, devido ao  Sapron não pegar de forma instantânea os bloqueios e extensões da Stays, nesse caso deve ser observado se a extensão  foi feita  a mais de 1 dia.
2. O segundo contexto é quando a pessoa que fez a reserva na Stays  inseriu o nome de outra pessoa na reserva.

**Possível Solução**

Para o contexto 2 a solução foi alterar o nome que estava associado à reserva no  Sapron pelo nome da pessoa que fez a reserva na Stays.  Essa alteração  foi feita diretamente no banco de dados, pesquisando pela reserva na tabela de `reservation_reservation`, com a reserva encontrada, indo em `guest_id`, depois em `user_id`  e alterando para o nome do dono da reserva.

Entenda mais  esse contexto lendo a conversa  do suporte: <https://seazone-fund.slack.com/archives/C02H5GM0VB5/p1683899405927859>

Algumas informações importantes para conseguir realizar o suporte:

* Código da Reserva
* Código do imóvel
* Nome do dono da reserva original