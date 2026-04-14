<!-- title: Deploy vibe coding: governança sem bloqueio Lovable | url: https://outline.seazone.com.br/doc/deploy-vibe-coding-governanca-sem-bloqueio-lovable-9QaM66pqbK | area: Tecnologia -->

# Deploy vibe coding: governança sem bloqueio Lovable

# Deploy seguro para vibe coding: governança sem fricção com Lovable

**O Lovable permite que times não-técnicos gerem apps React completos via IA, mas o deploy sem controle gera riscos reais — 45% do código gerado por IA introduz vulnerabilidades OWASP Top 10.** A solução não é bloquear, mas criar "golden paths" que tornam o caminho seguro o mais fácil. Este relatório detalha como estruturar um pipeline governado sobre AWS + GitHub Actions + Supabase, desde as capacidades reais do Lovable até exemplos concretos de GitHub Actions YAML, comparativos de plataformas de deploy e modelos de governança por tiers.

A abordagem recomendada combina três pilares: **o Lovable exporta código para GitHub** (ponte obrigatória para governança), **pipelines de segurança não-bloqueantes** escaneiam e notificam sem parar o deploy, e **um modelo de tiers** (sandbox → interno → produção) define qual nível de revisão cada app exige. Para plataforma de deploy, a estratégia híbrida — AWS Amplify para produção e Coolify/Dokploy em EC2 para ferramentas internas — maximiza segurança e eficiência de custo.


---

## Parte 1: Como o Lovable funciona por dentro

### Workspaces são a fronteira organizacional

O Lovable organiza tudo em **workspaces**, que funcionam como o equivalente a uma organização. Cada workspace compartilha um pool de créditos, e os projetos dentro dele herdam o plano contratado. Usuários podem ser convidados para o workspace inteiro ou para projetos específicos, com três papéis — **Owner, Admin e Editor**. Editors só editam projetos; Admins e Owners gerenciam integrações, conectores e membros.

Nos planos Business e Enterprise, admins controlam **conectores compartilhados** (habilitar/desabilitar por conector), **conectores pessoais MCP** (por servidor), configurações de privacidade e **controles de publicação** (publish interno vs externo). Existe também o recurso **Workspace Knowledge**, onde líderes técnicos definem instruções persistentes — padrões de código, requisitos de testes, bibliotecas preferidas, guardrails arquiteturais — que o Lovable aplica automaticamente a todos os projetos do workspace.

**Limitação importante: não existe hierarquia de workspaces nem sub-organizações.** Para separar por time ou domínio, é necessário criar workspaces separados, cada um com seu próprio plano e billing. O modelo de precificação é por workspace (não por usuário), com créditos compartilhados entre todos os membros.

### Integração com GitHub: sincronização bidirecional robusta

A integração com GitHub é o pilar central para qualquer estratégia de governança. O Lovable oferece **sync bidirecional**: edições no Lovable geram commits automáticos no GitHub, e commits pushados para a branch principal no GitHub refletem no Lovable em segundos. Apenas admins e owners do workspace podem gerenciar a integração GitHub.

**Detalhes críticos para SRE:**

* O Lovable **cria o repositório GitHub** durante a conexão — não é possível linkar a um repo existente (sem BYOR — "Bring Your Own Repository")
* A Lovable GitHub App pode ser instalada em contas pessoais ou **organizações GitHub**, com escopo configurável (todos repos ou repos selecionados)
* Cada projeto Lovable tem **um único repositório GitHub vinculado**
* Renomear, mover ou deletar o repositório GitHub **quebra permanentemente** o sync
* Branch switching está disponível como recurso experimental em Settings → Labs
* Uma vez no GitHub, o código pode ser deployado para **qualquer plataforma** (Vercel, Netlify, Amplify, Coolify, etc.) via CI/CD padrão

### Supabase: integração nativa profunda com riscos de governança

