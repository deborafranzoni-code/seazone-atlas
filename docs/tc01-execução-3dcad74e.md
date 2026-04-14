<!-- title: TC01 - Execução | url: https://outline.seazone.com.br/doc/tc01-execucao-wL3G6Ax0li | area: Tecnologia -->

# TC01 - Execução

## Contexto

==(SE APLICA APENAS A N8N-DEV)==

O ambiente `dev-n8n` no cluster GKE `cluster-tools-prod-gke` é um ambiente novo que ainda não possui VolumeSnapshot configurado. O backup atual é apenas em nível de aplicação via CronJob que exporta credentials e workflows em JSON para o GCS (`gs://szn-n8n-dev-backup/`).

O objetivo é executar um teste completo de DR que:


1. Configure e valide VolumeSnapshot (PVC nativo K8s) do Postgres
2. Valide o backup existente no GCS como fallback
3. Simule um desastre (delete do PVC)
4. Restaure o ambiente e registre tempos e comportamentos

**Componentes com estado:**

* `data-n8n-postgres-0` — 20Gi, `standard-rwo`, PV com reclaim policy `Delete` ⚠️
* `n8n-redis` — 5Gi, `standard-rwo` (cache, sem estado crítico)


---

## Fase 0  Pré-requisitos e Validação Inicial

**Objetivo:** Garantir que temos backups válidos antes de qualquer ação destrutiva.

### 0.1 — Verificar último backup GCS

1 - Listar backups disponíveis ![](/api/attachments.redirect?id=ccef8450-4f83-4e1b-87ed-a5306b9db740 " =733x473")

2 - Confirmar integridade do último backup (deve ter conteúdo não-vazio)

 ![](/api/attachments.redirect?id=6ff6648b-b4e9-4a08-b424-b01a456b5e99 " =1040x238")

Não há backup de hoje, forcei a criação.

 ![](/api/attachments.redirect?id=f5ec23a4-2ec8-44ed-8d28-fe4d512550bc " =1040x238")



---

## Fase 1 — Configurar VolumeSnapshot

**Objetivo:** Configurar o mecanismo de snapshot nativo do K8s (ainda não existe no cluster).

### 1.1 — Instalar VolumeSnapshotClass para GKE CSI

crd já existe 

 ![](/api/attachments.redirect?id=92ec9ec5-de15-4956-ad0d-24bd853e060f " =1040x238")

### 1.2 — Tirar snapshot do PVC do Postgres

Snapshot tirada

 ![](/api/attachments.redirect?id=b196347d-88d1-4068-8278-f8e8a80cec73 " =1040x356")

### Snapshot confirmada

 ![](/api/attachments.redirect?id=02abec83-e822-4741-93dd-1e87140519d5 " =959x815")


---

## Fase 2 — Proteger o PV e Parar a Aplicação

**Objetivo:** Evitar perda de dados acidental e garantir estado consistente antes do delete.

### 2.1 — Alterar reclaim policy do PV para Retain 

 ![](/api/attachments.redirect?id=44fa4756-4fa9-4ec2-857c-f4a734715c22 " =950x209")

### Politica do pv alterada para reter

 ![](/api/attachments.redirect?id=bc5ae1db-399c-4f68-9926-b98b57e59429 " =953x118")

  ![](/api/attachments.redirect?id=43a5c228-6255-49ce-b8b7-1f2abb37a1dc " =953x118")

### 2.2 — Anotar estado da aplicação antes do desastre

### Anotação de número de workflows e credentials ativos

 ![](/api/attachments.redirect?id=eecd409d-1b6f-4d00-a33e-cfc0a7aee350 " =950x229")

### 2.3 — Parar a aplicação (scale down)


1. Parar todos os componentes que usam o banco
2. ![](/api/attachments.redirect?id=8936f85c-4461-44ed-bb06-54efe6ad02d3 " =938x425")
3. Aguardar todos os pods pararem
4. Parar o Postgres por último
5. Anotar comportamento da aplicação durante downtime

   ![](/api/attachments.redirect?id=53caa962-eb54-424f-a080-44b5837ef5b8 " =946x564")


---

## Fase 3 — Simular o Desastre (Delete do PVC)

**Objetivo:** Deletar o PVC e observar o estado do cluster.

### 3.1 — Deletar o PVC

Hora do delete

 ![](/api/attachments.redirect?id=1c0c1305-72ca-4cf8-9caf-5c5ba01dbad8 " =946x145")

* PVC apagado PV permaneceu 

 ![](/api/attachments.redirect?id=d9c9db9d-063d-4996-bf85-f20f87bf3455 " =953x300")

### 3.2 — Verificar estado do cluster após delete

Estado do cluster pós delete 

 ![](/api/attachments.redirect?id=b2fcacf4-8e50-4171-9d85-3dc87e583e21 " =948x142")

 ![](/api/attachments.redirect?id=1b3de0c7-cf1c-46e4-bda0-ccf17ea4c74d " =928x492")Estado dos pods, volume pv


---

## Fase 4 — Restaurar a partir do VolumeSnapshot

**Objetivo:** Recriar o PVC a partir do snapshot tirado na Fase 1.

### 4.1 — Criar novo PVC a partir do snapshot

Restartando a PVC 

 ![](/api/attachments.redirect?id=5116c6ad-d605-4e4c-afe5-c5375701d5b6 " =908x630")

PVC reiniciado, volume do psql elevado a 1 escalado

 ![](/api/attachments.redirect?id=b19b59a0-ee19-4c47-896d-5be441363a64 " =908x181")


---

Dados recuperados 

 ![](/api/attachments.redirect?id=9a4383a7-4a9f-4fa8-8cdb-588a1a7a011b " =951x442")


## Fase 5 — Reativar a Aplicação

**Objetivo:** Subir o Postgres e verificar que os dados foram restaurados, depois subir tudo.


### 5.2 — Subir todos oscomponentes

 ![](/api/attachments.redirect?id=d23b4ef7-d351-4fb9-8642-f36c63682147 " =951x442")

### 5.3 — Validar aplicação em produção dev

Aplicação respondendo, workflows normalizados  ![](/api/attachments.redirect?id=4e2244e8-4e28-43ef-8439-984467c77d95 " =954x283")

✅ Critério: HTTP 200, UI acessível, workflows listados corretamente


---


---

## Resumo de Tempos Esperados

| Fase | Atividade |
|----|----|
| 0 | Validar backup GCS |
| 1 | Configurar + tirar snapshot |
| 2 | Proteger PV + parar app |
| 3 | Deletar PVC + observar |
| 4 | Restaurar PVC do snapshot |
| 5 | Subir app + validar dados |