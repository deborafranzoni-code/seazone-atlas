<!-- title: Celery | url: https://outline.seazone.com.br/doc/celery-7qCwTKDKvb | area: Tecnologia -->

# Celery

---

> Documentação geral sobre o Celery (Como funciona e qual sua utilidade fora e dentro da empresa)

[Celery.docx](Celery%200b6fc799c5224583a0f4482aafaa9357/Celery.docx)

* **Conteúdo do docx**

  **Como funcionam as Tasks:**

  O celery é uma ferramenta que atua criando filas de tarefas. Seu principal objetivo é, executar de forma paralela ao programa principal, tarefas que muitas vezes podem ser custosas. Fazendo assim, com que não percamos tempo de processamento na operação demandada ao celery, e podendo recuperar o resultado dessa operação mais adiante.

  A fila de funcionamento do celery tem formato parecido com este:

  ![Untitled](/api/attachments.redirect?id=b60b3a88-9042-49d8-9242-211ca7cf889a)

  Onde as tasks são organizadas em filas pelo "Broker" e capturadas sequencialmente uma a uma pelos "workers". O resultado dessa tarefa pode ficar em espera ou ser armazenado em qualquer tipo de banco de dados.

  **Por que precisamos do Celery?**

  De forma geral o Celery proporciona vantagens principalmente no quesito da escalabilidade, visto que, ao delegar tarefas para um processamento paralelo não perdemos tempo de processo naquela função e podemos seguir com o código normalmente. Além disso, o Celery também é suportado por praticamente todos os Browsers modernos, facilitando a integração.

  Num contexto mais local, o Celery é usado no Sapron em algumas operações de interesse como por exemplo: enviar um email, uma mensagem no slack, ou realizar cálculos do financeiro.


---

## Exemplos explicados de tasks delegadas ao Celery no SAPRON

> Para encontrar onde estão as tasks no repositório do SAPRON basta procurar pelos arquivos "tasks.py" em algum módulo de interesse. Por exemplo, pelo caminho: backend → property → tasks.py É possível encontrar as tasks também, ao filtrar por: "@app.task" e "@shared_task"


---

> A task 'channel_manager.stays.handle_reservation' é ativa sempre que uma reserva é realizada sob um listing ainda inexistente. Quando isso acontece, paralelamente à todo script de reservas é ativa a classe 'stays_handle_reservation' que cria o listing esperado e aloca esta reserva a ele.

Interessante ressaltar que dentro desta classe existe uma outra task delegada ao celery a 'send_slack_message', que dispara a um canal de slack uma mensagem avisando que o listing em questão foi criado automaticamente

> \

```python
@shared_task(
    name='channel_manager.stays.handle_reservation',
    max_retries=2,
    default_retry_delay=5,
    autoretry_for=(Exception,),
    ignore_result=True,
)
def stays_handle_reservation(stays_reservation: Dict[str, Any]):
    with transaction.atomic():
        log.info("atualizando reserva stays: %s", stays_reservation)
        handler = factory.stays_handler()
        result = handler.handle(stays_reservation)

    if result.listing_created and result.sapron_reservation.listing.ota.name != "Blocking":
        send_slack_message.delay(
            channel_name="#ota-anuncios",
            text=(
                "Para inserir a reserva *{stays_reserv_code}*, "
                "o Sapron criou automaticamente o listing:\n"
                "- ID: *{listing_id}*\n"
                "- Imóvel: *{property_code}* \n"
                "- OTA: *{ota_name}*"
            ).format(
                stays_reserv_code=stays_reservation["id"],
                listing_id=result.sapron_reservation.listing.id,
                property_code=result.sapron_reservation.listing.property.code,
                ota_name=result.sapron_reservation.listing.ota.name,
            ),
            title="Criação de listing para inserção de reserva",
            fallback=(
                "O Sapron criou automaticamente o listing {property_code} - {ota_name} "
                "para inserção da reserva {stays_reserv_code}"
            ).format(
                stays_reserv_code=stays_reservation["id"],
                property_code=result.sapron_reservation.listing.property.code,
                ota_name=result.sapron_reservation.listing.ota.name,
            ),
        )
```

> A task 'channel_manager.stays.import_new_reservations' é delegada ao celery em um certo período de tempo ou quando acionada. Ela busca pela classe 'stays_dispatch_reservations_by_date' que importa da stays para o banco de dados do SAPRON reservas que foram inseridas no intervalo de tempo do parâmetro dado. No caso da nossa task em questão o intervalo de tempo é o dia atual e portanto, ela importa as reservas de hoje.

```python
@shared_task(
    name='channel_manager.stays.import_new_reservations',
    max_retries=10,
    default_retry_delay=1,
    autoretry_for=(Exception,),
)
def stays_import_new_reservations():
    start_date = datetime.now().date() - timedelta(days=1)
    end_date = datetime.now().date()
    _stays_dispatch_reservations(start_date, end_date, "creation")
```

> A task 'financial_property_consolidate' delega ao celery, sempre que demandada a classe 'PropertyFinancialClosing()' passando como parâmetros a data atual ou datas passadas, caso queira o resultado de um fechamento anterior. Delegar a classe citada ao celery é interessante pois além de pesada, visto que compila o fechamento de um proprietário, é possível passarmos também parâmetros a ela.

```python
@shared_task(name='financial_property_consolidate', ignore_result=True)
def property_consolidate(date=None, properties=None, owners=None):
    # By default run consolidation
    # for yesterday
    if date is None:
        consolidate_date = datetime.date.today()
    else:
        # But if a date is passed
        # run consolidation for that date
        consolidate_date = datetime.datetime.strptime(date, '%Y-%m').date()

    LOGGER.info(f'Starting Property financial closing consolidation for date {consolidate_date}')
    consolidation = PropertyFinancialClosing()
    consolidation.execute(consolidate_date, properties, owners)
    LOGGER.info('end of task')
```