O Lovable tem a integração mais profunda com Supabase entre todas as ferramentas de vibe coding. Via OAuth, o usuário seleciona qual organização e projeto Supabase conectar. O Lovable então gera automaticamente tabelas, schemas, fluxos de autenticação, Edge Functions e políticas Row Level Security (RLS) a partir de prompts em linguagem natural.

**Para governança**, cada projeto Lovable se conecta a **um único projeto Supabase**, selecionado durante o setup. Porém, **não existe mecanismo nativo para restringir quais projetos Supabase podem ser conectados** — um usuário pode conectar um projeto Supabase pessoal em vez do corporativo. Isso exige validação no pipeline CI/CD (detalhado na Parte 3).

O Lovable também lançou o **Lovable Cloud** como alternativa ao Supabase, oferecendo backend integrado (auth, database, storage) sem necessidade de conta Supabase separada.

### API, CLI e webhooks: lacunas significativas

O Lovable **não possui webhooks ou eventos nativos** que disparam quando um projeto é publicado. A única API pública é o **"Build with URL"** — permite gerar apps programaticamente via URL, útil para automação básica mas não para governança de deploy. **Não existe CLI oficial.**

**Workaround essencial:** Como o Lovable faz push para GitHub a cada alteração, é possível usar **GitHub webhooks e GitHub Actions** como sistema de eventos. Toda mudança no Lovable vira um commit no GitHub, que pode disparar pipelines, notificações e validações. **O GitHub é o ponto de controle obrigatório** para qualquer estratégia de governança.

### MCP nativo e controles enterprise

Desde novembro de 2025, o Lovable suporta nativamente o **Model Context Protocol (MCP)** como "Personal connectors". Admins podem conectar MCPs pré-configurados (Jira, Confluence, Notion, Linear, n8n, Amplitude, entre outros) ou **servidores MCP customizados** com endpoints internos. Nos planos Business e Enterprise, admins controlam quais MCPs estão habilitados para todo o workspace via configurações de privacidade.

**Features enterprise confirmadas:**

* **SSO/SAML** (OIDC e SAML 2.0) com Okta, Auth0, Microsoft Entra ID — disponível nos planos Business e Enterprise
* **SCIM provisioning** para gestão automatizada de usuários (Enterprise)
* **Audit logs** (Enterprise)
* **RBAC** com permissões separadas para visualizar, editar, aprovar e publicar
* **SOC 2 Type II**, **ISO 27001:2022** e **GDPR**
* **Data residency** com hosting regional (EU, US, Austrália)
* Opt-out de training: dados e código **não são usados para treinar modelos** nos planos Business/Enterprise

| Plano | Preço | Créditos | Destaques |
|----|----|----|----|
| Free | $0/mês | 5/dia (30/mês) | Projetos públicos, sync GitHub, deploy básico |
| Pro | $25/mês | 100/mês + 5/dia | Projetos privados, domínios custom, roles |
| Business | $50/mês | 100/mês+ | SSO, publish interno, workspace de equipe |
| Enterprise | Custom | Custom | SCIM, audit logs, design systems, suporte dedicado |


---

## Parte 2: Onde fazer deploy — o comparativo que importa

### Quatro plataformas, dois paradigmas

Para frontends React/Next.js gerados pelo Lovable, existem dois paradigmas: **plataformas gerenciadas** (Vercel, AWS Amplify) e **PaaS self-hosted** (Coolify, Dokploy) rodando em EC2 dentro da sua AWS.

| Critério | Vercel | AWS Amplify | Coolify | Dokploy |
|----|----|----|----|----|
| **Custo** | $20/user/mês (Pro) | Pay-as-you-go (\~$1-66/mês) | Gratuito + custo EC2 | Gratuito + custo EC2 |
| **Vendor lock-in** | Alto | Moderado (AWS) | Mínimo | Mínimo |
| **GitHub Actions** | CLI nativa + Actions | App + CLI headless | Webhook API + Actions | Action oficial + Webhook |
| **RBAC** | ★★★★★ (Enterprise) | ★★★★★ (IAM) | ★★☆☆☆ | ★★★☆☆ |
| **Audit logs** | Enterprise only | CloudTrail (completo) | Não implementado | Enterprise/Cloud |
| **Dados na AWS** | Não | ★★★★★ Nativo | ★★★★★ (EC2/VPC) | ★★★★★ (EC2/VPC) |
| **Next.js** | ★★★★★ (criador) | ★★★★☆ | ★★★☆☆ (Docker) | ★★★☆☆ (Docker) |
| **CDN** | Edge global | CloudFront | Manual | Manual |
| **SSO** | Pro (self-serve) | IAM Identity Center | Externo apenas | Built-in (better-auth) |

