<!-- title: Testes A/B na Wallet com Posthog | url: https://outline.seazone.com.br/doc/testes-ab-na-wallet-com-posthog-rNNcFh5hGm | area: Tecnologia -->

# Testes A/B na Wallet com Posthog

* Configurações recomendadas:
* 👍 Persist flag across authentication steps
* Fluxo padrão: control
* Fluxo novo: test

# Funções

* getExperiment
* getFeatureFlag
* useFeatureFlag
* useExperiment

## Funcionamento

* bootstrapData - puxa feature flags diretamente do servidor para amenizar erros de flickering com FFs não carregando imediatamente no client
* PosthogProvider - Inicializa o posthog
* Para servidor: getExperiment e getFeatureFlag
* Para client: useFeatureFlag ou useExperiment

## QA

* Armazenamento Local → ph_phc_4DRZLT7olFNxEdm… → $feature_flag_details → ff_do_experimento

## Página Inicial: Home vs Financeiro

* Caso A: Exibir fluxo padrão
  * Carrega a página padrão da home (contém Meus Imóveis Ativos, Próximas Reservas)
  * Exibe  
  * Não permite a utilização de searchParams na home. (year, month, property_id)
  * \