<!-- title: Diário de Bordo - Regras da acomodação | url: https://outline.seazone.com.br/doc/diario-de-bordo-regras-da-acomodacao-MrNJeFgfv4 | area: Tecnologia -->

# Diário de Bordo - Regras da acomodação

## Edição de regras na Stays

Rota: `PATCH` `https://ssl.stays.com.br/external/v1/settings/listing/:listingId/house-rules`

Ex. de payload:

```json
{
    "smokingAllowed": false,
    "eventsAllowed": false,
    "quietHours": true,
    "kidsAllowed": true,
    "babiesAllowed": true,
    "quietHoursDetails": {
        "_i_from": 22,
        "_i_to": 7
    },
    "petsAllowed": "yes",
    "petsPriceType": "chargesmayapply",
    "_i_kids": 1,
    "_mskids": {
        "pt_BR": "<p>Será permitida no máximo 1 criança neste imóvel</p>"
    },
    "_i_babies": 3,
    "_msbabies": {
        "pt_BR": "<p>Neste imóvel é permitido até 3 bebê(s)</p>"
    },
    "_i_babyCribs": 1,
    "_mshouserules": {
        "pt_BR": "IMPORTANTE:<br><br>- Check-in: a partir das 15h;<br><br>- Checkout: até as 11h;<br><br>- Recepção 24h;<br><br>- No check-in, será entregue apenas um cartão-chave por apartamento, será realizado o cadastro facial e da placa do veículo para acesso à garagem.<br><br>- Segunda via do cartão: R$ 50,00.<br><br>- Roupas de cama/banho e limpeza extras são solicitadas e pagas à parte, direto com a Seazone;<br><br>- Proibida a entrada de hóspedes e/ou visitas além da capacidade do imóvel;<br><br>- Não é permitido fumar;<br><br>- Não é permitido pets;<br><br>- Festas e som alto são estritamente proibidos, sujeito a multa;<br><br>- Horário de silêncio: das 22h às 7h;<br><br>- Qualquer desrespeito às regras do condomínio/vizinhança são de responsabilidade do hóspede, assim como multas.",
        "es_ES": "IMPORTANTE:<br><br>- Check-in: a partir de las 15h;<br><br>- Checkout: hasta las 11h;<br><br>- Recepción 24h;<br><br>- En el check-in, se entregará solo una tarjeta clave por apartamento, y se realizará el registro facial y de la matrícula del vehículo para el acceso al garaje.<br><br>- Duplicado de la tarjeta: R$ 50,00.<br><br>- Ropa de cama/baño y limpieza extras se solicitan y pagan por separado, directamente con Seazone;<br><br>- Prohibida la entrada de huéspedes y/o visitas que excedan la capacidad del inmueble;<br><br>- No está permitido fumar;<br><br>- No se permiten mascotas;<br><br>- Las fiestas y el volumen alto de música están estrictamente prohibidos, sujeto a multa;<br><br>- Horario de silencio: de 22h a 7h;<br><br>- Cualquier incumplimiento de las reglas del condominio/vecindario es responsabilidad del huésped, así como las multas.",
        "en_US": "IMPORTANT:<br><br>- Check-in: from 3 PM;<br><br>- Checkout: until 11 AM;<br><br>- 24h reception;<br><br>- At check-in, only one key card per apartment will be provided, and facial and vehicle license plate registration will be done for garage access.<br><br>- Replacement card: R$ 50.00.<br><br>- Extra bed/bath linens and cleaning must be requested and paid separately, directly with Seazone;<br><br>- Entry of guests and/or visitors beyond the property's capacity is prohibited;<br><br>- Smoking is not allowed;<br><br>- Pets are not allowed;<br><br>- Parties and loud music are strictly prohibited, subject to fines;<br><br>- Quiet hours: from 10 PM to 7 AM;<br><br>- Any violation of the condominium/neighborhood rules is the guest's responsibility, including fines."
    }
}
```


## Problemas e limitações

* A API da Stays não permite a edição da idade mínima do hóspede