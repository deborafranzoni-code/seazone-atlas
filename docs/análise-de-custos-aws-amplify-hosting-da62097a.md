<!-- title: Análise de Custos — AWS Amplify Hosting | url: https://outline.seazone.com.br/doc/analise-de-custos-aws-amplify-hosting-qgB6bDwed1 | area: Tecnologia -->

# Análise de Custos — AWS Amplify Hosting

# Análise de Custos — AWS Amplify Hosting

> Análise completa de custos do AWS Amplify Hosting: tabela de preços, simulações por perfil de aplicação, comparativo com alternativas e recomendações.


---

## 1. Modelo de Cobrança

O AWS Amplify Hosting utiliza modelo **pay-as-you-go** — sem custos fixos, sem contratos mínimos. Você paga apenas pelo que consome, com free tier generoso para aplicações de baixo tráfego.


---

## 2. Tabela de Preços Completa

### Hospedagem (Static Sites / SPA)

| Recurso | Free Tier (mensal) | Preço excedente |
|----|----|----|
| **Build minutes** (Standard: 8 GB / 4 vCPUs) | 1.000 min | **$0,01 / min** |
| **Build minutes** (Large: 16 GB / 8 vCPUs) | — | **$0,025 / min** |
| **Build minutes** (XLarge: 72 GB / 36 vCPUs) | — | **$0,10 / min** |
| **Data Transfer (CDN)** | 15 GB | **$0,15 / GB** |
| **Storage** | 5 GB | **$0,023 / GB/mês** |

### SSR (Server-Side Rendering — Next.js, Nuxt, etc.)

| Recurso | Free Tier (mensal) | Preço excedente |
|----|----|----|
| **Requests** | 500.000 | **$0,30 / 1M requests** |
| **Compute (GB-hour)** | 100 GB-hours | **$0,20 / GB-hour** |

### Opcionais

| Recurso | Custo |
|----|----|
| **WAF (Web Application Firewall)** | $15/mês por app + custos WAF associados |
| **Domínio customizado + SSL** | Gratuito (incluso) |
| **Previews por PR** | Mesmo custo de build (consome build minutes) |


---

## 3. Simulações de Custo por Perfil

### Caso 1: Landing Page / Blog Estático

> Site estático com poucas páginas, baixo tráfego, atualizações esporádicas.

| Parâmetro | Valor |
|----|----|
| Deploys/mês | 5 |
| Tempo de build | 1 min |
| Tamanho do site | 50 MB |
| Visitantes/mês | 2.000 |
| Data transfer | \~1 GB |

| Item | Cálculo | Custo |
|----|----|----|
| Build | 5 min (free tier: 1.000 min) | $0,00 |
| Transfer | 1 GB (free tier: 15 GB) | $0,00 |
| Storage | 50 MB (free tier: 5 GB) | $0,00 |
| **Total** |    | **$0,00/mês** |


---

### Caso 2: Dashboard Interno / SPA (React, Vue, Angular)

> Aplicação SPA usada internamente por uma equipe de 20-50 pessoas.

| Parâmetro | Valor |
|----|----|
| Deploys/mês | 30 (1/dia, CI/CD automático) |
| Tempo de build | 2 min |
| Tamanho do bundle | 1-3 MB |
| Usuários ativos | 30 |
| Data transfer | \~3 GB |

| Item | Cálculo | Custo |
|----|----|----|
| Build | 60 min (free tier) | $0,00 |
| Transfer | 3 GB (free tier) | $0,00 |
| Storage | 3 MB (free tier) | $0,00 |
| **Total** |    | **$0,00/mês** |

> Nosso caso com o **sz-cloud-cost** se encaixa aqui. Custo zero.


---

### Caso 3: SaaS B2B com SSR (Next.js)

> Plataforma SaaS com server-side rendering, 500 clientes ativos, área autenticada.

| Parâmetro | Valor |
|----|----|
| Deploys/mês | 60 (2/dia) |
| Tempo de build | 5 min |
| Visitantes/mês | 50.000 |
| Page views/mês | 300.000 |
| SSR requests/mês | 300.000 |
| SSR compute | 50 GB-hours |
| Data transfer | \~40 GB |

