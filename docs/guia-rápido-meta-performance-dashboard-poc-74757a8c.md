<!-- title: Guia Rápido: Meta Performance Dashboard (POC) | url: https://outline.seazone.com.br/doc/guia-rapido-meta-performance-dashboard-poc-5dAFJUvzK4 | area: Tecnologia -->

# Guia Rápido: Meta Performance Dashboard (POC)

*Versão: 1.0*

*Atualizado: 01-10-2025*

## **Objetivo**:

 Ajudar o RM a **priorizar ações diárias** com base em dados atualizados, focando nos imóveis com **maior potencial de impacto** no fechamento da meta mensal.

## **🔍 O que é a "Berlinda"?**


1. ### **Definição**: Imóveis com atingimento da meta entre 80% e 110%.
2. ***Por que focar nela?***\nSão os imóveis que:
   * Estão **perto da meta** (baixo esforço para fechar),
   * Têm **maior margem de manobra** (ainda têm dias disponíveis),
   * Representam o **melhor custo-benefício operacional**.\n

***✅ Não é um status fixo — muda diariamente conforme o faturamento e o desempenho dos concorrentes.***\n  

## **📊 Status Operacional (5 categorias)**

| STATUS | O QUE SIGNIFICA | AÇÕES RECOMENDADAS |
|----|----|----|
| **🟢 Abaixo viável** | Está**abaixo da meta**, mas**tem dias disponíveis**e, com o desempenho atual,**consegue bater a meta**. | **Monitorar**— geralmente não precisa de ajuste. |
| **🟠 Abaixo precisa esforço** | Está**abaixo da meta**, tem dias disponíveis, mas**não vai bater a meta com o desempenho atual**. | **Intervir**— ajustar preço, campanha ou TO. |
| **🔴 Abaixo inviável** | Está**abaixo da meta**e**não tem mais dias disponíveis**. | **Não agir**— só aprender para o próximo mês. |
| **🟡 Acima com risco** | Está**na meta ou acima**, mas**ainda tem dias disponíveis**→ pode**cair se concorrentes seguirem faturando**. | **Proteger**— manter desempenho, evitar cancelamentos. |
| **🟡 Acima sem ação** | Já**bateu a meta**e**não tem mais dias disponíveis**. | **Só monitorar**— não há janela de ação. |

> 💡 **Importante**: A meta é **dinâmica** — muda conforme os concorrentes faturam. Um imóvel pode estar "acima" hoje e "abaixo" amanhã.


## **🎯 Score de Prioridade**

* **O que é?** Um número de **0 a 100** que indica **quão crítico é agir agora**.
* **Como é calculado?**
  * Para quem está **abaixo da meta**: considera **falta de meta**, **dias necessários**, **dias disponíveis** e **potencial de recuperação**.
  * Para quem está **acima da meta**: considera **quão perto está de 100%** + **dias disponíveis** (quanto mais perto e mais dias, maior o risco de cair).
* **Faixas**:
  * **Crítico (80–100)**: Alto impacto + baixo esforço (ex: falta 1 dia para bater meta).
  * **Alta (50–79)**: Viável, mas exige atenção.
  * **Média/Baixa (0–49)**: Pouco impacto ou inviável.

> ✅ O score usa **rank percentil** (não média), então **não é distorcido por outliers**.


## **📅 Atualização dos Dados**

* Os dados são atualizados **toda segunda-feira**.
* A data exibida no rodapé é a **data de geração do arquivo**, **não a do acesso**.
* Exemplo: "Dados atualizados em: **25/09/2025**" → análise do mês de **setembro**, com corte em 25/09.


## **🧭 Próximos Passos (Roteiro da POC → MVP)**


1. **Validação da lógica atual** (esta fase):
   * Testar se os status e o score ajudam na tomada de decisão.
   * Coletar feedbacks reais de uso.
2. **Expansão do funil** (Q4):
   * Aplicar lógica semelhante aos grupos **"Atenção"** e **"Crítico"**.
   * Criar recomendações automáticas (ex: "reduzir preço em X%").
3. **MVP (próximo trimestre)**:
   * Integração com sistemas de pricing e campanhas.
   * Alertas proativos (ex: "imóvel X está prestes a sair da Berlinda").
   * Histórico de performance e comparação mês a mês.


\