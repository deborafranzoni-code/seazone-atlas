<!-- title: Consolidação | url: https://outline.seazone.com.br/doc/consolidacao-HNEC2dXo3z | area: Tecnologia -->

# Consolidação

A consolidação é o processo de gerar as NF que serão emitidas pela Seazone para os proprietários. Dentro desse processo também é gerada uma lista de NF que é enviada para os anfitriões para os mesmos poderem emitir sua nota fiscal. No caso dessas NF do anfitrião a Seazone não emite, é responsabilidade do anfitrião de emitir.

## Regras Gerais

Regras para o cálculo e como cada NF é gerada dentro da consolidação.

### Endereço de cobrança

O endereço de cobrança é importante pois é um agrupador de valores. Temos um cadastro para o endereço de cobrança na tabela `Invoice_Details` , esse endereço é cadastrado no imóvel e no proprietário. O endereço cadastrado no proprietário é o padrão e se um imóvel não tem um endereço de cobrança cadastrado é utilizado a do proprietário. Cada imóvel de um proprietário pode ter um endereço de cobrança diferente e será gerado NF diferentes para cada imóvel nesse caso.

### Receita do imóvel

As receitas dos imóvel estão na tabela `Revenues` e são utilizadas para pegar o campo `commission` . Essa tabela é preenchida no processo de fechamento financeiro para calcular a comissão do imóvel que será paga para a Seazone.

### Receita do anfitrião

A receita do anfitrião está na tabela `Host_Revenues` e são utilizadas para pegar o campo `reservation_incomes` . Esse campo se refere a receita que o imóvel desse anfitrião teve no mês com reservas.

### Troca de anfitrião

Se houver uma troca de anfitrião em um imóvel, a consolidação identifica essa troca e faz um fluxo diferente para esse imóvel. É calculado o valor de cada anfitrião separadamente, de acordo com a receita que o mesmo teve enquanto era anfitrião do imóvel no mês. Esse valor se encontra na tabela `Host_Revenues` já com o valor calculado de acordo com a troca.

### Valor da NF

* Valor da NF do anfitrião: É calculado pegando o `reservation_incomes` que o anfitrião teve na propriedade no mês e multiplicando pela **taxa de comissão de reserva** do anfitrião. Esse valor de encontra na tabela `Host` no campo `reservation_commission_fee` e tem como um valor padrão 8%, podendo variar de acordo com o anfitrião.
* Valor da NF do proprietário: É calculado pegando o `commission` da propriedade e subtraindo o valor de **comissão de reserva** do anfitrião, calculado acima.

### Cálculo

$ValorNFAnfitrião = ReceitaReservas\*Taxa$

$ValorNFProprietário = Comissão - ValorNFAnfitrião$

### Salvando os dados

Ao final do processo com os valores de NF do proprietário e do anfitrião, os dados são salvos em suas respectivas tabelas. O valor de NF do proprietário é salvo na tabela `nf` onde se encontra todas as NF que a Seazone deve emitir. O valor de NF do anfitrião é salvo na tabela `NFHost` onde é se encontra a lista que será enviada para os anfitrião informando os dados de cada NF que ele deve emitir.