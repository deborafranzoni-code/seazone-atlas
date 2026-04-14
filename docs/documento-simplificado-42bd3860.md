<!-- title: Documento Simplificado | url: https://outline.seazone.com.br/doc/documento-simplificado-9TqZ5NSzzQ | area: Tecnologia -->

# Documento Simplificado

**1. Problema**

* **Dificuldade de investigação rápida**: Quando o KPI do MAPE dos últimos 15 dias sofre alterações bruscas (ex: de 0.25 para 0.35), não temos uma forma ágil de identificar a causa raiz.
* **Processo manual ineficiente**:
  * Requer queries complexas no Athena/S3.
  * Análise individual de IDs impactados.
  * Dificuldade em distinguir entre:
    * Erros de dados (ex: scraping incorreto).
    * Outliers naturais do MAPE (ex: imóveis com MAPE > 1000%).
    * Problemas estruturais (ex: falhas na detecção de bloqueios).
* **Impacto**: Horas de investigação, atraso em ações corretivas e risco de decisões baseadas em dados não validados.

**2. Solução Proposta**

* **Ferramenta "Auditoria do MAPE"**: Sistema simples para comparar dados entre duas datas e identificar **o que mudou** e **por quê**.
* **Princípios**:
  * Foco em velocidade (investigação em minutos, não horas).
  * Direcionamento automático à causa raiz.
  * Interface amigável para não-técnicos .



3. Funcionalidades Chave (MVP)

| **Funcionalidade** | **Descrição** |
|----|----|
| **Comparação entre Datas** | Selecionar 2 períodos (ex: 15 dias antes vs. agora) e visualizar:- Variação do MAPE global e por tipo (faturamento, ocupação).- Lista de imóveis com maior impacto (top 10). |
| **Drill-down por ID** | Para cada imóvel crítico:- Gráfico de comparação: real vs. previsto.- Flag de problemas: `n_inf` , bloqueios incorretos, outliers. |
| **Classificação de Causas** | Sistema automático de categorização:- **Erros de dados**: Variação > 100% + `n_inf` alto- **Outliers**: MAPE individual > 500% sem padrão recorrente.- **Problemas estruturais**: Queda no MAPE com bloqueios corretos. |
| **Alertas Inteligentes** | Notificações no Slack quando:- MAPE ultrapassa 30%.- 3+ imóveis com MAPE > 1000% no mesmo dia. |

**4. Benefícios Esperados**

* **Redução de 80% no tempo de investigação** (de horas para minutos).
* **Identificação precisa da causa raiz** .
* **Prevenção de decisões equivocadas** baseadas em dados não validados.


\