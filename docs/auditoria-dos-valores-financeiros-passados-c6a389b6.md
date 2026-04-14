<!-- title: Auditoria dos valores financeiros passados | url: https://outline.seazone.com.br/doc/auditoria-dos-valores-financeiros-passados-zHwQjqVfNb | area: Tecnologia -->

# Auditoria dos valores financeiros passados

Foi criado uma tabela e um endpoint onde é possível obter um CSV com as informações para verificar alterações em dados financeiros passados de fechamentos que já foram validados.

As informações para auditoria ficam salvas na tabela `financial_property_financial_audit` mas é possível obter um CSV com as informações. Para isso é preciso seguir as instruções no [Pull Request #1232](https://github.com/Khanto-Tecnologia/sapron-pms-web/pull/1232)

É salvo na tabela um registro sempre que algum fechamento de algum imóvel em um mês anterior ao atual sofre alguma alteração em seus valores financeiros.

É registrado o imóvel, data/hora do evento, data de referência do fechamento e os dados financeiros (valor antigo e novo).