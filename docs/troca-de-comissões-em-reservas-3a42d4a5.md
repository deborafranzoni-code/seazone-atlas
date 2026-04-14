<!-- title: Troca de comissões em reservas | url: https://outline.seazone.com.br/doc/troca-de-comissoes-em-reservas-hbDAriwJz5 | area: Tecnologia -->

# Troca de comissões em reservas

Regra: o worker não atualiza os dados da reserva se o campo "Conciliada=true"

O que fazer: primeiro, trocar "Conciliada=false"; segundo, fazer atualizações solicitadas; terceiro. trocar "Conciliada=true".