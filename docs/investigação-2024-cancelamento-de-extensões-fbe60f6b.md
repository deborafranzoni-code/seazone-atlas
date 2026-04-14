<!-- title: [Investigação 2024] Cancelamento de Extensões | url: https://outline.seazone.com.br/doc/investigacao-2024-cancelamento-de-extensoes-GRVQlgTz93 | area: Tecnologia -->

# [Investigação 2024] Cancelamento de Extensões

Recentemente, foi identificado um problema onde a cadeia de extensões que compõem uma reserva é quebrada quando, por algum motivo, uma extensão é cancelada e posteriormente recriada. O objetivo dessa doc é auxiliar no entendimento do fluxo atual, assim como na formulação da solução.

## Fluxo atual

Para entendermos o fluxo atual seguiremos o caso descrito abaixo e descrito nesse [diagrama](https://drive.google.com/file/d/1_q1NoZLQVoUkvtqirl5CmX-2DXcpK1O8/view?usp=sharing).


1. Uma reserva é importada. Chamaremos ela de **reserva original** por que ela é a reserva que dá início ao fluxo. Essa reserva inicialmente possui os campos `original_reservation_id`, `late_extension_id` e `early_extension_id` como nulos. Imagine a caixa preta como sento a entidade `reservation` e o número dentro dela como sendo o seu `id` ou a sua ordem de criação em relação as demais.

 ![](/api/attachments.redirect?id=4439bad1-589b-4072-b620-7bf99996ea98)



1. Após a criação da original, é criado uma `early extension` de `id` 2. Ela possui o campo `original_reservation_id = 1`, indicando que ela antecede a de `id 1`. Já a reserva original (1) possui o campo `early_extension_id = 2` indicando que a reserva 2 antecede a ela. A seta entre elas indica esses apontamentos.

 ![](/api/attachments.redirect?id=32216e85-c249-49a4-babc-ff6070a19340)



1. Da mesma forma, é criada uma `late extension`  de `id` 3. Semelhante ao passo anterior, ela possui o campo `original_reservation_id = 1` e a reserva original (1) tem seu campo `late_extension_id = 3`, indicando o relacionamento entre elas.

 ![](/api/attachments.redirect?id=579fe17b-dc74-42a3-9107-1aaee8f7756b)



1. Criando mais algumas extensões para a reserva, ficamos com os seguintes apontamentos.

 ![](/api/attachments.redirect?id=fa9b1ff2-8802-48e3-87f8-9c7a39961e3d)



1. Os problemas de apontamento começam ao cancelarmos uma extensão. Ao cancelarmos a `early_extension` 2, os apontamentos que referenciam essa extensão não são modificados, fazendo com que a cadeia de reservas aponte para uma extensão que não existe mais. Esses apontamentos são destacados em laranja na imagem.

 ![](/api/attachments.redirect?id=df6eb0f8-cd7f-4600-9cac-95c35512c26a)



1. Quando a reserva cancelada for recriada, agora com ID 6, os apontamentos de 5 e 1 não são alterados corretamente, tornando a nova extensão 6 impossível de ser identificada em alguns casos.

 ![](/api/attachments.redirect?id=8b50c5ba-c7e3-4581-a45d-a2c9d054f577)


## Objetivo

O principal objetivo é corrigir os apontamentos sempre que identificarmos que uma reserva cancelada no fluxo, assim como descrito na figura abaixo.

 ![](/api/attachments.redirect?id=66c76436-91ce-4880-951b-1875677ec5aa)


> ℹ️ O caso descrito pode ser visto no banco de staging com a seguinte query

```sql
select
  r.id,
  r.original_reservation_id,
  r.late_extension_reservation_id,
  r.early_extension_reservation_id,
  r.status,
  r.check_in_date,
  r.check_out_date
from
  reservation_reservation r
where
  r.stays_reservation_code in (
    'OP16I',
    'OQ27I',
    'OR15I',
    'OS29I',
    'OT17I',
    'OQ28I'
  )
order by
  r.check_in_date asc;
```

## Solução

Um dos pontos chaves da resolução é a escolha correta da `original_reservation` no momento da importação da nova reserva. Para casos como o descrito a cima, podemos apenas:


1. Procurar se existe uma reserva com as mesmas datas de `check in` e `check out` da reserva a ser importada.
2. Caso positivo, cancelamos a reserva já existente e a nova reserva herda a `late_extension_reservation_id`, `early_extension_reservation_id` e `original_reservation_id` dessa.

Referente ao fluxo de cancelamento da reserva, devemos apenas remover todos os apontamentos que fazem referência à reserva em questão.

⚠️ A solução proposta cobrirá apenas casos semelhantes com o apontado nesse documento. Em casos onde a reserva recriada possui datas diferentes de *check in* e *check out,* o ajuste não terá efeito.

## Refactor do modelo de reservas

Essa investigação trouxe à tona as falhas do modelo atual. O excesso de dados salvos na tabela `reservation` e o relacionamento entre extensões acabaram por complicar o processo. Com isso, surgiu a necessidade de reavaliar o modelo atual e algumas propostas foram surgindo.

Uma das propostas constitui em uma refatoração total no modelo de reservas, podendo ser feita de dois modos:


1. Separando reservas e extensões em dois modelos, com suas próprias tabelas e regras de negócio
2. Aproveitar o modelo atual, onde reservas e extensões compartilham do mesmo modelo, mas removendo dados desnecessários como `has_early_extension`, `is_extension`, `early_extension_reservation_id` e etc, mantendo apenas o registro para a reserva original da corrente de extensões.

Um ponto a se ressaltar é que esse refactor teria efeito em praticamente todos os sistemas existentes no Sapron, o que mostra a necessidade de um planejamento prévio bem executado.

## Glossário

| Nome | Descrição |
|----|----|
| early extension | extensão que adianta o dia de check in. |
| late extension | extensão que atrasa o dia de check out. |
| `original_reservation_id` | campo que indica a reserva que uma extensão se refere. Se a extensão for do tipo *early,* a `original_reservation_id` será a reserva imediatamente após a extensão. Se for uma *late,* o campo indicará a reserva imediatamente anterior à ela. |
| `early_extension_id` | campo que indica a extensão do tipo *early* imediatamente anterior à reserva |
| `late_extension_id` | campo que indica a extensão do tipo *late* imediatamente posterior à reserva |