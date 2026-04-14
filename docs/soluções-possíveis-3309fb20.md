<!-- title: Soluções possíveis | url: https://outline.seazone.com.br/doc/solucoes-possiveis-TIfShXOOet | area: Tecnologia -->

# Soluções possíveis

# Soluções possíveis

> Caso de exemplo
>
> Ex: usuário estará em lua de mel e deseja aquela propriedade em específico por somente um dia, mas o mínimo para aquelas datas é de 3 dias


## 1.  Oferecer na própria busca datas alternativas possíveis que levem em conta o min stays. O usuário sabe da regra e decide se quer.

> Usuário vê na própria busca que existe um mínimo de diárias naquelas propriedades, e recebe sugestões de novas datas à partir daquelas datas.
>
> Por exemplo:
>
> → Há um mínimo de 3 diárias nas nossas propriedades para essas datas, você pode reservar para essas datas e ficar somente 1 diária se quiser.


**Pros**

* Mais fácil de implementar
* Se houver vendas, podemos investir mais nisso

**Cons**

* O usuário pode sentir que está sendo prejudicado por ter que reservar mais dias 
* Não podemos devolver os dias extras de volta para a operação
* Se não houver vendas, precisamos validar os motivos


## 2.  Oferecer na própria busca datas alternativas possíveis que levem em conta o min stays. Dizer ao usuário que está recebendo X dias de graça.

> Usuário vê as propriedades com as datas correspondentes corretas, mas com uma promoção de 2 datas gratuitas
>
> Por exemplo:
>
> → Encontramos esses resultados aqui em promoção, pague 1  diária e leve 3 


**Pros**

* Ainda fácil de implementar
* Se houver vendas, podemos investir mais nisso e fazer a versão 3
* Dá ao usuário a percepção de que está levando algo em promoção

**Cons**

* O usuário pode ainda se sentir prejudicado pelo alto preço comparado com datas mais próximas
* Não podemos devolver os dias extras de volta para a operação
* Se não houver vendas, precisamos validar os motivos

## 3. \[ Sonho \] Usuário não tem diferença na experiência. Acredita que esse é o preço real e por baixo dos panos vendemos 1 dia pelo preço de 3 (por exemplo)


> Usuário vê as propriedades com as datas BUSCADAS, mas com o preço do mínimo de dias. O usuário acredita que reservou somente 1 dia.
>
> Por exemplo:
>
> → Do dia 1/4 ao dia 2/4 por 1300 reais. (Preço real é do dia 1 ao dia 4/4 por 1300 reais)


**Pros**

* Usuário não se sente prejudicado
* Podemos devolver os dias extras à RM
* Podemos dar os outros dias gratuitos aos hóspedes para não ter problemas no atendimento

**Cons**

* Muito dificil de implementar: enquanto as outras duas implementações envolvem somente o backend retornando mais resultados e uma mudança pequena de layout, essa mudança 


## 4. **✅** Solução Aceita: Usuário não tem diferença de experiência na busca e na página do imóvel. Acredita que esse é o preço real. E quando ele clica para reservar mostramos um popup para ele reservar com o atendimento.


> Usuário vê as propriedades com as datas BUSCADAS, mas com o preço do mínimo de dias. O usuário acredita que reservou somente 1 dia.
>
> Por exemplo:
>
> → Do dia 1/4 ao dia 2/4 por 1300 reais. (Preço real é do dia 1 ao dia 4/4 por 1300 reais). Na página do imóvel ele vê também o mesmo preço que viu na página de busca.


\