| Item | Cálculo | Custo |
|----|----|----|
| Build | 300 min (free tier) | $0,00 |
| Transfer | 40 GB - 15 GB free = 25 GB × $0,15 | **$3,75** |
| Storage | \~500 MB (free tier) | $0,00 |
| SSR Requests | 300k (free tier: 500k) | $0,00 |
| SSR Compute | 50 GB-h (free tier: 100 GB-h) | $0,00 |
| **Total** |    | **\~$3,75/mês** |


---

### Caso 4: E-commerce de Médio Porte (Next.js SSR)

> Loja virtual com catálogo grande, SEO via SSR, tráfego constante.

| Parâmetro | Valor |
|----|----|
| Deploys/mês | 100 (múltiplos por dia) |
| Tempo de build | 8 min (Large instance) |
| Visitantes/mês | 200.000 |
| Page views/mês | 1.500.000 |
| SSR requests/mês | 1.500.000 |
| SSR compute | 400 GB-hours |
| Data transfer | \~150 GB |

| Item | Cálculo | Custo |
|----|----|----|
| Build (Large) | 800 min × $0,025 | **$20,00** |
| Transfer | 150 GB - 15 free = 135 GB × $0,15 | **$20,25** |
| Storage | \~2 GB (free tier) | $0,00 |
| SSR Requests | 1.5M - 500k free = 1M × $0,30/1M | **$0,30** |
| SSR Compute | 400 - 100 free = 300 GB-h × $0,20 | **$60,00** |
| **Total** |    | **\~$100,55/mês** |


---

### Caso 5: Portal de Alto Tráfego (SPA + CDN Heavy)

> Aplicação SPA com muitos assets, 1M+ visitantes/mês, alta transferência de dados.

| Parâmetro | Valor |
|----|----|
| Deploys/mês | 150 |
| Tempo de build | 3 min |
| Visitantes/mês | 1.000.000 |
| Data transfer | \~500 GB |

| Item | Cálculo | Custo |
|----|----|----|
| Build | 450 min (free tier) | $0,00 |
| Transfer | 500 GB - 15 free = 485 GB × $0,15 | **$72,75** |
| Storage | \~5 GB (free tier) | $0,00 |
| **Total** |    | **\~$72,75/mês** |


---

## 4. Resumo Visual das Simulações

| Cenário | Tipo | Visitantes/mês | Custo/mês |
|----|----|----|----|
| Landing page / blog | Static | 2.000 | **$0** |
| Dashboard interno (SPA) | Static | 500 | **$0** |
| SaaS B2B | SSR (Next.js) | 50.000 | **\~$4** |
| E-commerce médio | SSR (Next.js) | 200.000 | **\~$101** |
| Portal alto tráfego | SPA | 1.000.000 | **\~$73** |


---

## 5. Comparativo com Alternativas

### Custo Mensal por Plataforma

| Cenário | AWS Amplify | Vercel (Pro) | Netlify (Pro) | S3 + CloudFront |
|----|----|----|----|----|
| **Landing page** (2k visits) | $0 | $20¹ | $19¹ | \~$0,50 |
| **Dashboard SPA** (30 users) | $0 | $20¹ | $19¹ | \~$0,50 |
| **SaaS B2B SSR** (50k visits) | \~$4 | $20 + overages¹ | $19 + overages¹ | N/A² |
| **E-commerce SSR** (200k visits) | \~$101 | \~$60-150³ | \~$57-99³ | N/A² |
| **Alto tráfego SPA** (1M visits) | \~$73 | $20 + \~$55⁴ | $19 + \~$55⁴ | \~$45 |

> ¹ Vercel e Netlify cobram plano fixo por membro do time ($20/seat e $19/seat respectivamente), mesmo com baixo uso. ² S3+CloudFront não suporta SSR nativamente — requer Lambda@Edge, o que complica e encarece. ³ Custos de function execution e bandwidth overages variam significativamente. ⁴ Bandwidth overage após free tier do plano.

