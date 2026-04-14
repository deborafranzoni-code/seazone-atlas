<!-- title: Análise de categorias | url: https://outline.seazone.com.br/doc/analise-de-categorias-iYTB9pdpRR | area: Tecnologia -->

# Análise de categorias

A análise de categorias de imóveis acontece através da estratégia de analisar o faturamento mensal dos imóveis da mesma categoria. 

### **Metodologia**


1. **Definição da Banda:** Para cada categoria de imóvel, a banda de faturamento foi definida utilizando os percentis 25 e 75 do faturamento dos imóveis da categoria como limites inferior e superior, respectivamente.
2. **Classificação dos Imóveis:** Os imóveis foram classificados como "fora da banda" se o seu faturamento estivesse fora dos limites da banda.
3. **Métricas de Percentil:** Foram utilizadas diferentes métricas de percentil para avaliar o impacto na identificação de imóveis fora da banda. As métricas foram:
   * **Percentil 90, 80, 75:** Para identificar imóveis com faturamento acima da banda superior.
   * **Percentil 20, 15, 10:** Para identificar imóveis com faturamento abaixo da banda inferior.
4. **Avaliação dos Resultados:** Foram analisados a quantidade de imóveis identificados como fora da banda para cada métrica de percentil, bem como a precisão da classificação.


### Percentis 75-25

Número de identificados como fora da banda: 307

 ![Gráfico de Bandas: Mostra a distribuição dos imóveis fora da banda, divididos entre os que faturam acima e abaixo da categoria](/api/attachments.redirect?id=a6d1fe3b-50ab-4898-982f-6dc1c7ab70ee " =990x590") ![Gráfico de Strata: Exibe o número de imóveis fora da banda por strata.](/api/attachments.redirect?id=57557866-274d-4d37-9baf-a9d78c6068e8 " =990x590")


 ![Gráfico de Categorias: Representa o número de imóveis por categoria (categorias com mais de um imóvel fora da banda).](/api/attachments.redirect?id=0483ed65-8568-4cf1-91c3-6c5efc9b57b5 " =1190x590")


### Percentil 80-20

 ![Gráfico de Bandas: Mostra a distribuição dos imóveis fora da banda, divididos entre os que faturam acima e abaixo da categoria](/api/attachments.redirect?id=dbe03b86-47b2-4e90-880c-a28d964a7300 " =990x590") ![Gráfico de Strata: Exibe o número de imóveis fora da banda por strata.](/api/attachments.redirect?id=6838cd62-a778-4917-8c04-f2d6189c389d " =989x590")


 ![Gráfico de Categorias: Representa o número de imóveis por categoria (categorias com mais de um imóvel fora da banda).](/api/attachments.redirect?id=f6ae56f5-b439-4c5b-95e3-13c881001da0 " =1190x590")


### Percentil 90-10

 ![Gráfico de Strata: Exibe o número de imóveis fora da banda por strata.](/api/attachments.redirect?id=2de35317-7afe-462d-ad95-e5214eb82abd " =989x590") ![Gráfico de Categorias: Representa o número de imóveis por categoria (categorias com mais de um imóvel fora da banda).](/api/attachments.redirect?id=87365046-0acd-4fd3-8351-5cf9a1885679 " =1189x590")


Avaliação dos imóveis

RPM103 - Esse imóvel parece mais espaçoso e com móveis mais "bem cuidados", mas não tão diferente. Lista de concorrentes: 1032606587960523259, 16313012, 21028263, 29610571, 33013254.

 ![](/api/attachments.redirect?id=0c3dfe01-51a3-4be1-8c95-5ef316382d5a)


SGB302 - Essa imovel parece menos atrativou de strata menor que esses:  15632254, 16017693, 21025393, 51453135, 8838629

 ![](/api/attachments.redirect?id=6bca9803-3efb-45c8-908b-78aec934028c)


\
imovel apontado como anomalo percentil 75-25  e concorrentes - abaixo dos concorrentes


 ![](/api/attachments.redirect?id=8383bb2d-4de7-4203-9454-38d155f59225) ![](/api/attachments.redirect?id=e4bc7008-c5d2-478c-a99b-c4f61cfa5f56) ![](/api/attachments.redirect?id=877450bf-bd23-4896-baeb-b4964aa867e2)

 ![](/api/attachments.redirect?id=e2a1d879-4bb3-4677-84cb-65c6b18ba05b)

imoveis com uma strata abaixo


 ![](/api/attachments.redirect?id=0ac607da-9525-4c71-afc7-67be1cb533ae)

 ![](/api/attachments.redirect?id=5c155d4c-cd18-49b8-9050-5397526af4d2)

 ![](/api/attachments.redirect?id=ccedcdea-9409-4fb5-90fd-d3e1f7c0be3f)


imovel apontado como anomalo percentil 80-20  e concorrentes - parecem os mesmo mas com fotos mais profissionais

 ![](/api/attachments.redirect?id=6aac00df-f010-4cd8-afe9-17b48efab9bc)

 ![](/api/attachments.redirect?id=32426133-ec6e-4713-a964-162b8d72e321) ![](/api/attachments.redirect?id=1767c8ae-572b-432a-bd55-f233fd6d24a7) ![](/api/attachments.redirect?id=c23c8267-2e86-4b15-a6ff-44a86fd212d2)


imoveis de uma strata acima

 ![](/api/attachments.redirect?id=8bf23299-4b0d-41f8-974e-a5b22ee2b70f) ![](/api/attachments.redirect?id=d0f209f4-4236-4454-80d5-4c8e2cb3a5ba) ![](/api/attachments.redirect?id=e103c931-2c25-4b5e-bd88-60c6757b0a9b)

 ![](/api/attachments.redirect?id=f8ad1bbe-2355-4633-b2b7-b92d89a801e2)