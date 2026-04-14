<!-- title: Website de Reservas: Queda  da Taxa de Conversão Global | url: https://outline.seazone.com.br/doc/website-de-reservas-queda-da-taxa-de-conversao-global-Mj62CzJefi | area: Tecnologia -->

# Website de Reservas: Queda  da Taxa de Conversão Global

### 1. Resumo

A taxa de conversão estava crescendo desde outubro e, repentinamente, apresentou queda próxima a 18 de dezembro. Este documento tem como objetivo diagnosticar os pontos críticos do funil de conversão e propor ações de melhoria para recuperar e potencializar a performance do site.

 ![](/api/attachments.redirect?id=8d69fd77-87e8-4c1b-b033-e306e946bb93 " =1189x561")


 ![](/api/attachments.redirect?id=4e02cf27-5bba-49f8-be2c-6b3f342194c8 " =1192x564")

### 2. Análise do Funil de Conversão

O funil foi dividido em quatro etapas principais:

* **Home → Busca:** A entrada dos usuários e a transição para a busca de imóveis.
* **Busca → Imóvel:** A entrada dos usuários e a transição para a busca de imóveis. ( não foi abordada aqui pois não sofreu quedas de conversão).
* **Imóvel → Confirmar e Pagar:** Navegação na página do imóvel e início do processo de reserva.
* **Confirmar e Pagar → Gateway:** Fluxo crítico de finalização do pagamento.
* **Checkout na Plataforma de Tuna:** Pagamento dentro da plataforma tuna


## Diagnóstico do Funil

### Home → Busca

 ![](/api/attachments.redirect?id=cc288b83-adb2-4a65-b0ec-584faf8f12c3 " =1184x560")

A performance da Home vem caindo e foram identificados pontos de melhoria, porém nada que seja extremamente crítico para a queda da taxa de conversão global.

#### 3.1. Home → Busca: Pontos de melhoria

* **Autocomplete não configurado corretamente**\n*Problema:* O autocomplete não reconhece o destino completo digitado.\n*Solução:* Ajustar as regras de configuração para melhorar o match com os termos pesquisados.
* **Redirecionamento inadequado ao apertar "Enter"**\n*Problema:* Usuários digitam o nome da localidade e, ao pressionar "Enter", são direcionados para resultados irrelevantes (ex.: predominância de "Campos do Jordão").\n*Solução:* Direcionar o usuário para a primeira cidade sugerida pelo autocomplete ou, na ausência de resultados, para uma página que liste todas as opções.
* **Carregamento lento dos cards de cidades**\n*Problema:* Imagens dos cards estão demorando para carregar.\n*Solução:* Investigar e otimizar a infraestrutura de CDN para melhorar a velocidade de carregamento.
* **Banner de promoções oculto**\n*Problema:* O banner que divulga cupons e promoções foi escondido nas alterações de design, perdendo seu potencial de aumentar as vendas.\n*Solução:* Reabrir a home com a aba de promoções visível.
* **Baixa navegabilidade dos ícones (cabana, pé na área, resorts, etc.)**\n*Problema:* Ícones que deveriam ser interativos não aparecem clicáveis.\n*Solução:* Realizar um redesign para melhorar a usabilidade e a navegabilidade.
* **Exibição de "3 bolinhas" durante o carregamento**\n*Problema:* Indicador de carregamento pouco informativo que gera sensação de espera prolongada.\n*Solução:* Implementar um indicador de carregamento mais intuitivo e dinâmico.
* **Listagem de imóveis (especialmente cabanas) na página de busca**\n*Observação:* Atualmente, a nova home prioriza a exibição das cidades em vez dos próprios imóveis.\n*Impacto:* Baixo.
* **Exibição incorreta dos preços**\n*Problema:* Nos cards de cidades, o subtítulo exibe "Preços à partir de…" utilizando o preço máximo em vez do mínimo (ex.: "Florianópolis à partir de R$2000" ao invés de R$300).\n*Solução:* Corrigir a lógica de apresentação dos preços.

### Imóvel → Confirmar e Pagar

 ![](/api/attachments.redirect?id=204ac22a-4a94-40da-b114-e2096ed2e892 " =1187x559")

A página do imóvel também apresenta queda de performance

Problemas encontrados:


1. **Página do imóvel com datas passadas causando erros**\n*Problema:* Links compartilhados (por exemplo, via WhatsApp) podem conter datas passadas, resultando em falhas no carregamento da página.\n*Solução:* Implementar uma verificação que redirecione ou ajuste a data, prevenindo erros de timeout.
2. **Inconsistência na exibição de amenities**\n*Problema:* Alguns ícones de amenities estão ausentes ou mal exibidos.\n*Solução:* Revisar e padronizar a exibição dos ícones (considerada uma questão de menor criticidade).
3. **==Erro de upstream (extremamente crítico)==**

   *==Problema:==* ==É um erro de carregamento que vários usuários recebem uma tela preta em vez de conseguir acessar a página estão recebendo que envolve infra e frontend== \n*==Solução:==* ==Readequar a infra estrutura do site e mudar a maneira como o frontend está lidando com as chamadas às APIs.==

