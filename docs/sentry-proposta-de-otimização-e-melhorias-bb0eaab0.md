<!-- title: [SENTRY] Proposta de Otimização e Melhorias | url: https://outline.seazone.com.br/doc/sentry-proposta-de-otimizacao-e-melhorias-e5BJKce269 | area: Tecnologia -->

# [SENTRY] Proposta de Otimização e Melhorias

## Visão geral:

Análise da configuração atual (`sentry.config.ts`, `vite.config.ts` e `UserContext`) com foco em adequação ao plano Free, eliminação de ruído e correção dos mapas de código.

## 1. Consumo de Cota e "Ruído" (Plano Free)


**🔴 O Problema** O `tracesSampleRate` não está configurado (padrão 100%) e a lista de `ignoreErrors` está vazia. Analisando os logs recentes, erros de conexão do cliente estão poluindo o painel e consumindo cota inutilmente.

**✅ A Sugestão** Blindar a inicialização no `Sentry.init`:


1. **Amostragem:** Fixar `tracesSampleRate: 0.1` (10%) em produção.
2. **Session Replay:** Ativar apenas no erro (`replaysOnErrorSampleRate: 1.0`).
3. **Filtros (Ignore List):** Adicionar os erros específicos que identificamos nos logs:
   * `Network Error`
   * `Request aborted` (Axios - cancelamento pelo usuário)
   * `Failed to fetch` (Bloqueadores/Offline)
   * `ResizeObserver loop limit exceeded`
   * `Authentication credentials were not provided` (Sessão expirada/401).
   * Filtrar erros 401, 404, 409


---


## 2. Identificação do Usuário


**🔴 O Problema** Os erros chegam como "Anônimos". Sem o ID ou Role (ex: Owner vs Admin), não conseguimos priorizar o impacto do bug.

**✅ A Sugestão** Injetar o rastreamento no `UserContext.tsx`, que já centraliza a autenticação.

* Informações que precisa enviar:
* Nome completo, main role, email, id

```javascript
// UserContext.tsx
useEffect(() => {
  if (userInformation) {
    Sentry.setUser({
      id: String(userInformation.user_id),
      email: user?.email,
      username: userInformation.nickname,
      segment: userInformation.main_role // Permite filtrar bugs só de "Owners"
    });
  } else {
    Sentry.setUser(null);
  }
}, [userInformation]);
```


---


### 3. Tratamento de Erros de Deploy (Chunk Load Error)


**🔴 O Problema** Nos logs, identificamos erros como `Failed to fetch dynamically imported module`. Isso ocorre após um novo deploy: o navegador do usuário tenta buscar um arquivo antigo (cacheado) que não existe mais no servidor, travando a aplicação (tela branca) durante a navegação.

**✅ A Sugestão** Implementar um **tratamento global** para esse erro específico.

* **Opção A (Transparente):** Forçar um reload automático (`window.location.reload()`) ao detectar esse erro. *Nota: Pode causar perda de dados de formulários não salvos, mas recupera a usabilidade imediatamente.*
* **Opção B (Conservadora):** Exibir um **Error Boundary** amigável com um botão "Atualizar Versão", informando ao usuário que uma atualização é necessária.


---

### 4. Monitoramento de Navegação (React Router)


**🔴 O Problema** Com a amostragem de performance ativada (`0.1`), precisamos garantir que os dados sejam úteis. Sem integração com o roteador, as transações ficam com nomes genéricos (ex: `/index.html`), impedindo a identificação de quais telas específicas (ex: `/parceiros/painel`) estão lentas.

**✅ A Sugestão** Como o projeto utiliza `react-router-dom` (v6), devemos configurar a integração oficial do Sentry:

* Envolver as rotas com `Sentry.withSentryReactRouterV6Routing`.
* Isso gera nomes de transações parametrizados (ex: `/parceiros/ganhos`) e melhora a rastreabilidade da jornada do usuário (breadcrumbs).


##  5.Estabilidade dos Source Maps (Debug)


**🔴 O Problema** A desminificação dos erros apresenta inconsistência.

* Em alguns casos (ex: Staging), o Sentry consegue mapear o arquivo original.
* Em outros (ex: Produção), variáveis aparecem minificadas (ex: `Cn.response`), dificultando a leitura. Isso ocorre porque a associação entre o "Build" e o "Erro" está sendo feita por inferência, e não por uma **Release** explícita, o que pode falhar dependendo do deploy.

**✅ A Sugestão** Garantir a sincronia perfeita configurando a **Release** (versão):


1. **No** `**vite.config.ts**`**:** Configurar a propriedade `release` no plugin do Sentry.
2. **No** `**sentry.config.ts**`**:** Adicionar a mesma propriedade `release` na inicialização.


\