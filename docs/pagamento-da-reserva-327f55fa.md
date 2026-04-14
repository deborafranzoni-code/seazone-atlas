<!-- title: Pagamento da reserva | url: https://outline.seazone.com.br/doc/pagamento-da-reserva-tyIfeDleFr | area: Tecnologia -->

# Pagamento da reserva

## Pagar.me


---

Inicialmente vamos utilizar o **checkout**  do **pagar.me** para agilizar o desenvolvimento, possibilitando o pagamento com cartão de crédito parcelado até 12x ou à vista com o PIX\*\*.\*\*

* ***TO-DO Futuro***
  * Implementar checkout próprio A responsabilidade por ter que guardar dados do pagamento (cartão), será grande e teremos que investir tempo pra proteger bem esses dados e garantir que nada vai vazar. Vimos que teremos que seguir os padrões do **[PCI DSS](https://business.ebanx.com/en/resources/payments-explained/pci-dss-compliance)**. Pra oferecer pagamentos com 1-clique teriamos ainda mais trabalho (teremos que implementar tokenização dos dados do cartão)

[\*\*Documentação da API](https://github.com/Khanto-Tecnologia/seazone-reservas-api/blob/develop/docs/CHECKOUT.md) para integração com Front\*\*

* Após confirmar uma reserva e a mesma estiver no status **CONFIRMED**
* Fazer um POST para `/reservations/<RESERVATION_ID>/checkout` ([link swagger](https://api.staging.reservas.sapron.com.br/docs#/reservations/reservation_checkout_reservations__reservation_id__checkout_post))
  * Será retornada uma url do Pagarme para checkout.
  * Redirecionar o navegador para essa url.
  * Ao termino do checkout será redirecionado novamente para o site de reservas.

### Teste em ambiente de Staging/Desenvolvimento

Os testes em staging e desenvolvimento é realizado através de simulador de pagamento.

> *Simulador é um conjunto de regras do ambiente de testes da Pagar.me que utilizamos para simular diferentes situações que podem ocorrem em produção. A ideia é que possam testar os mais diversos cenários, afim de construir uma solução completa, sem deixar a segurança e praticidade de um ambiente de testes.* **Referência:** [https://docs.pagar.me/docs/o-que-é-um-simulador](https://docs.pagar.me/docs/o-que-%C3%A9-um-simulador)

[Simulador de Cartão de Crédito](https://docs.pagar.me/docs/simulador-de-cart%C3%A3o-de-cr%C3%A9dito)

[Simulador de PIX](https://docs.pagar.me/docs/simulador-pix)

[Simulador PSP](https://docs.pagar.me/docs/simulador-psp)

### **Como Funciona o Parcelamento?**

Cada opção de parcelamento está associado a um juros bancários correspondente a quantidade de vezes, aumentando progressivamente. Assim, foi implementado um correção no valor da reserva, aumentando seu valor bruto conforme a quantidade de parcelas selecionadas, ou seja: os juros excedentes são jogados para o cliente. Assim, para a Seazone toda reserva e deduções podem ser consideradas como uma reserva à vista.

Uma explicação mais analíticas das taxas e reajustes estão na planilha:


Dessa forma, após o pagamento e deduções das taxas bancárias executadas de forma automática (no momento da cobrança) pelo pagarme, sempre irá resultar no mesmo valor (chamado de valor líquido bancário/pagarme).

 ![Untitled](/api/attachments.redirect?id=7f1c9cb4-adee-4e7c-b2eb-55128a070313)

Para reservas vendidas diretamente no site (não considerando qualquer outra origem, por exemplo reservas feitas direto pelo atendimento na Stays), a taxa de OTA a ser considerada é de 15% sobre o valor líquido bancário. Sendo para qualquer opção de parcelamento, o lucro da OTA correspondente aos 15% de receitas MENOS o valor da taxa à vista (4% aproximadamente do bruto da reserva).

## Paypal


---

Inicialmente vamos utilizar o **checkout**  do **Paypal** para agilizar o desenvolvimento\*\*.\*\*

### Teste em ambiente de Staging/Desenvolvimento

Os testes em ambiente de Staging e Desenvolvimento podem ser realizados usando a conta de Sanbox do Paypal.

Para ter acesso à ela, é preciso acessar o a plataforma do Paypal no Dashboard de Desenvolvedor. Em seguida vá em: Testing Tools > Sandbox Accounts e use uma das contas para testar.

⚠️ Verifique se o toggle "Sanbox" está voltado para Sanbox e não Live.

## Envio do valor líquido da reserva para Stays


---

***Obs:*** *Aqui neste caso, quando falamos valor líquido significa que o valor das taxas do gateway subtraído do valor pago pelo hóspede (valor_pago - taxas).*

### **Por que estamos enviando o valor líquido para Stays?**

Fazemos isso para que o Sapron consiga calcular corretamente a divisão de valores para as respectivas partes.

### **Como isso é feito, qual a lógica para enviar o valor correto?**

É utilizado como base o valor presente no campo **effective_price** que é o valor efetivo que será cobrado do hóspede.

**Sabemos que:**

* Ao enviar o campo `_f_expected` value na API de reservas da Stays, ele altera **apenas o valor de diárias**, que não necessariamente será igual ao valor total.
* Caso tenha alguma cupom aplicado, o valor do cupom não irá se alterar
* Uma vez aplicado o cupom em uma reserva, o valor do cupom não se altera, portanto, o valor do cupom quando desconto por percentual, sempre é referente percentual do valor original da reserva.
* O valor do **cupom** é **subtraído** do valor da reserva na Stays
* O valor da **taxa de limpeza** é **somado** ao valor da reserva na Stays
* O Pagar.me retorna os **valores das taxas** que são descontadas por eles, do valor cobrado do hóspede

Sabendo disso, precisamos calcular corretamente o valor do `_f_expected` para que na Stays seja registrado o valor líquido da reserva que é exibido na cobrança, no Pagar.me. Para isso, chegamos na seguinte lógica:

* `nights_price`       = `total_price - cleaning_fee`
* `effective_price`  = `(nights_price - cupom_discount) + cleaning_fee`
* `net_value`            = `effective_price - gateway_fee`
* `_f_expected`:
  * Se **possui cupom**: `_f_expected`        = `net_value + cupom_discount - cleaning_fee`
  * Se **não possui cupom**: `_f_expected` = `net_value - cleaning_fee`

  *Somamos o cupom pois a Stays irá subtrair; Subtraímos a cleaning_fee pois a Stays irá somá-la; Essas duas coisas ocorrem no momento em que é enviado a requisição de alteração para a Stays, ela já calcula automaticamente. Basicamente, nossa lógica é somar o que é subtraído, e subtrair o que é somado, pela Stays no registro da reserva.*

<aside> ℹ️ `_f_expected`: Valor enviado para a Stays para substituir o valor de diárias da reserva.

`net_value`: Valor líquido Pagar.me

`effective_price`: Valor efetivo que será cobrado do hóspede

`cupom_discount`: Valor referente ao desconto aplicado pelo cupom. `diaras * cupom`

`gateway_fee`: Valor total das taxas cobradas pelo PagarMe. Ele é obtido através da cobrança que é gerada pelo pedido criado no Pagar.me referente a uma determinada reserva.

</aside>

### **Onde está o código?**

**Confirmação da reserva**


**Confirmação do Pagamento**