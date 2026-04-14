<!-- title: Documentação de Migração para Redux - Página de Parceiros | url: https://outline.seazone.com.br/doc/documentacao-de-migracao-para-redux-pagina-de-parceiros-p3db5r0e5o | area: Tecnologia -->

# Documentação de Migração para Redux - Página de Parceiros

Esta documentação detalha o plano técnico para migrar o gerenciamento de estado da página de Parceiros de **Context API** para **Redux** (utilizando Redux Toolkit).

## 1. Objetivo

Substituir o `PartnerContext` por uma arquitetura baseada em Redux para melhorar a previsibilidade do estado, facilitar a depuração e preparar a aplicação para escalabilidade.

## 2. Dependências Necessárias

Será necessário instalar as seguintes bibliotecas:

* **@reduxjs/toolkit**: Biblioteca oficial e recomendada para Redux moderno.
* **react-redux**: Bindings oficiais do React para Redux.

`npm install @reduxjs/toolkit react-redux `

## 3. Estrutura de Pastas Proposta

Recomendamos criar uma estrutura organizada dentro de `src/store` ou manter próximo ao módulo de parceiros se for um Redux modular.

```bash
src/
  store/
    index.ts          # Configuração da Store principal
    hooks.ts          # Hooks tipados (useAppDispatch, useAppSelector)
    modules/
      partners/       # Módulo específico de Parceiros
        index.ts      # Exportação dos reducers
        slice.ts      # Definição do Slice (State + Reducers)
        thunks.ts     # Ações assíncronas (API calls)
        selectors.ts  # Seletores para buscar dados da store
        types.ts      # Tipagem do estado
```


## 4. Mapeamento do Estado (Context vs Redux)

O `PartnerContext` atual gerencia diversos domínios de dados. No Redux, isso será organizado em um ou mais *slices*.

### Estado Inicial (`partnersSlice`)

```typescript
interface PartnersState {
  // Filtros
  filters: {
    page: number;
    pageSize: number;
    activeStatus: IIndicationsStatus | undefined;
    activePage: "locacao" | "spot" | "terreno" | "construtora";
    year?: number;
    month?: number;
    // ... outros filtros
  };
  // Dados de Indicações (Cache)
  indications: {
    propertys: IPropertyIndication[];
    spots: IInvestmentIndication[];
    allotments: IAllotmentIndication[];
    builders: IBuilderIndication[];
    loading: boolean;
    error: string | null;
  };
  // Resumos e Contadores
  summary: {
    balance: IPartnersBalanceSummary | null;
    indications: IPartnersIndicationsSummary | null;
    resume: IPartnersResume | undefined;
    counts: IndicationCounts;
  };
  // UI e Auxiliares
  ui: {
    showBurgerMenu: boolean;
    successScreen: boolean;
    loading: {
      main: boolean;
      aux: boolean;
    };
    hideElements: IHideElements;
    welcome: { is: boolean };
  };
  // Dados Bancários e Financeiros
  financial: {
    banks: RequiredBank[];
    bankDetails: GetPartnersBankDetailsBase[];
    withdrawRequests: IPartinersFinancialWithdrawBase[];
    loading: boolean;
  };
}
```


## 5. Migração de Funcionalidades

### 5.1. Ações Síncronas (Reducers)

Funções que apenas alteram estado local serão convertidas em *reducers* dentro do `createSlice`.

* `setFilters` -> `setFilters`
* `setShowBurgerMenu` -> `toggleBurgerMenu`
* `setSuccessScreen` -> `setSuccessScreen`
* `setHideElements` -> `setHideElements`

### 5.2. Ações Assíncronas (Integração com TanStack Query)

> ⚠️ **ATENÇÃO:** Como haverá uso de TanStack Query em paralelo, **não utilizaremos Thunks** para chamadas de API.

O fluxo será:


1. **Redux:** Armazena os filtros (ex: `filters.page`, `filters.status`).
2. **Componente:** Lê os filtros do Redux via `useSelector`.
3. **TanStack Query:** Recebe os filtros como dependência e busca os dados automaticamente.

**Exemplo de Integração:**

```typescript
// Componente
const filters = useAppSelector((state) => state.partners.filters);
// A query roda automaticamente sempre que 'filters' mudar no Redux
const { data } = useQuery({
  queryKey: ["indications", filters],
  queryFn: () => getIndications(filters),
});
```

*Isso simplifica drasticamente o lado do Redux, pois removemos toda a complexidade de Thunks, Loading States e Tratamento de Erro da Store.*

