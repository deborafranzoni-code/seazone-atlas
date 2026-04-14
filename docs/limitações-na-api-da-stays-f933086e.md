<!-- title: Limitações na API da Stays | url: https://outline.seazone.com.br/doc/limitacoes-na-api-da-stays-tksc0R326a | area: Tecnologia -->

# Limitações na API da Stays

# Outras Dependências

A rota `https://ssl.stays.com.br/external/v1/content/listing-rooms/:listing-id` não permite a definição do subtipo dos cômodos (Como se chama este espaço personalizado?) que são do tipo `'Outras Dependências' (5ab8f8a2f6b2dc2e97f97048)`


 ![](/api/attachments.redirect?id=ed262c13-f64c-48e7-9764-18f5752a33c9 " =770x377")

A rota 


## Idade Mínima nas Regras da Acomodação

A rota `https://ssl.stays.com.br/external/v1/settings/listing/:listing-id/house-rules` não permite a inserção da idade mínima nas regras da acomodação


 ![](/api/attachments.redirect?id=82714121-e20c-4e3d-a19d-8668edae4436 " =767x327")

### Exemplo de Payload Utilizado

```javascript
[
  {
    "smokingAllowed": false,
    "eventsAllowed": false,
    "kidsAllowed": true,
    "_i_kids": 14,
    "babiesAllowed": true,
    "_i_babies": 14,
    "quietHours": true,
    "quietHoursDetails": {
      "_i_from": 22,
      "_i_to": 7
    },
    "petsAllowed": "no",
    "petsPriceType": "free",
    "_mskids": {
      "pt_BR": ""
    },
    "_msbabies": {
      "pt_BR": ""
    },
    "_mshouserules": {
      "pt_BR": "IMPORTANTE:<br>- Check-in: das 15h às 20h;<br>- Checkout: até as 11h;<br>- Para check-in após as 20h, há cobrança adicional de taxa de conveniência no valor de R$50 até as 22h e de R$100 após as 22h;<br>- Para reservas com check-in no mesmo dia, pode ser necessário um tempo de espera adicional devido ao deslocamento do anfitrião até o imóvel;<br>- Roupas de cama/banho e limpeza extras são solicitadas e pagas à parte, direto com a Seazone;<br>- É proibida a entrada de hóspedes e/ou visitantes que excedam a capacidade do imóvel e que não estejam cadastrados na reserva;<br>- Não é permitido fumar;<br>- Não é permitido pets;<br>- Festas e som alto são estritamente proibidos, sujeito a multa;<br>- Horário de silêncio: das 22h às 7h;<br>- Qualquer desrespeito é de responsabilidade do hóspede, assim como multas;<br>- Para estadias superiores a 30 dias, será cobrada uma taxa extra de limpeza referente a uma nova limpeza no imóvel e à troca de roupas de cama e toalhas durante o período;<br>- Antes do check-in, poderá ser solicitado o envio de documentação dos hóspedes para confirmação dos dados.",
      "es_ES": "IMPORTANTE:<br>- Check-in: de 15:00 a 20:00 h;<br>- Check-out: hasta las 11:00 h;<br>- Para check-in después de las 20:00 h, se aplicará un cargo adicional de R$50 hasta las 22:00 h y de R$100 después de las 22:00 h;<br>- Para reservas con check-in el mismo día, podría ser necesario un tiempo de espera adicional debido al desplazamiento del anfitrión a la propiedad;<br>- La ropa de cama/toallas adicionales y el servicio de limpieza se solicitan y pagan por separado, directamente con Seazone;<br>- Se prohíbe la entrada a huéspedes o visitantes que excedan la capacidad de la propiedad y no estén registrados en la reserva;<br>- No se permite fumar;<br>- No se admiten mascotas;<br>- Las fiestas y la música alta están estrictamente prohibidas, sujetas a multas;<br>- Horario de silencio: de 22:00 a 7:00 h;<br>- Cualquier falta de respeto es responsabilidad del huésped, al igual que cualquier multa;<br>Para estancias superiores a 30 días, se cobrará un cargo adicional por limpieza, incluyendo la reposición de ropa de cama y toallas durante el periodo.<br>Antes del check-in, se podrá solicitar a los huéspedes que envíen documentación que confirme sus datos.",
      "en_US": "IMPORTANT:<br>- Check-in: from 3 PM to 8 PM;<br>- Check-out: until 11 AM;<br>- For check-in after 8 PM, there is an additional convenience fee of R$50 until 10 PM and R$100 after 10 PM;<br>- For reservations with same-day check-in, additional waiting time may be necessary due to the host's travel to the property;<br>- Extra bed linens/towels and cleaning services are requested and paid for separately, directly with Seazone;<br>- Guests and/or visitors exceeding the property's capacity and who are not registered in the reservation are prohibited from entering;<br>- Smoking is not allowed;<br>- Pets are not allowed;<br>- Parties and loud music are strictly prohibited, subject to fines;<br>- Quiet hours: from 10 PM to 7 AM;<br>- Any disrespect is the responsibility of the guest, as are any fines;<br>- For stays longer than 30 days, an extra cleaning fee will be charged for a new cleaning of the property and the replacement of bed linen and towels during the period;<br>- Before check-in, guests may be asked to send documentation to confirm their details."
    }
  }
]
```


\