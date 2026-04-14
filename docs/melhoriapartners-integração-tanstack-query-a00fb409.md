<!-- title: [Melhoria/Partners] Integração TanStack Query | url: https://outline.seazone.com.br/doc/melhoriapartners-integracao-tanstack-query-cbZd4S17Ot | area: Tecnologia -->

# [Melhoria/Partners] Integração TanStack Query

Documentação: 

* [TanStack Query v3 Docs](https://tanstack.com/query/v3/docs/react/overview)
* [React Query DevTools](https://tanstack.com/query/v3/docs/react/devtools)


---

### Configuração Atual:

O projeto já possui o React Query v3:

```json
"dependencies": {
  "react-query": "^3.34.16"
}
```

O QueryClient já esta configurado globalmente: 

**Arquivo:** `/app/src/utils/QueryClient/QueryClient.ts`

```typescript

import { QueryClient } from 'react-query';

export const queryClient = new QueryClient();
```

**Arquivo:** `/app/src/App.tsx`

```typescript

import { QueryClientProvider } from 'react-query';
import { queryClient } from '@/utils/QueryClient/QueryClient';

// ...
<QueryClientProvider client={queryClient}>
  {/* App content */}
</QueryClientProvider>
```



---

### O Problema: 

A arquitetura atual da página de Parceiros apresenta alto acoplamento e complexidade desnecessária, dificultando a manutenção e degradando a experiência do usuário.

* **Contexto Monolítico:** O arquivo `PartnerContext.tsx` possui mais de 900 linhas, misturando regras de negócio, estado de UI, chamadas diretas ao Axios e transformações de dados manuais.
* **Gerenciamento Manual de Estado:** Uso excessivo de `useState` e `useEffect` para controlar loading, erros e paginação.
* **Ausência de Cache:** Requisições são refeitas desnecessariamente ao navegar entre abas, sem estratégia de *stale-while-revalidate*.
* **Inconsistência de Tipos:** Conflitos entre `UserInformation` e `UserMeProps`, gerando código frágil.

### 1. Estrutura Atual de Parceiros

**Arquivos principais:**

* `/app/src/pages/Partners/Partners.tsx` - Componente principal
* `/app/src/context/Partners/Partner/PartnerContext.tsx` - Context atual
* `/app/src/services/Partner/request.ts` - Funções de API
* `/app/src/services/Partner/types.ts` - Tipos TypeScript

**Principais endpoints utilizados:**

```typescript
// Resumo do parceiro

GET /partners/resume/

// Indicações por tipo

GET /partners/v2/indications/property/
GET /partners/v2/indications/allotment/
GET /partners/v2/indications/investment/
GET /partners/v2/indications/building/

// Sumários

GET /partners/indications-property/summary

GET /partners/indications-allotment/summary

GET /partners/indications-investment/summary

GET /partners/indications-building/summary

// Balanço

GET /partners/balance/summary
```


### Criar Hooks Customizados com React Query

* Cada tipo de dado que precisa buscar terá um hook

```javascript
/app/src/hooks/usePartners/
├── index.ts                          # Exports centralizados
├── queries/                          # Leitura de dados (GET)
│   ├── usePartnerResume.ts           
│   ├── useBalanceSummary.ts          
│   ├── useIndicationsSummary.ts      
│   ├── usePropertyIndications.ts     
│   ├── useAllotmentIndications.ts    
│   ├── useInvestmentIndications.ts   
│   ├── useBuilderIndications.ts      
│   └── useBankDetails.ts             
├── mutations/                        # Escrita de dados (POST/PUT/DELETE)
│   ├── useCreatePropertyIndication.ts
│   └── useCreateWithdrawRequest.ts
└── utils/
    ├── queryKeys.ts                  # Factory de chaves de cache
    └── transformers.ts               # Tratamento de dados puro
```

### EXEMPLO:

**Arquivo:** `/app/src/hooks/usePartners/usePartnerResume.ts`

```typescript

import { useQuery } from 'react-query';
import { getPartnersResume } from '@/services/Partner/Resume/request';
import { IPartnersResume } from '@/pages/Partners/types';

/**
 * Hook para buscar o resumo do parceiro
 * 
 * @returns Query com dados do resumo, loading e error states
 */
export function usePartnerResume() {
  return useQuery<IPartnersResume, Error>(
    ['partner', 'resume'], // Query key
    getPartnersResume,     // Query function
    {
    //5 minutos para sair da tela e voltar e ele não fará uma nova chamada à API
      staleTime: 1000 * 60 * 5, // 5 minutos 
    //os dados ficam na memória por 10 minutos antes de serem deletados  
      cacheTime: 1000 * 60 * 10,
    //2 requisições automaticas antes de disparar o erro final  
      retry: 2,
    //desativa o comportamento padrão de recarregar os dados toda vez que o usuário clica na janela do navegador 
      refetchOnWindowFocus: false,
    }
  );
}
```

**componente:**

```typescript

import { usePartnerResume } from '@/hooks/usePartners/usePartnerResume';

function PartnerPanel() {
  const { 
    data: resume, 
    isLoading, 
    isError, 
    error,
    refetch 
  } = usePartnerResume();

  if (isLoading) {
    return <Loading />;
  }

  if (isError) {
    return <ErrorMessage error={error} />;
  }

  return (
    <div>
      <h1>Bem-vindo, {resume?.partner_name}</h1>
      <p>Total de indicações: {resume?.total_indications}</p>
    </div>
  );
}
```


### Adaptação da Camada de Service (`request.ts`)

**Mudança Crítica:** Para o React Query funcionar corretamente, as funções de requisição devem ser "limpas".

### As 3 Regras de Ouro:


1. **Retorno:** Retornar apenas os dados (`response.data`), não o objeto Axios completo.
2. **Erros:** **NUNCA** usar `try/catch`. O erro deve ser propagado para o React Query tratar.
3. **Tipagem:** Retornar `Promise<TipoDoDado>`.

#### ❌ Antes 

```javascript
// Engole o erro e retorna objeto sujo
export async function getPartnersResume() {
  try {
    const response = await api.get('/partners/resume/');
    return response; 
  } catch (error) {
    console.log(error);
    return null;
  }
}
```

#### ✅ Depois (Padrão React Query)

```javascript
import { IPartnersResume } from './types';

// O erro explode aqui e é capturado pelo hook useQuery
export async function getPartnersResume(): Promise<IPartnersResume> {
  const { data } = await api.get<IPartnersResume>('/partners/resume/');
  return data; 
}
```


### Tratamento Global de Erros

Configurar no `QueryClient` para evitar repetição de Toasts em todo componente.

```javascript
// /app/src/utils/QueryClient/QueryClient.ts
export const queryClient = new QueryClient({
  queryCache: new QueryCache({
    onError: (error: any) => {
      // Captura erros de GET (401, 404, 500)
      toast.error(`Erro ao carregar: ${error.message}`);
    },
  }),
  mutationCache: new MutationCache({
    onError: (error: any) => {
      // Captura erros de POST/PUT
      if (error?.response?.status !== 422) { 
         toast.error(`Erro na operação: ${error.message}`);
      }
    },
  }),
});
```


## ✅ Melhores Práticas

### 1. Organização de Query Keys

Usar uma estrutura hierárquica consistente:

```typescript
// ❌ Evite
['indications']
['property-indications']
['getPropertyIndications']

// ✅ Recomendado
['partner', 'indications', 'property']
['partner', 'indications', 'property', { page: 1, status: 'approved' }]
['partner', 'summary', 'property']
['partner', 'balance']
```

### 2. Configuração de Cache

```typescript
// Dados que mudam raramente (configurações, listas estáticas)
staleTime: 1000 * 60 * 30, // 30 minutos

cacheTime: 1000 * 60 * 60, // 1 hora

// Dados que mudam frequentemente (indicações, balanço)
staleTime: 1000 * 60 * 2,  // 2 minutos

cacheTime: 1000 * 60 * 10, // 10 minutos

// Dados em tempo real

staleTime: 0,
cacheTime: 0,
refetchInterval: 1000 * 30, // 30 segundos
```



---

# Plano de Execução 


1. ###  Fundação e Tipagem (Preparação)

*Objetivo: Preparar a base do código e tipos sem alterar a interface visual.*

* ~~\[ X \] **Task 1.1:** Refatorar e unificar tipos~~ `~~UserInformation~~` ~~e~~ `~~UserMeProps~~` ~~em~~ `~~/services/User/types.ts~~`~~.~~
* ~~\[ X \] **Task 1.2: Atualizar**~~ `**~~request.ts~~**`**~~:~~** ~~Remover~~ `~~try/catch~~` ~~e retornar~~ `~~data~~` ~~direto (aplicar novo padrão).~~
* ~~\[ X \] **Task 1.3:** Criar estrutura de pastas (~~`~~/hooks/usePartners/~~`~~) e arquivo~~ `~~queryKeys.ts~~`~~.~~
* ~~\[ X \] **Task 1.4:** Configurar~~ `~~QueryClient~~` ~~com tratamento global de erros (Toast).~~

  \


2. ### Consultas Simples (Leitura)

*Objetivo: Migrar dados de visualização rápida (Dashboard e Resumos).*

* **~~Task 2.1:~~** ~~Implementar hook~~ `~~usePartnerResume~~` ~~(Derivar dados do UserContext).~~
* **~~Task 2.2:~~** ~~Implementar hook~~ `~~useBalanceSummary~~` ~~(Balanço financeiro).~~
* **~~Task 2.3:~~** ~~Implementar hook~~ `~~useIndicationsSummary~~` ~~(Queries paralelas para os 4 tipos).~~
* **~~Task 2.4:~~** ~~Atualizar componente~~ `~~PartnerPanel~~` ~~para usar esses hooks e remover lógica antiga do Context~~.



3. ### ~~Listagens Complexas (Paginação)~~

*~~Objetivo: Migrar as tabelas de dados principais.~~*

* **~~Task 3.1:~~** ~~Implementar~~ `~~usePropertyIndications~~` ~~(Locação) com paginação e filtros.~~
* **~~Task 3.2:~~** ~~Implementar hooks para:~~
  * `~~useAllotmentIndications~~` ~~(Terrenos).~~
  * `~~useInvestmentIndications~~` ~~(Investimentos).~~
  * `~~useBuilderIndications~~` ~~(Construtoras).~~
* **~~Task 3.3:~~** ~~Refatorar componentes de tabela para consumir props~~ `~~isLoading~~`~~,~~ `~~isPreviousData~~` ~~e dados dos novos hooks.~~



4. ### Mutações (Escrita)

*Objetivo: Migrar formulários e ações do usuário.*

* **Task 4.1:** Implementar mutations para criação de indicações:
  * `useCreatePropertyIndication`
  * `useCreateAllotmentIndication`
  * `useCreateInvestmentIndication`
  * `useCreateBuilderIndication`
* **Task 4.3:** Configurar invalidação automática de cache (`onSuccess`) para atualizar as listas e saldos sem refresh.
* **Task 4.4:** Substituir chamadas diretas do Axios nos formulários pelos novos hooks.

  \

### 5.  Limpeza e Desacoplamento

*Objetivo: Remover código morto e finalizar a arquitetura.*

* **Task 5.1:** Remover todas as funções de fetch, `useEffect` de dados e estados manuais (`loading`, `data`) do `PartnerContext`.


\