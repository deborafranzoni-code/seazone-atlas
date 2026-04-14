<!-- title: Anfitrião | url: https://outline.seazone.com.br/doc/anfitriao-D9xcfK7Y6O | area: Tecnologia -->

# Anfitrião

* **Observação a respeito do novo modelo de anfitriões 10/2022**

  > Altera o fechamento do Anfitrião e da da propriedade para o novo modelo de franquia da Seazone. O novo modelo passa a valor em 10/2022 e para manter compatibilidade com os fechamentos antes de outubro os campos antigos foram alterados para ter o prefixo `legacy_`, enquanto novos campos foram adicionados para armazenas os novos valores. Para ser recalculado o fechamento legado (09/2022 para trás) foi implementado uma checagem de data e qualquer fechamento maior igual 10/2022 usa o novo modelo e menor igual 09/2022 usa o fechamento legado.

  > Implementando lógica para preecher os valores das colunas `Comissão de Reservas`, `Royalties` e `Comissão` na página de fechamento do anfitrião:
  > * `A regra é que para o fechamento do anfitrião dos meses de **OUTUBRO/2022 em diante** usaremos:`1°) Coluna **Royalties (Header do Grid):** usar valor igual a `0`2°) Coluna **Comissão de Reservas (Header do Grid):** usar valor retornado pela api no campo `reservations_commission`2°) **Coluna Comissão (Lista de Reservas):** usar valor retornado pela api no campo `reservations_commission`
  > * `Já para os meses **antes de OUTUBRO/2022**:`1°) Coluna **Royalties (Header do Grid):** usar valor retornado pela api no campo `legacy_royalties_seazone`2°) Coluna **Comissão de Reservas (Header do Grid):** usar valor retornado pela api no campo `legacy_reservations_commission`2°) Coluna **Comissão (Lista de Reservas):** usar valor retornado pela api no campo `legacy_commission`
  * Referencias

    [Trello](https://trello.com/c/LNrIxSr7)

    \
    \

### Despesas

Despesas onde o quem paga é o Proprietário são reembolsadas ao Anfitrião como repasse no mês de referência pelo **proprietário,** descontando do repasse dele\*\*.\*\*

Quando o quem paga é a Seazone, a despesa é reembolsada pela Seazone, descontando do repasse da Seazone.

Quando "quem paga" é o Anfitrião, a despesa é descontada do repasse do próprio.


---

Com a mudança realizada no [PR](https://github.com/Khanto-Tecnologia/sapron-pms-web/pull/1169), agora será possível inserir despesas apenas para o Anfitrião não mencionando a propriedade.

Essa despesa que não tem a propriedade, deverá ser considerada no cálculo do fechamento do anfitrião junto com as outras despesas dele, porém, ela não aparecerá para os imóveis dele.

Para saber quem é o anfitrião é preciso verificar o campo **responsible_user** que faz referencia à tabela de Users, mas sempre se referente à um Anfitrião.

Esse tipo de despesa também deve aparecer na lista de Despesas do Anfitrião.

### **Saldos**

* Inicial: É o saldo final do mês anterior.
* Final: Saldo final do mês atual e será o saldo inicial do mês seguinte.


---

* **Check de quem é o host na data do fechamento**

  Ao ser feito a troca de host em uma propriedade e mesmo gerando a informação da troca na tabela `Host_time_in_property`. O fechamento financeiro criava um novo lançamento para o host novo em um mês que ele não era o host da propriedade, ou seja, quando o fechamento era executado para datas passadas. Esse PR trás uma validação para ser checado quem era o host na data do fechamento. <https://github.com/Khanto-Tecnologia/sapron-pms-web/pull/1661>
* Fechamento do Anfitrião é independente do fechamento da propriedade

  > O fechamento do Anfitrião não depende mais do fechamento da propriedade. Por causa dos trocas de anfitrião, não tem como utilizar os dados do fechamento da propriedade, sendo que ela não observa essa questão de trocas.

  Alteração implementada neste **[PR](https://github.com/Khanto-Tecnologia/sapron-pms-web/pull/1818)**
* Troca de anfitrião no dia 1 do mês

  Para quando a data de troca de um host for o dia 1º. O fechamento não será realizado para o antigo anfitrião, de forma que o novo anfitrião detém todas as receitas daquele mês


---

* Chamadas em APIs para trazer os dados

  <https://github.com/Khanto-Tecnologia/sapron-pms-web/pull/1975>