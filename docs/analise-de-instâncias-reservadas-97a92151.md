<!-- title: Analise de instâncias reservadas | url: https://outline.seazone.com.br/doc/analise-de-instancias-reservadas-RJp1A7jk3k | area: Tecnologia -->

# Analise de instâncias reservadas

Análise feita com auxilio de IA a partir dessa planilha : 

[https://docs.google.com/spreadsheets/d/1HbO4S8Qc5wQvkrirQGsHgBbvvm1fOZo-txTJIiXs9Pc/edit?gid=0#gid=0](https://docs.google.com/spreadsheets/d/1HbO4S8Qc5wQvkrirQGsHgBbvvm1fOZo-txTJIiXs9Pc/edit?gid=0#gid=0)

padrão identificado nos dados mostra que a AWS penaliza o custo de oportunidade de capital: a diferença entre o "No Upfront" (Sem Adiantamento) e o "All Upfront" (Totalmente Adiantado) é marginal (\~2-3%), o que não justifica a imobilização de capital.

Abaixo, as recomendações técnicas por categoria de instância:


---

### 1. Instâncias de Micro/Pequeno Porte (t2.micro, t3a.large, c6g.large)

**Recomendação:** Reserved 1 ano - Mensal (Sem Adiantamento)

* **Racional Técnico:** Para instâncias de baixo custo absoluto, o esforço administrativo de gerir contratos de 3 anos supera a economia. O modelo de 1 ano mensal oferece o equilíbrio ideal entre desconto (\~37%) e flexibilidade anual.
* **Prós:** Rápido ajuste de arquitetura caso a carga de trabalho mude; impacto nulo no fluxo de caixa.
* **Contras:** Custo por GB de RAM/CPU levemente superior ao modelo de 3 anos.

### 2. Instâncias de Uso Geral e Memória (m6g.large até r6g.xlarge)

**Recomendação:** Reserved 3 anos - Mensal (Sem Adiantamento)

* **Racional Técnico:** Estas são instâncias "core" de infraestrutura (bancos de dados e backends estáveis). Como o adiantamento de 3 anos é **USD 0,00** e o desconto salta para **\~56%**, esta é a eficiência máxima de custo por performance (Price/Perf).
* **Exemplo r6g.xlarge:** Redução de **USD 234,77** para **USD 101,40** (Mensal).
* **Prós:** Menor custo fixo mensal possível sem desembolso inicial; proteção contra reajustes de preços.
* **Contras:** *Vendor Lock-in* de longa duração; se a tecnologia Graviton evoluir para uma família m7g, você está preso à m6g por 3 anos.

### 3. Instâncias de Alta Performance (m6g.2xlarge até r6g.4xlarge)

**Recomendação:** Reserved 1 ano - Mensal (Sem Adiantamento)

* **Racional Técnico:** Em máquinas de grande porte, o risco de ociosidade é caro. Comprometer-se por 3 anos com uma r6g.4xlarge (USD 939/mês no On-demand) pode gerar um "custo fantasma" alto se a aplicação for otimizada e passar a exigir menos recursos.
* **Ponto Crítico:** O adiantamento "Parcial" de 3 anos para uma r6g.4xlarge é de **USD 5.147,00**. Este capital investido no seu *core business* provavelmente renderá mais do que a economia extra de USD 30/mês que o adiantamento oferece sobre o plano mensal.
* **Prós:** Redução imediata de custos de escala sem comprometer o OPEX de curto prazo.
* **Contras:** Exige monitoramento constante de utilização (Right-sizing) para não pagar por capacidade ociosa reservada.


---

### Tabela Comparativa de Estratégia (Base: m6g.xlarge)

| **Modelo** | **Custo Mensal** | **Upfront** | **Eficiência de Caixa** | **Risco de Lock-in** |
|----|----|----|----|----|
| **On-demand** | USD 178,70 | $0 | Baixa (Caro) | Zero |
| **1 ano Mensal** | **USD 112,57** | **$0** | **Alta (Ideal)** | Baixo (12 meses) |
| **3 anos Mensal** | **USD 77,23** | **$0** | **Máxima** | Alto (36 meses) |
| **1 ano Total** | USD 105,08 | $1.261 | Baixa (ROI ruim) | Baixo |


---

### Resumo das Recomendações Técnicas:


1. **Regra de Ouro:** **Esqueça o "All Upfront" e "Partial Upfront".** A base de dados mostra que o benefício marginal de adiantar USD 1.000+ é de apenas \~USD 5 a USD 7 mensais. Financeiramente, é mais inteligente manter o dinheiro em caixa ou investir em desenvolvimento.
2. **Ação Imediata:** Converta instâncias de banco de dados (r6g) estáveis para **3 anos Mensal (No Upfront)**. A economia de 56% é imbatível.
3. **Ação para Workers/APIs:** Converta instâncias m6g/c6g para **1 ano Mensal (No Upfront)**. Isso mantém a agilidade para migrar de família de instância no próximo ciclo de renovação.