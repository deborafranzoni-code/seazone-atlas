<!-- title: Ferramentas | url: https://outline.seazone.com.br/doc/ferramentas-MZHTjKKwqs | area: Tecnologia -->

# Ferramentas

## **Orquestradores**

* **n8n** – Orquestrações de negócio, integrações entre sistemas, APIs e fluxos operacionais
* **GitHub Actions** – CI/CD das automações, versionamento e deploy
* **Kestra** – Execução de scripts complexos (Python, Go, JS), pipelines técnicos e agentes de IA mais avançados
  * POC Apresentação ao time web
* Argo-workflows - (Depreciado)
  * Migrar workflows para kestra

## Base de Dados

* **Postgres** (Cloud SQL - Instancia de Tools) \*Criar épico - @[John Paulo da Silva Paiva](mention://a1e13a26-3622-4bc7-9124-75eb70a7f450/user/fe961e04-fb16-4dab-b8b9-0d6428861ad2)  @[Yuri Braga de Castro Myakava](mention://67f4b17b-b945-4a37-98c9-d65ecacce4fe/user/f4030b8e-09dc-48b3-8fef-1a29fee300cd)  @[Gustavo Felipe Rodrigues Barbosa](mention://43e29e77-0481-4728-b174-a16bcbc7ef55/user/37cfa6bf-3985-4c68-a1ae-ae769143281d) 
  * Documentar como usar e deixar disponivel para o publico
  * Definir bases de dados e tabelas que serão usadas pela automaçao 
  * Padronizar nomenclaturas
  * Extensão pgvector para usar como banco de dados vetorial
  * Novos desenvolvimentos utilizaram o postgres
* **Redis** (filas, cache e controle de concorrência)
  * Definir padrao, como usar, doc.
  * Limite de 16 bases de dados (0 a 15) (outline já usa 1)
* **S3 ou GCS** (armazenamento de arquivos e artefatos)
  * Documentação como usar
  * Criar credenciais com permissoes minimas ao bucket
* **Baserow** - (Depreciado)
  * Migrar bases para postgres
  * Mapear quem tá usando
  * Avisar da depreciação

## **Frontend Interno (parametrização das automações)**

* **Retool** (painéis internos, CRUDs, parametrizações)
  * Migrar views do baserow para ele, usando postgres
  * Para todas as automações parametrizáveis, criar tela no ==Retool== @[Geozedeque Guimaraes Souza](mention://61a85044-3a21-4346-bede-9cba969d8810/user/2ab30d55-15ef-4247-bac7-4470c61a9b46)  adicionar como requisito para entrega.

## Inteligência Artificial

* **Gemini (Google)**
  * Criar e padronizar as credenciais
* OpenAI
  * Criar e padronizar as credenciais

> (Recomendado criar uma camada interna para desacoplar os provedores de IA dos fluxos.)

## Versionamento

* **GitHub**
  * Adicionar fluxos antigos no versionamento
  * Todos os novos em produção devem estar versionados (importante confirmar se foi versionado)

## Monitoramento e Observabilidade

* **Dashboards**
  * **Grafana**
  * **Retool**
  * **Metabase**
* **Alertas (via slack, ntfy e/ou whatsapp)**
  * Kuma
  * Alerts Grafana

## Mensageria e Notificações

* Slack (notificações internas)
* SES (e-mails transacionais) verificar alternativas com google