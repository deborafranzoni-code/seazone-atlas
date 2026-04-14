<!-- title: Bloqueios de Último Minuto | url: https://outline.seazone.com.br/doc/bloqueios-de-ultimo-minuto-WbIa5VgBd5 | area: Tecnologia -->

# Bloqueios de Último Minuto

# O que é um bloqueio de último minuto?

Normalmente , um bloqueio de último minuto irá utilizar uma lógica para bloquear uma data caso o dia anterior esteja ocupado. Ele se chama bloqueio de último minuto porque a data bloqueada normalmente será hoje ou no máximo amanha. Isso é necessário porque se uma reserva for criada muito em cima da hora, fica difícil para realizar a limpeza e preparar o imóvel para receber outro hospede, então alguns hotéis possuem regras especificas que não permitem reservas muito em cima da hora.

A ideia do bloqueio é rodar um script por num serviço da AWS, normalmente eles rodam na madrugada ou um dia antes da data alvo, e caso ele detectem que antes da data alvo existe uma reserva, mas a data alvo não está ocupada, então é gerado um bloqueio nessa data alvo.

Aqui embaixo está um pequeno exemplo observado na Stays. O script rodou no dia 26/04 as 20:00 horas, sendo que a data alvo era o dia 27/04, como o dia antes da data alvo está ocupado, mas a data alvo estava livre, foi gerado um bloqueio de último minuto nesse imóvel na data 27/04.

 ![Untitled](Bloqueios%20de%20U%CC%81ltimo%20Minuto%205a11b639dc0e46668072b11857cdbc9e/Untitled.png)

 ![Untitled](Bloqueios%20de%20U%CC%81ltimo%20Minuto%205a11b639dc0e46668072b11857cdbc9e/Untitled%201.png)

# Quais são as regras?

**ILC**: Atualmente, existe apenas uma regra para os ILC.

* Apartamento com **check out previsto para amanhã**, só serão aceitos check in para amanhã **até hoje as 20h00** horário de brasília.

**JBV**: Atualmente, existem duas regras para os JBV.

* Apartamento com c**heck out previsto para hoje**, só serão aceitos check in para hoje **até hoje as 11h00** horário de brasília.
* Apartamento **sem ocupação ontem**, só serão aceitos check in para hoje **até hoje as 19h00** horário de brasília.

# Infraestrutura na AWS

Github: <https://github.com/Khanto-Tecnologia/api-stays>

O script se encontra no repositorio API-Stays, na pasta patch/last_minute_block. Ele é um lambda que é triggado por regras do EventBridge. Como existem 3 regras de hotel, também existem 3 regras do EventBridge e cada uma passa um parâmetro especifico que determina qual regra de hotel aplicar. Lembrando que hoje existem 1 regra pros ILCs e 2 pro JBVs.

O lambda recebe de parâmetro rule_condition, que pode ser JBV_1, JBV_2 ou ILC_1. Abaixo se encontra a função logic_to_block que descreve o que cada regra faz. Essa função é aplicada para todos os imóveis do grupo (JBVs ou ILCs). Em resumo, ela faz uma validação se será necessário bloquear a data e, caso seja, é retornado qual data que deve ser bloqueada.

```python
def logic_to_block(listing, rule_condition):
    if rule_condition == 'JBV_1':
        is_to_block = (is_checkout_booked(listing, today) or is_checkout_blocked(listing, today)) and not(
                        is_checkin_booked(listing, today) or is_checkin_blocked(listing, today))
        block_date = today
    elif rule_condition == 'JBV_2':
        is_to_block = not (is_date_occupied(listing, yesterday) or is_date_blocked(listing, yesterday)) and not(
                            is_checkin_booked(listing, today) or is_checkin_blocked(listing, today))
        block_date = today
    elif rule_condition == 'ILC_1':
        is_to_block = (is_checkout_booked(listing, tomorrow) or is_checkout_blocked(listing, tomorrow)) and not(
                        is_checkin_booked(listing, tomorrow) or  is_checkin_blocked(listing, tomorrow))
        block_date = tomorrow
    return is_to_block, block_date
```

É importante comentar que, **para uma data ser considerada "ocupada" nas regras de hotel, ela pode ser reservada ou bloquada**, é por isso que no script acima, em todas as condições, é verificado se a data está ocupada ou bloquada. **Entretanto, a única exceção a isso são os bloqueios gerados pelo próprio bloqueio de último minute**. Eles não são considerados uma ocupação na lógica dos bloqueios de último minuto e é por isso que as funções is_checkout_blocked, is_checkin_blocked ou is_date_blocked fazem a verificação abaixo (INTERNAL_NOTE é a observação default que esses bloqueios geram):

```python
if listing.json()[0]["internalNote"] in [INTERNAL_NOTE]:
	return False
```