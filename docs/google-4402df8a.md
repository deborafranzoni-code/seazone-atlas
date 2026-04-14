<!-- title: Google | url: https://outline.seazone.com.br/doc/google-zb7X9G0EIT | area: Tecnologia -->

# Google

# Google Hotels (Vacation Rentals)

## Feed de Propriedades

https://developers.google.com/hotels/vacation-rentals/dev-guide/onboarding?hl=pt-br

Um feed de listagem de aluguel por temporada contém todas as propriedades a serem exibidas no Google. Esse feed contém os atributos físicos da propriedade, incluindo nome, endereço, locais de geocódigos, URLs de imagem, URLs de sites e comodidades.

### Método 2: feed de lista em XML

Esse método é uma boa opção para parceiros de conectividade e parceiros com inventários maiores. Para o processamento inicial, os parceiros criam um feed de lista de aluguel por temporada e incluem atributos exclusivos para aluguéis por temporada.

### Criar os arquivos XML

Para o processamento inicial, você precisa compartilhar um feed de fichas com o Gerente técnico de contas do Google de acordo com as especificações fornecidas na [referência XML do feed de lista de hotéis](https://developers.google.com/hotels/hotel-prices/xml-reference/hotel-list-feed?hl=pt-br#attribute-names-vr). No entanto, diferentemente das listas de hotéis, você precisa incluir [atributos relevantes específicos para aluguéis por temporada](https://developers.google.com/hotels/vacation-rentals/dev-guide/vr-attributes?hl=pt-br). O processamento do feed de fichas pode levar de duas a quatro semanas. Durante esse tempo, o Google entrará em contato com você para ajudar na solução de problemas e na otimização do feed.

<aside> 💡 **Importante** :se você omitir os valores de atributos listados como **Opcional (altamente recomendado)**, isso não impedirá que o feed de lista seja validado, mas poderá fazer com que a listagem não apareça nos resultados da pesquisa quando determinados filtros forem aplicados.

</aside>

### Hospedar o feed de fichas e a estrutura de arquivos

Hospede seu feed de fichas em um arquivo .zip. O Google busca o conjunto mais recente de listas de propriedades no seu inventário diariamente.

Lembre-se dos seguintes requisitos para importar o arquivo de listagem hospedado:

* Os arquivos ZIP precisam ser compartilhados com o Google.
* Os feeds devem ser compartilhados apenas no formato .zip (sem .tar ou .gz).
* Cada arquivo ZIP pode conter vários arquivos XML de listagem.
* **Cada arquivo XML pode conter mais de uma listagem (preferencial).**
* Cada arquivo XML precisa ter menos de 100 MB.
* Cada arquivo XML só pode conter um idioma.
  * Exemplo: `xml{:.readonly} <listings><language>en</language>...</listings>`
  * Para idiomas não principais, inclua apenas o ID exclusivo do hotel e o conteúdo da propriedade somente nesse idioma.