## 6. Plano de Implementação (Passo a Passo)

### Fase 1: Configuração (Setup)

*  Instalar dependências.
*  Configurar a `store` global em `src/store/index.ts`.
*  Envolver a aplicação (ou a rota de parceiros) com o `<Provider store={store}>`.

### Fase 2: Criação do Slice de Parceiros

*  Criar `src/store/modules/partners/slice.ts`.
*  Definir o `initialState` baseado no Contexto atual.
*  Implementar os reducers básicos (filtros, UI).

### Fase 3: Migração de Chamadas de API (Adaptação para TanStack Query)

*  Não criar Thunks.
*  Garantir que os seletores do Redux estejam prontos para serem consumidos pelos hooks do TanStack Query.
*  Ajudar na integração: O componente deve pegar o filtro do Redux e passar para o hook do TanStack Query.

### Fase 4: Conexão com Componentes

*  Substituir `usePartners()` por `useAppSelector` e `useAppDispatch` nos componentes.
  * Ex: `const { filters } = usePartners()` vira `const filters = useAppSelector(state => state.partners.filters)`.
  * Ex: `setFilters(newFilters)` vira `dispatch(setFilters(newFilters))`.
* Remover o `PartnersContextProvider` do arquivo `Partners.tsx`.

## 7. Divisão de Tarefas no JIRA

Sugestão de estrutura para as subtarefas (Sub-tasks) dentro da História no JIRA:


1. **\[Setup\] Configuração Inicial do Redux**
   * Instalar dependências e configurar a Store.
   * Configurar o Provider na aplicação.
2. **\[Migração\] Estado de UI e Filtros (Client State)**
   * Migrar estados visuais (filtros, modais, menus) para o Redux.
   * Conectar componentes de UI ao Redux.
3. **\[Integração\] Conexão com TanStack Query (Server State)**
   * *Importante:* O Redux **NÃO** deve gerenciar o cache ou chamadas de API.
   * O Redux deve armazenar apenas os **parâmetros** para as queries.
   * Os componentes usarão `useAppSelector` para pegar os filtros e `useQuery` para buscar os dados.
4. **\[Cleanup\] Remoção do Context API**
   * Remover o `PartnerContext` antigo após a migração completa.

## 8. Estratégia de Trabalho em Paralelo (Redux vs TanStack Query)

Para evitar conflitos de merge e retrabalho entre os dois desenvolvedores, seguiremos este protocolo:

### 8.1. Fase de Construção Isolada (Sem conflitos)

* **Dev Redux:** Trabalha exclusivamente na pasta `src/store`. Cria a Store, Slices e Seletores. **Não altera componentes ainda.**
* **Dev TanStack:** Trabalha exclusivamente na criação de Custom Hooks (ex: `src/hooks/useIndicationsQuery`). **Não altera componentes ainda.**

### 8.2. O "Contrato" de Interface

Antes de começar, ambos devem concordar com o formato do estado dos filtros no Redux.

**Contrato Sugerido:**

```typescript
interface FilterState {
  page: number;
  pageSize: number;
  status: string | undefined;
  type: 'locacao' | 'spot' | 'terreno' | 'construtora';
  // ... outros
}
```

### 8.3. Fase de Integração (Migração de Componentes)

Para minimizar conflitos nos arquivos `.tsx`:

* **Dev Redux (Foco em Inputs/Controles):**
  * Prioriza arquivos de **escrita**: `Filters.tsx`, `Header.tsx`, `EditBOSidebar.tsx`.
  * Substitui `setFilters` do Context por `dispatch(setFilters)`.
* **Dev TanStack (Foco em Outputs/Visualização):**
  * Prioriza arquivos de **leitura**: `Grid.tsx`, `Dashboard.tsx`, `Summary.tsx`.
  * Substitui `indications` do Context pelo hook `useIndicationsQuery`.

### 8.4. A Morte do Contexto

O arquivo `PartnerContext.tsx` só deve ser deletado quando **ambas** as partes terminarem. Sugiro que o **Dev Redux** fique responsável por essa limpeza final (Task de Cleanup).

## 9. Benefícios Esperados


1. **DevTools:** Poder visualizar o histórico de ações e estado com Redux DevTools.
2. **Performance:** Componentes só renderizam se o pedaço específico do estado que eles observam mudar (seletores granulares).
3. **Separação de Responsabilidades:**
   * *Redux:* Gerencia o estado da aplicação (O que o usuário selecionou/filtrou).
   * *TanStack Query:* Gerencia o estado do servidor (Dados da API, Cache, Loading).