<!-- title: Feature Manager | url: https://outline.seazone.com.br/doc/feature-manager-udlBWEUIu7 | area: Tecnologia -->

# Feature Manager

# Experiments & Feature Flags System

Sistema centralizado para gerenciamento de Feature Flags e Testes A/B, utilizando uma arquitetura agnóstica a fornecedores (*Vendor Agnostic*) com **GrowthBook** e **PostHog**.

## Arquitetura

Para evitar *Vendor Lock-in* e garantir performance, utilizamos o **Facade Pattern** e **Hybrid Rendering**.

* **Single Source of Truth (**`**keys.ts**`**):** Todas as flags são declaradas centralmente para garantir tipagem e evitar "magic strings".
* **Zero Flicker:** O estado das flags é calculado no **Servidor** (SSR/RSC) e hidratado no **Cliente**, evitando que a interface "pisque" ou sofra *Hydration Mismatch*.
* **Abstração:** O código da aplicação não importa o SDK do GrowthBook ou PostHog diretamente. Tudo passa pelo `FeatureManager`.

## Estrutura de Arquivos

```javascript
container/
├── init-experiments-provider.ts # Client Component que hidrata os SDKs reais
├── index.ts                     # Exports públicos
├── server/                      # Utilitários de Server-Side Fetching
├── cookies/                     # Abstração de leitura de cookies (SSR vs RSC)
└── fetcher/                     # Lógica HTTP unificada para APIs externas

context/
├── index.tsx                    # Contexto React + Hook useFeature()
└── ...                          # Instância do StaticAdapter para renderização inicial

core/
├── interfaces/                  # Contratos (Interfaces) dos Adapters
├── keys/                        # Definição das chaves das flags (Single Source of Truth)
├── single/                      # Definições individuais de flags complexas
└── types/                       # Tipos globais (FeatureResult, ServerSnapshot)

manager/
└── feature-manager.ts           # Lógica de negócio (Overrides, Force Logic, Cache)

providers/
├── growthbook/                  # Adapter do GrowthBook
├── posthog/                     # Adapter do PostHog (Híbrido)
├── static-adapter/              # Adapter Read-Only para SSR/Initial Render
└── mock/                        # Adapter para Testes Unitários
```



---


## Guia de Uso

A inicialização dos experimentos é centralizada no componente `InitExperimentsProviderV2`. Ele atua como um **Smart Wrapper** que detecta o ambiente e hidrata os SDKs (PostHog e GrowthBook) com os dados trazidos do servidor, além de gerenciar cookies de identificação automaticamente.


### 1. Criando uma Nova Flag


1. Crie a flag no painel da ferramenta (ex: GrowthBook).
2. Adicione a chave no arquivo `core/keys/index.ts`.

```javascript
// core/keys/index.ts

export const FEATURE_FLAGS_KEYS = {
  // Simple flag mapping
  NEW_CHECKOUT_FLOW: { is: "ff_novo_checkout" },
  
  // Flag with forced value (ignores providers)
  MAINTENANCE_MODE: { 
    is: "ff_maintenance",
    _force_is: true, // Forces 'true' regardless of the provider
    _force_payload: { reason: "Database migration" }
  }
};
```

> **Nota:** O uso de `_force_is` e `_force_payload` é útil para *cleanups* ou *hotfixes* sem depender da API externa.



---


### 2. Consumindo no App Router (Next.js 13+)

No App Router, a busca de dados ocorre no servidor (`RootLayout`) e o estado é passado para o cliente.

#### Configuração no `layout.tsx`

```javascript
// app/layout.tsx
import { InitExperimentsProviderV2 } from "@/service/experiments/container/init-experiments-provider";
import { fetchFromServerRSC } from "@/service/experiments/container/server/fetcher/rsc";

export default async function RootLayout({ children }: { children: React.ReactNode }) {
  // Fetches flags from both PostHog and GrowthBook server-side
  const experiments = await fetchFromServerRSC();

  return (
    <html lang="pt-br">
      <body>
        <InitExperimentsProviderV2 experiments={experiments}>
          {children}
        </InitExperimentsProviderV2>
      </body>
    </html>
  );
}
```

#### Consumindo em Componentes

```javascript
"use client";
import { useFeature } from "@/service/experiments/context";

export const CheckoutButton = () => {
  const { is, payload } = useFeature("NEW_CHECKOUT_FLOW");

  if (!is) return <button>Checkout Clássico</button>;

  // Example of using payload if available
  const btnColor = payload?.color || 'blue';

  return <button style={{ backgroundColor: btnColor }}>Checkout Novo</button>;
};
```



---


## 3. Consumindo no Pages Router (Legado)

### A. Buscando Dados no Server-Side (`getServerSideProps`)

Cada página que precisa de features flags deve buscar os dados no servidor e repassá-los via props.

```javascript
import { fetchFromServerSSR } from "@/service/experiments/container/server/fetcher/ssr";

export const getServerSideProps = async (ctx: GetServerSidePropsContext) => {
  // Fetches flags from both providers (PostHog/GrowthBook)
  const experiments = await fetchFromServerSSR(ctx);

  return {
    props: {
      experiments, // Will be accessible in _app.tsx via pageProps
    },
  };
};
```

### B. Configuração Global (`_app.tsx`)

No `_app.tsx`, basta envolver a aplicação com o provider. Ele detectará automaticamente se `pageProps.experiments` existe e fará a hidratação correta.

```javascript
// pages/_app.tsx
import { InitExperimentsProviderV2 } from "@/service/experiments/container/init-experiments-provider";
import type { AppProps } from "next/app";

export default function App({ Component, pageProps }: AppProps) {
  return (
    <InitExperimentsProviderV2 
      experiments={pageProps.experiments}
      // Optional: Custom initialization config if needed
      init={{
        posthog: { is: true },
        growthbook: { is: true }
      }}
    >
      <Component {...pageProps} />
    </InitExperimentsProviderV2>
  );
}
```



---


## 4. Como o Provider Funciona (`InitExperimentsProviderV2`)

Este componente atua como um **Smart Wrapper**:


1. **Cenário Híbrido (SSR Data presente):** Se `experiments` for passado, ele inicializa os SDKs com o cache do servidor (Zero Latency) e salva o cookie de usuário.
2. **Cenário Client-Only:** Se `experiments` for `undefined` (navegação client-side ou página sem SSR), ele inicializa os SDKs no modo padrão (Client fetch).
3. **Cookies:** Gerencia automaticamente a persistência do `szn_user_id`.



---


## 5. Testes e Mocks

Para testes unitários, não mocke o `fetch` global. Utilize o `MockAdapter` fornecido.

```javascript
// __tests__/checkout.test.ts
import { Experiments } from "@/service/experiments";

test("deve renderizar o novo checkout", () => {
  // Forces the flag state for this test context
  Experiments.mock({
    NEW_CHECKOUT_FLOW: { is: true, variant: "A" }
  });

  // ... render component and assert
});
```