<!-- title: PRICE_AV | url: https://outline.seazone.com.br/doc/price_av-Si5FMNZgyF | area: Tecnologia -->

# PRICE_AV

![](/api/attachments.redirect?id=b6d0777a-8cab-4838-8d4b-238c74913652)

Diagrama Simplificado ([Video explicativo](https://drive.google.com/file/d/1h548x9V9Cb2NS_IZ3fo175Q7jI4I8zP_/view)): [link_miro](https://miro.com/app/board/uXjVKJHYMnM=/)

### Documentação em Video:

* [Explicação do Funcionamento do price_av](https://drive.google.com/file/d/13EuqiwALv_qnMhFjwZcypSWrY3vvc3NW/view?usp=sharing)
* [Como roda o pipe-airbnb-scraper e pipe-airbnb-scraper-priceav](https://drive.google.com/file/d/1x_E9BS3RcGQ5H5A7fwJ4vbEYG1FPs_Lq/view)
* [Código generalidades Scrapers](https://drive.google.com/file/d/1ADXmOfcGWIPap9OB9tTX_aN1hlpmt_3h/view?usp=sharing)
* [Código pipe-airbnb-scraper-price-v2](https://drive.google.com/file/d/11TeobbQ3JjiPcb5dC5kFQDBXUxo2n8SP/view)
* [Código pipe-airbnb-scraper-priceav](https://drive.google.com/file/d/1e7KMbuPXvVOnUle0mbRw9g_ris4539qF/view)

# **Perguntas Iniciais**

* Qual preço eu coloco nas diárias? Como precificar?
* Quanto um imóvel fatura no Airbnb?
* Como eu encontro imóveis baratos?

# **Solução inicial**

Para conseguir entender como precificar e quanto um imóvel fatura, precisamos primeiro conseguir dados dos anúncios, para ter uma informação correta e não apenas suposições. Principalmente dos dias em que ele fica ocupado e o preço cobrado por essa diária, assim já conseguimos ter uma noção inicial do faturamento. Para precificação podemos procurar por imóveis parecidos com o que se deseja precificar  e assim criar um sistema de precificação baseado nos valores de mercado.

# **Funcionamento (price_v2)**

O scraper **price_v2** utiliza API do Airbnb de disponibilidade para verificar os dias disponíveis, estadia mínima, preço da estadia e se é *Instant_Book*, isto é, se caso você fizer uma reserva não precisa de aprovação do usuário para ser confirmada.

Para fazer a requisição precisamos apenas acessar a página do anúncio, fazendo a requisição da API, retornando um .json com as informações, o scraper de preço roda diariamente com aproximadamente 30 mil anúncios.

 ![](/api/attachments.redirect?id=143afa8d-82f4-48cc-9eed-d43c15f6a7f5)

Como podemos ver pela imagem acima algumas datas estão ocupadas(riscadas) e as outras livres, quando fazemos a requisição, adquirimos as datas do dia do mês atual mais os dias dos próximos 11 meses, dando no total 12 meses. No caso da imagem, o primeiro dia seria 01/03/2022 e o último 28/02/2023.

Vale ressaltar que o scrap, apesar de adquirir alguns dias que são anteriores ao dia atual da scrapagem, ele somente verifica os dias após, pois como podemos ver na imagem (feita em 29/03/2022) os dias anteriores aparecem como ocupados, não sendo útil para scrapagem.

Podemos dizer que o scraper se divide em dois para salvar os dados, sendo o primeiro para salvar o preço. Os dados adquiridos salvos são:

* **airbnb_listing_id:** Id fornecido em cada listing pelo Airbnb.
* **date:** Data que está sendo verificado o preço.
* **price:** Preço para alugar o anúncio.
* **price_string:** Preço com tipo da moeda junto.
* **minium_stay:** Estadia mínima.
* **available:** Verifica se está disponível na data selecionada.
* **av_for_checkin:** Verifica se está disponível para check-in na data selecionada.
* **aquision_date: D**ata de aquisição dos dados.

Na segunda parte de salvar os dados, ele foca em salvar se é Instant_book, os dados salvos são:

* **airbnb_listing_id:** Id fornecido em cada listing pelo Airbnb.
* **date:** Data que está sendo verificado o preço.
* **aquision_date:** Data de aquisição dos dados.

## **Problemas** **do scraper**

A API v2 parou de funcionar por um período de tempo (hoje está funcionando normalmente), no caso quando selecionava um data, o preço retornava sempre **null**.

## **Soluções encontradas**

Foram criados 3 outros scrapers utilizando outra API do Airbnb. Um scraper que consegue verificar a disponibilidade, um segundo que consegue verificar o preço, e o terceiro que verifica se é *Instant_Book*\*. O que deixou a operação 3 vezes mais cara, pois antes o que uma execução conseguia adquirir, com esta solução é preciso fazer 3.

Importante ressaltar que hoje esses 3 scrapers rodam quando o price_v2 "falha", sendo assim eles executam nessa ordem:

**price_v2→(Falha para obter dados)→availability→price→instant_book**