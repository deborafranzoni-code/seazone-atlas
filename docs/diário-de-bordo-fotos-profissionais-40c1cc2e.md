<!-- title: Diário de bordo - Fotos profissionais | url: https://outline.seazone.com.br/doc/diario-de-bordo-fotos-profissionais-Vysb7ed6eu | area: Tecnologia -->

# Diário de bordo - Fotos profissionais

# Google Drive

## Acesso à fotos e pastas no Google Drive

A fim de buscar as informações no Google Drive, foi realizada a criação de uma credencial do tipo `Google Service Account API`. Esse tipo de credencial age como uma "conta", que possui um e-mail que pode ser utilizado para compartilhar arquivos específicos com o "usuário".

\n**Email:** `criacao-anuncio-fotos-gdrive@sandbox-439302.iam.gserviceaccount.com`


Foi solicitado, à equipe responsável por organizar as fotos do drive, o compartilhamento da pasta "raiz" de informação com a conta em questão - dessa forma, a mesma possuirá acesso a todas as sub-pastas da operação - e consequentemente à todos os diretórios de fotos para a criação de anúncio.


**OBS**: A credencial do Google Drive foi salva como `Drive Fotos Profissionais` , e pode ser reutilizada na configuração dos nós que exijam acesso às fotos

## Pesquisa de arquivos em uma pasta

Ao analisar um link de pasta no Google Drive, o mesmo possui a seguinte anatomia:

\nURL: `https://drive.google.com/drive/folders/1VwOPQ3LEeqjBE-51r-YqWjzy7_nzNXmO`

Protocolo+Domínio+Path: `https://drive.google.com/drive/folders` 

Id pasta: `1VwOPQ3LEeqjBE-51r-YqWjzy7_nzNXmO`\n\nUsando o ID da pasta é possível realizar uma Query (Nó de GDrive no N8N) a fim de buscar pastas e arquivos "filhos".

 ![](/api/attachments.redirect?id=b7380ab5-6bf6-4ea2-a3fb-ef33e09cc13f " =556x442")

## Download de arquivos

Arquivos podem ser armazenados a partir de seu ID ou URL.

Considerando que a listagem de itens em uma pasta traz os IDs de todos os itens contidos nessa, a opção mais adequada para o fluxo é realizar o download de cada arquivo por meio da informação de seu ID.

 ![](/api/attachments.redirect?id=6761feab-d322-4ed5-89bf-fdd906510822 " =556x442")

A ferramenta permite "salvar" o arquivo em um field específico de output - podendo esse ser usado em futuras etapas.


# Stays

## Get de Cômodos da Propriedade

**GET** `https://ssl.stays.com.br/external/v1/content/listing-rooms/:listingId`

* Response

```json
[
    {
        "_id": "6434810a6048c715dbb66d64",
        "_idlisting": "604e42ff500e5de7df1a1e11",
        "_idtype": "5ab8f8a2f6b2dc2e97f9704f",
        "beds": [
            {
                "_id": "5ab8f8a2f6b2dc2e97f97041",
                "_i_count": 2
            }
        ],
        "images": [
            {
                "_id": "650212cc058c43f7efbf943b"
            },
            {
                "_id": "650212ccfcea6ee7574ae5cb"
            },
            {
                "_id": "650212d2058c43f7efbf9448"
            },
            {
                "_id": "650212d2fe266843e1c17906"
            },
            {
                "_id": "650212d4fcea6ee7574ae5cd"
            }
        ],
        "_i_order": 0
    },
    {
        "_id": "6434814c870d6ecc3ebf06cb",
        "_idlisting": "604e42ff500e5de7df1a1e11",
        "_idtype": "5ad9b01422261d6cda27d3e1",
        "beds": [],
        "images": [
            {
                "_id": "650216226ad94d10e8db9853"
            }
        ],
        "_i_order": 1
    }
]
```

seleciona o quarto desejado com o idtype

## Upload de Fotos

Antes de podermos vincular uma foto a um comodo, temos que fazer o upload via  **POST** `https://ssl.stays.com.br/external/v1/content/upload-images`

* Adicionar content-type

| Content-Type | multipart/form-data |
|----|----|

* Adicionar Imagem no Form-Data

!\[\[Pasted image 20260226134849.png\]\]

* Performar o Post
* Response

```json
[
    "69a07d919923e0a093e79ebc"
]
```

## Update do Quarto

Para realizar o update a gente precisa dos dados anteriores do quarto + a imagem que queremos por no final da lista via **PATCH** `https://ssl.stays.com.br/external/v1/content/listing-rooms/:listingId/:roomId`

* Payload

```json
{
    "_idtype": "5ab8f8a2f6b2dc2e97f9704f",
    "beds": [
            {
                "_id": "5ab8f8a2f6b2dc2e97f97041",
                "_i_count": 2
            }
        ],
    "images": [
        {
            "_id": "650212cc058c43f7efbf943b"
        },
        {
            "_id": "650212ccfcea6ee7574ae5cb"
        },
        {
            "_id": "650212d2058c43f7efbf9448"
        },
        {
            "_id": "650212d2fe266843e1c17906"
        },
        {
            "_id": "650212d4fcea6ee7574ae5cd"
        },
        {
            "_id": "69a07d919923e0a093e79ebc" /*O Id da nossa imagem nova*/
        }
    ]
}
```

* Response

```json
{
    "_id": "6434810a6048c715dbb66d64",
    "_idlisting": "604e42ff500e5de7df1a1e11",
    "_idtype": "5ab8f8a2f6b2dc2e97f9704f",
    "beds": [
        {
            "_id": "5ab8f8a2f6b2dc2e97f97041",
            "_i_count": 2
        }
    ],
    "images": [
        {
            "_id": "650212cc058c43f7efbf943b"
        },
        {
            "_id": "650212ccfcea6ee7574ae5cb"
        },
        {
            "_id": "650212d2058c43f7efbf9448"
        },
        {
            "_id": "650212d2fe266843e1c17906"
        },
        {
            "_id": "650212d4fcea6ee7574ae5cd"
        },
        {
            "_id": "69a07d919923e0a093e79ebc"
        }
    ],
    "_i_order": 0
}
```

Existe um grave efeito colateral de ser deletado as tags das fotos, ainda precisa ser resolvido