<!-- title: Smart Testings SAPRON | url: https://outline.seazone.com.br/doc/smart-testings-sapron-TcKTSDqCpw | area: Tecnologia -->

# Smart Testings SAPRON

**Assunto:** Implementação de automação de testes para garantia de qualidade e redução de débitos técnicos.

## 1. Objetivo

O SAPRON é um ecossistema complexo com múltiplos perfis e fluxos (Admin, Host, Owner, Partner). Atualmente, o processo de refatoração e lançamento de novas features enfrenta o gargalo da **regressão manual**, que é lenta e suscetível a falhas humanas.

Esta proposta visa implementar uma **Arquitetura de Testes E2E Inteligente (Smart Testing)** que automatiza a validação de jornadas críticas, garantindo que o sistema não "quebre" após atualizações, sem onerar o tempo de desenvolvimento ou os custos de infraestrutura.

## 2. Arquitetura Técnica

Para garantir manutenibilidade, os testes serão construídos em três camadas:


1. **Page Objects Pattern:** Encapsula a interface. Se a UI mudar (MUI/React), atualizamos um único arquivo de mapeamento, e não todos os testes.
2. **Business Logic Layer:** Serviços reutilizáveis que executam ações de negócio (ex: `createNewIndication()`).
3. **Smart Mapping:** Inteligência que analisa o `git diff` e executa apenas os testes impactados pelas mudanças de código.


```
cypress/
├── e2e/business-flows/          # Testes por jornada de negócio
│   ├── partners/                # Fluxo de parceiros
│   ├── owner/                   # Fluxo de proprietários
│   ├── host/                    # Fluxo de anfitriões
│   ├── financial/               # Fluxo financeiro
│   └── onboarding/              # Fluxo de cadastro
│
├── support/
│   ├── page-objects/            # Encapsula elementos da UI
│   ├── business-logic/          # Regras de negócio reutilizáveis
│   ├── helpers/                 # Utilitários
│   └── fixtures/                # Dados de teste
```

Domínios mapeados:

* ✅ **Partners**: Indicação, ganhos, saques
* ✅ **Owner**: Gestão de imóveis, extrato financeiro
* ✅ **Host**: Controle de propriedades, despesas
* ✅ **Financial**: Fechamento financeiro, conciliação
* ✅ **Onboarding**: Cadastro de imóveis
* ✅ **Damages**: Relato e resolução de danos

## 3. Onde e Como os Testes Serão Realizados?

### 3.1. Integração no Fluxo de Pull Request (PR)

Os testes não serão manuais. Eles farão parte do **Pipeline de CI/CD (GitHub Actions)**.

* **Gatilho:** Sempre que uma PR for aberta ou atualizada.
* **Bloqueio de Merge:** Se um teste de fluxo crítico falhar, o GitHub impede o merge automaticamente até que o erro seja corrigido.
* **Feedback:** O desenvolvedor recebe um relatório na própria PR com vídeos e capturas de tela do erro.

### 3.2. Estratégia de Banco de Dados e Isolamento

Para garantir que os testes sejam confiáveis e não "sujem" dados reais, adotaremos a estratégia de **Banco de Dados de Teste com Seeding**:

* **Ambiente:** Utilizaremos um banco de dados espelho de staging (`sapron_test`).
* **Data Seeding:** Antes de cada execução, um script de "Seed" limpa e popula o banco com dados controlados (usuários teste, propriedades fictícias e tokens de autenticação).
* **Isolamento:** Cada suite de teste utiliza contas únicas para evitar colisões quando múltiplos desenvolvedores abrem PRs simultaneamente.

## 4. Diferencial: Smart Test Selection (ROI de Tempo)

Diferente de testes E2E tradicionais que levam horas, o **Smart Testing** mapeia dependências:

| **Se o desenvolvedor alterar...** | **O Smart Map executa...** | **Tempo Estimado** |
|----|----|----|
| Módulo de Parceiros (`/partners`) | Apenas o fluxo de indicações e ganhos. | \~3 min |
| Módulo Financeiro (`/financial`) | Regressão de fechamento e repasses. | \~5 min |
| Componentes Globais (`/common`) | Suite completa de regressão (Safety Fallback). | \~15 min |

## 5. Métricas de Sucesso 

A eficácia do projeto será medida trimestralmente através de:


1. **Redução no Tempo de QA:** Meta de diminuir em **70%** o esforço manual de regressão por release.
2. **Taxa de Bug Leakage:** Redução de bugs críticos em produção (identificação de falhas ainda em ambiente de PR).
3. **MTTR (Mean Time to Repair):** Diminuir o tempo de correção de bugs, já que o Playwright/Cypress entrega o vídeo exato do erro para o dev.
4. **Confiabilidade de Deploy:** Aumento da frequência de deploys sem incidentes de rollback.


### **Estrutura de Diretórios**

```
cypress/
├── e2e/
│   ├── business-flows/
│   │   ├── partners/
│   │   │   ├── indication-flow.cy.ts
│   │   │   ├── earnings-flow.cy.ts
│   │   │   └── cashout-flow.cy.ts
│   │   ├── owner/
│   │   │   ├── property-management.cy.ts
│   │   │   └── financial-extract.cy.ts
│   │   ├── host/
│   │   ├── financial/
│   │   ├── onboarding/
│   │   └── damages/
│   └── tests/ (legado)
│
├── support/
│   ├── page-objects/
│   │   ├── common/
│   │   │   ├── BasePage.ts
│   │   │   ├── LoginPage.ts
│   │   │   └── NavigationPage.ts
│   │   ├── partners/
│   │   ├── owner/
│   │   └── index.ts
│   │
│   ├── business-logic/
│   │   ├── partners/
│   │   │   ├── IndicationService.ts
│   │   │   ├── EarningsService.ts
│   │   │   └── CashoutService.ts
│   │   ├── auth/
│   │   └── index.ts
│   │
│   ├── helpers/
│   │   ├── api-helpers.ts
│   │   ├── data-generators.ts
│   │   └── date-helpers.ts
│   │
│   ├── fixtures/
│   │   ├── users/
│   │   └── business-data/
│   │
│   └── commands/
│       ├── auth-commands.ts
│       └── api-commands.ts
│
└── smart-map.js
```


\