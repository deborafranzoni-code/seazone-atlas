<!-- title: Casos de Teste | url: https://outline.seazone.com.br/doc/casos-de-teste-h1QkAvnpFD | area: Tecnologia -->

# Casos de Teste

## Matriz de Casos de Teste DR

Abaixo estão todos os cenários de desastre relevantes para o ambiente `n8n-dev`. O teste executado neste relatório cobre o **TC-01**.

| ID | Cenário | Componente | Criticidade | Status |
|----|----|----|----|----|
| TC-01 | ==Perda do PVC do Postgres(SE APLICA APENAS A N8N-DEV)== | `n8n-postgres` | Alta | ✅ Executado |
| TC-02 | Restauração via backup GCS (sem snapshot) | GCS / `n8n-postgres` | Alta | ✅ Executado |
| TC-03 | Falha de nó (node failure) | GKE node pool | Alta | ✅ Executado |
| TC-04 | Corrupção de Secret / ConfigMap | `n8n-editor`, `n8n-postgres` | Alta | ✅ Executado |
| TC-05 | Falha do Redis | `n8n-redis` | Média | ✅ Executado |
| TC-06 | Deploy com imagem inválida (rollback) | Todos deployments | Média | ✅ Executado |


---

### TC-01 - Perda do PVC do Postgres ==(SE APLICA APENAS A N8N-DEV)==

### ✅ Executado

**Cenário:** PVC do Postgres deletado acidentalmente. **Método de restauração:** VolumeSnapshot (`csi-gce-pd-vsc`) 

**Resultado:** Dados 100% íntegros. Retorno em \~22 min, Zero perca. 

Detalhes:  @[TC01 -Relatório — n8n-dev](mention://83a722d3-a748-47b6-b017-8cc50c2f3053/document/cc850b5a-45ab-4d65-9943-c7d081ba6ab1)

Execução: @[TC01 - Execução — n8n-dev](mention://e7458e7f-f6d9-4872-8d54-0d694137437a/document/3dcad74e-1aa1-4d12-ab62-07a8da9559dc)


---

### TC-02 -  Restauração via Backup GCS (sem snapshot)

✅ Executado

**Cenário:** PVC perdido e nenhum VolumeSnapshot disponível. Fallback para o backup JSON no GCS. **Objetivo:** Validar que workflows e credentials podem ser reimportados via CLI do n8n a partir dos arquivos `gs://szn-n8n-dev-backup/`.

**Passos a seguir:**

```bash
1. Subir Postgres zerado (sem dados)
2. Baixar backup mais recente do GCS
3. Importar via n8n CLI
```

Detalhes: @[TC02 - Relatório Restauração via Backup GCS](mention://eab75779-3812-4900-a3f5-08437ebb2359/document/2f6eb201-f95e-47f8-9662-05329deea9b5)

### TC-03 -  Falha de Nó (Node Failure)

✅ Executado

**Cenário:** Nó onde o `n8n-postgres-0` está rodando é drenado ou removido do cluster. **Objetivo:** Validar que o StatefulSet reagenda o pod em outro nó e monta o PVC corretamente.

**Passos sugeridos:**

```bash
Identificar nó atual
Drenar o nó (simular falha)
Observar reagendamento
Restaurar o nó após o teste
```

**Critério de sucesso:** pod reagendado em outro nó, dados íntegros. 

`standard-rwo` é zonal, o novo nó precisa estar na mesma zona do PV.

Detalhes: @[TC03 - Relatório - Node Failure](mention://f7088387-5b67-415b-9541-88b7ee2beeaa/document/0f3b751e-aa33-4fa7-8271-8cfca4ff2c32)


---

### TC-04 -  Corrupção de Secret / ConfigMap

✅ Executado

**Cenário:** Secret com credenciais do Postgres ou encryption key do n8n é deletado ou corrompido. **Objetivo:** Validar que há backup dos Secrets e procedimento de restauração documentado.

**Passos sugeridos:**

```bash
Fazer backup antes
Simular corrupção
Observar comportamento (pods devem entrar em erro)
Restaurar
```

Se a encryption key do n8n for perdida, credentials armazenadas no banco ficam ilegíveis mesmo com dados íntegros. 

Detalhes: @[TC-04 - Relatório - Corrupção de Secret](mention://3f8885f3-c070-458c-a87d-8a4da584ecba/document/df6aae97-43c5-4115-b427-8f24e9deb35b)


---

### TC-05 — Falha do Redis

✅ Executado

**Cenário:** Pod `n8n-redis` é deletado ou PVC do Redis é perdido. **Objetivo:** Confirmar que a perda do Redis não causa perda de dados críticos — apenas impacto em filas/cache.

**Passos sugeridos:**

```bash
Deletar pod
Observar: workflows em execução devem ser reprocessados ou perdidos
Observar: n8n-workers deve se reconectar automaticamente
```

**Critério de sucesso:** Redis reinicia limpo, workers reconectam, sem impacto em workflows persistidos. 

[Detalhes:  ](https://outline.seazone.com.br/doc/tc05-relatorio-falha-do-redis-dkgwBw0Qp1)@[TC05 - Relatório Falha do Redis](mention://84f4a4ac-d4f7-4d04-a0a2-d2d06217092f/document/ff0112a7-1dc2-4830-902c-ed00b38faf05)


---

### TC-07 — Deploy com Imagem Inválida (Rollback)

✅ Executado

**Cenário:** Deploy acidental com imagem inexistente ou com bug crítico. **Objetivo:** Validar procedimento de rollback rápido.

**Passos sugeridos:**

```bash
Simular deploy ruim
Observar ImagePullBackOff
Rollback
```

**Critério de sucesso:** rollback concluído , HTTP 200 restaurado. 

[Detalhes: ](https://outline.seazone.com.br/doc/tc05-relatorio-falha-do-redis-dkgwBw0Qp1) @[TC06 - Relatório - Deploy com Imagem Inválida (Rollback)](mention://4c4def1e-002e-42fc-9b76-72db8a94f898/document/c3953a02-6cb3-4cc1-a3cb-be2fbbb0543d)


---