<!-- title: Lógica de Cálculo e Escolha de Métricas | url: https://outline.seazone.com.br/doc/logica-de-calculo-e-escolha-de-metricas-m7tPOKa1gw | area: Tecnologia -->

# Lógica de Cálculo e Escolha de Métricas

## **1. Cálculo do Status Operacional**

O status é definido **em tempo real**, com base em **3 condições**:

**a) Está acima ou abaixo da meta?**

* Usa `faturamento_mes >= meta` .
* **Importante**: a meta é dinâmica (50% do percentil dos concorrentes), então pode mudar até o último dia.

**b) Tem dias disponíveis para agir?**

* Usa `ocupacao_ainda_disponivel` (dias futuros livres, já ajustado para a data de corte).
* Se `dias_disponiveis == 0` → **sem janela de ação**.

**c) Consegue bater a meta com o desempenho atual?**

* Calcula `potencial_realista = faturamento_mes + (to_listings * dias_disponiveis * media_preco_disponivel)`
* Se `potencial_realista >= meta` → **viável sem intervenção**.

**🧠 Regras de decisão:**

| CONDIÇÃO | STATUS |
|----|----|
| `faturamento < meta`e`dias_disponiveis == 0` | 🔴 Abaixo inviável |
| `faturamento < meta`e`dias_disponiveis > 0`e`potencial_realista >= meta` | 🟢 Abaixo viável |
| `faturamento < meta`e`dias_disponiveis > 0`e`potencial_realista < meta` | 🟠 Abaixo precisa esforço |
| `faturamento >= meta`e`dias_disponiveis == 0` | 🟡 Acima sem ação |
| `faturamento >= meta`e`dias_disponiveis > 0` | 🟡 Acima com risco |

> ✅ **Não existe "folga"**: mesmo acima da meta, se há dias disponíveis, há risco de queda.

## **🎯 2. Cálculo do Score de Prioridade**

O score é **simétrico** (trata desvios acima e abaixo da meta de forma equivalente) e usa **rank percentil** (não média) para evitar distorções.

**a) Para quem está abaixo da meta:**

`score = (falta_meta / meta) × (1 / dias_disponiveis) × (potencial_max - faturamento) × (1 / dias_necessarios)`

* **Quanto menor o esforço** (poucos dias necessários) e **maior o impacto** (falta_meta alta), **maior o score**.

**b) Para quem está acima da meta:**

`score = (1 - |atingimento_meta - 1|) × dias_disponiveis × media_preco_disponivel`

* **Quanto mais perto de 100%** e **mais dias disponíveis**, **maior o risco de cair** → maior prioridade.

**c) Normalização:**

* Usa **rank percentil**: o imóvel com maior score = 100, o menor = 0.
* Garante distribuição uniforme, mesmo com outliers.


---

## **📈 3. Justificativa dos Gráficos e Filtros**

**a) KPIs principais**

* **Total na Berlinda**: foco do dashboard.
* **Viáveis**: soma de Abaixo viável + Abaixo precisa de esforço→ mostra potencial de recuperação.
* **Acima com risco**: alerta para imóveis que podem sair da meta.
* **Prioritários**: apenas Crítico/Alta → direciona esforço.

**b) Gráfico de Status Operacional**

* **Por quê?** Mostra a **composição qualitativa** do portfólio.
* **Filtro?** Usa os mesmos filtros globais (carteira, estado etc.) para análise segmentada.

**c) Scatter Plot: Viabilidade × Prioridade**

* **Eixo Y**: `score_normalizado` → prioridade de ação.
* **Eixo X**: variável selecionável (`dias_disponiveis`, `falta_meta`, etc.) → permite explorar diferentes dimensões.
* **Tamanho**: `abs(falta_meta)` → destaca impacto financeiro.
* **Cor**: status operacional → separa quem precisa de ação de quem não precisa.

**d) Tabela Operacional**

* **Colunas escolhidas**: métricas-chave para decisão (meta, faturamento, TO, preço, dias).
* **Filtros locais**: permite isolar **Crítico + Abaixo viável**, por exemplo.
* **Ordenação**: por prioridade descendente → os mais urgentes ficam no topo.


---

## **🛠️ 4. Como ajustar a lógica**

Se quiser modificar:

* **Limiares de score**: altere as faixas em `classificar_prioridade()`.
* **Regras de status**: edite a função `definir_status()`.
* **Fórmula do score**: ajuste `calcular_score()` (ex: dar mais peso ao preço ou ao TO).

> Qualquer mudança deve ser testada com casos reais (ex: imóvel que falta 1 dia para bater meta deve ter score alto).

\n