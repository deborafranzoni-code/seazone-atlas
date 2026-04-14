<!-- title: SonarQube | url: https://outline.seazone.com.br/doc/sonarqube-8iZWSt38eD | area: Tecnologia -->

# SonarQube

## Fluxo/processo

Foi feito deploy para um servidor central em produção. A dinâmica está funcioanndo da seguinte forma:

A análise é executada no ambiente local e envia os dados para o servidor em produção. É possível também rodar localmente, basta alterar as variáveis de ambiente, conforme descrito no próximo tópico.

As configurações do Scanner ficam dentro do arquivo 'sonar-project.properties', incluindo informações como: nome do projeto, host e token de autenticação.

## Ambiente local

Em ambos projetos (front e back) é necessário criar duas variáveis de ambiente:

* *SONAR_HOST_URL → contém o servidor para onde os reports devem ser enviados*
* *SONAR_TOKEN → token de autenticação para que seja possível enviar os reports*

Foram criados dois containers no docker-compose.yml, tanto no front quanto no back, localmente para rodar o SonarQube: o servidor e o scanner.

O SonarQube seta automaticamente um usuário 'admin' com a senha também 'admin'. Para gerar o token, basta ir no ícone na lateral superior direito no painel, clicar em 'My account' e em seguida na aba 'Security', conforme imagem.

 ![Screenshot from 2023-10-31 18-41-44.png](/api/attachments.redirect?id=99ec27b0-9715-4dba-9de8-fd027e8e079a)

**Frontend** Variáveis de ambiente para servidor local:

* *SONAR_HOST_URL:* [http://sonarqube-front:9000](http://sonarqube-front:9000/)
* *SONAR_TOKEN: token gerado após logar com o usuário padrão, descrito abaixo.*

O acesso local ao servidor pode ser feito no url: http://localhost:10000.

Para executar o servidor local basta executar o comando `docker-compose up sonarqube-front`.

Após o servidor subir, o scanner pode ser executado com o comando `docker-compose up scanner-front`.

**Backend**

Variáveis de ambiente para servidor local:

* *SONAR_HOST_URL:* [http://sonarqube-backend:9000](http://sonarqube-front:9000/)
* *SONAR_TOKEN: token gerado após logar com o usuário padrão, descrito abaixo.*

O acesso local ao servidor pode ser feito no url: http://localhost:9000.

Para que a cobertura de testes possa ser medida, foram instaladas algumas bibbliotecas antes e feita uma configuração no arquivo '.coveragerc'. É necessário rodar o comando `coverave xml`, que irá gerar um arquivo xml que será lido pelo scanner.

Para executar o servidor local basta executar o comando `docker-compose up sonarqube_backend`.

Após o servidor subir, o scanner pode ser executado com o comando `docker-compose up scanner_backend`.

## Servidor de Produção

Para que o envio seja feito para o servidor em produção. basta alterar a variável *SONAR_HOST_URL para 'https://sonar.sapron.com.br' e a variável SONAR_TOKEN para o respectivo token do seu usuário.*

**Frontend**

O scanner pode ser executado com o comando `docker-compose up scanner-front`.

**Backend**

Para que a cobertura de testes possa ser medida, foram instaladas algumas bibbliotecas antes e feita uma configuração no arquivo '.coveragerc'. É necessário rodar o comando `coverave xml`, que irá gerar um arquivo xml que será lido pelo scanner.

O scanner pode ser executado com o comando `docker-compose up scanner_backend`.

Os dados são persistidos no banco de dados de produção. As informações de acesso desse banco estão no Vault.