### Confirmar e Pagar → Gateway (A parte mais crítica)

 ![](/api/attachments.redirect?id=03aa2b5b-8a7a-40c9-9aac-22884425e8a6 " =1189x560")

Houve uma queda grande no início de dezembro que pode estar relacionada ao fluxo sem login. Pelo que foi investigado:

 ![](/api/attachments.redirect?id=926a6d14-a1aa-4ea1-ac6f-75b91306b641 " =1191x564")

O número de usuários que entra nessa página aumentou muito devido ao fluxo sem login porém…

 ![](/api/attachments.redirect?id=74d0e25d-478e-4b81-b228-87dea6707295 " =1198x562")

O número absoluto de usuários clicando que querem pagar caiu. 

**Por que não reverter para o fluxo com login ?**


1. O fluxo sem login foi implementado já tem alguns meses e desde lá houveram muitas mudanças e poucos testes realizados. Reviver o fluxo sem login não necessariamente seria uma volta positiva à esta altura. Além do que, demandaria muito esforço para devolver saúde aos componentes que ficaram sem testes durante os últimos meses. 
2. Os problemas do fluxo com login barravam muitas pessoas de comprar de fato. Com a remoção do login conseguimos mais do que dobrar o número de usuários que chegam à etapa final do funil. Eu gostaria de tentar converter esses usuários que estão chegando ali antes de reverter.
3. Caso o problema não dê sinais de melhoria até o final do mês de fevereiro, podemos colocar esforços para colocar no ar novamente o fluxo com login e ir acompanhando em forma de teste AB a performance do fluxo sem login aos poucos.

Quais o problemas atuais?


1. **Novo Layout do Fluxo Sem Login**

   O novo layout do fluxo sem login introduziu diversas mudanças simultâneas que não foram testadas isoladamente, o que pode ter contribuído para a queda na taxa de conversão.

   **Problema:**\nA implementação de múltiplas alterações ao mesmo tempo, sem a devida validação individual, pode ter gerado confusão e impactado negativamente a experiência do usuário.
2. **Posicionamento do Componente de Cupom**

   No layout antigo, a primeira interação do usuário na página era a inserção do cupom — um fator comprovado que impulsiona as vendas. Com as mudanças recentes, a solicitação do cupom ocorre somente após o preenchimento dos demais dados, o que pode aumentar o abandono do carrinho.

   **Solução Proposta:**\nRealizar um teste A/B na versão mobile, reposicionando o cupom para o topo da página, onde a alteração de design é mais simples e pode potencialmente melhorar a conversão.
3. **Indicação de urgência insuficiente**\n*Problema:* Não está claro para o usuário que o imóvel ficará reservado por apenas 30 minutos.\n*Solução:* Evidenciar a urgência na comunicação para incentivar a finalização da compra.
4. **Pagamento para usuários estrangeiros**\n*Problema:* Usuários estrangeiros não conseguem pagar com cartão de crédito devido à exigência de CPF.\n*Solução:* Estudar a liberação do cartão de crédito para estrangeiros.
5. **Comparação de preços com outras OTAs**\n*Problema:* Usuários realizam pesquisas de preços em outras plataformas, o que pode levar à desistência da compra.\n*Solução:* Exibir, de forma transparente, os preços praticados por outras OTAs na nossa página.

### Checkou dentro da Plataforma de Tuna 

A taxa de aprovação do tuna está bem alta:

 ![](/api/attachments.redirect?id=73fa15a2-acc4-4dfb-a3ea-4c5bb0f4e2c8 " =1187x560")

Porém… não podemos confundir taxa de aprovação com taxa de conversão.

O checkout deles tem uma taxa de conversão muito baixa, o que indica que muitos usuários não estão conseguindo prosseguir dentro do checkout deles até concluir a compra:

 ![](/api/attachments.redirect?id=c079562b-dfe0-419f-9f45-0b498bea6e11 " =1191x560")

Apesar desse checkout estar fora do nosso controle como performance, está no nosso controle a implementação de um gateway próprio.

**Exemplo de problemas que podemos atuar com baixo esforço:**

→ não consegue trocar a opção de pagamento → tuna mostra o seletor

→ pix no tuna nao está funcionando pagina de aguardando pagamento 

# Matriz de Impacto x Esforço dos problemas apresentados

| **Baixo Esforço / Alto Impacto** | **Esforço** | **Impacto** | Tipo | **Status** | **Prazo** |
|----|----|----|----|----|----|
| Autocomplete | 1 | 4 | Bug | 
:::tip
Em andamento

::: | 28/02 |
| Banner de promoções escondido | 1 | 2 | Bug | 
:::success
Done

::: | Entregue 23/01 |
| Preços na nova home errados | 1 | 4 | Bug | 
:::success
Done

