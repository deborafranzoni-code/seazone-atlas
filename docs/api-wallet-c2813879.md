<!-- title: [API] Wallet | url: https://outline.seazone.com.br/doc/api-wallet-e1IHl80eKd | area: Tecnologia -->

# [API] Wallet

1. Clone o projeto na pasta desejada

```bash
git clone https://github.com/seazone-tech/wallet-service/
```



2. Dentro do projeto, crie uma pasta para o ambiente virtual

```bash
mkdir .venv
```



3. Na pasta do projeto, crie o venv com o comando

```bash
python3 -m venv ~/path/to/project/.venv/wallet-service
```



4. Ative o ambiente virtual

```bash
source .venv/wallet-service/bin/activate
```



5. Baixe as dependências

```bash
pip install -r requirements.txt
```



6. Rodar o projeto

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload 
```


:::info
Talvez seja necessário exportar o PYPATH `export PYTHONPATH=$(pwd)/app`

:::



7. Rode o arquivo `docker-compose.yml`

```bash
docker compose up -d
```



8. Em um navegador, acesse `localhost:8000/docs`. Deve ser exibida a tela inicial do swagger

 ![](/api/attachments.redirect?id=e9c7bfeb-2684-4692-ae6c-33559464a221 " =1714x716")


:::success
Finalizamos por aqui **✅**

:::


\n