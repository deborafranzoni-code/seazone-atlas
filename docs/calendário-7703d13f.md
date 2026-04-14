<!-- title: Calendário | url: https://outline.seazone.com.br/doc/calendario-BK9dV5w30P | area: Tecnologia -->

# Calendário

**Objetivo:**

Implementar o **Calendário do Proprietário** para visualização, gerenciamento de bloqueios e controle de disponibilidades de imóveis.


---

### Requisitos Funcionais:


1. **Escolha de Filtros**:
   * O proprietário deve selecionar **mês** e **imóvel** para visualizar o calendário.
2. **Realização de Bloqueios**:
   * Permitir que o proprietário insira bloqueios no calendário, desde que:
     * O imóvel esteja disponível nas datas selecionadas.
     * A disponibilidade leve em consideração o **tempo de preparo**, quando aplicável.
3. **Desbloqueio de Bloqueios**:
   * O proprietário pode realizar o desbloqueio, mas apenas para bloqueios que foram **criados pelo próprio proprietário**.
   * **Bloqueios que Não Podem Ser Desbloqueados pelo Proprietário**:
     * Bloqueios de **anfitrião**.
     * Bloqueios de **manutenção**.


---

### Regras de Negócio:


1. **Tempo de Preparo e Bloqueios**:
   * Caso exista uma reserva que possui tempo de preparo, então ao inserir um bloqueio não é necessário inserir um tempo de preparo de in ou de out
   * **Tipos de Bloqueio que Não Exigem Tempo de Preparo**:
     * **Manutenção**: Não exige tempo de preparo.
     * **Limpeza**: Não exige tempo de preparo.
     * **Anfitrião**: Não exige tempo de preparo.
2. **Dias de Preparo**:
   * **Sobreposição**:
     * Bloqueios com tempo de preparo se sobrepõem automaticamente, garantindo que **check-ins e check-outs** possam ocorrer caso já existam bloqueios cobrindo as mesmas datas.
   * **Imóveis sem Dias de Preparo**:
     * Para imóveis com **0 dias de preparo**, é permitido finalizar uma reserva e iniciar outra no mesmo dia.