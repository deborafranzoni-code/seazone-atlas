<!-- title: Links encurtados | url: https://outline.seazone.com.br/doc/links-encurtados-oBaZVgp6ck | area: Tecnologia -->

# Links encurtados

### Pág. Resultados da Busca | Link encurtado para pesquisa pelo código do imóvel

> Última atualização 07/07/2023 13:28

> [PR da primeira implementação](https://github.com/Khanto-Tecnologia/seazone-reservas-frontend/pull/143)

Há 3 lógicas implementadas para realizar o redirecionamento:


1. Quando o user acessa a url `/resultados-da-busca/` o sistema redireciona para a página de resultados com os filtros `default` (busca sem datas e sem destino, sem filtros).
   * **Exemplo**
     * Usuário acessa: <https://seazone.com.br/resultados-da-busca/>
     * Sistema redireciona o usuário para a página de resultados da busca, sem informar um destino, datas, ou qualquer outro filtro:

       ```html
       [https://seazone.com.br/resultados-da-busca/qualquer-destino?id=&destinationName=&checkin=&checkout=&adults=1&kids=0&babies=0&page=1](https://seazone.com.br/resultados-da-busca/qualquer-destino?id=&destinationName=&checkin=&checkout=&adults=1&kids=0&babies=0&page=1)
       ```
2. Quando o usuário acessa a URL `/resultados-da-busca/**s/{codigo_imovel}**` ele será leva a página de resultados da busca, aplicando o filtro pelo imóvel código do imóvel informado.

   `/s/`: Abreviação para ***"short"***

   É possível informar parte do código ou o código inteiro para realizar a busca.
   * **Exemplo**
     * Usuário acessa a URL: <https://seazone.com.br/resultados-da-busca/s/MAV>
     * Sistema redireciona o usuário para a página de resultados, filtrando pelo código (ou parte do código) informado na URL:

       ```html
        [https://seazone.com.br/resultados-da-busca/qualquer-destino?id=&destinationName=&checkin=&checkout=&adults=1&kids=0&babies=0&page=1&property_code=FDU](https://seazone.com.br/resultados-da-busca/qualquer-destino?id=&destinationName=&checkin=&checkout=&adults=1&kids=0&babies=0&page=1&property_code=FDU)
       ```
3. Além da forma dita no **item 2**, também é possível buscar da seguinte forma, informando o código do imóvel como parâmetro na URL: [seazone.com.br/resultados-da-busca/qualquer-destino\*\*?property_code=MAV001\*\*](https://seazone.com.br/resultados-da-busca/qualquer-destino?property_code=MAV001)

### Pág. Detalhes do Imóvel | Link encurtado para acessar diretamente a página de Detalhes do Imóvel

> Última atualização 07/07/2023 13:28

> [PR da primeira implementação](https://github.com/Khanto-Tecnologia/seazone-reservas-frontend/pull/143)

Atualmente, a lógica implementada se dá pela inserção do path `/s/{codigo_imovel}` na URL. Ao fazer isso, o usuário será levado direto para a página do imóvel, caso o código informado seja válido.

* **Exemplo**
  * Usuário acessar [seazone.com.br/s/RAI014](http://seazone.com.br/s/RAI014)
  * Sistema redireciona usuário para a página do imóvel de código igual a "RAI014": [https://seazone.com.br/studio-aconchegante-a-450m-mar-canasvieiras-rai014\*\*/44/\*\*adults=1;kids=0;babies=0](https://seazone.com.br/studio-aconchegante-a-450m-mar-canasvieiras-rai014/44/;/adults=1;kids=0;babies=0)
    * Para realizar essa busca, é feita uma busca pelo imóvel no código informado, e então redirecionado o usuário para a página dele. Para que seja carregada a página do imóvel, é preciso passar o ID dele no path da URL:

      ```html
      https://seazone.com.br/{titulo-do-listing}/**{property_id}**/{checkin};{checkout}/adults=1;kids=0;babies=0
      ```


---