<!-- title: Anatomia de um Scraper | url: https://outline.seazone.com.br/doc/anatomia-de-um-scraper-hOfXDfO2ZX | area: Tecnologia -->

# Anatomia de um Scraper

Na construção de diversos scrappers, notamos uma série de padrões. Para garantir a qualidade do nosso produto, pedimos que todos os Scrappers tenham, no mínimo:


 1. Documentação - outline

    Todo scrapper deve estar documentado [aqui](/doc/scrapers-5CqGAwYiZM).
 2. Orquestração - Airflow

    Todo Scrapper deve rodar periodicamente. Utilizamos o Airflow como ferramenta para garantir e organizar a execução. Nosso Airflow é hosteado a AWS no MWAA.
 3. Repositório de código - Github

    Todo Scrapper é composto por scripts (normalmente python), que devem estar em um repositório próprio no Github.
 4. Repositório de arquivos - S3

    Todo Scrapper precisa de um repositório para arquivos que utiliza (Bill, pq q isso é necessário?).
 5. Sistema de filas - SQS Para garantir que, dada a falha na scrappagem, não haja perda de dados, é necessário a utilização de um sistema de filas. Normalmente utilizamos a SQS na AWS.
 6. Task Definition na ECS

    Todo Scrapper possúi, atomicamente, um script que recebe uma lista de informações para obter, e a obtém na WEB. Utilizamos uma Task Definition na ECS contendo esse script conteinerizado.
 7. Cluster na ECS

    Precisamos de uma infraestrutura que realiza o processamento necessário do Scrapper. Utilizamos um cluster na ECS para isso.
 8. Service na ECS

    Como temos um volume muito grande de dados para serem obtidos, utilizamos várias tasks definitions em paralelo. Dessa forma, o Airflow aciona um service que é responsável pela orquestração de múltiplas Task Definitions em paralelo.
 9. Testes

    Testes são uma parte fundamental do desenvolvimento de qualquer software. Eles facilitam a manutenção, permitindo rápidas verificações do funcionamento do código, mesmo após várias edições.

    Temos um talks sobre testes unitários disponível **[aqui.](https://drive.google.com/drive/folders/1DjEQeNT43APBwd91qpHCsJS2Tb9mPI9E)**
10. Repositório de Containers - ECR

    Utilizamos um repositório com os containers utilizados em diversos projetos.
11. Continuous Integration Service - Github Actions

    Para garantir que mudanças feitas no Scrapper são colocadas em produção, utilizamos o Github Actions
12. Detecção de falhas

    Todo Scrapper precisa de um sistema de detecção de falhas, que envia um email ou mensagem no slack havendo falhas na DAG, no script, ou se os dados obtidos não estiverem coerentes. Existem 4 falhas que devem ser detectadas sempre que ocorrerem:

    
    1. Falha na DAG/Script

       
       1. Representa um script que encerrou com um erro.
    2. Falha na inserção dos dados

       
       1. Apesar do script ter sido concluído com sucesso, é possível que os dados não tenham sido inseridos no banco, se o banco travar, por exemplo.
    3. Falha dos valores

       
       1. Se os dados não fazem sentido ou não estão de acordo com a realidade, como uma diária por R$10,00 quando deveria ser R$1000,00.
    4. Falha na captura dos dados

       
       1. A API alterou a estrutura da resposta, ou o site está em manutenção.
13. Variáveis de ambiente Os scrappers precisam de parâmetros que são definidos como variáveis de ambiente para facilitar a sua mudança sem necessitar mudar o código. Definir quais variáveis são de ambiente e onde estão definidas é parte importante do processo.


\
 👉 Confira aqui a call de Livecoding de scrapers com @Francisco Silveira Burigo e @Augusto Hideki passando por alguns princípios básicos de scrapagem em uma demonstração de dois métodos:

* scrapagem de HTML de página estática usando BeautifulSoup
* scrapagem pelas APIs públicas de um site


[https://drive.google.com/file/d/1-f%5FVVLx9xaYPKbMMxMXB1VYHeHTTEEf1/view](https://drive.google.com/file/d/1-f%5FVVLx9xaYPKbMMxMXB1VYHeHTTEEf1/view)