::: | Entregue 23/01 |
| Teste AB no mobile com o cupom em cima  | 1 | 4 | Melhoria | 
:::success
Em Teste

::: |    |
| Liberar pagamentos no cartão para estrangeiros | 1 | 5 | Melhoria | 
:::tip
Em discovery

::: |    |
| Tela de aguardando pagamento: link para pagamento pix não funciona | 1 | 4 | Bug | 
:::success
Done

::: | Entregue 18/02 |
| Digitar nome da localidade e apertar enter: busca sem destino | 2 | 4 | Bug | 
:::success
Done

::: | Entregue 07/02 |
| Demora para carregar o card das cidades | 2 | 1 | Bug | 
:::warning
Não priorizado

::: |    |
| Navegabilidade baixa na home | 2 | 1 | Melhoria | Entra dentro do novo teste ab da nova home | 28/02 |
| Página do imóvel com datas passadas quebrando | 2 | 5 | Bug | 
:::info
Priorizado

::: | 28/02 |
| Inconsistência de amenities | 2 | 1 | Bug | 
:::warning
Não priorizado

::: |    |
| Não há indicativo de urgência | 2 | 3 | Melhoria | 
:::tip
Em andamento

::: | 28/02 |
| Barrar login na compra - teste ab | 2 | 2 | Melhoria | 
:::warning
Não priorizado

::: |    |
| Mensagem de erro durante a compra via celular | 2 | 5 | Bug | 
:::success
Done

::: | 28/02 |
| Problema na busca com crianças e bebês | 2 | 3 | Bug | 
:::success
Done

::: | Entregue 30/02 |
| Cupons de uso baseado em e-mail quebrando no fluxo sem login | 2 | 3 | Bug | 
:::success
Done

::: | Entregue 17/02 |
| Sumir com as 3 bolinhas | 3 | 2 | Melhoria | 
:::warning
Não priorizado

::: |    |
| Apresentar preço de outras OTAs | 3 | 4 | Melhoria | 
:::warning
Não priorizado

::: |    |
| Garantia de Preço Mínimo | 3 | 3 | Melhoria | 
:::warning
Não priorizado

::: |    |
| Barrar e-mails suspeitos de fraude de comprar no fluxo sem login para poder liberar a bahia para o carnaval | 3 | 5 | Bug | 
:::success
Done

::: | Entregue 17/02 |
| Usuários comprando sem nome e telefone | 3 | 4 | Bug | 
:::success
Done

::: | Entregue 31/01 |
| Checkout proprio | 5 | 5 | Melhoria | 
:::tip
Em discovery

::: | 30/04 |


\
# Updates 20 de Fevereiro


Os resultados das nossas ações podem ser percebidos das seguintes maneiras:


 ![](/api/attachments.redirect?id=e232e37c-bfde-4626-8ce5-658d4d9d9319 " =1189x548")

Percebemos que a home parece ter já se recuperado com as melhorias feitas principalmente:

* Preços aparecendo errado (aparecendo o preço máximo em vez do preço mínimo)
* Melhorias na busca ( melhorias de autocomplete e funcionalidade do enter )


 ![](/api/attachments.redirect?id=54cdc187-f491-4bd3-832a-656015c2cbea " =1183x553")

Percebe-se uma trend de alta, retomando aos patamares de novembro e isso se deve à:

* Estancamos problemas gerados por cupons inválidos
* Melhorias na usabilidade de campos no preenchimento 
* Bugs que não davam transparência de preço para o parcelamento do cartão
* Ainda está por vir:
  * Melhor feedback ao usuário do que já foi preenchido e do que ainda precisa ser preenchido


Mais evidências de que estamos no caminho certo:

 ![](/api/attachments.redirect?id=ebe7407e-06d1-49a7-9b46-c7fa9803d3ce " =1087x297")

No dia 19/02 conseguimos vender 94% das reservas sem problemas nos quais os hóspedes precisaram recorrer ao atendimento. No dia 20/02 subiram mudanças que causavam um bug de input de dados no campo do cpf que impediu algumas reservas diretas (como pode ser observado). Já no dia 21/02 após reverter as mudanças estamos novamente no caminho certo.


# Próximos passos

 ![](/api/attachments.redirect?id=3b85d7ae-bed2-4314-9698-76c0a3641d9d " =1441x714")

Esta é a tela atual de confirmar e pagar. O usuário as vezes tem dificuldade de entender o que ainda precisa ser preenchido para que o botão de confirmar e pagar se acenda.

Já esta é a versão com algumas melhorias de interface que deixam mais claro para o usuário o que deve ser feito e o motivo pelos quais coletamos dados como e-mail e telefone.

 ![](/api/attachments.redirect?id=01ff06b5-7b1e-4b7c-b98b-55c3f5ee4374 " =587x406")

É um teste que vamos fazer para entender se isso ajuda os usuários a completarem ainda mais esta etapa da reserva.


Outras pontos que podem ser considerados para melhorias futuras:

* Reforçar os pontos positivos da propriedade nessa tela.