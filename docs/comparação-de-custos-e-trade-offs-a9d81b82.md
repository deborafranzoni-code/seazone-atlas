<!-- title: Comparação de Custos e Trade-offs | url: https://outline.seazone.com.br/doc/comparacao-de-custos-e-trade-offs-HehZtgZyD1 | area: Tecnologia -->

# Comparação de Custos e Trade-offs

## Custos mensais (us-central1)

### HashiCorp Vault (atual)

| Recurso | Tipo | Custo/mês |
|----|----|----|
| GCE VM `vault` | e2-medium (2 vCPU, 4 GB RAM) | \~$33,47 |
| Disco persistente | 10 GB standard PD | \~$0,40 |
| IP externo estático | Em uso | $0,00 |
| **Total** |    | **\~$33,87/mês (\~$406/ano)** |

### Passbolt CE (novo)

| Recurso | Tipo | Custo/mês |
|----|----|----|
| GKE | Usa node pool existente | $0,00 |
| Cloud SQL Postgres | Instância `tools` já existia (n8n, Outline, Kestra) | $0,00 incremental |
| AWS SES | Convites/notificações internas | \~$0,00 |
| SSM Advanced tier | 4 parâmetros × $0,05 | \~$0,20 |
| GCS backup | \~2 MB/mês | <$0,01 |
| **Total** |    | **\~$0,20/mês (\~$2,40/ano)** |

**Economia potencial ao descomissionar o Vault: \~$33,67/mês (\~$404/ano)**


---

## Trade-offs

### Vault — pontos fortes

* API-first, integrações nativas
* Audit log nativo
* Multi-backend: AWS, GCP, LDAP, bancos de dados, etc.

### Vault — pontos fracos

* Custo de \~$34/mês em VM dedicada, sem HA (single point of failure)
* UX ruim para uso humano — sem extensão de browser, sem app mobile
* Manutenção de SO e patches na VM

### Passbolt CE — pontos fortes

* Custo incremental zero (usa infra existente)
* UX excelente para uso humano: extensão Chrome/Firefox.
* GPG end-to-end: o servidor nunca vê as senhas em texto claro
* Backup diário automatizado no GCS, chaves no SSM — sem PVCs

### Passbolt CE — pontos fracos

* Extensão de browser obrigatória para todos os usuários
* SSO (LDAP/SAML) só no plano Pro (\~$49/mês para até 10 usuários)