<!-- title: Migrar Reservas via Sapron | url: https://outline.seazone.com.br/doc/migrar-reservas-via-sapron-WQSqy7m5Ei | area: Tecnologia -->

# Migrar Reservas via Sapron

Uma forma de Migrar reservas manualmente é seguindo essa documentação [aqui](https://outline.seazone.com.br/doc/reservas-migrar-reservas-de-imovel-x-para-y-ynOAwq8AV4)

Outra forma de migrar é via sapron, precisar verificar algumas informações: 



1. Primeiro precisa verificar as datas de ativação e inativação dos imoveis com o codigo solicitado no suporte, pois pode ter um ou mais imoveis com diferentes status com o mesmo código.


Usando esse metabase - <https://metabase.seazone.com.br/question/1082-property-by-code>


Tendo como exemplo o imovel: JBV157, ele tem 2 registros

 ![](/api/attachments.redirect?id=740b7f3e-cf49-4cc4-a3f2-82122387866d " =822x149")



2. Pesquisar as reservas que tem com esse codigo de imovel, usar esse metabase aqui <https://metabase.seazone.com.br/question/1171-reservation-by-property-code>

Você vai ver que o propertyID 6161 tem reservas com checkIn desde 04-03-26, isso porque a data de Ativação do PropertyID é dia 02-03-2026, assim todas as reservas depois do 02-03 serão desse imovel.


 ![](/api/attachments.redirect?id=350dd758-1955-4ab0-904a-c5fe61629b47 " =1094x502")



3. Procurar a reserva que quer ser migrada pelo codigo STAYS: Ex. HC199J

A reserva não pode migrar pois a data de ativação dessde propertyID é 02-03 e o checkin da reserva é 01-03

 ![](/api/attachments.redirect?id=82d40191-9358-40be-a7d6-3283ec57c20b " =1343x559")


Nesses casos, precisa pedir para o pessoal definir uma nova data de ativação do propertyID 6161, teria que ser ativada o dia 01-03-2026, para a reserva migrar.



4. Se estiver dentro do periodo, pode Importar novamente a reserva via: 

Sapron > Financeiro> Painel Gerenciamento > Importar reservas pelo codigo STAYS


## **Regra de Migração de Reservas quando tem Troca de Propietario**

### **Processo Automático via Sapron**

A migração de reservas acontece **automaticamente** quando há troca de proprietário. O Sapron considera **dois fatores principais** para realizar essa migração:

* **Data de início de contrato do propertyID do novo proprietário**
* **Data de ativação do imóvel do propertyID do novo proprietário**

## **Fluxo Operacional**

O processo ideal segue esta sequência 


1. Escolher **"Uma Data X" de Troca de Proprietário** considerando o seguinte:

   
   1. A "data x" será usada para migrar as reservas (com data de checkIn) maior ou igual a "data x"
   2. A "data x" não pode ser no meio de uma reserva

      
      1. Ex. se é definido a data de troca no dia 13/03/26, todas as reservas que tenham checkIn a partir de 13-03-26 serão migradas, reservas anteriores a essa data não serão migradas.
2. O propertyID_antigo é inativado na **"Data X"**
3. O propertyID_novo é ativado na "**Data X**"
4. As reservas são **migradas automaticamente** considerando a "Data x"

   \
5. \
6. \
   \

**Migração Automática de Reservas: Troca de Proprietário (Sapron)**

O Sapron migra as reservas automaticamente com base na **Data de Corte**, a data de corte deve coincidir com o **início do novo contrato e a ativação do novo PropertyID**.

**Regras Principais:**

* **Critério:** Migram apenas reservas com check-in **igual ou posterior** à **Data de Corte.**
* **Restrição:** A Data de Corte não pode ocorrer durante uma reserva em andamento.

**Fluxo Operacional:**


1. Definir a **Data de Corte**.
2. Inativar o PropertyID antigo e ativar o novo PropertyID na **Data de Corte**.
3. O sistema realiza a migração automática das reservas considerando a Data de Corte.