**Vercel** é imbatível em DX para Next.js mas cria dependência forte de vendor, e o salto de preço Pro → Enterprise ($20K+/ano) é significativo. **AWS Amplify** é a escolha natural para empresas AWS-first: dados ficam na AWS, integra com IAM, CloudTrail e CloudWatch nativamente, e o custo é previsível com pay-as-you-go. **Coolify** (Apache 2.0, open source verdadeiro) e **Dokploy** (source-available com restrições comerciais) rodam em Docker na sua infraestrutura, com custo previsível igual ao custo do EC2.

### Amplify vs self-hosted para dados na AWS

Para **apps de produção voltados a clientes**, o **AWS Amplify é mais vantajoso**: zero overhead operacional, CI/CD gerenciado, CloudFront como CDN, CloudTrail para auditoria completa, e cobertura de compliance (SOC 2, HIPAA, PCI DSS) herdada da AWS. Limitações incluem ausência de on-demand ISR e limite de 220 MB no output de build SSR.

Para **ferramentas internas e protótipos vibe-coded**, **Coolify ou Dokploy em EC2 são mais eficientes**: um t3.xlarge (\~$120/mês) pode hospedar dezenas de apps simultaneamente, sem cobrança por deploy, bandwidth ou seat. Ambos usam **Traefik** como reverse proxy com SSL automático via Let's Encrypt e suportam domínios customizados e internos (ideais para `*.tools.empresa.internal`).

### Deploy automático via GitHub webhooks

**Coolify** oferece três métodos: GitHub App (recomendado, com auto-deploy on push e preview deployments em PRs), Deploy Webhooks (URL única por recurso, chamável via `curl` com Bearer token), e integração direta com GitHub Actions (build Docker → push para GHCR → trigger deploy via webhook).

**Dokploy** oferece mecanismo similar: toggle "Auto Deploy" que gera webhook URL para adicionar ao GitHub, Action oficial (`dokploy/dokploy-action@v1`), e API REST completa (`POST /api/application.deploy` com x-api-key). Suporta keywords de skip (`[skip ci]`, `[no deploy]`) e watchPaths para deploy seletivo.

### A estratégia híbrida recomendada

A configuração ideal combina ambos paradigmas:

* **AWS Amplify** para apps de produção customer-facing (compliance, CDN, auditoria via CloudTrail)
* **Dokploy em EC2** para ferramentas internas e protótipos (custo fixo, controle total, domínios internos)
* **GitHub Actions** como CI/CD unificado, triggerando deploys em ambas plataformas
* **CloudFront** na frente do Dokploy se CDN/WAF for necessário para apps internos expostos

Dokploy leva vantagem sobre Coolify para este contexto enterprise por ter SSO built-in, RBAC mais granular na versão Enterprise, Docker Swarm nativo para multi-node, e melhor estabilidade reportada em produção.


---

## Parte 3: Pipeline de segurança que não bloqueia (mas protege)

### Por que código vibe-coded precisa de scanning rigoroso

Dados recentes são alarmantes: o Veracode 2025 GenAI Code Security Report testou 100+ LLMs em 80 tarefas de coding e encontrou que **45% do código gerado por IA introduz vulnerabilidades OWASP Top 10**, com **2.74x mais vulnerabilidades** que código humano. JavaScript tem taxa de falha de 38-45%, com **86% de falha** em defesas contra XSS e **88% de falha** contra Log Injection. A Apiiro encontrou em empresas Fortune 50 um aumento de **322% em caminhos de escalação de privilégio** e **40% mais secrets expostos** em código AI.

