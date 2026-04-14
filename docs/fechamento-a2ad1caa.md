<!-- title: Fechamento | url: https://outline.seazone.com.br/doc/fechamento-IHEof77WHn | area: Tecnologia -->

# Fechamento

> Informações das páginas de fechamento e também dos cálculos que estão sendo realizados na página.

### Cálculos

[Imóvel](/doc/imovel-lUYhfjC2w1)

[Proprietário](/doc/proprietario-WVSPWtf8cO)

[Anfitrião](/doc/anfitriao-4W3NsNBM9u)

* **Observações**
  * **Tratamento de imóveis, proprietários e anfitriões inativos**

    Foi definido que o fechamento financeiro não deve mais considerar o status de `Ativo` para a propriedade, anfitrião e proprietário.

    Para isso o fechamento para a **propriedade** e **proprietário** serão executados para todas as propriedades com status diferente de `Onboarding`.

    Para o **anfitrião**, se o mesmo estiver inativo, será chegado na tabela de log `property_host_time_in_property` se houve uma alteração de anfitrião. Se houver registro e o anfitrião inativo estiver como host antigo será feito o fechamento para e para meses futuros de acordo com a configuração de OTA que pagam com delay.
    * Referencias
      * [PR #1483](https://github.com/Khanto-Tecnologia/sapron-pms-web/pull/1483)
      * \


---

### Ações

* **Atualizar dados**
  * Necessário selecionar as linhas que deseja atualizar, após isso deve clicar na ação de Atualizar dados.
  * Ao atualizar dados, todos as linhas selecionadas serão atualizadas, rodando o cálculo de fechamento e exibindo no front os valores atualizados.
  * Ao atualizar as dados é sempre recalculado quem esta com o Open, indiferente se for a `revenue` ou `revenue_ota`. Apenas aparece que quando a `revenue_ota`  esta Closed não atualiza os dados porque como não tem alteração de faturamento e receita, os dados na `revenue` não alteram de valor, mas eles foram recalculados
  * \
* **Validação de dados**
  * Necessário selecionar as linhas que deseja validar, após isso deve clicar na ação de validar dados.
  * Ao **validar os dados** os registros (das tabelas Revenues e Revenues_OTA) são atualizados com o `*status='Closed'`.\*
  * No front toda registro validado fica com a linha na cor verde.
  * Uma vez validado, os valores não se alteram.
* **Desvalidação de dados**
  * Necessário selecionar as linhas que deseja validar, após isso deve clicar na ação de validar dados.
  * Ao **desvalidar os dados** os registros (das tabelas Revenues e Revenues_OTA) são atualizados com o `*status='Open'*`
  * No front toda registro validado fica com a linha na cor cinza.
  * Uma vez desvalidado, os valores poderão se alterar ao editar informações e/ou ao [Atualizar os dados](/doc/fechamento-Fmnwd0rJ77).