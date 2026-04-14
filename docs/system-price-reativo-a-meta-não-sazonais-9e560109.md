<!-- title: System Price reativo a meta (Não Sazonais) | url: https://outline.seazone.com.br/doc/system-price-reativo-a-meta-nao-sazonais-FrgSBjqC0M | area: Tecnologia -->

# System Price reativo a meta (Não Sazonais)

**Autor:** Lucas Abel ( DPM )

**Versão:** 1.0 


## **1. Visão Geral e Objetivos**

Esta é a primeira entrega do pacote de melhorias de inteligência do System Price. O objetivo é criar um **mecanismo de feedback interno** baseado na performance individual de cada imóvel.

Diferente da lógica atual que foca em "O que o concorrente está cobrando?", aqui focamos em "Como este imóvel está performando vs. a Meta de Faturamento?". O sistema deve corrigir preços automaticamente para tentar zerar o número de imóveis em status "Crítico" e "Berlinda".

## **2. Requisitos Funcionais (Lógica de Negócio)**

### **2.1. Cálculo de Status de Performance**

O sistema deve replicar (ou consumir) a lógica de classificação do BI **Meta Performance** para definir o status do imóvel no mês atual:

* **OK:** Acima da meta.
* **Berlinda:** Um pouco abaixo ou um pouco acima da meta (na briga).
* **Atenção:** Abaixo da meta.
* **Crítico:** Muito abaixo da meta.
* **Superestimado:** Muito acima da meta (faturamento > 2x a meta).

### **2.2. Regras de Ajuste de Preço (Saída)**

O ajuste deve ocorrer na **saída** (final do cálculo), somando ou subtraindo um valor/percentual do preço sugerido pela Matriz de Parâmetros.

* **OK:** Não alterar o preço. (Preço Final = Preço Matriz).
* **Superestimado:** O imóvel esta performando acima, podemos aumentar o preço para 'segurar'.
* **Berlinda:** O imóvel precisa de um "empurrão" para bater a meta. Aplicar **Desconto Moderado**.
* **Atenção / Crítico:** O imóvel está performando mal. Aplicar **Desconto Agressivo** (maior para Crítico).

### **2.3. Tratamento de Exceções (Dias Bloqueados)**

Antes de aplicar qualquer desconto (Berlinda/Crítico), o sistema deve verificar a **Disponibilidade**:

* Se o imóvel tem **muitos dias bloqueados** no período restante do mês, ele pode estar "Crítico" por falta de oferta, não por preço.
* *Regra:* Se o potencial de ocupação for muito baixo devido a bloqueios, **não aplicar desconto** (ou aplicar desconto zero), pois baixar o preço não gerará vendas.

### **2.4. Frequência**

* A regra deve rodar diariamente (junto com o processamento normal do System Price / Tem praça), permitindo correções rápidas de rumo.

## **3. Escopo de Dados**

* **Mercado:** Mercados Não Sazonais (Goiânia, SP, RS, PR - para validação).
* **Dados Necessários:**
  * Faturamento Atual do Imóvel (Acumulado mês).
  * Meta de Faturamento do Imóvel.
  * Preço Sugerido pela Matriz (Base).
  * Quantidade de Dias Bloqueados / Disponíveis no mês.

## **4. Critérios de Sucesso**

* Imóveis classificados como "Crítico" devem ter preços reduzidos automaticamente.
* Imóveis "Superestimados" devem ter preços aumentados.
* O impacto deve ser visível na curva de faturamento após alguns dias de rodada.