<!-- title: Getting Started | url: https://outline.seazone.com.br/doc/getting-started-7L9JsczFwi | area: Tecnologia -->

# Getting Started

This wiki is built in Notion. Here are all the tips you need to contribute.

# Sapron || Backend

O projeto do backend está na pasta `sapron-pms-web/backend`.

> ATENÇÃO¹: executar todos os comandos abaixo no diretório raiz do projeto

> ATENÇÃO²: Você pode seguir este README até o fim da seção PostgreSQL e rodar o comando make setup


---

## Requisitos

* Ambiente virtual

```
python3 -m pip install --upgrade pip # Atualiza o pip
python3 -m pip install virtualenv # Instala o pacote virtualenv

python3 -m venv .venv # Cria uma virtualenv para o projeto
source ~/Projects/sapron-pms-web/.venv/bin/activate # Ativa a venv
pip install -r backend/requirements-dev.txt # Instala os requisitos
```

* Docker e Docker Compose

  Utilizamos o `docker` e o `docker-compose` para o ambiente de desenvolvimento. Para instalar basta seguir os passos descritos na documentação oficial:
  * [Docker](https://docs.docker.com/engine/install/ubuntu/)
  * [Docker-Compose](https://docs.docker.com/compose/install/)


---

## PostgreSQL

O PostgrsSQL é executado através do container `db`, configurado no arquivo `docker-compose.yml`.

### Iniciando o banco

```bash
docker-compose up -d db
```

### Gerando e rodando migrations

* **Python Manage**

```bash
# Gerar migrations para todos os apps
python backend/manage.py makemigrations
# Roda migrations
python backend/manage.py migrate
```

```bash
# Gerar migrations para o app financial
python backend/manage.py makemigrations financial
# Roda migration
python backend/manage.py migrate
```

* **Makefile**

```bash
# Gerar migrations para todos os apps
make migrate-generate
# Roda migrations
make migrate-run
```

### Inserindo dados no DB

Para popular o banco, primeiro é necessário **apagar todos os dados**

```bash
./cli/python backend/manage.py flush # Limpar todas as tabelas
./cli/python backend/manage.py filler # Popula o banco
```


---

## Rodar o backend

### DotEnv

Para rodar o projeto será necessário configurar o arquivo `.env` contendo `secrets` do projeto.

```bash
cp .env.dist .env # .env na raiz:
cp backend/.env.dist backend/.env # .env no backend/
```

### RUN

* Python `python3 backend/manage.py runserver`
* Makefile `make docker-backend`
* docker-compose `docker-compose up -d web`
* Rodar o linter flake8: `python3 -m flake8`

Acesse a documentação dos endpoints da `*API*`:

<http://localhost:8000/swagger/>


---

## Como contribuir

Esse projeto usa uma versão modificada do Git Flow.

Todo novo desenvolvimento deve ser iniciado a partir da branch main. Quando o desenvolvimento estiver pronto para ser revisado, crie um `pull request` comparando a sua branch com a main.

### Nomenclatura de branch

> Novas funcionalidades: <br /> git checkout feature/<NOVA-FUNCIONALIDADE>
>
> **Correção de bugs**: <br /> `git checkout fix/<CORREÇÃO>`

### Padrão de mensagens em seus commits

Caso o `CHANGELOG` e a adição de `releases` sejam implentados, as mensagens de commits deve ser padronizadas para atender os requisitos da funcionalidade. Utilizamos **mensagens em inglês** para descrever nossas modificações. Procure seguir o padrão definido pelo time de desenvolvimento do [Angular](https://github.com/angular/angular/blob/22b96b9/CONTRIBUTING.md#-commit-message-guidelines).

> Para facilitar a escrita de bons commits, \n instale a extensão do VSCode visual studio code commitizen support. \n Após adicionar suas modificações com git add file \n Pressione ctrl+shift+P\n Pesquise por commitizen: conventional commits e pressione enter. \n A biblioteca fará um pequeno questionário sobre seu commit e formulará a mensagem para você.\n Ao fim, git push -u origin <branch>

Caso queira utilizar o terminal, siga os prefixos:

```bash
git commit -m 'feat: message' # <new feature>
git commit -m 'fix: message' # <documentation a bug fix>
git commit -m 'docs: message' # <documentation only>
git commit -m 'style: message' # <changes that do not affect the meaning of the code>
git commit -m 'refactor: message' # <neither fixes a bug nor adds feature>
git commit -m 'perf: message' # <a code change that improves performance>
git commit -m 'test: message' # <adding missing tests or correcting existing tests>
git commit -m 'build: message' # <changes that affect the build or dependecies>
git commit -m 'ci: message' # <changes to our CI conf files>
git commit -m 'chore: message' # <changes that do not modify src or test files>
```

> Para mais informações veja [CONTRIBUITING.md](https://github.com/billbenettiSeazone/sapron-pms-web/blob/main/CONTRIBUTING.md)