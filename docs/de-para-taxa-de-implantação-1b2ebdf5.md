<!-- title: De / Para – Taxa de Implantação | url: https://outline.seazone.com.br/doc/de-para-taxa-de-implantacao-hC8BMamGjI | area: Tecnologia -->

# De / Para – Taxa de Implantação

### **Cenário 1 — À vista**

**Pipedrive**

* A vista no valor de 999

**Sapron**

* `implantation_fee_total_value`: **999**
* `implantation_fee_entrance_value`: **999**
* `entrance_payment_method`: **pix**
* `payment_installments`: **null**
* `payment_method`: **null**


---

### **Cenário 2 — Parcelado (3x)**

**Pipedrive**

* 3 parcelas com total de 1499

**Sapron**

* `implantation_fee_total_value`: **1499**
* `implantation_fee_entrance_value`: **0**
* `entrance_payment_method`: **null**
* `payment_installments`: **3**
* `payment_method`: **pix**


---

### Cenário 3 - Entrada + abatimento

**Pipedrive**

* Entrada de 399 + abatimento fechamento com total de 999 

**Sapron** 

* `implantation_fee_total_value`: **999**
* `implantation_fee_entrance_value`: **399**
* `entrance_payment_method`: **pix**
* `payment_installments`: **null**
* `payment_method`: **discount_rate**


Novo campo no pipedrive:

46821f8f881ac569b42a0e5c14c7ff20eddbcbac