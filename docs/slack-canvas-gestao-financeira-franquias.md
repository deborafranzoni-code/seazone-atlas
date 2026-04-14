<!-- title: [Slack] Processo de Gestão Financeira das Franquias | url: https://seazone-fund.slack.com/docs/TDLTVAWQ6/F09JDHM3CV8 | area: Administrativo Financeiro -->

# Processo de Gestão Financeira das Franquias

Setor Responsável: Franquias Backoffice

## Objetivo

Garantir o acompanhamento e controle financeiro das franquias, assegurando que os pagamentos das taxas de franquia sejam realizados corretamente e que o faturamento esteja em conformidade com a topologia prevista.

## Escopo

Incluso:
- Monitoramento de taxas de franquia em aberto
- Acompanhamento da cadência de pagamentos
- Análise de clusters de faturamento em comparação à topologia
- Geração de encaminhamentos para áreas responsáveis (operações, financeiro)

Fora do escopo: cobrança direta de franqueados e negociações comerciais.

## Fluxo do Processo

### 1. Identificar franquias ruins/péssimas com taxa em aberto
- Clicar na barra de classificação de score no BI de Gestão de Franquias
- Verificar na tabela quais franquias estão nesta situação
- Solicitar análise ao Analista de Operações via canal de suporte

### 2. Identificar franquias com taxa em aberto, comissão e sem pagamento
- Acessar aba "Cadência de pagamento Taxa de Franquias"
- Verificar tabela "Ausência de abatimentos em meses com comissão"
- Se identificada situação irregular: contatar o financeiro para entendimento ou ajuste no repasse

### 3. Identificar franquias com cluster de faturamento abaixo do esperado

Tabela de clusters esperados por topologia:

| Topologia | Cluster Esperado | Fat. Médio Mín. | Fat. Médio Máx. |
|---|---|---|---|
| Micro Franquia | Baixo | R$ 0 | R$ 20.000 |
| Franquia Pequena | Médio-Baixo | R$ 20.000 | R$ 40.000 |
| Franquia Média | Médio | R$ 40.000 | R$ 60.000 |
| Franquia Grande | Médio-Alto | R$ 60.000 | R$ 100.000 |
| Franquia Master | Alto | R$ 100.000 | Sem limite |

Análises para franquias fora da relação:
- Média de imóveis e queda de imóveis
- Tamanho dos imóveis (nº quartos) vs outras franquias do mesmo cluster
- Faturamento por imóvel vs outras franquias
- Taxa de limpeza vs outras franquias

## KPIs

1. Aba Taxa de Franquias: taxa total, entradas, abatimentos, descontos, qtd em aberto
2. Aba Cadência de pagamento: tempo médio de quitação
3. Aba Cluster de faturamento: cruzamento cluster vs topologia

## Prazos e SLA

- Franquias com taxa em aberto + comissão sem pagamento: mensalmente, todo dia 10
- Franquias ruins/péssimas com taxa em aberto: mensalmente, todo dia 16
- Franquias com cluster abaixo do esperado: ao rodar análise de resultado
