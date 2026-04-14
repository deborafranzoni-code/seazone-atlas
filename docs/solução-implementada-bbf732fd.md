<!-- title: Solução Implementada | url: https://outline.seazone.com.br/doc/solucao-implementada-x3hLatGxQH | area: Tecnologia -->

# Solução Implementada

## 4. **✅** Solução Aceita: 

Usuário não tem diferença de experiência na busca e na página do imóvel. Acredita que esse é o preço real. E quando ele clica para reservar mostramos um popup para ele reservar com o atendimento.


> Usuário vê as propriedades com as datas BUSCADAS, mas com o preço do mínimo de dias. O usuário acredita que reservou somente 1 dia.
>
> Por exemplo:
>
> → Do dia 1/4 ao dia 2/4 por 1300 reais. (Preço real é do dia 1 ao dia 4/4 por 1300 reais). Na página do imóvel ele vê também o mesmo preço que viu na página de busca.


### Card da tarefa no Jira  - <https://seazone.atlassian.net/browse/SZRDEV-1177>

**Problema**

Atualmente o usuário que quer reservar menos do que 3 dias com antecedência não consegue e encontra 0 resultados. No geral, isso acontece em 10% dos usuários que acessam o nosso site. Porém, em salvador (nosso foco) essa porcentagem pode chegar em até 40% porque usuários em salvador reservam com muita antecedência (1 mês em média).

**Solução Proposta**

Vamos supor que o usuário quer reservar para daqui 1 mês por somente 1 dia. Do dia 1 ao dia 2 de junho. Vamos supor que nessa data o mínimo seja de 3 noites. Vamos supor que o preço total para 3 noites seja de 1000 reais. 

O que atualmente aparece para o usuário: 0 resultados.

O que aparecerá: todas as propriedades, nas datas buscadas (1/6 à 2/6) porém com o preço do mínimo de 3 noites (R$1000).

O usuário acredita que R$1000 é o preço para 1 noite.

Então procede para a página do imóvel onde esse valor deve persistir.

O usuário deve visualizar as suas datas desejadas (1/6 → 2/6) e ver o preço do minimo de noites (R$1000 1/6 → 4->6).

Nessa página deve aparecer o botão de "Reserva Whatsapp", conforme o figma.

Os cliques nesse botão devem ser traqueados no evento:\nIMÓVEL - clicou em reserva whatsapp

Deve ser possível desligar o teste via feature flag

O botão de whatsapp só aparece para as reservas que se enquadram neste problema de min stays, se o usuário mudar as datas na página do imóvel para outras datas, deve aparecer o botão normal.

Na página do imóvel, ao selecionar as datas pelo calendário, deve ser possível selecionar menos do que o mínimo de noites também  


**FAQ**


1. Mas e se o mínimo for de 2 noites? Ou 4 noites? → Mostramos o preço do que é de fato o mínimo, seja 2, 3 ou 4 noites. Nós não buscamos acima de 4 noites.
2. E devo buscar datas disponíveis antes também? → Não! O primeiro dia da reserva deve sempre ser o mesmo dia selecionado pelo usuário. Isso acontece porque é importante que o anfitrião se prepare para fazer o checkin naquele dia.


\

\