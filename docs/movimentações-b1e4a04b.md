<!-- title: Movimentações | url: https://outline.seazone.com.br/doc/movimentacoes-Xh9BcfZpsw | area: Tecnologia -->

# Movimentações

### **Objetivo:**

Definir o **mapeamento (de/para)** das movimentações registradas em nossos bancos de dados e a forma como essas informações devem ser traduzidas e exibidas no **WALLET do proprietário**.


---

### Mapeamento de Movimentações:

| **Wallet** | **Descrição** | **Coluna** |
|----|----|----|
| **DESPESAS** | Despesas associadas às propriedades gerenciadas pela Seazone. | **expenses** |
| **TAXA DE IMPLANTAÇÃO** | Registro de valor de saída referente à taxa de implantação de um imóvel. | **implantation_fee** |
| **AJUSTE MANUAL** | Registro de um ajuste manual, que pode ser uma entrada ou saída. | **manual_fit** |
| **AJUSTE DE RESERVA** | Registro de um ajuste manual relacionado a uma reserva, que pode ser entrada ou saída. | **reservation_manual_fit** |
| **DIÁRIAS** | Registro de valor de entrada referente aos ganhos de diárias em uma reserva. | **revenue** |
| **COMISSÃO** | Registro de valor de entrada referente à comissão da Seazone. | **seazone_commission + host_commission** |
| **REPASSE** | Registro de valor de saída referente ao repasse mensal feito ao proprietário. | **ted** |


---

### Considerações Importantes:


1. **Distinção de Entradas e Saídas**:
   * Ajustes manuais (**manual_fit**) e ajustes relacionados a reservas (**reservation_manual_fit**) podem ser tanto entradas quanto saídas. Essa distinção deve ser mantida e exibida no Wallet.