Riscos específicos para projetos Lovable/React/Supabase incluem: chaves Supabase hardcoded no fonte (especialmente `SUPABASE_SERVICE_ROLE_KEY`), uso de `dangerouslySetInnerHTML` sem sanitização, dependências com CVEs conhecidos, pacotes "alucinados" (slopsquatting), e fluxos de auth simplificados sem rate limiting ou validação adequada.

### Stack de ferramentas recomendado

| Camada | Ferramenta | Propósito | Blocking? |
|----|----|----|----|
| Dependências | **Trivy** (pinado por SHA!) | CVEs em pacotes npm | Não → Sim (fase 3) |
| SAST | **Semgrep** | Vulnerabilidades no código | Não → Sim (fase 3) |
| Secrets | **Gitleaks** | API keys, tokens hardcoded | Não → Sim (fase 3) |
| Qualidade | **SonarCloud** | Bugs, code smells, hotspots | Não → Sim (fase 4) |
| Supabase | **Script customizado** | Validar projeto aprovado | Alerta apenas |
| Notificação | **Slack** | Alertas em tempo real | N/A |

**Alerta crítico sobre Trivy (março 2026):** O `aquasecurity/trivy-action` sofreu um ataque de supply chain onde atacantes fizeram force-push em 75 de 76 tags de versão, injetando malware que exfiltrava secrets de CI/CD. **Sempre pine GitHub Actions por commit SHA completo**, nunca por tag de versão. Isso vale para todas as actions de terceiros.

### Rulesets Semgrep essenciais para React/Next.js vibe-coded

O Semgrep deve ser configurado com os seguintes rulesets: `p/react` (XSS via `dangerouslySetInnerHTML`, métodos não sanitizados), `p/nextjs` (issues específicos de Next.js), `p/javascript` e `p/typescript` (eval, prototype pollution), `p/owasp-top-ten` (padrões OWASP), e `p/secrets` (hardcoded secrets e tokens). Para detecção de secrets, **Gitleaks** é recomendado por ser o mais rápido, ter output SARIF nativo (integra direto com GitHub Security tab), e melhor suporte a pre-commit hooks. Para scans profundos periódicos, TruffleHog complementa com verificação de credenciais ativas.

### Validação do projeto Supabase no CI/CD

Para garantir que código vibe-coded conecta ao Supabase corporativo (e não a um projeto pessoal), duas abordagens são recomendadas:

**Abordagem 1 — Validação por URL pattern:** Manter uma lista de project refs aprovados como GitHub Secret (`APPROVED_SUPABASE_REFS`) e verificar se o `NEXT_PUBLIC_SUPABASE_URL` no código contém apenas refs dessa lista.

**Abordagem 2 — Validação via Supabase Management API:** Usar `GET /v1/projects` com um `SUPABASE_ACCESS_TOKEN` corporativo para verificar se o project ref encontrado no código pertence à organização Supabase da empresa. Isso é mais robusto pois valida ownership, não apenas um ID estático.

Adicionalmente, o pipeline deve detectar URLs Supabase hardcoded diretamente no código (em vez de `process.env`) e alertar para uso de environment variables.

### Pipeline completo non-blocking em GitHub Actions

O padrão arquitetural é: **todos os checks de segurança rodam em paralelo, o deploy roda independentemente (sem** `**needs**` **nos checks), e um job de notificação agrega resultados e envia para Slack.** Os mecanismos-chave são:

* `continue-on-error: true` em steps e jobs de segurança
* `exit-code: 0` nos parâmetros de Trivy e Semgrep (retornam sucesso mesmo com findings)
* `needs: []` vazio no job de deploy (roda em paralelo, não depende dos checks)
* `if: always()` no job de notificação (garante que alertas disparam independentemente do resultado)
* Upload SARIF para o GitHub Security Dashboard em todos os scans (visibilidade centralizada)