### Comparativo Qualitativo

| Critério | Amplify | Vercel | Netlify | S3 + CloudFront |
|----|----|----|----|----|
| **Custo mínimo** | $0 (pay-as-you-go) | $20/mês/seat | $19/mês/seat | \~$0,50/mês |
| **Previsibilidade** | Variável | Fixo + overages | Fixo + overages | Variável |
| **Setup** | Simples | Muito simples | Muito simples | Complexo |
| **SSR support** | Next.js, Nuxt, etc. | Next.js (nativo) | Next.js, Astro | Requer Lambda@Edge |
| **Preview por PR** | Sim | Sim | Sim | Manual |
| **Domínio + SSL** | Grátis | Grátis | Grátis | Grátis (ACM) |
| **WAF integrado** | Sim ($15/mês) | Enterprise only | Enterprise only | Sim (AWS WAF) |
| **Lock-in** | AWS | Vercel | Netlify | AWS |
| **Ideal para** | Equipes AWS | Startups, DX-first | Jamstack teams | Controle total |


---

## 6. Quando Escolher AWS Amplify

**Amplify é a melhor opção quando:**

* A organização já está no ecossistema AWS
* A aplicação é uma SPA ou site estático com tráfego baixo/médio (free tier cobre)
* Você precisa de integração nativa com serviços AWS (Cognito, S3, AppSync, etc.)
* O time é pequeno — sem custo por seat como Vercel/Netlify
* Você precisa de WAF integrado

**Considere alternativas quando:**

* O foco é DX (Developer Experience) acima de tudo → **Vercel**
* A equipe é Jamstack-first com edge functions → **Netlify**
* O tráfego é muito alto e o app é 100% estático → **S3 + CloudFront** (mais barato)
* Você precisa de SSR avançado com edge rendering → **Vercel** (melhor suporte Next.js)


---

## 7. Dicas para Otimizar Custos no Amplify


1. **Cache headers agressivos** — assets imutáveis com `max-age=31536000` reduzem data transfer
2. **Builds condicionais** — usar `amplify.yml` com `preBuild` para skipar builds sem mudanças reais
3. **Instância de build Standard** — suficiente para 95% dos projetos ($0,01/min vs $0,025/min da Large)
4. **Monitorar Usage** — Amplify Console → Monitoring → Usage para acompanhar consumo vs free tier
5. **Comprimir assets** — Vite/webpack com gzip/brotli reduz transfer em \~70%
6. **Evitar rebuilds desnecessários** — branch filters no Amplify para não buildar pushes em branches irrelevantes


---

## 8. Caso Específico: sz-cloud-cost (Seazone)

O **sz-cloud-cost** (dashboard de custos cloud) se encaixa no **Caso 2 (Dashboard Interno)**:

* SPA React + Vite (\~1.3 MB bundle)
* \~30 usuários internos (@seazone.com.br)
* Dados servidos pelo Supabase (não pelo Amplify)
* **Custo estimado: $0,00/mês** (100% coberto pelo free tier)
* PR de deploy: [seazone-tech/sz-cloud-cost#1](https://github.com/seazone-tech/sz-cloud-cost/pull/1)


---

## Referências

* [AWS Amplify Pricing — Página oficial](https://aws.amazon.com/amplify/pricing/)
* [AWS Pricing Calculator](https://calculator.aws/)
* [AWS Amplify vs Vercel — Comparativo 2026](https://www.agilesoftlabs.com/blog/2026/01/aws-amplify-vs-vercel-2026-complete)
* [Vercel vs Netlify vs AWS Amplify — Pricing](https://www.getmonetizely.com/articles/vercel-vs-netlify-vs-aws-amplify-which-jamstack-hosting-pricing-model-is-right-for-you)
* [Better Stack — Vercel vs Netlify vs Amplify](https://betterstack.com/community/guides/scaling-nodejs/vercel-vs-netlify-vs-aws-amplify/)


---

*Relatório gerado em 19/03/2026 — Seazone SRE*