<!-- title: Home | url: https://outline.seazone.com.br/doc/home-ZetmmUv94S | area: Tecnologia -->

# Home

A Home é dividida em três principais sessões, sendo elas grid financeiro, meus imóveis e próximas reservas.

**Implementação do GRID Financeiro - Regras de Exibição e Negócio**

### Regras de Exibição:


1. O GRID deve ser fixo na tela, visível o tempo todo durante a navegação.
2. As informações exibidas devem ser retornadas com granularidade mensal.
3. Em caso de múltiplos imóveis, o usuário deve ter a opção de filtrar os dados por imóvel específico.
4. Ao abrir a tela, as informações exibidas por padrão devem corresponder:
   * Ao mês atual.
   * À visualização de "Todos os imóveis" (quando houver mais de um).
5. Caso o usuário possua apenas um imóvel, o filtro de seleção de imóveis não deve ser exibido.

### Regras de Negócio:

* **Diárias Executadas:** Corresponde ao total de diárias recebidas no mês de referência que foram efetivamente ocupadas pelos hóspedes. Inclui somatório das diárias de todas as plataformas (Airbnb, Website Seazone, Booking, Expedia, Decolar) mais os ajustes positivos. **Este valor não reflete o repasse ao proprietário.**
* **Acumulado 2024:** Representa o somatório do valor total faturado ao longo do ano de 2024.
* **Receitas:** Refere-se ao valor total das diárias do mês corrente que foram utilizadas e pagas nas plataformas Airbnb e Website Seazone, somado às diárias do mês anterior das plataformas Booking, Expedia, Decolar e aos ajustes positivos.
* **Descontos:** Inclui todas as despesas relacionadas ao imóvel, como ajustes financeiros negativos, comissões e taxas de adesão.
* **Resultado:** Calculado como a diferença entre as **Receitas** e os **Descontos** no mês corrente.

### Observação:

Por padrão, os valores exibidos devem representar o total de todos os imóveis. Contudo, essa exibição será ajustada conforme o filtro de imóvel específico selecionado pelo usuário.

## Meus Imóveis

### **Regras de Exibição:**


1. O proprietário deve visualizar a lista de seus imóveis, com a possibilidade de ver o **status atual** de cada imóvel.

**Status disponíveis**:

* **Locado**
* **Bloqueado**
* **Livre**
* **Inativo**
* **Implantação**


1. Para proprietários com mais de um imóvel, devem estar disponíveis filtros para: ◦ Seleção por **status** (locado, bloqueado, livre). ◦ Seleção por **imóvel** específico.
2. O proprietário deve ter a opção de: ◦ **Bloquear** um imóvel específico diretamente na interface. ◦ Ser **redirecionado para o módulo Financeiro** do imóvel. ◦ Visualizar o **calendário de disponibilidades**, que mostrará as datas de locação, bloqueios e períodos livres.

**Regras de Negócio:**

* **Resultado do Mês**: Representa a diferença entre as **Receitas** e **Descontos** referentes ao mês corrente para o imóvel selecionado.
* **Taxa de Ocupação**: Percentual de ocupação do imóvel, considerando apenas as datas que **não possuem bloqueio**.
* **Receita**: Valor total das diárias utilizadas e pagas no mês corrente pelas plataformas Airbnb e Website Seazone, somado às diárias do mês anterior provenientes de Booking, Expedia, Decolar, e ajustes positivos. O cálculo é feito para o imóvel específico selecionado.
* **Descontos**: Total de todas as despesas relacionadas ao imóvel, incluindo ajustes financeiros negativos, comissões e taxas de adesão, também referentes ao imóvel específico selecionado.

### **Observações:**

Inclusão do banner SPOT após os imóveis conforme figma.

## Próximas Reservas

### Regras de Exibição

* Realizar a exibição das 5 próximas reservas , levando em consideração todos os imóveis do proprietário.