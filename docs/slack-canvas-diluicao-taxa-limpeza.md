<!-- title: [Slack] Diluição da Taxa de Limpeza no Valor das Diárias | url: https://seazone-fund.slack.com/docs/TDLTVAWQ6/F08CX10TWKB | area: Administrativo Financeiro -->

# Diluição da Taxa de Limpeza no Valor das Diárias

## Objetivo

Teste para avaliar melhoria no modelo de precificação, diluindo a taxa de limpeza no valor das diárias em vez de cobrar separadamente. Abordagem já utilizada por diferentes players do mercado.

## Lógica do Processo

O sistema opera com linhas tarifárias por período de estadia (1 a 28 noites). A taxa de limpeza é dividida pelo número de noites e somada à diária base.

Exemplo com taxa de limpeza R$300 e diária base R$500:
- 1 noite: R$300/1 = +R$300 → diária R$800
- 2 noites: R$300/2 = +R$150 → diária R$650
- 3 noites: R$300/3 = +R$100 → diária R$600
- 7 noites: R$300/7 = +R$42,86 → diária R$542,86
- 28 noites: R$300/28 = +R$10,71 → diária R$510,71

Importante: o valor diluído diminui progressivamente com mais noites. A diluição afeta mais estadias curtas.

## Cenários Especiais

### Estadias intermediárias (ex: 15 noites usando Tarifa 07)
Modelo antigo: 15 × R$500 + R$300 = R$7.800
Modelo novo: 15 × R$542,86 = R$8.142,90 (+R$342,90)

### Impacto dos descontos (10% em 3 noites)
Modelo antigo: 3 × R$400 - 10% + R$300 (sem desconto) = R$1.380
Modelo novo: 3 × R$500 - 10% = R$1.350 (cliente paga menos com desconto aplicado sobre total)

## Como Operacionalizar

1. Verificar taxa de limpeza do imóvel na Stays (Financeiro → Configuração geral de preço → Cleaning Fee)
2. Configurar na planilha de Setup do Sirius (aba "Taxa de Limpeza": código + valor)
3. Enviar parâmetros (aba "Grupos" → botão Executar)
4. Aguardar atualização dos preços (reenviar ou esperar gapper a cada 3h)
5. Verificar na Stays se a diluição aplicou corretamente (Financeiro → Configuração das diárias)
6. Zerar a taxa de limpeza na Stays APENAS após confirmar a correta diluição

## Pontos de Atenção

- O fechamento financeiro deve discriminar claramente valores de diária vs taxa de limpeza no repasse ao anfitrião
- Acompanhar as primeiras reservas após a mudança
- Confirmar se a diluição está funcionando em todas as faixas tarifárias
