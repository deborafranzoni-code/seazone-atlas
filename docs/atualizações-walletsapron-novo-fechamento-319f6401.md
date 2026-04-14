<!-- title: Atualizações Wallet/Sapron - Novo Fechamento | url: https://outline.seazone.com.br/doc/atualizacoes-walletsapron-novo-fechamento-OT5cyNCOEs | area: Tecnologia -->

# Atualizações Wallet/Sapron - Novo Fechamento

## **Atualizações – Wallet**

Com a alteração no modelo de pagamento, que agora considera o fechamento de reservas por diárias, será necessário realizar as seguintes atualizações na Wallet para adequação às novas regras:

#### **Home**

No **Grid Financeiro**, as seguintes mudanças devem ser aplicadas:

* Atualização dos campos:
  * **Diárias Executadas** → **Reservas Executadas**
  * **Diárias Acumuladas** → **Reservas Acumuladas**
* Substituição do termo **"Diária"** por **"Reserva"** para melhorar o entendimento do proprietário.
* Garantir que reservas que atravessam mais de um mês sejam contabilizadas a partir do `cash_date` e apenas no mês em que forem finalizadas, considerando que a visualização do grid financeiro é mensal.

#### **Extrato Detalhado**

**Receitas**

* Atualizar o campo **Diárias Executadas** para **Reservas Executadas**.
* Garantir que a reserva apareça como receita **somente no mês em que for finalizada**.

**Descontos**

* Atualmente, os valores de comissão para reservas que se estendem por mais de um mês são descontados proporcionalmente a cada dia da reserva dentro de cada mês.
* A partir da mudança, o desconto da comissão deve ser aplicado **integralmente no mês em que a reserva for finalizada**.
  * OBS: caso a reserva tenha mais de 30 dias de duração, ela será quebrada a cada 30 dias para fins de fechamento. Ex: se uma reserva possui 35 dias, ela será dividida em uma reserva de 30 dias e outra de 5 dias para fins de fechamento.
  * O pagamento das OTAs Booking e Decolar são feitas sempre no mês seguinte após o checkout.

**Tooltips** 

* Realizar ajuste de diárias → reservas em todas as tooltips da plataforma

==As alterações serão feitas de forma que após a alteração do fechamento realizaremos as trocas de nomenclatura e lógica de pagamento, porém os meses anteriores a subida da mudança manterão o comportamento que já existe hoje.== 


## **Atualizações – Sapron HOST**

Com as mudanças no modelo de pagamento das reservas no novo fechamento, as seguintes atualizações devem ser aplicadas na visualização do **Host**:

#### **Dashboard Financeiro**

* Atualmente, a divisão de pagamento é feita com base no mês em que a diária ocorreu. Com a mudança, deve-se garantir que reservas que atravessam mais de um mês sejam contabilizadas **a partir do cash_date** e **apenas no mês em que forem finalizadas**.
* Atualizar a nomenclatura dos seguintes campos para alinhar a comunicação:
  * **Diárias Executadas** → **Reservas Executadas**
  * **Diárias Pagas** → **Reservas Pagas**

#### **Contagem de Diárias e Limpeza**

* Garantir que a contagem esteja considerando **o total de reservas realizadas**, e não apenas o registro da reserva.
* Após a mudança, a reserva passará a ter **apenas um registro** na **Closing Property Resume**.