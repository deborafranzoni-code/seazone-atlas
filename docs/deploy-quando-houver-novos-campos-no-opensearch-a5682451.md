<!-- title: Deploy quando houver novos campos no opensearch | url: https://outline.seazone.com.br/doc/deploy-quando-houver-novos-campos-no-opensearch-nEd3htezbc | area: Tecnologia -->

# Deploy quando houver novos campos no opensearch

Ao realizarmos um deploy para staging e/ou produção, é executado um código chamado `create_indexes` que executa uma série de instruções viabilizando a criação desses campos (índices) no opensearch.

Em algumas situações, esses campos são preenchidos apenas depois de executarmos alguns códigos, como por exemplo o `pull_properties` que indexa propriedades no opensearch.

* Caso tentemos **acessar um campo que ainda não foi indexado** teremos um erro, fazendo com que a aplicação quebre.
* Caso tentemos **realizar uma operação** para ordernar um campo que ainda não recebeu seus respectivos valores e está com o valor `null` , por exemplo, também faremos com que a aplicação quebre.

Para evitar que esses problemas acontecam, podemos separar os deploys em duas partes:


1. **Subir o deploy com as alterações que realizam as indexações e a atribuição dos valores aos seus respectivos campos.**
2. **Subir o deploy com os códigos que utilizam e realizam operações com estes campos adicionados.**

**OBS**:

* Algo interessante a se fazer é **localmente** escrever todo o fluxo de código desde a adição dos novos campos e a utilização deles dentro dos contextos onde serão necessitados, realizar os testes necessários para assegurar que o código está se comportando como o esperado e também atendendo as regras de negócio do projeto/tarefa. Caso esteja tudo certo com o seu código, comente as utilizações desses campos nos locais onde não estão sendo indexados/recebendo atribuições de valores, e suba o deploy como mencionado nos passos acima.

  **ex:**

  No cenário abaixo iremos tratar `campo_novo_teste` como o novo campo no nosso opensearch/sistema.

  Subimos o primeiro deploy com o código que cria os índices contendo os novos campos e também os que atribuem valores à eles e ao realizarmos o primeiro deploy (passo 1)  o código que utiliza estes campos devem estar comentados, no caso abaixo, o campo`campo_novo_teste`:

  ```python
  # Neste trecho de código estamos criando ou atualizando 
  # valores aos campos do índice chamado indice_exemplo
  opensearch.update(
  	index="indice_exemplo",
  	body={
  	    "doc": {
  	        "campo_antigo_teste": campo_antigo,
  	        "campo_novo_teste": campo_novo,
  	    },
  	    "doc_as_upsert": True,
  	},
  	id=indice.id
  )
  
  # Imagine que aqui nós estamos falando do retorno de um endpoint
  # que não necessariamente irá rodar após o trecho de código acima.
  # São partes isoladas dentro do sistema e não estão estruturados
  # de maneira sequencial como podemos enxergar aqui.
  return {
          "total_results": len(response),
          "results": [
              IndiceExemploValor(
                  id=indice_exemplo_valor["_id"],
                  campo_antigo_teste=indice_exemplo_valor["_source"]["campo_antigo_teste"],
                  # campo_novo_teste=indice_exemplo_valor["_source"]["campo_novo_teste"],
              )
              for indice_exemplo_valor in indice_exemplo
          ]
      }
  ```

  Após realizar os deploys do código acima, staging e produção irão indexar esses novos campos e atribuir seus respectivos valores e então podemos seguir para a segunda parte do deploy que é subir o campo `campo_novo_teste` em suas utilizações descomentados:

  ```python
  opensearch.update(
  	index="indice_exemplo",
  	body={
  	    "doc": {
  	        "campo_antigo_teste": valor_campo_antigo,
  	        "campo_novo_teste": valor_campo_novo,
  	    },
  	    "doc_as_upsert": True,
  	},
  	id=indice.id
  )
  
  # Descomentamos o campo campo_novo_teste já que agora ele pode
  # ser acessado e tratado normalmente já que passou por todo o fluxo de
  # indexação e associação de valores à ele mesmo.
  return {
          "total_results": len(response),
          "results": [
              IndiceExemploValor(
                  id=indice_exemplo_valor["_id"],
                  campo_antigo_teste=indice_exemplo_valor["_source"]["campo_antigo_teste"],
                  campo_novo_teste=indice_exemplo_valor["_source"]["campo_novo_teste"],
              )
              for indice_exemplo_valor in indice_exemplo
          ]
      }
  ```