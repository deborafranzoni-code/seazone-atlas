<!-- title: Fechamento - Sapron | url: https://outline.seazone.com.br/doc/fechamento-sapron-1etzx2C0VN | area: Tecnologia -->

# 🧮 Fechamento - Sapron

# **==Anfitrião==**

## Taxa de limpeza\n\n**Associação da Taxa de Limpeza à Reserva**

* Os valores de Taxa de Limpeza estão sempre vinculados à **reserva correspondente** na Stays, e isso não poderá ser alterado no Sapron.
* Em caso de necessidade de alterar a reserva na qual a taxa de limpeza deve ser associada, o ajuste deve ser feito na Stays para então ser sincronizada no Sapron.


**Espelhamento no Sapron**

* O Sapron refletirá os dados de limpeza registrados na Stays, seguindo as seguintes regras:
* **Caso 1:** Se na Stays o valor da taxa de limpeza estiver associado à reserva principal, ele aparecerá na reserva principal no Sapron e será exibido no Fechamento na data de checkout da reserva principal.
* **Caso 2:** Se na Stays houver mais de um valor de taxa de limpeza (por exemplo, uma taxa para a reserva original e outra para uma extensão), ambos os valores serão contabilizados separadamente na data de checkout de cada reserva.
* **Caso 3:** Se na Stays o valor da taxa de limpeza estiver associado somente à extensão, ele será exibido apenas na data de checkout da extensão correspondente no Sapron.

**Fluxo de troca de anfitrião no Sapron**

* A troca de anfitrião deve ser realizada na tela *editar dados >> mudança de anfitrião*. Selecione Imóvel, novo anfitrião e Data de alteração.

**Regras de negócio**

* Não é possível realizar troca de anfitriões em uma data que ocorre no meio de uma reserva.
* Caso haja troca de anfitrião em um imóvel com um out de uma reserva e um in de outra reserva no mesmo dia, comissão e taxa de limpeza do out é contabilizada para o anfitrião antigo e comissão e taxa de limpea do in é contabilizada para o novo anfitrião.

**Efetivação da troca nas tabelas**

* Uma vez que há uma *data de entrega de chaves* agendada, esta será efetivada **apenas** na data prevista.
* A query de troca roda todos os dias às 23h, efetivando as trocas agendadas para o dia corrente.
* Após rodar a query o novo anfitrião é alterado nas tabelas Property_Property e Reservation_reservation; garantindo que todas as reservas com check-in igual ou maior a data de entrega das chaves passem a ser de responsabilidade do novo anfitrião.


