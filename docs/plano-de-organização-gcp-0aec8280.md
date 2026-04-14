<!-- title: Plano de organização GCP | url: https://outline.seazone.com.br/doc/plano-de-organizacao-gcp-4nenDMIoEw | area: Tecnologia -->

# Plano de organização GCP

## 1. Visão Geral

Com a expiração dos créditos do Google Cloud em **07/01/2026**, este plano estabelece a nova estrutura de governança financeira para garantir a previsibilidade de gastos e a atribuição correta de custos por Unidade de Negócio (BU).


---

## 2. Nova Estrutura de Hierarquia (Organização)

Para facilitar a visualização de custos por BU e Produto, adotaremos a estrutura de **Pastas**:

* **Nível 1: Organização (seazone.com.br)**
* **Nível 2: Pastas por BU** (Ex: `BU-Gestao`, `BU-Vendas`, `BU-Tecnologia`)
  * *Objetivo:* Isolar orçamentos e facilitar relatórios agregados por diretoria.
* **Nível 3: Projetos por Produto/Ambiente** (Ex: `prop-backend-prod`, `data-cat-auto-strata-hml`)
  * *Objetivo:* Cada projeto deve representar um produto específico ou um ambiente de desenvolvimento/homologação.


---

## 3. Governança e Controle de Acesso

Para evitar gastos não planejados e a criação de "Shadow IT", aplicaremos as seguintes restrições:

### 3.1. Restrição de Faturamento (Billing)

* **Acesso Restrito:** Apenas os administradores de infraestrutura/financeiro possuirão o papel de `Billing Account User`.
* **Fluxo de Solicitação:** Desenvolvedores não podem mais vincular projetos à conta pagadora diretamente. Novos projetos devem ser solicitados via canal do slack #suporte-plataforma.

### 3.2. Políticas de Organização (Org Policies)

* **Project Creator:** Remoção da permissão de criação de projetos para usuários comuns no nível da organização.
* **Labels Obrigatórios:** Implementação de política para que nenhum recurso (Cloud SQL, VM) seja criado sem as tags:
  * `bu`: Identificação da unidade de negócio.
  * `env`: Identificação do ambiente (prod, dev, staging).
  * `product`: Centro de custo para faturamento.


---

## 4. Auditoria e Revisão de Projetos Atuais

Iniciaremos uma força-tarefa para classificar o inventário atual:


1. **Mapeamento:** Identificar todos os projetos vinculados à conta Seazone (conta pagadora).
2. **Migração:** Mover projetos existentes para suas respectivas Pastas de BU.
3. **Descomissionamento:** Projetos sem dono ou sem uso identificado serão desligados após 7 dias de aviso prévio.


---

## 5. Plano de Redução de Custos (Foco: Cloud SQL)

O Cloud SQL é hoje o nosso maior ofensor financeiro. As ações imediatas são:

| **Ação** | **Descrição** | **Potencial de Economia** |
|----|----|----|
| **Downgrade Enterprise Plus** | Mudar instâncias de `Enterprise Plus` para `Enterprise` em ambientes não críticos. | \~30% a 50% |
| **Right-sizing (RAM/CPU)** | Redimensionar máquinas subutilizadas com base nas métricas do Cloud Monitoring. | Variável |
| **Zonal vs Regional** | Converter instâncias de bancos de desenvolvimento de "Regional" para "Zonal". | \~50% no custo da instância |
| **Committed Use (CUDs)** | Após o right-sizing, contratar uso comprometido de 1 ano para bases estáveis. | \~25% a 40% |


---

## 6. Monitoramento de Longo Prazo

* **Exportação para BigQuery:** Ativação do faturamento detalhado para análise granular (por hora)?.
* **Dashboards no Looker Studio:** Criação de visão executiva para os gestores de cada BU acompanharem seus gastos mensais (se puder agregar com a AWS, pode ser um portal unico de gastos).
* **Alertas de Orçamento:** Configuração de notificações automáticas em 50%, 80% e 100% do orçamento previsto por pasta.


# 7. Padrão de Nomenclatura de Projetos

Todos os **novos projetos** devem obrigatoriamente seguir o padrão de nomenclatura definido abaixo. Esse padrão tem como objetivo garantir padronização, facilitar a organização, a identificação dos projetos e a gestão dos ambientes.

## Estrutura do *Project ID*

O formato padrão é:

`sz-[bu]-[item](-[env])`

### Componentes

* **sz**\nPrefixo fixo que identifica a organização **Seazone**.
* **bu** (*Business Unit*)\nUnidade de negócio à qual o projeto pertence.\nExemplos: `shared`, `dados`, `hospedagem`.
* **propósito**\nNome curto e descritivo do sistema, serviço ou produto.\nExemplos: `core`, `app`, `lake`, `booking`, `site`.
* **env** (*opcional*)\nAmbiente do projeto.\nDeve ser informado **obrigatoriamente** quando o projeto **não** for de produção.\nExemplo de valores permitidos:
  * `dev` — Desenvolvimento
  * `stg` — Staging

> ⚠️ Projetos de produção **não** precisam incluir o sufixo de ambiente.

## Exemplos Válidos

* `sz-dados-booking`\nProjeto de dados relacionado ao Booking (produção).
* `sz-hospedagem-site`\nProjeto do site da unidade de hospedagem (produção).
* `sz-hospedagem-site-dev`\nProjeto do site da unidade de hospedagem em ambiente de desenvolvimento.