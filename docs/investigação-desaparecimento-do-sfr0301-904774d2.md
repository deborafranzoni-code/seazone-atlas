<!-- title: Investigação: Desaparecimento do SFR0301 | url: https://outline.seazone.com.br/doc/investigacao-desaparecimento-do-sfr0301-xH8FdVGava | area: Tecnologia -->

# Investigação: Desaparecimento do SFR0301

O imóvel não aparece apenas no link curto, mas é acessível via pesquisa, ou seja, está sendo anunciado corretamente. <https://seazone.com.br/acomodacoes/apto-c-churrasq-privativa-a-180m-do-mar-sfr0301/5469/2026-01-02;2026-01-09/adults=1;kids=0;babies=0?ignore_min_stay=true>

# Porque isso acontece?

Basicamente porque o imóvel não tem disponibilidade em datas próximas.

O processo de busca com link curto não permite a gente selecionar datas, visto que seu formato é **[seazone.com.br/s/codigo-do-imovel](http://seazone.com.br/s/codigo-do-imovel)**, sendo assim, o que ele faz é buscar por datas disponíveis mais próximas (`_closest_available_dates`). Cada imóvel do site tem registrado essas datas e existem algumas regras sobre elas.

## Lógica por trás das datas próximas disponíveis

Basicamente, na hora de atribuir essas "datas disponíveis mais próximas" o sistema procura por 3, 4 ou 5 dias **consecutivos** que estejam **disponíveis** e que **respeitem o min_stay.** Existe também uma ordem de precedência do maior período para o menor, ou seja, se encontrar 5 datas, retorna as 5, se encontrar 4, retorna as 4 e assim por diante, caso nada seja econtrado, nada é retornado.

```javascript
@staticmethod
def _get_closest_available_dates(availability_metadata: dict[str, Any]) -> list[str]:
    start_date = datetime.datetime.now().date() + datetime.timedelta(1)
    end_date = start_date + datetime.timedelta(180)

    dates_3_days = []
    dates_4_days = []
    dates_5_days = []
    availability_count = 0
    while start_date < end_date:
        date_str = start_date.isoformat()
        is_avail = (
            availability_metadata.get(
                f"{date_str}_avail",
            )
            == 1
        )

        min_stay = availability_metadata.get(f"{date_str}_min_stay", 0)

        if is_avail:
            availability_count += 1
            if len(dates_3_days) < 3 and availability_count <= 3:
                if min_stay <= 3:
                    dates_3_days.append(date_str)

            if len(dates_4_days) < 4 and availability_count <= 4:
                if min_stay <= 4:
                    dates_4_days.append(date_str)

            if len(dates_5_days) < 5 and availability_count <= 5:
                if min_stay <= 5:
                    dates_5_days.append(date_str)

            if availability_count == 5:
                break

        else:
            availability_count = 0
            if dates_5_days and len(dates_5_days) < 5:
                dates_5_days = []
            if dates_4_days and len(dates_4_days) < 4:
                dates_4_days = []
            if dates_3_days and len(dates_3_days) < 3:
                dates_3_days = []

        start_date += datetime.timedelta(1)

    if len(dates_5_days) == 5:
        return dates_5_days
    if len(dates_4_days) == 4:
        return dates_4_days
    if len(dates_3_days) == 3:
        return dates_3_days

    return []
```

## Olhando para o calendário do imóvel

A contagem começa no dia de amanhã, ou seja, se hoje é 04/12/2025, na hora de procurar as datas próximas disponíveis estaremos começando de 05/12/25. Sabendo disso, podemos olhar o calendário do SFR0301 para entender algumas coisas.

### 05/12 - 06/12

 ![](/api/attachments.redirect?id=b5d8276e-c899-494d-b613-f381000ca856 " =707x451")

Não é considerando uma data próxima disponível porque a disponibilidade mínima é de 3 dias consecutivos.

### 13/12 - 14/12

 ![](/api/attachments.redirect?id=8850d5eb-e4dc-46cb-8cf6-0fd8e7c07c69 " =707x451")

Não é considerando uma data próxima disponível porque a disponibilidade mínima é de 3 dias consecutivos.

### A partir do dia 27/12/25 até 06/01/26

**A partir desse período** a estadia minima (`min_stay`) **passa a ser de 7 dias**. Isso faz com que nenhuma data seja considerada pois, na nossa busca por datas próximas disponíveis consideramos que o `min_stay` precisa ser menor ou igual a quantidade de dias consecutivos disponíveis, e, como vimos anteriormente, o máximo de dias consecutivos que consideramos é 5, e 7 nunca será menor ou igual a 5.

### E porque a partir do dia 07/01/2026 as datas próximas não aparecem?

A partir do dia 07/01 o `min_stay` passa a ser 1, mas o imóvel continua sem datas próximas disponíveis por causa da maneira como incrementamos o `availability_count`, ele está sendo incrementado mesmo quando os dias não obedecem o `min_stay`, ou seja, se ocorrerem 5 dias consecutivos com `avail = 1` (mesmo que nenhum tenha `min_stay <= 5`), `availability_count` atingirá 5 e o `if availability_count == 5: break` vai sair do loop **antes** de preencher qualquer lista. No final, todas as listas permanecem vazias e a função retorna `[]`.

# E agora?

## Forma mais simples de resolver

Podemos simplesmente passar a incrementar o `availability_count` somente quando os dias obedecem ao `min_stay`.

Isso resolve esse comportamento anterior:

* 5 dias consecutivos com `avail = 1`
* **mas todos com min_stay > 5**
* contador chegava em 5
* função dava `break`
* mas nenhuma lista tinha dados válidos
* resultado: `[]`

Dessa forma, após esse ajuste, o dia 07/01 em diante passaria a ser considerado um range de datas próximas disponíveis.

Resumindo, antes procurávamos por **dias consecutivos "disponíveis" mas não necessariamente reserváveis**, por conta do min_stays. Agora, com o ajuste, passamos a procurar por **dias consecutivos reserváveis sem restrição de min_stay**.

Com essa abordagem, o código ficaria assim:

```sql
@staticmethod
def _get_closest_available_dates(availability_metadata: dict[str, Any]) -> list[str]:
    start_date = datetime.datetime.now().date() + datetime.timedelta(1)
    availability_window = int(os.environ.get("AVAILABILITY_WINDOW"))
    end_date = start_date + datetime.timedelta(availability_window)

    dates_3_days = []
    dates_4_days = []
    dates_5_days = []
    availability_count = 0
    while start_date < end_date:
        date_str = start_date.isoformat()
        is_avail = (
            availability_metadata.get(
                f"{date_str}_avail",
            )
            == 1
        )

        min_stay = availability_metadata.get(f"{date_str}_min_stay", 0)

        if is_avail and min_stay <= 5:
            availability_count += 1
            if len(dates_3_days) < 3 and availability_count <= 3:
                if min_stay <= 3:
                    dates_3_days.append(date_str)

            if len(dates_4_days) < 4 and availability_count <= 4:
                if min_stay <= 4:
                    dates_4_days.append(date_str)

            if len(dates_5_days) < 5 and availability_count <= 5:
                if min_stay <= 5:
                    dates_5_days.append(date_str)

            if availability_count == 5:
                break

        else:
            availability_count = 0
            if dates_5_days and len(dates_5_days) < 5:
                dates_5_days = []
            if dates_4_days and len(dates_4_days) < 4:
                dates_4_days = []
            if dates_3_days and len(dates_3_days) < 3:
                dates_3_days = []

        start_date += datetime.timedelta(1)

    if len(dates_5_days) == 5:
        return dates_5_days
    if len(dates_4_days) == 4:
        return dates_4_days
    if len(dates_3_days) == 3:
        return dates_3_days

    return []
```

## Outros caminhos

Esse trecho de código tem muitas regras de negócio, como por exemplo, que o mínimo de dias consecutivos para obter datas próximas disponíveis é 3 e o máximo é 5. Talvez em algum momento, se quisermos, poderiámos repensar essa regra.