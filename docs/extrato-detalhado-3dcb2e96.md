<!-- title: Extrato Detalhado | url: https://outline.seazone.com.br/doc/extrato-detalhado-eJIJ2etA6B | area: Tecnologia -->

# Extrato Detalhado

## Receitas 

**Objetivo:**

Implementar a listagem de **movimentações financeiras positivas** associadas ao proprietário.

**Regras de Negócio:**


1. **Tipos de Movimentações**: A listagem deve incluir as seguintes movimentações positivas:
   * **Repasse**: Valores enviados ao proprietário.
   * **Diárias Executadas e Pagas no Mês Vigente**: Referentes às reservas concluídas e pagas no mês atual.
   * **Diárias Executadas no Mês Anterior e Pagas no Mês Atual**: Reservas realizadas no mês anterior com pagamento efetuado no mês vigente.
   * **Ajuste de Reserva (Positivo)**: Ajustes relacionados a reservas que resultem em crédito.
   * **Ajuste Manual (Positivo)**: Ajustes manuais inseridos com valor positivo.
2. **Nota Fiscal**:
   * Movimentações do tipo **Repasse** e **Ajuste Manual** podem conter uma Nota Fiscal associada.
   * Caso uma Nota Fiscal esteja disponível, abaixo do valor da movimentação deve ser exibido um link 
   * O link deve redirecionar o usuário diretamente ao arquivo 

### Requisitos de Implementação:


1. **Ordenação e Exibição**:
   * As movimentações devem ser ordenadas cronologicamente, com as mais recentes exibidas no topo.
2. **Formato da Listagem**:

* Diárias: data de vigência da hospedagem 
* Ajustes: data da realização do ajuste 

## Descontos

**Objetivo:**

Implementar a listagem das **movimentações financeiras de descontos** associados ao proprietário.

### Regras de Negócio:


1. **Tipos de Movimentações**: A listagem deve incluir os seguintes descontos:
   * **Comissão Paga**:
     * Indicar o **imóvel** ao qual a comissão se refere.
   * **Despesas**:
     * Incluir um **link para a Nota Fiscal (NF)** associada à movimentação.
   * **Ajuste Manual (Negativo)**:
     * Caso exista uma Nota Fiscal, exibir um **link para a NF** associado à movimentação.
   * **Ajuste de Reserva (Negativo)**:
     * Caso exista um documento relacionado, exibir um **link para o documento** associado.