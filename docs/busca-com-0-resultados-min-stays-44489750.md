<!-- title: Busca com 0 resultados => "Min Stays" | url: https://outline.seazone.com.br/doc/busca-com-0-resultados-min-stays-uC0BsoaUKG | area: Tecnologia -->

# 🔎 Busca com 0 resultados => "Min Stays"

# Problema

Atualmente o usuário que quer reservar menos do que 3 dias com antecedência não consegue e encontra 0 resultados. No geral, isso acontece em 10% dos usuários que acessam o nosso site. Porém, em salvador (nosso foco) essa porcentagem pode chegar em até 40% porque usuários em salvador reservam com muita antecedência (1 mês em média).

# Regras aplicadas - "Min Stays"

Os valores para pesquisas podem ser editavas via ff no Posthog [exp_ignore_min_stay](https://us.posthog.com/project/47303/feature_flags/157770), nesse payload tem dois valores, o `max_stay_suggestion` e o `min_search_results` , a definição deles é essa logo abaixo.


`max_stay_suggestion:` define o número máximo de dias que o sistema irá estender a data de checkout durante a busca. Exemplo: se definido como 7, o sistema tentará aumentar o período até 7 dias, procurando por propriedades disponíveis.

\n`min_search_results:` define o número mínimo de propriedades necessárias para encerrar a busca. Enquanto o resultado estiver abaixo desse valor, o sistema continuará tentando ampliar o período até atingir o limite definido por `max_stay_suggestion`.


Os dados atualmente são:

`{"max_stay_suggestion": 5, "min_search_results": 9}`


\
[Solução Implementada](/doc/solucao-implementada-x3hLatGxQH#h-4-%E2%9C%85-solucao-aceita)

#