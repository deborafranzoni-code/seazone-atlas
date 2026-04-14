<!-- title: Checklist de Engenharia | url: https://outline.seazone.com.br/doc/checklist-de-engenharia-1tKQGV8b0o | area: Tecnologia -->

# ✅ Checklist de Engenharia

:hourglass_flowing_sand: **Status:** ongoing


---

## Front-End

### Geral

- [ ] A feature é paralelizável?


- [ ] A feature altera algum fluxo já existente?

  
:::info
  *Se sim, é legal verificar se esses fluxos serão impactados pelas alterações.*

  :::

### PostHog

- [ ] Precisa de feature flags?
- [ ] Precisa de rollout parcial?
- [ ] Precisa capturar eventos?

### **Conteúdo estático**

- [ ] Possui conteúdo estático (imagens, vídeos, etc.)?
- [ ] O conteúdo precisa de controle externo (via PostHog, S3 ou outro)?

### Monitoramento

- [ ] Precisa de error tracking (Sentry/PostHog)?