```yaml
# Estrutura simplificada do pipeline

jobs:
  trivy-scan:        # Roda em paralelo
    continue-on-error: true
  semgrep-scan:      # Roda em paralelo
    continue-on-error: true
  gitleaks-scan:     # Roda em paralelo
    continue-on-error: true
  supabase-check:    # Roda em paralelo
    continue-on-error: true
  deploy:
    needs: []        # NÃO depende dos checks — deploya sempre
  notify:
    needs: [trivy-scan, semgrep-scan, gitleaks-scan, supabase-check]
    if: always()     # Notifica SEMPRE — Slack com resumo
```

### Estratégia de escalação gradual

**Fase 1 (agora):** Non-blocking + alertas Slack → construir consciência. **Fase 2 (30 dias):** Adicionar comentários em PRs via Semgrep → educar desenvolvedores. **Fase 3 (60 dias):** Bloquear apenas findings CRITICAL (`exit-code: 1` + `severity: 'CRITICAL'`). **Fase 4 (90 dias):** Quality Gate completo com SonarCloud. Esta abordagem gradual evita resistência dos times e permite que a cultura de segurança se desenvolva organicamente.


---

## Parte 4: Governança que facilita em vez de bloquear

### O modelo de três tiers para apps vibe-coded

A separação mais eficaz é um **sistema de tiers baseado em risco**, não em tecnologia. Cada tier define domínio, pipeline, revisão e budget:

**Tier 1 — Sandbox/Experimentação Interna:** Apps internos, protótipos, dashboards sem dados sensíveis. Domínio `*.sandbox.internal.empresa.com`. Review 100% automatizado (security scan + lint). Auto-deploy em pipeline verde. SRE tem visibilidade via dashboard, sem aprovação necessária. Budget com cap de $50/mês por app.

**Tier 2 — Produção Interna:** Ferramentas internas com dados de negócio, workflows tocando bancos de produção. Domínio `*.tools.empresa.com`. Review automatizado + notificação assíncrona ao SRE. Auto-deploy com rollback obrigatório. SRE faz review semanal via digest. Budget de $200/mês com alertas em 80%.

**Tier 3 — Customer-Facing / Regulado:** Features voltadas a clientes, handling de PII, dados financeiros. Domínio `app.empresa.com`. Code review completo + security review + architecture review. Deploy requer aprovação SRE, canary deployment obrigatório. SLOs definidos, error budgets rastreados. Budget justificado pelo negócio e aprovado por SRE.

### Golden paths: o caminho certo é o mais fácil

O conceito de **Golden Path**, criado pelo Spotify e chamado de "Paved Road" pelo Netflix, é fundamental para governança de vibe coding. A ideia é simples: se o caminho seguro e governado for mais fácil que o alternativo, os times vão seguí-lo naturalmente. O golden path para apps Lovable deveria ser:

**1. Scaffold** → Um template Backstage cria automaticamente o repositório GitHub (a partir de um template aprovado), provisiona o projeto Supabase corporativo (com RLS pré-configurado), configura o workflow GitHub Actions (lint + test + security scan + deploy), e registra o serviço no catálogo.

**2. Develop** → O time usa Lovable para gerar código dentro do template. Um arquivo `AGENTS.md` define constraints arquiteturais. Regras ESLint pré-configuradas capturam problemas comuns de código AI. O Workspace Knowledge do Lovable reforça padrões.

**3. Validate** → Pipeline automatizado roda análise estática, scan de segurança, verificação do projeto Supabase, estimativa de custo e scan de dependências — tudo non-blocking com notificação.

**4. Deploy** → Baseado no tier: Tier 1 auto-deploya, Tier 2 auto-deploya + notifica SRE, Tier 3 requer aprovação.

**5. Observe** → App registrado automaticamente no service catalog com dashboard Grafana provisionado, tracking de error budget e custos.

