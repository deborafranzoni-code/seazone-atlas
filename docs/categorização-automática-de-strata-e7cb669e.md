<!-- title: Categorização automática de Strata | url: https://outline.seazone.com.br/doc/categorizacao-automatica-de-strata-4zxO7W9qzi | area: Tecnologia -->

# Categorização automática de Strata

# Documentação Dataset

O Dataset do projeto de Categorização é consituido por imagens scrappadas do Airbnb e informações da Categoria do anúncio classificado pelo time de RM.

Link do DataSet na cloud:

* [AWS](https://us-west-2.console.aws.amazon.com/s3/buckets/brlink-seazone-models-data?region=us-west-2&bucketType=general&prefix=categorizacao-dataset/&showversions=false)

## Origem dos Dados

### Scrapper

Foi construído um MVP para scrappar as imagens do Airbnb. O script está salvo aqui: <https://github.com/seazone-tech/Util-dados/tree/main/Marcio/ImageScrapper>

O scrapper funciona da seguinte maneira:

* Ele recebe de input um id do airbnb.
* Cria uma pasta com o id do airbnb.
* Pega o html da página a partir do BeautifulSoup.
* Encontra no html os links de download das imagens + alguns metadados como título e seção da imagem.
* Faz o download das imagens e salva dentro da respectiva pasta do id do airbnb.
* Salva um json chamado file.json dentro da respectiva pasta do id airbnb. Esse arquivo vai ter alguns dos metadados da imagem.

O formato que o scrapper salva os dados é o seguinte:

 ![](/api/attachments.redirect?id=4e053bf7-257d-495f-835e-f5f02b938a12)

Formato do file.json:

```json
[
   {
      "id":"1172346465",
      "url":"https://a0.muscache.com/im/pictures/289966b1-3196-4dc1-baa4-02c8bd1ed982.jpg",
      "label":"Desk for work and meals",
      "room_title":"Living room",
      "image_name":"289966b1-3196-4dc1-baa4-02c8bd1ed982.jpg"
   },
   {
      "id":"1172346474",
      "url":"https://a0.muscache.com/im/pictures/30204b38-25f0-4fd0-b0f4-948749f106e9.jpg",
      "label":"Full kitchen image 1",
      "room_title":"Full kitchen",
      "image_name":"30204b38-25f0-4fd0-b0f4-948749f106e9.jpg"
   },
   …
]
```

### Seleção de ids para scrappar

Nesse primeiro MVP foram selecionados 417 anúncios para serem scrappados.

A lógica de escolha foi pegar as regiões mais balanceadas dentre as stratas e que se comportam de forma similar.

Uma Categoria é composta pelo poligono + tipo + quartos + strata, então no MVP procurou-se anúncios a partir de poligono + tipo + quartos com número parecido de concorrentes em cada strata. Filtro:

* Mais de 100 concorrentes.
* Pelo menos 10 em cada strata.

As 5 melhores foram as seguintes:

 ![](/api/attachments.redirect?id=3517553c-7dc7-44ac-a669-ea2419242234)

No final, optou-se em pegar todos os concorrentes das "categorias":

* Florianpolis-Jurere_Tradicional-apartamento-1Q
* Florianopolis-Centrao-apartamento-1Q
* Florianopolis-UFSC-1Q
* Florianopolis-Beira_mar-apartamento-1Q

O motivo é que todas são apartamentos de 1 quarto, parte está perto de praia e parte está em cidade, então elas tem um número suficiente de concorrentes para testarmos e tem um pouco de variabilidade dentre cidade e praia.

Descobriu-se que alguns imóveis estavam classificados em mais de uma strata e que alguns anúncios morreram, então no final a distribuição ficou:

* SIM: 26
* JR: 130
* SUP: 126
* TOP: 79
* MASTER: 56

## Organização e Schema

Depois de baixar todas as imagens, foi criado uma tabela onde junta-se todas as informações relevantes da imagem (ela foi criada a partir dos file.json e dados dos concorrentes classificados pelo RM).

 ![](/api/attachments.redirect?id=cb33e4b7-549f-4a34-a7c4-9a271ce927c3)

**Schema:**

* **airbnb_listing_id:** id do anúncio no airbnb, vai ser usada para diferenciar conjunto treino/test futuramente.
* **id:** id da imagem, no conjunto de dados esse id é único.
* **image_path:** path até a imagem, vai ser usado na hora de passar pro modelo.
* **image_name:** É o nome da imagem. É importante comentar que imagens com o mesmo nome (mesmo em imóveis diferentes) são A MESMA imagem, então é necessário uma lógica em cima disso na hora de separar em treino/teste.
* **label:** É o nome da imagem, toda imagem tem label (as vezes é um nome genérico como "Listing image 42").
* **room_title:** Tem vários nulos, mas essas são as seções das fotos (vem em inglês, exemplos: Bedrooms, Living room, Pool, Bedroom 1, etc).
* **polygon, listing_type, number_of_bedrooms:** São informações que definem a categoria do anúncio, mas nesse primeiro momento não serão usadas.
* **strata:** Strata do anúncio. Nesse primeiro momento o label do modelo será a strata.

**Exemplo de Label:**

 ![](/api/attachments.redirect?id=70b32571-2bf5-480b-bd4d-8c82c8674190)

**Exemplo de room title:**

 ![](/api/attachments.redirect?id=18c868b7-add9-4eab-b1b9-cc5f02f6cd34)

**Distribuição da Strata (12084 imagens totais):**

* SIM: 562
* JR: 3280
* SUP: 3823
* TOP: 2354
* MASTER: 2065

Como foi gerado uma tabela centralizada com as informações das imagens, os arquivos file.json não são mais necessários.

O formato final do diretório ficou esse:

 ![](/api/attachments.redirect?id=8e31bae4-26b2-4dbc-9dbb-60a706e2c51f)

## Qualidade dos Dados

### Imagens Duplicadas

Analisando os dados, descobriu-se que imagens com o MESMO image_name são idênticas, mesmo estando em imóveis diferentes. Ao todo 413  imagens possuíam o mesmo nome, exemplo de imagens duplicadas:

 ![](/api/attachments.redirect?id=46d19695-ecb9-46cd-9056-7796772147cd)

[id_airbnb: 37110904](https://www.airbnb.com.br/rooms/37110904?source_impression_id=p3_1729168553_P3sWxCtqD944E57j&modal=PHOTO_TOUR_SCROLLABLE&modalItem=1075395469)

 ![](/api/attachments.redirect?id=095fd5d6-668a-42cd-97c4-b7dfea617803)

[id_airbnb: 580225331467704998](https://www.airbnb.com.br/rooms/580225331467704998?source_impression_id=p3_1729168663_P3W-QCLYQTw1Tp-x&modal=PHOTO_TOUR_SCROLLABLE&modalItem=1358315396)

Também descobriu-se que haviam outras imagens duplicadas, mas que não dependiam do image_name, então foi necessário fazer uma lógica que encontra-se essas imagens duplicadas.

A ideia mais eficiente em termos de processamento foi gerar um hash da imagem. A partir dos pixels dela, gerar uma sequência de números única e usar isso para encontrar duplicidades.

Este foi o tutorial seguido: <https://pyimagesearch.com/2017/11/27/image-hashing-opencv-python/>

O hash conseguiu identificar **1198** imagens duplicadas (dessas, 917 não tinham o mesmo nome).

### Imagens Irrelevantes

Dentro do conjunto de dados, existem algumas imagens irrelevantes a categorização.

Essa praia não tem relaçãp com a strata do imóvel, é só uma foto da praia que fica perto dele.

 ![](/api/attachments.redirect?id=d272922e-d72a-4e61-a503-db74381262f3)

As vezes também colocam a logo de uma empresa.

 ![](/api/attachments.redirect?id=879f0a49-6be4-4840-8a78-89e2a35db20c)

 ![](/api/attachments.redirect?id=e182aa47-af8e-4282-a0bb-2f25eb878b53)

A imagem ocasionalmente também tem bordas, dependendo do modelo elas precisam ser tratadas.

A forma encontrada de filtrar as os dois primeiros tipos foi se basear no metadado room_title.

Apenas metade das imagens possuem esse campo informado, mas nas que possuem podemos usa-lo para filtrar imagens desnecessárias, como as do tipo "common place":

 ![](/api/attachments.redirect?id=da8484dc-1be5-4bb8-a3fe-1fab30993e7c)

 ![](/api/attachments.redirect?id=701b74b6-fb7b-42d8-9b97-45cb7db64895)

### Dataset Final

Após as desduplicações e filtros em cima do campo room_title, o dataset final possuí 10816 imagens rotuladas como:

* SIM: 487
* JR: 2963
* SUP: 3410
* TOP: 2030
* MASTER: 1926


# Modelo Baseline

A partir do dataset criado, o próximo passo é tentar gerar um primeiro modelo para fazer um teste de categorização automática

## Modelos Existentes

Dentre os modelos já existentes, existem duas soluções comumente usadas.


1. **Transfer learning**

   
   1. **[Hotelify: A classifier for hotel images](https://github.com/omega-rg/Hotelify-A-classifier-for-hotel-images?tab=readme-ov-file#hotelify-a-classifier-for-hotel-images)**
   2. **[Real Estate Image Classification using Transfer Learning](https://arnav-andraskar.medium.com/real-estate-image-classifier-9e15dcb5cafa)**
   3. [NVIDIA Image Quality Assessment](https://github.com/idealo/image-quality-assessment/tree/master)
2. **Segmentação**

   
   1. [House price estimation from visual and textual features](https://arxiv.org/pdf/1609.08399)

**Transfer Learning**

Essa técnica é boa quando o conjunto de dados não é grande o suficiente para treinar um modelo de machine learning do zero.

A técnica consiste em pegar um modelo pré-treinado para resolver um problema parecido e o treinar/adaptar para o novo conjunto de dados.

**Segmentação**

Outra técnica é segmentar os pontos de interesse das imagens e usa-las de input para o modelo (circular as cadeiras, geladeiras, camas, etc).

Uma solução que não envolva tanto trabalho manual seria usando algoritimos de extração de features, como o SURF. Esse algoritimo foi usado em conjunto com informações textuais no artigo citado acima para prever o preço de casas.

Como esse tipo de estratégia é bem diferente da outra, por enquanto não será abordada.

## Pré-processamento

O input dos modelos precisa seguir um padrão de tamanho e normalização. Abaixo estão as configurações dos modelos pré treinados escolhidos para realizar os testes de transfer learning.

* **InceptionV3**: Pixels entre -1 e 1, precisa ser RGB e no mínimo tem que ser 75x75 (padrão é 299x299)
* **ResNet50V2:** Pixels entre -1 e 1, precisa ser RGB e no mínimo tem que ser 30x30 (padrão é 224x224)
* **VGG19:** Pixels precisam ser normalizados em volta do 0, mas **SEM SCALAR**, precisa ser BGR e no mínimo tem que ser 32x32 (padrão é 224x224)

Foi separado o conjunto de dados em treino, teste e validação. A separação tenta seguir as proporções de strata do dataset.

| **Strata** | **Treino (80%)** | **Validação (10%)** | **Teste (10%)** |
|:---:|:---:|:---:|:---:|
| SIM | 398 | 13 | 76 |
| JR | 2201 | 349 | 413 |
| SUP | 2774 | 321 | 315 |
| TOP | 1752 | 138 | 140 |
| MASTER | 1620 | 173 | 133 |

Também é importante usar algumas técnicas de data augmentation. A ideia é que a cada época, as imagens de treino se alterem um pouco (rotação, brilho, virar horizontalmente, etc), isso ajuda a evitar o overfitting. Foi usado a classe `ImageDataGenerator` do tensorflow/keras para isso.

Por último, na criação dos modelos, é esperado o padrão one-hot-encoding, ou seja, a coluna de strata do Dataset precisa ser modificada para possuir 5 colunas de 0 ou 1 que representam cada uma das stratas:

* SIM: 10000
* JR: 01000
* SUP: 00100
* TOP: 00010
* MASTER: 00001

Aqui é usado o método `ImageDataGenerator.flow_from_dataframe`, ele automaticamente consegue fazer essa conversão.

## Testes Transfer Learning

Foi criado uma pipeline para treinar os modelos em cima de cada um dos modelos base.

Os modelos em si são bem simples, é pego o modelo base e adicionado 3 camadas extras:

* **Camada GlobalAveragePooling2D:** É usada para reduzir a dimensionalidade do output do modelo base. 
* **Camada Dropout:** Durante o treinamento ela desativa algumas conexões dos neurônios para evitar overfitting.
* **Camada de Saída:** Composta por 5 neurônios ativados pela função de ativação softmax. Cada neurônio é responsável por predizer a probabilidade de imagem ser de sua respectiva strata.

Foram geradas as métricas de acurácia, recall, precision e f1_score em cima de cada modelo base. Como o modelo faz a predição em cima da imagem, também é interessante gerar métricas para descobrir se o modelo acertaria a strata do imóvel.

Como o modelo fornece a probabilidade da imagem ser de cada strata, é feito a média das probabilidade de cada imagem do imóvel, no final, a predição da strata do imóvel é aquela strata com maior probabilidade.

### Métricas em cima do conjunto de validação:

#### InceptionV3

| **Métrica** | **Valor nível imagem** | **Valor nível imóvel** |
|----|----|----|
| accuracy | 0.36720 | 0.53846 |
| recall | 0.24457 | 0.29134 |
| precision | 0.25191 | 0.22445 |
| f1_score | 0.24001 | 0.24861 |

#### ResNet50V2

| **Métrica** | **Valor nível imagem** | **Valor nível imóvel** |
|----|----|----|
| accuracy | 0.34808 | 0.53846 |
| recall | 0.25982 | 0.3 |
| precision | 0.26483 | 0.24965 |
| f1_score | 0.25477 | 0.24688 |

#### VGG19

| **Métrica** | **Valor nível imagem** | **Valor nível imóvel** |
|----|----|----|
| accuracy | 0.32293 | 0.53846 |
| recall | 0.26686 | 0.28269 |
| precision | 0.25467 | 0.26727 |
| f1_score | 0.25467 | 0.26910 |

#### Dummy

Também foi gerado um modelo Dummy para saber se o modelo está se desempenhando melhor do que um modelo que "chutaria" as stratas. No dummy foi usado a configuração stratified, então ele chuta os valores de acordo com a proporção de cada strata. A nível imagem fica apenas 5-10% abaixo dos outros, mas a nível imóvel piora bastante.

| **Métrica** | **Valor nível imagem** | **Valor nível imóvel** |
|----|----|----|
| accuracy | 0.24748 | 0.25641 |
| recall | 0.20435 | 0.17846 |
| precision | 0.19833 | 0.09454 |
| f1_score | 0.19632 | 0.11826 |

#### Conclusão

Todos os modelos a nível imóvel tiveram a mesma acurácia, ou seja, acertaram 21 dos 39 imóveis disponíveis no conjunto de validação. Como o VGG19 teve um f1_score um pouco melhor a nível imóvel ele foi escolhido para seguir os testes.

### Fine Tunning

O processo padrão de fazer transfer learning é:


1. Carregar o modelo base;
2. Criar as camadas dentre o modelo base e a saída do modelo;
3. Treinar APENAS as camadas extras criadas;
4. Diminuir o learning rate e treinar o modelo INTEIRO (modelo base também)

Fazendo o fine tunning do VGG19, parece que não ficou bom, elas ficaram um pouco abaixo das métricas anteriores.

| **Métrica** | **Valor nível imagem** | **Valor nível imóvel** |
|----|----|----|
| accuracy | 0.31589 | 0.41025 |
| recall | 0.22374 | 0.26923 |
| precision | 0.23258 | 0.33096 |
| f1_score | 0.21496 | 0.24285 |

O modelo final será o VGG19 padrão, sem fine tunning.

## Baseline Final

O modelo Baseline final escolhido foi o que utiliza o modelo base VGG19, sendo que o tamanho da imagem escolhida foi 256x256, esta é a configuração:

 ![](/api/attachments.redirect?id=8f5e4f8c-d56d-4af7-878e-2142e277e93c " =464x317")

#### Métricas em cima do conjunto de validação:

| **Métrica** | **Valor nível imagem** | **Valor nível imóvel** |
|----|----|----|
| accuracy | 0.32293 | 0.53846 |
| recall | 0.26686 | 0.28269 |
| precision | 0.25467 | 0.26727 |
| f1_score | 0.25467 | 0.26910 |

Matriz de confusão:

 ![](/api/attachments.redirect?id=71597f87-be21-4fd2-9dd7-fbbf35640500)

* Existe apenas 1 SIM nesse conjunto, 3 imagens o modelo acertou, mas 9 disse ser JR.
* Os JR ele acertou bem.
* Ele acertou a maioria dos imóveis SUP, mas também disse que algumas imagens eram JR e por algum motivo MASTER.
* Os TOP ele não pegou, deu predict em JR, SUP e MASTER.
* Ele até acertou algumas imagens em MASTER, mas a maioria disse ser JR.

#### Métricas em cima do conjunto de teste:

| **Métrica** | **Valor nível imagem** | **Valor nível imóvel** |
|----|----|----|
| accuracy | 0.38068 | 0.43589 |
| recall | 0.27232 | 0.35666 |
| precision | 0.25388 | 0.27032 |
| f1_score | 0.24918 | 0.29790 |

Matriz de confusão:

 ![](/api/attachments.redirect?id=7a03c58a-faae-4b59-b6d1-3339e75b5d7b)

Se comportou de forma parecida com no conjunto de validação, sendo que uma diferença que notei foi que conseguiu dar predict em 3 MASTER, mas também deu muitos predict em JR.

## Possíveis Melhorias

* Aumentar o dataset: Existem poucos exemplos de SIM no dataset, isso faz com que o modelo tenha dificuldade em predizer eles (em todos os casos o predict final foi em JR). Os exemplos encontrados na internet também usam mais de 50k imagens para transfer learning.
* O modelo errou várias das imagens SUP e não deu predict em imóveis TOP. Tentar entender o motivo disso (se o problema está nas imagens ou no modelo escolhido).

Além disso, também foram feitos outros testes que faziam sentido, mas dentro do período de tempo não funcionaram muito bem. As vezes seria interessante tentar de novo, eles foram descritos no card: <https://seazone.atlassian.net/jira/software/c/projects/DS/boards/22?selectedIssue=DS-266>. 

* **Ordinal classification:** Fazer o modelo entender que SIM < JR < SUP < TOP < MASTER).
* **Class Weights:** Atribuir pesos maiores para as classes menos representativas no conjunto de dados durante o treinamento.
* **Fine Tunning:** Durante os testes o processo de fine tunning não melhorou o modelo como era do esperado, tentar entender o motivo e melhorar esse aspecto.


# Testes com IA Generativa

Uma segunda abordagem pensada foi de usar IA Generativa (como ChatGPT e Gemini) para analisar as imagens e automaticamente criar features para ajudar na categorização

## GCP

Dentro do GCP existe o Gemini, sendo que há 2 serviços que servem como um Front para o Gemini, tem o Google AI Studio e o Vortex AI

#### Google AI Studio

Esse aqui é bom para desenvolvimento, ele é mais rápido e fácil de usar. Ele também é mais barato que o outro.

custos: <https://ai.google.dev/pricing?hl=pt-br&authuser=1#1_5flash>

Os custos são por TOKEN, sendo que uma imagem dá uns 250-300 tokens dependendo.

#### Vortex AI

Esse é bom para criar modelos que vão ser scalados para múltiplos usuários, as opções de segurança e compliance dele também são melhores. Ele também ofereçe uma customização maior para fazer o fine tuning do modelo, **mas ele é mais caro**.

Custos: <https://cloud.google.com/vertex-ai/generative-ai/pricing#google_models>

O custo dos textos (prompt) são cobrados por caractere, enquanto que o custo de imagem é fixo.

#### Opções de modelo

Nos dois serviços é possível **criar e salvar prompts personalizados.** Depois, é só rodar um script que chama o endpoint do respectivo serviço e gerar a resposta.

Foram feitos alguns testes inciais em código usando os dois serviços, eles são bem tranquilos de usar.

Uma outra forma de fazer é através do **fine tuning**. Podemos criar um dataset personalizado (com pelo menos 100 entradas, mas acho que o ideal seria ter de 500-1000), nele especificamos a imagem + o prompt e colocamos o resultado esperado, ou seja, algo como {'room': 'bedroom', 'features': \[{'TV': 'modern'}, {'bed': 'modern'}, {'curtains': 'modern'}, {'nightstand': 'standard'}, {'lamp': 'standard'}\]}.

Vantagens do fine tuning:

* Reduz os custos da inferência, visto que uma vez treinado é possível diminuir boa parte do texto do prompt de entrada
* O modelo aprende melhor o dominio e sintaxe esperada do problema, então podemos especificar para ele o que seria uma geladeira simples ou moderna, por exemplo.

Tanto o **Google AI Studio** como o **Vortex AI** possuem opções de fine tuning, mas o Vortext AI parece ter mais opções de modelos base para escolhermos, além de parecer mais customizavel.

#### Prompt

Foi criado um Prompt inicial para o modelo **Gemini 1.5 Flash 002**

```none
You are a property quality describer. You will be reciving images of properties being listed to rent (house, apartament, hotel) and your goal is to identify and determine quality features of the objects identified, like the furniture, appliances, bathroom fixtures, air conditioning, electronics and other important features for property evaluation like pool and so on.

The qualities levels can be simple, standard or modern.

You also rate the outside view. If they view is visible in the pic, then you can rate it to be good or bad depending if you can see a beach or not.

It is also important to specify if the pool, grill, gym and so on are for public or private use, since they are important for property evaluation.

Sometimes the images will have nothing to do with the property evaluation, so in this cases the quality features should be disregarded. If a feature is missing from the image it should also be disregarded.

Your response must be in a JSON format where room is the name of the room and features are a list of objects being measured with their quality level and if the features are a pool, grill or gym, specify if they are for public or private use. If the images have nothing to do with the property evaluation then return 'bad_image': True and explain why.

if the image is important, you ignore the room and use this JSON schema:
[{'room': str, 'features': list[dict [str]]}]
example: 
[{'room': 'bedroom', 'features': ['TV': 'modern', 'bed': 'simple']}, {'room': 'kitchen', 'features': ['fridge': 'standard ']}]
[{'room': 'outside', 'features': ['pool': 'modern', 'use': 'private']}]

if the image is not important, use this JSON schema:
[{'bad_image': True, 'reason': str}]
```

Ele faz o seguinte:

* Ele detecta que tipo de quarto a imagem é (sala, cozinha, exterior, etc)
* Ele identifica features na imagem (sofa, geladeira, etc) e atribui um nível de qualidade a elas (simple, standard e modern)
* Caso haja vista para fora, ela será good ou bad dependendo se dá pra ver o mar ou não
* Áreas que podem ser públicas como piscina o modelo também traz se elas são públicas ou privadas
* Caso a imagem não tenha nada a ver com a avaliação da propriedade (como uma foto da praia), então a API retorna que a imagem é ruim e diz o motivo dela ser ruim
* O prompt especifica o formato esperado do json de saída

## Gemini VS ChatGPT

O modelo escolhido do Gemini foi o **Gemini 1.5 Flash 002** e no ChatGPT foi o **ChatGPT 4o**

A ideia da comparação foi, a partir do mesmo prompt, comparar o resultado dentre Gemini x ChatGPT x Verdade.

Foi criado uma planilha de comparação: [acertividade_features_ia](https://docs.google.com/spreadsheets/d/1GysH01e9jrmswaWKhgatU85PwsJRlOOU-o0RYYyCjSs/edit?gid=1962037225#gid=1962037225)

Foram selecionadas 59 imagens, a ideia foi pegar pelo menos um pouco de cada strata e pegar um pouco de cada tipo de quarto (room_title) e também pegar umas imagens nada a ver (como imagens de praia ou restaurante) e ver se o modelo consegue identificar todos os casos.

Cada uma das imagens foi analisada e foi criado a coluna qualidade_humana onde um humano classificou **cada mobilia** **ou objeto de interesse** encontrado na imagem.

A porcentagem de cada strata e de cada qualidade de mobilia se encontra abaixo:

 ![](/api/attachments.redirect?id=0988507c-82f9-4a4f-b8a1-4732aa024bb2)

### Gemini

Foi feito um script para rodar a categorização de cada mobilia de forma assincrona.

Para executa-lo é necessário três coisas:

* Baixar as biblioteca do google e configurar as credenciais no terminal
* Baixar o csv chosen_pics.csv presente na **[aba chosen_pics da planilha](https://docs.google.com/spreadsheets/d/1GysH01e9jrmswaWKhgatU85PwsJRlOOU-o0RYYyCjSs/edit?gid=624576225#gid=624576225)**
* Baixar todas as imagens usada dentro duma pasta local, o nome da pasta local tem que ser upload. [Link das imagens para baixar](https://drive.google.com/drive/u/1/folders/1R6b8MkXr-HKrwn3vciB6jgvFTE0OJGNV)
* Criar uma chave the API com permissão de usar o Gemini e coloca-la num arquivo .env

```python
import google.generativeai as genai
import asyncio
import pandas as pd
import os
from PIL import Image
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.environ["API_KEY"])

# Create the model
generation_config = {
  "temperature": 0,
  "top_p": 0,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "application/json",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash-002",
  generation_config=generation_config,
  system_instruction="You are a property quality describer. You will be reciving images of properties being listed to rent (house, apartament, hotel) and your goal is to identify and determine quality features of the objects identified, like the furniture, appliances, bathroom fixtures, air conditioning, electronics and other important features for property evaluation like pool and so on.\n\nThe qualities levels can be simple, standard or modern.\n\nYou also rate the outside view. If they view is visible in the pic, then you can rate it to be good or bad depending if you can see a beach or not.\n\nIt is also important to specify if the pool, grill, gym and so on are for public or private use, since they are important for property evaluation.\n\nSometimes the images will have nothing to do with the property evaluation, so in this cases the quality features should be disregarded. If a feature is missing from the image it should also be disregarded.\n\nYour response must be in a JSON format where room is the name of the room and features are a list of objects being measured with their quality level and if the features are a pool, grill or gym, specify if they are for public or private use. If the images have nothing to do with the property evaluation then return 'bad_image': True and explain why.\n\nif the image is important, you ignore the room and use this JSON schema:\n[{'room': str, 'features': list[dict [str]]}]\nexample: \n[{'room': 'bedroom', 'features': ['TV': 'modern', 'bed': 'simple']}, {'room': 'kitchen', 'features': ['fridge': 'standard ']}]\n[{'room': 'outside', 'features': ['pool': 'modern', 'use': 'private']}]\n\nif the image is not important, use this JSON schema:\n[{'bad_image': True, 'reason': str}]",
)

async def generate_request(img: str) -> str:
	r = await model.generate_content_async(["Describe the image", Image.open(img)])
	response_dict = {}
	response_dict['response'] = json.loads(r.text)
	response_dict['image_path'] = img
	response_dict['prompt_token_count'] = r.usage_metadata.prompt_token_count
	response_dict['candidates_token_count'] = r.usage_metadata.candidates_token_count
	response_dict['total_token_count'] = r.usage_metadata.total_token_count
	return response_dict

chosen_pics = pd.read_csv('chosen_pics.csv')
images = [f'upload/{image}' for image in chosen_pics['image_name']]
jobs = asyncio.gather(*[generate_request(img) for img in images], return_exceptions=True)
results = await jobs
```

Parâmetros usados:

* top_k: 40, esse é o default
* top_p e temperatura: 0, a ideia é fazer com que todas vez que seja feito o request o Gemini retorne o mesmo resultado, então por isso esses são zero.

### ChatGPT

Mudanças em relação ao Gemini:

* O request foi feito de forma manual, ou seja, não foi usado a API.
* O prompt mudou um pouco para gerar o resultado em csv facilitando a comparação na planilha. Ele também mudou para ser feito em batches de 10 o que reduziria o tempo nosso de colocar os resultados para a planilha.

```python
Quero que tu use o prompt a baixo: 

"You are a property quality describer. You will be reciving images of properties being listed to rent (house, apartament, hotel) and your goal is to identify and determine quality features of the objects identified, like the furniture, appliances, bathroom fixtures, air conditioning, electronics and other important features for property evaluation like pool and so on.

The qualities levels can be simple, standard or modern.

You also rate the outside view. If they view is visible in the pic, then you can rate it to be good or bad depending if you can see a beach or not.

It is also important to specify if the pool, grill, gym and so on are for public or private use, since they are important for property evaluation.

Sometimes the images will have nothing to do with the property evaluation, so in this cases the quality features should be disregarded. If a feature is missing from the image it should also be disregarded.

Your response must be in a JSON format where room is the name of the room and features are a list of objects being measured with their quality level and if the features are a pool, grill or gym, specify if they are for public or private use. If the images have nothing to do with the property evaluation then return 'bad_image': True and explain why.

if the image is important, you ignore the room and use this JSON schema:
[{'room': str, 'features': list[dict [str]]}]
example: 
[{'room': 'bedroom', 'features': ['TV': 'modern', 'bed': 'simple']}, {'room': 'kitchen', 'features': ['fridge': 'standard ']}]
[{'room': 'outside', 'features': ['pool': 'modern', 'use': 'private']}]

if the image is not important, use this JSON schema:
[{'bad_image': True, 'reason': str}]"

e usando este prompt acima, obedecendo toda as regras acima. 
E no final transforme o JSON criado em um .csv nesta configuração a baixo... 

id_foto	Comodo	Feature	Qualidade_dada
bbf2e650-b2df-4a50-b075-ba48b74c1aa6.jpeg	living_room	sofá	padrão
bbf2e650-b2df-4a50-b075-ba48b74c1aa6.jpeg	living_room	televisão	padrão
bbf2e650-b2df-4a50-b075-ba48b74c1aa6.jpeg	living_room	mesa	padrão
bbf2e650-b2df-4a50-b075-ba48b74c1aa6.jpeg	kitchen	armários	padrão
bbf2e650-b2df-4a50-b075-ba48b74c1aa6.jpeg	dining_room	mesa	padrão
bbf2e650-b2df-4a50-b075-ba48b74c1aa6.jpeg	dining_room	cadeiras	padrão

Note que no .csv final, a feature precisa vir em lingua portuguesa, o comodo em ingles... mantenha o padrão final de linguagem. 

O prompt deve ser aplicado nas fotos que estão em anexo. 

Tente identificar o máximo de mobilias que conseguir
```

* Não foi criado um chat novo toda vez que o request era feito, então o chatGPT tentava responder com o contexto da conversa toda fazendo ele se perder um pouco.

Todas as mudanças citadas acima foram feitas para acelerar o processo de comparação, mas vale comentar que podem ter afetado um pouco negativamente o desempenho do modelo

### Comparação

Vale comentar que nessa comparação, 3 imagens não foram usadas no chatGPT, e3335e74-5a17-47fa-b747-bfde9214f58f.jpeg, dff9334a-d705-4de2-96df-3b5a36453287.jpeg e 2a2dbd9b-23de-4517-9803-654b71d61ca8.jpeg.

Elas equivalem a apenas 10 features (3.2%), então por isso não deve afetar muito o resultado da analise final.

O motivo delas estarem faltando foi só porque durante os testes o chatGPT não retornou elas e isso passou batido.

#### Primeira Etapa

Primeiro foi visto a porcentagem de cada tipo de qualidade. Nulo é quando a IA não encontrou uma feature que o humano encontrou.

 ![](/api/attachments.redirect?id=a518be3c-995f-4625-86d6-4ebbce5d63bd)

* Apesar de a categoria Master ser a Strata que mais aparece nas fotos, na classificação humana a qualidade Moderno (8%), associada à categoria Master, aparece significativamente menos do que Standard (46%) e Simples (36%). Isso sugere uma possível inconsistência na definição de Master ou na interpretação dos critérios pelos humanos.
* O modelo Geminin teve 30% de valores nulos na detecção de qualidade, enquanto o ChatGPT apresentou 55%. Isso indica que o Geminin parece identificar mais objetos ou características alinhadas com a percepção humana do que o ChatGPT.
* O Geminin demonstrou uma dominância na classificação Standard (47%), valor próximo à proporção encontrada na avaliação humana (46%). Essa similaridade pode indicar que o domínio de Standard é um reflexo do dataset analisado. No entanto, o forte desbalanceamento pode causar problemas em modelos futuros, como enviesamento ou dificuldade para diferenciar subclasses. Uma solução seria dividir Standard em subcategorias (ex.: standard_low, standard_high).
* O ChatGPT apresentou uma dominância marcante na detecção de Moderna, classificando mais do que o dobro de Moderna em relação às categorias Standard e Simples. Isso sugere um possível viés causado pelo prompt usado, que pode ser menos criterioso na avaliação do mobiliário. Seria interessante testar variações no prompt para confirmar a hipótese.

#### Segunda Etapa

Aqui foram definidos os cenários de Avaliação.

Segue as definições… 


1. **Correspondência Direta**: Tanto o humano quanto a IA forneceram a mesma classificação.
2. **Discordância**: Humano e IA forneceram classificações diferentes.
3. **Humano Não Detectou (Casos 'Existe')**: A IA detectou um item que o humano não percebeu, e é confirmado que o item existe.
4. **Detecção Falsa**: A IA detectou um item que o humano não percebeu, e não há indicação de 'existe'.

**Tratando os Casos 'Existe'**

* **Casos 'Existe'**: Quando a IA detecta um item que o humano não percebeu, mas que de fato existe.

**Definindo Métricas:**

* Como usamos modelos para classificar as mobilias, acredito que as metricas padrão usadas para modelos de classificação se encaixam bem, com isto foi usadas as classicas:
  * Acurácia
    * **Considerações**:
      * Excluir os casos 'Existe'
  * Precisão, Recall e F1-Score
    * **Considerações**:
      * **Verdadeiros Positivos (VP)**: IA e humano atribuíram a mesma classificação.
      * **Falsos Positivos (FP)**: A IA atribuiu uma classificação quando o humano não o fez ('Nulo' ou 'Nada a Ver'), e não há indicação de 'Existe'.
      * **Falsos Negativos (FN)**: O humano atribuiu uma classificação, mas a IA não.
      * **Verdadeiros Negativos (VN)**: Tanto a IA quanto o humano não atribuíram uma classificação ('Nulo' ou 'Nada a Ver').

**Metricas calculadas:**

* Acurácia:

  ![](/api/attachments.redirect?id=3e793ae8-80f3-420c-8928-ebf0c46903bd)

Foi gerado considerando quando o modelo não classificou a feature definida pelo humano e excluindo estas previsões, para medirmos a acertividade do modelo quando ele encontra a mesma feature do humano.

Vemos que em ambos os casos a acuracia não foi alta, porém o GEMININ teve um resultado muito melhor do que o ChatGPT, obtendo uma acuracia com quase duas vezes maior.

* Precision, Recall , f1-score

O Geminin obteve uma media em todos as classificações resumida a baixo:

* precision: 0.49
* recall: 0.41
* f1-score: 0.36

Enquanto a media obtida nas classificaçoes de qualidade do ChatGPT foi:

* precision: 0.42
* recall: 0.41
* f1-score: 0.28

Vemos novamente que ambos tiveram um desempenho não muito alto, porém em todas as métricas o Geminin obteve melhores resultados.

Gráficos:

 ![](/api/attachments.redirect?id=797e9103-f512-4c38-b6ad-941e93efd5c8)

Por ultimo foi feita uma Matriz confusão, segue a baixo:

 ![](/api/attachments.redirect?id=44f67e91-c6c9-451d-848e-5b7cdf118121)

* Geminin:
  * Obteve um grande acerto na qualidade Standard, porém com muitos features detectadas pelo humano que o modelo não achou, ficando com 47 nulos;
  * Na qualidade moderna, percebemos que o modelo não conseguiu capturar de acertiva com a avaliação humana, considerando mais standards aqui de forma errada. O que demonstra que o modelo ficou bem inviesado em considerar mobilias como standard que era a maioria das mobilias neste dataset.
  * O modelo não conseguiu qualificar de forma eficaz uma vista ruim, tendo apenas um acerto, porém a maioria das vezes ele nem classificou a vista ruim, tendo dois casos que classificou a vista ruim como boa;
  * O modelo identificou divesos moveis que não existiam;
  * O modelo tem dificuldade de identifica mobilias Simples, novamente ficando enviesado a classificar a maioria como standard;
  * Conseguiu capturar a metade das vezes que a imagem não fazia sentido;
  * Obteve bom acerto para identificar vista boa, porém o dataset só tinha duas, que é uma baixa amostragem.
* ChatGPT
  * Comparado com o Geminin, o modelo conseguiu desempenhar melhor e identificar mobilias modernas e simples. Se destacando na identificação das Modernas. Porém parece um pouco enviesado, pois identificou muitas modernas quando eram standard;
  * O modelo identificou bem menos mobilia do que o Geminin o que fica claro com o grande numero de nulos em todas as qualidades (talvez possa ser por causa das mudanças na forma como o request foi feito)

#### Conclusões

* Ficou claro que apesar de estar longe do ideal, o Geminin usando um prompt quase idêntico teve resultados melhores do que o ChatGPT e considerando que já temos creditos para usar podemos considerar que este estudo validou o uso do Geminin provando que tem um grande potêncial ao obter melhor desempenho do que a IA Generative mais usada atualmente no mercado.
* Porém temos muito trabalho em melhorar o modelo, tanto melhorando o prompt como tentando usar treinamento que a Geminin permite, algumas tentativas que poderm ser testadas nas próxima etapa:
  * Ter mais divisões de qualidade, vimos que mesmo na classificação humana a categoria standard ficou muito dominante tendo um desbalanceamento de classes, sugestão de termos 4 classes, com nomes diferentes do que usamos para categorização, para não causar confusão, uma ideia: economica, padrao, premium, luxo.
  * Treinar o Geminin com imagens rotuladas por humanos, para ele conseguir entender melhor qual a qualidade é esperada para cada mobilia;
  * Especificar melhor o prompt, detalhando mais o que seria cada mobilia;
  * Definir as mobilias que o modelo deve encontrar, predefinindo todas as features, usar de inicio as principais, depois podemos ir aumentando caso sentimos falta de alguma.
    * Sofa, TV, mesa, lustre, geladeira, armario, fogão, bancada, pia, coifa. É importante levantar só as principais para conseguirmos rotular e mandar de exemplo para o modelo aprender as classificações.
  * Fazer testes separando as features em tipo de feature, como mobilia, decorações, eletrodomésticos, acabamentos, etc

# Criação de Features Gemini

Todos os testes realizados podem ser encontrados no card: <https://seazone.atlassian.net/jira/software/c/projects/DS/boards/22?selectedIssue=DS-254>

Os scripts também se encontram no repositório: <https://github.com/seazone-tech/Util-dados>

## Prompt Qualidade

O prompt por qualidade é uma tentativa de melhorar os leveis de qualidade explorados nos tópicos anterior. 

```none
You are a property quality describer. You will be reciving images of properties being listed to rent (house, apartament, hotel) and your goal is to identify and determine quality features of the objects identified, like the furniture, appliances, bathroom fixtures, air conditioning, electronics, finishing, decoration and other important features for property evaluation like pool and so on.

The types of features you identify can be one of the following: air_conditioning, bed, bench, chair, cabinet, coffee_machine, table, couch, countertop, curtains, fridge, lights, microwave, mirror, nightstand, ottoman, painting, playground, pool, range_hood, rug, shelf, shower, sink, stove, toilet, tv, tv_stand, view, gym, jacuzzi, garden, floor, walls, washing_machine.

The qualities levels can be Economy, Basic, Mid-Range and Luxury.
1. Economy: This level represents the lowest quality, often featuring very basic, cheaply made furniture, possibly showing signs of wear and tear even when new. Materials are likely to be very low-grade, and functionality may be compromised.
2. Basic: This level represents furniture that is functional but lacks in aesthetics, durability, and craftsmanship. Think inexpensive materials, mass-produced designs, but a step up from Economy in terms of durability and appearance.
3. Mid-Range: Furniture in this category offers a step up in quality and design. Materials are generally better (e.g., solid wood instead of particleboard), construction is more durable, and aesthetics are more refined.
4. Luxury: This represents the highest tier, featuring exceptionally high-quality materials, intricate detailing, and often bespoke or custom-made pieces. Think heirloom-quality furniture with significant monetary and aesthetic value.

You also rate the outside view. If they view is visible in the pic, then you can rate it to be Bad or Good.
1. Good: You can see a beach or lake from the view
2. Bad: You cannot see a beach or lake from the view

Sometimes the images will have nothing to do with the property evaluation, so in this cases the quality features should be disregarded. Always try to find and return all the features you find in the picture, only if a feature is missing from the image you should disregarded it. Always try to return the wall and floor quality if they are visible in the picture.

Your response must be in a JSON format where room is the name of the room and features are a list of objects being measured with their quality level. If the images have nothing to do with the property evaluation then return 'bad_image': True and explain why.

if the image is important, use this JSON schema:
[{'room': str, 'features': list[dict [str]]}]
example: 
* [{'room': 'bedroom', 'features': [{'tv': 'Basic'}, {'bed': 'Mid-Range'}, {'view': 'Bad'}]}, {'room': 'kitchen', 'features': [{'fridge': 'Mid-Range'}]}]
* [{'room': 'outside', 'features': [{'pool': 'Luxury'}, {'view': 'Good'}]}]

if the image is not important, use this JSON schema:
[{'bad_image': True, 'reason': str}]
```

**Mudanças**:

* As qualidades podem ser Economy, Basic, Mid-Range ou Luxury, inclusive é especificado no prompt o que cada uma é.
* Retornar a qualidade do piso e parede.
* É especificado quais features ele vai retornar air_conditioning, bed, bench, chair, cabinet, coffee_machine, table, couch, countertop, curtains, fridge, lights, microwave, mirror, nightstand, ottoman, painting, playground, pool, range_hood, rug, shelf, shower, sink, stove, toilet, tv, tv_stand, view, gym, jacuzzi, garden, floor, walls, washing_machine.
* Não é mais retornado se a piscina é pública ou privada, visto que isso não estava sendo usado nas validações e aumentava a complexidade do prompt

**Conclusões**:

* Testando nas 59 imagens selecionadas, nenhuma feature ficou Economy, então é necessário achar uma forma melhor de regular essas divisões
* Não são todos os objetos que fazem sentido serem dividos em 4 níveis de qualidade. 

## Prompt Score

A ideia do prompt score é fazer o gemini retornar um número de 0 a 100, então se definirmos os requisitos para ser um 0 e para ser um 100 o gemini consegue dar um score justo com base nisso. Isso acaba com o problema anterior de algumas features não serem possíveis de dividir em 4 níveis de qualidade.

### Score por objeto

A ideia desse score é que, para cada feature (tv, ar condicionado, fogão, etc), definir as caracteristicas que os tornariam 0, 50 e 100, para então deixar o geminir dar um score justo para elas. Depois, podemos pegar esse scores e atribuir algum peso para cada uma e inferir a strata do imóvel.

**Detalhe:**

* Não está levando em conta áreas de recreação (como piscina), nem acabamentos (piso e parede) ou a qualidade de iluminação da foto.
* O prompt olha a vista e, se tiver vista para o mar, é retornado 1, caso contrário, é retornado 0.

```none
You are a property quality describer. You will be reciving an image of a property being listed to rent (house, apartament, hotel) and your goal is to identify and determine a quality score for the objects identified. The list of objects you are suposed to find are: air_conditioning, bed, bench, chair, cabinet, coffee_machine, table, couch, countertop, curtains, fridge, lights, microwave, mirror, nightstand, ottoman, range_hood, rug, shelf, shower, sink, stove, toilet, tv, tv_stand, washing_machine.

If the image is important, then your goal is to find features in the image and determine a quality score for each of them. The score is a continuous number that goes from 0 to 100. The features you need to identify along with their basic score descriptions are listed below, so anything below the 0 description will be considered a 0 score and anything above the 100 score will be considered a 100, but if something is in between, you use your intelligence to interpolate the correct quality score.

air_conditioning
* 0: Small, older unit, struggles to cool effectively, might be noisy
* 100: Central AC, seamlessly integrated, quiet and efficient, smart thermostat

bed
* 0: Basic metal frame, simple mattress, showing signs of wear
* 50: Wooden/upholstered frame, comfortable mattress, standard size
* 100: Large, luxurious frame, premium mattress, adjustable settings, high-quality linens

bench
* 0: Simple, repurposed item serving as a bench
* 50: Functional bench, basic upholstery/simple wood design
* 100: Stylish, well-designed, high-quality materials/upholstery

chair
* 0: Basic, unpadded, mismatched/showing age
* 50: Functional, comfortable, simple upholstery/solid construction
* 100: Designer chair, ergonomic, high-quality materials, stylish

cabinet
* 0: Basic, freestanding, limited storage, simple hardware
* 50: Functional, adequate storage, possible wear
* 100: Built-in, custom, ample storage, soft-close, high-end hardware

coffee_machine
* 0: Basic drip, stained/heavy use
* 50: Standard, some additional features (e.g., timer)
* 100: High-end espresso machine, multiple settings/features

table
* 0: Small, basic, showing wear/instability
* 50: Functional, adequate size, simple design
* 100: Large, well-crafted, high-quality materials, centerpiece

couch
* 0: Basic, worn upholstery/simple frame
* 50: Comfortable, decent upholstery, sturdy frame
* 100: Large, luxurious, premium upholstery, comfortable seating, stylish

countertop
* 0: Basic laminate, visible seams/wear
* 50: Solid surface, good condition
* 100: High-end (granite/quartz), seamless, stylish

curtains
* 0: Minimal, thin/ill-fitting
* 50: Functional, adequate light/privacy control
* 100: High-quality, custom, enhance aesthetics/light control

fridge
* 0: Simple fridge, no divisions with the freezer, the paiting might be old. A minibar is always a simple fridge.
* 100: Modern fridge, triplex, can make ice automatically, the color is darker.

lights (lamp, chandelier)
* 0: Basic, bare bulb, minimal illumination
* 50: Functional, adequate lighting
* 100: Designer fixtures, ambiance, highlight features

microwave
* 0: Small, basic, limited features
* 50: Standard, adequate power/functionality
* 100: High-end, advanced features (convection, sensor)

mirror
* 0: Small, simple, basic frame
* 50: Functional, adequate size, decorative frame
* 100: Large, stylish, high-quality frame, enhances aesthetics

nightstand
* 0: Basic, small surface, repurposed item
* 50: Functional, drawer/shelf storage
* 100: Stylish, ample storage, complements furniture

ottoman
* 0: Simple, basic, showing wear
* 50: Functional, comfortable upholstery, sturdy frame
* 100: Stylish, premium upholstery, storage, complements décor

range_hood
* 0: Basic, recirculating, minimal ventilation
* 50: Standard, adequate ventilation/lighting
* 100: High-end, powerful ventilation, integrated lighting, stylish

rug
* 0: Small, basic, wear/fading
* 50: Functional, adequate size/quality
* 100: Large, high-quality, premium materials, warmth/style

shelf
* 0: Basic, freestanding, limited storage
* 50: Functional, adequate storage
* 100: Built-in/custom, ample storage, integrated lighting, stylish

shower
* 0: Basic stall, simple showerhead, limited features
* 50: Functional, standard showerhead, adequate pressure
* 100: Luxurious, multiple showerheads, rainfall, high-end fixtures

sink
* 0: Basic, simple fixtures
* 50: Functional, standard fixtures, good condition
* 100: Stylish, high-end fixtures (vessel/waterfall)

stove
* 0: Basic, limited features, simple controls
* 50: Functional, standard features, adequate burners
* 100: High-end, advanced features (convection, smooth top)

toilet
* 0: Basic, standard functionality
* 50: Standard, good condition, efficient flushing
* 100: High-efficiency, advanced features (dual flush, heated seat)

tv
* 0: An old tube tv, small TV is also a sign of a bad score.
* 50: 50: A not soo thin flat-screen TV, but also smaller (about 32 inches). 
* 100: A new looking thin TV, usually hung on the wall, larger than 42 inches.

tv_stand
* 0: Basic, small surface, repurposed item
* 50: Functional, storage for components
* 100: Stylish, ample storage, cable management, complements system

washing_machine.
* 0: Basic top-load, limited features
* 50: Standard, adequate capacity, basic settings
* 100: High-efficiency front-load, advanced features (steam, multiple cycles)

You always try to follow this descriptions when giving a score to a feature, you also always try to find and return all the features you find in the image, but you do not create new features, so if the feature is missing from the image you should disregard it. If the feature is missing you do not give it a score.

You also rate the outside view. If the picture is taken from inside the property, but you can see the outside from a window or balcony, then you can rate it to be 1 or 0. If the view is not present in the picture you can ignore it.
* 1: You can see a beach or lake from the view
* 0: You cannot see a beach or lake from the view

If the image is not important to the property evaluation (like it was taken outside the property), then you will return the reason why as in this JSON schema dict[str, str]:
* example1: {'bad_image': 'The image is bad because of this reason'}

If the image is important, then your response must be in a JSON format representing a dictionary where the key is the feature name and the value is the score quality. If the image has two of the same feature (like two tvs) then add a "-" and a number to differentiate them, like "tv-1" and "tv-2".

Use this JSON schema: dict[str, int]
* example1: {'tv': 50, 'bed': 70, 'view': 0, 'fridge': 10}
* example2: {'sink': 80, 'view': 1}
* example3: {'light-1': 10, 'stove': 50, 'light-2': 80}
```

**Resultado:**

Foi calculado a média dos scores de cada feature das imagens do imóvel. Então, se um imóvel possuí 10 imagens, é primeiro obtido o score de cada feature de todas as imagens e esse score é somado e dividio pelo número total de features.

Se a vista for 1, então ela entra como um valor de 100 no cálculo, caso contrário, ela não entra no cálculo (vista 0 não penaliza a média)

 ![](/api/attachments.redirect?id=6fa877db-f97c-41a4-a92b-8417c0f69666 " =1064x449")

### Score por tipo

A ideia do score por tipo é dar um score para cada tipo de avaliação da propriedade, então em vez do gemini encontrar os objetos da imagem, ele atribui um score para os Acabamentos, Eletronicos, Móveis, Decorações, Iluminação e Espaço.

O score novamente vai de 0 a 100 e é explicado o que os scores de 0, 50 e 100 representam.

**Detalhes:**

* Não há menção da vista que o imóvel possuí.
* Se uma imagem não faz sentido para a avaliação, o gemini é instruido a ignorar ela e retornar a imagem com problema e o motivo do problema.
* A ideia aqui é usar TODAS as imagens do imóvel de uma só vez, então fazer um request por imóvel.

```none
As a property quality describer, your role is to evaluate and determine a quality score for some features inside of a property being listed to rent (house, apartament, hotel).

You will be receiving images of the property, and the list of features you are suppose to give a score are:
* Finishes: Quality of floors, walls, ceilings, coverings and architectural details.
* Electronics: Quality of household and electronic appliances, old, modern, large, functional, fit well into the environment
* Furniture: Quality, style, state of conservation and harmony of furniture and the environment.
* Decoration: Presence of decorative elements, style, combination of colors and textures.
* Lighting: Quality of natural and artificial lighting, presence of lamps or lighting details.
* Space: Furniture arrangement, feeling of spaciousness, functionality of the space.

The score is a number that goes from 0 to 100, you need to follow the examples bellow and give a score for each of the features above.
* 0: Low quality environment, with simple or worn finishes, old appliances and small electronics, basic furniture or in poor condition, non-existent or disharmonious decoration, insufficient lighting and disorganized space.
* 50: Medium quality environment, with adequate finishes, somewhat new appliances and functional electronics, functional furniture in good condition, simple but coherent decoration, satisfactory lighting and good organization of the space.
* 100: High quality environment, with high standard finishes, very modern appliances and electronics that adapt well to the environment, designer or luxury furniture in excellent condition, sophisticated and harmonious decoration, planned lighting and optimized and functional space.

Consistency and following the rules are top priorities, so you will always return a quality score for all the features mentioned following the rules, but feel free to interpolate the score between 0 and 100.

You also need to watch for images taken outside of the property or that have nothing to do with the property evaluation, because those are not important and you do not consider them in your evaluation when scoring.

Your response must be in a JSON format representing a dictionary where the key is the feature name and the value is the score quality.
If you detect an image that has nothing to do with the property evaluation you return it in the 'BadImage' key and the value is a dictionary where they key is the name of the image and the value is the reason why the image is not important.

Response examples:
* example1: {'Finishes': 50, 'Electronics': 20, 'Furniture': 40, 'Decoration': 80, 'Lighting: 100, 'Space': 60}
* example2: {'Finishes': 20, 'Electronics': 0, 'Furniture': 50, 'Decoration': 40, 'Lighting: 40, 'Space': 100, 'BadImage': {'image1.png': 'The image shows a street sign'}}
* example3: {'Finishes': 80, 'Electronics': 100, 'Furniture': 80, 'Decoration': 60, 'Lighting: 20, 'Space': 30, 'BadImage': {'image14.png': 'The image shows a street sign, 'image20.png': 'The image only shows a beach'}}
```

**Resultado:**

O score final foi apenas a soma de todos os scores. Os imóveis utilizados para o teste foram ordenados pelo valor final e, nessa ordenação, o resultado final fez sentido.

* O primeiro imóvel crashou por causa do tamanho do request, isso ainda não tinha sido corrigido no momento do print.
* Os scores dos SIM, JR e SUP estão fazendo bastante sentido ao ordenar. O problema são os 2 MASTER e aquele SUP em segundo lugar. Esses 2 MASTERs não possuem fotos tão boas e o SUP que está em segundo possuí fotos incríveis.
* Outro problema é que os scores dos SIM estão relativamente altos, eles deveriam estar mais próximos de 0.

 ![](/api/attachments.redirect?id=5f0f19a5-c215-44d2-929c-a5c0986f2167 " =1177x437")

## Fine Tuning

Apesar de ser possível fazer o fine tuning pelo Google AI Studio, hoje (2024-12-03), não é possível usar as versões mais recentes do gemini (gemini-1.5-flash-002) e também não é possível colocar imagens no Dataset de treino.

Por esses motivos, foi optado em usar o VERTEX AI para fazer o fine tuning.

### Dataset de treino

O primeiro passo é montar o dataset que será usado pro treinamento, ele precisa se basear no seguinte template json (esse template representa apenas 1 exemplo):

```json
{
    "systemInstruction": {
        "role": "",
        "parts": [
            {
                "text": "You are an image describer"
            }
        ]
    },
    "contents": [
        {
            "role": "user",
            "parts": [
                {
                    "fileData": {
                        "mimeType": "image/jpeg",
                        "fileUri": "gs://cloud-samples-data/ai-platform/generative_ai/gemini-1_5/image/longcap100/91.jpeg"
                    }
                },
                {
                    "text": "Describe this image in detail that captures the essence of it."
                }
            ]
        },
        {
            "role": "model",
            "parts": [
                {
                    "text": "A person wearing a pink shirt and a long-sleeved shirt with a large cuff, has their hand on a concrete ledge. The hand is on the edge of the ledge, and the thumb is on the edge of the hand. The shirt has a large cuff, and the sleeve is rolled up. The shadow of the hand is on the wall."
                }
            ]
        }
    ]
}
```

* systemInstruction: Possuí as instruções do sistema usadas no prompt
  * A "role" aqui não importa, pode ser qualquer valor
  * Apesar de "parts" ser uma lista, ela só tem um elemento
* contents: Possuí o histórico de conversas entre o usuário e o modelo. Mensagens do usuário vão ter a role "user" e resposta do modelo vão ter a role "model".
  * Quando o input for imagem, é necessário usar o link do cloud storage junto com o tipo da imagem (image/png, image/jpeg, image/webp)

Na documentação do Vertex AI, recomenda-se pelo menos 100 exemplos para fazer o fine tuning, além disso, o formtado esperado é em jsonl, ou seja, várias linhas com os exemplos na formatação comentada acima. O Exemplo abaixo é as primeiras 3 linhas do dataset final:

```json
{"systemInstruction": {"role": "", "parts": [{"text": "You are a property quality describer. You will be reciving an image of a property being listed to rent (house, apartament, hotel) and your goal is to identify and determine a quality score for the objects identified. The list of objects you are suposed to find are: air_conditioning, bed, bench, chair, cabinet, table, couch, countertop, curtains, fridge, lights, microwave, mirror, nightstand, ottoman, range_hood, rug, shelf, shower, sink, stove, toilet, tv, tv_stand, washing_machine.\n\nIf the image is important, then your goal is to find features in the image and determine a quality score for each of them. The score is a continuous number that goes from 0 to 100. The features you need to identify along with their basic score descriptions are listed below, so anything below the 0 description will be considered a 0 score and anything above the 100 score will be considered a 100, but if something is in between, you use your intelligence to interpolate the correct quality score.\n\nair_conditioning\n* 0: Small, older unit, struggles to cool effectively, might be noisy\n* 100: Central AC, seamlessly integrated, quiet and efficient, smart thermostat\n\nbed\n* 0: Basic metal frame, simple mattress, showing signs of wear\n* 50: Wooden/upholstered frame, comfortable mattress, standard size\n* 100: Large, luxurious frame, premium mattress, adjustable settings, high-quality linens\n\nbench\n* 0: Simple, repurposed item serving as a bench\n* 50: Functional bench, basic upholstery/simple wood design\n* 100: Stylish, well-designed, high-quality materials/upholstery\n\nchair\n* 0: Basic, unpadded, mismatched/showing age\n* 50: Functional, comfortable, simple upholstery/solid construction\n* 100: Designer chair, ergonomic, high-quality materials, stylish\n\ncabinet\n* 0: Basic, freestanding, limited storage, simple hardware\n* 50: Functional, adequate storage, possible wear\n* 100: Built-in, custom, ample storage, soft-close, high-end hardware\n\ntable\n* 0: Small, basic, showing wear/instability\n* 50: Functional, adequate size, simple design\n* 100: Large, well-crafted, high-quality materials, centerpiece\n\ncouch\n* 0: Basic, worn upholstery/simple frame\n* 50: Comfortable, decent upholstery, sturdy frame\n* 100: Large, luxurious, premium upholstery, comfortable seating, stylish\n\ncountertop\n* 0: Basic laminate, visible seams/wear\n* 50: Solid surface, good condition\n* 100: High-end (granite/quartz), seamless, stylish\n\ncurtains\n* 0: Minimal, thin/ill-fitting\n* 50: Functional, adequate light/privacy control\n* 100: High-quality, custom, enhance aesthetics/light control\n\nfridge\n* 0: Simple fridge, no divisions with the freezer, the paiting might be old. A minibar is always a simple fridge.\n* 100: Modern fridge, triplex, can make ice automatically, the color is darker.\n\nlights (lamp, chandelier)\n* 0: Basic, bare bulb, minimal illumination\n* 50: Functional, adequate lighting\n* 100: Designer fixtures, ambiance, highlight features\n\nmicrowave\n* 0: Small, basic, limited features\n* 50: Standard, adequate power/functionality\n* 100: High-end, advanced features (convection, sensor)\n\nmirror\n* 0: Small, simple, basic frame\n* 50: Functional, adequate size, decorative frame\n* 100: Large, stylish, high-quality frame, enhances aesthetics\n\nnightstand\n* 0: Basic, small surface, repurposed item\n* 50: Functional, drawer/shelf storage\n* 100: Stylish, ample storage, complements furniture\n\nottoman\n* 0: Simple, basic, showing wear\n* 50: Functional, comfortable upholstery, sturdy frame\n* 100: Stylish, premium upholstery, storage, complements d\u00e9cor\n\nrange_hood\n* 0: Basic, recirculating, minimal ventilation\n* 50: Standard, adequate ventilation/lighting\n* 100: High-end, powerful ventilation, integrated lighting, stylish\n\nrug\n* 0: Small, basic, wear/fading\n* 50: Functional, adequate size/quality\n* 100: Large, high-quality, premium materials, warmth/style\n\nshelf\n* 0: Basic, freestanding, limited storage\n* 50: Functional, adequate storage\n* 100: Built-in/custom, ample storage, integrated lighting, stylish\n\nshower\n* 0: Basic stall, simple showerhead, limited features\n* 50: Functional, standard showerhead, adequate pressure\n* 100: Luxurious, multiple showerheads, rainfall, high-end fixtures\n\nsink\n* 0: Basic, simple fixtures\n* 50: Functional, standard fixtures, good condition\n* 100: Stylish, high-end fixtures (vessel/waterfall)\n\nstove\n* 0: Basic, limited features, simple controls\n* 50: Functional, standard features, adequate burners\n* 100: High-end, advanced features (convection, smooth top)\n\ntoilet\n* 0: Basic, standard functionality\n* 50: Standard, good condition, efficient flushing\n* 100: High-efficiency, advanced features (dual flush, heated seat)\n\ntv\n* 0: An old tube tv, small TV is also a sign of a bad score.\n* 50: 50: A not soo thin flat-screen TV, but also smaller (about 32 inches). \n* 100: A new looking thin TV, usually hung on the wall, larger than 42 inches.\n\ntv_stand\n* 0: Basic, small surface, repurposed item\n* 50: Functional, storage for components\n* 100: Stylish, ample storage, cable management, complements system\n\nwashing_machine.\n* 0: Basic top-load, limited features\n* 50: Standard, adequate capacity, basic settings\n* 100: High-efficiency front-load, advanced features (steam, multiple cycles)\n\nYou always try to follow this descriptions when giving a score to a feature, you also always try to find and return all the features you find in the image, but you do not create new features, so if the feature is missing from the image you should disregard it. If the feature is missing you do not give it a score.\n\nYou also rate the outside view. If the picture is taken from inside the property, but you can see the outside from a window or balcony, then you can rate it to be 1 or 0. If the view is not present in the picture you can ignore it.\n* 1: You can see a beach or lake from the view\n* 0: You cannot see a beach or lake from the view\n\nIf the image is not important to the property evaluation (like it was taken outside the property), then you will return the reason why as in this JSON schema dict[str, str]:\n* example1: {'bad_image': 'The image is bad because of this reason'}\n\nIf the image is important, then your response must be in a JSON format representing a dictionary where the key is the feature name and the value is the score quality. If the image has two of the same feature (like two tvs) then add a \"-\" and a number to differentiate them, like \"tv-1\" and \"tv-2\".\n\nUse this JSON schema: dict[str, int]\n* example1: {'tv': 50, 'bed': 70, 'view': 0, 'fridge': 10}\n* example2: {'sink': 80, 'view': 1}\n* example3: {'light-1': 10, 'stove': 50, 'light-2': 80}"}]}, "contents": [{"role": "user", "parts": [{"fileData": {"mimeType": "image/jpeg", "fileUri": "gs://categorizacao/dataset/866586878369438057/0000fe96-27a4-453d-8dbf-ccec33fc2578.jpeg"}}, {"text": "Find me this image features and scores"}]}, {"role": "model", "parts": [{"text": "{\"air_conditioning\": \"100\", \"bench\": \"70\", \"chair\": \"70\", \"couch\": \"100\", \"countertop\": \"70\", \"ottoman\": \"100\", \"rug\": \"70\", \"table\": \"100\", \"tv\": \"70\", \"tv_stand\": \"70\", \"view\": \"0\"}"}]}]}
{"systemInstruction": {"role": "", "parts": [{"text": "You are a property quality describer. You will be reciving an image of a property being listed to rent (house, apartament, hotel) and your goal is to identify and determine a quality score for the objects identified. The list of objects you are suposed to find are: air_conditioning, bed, bench, chair, cabinet, table, couch, countertop, curtains, fridge, lights, microwave, mirror, nightstand, ottoman, range_hood, rug, shelf, shower, sink, stove, toilet, tv, tv_stand, washing_machine.\n\nIf the image is important, then your goal is to find features in the image and determine a quality score for each of them. The score is a continuous number that goes from 0 to 100. The features you need to identify along with their basic score descriptions are listed below, so anything below the 0 description will be considered a 0 score and anything above the 100 score will be considered a 100, but if something is in between, you use your intelligence to interpolate the correct quality score.\n\nair_conditioning\n* 0: Small, older unit, struggles to cool effectively, might be noisy\n* 100: Central AC, seamlessly integrated, quiet and efficient, smart thermostat\n\nbed\n* 0: Basic metal frame, simple mattress, showing signs of wear\n* 50: Wooden/upholstered frame, comfortable mattress, standard size\n* 100: Large, luxurious frame, premium mattress, adjustable settings, high-quality linens\n\nbench\n* 0: Simple, repurposed item serving as a bench\n* 50: Functional bench, basic upholstery/simple wood design\n* 100: Stylish, well-designed, high-quality materials/upholstery\n\nchair\n* 0: Basic, unpadded, mismatched/showing age\n* 50: Functional, comfortable, simple upholstery/solid construction\n* 100: Designer chair, ergonomic, high-quality materials, stylish\n\ncabinet\n* 0: Basic, freestanding, limited storage, simple hardware\n* 50: Functional, adequate storage, possible wear\n* 100: Built-in, custom, ample storage, soft-close, high-end hardware\n\ntable\n* 0: Small, basic, showing wear/instability\n* 50: Functional, adequate size, simple design\n* 100: Large, well-crafted, high-quality materials, centerpiece\n\ncouch\n* 0: Basic, worn upholstery/simple frame\n* 50: Comfortable, decent upholstery, sturdy frame\n* 100: Large, luxurious, premium upholstery, comfortable seating, stylish\n\ncountertop\n* 0: Basic laminate, visible seams/wear\n* 50: Solid surface, good condition\n* 100: High-end (granite/quartz), seamless, stylish\n\ncurtains\n* 0: Minimal, thin/ill-fitting\n* 50: Functional, adequate light/privacy control\n* 100: High-quality, custom, enhance aesthetics/light control\n\nfridge\n* 0: Simple fridge, no divisions with the freezer, the paiting might be old. A minibar is always a simple fridge.\n* 100: Modern fridge, triplex, can make ice automatically, the color is darker.\n\nlights (lamp, chandelier)\n* 0: Basic, bare bulb, minimal illumination\n* 50: Functional, adequate lighting\n* 100: Designer fixtures, ambiance, highlight features\n\nmicrowave\n* 0: Small, basic, limited features\n* 50: Standard, adequate power/functionality\n* 100: High-end, advanced features (convection, sensor)\n\nmirror\n* 0: Small, simple, basic frame\n* 50: Functional, adequate size, decorative frame\n* 100: Large, stylish, high-quality frame, enhances aesthetics\n\nnightstand\n* 0: Basic, small surface, repurposed item\n* 50: Functional, drawer/shelf storage\n* 100: Stylish, ample storage, complements furniture\n\nottoman\n* 0: Simple, basic, showing wear\n* 50: Functional, comfortable upholstery, sturdy frame\n* 100: Stylish, premium upholstery, storage, complements d\u00e9cor\n\nrange_hood\n* 0: Basic, recirculating, minimal ventilation\n* 50: Standard, adequate ventilation/lighting\n* 100: High-end, powerful ventilation, integrated lighting, stylish\n\nrug\n* 0: Small, basic, wear/fading\n* 50: Functional, adequate size/quality\n* 100: Large, high-quality, premium materials, warmth/style\n\nshelf\n* 0: Basic, freestanding, limited storage\n* 50: Functional, adequate storage\n* 100: Built-in/custom, ample storage, integrated lighting, stylish\n\nshower\n* 0: Basic stall, simple showerhead, limited features\n* 50: Functional, standard showerhead, adequate pressure\n* 100: Luxurious, multiple showerheads, rainfall, high-end fixtures\n\nsink\n* 0: Basic, simple fixtures\n* 50: Functional, standard fixtures, good condition\n* 100: Stylish, high-end fixtures (vessel/waterfall)\n\nstove\n* 0: Basic, limited features, simple controls\n* 50: Functional, standard features, adequate burners\n* 100: High-end, advanced features (convection, smooth top)\n\ntoilet\n* 0: Basic, standard functionality\n* 50: Standard, good condition, efficient flushing\n* 100: High-efficiency, advanced features (dual flush, heated seat)\n\ntv\n* 0: An old tube tv, small TV is also a sign of a bad score.\n* 50: 50: A not soo thin flat-screen TV, but also smaller (about 32 inches). \n* 100: A new looking thin TV, usually hung on the wall, larger than 42 inches.\n\ntv_stand\n* 0: Basic, small surface, repurposed item\n* 50: Functional, storage for components\n* 100: Stylish, ample storage, cable management, complements system\n\nwashing_machine.\n* 0: Basic top-load, limited features\n* 50: Standard, adequate capacity, basic settings\n* 100: High-efficiency front-load, advanced features (steam, multiple cycles)\n\nYou always try to follow this descriptions when giving a score to a feature, you also always try to find and return all the features you find in the image, but you do not create new features, so if the feature is missing from the image you should disregard it. If the feature is missing you do not give it a score.\n\nYou also rate the outside view. If the picture is taken from inside the property, but you can see the outside from a window or balcony, then you can rate it to be 1 or 0. If the view is not present in the picture you can ignore it.\n* 1: You can see a beach or lake from the view\n* 0: You cannot see a beach or lake from the view\n\nIf the image is not important to the property evaluation (like it was taken outside the property), then you will return the reason why as in this JSON schema dict[str, str]:\n* example1: {'bad_image': 'The image is bad because of this reason'}\n\nIf the image is important, then your response must be in a JSON format representing a dictionary where the key is the feature name and the value is the score quality. If the image has two of the same feature (like two tvs) then add a \"-\" and a number to differentiate them, like \"tv-1\" and \"tv-2\".\n\nUse this JSON schema: dict[str, int]\n* example1: {'tv': 50, 'bed': 70, 'view': 0, 'fridge': 10}\n* example2: {'sink': 80, 'view': 1}\n* example3: {'light-1': 10, 'stove': 50, 'light-2': 80}"}]}, "contents": [{"role": "user", "parts": [{"fileData": {"mimeType": "image/jpeg", "fileUri": "gs://categorizacao/dataset/761515606237649229/05c64e9d-e45a-4729-a02f-a459d00c8db7.jpeg"}}, {"text": "Find me this image features and scores"}]}, {"role": "model", "parts": [{"text": "{\"air_conditioning\": \"100\", \"couch\": \"100\", \"lights\": \"70\", \"rug\": \"80\", \"tv\": \"100\", \"tv_stand\": \"100\"}"}]}]}
{"systemInstruction": {"role": "", "parts": [{"text": "You are a property quality describer. You will be reciving an image of a property being listed to rent (house, apartament, hotel) and your goal is to identify and determine a quality score for the objects identified. The list of objects you are suposed to find are: air_conditioning, bed, bench, chair, cabinet, table, couch, countertop, curtains, fridge, lights, microwave, mirror, nightstand, ottoman, range_hood, rug, shelf, shower, sink, stove, toilet, tv, tv_stand, washing_machine.\n\nIf the image is important, then your goal is to find features in the image and determine a quality score for each of them. The score is a continuous number that goes from 0 to 100. The features you need to identify along with their basic score descriptions are listed below, so anything below the 0 description will be considered a 0 score and anything above the 100 score will be considered a 100, but if something is in between, you use your intelligence to interpolate the correct quality score.\n\nair_conditioning\n* 0: Small, older unit, struggles to cool effectively, might be noisy\n* 100: Central AC, seamlessly integrated, quiet and efficient, smart thermostat\n\nbed\n* 0: Basic metal frame, simple mattress, showing signs of wear\n* 50: Wooden/upholstered frame, comfortable mattress, standard size\n* 100: Large, luxurious frame, premium mattress, adjustable settings, high-quality linens\n\nbench\n* 0: Simple, repurposed item serving as a bench\n* 50: Functional bench, basic upholstery/simple wood design\n* 100: Stylish, well-designed, high-quality materials/upholstery\n\nchair\n* 0: Basic, unpadded, mismatched/showing age\n* 50: Functional, comfortable, simple upholstery/solid construction\n* 100: Designer chair, ergonomic, high-quality materials, stylish\n\ncabinet\n* 0: Basic, freestanding, limited storage, simple hardware\n* 50: Functional, adequate storage, possible wear\n* 100: Built-in, custom, ample storage, soft-close, high-end hardware\n\ntable\n* 0: Small, basic, showing wear/instability\n* 50: Functional, adequate size, simple design\n* 100: Large, well-crafted, high-quality materials, centerpiece\n\ncouch\n* 0: Basic, worn upholstery/simple frame\n* 50: Comfortable, decent upholstery, sturdy frame\n* 100: Large, luxurious, premium upholstery, comfortable seating, stylish\n\ncountertop\n* 0: Basic laminate, visible seams/wear\n* 50: Solid surface, good condition\n* 100: High-end (granite/quartz), seamless, stylish\n\ncurtains\n* 0: Minimal, thin/ill-fitting\n* 50: Functional, adequate light/privacy control\n* 100: High-quality, custom, enhance aesthetics/light control\n\nfridge\n* 0: Simple fridge, no divisions with the freezer, the paiting might be old. A minibar is always a simple fridge.\n* 100: Modern fridge, triplex, can make ice automatically, the color is darker.\n\nlights (lamp, chandelier)\n* 0: Basic, bare bulb, minimal illumination\n* 50: Functional, adequate lighting\n* 100: Designer fixtures, ambiance, highlight features\n\nmicrowave\n* 0: Small, basic, limited features\n* 50: Standard, adequate power/functionality\n* 100: High-end, advanced features (convection, sensor)\n\nmirror\n* 0: Small, simple, basic frame\n* 50: Functional, adequate size, decorative frame\n* 100: Large, stylish, high-quality frame, enhances aesthetics\n\nnightstand\n* 0: Basic, small surface, repurposed item\n* 50: Functional, drawer/shelf storage\n* 100: Stylish, ample storage, complements furniture\n\nottoman\n* 0: Simple, basic, showing wear\n* 50: Functional, comfortable upholstery, sturdy frame\n* 100: Stylish, premium upholstery, storage, complements d\u00e9cor\n\nrange_hood\n* 0: Basic, recirculating, minimal ventilation\n* 50: Standard, adequate ventilation/lighting\n* 100: High-end, powerful ventilation, integrated lighting, stylish\n\nrug\n* 0: Small, basic, wear/fading\n* 50: Functional, adequate size/quality\n* 100: Large, high-quality, premium materials, warmth/style\n\nshelf\n* 0: Basic, freestanding, limited storage\n* 50: Functional, adequate storage\n* 100: Built-in/custom, ample storage, integrated lighting, stylish\n\nshower\n* 0: Basic stall, simple showerhead, limited features\n* 50: Functional, standard showerhead, adequate pressure\n* 100: Luxurious, multiple showerheads, rainfall, high-end fixtures\n\nsink\n* 0: Basic, simple fixtures\n* 50: Functional, standard fixtures, good condition\n* 100: Stylish, high-end fixtures (vessel/waterfall)\n\nstove\n* 0: Basic, limited features, simple controls\n* 50: Functional, standard features, adequate burners\n* 100: High-end, advanced features (convection, smooth top)\n\ntoilet\n* 0: Basic, standard functionality\n* 50: Standard, good condition, efficient flushing\n* 100: High-efficiency, advanced features (dual flush, heated seat)\n\ntv\n* 0: An old tube tv, small TV is also a sign of a bad score.\n* 50: 50: A not soo thin flat-screen TV, but also smaller (about 32 inches). \n* 100: A new looking thin TV, usually hung on the wall, larger than 42 inches.\n\ntv_stand\n* 0: Basic, small surface, repurposed item\n* 50: Functional, storage for components\n* 100: Stylish, ample storage, cable management, complements system\n\nwashing_machine.\n* 0: Basic top-load, limited features\n* 50: Standard, adequate capacity, basic settings\n* 100: High-efficiency front-load, advanced features (steam, multiple cycles)\n\nYou always try to follow this descriptions when giving a score to a feature, you also always try to find and return all the features you find in the image, but you do not create new features, so if the feature is missing from the image you should disregard it. If the feature is missing you do not give it a score.\n\nYou also rate the outside view. If the picture is taken from inside the property, but you can see the outside from a window or balcony, then you can rate it to be 1 or 0. If the view is not present in the picture you can ignore it.\n* 1: You can see a beach or lake from the view\n* 0: You cannot see a beach or lake from the view\n\nIf the image is not important to the property evaluation (like it was taken outside the property), then you will return the reason why as in this JSON schema dict[str, str]:\n* example1: {'bad_image': 'The image is bad because of this reason'}\n\nIf the image is important, then your response must be in a JSON format representing a dictionary where the key is the feature name and the value is the score quality. If the image has two of the same feature (like two tvs) then add a \"-\" and a number to differentiate them, like \"tv-1\" and \"tv-2\".\n\nUse this JSON schema: dict[str, int]\n* example1: {'tv': 50, 'bed': 70, 'view': 0, 'fridge': 10}\n* example2: {'sink': 80, 'view': 1}\n* example3: {'light-1': 10, 'stove': 50, 'light-2': 80}"}]}, "contents": [{"role": "user", "parts": [{"fileData": {"mimeType": "image/jpeg", "fileUri": "gs://categorizacao/dataset/866586878369438057/0733b60a-1bde-4de5-b163-1e31a964bf4e.jpeg"}}, {"text": "Find me this image features and scores"}]}, {"role": "model", "parts": [{"text": "{\"air_conditioning\": \"100\", \"bench\": \"70\", \"cabinet\": \"70\", \"couch\": \"100\", \"painting\": \"70\", \"suporte de tv\": \"100\", \"tv\": \"70\", \"view\": \"0\"}"}]}]}
```

Foi escolhido realizar o fine tuning em cima do prompt de [Score por objeto](https://outline.seazone.com.br/doc/categorizacao-automatica-de-strata-OJOSayKleB#h-score-por-objeto), visto que já tinhamos 59 imagens classificadas em Simples, Standard e Modern e converte-las para um número de 0-100 seria mais fácil.

A planilha [acertividade_features_ia (Métrica Score)](https://docs.google.com/spreadsheets/d/1GysH01e9jrmswaWKhgatU85PwsJRlOOU-o0RYYyCjSs/edit?gid=1128195111#gid=1128195111) possuí ao todo 69 imagens (10 novas imagens desde o experimento antigo) onde foi classificado por um humano todas as features e scores das imagens.

Foi criado o bucket categorizacao: <https://console.cloud.google.com/storage/browser/categorizacao>.

Foi feito o upload de todas as 12k imagens baixadas para esse bucket (dentro da pasta dataset), assim como o arquivo jsonl foi salvo em [finetunning/](https://console.cloud.google.com/storage/browser/categorizacao/finetunning?pageState=(%22StorageObjectListTable%22:(%22f%22:%22%255B%255D%22))&authuser=1)[categorizacao-train-data.jsonl](https://console.cloud.google.com/storage/browser/_details/categorizacao/finetunning/categorizacao-train-data.jsonl?pageState=(%22StorageObjectListTable%22:(%22f%22:%22%255B%255D%22))&authuser=1).

Lembrando que foi necessário realizer o upload das imagens no GCP porque para criar o dataset de treino, as imagens precisam estar no GCP.

### Modelo

O modelo tunado foi criado pelo próprio console no Vertex AI. Foi utilizado os parametros default.

A primeira coisa que acontece ao começar um job de tunning é uma avaliação do dataset. Nesse processo, ele contabilizou que haviam 145994 tokens, além disso, na aba de details, ele recomendou 10 épocas de treinamento. ![](/api/attachments.redirect?id=d9218dff-dd8f-490d-8c5f-d13bedac3b89 " =717x360")O custo para treinar o gemini-flash é de $8 a cada milhão de token, sendo que os tokens são pra cada época de treino, ou seja, ao todo o job consumiu 145994 \* 10 = 1459940, dando $11.68.

Depois de treinado, o Vertex AI automaticamente criou o endpoint e não há custos envolvidos por esse endpoint estar no ar.

Para usar o novo modelo em script é o mesmo padrão de antes, mas agora em vez de colocar no campo de nome "gemini-1.5-flash-002", é preciso colocar "projects/361482453635/locations/us-central1/endpoints/8278611173130108928" (esse é o caminho do endpoint criado).

**O custo de USAR o modelo tunado é o MESMO do modelo base (gemini-1.5-flash-002)**, a príncipio o único custo extra envolvido é o de treino.

### Comparação

Na planilha [acertividade_features_ia (](https://docs.google.com/spreadsheets/d/1GysH01e9jrmswaWKhgatU85PwsJRlOOU-o0RYYyCjSs/edit?gid=1771768460#gid=1771768460)**[Metrica Resultado Tunning) ](https://docs.google.com/spreadsheets/d/1GysH01e9jrmswaWKhgatU85PwsJRlOOU-o0RYYyCjSs/edit?gid=1771768460#gid=1771768460)**se encontra o resultado do fine tuning. Ela tem o score do humano, o score_flash (modelo normal) e o score_tune (modelo tunado).

A príncipio, o modelo tunado está identificando muitos 0s e, analisando os casos, parece que se ele identifica uma feature e este feature está meio "escondida" ele está dando 0.

Exemplo: O ar condicionado abaixo:

 ![](/api/attachments.redirect?id=36be4606-a378-4b23-ab77-9f7d030e1eb5 " =253x337")

Apesar disso, calculado algumas métricas básicas, parece que o fine tuning ficou um pouco melhor do que o modelo normal, mas esses resultados são em cima do mesmo conjuto de dados usado para o treino, então não conseguimos dizer se está com overfitting ou não, é necessário classficarmos na mão um outro dataset de validação para obtermos essa informação.

* Média do erro
  * flash 8.406976
  * tune -1.301369
* MAE
  * flash 20.468992248062015
  * tune 19.41780821917808
* RMSE
  * flash 26.516120590365226
  * tune 25.778960307206884

## Dataset Final (com features)

Nesse primeiro momento, foi criado um dataset usando o [Prompt Score por Tipo](https://outline.seazone.com.br/doc/categorizacao-automatica-de-strata-OJOSayKleB#h-score-por-tipo). O motivo dessa escolha é que suas features são mais simples de serem usadas o que facilitaria a criação de um primeiro modelo. O modelo que usou o Fine Tuning também não aparentou ter grande melhora sobre o gemini padrão.

Como base pro dataset de imagens, foi utilizado o dataset INICIAL, ou seja, aquele sem filtros de imagens duplicadas ou irrelevantes.

Foi criado um script que usa o Vertex AI para fazer os requests (como existem alguns imóvies com muitas imagens, usando o gemini padrão request passaria do limite de dados, mas o Vertex AI permite passar link das imagens no GCP facilitando esse processo).

Os scripts também se encontram no reposistório.

No final a tabela tem essa aparencia:

 ![](/api/attachments.redirect?id=fa38561d-2704-48be-a123-15a8d19d9e2c)

* **airbnb_listing_id:** id do imóvel, a tabela tem uma linha por id do imóvel.
* **prompt_token_count:** tamanho do prompt de input (a parte de texto + imagens), o metodo de cobrança do vertex AI usa número de imagens e caracteres, então essa coluana serve apenas para termos uma noção básica do custo.
* **candidates_token_count:** número de tokens de saída do modelo.
* **total_token_count:** a soma dos tokens de entrada e saída.
* **cached_content_token_count:** tokens em cache, nesse request em específico sempre é 0, pois não usa cache.
* **Finishes, Eletronics, Furniture, Decoration, Lighting, Space:** features que o modelo retorna.
* **BadImage:** lista de listas onde cada sublista vai ter o nome da imagem e o motivo dela estar sendo ignorada.

No final do script, o resultado é salvo no Bucket do GCP, então a tabela está na nuvem para ser baixada.

Aqui está a proporção de cada feature:

 ![](/api/attachments.redirect?id=07da29ec-5ef4-46da-a19f-98a47893fa05)

## ImageScoreModel

A ideia do ImageScoreModel é desenvolver um modelo baseline de classificação de stratas utilizando exclusivamente os scores das features extraídas. A ideia é ele ser bem simples, ou seja, tentar criar regras e thresholds para cada strata ainda sem o uso de machine learning.

Foi criado a feature 'avg', que é uma simples média entre as 6 features acima e, a partir dela, foram criados thresholds para definir cada strata.

 ![](/api/attachments.redirect?id=bf9210b6-bc3b-4339-a168-c5f8306b4049 " =717x279")

### Definindo intervalos iguais

A primeira ideia de threshold foi definir intervalos iguais para cada strata, ou seja, as primeiras 20% de 'avg' seriam SIM, as próximas 20% seriam JR e assim por diante.

Os thresholds ficaram:

* **SIM:** abaixo de 68.33
* **JR:** entre 68.33 e 70
* **SUP:** entre 70 e 75
* **TOP:** entre 75 e 80
* **MASTER:** acima de 80

**Resultado:**

 ![](/api/attachments.redirect?id=f8522bd2-372c-47eb-8f60-5e52c211143f " =632x640")

### Explicação das métricas

Como o modelo é multiclasse, pode ficar meio confuso de entender como os cálculos das métricas funcionam.

O cálculo da métrica é feito POR CLASSE, ou seja, cada classe terá seu próprio conjunto de TP, FP, FP, FN.

* ![](/api/attachments.redirect?id=9b590daa-16ee-4539-8bbd-b557fd19fb1f " =337x237")**TP (True Positive)**: Elemento da diagonal principal da classe X.
* **FP (FalsePositive)**: Elementos previstos da respectiva coluna da classe X, mas que não são o TP (amarelo).
* **FN (False Negative)**: Elementos reais da respectiva linha da classe X, mas que não são o TP (azul).
* **TN (True Negative)**: São todos os outros casos, ou seja, os elementos fora da linha e coluna da respectiva classe X.

**Metricas Classificação:**

* **Por classe**
  * **precision:** TP / (TP + FP)
  * **recall**: TP / (TP + FN)
  * f1_score: 2 \* (precision \* recall) / (precision + recall)
* **macro avg**: Média dos resultados das métricas cálculadas por classe
* **support**: número de ocorrencias da classe real
* **weighted avg**: Média ponderada das métricas cálculadas por classe. O peso da ponderação é o número de elementos na classe, ou seja, o support.
* **accuracy**: diagonal principal (acertos) dividido pelo número total (411)

**Métricas regressão:**

* **Por classe:**
  * **mae_real**: é calculado por classe REAL, ou seja, é pego todos os imóveis que realmente são SIM e é calculado o MAE deles. Isso é feito para cada classe.
  * **mae_predict**: é calculado por classe predita.
  * **support**: número de ocorrencias da classe real
  * **support_predict**: número de ocorrencias da classe predita
* **macro avg**: Média de cada MAEs acima.
* **weighted avg**: Média ponderada dos MAEs por classe. O peso do mape_real é o support, enquanto que o do mape_predict é o support_predict.
* **mae e rmse**: Eu faço o cálculo do RMSE e refaço o cálculo do MAE usando todas as predições ao mesmo tempo. No caso esse MAE fica igual ao weighted avg MAE, visto que matemáticamente os dois cálculos são iguais. A príncipio não achei necessário também calcular o rmse por classe, acho que o MAE já é o suficiente para entendermos o erro.

### Definindo intervalos iguais e normalizando

Outra ideia de threshold foi primeiro normalizar as features para depois calcular a média delas. A ideia é que, como na prática as features possuem intervalos diferentes, ao normalizar em um intervalo especifico elas começariam a atribuir peso similares (por exemplo, o menor valor de Finishes é 60, enquanto que o de Decoration é 10, a média deles é 35, mas como eles são os piores valores de suas respectivas features, faria mais sentido esse resultado ser 0).

Foi utilizado o MinMaxScaler do sklearn para definir os intervalos entre 0 e 1.

 ![](/api/attachments.redirect?id=4d132163-b854-41c0-a1a6-a2a912072b29 " =759x206")

Utilizando a mesma lógica de definir intervalos iguais para cada strata, ou seja, as primeiras 20% de 'avg' seriam SIM, as próximas 20% seriam JR e assim por diante, os thresholds ficam:

* **SIM:** abaixo de 0.557468
* **JR:** entre 0.557468 e 0.595283
* **SUP:** entre 0.595283e 0.664928
* **TOP:** entre 0.664928e 0.767467
* **MASTER:** acima de 0.767467

**Resultado:**

 ![](/api/attachments.redirect?id=36ec08eb-44d8-44de-a11c-31a3c556b79e " =548x567")


### Definindo intervalos stratificados

Nessa ideia de threshold, em vez de pegarmos intervalos iguais de 20%, os intervalos se baseiam na proporção de stratas do conjunto de dados, então os thresholds ficam:

* **SIM:** abaixo de 61.561233
* **JR:** entre 61.561233 e 69.689781
* **SUP:** entre 69.689781 e 76.105028
* **TOP:** entre 76.105028 e 81.780211
* **MASTER:** acima de 81.780211

O problema de fazer dessa forma, é que precisamos saber com antecedência a proporção de strata dos imóveis numa região, se não temos essa proporção então precisamos estimar uma, então como estou usando o mesmo conjunto de dados para estimar a proporção e para fazer o predict, está lógica está "roubando" um pouco.

 ![](/api/attachments.redirect?id=cd693c89-856c-4809-918a-372265f98d51 " =590x613")

### Comparação

Foi gerado uns gráficos para ajudar a comparar cada métrica. Os da esquerda são as "macro avg" e o da direita são os "weighted avg".

 ![](/api/attachments.redirect?id=fcdf915e-10c5-42e9-bc01-bbe693195725)

Dentre os experimentos, o melhor ImageScoreModel ficou o com intervalos stratificados, entretanto, como ele precisa conhecer primeiro o conjunto de dados, então a príncipio será utilizado o modelo normalizado de baseline para os próximos experimentos que utilizarão machine learning.

# MVP Florianópolis

O MVP inteiro foi desenvolvido nesse epic: <https://seazone.atlassian.net/jira/software/c/projects/DS/boards/22?selectedIssue=DS-415>

O notebook usado pode se encontrar aqui: <https://github.com/seazone-tech/Util-dados/blob/main/data-solutions/image_score_model/modelo_florianopolis_production_final.ipynb>

## Definição do Escopo e Features

Foi definido um scopo inicial de Florianópolis, visto que é uma região mais conhecida, além disso, estamos usando apenas até 2 imóveis, visto que isso representa a maior parte da operação.

### Filtros

**Imóveis de Treino:**

* **Região:** Florianópolis-SC
* **Tipo:** Casa ou Apartamento
* **Número de quartos:** 0 a 2
* **Filtros de Review:** 
  * nota > 4.6  e >= 10 REVIEWS OU
  * nota > 4.9 e >= 5 Reviews; 
* **Faturamento:** Ter faturado mais do que 500 nos últimos 90 dias. 

**Imóveis de Validação:**

* Imóveis da Seazone
* Não precisam passar nos filtros de review/faturamento

### Dataset

**Treinamento**

Alguns imóveis a gente ainda não tinha imagem, então ficaram de fora do escopo inicial.

* **Ids fora da lista:** 2292
* **Concorrentes sem Strata com imagens:** 533
* **Total de Concorrentes com Strata e imagens:** 4090 
* **Total por strata:** 
  * **SIM: 603 (14.74%)**
  * **JR: 1509 (36.89%)**
  * **SUP: 1382 (33.79%)**
  * **TOP: 548 (13.40%)**
  * **MASTER: 48 (1.17%)**

**Validação**

* **Total de Imóveis Seazone:** 361
* **Total por strata:** 
  * **SIM:** 8 (2.21%)
  * **JR:** 96 (26.52%)
  * **SUP:** 136 (37.57%)
  * **TOP:** 115 (31.77%)
  * **MASTER:** 6 (1.65%)

### Features

Ideias iniciais de novas features:

* Preço médio das ocupações no último ano
* Taxa de ocupação no último ano
* Faturamento médio no último ano
* Número de quartos
* Tipo (apartamento ou casa)
* Novas amenities
* Distância do mar
* Alguma feature de generalização de localização (diferença do imóvel dentro de seu bairro ou cluster).

#### Features Mar

Foi feito o download de 2 datasets de poligonos da internet. Foi usado geopandas para calcular a distância dos imóveis com o poligono mais próximo.

* Dataset contendo mar (vermelho): <https://osmdata.openstreetmap.de/data/water-polygons.html>
* Dataset contendo lagos e rios (azul): <https://download.geofabrik.de/south-america/brazil.html>

 ![Polígonos de água](/api/attachments.redirect?id=4451dd6b-afc6-415e-af66-3219947e15d7 " =299x254")

Após os testes foi optado em utilizar apenas o dataset contendo mar, visto que o dataset contendo lagos e rios apresentava muitos casos de rios pequenos de pouco interesse (se fosse apenas a Lagoa da Conceição talvez fizesse sentido).

Foi criado 4 features de teste:

* close_to_water: até 120 metros
* medium_to_water: dentre 120 e 400 metros
* far_to_water: mais que 400 metros
* discrete_water_distance: 0, 1 ou 2 dependendo se está perto, medio ou longe do mar

Proporção:

 ![](/api/attachments.redirect?id=b88cd480-75b4-4324-a310-acbe087c8f03 " =299x289")

#### Features Amenities

Existem muitas amenities com nomes diferentes, mas que representam algo parecido, como *TV 32 polegadas* e *TV 34 polegadas*, então as vezes é necessário agrupa-las numa feature só, por isso elas foram todas padronizadas para não ter acento e serem letras minúsculas.

* **vista** contem um dos seguintes valores : *vista para o mar, vista para as aguas, vista para o oceano, vista para o lago, vista para a praia, vista para a baia, vista para o canal, vista para o porto, vista para a marina, vista para o rio*
* **jacuzzi** precisa ser *jacuzzi privativa*
* **acesso** contem *acesso* na string e também *praia* ou *lago*
* as outras amenities apenas precisam ter seu próprio nome na string

 ![](/api/attachments.redirect?id=57af0466-c677-4e94-95f3-59f077b9b6a4 " =411x328")

#### Features Preço

* **avg_price:** Média do preço ocupado médio mensal do último ano do imóvel, então se a média de janeiro fosse 500 e a de fevereiro fosse 100, o avg_price é (500 + 100)/2 = 300
* **avg_price_normal**: Média do preço mensal multiplicada pelo número de dias ocupados, então se em janeiro houveram 2 dias ocupados com média 500 e fevereiro 1 dia com média 100, o avg_price_normal será (2\*500 + 1\*100)/3 = 366.67
* **avg_price_by_room**: É o avg_price_normal dividido pelo número de quartos (para 0 quartos utilizo 1).
* **to**: total de dias ocupados do ano dividio pelo número de dias não bloqueados do ano.
* **fat**: avg_price_normal multiplicado pela to
* **fat_by_room**: É o fat dividido pelo número de quartos (para 0 quartos utilizo 1).
* **fat_by_room_normal:** Aplico log1p em cima de fat_by_room. O log1p aplica ln(1+x), dessa forma nunca fica ln(0).

  \

 ![](/api/attachments.redirect?id=32d5c392-4a6f-4444-846b-9d92b0d75b96 " =636x271")

#### Correlações

Abaixo se encontra a matriz com todas as correlações de spearman.

 ![](/api/attachments.redirect?id=c700301e-07e2-4d9b-b66d-0433954d6ea4)

* As melhores foram piscina, avg_price/avg_price_normal (0.38 e 0.37) e fat (0.41), inclusive a correlação delas ficou acima da feature de Decoration do Gemini.
* listing_type, academia, ar condicionado ficaram na faixa do 0.23-0.27.
* As features de distancia da água que deram bastante trabalho de criar ficaram praticamente iguais a feature de vista.

### Seleção de Features

A partir de alguns testes utilizando alguns algoritimos de seleção de features, assim como uma analise da matriz de confusão das correlaçÕes, no final optou-se em utilizar os seguintes atributos: Finishes, Electronics, Furniture, Space, vista, jacuzzi, piscina, discrete_water_distance, type_apartamento, fat_by_room.

* As featues de Decoration e Lighting do Gemini foi excluída, visto que não era boa o batante para ajudar o modelo. 
* Apenas vista, jacuzzi e piscina estão sendo usadas nas amenities.
* Apesar de ter menor correlação, nos testes a feature *fat_by_room* se desempenhou melhor que a *fat*. Além disso, não faz sentido ter *fat* e *price*/*to*, então apenas a fat_by_room está sendo considerada.

## Tunagem Modelo

Foram feitos alguns testes com LogisticRegression, RandomForest e XGBoost. No final o algoritimo mais consistente foi o LogisticRegression.

Aqui está a explicação das métricas: [Criação de Features Gemini/ImageScoreModel/Explicação das métricas](https://outline.seazone.com.br/doc/categorizacao-automatica-de-strata-OJOSayKleB#h-explicacao-das-metricas)

Foi feito uma cross validation de 5 iterações em cima do melhor modelo. Os grupos não eram stratificados, ou seja, eles não tentavam manter a proporção de cada strata.

### Métricas

A strata com maior erro é SUP, entretanto, a strata MASTER apresenta uma variabilidade muito grande no conjunto de validação. Fazendo 5 grupos, o grupo de validação fica em média com apenas 10 imóveis tornando difícil a metrificação, mas a príncipio o modelo também tem dificuldade em predizer MASTERs.

**Validação:**

 ![](/api/attachments.redirect?id=bdda2392-2b5b-4cf0-9b7a-dfc1eec436d3 " =524x244")

**Treino:**

 ![](/api/attachments.redirect?id=b171706f-b1a8-4a33-a25c-fd51160cb42b " =524x242")

**Importancia de cada Feature:**

 ![](/api/attachments.redirect?id=83cdc1a7-94c4-4819-a9aa-0d6be598a4e0 " =524x345")

* Features Gemini:
  * SIM e JR o modelo penaliza
  * SUP algumas penaliza outras promove
  * TOP e MASTER todas promovem uma strata melhor.
* Apartamento:
  * Parece que existem muitas casas que são MASTER, então o modelo penaliza apartamento para MASTER.
* fat_by_room:
  * O modelo está penalizando faturamentos baixos para SIM e JR e promovendo faturamento altos para MASTER/TOP.
* amenities (jacuzzi, piscina e vista)
  * SIM e JR são penalizados
  * SUP é penalizado por vista, mas promovido se ter piscina
  * TOP e MASTER são promovidas.
* water_distance
  * Esse é um valor discreto que pode ser 0 (colado na praia), 1 (perto) ou 2 (longe)
  * SIM e JR são promovidos quanto maior a distancia da água.
  * SUP tanto faz
  * TOP e MASTER são promovidos quanto mais perto do mar

### Validação Seazone

O modelo final foi treinado em cima do dataset inteiro, depois foi feito um predict dos dados de treino e dos dados da Seazone (os dados da Seazone nunca foram usados durante o treinamento).

Também foi feita a predição em cima dos 533 que não possuíam stratas.

A seguinte planilha apresenta todos os dados: <https://docs.google.com/spreadsheets/d/1kVWFUCmF9uCDx3_-Iu0ZvCEw2deUnwjrkBrrz4n3F6k>

 ![](/api/attachments.redirect?id=95d1af22-1adc-4561-a323-16b564620490)

* **Treino:** 
  * **Acerto: 48.36%**
  * **1 Grau de erro: 43.23%**
  * **Erros =>2 grau: 8.41%**
  * ***__Acerto + 1 Grau de erro: 91.59%__***
* **Validação:** 
  * **Acerto: 55.68%**
  * **1 Grau de erro: 41.27%** 
  * **Erros =>2 grau: 3.05%**
  * ***__Acertos + 1 grau de erro: 96.95%__***

Se considerarmos acertos como imóveis que ficaram próximos da diagonal principal, o modelo está muito bom.

Vale ressaltar que existe um problema de consistência dos dados de treino, visto que eles são muito mais propícios a erros humanos.

**Casos onde Modelo acertou, mas strata estava errada:**

* **__[822592322001721648 ](https://www.airbnb.com.br/rooms/822592322001721648?source_impression_id=p3_1743449263_P39zc5YhpmyuOXvz)__**
  * **Strata: TOP**
  * **Predição SIM**
* **__[1065323683036397694](https://www.airbnb.com.br/rooms/1065323683036397694?source_impression_id=p3_1743449466_P3Ju36D-SePgbeuk)__**
  * **Strata : JR**
  * **Predição: MASTER**

**Não são todos os casos que são assim, também existem aqueles que o modelo errou bastante:**

* **__[53505323](https://www.airbnb.com.br/rooms/53505323)__**
  * **Strata: SUP**
  * **Predição: MASTER**
  * **Gemini classificou bem demais o imóvel**
* **__[SDR005](https://www.airbnb.com.br/h/seazone-SDR005)__**
  * **Strata: SUP**
  * **Predição: SIM**
  * **Não identificou acesso a lagoa**


## Próximos Passos

O projeto foi [apresentado (link)](https://docs.google.com/presentation/d/19jNiQIIZw11ygJd0qFEKuTA3f7LYngiyyWFgUkuyDNs/edit)  e próximos passos foram definidos.

### Plano de Ação


1. Classificar listings de Salvador (seria útil pro modelo conseguir classificar Salvador, visto que essa é a próxima área de interesse que a Seazone quer focar e expandir).
2. Análise qualitativa:

   
   1. Exercicio com RM categorizando imóveis, assim podemos entender o quanto que humanos erram a stratificação e o quão subjetivo ela é, as métricas de +1 strata de erro também vão fazer mais sentido.
   2. Foi criado essa planilha: [Imóveis para stratificar](https://docs.google.com/spreadsheets/d/1cAGxOwINJGfEdDI8w19pevFXnSBvSa4tnPdWKjr6rb4/edit?gid=0#gid=0). A lógica usada para gerar a lista foi de pegar uns 200 ids que possuem proporção nas features.

      
      1. Foi pego um subconjunto de 184 que mantem a proporção do tipo, quarto, strata, jaccuzi e vista.
      2. Foi complementado com 16 MASTERs aleatórios (como existem poucos MASTERs, fazendo apenas o primeiro ponto eram retornados 0 nessa strata).
   3. Indicador de qualidade nas respostas de predição do modelo (cruzar dados de faturamento ou outras evidências que nos dê confiança na predição).
3. Automatizar todo fluxo de obtenção de dados para classificação de strata.

   
   1. É necessário baixarmos imagens de outras regiões para conseguirmos expandir o modelo.
   2. Fazer os requests com o Gemini para obtermos as features.
   3. Retreinar o modelo com os novos dados.
4. Na apresentação:

   
   1. Trazer case fora de floripa
5. Plano de ampliação (War): Mapear lugares onde podemos aplicar o mesmo modelo criado atualmente (características de floripa), e levantar outros estados com características que precisam adicionar características no modelo.