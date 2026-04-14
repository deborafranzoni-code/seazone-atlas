<!-- title: Termos de uso | url: https://outline.seazone.com.br/doc/termos-de-uso-am4a8AolkC | area: Tecnologia -->

# Termos de uso

Este documento tem como propósito registrar as mudanças e ações necessárias para o novo fluxo de termos de uso

## Novas tabelas

Serão criadas novas tabelas próprias para o armazenamento de dados dos termos de uso e do aceite desses termos pelos usuários.

### Tabela terms_of_use

Essa tabela será responsável por armazenar os dados de um determinado termo de uso. Ela seguirá a seguinte estrutura

| Campo | Tipo | Nullable | Descrição | Obs |
|----|----|----|----|----|
| `id` | `primary_key` | `false` | ID do termo de uso | auto generated |
| `created_at` | `datetime` | `false` | Data de criação do registro | `default now()` |
| `updated_at` | `datetime` | `false` | Data de alteração do registro | `default now()` |
| `date_ref` | `date` | `false` | Data de referência do termo. Data em que o termo passa a ser válido |    |
| `version` | `varchar` | `false` | Versão do termo de uso | padrão `vX.X`(`v1.0`, `v2.0`…) |
| `s3_key` | `varchar` | `false` | Chave do arquivo de testconteúdo do termo de uso no S3 |    |
| `target_role` | `enum` | `false` | Função que deve ser afetada pelo termo de uso | valores: `owner`, `host`, `partner` |
| `is_active` | `bool` | `false` | Indica se o termo de uso está em vigor |    |

Para essa tabela, deve-se primeiramente criar o `enum` `target_role`.

```sql
CREATE TYPE
  target_role AS ENUM('owner', 'host', 'partner');
  
```

Após isso, o `enum` criado pode ser usado na criação da tabela.

```sql
CREATE TABLE
  terms_of_use (
  	id SERIAL PRIMARY KEY,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    date_ref DATE NOT NULL,
    version VARCHAR(4) NOT NULL,
    s3_key VARCHAR NOT NULL,
    target_role target_role NOT NULL,
    is_active bool NOT NULL
  );
  
```

### Tabela terms_of_use_acceptance

Essa tabela será responsável por armazenar os dados dos aceites dos termos de uso.

| Campo | Tipo | Nullable | Descrição | Obs |
|----|----|----|----|----|
| `id` | `primary_key` | `false` | ID do termo de uso | auto generated |
| `created_at` | `datetime` | `false` | Data de criação do registro | `default now()` |
| `updated_at` | `datetime` | `false` | Data de alteração do registro | `default now()` |
| `accepted_at` | `datetime` | `false` | Data de aceitação do termo | `default now()` |
| `user_ip` | `varchar` | `false` | IP do usuário que aceitou o termo |    |
| `user_agent` | `varchar` | `false` | Agent do usuário que aceitou o termo |    |
| `terms_of_use_id` | `int foreign key` | `false` | ID do termo de uso | tabela `terms_of_use` |
| `user_id` | `int foreign key` | `false` | ID do usuário | tabela `account_user` |

```sql
CREATE TABLE
  terms_of_use_acceptance (
  	id SERIAL PRIMARY KEY,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    accepted_at TIMESTAMP NOT NULL DEFAULT NOW(),
    user_ip VARCHAR NOT NULL,
    user_agent VARCHAR NOT NULL,
    terms_of_use_id int NOT NULL,
    user_id int NOT NULL,
    CONSTRAINT fk_terms_of_use FOREIGN KEY (terms_of_use_id) REFERENCES terms_of_use(id) ON DELETE CASCADE,
    CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES "account_user"(id) ON DELETE CASCADE
  );
```

## Estrutura no S3

Os texto de conteúdo dos termos de uso ficarão armazenados no S3, respeitando um padrão de diretórios que permita o versionamento dos textos. A estrutura será como ilustrado a baixo.


 ![](/api/attachments.redirect?id=0047b400-aaa1-470e-a6f0-8dcf48c3a3a1 " =426x")

Com essa estrutura, é possível tanto versionar os termos de uso quanto separá-los por tipo de usuário alvo. 

O conteúdo será disponibilizado em um JSON que seguirá a seguinte estrutura.

```json
{
  "pt-br": {
    "title": str,
    "content": str
  },
  "eng": {
    "title": str,
    "content": str
  }
}
```

## Atualização de termos de uso

Quando uma nova versão de termos de uso for lançada, **um novo registro deve ser criado tanto no S3 quanto no banco de dados**. Registros antigos **não devem ser modificados.**

Para que um novo termo de uso seja inserido, deve ser seguido o seguinte fluxo:


1. Inserir um novo registro no S3, respeitando a organização de usuários alvo e versionamento;
2. Inativar no banco de dados os termos de uso dos usuários alvo;
3. Inserir o registro do novo termo de uso
4. Ativar o registro do novo termo de uso

Para fins de exemplo, usaremos uma atualização nos termos de uso de proprietários.

Para o passo 1, deve-se criar uma nova pasta no S3 dentro de `termos_of_use/owner` com a nova versão do termo. A estrutura deve ficar como a ilustrada a baixo.  


 ![](/api/attachments.redirect?id=e0ac99e0-8f0f-409d-a1d1-44079b407b0c)

Após isso, deve ser inativado os termos de proprietário antigos e inserido o novo (já ativado), o que pode ser feito com a seguinte transaction.

```sql
BEGIN;

// Passo 2
UPDATE
  terms_of_use
SET
  is_active = false
WHERE
  target_role = 'owner'
  AND is_active = true;

// Passos 3 e 4
INSERT INTO
  terms_of_use (version, s3_key, target_role, is_active) 
VALUES ('v3.0', 'uri/of/new/object', 'owner', true);

COMMIT;
```

## Queries úteis

### Termo de uso mais recente

```sql
select * from terms_of_use where is_active and target_role = DESIRED_ROLE order by date_ref desc;
```

### Inserção de novo termo

```sql
BEGIN;

UPDATE
  terms_of_use
SET
  is_active = false
WHERE
  target_role = TARGET_ROLE
  AND is_active = true;

INSERT INTO
  terms_of_use (version, s3_key, target_role, is_active, date_ref) 
VALUES (NEW_VERSION, NEW_OBJECT_URI, TARGET_ROLE, TERM_STATUS, DATE_REF);

COMMIT;
```

### Termo ativo pendente pelo usuário

```sql
SELECT
  tou.*
FROM
  terms_of_use tou
LEFT JOIN terms_of_use_acceptance toua 
  ON tou.id = toua.terms_of_use_id AND toua.user_id = USER_ID
WHERE
  toua.id IS NULL
  AND tou.target_role = USER_ROLE
  AND tou.is_active;
```