O conceito emergente de **Spec-Driven Development** (reconhecido pelo Thoughtworks como uma das práticas mais importantes de 2025) complementa o golden path: antes de usar o Lovable, o time produz uma especificação estruturada que serve como blueprint para a geração de código AI. Isso reduz a aleatoriedade do vibe coding sem eliminar sua velocidade.

### Review leve com visibilidade total para SRE

O Google SRE Book é direto: "Engenheiros tendem a contornar processos que consideram muito onerosos ou com valor insuficiente." A revisão deve ser **automatizada e assíncrona**, nunca um gate manual para Tiers 1 e 2.

O modelo recomendado combina:

**Automated Production Readiness Review (PRR):** Security scan automatizado no CI/CD (bloqueia só para vulnerabilidades críticas), audit de dependências automatizado, estimativa de custo com threshold, verificação de RLS/Auth no Supabase, checagem de observabilidade (logging e metrics configurados). Tudo isso roda sem intervenção humana.

**Deployment Dashboard para SRE:** Visão real-time de todos os deploys em todos os times. Classificação por cores (verde/amarelo/vermelho) baseada em risco. Digest semanal auto-gerado. Detecção de anomalias em padrões de deploy. Tracking de custo por app/time/deploy. Ferramentas: Backstage + Grafana ou Harness IDP com scorecards.

**Policy-as-Code com OPA:** Definir políticas de deploy em Git, avaliar automaticamente. Exemplos: bloquear deploy sem tag de owner, exigir monitoring habilitado, alertar se custo estimado excede threshold do tier. O padrão "**proceed with justification**" é essencial: permitir saídas do golden path, mas com obrigações extras (logging adicional, security review focado, budgets mais apertados). Construir o override dentro da plataforma como flag documentado.

### Observabilidade centralizada para muitos apps AI

Para dezenas ou centenas de apps vibe-coded, a observabilidade precisa ser automatizada e padronizada. A recomendação do InfoWorld é pragmática: "Não invente um 'AI log'; use OpenTelemetry para que prompts, model IDs, tokens, latência e custo sejam rastreáveis nas mesmas ferramentas que SREs já operam."

O stack recomendado para AWS inclui **Grafana + Prometheus** (ou CloudWatch) para métricas, **Grafana Loki** (ou CloudWatch Logs) para logs centralizados, e **AWS Cost Explorer** com plugin Backstage para tracking de custo por app. Todo golden path template deve incluir observabilidade por padrão — config de logging, endpoints de métricas e health checks. O formato de log deve ser JSON estruturado com campos padronizados (`app_id`, `tier`, `owner`, `team`).


---

## Conclusão: o framework completo em ação

A chave para governar vibe coding em escala não é restringir, mas **tornar o caminho governado irresistivelmente fácil**. O framework proposto se sustenta em três decisões arquiteturais: o **GitHub como ponto de controle universal** (já que o Lovable não tem webhooks nativos, todo commit vira trigger), o **pipeline non-blocking com escalação gradual** (alertar primeiro, bloquear depois), e o **modelo de tiers** que calibra fricção com risco.

Para implementação, a sequência recomendada é: **Semanas 1-4**, estabelecer o service catalog (Backstage), criar o primeiro golden path template (React + Supabase + GitHub Actions) e definir os 3 tiers. **Semanas 5-8**, implementar o pipeline de segurança non-blocking, dashboard de visibilidade SRE e tracking de custos. **Semanas 9-12**, adicionar políticas OPA avançadas, scorecards de compliance e workflow de decommission automático para apps abandonados.

O insight menos óbvio desta pesquisa é que **o Lovable Enterprise já resolve boa parte do problema de governança no nível da plataforma** — com Workspace Knowledge para padrões, controles de publicação, SSO/SCIM e audit logs. Combinando esses controles nativos com o pipeline GitHub Actions descrito e a estratégia híbrida Amplify + Dokploy, o time de SRE ganha visibilidade completa sem se tornar bottleneck. A velocidade do vibe coding se preserva; os riscos se gerenciam via automação.