<!-- title: Atualização Necessária para Suporte ao Google Maps Marker Depreciado | url: https://outline.seazone.com.br/doc/atualizacao-necessaria-para-suporte-ao-google-maps-marker-depreciado-eI1hhffnjq | area: Tecnologia -->

# Atualização Necessária para Suporte ao Google Maps Marker Depreciado

Task [SZRDEV-1041](https://seazone.atlassian.net/browse/SZRDEV-1041) 



:::tip
## **TL;DR**

O `google.maps.Marker` será depreciado em fevereiro de 2024.

Isso impacta o mapa utilizado na tela de resultados-da-busca no website

Devendo ser substituído pelo `AdvancedMarkerElement`. Nossa biblioteca atual não suporta a nova tecnologia, exigindo ação.\n

* O google.maps.Marker será depreciado, mas continuará funcional.


* Nossa biblioteca atual não tem suporte ao AdvancedMarkerElement.
* A nova versão prometida pela Google apresenta marcadores 40% mais leves.
* Os mantenedores da biblioteca atual não indicaram solução até o momento.\n

**Soluções:**

* Migrar para @visgl/react-google-maps (recomendação oficial, estável e de longo prazo).
* Alterar e manter localmente o código da biblioteca atual, com risco de incompatibilidades no React.


***Sugestão:*** *Optar pela biblioteca recomendada para evitar dores futuras.*

:::


# **Cenário Atual**

Ao realizar uma busca por uma data ou localização no website hoje é possível visualizar um mapa interativo (usando uma biblioteca React para Google Maps para ser exibido) na lateral direita, onde exibimos a localização dos imóveis 


 ![](/api/attachments.redirect?id=1196a34e-eddc-4cbe-a7c2-ba87395bae2a)

# **O Problema**

O mapa que utilizamos, se baseia numa biblioteca para reactjs que implementa uma visualização do google maps, esse que utiliza o recurso do `google.maps.Marker`para marcar a localização dos imóveis


 ![](/api/attachments.redirect?id=6d561a35-f2af-4af4-ba14-db9f9269313b)


Recentemente essa mensagem começou a ser exibida no console ao abrirmos essa página, informando que o recurso do google maps `google.maps.Marker` será descontinuado em breve

 

 ![](/api/attachments.redirect?id=f3459760-ca1b-4cc5-a06c-f545d94736bf "left-50 =374x263")Conforme comunicado na mensagem de aviso da biblioteca JavaScript do Google Maps. A partir de **21 de fevereiro de 2024** o `google.maps.Marker` Será considerado obsoleto (deprecated) e substituido por:

```javascript
google.maps.marker.AdvancedMarkerElement
```


\

De forma resumida o google esta depreciando esse marcador e substituindo pelo `AdvancedMarkerElement` cujo qual a nossa biblioteca atual não apresenta suporte, analisando o repositório não foi encontrado nenhuma solução aparente por parte dos mantenedores da biblbioteca.


Ainda que o nosso marcador atual fique depreciado a google seguira dando suporte para ele, oq significa que não vai parar de funcionar, ainda assim é recomendado que busquemos uma solução definitiva para fazer essa migração, tendo em vista que os novos marcadores são 40% mais leves segundo a própria documentação do google.

# **Soluções Propostas**

## **1. Utilizar a biblioteca recomendada pelo google** 


Utilizar a biblioteca `@visgl/react-google-maps` a mesma utilizada pelo prórpio google maps nos tutoriais postados no youtube.


Com essa abordagem seria necessário rever a lógica da nossa biblitoeca atual e trazer para essa nova biblioteca que da suporte aos novos marcadores do google, isso poderia gerar um trabalho de inicio para o time, mas acredito que a longo prazo dado ao fato dessa biblioteca ser atualizada regularmente, não teriamos outras dores como essa no futuro.


Além disso, há uma playlist completa no canal oficial do Google Maps com instruções detalhadas para implementar essa biblioteca, o que facilita o aprendizado e a integração.


[https://www.youtube.com/watch?v=8kxYqoY2WwE&t=400s](https://www.youtube.com/watch?v=8kxYqoY2WwE&t=400s)


\
## **2. Alterar o código fonte da biblioteca atual.**


Um comentário postado em uma issue na nossa biblioteca atual sugere ter resolvido o problema.


Entretanto, pelo que verifiquei, seria necessário realizarmos o build de uma versão personalizada da biblioteca, já que ainda não foi lançada uma nova release oficial contendo a correção. Isso, claro, considerando que a solução apresentada no comentário de fato resolve o problema identificado.


De acordo com o comentário, o usuário copiou o componente da outra biblioteca recomendada pela Google e o inseriu no código-fonte da nossa biblioteca atual. Embora essa abordagem pareça funcional, a maior complexidade reside no fato de que precisaríamos copiar todo o código da biblioteca e mantê-lo de forma local em nosso projeto, já que a alteração sugerida não foi incorporada oficialmente em uma release.


Outro ponto crítico é a compatibilidade com a versão do React que utilizamos. A biblioteca pode conter dependências ou implementações que não sejam totalmente compatíveis com nossa versão atual, o que exigiria ajustes adicionais ou até a atualização do React em nosso projeto. Esse processo pode gerar impactos consideráveis, tanto em termos de desenvolvimento quanto na estabilidade do sistema


> Link para a discussão: [GitHub Issue](https://github.com/JustFly1984/react-google-maps-api/issues/3250#issuecomment-2040911673)


# **Recomendações**

* Avaliar a abordagem de migração para a `@visgl/react-google-maps` pela estabilidade e suporte contínuo.
* Analisar custos e prazos associados ao retrabalho inicial versus a manutenção futura.