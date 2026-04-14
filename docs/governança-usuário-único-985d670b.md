<!-- title: Governança — Usuário Único | url: https://outline.seazone.com.br/doc/governanca-usuario-unico-idsix9IYrQ | area: Tecnologia -->

# Governança — Usuário Único

---

## O que temos disponível no OSS

| Feature | Disponível | Função |
|----|----|----|
| ==Namespaces hierárquicos== | ✅ | Organização lógica de flows |
| ==Labels== | ✅ | Filtragem e agrupamento de flows/execuções |
| ==Namespace Files== | ✅ | Scripts e configs reutilizáveis por namespace |
| ==Revisions de flows== | ✅ | Histórico automático + rollback |
| ==Subflows== | ✅ | Reutilização de flows |
| ==Error Handling / Retry== | ✅ | Resiliência nas execuções |
| ==RBAC== | ❌ | Enterprise only |
| ==Audit Logs== | ❌ | Enterprise only |
| ==Custom Blueprints== | ❌ | Enterprise only |
| ==Service Accounts / API Tokens== | ❌ | Enterprise only |


---

## 1. Namespaces — Estrutura de Organização

Namespaces são a principal ferramenta de governança disponível no OSS. Funcionam como pastas lógicas com hierarquia ilimitada usando `.` como separador.

### Estrutura recomendada pelo Kestra

```
empresa
├── empresa.hosting
│   ├── empresa.hosting.review-reminder
│   └── empresa.hosting.pre-check-in
├── empresa.reservas
│   ├── empresa.reservas.overbooking
│   └── empresa.reservas.properties-ranking
└── empresa.revops
    └── empresa.revops.leads
```

### Regras importantes

* Uma vez que um flow é salvo em um namespace, **não é possível trocar**, precisa criar um novo flow
* No OSS, todos os namespaces são visíveis pelo usuário único, não há isolamento entre eles


---

## 2. Labels 

Labels são pares chave-valor que funcionam como tags nos flows e execuções. São a principal forma de **filtrar e agrupar** no UI do Kestra OSS.

### Labels úteis 

| Label | Valores exemplo | Para quê |
|----|----|----|
| `team` | hosting, reservas, revops | Separa por área mesmo sem RBAC |
| `environment` | production, staging | Identifica contexto da execução |
| `project` | ranking-conversion, overbooking | Agrupa workflows relacionados |
| `status` | active, deprecated, testing | Ciclo de vida do workflow |
| `owner` | nome ou time responsável | Responsabilidade |


---

## 3. Key-Value Store (KV) — Estado Compartilhado

O KV Store permite compartilhar dados entre execuções diferentes dentro do mesmo namespace. Disponível no OSS desde a versão 0.18.

### Casos de uso

* Armazenar configuração que muda com frequência (sem precisar editar o YAML)
* Compartilhar resultados entre flows
* Manter estado entre execuções (ex: última data processada)

### Propriedades do KV Store

| Propriedade | Detalhes |
|----|----|
| Tipos suportados | string, number, boolean, datetime, date, duration, JSON |
| TTL | Opcional. Formato ISO 8601 (ex: `P7D` = 7 dias) |
| Acesso cross-namespace | Possível entre namespaces permitidos |


---

## 4. Namespace Files — Scripts e Configs Reutilizáveis

Namespace Files permite armazenar arquivos (scripts Python, queries SQL, configs) por namespace e reutilizá-los em qualquer flow daquele namespace.

### Vantagens

* Scripts não ficam inlined no YAML do flow (mais limpo e manutenível)
* Compartilha código entre flows do mesmo namespace sem duplicar


---

## 5. Naming Conventions — Consistência

Convenção de nomes recomendada pelo Kestra para manter tudo organizado:

### Namespaces

```
empresa.time.projeto
```

### Flow IDs

Usar `snake_case` ou `camelCase` 

### Task IDs dentro do flow

Sejam descritivos e curtos:

```yaml
tasks:
  - id: fetch_posthog_views
  - id: fetch_metabase_reservations
  - id: calculate_ranking
  - id: upload_to_s3
```


---

## 6. Governança via Git (substituto para Audit Logs)

Como Audit Logs são Enterprise only, o Git serve como trilha de auditoria no OSS:

* Cada mudança nos YAMLs dos flows passa por **commit + PR** no repositório
* O histórico do Git registra **quem mudou, o que mudou e quando**
* Combinado com **Revisions** (built-in no Kestra), temos duas camadas de histórico

Referência completa: [versionamento-e-backup.md](https://outline.seazone.com.br/doc/versionamento-e-backup-de-workflows-no-kestra-oss-hfENzjMwOS)


---

## Fontes

* [Namespaces](https://kestra.io/docs/workflow-components/namespace)
* [Labels](https://kestra.io/docs/workflow-components/labels)
* [KV Store](https://kestra.io/docs/concepts/kv-store)
* [Naming Conventions](https://kestra.io/docs/best-practices/naming-conventions)
* [Business Unit Separation](https://kestra.io/docs/best-practices/business-unit-separation)
* [OSS vs Enterprise](https://kestra.io/docs/oss-vs-paid)
* [Kestra 0.18 — KV Store no OSS](https://kestra.io/blogs/2024-08-06-release-0-18)