Para detalhes técnicos e acesse a documentação: [Migração de anfitrião](https://outline.seazone.com.br/doc/migracao-de-anfitriao-2g0Ku8WDAe)

## Migração de anfitrião

**Fluxo de troca de anfitrião no Sapron**

* A troca de anfitrião deve ser realizada na tela *editar dados >> mudança de anfitrião*. Selecione Imóvel, novo anfitrião e Data de alteração.

**Regras de negócio**

* Não é possível realizar troca de anfitriões em uma data que ocorre no meio de uma reserva.
* Caso haja troca de anfitrião em um imóvel com um out de uma reserva e um in de outra reserva no mesmo dia, comissão e taxa de limpeza do out é contabilizada para o anfitrião antigo e comissão e taxa de limpea do in é contabilizada para o novo anfitrião.

**Efetivação da troca nas tabelas**

* Uma vez que há uma *data de entrega de chaves* agendada, esta será efetivada **apenas** na data prevista.
* A query de troca roda todos os dias às 23h, efetivando as trocas agendadas para o dia corrente.
* Após rodar a query o novo anfitrião é alterado nas tabelas Property_Property e Reservation_reservation; garantindo que todas as reservas com check-in igual ou maior a data de entrega das chaves passem a ser de responsabilidade do novo anfitrião.


Para detalhes técnicos e acesse a documentação: [Migração de anfitrião](https://outline.seazone.com.br/doc/migracao-de-anfitriao-2g0Ku8WDAe)

## Taxa de Franquia

**Instruções para registro de Taxas de Franquia**

* Os valores referentes às taxas de franquia cobradas, pagas (via PIX), descontos concedidos ou dívidas perdoadas deverão ser registrados mensalmente utilizando [esta planilha](https://docs.google.com/spreadsheets/d/1AhZo2AmzXjJLSbRfHDsqv8qT1i99IZXmzaLFYEuE_7U/edit?gid=1805712756#gid=1805712756) template.

**Preenchimento da Planilha Template**

* Na primeira linha do template, há comentários detalhando como preencher cada coluna. **Atente-se** às instruções de formato e valores especificados.

**Registro dos Valores**

* Após o preenchimento correto da planilha, os dados serão utilizados para povoar o banco de dados por meio de uma query. Essa operação irá atualizar a tabela: [Financial Host Franchise Fee Payment](https://metabase.sapron.com.br/question#eyJkYXRhc2V0X3F1ZXJ5Ijp7ImRhdGFiYXNlIjoyLCJ0eXBlIjoicXVlcnkiLCJxdWVyeSI6eyJzb3VyY2UtdGFibGUiOjIzOX19LCJkaXNwbGF5IjoidGFibGUiLCJ2aXN1YWxpemF0aW9uX3NldHRpbmdzIjp7fX0=)

**Tabela Financial Host Franchise Fee Payment**

* Esta tabela contém **todos os valores** de taxas de franquia cobradas, **inclusive retroativos.**
* Os métodos de pagamento podem ser filtrados na coluna Payment Method.

**Métodos de Pagamento Disponíveis**

* **debit**: Pagamento via PIX. Utilize este método para valores que não são abatidos da comissão do anfitrião.
* **discount**: Dívidas perdoadas ou descontos concedidos. Use este método para registrar valores que foram perdoados ou oferecidos como desconto.
* **commission_abatement**: Abatimento da taxa de franquia na comissão. Este método deve ser utilizado para valores cobrados no mês e abatidos diretamente da comissão do anfitrião.

# Proprietário

## Troca de Proprietário

**Fluxo de troca de proprietário no Sapron**

* **Inativar o imóvel vendido:** Em <https://sapron.com.br/inserirdados/mudar-status-imovel>, mudar o status do imóvel desejado para "Inativo";
* **Cadastrar o imóvel com mesmo código destinado ao novo proprietário:** Em <https://sapron.com.br/onboarding>, cadastrar o proprietário (opcional) e o imóvel com o mesmo código;
* **Ativar o imóvel do novo proprietário:** Em <https://sapron.com.br/inserirdados/mudar-status-imovel>, quando o Onboarding for concluído, mudar o status do novo imóvel para "Ativo" com a data onde a migração das reservas deve iniciar. Nesta etapa deve-se garantir que a data de início de contrato é *igual* a data de ativação do imóvel.

**Regras de negócio**

* Não é possível trocar um proprietário durante uma reserva ativa
* A data de ativação do novo imóvel é o indicativo de quando as reservas devem migrar. Reservas com data igual ou maior a data de início de contrato são migradas para o novo proprietário.
* A data de ativação do imóvel deve ser igual a data de início de contrato.
* A data de inativação do antigo imóvel não pode ser maior que a data de ativação do novo imóvel && data de início de contrato do novo imóvel.

**Efetivação da troca nas tabelas**

* Uma vez que um imóvel foi ativado e outro com o mesmo código foi inativado, as reservas migram de um imóvel para outro após 6 horas realizada a ação.
* Verifica-se na Reservation_reservation reservas com check-in igual ou maior a data de ativação do novo imóvel e a coluna Property_id é populada com novo imóvel ao qual pertence a reserva
* Mantemos o registro no banco de dados do imóvel antigo e do imóvel novo, de forma que teremos dois ids para o mesmo código do imóvel.

Para detalhes técnicos e acesse a documentação: [Migração de reservas na Troca de Propritários](https://outline.seazone.com.br/doc/migracao-de-reservas-na-troca-de-proprietarios-LREa34Xflm/insights)

## Troca de comissão do imóvel & anfitrião

**Fluxo de troca de comissões no Sapron**

* **Trocar a comissão do imóvel e/ou Anfitrião:** Em https://sapron.com.br/editardados/propriedade, insira a nova comissão do imóvel e/ou anfitrião e selecione a Data de efetivação.
* **Confirme a data de troca e novos valores:** Após inserir os novos valores, clique em "salvar". Verifique os valores e data de troca inseridos no modal de confirmação.


**Regras de negócio**

* Não é possível realizar trocas de comissão do passado;
* A nova comissão é aplicada *apenas* para reservas com check-in igual ou maior a data selecionada. Isso indica que uma reserva não poderá ter valores diferentes de comissão, ou seja, se na data do check in a comissão é um valor X, esse valor será obrigatoriamente o mesmo até o dia do check out.
* A alteração da comissão é efetivada nas tabelas Reservation_Reservation e Property_Property e Property Audit *apenas* na data de troca. Se a data de troca for a data corrente, as tabelas correlatas são atualizadas logo após salvar os dados.


**Efetivação da troca nas tabelas**

* Uma vez que houve troca de comissão (imóvel ou anfitrião) os dados ficam salvos na tabela Property Comission Time in Property.
* Se a data de efetivação da troca de comissão for para o dia corrente, as comissões são alteradas nas tabelas Property Property, Property Audit e efetivadas nas reservas ativas da Reservation Reservation.
* Caso data de efetivação das comissões for para datas futuras (agendada) a comissão é salva inicialmente na Property Comission Time in Property e no dia de efetivação ela é alterada nas tabelas correlatas (Property Property, Property Audit e efetivadas nas reservas ativas da Reservation Reservation)

# Tratamento de extensões Airbnb

**Alterações Implementadas**

**Unificação das Extensões**

* Extensões realizadas diretamente no Airbnb não serão mais separadas na tabela Reservation reservation.
* Todas as informações da reserva original e suas extensões permanecerão no mesmo ID da tabela Reservation Reservation


**Espelhamento com Stays**

* As extensões serão tratadas como um espelho da Stays, garantindo que reservas e suas alterações fiquem em um único id na tabela de referência.


**Exceções**

* Quando uma reserva é criada originalmente via Airbnb e a extensão é realizada via Stays, então extensão continuará sendo tratada como um registro separado.