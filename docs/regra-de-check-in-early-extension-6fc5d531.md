<!-- title: Regra de Check-in Early Extension | url: https://outline.seazone.com.br/doc/regra-de-check-in-early-extension-eMleNpootX | area: Tecnologia -->

# Regra de Check-in Early Extension

---

### Regras de Comportamento — Early Extension

Uma reserva pode receber uma **early extension**, permitindo que o hóspede **antecipe a data de check-in** em relação à reserva original. Nesse caso, as regras de negócio definem os seguintes comportamentos:

#### **Tela de Controle — Card de Check-in**

O card de check-in deve aparecer **na data mais próxima de entrada**, considerando tanto a reserva original quanto a extensão.

**Exemplo:**\nSe a reserva original ("reserva mãe") é de **31/10 a 10/11**, e o hóspede adquire uma early extension para **30/10**, o card deve ser exibido a partir do **dia 30/10**, que é a nova data de início da estadia.

Entretanto, as **informações do card devem permanecer vinculadas à reserva mãe**, ou seja, o **código da reserva exibido deve ser o da reserva original**, e não o da extensão.

#### **Pré-Check-in**

Para acessar o formulário de pré-check-in, o hóspede deve inserir o **código da reserva original**.\nO código gerado pela Stays para a extensão **não deve ser considerado**.

No entanto, ao entrar no formulário, as **datas apresentadas devem refletir o início atualizado da hospedagem**, já considerando o adiantamento da early extension.

Dessa forma, o sistema deve **tratar a reserva original e a extensão como uma única reserva contínua**, unificando as informações e datas de ambas.