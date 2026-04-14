<!-- title: Documentação Técnica | url: https://outline.seazone.com.br/doc/documentacao-tecnica-xb2RbZ8mhe | area: Tecnologia -->

# Documentação Técnica

# SeaNotes - Documentação Técnica

Versão 0.1 (POC) | Seazone Tech

**Documentação de Apoio:** <https://github.com/seazone-tech/governanca-seanotes/blob/feature/docker/docs/README.md>


---

## Arquitetura

 ![](/api/attachments.redirect?id=5e70498d-24ff-4239-8b19-4db5c2e6f47e " =2816x1536")


```
Google Drive → Download → Gemini AI → Upload Insight
```

**Componentes:**

* `google_drive_auth.py`: OAuth 2.0
* `transcription_downloader.py`: Download (txt/md/Google Docs)
* `gemini_analyzer.py`: Análise com Gemini
* `processed_files_tracker.py`: Tracking de arquivos processados


---

## Setup

```bash
# Clone e instale

git clone https://github.com/seazone-tech/poc-transcribe-governanca.git

cd poc-transcribe-governanca

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

# Configure

cp config/.env.example .env
# Edite .env com GEMINI_API_KEY

# Credenciais Google (OAuth 2.0)
# 1. https://console.cloud.google.com/apis/credentials
# 2. Criar OAuth 2.0 Client ID (Desktop)
# 3. Download → credentials.json (raiz do projeto)

# Primeiro login

python main.py  # Gera token.json
```


---

## Execução

**Manual:**

```bash

python main.py
```

**Docker:**

```bash

docker-compose up -d
```


---

## Estrutura

```
src/
├── app/main_insights.py          # Pipeline principal
├── core/
│   ├── google_drive_auth.py      # OAuth
│   └── processed_files_tracker.py # Tracking
└── services/
    ├── transcription_downloader.py
    └── gemini_analyzer.py
```


---

## Sistema de Tracking (last_check)

O SeaNotes usa arquivos `.last_check_{folder_id}.json` para controlar quais transcrições processar.

**Como funciona:**

Na primeira execução, o arquivo `.last_check` não existe:

* Processa **todos** os arquivos da pasta
* Cria `.last_check_{folder_id}.json` com timestamp atual

Nas próximas execuções:

* Lê o timestamp do `.last_check`
* Processa apenas arquivos **modificados após** esse timestamp
* Atualiza o `.last_check` com novo timestamp

**Estrutura do arquivo:**

```json
{
  "folder_id": "1ABC...",
  "last_check": "2024-12-03T14:30:00Z",
  "processed_files": {
    "file_id_1": {
      "name": "reuniao.txt",
      "modified_time": "2024-12-03T10:00:00Z",
      "processed_at": "2024-12-03T10:15:00Z"
    }
  }
}
```

**Localização:** `{OUTPUT_DIR}/.last_check_{folder_id}.json`

**Forçar reprocessamento:**

```bash
# Deletar tracking de uma pasta específica

rm output/.last_check_1ABC*.json

# Deletar todos

rm output/.last_check*.json

# Ou usar flag

python main.py --force
```


---

## Configuração (.env)

```env

GOOGLE_DRIVE_FOLDER_ID=           # Vazio = auto-discovery

GEMINI_API_KEY=sua_key            
ENABLE_GEMINI_ANALYSIS=true

OUTPUT_DIR=./output
```


---

## Agendamento

**n8n:**

* Trigger: Schedule (15 min)
* Action: `docker-compose run --rm seanotes`

**Cron:**

```bash
*/15 * * * * cd /path/to/seanotes && docker-compose run --rm seanotes
```


---

## Troubleshooting

**"Nenhum arquivo encontrado":**

```bash

python scripts/debug_drive.py

python main.py --force  # Reprocessa tudo
```

**"Erro de autenticação":**

```bash

rm token.json

python main.py
```


---

Seazone Tech | v0.1